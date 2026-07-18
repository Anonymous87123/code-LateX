#!/usr/bin/env python3
"""Capture one fresh Codex generation trial without overstating isolation.

This runner owns the output, context capture, transcript, receipt, and run record.
It deliberately caps the local Windows ``codex exec -s read-only`` path at E2:
read-only execution is observable, but filesystem blindness is not.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence


SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent
AUDITOR_PATH = SCRIPT_DIR / "audit_humanize_generation_qualification.py"
PUBLIC_SCHEMA = "humanize-generation-public-fixture/v1"
PUBLIC_SEAL_SCHEMA = "humanize-generation-public-seal/v1"
PUBLIC_CONTEXT_SCHEMA = "humanize-generation-public-context/v1"
CONTEXT_SCHEMA = "humanize-generation-runner-context/v1"
RECEIPT_SCHEMA = "humanize-generation-runner-receipt/v1"
RUN_SEAL_SCHEMA = "humanize-generation-run-seal/v1"
RUNNER_VERSION = "1.0.0"
SAFE_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]{0,95}$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
ATOM_LEAK_RE = re.compile(
    r"\b(?:MODE|INT|OUT|DEC|ROUTE|VOICE|ROLE|PATH|LONG)-\d{2}(?:/[A-Za-z0-9_.-]+)?\b"
)
FORBIDDEN_PUBLIC_PARTS = {"oracle", "oracles", "gold", "expected", "assertion", "assertions"}
PUBLIC_FILENAMES = {"public-manifest.json", "public-seal.json"}
ALLOWED_INPUT_SUFFIXES = {".md", ".tex", ".txt"}
PARAM_VALUES = {
    "mode": {"DIAGNOSE", "REWRITE", "DRAFT"},
    "scene": {"AUTO", "COURSE", "MODELING", "RESEARCH", "GENERAL"},
    "intensity": {"LIGHT", "BALANCED", "STRUCTURAL"},
    "output": {"CLEAN", "ANNOTATED", "PATCH"},
    "report_context": {"NONE", "REPORT_INFORMED"},
}
LOCK_FIELDS = {"scope", "title_lock", "structure_lock"}
PUBLIC_CONTEXT_FIELDS = {
    "schema_version",
    *PARAM_VALUES,
    *LOCK_FIELDS,
    "task_options",
}
TASK_OPTION_FIELDS = {
    "operation",
    "locked_literals",
    "summary_max_sentences",
    "required_output_format",
    "preserve_three_groups",
    "vary_paragraph_rhythm_without_forced_asymmetry",
    "preserve_numbers_math",
}
INHERITED_ENV_NAMES = {
    "ALLUSERSPROFILE",
    "APPDATA",
    "COMSPEC",
    "HOMEDRIVE",
    "HOMEPATH",
    "LOCALAPPDATA",
    "NUMBER_OF_PROCESSORS",
    "OS",
    "PATH",
    "PATHEXT",
    "PROCESSOR_ARCHITECTURE",
    "PROGRAMDATA",
    "PROGRAMFILES",
    "PROGRAMFILES(X86)",
    "SYSTEMDRIVE",
    "SYSTEMROOT",
    "TEMP",
    "TMP",
    "USERPROFILE",
    "WINDIR",
}


class RunnerError(ValueError):
    """Raised for an invalid fixture or an infrastructure-invalid run."""


@dataclass(frozen=True)
class PublicCase:
    case_id: str
    root: Path
    input_path: Path
    prompt_path: Path
    public_context_path: Path
    manifest_path: Path
    seal_path: Path
    params: Mapping[str, Any]
    locks: Mapping[str, Any]
    task_options: Mapping[str, Any]
    manifest_sha256: str
    seal_sha256: str


@dataclass(frozen=True)
class Invocation:
    command: tuple[str, ...]
    pid: int
    returncode: int
    stdout: bytes
    stderr: bytes
    timed_out: bool
    started_at: str
    ended_at: str


def _canonical_json(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")


def _sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _file_sha256(path: Path) -> str:
    return _sha256(path.read_bytes())


def _strict_json(raw: bytes, label: str) -> Any:
    def reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise RunnerError(f"{label} contains duplicate JSON key: {key}")
            result[key] = value
        return result

    try:
        return json.loads(raw.decode("utf-8-sig"), object_pairs_hook=reject_duplicates)
    except (UnicodeError, json.JSONDecodeError) as error:
        raise RunnerError(f"{label} is not strict UTF-8 JSON: {error}") from error


def _require_object(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise RunnerError(f"{label} must be an object")
    return value


def _require_exact_fields(value: Mapping[str, Any], allowed: set[str], label: str) -> None:
    unknown = sorted(set(value) - allowed)
    missing = sorted(allowed - set(value))
    if unknown or missing:
        details = []
        if unknown:
            details.append("unknown=" + ",".join(unknown))
        if missing:
            details.append("missing=" + ",".join(missing))
        raise RunnerError(f"{label} fields are invalid ({'; '.join(details)})")


def _safe_relative(root: Path, value: Any, label: str) -> Path:
    if not isinstance(value, str) or not value.strip() or "\x00" in value:
        raise RunnerError(f"{label} must be a non-empty relative path")
    supplied = Path(value)
    if supplied.is_absolute() or supplied.drive:
        raise RunnerError(f"{label} must stay inside the public fixture")
    root_resolved = root.resolve(strict=True)
    try:
        resolved = (root_resolved / supplied).resolve(strict=True)
        resolved.relative_to(root_resolved)
    except (OSError, ValueError) as error:
        raise RunnerError(f"{label} escapes or is unreadable: {error}") from error
    return resolved


def _descriptor(root: Path, value: Any, label: str) -> Path:
    descriptor = _require_object(value, label)
    _require_exact_fields(descriptor, {"path", "sha256"}, label)
    path = _safe_relative(root, descriptor["path"], f"{label}.path")
    supplied_hash = descriptor["sha256"]
    if not isinstance(supplied_hash, str) or not SHA256_RE.fullmatch(supplied_hash):
        raise RunnerError(f"{label}.sha256 must be a lowercase SHA-256")
    if _file_sha256(path) != supplied_hash:
        raise RunnerError(f"{label} hash does not match sealed bytes")
    return path


def _public_leak_check(case_id: str, paths: Sequence[Path]) -> None:
    for path in paths:
        if path.stem.lower() in FORBIDDEN_PUBLIC_PARTS:
            raise RunnerError(f"public fixture path exposes oracle vocabulary: {path.name}")
        try:
            text = path.read_text(encoding="utf-8-sig")
        except UnicodeError as error:
            raise RunnerError(f"public fixture is not UTF-8: {path.name}: {error}") from error
        match = ATOM_LEAK_RE.search(text)
        if match:
            raise RunnerError(
                f"public fixture {case_id} leaks qualification atom ID: {match.group(0)}"
            )


def load_public_case(case_root: Path) -> PublicCase:
    root = case_root.resolve(strict=True)
    if not root.is_dir():
        raise RunnerError("public fixture root must be a directory")
    manifest_path = root / "public-manifest.json"
    seal_path = root / "public-seal.json"
    manifest = _require_object(
        _strict_json(manifest_path.read_bytes(), "public manifest"), "public manifest"
    )
    _require_exact_fields(
        manifest,
        {"schema_version", "case_id", "input", "prompt", "public_context"},
        "public manifest",
    )
    if manifest["schema_version"] != PUBLIC_SCHEMA:
        raise RunnerError(f"public manifest schema must be {PUBLIC_SCHEMA}")
    case_id = manifest["case_id"]
    if not isinstance(case_id, str) or not SAFE_ID_RE.fullmatch(case_id):
        raise RunnerError("public manifest case_id is unsafe")
    input_path = _descriptor(root, manifest["input"], "public manifest.input")
    prompt_path = _descriptor(root, manifest["prompt"], "public manifest.prompt")
    public_context_path = _descriptor(
        root, manifest["public_context"], "public manifest.public_context"
    )
    if input_path.suffix.lower() not in ALLOWED_INPUT_SUFFIXES:
        raise RunnerError("public input must be .md, .tex, or .txt")
    if prompt_path.name != "prompt.txt":
        raise RunnerError("public prompt path must be prompt.txt")
    if public_context_path.name != "public-context.json":
        raise RunnerError("public context path must be public-context.json")
    public_context = _require_object(
        _strict_json(public_context_path.read_bytes(), "public context"),
        "public context",
    )
    _require_exact_fields(public_context, PUBLIC_CONTEXT_FIELDS, "public context")
    if public_context["schema_version"] != PUBLIC_CONTEXT_SCHEMA:
        raise RunnerError(f"public context schema must be {PUBLIC_CONTEXT_SCHEMA}")
    params = {key: public_context[key] for key in PARAM_VALUES}
    for key, allowed in PARAM_VALUES.items():
        if params[key] not in allowed:
            raise RunnerError(f"public context.{key} is invalid")
    locks = {key: public_context[key] for key in LOCK_FIELDS}
    if locks["scope"] not in {"selection", "section", "document"}:
        raise RunnerError("public context.scope is invalid")
    if type(locks["title_lock"]) is not bool or type(locks["structure_lock"]) is not bool:
        raise RunnerError("public context lock flags must be booleans")
    task_options = _require_object(public_context["task_options"], "public context.task_options")
    extra_task_options = sorted(set(task_options) - TASK_OPTION_FIELDS)
    if extra_task_options:
        raise RunnerError(
            "public context.task_options has unknown fields: " + ", ".join(extra_task_options)
        )
    operation = task_options.get("operation")
    if operation is not None and operation not in {"PREPARE_LONG_DOCUMENT"}:
        raise RunnerError("public context.task_options.operation is invalid")
    required_output = task_options.get("required_output_format")
    if required_output is not None and required_output not in {"JSON_INCLUDE_MANIFEST"}:
        raise RunnerError("public context.task_options.required_output_format is invalid")
    summary_max = task_options.get("summary_max_sentences")
    if (
        summary_max is not None
        and (
            not isinstance(summary_max, int)
            or isinstance(summary_max, bool)
            or summary_max < 0
            or summary_max > 5
        )
    ):
        raise RunnerError("public context.task_options.summary_max_sentences is invalid")
    for key in (
        "preserve_three_groups",
        "vary_paragraph_rhythm_without_forced_asymmetry",
        "preserve_numbers_math",
    ):
        if key in task_options and type(task_options[key]) is not bool:
            raise RunnerError(f"public context.task_options.{key} must be boolean")
    locked_literals = task_options.get("locked_literals", [])
    if (
        not isinstance(locked_literals, list)
        or not all(isinstance(item, str) and item for item in locked_literals)
        or len(locked_literals) > 32
    ):
        raise RunnerError("public context.task_options.locked_literals is invalid")
    seal = _require_object(_strict_json(seal_path.read_bytes(), "public seal"), "public seal")
    _require_exact_fields(
        seal,
        {"schema_version", "case_id", "public_manifest_sha256", "artifact_sha256"},
        "public seal",
    )
    if seal["schema_version"] != PUBLIC_SEAL_SCHEMA:
        raise RunnerError(f"public seal schema must be {PUBLIC_SEAL_SCHEMA}")
    if seal["case_id"] != case_id:
        raise RunnerError("public seal case_id does not match manifest")
    manifest_hash = _file_sha256(manifest_path)
    if seal["public_manifest_sha256"] != manifest_hash:
        raise RunnerError("public seal does not bind the manifest")
    expected_artifacts = {
        "input": _file_sha256(input_path),
        "prompt": _file_sha256(prompt_path),
        "public_context": _file_sha256(public_context_path),
    }
    if seal["artifact_sha256"] != expected_artifacts:
        raise RunnerError("public seal artifact hashes do not match manifest roles")
    permitted = PUBLIC_FILENAMES | {
        input_path.name,
        prompt_path.name,
        public_context_path.name,
    }
    extras = sorted(
        item.name
        for item in root.iterdir()
        if item.name not in permitted
    )
    if extras:
        raise RunnerError("public fixture contains unsealed extra entries: " + ", ".join(extras))
    _public_leak_check(case_id, [input_path, prompt_path, public_context_path])
    return PublicCase(
        case_id=case_id,
        root=root,
        input_path=input_path,
        prompt_path=prompt_path,
        public_context_path=public_context_path,
        manifest_path=manifest_path,
        seal_path=seal_path,
        params=params,
        locks=locks,
        task_options=task_options,
        manifest_sha256=manifest_hash,
        seal_sha256=_file_sha256(seal_path),
    )


def _load_auditor() -> Any:
    spec = importlib.util.spec_from_file_location(
        "humanize_generation_qualification_auditor", AUDITOR_PATH
    )
    if spec is None or spec.loader is None:
        raise RunnerError("cannot load qualification auditor")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _qualification_bindings(skill_root: Path) -> tuple[Any, dict[str, str]]:
    auditor = _load_auditor()
    bindings = auditor._current_bindings(
        skill_root,
        skill_root / "references" / "evaluation-contract.md",
        skill_root / "references" / "generation-qualification-requirements.json",
    )
    return auditor, dict(bindings)


def _make_read_only(root: Path) -> None:
    for path in [root, *root.rglob("*")]:
        try:
            path.chmod(stat.S_IREAD | (stat.S_IEXEC if path.is_dir() else 0))
        except OSError:
            # The receipt never treats chmod as an isolation proof.
            pass


def _copy_skill_snapshot(source: Path, target: Path, auditor: Any) -> str:
    shutil.copytree(
        source,
        target,
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "*.pyo"),
    )
    source_hash, _ = auditor._skill_snapshot(source)
    copied_hash, _ = auditor._skill_snapshot(target)
    if source_hash != copied_hash:
        raise RunnerError("copied Skill snapshot does not match source Skill")
    _make_read_only(target)
    return source_hash


def _effective_prompt(
    public_prompt: str,
    input_name: str,
    params: Mapping[str, Any],
    locks: Mapping[str, Any],
    task_options: Mapping[str, Any],
) -> str:
    params_text = json.dumps(params, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    locks_text = json.dumps(locks, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    task_options_text = json.dumps(
        task_options, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    )
    return (
        "Use the humanize-academic-chinese Skill at skill/SKILL.md for this one task.\n"
        f"Read the source artifact at case/{input_name}.\n"
        f"Apply this exact configuration: {params_text}.\n"
        f"Honor these scope and structure locks: {locks_text}.\n"
        f"Honor these task options when present: {task_options_text}.\n"
        "Do not inspect paths outside this execution root. Do not look for tests, prior "
        "outputs, gold text, qualification atoms, or evaluator material.\n"
        "Return the requested deliverable in the final response only.\n\n"
        "User request:\n"
        + public_prompt.strip()
        + "\n"
    )


def _sanitized_environment() -> tuple[dict[str, str], list[str]]:
    inherited = {
        key: value
        for key, value in os.environ.items()
        if key.upper() in INHERITED_ENV_NAMES
    }
    return inherited, sorted(inherited)


def _context_payload(
    case: PublicCase,
    bindings: Mapping[str, str],
    model: str | None,
    env_names: Sequence[str],
    codex_version: str,
) -> dict[str, Any]:
    return {
        "schema_version": CONTEXT_SCHEMA,
        "runner_version": RUNNER_VERSION,
        "case_id": case.case_id,
        "public_manifest_sha256": case.manifest_sha256,
        "public_seal_sha256": case.seal_sha256,
        "public_context_sha256": _file_sha256(case.public_context_path),
        "qualification_bindings": dict(bindings),
        "model_requested": model,
        "codex_version": codex_version,
        "session_policy": {
            "ephemeral": True,
            "resume_used": False,
            "ignore_user_config": True,
            "ignore_rules": True,
            "sandbox": "read-only",
        },
        "capture": {
            "user_prompt": "EXACT_BYTES_CAPTURED",
            "system_messages": "UNAVAILABLE_FROM_CODEX_EXEC_CLI",
            "developer_messages": "UNAVAILABLE_FROM_CODEX_EXEC_CLI",
            "tool_events": "CODEX_JSONL",
        },
        "isolation": {
            "process_boundary_observed": True,
            "filesystem_isolation_verified": False,
            "excluded_roots_unreachable_verified": False,
            "skill_snapshot_staged_read_only": True,
            "public_fixture_staged_read_only": True,
            "hidden_oracle_handle_passed_to_runner": False,
            "oracle_catalog_visible_to_generator": True,
            "evidence_cap": "E2",
            "reason": (
                "read-only codex sandbox does not prove host paths are unreadable, and the "
                "qualification catalog is part of the staged full Skill snapshot"
            ),
        },
        "environment_allowlist_names": list(env_names),
        "params": dict(case.params),
        "locks": dict(case.locks),
    }


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _invoke_codex(
    command: Sequence[str], prompt: bytes, env: Mapping[str, str], timeout: int
) -> Invocation:
    started_at = _utc_now()
    process = subprocess.Popen(
        list(command),
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=dict(env),
        shell=False,
    )
    timed_out = False
    try:
        stdout, stderr = process.communicate(input=prompt, timeout=timeout)
    except subprocess.TimeoutExpired:
        timed_out = True
        process.terminate()
        try:
            stdout, stderr = process.communicate(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            stdout, stderr = process.communicate()
    return Invocation(
        command=tuple(str(item) for item in command),
        pid=process.pid,
        returncode=process.returncode,
        stdout=stdout,
        stderr=stderr,
        timed_out=timed_out,
        started_at=started_at,
        ended_at=_utc_now(),
    )


def _codex_version(codex: str, env: Mapping[str, str]) -> str:
    result = subprocess.run(
        [codex, "--version"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=dict(env),
        shell=False,
        timeout=15,
        check=False,
    )
    if result.returncode != 0:
        raise RunnerError("cannot query codex CLI version")
    return result.stdout.decode("utf-8", errors="replace").strip()


def _event_ids(raw: bytes) -> dict[str, list[str]]:
    found: dict[str, set[str]] = {
        "request_id": set(),
        "response_id": set(),
        "turn_id": set(),
    }

    def visit(value: Any) -> None:
        if isinstance(value, dict):
            for key, item in value.items():
                if key in found and isinstance(item, str) and item:
                    found[key].add(item)
                visit(item)
        elif isinstance(value, list):
            for item in value:
                visit(item)

    for number, line in enumerate(raw.splitlines(), 1):
        if not line.strip():
            continue
        try:
            visit(json.loads(line.decode("utf-8")))
        except (UnicodeError, json.JSONDecodeError) as error:
            raise RunnerError(f"codex JSONL event {number} is invalid: {error}") from error
    return {key: sorted(values) for key, values in found.items()}


def run_trial(
    case_root: Path,
    output_root: Path,
    *,
    model: str | None = None,
    codex_bin: str = "codex",
    timeout: int = 900,
    skill_root: Path = SKILL_ROOT,
) -> dict[str, Any]:
    case = load_public_case(case_root)
    skill = skill_root.resolve(strict=True)
    output = output_root.resolve(strict=False)
    try:
        output.relative_to(skill)
    except ValueError:
        pass
    else:
        raise RunnerError("runner output must stay outside the Skill root")
    if output.exists() and any(output.iterdir()):
        raise RunnerError("runner output directory must be new or empty")
    output.mkdir(parents=True, exist_ok=True)
    request_dir = output / "request"
    response_dir = output / "response"
    transcript_dir = output / "transcript"
    execution_dir = output / "execution"
    for directory in (request_dir, response_dir, transcript_dir, execution_dir):
        directory.mkdir()

    auditor, bindings = _qualification_bindings(skill)
    staged_skill = execution_dir / "skill"
    skill_hash = _copy_skill_snapshot(skill, staged_skill, auditor)
    if bindings.get("skill_snapshot_sha256") != skill_hash:
        raise RunnerError("qualification bindings do not match staged Skill snapshot")

    case_dir = execution_dir / "case"
    case_dir.mkdir()
    staged_input = case_dir / case.input_path.name
    staged_public_prompt = case_dir / "prompt.txt"
    staged_public_context = case_dir / "public-context.json"
    shutil.copyfile(case.input_path, staged_input)
    shutil.copyfile(case.prompt_path, staged_public_prompt)
    shutil.copyfile(case.public_context_path, staged_public_context)
    _make_read_only(case_dir)

    input_copy = request_dir / case.input_path.name
    public_prompt_copy = request_dir / "public-prompt.txt"
    public_context_copy = request_dir / "public-context.json"
    shutil.copyfile(case.input_path, input_copy)
    shutil.copyfile(case.prompt_path, public_prompt_copy)
    shutil.copyfile(case.public_context_path, public_context_copy)
    public_prompt = case.prompt_path.read_text(encoding="utf-8-sig")
    effective_prompt = _effective_prompt(
        public_prompt,
        case.input_path.name,
        case.params,
        case.locks,
        case.task_options,
    )
    prompt_path = request_dir / "prompt.txt"
    prompt_path.write_text(effective_prompt, encoding="utf-8", newline="\n")

    env, env_names = _sanitized_environment()
    resolved_codex = shutil.which(codex_bin, path=env.get("PATH"))
    if resolved_codex is None:
        raise RunnerError(f"codex executable not found: {codex_bin}")
    version = _codex_version(resolved_codex, env)
    context = _context_payload(case, bindings, model, env_names, version)
    context_path = request_dir / "context.json"
    context_path.write_bytes(_canonical_json(context))

    output_path = response_dir / f"output{case.input_path.suffix.lower()}"
    command = [
        resolved_codex,
        "exec",
        "--ephemeral",
        "--ignore-user-config",
        "--ignore-rules",
        "--skip-git-repo-check",
        "-s",
        "read-only",
        "-C",
        str(execution_dir),
        "--json",
        "--color",
        "never",
        "-o",
        str(output_path),
    ]
    if model:
        command.extend(["-m", model])
    command.append("-")
    invocation = _invoke_codex(command, effective_prompt.encode("utf-8"), env, timeout)
    events_path = transcript_dir / "events.jsonl"
    stderr_path = transcript_dir / "stderr.txt"
    events_path.write_bytes(invocation.stdout)
    stderr_path.write_bytes(invocation.stderr)
    event_ids: dict[str, list[str]] = {}
    event_error: str | None = None
    try:
        event_ids = _event_ids(invocation.stdout)
    except RunnerError as error:
        event_error = str(error)

    receipt = {
        "schema_version": RECEIPT_SCHEMA,
        "runner_version": RUNNER_VERSION,
        "campaign_id": None,
        "case_id": case.case_id,
        "run_id": "RUN-" + uuid.uuid4().hex,
        "runner_executable_sha256": _file_sha256(Path(__file__).resolve()),
        "codex_executable": str(Path(resolved_codex).resolve()),
        "codex_executable_sha256": _file_sha256(Path(resolved_codex).resolve()),
        "codex_version": version,
        "process_identity": {"pid": invocation.pid, "new_process_observed": True},
        "started_at": invocation.started_at,
        "ended_at": invocation.ended_at,
        "model_requested": model,
        "provider_ids": event_ids,
        "provider_request_id_observed": bool(event_ids.get("request_id")),
        "sandbox": "read-only",
        "filesystem_isolation_verified": False,
        "excluded_roots_unreachable_verified": False,
        "oracle_catalog_visible_to_generator": True,
        "evidence_cap": "E2",
        "artifact_sha256": {
            "input": _file_sha256(input_copy),
            "public_context": _file_sha256(public_context_copy),
            "prompt": _file_sha256(prompt_path),
            "context": _file_sha256(context_path),
            "events": _file_sha256(events_path),
            "stderr": _file_sha256(stderr_path),
            "output": _file_sha256(output_path) if output_path.exists() else None,
        },
        "qualification_bindings": bindings,
        "public_manifest_sha256": case.manifest_sha256,
        "public_seal_sha256": case.seal_sha256,
        "exit_status": {
            "returncode": invocation.returncode,
            "timed_out": invocation.timed_out,
            "event_parse_error": event_error,
            "output_present": output_path.exists() and output_path.stat().st_size > 0,
        },
    }
    receipt_path = output / "runner-receipt.json"
    receipt_path.write_bytes(_canonical_json(receipt))

    successful = (
        invocation.returncode == 0
        and not invocation.timed_out
        and event_error is None
        and output_path.exists()
        and output_path.stat().st_size > 0
    )
    if not successful:
        raise RunnerError(
            "codex invocation is infrastructure-invalid; inspect runner-receipt.json"
        )

    artifact_hashes = {
        "input": _file_sha256(input_copy),
        "output": _file_sha256(output_path),
        "prompt": _file_sha256(prompt_path),
        "context": _file_sha256(context_path),
    }
    public_artifact_hashes = {
        "input": _file_sha256(input_copy),
        "prompt": _file_sha256(prompt_path),
        "public_context": _file_sha256(public_context_copy),
    }
    run_record = {
        "schema_version": auditor.GENERATION_RUN_RECORD_SCHEMA,
        "run_id": receipt["run_id"],
        "fresh_context": True,
        "blindness_attestation": auditor.BLINDNESS_ATTESTATION,
        "artifact_sha256": artifact_hashes,
        "public_artifact_sha256": public_artifact_hashes,
        "qualification_bindings": bindings,
        "oracle_catalog_visible_to_generator": True,
        "filesystem_isolation_verified": False,
        "isolation_verification_source": "LOCAL_RUNNER_UNVERIFIED",
        "runner_receipt_sha256": _file_sha256(receipt_path),
        "execution_provenance": {
            "source": "HARNESS_OWNED_LOCAL_RUNNER",
            "process_boundary_observed": True,
            "filesystem_isolation_verified": False,
            "oracle_catalog_visible_to_generator": True,
            "evidence_cap": "E2",
        },
    }
    run_record_path = output / "run-record.json"
    run_record_path.write_bytes(_canonical_json(run_record))
    seal = {
        "schema_version": RUN_SEAL_SCHEMA,
        "run_id": receipt["run_id"],
        "case_id": case.case_id,
        "run_record_sha256": _file_sha256(run_record_path),
        "runner_receipt_sha256": _file_sha256(receipt_path),
        "artifact_sha256": artifact_hashes,
        "public_artifact_sha256": public_artifact_hashes,
        "transcript_sha256": {
            "events": _file_sha256(events_path),
            "stderr": _file_sha256(stderr_path),
        },
    }
    seal_path = output / "run-seal.json"
    seal_path.write_bytes(_canonical_json(seal))
    return {
        "status": "CAPTURED_E2",
        "case_id": case.case_id,
        "run_id": receipt["run_id"],
        "evidence_cap": "E2",
        "filesystem_isolation_verified": False,
        "output": str(output_path),
        "run_record": str(run_record_path),
        "runner_receipt": str(receipt_path),
        "run_seal": str(seal_path),
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Run one sealed public humanize fixture through a fresh local Codex process. "
            "The built-in local backend is capped at E2 because host-read isolation is unverified."
        )
    )
    parser.add_argument("case_root", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--model")
    parser.add_argument("--codex-bin", default="codex")
    parser.add_argument("--timeout", type=int, default=900)
    parser.add_argument("--format", choices=("json", "text"), default="text")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.timeout < 1 or args.timeout > 3600:
            raise RunnerError("timeout must be between 1 and 3600 seconds")
        result = run_trial(
            args.case_root,
            args.output,
            model=args.model,
            codex_bin=args.codex_bin,
            timeout=args.timeout,
        )
    except (RunnerError, OSError, subprocess.SubprocessError) as error:
        result = {"status": "INFRA_INVALID", "error": str(error), "evidence_cap": "E0"}
        if args.format == "json":
            print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        else:
            print(f"INFRA_INVALID: {error}")
        return 1
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    else:
        print(
            f"{result['status']} run_id={result['run_id']} "
            "filesystem_isolation_verified=false"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
