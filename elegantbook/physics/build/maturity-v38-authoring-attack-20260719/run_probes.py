from __future__ import annotations

import copy
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SKILL = Path(r"C:\Users\Lenovo\.codex\skills\humanize-academic-chinese")
SCAFFOLD = SKILL / "scripts" / "scaffold_humanize_short_patch.py"
BUILDER = SKILL / "scripts" / "build_humanize_short_patch.py"
PYTHON = sys.executable


def write_json(name: str, value: object) -> Path:
    path = ROOT / name
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return path


def run(case_id: str, argv: list[str], expected: str) -> dict[str, object]:
    completed = subprocess.run(
        argv,
        cwd=ROOT,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=False,
        check=False,
    )
    stdout = completed.stdout.decode("utf-8", errors="strict")
    stderr = completed.stderr.decode("utf-8", errors="replace")
    parsed = None
    parse_error = None
    try:
        parsed = json.loads(stdout)
    except Exception as exc:
        parse_error = f"{type(exc).__name__}: {exc}"
    record = {
        "case_id": case_id,
        "expected": expected,
        "argv": argv,
        "returncode": completed.returncode,
        "stdout": stdout,
        "stderr": stderr,
        "stdout_json": parsed,
        "stdout_json_parse_error": parse_error,
        "traceback_seen": "Traceback (most recent call last)" in stdout + stderr,
        "skill_path_seen_in_output": str(SKILL) in stdout + stderr,
        "workspace_path_seen_in_output": str(ROOT) in stdout + stderr,
    }
    write_json(f"record-{case_id}.json", record)
    return record


def finalize_argv(source: str, authoring: str, output: str) -> list[str]:
    return [
        PYTHON,
        str(SCAFFOLD),
        "finalize",
        source,
        "--authoring",
        authoring,
        "--output",
        output,
        "--format",
        "json",
    ]


def create_argv(source: str, source_kind: str, output: str) -> list[str]:
    return [
        PYTHON,
        str(SCAFFOLD),
        "create",
        source,
        "--scene",
        "GENERAL",
        "--source-kind",
        source_kind,
        "--output",
        output,
        "--format",
        "json",
    ]


def build_argv(source: str, selection: str, output: str) -> list[str]:
    return [
        PYTHON,
        str(BUILDER),
        source,
        "--selection-spec",
        selection,
        "--output",
        output,
        "--format",
        "json",
    ]


def valid_authoring(scaffold: dict[str, object], *, inline: bool) -> dict[str, object]:
    value = copy.deepcopy(scaffold)
    spans = {span["span_id"]: span for span in value["spans"]}
    resolutions = value["lexical_resolutions"]
    finding_to_span: dict[str, str] = {}
    for span in spans.values():
        for finding_id in span["finding_ids"]:
            finding_to_span[finding_id] = span["span_id"]
    first = resolutions[0]
    first_span_id = finding_to_span[first["finding_id"]]
    value["hunks"] = [
        {
            "hunk_id": "H001",
            "span_id": first_span_id,
            "decision": "DELETE_STYLE_SHELL",
            "replacement": "",
            "reason": "删除不承载独立命题的重点提示壳。",
        }
    ]
    first.update(
        {
            "decision": "HUNK",
            "hunk_id": "H001",
            "reason": "该候选由 H001 精确处理。",
        }
    )
    for resolution in resolutions[1:]:
        resolution.update(
            {
                "decision": "KEEP",
                "hunk_id": None,
                "reason": "该位置保留具体学习动作或来源主张，需连续阅读复核。",
            }
        )
    value["selected_spans"] = []
    if inline:
        value["selected_spans"] = [
            {
                "selection_id": "S001",
                "span_id": first_span_id,
                "decision": "HUNK",
                "hunk_id": "H001",
                "reason": "调用方将该精确片段列入本次处理范围。",
            }
        ]
    return value


def structured_fail(record: dict[str, object]) -> bool:
    payload = record["stdout_json"]
    return (
        record["returncode"] == 1
        and isinstance(payload, dict)
        and payload.get("status") == "FAIL"
        and payload.get("exit_code") == 1
        and record["stderr"] == ""
        and not record["traceback_seen"]
    )


