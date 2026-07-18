#!/usr/bin/env python3
"""Build an auditable, excerpt-free action profile from approved MD/TeX sources.

The profile is intentionally not a language-model prompt and not a corpus export.
It verifies that abstract action cards still point at readable source locations,
then emits hashes and audit statuses rather than any source prose. This makes
source-derived editing actions reproducible without turning private documents
into a sentence bank.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Sequence


SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
DEFAULT_CATALOG = SKILL_DIR / "references" / "corpus-action-sources.json"
VALID_SCENES = {"ALL", "COURSE", "GENERAL", "MODELING", "RESEARCH", "REPORT"}
VALID_CARD_KINDS = {"positive_action", "negative_guard"}
VALID_ORIGIN_CLASSES = {
    "HUMAN_CONFIRMED",
    "MODEL_GENERATED",
    "MODEL_ORIGIN_UNRESOLVED",
    "OCR_INHERITED",
    "THIRD_PARTY",
    "UNKNOWN",
}
POSITIVE_DISALLOWED_ORIGINS = {"MODEL_GENERATED"}
EXCLUDED_ROLES = {"unreadable_excluded", "user_excluded", "version_duplicate_excluded"}
CARD_SOURCE_ROLES = {
    "positive_action": {"positive_action_reference"},
    "negative_guard": {"negative_template_reference"},
}


class CatalogError(ValueError):
    """Raised when the static source-action catalog is invalid."""


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _has_disallowed_controls(text: str) -> bool:
    return any((ord(char) < 32 and char not in "\t\n\r") or 0x7F <= ord(char) <= 0x9F for char in text)


def decode_source(raw: bytes) -> tuple[str | None, str | None, str | None]:
    """Decode a source conservatively and return text, encoding, and an issue."""
    if b"\x00" in raw:
        return None, None, "binary_or_nul_bytes"
    if raw.startswith((b"\xff\xfe", b"\xfe\xff")):
        return None, None, "unsupported_utf16_bom"
    for encoding in ("utf-8-sig", "utf-8", "gb18030"):
        try:
            text = raw.decode(encoding)
        except UnicodeDecodeError:
            continue
        if "\ufffd" in text:
            return None, encoding, "replacement_character"
        if _has_disallowed_controls(text):
            return None, encoding, "disallowed_control_characters"
        return text, encoding, None
    return None, None, "undecodable_utf8_or_gb18030"


def _require_mapping(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise CatalogError(f"{label} must be an object")
    return value


def _require_text(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise CatalogError(f"{label} must be a non-empty string")
    return value.strip()


def load_catalog(path: Path) -> dict[str, Any]:
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError as error:
        raise CatalogError(f"cannot read catalog: {error}") from error
    try:
        catalog = json.loads(raw)
    except json.JSONDecodeError as error:
        raise CatalogError(f"invalid catalog JSON: {error}") from error
    catalog = _require_mapping(catalog, "catalog")
    if catalog.get("schema_version") != 2:
        raise CatalogError("unsupported or missing schema_version")
    if "source_excerpt" in raw or "source_text" in raw:
        raise CatalogError("catalog must not store source excerpts or source text")
    sources = catalog.get("sources")
    cards = catalog.get("action_cards")
    if not isinstance(sources, list) or not sources:
        raise CatalogError("sources must be a non-empty array")
    if not isinstance(cards, list) or not cards:
        raise CatalogError("action_cards must be a non-empty array")
    return catalog


def _source_index(catalog: dict[str, Any]) -> dict[str, dict[str, Any]]:
    index: dict[str, dict[str, Any]] = {}
    for position, raw_source in enumerate(catalog["sources"], start=1):
        source = _require_mapping(raw_source, f"sources[{position}]")
        source_id = _require_text(source.get("id"), f"sources[{position}].id")
        if source_id in index:
            raise CatalogError(f"duplicate source id: {source_id}")
        _require_text(source.get("path"), f"source {source_id}.path")
        role = _require_text(source.get("role"), f"source {source_id}.role")
        origin_class = _require_text(
            source.get("origin_class"), f"source {source_id}.origin_class"
        )
        if origin_class not in VALID_ORIGIN_CLASSES:
            raise CatalogError(
                f"source {source_id} has invalid origin_class {origin_class}"
            )
        if role == "positive_action_reference" and origin_class in POSITIVE_DISALLOWED_ORIGINS:
            raise CatalogError(
                f"source {source_id} origin {origin_class} cannot use role "
                "positive_action_reference"
            )
        scopes = source.get("scene_scope")
        if not isinstance(scopes, list) or not scopes or any(scope not in VALID_SCENES for scope in scopes):
            raise CatalogError(f"source {source_id} has invalid scene_scope")
        if role in EXCLUDED_ROLES and not _require_text(source.get("exclude_reason"), f"source {source_id}.exclude_reason"):
            raise CatalogError(f"source {source_id} needs an exclusion reason")
        index[source_id] = source
    for source_id, source in index.items():
        duplicate_of = source.get("duplicate_of")
        if duplicate_of and duplicate_of not in index:
            raise CatalogError(f"source {source_id} references unknown duplicate target {duplicate_of}")
    return index


def _validate_cards(catalog: dict[str, Any], source_index: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    cards: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    for position, raw_card in enumerate(catalog["action_cards"], start=1):
        card = _require_mapping(raw_card, f"action_cards[{position}]")
        card_id = _require_text(card.get("id"), f"action_cards[{position}].id")
        if card_id in seen_ids:
            raise CatalogError(f"duplicate action card id: {card_id}")
        seen_ids.add(card_id)
        scene = _require_text(card.get("scene"), f"card {card_id}.scene")
        if scene not in VALID_SCENES:
            raise CatalogError(f"card {card_id} has invalid scene {scene}")
        kind = _require_text(card.get("kind"), f"card {card_id}.kind")
        if kind not in VALID_CARD_KINDS:
            raise CatalogError(f"card {card_id} has invalid kind {kind}")
        required_anchor_roles = card.get("required_anchor_roles")
        if (
            not isinstance(required_anchor_roles, list)
            or not required_anchor_roles
            or any(not isinstance(role, str) or not role.strip() for role in required_anchor_roles)
            or len({role.strip() for role in required_anchor_roles}) != len(required_anchor_roles)
        ):
            raise CatalogError(f"card {card_id}.required_anchor_roles must be a non-empty unique string array")
        detector = card.get("detector")
        if kind == "negative_guard":
            if not isinstance(detector, dict):
                raise CatalogError(f"card {card_id}.detector must be an object for a negative guard")
            groups = detector.get("pattern_groups")
            minimum_groups = detector.get("minimum_groups")
            if not isinstance(groups, list) or not groups:
                raise CatalogError(f"card {card_id}.detector.pattern_groups must be non-empty")
            if not isinstance(minimum_groups, int) or not 1 <= minimum_groups <= len(groups):
                raise CatalogError(f"card {card_id}.detector.minimum_groups is invalid")
            seen_group_ids: set[str] = set()
            for group_position, raw_group in enumerate(groups, start=1):
                group = _require_mapping(raw_group, f"card {card_id}.detector.pattern_groups[{group_position}]")
                group_id = _require_text(group.get("id"), f"card {card_id} detector group id")
                pattern = _require_text(group.get("regex"), f"card {card_id} detector regex")
                minimum_occurrences = group.get("minimum_occurrences", 1)
                if group_id in seen_group_ids:
                    raise CatalogError(f"card {card_id} has duplicate detector group {group_id}")
                seen_group_ids.add(group_id)
                if not isinstance(minimum_occurrences, int) or minimum_occurrences < 1:
                    raise CatalogError(f"card {card_id} detector group {group_id} has invalid minimum_occurrences")
                try:
                    re.compile(pattern)
                except re.error as error:
                    raise CatalogError(f"card {card_id} detector group {group_id} has invalid regex: {error}") from error
        elif detector is not None:
            raise CatalogError(f"positive card {card_id} must not define a negative detector")
        _require_text(card.get("action"), f"card {card_id}.action")
        for field in ("requires", "forbids"):
            values = card.get(field)
            if not isinstance(values, list) or not values or any(not isinstance(value, str) or not value.strip() for value in values):
                raise CatalogError(f"card {card_id}.{field} must be a non-empty string array")
        refs = card.get("source_refs")
        if not isinstance(refs, list) or not refs:
            raise CatalogError(f"card {card_id}.source_refs must be non-empty")
        for ref_position, raw_ref in enumerate(refs, start=1):
            ref = _require_mapping(raw_ref, f"card {card_id}.source_refs[{ref_position}]")
            source_id = _require_text(ref.get("source_id"), f"card {card_id} source ref")
            if source_id not in source_index:
                raise CatalogError(f"card {card_id} references unknown source {source_id}")
            source = source_index[source_id]
            if source["role"] in EXCLUDED_ROLES:
                raise CatalogError(f"card {card_id} cannot use excluded source {source_id}")
            if source["role"] not in CARD_SOURCE_ROLES[kind]:
                raise CatalogError(
                    f"card {card_id} kind {kind} cannot use source role {source['role']} from {source_id}"
                )
            if scene != "ALL" and "ALL" not in source["scene_scope"] and scene not in source["scene_scope"]:
                raise CatalogError(f"card {card_id} scene {scene} conflicts with source {source_id}")
            start = ref.get("line_start")
            end = ref.get("line_end")
            if not isinstance(start, int) or not isinstance(end, int) or start < 1 or end < start:
                raise CatalogError(f"card {card_id} has invalid line range for {source_id}")
        cards.append(card)
    return cards


def _audited_source(source: dict[str, Any], referenced_ranges: list[tuple[int, int]]) -> tuple[dict[str, Any], list[str] | None]:
    """Read one source only when its role permits reading; never return prose to outputs."""
    source_id = source["id"]
    record: dict[str, Any] = {
        "id": source_id,
        "source_tier": source.get("source_tier", "unknown"),
        "origin_class": source["origin_class"],
        "scene_scope": source["scene_scope"],
        "role": source["role"],
        "path": source["path"],
        "referenced_ranges": [{"line_start": start, "line_end": end} for start, end in referenced_ranges],
    }
    if source["role"] in EXCLUDED_ROLES:
        record.update({"status": "EXCLUDED_CONFIG", "reason": source["exclude_reason"]})
        if source.get("duplicate_of"):
            record["duplicate_of"] = source["duplicate_of"]
        return record, None

    path = Path(source["path"])
    try:
        raw = path.read_bytes()
    except FileNotFoundError:
        record.update({"status": "MISSING", "reason": "source_file_not_found"})
        return record, None
    except OSError as error:
        record.update({"status": "UNREADABLE", "reason": type(error).__name__})
        return record, None
    text, encoding, issue = decode_source(raw)
    if text is None:
        record.update({"status": "SKIPPED_UNREADABLE", "reason": issue, "sha256": sha256_bytes(raw)})
        return record, None
    lines = text.splitlines()
    record.update({
        "status": "READABLE",
        "encoding": encoding,
        "sha256": sha256_bytes(raw),
        "line_count": len(lines),
    })
    return record, lines


def _range_audit(lines: list[str] | None, start: int, end: int) -> dict[str, Any]:
    result: dict[str, Any] = {"line_start": start, "line_end": end}
    if lines is None:
        result.update({"status": "SOURCE_UNAVAILABLE"})
        return result
    if end > len(lines):
        result.update({"status": "OUT_OF_RANGE", "source_line_count": len(lines)})
        return result
    selected = lines[start - 1:end]
    nonblank = [line for line in selected if line.strip()]
    if not nonblank:
        result.update({"status": "EMPTY_RANGE"})
        return result
    selected_bytes = "\n".join(selected).encode("utf-8")
    result.update({
        "status": "VERIFIED",
        "nonblank_line_count": len(nonblank),
        "content_sha256": sha256_bytes(selected_bytes),
    })
    return result


def build_action_profile(catalog_path: Path = DEFAULT_CATALOG) -> dict[str, Any]:
    """Return a deterministic profile; it contains source fingerprints, never prose."""
    catalog = load_catalog(catalog_path)
    source_index = _source_index(catalog)
    cards = _validate_cards(catalog, source_index)
    referenced_ranges: dict[str, list[tuple[int, int]]] = {source_id: [] for source_id in source_index}
    for card in cards:
        for ref in card["source_refs"]:
            referenced_ranges[ref["source_id"]].append((ref["line_start"], ref["line_end"]))

    source_records: dict[str, dict[str, Any]] = {}
    readable_lines: dict[str, list[str] | None] = {}
    for source_id, source in source_index.items():
        record, lines = _audited_source(source, referenced_ranges[source_id])
        source_records[source_id] = record
        readable_lines[source_id] = lines

    card_records: list[dict[str, Any]] = []
    for card in cards:
        ref_records = []
        usable = True
        for ref in card["source_refs"]:
            source_id = ref["source_id"]
            range_record = _range_audit(readable_lines[source_id], ref["line_start"], ref["line_end"])
            range_record["source_id"] = source_id
            ref_records.append(range_record)
            usable = usable and range_record["status"] == "VERIFIED"
        card_record = {
            "id": card["id"],
            "scene": card["scene"],
            "kind": card["kind"],
            "required_anchor_roles": card["required_anchor_roles"],
            "action": card["action"],
            "requires": card["requires"],
            "forbids": card["forbids"],
            "copy_limit": catalog["global_copy_limit"],
            "source_refs": ref_records,
            "status": "AVAILABLE" if usable else "UNAVAILABLE",
        }
        if card["kind"] == "negative_guard":
            card_record["detector"] = card["detector"]
        card_records.append(card_record)

    source_statuses = Counter(record["status"] for record in source_records.values())
    card_statuses = Counter(record["status"] for record in card_records)
    catalog_cards = {card["id"]: card for card in cards}
    scene_corpus_support: dict[str, dict[str, Any]] = {}
    for scene in sorted(VALID_SCENES - {"ALL"}):
        available_positive = [
            record
            for record in card_records
            if record["kind"] == "positive_action"
            and record["scene"] in {scene, "ALL"}
            and record["status"] == "AVAILABLE"
        ]
        source_ids = {
            ref["source_id"]
            for record in available_positive
            for ref in catalog_cards[record["id"]]["source_refs"]
        }
        independent_units = {
            source_index[source_id].get("composition_family_id", source_id)
            for source_id in source_ids
        }
        minimum = 2 if scene == "GENERAL" else 1
        scene_corpus_support[scene] = {
            "status": "SUPPORTED" if len(independent_units) >= minimum else "CORPUS_INSUFFICIENT",
            "minimum_independent_positive_sources": minimum,
            "independent_positive_source_count": len(independent_units),
            "available_positive_action_card_count": len(available_positive),
            "source_ids": sorted(source_ids),
            "positive_source_origin_classes": dict(sorted(Counter(
                source_index[source_id]["origin_class"] for source_id in source_ids
            ).items())),
            "origin_assurance": (
                "UNRESOLVED_PRESENT"
                if any(
                    source_index[source_id]["origin_class"] in {"MODEL_ORIGIN_UNRESOLVED", "UNKNOWN"}
                    for source_id in source_ids
                )
                else "DECLARED"
            ),
        }
    return {
        "schema_version": 2,
        "tool": "build_humanize_action_profile.py",
        "catalog_path": str(catalog_path),
        "purpose": catalog["purpose"],
        "global_copy_limit": catalog["global_copy_limit"],
        "status": "PASS" if not card_statuses.get("UNAVAILABLE") else "REVIEW",
        "sources": [source_records[source_id] for source_id in source_index],
        "action_cards": card_records,
        "summary": {
            "source_statuses": dict(sorted(source_statuses.items())),
            "origin_class_statuses": dict(sorted(Counter(
                source["origin_class"] for source in source_index.values()
            ).items())),
            "model_generated_positive_source_count": sum(
                1
                for source in source_index.values()
                if source["origin_class"] == "MODEL_GENERATED"
                and source["role"] == "positive_action_reference"
            ),
            "action_card_statuses": dict(sorted(card_statuses.items())),
            "available_action_cards": card_statuses.get("AVAILABLE", 0),
            "unavailable_action_cards": card_statuses.get("UNAVAILABLE", 0),
            "scene_corpus_support": scene_corpus_support,
            "source_text_exported": False,
        },
    }


def write_profile(profile: dict[str, Any], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(profile, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG, help="source-action catalog JSON")
    parser.add_argument("--output", type=Path, required=True, help="profile JSON to create or replace")
    parser.add_argument("--format", choices=("json", "text"), default="json")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    args = build_parser().parse_args(argv)
    try:
        profile = build_action_profile(args.catalog)
        write_profile(profile, args.output)
    except CatalogError as error:
        print(f"catalog error: {error}", file=sys.stderr)
        return 1
    if args.format == "text":
        summary = profile["summary"]
        print(
            f"{profile['status']}: {summary['available_action_cards']} available, "
            f"{summary['unavailable_action_cards']} unavailable; output={args.output}"
        )
    else:
        print(json.dumps({"status": profile["status"], "summary": profile["summary"], "output": str(args.output)}, ensure_ascii=False))
    return 0 if profile["status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
