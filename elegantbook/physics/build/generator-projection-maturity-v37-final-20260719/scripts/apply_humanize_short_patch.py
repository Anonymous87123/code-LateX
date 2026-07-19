#!/usr/bin/env python3
"""Validate and apply a source-bound short Humanize PATCH to a new directory."""

from __future__ import annotations

import argparse
import difflib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Sequence


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import build_humanize_short_patch as short_patch  # noqa: E402


ShortPatchError = short_patch.ShortPatchError
RESULT_SCHEMA = "humanize-short-patch-result/v1"
EVIDENCE_MANIFEST_SCHEMA = "humanize-short-patch-evidence-manifest/v1"
COVERAGE_RESULT_FIELDS = {
    "coverage_path",
    "coverage_status",
    "coverage_completion_claim_allowed",
    "semantic_completeness_claim_allowed",
    "coverage_claim_scope",
    "coverage_scene",
    "coverage_scan_scene",
    "coverage_source_kind",
}
LEGACY_RESULT_FIELDS = {
    "schema_version",
    "status",
    "delivery_gate_status",
    "exit_code",
    "structural_validation_status",
    "patch_application_status",
    "unified_validator_status",
    "hard_invariant_layer_status",
    "validator_delivery_gate_status",
    "validator_exit_code",
    "paired_quality_review_status",
    "semantic_judgment",
    "source_sha256",
    "candidate_sha256",
    "bundle_sha256",
    "hunks_total",
    "decision_counts",
    "unresolved_total",
    "patch_hunks_source_partition",
    "unlisted_source_policy",
    "candidate_path",
    "diff_path",
    "bundle_path",
    "validation_path",
    "source_snapshot_path",
    "evidence_manifest_path",
    "artifacts_written",
    "humanize_quality_claim_allowed",
    "completion_claim_allowed",
}
TRANSITIONAL_RESULT_FIELDS = LEGACY_RESULT_FIELDS | {
    "coverage_path",
    "coverage_status",
    "coverage_completion_claim_allowed",
    "semantic_completeness_claim_allowed",
}
CURRENT_RESULT_FIELDS = LEGACY_RESULT_FIELDS | COVERAGE_RESULT_FIELDS | {
    "delivery_gate_exit_code"
}


def _candidate_name(source_path: Path) -> str:
    suffix = source_path.suffix.casefold()
    if suffix == ".ltx":
        return "candidate.review.tex"
    return "candidate.review" + (suffix if suffix in {".md", ".tex", ".txt"} else ".txt")


def _apply_bytes(source: bytes, bundle: dict[str, Any]) -> bytes:
    pieces: list[bytes] = []
    cursor = 0
    for hunk in bundle["hunks"]:
        start = int(hunk["start_byte"])
        end = int(hunk["end_byte"])
        pieces.append(source[cursor:start])
        pieces.append(str(hunk["replacement"]).encode("utf-8"))
        cursor = end
    pieces.append(source[cursor:])
    return b"".join(pieces)


def _diff(source: bytes, candidate: bytes) -> bytes:
    before = source.decode("utf-8").splitlines(keepends=True)
    after = candidate.decode("utf-8").splitlines(keepends=True)
    rendered = "".join(
        difflib.unified_diff(
            before,
            after,
            fromfile="source",
            tofile="candidate",
            lineterm="\n",
        )
    )
    return rendered.encode("utf-8")


def _run_validator(
    source_path: Path,
    candidate_path: Path,
    bundle: dict[str, Any],
) -> tuple[dict[str, Any], bytes]:
    validator = SCRIPT_DIR / "validate_humanize_output.py"
    if validator.is_symlink() or not validator.is_file():
        raise ShortPatchError("UNIFIED_VALIDATOR_UNAVAILABLE")
    command = [
            sys.executable,
            str(validator),
            str(source_path),
            str(candidate_path),
            "--mode",
            "REWRITE",
            "--scene",
            str(bundle["scene"]),
            "--format",
            "json",
        ]
    for term in bundle["protected_terms"]:
        command.extend(("--term", str(term)))
    process = subprocess.run(
        command,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=False,
        check=False,
    )
    if process.stderr:
        raise ShortPatchError("UNIFIED_VALIDATOR_STDERR_NONEMPTY")
    try:
        payload = short_patch.strict_json_bytes(process.stdout, "validator output")
    except ShortPatchError as error:
        raise ShortPatchError("UNIFIED_VALIDATOR_OUTPUT_INVALID") from error
    if not isinstance(payload, dict):
        raise ShortPatchError("UNIFIED_VALIDATOR_OUTPUT_INVALID")
    observed_exit = process.returncode
    recorded_exit = payload.get("exit_code")
    delivery = payload.get("delivery_gate_status")
    hard_layer = payload.get("hard_invariant_layer_status")
    mechanical = payload.get("mechanical_validation_status")
    evidence = payload.get("evidence")
    if (
        observed_exit not in {0, 1, 2}
        or isinstance(recorded_exit, bool)
        or not isinstance(recorded_exit, int)
        or recorded_exit != observed_exit
        or delivery not in {"PASS", "REVIEW", "FAIL"}
        or mechanical not in {"PASS", "REVIEW", "FAIL"}
        or hard_layer not in {"PASS", "FAIL"}
        or not isinstance(evidence, dict)
    ):
        raise ShortPatchError("UNIFIED_VALIDATOR_RESULT_INCONSISTENT")
    expected = {"PASS": 0, "REVIEW": 2, "FAIL": 1}
    if expected[delivery] != observed_exit:
        raise ShortPatchError("UNIFIED_VALIDATOR_RESULT_INCONSISTENT")
    if (mechanical == "FAIL" or hard_layer == "FAIL") and (
        delivery != "FAIL" or observed_exit != 1
    ):
        raise ShortPatchError("UNIFIED_VALIDATOR_RESULT_INCONSISTENT")
    expected_before = str(bundle["source_sha256"])
    expected_after = short_patch.sha256(candidate_path.read_bytes())
    if (
        evidence.get("before_sha256") != expected_before
        or evidence.get("after_sha256") != expected_after
    ):
        raise ShortPatchError("UNIFIED_VALIDATOR_EVIDENCE_HASH_MISMATCH")
    if observed_exit == 1 or delivery == "FAIL" or hard_layer == "FAIL":
        raise ShortPatchError("UNIFIED_VALIDATOR_FAILED")
    return payload, process.stdout


