#!/usr/bin/env python3
"""Verify a published short PATCH directory as a closed self-consistency record."""

from __future__ import annotations

import argparse
import json
import os
import re
import stat
import sys
import tempfile
from pathlib import Path
from typing import Any, Mapping, Sequence


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import apply_humanize_short_patch as applicator  # noqa: E402
import build_humanize_short_patch as short_patch  # noqa: E402
import validate_humanize_output as unified_validator  # noqa: E402


ShortPatchError = short_patch.ShortPatchError
VERIFICATION_SCHEMA = "humanize-short-patch-verification/v2"
MANIFEST_FIELDS = {"schema_version", "integrity_scope", "artifacts", "manifest_sha256"}
ARTIFACT_FIELDS = {"path", "size", "sha256"}
FIXED_ARTIFACTS = {
    "source.snapshot.bin",
    "patch.diff",
    "patch.bundle.json",
    "validation.json",
    "result.json",
}
ALLOWED_CANDIDATE_NAMES = {
    "candidate.review.md",
    "candidate.review.tex",
    "candidate.review.txt",
}
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


class _StrictArgumentParser(argparse.ArgumentParser):
    def error(self, _message: str) -> None:
        raise ShortPatchError("INVALID_ARGUMENTS")


def _exact_fields(value: Mapping[str, Any], expected: set[str], label: str) -> None:
    actual = set(value)
    if actual != expected:
        raise ShortPatchError(
            f"{label} fields drifted; missing={sorted(expected - actual)}, "
            f"unknown={sorted(actual - expected)}"
        )


def _root(path: Path) -> Path:
    root = Path(os.path.abspath(os.fspath(path)))
    short_patch._assert_no_reparse_chain(root, "evidence directory")
    try:
        metadata = os.stat(root, follow_symlinks=False)
    except OSError as error:
        raise ShortPatchError("evidence directory is missing") from error
    if not stat.S_ISDIR(metadata.st_mode):
        raise ShortPatchError("evidence directory must be a regular directory")
    return root


def _manifest_hash(payload: Mapping[str, Any]) -> str:
    unsigned = dict(payload)
    unsigned.pop("manifest_sha256", None)
    return short_patch.sha256(short_patch.canonical_json(unsigned))


def _load_json(path: Path, label: str) -> tuple[dict[str, Any], bytes]:
    raw = short_patch._regular_input(path, label, short_patch.MAX_JSON_BYTES)
    payload = short_patch.strict_json_bytes(raw, label)
    if not isinstance(payload, dict):
        raise ShortPatchError(f"{label} must be an object")
    return payload, raw


def _current_policy_hashes() -> dict[str, str]:
    return unified_validator._policy_hashes()


def _recorded_policy_hashes(validation: Mapping[str, Any]) -> dict[str, str]:
    evidence = validation.get("evidence")
    if not isinstance(evidence, dict):
        raise ShortPatchError("validation evidence is missing")
    policy = evidence.get("policy_hashes")
    if not isinstance(policy, dict) or not policy:
        raise ShortPatchError("validation policy_hashes are missing")
    for key, value in policy.items():
        if (
            not isinstance(key, str)
            or not key
            or not isinstance(value, str)
            or not SHA256_RE.fullmatch(value)
        ):
            raise ShortPatchError("validation policy_hashes are invalid")
    return dict(policy)


def _replay_validation(
    source: bytes,
    candidate: bytes,
    candidate_name: str,
    bundle: dict[str, Any],
) -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="humanize-short-patch-replay-") as temp:
        root = Path(temp)
        source_path = root / "source.snapshot.bin"
        candidate_path = root / candidate_name
        source_path.write_bytes(source)
        candidate_path.write_bytes(candidate)
        replayed, _raw = applicator._run_validator(source_path, candidate_path, bundle)
    return replayed


def _live_source_status(path: Path | None, expected_sha256: str) -> dict[str, Any]:
    if path is None:
        return {"status": "NOT_PROVIDED", "expected_sha256": expected_sha256}
    try:
        observed = short_patch.read_source(path)
    except (OSError, ShortPatchError):
        return {"status": "UNAVAILABLE", "expected_sha256": expected_sha256}
    observed_sha256 = short_patch.sha256(observed)
    return {
        "status": "MATCH" if observed_sha256 == expected_sha256 else "NOT_CURRENT",
        "expected_sha256": expected_sha256,
        "observed_sha256": observed_sha256,
    }


