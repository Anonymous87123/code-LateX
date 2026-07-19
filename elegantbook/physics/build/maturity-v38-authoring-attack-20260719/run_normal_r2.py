from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SCRIPTS = Path(r"C:\Users\Lenovo\.codex\skills\humanize-academic-chinese\scripts")
PYTHON = sys.executable


def save_json(name: str, value: object) -> None:
    (ROOT / name).write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def run(case_id: str, argv: list[str]) -> dict[str, object]:
    proc = subprocess.run(
        argv,
        cwd=ROOT,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=False,
        check=False,
    )
    stdout = proc.stdout.decode("utf-8", errors="strict")
    record = {
        "case_id": case_id,
        "argv": argv,
        "returncode": proc.returncode,
        "stdout": stdout,
        "stdout_json": json.loads(stdout),
        "stderr": proc.stderr.decode("utf-8", errors="replace"),
        "traceback_seen": b"Traceback (most recent call last)" in proc.stdout + proc.stderr,
    }
    save_json(f"record-r2-{case_id}.json", record)
    return record


def corrected(source_name: str, target_name: str) -> None:
    value = json.loads((ROOT / source_name).read_text(encoding="utf-8"))
    value["lexical_resolutions"][0]["reason"] = None
    save_json(target_name, value)


def main() -> int:
    corrected("valid-document.authoring.json", "valid-document-r2.authoring.json")
    corrected("valid-inline.authoring.json", "valid-inline-r2.authoring.json")
    scaffold = str(SCRIPTS / "scaffold_humanize_short_patch.py")
    builder = str(SCRIPTS / "build_humanize_short_patch.py")
    records = [
        run(
            "normal-document-finalize",
            [PYTHON, scaffold, "finalize", "source.md", "--authoring", "valid-document-r2.authoring.json", "--output", "valid-document-r2.selection.json", "--format", "json"],
        ),
        run(
            "normal-document-build",
            [PYTHON, builder, "source.md", "--selection-spec", "valid-document-r2.selection.json", "--output", "valid-document-r2.bundle.json", "--format", "json"],
        ),
        run(
            "normal-inline-finalize",
            [PYTHON, scaffold, "finalize", "source.md", "--authoring", "valid-inline-r2.authoring.json", "--output", "valid-inline-r2.selection.json", "--format", "json"],
        ),
        run(
            "normal-inline-build",
            [PYTHON, builder, "source.md", "--selection-spec", "valid-inline-r2.selection.json", "--output", "valid-inline-r2.bundle.json", "--format", "json"],
        ),
    ]
    summary = {
        "all_passed": all(
            item["returncode"] == 0
            and item["stderr"] == ""
            and not item["traceback_seen"]
            and item["stdout_json"].get("status") in {"FINALIZED", "BUNDLED"}
            for item in records
        ),
        "records": [
            {
                "case_id": item["case_id"],
                "returncode": item["returncode"],
                "status": item["stdout_json"].get("status"),
                "schema_version": item["stdout_json"].get("schema_version"),
            }
            for item in records
        ],
    }
    save_json("summary-r2.json", summary)
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))
    return 0 if summary["all_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