def _result(
    bundle: dict[str, Any],
    candidate: bytes,
    candidate_name: str,
    validation: dict[str, Any],
) -> dict[str, Any]:
    counts = {decision: 0 for decision in sorted(short_patch.ALLOWED_DECISIONS)}
    for hunk in bundle["hunks"]:
        counts[hunk["decision"]] += 1
    coverage = bundle.get("coverage")
    coverage_present = isinstance(coverage, dict)
    artifacts_written = [
        candidate_name,
        "patch.diff",
        "patch.bundle.json",
        "source.snapshot.bin",
        "validation.json",
        "result.json",
        "evidence-manifest.json",
    ]
    if coverage_present:
        artifacts_written.insert(1, "coverage.json")
    return {
        "schema_version": RESULT_SCHEMA,
        "status": "REVIEW",
        "delivery_gate_status": "REVIEW",
        "delivery_gate_exit_code": 2,
        "exit_code": 2,
        "structural_validation_status": "PASS",
        "patch_application_status": "PASS",
        "unified_validator_status": validation["mechanical_validation_status"],
        "hard_invariant_layer_status": validation["hard_invariant_layer_status"],
        "validator_delivery_gate_status": validation["delivery_gate_status"],
        "validator_exit_code": validation["exit_code"],
        "paired_quality_review_status": validation["paired_quality_review_status"],
        "semantic_judgment": "NOT_EVALUATED",
        "source_sha256": bundle["source_sha256"],
        "candidate_sha256": short_patch.sha256(candidate),
        "bundle_sha256": bundle["bundle_sha256"],
        "hunks_total": len(bundle["hunks"]),
        "decision_counts": counts,
        "unresolved_total": counts["UNRESOLVED"],
        "patch_hunks_source_partition": "NON_OVERLAPPING",
        "unlisted_source_policy": "COPY_EXACT",
        "candidate_path": candidate_name,
        "diff_path": "patch.diff",
        "bundle_path": "patch.bundle.json",
        "validation_path": "validation.json",
        "source_snapshot_path": "source.snapshot.bin",
        "evidence_manifest_path": "evidence-manifest.json",
        "coverage_path": "coverage.json" if coverage_present else None,
        "coverage_status": (
            str(coverage["mechanical_coverage_status"])
            if coverage_present
            else "NOT_PROVIDED"
        ),
        "coverage_completion_claim_allowed": bool(
            coverage_present and coverage["coverage_completion_claim_allowed"] is True
        ),
        "semantic_completeness_claim_allowed": False,
        "coverage_claim_scope": (
            coverage["coverage_claim_scope"] if coverage_present else None
        ),
        "coverage_scene": (
            coverage["source"]["scene"] if coverage_present else None
        ),
        "coverage_scan_scene": (
            coverage["source"]["scan_scene"] if coverage_present else None
        ),
        "coverage_source_kind": (
            coverage["source"]["source_kind"] if coverage_present else None
        ),
        "artifacts_written": artifacts_written,
        "humanize_quality_claim_allowed": False,
        "completion_claim_allowed": False,
    }