def _review_result(
    base: dict[str, Any],
    *,
    policy_status: str,
    replay_status: str,
    live_status: dict[str, Any],
    reasons: list[str],
) -> dict[str, Any]:
    return {
        **base,
        "status": "REVIEW",
        "exit_code": 2,
        "current_policy_status": policy_status,
        "current_policy_replay_status": replay_status,
        "live_source_status": live_status,
        "review_reasons": reasons,
    }


def verify_directory(
    path: Path,
    *,
    live_source: Path | None = None,
) -> dict[str, Any]:
    root = _root(path)
    manifest, _manifest_raw = _load_json(
        root / "evidence-manifest.json", "evidence manifest"
    )
    _exact_fields(manifest, MANIFEST_FIELDS, "evidence manifest")
    if manifest.get("schema_version") != applicator.EVIDENCE_MANIFEST_SCHEMA:
        raise ShortPatchError("evidence manifest schema_version is invalid")
    if manifest.get("integrity_scope") != "SELF_CONSISTENCY_ONLY":
        raise ShortPatchError("evidence manifest integrity_scope is invalid")
    if manifest.get("manifest_sha256") != _manifest_hash(manifest):
        raise ShortPatchError("evidence manifest_sha256 mismatch")
    entries = manifest.get("artifacts")
    if not isinstance(entries, list) or not entries:
        raise ShortPatchError("evidence manifest artifacts must be non-empty")
    records: dict[str, dict[str, Any]] = {}
    candidate_names: list[str] = []
    for index, entry in enumerate(entries):
        label = f"evidence manifest.artifacts[{index}]"
        if not isinstance(entry, dict):
            raise ShortPatchError(f"{label} must be an object")
        _exact_fields(entry, ARTIFACT_FIELDS, label)
        name = entry.get("path")
        if not isinstance(name, str) or not name or name in records:
            raise ShortPatchError(f"{label}.path is invalid or duplicate")
        if Path(name).name != name or "/" in name or "\\" in name:
            raise ShortPatchError(f"{label}.path must be a basename")
        if name in ALLOWED_CANDIDATE_NAMES:
            candidate_names.append(name)
        elif name not in FIXED_ARTIFACTS:
            raise ShortPatchError(f"{label}.path is not an allowed artifact")
        size = entry.get("size")
        digest = entry.get("sha256")
        if isinstance(size, bool) or not isinstance(size, int) or size < 0:
            raise ShortPatchError(f"{label}.size is invalid")
        if not isinstance(digest, str) or not SHA256_RE.fullmatch(digest):
            raise ShortPatchError(f"{label}.sha256 is invalid")
        records[name] = entry
    if set(records) != FIXED_ARTIFACTS | set(candidate_names) or len(candidate_names) != 1:
        raise ShortPatchError("evidence manifest artifact roles are incomplete")
    actual = {
        child.name
        for child in root.iterdir()
        if child.is_file() or child.is_symlink()
    }
    expected = {*records, "evidence-manifest.json"}
    if actual != expected or any(child.is_dir() for child in root.iterdir()):
        raise ShortPatchError("evidence directory is not a closed file set")
    artifact_bytes: dict[str, bytes] = {}
    for name, record in records.items():
        raw = short_patch._regular_input(root / name, f"artifact {name}")
        if len(raw) != record["size"]:
            raise ShortPatchError(f"artifact_size mismatch: {name}")
        if short_patch.sha256(raw) != record["sha256"]:
            raise ShortPatchError(f"artifact_sha256 mismatch: {name}")
        artifact_bytes[name] = raw

    source = short_patch.read_source(root / "source.snapshot.bin")
    bundle, bundle_raw = short_patch.load_bundle(root / "patch.bundle.json", source)
    candidate_name = candidate_names[0]
    candidate = artifact_bytes[candidate_name]
    if applicator._apply_bytes(source, bundle) != candidate:
        raise ShortPatchError("candidate is not the deterministic bundle application")
    if applicator._diff(source, candidate) != artifact_bytes["patch.diff"]:
        raise ShortPatchError("patch.diff does not match source and candidate")
    if bundle_raw != artifact_bytes["patch.bundle.json"]:
        raise ShortPatchError("bundle bytes changed during verification")

    validation = short_patch.strict_json_bytes(
        artifact_bytes["validation.json"], "validation artifact"
    )
    result = short_patch.strict_json_bytes(artifact_bytes["result.json"], "result artifact")
    if not isinstance(validation, dict) or not isinstance(result, dict):
        raise ShortPatchError("validation and result artifacts must be objects")
    evidence = validation.get("evidence")
    if not isinstance(evidence, dict):
        raise ShortPatchError("validation evidence is missing")
    if evidence.get("before_sha256") != short_patch.sha256(source):
        raise ShortPatchError("validation before_sha256 mismatch")
    if evidence.get("after_sha256") != short_patch.sha256(candidate):
        raise ShortPatchError("validation after_sha256 mismatch")
    required_result = {
        "schema_version": applicator.RESULT_SCHEMA,
        "status": "REVIEW",
        "delivery_gate_status": "REVIEW",
        "exit_code": 2,
        "source_sha256": short_patch.sha256(source),
        "candidate_sha256": short_patch.sha256(candidate),
        "bundle_sha256": bundle["bundle_sha256"],
        "candidate_path": candidate_name,
        "diff_path": "patch.diff",
        "bundle_path": "patch.bundle.json",
        "validation_path": "validation.json",
        "source_snapshot_path": "source.snapshot.bin",
        "evidence_manifest_path": "evidence-manifest.json",
        "humanize_quality_claim_allowed": False,
        "completion_claim_allowed": False,
    }
    for key, expected_value in required_result.items():
        if result.get(key) != expected_value:
            raise ShortPatchError(f"result field mismatch: {key}")
    if set(result.get("artifacts_written", [])) != expected:
        raise ShortPatchError("result artifacts_written does not match the closed file set")
    if result.get("validator_exit_code") != validation.get("exit_code"):
        raise ShortPatchError("result validator_exit_code mismatch")
    if result.get("validator_delivery_gate_status") != validation.get("delivery_gate_status"):
        raise ShortPatchError("result validator_delivery_gate_status mismatch")
    if result.get("unified_validator_status") != validation.get("mechanical_validation_status"):
        raise ShortPatchError("result unified_validator_status mismatch")
    expected_source_sha256 = short_patch.sha256(source)
    live_status = _live_source_status(live_source, expected_source_sha256)
    base = {
        "schema_version": VERIFICATION_SCHEMA,
        "record_integrity_status": "PASS",
        "integrity_scope": "SELF_CONSISTENCY_ONLY",
        "manifest_sha256": manifest["manifest_sha256"],
        "source_sha256": expected_source_sha256,
        "candidate_sha256": short_patch.sha256(candidate),
        "delivery_gate_status": "REVIEW",
        "delivery_gate_exit_code": 2,
        "humanize_quality_claim_allowed": False,
        "completion_claim_allowed": False,
        "academic_correctness": "NOT_EVALUATED",
    }
    recorded_policy = _recorded_policy_hashes(validation)
    try:
        current_policy = _current_policy_hashes()
    except (OSError, ValueError):
        reasons = ["CURRENT_POLICY_UNAVAILABLE"]
        if live_status["status"] != "MATCH" and live_status["status"] != "NOT_PROVIDED":
            reasons.append(
                "LIVE_SOURCE_NOT_CURRENT"
                if live_status["status"] == "NOT_CURRENT"
                else "LIVE_SOURCE_UNAVAILABLE"
            )
        return _review_result(
            base,
            policy_status="UNAVAILABLE",
            replay_status="NOT_RUN",
            live_status=live_status,
            reasons=reasons,
        )
    if recorded_policy != current_policy:
        reasons = ["POLICY_DRIFT"]
        if live_status["status"] == "NOT_CURRENT":
            reasons.append("LIVE_SOURCE_NOT_CURRENT")
        elif live_status["status"] == "UNAVAILABLE":
            reasons.append("LIVE_SOURCE_UNAVAILABLE")
        return _review_result(
            base,
            policy_status="DRIFT",
            replay_status="NOT_RUN",
            live_status=live_status,
            reasons=reasons,
        )
    try:
        replayed = _replay_validation(source, candidate, candidate_name, bundle)
    except OSError:
        reasons = ["CURRENT_POLICY_REPLAY_UNAVAILABLE"]
        if live_status["status"] == "NOT_CURRENT":
            reasons.append("LIVE_SOURCE_NOT_CURRENT")
        elif live_status["status"] == "UNAVAILABLE":
            reasons.append("LIVE_SOURCE_UNAVAILABLE")
        return _review_result(
            base,
            policy_status="MATCH",
            replay_status="NOT_RUN",
            live_status=live_status,
            reasons=reasons,
        )
    replay_policy = _recorded_policy_hashes(replayed)
    if replay_policy != current_policy:
        return _review_result(
            base,
            policy_status="CHANGED_DURING_REPLAY",
            replay_status="NOT_RUN",
            live_status=live_status,
            reasons=["POLICY_CHANGED_DURING_REPLAY"],
        )
    if replayed != validation:
        raise ShortPatchError("CURRENT_POLICY_REPLAY_MISMATCH")
    reasons: list[str] = []
    if live_status["status"] == "NOT_CURRENT":
        reasons.append("LIVE_SOURCE_NOT_CURRENT")
    elif live_status["status"] == "UNAVAILABLE":
        reasons.append("LIVE_SOURCE_UNAVAILABLE")
    if reasons:
        return _review_result(
            base,
            policy_status="MATCH",
            replay_status="PASS",
            live_status=live_status,
            reasons=reasons,
        )
    return {
        **base,
        "status": "PASS",
        "exit_code": 0,
        "current_policy_status": "MATCH",
        "current_policy_replay_status": "PASS",
        "live_source_status": live_status,
        "review_reasons": [],
    }


