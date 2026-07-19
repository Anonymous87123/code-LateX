#!/usr/bin/env python3
"""Build a source-bound, non-overlapping short Humanize PATCH bundle."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import stat
import sys
import tempfile
import unicodedata
from collections import Counter
from pathlib import Path
from typing import Any, Mapping, Sequence


SELECTION_SCHEMA = "humanize-short-patch-selection/v1"
BUNDLE_SCHEMA = "humanize-short-patch/v1"
OFFSET_UNIT = "UTF8_BYTES"
MAX_JSON_BYTES = 2 * 1024 * 1024
MAX_SOURCE_BYTES = 64 * 1024 * 1024
MAX_JSON_DEPTH = 32
MAX_HUNKS = 1000
HUNK_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]{0,63}$")
HEX64_RE = re.compile(r"^[0-9a-f]{64}$")
ALLOWED_DECISIONS = {"DELETE_STYLE_SHELL", "REWRITE", "UNRESOLVED"}
ALLOWED_REQUESTED_OUTPUTS = {"CLEAN", "PATCH"}
ALLOWED_SCENES = {"AUTO", "GENERAL", "COURSE", "MODELING", "RESEARCH"}
ALLOWED_INTENSITIES = {"LIGHT", "BALANCED"}
SELECTION_FIELDS = {
    "schema_version",
    "requested_output",
    "mode",
    "scene",
    "intensity",
    "protected_terms",
    "hunks",
}
SELECTION_HUNK_FIELDS = {
    "hunk_id",
    "decision",
    "source_text",
    "start_byte",
    "replacement",
    "reason",
}
BUNDLE_FIELDS = {
    "schema_version",
    "source_sha256",
    "source_size_bytes",
    "source_encoding",
    "offset_unit",
    "selection_spec_sha256",
    "requested_output",
    "effective_output",
    "mode",
    "scene",
    "intensity",
    "protected_terms",
    "patch_hunks_source_partition",
    "unlisted_source_policy",
    "semantic_judgment",
    "completion_claim_allowed",
    "hunks",
    "bundle_sha256",
}
BUNDLE_HUNK_FIELDS = {
    "hunk_id",
    "decision",
    "start_byte",
    "end_byte",
    "source_text",
    "source_text_sha256",
    "replacement",
    "replacement_sha256",
    "reason",
}
GENERIC_REASONS = {
    "todo",
    "待定",
    "保持原样",
    "无需修改",
    "已经自然",
    "没有问题",
}
BIDI_CONTROLS = {
    "\u061c",
    "\u200e",
    "\u200f",
    "\u202a",
    "\u202b",
    "\u202c",
    "\u202d",
    "\u202e",
    "\u2066",
    "\u2067",
    "\u2068",
    "\u2069",
}


class ShortPatchError(ValueError):
    """Raised when a short PATCH cannot be bound without ambiguity."""


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical_json(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def _reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ShortPatchError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _reject_float(value: str) -> Any:
    raise ShortPatchError(f"JSON floating-point number is forbidden: {value}")


def _reject_constant(value: str) -> Any:
    raise ShortPatchError(f"JSON non-finite number is forbidden: {value}")


def _check_depth(value: Any, depth: int = 0) -> None:
    if depth > MAX_JSON_DEPTH:
        raise ShortPatchError("JSON nesting is too deep")
    if isinstance(value, dict):
        for child in value.values():
            _check_depth(child, depth + 1)
    elif isinstance(value, list):
        for child in value:
            _check_depth(child, depth + 1)


def strict_json_bytes(raw: bytes, label: str) -> Any:
    if len(raw) > MAX_JSON_BYTES:
        raise ShortPatchError(f"{label} exceeds {MAX_JSON_BYTES} bytes")
    try:
        text = raw.decode("utf-8-sig")
    except UnicodeError as error:
        raise ShortPatchError(f"{label} is not strict UTF-8 JSON") from error
    if "\ufffd" in text:
        raise ShortPatchError(f"{label} contains a Unicode replacement character")
    try:
        value = json.loads(
            text,
            object_pairs_hook=_reject_duplicate_keys,
            parse_float=_reject_float,
            parse_constant=_reject_constant,
        )
    except json.JSONDecodeError as error:
        raise ShortPatchError(f"{label} is not valid JSON: {error}") from error
    _check_depth(value)
    return value


def _exact_fields(value: Mapping[str, Any], expected: set[str], label: str) -> None:
    actual = set(value)
    if actual != expected:
        raise ShortPatchError(
            f"{label} fields drifted; missing={sorted(expected - actual)}, "
            f"unknown={sorted(actual - expected)}"
        )


def _absolute_without_resolving(path: Path) -> Path:
    return Path(os.path.abspath(os.fspath(path)))


def _assert_no_reparse_chain(path: Path, label: str) -> None:
    absolute = _absolute_without_resolving(path)
    parts = absolute.parts
    current = Path(parts[0])
    reparse_flag = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
    for part in parts[1:]:
        current /= part
        try:
            metadata = os.lstat(current)
        except FileNotFoundError:
            break
        if stat.S_ISLNK(metadata.st_mode) or (
            getattr(metadata, "st_file_attributes", 0) & reparse_flag
        ):
            raise ShortPatchError(f"{label} path contains a symlink or reparse point")


def safe_input_path(path: Path, label: str) -> Path:
    absolute = _absolute_without_resolving(path)
    _assert_no_reparse_chain(absolute, label)
    try:
        metadata = os.stat(absolute, follow_symlinks=False)
    except OSError as error:
        raise ShortPatchError(f"{label} must be a regular non-symlink file") from error
    if not stat.S_ISREG(metadata.st_mode):
        raise ShortPatchError(f"{label} must be a regular non-symlink file")
    if metadata.st_nlink != 1:
        raise ShortPatchError(f"{label} must not be a hardlink")
    return absolute


def safe_output_path(path: Path, label: str = "output") -> Path:
    absolute = _absolute_without_resolving(path)
    _assert_no_reparse_chain(absolute.parent, label)
    if absolute.exists() or absolute.is_symlink():
        raise ShortPatchError("output_exists")
    return absolute


def _regular_input(path: Path, label: str, limit: int | None = None) -> bytes:
    path = safe_input_path(path, label)
    try:
        raw = path.read_bytes()
    except OSError as error:
        raise ShortPatchError(f"{label} is unreadable: {type(error).__name__}") from error
    if limit is not None and len(raw) > limit:
        raise ShortPatchError(f"{label} exceeds {limit} bytes")
    return raw


def read_source(path: Path) -> bytes:
    raw = _regular_input(path, "source", MAX_SOURCE_BYTES)
    try:
        text = raw.decode("utf-8")
    except UnicodeError as error:
        raise ShortPatchError("source is not strict UTF-8") from error
    if "\ufffd" in text:
        raise ShortPatchError("source contains a Unicode replacement character")
    return raw


def _required_string(value: Any, label: str, *, allow_empty: bool = False) -> str:
    if not isinstance(value, str) or (not allow_empty and not value):
        suffix = "a string" if allow_empty else "a non-empty string"
        raise ShortPatchError(f"{label} must be {suffix}")
    try:
        value.encode("utf-8")
    except UnicodeError as error:
        raise ShortPatchError(f"{label} is not valid Unicode") from error
    return value


def _specific_reason(value: Any, label: str) -> str:
    reason = _required_string(value, label).strip()
    if reason.casefold() in GENERIC_REASONS:
        raise ShortPatchError(f"{label} is generic or unfinished")
    return reason


def _integer(value: Any, label: str, *, minimum: int = 0) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
        raise ShortPatchError(f"{label} must be an integer >= {minimum}")
    return value


def _protected_terms(value: Any, label: str) -> list[str]:
    if not isinstance(value, list) or len(value) > 128:
        raise ShortPatchError(f"{label} must be an array with at most 128 entries")
    terms: list[str] = []
    seen: set[str] = set()
    for index, raw_term in enumerate(value):
        term = _required_string(raw_term, f"{label}[{index}]")
        if len(term) > 512 or any(character in term for character in ("\x00", "\r", "\n")):
            raise ShortPatchError(f"{label}[{index}] is invalid")
        if term in seen:
            raise ShortPatchError(f"{label} contains a duplicate term")
        seen.add(term)
        terms.append(term)
    return terms


def _validate_decision(
    decision: str,
    source_text: str,
    replacement: str,
    label: str,
) -> None:
    if decision not in ALLOWED_DECISIONS:
        raise ShortPatchError(f"{label}.decision is not supported")
    if decision == "DELETE_STYLE_SHELL" and replacement != "":
        raise ShortPatchError(f"{label} DELETE_STYLE_SHELL replacement must be empty")
    if decision == "UNRESOLVED" and replacement != source_text:
        raise ShortPatchError(f"{label} UNRESOLVED replacement must equal source_text")
    if decision == "REWRITE" and (not replacement or replacement == source_text):
        raise ShortPatchError(f"{label} REWRITE replacement must be non-empty and changed")


def _cluster_connector(character: str) -> bool:
    codepoint = ord(character)
    return (
        bool(unicodedata.combining(character))
        or character in {"\u200c", "\u200d"}
        or 0xFE00 <= codepoint <= 0xFE0F
        or 0xE0100 <= codepoint <= 0xE01EF
        or 0x1F3FB <= codepoint <= 0x1F3FF
    )


def _validate_source_boundaries(source: bytes, start: int, end: int, label: str) -> None:
    if (start > 0 and source[start - 1 : start + 1] == b"\r\n") or (
        end < len(source) and source[end - 1 : end + 1] == b"\r\n"
    ):
        raise ShortPatchError(f"{label} splits a CRLF sequence")
    left_start = source[:start].decode("utf-8")
    right_start = source[start:].decode("utf-8")
    left_end = source[:end].decode("utf-8")
    right_end = source[end:].decode("utf-8")
    if (
        (right_start and _cluster_connector(right_start[0]))
        or (left_start and left_start[-1] == "\u200d")
        or (right_end and _cluster_connector(right_end[0]))
        or (left_end and left_end[-1] == "\u200d")
    ):
        raise ShortPatchError(f"{label} splits a grapheme-like sequence")


def _validate_replacement_controls(source_text: str, replacement: str, label: str) -> None:
    source_counts = Counter(source_text)
    replacement_counts = Counter(replacement)
    for character, count in replacement_counts.items():
        if character == "\x00":
            raise ShortPatchError(f"{label} replacement contains NUL")
        if character in BIDI_CONTROLS and count > source_counts[character]:
            raise ShortPatchError(f"{label} replacement introduces a bidi control")
        if (
            unicodedata.category(character) == "Cf"
            and count > source_counts[character]
        ):
            raise ShortPatchError(f"{label} replacement introduces a format control")
        if (
            unicodedata.category(character) == "Cc"
            and character not in {"\t", "\r", "\n"}
            and count > source_counts[character]
        ):
            raise ShortPatchError(f"{label} replacement introduces a control character")


def _locate(source: bytes, source_text: str, requested_start: Any, label: str) -> tuple[int, int]:
    needle = source_text.encode("utf-8")
    if not needle:
        raise ShortPatchError(f"{label}.source_text must not be empty")
    if requested_start is None:
        start = source.find(needle)
        if start < 0:
            raise ShortPatchError(f"{label}.source_text is missing from source")
        positions = [start]
        cursor = start + 1
        while len(positions) <= 16:
            found = source.find(needle, cursor)
            if found < 0:
                break
            positions.append(found)
            cursor = found + 1
        if len(positions) > 1:
            shown = positions[:16]
            suffix = ", ..." if len(positions) > 16 else ""
            raise ShortPatchError(
                f"{label}.source_text is ambiguous; provide start_byte; "
                f"candidate_start_bytes={shown}{suffix}"
            )
    else:
        start = _integer(requested_start, f"{label}.start_byte")
        if source[start : start + len(needle)] != needle:
            raise ShortPatchError(f"{label}.start_byte does not match source_text")
    return start, start + len(needle)


def _bundle_hash(payload: Mapping[str, Any]) -> str:
    unsigned = dict(payload)
    unsigned.pop("bundle_sha256", None)
    return sha256(canonical_json(unsigned))


def validate_bundle_payload(payload: Any, source: bytes | None = None) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise ShortPatchError("bundle must be a JSON object")
    _exact_fields(payload, BUNDLE_FIELDS, "bundle")
    if payload.get("schema_version") != BUNDLE_SCHEMA:
        raise ShortPatchError(f"bundle.schema_version must be {BUNDLE_SCHEMA}")
    if not isinstance(payload.get("source_sha256"), str) or not HEX64_RE.fullmatch(payload["source_sha256"]):
        raise ShortPatchError("bundle.source_sha256 must be a lowercase SHA-256")
    _integer(payload.get("source_size_bytes"), "bundle.source_size_bytes")
    if payload.get("source_encoding") != "utf-8":
        raise ShortPatchError("bundle.source_encoding must be utf-8")
    if payload.get("offset_unit") != OFFSET_UNIT:
        raise ShortPatchError(f"bundle.offset_unit must be {OFFSET_UNIT}")
    if not isinstance(payload.get("selection_spec_sha256"), str) or not HEX64_RE.fullmatch(payload["selection_spec_sha256"]):
        raise ShortPatchError("bundle.selection_spec_sha256 must be a lowercase SHA-256")
    if payload.get("requested_output") not in ALLOWED_REQUESTED_OUTPUTS:
        raise ShortPatchError("bundle.requested_output is invalid")
    if payload.get("effective_output") != "PATCH":
        raise ShortPatchError("bundle.effective_output must be PATCH")
    if payload.get("mode") != "REWRITE":
        raise ShortPatchError("bundle.mode must be REWRITE")
    if payload.get("scene") not in ALLOWED_SCENES:
        raise ShortPatchError("bundle.scene is invalid")
    if payload.get("intensity") not in ALLOWED_INTENSITIES:
        raise ShortPatchError("bundle.intensity is invalid")
    _protected_terms(payload.get("protected_terms"), "bundle.protected_terms")
    if payload.get("patch_hunks_source_partition") != "NON_OVERLAPPING":
        raise ShortPatchError("bundle patch partition must be NON_OVERLAPPING")
    if payload.get("unlisted_source_policy") != "COPY_EXACT":
        raise ShortPatchError("bundle unlisted source policy must be COPY_EXACT")
    if payload.get("semantic_judgment") != "NOT_EVALUATED":
        raise ShortPatchError("bundle semantic_judgment must be NOT_EVALUATED")
    if payload.get("completion_claim_allowed") is not False:
        raise ShortPatchError("bundle completion_claim_allowed must be false")
    hunks = payload.get("hunks")
    if not isinstance(hunks, list) or not hunks or len(hunks) > MAX_HUNKS:
        raise ShortPatchError("bundle.hunks must be a non-empty bounded array")
    seen_ids: set[str] = set()
    previous_start = -1
    previous_end = 0
    for index, raw_hunk in enumerate(hunks):
        label = f"bundle.hunks[{index}]"
        if not isinstance(raw_hunk, dict):
            raise ShortPatchError(f"{label} must be an object")
        _exact_fields(raw_hunk, BUNDLE_HUNK_FIELDS, label)
        hunk_id = _required_string(raw_hunk.get("hunk_id"), f"{label}.hunk_id")
        if not HUNK_ID_RE.fullmatch(hunk_id):
            raise ShortPatchError(f"{label}.hunk_id is invalid")
        collision_key = hunk_id.casefold()
        if collision_key in seen_ids:
            raise ShortPatchError(f"duplicate hunk_id: {hunk_id}")
        seen_ids.add(collision_key)
        start = _integer(raw_hunk.get("start_byte"), f"{label}.start_byte")
        end = _integer(raw_hunk.get("end_byte"), f"{label}.end_byte", minimum=1)
        if end <= start:
            raise ShortPatchError(f"{label} has an empty or reversed source span")
        if start < previous_start:
            raise ShortPatchError(f"{label} is out of source order")
        if start < previous_end:
            raise ShortPatchError(f"{label} overlaps a previous hunk")
        previous_start, previous_end = start, end
        source_text = _required_string(raw_hunk.get("source_text"), f"{label}.source_text")
        replacement = _required_string(raw_hunk.get("replacement"), f"{label}.replacement", allow_empty=True)
        decision = _required_string(raw_hunk.get("decision"), f"{label}.decision")
        _specific_reason(raw_hunk.get("reason"), f"{label}.reason")
        _validate_decision(decision, source_text, replacement, label)
        _validate_replacement_controls(source_text, replacement, label)
        source_text_raw = source_text.encode("utf-8")
        replacement_raw = replacement.encode("utf-8")
        if end - start != len(source_text_raw):
            raise ShortPatchError(f"{label} byte span does not match source_text")
        if raw_hunk.get("source_text_sha256") != sha256(source_text_raw):
            raise ShortPatchError(f"{label}.source_text_sha256 mismatch")
        if raw_hunk.get("replacement_sha256") != sha256(replacement_raw):
            raise ShortPatchError(f"{label}.replacement_sha256 mismatch")
        if source is not None:
            if end > len(source) or source[start:end] != source_text_raw:
                raise ShortPatchError(f"{label} does not match current source bytes")
            _validate_source_boundaries(source, start, end, label)
    if payload.get("bundle_sha256") != _bundle_hash(payload):
        raise ShortPatchError("bundle_sha256 mismatch")
    if source is not None:
        if payload["source_sha256"] != sha256(source):
            raise ShortPatchError("source_sha256 mismatch")
        if payload["source_size_bytes"] != len(source):
            raise ShortPatchError("source_size_bytes mismatch")
    return dict(payload)


def _build_payload(source: bytes, spec_raw: bytes, spec: Any) -> dict[str, Any]:
    if not isinstance(spec, dict):
        raise ShortPatchError("selection spec must be a JSON object")
    _exact_fields(spec, SELECTION_FIELDS, "selection spec")
    if spec.get("schema_version") != SELECTION_SCHEMA:
        raise ShortPatchError(f"selection spec schema_version must be {SELECTION_SCHEMA}")
    requested_output = spec.get("requested_output")
    if requested_output not in ALLOWED_REQUESTED_OUTPUTS:
        raise ShortPatchError("selection spec requested_output must be CLEAN or PATCH")
    if spec.get("mode") != "REWRITE":
        raise ShortPatchError("selection spec mode must be REWRITE")
    scene = spec.get("scene")
    if scene not in ALLOWED_SCENES:
        raise ShortPatchError("selection spec scene is invalid")
    intensity = spec.get("intensity")
    if intensity not in ALLOWED_INTENSITIES:
        raise ShortPatchError("selection spec intensity must be LIGHT or BALANCED")
    protected_terms = _protected_terms(
        spec.get("protected_terms"), "selection spec.protected_terms"
    )
    raw_hunks = spec.get("hunks")
    if not isinstance(raw_hunks, list) or not raw_hunks or len(raw_hunks) > MAX_HUNKS:
        raise ShortPatchError("selection spec hunks must be a non-empty bounded array")
    hunks: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    previous_start = -1
    previous_end = 0
    for index, raw_hunk in enumerate(raw_hunks):
        label = f"selection spec.hunks[{index}]"
        if not isinstance(raw_hunk, dict):
            raise ShortPatchError(f"{label} must be an object")
        _exact_fields(raw_hunk, SELECTION_HUNK_FIELDS, label)
        hunk_id = _required_string(raw_hunk.get("hunk_id"), f"{label}.hunk_id")
        if not HUNK_ID_RE.fullmatch(hunk_id):
            raise ShortPatchError(f"{label}.hunk_id is invalid")
        collision_key = hunk_id.casefold()
        if collision_key in seen_ids:
            raise ShortPatchError(f"duplicate hunk_id: {hunk_id}")
        seen_ids.add(collision_key)
        decision = _required_string(raw_hunk.get("decision"), f"{label}.decision")
        source_text = _required_string(raw_hunk.get("source_text"), f"{label}.source_text")
        replacement = _required_string(raw_hunk.get("replacement"), f"{label}.replacement", allow_empty=True)
        reason = _specific_reason(raw_hunk.get("reason"), f"{label}.reason")
        _validate_decision(decision, source_text, replacement, label)
        start, end = _locate(source, source_text, raw_hunk.get("start_byte"), label)
        _validate_replacement_controls(source_text, replacement, label)
        _validate_source_boundaries(source, start, end, label)
        if start < previous_start:
            raise ShortPatchError(f"{label} is out of source order")
        if start < previous_end:
            raise ShortPatchError(f"{label} overlaps a previous hunk")
        previous_start, previous_end = start, end
        source_text_raw = source_text.encode("utf-8")
        replacement_raw = replacement.encode("utf-8")
        hunks.append(
            {
                "hunk_id": hunk_id,
                "decision": decision,
                "start_byte": start,
                "end_byte": end,
                "source_text": source_text,
                "source_text_sha256": sha256(source_text_raw),
                "replacement": replacement,
                "replacement_sha256": sha256(replacement_raw),
                "reason": reason,
            }
        )
    payload: dict[str, Any] = {
        "schema_version": BUNDLE_SCHEMA,
        "source_sha256": sha256(source),
        "source_size_bytes": len(source),
        "source_encoding": "utf-8",
        "offset_unit": OFFSET_UNIT,
        "selection_spec_sha256": sha256(spec_raw),
        "requested_output": requested_output,
        "effective_output": "PATCH",
        "mode": "REWRITE",
        "scene": scene,
        "intensity": intensity,
        "protected_terms": protected_terms,
        "patch_hunks_source_partition": "NON_OVERLAPPING",
        "unlisted_source_policy": "COPY_EXACT",
        "semantic_judgment": "NOT_EVALUATED",
        "completion_claim_allowed": False,
        "hunks": hunks,
        "bundle_sha256": "",
    }
    payload["bundle_sha256"] = _bundle_hash(payload)
    validate_bundle_payload(payload, source)
    return payload


def _atomic_write_new(path: Path, raw: bytes) -> None:
    path = safe_output_path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.staging-", dir=path.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
        try:
            os.link(temporary, path)
        except FileExistsError as error:
            raise ShortPatchError("output_exists") from error
    finally:
        temporary.unlink(missing_ok=True)


def build_bundle(source_path: Path, spec_path: Path, output_path: Path) -> dict[str, Any]:
    source_path = safe_input_path(source_path, "source")
    spec_path = safe_input_path(spec_path, "selection spec")
    output_path = safe_output_path(output_path)
    source = read_source(source_path)
    spec_raw = _regular_input(spec_path, "selection spec", MAX_JSON_BYTES)
    spec = strict_json_bytes(spec_raw, "selection spec")
    payload = _build_payload(source, spec_raw, spec)
    encoded = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True).encode("utf-8") + b"\n"
    if read_source(source_path) != source:
        raise ShortPatchError("source changed while building bundle")
    if _regular_input(spec_path, "selection spec", MAX_JSON_BYTES) != spec_raw:
        raise ShortPatchError("selection spec changed while building bundle")
    _atomic_write_new(output_path, encoded)
    return payload


def load_bundle(path: Path, source: bytes | None = None) -> tuple[dict[str, Any], bytes]:
    raw = _regular_input(path, "bundle", MAX_JSON_BYTES)
    payload = strict_json_bytes(raw, "bundle")
    return validate_bundle_payload(payload, source), raw


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Build a strict source-bound short Humanize PATCH bundle; never modify the source."
    )
    parser.add_argument("source", type=Path, help="strict UTF-8 source file")
    parser.add_argument("--selection-spec", required=True, type=Path, help="humanize-short-patch-selection/v1 JSON")
    parser.add_argument("--output", required=True, type=Path, help="new bundle path")
    parser.add_argument("--format", choices=("json", "text"), default="text")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")
    args = build_parser().parse_args(argv)
    try:
        payload = build_bundle(args.source, args.selection_spec, args.output)
    except (OSError, ShortPatchError) as error:
        result = {
            "schema_version": BUNDLE_SCHEMA,
            "status": "FAIL",
            "error": str(error),
            "completion_claim_allowed": False,
        }
        print(json.dumps(result, ensure_ascii=False) if args.format == "json" else f"FAIL: {error}")
        return 1
    result = {
        "schema_version": BUNDLE_SCHEMA,
        "status": "BUNDLED",
        "hunks_total": len(payload["hunks"]),
        "bundle_sha256": payload["bundle_sha256"],
        "patch_hunks_source_partition": "NON_OVERLAPPING",
        "semantic_judgment": "NOT_EVALUATED",
        "completion_claim_allowed": False,
    }
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    else:
        print(f"BUNDLED hunks={result['hunks_total']} bundle={result['bundle_sha256']}")
        print("completion_claim_allowed=false; run apply_humanize_short_patch.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