def _manifest(staging: Path, artifact_names: set[str]) -> dict[str, Any]:
    artifacts = []
    for name in sorted(artifact_names, key=lambda value: value.encode("utf-8")):
        raw = (staging / name).read_bytes()
        artifacts.append({"path": name, "size": len(raw), "sha256": short_patch.sha256(raw)})
    payload: dict[str, Any] = {
        "schema_version": EVIDENCE_MANIFEST_SCHEMA,
        "integrity_scope": "SELF_CONSISTENCY_ONLY",
        "artifacts": artifacts,
        "manifest_sha256": "",
    }
    unsigned = dict(payload)
    unsigned.pop("manifest_sha256")
    payload["manifest_sha256"] = short_patch.sha256(short_patch.canonical_json(unsigned))
    return payload


def apply_patch(source_path: Path, bundle_path: Path, output_dir: Path) -> dict[str, Any]:
    source_path = short_patch.safe_input_path(source_path, "source")
    bundle_path = short_patch.safe_input_path(bundle_path, "bundle")
    output_dir = short_patch.safe_output_path(output_dir)
    source = short_patch.read_source(source_path)
    bundle, bundle_raw = short_patch.load_bundle(bundle_path, source)
    candidate = _apply_bytes(source, bundle)
    candidate_name = _candidate_name(source_path)
    output_dir.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(
        tempfile.mkdtemp(prefix=f".{output_dir.name}.staging-", dir=output_dir.parent)
    )
    published = False
    try:
        source_snapshot_path = staging / "source.snapshot.bin"
        source_snapshot_path.write_bytes(source)
        candidate_path = staging / candidate_name
        candidate_path.write_bytes(candidate)
        validation, validation_raw = _run_validator(
            source_snapshot_path, candidate_path, bundle
        )
        result = _result(bundle, candidate, candidate_name, validation)
        (staging / "patch.diff").write_bytes(_diff(source, candidate))
        (staging / "patch.bundle.json").write_bytes(bundle_raw)
        (staging / "validation.json").write_bytes(validation_raw)
        if "coverage" in bundle:
            (staging / "coverage.json").write_text(
                json.dumps(bundle["coverage"], ensure_ascii=False, indent=2, sort_keys=True)
                + "\n",
                encoding="utf-8",
            )
        (staging / "result.json").write_text(
            json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        evidence_artifacts = {
            candidate_name,
            "patch.diff",
            "patch.bundle.json",
            "source.snapshot.bin",
            "validation.json",
            "result.json",
        }
        if "coverage" in bundle:
            evidence_artifacts.add("coverage.json")
        manifest = _manifest(staging, evidence_artifacts)
        (staging / "evidence-manifest.json").write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        expected = {*evidence_artifacts, "evidence-manifest.json"}
        actual = {path.name for path in staging.iterdir() if path.is_file()}
        if actual != expected:
            raise ShortPatchError("staging output file set drifted")
        if short_patch.read_source(source_path) != source:
            raise ShortPatchError("source changed while applying patch")
        current_bundle, current_bundle_raw = short_patch.load_bundle(bundle_path, source)
        if current_bundle_raw != bundle_raw or current_bundle["bundle_sha256"] != bundle["bundle_sha256"]:
            raise ShortPatchError("bundle changed while applying patch")
        if output_dir.exists() or output_dir.is_symlink():
            raise ShortPatchError("output_exists")
        short_patch._assert_no_reparse_chain(output_dir.parent, "output")
        os.rename(staging, output_dir)
        published = True
    finally:
        if not published and staging.exists():
            shutil.rmtree(staging)
    return result


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Strictly validate and apply a humanize-short-patch/v1 or v2 bundle to a new "
            "derived directory. The source is never overwritten."
        )
    )
    parser.add_argument("source", type=Path, help="the exact strict UTF-8 source bound by the bundle")
    parser.add_argument("--bundle", required=True, type=Path, help="humanize-short-patch/v1 or v2 bundle")
    parser.add_argument("--output", required=True, type=Path, help="new output directory")
    parser.add_argument("--format", choices=("json", "text"), default="text")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")
    args = build_parser().parse_args(argv)
    try:
        result = apply_patch(args.source, args.bundle, args.output)
    except (OSError, ShortPatchError) as error:
        failure = {
            "schema_version": RESULT_SCHEMA,
            "delivery_gate_status": "FAIL",
            "exit_code": 1,
            "error": str(error),
            "humanize_quality_claim_allowed": False,
            "completion_claim_allowed": False,
        }
        print(json.dumps(failure, ensure_ascii=False) if args.format == "json" else f"DELIVERY FAIL exit=1\n{error}")
        return 1
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    else:
        print("DELIVERY REVIEW exit=2")
        print(
            f"structural_validation=PASS hunks={result['hunks_total']} "
            f"unresolved={result['unresolved_total']}"
        )
        print(
            f"unified_validator={result['unified_validator_status']}; "
            f"paired_quality={result['paired_quality_review_status']}; "
            f"coverage={result['coverage_status']}; "
            "semantic_judgment=NOT_EVALUATED"
        )
        if result["coverage_status"] == "PASS":
            print(
                f"coverage_scope={result['coverage_claim_scope']} "
                f"scene={result['coverage_scene']} "
                f"scan_scene={result['coverage_scan_scene']}"
            )
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