def build_parser() -> argparse.ArgumentParser:
    parser = _StrictArgumentParser(
        description=(
            "Verify a short PATCH record, replay the current validator policy, and "
            "optionally compare a live source."
        )
    )
    parser.add_argument("evidence_dir", type=Path)
    parser.add_argument(
        "--live-source",
        type=Path,
        help="Optional current source path; drift or unavailability returns REVIEW/2.",
    )
    parser.add_argument("--format", choices=("json", "text"), default="text")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    raw_argv = list(sys.argv[1:] if argv is None else argv)
    json_requested = any(
        raw_argv[index] == "--format"
        and index + 1 < len(raw_argv)
        and raw_argv[index + 1] == "json"
        for index in range(len(raw_argv))
    )
    try:
        args = build_parser().parse_args(raw_argv)
        result = verify_directory(args.evidence_dir, live_source=args.live_source)
    except (OSError, ShortPatchError) as error:
        failure = {
            "schema_version": VERIFICATION_SCHEMA,
            "status": "FAIL",
            "exit_code": 1,
            "record_integrity_status": "FAIL",
            "integrity_scope": "SELF_CONSISTENCY_ONLY",
            "error": str(error),
            "humanize_quality_claim_allowed": False,
            "completion_claim_allowed": False,
        }
        print(
            json.dumps(failure, ensure_ascii=False)
            if json_requested
            else f"VERIFICATION FAIL exit=1\n{error}"
        )
        return 1
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    elif result["status"] == "REVIEW":
        print(
            "INTEGRITY PASS scope=SELF_CONSISTENCY_ONLY; "
            f"VERIFICATION REVIEW exit=2 current_policy={result['current_policy_status']} "
            f"replay={result['current_policy_replay_status']} "
            f"live_source={result['live_source_status']['status']}; DELIVERY REVIEW"
        )
        print("review_reasons=" + ",".join(result["review_reasons"]))
    else:
        print(
            "INTEGRITY PASS exit=0 scope=SELF_CONSISTENCY_ONLY; "
            "CURRENT_POLICY_REPLAY PASS; DELIVERY REVIEW"
        )
        print("humanize_quality_claim_allowed=false; academic_correctness=NOT_EVALUATED")
    return int(result["exit_code"])


if __name__ == "__main__":
    raise SystemExit(main())
