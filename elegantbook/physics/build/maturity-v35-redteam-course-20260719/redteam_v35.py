from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
BASE = ROOT / "baseline"
VERIFY = Path(
    r"C:\Users\Lenovo\.codex\skills\humanize-academic-chinese\scripts\verify_humanize_short_patch.py"
)


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical(value: object) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: dict) -> None:
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def attack_dir(name: str) -> Path:
    path = ROOT / name
    if path.exists() or path.is_symlink():
        if path.is_dir() and not path.is_symlink():
            shutil.rmtree(path)
        else:
            path.unlink()
    shutil.copytree(BASE, path)
    return path


def reseal_manifest(path: Path) -> None:
    manifest_path = path / "evidence-manifest.json"
    manifest = load_json(manifest_path)
    for item in manifest["artifacts"]:
        raw = (path / item["path"]).read_bytes()
        item["size"] = len(raw)
        item["sha256"] = sha256(raw)
    unsigned = dict(manifest)
    unsigned.pop("manifest_sha256", None)
    manifest["manifest_sha256"] = sha256(canonical(unsigned))
    write_json(manifest_path, manifest)


def reseal_manifest_self_only(path: Path) -> None:
    manifest_path = path / "evidence-manifest.json"
    manifest = load_json(manifest_path)
    unsigned = dict(manifest)
    unsigned.pop("manifest_sha256", None)
    manifest["manifest_sha256"] = sha256(canonical(unsigned))
    write_json(manifest_path, manifest)


