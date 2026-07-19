#!/usr/bin/env python3
"""Create and finalize a source-bound authoring scaffold for short PATCH v2."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import build_humanize_short_patch as short_patch  # noqa: E402


coverage_layer = short_patch.coverage_layer
AUTHORING_SCHEMA = "humanize-short-patch-selection-authoring/v1"
SELECTION_SCHEMA = short_patch.SELECTION_SCHEMA_V2
HEX64_RE = re.compile(r"^[0-9a-f]{64}$")
AUTHORING_FIELDS = {
    "schema_version",
    "source",
    "configuration",
    "policy_hashes",
    "high_findings",
    "inventory_sha256",
    "spans",
    "hunks",
    "lexical_resolutions",
    "selected_spans",
    "explicit_conflicts",
    "completion_claim_allowed",
    "humanize_quality_claim_allowed",
}
SOURCE_FIELDS = {
    "sha256",
    "size_bytes",
    "encoding",
    "offset_unit",
    "document_format",
    "scan_scene",
}
CONFIGURATION_FIELDS = {
    "requested_output",
    "mode",
    "scene",
    "intensity",
    "source_kind",
    "protected_terms",
}
HIGH_FINDING_FIELDS = {
    "finding_id",
    "signal_id",
    "severity",
    "role",
    "start_byte",
    "end_byte",
    "source_text",
    "source_text_sha256",
    "automatic_reason",
}
SPAN_FIELDS = {"span_id", "finding_ids", "source_text", "start_byte"}
HUNK_FIELDS = {"hunk_id", "span_id", "decision", "replacement", "reason"}
RESOLUTION_FIELDS = {"finding_id", "decision", "hunk_id", "reason"}
SELECTED_FIELDS = {"selection_id", "span_id", "decision", "hunk_id", "reason"}
CONFLICT_FIELDS = set(coverage_layer.CONFLICT_FIELDS)
RESOLUTION_DECISIONS = {"PENDING", "HUNK", "KEEP"}


class AuthoringError(ValueError):
    """Raised when an authoring scaffold cannot be safely finalized."""


class _StrictArgumentParser(argparse.ArgumentParser):
    def error(self, _message: str) -> None:
        raise AuthoringError("INVALID_ARGUMENTS")


def current_policy_hashes() -> dict[str, str]:
    return coverage_layer.current_policy_hashes()


def _exact_fields(value: Mapping[str, Any], expected: set[str], label: str) -> None:
    actual = set(value)
    if actual != expected:
        raise AuthoringError(
            f"{label} fields drifted; missing={sorted(expected - actual)}, "
            f"unknown={sorted(actual - expected)}"
        )


def _identifier(value: Any, label: str) -> str:
    identifier = short_patch._required_string(value, label)
    if not short_patch.HUNK_ID_RE.fullmatch(identifier):
        raise AuthoringError(f"{label} is invalid")
    return identifier


def _document_format(path: Path) -> str:
    return "tex" if path.suffix.casefold() in {".tex", ".ltx"} else "markdown"


def _source_record(source: bytes, document_format: str) -> dict[str, Any]:
    return {
        "sha256": short_patch.sha256(source),
        "size_bytes": len(source),
        "encoding": "utf-8",
        "offset_unit": short_patch.OFFSET_UNIT,
        "document_format": document_format,
        "scan_scene": "AUTO",
    }


def _inventory_hash(
    source: Mapping[str, Any],
    configuration: Mapping[str, Any],
    policy_hashes: Mapping[str, str],
    findings: Sequence[Mapping[str, Any]],
) -> str:
    return short_patch.sha256(
        short_patch.canonical_json(
            {
                "source": dict(source),
                "configuration": dict(configuration),
                "policy_hashes": dict(policy_hashes),
                "high_findings": [dict(item) for item in findings],
            }
        )
    )


def _group_finding_spans(findings: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[tuple[int, int, str], list[str]] = {}
    for finding in findings:
        key = (
            int(finding["start_byte"]),
            int(finding["end_byte"]),
            str(finding["source_text"]),
        )
        grouped.setdefault(key, []).append(str(finding["finding_id"]))
    spans: list[dict[str, Any]] = []
    for index, ((start, _end, text), finding_ids) in enumerate(
        sorted(grouped.items(), key=lambda item: (item[0][0], item[0][1], item[0][2])),
        start=1,
    ):
        spans.append(
            {
                "span_id": f"A{index:03d}",
                "finding_ids": finding_ids,
                "source_text": text,
                "start_byte": start,
            }
        )
    return spans


def create_scaffold(
    source_path: Path,
    output_path: Path,
    *,
    requested_output: str,
    scene: str,
    intensity: str,
    source_kind: str,
    protected_terms: Sequence[str],
) -> dict[str, Any]:
    source_path = short_patch.safe_input_path(source_path, "source")
    output_path = short_patch.safe_output_path(output_path)
    source = short_patch.read_source(source_path)
    if requested_output not in short_patch.ALLOWED_REQUESTED_OUTPUTS:
        raise AuthoringError("requested_output is invalid")
    if scene not in short_patch.ALLOWED_SCENES:
        raise AuthoringError("scene is invalid")
    if intensity not in short_patch.ALLOWED_INTENSITIES:
        raise AuthoringError("intensity is invalid")
    if source_kind not in coverage_layer.SOURCE_KINDS:
        raise AuthoringError("source_kind is invalid")
    terms = short_patch._protected_terms(list(protected_terms), "protected_terms")
    document_format = _document_format(source_path)
    policy_before = current_policy_hashes()
    findings = coverage_layer.scan_high_findings(
        source, document_format=document_format
    )
    source_record = _source_record(source, document_format)
    configuration = {
        "requested_output": requested_output,
        "mode": "REWRITE",
        "scene": scene,
        "intensity": intensity,
        "source_kind": source_kind,
        "protected_terms": terms,
    }
    payload: dict[str, Any] = {
        "schema_version": AUTHORING_SCHEMA,
        "source": source_record,
        "configuration": configuration,
        "policy_hashes": policy_before,
        "high_findings": findings,
        "inventory_sha256": _inventory_hash(
            source_record, configuration, policy_before, findings
        ),
        "spans": _group_finding_spans(findings),
        "hunks": [],
        "lexical_resolutions": [
            {
                "finding_id": item["finding_id"],
                "decision": "PENDING",
                "hunk_id": None,
                "reason": None,
            }
            for item in findings
            if item["role"] == "CANDIDATE"
        ],
        "selected_spans": [],
        "explicit_conflicts": [],
        "completion_claim_allowed": False,
        "humanize_quality_claim_allowed": False,
    }
    encoded = (
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True).encode("utf-8")
        + b"\n"
    )
    if short_patch.read_source(source_path) != source:
        raise AuthoringError("SOURCE_CHANGED_DURING_CREATE")
    if current_policy_hashes() != policy_before:
        raise AuthoringError("POLICY_CHANGED_DURING_CREATE")
    short_patch._atomic_write_new(output_path, encoded)
    return payload


def _validate_source_record(
    recorded: Any, source: bytes, document_format: str
) -> dict[str, Any]:
    if not isinstance(recorded, dict):
        raise AuthoringError("source record must be an object")
    _exact_fields(recorded, SOURCE_FIELDS, "source record")
    if recorded != _source_record(source, document_format):
        raise AuthoringError("SOURCE_DRIFT")
    return dict(recorded)


def _validate_configuration(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise AuthoringError("configuration must be an object")
    _exact_fields(value, CONFIGURATION_FIELDS, "configuration")
    if value.get("requested_output") not in short_patch.ALLOWED_REQUESTED_OUTPUTS:
        raise AuthoringError("configuration.requested_output is invalid")
    if value.get("mode") != "REWRITE":
        raise AuthoringError("configuration.mode must be REWRITE")
    if value.get("scene") not in short_patch.ALLOWED_SCENES:
        raise AuthoringError("configuration.scene is invalid")
    if value.get("intensity") not in short_patch.ALLOWED_INTENSITIES:
        raise AuthoringError("configuration.intensity is invalid")
    if value.get("source_kind") not in coverage_layer.SOURCE_KINDS:
        raise AuthoringError("configuration.source_kind is invalid")
    value = dict(value)
    value["protected_terms"] = short_patch._protected_terms(
        value.get("protected_terms"), "configuration.protected_terms"
    )
    return value


def _validate_policy(value: Any, current: Mapping[str, str]) -> dict[str, str]:
    if not isinstance(value, dict) or not value:
        raise AuthoringError("policy_hashes must be an object")
    if set(value) != set(current):
        raise AuthoringError("SCAFFOLD_POLICY_DRIFT")
    for key, digest in value.items():
        if not isinstance(key, str) or not key or not isinstance(digest, str) or not HEX64_RE.fullmatch(digest):
            raise AuthoringError("policy_hashes are invalid")
    if value != current:
        raise AuthoringError("SCAFFOLD_POLICY_DRIFT")
    return dict(value)


def _validate_high_findings(
    recorded: Any,
    current: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    if not isinstance(recorded, list):
        raise AuthoringError("high_findings must be an array")
    for index, item in enumerate(recorded):
        if not isinstance(item, dict):
            raise AuthoringError(f"high_findings[{index}] must be an object")
        _exact_fields(item, HIGH_FINDING_FIELDS, f"high_findings[{index}]")
    if recorded != list(current):
        raise AuthoringError("HIGH_INVENTORY_DRIFT")
    return [dict(item) for item in recorded]


def _resolve_spans(
    source: bytes,
    raw_spans: Any,
    findings: Sequence[Mapping[str, Any]],
) -> dict[str, dict[str, Any]]:
    if not isinstance(raw_spans, list) or not raw_spans:
        raise AuthoringError("spans must be a non-empty array")
    finding_by_id = {str(item["finding_id"]): item for item in findings}
    finding_membership: dict[str, str] = {}
    spans: dict[str, dict[str, Any]] = {}
    span_ranges: set[tuple[int, int]] = set()
    for index, item in enumerate(raw_spans):
        label = f"spans[{index}]"
        if not isinstance(item, dict):
            raise AuthoringError(f"{label} must be an object")
        _exact_fields(item, SPAN_FIELDS, label)
        span_id = _identifier(item.get("span_id"), f"{label}.span_id")
        key = span_id.casefold()
        if key in spans:
            raise AuthoringError("duplicate span_id")
        text = short_patch._required_string(item.get("source_text"), f"{label}.source_text")
        try:
            start, end = short_patch._locate(
                source, text, item.get("start_byte"), label
            )
            short_patch._validate_source_boundaries(source, start, end, label)
        except short_patch.ShortPatchError as error:
            raise AuthoringError(str(error)) from error
        if (start, end) in span_ranges:
            raise AuthoringError("duplicate source span")
        span_ranges.add((start, end))
        ids = item.get("finding_ids")
        if (
            not isinstance(ids, list)
            or any(not isinstance(finding_id, str) for finding_id in ids)
            or len(ids) != len(set(ids))
        ):
            raise AuthoringError(f"{label}.finding_ids is invalid")
        for finding_id in ids:
            if not isinstance(finding_id, str) or finding_id not in finding_by_id:
                raise AuthoringError(f"{label}.finding_ids contains an unknown finding")
            if finding_id in finding_membership:
                raise AuthoringError("finding_id is bound by multiple spans")
            finding = finding_by_id[finding_id]
            if start != finding["start_byte"] or end != finding["end_byte"]:
                raise AuthoringError("finding span binding drifted")
            finding_membership[finding_id] = span_id
        spans[key] = {
            "span_id": span_id,
            "source_text": text,
            "start_byte": start,
            "end_byte": end,
        }
    if set(finding_membership) != set(finding_by_id):
        raise AuthoringError("high finding span registry is incomplete")
    return spans


def _compile_hunks(
    raw_hunks: Any, spans: Mapping[str, Mapping[str, Any]]
) -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]]]:
    if not isinstance(raw_hunks, list) or not raw_hunks or len(raw_hunks) > short_patch.MAX_HUNKS:
        raise AuthoringError("hunks must be a non-empty bounded array")
    hunks: list[dict[str, Any]] = []
    by_id: dict[str, dict[str, Any]] = {}
    for index, item in enumerate(raw_hunks):
        label = f"hunks[{index}]"
        if not isinstance(item, dict):
            raise AuthoringError(f"{label} must be an object")
        _exact_fields(item, HUNK_FIELDS, label)
        hunk_id = _identifier(item.get("hunk_id"), f"{label}.hunk_id")
        hunk_key = hunk_id.casefold()
        if hunk_key in by_id:
            raise AuthoringError("duplicate hunk_id")
        span_id = _identifier(item.get("span_id"), f"{label}.span_id")
        span = spans.get(span_id.casefold())
        if span is None:
            raise AuthoringError(f"{label}.span_id is unknown")
        decision = short_patch._required_string(item.get("decision"), f"{label}.decision")
        replacement = short_patch._required_string(
            item.get("replacement"), f"{label}.replacement", allow_empty=True
        )
        reason = short_patch._specific_reason(item.get("reason"), f"{label}.reason")
        try:
            short_patch._validate_decision(
                decision, str(span["source_text"]), replacement, label
            )
            short_patch._validate_replacement_controls(
                str(span["source_text"]), replacement, label
            )
        except short_patch.ShortPatchError as error:
            raise AuthoringError(str(error)) from error
        compiled = {
            "hunk_id": hunk_id,
            "decision": decision,
            "source_text": span["source_text"],
            "start_byte": span["start_byte"],
            "replacement": replacement,
            "reason": reason,
        }
        hunks.append(compiled)
        by_id[hunk_key] = {**compiled, "end_byte": span["end_byte"], "span_id": span_id}
    return hunks, by_id


def _compile_resolutions(
    raw: Any,
    findings: Sequence[Mapping[str, Any]],
    hunks: Mapping[str, Mapping[str, Any]],
) -> list[dict[str, Any]]:
    if not isinstance(raw, list):
        raise AuthoringError("lexical_resolutions must be an array")
    candidate_by_id = {
        str(item["finding_id"]): item
        for item in findings
        if item["role"] == "CANDIDATE"
    }
    seen: set[str] = set()
    keeps: list[dict[str, Any]] = []
    for index, item in enumerate(raw):
        label = f"lexical_resolutions[{index}]"
        if not isinstance(item, dict):
            raise AuthoringError(f"{label} must be an object")
        _exact_fields(item, RESOLUTION_FIELDS, label)
        finding_id = short_patch._required_string(item.get("finding_id"), f"{label}.finding_id")
        if finding_id not in candidate_by_id or finding_id in seen:
            raise AuthoringError("lexical_resolutions has an unknown or duplicate finding_id")
        seen.add(finding_id)
        decision = short_patch._required_string(item.get("decision"), f"{label}.decision")
        if decision not in RESOLUTION_DECISIONS:
            raise AuthoringError(f"{label}.decision is invalid")
        if decision == "PENDING":
            raise AuthoringError("PENDING_LEXICAL_RESOLUTION")
        finding = candidate_by_id[finding_id]
        if decision == "HUNK":
            hunk_id = _identifier(item.get("hunk_id"), f"{label}.hunk_id")
            hunk = hunks.get(hunk_id.casefold())
            if hunk is None or not (
                int(hunk["start_byte"]) <= int(finding["start_byte"])
                and int(hunk["end_byte"]) >= int(finding["end_byte"])
            ):
                raise AuthoringError("LEXICAL_HUNK_MISMATCH")
            if item.get("reason") is not None:
                raise AuthoringError(f"{label}.reason must be null for HUNK")
        else:
            if item.get("hunk_id") is not None:
                raise AuthoringError(f"{label}.hunk_id must be null for KEEP")
            reason = short_patch._specific_reason(item.get("reason"), f"{label}.reason")
            keeps.append(
                {
                    "signal_id": finding["signal_id"],
                    "source_text": finding["source_text"],
                    "start_byte": finding["start_byte"],
                    "reason": reason,
                }
            )
    if seen != set(candidate_by_id):
        raise AuthoringError("lexical_resolutions does not cover every candidate high")
    return keeps


def _compile_selected(
    raw: Any,
    spans: Mapping[str, Mapping[str, Any]],
    hunks: Mapping[str, Mapping[str, Any]],
) -> list[dict[str, Any]]:
    if not isinstance(raw, list):
        raise AuthoringError("selected_spans must be an array")
    selected: list[dict[str, Any]] = []
    for index, item in enumerate(raw):
        label = f"selected_spans[{index}]"
        if not isinstance(item, dict):
            raise AuthoringError(f"{label} must be an object")
        _exact_fields(item, SELECTED_FIELDS, label)
        selection_id = _identifier(item.get("selection_id"), f"{label}.selection_id")
        span_id = _identifier(item.get("span_id"), f"{label}.span_id")
        span = spans.get(span_id.casefold())
        if span is None:
            raise AuthoringError(f"{label}.span_id is unknown")
        decision = short_patch._required_string(item.get("decision"), f"{label}.decision")
        reason = short_patch._specific_reason(item.get("reason"), f"{label}.reason")
        if decision == "HUNK":
            hunk_id = _identifier(item.get("hunk_id"), f"{label}.hunk_id")
            hunk = hunks.get(hunk_id.casefold())
            if hunk is None or hunk["span_id"].casefold() != span_id.casefold():
                raise AuthoringError("SELECTION_HUNK_MISMATCH")
        elif decision == "KEEP":
            if item.get("hunk_id") is not None:
                raise AuthoringError(f"{label}.hunk_id must be null for KEEP")
            hunk_id = None
        else:
            raise AuthoringError(f"{label}.decision is invalid")
        selected.append(
            {
                "selection_id": selection_id,
                "source_text": span["source_text"],
                "start_byte": span["start_byte"],
                "decision": decision,
                "hunk_id": hunk_id,
                "reason": reason,
            }
        )
    return selected


def _compile_conflicts(raw: Any) -> list[dict[str, Any]]:
    if not isinstance(raw, list):
        raise AuthoringError("explicit_conflicts must be an array")
    conflicts: list[dict[str, Any]] = []
    for index, item in enumerate(raw):
        label = f"explicit_conflicts[{index}]"
        if not isinstance(item, dict):
            raise AuthoringError(f"{label} must be an object")
        _exact_fields(item, CONFLICT_FIELDS, label)
        conflicts.append(dict(item))
    return conflicts


def finalize_scaffold(
    source_path: Path,
    authoring_path: Path,
    output_path: Path,
) -> dict[str, Any]:
    source_path = short_patch.safe_input_path(source_path, "source")
    authoring_path = short_patch.safe_input_path(authoring_path, "authoring scaffold")
    output_path = short_patch.safe_output_path(output_path)
    source = short_patch.read_source(source_path)
    authoring_raw = short_patch._regular_input(
        authoring_path, "authoring scaffold", short_patch.MAX_JSON_BYTES
    )
    payload = short_patch.strict_json_bytes(authoring_raw, "authoring scaffold")
    if not isinstance(payload, dict):
        raise AuthoringError("authoring scaffold must be an object")
    _exact_fields(payload, AUTHORING_FIELDS, "authoring scaffold")
    if payload.get("schema_version") != AUTHORING_SCHEMA:
        raise AuthoringError("authoring scaffold schema_version is invalid")
    if payload.get("completion_claim_allowed") is not False or payload.get("humanize_quality_claim_allowed") is not False:
        raise AuthoringError("authoring scaffold claim flags are invalid")
    document_format = _document_format(source_path)
    source_record = _validate_source_record(payload.get("source"), source, document_format)
    configuration = _validate_configuration(payload.get("configuration"))
    policy_before = current_policy_hashes()
    policy = _validate_policy(payload.get("policy_hashes"), policy_before)
    current_findings = coverage_layer.scan_high_findings(
        source, document_format=document_format
    )
    findings = _validate_high_findings(payload.get("high_findings"), current_findings)
    expected_inventory_hash = _inventory_hash(
        source_record, configuration, policy, findings
    )
    if payload.get("inventory_sha256") != expected_inventory_hash:
        raise AuthoringError("inventory_sha256 mismatch")
    spans = _resolve_spans(source, payload.get("spans"), findings)
    raw_resolutions = payload.get("lexical_resolutions")
    if isinstance(raw_resolutions, list) and any(
        isinstance(item, dict) and item.get("decision") == "PENDING"
        for item in raw_resolutions
    ):
        raise AuthoringError("PENDING_LEXICAL_RESOLUTION")
    hunks, hunk_by_id = _compile_hunks(payload.get("hunks"), spans)
    lexical_keeps = _compile_resolutions(
        raw_resolutions, findings, hunk_by_id
    )
    selected = _compile_selected(payload.get("selected_spans"), spans, hunk_by_id)
    conflicts = _compile_conflicts(payload.get("explicit_conflicts"))
    if configuration["source_kind"] == "INLINE_SELECTION" and not selected:
        raise AuthoringError("BOUND_SELECTION_REQUIRED")
    selection: dict[str, Any] = {
        "schema_version": SELECTION_SCHEMA,
        "requested_output": configuration["requested_output"],
        "mode": "REWRITE",
        "scene": configuration["scene"],
        "intensity": configuration["intensity"],
        "protected_terms": configuration["protected_terms"],
        "hunks": hunks,
        "coverage": {
            "source_kind": configuration["source_kind"],
            "lexical_keeps": lexical_keeps,
            "selected_spans": selected,
            "explicit_conflicts": conflicts,
        },
    }
    encoded = (
        json.dumps(selection, ensure_ascii=False, indent=2, sort_keys=True).encode("utf-8")
        + b"\n"
    )
    try:
        short_patch._build_payload(
            source,
            encoded,
            selection,
            document_format=document_format,
        )
    except (short_patch.ShortPatchError, coverage_layer.CoverageError) as error:
        raise AuthoringError(str(error)) from error
    if short_patch.read_source(source_path) != source:
        raise AuthoringError("SOURCE_CHANGED_DURING_FINALIZE")
    if short_patch._regular_input(
        authoring_path, "authoring scaffold", short_patch.MAX_JSON_BYTES
    ) != authoring_raw:
        raise AuthoringError("AUTHORING_CHANGED_DURING_FINALIZE")
    if current_policy_hashes() != policy_before:
        raise AuthoringError("POLICY_CHANGED_DURING_FINALIZE")
    short_patch._atomic_write_new(output_path, encoded)
    return selection


def build_parser() -> argparse.ArgumentParser:
    parser = _StrictArgumentParser(
        description="Create or finalize a source-bound short PATCH authoring scaffold."
    )
    subparsers = parser.add_subparsers(
        dest="command", required=True, parser_class=_StrictArgumentParser
    )
    create = subparsers.add_parser("create")
    create.add_argument("source", type=Path)
    create.add_argument("--requested-output", choices=("CLEAN", "PATCH"), default="PATCH")
    create.add_argument("--scene", choices=tuple(sorted(short_patch.ALLOWED_SCENES)), required=True)
    create.add_argument("--intensity", choices=tuple(sorted(short_patch.ALLOWED_INTENSITIES)), default="BALANCED")
    create.add_argument("--source-kind", choices=tuple(sorted(coverage_layer.SOURCE_KINDS)), required=True)
    create.add_argument("--term", action="append", default=[])
    create.add_argument("--output", required=True, type=Path)
    create.add_argument("--format", choices=("json", "text"), default="text")
    finalize = subparsers.add_parser("finalize")
    finalize.add_argument("source", type=Path)
    finalize.add_argument("--authoring", required=True, type=Path)
    finalize.add_argument("--output", required=True, type=Path)
    finalize.add_argument("--format", choices=("json", "text"), default="text")
    return parser


def _requested_format(argv: Sequence[str]) -> str:
    for index, value in enumerate(argv):
        if value == "--format" and index + 1 < len(argv):
            return "json" if argv[index + 1] == "json" else "text"
        if value == "--format=json":
            return "json"
    return "text"


def main(argv: Sequence[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")
    raw_argv = list(sys.argv[1:] if argv is None else argv)
    output_format = _requested_format(raw_argv)
    try:
        args = build_parser().parse_args(raw_argv)
        if args.command == "create":
            payload = create_scaffold(
                args.source,
                args.output,
                requested_output=args.requested_output,
                scene=args.scene,
                intensity=args.intensity,
                source_kind=args.source_kind,
                protected_terms=args.term,
            )
            result = {
                "schema_version": AUTHORING_SCHEMA,
                "status": "PENDING",
                "high_findings_total": len(payload["high_findings"]),
                "pending_resolutions_total": len(payload["lexical_resolutions"]),
                "completion_claim_allowed": False,
                "humanize_quality_claim_allowed": False,
            }
        else:
            selection = finalize_scaffold(
                args.source, args.authoring, args.output
            )
            result = {
                "schema_version": selection["schema_version"],
                "status": "FINALIZED",
                "hunks_total": len(selection["hunks"]),
                "selected_spans_total": len(selection["coverage"]["selected_spans"]),
                "explicit_conflicts_total": len(selection["coverage"]["explicit_conflicts"]),
                "completion_claim_allowed": False,
                "humanize_quality_claim_allowed": False,
            }
    except (OSError, AuthoringError, short_patch.ShortPatchError) as error:
        failure = {
            "schema_version": AUTHORING_SCHEMA,
            "status": "FAIL",
            "error": str(error),
            "completion_claim_allowed": False,
            "humanize_quality_claim_allowed": False,
        }
        print(
            json.dumps(failure, ensure_ascii=False, sort_keys=True)
            if output_format == "json"
            else f"FAIL: {error}"
        )
        return 1
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    elif result["status"] == "PENDING":
        print(
            f"PENDING high={result['high_findings_total']} "
            f"resolutions={result['pending_resolutions_total']}"
        )
        print("completion_claim_allowed=false; edit the scaffold, then run finalize")
    else:
        print(
            f"FINALIZED hunks={result['hunks_total']} "
            f"selected={result['selected_spans_total']}"
        )
        print("completion_claim_allowed=false; run build_humanize_short_patch.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
