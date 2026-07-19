#!/usr/bin/env python3
"""Create fail-closed rewrite bundle scaffolds from a prepared long-document run.

The generated files contain frozen bindings and the masked text, but are not
completion artifacts.  ``PENDING`` is intentionally unsupported by finalize;
the caller must choose ``REWRITE`` or ``NO_CHANGE`` and supply the corresponding
body/reason before the normal gates can run.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any


HEX64 = re.compile(r"^[0-9a-f]{64}$")
UNIT_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]{0,127}$")
ALLOWED_DECISIONS = {"REWRITE", "NO_CHANGE"}
SCAFFOLD_SCHEMA = "humanize-rewrite-scaffold/v2"


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _load_json(path: Path) -> dict[str, Any]:
    raw = path.read_bytes()
    value = json.loads(raw.decode("utf-8-sig"))
    if not isinstance(value, dict):
        raise ValueError(f"chunk is not an object: {path.name}")
    return value


def _pending_chunks(run_dir: Path) -> list[dict[str, Any]]:
    chunks_dir = run_dir / "chunks"
    if not chunks_dir.is_dir():
        raise ValueError("run_dir/chunks is missing")
    chunks: list[dict[str, Any]] = []
    for path in sorted(chunks_dir.glob("*.json"), key=lambda item: item.name.casefold()):
        chunk = _load_json(path)
        if chunk.get("status") != "PENDING":
            continue
        unit_id = chunk.get("unit_id")
        binding = chunk.get("chunk_binding_sha256")
        voice = chunk.get("voice_profile_sha256")
        masked = chunk.get("masked_text")
        if not isinstance(unit_id, str) or not UNIT_ID.fullmatch(unit_id):
            raise ValueError(f"pending chunk missing unit_id: {path.name}")
        if not isinstance(binding, str) or not HEX64.fullmatch(binding):
            raise ValueError(f"pending chunk has invalid chunk binding: {path.name}")
        if not isinstance(voice, str) or not HEX64.fullmatch(voice):
            raise ValueError(f"pending chunk has invalid voice binding: {path.name}")
        if not isinstance(masked, str):
            raise ValueError(f"pending chunk has invalid masked_text: {path.name}")
        chunk["_chunk_path"] = str(path)
        chunks.append(chunk)
    return chunks


def _bundle(chunk: dict[str, Any], decision: str) -> dict[str, Any]:
    common: dict[str, Any] = {
        "unit_id": chunk["unit_id"],
        "chunk_binding_sha256": chunk["chunk_binding_sha256"],
        "decision": decision,
        "voice_profile_sha256": chunk["voice_profile_sha256"],
        "keep_reasons": {},
    }
    if decision == "REWRITE":
        common["masked_text"] = chunk["masked_text"]
    else:
        # Deliberately invalid until the caller replaces this marker with a
        # concrete >=4-Chinese-character NO_CHANGE reason.
        common["reason"] = "TODO"
    return common


def _normalize_decisions(
    chunks: list[dict[str, Any]],
    decision: str | None,
    decision_map: dict[str, str] | None,
) -> dict[str, str]:
    if (decision is None) == (decision_map is None):
        raise ValueError("provide exactly one of decision or decision_map")
    unit_ids = {str(chunk["unit_id"]) for chunk in chunks}
    if decision is not None:
        normalized = decision.upper()
        if normalized not in ALLOWED_DECISIONS:
            raise ValueError("decision must be REWRITE or NO_CHANGE")
        return {unit_id: normalized for unit_id in unit_ids}
    assert decision_map is not None
    if set(decision_map) != unit_ids:
        raise ValueError("decision_map must contain exactly every pending unit_id")
    normalized_map: dict[str, str] = {}
    for unit_id, value in decision_map.items():
        if not isinstance(unit_id, str) or not UNIT_ID.fullmatch(unit_id):
            raise ValueError("decision_map contains invalid unit_id")
        if not isinstance(value, str) or value.upper() not in ALLOWED_DECISIONS:
            raise ValueError("decision_map values must be REWRITE or NO_CHANGE")
        normalized_map[unit_id] = value.upper()
    return normalized_map


def scaffold(
    run_dir: Path,
    output: Path,
    decision: str | None = None,
    decision_map: dict[str, str] | None = None,
) -> dict[str, Any]:
    run_dir = run_dir.resolve()
    output = output.resolve()
    if not run_dir.is_dir():
        raise ValueError("run_dir must be a directory")
    if output.exists():
        if not output.is_dir() or any(output.iterdir()):
            raise ValueError("output must be a new empty directory")
    else:
        output.mkdir(parents=True)
    chunks = _pending_chunks(run_dir)
    decisions = _normalize_decisions(chunks, decision, decision_map)
    # Unit IDs become output filenames. Reject path syntax and Windows
    # case-insensitive collisions before writing anything to the destination.
    seen_unit_ids: set[str] = set()
    for chunk in chunks:
        unit_id = str(chunk["unit_id"])
        collision_key = unit_id.casefold()
        if collision_key in seen_unit_ids:
            raise ValueError(f"duplicate pending unit_id: {unit_id}")
        seen_unit_ids.add(collision_key)
    records: list[dict[str, Any]] = []
    for chunk in chunks:
        path = output / f"{chunk['unit_id']}.json"
        unit_decision = decisions[chunk["unit_id"]]
        payload = _bundle(chunk, unit_decision)
        encoded = (json.dumps(payload, ensure_ascii=False, indent=2, separators=(",", ": ")) + "\n").encode("utf-8")
        path.write_bytes(encoded)
        records.append(
            {
                "unit_id": chunk["unit_id"],
                "path": path.name,
                "decision": unit_decision,
                "template_sha256": sha256(encoded),
            }
        )
    metadata = {
        "schema_version": SCAFFOLD_SCHEMA,
        "run_dir_name": run_dir.name,
        "decision": (
            "EMPTY"
            if not decisions
            else next(iter(set(decisions.values())))
            if len(set(decisions.values())) == 1
            else "MIXED"
        ),
        "decision_map": dict(sorted(decisions.items())),
        "pending_units_total": len(chunks),
        "templates_total": len(records),
        "completion_claim_allowed": False,
        "requires_manual_completion": True,
        "records": records,
    }
    (output / "scaffold_metadata.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return metadata


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="为 prepare 长文运行生成带冻结 binding 的安全改写包骨架；骨架不是完成态。"
    )
    parser.add_argument("--run-dir", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    decision_group = parser.add_mutually_exclusive_group(required=True)
    decision_group.add_argument("--decision", choices=sorted(ALLOWED_DECISIONS))
    decision_group.add_argument(
        "--decision-map",
        type=Path,
        help="UTF-8 JSON object mapping every pending unit_id to REWRITE or NO_CHANGE",
    )
    parser.add_argument("--format", choices=("json", "text"), default="text")
    args = parser.parse_args(argv)
    try:
        decision_map = None
        if args.decision_map is not None:
            parsed = json.loads(args.decision_map.read_bytes().decode("utf-8-sig"))
            if not isinstance(parsed, dict):
                raise ValueError("decision_map JSON must be an object")
            decision_map = parsed
        result = scaffold(args.run_dir, args.output, args.decision, decision_map)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        payload = {
            "schema_version": SCAFFOLD_SCHEMA,
            "status": "FAIL",
            "error": str(error),
            "completion_claim_allowed": False,
        }
        print(json.dumps(payload, ensure_ascii=False) if args.format == "json" else f"FAIL: {error}")
        return 1
    result["status"] = "SCAFFOLDED"
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"SCAFFOLDED decision={result['decision']} templates={result['templates_total']}")
        print("completion_claim_allowed=false; edit each template and run finalize")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