def main() -> int:
    records: list[dict[str, object]] = []

    baseline = json.loads((ROOT / "baseline.authoring.json").read_text(encoding="utf-8"))
    valid_doc = valid_authoring(baseline, inline=False)
    write_json("valid-document.authoring.json", valid_doc)
    records.append(
        run(
            "normal-document-finalize",
            finalize_argv("source.md", "valid-document.authoring.json", "valid-document.selection.json"),
            "FINALIZED/0",
        )
    )
    records.append(
        run(
            "normal-document-build",
            build_argv("source.md", "valid-document.selection.json", "valid-document.bundle.json"),
            "BUNDLED/0",
        )
    )

    records.append(
        run(
            "normal-inline-create",
            create_argv("source.md", "INLINE_SELECTION", "inline.authoring.json"),
            "PENDING/0",
        )
    )
    inline = json.loads((ROOT / "inline.authoring.json").read_text(encoding="utf-8"))
    valid_inline = valid_authoring(inline, inline=True)
    write_json("valid-inline.authoring.json", valid_inline)
    records.append(
        run(
            "normal-inline-finalize",
            finalize_argv("source.md", "valid-inline.authoring.json", "valid-inline.selection.json"),
            "FINALIZED/0",
        )
    )
    records.append(
        run(
            "normal-inline-build",
            build_argv("source.md", "valid-inline.selection.json", "valid-inline.bundle.json"),
            "BUNDLED/0",
        )
    )

    records.append(
        run(
            "pending-finalize",
            finalize_argv("source.md", "baseline.authoring.json", "pending.selection.json"),
            "structured FAIL/1",
        )
    )

    drift_source = ROOT / "source-drift.md"
    drift_source.write_bytes((ROOT / "source.md").read_bytes())
    records.append(
        run(
            "source-drift-create",
            create_argv("source-drift.md", "DOCUMENT", "source-drift.authoring.json"),
            "PENDING/0",
        )
    )
    drift_source.write_bytes(drift_source.read_bytes() + "\n新增一行。\n".encode("utf-8"))
    records.append(
        run(
            "source-drift-finalize",
            finalize_argv("source-drift.md", "source-drift.authoring.json", "source-drift.selection.json"),
            "structured FAIL/1",
        )
    )

    policy = copy.deepcopy(valid_doc)
    policy["policy_hashes"]["lexicon_sha256"] = "0" * 64
    write_json("policy-drift.authoring.json", policy)
    records.append(
        run(
            "policy-drift-finalize",
            finalize_argv("source.md", "policy-drift.authoring.json", "policy-drift.selection.json"),
            "structured FAIL/1",
        )
    )

    duplicate_span = copy.deepcopy(valid_doc)
    duplicate_span["spans"].append(copy.deepcopy(duplicate_span["spans"][0]))
    write_json("duplicate-span.authoring.json", duplicate_span)
    records.append(
        run(
            "duplicate-span-finalize",
            finalize_argv("source.md", "duplicate-span.authoring.json", "duplicate-span.selection.json"),
            "structured FAIL/1",
        )
    )

    missing_span = copy.deepcopy(valid_doc)
    missing_span["hunks"][0]["span_id"] = "Z999"
    write_json("missing-span-ref.authoring.json", missing_span)
    records.append(
        run(
            "missing-span-ref-finalize",
            finalize_argv("source.md", "missing-span-ref.authoring.json", "missing-span-ref.selection.json"),
            "structured FAIL/1",
        )
    )

    duplicate_hunk = copy.deepcopy(valid_doc)
    duplicate_hunk["hunks"].append(copy.deepcopy(duplicate_hunk["hunks"][0]))
    write_json("duplicate-hunk.authoring.json", duplicate_hunk)
    records.append(
        run(
            "duplicate-hunk-finalize",
            finalize_argv("source.md", "duplicate-hunk.authoring.json", "duplicate-hunk.selection.json"),
            "structured FAIL/1",
        )
    )

    missing_hunk = copy.deepcopy(valid_doc)
    missing_hunk["lexical_resolutions"][0]["hunk_id"] = "H999"
    write_json("missing-hunk-ref.authoring.json", missing_hunk)
    records.append(
        run(
            "missing-hunk-ref-finalize",
            finalize_argv("source.md", "missing-hunk-ref.authoring.json", "missing-hunk-ref.selection.json"),
            "structured FAIL/1",
        )
    )

    invalid_source = ROOT / "invalid-utf8.md"
    invalid_source.write_bytes(b"valid-prefix\n\xff\xfe\n")
    records.append(
        run(
            "invalid-utf8-source-create",
            create_argv("invalid-utf8.md", "DOCUMENT", "invalid-utf8-source.authoring.json"),
            "structured FAIL/1",
        )
    )

    invalid_authoring = ROOT / "invalid-utf8.authoring.json"
    invalid_authoring.write_bytes(b'{"schema_version":"broken",\xff}')
    records.append(
        run(
            "invalid-utf8-authoring-finalize",
            finalize_argv("source.md", "invalid-utf8.authoring.json", "invalid-utf8-authoring.selection.json"),
            "structured FAIL/1",
        )
    )

    existing_create = ROOT / "existing-create.json"
    existing_create.write_text("SENTINEL-CREATE\n", encoding="ascii")
    records.append(
        run(
            "existing-output-create",
            create_argv("source.md", "DOCUMENT", "existing-create.json"),
            "structured FAIL/1 and sentinel unchanged",
        )
    )

    existing_finalize = ROOT / "existing-finalize.json"
    existing_finalize.write_text("SENTINEL-FINALIZE\n", encoding="ascii")
    records.append(
        run(
            "existing-output-finalize",
            finalize_argv("source.md", "valid-document.authoring.json", "existing-finalize.json"),
            "structured FAIL/1 and sentinel unchanged",
        )
    )

    existing_build = ROOT / "existing-build.json"
    existing_build.write_text("SENTINEL-BUILD\n", encoding="ascii")
    records.append(
        run(
            "existing-output-build",
            build_argv("source.md", "valid-document.selection.json", "existing-build.json"),
            "structured FAIL/1 and sentinel unchanged",
        )
    )

    assertions = {
        "normal_document_finalize": records[0]["returncode"] == 0
        and records[0]["stdout_json"].get("status") == "FINALIZED",
        "normal_document_build": records[1]["returncode"] == 0
        and records[1]["stdout_json"].get("status") == "BUNDLED",
        "normal_inline_create": records[2]["returncode"] == 0
        and records[2]["stdout_json"].get("status") == "PENDING",
        "normal_inline_finalize": records[3]["returncode"] == 0
        and records[3]["stdout_json"].get("status") == "FINALIZED",
        "normal_inline_build": records[4]["returncode"] == 0
        and records[4]["stdout_json"].get("status") == "BUNDLED",
        "all_expected_failures_structured": all(structured_fail(item) for item in records[5:] if item["case_id"] != "source-drift-create"),
        "create_sentinel_unchanged": existing_create.read_text(encoding="ascii") == "SENTINEL-CREATE\n",
        "finalize_sentinel_unchanged": existing_finalize.read_text(encoding="ascii") == "SENTINEL-FINALIZE\n",
        "build_sentinel_unchanged": existing_build.read_text(encoding="ascii") == "SENTINEL-BUILD\n",
        "no_tracebacks": not any(item["traceback_seen"] for item in records),
        "no_absolute_paths_in_output": not any(
            item["skill_path_seen_in_output"] or item["workspace_path_seen_in_output"]
            for item in records
        ),
    }
    summary = {
        "assertions": assertions,
        "records": [
            {
                "case_id": item["case_id"],
                "returncode": item["returncode"],
                "status": item["stdout_json"].get("status") if isinstance(item["stdout_json"], dict) else None,
                "exit_code": item["stdout_json"].get("exit_code") if isinstance(item["stdout_json"], dict) else None,
                "error": item["stdout_json"].get("error") if isinstance(item["stdout_json"], dict) else None,
                "traceback_seen": item["traceback_seen"],
                "path_seen": item["skill_path_seen_in_output"] or item["workspace_path_seen_in_output"],
            }
            for item in records
        ],
    }
    write_json("summary.json", summary)
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))
    return 0 if all(assertions.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
