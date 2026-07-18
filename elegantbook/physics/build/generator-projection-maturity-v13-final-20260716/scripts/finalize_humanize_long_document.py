#!/usr/bin/env python3
"""Validate and assemble long-document humanization units without touching sources."""

from __future__ import annotations

import argparse
import csv
import difflib
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
import unicodedata
from collections import Counter, defaultdict
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Sequence


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import check_humanize_invariants as invariants  # noqa: E402
import prepare_humanize_long_document as preparer  # noqa: E402
import validate_humanize_output as output_validator  # noqa: E402
import build_humanize_voice_profile as voice_profiles  # noqa: E402
import build_humanize_action_profile as action_profiles  # noqa: E402


PLACEHOLDER_RE = re.compile(r"\[\[PROTECTED:(?P<id>[^:\]]+):(?P<hash>[0-9a-f]{12})\]\]")
HAN_RE = re.compile(r"[\u3400-\u9fff]")
TEX_COMMAND_TOKEN_RE = re.compile(r"\\[A-Za-z@]+\*?|\\[^A-Za-z\s]")
TERMINAL_STATUSES = {
    "DONE",
    "NO_CHANGE",
    "SKIPPED_PROTECTED",
    "SKIPPED_GARBLED",
    "UNRESOLVED",
    "CHANGED_AFTER_SNAPSHOT",
}

BOUNDARY_TEMPLATE_CUE_RE = re.compile(
    r"^(?:本文|本节|本研究|这里|这一|首先|其次|最后|综上|因此|由此|需要|值得|关键|更直接|换言|在此基础|进一步)"
)
PURE_TEX_STRUCTURE_LINE_RE = re.compile(
    r"^\s*\\(?:begin|end|part|chapter|section|subsection|subsubsection|paragraph|subparagraph|label|input|include)\b.*$"
)
ZERO_WIDTH_RE = re.compile(r"[\u200b-\u200f\u2060\ufeff]")
HAN_GAP_RE = re.compile(r"(?<=[\u3400-\u9fff])[ \t\u00a0\u3000]+(?=[\u3400-\u9fff])")


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


@contextmanager
def _run_lock(run_dir: Path):
    """Serialize finalization for one run directory across threads/processes."""
    lock_path = run_dir / ".finalize.lock"
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    handle = lock_path.open("a+b")
    try:
        handle.seek(0, os.SEEK_END)
        if handle.tell() == 0:
            handle.write(b"0")
            handle.flush()
        handle.seek(0)
        if os.name == "nt":
            import msvcrt

            # LK_NBLCK has a deterministic retry loop; LK_LOCK gives up after
            # a platform-defined number of attempts under sustained contention.
            while True:
                try:
                    msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
                    break
                except OSError:
                    time.sleep(0.05)
        else:
            import fcntl

            fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        yield
    finally:
        try:
            handle.seek(0)
            if os.name == "nt":
                import msvcrt

                msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                import fcntl

                fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
        finally:
            handle.close()


def _verify_prepare_integrity(run_dir: Path) -> None:
    manifest_path = run_dir / "prepare_integrity.json"
    if not manifest_path.is_file():
        raise ValueError("missing prepare_integrity.json; refuse unverifiable finalize")
    manifest = _load_json(manifest_path)
    if not isinstance(manifest, dict) or manifest.get("schema_version") != 1:
        raise ValueError("invalid prepare_integrity.json")
    artifacts = manifest.get("artifacts")
    if not isinstance(artifacts, list) or not artifacts:
        raise ValueError("prepare_integrity.json has no artifacts")
    expected_paths = {str(item.get("path", "")) for item in artifacts if isinstance(item, dict)}
    actual_paths = {
        str(path.relative_to(run_dir)).replace("\\", "/")
        for path in [
            run_dir / "snapshot.json",
            run_dir / "file_manifest.csv",
            run_dir / "protected_spans.jsonl",
            run_dir / "units.jsonl",
            run_dir / "coverage_ledger.csv",
            run_dir / "run_metadata.json",
            run_dir / "voice_profile.json",
            *[
                path
                for path in (
                    run_dir / "voice_sample_manifest.json",
                    run_dir / "voice_sample_spec.json",
                )
                if path.is_file()
            ],
            *sorted((run_dir / "chunks").glob("*.json"), key=lambda item: item.name.casefold()),
        ]
        if path.is_file()
    }
    if expected_paths != actual_paths:
        raise ValueError("prepare artifact set changed after snapshot")
    for item in artifacts:
        if not isinstance(item, dict) or not isinstance(item.get("path"), str):
            raise ValueError("invalid prepare integrity artifact")
        path = run_dir / item["path"]
        if not path.is_file() or sha256(path.read_bytes()) != item.get("sha256"):
            raise ValueError(f"prepare artifact changed after snapshot: {item['path']}")


def _reject_duplicate_json_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _parse_json_strict(text: str, label: str) -> Any:
    try:
        value = json.loads(
            text,
            object_pairs_hook=_reject_duplicate_json_keys,
            parse_constant=lambda token: (_ for _ in ()).throw(
                ValueError(f"invalid number {token}")
            ),
        )
        voice_profiles._reject_floats_and_depth(value)
        return value
    except (json.JSONDecodeError, ValueError) as error:
        raise ValueError(f"invalid strict JSON {label}: {error}") from error


def _load_json(path: Path) -> Any:
    # PowerShell's UTF-8 output commonly includes a BOM; rewrite bundles are
    # user-facing interchange files and should accept both UTF-8 variants.
    try:
        raw = path.read_bytes()
        text = raw.decode("utf-8-sig", errors="strict")
    except (OSError, UnicodeDecodeError) as error:
        raise ValueError(f"cannot read strict JSON {path}: {error}") from error
    return _parse_json_strict(text, str(path))


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            if line.strip():
                try:
                    rows.append(_parse_json_strict(line, f"{path}:{line_number}"))
                except ValueError as error:
                    raise ValueError(f"{path}:{line_number}: {error}") from error
    return rows


