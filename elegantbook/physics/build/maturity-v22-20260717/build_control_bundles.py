#!/usr/bin/env python3
"""Build a full-coverage control bundle set for the v22 real-material gate trial."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--special-bundle", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--validation-dir", type=Path)
    args = parser.parse_args()

    args.output.mkdir(parents=True, exist_ok=False)
    special = json.loads(args.special_bundle.read_text(encoding="utf-8"))
    special_unit = special["unit_id"]
    pending = 0
    for chunk_path in sorted((args.run_dir / "chunks").glob("*.json")):
        chunk = json.loads(chunk_path.read_text(encoding="utf-8"))
        if chunk.get("status") != "PENDING":
            continue
        pending += 1
        unit_id = chunk["unit_id"]
        if unit_id == special_unit:
            payload = special
        else:
            keep_reasons = {}
            if args.validation_dir is not None:
                validation_path = args.validation_dir / f"{unit_id}.validation.json"
                validation = json.loads(validation_path.read_text(encoding="utf-8"))
                keep_reasons = {
                    f"{item['signal_id']}@sha256:{item['finding_hash']}":
                    "原文既有表达；本工件只验证控制链，不据此作质量裁决"
                    for item in validation.get("unexplained_high_findings", [])
                }
            payload = {
                "unit_id": unit_id,
                "chunk_binding_sha256": chunk["chunk_binding_sha256"],
                "decision": "NO_CHANGE",
                "voice_profile_sha256": chunk["voice_profile_sha256"],
                "reason": "该单元保持现有结构；本工件只验证发布控制链",
                "keep_reasons": keep_reasons,
            }
        (args.output / f"{unit_id}.json").write_text(
            json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    print(json.dumps({"pending_units": pending, "bundles": len(list(args.output.glob('*.json')))}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