def run_verify(path: Path) -> dict:
    process = subprocess.run(
        [sys.executable, str(VERIFY), str(path), "--format", "json"],
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    payload = None
    try:
        payload = json.loads(process.stdout.decode("utf-8-sig"))
    except Exception:
        payload = {"raw_stdout": process.stdout.decode("utf-8", errors="replace")}
    return {
        "process_exit": process.returncode,
        "status": payload.get("status"),
        "reported_exit": payload.get("exit_code"),
        "error": payload.get("error", ""),
        "stderr": process.stderr.decode("utf-8", errors="replace"),
    }


def main() -> int:
    results: dict[str, dict] = {}

    path = attack_dir("attack-candidate-stale-manifest")
    candidate = next(path.glob("candidate.review.*"))
    candidate.write_bytes(candidate.read_bytes() + b"tamper")
    results["candidate_stale_manifest"] = run_verify(path)

    path = attack_dir("attack-candidate-resealed-manifest")
    candidate = next(path.glob("candidate.review.*"))
    candidate.write_bytes(candidate.read_bytes() + b"tamper")
    reseal_manifest(path)
    results["candidate_resealed_manifest"] = run_verify(path)

    path = attack_dir("attack-result-stale-manifest")
    result_path = path / "result.json"
    result = load_json(result_path)
    result["humanize_quality_claim_allowed"] = True
    write_json(result_path, result)
    results["result_stale_manifest"] = run_verify(path)

    path = attack_dir("attack-result-required-claim-resealed")
    result_path = path / "result.json"
    result = load_json(result_path)
    result["humanize_quality_claim_allowed"] = True
    result["delivery_gate_status"] = "PASS"
    write_json(result_path, result)
    reseal_manifest(path)
    results["result_required_claim_resealed"] = run_verify(path)

    path = attack_dir("attack-result-extra-quality-claims-resealed")
    result_path = path / "result.json"
    result = load_json(result_path)
    result["paired_quality_clearance_granted"] = True
    result["academic_correctness"] = "PASS"
    result["quality_status"] = "PASS"
    write_json(result_path, result)
    reseal_manifest(path)
    results["result_extra_quality_claims_resealed"] = run_verify(path)

    path = attack_dir("attack-validation-stale-manifest")
    validation_path = path / "validation.json"
    validation = load_json(validation_path)
    validation["evidence"]["after_sha256"] = "0" * 64
    write_json(validation_path, validation)
    results["validation_stale_manifest"] = run_verify(path)

    path = attack_dir("attack-validation-evidence-resealed")
    validation_path = path / "validation.json"
    validation = load_json(validation_path)
    validation["evidence"]["before_sha256"] = "1" * 64
    validation["evidence"]["after_sha256"] = "2" * 64
    write_json(validation_path, validation)
    reseal_manifest(path)
    results["validation_evidence_resealed"] = run_verify(path)

    path = attack_dir("attack-validation-quality-claims-resealed")
    validation_path = path / "validation.json"
    result_path = path / "result.json"
    validation = load_json(validation_path)
    result = load_json(result_path)
    validation["paired_quality_review_status"] = "PASS"
    validation["paired_quality_clearance_granted"] = True
    result["paired_quality_review_status"] = "PASS"
    result["paired_quality_clearance_granted"] = True
    write_json(validation_path, validation)
    write_json(result_path, result)
    reseal_manifest(path)
    results["validation_quality_claims_resealed"] = run_verify(path)

    path = attack_dir("attack-extra-file")
    (path / "extra.txt").write_text("extra", encoding="utf-8")
    results["extra_file"] = run_verify(path)

    path = attack_dir("attack-extra-file-listed-resealed")
    extra = path / "extra.txt"
    extra.write_text("extra", encoding="utf-8")
    manifest_path = path / "evidence-manifest.json"
    manifest = load_json(manifest_path)
    manifest["artifacts"].append(
        {"path": "extra.txt", "size": 5, "sha256": sha256(b"extra")}
    )
    write_json(manifest_path, manifest)
    reseal_manifest_self_only(path)
    results["extra_file_listed_resealed"] = run_verify(path)

    path = attack_dir("attack-manifest-bad-self-hash")
    manifest_path = path / "evidence-manifest.json"
    manifest = load_json(manifest_path)
    manifest["manifest_sha256"] = "f" * 64
    write_json(manifest_path, manifest)
    results["manifest_bad_self_hash"] = run_verify(path)

    path = attack_dir("attack-manifest-parent-path-resealed")
    manifest_path = path / "evidence-manifest.json"
    manifest = load_json(manifest_path)
    manifest["artifacts"][0]["path"] = "../candidate.review.tex"
    write_json(manifest_path, manifest)
    reseal_manifest_self_only(path)
    results["manifest_parent_path_resealed"] = run_verify(path)

    path = attack_dir("attack-hardlink-artifact")
    candidate = next(path.glob("candidate.review.*"))
    target = ROOT / "hardlink-target.bin"
    target.write_bytes(candidate.read_bytes())
    candidate.unlink()
    hardlink_status = "CREATED"
    try:
        os.link(target, candidate)
    except OSError as error:
        hardlink_status = f"SKIPPED:{type(error).__name__}:{error}"
    results["hardlink_artifact"] = (
        run_verify(path)
        if hardlink_status == "CREATED"
        else {"process_exit": None, "status": "SKIPPED", "error": hardlink_status}
    )
    results["hardlink_artifact"]["setup"] = hardlink_status

    symlink = ROOT / "attack-symlink-root"
    if symlink.exists() or symlink.is_symlink():
        if symlink.is_dir() and not symlink.is_symlink():
            shutil.rmtree(symlink)
        else:
            symlink.unlink()
    link_status = "CREATED"
    try:
        os.symlink(BASE, symlink, target_is_directory=True)
    except OSError as error:
        link_status = f"SKIPPED:{type(error).__name__}:{error}"
    results["reparse_or_symlink_root"] = (
        run_verify(symlink)
        if link_status == "CREATED"
        else {"process_exit": None, "status": "SKIPPED", "error": link_status}
    )
    results["reparse_or_symlink_root"]["setup"] = link_status

    write_json(ROOT / "attack-results.json", results)
    for name, result in results.items():
        print(
            f"{name}: process_exit={result.get('process_exit')} "
            f"status={result.get('status')} error={result.get('error', '')}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