def _load_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def _write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _write_csv(path: Path, rows: Sequence[dict[str, Any]], fields: Sequence[str]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


VOICE_UNIT_FIELDS = (
    "voice_profile_id",
    "voice_profile_revision",
    "voice_profile_confidence",
    "voice_profile_kind",
    "voice_profile_source",
    "voice_profile_binding_scene",
    "voice_profile_sha256",
    "voice_default_disclosure",
)


def _validate_frozen_voice_evidence(
    profile: dict[str, Any],
    manifest_path: Path,
    spec_path: Path,
) -> dict[str, Any]:
    manifest = preparer.voice_profile_validator.validate_manifest_object(
        voice_profiles._load_json_strict(manifest_path)
    )
    preparer.voice_profile_validator.validate_profile_manifest_binding(profile, manifest)
    spec = voice_profiles._load_json_strict(spec_path)
    voice_profiles._validate_spec(spec)
    spec_sha256 = voice_profiles._sha256_bytes(
        voice_profiles._canonical_json_bytes(spec)
    )
    if spec_sha256 != manifest["sample_spec_sha256"]:
        raise ValueError("frozen voice sample spec does not match manifest")
    return manifest


def _validate_voice_profile_binding(
    run_dir: Path,
    metadata: dict[str, Any],
    units: Sequence[dict[str, Any]],
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Validate the frozen Profile independently of the integrity manifest."""
    profile_path = run_dir / "voice_profile.json"
    if not profile_path.is_file():
        raise ValueError("missing voice_profile.json")
    profile = voice_profiles.load_and_validate_profile(profile_path)
    if profile.get("validation_status") != "PASS":
        raise ValueError("frozen voice Profile status is not PASS")
    binding = metadata.get("voice_binding")
    if not isinstance(binding, dict):
        raise ValueError("run_metadata.json has no voice_binding")
    expected_binding = {
        "voice_profile_id": profile.get("profile_id"),
        "voice_profile_revision": profile.get("revision"),
        "voice_profile_confidence": profile.get("confidence"),
        "voice_profile_kind": profile.get("profile_kind"),
        "voice_profile_binding_scene": profile.get("binding_scene"),
        "voice_profile_sha256": profile.get("profile_sha256"),
        "voice_default_disclosure": bool(profile.get("defaults", {}).get("disclosure_required", False)),
    }
    for key, expected in expected_binding.items():
        if binding.get(key) != expected:
            raise ValueError(f"voice binding metadata mismatch: {key}")
    profile_source = str(binding.get("profile_source", ""))
    if profile_source not in {"SCENE_DEFAULT", "SUPPLIED"}:
        raise ValueError("invalid voice profile source")
    profile_scene = str(profile.get("binding_scene", "")).upper()
    requested_scene = str(metadata.get("scene", "")).upper()
    if requested_scene not in {"AUTO", "COURSE", "MODELING", "RESEARCH", "GENERAL"}:
        raise ValueError("run metadata scene is invalid")
    effective_scene = "GENERAL" if requested_scene == "AUTO" else requested_scene
    if (
        str(binding.get("requested_scene", "")).upper() != requested_scene
        or str(binding.get("scene_binding_status", ""))
        != ("UNRESOLVED_AUTO" if requested_scene == "AUTO" else "BOUND")
        or str(binding.get("profile_binding_scene", "")).upper() != profile_scene
        or str(binding.get("voice_profile_binding_scene", "")).upper() != profile_scene
        or str(binding.get("binding_scene", "")).upper() != profile_scene
        or profile_scene != effective_scene
    ):
        raise ValueError("voice Profile scene binding mismatch")
    if profile.get("profile_kind") == "DEFAULT":
        scene = str(profile.get("binding_scene", "")).upper()
        evidence_status = binding.get("voice_evidence_status")
        if evidence_status == "DETERMINISTIC_DEFAULT":
            rebuilt = voice_profiles.build_scene_default_profile(scene)
            if _canonical_json(rebuilt) != _canonical_json(profile):
                raise ValueError("scene default voice profile differs from deterministic registry")
        elif evidence_status == "REBUILT_DEFAULT_PASS":
            manifest_path = run_dir / "voice_sample_manifest.json"
            spec_path = run_dir / "voice_sample_spec.json"
            if not manifest_path.is_file() or not spec_path.is_file():
                raise ValueError("evidence-bound default Profile artifact is missing")
            _validate_frozen_voice_evidence(profile, manifest_path, spec_path)
        else:
            raise ValueError("default voice evidence status is invalid")
    else:
        if profile_source != "SUPPLIED" or binding.get("voice_evidence_status") != "REBUILT_PASS":
            raise ValueError("personal voice profile lacks rebuilt evidence status")
        manifest_path = run_dir / "voice_sample_manifest.json"
        spec_path = run_dir / "voice_sample_spec.json"
        if not manifest_path.is_file() or not spec_path.is_file():
            raise ValueError("personal voice profile evidence artifact is missing")
        _validate_frozen_voice_evidence(profile, manifest_path, spec_path)
    for unit in units:
        for key in VOICE_UNIT_FIELDS:
            metadata_key = key
            if key == "voice_profile_source":
                expected = profile_source
            else:
                expected = binding.get(metadata_key)
            if unit.get(key) != expected:
                raise ValueError(f"voice binding unit mismatch: {unit.get('unit_id', '')}:{key}")
    return profile, binding


def _bundle_voice_binding_error(bundle: dict[str, Any], expected_sha256: str) -> str | None:
    if "voice_profile_sha256" not in bundle:
        return "voice_profile_hash_missing"
    value = bundle.get("voice_profile_sha256")
    if not isinstance(value, str) or not re.fullmatch(r"[0-9a-f]{64}", value):
        return "voice_profile_hash_invalid"
    if value != expected_sha256:
        return "voice_profile_hash_mismatch"
    return None


def _bundle_chunk_binding_error(bundle: dict[str, Any], unit: dict[str, Any]) -> str | None:
    if "unit_id" not in bundle:
        return "bundle_unit_id_missing"
    bundle_unit_id = bundle.get("unit_id")
    if not isinstance(bundle_unit_id, str) or not bundle_unit_id:
        return "bundle_unit_id_invalid"
    if bundle_unit_id != unit.get("unit_id"):
        return "bundle_unit_id_mismatch"
    if "chunk_binding_sha256" not in bundle:
        return "chunk_binding_hash_missing"
    binding_hash = bundle.get("chunk_binding_sha256")
    if not isinstance(binding_hash, str) or not re.fullmatch(r"[0-9a-f]{64}", binding_hash):
        return "chunk_binding_hash_invalid"
    if binding_hash != unit.get("chunk_binding_sha256"):
        return "chunk_binding_hash_mismatch"
    return None


def _decode(raw: bytes, encoding: str) -> str:
    if encoding in {"utf-8", "utf-8-sig"}:
        return raw.decode("utf-8-sig")
    if encoding == "gb18030":
        return raw.decode("gb18030")
    raise ValueError(f"unsupported snapshot encoding: {encoding}")


def _encode(text: str, encoding: str, original_raw: bytes) -> bytes:
    if encoding == "utf-8-sig":
        return text.encode("utf-8-sig")
    if encoding == "utf-8":
        return text.encode("utf-8")
    if encoding == "gb18030":
        return text.encode("gb18030")
    return original_raw


def _rewrite_bundle(path: Path) -> dict[str, Any]:
    if path.suffix.lower() == ".json":
        payload = _load_json(path)
        if not isinstance(payload, dict):
            raise ValueError(f"rewrite bundle must be an object: {path}")
        return payload
    return {
        "decision": "REWRITE",
        "masked_text": path.read_text(encoding="utf-8-sig"),
        "keep_reasons": {},
    }


def _warning_review_bundle(
    bundle: dict[str, Any],
) -> tuple[dict[str, str], str, str, str]:
    if "accepted_warnings" in bundle:
        raise ValueError("retired_accepted_warnings_field")
    resolutions = bundle.get("warning_resolutions", {})
    if not isinstance(resolutions, dict):
        raise ValueError("warning_resolutions must be an object")
    warning_resolutions = {str(key): str(value) for key, value in resolutions.items()}
    request_value = bundle.get("warning_review_request_sha256", "")
    if request_value is None:
        request_value = ""
    if not isinstance(request_value, str):
        raise ValueError("invalid_warning_review_request_sha256")
    request_sha256 = request_value.strip().lower()
    review_present = "warning_review" in bundle

    if not warning_resolutions:
        if review_present:
            raise ValueError("warning_review_without_warning_resolutions")
        if request_sha256:
            raise ValueError("warning_review_request_without_warning_resolutions")
        return warning_resolutions, "", "NONE", ""

    if not re.fullmatch(r"[0-9a-f]{64}", request_sha256):
        raise ValueError("invalid_warning_review_request_sha256")
    if not review_present:
        raise ValueError("missing_warning_review")
    review = bundle.get("warning_review")
    if not isinstance(review, dict):
        raise ValueError("invalid_warning_review")
    if set(review) != {"reviewer_kind", "reviewer_id"}:
        raise ValueError("invalid_warning_review_fields")

    reviewer_kind = review.get("reviewer_kind")
    if not isinstance(reviewer_kind, str) or reviewer_kind.strip().upper() != "HUMAN":
        raise ValueError("warning_reviewer_kind_not_human")
    reviewer_id = review.get("reviewer_id")
    if not isinstance(reviewer_id, str):
        raise ValueError("invalid_warning_reviewer_id")
    reviewer_id = reviewer_id.strip()
    if (
        len(reviewer_id) < 3
        or len(reviewer_id) > 128
        or any(char in reviewer_id for char in "\r\n")
    ):
        raise ValueError("invalid_warning_reviewer_id")
    return warning_resolutions, request_sha256, "HUMAN", reviewer_id


def _validate_rewrite_bundle_fields(bundle: dict[str, Any], decision: str) -> None:
    common = {
        "decision",
        "bundle_path",
        "unit_id",
        "chunk_binding_sha256",
        "keep_reasons",
        "warning_resolutions",
        "warning_review_request_sha256",
        "warning_review",
        "voice_profile_sha256",
    }
    allowed = common | ({"masked_text"} if decision == "REWRITE" else {"reason"})
    unknown = sorted(set(bundle) - allowed)
    if unknown:
        raise ValueError("unknown_rewrite_bundle_fields:" + ",".join(unknown))


def collect_rewrites(directory: Path) -> dict[str, dict[str, Any]]:
    rewrites: dict[str, dict[str, Any]] = {}
    if not directory.is_dir():
        raise FileNotFoundError(directory)
    for path in sorted(directory.iterdir(), key=lambda item: item.name.casefold()):
        if not path.is_file() or path.suffix.lower() not in {".json", ".txt"}:
            continue
        unit_id = path.stem
        if unit_id in rewrites:
            raise ValueError(f"duplicate rewrite for {unit_id}")
        payload = _rewrite_bundle(path)
        payload["bundle_path"] = str(path.resolve())
        rewrites[unit_id] = payload
    return rewrites


def _placeholder_token(span: dict[str, Any]) -> str:
    return f"[[PROTECTED:{span['protected_id']}:{span['sha256'][:12]}]]"


def restore_protected(
    masked_text: str,
    expected_ids: Sequence[str],
    span_map: dict[str, dict[str, Any]],
) -> tuple[str | None, list[str]]:
    errors: list[str] = []
    expected = set(expected_ids)
    seen_matches = list(PLACEHOLDER_RE.finditer(masked_text))
    seen_ids = [match.group("id") for match in seen_matches]
    unknown = sorted(set(seen_ids) - expected)
    missing = sorted(expected - set(seen_ids))
    duplicates = sorted(item for item, count in Counter(seen_ids).items() if count != 1)
    if unknown:
        errors.append("unknown_placeholders:" + ",".join(unknown))
    if missing:
        errors.append("missing_placeholders:" + ",".join(missing))
    if duplicates:
        errors.append("duplicate_placeholders:" + ",".join(duplicates))
    for match in seen_matches:
        protected_id = match.group("id")
        span = span_map.get(protected_id)
        if span and match.group("hash") != span["sha256"][:12]:
            errors.append(f"placeholder_hash_mismatch:{protected_id}")
    if errors:
        return None, errors
    restored = masked_text
    for protected_id in expected_ids:
        span = span_map[protected_id]
        restored = restored.replace(_placeholder_token(span), span["content"])
    if "[[PROTECTED:" in restored:
        errors.append("placeholder_remained_after_restore")
        return None, errors
    return restored, []


def _specific_reason(reason: str) -> bool:
    return len(re.findall(r"[\u3400-\u9fff]", reason)) >= 4


def _normalize_context(text: str) -> str:
    without_placeholders = PLACEHOLDER_RE.sub("", text)
    return re.sub(r"\s+", "", without_placeholders)


def _style_blocks(masked_text: str, unit_id: str, scene: str) -> list[dict[str, Any]]:
    """Return author-facing paragraph blocks without protected payload bytes."""
    text = masked_text.replace("\r\n", "\n").replace("\r", "\n")
    text = PLACEHOLDER_RE.sub(" ", text)
    blocks: list[dict[str, Any]] = []
    for paragraph_index, raw_block in enumerate(re.split(r"\n[ \t]*\n+", text), 1):
        lines = [
            line
            for line in raw_block.splitlines()
            if not PURE_TEX_STRUCTURE_LINE_RE.match(line)
        ]
        block = "\n".join(lines).strip()
        han = "".join(HAN_RE.findall(block))
        if len(han) < 4:
            continue
        blocks.append(
            {
                "unit_id": unit_id,
                "scene": str(scene).upper(),
                "paragraph_index": paragraph_index,
                "text": block,
                "han": han,
            }
        )
    return blocks


def _feature_support(blocks: Sequence[dict[str, Any]], code: str) -> int:
    extractor = voice_profiles.FEATURE_EXTRACTORS.get(code)
    if extractor is None:
        raise ValueError(f"unsupported Voice feature code: {code}")
    pattern = extractor["pattern"]
    return sum(1 for block in blocks if pattern.search(str(block["text"])))


def _ratio_ppm(numerator: int, denominator: int) -> int:
    return numerator * 1_000_000 // denominator if denominator else 0


def _opening_groups(
    blocks: Sequence[dict[str, Any]],
    *,
    width: int,
    require_template_cue: bool,
) -> dict[str, set[str]]:
    groups: dict[str, set[str]] = defaultdict(set)
    for block in blocks:
        han = str(block["han"])
        if len(han) < width:
            continue
        key = han[:width]
        if require_template_cue and not BOUNDARY_TEMPLATE_CUE_RE.match(key):
            continue
        groups[key].add(str(block["unit_id"]))
    return groups


def _voice_negative_result(
    control: dict[str, Any],
    before_blocks: Sequence[dict[str, Any]],
    after_blocks: Sequence[dict[str, Any]],
) -> dict[str, Any]:
    code = str(control.get("value", {}).get("code", ""))
    result: dict[str, Any] = {
        "feature_key": str(control.get("feature_key", "")),
        "code": code,
        "status": "PASS",
        "before_occurrences": 0,
        "after_occurrences": 0,
        "before_units": 0,
        "after_units": 0,
        "amplified_keys": [],
    }
    if code == "KNOWN_AI_TEMPLATE_SHELL":
        before_hits = [
            block for block in before_blocks if voice_profiles.AI_SHELL_RE.search(str(block["text"]))
        ]
        after_hits = [
            block for block in after_blocks if voice_profiles.AI_SHELL_RE.search(str(block["text"]))
        ]
        result.update(
            {
                "before_occurrences": sum(
                    len(voice_profiles.AI_SHELL_RE.findall(str(block["text"]))) for block in before_blocks
                ),
                "after_occurrences": sum(
                    len(voice_profiles.AI_SHELL_RE.findall(str(block["text"]))) for block in after_blocks
                ),
                "before_units": len({str(block["unit_id"]) for block in before_hits}),
                "after_units": len({str(block["unit_id"]) for block in after_hits}),
            }
        )
        if (
            result["after_occurrences"] > result["before_occurrences"]
            or result["after_units"] > result["before_units"]
        ):
            result["status"] = "REVIEW"
        return result
    if code == "REPEATED_PARAGRAPH_OPENING":
        before_groups = _opening_groups(
            before_blocks, width=4, require_template_cue=False
        )
        after_groups = _opening_groups(
            after_blocks, width=4, require_template_cue=False
        )
        amplified = [
            {
                "opening": key,
                "before_units": len(before_groups.get(key, set())),
                "after_units": len(unit_ids),
                "unit_ids": sorted(unit_ids),
            }
            for key, unit_ids in sorted(after_groups.items())
            if len(unit_ids) >= 3 and len(unit_ids) > len(before_groups.get(key, set()))
        ]
        result.update(
            {
                "before_occurrences": sum(len(value) for value in before_groups.values()),
                "after_occurrences": sum(len(value) for value in after_groups.values()),
                "before_units": len({unit for values in before_groups.values() for unit in values}),
                "after_units": len({unit for values in after_groups.values() for unit in values}),
                "amplified_keys": amplified[:20],
            }
        )
        if amplified:
            result["status"] = "REVIEW"
        return result
    result["status"] = "REVIEW"
    result["reason"] = "UNSUPPORTED_NEGATIVE_CONTROL"
    return result


def _audit_voice_conformance(
    profile: dict[str, Any],
    records: Sequence[dict[str, Any]],
    *,
    scene_routing_status: str,
) -> dict[str, Any]:
    evaluated = [
        record
        for record in records
        if record.get("state") in {"DONE", "NO_CHANGE"}
        and isinstance(record.get("after_masked"), str)
    ]
    expected = [record for record in records if record.get("expected")]
    before_blocks = [
        block
        for record in evaluated
        for block in _style_blocks(
            str(record["before_masked"]), str(record["unit_id"]), str(record["scene"])
        )
    ]
    after_blocks = [
        block
        for record in evaluated
        for block in _style_blocks(
            str(record["after_masked"]), str(record["unit_id"]), str(record["scene"])
        )
    ]
    reasons: list[str] = []
    if len(evaluated) != len(expected):
        reasons.append("INCOMPLETE_EDITABLE_UNITS")
    if scene_routing_status != "PASS":
        reasons.append("SCENE_ROUTING_NOT_PASS")
    if any(str(record.get("style_validation")) != "PASS" for record in evaluated):
        reasons.append("UNIT_STYLE_VALIDATION_NOT_PASS")

    profile_kind = str(profile.get("profile_kind", ""))
    feature_results: list[dict[str, Any]] = []
    negative_results: list[dict[str, Any]] = []
    if profile_kind == "DEFAULT":
        status = "PASS" if not reasons else "REVIEW"
        return {
            "schema_version": "humanize-document-voice-conformance/v1",
            "status": status,
            "basis": "SCENE_DEFAULT_UNIT_VALIDATION",
            "profile_kind": profile_kind,
            "profile_sha256": profile.get("profile_sha256"),
            "feature_extractor_policy_sha256": voice_profiles.FEATURE_EXTRACTOR_POLICY_SHA256,
            "identity_verified": False,
            "personal_voice_claim_allowed": False,
            "personal_voice_conformance_status": "NOT_APPLICABLE",
            "expected_units": len(expected),
            "evaluated_units": len(evaluated),
            "before_blocks": len(before_blocks),
            "after_blocks": len(after_blocks),
            "feature_results": feature_results,
            "negative_results": negative_results,
            "review_reasons": sorted(set(reasons)),
            "limitations": [
                "PASS confirms deterministic scene-default binding and unit validator coverage only.",
                "It does not reproduce or verify a personal author identity.",
            ],
        }

    if profile_kind != "PERSONAL":
        reasons.append("UNSUPPORTED_PROFILE_KIND")
    if len(after_blocks) < 6:
        reasons.append("INSUFFICIENT_TARGET_BLOCKS")

    for feature in profile.get("features", []):
        code = str(feature.get("value", {}).get("code", ""))
        scope = {str(item).upper() for item in feature.get("scope", [])}
        scoped_before = [
            block
            for block in before_blocks
            if "GLOBAL" in scope or str(block["scene"]).upper() in scope
        ]
        scoped_after = [
            block
            for block in after_blocks
            if "GLOBAL" in scope or str(block["scene"]).upper() in scope
        ]
        result: dict[str, Any] = {
            "feature_key": str(feature.get("feature_key", "")),
            "code": code,
            "disposition": str(feature.get("disposition", "")),
            "status": "PASS",
            "profile_ratio_ppm": int(feature.get("evidence", {}).get("support_ratio_ppm", 0)),
            "before_opportunities": len(scoped_before),
            "after_opportunities": len(scoped_after),
        }
        extractor = voice_profiles.FEATURE_EXTRACTORS.get(code)
        if extractor is None:
            current_extractor_sha256 = ""
        else:
            current_extractor_sha256 = voice_profiles._stable_hash(
                {
                    "rule_id": extractor["rule_id"],
                    "pattern": extractor["pattern"].pattern,
                    "flags": extractor["pattern"].flags,
                    "code": code,
                }
            )
        declared_extractor_sha256 = str(
            feature.get("evidence", {}).get("extractor_sha256", "")
        )
        result["declared_extractor_sha256"] = declared_extractor_sha256
        result["current_extractor_sha256"] = current_extractor_sha256
        if declared_extractor_sha256 != current_extractor_sha256:
            result.update(
                {
                    "before_support": 0,
                    "after_support": 0,
                    "before_ratio_ppm": 0,
                    "after_ratio_ppm": 0,
                    "status": "REVIEW",
                    "reason": "FEATURE_EXTRACTOR_BINDING_MISMATCH",
                }
            )
            feature_results.append(result)
            reasons.append("FEATURE_EXTRACTOR_BINDING_MISMATCH")
            continue
        try:
            before_support = _feature_support(scoped_before, code)
            after_support = _feature_support(scoped_after, code)
        except ValueError:
            result.update(
                {
                    "before_support": 0,
                    "after_support": 0,
                    "before_ratio_ppm": 0,
                    "after_ratio_ppm": 0,
                    "status": "REVIEW",
                    "reason": "UNSUPPORTED_FEATURE_CODE",
                }
            )
            feature_results.append(result)
            reasons.append("UNSUPPORTED_FEATURE_CODE")
            continue
        before_ratio = _ratio_ppm(before_support, len(scoped_before))
        after_ratio = _ratio_ppm(after_support, len(scoped_after))
        tolerance = max(
            250_000,
            _ratio_ppm(1, max(len(scoped_before), len(scoped_after), 1)),
        )
        support_drop = before_support - after_support
        ratio_drop = before_ratio - after_ratio
        material_regression = (
            len(scoped_after) >= 6
            and support_drop >= 2
            and ratio_drop >= 250_000
            and after_ratio < result["profile_ratio_ppm"]
        )
        severe_absolute_gap = (
            code in {"EXPLICIT_TERMINAL_PUNCTUATION", "NON_LIST_PROSE"}
            and
            len(scoped_after) >= 12
            and result["profile_ratio_ppm"] - after_ratio >= 600_000
        )
        structural_floor = max(300_000, result["profile_ratio_ppm"] - 400_000)
        structural_regression = (
            code in {"EXPLICIT_TERMINAL_PUNCTUATION", "NON_LIST_PROSE"}
            and len(scoped_after) >= 8
            and after_ratio < structural_floor
            and after_ratio < before_ratio
        )
        result.update(
            {
                "before_support": before_support,
                "after_support": after_support,
                "before_ratio_ppm": before_ratio,
                "after_ratio_ppm": after_ratio,
                "tolerance_ppm": tolerance,
                "support_drop": support_drop,
                "ratio_drop_ppm": ratio_drop,
                "material_regression": material_regression,
                "severe_absolute_gap": severe_absolute_gap,
                "structural_floor_ppm": structural_floor,
                "structural_regression": structural_regression,
            }
        )
        if len(scoped_after) < 6:
            result["status"] = "REVIEW"
            result["reason"] = "INSUFFICIENT_SCOPED_TARGET_BLOCKS"
            reasons.append("INSUFFICIENT_SCOPED_TARGET_BLOCKS")
        elif material_regression or severe_absolute_gap or structural_regression:
            result["status"] = "REVIEW"
            result["reason"] = (
                "MATERIAL_PREFERRED_FEATURE_REGRESSION"
                if material_regression
                else "SEVERE_PROFILE_FEATURE_GAP"
                if severe_absolute_gap
                else "STRUCTURAL_VOICE_FEATURE_REGRESSION"
            )
            reasons.append("MATERIAL_PREFERRED_FEATURE_REGRESSION")
        feature_results.append(result)

    for control in profile.get("negative_controls", []):
        result = _voice_negative_result(control, before_blocks, after_blocks)
        negative_results.append(result)
        if result["status"] != "PASS":
            reasons.append("VOICE_NEGATIVE_CONTROL_AMPLIFIED")

    status = "PASS" if not reasons else "REVIEW"
    return {
        "schema_version": "humanize-document-voice-conformance/v1",
        "status": status,
        "basis": "PERSONAL_PROFILE_NON_REGRESSION",
        "profile_kind": profile_kind,
        "profile_sha256": profile.get("profile_sha256"),
        "identity_verified": False,
        "personal_voice_claim_allowed": bool(
            profile.get("defaults", {}).get("personal_voice_claim_allowed", False)
        ),
        "personal_voice_conformance_status": status,
        "expected_units": len(expected),
        "evaluated_units": len(evaluated),
        "before_blocks": len(before_blocks),
        "after_blocks": len(after_blocks),
        "feature_results": feature_results,
        "negative_results": negative_results,
        "feature_extractor_policy_sha256": voice_profiles.FEATURE_EXTRACTOR_POLICY_SHA256,
        "review_reasons": sorted(set(reasons)),
        "limitations": [
            "Feature ratios are conservative non-regression checks, not authorship proof.",
            "Unencoded semantic voice choices remain outside deterministic evaluation.",
        ],
    }


def _template_match_text(text: str) -> str:
    normalized = unicodedata.normalize("NFKC", text)
    normalized = ZERO_WIDTH_RE.sub("", normalized)
    return HAN_GAP_RE.sub("", normalized)


def _signal_occurrences(
    signal: dict[str, Any], blocks: Sequence[dict[str, Any]]
) -> list[dict[str, Any]]:
    occurrences: list[dict[str, Any]] = []
    for block in blocks:
        match_text = _template_match_text(str(block["text"]))
        raw_matches: list[re.Match[str]] = []
        for pattern in output_validator.lexical._signal_patterns(signal):
            raw_matches.extend(pattern.finditer(match_text))
        for start, end, matched in output_validator.lexical._deduplicate_matches(raw_matches):
            if output_validator.lexical._exclusion_reason(
                match_text, start, end, signal
            ):
                continue
            occurrences.append(
                {
                    "unit_id": str(block["unit_id"]),
                    "paragraph_index": int(block["paragraph_index"]),
                    "matched": matched,
                }
            )
    return occurrences


def _guard_group_occurrences(
    group: dict[str, Any], blocks: Sequence[dict[str, Any]]
) -> list[dict[str, Any]]:
    pattern = re.compile(str(group["regex"]))
    occurrences: list[dict[str, Any]] = []
    for block in blocks:
        match_text = _template_match_text(str(block["text"]))
        for match in pattern.finditer(match_text):
            occurrences.append(
                {
                    "unit_id": str(block["unit_id"]),
                    "paragraph_index": int(block["paragraph_index"]),
                    "matched": match.group(0),
                    "matched_sha256": sha256(match.group(0).encode("utf-8")),
                }
            )
    return occurrences


def _audit_cross_unit_repetition(records: Sequence[dict[str, Any]]) -> dict[str, Any]:
    evaluated = [
        record
        for record in records
        if record.get("state") in {"DONE", "NO_CHANGE"}
        and isinstance(record.get("after_masked"), str)
    ]
    expected = [record for record in records if record.get("expected")]
    before_blocks = [
        block
        for record in evaluated
        for block in _style_blocks(
            str(record["before_masked"]), str(record["unit_id"]), str(record["scene"])
        )
    ]
    after_blocks = [
        block
        for record in evaluated
        for block in _style_blocks(
            str(record["after_masked"]), str(record["unit_id"]), str(record["scene"])
        )
    ]
    findings: list[dict[str, Any]] = []
    inherited_findings: list[dict[str, Any]] = []
    blocking_unit_ids: set[str] = set()
    guard_review_reasons: list[str] = []
    action_profile: dict[str, Any] | None = None
    action_profile_sha256 = ""
    action_catalog_sha256 = ""
    active_detector_definition_sha256: list[str] = []
    lexicon = output_validator.lexical.load_lexicon()
    for signal in lexicon["signals"]:
        if signal.get("category") != "repair-template-repetition":
            continue
        before_hits = _signal_occurrences(signal, before_blocks)
        after_hits = _signal_occurrences(signal, after_blocks)
        before_by_unit = Counter(item["unit_id"] for item in before_hits)
        after_by_unit = Counter(item["unit_id"] for item in after_hits)
        after_units = sorted({item["unit_id"] for item in after_hits})
        introduced_units = sorted(
            unit_id
            for unit_id, count in after_by_unit.items()
            if count > before_by_unit.get(unit_id, 0)
        )
        minimum = int(signal.get("threshold", {}).get("min_occurrences", 1))
        if (
            len(after_hits) >= minimum
            and len(after_units) >= 2
            and introduced_units
        ):
            blocking_unit_ids.update(introduced_units)
            findings.append(
                {
                    "kind": "REPAIR_SIGNAL_FAMILY",
                    "signal_id": str(signal.get("id", "")),
                    "before_occurrences": len(before_hits),
                    "after_occurrences": len(after_hits),
                    "before_units": sorted({item["unit_id"] for item in before_hits}),
                    "after_units": after_units,
                    "introduced_unit_ids": introduced_units,
                    "matches": [item["matched"] for item in after_hits[:20]],
                }
            )
        elif len(after_hits) >= minimum and len(after_units) >= 2:
            inherited_findings.append(
                {
                    "kind": "REPAIR_SIGNAL_FAMILY",
                    "signal_id": str(signal.get("id", "")),
                    "before_occurrences": len(before_hits),
                    "after_occurrences": len(after_hits),
                    "units": after_units,
                }
            )

    try:
        action_profile = action_profiles.build_action_profile()
        action_profile_sha256 = sha256(
            json.dumps(
                action_profile,
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
            ).encode("utf-8")
        )
        action_catalog_sha256 = sha256(action_profiles.DEFAULT_CATALOG.read_bytes())
    except (OSError, UnicodeError, ValueError) as error:
        guard_review_reasons.append(
            f"ACTION_PROFILE_UNAVAILABLE:{type(error).__name__}"
        )

    active_scenes = {str(record.get("scene", "")).upper() for record in evaluated}
    if action_profile is not None:
        for guard in action_profile.get("action_cards", []):
            if guard.get("kind") != "negative_guard":
                continue
            guard_scene = str(guard.get("scene", "")).upper()
            if guard_scene != "ALL" and guard_scene not in active_scenes:
                continue
            if guard.get("status") != "AVAILABLE":
                guard_review_reasons.append(
                    f"NEGATIVE_GUARD_UNAVAILABLE:{guard.get('id', '')}"
                )
                continue
            before_group_results: list[dict[str, Any]] = []
            after_group_results: list[dict[str, Any]] = []
            introduced_units: set[str] = set()
            detector = guard["detector"]
            detector_sha256 = sha256(
                json.dumps(
                    detector,
                    ensure_ascii=False,
                    sort_keys=True,
                    separators=(",", ":"),
                ).encode("utf-8")
            )
            active_detector_definition_sha256.append(detector_sha256)
            for group in detector["pattern_groups"]:
                before_hits = _guard_group_occurrences(group, before_blocks)
                after_hits = _guard_group_occurrences(group, after_blocks)
                before_by_unit = Counter(item["unit_id"] for item in before_hits)
                after_by_unit = Counter(item["unit_id"] for item in after_hits)
                group_introduced = {
                    unit_id
                    for unit_id, count in after_by_unit.items()
                    if count > before_by_unit.get(unit_id, 0)
                }
                introduced_units.update(group_introduced)
                minimum = int(group.get("minimum_occurrences", 1))
                before_group_results.append(
                    {
                        "id": group["id"],
                        "occurrences": len(before_hits),
                        "minimum_occurrences": minimum,
                        "units": sorted(before_by_unit),
                        "triggered": len(before_hits) >= minimum,
                    }
                )
                after_group_results.append(
                    {
                        "id": group["id"],
                        "occurrences": len(after_hits),
                        "minimum_occurrences": minimum,
                        "units": sorted(after_by_unit),
                        "introduced_unit_ids": sorted(group_introduced),
                        "triggered": len(after_hits) >= minimum,
                    }
                )
            triggered_after = [item for item in after_group_results if item["triggered"]]
            triggered_before = [item for item in before_group_results if item["triggered"]]
            matched_after_units = {
                unit_id for item in triggered_after for unit_id in item["units"]
            }
            detector_triggered = (
                len(triggered_after) >= int(detector["minimum_groups"])
                and len(matched_after_units) >= 2
            )
            if detector_triggered and introduced_units:
                blocking_unit_ids.update(introduced_units)
                findings.append(
                    {
                        "kind": "CORPUS_NEGATIVE_GUARD",
                        "card_id": str(guard.get("id", "")),
                        "scene": guard_scene,
                        "definition_sha256": detector_sha256,
                        "minimum_groups": int(detector["minimum_groups"]),
                        "before_groups": before_group_results,
                        "after_groups": after_group_results,
                        "introduced_unit_ids": sorted(introduced_units),
                    }
                )
            elif detector_triggered:
                inherited_findings.append(
                    {
                        "kind": "CORPUS_NEGATIVE_GUARD",
                        "card_id": str(guard.get("id", "")),
                        "scene": guard_scene,
                        "before_triggered_groups": len(triggered_before),
                        "after_triggered_groups": len(triggered_after),
                        "units": sorted(matched_after_units),
                    }
                )

    before_openings = _opening_groups(
        before_blocks, width=6, require_template_cue=True
    )
    after_openings = _opening_groups(
        after_blocks, width=6, require_template_cue=True
    )
    for opening, unit_ids in sorted(after_openings.items()):
        before_units = before_openings.get(opening, set())
        if len(unit_ids) >= 3 and len(unit_ids) > len(before_units):
            introduced_units = sorted(unit_ids - before_units)
            blocking_unit_ids.update(introduced_units)
            findings.append(
                {
                    "kind": "REPEATED_TEMPLATE_OPENING",
                    "opening": opening,
                    "before_unit_count": len(before_units),
                    "after_unit_count": len(unit_ids),
                    "before_units": sorted(before_units),
                    "after_units": sorted(unit_ids),
                    "introduced_unit_ids": introduced_units,
                }
            )
        elif len(unit_ids) >= 3:
            inherited_findings.append(
                {
                    "kind": "REPEATED_TEMPLATE_OPENING",
                    "opening": opening,
                    "unit_count": len(unit_ids),
                    "units": sorted(unit_ids),
                }
            )

    incomplete = len(evaluated) != len(expected)
    status = (
        "PASS"
        if not incomplete and not findings and not guard_review_reasons
        else "REVIEW"
    )
    policy = {
        "version": "cross-unit-repetition/v1",
        "author_view": "masked_text_without_protected_payload",
        "repair_signal_categories": ["repair-template-repetition"],
        "boundary_opening_han_chars": 6,
        "boundary_minimum_units": 3,
        "comparison": "after must not introduce additional cross-unit coverage",
        "template_normalization": "NFKC+remove-zero-width+remove-Han-internal-space",
        "corpus_negative_guards": True,
    }
    for finding in findings:
        fingerprint_payload = dict(finding)
        finding["finding_fingerprint"] = sha256(
            json.dumps(
                fingerprint_payload,
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
            ).encode("utf-8")
        )
    unit_inventory = [
        {
            "unit_id": str(record.get("unit_id", "")),
            "scene": str(record.get("scene", "")),
            "expected": bool(record.get("expected")),
            "state": str(record.get("state", "")),
        }
        for record in records
    ]
    before_document_view = [
        {
            "unit_id": str(record.get("unit_id", "")),
            "sha256": sha256(str(record.get("before_masked", "")).encode("utf-8")),
        }
        for record in records
    ]
    after_document_view = [
        {
            "unit_id": str(record.get("unit_id", "")),
            "sha256": (
                sha256(str(record.get("after_masked", "")).encode("utf-8"))
                if isinstance(record.get("after_masked"), str)
                else ""
            ),
        }
        for record in records
    ]
    return {
        "schema_version": "humanize-cross-unit-repetition/v1",
        "status": status,
        "expected_units": len(expected),
        "evaluated_units": len(evaluated),
        "before_blocks": len(before_blocks),
        "after_blocks": len(after_blocks),
        "findings": findings[:40],
        "finding_count": len(findings),
        "inherited_findings": inherited_findings[:40],
        "inherited_finding_count": len(inherited_findings),
        "blocking_unit_ids": sorted(blocking_unit_ids),
        "review_reasons": (
            (["INCOMPLETE_EDITABLE_UNITS"] if incomplete else [])
            + sorted(set(guard_review_reasons))
        ),
        "action_catalog_sha256": action_catalog_sha256,
        "action_profile_sha256": action_profile_sha256,
        "action_profile_status": (
            str(action_profile.get("status", "")) if action_profile is not None else "NOT_AVAILABLE"
        ),
        "active_detector_definition_sha256": sorted(
            set(active_detector_definition_sha256)
        ),
        "lexical_policy_sha256": sha256(
            output_validator.lexical.DEFAULT_LEXICON.read_bytes()
        ),
        "unit_inventory_sha256": sha256(
            json.dumps(
                unit_inventory,
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
            ).encode("utf-8")
        ),
        "before_logical_document_sha256": sha256(
            json.dumps(
                before_document_view,
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
            ).encode("utf-8")
        ),
        "candidate_logical_document_sha256": sha256(
            json.dumps(
                after_document_view,
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
            ).encode("utf-8")
        ),
        "evaluation_scope": "PARTIAL" if incomplete else "FULL",
        "policy": policy,
        "policy_sha256": sha256(
            json.dumps(policy, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ),
    }


def _copied_read_only_context(original: str, restored: str, chunk: dict[str, Any]) -> list[str]:
    original_normalized = _normalize_context(original)
    restored_normalized = _normalize_context(restored)
    copied: list[str] = []
    for field in ("read_only_context_before", "read_only_context_after"):
        context = _normalize_context(str(chunk.get(field, "")))
        if len(context) < 4 or context in original_normalized:
            continue
        if context in restored_normalized:
            copied.append(field)
    return copied


def _protected_content_count_changes(
    original: str,
    restored: str,
    expected_ids: Sequence[str],
    span_map: dict[str, dict[str, Any]],
) -> list[str]:
    def canonical_newlines(value: str) -> str:
        return value.replace("\r\n", "\n").replace("\r", "\n")

    canonical_original = canonical_newlines(original)
    canonical_restored = canonical_newlines(restored)
    changed: list[str] = []
    for protected_id in expected_ids:
        content = canonical_newlines(str(span_map[protected_id]["content"]))
        if content and canonical_original.count(content) != canonical_restored.count(content):
            changed.append(protected_id)
    return changed


def _relative_render_paths(files: Sequence[dict[str, Any]]) -> dict[str, Path]:
    existing_paths = [
        Path(item["path"])
        for item in files
        if item["status"] not in {"UNRESOLVED", "UNRESOLVED_INCLUDE", "SKIPPED_GARBLED"}
    ]
    parents = [str(path.parent) for path in existing_paths]
    common: Path | None = None
    if parents:
        try:
            common = Path(os.path.commonpath(parents))
        except ValueError:
            common = None
    output: dict[str, Path] = {}
    for item in files:
        path = Path(item["path"])
        if common is not None:
            try:
                relative = path.relative_to(common)
            except ValueError:
                relative = Path(f"{item['file_id']}{path.suffix or '.txt'}")
        else:
            relative = Path(f"{item['file_id']}{path.suffix or '.txt'}")
        output[item["file_id"]] = relative
    return output


def _directory_hashes(root: Path) -> dict[str, str]:
    if not root.is_dir():
        return {}
    return {
        str(path.relative_to(root)).replace("\\", "/"): sha256(path.read_bytes())
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


TRANSIENT_FINALIZE_NAMES = {
    ".validation_staging",
    ".diffs_staging",
    ".rendered_staging",
    ".compile_check_staging",
    ".finalize.lock",
}


def _run_state_hashes(run_dir: Path) -> dict[str, str]:
    """Hash all pre-existing run artifacts that a check command must not mutate."""
    if not run_dir.is_dir():
        return {}
    output: dict[str, str] = {}
    for path in sorted(run_dir.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(run_dir)
        if any(part in TRANSIENT_FINALIZE_NAMES for part in relative.parts):
            continue
        output[str(relative).replace("\\", "/")] = sha256(path.read_bytes())
    return output


def _copy_for_check(source: Path, destination: Path) -> None:
    """Create a disposable check workspace without exposing the publish tree."""
    if destination.exists():
        shutil.rmtree(destination)
    shutil.copytree(source, destination)


def _commit_evidence_directory(staged: Path, destination: Path) -> None:
    if destination.exists():
        shutil.rmtree(destination)
    staged.rename(destination)


def _source_changes(file_manifest: Sequence[dict[str, Any]]) -> list[dict[str, str]]:
    changes: list[dict[str, str]] = []
    for record in file_manifest:
        if not record["sha256"]:
            continue
        source = Path(record["path"])
        if not source.exists():
            changes.append(
                {
                    "file_id": record["file_id"],
                    "path": record["path"],
                    "snapshot_sha256": record["sha256"],
                    "current_sha256": "",
                    "current_state": "MISSING",
                }
            )
            continue
        if not source.is_file():
            changes.append(
                {
                    "file_id": record["file_id"],
                    "path": record["path"],
                    "snapshot_sha256": record["sha256"],
                    "current_sha256": "",
                    "current_state": "NOT_FILE",
                }
            )
            continue
        current_hash = sha256(source.read_bytes())
        if current_hash != record["sha256"]:
            changes.append(
                {
                    "file_id": record["file_id"],
                    "path": record["path"],
                    "snapshot_sha256": record["sha256"],
                    "current_sha256": current_hash,
                    "current_state": "MODIFIED",
                }
            )
    return changes


def _compile_check_result(
    *,
    status: str,
    command: str = "",
    exit_code: int | None = None,
    stdout: str = "",
    stderr: str = "",
    cwd: Path | None = None,
    integrity_status: str = "NOT_RUN",
    integrity_changes: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build one stable compile-check payload for executed and skipped checks."""
    return {
        "status": status,
        "command": command,
        "exit_code": exit_code,
        "stdout": stdout,
        "stderr": stderr,
        "cwd": str(cwd.resolve()) if cwd is not None else None,
        "integrity_status": integrity_status,
        "integrity_changes": dict(integrity_changes or {}),
    }


def _run_compile(command: str | None, cwd: Path) -> dict[str, Any]:
    if not command:
        return _compile_check_result(status="NOT_RUN")
    completed = subprocess.run(
        command,
        cwd=cwd,
        shell=True,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    return _compile_check_result(
        status="PASS" if completed.returncode == 0 else "FAIL",
        command=command,
        exit_code=completed.returncode,
        stdout=completed.stdout[-8000:],
        stderr=completed.stderr[-8000:],
        cwd=cwd,
    )


LEDGER_FIELDS = (
    "unit_id",
    "file_id",
    "heading_path",
    "part",
    "start_line",
    "end_line",
    "line_count",
    "scene",
    "voice_profile_id",
    "voice_profile_revision",
    "voice_profile_confidence",
    "voice_profile_kind",
    "voice_profile_source",
    "voice_profile_binding_scene",
    "voice_profile_sha256",
    "voice_default_disclosure",
    "chunk_binding_sha256",
    "mode",
    "intensity",
    "owner_chunk",
    "context_before_unit",
    "context_after_unit",
    "author_chars",
    "protected_spans",
    "status",
    "hash_before",
    "hash_after",
    "diff_path",
    "protected_hashes_ok",
    "style_validation",
    "notes",
)

INITIAL_UNIT_STATUSES = {
    "PENDING",
    "SKIPPED_PROTECTED",
    "UNRESOLVED",
    "SKIPPED_GARBLED",
    "CHANGED_AFTER_SNAPSHOT",
}


def _without_prepare_private_fields(row: dict[str, Any]) -> dict[str, Any]:
    """Return the public initial-unit representation emitted by prepare."""
    return {
        key: value
        for key, value in row.items()
        if key not in {"masked_text", "read_only_context_before", "read_only_context_after"}
    }


def _canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _rebuild_prepare_state(
    run_dir: Path,
    snapshot: dict[str, Any],
    file_manifest: Sequence[dict[str, str]],
    metadata: dict[str, Any],
    units: Sequence[dict[str, Any]],
    spans: Sequence[dict[str, Any]],
) -> None:
    """Reconstruct prepare output from frozen source copies before trusting any ledger state.

    The integrity manifest detects ordinary tampering. This independent rebuild also detects an
    attacker who edits both ``units.jsonl`` and the manifest: initial statuses, offsets, hashes,
    masks, and read-only context must still be derivable from the frozen source bytes.
    """
    budgets = metadata.get("budgets")
    if not isinstance(budgets, dict):
        raise ValueError("run_metadata.json has no prepare budgets")
    scene = str(metadata.get("scene", "AUTO")).upper()
    wrappers = frozenset(str(item) for item in metadata.get("editable_style_wrappers", []))
    expected_units: list[dict[str, Any]] = []
    expected_spans: list[dict[str, Any]] = []
    for record in file_manifest:
        snapshot_copy = str(record.get("snapshot_copy", ""))
        status = str(record.get("status", ""))
        if not snapshot_copy or status in {"UNRESOLVED", "UNRESOLVED_INCLUDE", "SKIPPED_GARBLED"}:
            continue
        copy_path = run_dir / snapshot_copy
        if not copy_path.is_file():
            raise ValueError(f"missing prepare source copy: {snapshot_copy}")
        raw = copy_path.read_bytes()
        if sha256(raw) != str(record.get("sha256", "")):
            raise ValueError(f"prepare source copy hash mismatch: {record.get('file_id', '')}")
        text = _decode(raw, str(record.get("encoding", "")))
        local_spans = preparer.protected_spans(
            text,
            str(record.get("suffix", "")),
            str(record.get("file_id", "")),
            wrappers,
        )
        expected_spans.extend(local_spans)
        file_units = preparer.build_units(
            dict(record),
            text,
            local_spans,
            scene=scene,
            voice_binding=dict(metadata.get("voice_binding", {})),
            max_author_chars=int(budgets.get("max_author_chars", 7000)),
            max_lines=int(budgets.get("max_lines", 600)),
            min_author_chars=int(budgets.get("min_author_chars", 1200)),
        )
        if str(record.get("changed_after_snapshot", "")).lower() == "true":
            for unit in file_units:
                unit["status"] = "CHANGED_AFTER_SNAPSHOT"
                unit["notes"] = (
                    (unit["notes"] + "; ") if unit.get("notes") else ""
                ) + "source_changed_after_snapshot"
        expected_units.extend(file_units)
    preparer.attach_read_only_context(expected_units)
    for unit in expected_units:
        unit["chunk_binding_sha256"] = preparer.materialize_chunk_payload(unit)[
            "chunk_binding_sha256"
        ]
    expected_public_units = [_without_prepare_private_fields(item) for item in expected_units]
    actual_public_units = [_without_prepare_private_fields(dict(item)) for item in units]
    if _canonical_json(actual_public_units) != _canonical_json(expected_public_units):
        raise ValueError("initial prepare state mismatch: units.jsonl does not match reconstructed source")
    if _canonical_json(list(spans)) != _canonical_json(expected_spans):
        raise ValueError("initial prepare state mismatch: protected_spans.jsonl does not match reconstructed source")

    ledger_path = run_dir / "coverage_ledger.csv"
    if not ledger_path.is_file():
        raise ValueError("missing coverage_ledger.csv")
    actual_ledger = _load_csv(ledger_path)
    ledger_fields = (
        "unit_id", "file_id", "heading_path", "part", "start_line", "end_line", "line_count",
        "scene", "voice_profile_id", "voice_profile_revision", "voice_profile_confidence",
        "voice_profile_kind", "voice_profile_source", "voice_profile_binding_scene",
        "voice_profile_sha256", "voice_default_disclosure", "chunk_binding_sha256",
        "mode", "intensity", "owner_chunk", "context_before_unit", "context_after_unit",
        "author_chars", "protected_spans", "status", "hash_before", "hash_after", "diff_path",
        "protected_hashes_ok", "style_validation", "notes",
    )
    expected_ledger = [
        {field: str(item.get(field, "")) for field in ledger_fields}
        for item in expected_public_units
    ]
    actual_ledger_normalized = [
        {field: item.get(field, "") for field in ledger_fields}
        for item in actual_ledger
    ]
    if _canonical_json(actual_ledger_normalized) != _canonical_json(expected_ledger):
        raise ValueError("initial prepare state mismatch: coverage_ledger.csv does not match reconstructed source")

    expected_snapshot_files = snapshot.get("files")
    manifest_projection = [
        {
            key: (
                int(record.get(key, "0") or 0)
                if key in {"bytes", "readable_bytes"}
                else str(record.get(key, "")).lower() == "true"
                if key == "changed_after_snapshot"
                else record.get(key, "")
            )
            for key in (
                "file_id", "path", "bytes", "readable_bytes", "encoding", "sha256", "modified_at",
                "changed_after_snapshot", "snapshot_copy", "status", "reason",
            )
        }
        for record in file_manifest
    ]
    if _canonical_json(expected_snapshot_files) != _canonical_json(manifest_projection):
        raise ValueError("initial prepare state mismatch: snapshot and file manifest disagree")

    # Chunks carry the masked text and adjacent read-only context used by the validator.
    for expected in expected_units:
        unit_id = str(expected["unit_id"])
        chunk_path = run_dir / "chunks" / f"{unit_id}.json"
        if not chunk_path.is_file():
            raise ValueError(f"missing prepare chunk: {unit_id}")
        expected_chunk = {
            key: value
            for key, value in expected.items()
            if key not in {"masked_text", "read_only_context_before", "read_only_context_after"}
        }
        expected_chunk["masked_text"] = expected["masked_text"]
        expected_chunk["read_only_context_before"] = expected["read_only_context_before"]
        expected_chunk["read_only_context_after"] = expected["read_only_context_after"]
        actual_chunk = _load_json(chunk_path)
        if _canonical_json(actual_chunk) != _canonical_json(expected_chunk):
            raise ValueError(f"initial prepare state mismatch: chunk {unit_id} differs from reconstructed source")


def _validate_initial_unit_states(units: Sequence[dict[str, Any]]) -> None:
    """Reject terminal status injection before any rewrite is considered."""
    seen: set[str] = set()
    for unit in units:
        unit_id = str(unit.get("unit_id", ""))
        if not unit_id or unit_id in seen:
            raise ValueError("invalid or duplicate initial unit_id")
        seen.add(unit_id)
        status = str(unit.get("status", ""))
        if status not in INITIAL_UNIT_STATUSES:
            raise ValueError(f"invalid initial unit status for {unit_id}: {status}")
        if status == "PENDING" and str(unit.get("hash_after", "")):
            raise ValueError(f"initial PENDING unit has hash_after: {unit_id}")


def _public_chunk_payload(chunk: dict[str, Any]) -> dict[str, Any]:
    """Return the prepare-time unit record embedded in an immutable chunk."""
    return {
        key: value
        for key, value in chunk.items()
        if key not in {"masked_text", "read_only_context_before", "read_only_context_after"}
    }


def _visible_author_chars(masked_text: str, suffix: str) -> int:
    visible = PLACEHOLDER_RE.sub("", masked_text)
    if suffix.lower() in {".tex", ".ltx"}:
        visible = TEX_COMMAND_TOKEN_RE.sub("", visible)
        visible = re.sub(r"[{}\[\]$&_^~]", " ", visible)
    else:
        visible = re.sub(r"[#>*_`|~-]", " ", visible)
    return len(HAN_RE.findall(visible))


def _validate_units_against_chunks(
    units: Sequence[dict[str, Any]],
    chunks: dict[str, dict[str, Any]],
    file_texts: dict[str, str],
    file_suffixes: dict[str, str],
    span_map: dict[str, dict[str, Any]],
) -> None:
    """Rebuild the initial unit identity instead of trusting a mutable ledger.

    ``prepare_integrity.json`` is deliberately treated as an audit aid, not as
    an independent trust anchor.  The chunk payloads are the canonical
    prepare-time records; each one is also checked against the frozen source
    substring and protected-span restoration.  A forged ``units.jsonl`` row
    therefore cannot turn editable content into a terminal state, even when a
    caller also rewrites the integrity manifest.
    """
    unit_ids = {str(item.get("unit_id", "")) for item in units}
    chunk_ids = set(chunks)
    if unit_ids != chunk_ids:
        raise ValueError("units.jsonl does not match canonical chunk set")

    for unit in units:
        unit_id = str(unit["unit_id"])
        chunk = chunks[unit_id]
        canonical = _public_chunk_payload(chunk)
        if unit != canonical:
            raise ValueError(f"units.jsonl does not match canonical chunk: {unit_id}")
        binding_hash = chunk.get("chunk_binding_sha256")
        if (
            not isinstance(binding_hash, str)
            or not re.fullmatch(r"[0-9a-f]{64}", binding_hash)
            or binding_hash != preparer.chunk_binding_sha256(chunk)
        ):
            raise ValueError(f"canonical chunk binding hash mismatch: {unit_id}")

        status = str(chunk.get("status", ""))
        if status not in INITIAL_UNIT_STATUSES:
            raise ValueError(f"invalid canonical chunk status for {unit_id}: {status}")
        if str(chunk.get("hash_after", "")):
            raise ValueError(f"canonical initial chunk has hash_after: {unit_id}")

        file_id = str(chunk.get("file_id", ""))
        source_text = file_texts.get(file_id)
        if source_text is None:
            raise ValueError(f"canonical chunk references unavailable file: {unit_id}")
        try:
            start = int(chunk["start"])
            end = int(chunk["end"])
        except (KeyError, TypeError, ValueError) as error:
            raise ValueError(f"invalid canonical chunk range: {unit_id}") from error
        if start < 0 or end <= start or end > len(source_text):
            raise ValueError(f"invalid canonical chunk range: {unit_id}")
        original = source_text[start:end]
        if sha256(original.encode("utf-8")) != str(chunk.get("hash_before", "")):
            raise ValueError(f"canonical chunk hash_before mismatch: {unit_id}")

        masked_text = chunk.get("masked_text")
        protected_ids = chunk.get("protected_ids", [])
        if not isinstance(masked_text, str) or not isinstance(protected_ids, list):
            raise ValueError(f"invalid canonical chunk payload: {unit_id}")
        restored, restore_errors = restore_protected(masked_text, protected_ids, span_map)
        if restore_errors or restored != original:
            detail = ",".join(restore_errors) or "restored_text_mismatch"
            raise ValueError(f"canonical chunk source mismatch: {unit_id}:{detail}")

        derived_author_chars = _visible_author_chars(
            masked_text,
            file_suffixes.get(file_id, ""),
        )
        try:
            declared_author_chars = int(chunk.get("author_chars", -1))
        except (TypeError, ValueError) as error:
            raise ValueError(f"invalid canonical author_chars: {unit_id}") from error
        if declared_author_chars != derived_author_chars:
            raise ValueError(f"canonical author_chars mismatch: {unit_id}")
        if status == "SKIPPED_PROTECTED" and derived_author_chars != 0:
            raise ValueError(f"SKIPPED_PROTECTED has editable content: {unit_id}")
        if status == "PENDING" and derived_author_chars == 0:
            raise ValueError(f"PENDING has no editable content: {unit_id}")


def _finalize_locked(
    run_dir: Path,
    rewrites_dir: Path,
    *,
    check_command: str | None = None,
) -> dict[str, Any]:
    _verify_prepare_integrity(run_dir)
    snapshot = _load_json(run_dir / "snapshot.json")
    file_manifest = _load_csv(run_dir / "file_manifest.csv")
    units = _load_jsonl(run_dir / "units.jsonl")
    spans = _load_jsonl(run_dir / "protected_spans.jsonl")
    run_metadata = _load_json(run_dir / "run_metadata.json")
    frozen_voice_profile, voice_binding = _validate_voice_profile_binding(run_dir, run_metadata, units)
    _rebuild_prepare_state(run_dir, snapshot, file_manifest, run_metadata, units, spans)
    _validate_initial_unit_states(units)
    span_map = {item["protected_id"]: item for item in spans}
    unit_map = {item["unit_id"]: item for item in units}
    chunks: dict[str, dict[str, Any]] = {}
    for unit_id in unit_map:
        chunk = _load_json(run_dir / "chunks" / f"{unit_id}.json")
        if not isinstance(chunk, dict) or chunk.get("unit_id") != unit_id:
            raise ValueError(f"invalid chunk payload for {unit_id}")
        chunks[unit_id] = chunk
    rewrites = collect_rewrites(rewrites_dir)
    unknown_units = sorted(set(rewrites) - set(unit_map))
    if unknown_units:
        raise ValueError("unknown rewrite units: " + ",".join(unknown_units))

    validation_dir = run_dir / ".validation_staging"
    diffs_dir = run_dir / ".diffs_staging"
    staging_dir = run_dir / ".rendered_staging"
    for temporary in (validation_dir, diffs_dir, staging_dir):
        if temporary.exists():
            shutil.rmtree(temporary)
    validation_dir.mkdir()
    diffs_dir.mkdir()
    staging_dir.mkdir()

    existing_rendered_before = (run_dir / "rendered").is_dir()
    existing_partial_before = (run_dir / "rendered_partial").is_dir()
    previous_accepted_units: set[str] = set()
    previous_ledger_path = run_dir / "coverage_ledger.final.csv"
    previous_partial_state_missing = existing_partial_before and not previous_ledger_path.is_file()
    if existing_partial_before and previous_ledger_path.is_file():
        previous_accepted_units = {
            row["unit_id"]
            for row in _load_csv(previous_ledger_path)
            if row.get("status") in {"DONE", "NO_CHANGE"}
        }

    file_texts: dict[str, str] = {}
    file_raw: dict[str, bytes] = {}
    file_encoding: dict[str, str] = {}
    file_suffixes: dict[str, str] = {
        str(record["file_id"]): str(record.get("suffix", ""))
        for record in file_manifest
    }
    for record in file_manifest:
        if not record["snapshot_copy"] or record["status"] in {
            "UNRESOLVED",
            "UNRESOLVED_INCLUDE",
            "SKIPPED_GARBLED",
        }:
            continue
        raw = (run_dir / record["snapshot_copy"]).read_bytes()
        if sha256(raw) != record["sha256"]:
            raise ValueError(f"snapshot copy hash mismatch: {record['file_id']}")
        file_raw[record["file_id"]] = raw
        file_encoding[record["file_id"]] = record["encoding"]
        file_texts[record["file_id"]] = _decode(raw, record["encoding"])

    _validate_units_against_chunks(
        units,
        chunks,
        file_texts,
        file_suffixes,
        span_map,
    )
    expected_voice_units = {
        unit_id for unit_id, chunk in chunks.items() if str(chunk.get("status")) == "PENDING"
    }
    initial_processable_editable_units = len(expected_voice_units)
    expected_voice_sha256 = str(voice_binding["voice_profile_sha256"])
    voice_hash_matched_units: set[str] = set()
    voice_hash_missing_units: set[str] = set()
    voice_hash_mismatched_units: set[str] = set()
    chunk_binding_matched_units: set[str] = set()
    chunk_binding_missing_units: set[str] = set()
    chunk_binding_mismatched_units: set[str] = set()

    accepted_by_file: dict[str, list[tuple[int, int, str, str]]] = {}
    validation_payloads: dict[str, dict[str, Any]] = {}
    for unit_id, bundle in rewrites.items():
        unit = unit_map[unit_id]
        if unit["status"] != "PENDING":
            unit["notes"] = (unit.get("notes", "") + "; " if unit.get("notes") else "") + "rewrite_submitted_for_non_pending_unit"
            unit["status"] = "UNRESOLVED"
            continue
        decision = str(bundle.get("decision", "REWRITE")).upper()
        if decision not in {"REWRITE", "NO_CHANGE"}:
            unit["status"] = "UNRESOLVED"
            unit["notes"] = f"unsupported_decision:{decision}"
            continue
        try:
            _validate_rewrite_bundle_fields(bundle, decision)
            chunk_error = _bundle_chunk_binding_error(bundle, unit)
            if chunk_error:
                if chunk_error in {"bundle_unit_id_missing", "chunk_binding_hash_missing"}:
                    chunk_binding_missing_units.add(unit_id)
                else:
                    chunk_binding_mismatched_units.add(unit_id)
                unit["status"] = "UNRESOLVED"
                unit["notes"] = chunk_error
                continue
            chunk_binding_matched_units.add(unit_id)
            voice_error = _bundle_voice_binding_error(bundle, expected_voice_sha256)
            if voice_error:
                if voice_error == "voice_profile_hash_missing":
                    voice_hash_missing_units.add(unit_id)
                else:
                    voice_hash_mismatched_units.add(unit_id)
                unit["status"] = "UNRESOLVED"
                unit["notes"] = voice_error
                continue
            voice_hash_matched_units.add(unit_id)
            (
                warning_resolutions,
                warning_review_request_sha256,
                warning_reviewer_kind,
                warning_reviewer_id,
            ) = _warning_review_bundle(bundle)
        except ValueError as error:
            unit["status"] = "UNRESOLVED"
            unit["notes"] = f"invalid_warning_review:{error}"
            continue
        source_text = file_texts[unit["file_id"]]
        original = source_text[int(unit["start"]):int(unit["end"])]
        if sha256(original.encode("utf-8")) != unit["hash_before"]:
            unit["status"] = "CHANGED_AFTER_SNAPSHOT"
            unit["notes"] = "unit_source_hash_mismatch"
            continue
        if decision == "NO_CHANGE":
            reason = str(bundle.get("reason", "")).strip()
            if not _specific_reason(reason):
                unit["status"] = "UNRESOLVED"
                unit["notes"] = "NO_CHANGE requires a reason with at least 4 Chinese characters"
                continue
            no_change_keep = bundle.get("keep_reasons", {})
            if not isinstance(no_change_keep, dict):
                unit["status"] = "UNRESOLVED"
                unit["notes"] = "NO_CHANGE keep_reasons must be an object"
                continue
            try:
                valid_signal_ids = {
                    item["id"] for item in output_validator.lexical.load_lexicon()["signals"]
                }
                no_change_keep = output_validator._parse_keep_reasons(
                    [f"{key}={value}" for key, value in no_change_keep.items()],
                    valid_signal_ids,
                )
            except ValueError as error:
                unit["status"] = "UNRESOLVED"
                unit["notes"] = f"invalid_NO_CHANGE_keep_reason:{error}"
                continue
            suffix = Path(next(item["path"] for item in file_manifest if item["file_id"] == unit["file_id"])).suffix or ".txt"
            before_path = validation_dir / f"{unit_id}.before{suffix}"
            after_path = validation_dir / f"{unit_id}.after{suffix}"
            before_path.write_text(original, encoding="utf-8")
            after_path.write_text(original, encoding="utf-8")
            try:
                no_change_payload = output_validator.validate(
                    before_path,
                    after_path,
                    scene=unit["scene"],
                    keep_reasons=no_change_keep,
                    warning_resolutions=warning_resolutions,
                    warning_review_request_sha256=warning_review_request_sha256,
                    warning_reviewer_kind=warning_reviewer_kind,
                    warning_reviewer_id=warning_reviewer_id,
                    fragment_mode=True,
                )
            except ValueError as error:
                unit["status"] = "UNRESOLVED"
                unit["notes"] = f"invalid_warning_proposal:{error}"
                continue
            validation_payloads[unit_id] = no_change_payload
            _write_json(validation_dir / f"{unit_id}.validation.json", no_change_payload)
            if no_change_payload["status"] != "PASS":
                unit["status"] = "UNRESOLVED"
                unit["style_validation"] = no_change_payload["status"]
                unit["notes"] = "NO_CHANGE validator:" + no_change_payload["status"]
                continue
            unit["status"] = "NO_CHANGE"
            unit["hash_after"] = unit["hash_before"]
            unit["protected_hashes_ok"] = "PASS"
            unit["style_validation"] = "PASS"
            unit["notes"] = reason
            continue

        masked_text = bundle.get("masked_text")
        if not isinstance(masked_text, str):
            unit["status"] = "UNRESOLVED"
            unit["notes"] = "missing masked_text"
            continue
        restored, restore_errors = restore_protected(masked_text, unit["protected_ids"], span_map)
        if restored is None:
            unit["status"] = "UNRESOLVED"
            unit["protected_hashes_ok"] = "FAIL"
            unit["notes"] = " | ".join(restore_errors)
            continue
        protected_count_changes = _protected_content_count_changes(
            original,
            restored,
            unit["protected_ids"],
            span_map,
        )
        if protected_count_changes:
            unit["status"] = "UNRESOLVED"
            unit["protected_hashes_ok"] = "FAIL"
            unit["notes"] = "protected_content_count_changed:" + ",".join(protected_count_changes)
            continue
        copied_context = _copied_read_only_context(original, restored, chunks[unit_id])
        if copied_context:
            unit["status"] = "UNRESOLVED"
            unit["notes"] = "read_only_context_copied:" + ",".join(copied_context)
            continue
        if restored == original:
            unit["status"] = "UNRESOLVED"
            unit["notes"] = "REWRITE bundle is identical; use explicit NO_CHANGE with reason"
            continue

        suffix = Path(next(item["path"] for item in file_manifest if item["file_id"] == unit["file_id"])).suffix or ".txt"
        before_path = validation_dir / f"{unit_id}.before{suffix}"
        after_path = validation_dir / f"{unit_id}.after{suffix}"
        before_path.write_text(original, encoding="utf-8")
        after_path.write_text(restored, encoding="utf-8")
        keep_reasons = bundle.get("keep_reasons", {})
        if not isinstance(keep_reasons, dict):
            unit["status"] = "UNRESOLVED"
            unit["notes"] = "keep_reasons must be an object"
            continue
        try:
            valid_signal_ids = {
                item["id"] for item in output_validator.lexical.load_lexicon()["signals"]
            }
            keep_reasons = output_validator._parse_keep_reasons(
                [f"{key}={value}" for key, value in keep_reasons.items()],
                valid_signal_ids,
            )
        except ValueError as error:
            unit["status"] = "UNRESOLVED"
            unit["notes"] = f"invalid_keep_reason:{error}"
            continue
        try:
            payload = output_validator.validate(
                before_path,
                after_path,
                scene=unit["scene"],
                keep_reasons=keep_reasons,
                warning_resolutions=warning_resolutions,
                warning_review_request_sha256=warning_review_request_sha256,
                warning_reviewer_kind=warning_reviewer_kind,
                warning_reviewer_id=warning_reviewer_id,
                fragment_mode=True,
            )
        except ValueError as error:
            unit["status"] = "UNRESOLVED"
            unit["notes"] = f"invalid_warning_proposal:{error}"
            continue
        validation_payloads[unit_id] = payload
        _write_json(validation_dir / f"{unit_id}.validation.json", payload)
        unit["style_validation"] = payload["status"]
        unit["protected_hashes_ok"] = "PASS" if not payload["invariants"]["hard_failure"] else "FAIL"
        if payload["status"] != "PASS":
            unit["status"] = "UNRESOLVED"
            unit["notes"] = "validator:" + payload["status"] + ":" + ",".join(payload["review_reasons"])
            continue

        diff = "".join(
            difflib.unified_diff(
                original.splitlines(keepends=True),
                restored.splitlines(keepends=True),
                fromfile=f"{unit_id}.before",
                tofile=f"{unit_id}.after",
            )
        )
        diff_path = diffs_dir / f"{unit_id}.diff"
        diff_path.write_text(diff, encoding="utf-8")
        unit["status"] = "DONE"
        unit["hash_after"] = sha256(restored.encode("utf-8"))
        unit["diff_path"] = str(Path("diffs") / diff_path.name)
        accepted_by_file.setdefault(unit["file_id"], []).append(
            (int(unit["start"]), int(unit["end"]), restored, unit_id)
        )

    preliminary_style_records = [
        {
            "unit_id": unit_id,
            "scene": unit.get("scene", ""),
            "expected": unit_id in expected_voice_units,
            "state": unit.get("status", ""),
            "style_validation": unit.get("style_validation", ""),
            "before_masked": chunks[unit_id].get("masked_text", ""),
            "after_masked": (
                chunks[unit_id].get("masked_text", "")
                if unit.get("status") == "NO_CHANGE"
                else rewrites.get(unit_id, {}).get("masked_text")
                if unit.get("status") == "DONE"
                else None
            ),
        }
        for unit in units
        for unit_id in [str(unit["unit_id"])]
        if unit_id in expected_voice_units
    ]
    cross_unit_repetition = _audit_cross_unit_repetition(preliminary_style_records)
    _write_json(validation_dir / "cross_unit_repetition.json", cross_unit_repetition)
    blocked_by_repetition = set(cross_unit_repetition["blocking_unit_ids"])
    if blocked_by_repetition:
        for unit_id in sorted(blocked_by_repetition):
            unit = unit_map[unit_id]
            if unit.get("status") not in {"DONE", "NO_CHANGE"}:
                continue
            unit["status"] = "UNRESOLVED"
            unit["hash_after"] = ""
            unit["diff_path"] = ""
            unit["notes"] = (
                (str(unit.get("notes", "")) + "; ") if unit.get("notes") else ""
            ) + "cross_unit_repetition:introduced_template_family"
            diff_path = diffs_dir / f"{unit_id}.diff"
            if diff_path.exists():
                diff_path.unlink()
        for file_id, changes in list(accepted_by_file.items()):
            remaining = [item for item in changes if item[3] not in blocked_by_repetition]
            if remaining:
                accepted_by_file[file_id] = remaining
            else:
                accepted_by_file.pop(file_id, None)

    rendered_texts: dict[str, str] = dict(file_texts)
    for file_id, changes in accepted_by_file.items():
        text = rendered_texts[file_id]
        for start, end, replacement, _ in sorted(changes, key=lambda item: item[0], reverse=True):
            text = text[:start] + replacement + text[end:]
        rendered_texts[file_id] = text

    relative_paths = _relative_render_paths(file_manifest)
    rendered_manifest: list[dict[str, Any]] = []
    full_format_errors: list[dict[str, Any]] = []
    for record in file_manifest:
        file_id = record["file_id"]
        if file_id not in rendered_texts:
            continue
        relative = relative_paths[file_id]
        destination = staging_dir / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        raw = _encode(rendered_texts[file_id], file_encoding[file_id], file_raw[file_id])
        destination.write_bytes(raw)
        document_format = "tex" if Path(record["path"]).suffix.lower() in {".tex", ".ltx"} else "markdown"
        full_check = invariants.check_documents(
            file_texts[file_id],
            rendered_texts[file_id],
            document_format=document_format,
        )
        if full_check.errors:
            full_format_errors.append({"file_id": file_id, "errors": full_check.to_dict()["errors"]})
        rendered_manifest.append(
            {
                "file_id": file_id,
                "source_path": record["path"],
                "rendered_path": str(relative).replace("\\", "/"),
                "sha256": sha256(raw),
                "bytes": len(raw),
                "format_check": "FAIL" if full_check.errors else "PASS",
            }
        )

    statuses = Counter(str(unit["status"]) for unit in units)
    file_statuses = Counter(str(record["status"]) for record in file_manifest)
    pending = statuses.get("PENDING", 0) + statuses.get("IN_PROGRESS", 0)
    unresolved_units = sum(statuses.get(status, 0) for status in ("UNRESOLVED", "SKIPPED_GARBLED", "CHANGED_AFTER_SNAPSHOT"))
    unresolved_files = sum(
        file_statuses.get(status, 0)
        for status in ("UNRESOLVED", "UNRESOLVED_INCLUDE", "SKIPPED_GARBLED", "CHANGED_AFTER_SNAPSHOT")
    )
    source_changes_before_compile = _source_changes(file_manifest)
    run_state_before_compile = _run_state_hashes(run_dir)
    staging_hashes_before_compile = _directory_hashes(staging_dir)
    evidence_staging_hashes_before_compile = {
        "validation": _directory_hashes(validation_dir),
        "diffs": _directory_hashes(diffs_dir),
    }
    if source_changes_before_compile:
        compile_result = _compile_check_result(
            status="NOT_RUN_DUE_TO_SOURCE_CHANGE",
            command=check_command or "",
        )
    elif full_format_errors:
        compile_result = _compile_check_result(
            status="NOT_RUN_DUE_TO_FORMAT_FAILURE",
            command=check_command or "",
        )
    else:
        compile_workspace = run_dir / ".compile_check_staging"
        _copy_for_check(staging_dir, compile_workspace)
        try:
            compile_result = _run_compile(check_command, compile_workspace)
        finally:
            shutil.rmtree(compile_workspace, ignore_errors=True)

        staging_hashes_after_compile = _directory_hashes(staging_dir)
        evidence_staging_hashes_after_compile = {
            "validation": _directory_hashes(validation_dir),
            "diffs": _directory_hashes(diffs_dir),
        }
        run_state_after_compile = _run_state_hashes(run_dir)
        integrity_changes: dict[str, Any] = {}
        if staging_hashes_after_compile != staging_hashes_before_compile:
            integrity_changes["staging"] = {
                "before": staging_hashes_before_compile,
                "after": staging_hashes_after_compile,
            }
        if evidence_staging_hashes_after_compile != evidence_staging_hashes_before_compile:
            integrity_changes["evidence_staging"] = {
                "before": evidence_staging_hashes_before_compile,
                "after": evidence_staging_hashes_after_compile,
            }
        if run_state_after_compile != run_state_before_compile:
            integrity_changes["run_dir"] = {
                "before": run_state_before_compile,
                "after": run_state_after_compile,
            }
        if integrity_changes:
            compile_result["status"] = "FAIL"
            compile_result["integrity_status"] = "FAIL"
            compile_result["integrity_changes"] = integrity_changes
        else:
            compile_result["integrity_status"] = "PASS"
    source_changes = _source_changes(file_manifest)
    compile_or_concurrent_source_change = not source_changes_before_compile and bool(source_changes)
    processable_editable_units = initial_processable_editable_units
    empty_processable_scope = not file_manifest or not units or processable_editable_units == 0
    unresolved = unresolved_units + unresolved_files + len(source_changes) + (1 if empty_processable_scope else 0)

    hard_failure = (
        bool(full_format_errors)
        or compile_result["status"] == "FAIL"
        or compile_or_concurrent_source_change
    )
    discard_staged_evidence = bool(
        compile_result.get("integrity_changes", {}).get("evidence_staging")
    )
    current_accepted_units = {
        unit["unit_id"] for unit in units if unit["status"] in {"DONE", "NO_CHANGE"}
    }
    partial_regression_units = sorted(previous_accepted_units - current_accepted_units)
    partial_regression = existing_partial_before and (
        previous_partial_state_missing or bool(partial_regression_units)
    )
    if partial_regression:
        hard_failure = True
    complete = pending == 0 and not empty_processable_scope
    publish_name = "rendered" if complete and unresolved == 0 and not hard_failure else "rendered_partial"
    publish_dir = run_dir / publish_name
    idempotency = "NOT_RUN"
    preserve_published_evidence = False
    if partial_regression:
        rejected_dir = run_dir / "non_cumulative_staging"
        if rejected_dir.exists():
            shutil.rmtree(rejected_dir)
        staging_dir.rename(rejected_dir)
        published_path = str(run_dir / "rendered_partial")
        idempotency = "FAIL"
        preserve_published_evidence = True
    elif hard_failure:
        failed_dir = run_dir / "failed_staging"
        if failed_dir.exists():
            shutil.rmtree(failed_dir)
        staging_dir.rename(failed_dir)
        published_path = ""
        preserve_published_evidence = existing_rendered_before or existing_partial_before
    elif publish_dir.exists():
        if _directory_hashes(publish_dir) == _directory_hashes(staging_dir):
            idempotency = "PASS"
            shutil.rmtree(staging_dir)
            published_path = str(publish_dir)
        elif publish_name == "rendered_partial":
            history_path = run_dir / "partial_history.jsonl"
            history = {
                "replaced_at": utc_now(),
                "old_hashes": _directory_hashes(publish_dir),
                "new_hashes": _directory_hashes(staging_dir),
                "reason": "additional_or_revised_unit_bundles",
            }
            with history_path.open("a", encoding="utf-8", newline="") as handle:
                handle.write(json.dumps(history, ensure_ascii=False, sort_keys=True) + "\n")
            shutil.rmtree(publish_dir)
            staging_dir.rename(publish_dir)
            idempotency = "NOT_APPLICABLE_PROGRESS"
            published_path = str(publish_dir)
        else:
            different_dir = run_dir / "non_idempotent_staging"
            if different_dir.exists():
                shutil.rmtree(different_dir)
            staging_dir.rename(different_dir)
            idempotency = "FAIL"
            hard_failure = True
            published_path = str(publish_dir)
            preserve_published_evidence = True
    else:
        staging_dir.rename(publish_dir)
        published_path = str(publish_dir)

    stale_partial = run_dir / "rendered_partial"
    if not hard_failure and publish_name == "rendered" and stale_partial.exists():
        history_path = run_dir / "partial_history.jsonl"
        history = {
            "replaced_at": utc_now(),
            "old_hashes": _directory_hashes(stale_partial),
            "new_hashes": _directory_hashes(publish_dir),
            "reason": "full_terminal_coverage_published",
        }
        with history_path.open("a", encoding="utf-8", newline="") as handle:
            handle.write(json.dumps(history, ensure_ascii=False, sort_keys=True) + "\n")
        shutil.rmtree(stale_partial)

    if preserve_published_evidence or discard_staged_evidence:
        shutil.rmtree(validation_dir)
        shutil.rmtree(diffs_dir)
    else:
        _commit_evidence_directory(validation_dir, run_dir / "validation")
        _commit_evidence_directory(diffs_dir, run_dir / "diffs")
        _write_csv(run_dir / "coverage_ledger.final.csv", units, LEDGER_FIELDS)
        _write_csv(
            run_dir / "rendered_manifest.csv",
            rendered_manifest,
            ("file_id", "source_path", "rendered_path", "sha256", "bytes", "format_check"),
        )
    rollback = {
        "source_untouched": True,
        "snapshot_id": snapshot["snapshot_id"],
        "rollback_basis": "source/ snapshot copies and per-unit diffs",
        "published_path": published_path,
        "hard_failure": hard_failure,
        "action_on_failure": "Discard failed_staging/non_idempotent_staging; no source restoration is required.",
    }
    if not preserve_published_evidence and not discard_staged_evidence:
        _write_json(run_dir / "rollback_manifest.json", rollback)

    if hard_failure:
        status, exit_code = "FAIL", 1
    elif pending or unresolved:
        status, exit_code = "REVIEW", 2
    else:
        status, exit_code = "PASS", 0
    coverage_completion_claim_allowed = complete and unresolved == 0 and not hard_failure
    scene_routing_status = (
        "PASS"
        if units and all(str(unit.get("scene", "")).upper() in {"GENERAL", "COURSE", "MODELING", "RESEARCH"} for unit in units)
        else "NOT_EVALUATED"
    )
    voice_hash_missing_units.update(
        expected_voice_units - voice_hash_matched_units - voice_hash_mismatched_units
    )
    chunk_binding_missing_units.update(
        expected_voice_units
        - chunk_binding_matched_units
        - chunk_binding_mismatched_units
    )
    if not expected_voice_units:
        voice_binding_status = "NOT_EVALUATED"
    elif voice_hash_matched_units == expected_voice_units:
        voice_binding_status = "PASS"
    else:
        voice_binding_status = "REVIEW"
    if not expected_voice_units:
        rewrite_binding_status = "NOT_EVALUATED"
    elif chunk_binding_matched_units == expected_voice_units:
        rewrite_binding_status = "PASS"
    else:
        rewrite_binding_status = "REVIEW"
    style_records = [
        {
            "unit_id": unit_id,
            "scene": unit.get("scene", ""),
            "expected": unit_id in expected_voice_units,
            "state": unit.get("status", ""),
            "style_validation": unit.get("style_validation", ""),
            "before_masked": chunks[unit_id].get("masked_text", ""),
            "after_masked": (
                chunks[unit_id].get("masked_text", "")
                if unit.get("status") == "NO_CHANGE"
                else rewrites.get(unit_id, {}).get("masked_text")
                if unit.get("status") == "DONE"
                else None
            ),
        }
        for unit in units
        for unit_id in [str(unit["unit_id"])]
        if unit_id in expected_voice_units
    ]
    voice_conformance = _audit_voice_conformance(
        frozen_voice_profile,
        style_records,
        scene_routing_status=scene_routing_status,
    )
    voice_conformance_status = str(voice_conformance["status"])
    cross_unit_repetition_status = str(cross_unit_repetition["status"])
    humanize_second_pass_convergence = "NOT_RUN"
    voice_completion_claim_allowed = bool(
        coverage_completion_claim_allowed
        and scene_routing_status == "PASS"
        and voice_binding_status == "PASS"
        and rewrite_binding_status == "PASS"
        and voice_conformance_status == "PASS"
    )
    humanize_completion_claim_allowed = bool(
        voice_completion_claim_allowed
        and cross_unit_repetition_status == "PASS"
        and humanize_second_pass_convergence == "PASS"
    )
    metadata = {
        "tool": "finalize_humanize_long_document.py",
        "created_at": utc_now(),
        "snapshot_id": snapshot["snapshot_id"],
        "status": status,
        "exit_code": exit_code,
        "units_total": len(units),
        "processable_editable_units": processable_editable_units,
        "unit_statuses": dict(sorted(statuses.items())),
        "file_statuses": dict(sorted(file_statuses.items())),
        "rewrites_submitted": len(rewrites),
        "validation_results": {
            key: value["status"] for key, value in sorted(validation_payloads.items())
        },
        "full_format_errors": full_format_errors,
        "compile_check": compile_result,
        "published_path": published_path,
        "idempotency": idempotency,
        "assembly_replay_idempotency": idempotency,
        "humanize_second_pass_convergence": humanize_second_pass_convergence,
        "processable_scope_complete": complete,
        "empty_processable_scope": empty_processable_scope,
        "coverage_completion_claim_allowed": coverage_completion_claim_allowed,
        "scene_routing_status": scene_routing_status,
        "voice_profile_sha256": expected_voice_sha256,
        "voice_profile_manifest_sha256": frozen_voice_profile["sample_binding"]["manifest_sha256"],
        "voice_profile_bindings_total": len(expected_voice_units),
        "voice_profile_bindings_matched": len(voice_hash_matched_units),
        "voice_profile_bindings_missing": len(voice_hash_missing_units),
        "voice_profile_bindings_mismatched": len(voice_hash_mismatched_units),
        "voice_profile_default_units": sum(
            1 for unit in units if str(unit.get("voice_profile_source")) == "SCENE_DEFAULT"
        ),
        "voice_profile_default_scenes": sorted(
            {
                str(unit.get("scene", ""))
                for unit in units
                if str(unit.get("voice_profile_source")) == "SCENE_DEFAULT"
            }
        ),
        "voice_default_disclosure_required": bool(voice_binding.get("voice_default_disclosure")),
        "voice_binding_status": voice_binding_status,
        "rewrite_binding_status": rewrite_binding_status,
        "rewrite_bindings_total": len(expected_voice_units),
        "rewrite_bindings_matched": len(chunk_binding_matched_units),
        "rewrite_bindings_missing": len(chunk_binding_missing_units),
        "rewrite_bindings_mismatched": len(chunk_binding_mismatched_units),
        "voice_conformance_status": voice_conformance_status,
        "cross_unit_repetition_status": cross_unit_repetition_status,
        "voice_conformance": voice_conformance,
        "cross_unit_repetition": cross_unit_repetition,
        "voice_completion_claim_allowed": voice_completion_claim_allowed,
        "humanize_completion_claim_allowed": humanize_completion_claim_allowed,
        "full_completion_claim_allowed": humanize_completion_claim_allowed,
        "source_files_modified": len(source_changes),
        "source_files_modified_by_tool": 0 if not source_changes else None,
        "source_files_changed_since_snapshot": len(source_changes),
        "source_change_details": source_changes,
        "source_changes_before_compile": len(source_changes_before_compile),
        "source_changed_during_compile_or_finalize": compile_or_concurrent_source_change,
        "run_artifacts_changed_during_check": bool(compile_result.get("integrity_changes", {}).get("run_dir")),
        "staging_artifacts_changed_during_check": bool(compile_result.get("integrity_changes", {}).get("staging")),
        "evidence_artifacts_changed_during_check": bool(
            compile_result.get("integrity_changes", {}).get("evidence_staging")
        ),
        "partial_regression_units": partial_regression_units,
        "previous_partial_state_missing": previous_partial_state_missing,
        "published_evidence_preserved": preserve_published_evidence,
        "staged_evidence_discarded": discard_staged_evidence,
    }
    _write_json(run_dir / "finalization_metadata.json", metadata)
    return metadata


def finalize(
    run_dir: Path,
    rewrites_dir: Path,
    *,
    check_command: str | None = None,
) -> dict[str, Any]:
    run_dir = Path(run_dir)
    rewrites_dir = Path(rewrites_dir)
    with _run_lock(run_dir):
        return _finalize_locked(run_dir, rewrites_dir, check_command=check_command)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="验证长文单元改写、恢复保护区、生成逐节 diff 与派生稿；从不覆盖源文件。"
    )
    parser.add_argument("--run-dir", type=Path, required=True, help="prepare 命令的输出目录")
    parser.add_argument("--rewrites", type=Path, required=True, help="按 unit_id 命名的 .json/.txt 改写目录")
    parser.add_argument("--check-command", help="可选项目编译/格式命令，在 staging 根目录执行")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        metadata = finalize(
            args.run_dir.resolve(),
            args.rewrites.resolve(),
            check_command=args.check_command,
        )
    except (OSError, UnicodeError, ValueError, json.JSONDecodeError) as error:
        parser.error(str(error))
    print(json.dumps(metadata, ensure_ascii=False, indent=2, sort_keys=True))
    return int(metadata["exit_code"])


if __name__ == "__main__":
    raise SystemExit(main())
