#!/usr/bin/env python3
"""Validate and assemble long-document humanization units without touching sources."""

from __future__ import annotations

import argparse
import csv
import difflib
import hashlib
import importlib.util
import json
import os
import re
import shutil
import signal
import stat
import subprocess
import sys
import tempfile
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
import load_humanize_negative_guards as negative_guards  # noqa: E402


PLACEHOLDER_RE = re.compile(r"\[\[PROTECTED:(?P<id>[^:\]]+):(?P<hash>[0-9a-f]{12})\]\]")
HAN_RE = re.compile(r"[\u3400-\u9fff]")
SAFE_UNIT_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]{0,127}$")
TEX_COMMAND_TOKEN_RE = re.compile(r"\\[A-Za-z@]+\*?|\\[^A-Za-z\s]")
TERMINAL_STATUSES = {
    "DONE",
    "NO_CHANGE",
    "SKIPPED_PROTECTED",
    "SKIPPED_GARBLED",
    "UNRESOLVED",
    "CHANGED_AFTER_SNAPSHOT",
}
SECOND_PASS_RECEIPT_SCHEMA = "humanize-second-pass-convergence-receipt/v2"
STRUCTURAL_SEMANTIC_REVIEW_REQUEST_SCHEMA = (
    "humanize-structural-semantic-review-request/v1"
)
STRUCTURAL_TRANSACTION_BUNDLE_SCHEMA = "humanize-structural-transaction-bundle/v1"
STRUCTURAL_TRANSACTION_DECLINE_SCHEMA = "humanize-structural-transaction-decline/v1"
STRUCTURAL_TRANSACTION_REVIEW_REQUEST_SCHEMA = (
    "humanize-structural-transaction-review-request/v1"
)
STRUCTURAL_TRANSACTION_DECLINE_REASON_CODES = {
    "NO_CROSS_UNIT_STYLE_GAIN",
    "DEPENDENCY_OR_REFERENT_RISK",
    "CLAIM_EVIDENCE_ORDER_RISK",
    "QUESTION_ANSWER_PAIRING_RISK",
    "PROTECTED_BOUNDARY_RISK",
    "USER_SCOPE_LOCK",
    "MEMBER_COMMITTED_TO_OTHER_TRANSACTION",
    "OTHER_REVIEWED_NO_CHANGE",
}
SCAFFOLD_METADATA_NAME = "scaffold_metadata.json"
SCAFFOLD_METADATA_SCHEMAS = {
    "humanize-rewrite-scaffold/v1",
    "humanize-rewrite-scaffold/v2",
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
    if not isinstance(manifest, dict):
        raise ValueError("invalid prepare_integrity.json")
    if manifest.get("schema_version") == preparer.PREPARE_INTEGRITY_SCHEMA_VERSION:
        preparer.validate_integrity_manifest(run_dir, manifest)
        return
    if manifest.get("schema_version") != 1:
        raise ValueError("invalid prepare_integrity.json")
    if set(manifest) != {"schema_version", "artifacts"}:
        raise ValueError("invalid legacy prepare_integrity.json")
    if (run_dir / "structural_transaction_inventory.json").exists():
        raise ValueError("legacy prepare integrity cannot authorize transactions")
    metadata_path = run_dir / "run_metadata.json"
    if metadata_path.is_file():
        legacy_metadata = _load_json(metadata_path)
        if isinstance(legacy_metadata, dict) and any(
            str(key).startswith("structural_transaction_") for key in legacy_metadata
        ):
            raise ValueError("legacy prepare metadata cannot authorize transactions")
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
            run_dir / "scene_routing_policy.json",
            *[
                path
                for path in (
                    run_dir / "voice_profile.json",
                    run_dir / "voice_profile_set.json",
                    run_dir / "voice_sample_manifest.json",
                    run_dir / "voice_sample_spec.json",
                )
                if path.is_file()
            ],
            *(
                sorted(
                    (run_dir / "voice_profiles").glob("*.json"),
                    key=lambda item: item.name.casefold(),
                )
                if (run_dir / "voice_profiles").is_dir()
                else []
            ),
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


def _validate_second_pass_receipt(
    receipt_path: Path,
    *,
    snapshot_id: str,
    rendered_root: Path,
    rendered_manifest_path: Path,
    voice_profile_sha256: str,
    scene: str,
) -> dict[str, Any]:
    raise ValueError(
        "second-pass control-plane verification is unavailable in generator projection"
    )


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

AUTO_VOICE_BINDING_FIELDS = {
    "mode",
    "requested_scene",
    "scene_binding_status",
    "profile_source",
    "profile_set_sha256",
    "voice_default_disclosure",
    "voice_evidence_status",
    "profiles",
}
PROFILE_SET_ENTRY_FIELDS = {
    "path",
    "profile_id",
    "revision",
    "profile_kind",
    "binding_scene",
    "profile_sha256",
}
SINGLE_VOICE_BINDING_FIELDS = {
    "profile_source",
    "source_path",
    "binding_scene",
    "profile_binding_scene",
    "voice_profile_binding_scene",
    "requested_scene",
    "scene_binding_status",
    "voice_profile_id",
    "voice_profile_revision",
    "voice_profile_confidence",
    "voice_profile_kind",
    "voice_profile_sha256",
    "voice_default_disclosure",
    "voice_evidence_status",
}


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
) -> tuple[dict[str, dict[str, Any]], dict[str, dict[str, Any]], dict[str, Any]]:
    """Validate frozen single/Profile-set bindings independently of the seal."""
    requested_scene = str(metadata.get("scene", "")).upper()
    if requested_scene not in {"AUTO", "COURSE", "MODELING", "RESEARCH", "GENERAL"}:
        raise ValueError("run metadata scene is invalid")
    metadata_binding = metadata.get("voice_binding")
    if not isinstance(metadata_binding, dict):
        raise ValueError("run_metadata.json has no voice_binding")

    if requested_scene == "AUTO":
        if set(metadata_binding) != AUTO_VOICE_BINDING_FIELDS:
            raise ValueError("voice Profile set metadata keys mismatch")
        profile_set_path = run_dir / "voice_profile_set.json"
        if not profile_set_path.is_file():
            raise ValueError("missing voice_profile_set.json")
        profile_set = _load_json(profile_set_path)
        if not isinstance(profile_set, dict):
            raise ValueError("voice Profile set must be an object")
        expected_set_keys = {
            "schema_version",
            "requested_scene",
            "profile_source",
            "profiles",
            "claims",
            "profile_set_sha256",
        }
        if set(profile_set) != expected_set_keys:
            raise ValueError("voice Profile set keys mismatch")
        if (
            profile_set.get("schema_version") != "humanize-voice-profile-set/v1"
            or profile_set.get("requested_scene") != "AUTO"
            or profile_set.get("profile_source") != "SCENE_DEFAULT_SET"
        ):
            raise ValueError("voice Profile set identity is invalid")
        if profile_set.get("claims") != {
            "personal_voice_claim_allowed": False,
            "identity_verified": False,
        }:
            raise ValueError("voice Profile set claims exceed the local trust boundary")
        set_payload = dict(profile_set)
        declared_set_sha = set_payload.pop("profile_set_sha256", None)
        actual_set_sha = sha256(_canonical_json(set_payload).encode("utf-8"))
        if declared_set_sha != actual_set_sha:
            raise ValueError("voice Profile set self-hash mismatch")
        if (
            metadata_binding.get("mode") != "PROFILE_SET"
            or metadata_binding.get("requested_scene") != "AUTO"
            or metadata_binding.get("scene_binding_status") != "UNIT_ROUTED"
            or metadata_binding.get("profile_source") != "SCENE_DEFAULT_SET"
            or metadata_binding.get("profile_set_sha256") != actual_set_sha
            or metadata_binding.get("voice_evidence_status") != "DETERMINISTIC_DEFAULT_SET"
        ):
            raise ValueError("voice Profile set metadata mismatch")
        entries = profile_set.get("profiles")
        expected_scenes = {"GENERAL", "COURSE", "MODELING", "RESEARCH"}
        if not isinstance(entries, dict) or set(entries) != expected_scenes:
            raise ValueError("voice Profile set scenes mismatch")
        binding_entries = metadata_binding.get("profiles")
        if not isinstance(binding_entries, dict) or set(binding_entries) != expected_scenes:
            raise ValueError("voice Profile set binding entries mismatch")
        profiles: dict[str, dict[str, Any]] = {}
        bindings: dict[str, dict[str, Any]] = {}
        for scene in sorted(expected_scenes):
            entry = entries[scene]
            if not isinstance(entry, dict):
                raise ValueError(f"voice Profile set entry is invalid: {scene}")
            if set(entry) != PROFILE_SET_ENTRY_FIELDS:
                raise ValueError(f"voice Profile set entry keys mismatch: {scene}")
            expected_path = f"voice_profiles/{scene.lower()}.json"
            if entry.get("path") != expected_path:
                raise ValueError(f"voice Profile set path mismatch: {scene}")
            profile = voice_profiles.load_and_validate_profile(run_dir / expected_path)
            if profile.get("validation_status") != "PASS":
                raise ValueError(f"frozen voice Profile status is not PASS: {scene}")
            if (
                str(profile.get("binding_scene", "")).upper() != scene
                or profile.get("profile_kind") != "DEFAULT"
                or profile.get("profile_sha256") != entry.get("profile_sha256")
                or profile.get("profile_id") != entry.get("profile_id")
                or profile.get("revision") != entry.get("revision")
                or profile.get("profile_kind") != entry.get("profile_kind")
                or profile.get("binding_scene") != entry.get("binding_scene")
            ):
                raise ValueError(f"voice Profile set entry mismatch: {scene}")
            rebuilt = voice_profiles.build_scene_default_profile(scene)
            if _canonical_json(rebuilt) != _canonical_json(profile):
                raise ValueError(f"scene default voice profile differs from registry: {scene}")
            binding = binding_entries[scene]
            if not isinstance(binding, dict):
                raise ValueError(f"voice Profile binding is invalid: {scene}")
            expected_binding = preparer._voice_binding_from_profile(
                profile,
                requested_scene="AUTO",
                profile_source="SCENE_DEFAULT",
                source_path=expected_path,
                evidence_status="DETERMINISTIC_DEFAULT",
            )
            if _canonical_json(binding) != _canonical_json(expected_binding):
                raise ValueError(f"voice Profile binding mismatch: {scene}")
            profiles[scene] = profile
            bindings[scene] = binding
        for unit in units:
            scene = str(unit.get("scene", "")).upper()
            if scene not in bindings:
                raise ValueError(f"voice binding unit has invalid scene: {unit.get('unit_id', '')}")
            binding = bindings[scene]
            for key in VOICE_UNIT_FIELDS:
                expected = (
                    binding["profile_source"]
                    if key == "voice_profile_source"
                    else binding.get(key)
                )
                if unit.get(key) != expected:
                    raise ValueError(
                        f"voice binding unit mismatch: {unit.get('unit_id', '')}:{key}"
                    )
        return profiles, bindings, {
            "mode": "PROFILE_SET",
            "identity_sha256": actual_set_sha,
            "profile_set_sha256": actual_set_sha,
            "voice_profile_sha256": "",
            "voice_profile_manifest_sha256": "0" * 64,
            "voice_default_disclosure": True,
        }

    profile_path = run_dir / "voice_profile.json"
    if not profile_path.is_file():
        raise ValueError("missing voice_profile.json")
    profile = voice_profiles.load_and_validate_profile(profile_path)
    if profile.get("validation_status") != "PASS":
        raise ValueError("frozen voice Profile status is not PASS")
    binding = metadata_binding
    if set(binding) != SINGLE_VOICE_BINDING_FIELDS:
        raise ValueError("voice binding metadata keys mismatch")
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
    if (
        str(binding.get("requested_scene", "")).upper() != requested_scene
        or str(binding.get("scene_binding_status", ""))
        != "BOUND"
        or str(binding.get("profile_binding_scene", "")).upper() != profile_scene
        or str(binding.get("voice_profile_binding_scene", "")).upper() != profile_scene
        or str(binding.get("binding_scene", "")).upper() != profile_scene
        or profile_scene != requested_scene
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
    return {requested_scene: profile}, {requested_scene: binding}, {
        "mode": "SINGLE",
        "identity_sha256": str(profile["profile_sha256"]),
        "profile_set_sha256": "",
        "voice_profile_sha256": str(profile["profile_sha256"]),
        "voice_profile_manifest_sha256": str(
            profile.get("sample_binding", {}).get("manifest_sha256", "")
        ),
        "voice_default_disclosure": bool(binding.get("voice_default_disclosure")),
    }


def _bundle_voice_binding_error(bundle: dict[str, Any], expected_sha256: str) -> str | None:
    if "voice_profile_sha256" not in bundle:
        return "voice_profile_hash_missing"
    value = bundle.get("voice_profile_sha256")
    if not isinstance(value, str) or not re.fullmatch(r"[0-9a-f]{64}", value):
        return "voice_profile_hash_invalid"
    if value != expected_sha256:
        return "voice_profile_hash_mismatch"
    return None


def _validate_scene_routing_policy(run_dir: Path, metadata: dict[str, Any]) -> Path:
    frozen_path = run_dir / "scene_routing_policy.json"
    frozen, frozen_sha = preparer.scene_router.load_policy(frozen_path)
    current, current_sha = preparer.scene_router.load_policy()
    if _canonical_json(frozen) != _canonical_json(current) or frozen_sha != current_sha:
        raise ValueError("scene routing policy changed after prepare")
    if (
        metadata.get("scene_routing_policy_sha256") != current_sha
        or metadata.get("scene_routing_policy_revision") != current.get("revision")
    ):
        raise ValueError("scene routing policy metadata mismatch")
    return preparer.scene_router.DEFAULT_POLICY


def _validate_structural_transaction_inventory(
    run_dir: Path,
    metadata: dict[str, Any],
    snapshot: dict[str, Any],
    file_manifest: Sequence[dict[str, str]],
    units: Sequence[dict[str, Any]],
) -> dict[str, Any] | None:
    path = run_dir / "structural_transaction_inventory.json"
    if not path.is_file():
        if any(str(key).startswith("structural_transaction_") for key in metadata):
            raise ValueError("structural transaction metadata exists without inventory")
        return None
    inventory = _load_json(path)
    if not isinstance(inventory, dict):
        raise ValueError("invalid structural transaction inventory")
    rebuilt = preparer.build_structural_transaction_inventory(
        units,
        snapshot_id=str(snapshot.get("snapshot_id", "")),
        snapshot_sha256=sha256((run_dir / "snapshot.json").read_bytes()),
        file_sha256_by_id={
            str(record.get("file_id", "")): str(record.get("sha256", ""))
            for record in file_manifest
            if str(record.get("file_id", "")) and str(record.get("sha256", ""))
        },
        intensity=str(metadata.get("intensity", "")),
        scope=str(metadata.get("structural_transaction_scope", "NONE")),
    )
    if _canonical_json(inventory) != _canonical_json(rebuilt):
        raise ValueError("structural transaction inventory rebuild mismatch")
    return inventory


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


def _validate_scaffold_metadata(payload: Any, path: Path) -> None:
    """Validate, then ignore the metadata sidecar emitted by the scaffold tool.

    The sidecar is not a rewrite bundle.  It is nevertheless parsed strictly so
    a damaged or forged sidecar cannot be silently treated as harmless noise.
    """
    if not isinstance(payload, dict):
        raise ValueError(f"invalid scaffold metadata: {path.name}")
    schema_version = payload.get("schema_version")
    if schema_version not in SCAFFOLD_METADATA_SCHEMAS:
        raise ValueError(f"invalid scaffold metadata schema: {path.name}")
    expected = {
        "schema_version",
        "run_dir_name",
        "decision",
        "pending_units_total",
        "templates_total",
        "completion_claim_allowed",
        "requires_manual_completion",
        "records",
    }
    if schema_version == "humanize-rewrite-scaffold/v2":
        expected.add("decision_map")
    if set(payload) != expected:
        raise ValueError(f"invalid scaffold metadata fields: {path.name}")
    if not isinstance(payload.get("run_dir_name"), str) or not payload["run_dir_name"]:
        raise ValueError(f"invalid scaffold metadata run_dir_name: {path.name}")
    if payload.get("decision") not in {"REWRITE", "NO_CHANGE", "MIXED", "EMPTY"}:
        raise ValueError(f"invalid scaffold metadata decision: {path.name}")
    for field in ("pending_units_total", "templates_total"):
        value = payload.get(field)
        if isinstance(value, bool) or not isinstance(value, int) or value < 0:
            raise ValueError(f"invalid scaffold metadata count: {path.name}")
    if payload.get("completion_claim_allowed") is not False:
        raise ValueError(f"scaffold metadata completion claim must be false: {path.name}")
    if payload.get("requires_manual_completion") is not True:
        raise ValueError(f"scaffold metadata must require manual completion: {path.name}")
    records = payload.get("records")
    if not isinstance(records, list):
        raise ValueError(f"invalid scaffold metadata records: {path.name}")
    if payload["templates_total"] != len(records) or payload["pending_units_total"] != len(records):
        raise ValueError(f"scaffold metadata counts do not match records: {path.name}")
    decision_map = payload.get("decision_map")
    if schema_version == "humanize-rewrite-scaffold/v2":
        if not isinstance(decision_map, dict):
            raise ValueError(f"invalid scaffold metadata decision_map: {path.name}")
    else:
        if payload["decision"] in {"MIXED", "EMPTY"}:
            raise ValueError(f"v1 scaffold metadata cannot use MIXED decision: {path.name}")
        decision_map = None
    seen: set[str] = set()
    seen_exact: set[str] = set()
    for record in records:
        if not isinstance(record, dict) or set(record) != {
            "unit_id",
            "path",
            "decision",
            "template_sha256",
        }:
            raise ValueError(f"invalid scaffold metadata record: {path.name}")
        unit_id = record.get("unit_id")
        if not isinstance(unit_id, str) or not SAFE_UNIT_ID_RE.fullmatch(unit_id):
            raise ValueError(f"invalid scaffold metadata unit_id: {path.name}")
        key = unit_id.casefold()
        if key in seen:
            raise ValueError(f"duplicate scaffold metadata unit_id: {path.name}")
        seen.add(key)
        seen_exact.add(unit_id)
        if decision_map is not None and decision_map.get(unit_id) != record.get("decision"):
            raise ValueError(f"scaffold metadata decision_map mismatch: {path.name}")
        if record.get("path") != f"{unit_id}.json":
            raise ValueError(f"scaffold metadata path mismatch: {path.name}")
        if record.get("decision") not in {"REWRITE", "NO_CHANGE"}:
            raise ValueError(f"invalid scaffold metadata record decision: {path.name}")
        if payload["decision"] != "MIXED" and record.get("decision") != payload["decision"]:
            raise ValueError(f"scaffold metadata decision mismatch: {path.name}")
        if not isinstance(record.get("template_sha256"), str) or not re.fullmatch(
            r"[0-9a-f]{64}", record["template_sha256"]
        ):
            raise ValueError(f"invalid scaffold metadata template hash: {path.name}")
    if decision_map is not None and set(decision_map) != seen_exact:
        raise ValueError(f"scaffold metadata decision_map coverage mismatch: {path.name}")
    if payload["decision"] == "MIXED" and len(set(decision_map.values())) < 2:
        raise ValueError(f"scaffold metadata MIXED decision is not mixed: {path.name}")
    if payload["decision"] == "EMPTY" and records:
        raise ValueError(f"scaffold metadata EMPTY decision has records: {path.name}")


def _paragraph_order_blocks(masked_text: str) -> list[str]:
    blocks: list[str] = []
    for paragraph in preparer.structural_paragraph_blocks(masked_text):
        current: list[str] = []
        for line in paragraph.splitlines():
            stripped = line.strip()
            if stripped and re.fullmatch(r"(?:\[\[PROTECTED:[^\]]+\]\]\s*)+", stripped):
                if current:
                    blocks.append(" ".join(" ".join(current).split()))
                    current = []
                continue
            current.append(line)
        if current:
            normalized = " ".join(" ".join(current).split())
            if len(re.findall(r"[\u3400-\u9fff]", normalized)) >= 8:
                blocks.append(normalized)
    return blocks


def _non_structural_paragraph_order_check(
    before_masked: str,
    after_masked: str,
    intensity: str,
) -> dict[str, Any]:
    if intensity.upper() == "STRUCTURAL":
        return {"status": "NOT_APPLICABLE", "reason": "STRUCTURAL plan owns paragraph order"}
    before_blocks = _paragraph_order_blocks(before_masked)
    after_blocks = _paragraph_order_blocks(after_masked)
    before_counts = Counter(before_blocks)
    after_counts = Counter(after_blocks)
    after_positions = {block: index for index, block in enumerate(after_blocks)}
    preserved = [
        block
        for block in before_blocks
        if before_counts[block] == 1 and after_counts[block] == 1
    ]
    observed_order = [after_positions[block] for block in preserved]
    reordered = len(observed_order) >= 2 and observed_order != sorted(observed_order)
    return {
        "status": "REVIEW" if reordered else "PASS",
        "preserved_unique_paragraphs": len(observed_order),
        "reordered": reordered,
        "moved_paragraph_sha256": [
            sha256(block.encode("utf-8")) for block in preserved
        ]
        if reordered
        else [],
        "scope": "NON_STRUCTURAL_EXACT_PARAGRAPH_ORDER",
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
    if review_present:
        raise ValueError("warning_reviewer_identity_metadata_retired")

    if not warning_resolutions:
        if request_sha256:
            raise ValueError("warning_review_request_without_warning_resolutions")
        return warning_resolutions, "", "NONE", ""

    if not re.fullmatch(r"[0-9a-f]{64}", request_sha256):
        raise ValueError("invalid_warning_review_request_sha256")
    return warning_resolutions, request_sha256, "NONE", ""


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
        "structural_plan",
    }
    allowed = common | ({"masked_text"} if decision == "REWRITE" else {"reason"})
    unknown = sorted(set(bundle) - allowed)
    if unknown:
        raise ValueError("unknown_rewrite_bundle_fields:" + ",".join(unknown))


def _validate_structural_transaction_bundle_fields(bundle: dict[str, Any]) -> None:
    expected = {
        "schema_version",
        "transaction_id",
        "transaction_binding_sha256",
        "transaction_inventory_sha256",
        "unit_bindings",
        "fragments",
        "bundle_path",
    }
    if set(bundle) != expected:
        raise ValueError("structural_transaction_bundle_fields_invalid")
    if bundle.get("schema_version") != STRUCTURAL_TRANSACTION_BUNDLE_SCHEMA:
        raise ValueError("structural_transaction_bundle_schema_invalid")
    if not re.fullmatch(r"STX-[0-9a-f]{24}", str(bundle.get("transaction_id", ""))):
        raise ValueError("structural_transaction_id_invalid")
    for field in ("transaction_binding_sha256", "transaction_inventory_sha256"):
        if not re.fullmatch(r"[0-9a-f]{64}", str(bundle.get(field, ""))):
            raise ValueError(f"{field}_invalid")
    bindings = bundle.get("unit_bindings")
    if not isinstance(bindings, list) or len(bindings) != 2:
        raise ValueError("structural_transaction_unit_bindings_invalid")
    for binding in bindings:
        if not isinstance(binding, dict) or set(binding) != {
            "unit_id",
            "chunk_binding_sha256",
            "voice_profile_sha256",
        }:
            raise ValueError("structural_transaction_unit_binding_fields_invalid")
        if not isinstance(binding.get("unit_id"), str) or not binding["unit_id"]:
            raise ValueError("structural_transaction_unit_id_invalid")
        for field in ("chunk_binding_sha256", "voice_profile_sha256"):
            if not re.fullmatch(r"[0-9a-f]{64}", str(binding.get(field, ""))):
                raise ValueError(f"structural_transaction_{field}_invalid")
    fragments = bundle.get("fragments")
    if not isinstance(fragments, list) or len(fragments) != 2:
        raise ValueError("structural_transaction_fragments_invalid")
    for fragment in fragments:
        if not isinstance(fragment, dict) or set(fragment) != {
            "target_unit_id",
            "masked_text",
            "keep_reasons",
            "target_groups",
        }:
            raise ValueError("structural_transaction_fragment_fields_invalid")
        if not isinstance(fragment.get("target_unit_id"), str):
            raise ValueError("structural_transaction_target_unit_id_invalid")
        if not isinstance(fragment.get("masked_text"), str):
            raise ValueError("structural_transaction_masked_text_invalid")
        if not isinstance(fragment.get("keep_reasons"), dict):
            raise ValueError("structural_transaction_keep_reasons_invalid")
        groups = fragment.get("target_groups")
        if not isinstance(groups, list) or not groups:
            raise ValueError("structural_transaction_target_groups_invalid")
        for group in groups:
            if not isinstance(group, dict) or set(group) != {
                "source_refs",
                "target_paragraph_sha256",
                "responsibility",
                "reason",
            }:
                raise ValueError("structural_transaction_target_group_fields_invalid")
            refs = group.get("source_refs")
            if not isinstance(refs, list) or not refs:
                raise ValueError("structural_transaction_source_refs_invalid")
            for source_ref in refs:
                if not isinstance(source_ref, dict) or set(source_ref) != {
                    "unit_id",
                    "paragraph_id",
                }:
                    raise ValueError("structural_transaction_source_ref_fields_invalid")
                if not all(
                    isinstance(source_ref.get(field), str) and source_ref[field]
                    for field in ("unit_id", "paragraph_id")
                ):
                    raise ValueError("structural_transaction_source_ref_invalid")


def _validate_structural_transaction_decline_fields(bundle: dict[str, Any]) -> None:
    expected = {
        "schema_version",
        "decision",
        "transaction_id",
        "transaction_binding_sha256",
        "transaction_inventory_sha256",
        "unit_bindings",
        "reason_code",
        "reason",
        "evidence_refs",
        "bundle_path",
    }
    if set(bundle) != expected:
        raise ValueError("structural_transaction_decline_fields_invalid")
    if bundle.get("schema_version") != STRUCTURAL_TRANSACTION_DECLINE_SCHEMA:
        raise ValueError("structural_transaction_decline_schema_invalid")
    if bundle.get("decision") != "DECLINE":
        raise ValueError("structural_transaction_decline_decision_invalid")
    if not re.fullmatch(r"STX-[0-9a-f]{24}", str(bundle.get("transaction_id", ""))):
        raise ValueError("structural_transaction_decline_id_invalid")
    for field in ("transaction_binding_sha256", "transaction_inventory_sha256"):
        if not re.fullmatch(r"[0-9a-f]{64}", str(bundle.get(field, ""))):
            raise ValueError(f"structural_transaction_decline_{field}_invalid")
    bindings = bundle.get("unit_bindings")
    if not isinstance(bindings, list) or len(bindings) != 2:
        raise ValueError("structural_transaction_decline_unit_bindings_invalid")
    for binding in bindings:
        if not isinstance(binding, dict) or set(binding) != {
            "unit_id",
            "chunk_binding_sha256",
            "voice_profile_sha256",
        }:
            raise ValueError("structural_transaction_decline_unit_binding_fields_invalid")
        if not isinstance(binding.get("unit_id"), str) or not binding["unit_id"]:
            raise ValueError("structural_transaction_decline_unit_id_invalid")
        for field in ("chunk_binding_sha256", "voice_profile_sha256"):
            if not re.fullmatch(r"[0-9a-f]{64}", str(binding.get(field, ""))):
                raise ValueError(f"structural_transaction_decline_{field}_invalid")
    if bundle.get("reason_code") not in STRUCTURAL_TRANSACTION_DECLINE_REASON_CODES:
        raise ValueError("structural_transaction_decline_reason_code_invalid")
    if not _specific_decline_reason(str(bundle.get("reason", ""))):
        raise ValueError("structural_transaction_decline_reason_not_specific")
    evidence_refs = bundle.get("evidence_refs")
    if not isinstance(evidence_refs, list) or len(evidence_refs) < 2:
        raise ValueError("structural_transaction_decline_evidence_refs_invalid")
    normalized_refs: list[tuple[str, str]] = []
    for evidence_ref in evidence_refs:
        if not isinstance(evidence_ref, dict) or set(evidence_ref) != {
            "unit_id",
            "paragraph_id",
        }:
            raise ValueError("structural_transaction_decline_evidence_ref_fields_invalid")
        if not all(
            isinstance(evidence_ref.get(field), str) and evidence_ref[field]
            for field in ("unit_id", "paragraph_id")
        ):
            raise ValueError("structural_transaction_decline_evidence_ref_invalid")
        normalized_refs.append(
            (str(evidence_ref["unit_id"]), str(evidence_ref["paragraph_id"]))
        )
    if len(normalized_refs) != len(set(normalized_refs)):
        raise ValueError("structural_transaction_decline_evidence_ref_duplicate")


def _structural_transaction_unit_ids(bundle: dict[str, Any]) -> list[str]:
    _validate_structural_transaction_bundle_fields(bundle)
    return [str(item["unit_id"]) for item in bundle["unit_bindings"]]


def _validate_structural_plan(
    bundle: dict[str, Any],
    unit: dict[str, Any],
    chunk: dict[str, Any],
    masked_text: str,
    suffix: str,
    span_map: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    intensity = str(unit.get("intensity", "")).upper()
    plan = bundle.get("structural_plan")
    if intensity != "STRUCTURAL":
        if plan is not None:
            raise ValueError("structural_plan_not_allowed_for_non_structural_run")
        return {
            "status": "NOT_APPLICABLE",
            "change_applied": False,
            "limitations": "non-STRUCTURAL run",
        }
    if not isinstance(plan, dict):
        raise ValueError("structural_plan_missing")
    expected_plan_fields = {
        "schema_version",
        "source_inventory_sha256",
        "target_groups",
    }
    if set(plan) != expected_plan_fields:
        raise ValueError("structural_plan_fields_invalid")
    if plan.get("schema_version") != preparer.STRUCTURAL_PLAN_SCHEMA:
        raise ValueError("structural_plan_schema_invalid")

    source_inventory = chunk.get("structural_paragraphs")
    if not isinstance(source_inventory, list) or not source_inventory:
        raise ValueError("structural_source_inventory_missing")
    rebuilt_source = preparer.structural_paragraph_inventory(
        str(chunk.get("masked_text", "")),
        suffix.lower(),
        {
            protected_id: str(span_map.get(protected_id, {}).get("reason", ""))
            for protected_id in chunk.get("protected_ids", [])
        },
    )
    if _canonical_json(source_inventory) != _canonical_json(rebuilt_source):
        raise ValueError("structural_source_inventory_rebuild_mismatch")
    source_inventory_sha256 = preparer.structural_inventory_sha256(source_inventory)
    if (
        chunk.get("structural_inventory_sha256") != source_inventory_sha256
        or plan.get("source_inventory_sha256") != source_inventory_sha256
    ):
        raise ValueError("structural_source_inventory_hash_mismatch")

    source_ids = [str(item["paragraph_id"]) for item in source_inventory]
    source_by_id = {str(item["paragraph_id"]): item for item in source_inventory}
    source_blocks = preparer.structural_paragraph_blocks(
        str(chunk.get("masked_text", ""))
    )
    source_block_by_id = {
        str(item["paragraph_id"]): source_blocks[int(item["ordinal"]) - 1]
        for item in source_inventory
    }
    target_groups = plan.get("target_groups")
    target_blocks = preparer.structural_paragraph_blocks(masked_text)
    if not isinstance(target_groups, list) or len(target_groups) != len(target_blocks):
        raise ValueError("structural_target_group_count_mismatch")

    flattened: list[str] = []
    moved = 0
    merged = 0
    normalized_groups: list[list[str]] = []
    for target_index, (group, target_block) in enumerate(
        zip(target_groups, target_blocks), 1
    ):
        if not isinstance(group, dict) or set(group) != {
            "source_paragraph_ids",
            "target_paragraph_sha256",
            "responsibility",
            "reason",
        }:
            raise ValueError("structural_target_group_fields_invalid")
        group_ids = group.get("source_paragraph_ids")
        if (
            not isinstance(group_ids, list)
            or not group_ids
            or any(not isinstance(item, str) for item in group_ids)
        ):
            raise ValueError("structural_target_group_sources_invalid")
        if any(item not in source_by_id for item in group_ids):
            raise ValueError("structural_target_group_source_unknown")
        ordinals = [int(source_by_id[item]["ordinal"]) for item in group_ids]
        if ordinals != list(range(min(ordinals), max(ordinals) + 1)):
            raise ValueError("structural_merge_sources_must_be_adjacent_and_ordered")
        responsibilities = {
            str(source_by_id[item]["responsibility"]) for item in group_ids
        }
        if len(responsibilities) != 1:
            raise ValueError("structural_merge_changes_paragraph_responsibility")
        responsibility = next(iter(responsibilities))
        if group.get("responsibility") != responsibility:
            raise ValueError("structural_responsibility_claim_mismatch")
        if preparer._paragraph_responsibility(target_block) != responsibility:
            raise ValueError("structural_target_responsibility_drift")
        if not _specific_reason(str(group.get("reason", ""))):
            raise ValueError("structural_target_group_reason_not_specific")
        target_sha256 = sha256(target_block.encode("utf-8"))
        if group.get("target_paragraph_sha256") != target_sha256:
            raise ValueError("structural_target_paragraph_hash_mismatch")
        expected_protected_ids = [
            protected_id
            for source_id in group_ids
            for protected_id in source_by_id[source_id].get("protected_ids", [])
        ]
        target_protected_ids = [
            match.group("id")
            for match in preparer.PROTECTED_PLACEHOLDER_RE.finditer(target_block)
        ]
        if target_protected_ids != expected_protected_ids:
            raise ValueError("structural_protected_span_left_source_paragraph")
        for source_id in group_ids:
            source = source_by_id[source_id]
            if not bool(source.get("movable")) and (
                len(group_ids) != 1 or target_index != int(source["ordinal"])
            ):
                raise ValueError("structural_locked_paragraph_moved_or_merged")
        if len(group_ids) > 1:
            merged += len(group_ids) - 1
        expected_singleton = (
            [source_ids[target_index - 1]]
            if target_index <= len(source_ids)
            else []
        )
        if group_ids != expected_singleton:
            moved += 1
        flattened.extend(group_ids)
        normalized_groups.append(list(group_ids))

    if len(flattened) != len(set(flattened)) or sorted(flattened) != sorted(source_ids):
        raise ValueError("structural_source_paragraph_coverage_mismatch")
    default_groups = [[item] for item in source_ids]
    change_applied = normalized_groups != default_groups
    structural_baseline_groups = [
        " ".join(source_block_by_id[source_id].strip() for source_id in group_ids)
        for group_ids in normalized_groups
    ]
    structural_baseline = "\n\n".join(structural_baseline_groups)
    if masked_text.endswith(("\n", "\r")):
        structural_baseline += "\n"
    return {
        "status": "PASS",
        "schema_version": preparer.STRUCTURAL_PLAN_SCHEMA,
        "source_inventory_sha256": source_inventory_sha256,
        "source_paragraphs": len(source_ids),
        "target_paragraphs": len(target_blocks),
        "change_applied": change_applied,
        "moved_or_regrouped_targets": moved,
        "merged_source_paragraphs": merged,
        "title_lock": bool(chunk.get("structural_title_lock")),
        "scope": str(chunk.get("structural_scope", "")),
        "cross_unit_moves_allowed": bool(
            chunk.get("structural_cross_unit_moves_allowed")
        ),
        "semantic_mapping": "NOT_EVALUATED",
        "_baseline_masked_text": structural_baseline,
    }


def _structural_transaction_bundle_sha256(bundle: dict[str, Any]) -> str:
    return sha256(
        _canonical_json(
            {key: value for key, value in bundle.items() if key != "bundle_path"}
        ).encode("utf-8")
    )


def _bound_structural_transaction_candidate_envelope(
    bundle: dict[str, Any],
    inventory: dict[str, Any] | None,
    unit_map: dict[str, dict[str, Any]],
) -> tuple[dict[str, Any], list[str]]:
    if inventory is None:
        raise ValueError("structural_transaction_inventory_missing")
    if bundle["transaction_inventory_sha256"] != inventory.get("inventory_sha256"):
        raise ValueError("structural_transaction_inventory_hash_mismatch")
    authorization = inventory.get("scope_authorization")
    claims = inventory.get("claims")
    if not isinstance(authorization, dict) or not isinstance(claims, dict):
        raise ValueError("structural_transaction_inventory_authority_invalid")
    if (
        authorization.get("mechanical_scope_permission_granted") is not True
        or authorization.get("bound_transaction_bundle_required") is not True
        or authorization.get("candidate_inventory_is_execution_request") is not False
        or authorization.get("semantic_clearance_granted") is not False
        or claims.get("inventory_alone_execution_authorized") is not False
        or claims.get("semantic_mapping") != "NOT_EVALUATED"
    ):
        raise ValueError("structural_transaction_scope_not_authorized")
    candidates = inventory.get("transactions")
    if not isinstance(candidates, list):
        raise ValueError("structural_transaction_candidates_invalid")
    matches = [
        item
        for item in candidates
        if isinstance(item, dict)
        and item.get("transaction_id") == bundle["transaction_id"]
    ]
    if len(matches) != 1:
        raise ValueError("structural_transaction_candidate_not_unique")
    candidate = matches[0]
    if candidate.get("transaction_binding_sha256") != bundle[
        "transaction_binding_sha256"
    ]:
        raise ValueError("structural_transaction_binding_hash_mismatch")
    constraints = candidate.get("constraints")
    if not isinstance(constraints, dict) or (
        constraints.get("mechanical_scope_permission_granted") is not True
        or constraints.get("bound_transaction_bundle_required") is not True
        or constraints.get("candidate_inventory_is_execution_request") is not False
        or constraints.get("inventory_alone_execution_authorized") is not False
        or constraints.get("semantic_clearance_granted") is not False
        or constraints.get("atomic_pair_required") is not True
        or constraints.get("title_lock") is not True
        or constraints.get("cross_file") is not False
        or constraints.get("cross_heading") is not False
        or constraints.get("participant_split_or_delete") is not False
    ):
        raise ValueError("structural_transaction_candidate_constraints_invalid")
    compound_refs = candidate.get("compound_refs")
    if not isinstance(compound_refs, list) or len(compound_refs) != 2:
        raise ValueError("structural_transaction_compound_refs_invalid")
    candidate_unit_ids = [str(item.get("unit_id", "")) for item in compound_refs]
    binding_unit_ids = [str(item["unit_id"]) for item in bundle["unit_bindings"]]
    if binding_unit_ids != candidate_unit_ids or len(set(binding_unit_ids)) != 2:
        raise ValueError("structural_transaction_participant_mismatch")
    for binding, compound_ref in zip(bundle["unit_bindings"], compound_refs):
        unit_id = str(binding["unit_id"])
        unit = unit_map.get(unit_id)
        if unit is None:
            raise ValueError("structural_transaction_participant_unknown")
        if unit.get("status") != "PENDING" or str(unit.get("intensity", "")).upper() != "STRUCTURAL":
            raise ValueError("structural_transaction_participant_not_pending_structural")
        if (
            binding["chunk_binding_sha256"] != unit.get("chunk_binding_sha256")
            or binding["chunk_binding_sha256"]
            != compound_ref.get("chunk_binding_sha256")
        ):
            raise ValueError("structural_transaction_chunk_binding_mismatch")
        if binding["voice_profile_sha256"] != unit.get("voice_profile_sha256"):
            raise ValueError("structural_transaction_voice_binding_mismatch")
        if compound_ref.get("structural_inventory_sha256") != unit.get(
            "structural_inventory_sha256"
        ):
            raise ValueError("structural_transaction_source_inventory_mismatch")
    return candidate, candidate_unit_ids


def _bound_structural_transaction_candidate(
    bundle: dict[str, Any],
    inventory: dict[str, Any] | None,
    unit_map: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    _validate_structural_transaction_bundle_fields(bundle)
    candidate, candidate_unit_ids = _bound_structural_transaction_candidate_envelope(
        bundle, inventory, unit_map
    )
    fragment_unit_ids = [
        str(item["target_unit_id"]) for item in bundle["fragments"]
    ]
    if fragment_unit_ids != candidate_unit_ids:
        raise ValueError("structural_transaction_fragment_order_mismatch")
    return candidate


def _bound_structural_transaction_decline_candidate(
    bundle: dict[str, Any],
    inventory: dict[str, Any] | None,
    unit_map: dict[str, dict[str, Any]],
    chunks: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    _validate_structural_transaction_decline_fields(bundle)
    candidate, candidate_unit_ids = _bound_structural_transaction_candidate_envelope(
        bundle, inventory, unit_map
    )
    valid_refs = {
        (
            unit_id,
            str(paragraph.get("paragraph_id", "")),
        )
        for unit_id in candidate_unit_ids
        for paragraph in chunks[unit_id].get("structural_paragraphs", [])
        if isinstance(paragraph, dict) and paragraph.get("paragraph_id")
    }
    evidence_refs = [
        (str(item["unit_id"]), str(item["paragraph_id"]))
        for item in bundle["evidence_refs"]
    ]
    if any(item not in valid_refs for item in evidence_refs):
        raise ValueError("structural_transaction_decline_evidence_ref_unknown")
    evidenced_units = {unit_id for unit_id, _paragraph_id in evidence_refs}
    if evidenced_units != set(candidate_unit_ids):
        raise ValueError("structural_transaction_decline_evidence_member_coverage_mismatch")
    return candidate


def _transaction_source_inventory(
    unit_ids: Sequence[str],
    chunks: dict[str, dict[str, Any]],
) -> tuple[
    list[tuple[str, str]],
    dict[tuple[str, str], dict[str, Any]],
]:
    ordered_refs: list[tuple[str, str]] = []
    source_map: dict[tuple[str, str], dict[str, Any]] = {}
    for unit_id in unit_ids:
        chunk = chunks[unit_id]
        inventory = chunk.get("structural_paragraphs")
        if not isinstance(inventory, list) or not inventory:
            raise ValueError("structural_transaction_source_inventory_missing")
        blocks = preparer.structural_paragraph_blocks(str(chunk.get("masked_text", "")))
        if len(blocks) != len(inventory):
            raise ValueError("structural_transaction_source_blocks_mismatch")
        for item, block in zip(inventory, blocks):
            paragraph_id = str(item.get("paragraph_id", ""))
            ref = (unit_id, paragraph_id)
            if not paragraph_id or ref in source_map:
                raise ValueError("structural_transaction_source_ref_identity_invalid")
            record = dict(item)
            record["unit_id"] = unit_id
            record["block"] = block
            source_map[ref] = record
            ordered_refs.append(ref)
    return ordered_refs, source_map


def _validate_structural_transaction_fragment_plan(
    fragment: dict[str, Any],
    *,
    target_unit_id: str,
    ordered_source_refs: Sequence[tuple[str, str]],
    source_map: dict[tuple[str, str], dict[str, Any]],
) -> dict[str, Any]:
    target_blocks = preparer.structural_paragraph_blocks(fragment["masked_text"])
    target_groups = fragment["target_groups"]
    if len(target_blocks) != len(target_groups):
        raise ValueError("structural_transaction_target_group_count_mismatch")
    source_positions = {
        source_ref: index for index, source_ref in enumerate(ordered_source_refs)
    }
    claimed_refs: list[tuple[str, str]] = []
    normalized_groups: list[list[tuple[str, str]]] = []
    baseline_blocks: list[str] = []
    target_protected_ids: list[str] = []
    cross_unit_moves = 0
    moved_or_regrouped_targets = 0
    structural_deltas: list[dict[str, Any]] = []
    for target_ordinal, (group, target_block) in enumerate(
        zip(target_groups, target_blocks), 1
    ):
        refs = [
            (str(item["unit_id"]), str(item["paragraph_id"]))
            for item in group["source_refs"]
        ]
        if any(source_ref not in source_map for source_ref in refs):
            raise ValueError("structural_transaction_source_ref_unknown")
        positions = [source_positions[source_ref] for source_ref in refs]
        if positions != list(range(min(positions), max(positions) + 1)):
            raise ValueError(
                "structural_transaction_merge_sources_must_be_adjacent_and_ordered"
            )
        responsibilities = {
            str(source_map[source_ref]["responsibility"]) for source_ref in refs
        }
        if len(responsibilities) != 1:
            raise ValueError("structural_transaction_merge_changes_responsibility")
        responsibility = next(iter(responsibilities))
        if group.get("responsibility") != responsibility:
            raise ValueError("structural_transaction_responsibility_claim_mismatch")
        if preparer._paragraph_responsibility(target_block) != responsibility:
            raise ValueError("structural_transaction_target_responsibility_drift")
        if not _specific_reason(str(group.get("reason", ""))):
            raise ValueError("structural_transaction_target_reason_not_specific")
        if group.get("target_paragraph_sha256") != sha256(
            target_block.encode("utf-8")
        ):
            raise ValueError("structural_transaction_target_paragraph_hash_mismatch")
        expected_protected_ids = [
            protected_id
            for source_ref in refs
            for protected_id in source_map[source_ref].get("protected_ids", [])
        ]
        actual_protected_ids = [
            match.group("id")
            for match in preparer.PROTECTED_PLACEHOLDER_RE.finditer(target_block)
        ]
        if actual_protected_ids != expected_protected_ids:
            raise ValueError(
                "structural_transaction_protected_span_left_source_paragraph"
            )
        for source_ref in refs:
            source = source_map[source_ref]
            if source_ref[0] != target_unit_id:
                cross_unit_moves += 1
            if not bool(source.get("movable")) and (
                source_ref[0] != target_unit_id
                or len(refs) != 1
                or target_ordinal != int(source["ordinal"])
            ):
                raise ValueError(
                    "structural_transaction_locked_paragraph_moved_or_merged"
                )
            change_kinds: list[str] = []
            if source_ref[0] != target_unit_id:
                change_kinds.append("CROSS_UNIT_MOVE")
            if int(source["ordinal"]) != target_ordinal or len(refs) > 1:
                change_kinds.append("MOVE_OR_REGROUP_SOURCE_PARAGRAPH")
            if change_kinds:
                structural_deltas.append(
                    {
                        "from_unit_id": source_ref[0],
                        "to_unit_id": target_unit_id,
                        "paragraph_id": source_ref[1],
                        "source_ordinal": int(source["ordinal"]),
                        "target_ordinal": target_ordinal,
                        "change_kinds": change_kinds,
                        "responsibility": responsibility,
                        "target_paragraph_sha256": str(
                            group["target_paragraph_sha256"]
                        ),
                        "reason": str(group["reason"]),
                    }
                )
        if len(refs) != 1 or refs[0][0] != target_unit_id or int(
            source_map[refs[0]]["ordinal"]
        ) != target_ordinal:
            moved_or_regrouped_targets += 1
        claimed_refs.extend(refs)
        normalized_groups.append(refs)
        target_protected_ids.extend(expected_protected_ids)
        baseline_blocks.append(
            " ".join(str(source_map[source_ref]["block"]).strip() for source_ref in refs)
        )
    baseline_masked_text = "\n\n".join(baseline_blocks)
    if str(fragment["masked_text"]).endswith(("\n", "\r")):
        baseline_masked_text += "\n"
    return {
        "status": "PASS",
        "target_unit_id": target_unit_id,
        "claimed_refs": claimed_refs,
        "normalized_groups": normalized_groups,
        "target_protected_ids": target_protected_ids,
        "cross_unit_moves": cross_unit_moves,
        "moved_or_regrouped_targets": moved_or_regrouped_targets,
        "target_paragraphs": len(target_blocks),
        "structural_deltas": structural_deltas,
        "semantic_mapping": "NOT_EVALUATED",
        "_baseline_masked_text": baseline_masked_text,
    }


def _public_transaction_plan_check(plan_check: dict[str, Any]) -> dict[str, Any]:
    public = {
        key: value
        for key, value in plan_check.items()
        if not key.startswith("_") and key not in {"claimed_refs", "normalized_groups"}
    }
    public["claimed_refs"] = [
        {"unit_id": unit_id, "paragraph_id": paragraph_id}
        for unit_id, paragraph_id in plan_check.get("claimed_refs", [])
    ]
    public["normalized_groups"] = [
        [
            {"unit_id": unit_id, "paragraph_id": paragraph_id}
            for unit_id, paragraph_id in group
        ]
        for group in plan_check.get("normalized_groups", [])
    ]
    return public


def _build_structural_transaction_review_request(
    *,
    snapshot_id: str,
    bundle: dict[str, Any],
    candidate: dict[str, Any],
    transaction_result: dict[str, Any],
    fragment_results: dict[str, dict[str, Any]],
    document_gate: dict[str, Any],
) -> dict[str, Any]:
    unit_ids = [str(item["unit_id"]) for item in bundle["unit_bindings"]]
    artifact_fragments: dict[str, Any] = {}
    for unit_id in unit_ids:
        fragment = fragment_results[unit_id]
        artifact_fragments[unit_id] = {
            "chunk_binding_sha256": fragment["chunk_binding_sha256"],
            "voice_profile_sha256": fragment["voice_profile_sha256"],
            "source_before_sha256": sha256(fragment["original"].encode("utf-8")),
            "mechanical_baseline_sha256": sha256(
                fragment["invariant_before"].encode("utf-8")
            ),
            "candidate_after_sha256": sha256(fragment["restored"].encode("utf-8")),
            "plan_check_sha256": sha256(
                _canonical_json(fragment["plan_check_public"]).encode("utf-8")
            ),
            "validator_sha256": sha256(
                _canonical_json(fragment["validation_payload"]).encode("utf-8")
            ),
        }
    policy_hashes = {
        **output_validator._policy_hashes(),
        "finalizer_sha256": sha256(Path(__file__).resolve().read_bytes()),
        "preparer_sha256": sha256(Path(preparer.__file__).resolve().read_bytes()),
        "transaction_eligibility_policy_sha256": str(
            candidate.get("eligibility_policy_sha256", "")
        ),
    }
    source_mapping = [
        {
            "target_unit_id": str(fragment["target_unit_id"]),
            "target_groups": fragment["target_groups"],
        }
        for fragment in bundle["fragments"]
    ]
    structural_deltas: list[dict[str, Any]] = []
    for unit_id in unit_ids:
        for index, delta in enumerate(
            fragment_results[unit_id]["plan_check"].get(
                "structural_deltas", []
            ),
            1,
        ):
            structural_deltas.append(
                {
                    "delta_id": f"{bundle['transaction_id']}:{unit_id}:D{index:03d}",
                    **delta,
                }
            )
    context_hashes = {
        "outer_before_sha256": sha256(
            fragment_results[unit_ids[0]]["context_before"].encode("utf-8")
        ),
        "internal_left_after_sha256": sha256(
            fragment_results[unit_ids[0]]["context_after"].encode("utf-8")
        ),
        "internal_right_before_sha256": sha256(
            fragment_results[unit_ids[1]]["context_before"].encode("utf-8")
        ),
        "outer_after_sha256": sha256(
            fragment_results[unit_ids[1]]["context_after"].encode("utf-8")
        ),
    }
    request_body = {
        "schema": STRUCTURAL_TRANSACTION_REVIEW_REQUEST_SCHEMA,
        "status": "PENDING_EXTERNAL_REVIEW",
        "snapshot_id": snapshot_id,
        "transaction_id": bundle["transaction_id"],
        "unit_ids": unit_ids,
        "transaction_bundle_sha256": transaction_result["bundle_sha256"],
        "transaction_binding_sha256": bundle["transaction_binding_sha256"],
        "transaction_inventory_sha256": bundle["transaction_inventory_sha256"],
        "source_member_claim_sha256": transaction_result[
            "source_member_claim_sha256"
        ],
        "frozen_pair": {
            "candidate_scope": candidate.get("candidate_scope"),
            "file_id": candidate.get("file_id"),
            "heading_path": candidate.get("heading_path"),
            "scene": candidate.get("scene"),
            "boundary": candidate.get("boundary"),
            "compound_refs": candidate.get("compound_refs"),
            "constraints": candidate.get("constraints"),
        },
        "context_hashes": context_hashes,
        "source_mapping": source_mapping,
        "structural_deltas": structural_deltas,
        "artifacts": {
            "fragments": artifact_fragments,
            "document": {
                "mechanical_baseline_sha256": document_gate[
                    "mechanical_baseline_sha256"
                ],
                "candidate_after_sha256": document_gate["candidate_after_sha256"],
                "gate_evidence_sha256": document_gate["evidence_sha256"],
            },
        },
        "artifact_refs": {
            unit_id: {
                "before": f"validation/{unit_id}.before{fragment_results[unit_id]['suffix']}",
                "after": f"validation/{unit_id}.after{fragment_results[unit_id]['suffix']}",
                "validator": f"validation/{unit_id}.validation.json",
                "mechanical_plan": f"validation/{unit_id}.structural.json",
            }
            for unit_id in unit_ids
        },
        "document_gate": {
            "status": document_gate["status"],
            "format": document_gate["document_format"],
            "error_count": document_gate["error_count"],
        },
        "required_review_dimensions": [
            "CROSS_UNIT_PARAGRAPH_DEPENDENCY_AND_REFERENT_PRESERVED",
            "CLAIM_EVIDENCE_AND_CAUSAL_SCOPE_PRESERVED",
            "NEGATION_MODALITY_FOCUS_AND_CONDITION_PRESERVED",
            "TARGET_FRAGMENT_BOUNDARY_AND_READING_ORDER_ACCEPTABLE",
        ],
        "policy_hashes": policy_hashes,
        "trust_boundary": {
            "semantic_mapping": "NOT_EVALUATED",
            "academic_correctness": "NOT_EVALUATED",
            "local_clearance_supported": False,
            "external_signature_verified": False,
            "completion_claim_allowed": False,
        },
    }
    return {
        **request_body,
        "request_sha256": sha256(_canonical_json(request_body).encode("utf-8")),
    }


def _validate_structural_transaction(
    *,
    bundle: dict[str, Any],
    candidate: dict[str, Any],
    snapshot_id: str,
    unit_map: dict[str, dict[str, Any]],
    chunks: dict[str, dict[str, Any]],
    file_texts: dict[str, str],
    file_suffixes: dict[str, str],
    span_map: dict[str, dict[str, Any]],
    validation_dir: Path,
) -> dict[str, Any]:
    unit_ids = [str(item["unit_id"]) for item in bundle["unit_bindings"]]
    ordered_source_refs, source_map = _transaction_source_inventory(unit_ids, chunks)
    fragment_gate_statuses = {unit_id: "NOT_RUN" for unit_id in unit_ids}
    fragment_results: dict[str, dict[str, Any]] = {}
    errors: list[str] = []
    claimed_refs: list[tuple[str, str]] = []
    total_cross_unit_moves = 0
    for binding, fragment in zip(bundle["unit_bindings"], bundle["fragments"]):
        unit_id = str(binding["unit_id"])
        unit = unit_map[unit_id]
        suffix = file_suffixes.get(str(unit["file_id"]), ".txt") or ".txt"
        source_text = file_texts[str(unit["file_id"])]
        original = source_text[int(unit["start"]):int(unit["end"])]
        try:
            plan_check = _validate_structural_transaction_fragment_plan(
                fragment,
                target_unit_id=unit_id,
                ordered_source_refs=ordered_source_refs,
                source_map=source_map,
            )
            baseline_masked = str(plan_check.pop("_baseline_masked_text"))
            target_protected_ids = list(plan_check["target_protected_ids"])
            invariant_before, baseline_errors = restore_protected(
                baseline_masked, target_protected_ids, span_map
            )
            if invariant_before is None:
                raise ValueError(
                    "structural_transaction_baseline_restore:"
                    + "|".join(baseline_errors)
                )
            restored, restore_errors = restore_protected(
                str(fragment["masked_text"]), target_protected_ids, span_map
            )
            if restored is None:
                raise ValueError(
                    "structural_transaction_candidate_restore:"
                    + "|".join(restore_errors)
                )
            keep_reasons = output_validator._parse_keep_reasons(
                [f"{key}={value}" for key, value in fragment["keep_reasons"].items()],
                {
                    item["id"]
                    for item in output_validator.lexical.load_lexicon()["signals"]
                },
            )
            before_path = validation_dir / f"{unit_id}.before{suffix}"
            after_path = validation_dir / f"{unit_id}.after{suffix}"
            before_path.write_text(invariant_before, encoding="utf-8")
            after_path.write_text(restored, encoding="utf-8")
            validation_payload = output_validator.validate(
                before_path,
                after_path,
                scene=str(unit["scene"]),
                keep_reasons=keep_reasons,
                fragment_mode=True,
            )
            _stabilize_validation_evidence_refs(validation_payload, unit_id, suffix)
            paired_quality_request = _persist_paired_quality_review_request(
                validation_payload, validation_dir, unit_id
            )
            plan_check_public = _public_transaction_plan_check(plan_check)
            validation_payload["structural_plan_check"] = plan_check_public
            _write_json(
                validation_dir / f"{unit_id}.validation.json", validation_payload
            )
            _write_json(
                validation_dir / f"{unit_id}.structural.json", plan_check_public
            )
            fragment_gate_statuses[unit_id] = str(
                validation_payload["mechanical_validation_status"]
            )
            fragment_results[unit_id] = {
                "unit_id": unit_id,
                "suffix": suffix,
                "original": original,
                "invariant_before": invariant_before,
                "restored": restored,
                "plan_check": plan_check,
                "plan_check_public": plan_check_public,
                "validation_payload": validation_payload,
                "paired_quality_review_request": paired_quality_request,
                "chunk_binding_sha256": str(binding["chunk_binding_sha256"]),
                "voice_profile_sha256": str(binding["voice_profile_sha256"]),
                "context_before": str(
                    chunks[unit_id].get("read_only_context_before", "")
                ),
                "context_after": str(
                    chunks[unit_id].get("read_only_context_after", "")
                ),
            }
            claimed_refs.extend(plan_check["claimed_refs"])
            total_cross_unit_moves += int(plan_check["cross_unit_moves"])
            if validation_payload["mechanical_validation_status"] != "PASS":
                errors.append(
                    f"{unit_id}:fragment_validator:"
                    f"{validation_payload['mechanical_validation_status']}"
                )
            elif not _quality_review_only(validation_payload):
                errors.append(f"{unit_id}:paired_quality_review_request_missing")
        except (KeyError, TypeError, ValueError) as error:
            fragment_gate_statuses[unit_id] = "FAIL"
            errors.append(f"{unit_id}:{error}")

    bundle_sha256 = _structural_transaction_bundle_sha256(bundle)
    transaction_result: dict[str, Any] = {
        "transaction_id": bundle["transaction_id"],
        "bundle_sha256": bundle_sha256,
        "unit_ids": unit_ids,
        "status": "REVIEW",
        "atomic_gate_status": "ROLLED_BACK",
        "source_member_claim_status": "NOT_RUN",
        "source_member_claim_sha256": "",
        "fragment_gate_statuses": fragment_gate_statuses,
        "document_gate_status": "NOT_RUN",
        "change_applied": False,
        "cross_unit_moves_applied": 0,
        "rollback_reason": "FRAGMENT_GATE" if errors else "",
        "errors": errors,
        "review_request": {},
    }
    if errors or any(status != "PASS" for status in fragment_gate_statuses.values()):
        return {**transaction_result, "_fragment_results": fragment_results}

    expected_set = set(ordered_source_refs)
    claimed_set = set(claimed_refs)
    claim_payload = [
        {"unit_id": unit_id, "paragraph_id": paragraph_id}
        for unit_id, paragraph_id in claimed_refs
    ]
    transaction_result["source_member_claim_sha256"] = sha256(
        _canonical_json(claim_payload).encode("utf-8")
    )
    if (
        len(claimed_refs) != len(ordered_source_refs)
        or len(claimed_set) != len(claimed_refs)
        or claimed_set != expected_set
    ):
        transaction_result["source_member_claim_status"] = "FAIL"
        transaction_result["rollback_reason"] = "SOURCE_MEMBER_CLAIM"
        transaction_result["errors"].append(
            "structural_transaction_source_member_claim_mismatch"
        )
        return {**transaction_result, "_fragment_results": fragment_results}
    transaction_result["source_member_claim_status"] = "PASS"
    if total_cross_unit_moves <= 0:
        transaction_result["rollback_reason"] = "NO_CROSS_UNIT_MOVE"
        transaction_result["errors"].append(
            "structural_transaction_requires_real_cross_unit_move"
        )
        return {**transaction_result, "_fragment_results": fragment_results}

    first_chunk = chunks[unit_ids[0]]
    second_chunk = chunks[unit_ids[1]]
    pair_original = "".join(fragment_results[unit_id]["original"] for unit_id in unit_ids)
    pair_candidate = "".join(fragment_results[unit_id]["restored"] for unit_id in unit_ids)
    transaction_protected_ids = [
        protected_id
        for source_ref in ordered_source_refs
        for protected_id in source_map[source_ref].get("protected_ids", [])
    ]
    protected_count_changes = _protected_content_count_changes(
        pair_original,
        pair_candidate,
        transaction_protected_ids,
        span_map,
    )
    if protected_count_changes:
        transaction_result["rollback_reason"] = "PROTECTED_CONTENT_COUNT"
        transaction_result["errors"].append(
            "structural_transaction_protected_content_count_changed:"
            + ",".join(protected_count_changes)
        )
        return {**transaction_result, "_fragment_results": fragment_results}
    copied_context = _copied_read_only_context(
        pair_original,
        pair_candidate,
        {
            "read_only_context_before": first_chunk.get(
                "read_only_context_before", ""
            ),
            "read_only_context_after": second_chunk.get(
                "read_only_context_after", ""
            ),
        },
    )
    if copied_context:
        transaction_result["rollback_reason"] = "READ_ONLY_CONTEXT"
        transaction_result["errors"].append(
            "structural_transaction_read_only_context_copied:"
            + ",".join(copied_context)
        )
        return {**transaction_result, "_fragment_results": fragment_results}

    file_id = str(unit_map[unit_ids[0]]["file_id"])
    source_text = file_texts[file_id]
    mechanical_document = source_text
    candidate_document = source_text
    replacements = [
        (
            int(unit_map[unit_id]["start"]),
            int(unit_map[unit_id]["end"]),
            fragment_results[unit_id]["invariant_before"],
            fragment_results[unit_id]["restored"],
        )
        for unit_id in unit_ids
    ]
    for start, end, baseline, restored in sorted(
        replacements, key=lambda item: item[0], reverse=True
    ):
        mechanical_document = mechanical_document[:start] + baseline + mechanical_document[end:]
        candidate_document = candidate_document[:start] + restored + candidate_document[end:]
    suffix = file_suffixes.get(file_id, "")
    document_format = "tex" if suffix.lower() in {".tex", ".ltx"} else "markdown"
    full_check = invariants.check_documents(
        mechanical_document,
        candidate_document,
        document_format=document_format,
    )
    full_check_payload = full_check.to_dict()
    document_gate = {
        "status": "FAIL" if full_check.errors else "PASS",
        "document_format": document_format,
        "error_count": len(full_check.errors),
        "mechanical_baseline_sha256": sha256(mechanical_document.encode("utf-8")),
        "candidate_after_sha256": sha256(candidate_document.encode("utf-8")),
        "evidence_sha256": sha256(
            _canonical_json(full_check_payload).encode("utf-8")
        ),
        "evidence": full_check_payload,
    }
    transaction_result["document_gate_status"] = document_gate["status"]
    if full_check.errors:
        transaction_result["rollback_reason"] = "DOCUMENT_GATE"
        transaction_result["errors"].append(
            "structural_transaction_document_gate_failed"
        )
        return {
            **transaction_result,
            "_fragment_results": fragment_results,
            "_document_gate": document_gate,
        }

    transaction_result.update(
        {
            "status": "PASS",
            "atomic_gate_status": "PASS",
            "change_applied": True,
            "cross_unit_moves_applied": total_cross_unit_moves,
            "rollback_reason": "",
        }
    )
    review_request = _build_structural_transaction_review_request(
        snapshot_id=snapshot_id,
        bundle=bundle,
        candidate=candidate,
        transaction_result=transaction_result,
        fragment_results=fragment_results,
        document_gate=document_gate,
    )
    return {
        **transaction_result,
        "_fragment_results": fragment_results,
        "_document_gate": document_gate,
        "_review_request": review_request,
    }


def _build_structural_semantic_review_request(
    *,
    snapshot_id: str,
    unit_id: str,
    unit: dict[str, Any],
    chunk: dict[str, Any],
    bundle: dict[str, Any],
    structural_plan_check: dict[str, Any],
    original: str,
    invariant_before: str,
    restored: str,
    validation_payload: dict[str, Any],
    suffix: str,
) -> dict[str, Any] | None:
    """Build a review-only request for one mechanically valid structural change.

    The request deliberately has no local clearance field. It binds the candidate and
    mechanical evidence for an external reviewer, but cannot upgrade semantic status.
    """

    actual_content_changed = invariant_before != restored
    declared_structural_change = structural_plan_check.get("change_applied") is True
    if (
        structural_plan_check.get("status") != "PASS"
        or not (actual_content_changed or declared_structural_change)
        or validation_payload.get("hard_invariant_layer_status") != "PASS"
    ):
        return None
    plan = bundle.get("structural_plan")
    if not isinstance(plan, dict):
        return None
    source_inventory = chunk.get("structural_paragraphs")
    if not isinstance(source_inventory, list):
        return None
    source_by_id = {
        str(item.get("paragraph_id")): item
        for item in source_inventory
        if isinstance(item, dict)
    }
    target_groups = plan.get("target_groups")
    if not isinstance(target_groups, list):
        return None

    structural_deltas: list[dict[str, Any]] = []
    for target_ordinal, group in enumerate(target_groups, 1):
        if not isinstance(group, dict):
            continue
        source_ids = [str(item) for item in group.get("source_paragraph_ids", [])]
        source_ordinals = [
            int(source_by_id[item]["ordinal"])
            for item in source_ids
            if item in source_by_id
        ]
        change_kinds: list[str] = []
        if len(source_ids) > 1:
            change_kinds.append("MERGE_ADJACENT_SOURCE_PARAGRAPHS")
        if source_ordinals and source_ordinals[0] != target_ordinal:
            change_kinds.append("MOVE_OR_REGROUP_SOURCE_PARAGRAPHS")
        if not change_kinds:
            continue
        structural_deltas.append(
            {
                "delta_id": f"SD-{target_ordinal:03d}",
                "change_kinds": change_kinds,
                "target_ordinal": target_ordinal,
                "source_paragraph_ids": source_ids,
                "source_ordinals": source_ordinals,
                "responsibility": str(group.get("responsibility", "")),
                "reason": str(group.get("reason", "")),
                "target_paragraph_sha256": str(
                    group.get("target_paragraph_sha256", "")
                ),
            }
        )

    # A STRUCTURAL rewrite that changes text while declaring the default
    # one-to-one paragraph mapping is still semantically unaccounted for.  Do
    # not infer that it was merely local style editing: bind an explicit
    # reviewer delta so hidden payload swaps cannot become a PASS by omission.
    if not structural_deltas and structural_plan_check.get("change_applied") is not True:
        structural_deltas.append(
            {
                "delta_id": "SD-UNDECLARED-001",
                "change_kinds": ["UNDECLARED_CONTENT_CHANGE"],
                "target_ordinal": None,
                "source_paragraph_ids": [
                    str(item.get("paragraph_id", ""))
                    for item in source_inventory
                    if isinstance(item, dict)
                ],
                "source_ordinals": [
                    int(item.get("ordinal", 0))
                    for item in source_inventory
                    if isinstance(item, dict)
                ],
                "responsibility": "UNRESOLVED",
                "reason": "STRUCTURAL 文本发生变化，但 plan 未声明段落移动或合并；需要外部语义复核。",
                "target_paragraph_sha256": "",
            }
        )

    warning_request = validation_payload.get("warning_review_request")
    speech_act_warnings = (
        warning_request.get("warnings", [])
        if isinstance(warning_request, dict)
        else []
    )
    policy_hashes = {
        **output_validator._policy_hashes(),
        "finalizer_sha256": sha256(Path(__file__).resolve().read_bytes()),
        "preparer_sha256": sha256(Path(preparer.__file__).resolve().read_bytes()),
    }
    artifact_stem = f"validation/{unit_id}"
    request_body = {
        "schema": STRUCTURAL_SEMANTIC_REVIEW_REQUEST_SCHEMA,
        "status": "PENDING_EXTERNAL_REVIEW",
        "snapshot_id": snapshot_id,
        "unit_id": unit_id,
        "artifact": {
            "chunk_binding_sha256": str(unit.get("chunk_binding_sha256", "")),
            "voice_profile_sha256": str(unit.get("voice_profile_sha256", "")),
            "source_inventory_sha256": str(
                structural_plan_check.get("source_inventory_sha256", "")
            ),
            "structural_plan_sha256": sha256(
                _canonical_json(plan).encode("utf-8")
            ),
            "source_before_sha256": sha256(original.encode("utf-8")),
            "structural_baseline_masked_sha256": str(
                structural_plan_check.get("invariant_baseline_sha256", "")
            ),
            "structural_baseline_restored_sha256": sha256(
                invariant_before.encode("utf-8")
            ),
            "candidate_after_sha256": sha256(restored.encode("utf-8")),
            "context_before_sha256": sha256(
                str(chunk.get("read_only_context_before", "")).encode("utf-8")
            ),
            "context_after_sha256": sha256(
                str(chunk.get("read_only_context_after", "")).encode("utf-8")
            ),
        },
        "artifact_refs": {
            "before": f"{artifact_stem}.before{suffix}",
            "after": f"{artifact_stem}.after{suffix}",
            "mechanical_plan": f"{artifact_stem}.structural.json",
            "validator": f"{artifact_stem}.validation.json",
        },
        "mechanical_status": {
            "structural_plan_status": "PASS",
            "hard_invariant_layer_status": "PASS",
            "change_applied": actual_content_changed,
            "scope": str(structural_plan_check.get("scope", "")),
            "title_lock": bool(structural_plan_check.get("title_lock")),
            "cross_unit_moves_allowed": bool(
                structural_plan_check.get("cross_unit_moves_allowed")
            ),
        },
        "structural_deltas": structural_deltas,
        "speech_act_warnings": speech_act_warnings,
        "required_review_dimensions": [
            "PARAGRAPH_DEPENDENCY_AND_REFERENT_PRESERVED",
            "CLAIM_EVIDENCE_AND_CAUSAL_SCOPE_PRESERVED",
            "NEGATION_MODALITY_FOCUS_AND_CONDITION_PRESERVED",
            "PARAGRAPH_RESPONSIBILITY_AND_READING_ORDER_ACCEPTABLE",
        ],
        "policy_hashes": policy_hashes,
        "trust_boundary": {
            "semantic_mapping": "NOT_EVALUATED",
            "academic_correctness": "NOT_EVALUATED",
            "local_clearance_supported": False,
            "external_signature_verified": False,
            "completion_claim_allowed": False,
        },
    }
    return {
        **request_body,
        "request_sha256": sha256(_canonical_json(request_body).encode("utf-8")),
    }


def _stabilize_validation_evidence_refs(
    payload: dict[str, Any], unit_id: str, suffix: str
) -> None:
    """Replace transient staging paths with committed run-relative artifact refs."""

    evidence = payload.get("evidence")
    if not isinstance(evidence, dict):
        return
    evidence["before_path"] = f"validation/{unit_id}.before{suffix}"
    evidence["after_path"] = f"validation/{unit_id}.after{suffix}"


def _persist_paired_quality_review_request(
    payload: dict[str, Any],
    validation_dir: Path,
    unit_id: str,
) -> dict[str, Any] | None:
    request = payload.get("paired_quality_review_request")
    if not isinstance(request, dict):
        return None
    request_name = f"{unit_id}.paired-quality-review-request.json"
    _write_json(validation_dir / request_name, request)
    return {
        "status": str(request.get("status", "NOT_EVALUATED")),
        "path": str(Path("validation") / request_name).replace("\\", "/"),
        "request_sha256": str(request.get("request_sha256", "")),
        "decision": str(
            request.get("validation_context", {}).get("decision", "")
        ),
        "changes_total": len(request.get("changes", [])),
        "quality_clearance_granted": False,
    }


def _quality_review_only(payload: dict[str, Any]) -> bool:
    return bool(
        payload.get("mechanical_validation_status") == "PASS"
        and payload.get("paired_quality_review_status")
        == "PENDING_EXTERNAL_REVIEW"
        and payload.get("status") == "REVIEW"
        and set(payload.get("review_reasons", []))
        == {"paired_quality_not_evaluated"}
    )


def _discard_paired_quality_review_request(
    requests: dict[str, dict[str, Any]],
    validation_dir: Path,
    unit_id: str,
) -> None:
    record = requests.pop(unit_id, None)
    request_name = f"{unit_id}.paired-quality-review-request.json"
    if isinstance(record, dict):
        relative_path = str(record.get("path", ""))
        if relative_path:
            request_name = Path(relative_path).name
    # Fragment validation persists this file before the transaction-wide gate
    # is known, so a rolled-back pair may not yet have a public request record.
    path = validation_dir / request_name
    if path.is_file():
        path.unlink()


def collect_rewrites(
    directory: Path,
) -> tuple[
    dict[str, dict[str, Any]],
    dict[str, dict[str, Any]],
    dict[str, dict[str, Any]],
]:
    rewrites: dict[str, dict[str, Any]] = {}
    transactions: dict[str, dict[str, Any]] = {}
    declines: dict[str, dict[str, Any]] = {}
    if not directory.is_dir():
        raise FileNotFoundError(directory)
    for path in sorted(directory.iterdir(), key=lambda item: item.name.casefold()):
        if not path.is_file() or path.suffix.lower() not in {".json", ".txt"}:
            continue
        if path.name == SCAFFOLD_METADATA_NAME:
            if path.suffix.lower() != ".json":
                raise ValueError("scaffold metadata must be JSON")
            _validate_scaffold_metadata(_load_json(path), path)
            continue
        unit_id = path.stem
        payload = _rewrite_bundle(path)
        payload["bundle_path"] = str(path.resolve())
        if payload.get("schema_version") == STRUCTURAL_TRANSACTION_BUNDLE_SCHEMA:
            if path.suffix.lower() != ".json":
                raise ValueError("structural transaction bundle must be JSON")
            _validate_structural_transaction_bundle_fields(payload)
            transaction_id = str(payload["transaction_id"])
            if transaction_id in transactions:
                raise ValueError(
                    f"duplicate structural transaction for {transaction_id}"
                )
            transactions[transaction_id] = payload
            continue
        if payload.get("schema_version") == STRUCTURAL_TRANSACTION_DECLINE_SCHEMA:
            if path.suffix.lower() != ".json":
                raise ValueError("structural transaction decline must be JSON")
            _validate_structural_transaction_decline_fields(payload)
            transaction_id = str(payload["transaction_id"])
            if transaction_id in declines:
                raise ValueError(
                    f"duplicate structural transaction decline for {transaction_id}"
                )
            declines[transaction_id] = payload
            continue
        if unit_id in rewrites:
            raise ValueError(f"duplicate rewrite for {unit_id}")
        rewrites[unit_id] = payload
    return rewrites, transactions, declines


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


def _specific_decline_reason(reason: str) -> bool:
    han = "".join(re.findall(r"[\u3400-\u9fff]", reason))
    if len(han) < 8:
        return False
    generic = {
        "候选已经审阅无需调整",
        "已经审阅无需结构调整",
        "当前无需进行结构调整",
        "现有结构已经比较合理",
        "保持不变即可无需调整",
        "这个候选不需要执行",
        "没有必要进行结构调整",
        "暂时不需要进行结构调整",
    }
    if han in generic:
        return False
    return bool(
        re.search(
            r"段落|职责|对象|依赖|指代|题干|题解|证据|主张|结论|顺序|对应|"
            r"保护|公式|引语|标题|用户|锁定|收益|范围|边界|条件|因果|模态|成员",
            reason,
        )
    )


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


def _audit_voice_conformance_set(
    profiles: dict[str, dict[str, Any]],
    records: Sequence[dict[str, Any]],
    *,
    scene_routing_status: str,
) -> dict[str, Any]:
    if len(profiles) == 1:
        return _audit_voice_conformance(
            next(iter(profiles.values())),
            records,
            scene_routing_status=scene_routing_status,
        )
    per_scene: dict[str, dict[str, Any]] = {}
    for scene, profile in sorted(profiles.items()):
        scene_records = [
            record for record in records if str(record.get("scene", "")).upper() == scene
        ]
        if not scene_records:
            continue
        per_scene[scene] = _audit_voice_conformance(
            profile,
            scene_records,
            scene_routing_status=scene_routing_status,
        )
    status = (
        "PASS"
        if per_scene
        and scene_routing_status == "PASS"
        and all(result.get("status") == "PASS" for result in per_scene.values())
        else "REVIEW"
    )
    return {
        "schema_version": "humanize-document-voice-conformance-set/v1",
        "status": status,
        "basis": "SCENE_DEFAULT_PROFILE_SET_UNIT_VALIDATION",
        "profile_kind": "DEFAULT_SET",
        "identity_verified": False,
        "personal_voice_claim_allowed": False,
        "personal_voice_conformance_status": "NOT_APPLICABLE",
        "expected_units": sum(
            int(result.get("expected_units", 0)) for result in per_scene.values()
        ),
        "evaluated_units": sum(
            int(result.get("evaluated_units", 0)) for result in per_scene.values()
        ),
        "per_scene": per_scene,
        "review_reasons": (
            []
            if status == "PASS"
            else ["SCENE_PROFILE_SET_CONFORMANCE_NOT_PASS"]
        ),
        "limitations": [
            "PASS confirms per-unit deterministic scene-default binding and validator coverage only.",
            "It does not reproduce or verify a personal author identity.",
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
    negative_guard_registry: dict[str, Any] | None = None
    negative_guard_registry_sha256 = ""
    negative_guard_registry_source_sha256 = ""
    negative_guard_registry_source_format = "NOT_AVAILABLE"
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
        negative_guard_registry = negative_guards.load_negative_guard_registry()
        negative_guard_registry_sha256 = str(
            negative_guard_registry["registry_sha256"]
        )
        negative_guard_registry_source_sha256 = str(
            negative_guard_registry["source_sha256"]
        )
        negative_guard_registry_source_format = str(
            negative_guard_registry["source_format"]
        )
    except (
        OSError,
        UnicodeError,
        negative_guards.NegativeGuardRegistryError,
        ValueError,
    ) as error:
        guard_review_reasons.append(
            f"NEGATIVE_GUARD_REGISTRY_UNAVAILABLE:{type(error).__name__}"
        )

    active_scenes = {str(record.get("scene", "")).upper() for record in evaluated}
    if negative_guard_registry is not None:
        for guard in negative_guard_registry.get("guards", []):
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
        "negative_guard_registry_source_sha256": negative_guard_registry_source_sha256,
        "negative_guard_registry_sha256": negative_guard_registry_sha256,
        "negative_guard_registry_status": (
            str(negative_guard_registry.get("status", ""))
            if negative_guard_registry is not None
            else "NOT_AVAILABLE"
        ),
        "negative_guard_registry_source_format": negative_guard_registry_source_format,
        "negative_guard_loader_version": negative_guards.LOADER_VERSION,
        # Compatibility aliases for v17 receipts. These hashes now bind only
        # the detector registry, never an executable positive-action profile.
        "action_catalog_sha256": negative_guard_registry_source_sha256,
        "action_profile_sha256": negative_guard_registry_sha256,
        "action_profile_status": (
            str(negative_guard_registry.get("status", ""))
            if negative_guard_registry is not None
            else "NOT_AVAILABLE"
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

FAILED_ATTEMPT_METADATA_SCHEMA = "humanize-finalization-failed-attempt/v1"


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


def _is_link_or_reparse(path: Path) -> bool:
    if path.is_symlink():
        return True
    is_junction = getattr(os.path, "isjunction", None)
    if callable(is_junction) and is_junction(path):
        return True
    try:
        attributes = int(getattr(path.lstat(), "st_file_attributes", 0))
    except OSError:
        return False
    return bool(attributes & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0))


def _validate_transaction_source_tree(run_dir: Path) -> None:
    if _is_link_or_reparse(run_dir):
        raise ValueError("run directory must not be a symlink or reparse point")
    stack = [run_dir]
    while stack:
        parent = stack.pop()
        with os.scandir(parent) as entries:
            for entry in entries:
                path = Path(entry.path)
                relative = path.relative_to(run_dir)
                if any(
                    part in TRANSIENT_FINALIZE_NAMES for part in relative.parts
                ):
                    continue
                if _is_link_or_reparse(path):
                    raise ValueError(
                        "run artifact must not be a symlink or reparse point: "
                        + relative.as_posix()
                    )
                if entry.is_dir(follow_symlinks=False):
                    stack.append(path)
                elif entry.is_file(follow_symlinks=False):
                    if path.stat(follow_symlinks=False).st_nlink != 1:
                        raise ValueError(
                            "run artifact hard link is not supported: "
                            + relative.as_posix()
                        )
                else:
                    raise ValueError(
                        "unsupported run artifact type: " + relative.as_posix()
                    )


def _copy_run_state(run_dir: Path, backup_dir: Path) -> None:
    """Copy every non-transient run artifact before publication starts."""
    _validate_transaction_source_tree(run_dir)
    state_before = _run_state_hashes(run_dir)
    backup_dir.mkdir(parents=True, exist_ok=False)
    for source in sorted(run_dir.iterdir()):
        if source.name in TRANSIENT_FINALIZE_NAMES:
            continue
        destination = backup_dir / source.name
        if source.is_symlink():
            raise ValueError(f"run artifact symlink is not supported: {source.name}")
        if source.is_dir():
            shutil.copytree(
                source,
                destination,
                ignore=shutil.ignore_patterns(*TRANSIENT_FINALIZE_NAMES),
            )
        elif source.is_file():
            shutil.copy2(source, destination)
        else:
            raise ValueError(f"unsupported run artifact type: {source.name}")
    state_after = _run_state_hashes(run_dir)
    backup_state = _run_state_hashes(backup_dir)
    if state_before != state_after or state_before != backup_state:
        raise ValueError("run state changed while transaction backup was created")


def _remove_run_artifact(path: Path) -> None:
    if path.is_symlink() or path.is_file():
        path.unlink()
    elif path.is_dir():
        shutil.rmtree(path)


def _restore_run_state(run_dir: Path, backup_dir: Path) -> None:
    """Restore the exact pre-attempt run state while retaining the held lock."""
    for current in sorted(run_dir.iterdir()):
        if current.name == ".finalize.lock":
            continue
        _remove_run_artifact(current)
    for source in sorted(backup_dir.iterdir()):
        destination = run_dir / source.name
        if source.is_dir():
            shutil.copytree(source, destination)
        else:
            shutil.copy2(source, destination)


def _published_evidence_exists(root: Path) -> bool:
    return any(
        (root / name).exists()
        for name in (
            "rendered",
            "rendered_review",
            "rendered_partial",
            "validation",
            "diffs",
            "coverage_ledger.final.csv",
            "rendered_manifest.csv",
            "rollback_manifest.json",
            "finalization_metadata.json",
        )
    )


def _runtime_failure_metadata(
    error: BaseException,
    *,
    run_dir: Path,
    run_state_restored: bool,
    finalization_metadata_preserved: bool,
    published_evidence_preserved: bool,
) -> dict[str, Any]:
    return {
        "schema_version": FAILED_ATTEMPT_METADATA_SCHEMA,
        "tool": "finalize_humanize_long_document.py",
        "created_at": utc_now(),
        "status": "FAIL",
        "exit_code": 1,
        "candidate_assembly_status": "FAIL",
        "delivery_gate_status": "FAIL",
        "publish_state": "FAILED",
        "runtime_error": True,
        "failed_attempt": True,
        "error_type": type(error).__name__,
        "error": str(error),
        "run_dir": str(run_dir),
        "run_state_restored_after_failure": run_state_restored,
        "finalization_metadata_preserved": finalization_metadata_preserved,
        "published_evidence_preserved": published_evidence_preserved,
        "failed_attempt_metadata_path": "last_failed_attempt_metadata.json",
        "failed_attempt_evidence_status": "NOT_RETAINED_AFTER_ROLLBACK",
        "failed_attempt_evidence_paths_reusable": False,
        "humanize_completion_claim_allowed": False,
        "full_completion_claim_allowed": False,
        "academic_correctness": "NOT_EVALUATED",
    }


def _failed_attempt_record(
    metadata: dict[str, Any],
    *,
    run_dir: Path,
    finalization_metadata_preserved: bool,
    published_evidence_preserved: bool,
) -> dict[str, Any]:
    """Detach failed-attempt hashes from restored evidence namespaces."""
    record = json.loads(json.dumps(metadata, ensure_ascii=False))
    resolved_run_dir = run_dir.resolve(strict=False)

    def detach(value: Any, key: str = "") -> Any:
        if isinstance(value, dict):
            return {
                item_key: detach(item_value, str(item_key))
                for item_key, item_value in value.items()
            }
        if isinstance(value, list):
            return [detach(item, key) for item in value]
        if isinstance(value, str) and key in {
            "path",
            "before_path",
            "after_path",
            "diff_path",
            "published_path",
            "cwd",
        }:
            normalized = value.replace("\\", "/")
            is_failed_namespace = normalized.startswith(
                ("validation/", "diffs/", "rendered", ".")
            )
            if value:
                candidate = Path(value)
                if candidate.is_absolute():
                    try:
                        is_failed_namespace = (
                            candidate.resolve(strict=False).is_relative_to(
                                resolved_run_dir
                            )
                        )
                    except (OSError, ValueError):
                        is_failed_namespace = True
            if is_failed_namespace:
                return ""
        return value

    record = detach(record)
    record.update(
        {
            "schema_version": FAILED_ATTEMPT_METADATA_SCHEMA,
            "failed_attempt": True,
            "run_state_restored_after_failure": True,
            "finalization_metadata_preserved": finalization_metadata_preserved,
            "published_evidence_preserved": published_evidence_preserved,
            "failed_attempt_metadata_path": "last_failed_attempt_metadata.json",
            "failed_attempt_evidence_status": "NOT_RETAINED_AFTER_ROLLBACK",
            "failed_attempt_evidence_paths_reusable": False,
        }
    )
    return record


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
    process_containment: str = "NOT_RUN",
    descendant_cleanup: str = "NOT_RUN",
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
        "process_containment": process_containment,
        "descendant_cleanup": descendant_cleanup,
    }


def _assign_windows_kill_on_close_job(process: subprocess.Popen[str]) -> Any:
    import ctypes
    from ctypes import wintypes

    class IO_COUNTERS(ctypes.Structure):
        _fields_ = [
            ("ReadOperationCount", ctypes.c_uint64),
            ("WriteOperationCount", ctypes.c_uint64),
            ("OtherOperationCount", ctypes.c_uint64),
            ("ReadTransferCount", ctypes.c_uint64),
            ("WriteTransferCount", ctypes.c_uint64),
            ("OtherTransferCount", ctypes.c_uint64),
        ]

    class JOBOBJECT_BASIC_LIMIT_INFORMATION(ctypes.Structure):
        _fields_ = [
            ("PerProcessUserTimeLimit", ctypes.c_int64),
            ("PerJobUserTimeLimit", ctypes.c_int64),
            ("LimitFlags", wintypes.DWORD),
            ("MinimumWorkingSetSize", ctypes.c_size_t),
            ("MaximumWorkingSetSize", ctypes.c_size_t),
            ("ActiveProcessLimit", wintypes.DWORD),
            ("Affinity", ctypes.c_size_t),
            ("PriorityClass", wintypes.DWORD),
            ("SchedulingClass", wintypes.DWORD),
        ]

    class JOBOBJECT_EXTENDED_LIMIT_INFORMATION(ctypes.Structure):
        _fields_ = [
            ("BasicLimitInformation", JOBOBJECT_BASIC_LIMIT_INFORMATION),
            ("IoInfo", IO_COUNTERS),
            ("ProcessMemoryLimit", ctypes.c_size_t),
            ("JobMemoryLimit", ctypes.c_size_t),
            ("PeakProcessMemoryUsed", ctypes.c_size_t),
            ("PeakJobMemoryUsed", ctypes.c_size_t),
        ]

    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel32.CreateJobObjectW.argtypes = [ctypes.c_void_p, wintypes.LPCWSTR]
    kernel32.CreateJobObjectW.restype = wintypes.HANDLE
    kernel32.SetInformationJobObject.argtypes = [
        wintypes.HANDLE,
        ctypes.c_int,
        ctypes.c_void_p,
        wintypes.DWORD,
    ]
    kernel32.SetInformationJobObject.restype = wintypes.BOOL
    kernel32.AssignProcessToJobObject.argtypes = [wintypes.HANDLE, wintypes.HANDLE]
    kernel32.AssignProcessToJobObject.restype = wintypes.BOOL
    kernel32.TerminateJobObject.argtypes = [wintypes.HANDLE, wintypes.UINT]
    kernel32.TerminateJobObject.restype = wintypes.BOOL
    kernel32.CloseHandle.argtypes = [wintypes.HANDLE]
    kernel32.CloseHandle.restype = wintypes.BOOL

    job = kernel32.CreateJobObjectW(None, None)
    if not job:
        raise ctypes.WinError(ctypes.get_last_error())
    information = JOBOBJECT_EXTENDED_LIMIT_INFORMATION()
    information.BasicLimitInformation.LimitFlags = 0x00002000
    if not kernel32.SetInformationJobObject(
        job, 9, ctypes.byref(information), ctypes.sizeof(information)
    ):
        error = ctypes.WinError(ctypes.get_last_error())
        kernel32.CloseHandle(job)
        raise error
    if not kernel32.AssignProcessToJobObject(
        job, wintypes.HANDLE(int(process._handle))
    ):
        error = ctypes.WinError(ctypes.get_last_error())
        kernel32.CloseHandle(job)
        raise error
    return job, kernel32


def _terminate_compile_process_tree(
    process: subprocess.Popen[str], containment: Any
) -> str:
    if os.name == "nt":
        job, kernel32 = containment
        terminated = bool(kernel32.TerminateJobObject(job, 1))
        closed = bool(kernel32.CloseHandle(job))
        return "PASS" if terminated and closed else "FAIL"
    try:
        os.killpg(process.pid, signal.SIGKILL)
    except ProcessLookupError:
        pass
    except OSError:
        return "FAIL"
    return "PASS"


def _run_compile(command: str | None, cwd: Path) -> dict[str, Any]:
    if not command:
        return _compile_check_result(status="NOT_RUN")
    wrapper = (
        "import subprocess,sys; "
        "command=sys.stdin.read(); "
        "raise SystemExit(subprocess.call(command, shell=True))"
    )
    with tempfile.TemporaryFile() as stdout_file, tempfile.TemporaryFile() as stderr_file:
        popen_kwargs: dict[str, Any] = {
            "cwd": cwd,
            "stdin": subprocess.PIPE,
            "stdout": stdout_file,
            "stderr": stderr_file,
            "text": True,
            "encoding": "utf-8",
            "errors": "replace",
        }
        if os.name == "nt":
            popen_kwargs["creationflags"] = subprocess.CREATE_NO_WINDOW
            process_containment = "WINDOWS_JOB_OBJECT"
        else:
            popen_kwargs["start_new_session"] = True
            process_containment = "POSIX_PROCESS_GROUP"
        process = subprocess.Popen(
            [sys.executable, "-X", "utf8", "-c", wrapper],
            **popen_kwargs,
        )
        containment: Any = None
        try:
            if os.name == "nt":
                containment = _assign_windows_kill_on_close_job(process)
            process.communicate(command)
        except Exception:
            process.kill()
            process.wait()
            if containment is not None:
                _terminate_compile_process_tree(process, containment)
            raise
        descendant_cleanup = _terminate_compile_process_tree(
            process,
            containment,
        )
        stdout_file.seek(0)
        stderr_file.seek(0)
        stdout = stdout_file.read().decode("utf-8", errors="replace")
        stderr = stderr_file.read().decode("utf-8", errors="replace")
    status = (
        "PASS"
        if process.returncode == 0 and descendant_cleanup == "PASS"
        else "FAIL"
    )
    if descendant_cleanup != "PASS":
        stderr = (stderr + "\ncompile descendant cleanup failed").strip()
    return _compile_check_result(
        status=status,
        command=command,
        exit_code=process.returncode,
        stdout=stdout[-8000:],
        stderr=stderr[-8000:],
        cwd=cwd,
        process_containment=process_containment,
        descendant_cleanup=descendant_cleanup,
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
    "scene_requested",
    "scene_document_prior",
    "scene_routing_decision",
    "scene_routing_policy_sha256",
    "scene_routing_policy_revision",
    "scene_routing_top_score",
    "scene_routing_margin",
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
    "structural_plan_status",
    "structural_semantic_review_status",
    "paired_quality_review_status",
    "transaction_id",
    "transaction_status",
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
    voice_bindings: dict[str, dict[str, Any]],
    scene_policy_path: Path,
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
    intensity = str(metadata.get("intensity", "")).upper()
    if intensity not in preparer.REWRITE_INTENSITIES:
        raise ValueError("run_metadata.json has invalid rewrite intensity")
    wrappers = frozenset(str(item) for item in metadata.get("editable_style_wrappers", []))
    expected_units: list[dict[str, Any]] = []
    expected_spans: list[dict[str, Any]] = []
    frozen_texts: dict[str, str] = {}
    spans_by_file: dict[str, list[dict[str, Any]]] = {}
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
        file_id = str(record.get("file_id", ""))
        frozen_texts[file_id] = text
        local_spans = preparer.protected_spans(
            text,
            str(record.get("suffix", "")),
            str(record.get("file_id", "")),
            wrappers,
        )
        spans_by_file[file_id] = local_spans
        expected_spans.extend(local_spans)
    document_priors = preparer.build_logical_document_priors(
        [dict(record) for record in file_manifest],
        frozen_texts,
        spans_by_file,
        requested_scene=scene,
        scene_policy_path=scene_policy_path,
    )
    for record in file_manifest:
        file_id = str(record.get("file_id", ""))
        text = frozen_texts.get(file_id)
        if text is None:
            continue
        local_spans = spans_by_file[file_id]
        file_units = preparer.build_units(
            dict(record),
            text,
            local_spans,
            requested_scene=scene,
            voice_bindings=voice_bindings,
            scene_policy_path=scene_policy_path,
            document_prior_scene=document_priors.get(file_id, ""),
            intensity=intensity,
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
        "scene", "scene_requested", "scene_document_prior", "scene_routing_decision", "scene_routing_policy_sha256",
        "scene_routing_policy_revision", "scene_routing_top_score", "scene_routing_margin",
        "voice_profile_id", "voice_profile_revision", "voice_profile_confidence",
        "voice_profile_kind", "voice_profile_source", "voice_profile_binding_scene",
        "voice_profile_sha256", "voice_default_disclosure", "chunk_binding_sha256",
        "mode", "intensity", "structural_plan_status", "owner_chunk", "context_before_unit", "context_after_unit",
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
                "file_id", "path", "parent_file_id", "relation", "suffix", "bytes", "readable_bytes", "encoding", "sha256", "modified_at",
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


def _validate_prepare_metadata_derivations(
    metadata: dict[str, Any],
    snapshot: dict[str, Any],
    file_manifest: Sequence[dict[str, str]],
    units: Sequence[dict[str, Any]],
    spans: Sequence[dict[str, Any]],
    transaction_inventory: dict[str, Any] | None,
) -> None:
    expected_fields = {
        "tool",
        "created_at",
        "snapshot_id",
        "status",
        "scene",
        "intensity",
        "voice_binding",
        "scene_routing_status",
        "scene_routing_policy_sha256",
        "scene_routing_policy_revision",
        "scene_routing_summary",
        "budgets",
        "editable_style_wrappers",
        "files_total",
        "units_total",
        "protected_spans_total",
        "file_statuses",
        "unit_statuses",
        "processable_editable_units",
        "no_editable_scope",
        "completion_claim_allowed",
        "next_action",
        "integrity_manifest",
        "policy_snapshot",
        "policy_snapshot_sha256",
    }
    if transaction_inventory is not None:
        expected_fields.update(
            {
                "structural_transaction_scope",
                "structural_transaction_candidates",
                "structural_transaction_inventory",
                "structural_transaction_inventory_sha256",
                "structural_transaction_policy_revision",
                "structural_transaction_policy_sha256",
            }
        )
    if set(metadata) != expected_fields:
        raise ValueError("run metadata fields mismatch")
    preparer.validate_policy_snapshot(
        metadata.get("policy_snapshot"),
        metadata.get("policy_snapshot_sha256"),
    )
    if metadata.get("tool") != "prepare_humanize_long_document.py":
        raise ValueError("run metadata tool mismatch")
    created_at = metadata.get("created_at")
    if not isinstance(created_at, str):
        raise ValueError("run metadata created_at is invalid")
    try:
        datetime.fromisoformat(created_at.replace("Z", "+00:00"))
    except ValueError as error:
        raise ValueError("run metadata created_at is invalid") from error
    if metadata.get("snapshot_id") != snapshot.get("snapshot_id"):
        raise ValueError("run metadata snapshot binding mismatch")
    intensity = str(metadata.get("intensity", "")).upper()
    if intensity not in preparer.REWRITE_INTENSITIES:
        raise ValueError("run metadata intensity is invalid")
    if any(str(unit.get("intensity", "")).upper() != intensity for unit in units):
        raise ValueError("run metadata intensity does not match units")

    budgets = metadata.get("budgets")
    if not isinstance(budgets, dict) or set(budgets) != {
        "max_author_chars",
        "max_lines",
        "min_author_chars",
    }:
        raise ValueError("run metadata budgets mismatch")
    if any(
        not isinstance(value, int) or isinstance(value, bool) or value < 0
        for value in budgets.values()
    ):
        raise ValueError("run metadata budgets are invalid")
    wrappers = metadata.get("editable_style_wrappers")
    if (
        not isinstance(wrappers, list)
        or wrappers != sorted(set(wrappers))
        or any(item not in preparer.EDITABLE_STYLE_WRAPPERS for item in wrappers)
    ):
        raise ValueError("run metadata editable wrappers mismatch")

    file_statuses = Counter(str(record.get("status", "")) for record in file_manifest)
    unit_statuses = Counter(str(unit.get("status", "")) for unit in units)
    routing_decisions = Counter(
        str(unit.get("scene_routing_decision", ""))
        for unit in units
        if int(unit.get("author_chars", 0)) > 0
    )
    if not routing_decisions:
        scene_routing_status = "NOT_EVALUATED"
    elif routing_decisions.get("AMBIGUOUS"):
        scene_routing_status = "REVIEW"
    else:
        scene_routing_status = "PASS"
    processable = unit_statuses.get("PENDING", 0)
    run_status = (
        "REVIEW"
        if any(
            status in unit_statuses
            for status in ("UNRESOLVED", "SKIPPED_GARBLED", "CHANGED_AFTER_SNAPSHOT")
        )
        or any(
            status in file_statuses
            for status in (
                "UNRESOLVED",
                "UNRESOLVED_INCLUDE",
                "SKIPPED_GARBLED",
                "CHANGED_AFTER_SNAPSHOT",
            )
        )
        or processable == 0
        else "READY"
    )
    expected_values = {
        "status": run_status,
        "scene_routing_status": scene_routing_status,
        "scene_routing_summary": dict(sorted(routing_decisions.items())),
        "files_total": len(file_manifest),
        "units_total": len(units),
        "protected_spans_total": len(spans),
        "file_statuses": dict(sorted(file_statuses.items())),
        "unit_statuses": dict(sorted(unit_statuses.items())),
        "processable_editable_units": processable,
        "no_editable_scope": processable == 0,
        "completion_claim_allowed": False,
        "next_action": "Rewrite only PENDING chunk files, then validate and finalize them.",
        "integrity_manifest": "prepare_integrity.json",
    }
    if transaction_inventory is not None:
        expected_values.update(
            {
                "structural_transaction_scope": transaction_inventory[
                    "candidate_scope"
                ],
                "structural_transaction_candidates": len(
                    transaction_inventory["transactions"]
                ),
                "structural_transaction_inventory": (
                    "structural_transaction_inventory.json"
                ),
                "structural_transaction_inventory_sha256": transaction_inventory[
                    "inventory_sha256"
                ],
                "structural_transaction_policy_revision": transaction_inventory[
                    "eligibility_policy_revision"
                ],
                "structural_transaction_policy_sha256": transaction_inventory[
                    "eligibility_policy_sha256"
                ],
            }
        )
    mismatches = [
        key for key, expected in expected_values.items() if metadata.get(key) != expected
    ]
    if mismatches:
        raise ValueError(
            "run metadata derived fields mismatch: " + ",".join(sorted(mismatches))
        )


def _finalize_locked(
    run_dir: Path,
    rewrites_dir: Path,
    *,
    check_command: str | None = None,
    second_pass_receipt: Path | None = None,
) -> dict[str, Any]:
    _verify_prepare_integrity(run_dir)
    snapshot = _load_json(run_dir / "snapshot.json")
    file_manifest = _load_csv(run_dir / "file_manifest.csv")
    units = _load_jsonl(run_dir / "units.jsonl")
    spans = _load_jsonl(run_dir / "protected_spans.jsonl")
    run_metadata = _load_json(run_dir / "run_metadata.json")
    preparer.validate_policy_snapshot(
        run_metadata.get("policy_snapshot"),
        run_metadata.get("policy_snapshot_sha256"),
    )
    scene_policy_path = _validate_scene_routing_policy(run_dir, run_metadata)
    frozen_voice_profiles, voice_bindings, voice_identity = _validate_voice_profile_binding(
        run_dir, run_metadata, units
    )
    _rebuild_prepare_state(
        run_dir,
        snapshot,
        file_manifest,
        run_metadata,
        units,
        spans,
        voice_bindings,
        scene_policy_path,
    )
    _validate_initial_unit_states(units)
    transaction_inventory = _validate_structural_transaction_inventory(
        run_dir,
        run_metadata,
        snapshot,
        file_manifest,
        units,
    )
    _validate_prepare_metadata_derivations(
        run_metadata,
        snapshot,
        file_manifest,
        units,
        spans,
        transaction_inventory,
    )
    span_map = {item["protected_id"]: item for item in spans}
    unit_map = {item["unit_id"]: item for item in units}
    chunks: dict[str, dict[str, Any]] = {}
    for unit_id in unit_map:
        chunk = _load_json(run_dir / "chunks" / f"{unit_id}.json")
        if not isinstance(chunk, dict) or chunk.get("unit_id") != unit_id:
            raise ValueError(f"invalid chunk payload for {unit_id}")
        chunks[unit_id] = chunk
    rewrites, transaction_bundles, transaction_declines = collect_rewrites(rewrites_dir)
    unknown_units = sorted(set(rewrites) - set(unit_map))
    if unknown_units:
        raise ValueError("unknown rewrite units: " + ",".join(unknown_units))
    transaction_decision_conflicts = sorted(
        set(transaction_bundles) & set(transaction_declines)
    )
    if transaction_decision_conflicts:
        raise ValueError(
            "structural transaction execution and decline conflict: "
            + ",".join(transaction_decision_conflicts)
        )
    bound_transaction_declines: dict[str, dict[str, Any]] = {}
    for transaction_id, bundle in transaction_declines.items():
        candidate = _bound_structural_transaction_decline_candidate(
            bundle, transaction_inventory, unit_map, chunks
        )
        unit_ids = [str(item["unit_id"]) for item in bundle["unit_bindings"]]
        bound_transaction_declines[transaction_id] = {
            "schema_version": STRUCTURAL_TRANSACTION_DECLINE_SCHEMA,
            "status": "PASS",
            "disposition": "DECLINED",
            "transaction_id": transaction_id,
            "transaction_binding_sha256": candidate[
                "transaction_binding_sha256"
            ],
            "transaction_inventory_sha256": bundle[
                "transaction_inventory_sha256"
            ],
            "unit_ids": unit_ids,
            "bundle_sha256": _structural_transaction_bundle_sha256(bundle),
            "reason_code": bundle["reason_code"],
            "reason": bundle["reason"],
            "evidence_refs": bundle["evidence_refs"],
            "evidence_member_coverage": "PASS",
            "path": str(
                Path("validation") / f"{transaction_id}.decline.json"
            ).replace("\\", "/"),
        }
    unit_to_transaction: dict[str, str] = {}
    for transaction_id, bundle in transaction_bundles.items():
        participant_ids = _structural_transaction_unit_ids(bundle)
        unknown_participants = sorted(set(participant_ids) - set(unit_map))
        if unknown_participants:
            raise ValueError(
                "unknown structural transaction units: "
                + ",".join(unknown_participants)
            )
        overlap = sorted(set(participant_ids) & set(rewrites))
        if overlap:
            raise ValueError(
                "structural transaction member also has standalone rewrite: "
                + ",".join(overlap)
            )
        for unit_id in participant_ids:
            existing = unit_to_transaction.get(unit_id)
            if existing is not None:
                raise ValueError(
                    "structural transaction member claimed twice: "
                    f"{unit_id}:{existing},{transaction_id}"
                )
            unit_to_transaction[unit_id] = transaction_id

    validation_dir = run_dir / ".validation_staging"
    diffs_dir = run_dir / ".diffs_staging"
    staging_dir = run_dir / ".rendered_staging"
    for temporary in (validation_dir, diffs_dir, staging_dir):
        if temporary.exists():
            shutil.rmtree(temporary)
    validation_dir.mkdir()
    diffs_dir.mkdir()
    staging_dir.mkdir()
    for transaction_id, decline_record in sorted(
        bound_transaction_declines.items()
    ):
        _write_json(
            validation_dir / f"{transaction_id}.decline.json", decline_record
        )

    existing_rendered_before = (run_dir / "rendered").is_dir()
    existing_partial_before = (run_dir / "rendered_partial").is_dir()
    existing_review_before = (run_dir / "rendered_review").is_dir()
    previous_accepted_units: set[str] = set()
    previous_ledger_path = run_dir / "coverage_ledger.final.csv"
    previous_partial_state_missing = (
        existing_partial_before or existing_review_before
    ) and not previous_ledger_path.is_file()
    if (existing_partial_before or existing_review_before) and previous_ledger_path.is_file():
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
    voice_hash_matched_units: set[str] = set()
    voice_hash_missing_units: set[str] = set()
    voice_hash_mismatched_units: set[str] = set()
    chunk_binding_matched_units: set[str] = set()
    chunk_binding_missing_units: set[str] = set()
    chunk_binding_mismatched_units: set[str] = set()

    accepted_by_file: dict[str, list[tuple[int, int, str, str]]] = {}
    invariant_baseline_by_file: dict[str, list[tuple[int, int, str, str]]] = {}
    validation_payloads: dict[str, dict[str, Any]] = {}
    structural_plan_payloads: dict[str, dict[str, Any]] = {}
    structural_semantic_review_requests: dict[str, dict[str, Any]] = {}
    paired_quality_review_requests: dict[str, dict[str, Any]] = {}
    accepted_masked_by_unit: dict[str, str] = {}
    structural_transaction_results: dict[str, dict[str, Any]] = {}
    structural_transaction_review_requests: dict[str, dict[str, Any]] = {}
    bound_transaction_execution_ids: set[str] = set()
    for transaction_id, bundle in transaction_bundles.items():
        participant_ids = [str(item["unit_id"]) for item in bundle["unit_bindings"]]
        bundle_sha256 = _structural_transaction_bundle_sha256(bundle)
        try:
            candidate = _bound_structural_transaction_candidate(
                bundle, transaction_inventory, unit_map
            )
        except ValueError as error:
            transaction_result = {
                "transaction_id": transaction_id,
                "bundle_sha256": bundle_sha256,
                "unit_ids": participant_ids,
                "status": "REVIEW",
                "atomic_gate_status": "ROLLED_BACK",
                "source_member_claim_status": "NOT_RUN",
                "source_member_claim_sha256": "",
                "fragment_gate_statuses": {
                    unit_id: "NOT_RUN" for unit_id in participant_ids
                },
                "document_gate_status": "NOT_RUN",
                "change_applied": False,
                "cross_unit_moves_applied": 0,
                "rollback_reason": "AUTHORITY_BINDING",
                "errors": [str(error)],
                "review_request": {},
            }
        else:
            bound_transaction_execution_ids.add(transaction_id)
            chunk_binding_matched_units.update(participant_ids)
            voice_hash_matched_units.update(participant_ids)
            transaction_result = _validate_structural_transaction(
                bundle=bundle,
                candidate=candidate,
                snapshot_id=str(snapshot["snapshot_id"]),
                unit_map=unit_map,
                chunks=chunks,
                file_texts=file_texts,
                file_suffixes=file_suffixes,
                span_map=span_map,
                validation_dir=validation_dir,
            )

        fragment_results = transaction_result.pop("_fragment_results", {})
        document_gate = transaction_result.pop("_document_gate", None)
        review_request = transaction_result.pop("_review_request", None)
        if document_gate is not None:
            _write_json(
                validation_dir / f"{transaction_id}.document-gate.json",
                document_gate,
            )
        if transaction_result["atomic_gate_status"] == "PASS":
            if not isinstance(review_request, dict):
                raise ValueError(
                    "structural transaction PASS without semantic review request"
                )
            request_name = (
                f"{transaction_id}.structural-transaction-review-request.json"
            )
            _write_json(validation_dir / request_name, review_request)
            request_record = {
                "status": "PENDING_EXTERNAL_REVIEW",
                "path": str(Path("validation") / request_name).replace("\\", "/"),
                "request_sha256": review_request["request_sha256"],
            }
            transaction_result["review_request"] = request_record
            structural_transaction_review_requests[transaction_id] = request_record
            for unit_id in participant_ids:
                unit = unit_map[unit_id]
                fragment_result = fragment_results[unit_id]
                transaction_fragment = next(
                    item
                    for item in bundle["fragments"]
                    if item["target_unit_id"] == unit_id
                )
                accepted_masked_by_unit[unit_id] = str(
                    transaction_fragment["masked_text"]
                )
                plan_payload = dict(fragment_result["plan_check_public"])
                plan_payload.update(
                    {
                        "status": "PASS",
                        "change_applied": True,
                        "transaction_id": transaction_id,
                        "transaction_atomic_gate_status": "PASS",
                        "semantic_mapping": "NOT_EVALUATED",
                        "semantic_review_status": "PENDING_EXTERNAL_REVIEW",
                        "semantic_review": request_record,
                    }
                )
                structural_plan_payloads[unit_id] = plan_payload
                _write_json(
                    validation_dir / f"{unit_id}.structural.json", plan_payload
                )
                validation_payloads[unit_id] = fragment_result[
                    "validation_payload"
                ]
                paired_quality_request = fragment_result.get(
                    "paired_quality_review_request"
                )
                if isinstance(paired_quality_request, dict):
                    paired_quality_review_requests[unit_id] = (
                        paired_quality_request
                    )
                structural_semantic_review_requests[unit_id] = request_record
                unit["status"] = "DONE"
                unit["structural_plan_status"] = "PASS"
                unit["structural_semantic_review_status"] = (
                    "PENDING_EXTERNAL_REVIEW"
                )
                unit["style_validation"] = "PASS"
                unit["paired_quality_review_status"] = (
                    paired_quality_request.get("status", "NOT_EVALUATED")
                    if isinstance(paired_quality_request, dict)
                    else "NOT_EVALUATED"
                )
                unit["protected_hashes_ok"] = "PASS"
                unit["hash_after"] = sha256(
                    fragment_result["restored"].encode("utf-8")
                )
                diff = "".join(
                    difflib.unified_diff(
                        fragment_result["original"].splitlines(keepends=True),
                        fragment_result["restored"].splitlines(keepends=True),
                        fromfile=f"{unit_id}.before",
                        tofile=f"{unit_id}.after",
                    )
                )
                diff_path = diffs_dir / f"{unit_id}.diff"
                diff_path.write_text(diff, encoding="utf-8")
                unit["diff_path"] = str(Path("diffs") / diff_path.name)
                unit["transaction_id"] = transaction_id
                unit["transaction_status"] = "ATOMIC_PASS"
                unit["notes"] = "bound_structural_transaction_review_candidate"
                accepted_by_file.setdefault(str(unit["file_id"]), []).append(
                    (
                        int(unit["start"]),
                        int(unit["end"]),
                        fragment_result["restored"],
                        unit_id,
                    )
                )
                invariant_baseline_by_file.setdefault(
                    str(unit["file_id"]), []
                ).append(
                    (
                        int(unit["start"]),
                        int(unit["end"]),
                        fragment_result["invariant_before"],
                        unit_id,
                    )
                )
        else:
            for unit_id in participant_ids:
                _discard_paired_quality_review_request(
                    paired_quality_review_requests, validation_dir, unit_id
                )
                unit = unit_map[unit_id]
                fragment_result = fragment_results.get(unit_id, {})
                fragment_status = transaction_result[
                    "fragment_gate_statuses"
                ].get(unit_id, "NOT_RUN")
                unit["status"] = "UNRESOLVED"
                unit["structural_plan_status"] = "REVIEW"
                unit["structural_semantic_review_status"] = "NOT_ISSUED"
                unit["style_validation"] = fragment_status
                unit["protected_hashes_ok"] = (
                    "FAIL"
                    if any("protected" in item for item in transaction_result["errors"])
                    else "NOT_RUN"
                )
                unit["hash_after"] = ""
                unit["diff_path"] = ""
                unit["transaction_id"] = transaction_id
                unit["transaction_status"] = "ROLLED_BACK"
                unit["notes"] = (
                    "structural_transaction_rolled_back:"
                    + str(transaction_result["rollback_reason"])
                )
                plan_payload = {
                    "status": "REVIEW",
                    "change_applied": False,
                    "transaction_id": transaction_id,
                    "transaction_atomic_gate_status": "ROLLED_BACK",
                    "fragment_plan_status": (
                        fragment_result.get("plan_check_public", {}).get(
                            "status", "NOT_RUN"
                        )
                    ),
                    "semantic_mapping": "NOT_EVALUATED",
                    "semantic_review_status": "NOT_ISSUED",
                    "error": unit["notes"],
                }
                structural_plan_payloads[unit_id] = plan_payload
                _write_json(
                    validation_dir / f"{unit_id}.structural.json", plan_payload
                )
                if "validation_payload" in fragment_result:
                    validation_payloads[unit_id] = fragment_result[
                        "validation_payload"
                    ]
        structural_transaction_results[transaction_id] = transaction_result
        _write_json(
            validation_dir / f"{transaction_id}.transaction.json",
            transaction_result,
        )

    transaction_candidates = (
        transaction_inventory.get("transactions", [])
        if isinstance(transaction_inventory, dict)
        else []
    )
    structural_transaction_candidate_dispositions: dict[str, dict[str, Any]] = {}
    for candidate in transaction_candidates:
        transaction_id = str(candidate["transaction_id"])
        unit_ids = [
            str(item["unit_id"]) for item in candidate.get("compound_refs", [])
        ]
        common = {
            "transaction_id": transaction_id,
            "transaction_binding_sha256": candidate[
                "transaction_binding_sha256"
            ],
            "unit_ids": unit_ids,
        }
        if transaction_id in bound_transaction_execution_ids:
            transaction_result = structural_transaction_results[transaction_id]
            disposition = {
                **common,
                "disposition": "EXECUTED",
                "bundle_sha256": transaction_result["bundle_sha256"],
                "execution_status": transaction_result["atomic_gate_status"],
                "rollback_reason": transaction_result["rollback_reason"],
            }
        elif transaction_id in bound_transaction_declines:
            decline_record = bound_transaction_declines[transaction_id]
            disposition = {
                **common,
                "disposition": "DECLINED",
                "bundle_sha256": decline_record["bundle_sha256"],
                "reason_code": decline_record["reason_code"],
                "reason": decline_record["reason"],
                "evidence_refs": decline_record["evidence_refs"],
                "evidence_member_coverage": "PASS",
                "path": decline_record["path"],
            }
        else:
            disposition = {
                **common,
                "disposition": "PENDING",
                "reason": "no bound execution or decline artifact",
            }
        structural_transaction_candidate_dispositions[transaction_id] = disposition

    structural_transaction_candidates_total = len(
        structural_transaction_candidate_dispositions
    )
    structural_transaction_candidates_executed = sum(
        item["disposition"] == "EXECUTED"
        for item in structural_transaction_candidate_dispositions.values()
    )
    structural_transaction_candidates_declined = sum(
        item["disposition"] == "DECLINED"
        for item in structural_transaction_candidate_dispositions.values()
    )
    structural_transaction_candidates_pending = sum(
        item["disposition"] == "PENDING"
        for item in structural_transaction_candidate_dispositions.values()
    )
    transaction_inventory_status = (
        str(transaction_inventory.get("status", ""))
        if isinstance(transaction_inventory, dict)
        else "NOT_APPLICABLE"
    )
    if transaction_inventory_status in {"NOT_APPLICABLE", "DISABLED"}:
        structural_transaction_candidate_coverage_status = "NOT_APPLICABLE"
        structural_transaction_scope_complete: bool | None = None
    elif transaction_inventory_status == "EMPTY":
        structural_transaction_candidate_coverage_status = "PASS"
        structural_transaction_scope_complete = True
    elif structural_transaction_candidates_pending:
        structural_transaction_candidate_coverage_status = "REVIEW"
        structural_transaction_scope_complete = False
    else:
        structural_transaction_candidate_coverage_status = "PASS"
        structural_transaction_scope_complete = True

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
            voice_error = _bundle_voice_binding_error(
                bundle, str(unit.get("voice_profile_sha256", ""))
            )
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
            if bundle.get("structural_plan") is not None:
                unit["status"] = "UNRESOLVED"
                unit["structural_plan_status"] = "FAIL"
                unit["notes"] = "structural_plan_not_allowed_for_NO_CHANGE"
                structural_plan_payloads[unit_id] = {
                    "status": "FAIL",
                    "error": unit["notes"],
                }
                _write_json(
                    validation_dir / f"{unit_id}.structural.json",
                    structural_plan_payloads[unit_id],
                )
                continue
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
            _stabilize_validation_evidence_refs(
                no_change_payload, unit_id, suffix
            )
            paired_quality_request = _persist_paired_quality_review_request(
                no_change_payload, validation_dir, unit_id
            )
            if isinstance(paired_quality_request, dict):
                paired_quality_review_requests[unit_id] = paired_quality_request
                unit["paired_quality_review_status"] = paired_quality_request[
                    "status"
                ]
            else:
                unit["paired_quality_review_status"] = "NOT_EVALUATED"
            no_change_structural = {
                "status": (
                    "PASS"
                    if str(unit.get("intensity", "")).upper() == "STRUCTURAL"
                    else "NOT_APPLICABLE"
                ),
                "change_applied": False,
                "decision": "NO_CHANGE",
                "semantic_mapping": (
                    "PASS"
                    if str(unit.get("intensity", "")).upper() == "STRUCTURAL"
                    else "NOT_APPLICABLE"
                ),
                "semantic_review_status": "NOT_REQUIRED",
            }
            unit["structural_plan_status"] = no_change_structural["status"]
            unit["structural_semantic_review_status"] = no_change_structural[
                "semantic_review_status"
            ]
            structural_plan_payloads[unit_id] = no_change_structural
            no_change_payload["structural_plan_check"] = no_change_structural
            validation_payloads[unit_id] = no_change_payload
            _write_json(validation_dir / f"{unit_id}.validation.json", no_change_payload)
            _write_json(
                validation_dir / f"{unit_id}.structural.json",
                no_change_structural,
            )
            if no_change_payload["mechanical_validation_status"] != "PASS":
                unit["status"] = "UNRESOLVED"
                unit["style_validation"] = no_change_payload[
                    "mechanical_validation_status"
                ]
                unit["notes"] = (
                    "NO_CHANGE validator:"
                    + no_change_payload["mechanical_validation_status"]
                )
                continue
            if not _quality_review_only(no_change_payload):
                unit["status"] = "UNRESOLVED"
                unit["style_validation"] = "REVIEW"
                unit["notes"] = "NO_CHANGE paired quality request missing"
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
        suffix = file_suffixes.get(str(unit["file_id"]), ".txt") or ".txt"
        try:
            structural_plan_check = _validate_structural_plan(
                bundle,
                unit,
                chunks[unit_id],
                masked_text,
                suffix,
                span_map,
            )
        except ValueError as error:
            structural_plan_check = {
                "status": "FAIL",
                "error": str(error),
                "semantic_mapping": "NOT_EVALUATED",
            }
            structural_plan_payloads[unit_id] = structural_plan_check
            _write_json(
                validation_dir / f"{unit_id}.structural.json",
                structural_plan_check,
            )
            unit["status"] = "UNRESOLVED"
            unit["structural_plan_status"] = "FAIL"
            unit["structural_semantic_review_status"] = "NOT_ISSUED"
            unit["notes"] = "structural_plan:" + str(error)
            continue
        structural_baseline_masked = str(
            structural_plan_check.pop(
                "_baseline_masked_text",
                chunks[unit_id].get("masked_text", ""),
            )
        )
        structural_plan_check["invariant_baseline_sha256"] = sha256(
            structural_baseline_masked.encode("utf-8")
        )
        structural_plan_payloads[unit_id] = structural_plan_check
        _write_json(
            validation_dir / f"{unit_id}.structural.json",
            structural_plan_check,
        )
        unit["structural_plan_status"] = structural_plan_check["status"]
        unit["structural_semantic_review_status"] = (
            "NOT_ISSUED"
            if structural_plan_check.get("change_applied") is True
            else "NOT_REQUIRED"
        )
        restored, restore_errors = restore_protected(masked_text, unit["protected_ids"], span_map)
        if restored is None:
            unit["status"] = "UNRESOLVED"
            unit["protected_hashes_ok"] = "FAIL"
            unit["notes"] = " | ".join(restore_errors)
            continue
        invariant_before, invariant_restore_errors = restore_protected(
            structural_baseline_masked,
            unit["protected_ids"],
            span_map,
        )
        if invariant_before is None:
            unit["status"] = "UNRESOLVED"
            unit["protected_hashes_ok"] = "FAIL"
            unit["notes"] = "structural_baseline_restore:" + " | ".join(
                invariant_restore_errors
            )
            continue
        actual_structural_content_changed = restored != invariant_before
        structural_plan_check["actual_content_changed"] = (
            actual_structural_content_changed
        )
        paragraph_order_check = _non_structural_paragraph_order_check(
            structural_baseline_masked,
            masked_text,
            str(unit.get("intensity", "")),
        )
        structural_plan_check["non_structural_paragraph_order_check"] = (
            paragraph_order_check
        )
        if paragraph_order_check["status"] == "REVIEW":
            structural_plan_check.update(
                {
                    "status": "REVIEW",
                    "semantic_mapping": "NOT_EVALUATED",
                    "semantic_review_status": "BLOCKED_BY_SCOPE_VIOLATION",
                    "error": "undeclared_paragraph_reorder_not_allowed_for_non_structural_run",
                }
            )
            structural_plan_payloads[unit_id] = structural_plan_check
            _write_json(
                validation_dir / f"{unit_id}.structural.json",
                structural_plan_check,
            )
            unit["status"] = "UNRESOLVED"
            unit["structural_plan_status"] = "REVIEW"
            unit["structural_semantic_review_status"] = "BLOCKED_BY_SCOPE_VIOLATION"
            unit["notes"] = "non_structural_paragraph_reorder_detected"
            continue
        if (
            str(unit.get("intensity", "")).upper() == "STRUCTURAL"
            and actual_structural_content_changed
            and structural_plan_check.get("change_applied") is not True
        ):
            structural_plan_check["semantic_mapping"] = "NOT_EVALUATED"
            structural_plan_check["semantic_review_status"] = (
                "PENDING_EXTERNAL_REVIEW"
            )
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
        before_path.write_text(invariant_before, encoding="utf-8")
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
        _stabilize_validation_evidence_refs(payload, unit_id, suffix)
        paired_quality_request = _persist_paired_quality_review_request(
            payload, validation_dir, unit_id
        )
        if isinstance(paired_quality_request, dict):
            paired_quality_review_requests[unit_id] = paired_quality_request
            unit["paired_quality_review_status"] = paired_quality_request["status"]
        else:
            unit["paired_quality_review_status"] = "NOT_EVALUATED"
        validation_payloads[unit_id] = payload
        payload["structural_plan_check"] = structural_plan_check
        semantic_review_request = _build_structural_semantic_review_request(
            snapshot_id=str(snapshot["snapshot_id"]),
            unit_id=unit_id,
            unit=unit,
            chunk=chunks[unit_id],
            bundle=bundle,
            structural_plan_check=structural_plan_check,
            original=original,
            invariant_before=invariant_before,
            restored=restored,
            validation_payload=payload,
            suffix=suffix,
        )
        if semantic_review_request is not None:
            request_name = f"{unit_id}.structural-semantic-review-request.json"
            request_path = validation_dir / request_name
            _write_json(request_path, semantic_review_request)
            request_record = {
                "status": "PENDING_EXTERNAL_REVIEW",
                "path": str(Path("validation") / request_name).replace("\\", "/"),
                "request_sha256": semantic_review_request["request_sha256"],
            }
            structural_semantic_review_requests[unit_id] = request_record
            structural_plan_check["semantic_review"] = request_record
            structural_plan_check["semantic_review_status"] = (
                "PENDING_EXTERNAL_REVIEW"
            )
            unit["structural_semantic_review_status"] = (
                "PENDING_EXTERNAL_REVIEW"
            )
        elif (
            structural_plan_check.get("change_applied") is True
            or structural_plan_check.get("actual_content_changed") is True
        ):
            structural_plan_check["semantic_review_status"] = (
                "BLOCKED_BY_HARD_INVARIANT"
                if payload.get("hard_invariant_layer_status") != "PASS"
                else "NOT_ISSUED"
            )
            unit["structural_semantic_review_status"] = structural_plan_check[
                "semantic_review_status"
            ]
        else:
            structural_plan_check["semantic_review_status"] = "NOT_REQUIRED"
            unit["structural_semantic_review_status"] = "NOT_REQUIRED"
        structural_plan_payloads[unit_id] = structural_plan_check
        _write_json(
            validation_dir / f"{unit_id}.structural.json",
            structural_plan_check,
        )
        _write_json(validation_dir / f"{unit_id}.validation.json", payload)
        unit["style_validation"] = payload["mechanical_validation_status"]
        unit["protected_hashes_ok"] = "PASS" if not payload["invariants"]["hard_failure"] else "FAIL"
        if payload["mechanical_validation_status"] != "PASS":
            unit["status"] = "UNRESOLVED"
            unit["notes"] = (
                "validator:"
                + payload["mechanical_validation_status"]
                + ":"
                + ",".join(payload["review_reasons"])
            )
            continue
        if not _quality_review_only(payload):
            unit["status"] = "UNRESOLVED"
            unit["style_validation"] = "REVIEW"
            unit["notes"] = "paired quality request missing"
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
        accepted_masked_by_unit[unit_id] = masked_text
        unit["hash_after"] = sha256(restored.encode("utf-8"))
        unit["diff_path"] = str(Path("diffs") / diff_path.name)
        accepted_by_file.setdefault(unit["file_id"], []).append(
            (int(unit["start"]), int(unit["end"]), restored, unit_id)
        )
        invariant_baseline_by_file.setdefault(unit["file_id"], []).append(
            (int(unit["start"]), int(unit["end"]), invariant_before, unit_id)
        )

    file_level_coverage_gap = any(
        str(record.get("status", ""))
        in {
            "UNRESOLVED",
            "UNRESOLVED_INCLUDE",
            "SKIPPED_GARBLED",
            "CHANGED_AFTER_SNAPSHOT",
        }
        for record in file_manifest
    )
    for transaction_id, transaction in sorted(
        structural_transaction_results.items()
    ):
        if transaction.get("atomic_gate_status") != "PASS":
            continue
        participant_ids = set(transaction["unit_ids"])
        independent_coverage_gap = any(
            unit_id not in participant_ids
            and unit_map[unit_id].get("status") not in {
                "DONE",
                "NO_CHANGE",
                "SKIPPED_PROTECTED",
            }
            for unit_id in expected_voice_units
        )
        if not file_level_coverage_gap and not independent_coverage_gap:
            continue
        transaction.update(
            {
                "status": "REVIEW",
                "atomic_gate_status": "ROLLED_BACK",
                "change_applied": False,
                "rollback_reason": "INCOMPLETE_DOCUMENT_COVERAGE",
                "review_request": {},
                "errors": [
                    *transaction.get("errors", []),
                    "structural_transaction_review_only_publication_blocked",
                ],
            }
        )
        request_record = structural_transaction_review_requests.pop(
            transaction_id, None
        )
        if isinstance(request_record, dict):
            staged_request_path = validation_dir / Path(
                str(request_record.get("path", ""))
            ).name
            if staged_request_path.is_file():
                staged_request_path.unlink()
        for unit_id in transaction["unit_ids"]:
            structural_semantic_review_requests.pop(unit_id, None)
            _discard_paired_quality_review_request(
                paired_quality_review_requests, validation_dir, unit_id
            )
            accepted_masked_by_unit.pop(unit_id, None)
            unit = unit_map[unit_id]
            unit["status"] = "UNRESOLVED"
            unit["hash_after"] = ""
            unit["diff_path"] = ""
            unit["structural_plan_status"] = "REVIEW"
            unit["structural_semantic_review_status"] = "NOT_ISSUED"
            unit["transaction_status"] = "ROLLED_BACK"
            unit["notes"] = (
                "structural_transaction_rolled_back:INCOMPLETE_DOCUMENT_COVERAGE"
            )
            diff_path = diffs_dir / f"{unit_id}.diff"
            if diff_path.is_file():
                diff_path.unlink()
            plan_payload = structural_plan_payloads[unit_id]
            plan_payload.update(
                {
                    "status": "REVIEW",
                    "change_applied": False,
                    "transaction_atomic_gate_status": "ROLLED_BACK",
                    "semantic_review_status": "NOT_ISSUED",
                }
            )
            plan_payload.pop("semantic_review", None)
            _write_json(
                validation_dir / f"{unit_id}.structural.json", plan_payload
            )
        for file_id, changes in list(accepted_by_file.items()):
            remaining = [
                item for item in changes if item[3] not in participant_ids
            ]
            if remaining:
                accepted_by_file[file_id] = remaining
            else:
                accepted_by_file.pop(file_id, None)
        for file_id, changes in list(invariant_baseline_by_file.items()):
            remaining = [
                item for item in changes if item[3] not in participant_ids
            ]
            if remaining:
                invariant_baseline_by_file[file_id] = remaining
            else:
                invariant_baseline_by_file.pop(file_id, None)
        _write_json(
            validation_dir / f"{transaction_id}.transaction.json", transaction
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
                else accepted_masked_by_unit.get(unit_id)
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
    repetition_rolled_back_transactions = {
        unit_to_transaction[unit_id]
        for unit_id in blocked_by_repetition
        if unit_id in unit_to_transaction
    }
    for transaction_id in sorted(repetition_rolled_back_transactions):
        transaction = structural_transaction_results.get(transaction_id)
        if not isinstance(transaction, dict) or transaction.get(
            "atomic_gate_status"
        ) != "PASS":
            continue
        blocked_by_repetition.update(transaction["unit_ids"])
        transaction.update(
            {
                "status": "REVIEW",
                "atomic_gate_status": "ROLLED_BACK",
                "change_applied": False,
                "rollback_reason": "CROSS_UNIT_REPETITION",
                "review_request": {},
            }
        )
        transaction["errors"] = [
            *transaction.get("errors", []),
            "structural_transaction_cross_unit_repetition",
        ]
        request_record = structural_transaction_review_requests.pop(
            transaction_id, None
        )
        if isinstance(request_record, dict):
            request_path = run_dir / str(request_record.get("path", ""))
            staged_request_path = validation_dir / request_path.name
            if staged_request_path.is_file():
                staged_request_path.unlink()
        for member_id in transaction["unit_ids"]:
            structural_semantic_review_requests.pop(member_id, None)
            _discard_paired_quality_review_request(
                paired_quality_review_requests, validation_dir, member_id
            )
            plan_payload = structural_plan_payloads.get(member_id)
            if isinstance(plan_payload, dict):
                plan_payload.update(
                    {
                        "status": "REVIEW",
                        "change_applied": False,
                        "transaction_atomic_gate_status": "ROLLED_BACK",
                        "semantic_review_status": "NOT_ISSUED",
                    }
                )
                plan_payload.pop("semantic_review", None)
                _write_json(
                    validation_dir / f"{member_id}.structural.json",
                    plan_payload,
                )
        _write_json(
            validation_dir / f"{transaction_id}.transaction.json", transaction
        )
    if blocked_by_repetition:
        for unit_id in sorted(blocked_by_repetition):
            unit = unit_map[unit_id]
            if unit.get("status") not in {"DONE", "NO_CHANGE"}:
                continue
            unit["status"] = "UNRESOLVED"
            unit["hash_after"] = ""
            unit["diff_path"] = ""
            accepted_masked_by_unit.pop(unit_id, None)
            _discard_paired_quality_review_request(
                paired_quality_review_requests, validation_dir, unit_id
            )
            if unit_id in unit_to_transaction:
                unit["transaction_status"] = "ROLLED_BACK"
                unit["structural_plan_status"] = "REVIEW"
                unit["structural_semantic_review_status"] = "NOT_ISSUED"
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
        for file_id, changes in list(invariant_baseline_by_file.items()):
            remaining = [item for item in changes if item[3] not in blocked_by_repetition]
            if remaining:
                invariant_baseline_by_file[file_id] = remaining
            else:
                invariant_baseline_by_file.pop(file_id, None)

    rendered_texts: dict[str, str] = dict(file_texts)
    invariant_baseline_texts: dict[str, str] = dict(file_texts)
    for file_id, changes in accepted_by_file.items():
        text = rendered_texts[file_id]
        for start, end, replacement, _ in sorted(changes, key=lambda item: item[0], reverse=True):
            text = text[:start] + replacement + text[end:]
        rendered_texts[file_id] = text
    for file_id, changes in invariant_baseline_by_file.items():
        text = invariant_baseline_texts[file_id]
        for start, end, replacement, _ in sorted(
            changes, key=lambda item: item[0], reverse=True
        ):
            text = text[:start] + replacement + text[end:]
        invariant_baseline_texts[file_id] = text

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
            invariant_baseline_texts[file_id],
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
    second_pass_evidence: dict[str, Any] = {
        "status": "NOT_RUN",
        "receipt_sha256": "",
        "path": "",
        "units_total": 0,
        "evidence_cap": "E0",
        "filesystem_isolation_verified": False,
        "oracle_unreachable_verified": False,
    }
    review_only_transaction_present = any(
        result.get("atomic_gate_status") == "PASS"
        and result.get("change_applied") is True
        for result in structural_transaction_results.values()
    )
    # Every editable long-document unit requires a paired-quality request.
    # Missing request artifacts must block second-pass downgrade just as
    # pending requests do; otherwise a persistence failure could erase the
    # very gate that the receipt is forbidden to clear.
    review_only_quality_present = bool(expected_voice_units)
    if second_pass_receipt is not None and (
        review_only_transaction_present or review_only_quality_present
    ):
        second_pass_evidence = {
            "status": "FAIL",
            "receipt_sha256": "",
            "path": str(second_pass_receipt.resolve(strict=False)),
            "units_total": 0,
            "evidence_cap": "E0",
            "filesystem_isolation_verified": False,
            "oracle_unreachable_verified": False,
            "error": (
                "second_pass_receipt_not_allowed_for_review_candidate:"
                + (
                    "STRUCTURAL_TRANSACTION"
                    if review_only_transaction_present
                    else "PAIRED_QUALITY"
                )
            ),
        }
    elif second_pass_receipt is not None:
        try:
            second_pass_evidence = _validate_second_pass_receipt(
                second_pass_receipt.resolve(strict=True),
                snapshot_id=str(snapshot["snapshot_id"]),
                rendered_root=staging_dir,
                rendered_manifest_path=run_dir / "rendered_manifest.csv",
                voice_binding_sha256=str(voice_identity["identity_sha256"]),
                scene=str(run_metadata.get("scene", "")),
            )
        except (OSError, UnicodeError, ValueError, json.JSONDecodeError) as error:
            second_pass_evidence = {
                "status": "FAIL",
                "receipt_sha256": "",
                "path": str(second_pass_receipt.resolve(strict=False)),
                "units_total": 0,
                "evidence_cap": "E0",
                "filesystem_isolation_verified": False,
                "oracle_unreachable_verified": False,
                "error": str(error),
            }
    processable_editable_units = initial_processable_editable_units
    empty_processable_scope = not file_manifest or not units or processable_editable_units == 0
    unresolved = unresolved_units + unresolved_files + len(source_changes) + (1 if empty_processable_scope else 0)

    run_intensity = str(run_metadata.get("intensity", "")).upper()
    if run_intensity != "STRUCTURAL":
        structural_plan_status = "NOT_APPLICABLE"
    elif not expected_voice_units:
        structural_plan_status = "NOT_EVALUATED"
    elif all(
        str(unit_map[unit_id].get("structural_plan_status", "")) == "PASS"
        for unit_id in expected_voice_units
    ):
        structural_plan_status = "PASS"
    else:
        structural_plan_status = "REVIEW"
    structural_changes_applied = sum(
        1
        for payload in structural_plan_payloads.values()
        if payload.get("status") == "PASS"
        and (
            payload.get("change_applied") is True
            or payload.get("actual_content_changed") is True
        )
    )
    if structural_plan_status == "NOT_APPLICABLE":
        structural_semantic_mapping = "NOT_APPLICABLE"
    elif structural_plan_status != "PASS":
        structural_semantic_mapping = "NOT_EVALUATED"
    elif structural_changes_applied:
        structural_semantic_mapping = "NOT_EVALUATED"
    else:
        structural_semantic_mapping = "PASS"
    if run_intensity != "STRUCTURAL":
        structural_semantic_review_status = "NOT_APPLICABLE"
    elif not structural_changes_applied:
        structural_semantic_review_status = (
            "NOT_REQUIRED"
            if structural_plan_status == "PASS"
            else "NOT_EVALUATED"
        )
    elif len(structural_semantic_review_requests) == structural_changes_applied:
        structural_semantic_review_status = "PENDING_EXTERNAL_REVIEW"
    else:
        structural_semantic_review_status = "BLOCKED"

    paired_quality_units = {
        str(unit["unit_id"])
        for unit in units
        if str(unit.get("unit_id", "")) in expected_voice_units
        and str(unit.get("status", "")) in {"DONE", "NO_CHANGE"}
    }
    paired_quality_pending_units = {
        unit_id
        for unit_id in paired_quality_units
        if str(paired_quality_review_requests.get(unit_id, {}).get("status", ""))
        == "PENDING_EXTERNAL_REVIEW"
    }
    paired_quality_missing_units = paired_quality_units - set(
        paired_quality_review_requests
    )
    if not expected_voice_units:
        paired_quality_review_request_coverage_status = "NOT_APPLICABLE"
        paired_quality_gate_status = "NOT_APPLICABLE"
    elif paired_quality_missing_units or paired_quality_units != expected_voice_units:
        paired_quality_review_request_coverage_status = "REVIEW"
        paired_quality_gate_status = "BLOCKED"
    elif paired_quality_pending_units == expected_voice_units:
        paired_quality_review_request_coverage_status = "PASS"
        paired_quality_gate_status = "PENDING_EXTERNAL_REVIEW"
    else:
        paired_quality_review_request_coverage_status = "REVIEW"
        paired_quality_gate_status = "BLOCKED"
    paired_quality_clearance_granted = False

    hard_failure = (
        bool(full_format_errors)
        or compile_result["status"] == "FAIL"
        or compile_or_concurrent_source_change
        or second_pass_evidence["status"] == "FAIL"
    )
    discard_staged_evidence = bool(
        compile_result.get("integrity_changes", {}).get("evidence_staging")
    )
    current_accepted_units = {
        unit["unit_id"] for unit in units if unit["status"] in {"DONE", "NO_CHANGE"}
    }
    partial_regression_units = sorted(previous_accepted_units - current_accepted_units)
    partial_regression = (existing_partial_before or existing_review_before) and (
        previous_partial_state_missing or bool(partial_regression_units)
    )
    if partial_regression:
        hard_failure = True
    complete = pending == 0 and not empty_processable_scope
    if hard_failure:
        candidate_assembly_status, candidate_assembly_exit_code = "FAIL", 1
    elif pending or unresolved or structural_transaction_candidates_pending:
        candidate_assembly_status, candidate_assembly_exit_code = "REVIEW", 2
    else:
        candidate_assembly_status, candidate_assembly_exit_code = "PASS", 0
    structural_semantic_review_blocks_delivery = bool(
        candidate_assembly_status == "PASS"
        and structural_changes_applied
        and structural_semantic_mapping == "NOT_EVALUATED"
    )
    paired_quality_review_blocks_delivery = bool(
        candidate_assembly_status == "PASS"
        and paired_quality_gate_status
        in {"PENDING_EXTERNAL_REVIEW", "BLOCKED"}
    )
    review_candidate_blocks_delivery = bool(
        structural_semantic_review_blocks_delivery
        or paired_quality_review_blocks_delivery
    )
    if review_candidate_blocks_delivery:
        status, exit_code = "REVIEW", 2
    else:
        status, exit_code = candidate_assembly_status, candidate_assembly_exit_code
    delivery_gate_status = status
    if candidate_assembly_status == "PASS":
        publish_name = (
            "rendered_review"
            if review_candidate_blocks_delivery
            else "rendered"
        )
    else:
        publish_name = "rendered_partial"
    publish_dir = run_dir / publish_name
    published_namespace_conflict = bool(
        (publish_name == "rendered_review" and existing_rendered_before)
        or (publish_name == "rendered" and existing_review_before)
    )
    if published_namespace_conflict:
        hard_failure = True
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
        preserve_published_evidence = (
            existing_rendered_before
            or existing_partial_before
            or existing_review_before
        )
    elif publish_dir.exists():
        if _directory_hashes(publish_dir) == _directory_hashes(staging_dir):
            idempotency = "PASS"
            shutil.rmtree(staging_dir)
            published_path = str(publish_dir)
        elif publish_name in {"rendered_partial", "rendered_review"}:
            history_path = run_dir / "partial_history.jsonl"
            history = {
                "replaced_at": utc_now(),
                "old_hashes": _directory_hashes(publish_dir),
                "new_hashes": _directory_hashes(staging_dir),
                "reason": (
                    "revised_review_candidate"
                    if publish_name == "rendered_review"
                    else "additional_or_revised_unit_bundles"
                ),
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
    if (
        not hard_failure
        and publish_name in {"rendered", "rendered_review"}
        and stale_partial.exists()
    ):
        history_path = run_dir / "partial_history.jsonl"
        history = {
            "replaced_at": utc_now(),
            "old_hashes": _directory_hashes(stale_partial),
            "new_hashes": _directory_hashes(publish_dir),
            "reason": (
                "full_review_candidate_published"
                if publish_name == "rendered_review"
                else "full_terminal_coverage_published"
            ),
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
        "atomic_transactions": {
            transaction_id: {
                "unit_ids": list(result["unit_ids"]),
                "atomic_gate_status": result["atomic_gate_status"],
                "failure_gate": result["rollback_reason"],
                "accepted_member_count": sum(
                    1
                    for unit_id in result["unit_ids"]
                    if unit_map[unit_id].get("status") == "DONE"
                ),
                "published_member_count": (
                    sum(
                        1
                        for unit_id in result["unit_ids"]
                        if unit_map[unit_id].get("status") == "DONE"
                    )
                    if published_path and not hard_failure
                    else 0
                ),
            }
            for transaction_id, result in sorted(
                structural_transaction_results.items()
            )
        },
    }
    if not preserve_published_evidence and not discard_staged_evidence:
        _write_json(run_dir / "rollback_manifest.json", rollback)

    # Publication can still discover a non-idempotent candidate and upgrade the
    # assembly result to FAIL, so finalize the public statuses only afterwards.
    if hard_failure:
        candidate_assembly_status, candidate_assembly_exit_code = "FAIL", 1
    elif pending or unresolved or structural_transaction_candidates_pending:
        candidate_assembly_status, candidate_assembly_exit_code = "REVIEW", 2
    else:
        candidate_assembly_status, candidate_assembly_exit_code = "PASS", 0
    structural_semantic_review_blocks_delivery = bool(
        candidate_assembly_status == "PASS"
        and structural_changes_applied
        and structural_semantic_mapping == "NOT_EVALUATED"
    )
    paired_quality_review_blocks_delivery = bool(
        candidate_assembly_status == "PASS"
        and paired_quality_gate_status
        in {"PENDING_EXTERNAL_REVIEW", "BLOCKED"}
    )
    review_candidate_blocks_delivery = bool(
        structural_semantic_review_blocks_delivery
        or paired_quality_review_blocks_delivery
    )
    if review_candidate_blocks_delivery:
        status, exit_code = "REVIEW", 2
    else:
        status, exit_code = candidate_assembly_status, candidate_assembly_exit_code
    delivery_gate_status = status

    coverage_completion_claim_allowed = bool(
        complete
        and unresolved == 0
        and not hard_failure
        and structural_transaction_candidate_coverage_status
        in {"PASS", "NOT_APPLICABLE"}
    )
    routed_units = [unit for unit in units if int(unit.get("author_chars", 0)) > 0]
    if not routed_units:
        scene_routing_status = "NOT_EVALUATED"
    elif (
        run_metadata.get("scene_routing_status") == "PASS"
        and all(
            str(unit.get("scene", "")).upper()
            in {"GENERAL", "COURSE", "MODELING", "RESEARCH"}
            and str(unit.get("scene_routing_decision", ""))
            in {"EXPLICIT", "ROUTED", "ROUTED_DOCUMENT_PRIOR", "FALLBACK_GENERAL"}
            and unit.get("scene_routing_policy_sha256")
            == run_metadata.get("scene_routing_policy_sha256")
            for unit in routed_units
        )
    ):
        scene_routing_status = "PASS"
    else:
        scene_routing_status = "REVIEW"
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
                else accepted_masked_by_unit.get(unit_id)
                if unit.get("status") == "DONE"
                else None
            ),
        }
        for unit in units
        for unit_id in [str(unit["unit_id"])]
        if unit_id in expected_voice_units
    ]
    voice_conformance = _audit_voice_conformance_set(
        frozen_voice_profiles,
        style_records,
        scene_routing_status=scene_routing_status,
    )
    voice_conformance_status = str(voice_conformance["status"])
    cross_unit_repetition_status = str(cross_unit_repetition["status"])
    humanize_second_pass_convergence = str(second_pass_evidence["status"])
    second_pass_stability_status = {
        "PASS": "CONVERGENCE_OBSERVED",
        "REVIEW": "DISAGREEMENT_OR_INCOMPLETE",
        "FAIL": "INVALID_EVIDENCE",
        "NOT_RUN": "NOT_RUN",
    }.get(humanize_second_pass_convergence, "NOT_EVALUATED")
    voice_completion_claim_allowed = bool(
        coverage_completion_claim_allowed
        and scene_routing_status == "PASS"
        and voice_binding_status == "PASS"
        and rewrite_binding_status == "PASS"
        and voice_conformance_status == "PASS"
        and structural_plan_status in {"PASS", "NOT_APPLICABLE"}
        and structural_semantic_mapping in {"PASS", "NOT_APPLICABLE"}
    )
    humanize_completion_claim_allowed = bool(
        voice_completion_claim_allowed
        and cross_unit_repetition_status == "PASS"
        and humanize_second_pass_convergence == "PASS"
        and paired_quality_clearance_granted
    )
    metadata = {
        "tool": "finalize_humanize_long_document.py",
        "created_at": utc_now(),
        "snapshot_id": snapshot["snapshot_id"],
        "status": status,
        "exit_code": exit_code,
        "candidate_assembly_status": candidate_assembly_status,
        "candidate_assembly_exit_code": candidate_assembly_exit_code,
        "delivery_gate_status": delivery_gate_status,
        "publish_state": (
            "FAILED"
            if candidate_assembly_status == "FAIL"
            else "PARTIAL"
            if candidate_assembly_status == "REVIEW"
            else "REVIEW_CANDIDATE"
            if review_candidate_blocks_delivery
            else "FINAL"
        ),
        "units_total": len(units),
        "processable_editable_units": processable_editable_units,
        "unit_statuses": dict(sorted(statuses.items())),
        "unit_status_scope": "CANDIDATE_ASSEMBLY_NOT_DELIVERY",
        "file_statuses": dict(sorted(file_statuses.items())),
        "rewrites_submitted": len(rewrites) + sum(
            len(result["unit_ids"])
            for result in structural_transaction_results.values()
        ),
        "validation_results": {
            key: value["status"] for key, value in sorted(validation_payloads.items())
        },
        "mechanical_validation_results": {
            key: value.get("mechanical_validation_status", "NOT_RUN")
            for key, value in sorted(validation_payloads.items())
        },
        "full_format_errors": full_format_errors,
        "compile_check": compile_result,
        "published_path": published_path,
        "idempotency": idempotency,
        "assembly_replay_idempotency": idempotency,
        "humanize_second_pass_convergence": humanize_second_pass_convergence,
        "second_pass_stability_status": second_pass_stability_status,
        "second_pass_quality_clearance_granted": False,
        "humanize_second_pass_evidence": second_pass_evidence,
        "processable_scope_complete": complete,
        "empty_processable_scope": empty_processable_scope,
        "coverage_completion_claim_allowed": coverage_completion_claim_allowed,
        "paired_quality_review_request_coverage_status": (
            paired_quality_review_request_coverage_status
        ),
        "paired_quality_gate_status": paired_quality_gate_status,
        "paired_quality_review_requests": dict(
            sorted(paired_quality_review_requests.items())
        ),
        "paired_quality_units_total": len(paired_quality_units),
        "paired_quality_units_pending": len(paired_quality_pending_units),
        "paired_quality_units_missing": len(paired_quality_missing_units),
        "paired_quality_clearance_granted": paired_quality_clearance_granted,
        "paired_quality_local_clearance_supported": False,
        "paired_quality_limitations": (
            "request binding and coverage are deterministic; naturalness, independent "
            "benefit, collocation, hierarchy, and author-voice improvement remain "
            "PENDING_EXTERNAL_REVIEW"
        ),
        "scene_routing_status": scene_routing_status,
        "intensity": run_intensity,
        "scene_routing_policy_sha256": run_metadata.get("scene_routing_policy_sha256", ""),
        "voice_binding_sha256": voice_identity["identity_sha256"],
        "voice_profile_sha256": voice_identity["voice_profile_sha256"],
        "voice_profile_set_sha256": voice_identity["profile_set_sha256"],
        "voice_profile_manifest_sha256": voice_identity["voice_profile_manifest_sha256"],
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
        "voice_default_disclosure_required": bool(voice_identity["voice_default_disclosure"]),
        "voice_binding_status": voice_binding_status,
        "rewrite_binding_status": rewrite_binding_status,
        "rewrite_bindings_total": len(expected_voice_units),
        "rewrite_bindings_matched": len(chunk_binding_matched_units),
        "rewrite_bindings_missing": len(chunk_binding_missing_units),
        "rewrite_bindings_mismatched": len(chunk_binding_mismatched_units),
        "structural_plan_status": structural_plan_status,
        "structural_plan_results": {
            key: value.get("status", "NOT_RUN")
            for key, value in sorted(structural_plan_payloads.items())
        },
        "structural_changes_applied": structural_changes_applied,
        "structural_semantic_mapping": structural_semantic_mapping,
        "structural_semantic_review_status": structural_semantic_review_status,
        "structural_semantic_review_requests": dict(
            sorted(structural_semantic_review_requests.items())
        ),
        "structural_transactions_total": len(structural_transaction_results),
        "structural_transaction_declines_total": len(
            bound_transaction_declines
        ),
        "structural_transaction_decline_results": dict(
            sorted(bound_transaction_declines.items())
        ),
        "structural_transaction_candidate_dispositions": dict(
            sorted(structural_transaction_candidate_dispositions.items())
        ),
        "structural_transaction_candidates_total": (
            structural_transaction_candidates_total
        ),
        "structural_transaction_candidates_executed": (
            structural_transaction_candidates_executed
        ),
        "structural_transaction_candidates_declined": (
            structural_transaction_candidates_declined
        ),
        "structural_transaction_candidates_pending": (
            structural_transaction_candidates_pending
        ),
        "structural_transaction_candidate_coverage_status": (
            structural_transaction_candidate_coverage_status
        ),
        "structural_transaction_scope_complete": (
            structural_transaction_scope_complete
        ),
        "structural_transaction_results": dict(
            sorted(structural_transaction_results.items())
        ),
        "structural_transaction_review_requests": dict(
            sorted(structural_transaction_review_requests.items())
        ),
        "structural_transaction_rolled_back_ids": sorted(
            transaction_id
            for transaction_id, result in structural_transaction_results.items()
            if result.get("atomic_gate_status") == "ROLLED_BACK"
        ),
        "structural_semantic_review_local_clearance_supported": False,
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
        "published_namespace_conflict": published_namespace_conflict,
    }
    _write_json(run_dir / "finalization_metadata.json", metadata)
    return metadata


def finalize(
    run_dir: Path,
    rewrites_dir: Path,
    *,
    check_command: str | None = None,
    second_pass_receipt: Path | None = None,
) -> dict[str, Any]:
    run_dir = Path(run_dir)
    rewrites_dir = Path(rewrites_dir)
    with _run_lock(run_dir):
        with tempfile.TemporaryDirectory(
            prefix="humanize-finalize-transaction-"
        ) as temporary:
            backup_dir = Path(temporary) / "run-state"
            _copy_run_state(run_dir, backup_dir)
            previous_finalization_metadata = (
                backup_dir / "finalization_metadata.json"
            ).is_file()
            previous_published_evidence = _published_evidence_exists(backup_dir)
            try:
                metadata = _finalize_locked(
                    run_dir,
                    rewrites_dir,
                    check_command=check_command,
                    second_pass_receipt=second_pass_receipt,
                )
            except Exception as error:
                _restore_run_state(run_dir, backup_dir)
                failure = _runtime_failure_metadata(
                    error,
                    run_dir=run_dir,
                    run_state_restored=True,
                    finalization_metadata_preserved=(
                        previous_finalization_metadata
                    ),
                    published_evidence_preserved=previous_published_evidence,
                )
                try:
                    _write_json(
                        run_dir / "last_failed_attempt_metadata.json", failure
                    )
                except Exception:
                    # State restoration has priority over diagnostic persistence;
                    # preserve the original runtime exception for the caller.
                    pass
                raise

            restore_previous_state = bool(
                metadata.get("published_evidence_preserved")
                or metadata.get("run_artifacts_changed_during_check")
            )
            if restore_previous_state:
                _restore_run_state(run_dir, backup_dir)
                metadata = _failed_attempt_record(
                    metadata,
                    run_dir=run_dir,
                    finalization_metadata_preserved=(
                        previous_finalization_metadata
                    ),
                    published_evidence_preserved=previous_published_evidence,
                )
                _write_json(
                    run_dir / "last_failed_attempt_metadata.json", metadata
                )
                return metadata

            metadata.update(
                {
                    "failed_attempt": False,
                    "run_state_restored_after_failure": False,
                    "finalization_metadata_preserved": False,
                    "failed_attempt_metadata_path": "",
                }
            )
            _write_json(run_dir / "finalization_metadata.json", metadata)
            return metadata


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="验证长文单元改写、恢复保护区、生成逐节 diff 与派生稿；从不覆盖源文件。"
    )
    parser.add_argument("--run-dir", type=Path, required=True, help="prepare 命令的输出目录")
    parser.add_argument(
        "--rewrites",
        type=Path,
        required=True,
        help="按 unit_id 命名的 .json/.txt，或绑定 STX inventory 的 transaction bundle 目录",
    )
    parser.add_argument("--check-command", help="可选项目编译/格式命令，在 staging 根目录执行")
    parser.add_argument(
        "--second-pass-receipt",
        type=Path,
        help="控制面 verifier 产生的当前 rendered 绑定 receipt",
    )
    parser.add_argument(
        "--format",
        choices=("json", "text"),
        default="json",
        help="stdout 格式；text 只显示权威交付状态和关键未决项",
    )
    return parser


def _render_text_summary(metadata: dict[str, Any]) -> str:
    delivery = metadata.get("delivery_gate_status", metadata.get("status", "UNKNOWN"))
    exit_code = metadata.get("exit_code", 1)
    publish_state = metadata.get("publish_state", "UNKNOWN")
    lines = [
        f"DELIVERY {delivery} exit={exit_code} publish={publish_state}",
        "status_authority=delivery_gate_status+process_exit_code",
    ]
    if metadata.get("runtime_error"):
        lines.append(
            f"runtime_error={metadata.get('error_type', 'ERROR')}: {metadata.get('error', '')}"
        )
        return "\n".join(lines)
    lines.append(
        "candidate_assembly="
        + str(metadata.get("candidate_assembly_status", "NOT_RUN"))
        + "; paired_quality="
        + str(metadata.get("paired_quality_gate_status", "NOT_EVALUATED"))
    )
    statuses = metadata.get("unit_statuses", {})
    if isinstance(statuses, dict):
        rendered_statuses = ",".join(
            f"{key}={value}" for key, value in sorted(statuses.items())
        )
        lines.append(
            f"units[{rendered_statuses}]; scope=CANDIDATE_ASSEMBLY_NOT_DELIVERY"
        )
    published_path = str(metadata.get("published_path", ""))
    if published_path:
        label = "review_candidate" if publish_state == "REVIEW_CANDIDATE" else "published"
        lines.append(f"{label}={published_path}")
    compile_check = metadata.get("compile_check", {})
    if isinstance(compile_check, dict):
        lines.append(f"compile_check={compile_check.get('status', 'NOT_RUN')}")
    lines.append(
        "humanize_completion_claim_allowed="
        + str(bool(metadata.get("humanize_completion_claim_allowed"))).lower()
    )
    return "\n".join(lines)


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
            second_pass_receipt=args.second_pass_receipt,
        )
    except Exception as error:
        run_dir = args.run_dir.resolve(strict=False)
        failed_attempt_path = run_dir / "last_failed_attempt_metadata.json"
        metadata: dict[str, Any] | None = None
        if failed_attempt_path.is_file():
            try:
                candidate = _load_json(failed_attempt_path)
                if (
                    isinstance(candidate, dict)
                    and candidate.get("schema_version")
                    == FAILED_ATTEMPT_METADATA_SCHEMA
                    and candidate.get("error_type") == type(error).__name__
                    and candidate.get("error") == str(error)
                ):
                    metadata = candidate
            except Exception:
                metadata = None
        if metadata is None:
            metadata = _runtime_failure_metadata(
                error,
                run_dir=run_dir,
                run_state_restored=False,
                finalization_metadata_preserved=False,
                published_evidence_preserved=False,
            )
        if args.format == "text":
            print(_render_text_summary(metadata))
        else:
            print(json.dumps(metadata, ensure_ascii=False, indent=2, sort_keys=True))
        return 1
    if args.format == "text":
        print(_render_text_summary(metadata))
    else:
        print(json.dumps(metadata, ensure_ascii=False, indent=2, sort_keys=True))
    return int(metadata["exit_code"])


if __name__ == "__main__":
    raise SystemExit(main())
