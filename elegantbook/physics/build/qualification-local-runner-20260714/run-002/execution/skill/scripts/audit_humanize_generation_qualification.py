#!/usr/bin/env python3
"""Audit forward-generation qualification evidence for this Skill.

The auditor deliberately separates evidence integrity from qualification.  It never
executes commands supplied by a manifest: deterministic evidence can only be replayed
through a local tool allowlist with ``shell=False``.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence


SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_SKILL_ROOT = SCRIPT_DIR.parent
DEFAULT_REQUIREMENTS = (
    DEFAULT_SKILL_ROOT / "references" / "generation-qualification-requirements.json"
)
DEFAULT_CONTRACT = DEFAULT_SKILL_ROOT / "references" / "evaluation-contract.md"
DEFAULT_ORACLE_CATALOG = (
    DEFAULT_SKILL_ROOT / "references" / "generation-qualification-oracles.json"
)

REQUIREMENTS_SCHEMA = "humanize-generation-qualification-requirements/v1"
ORACLE_CATALOG_SCHEMA = "humanize-generation-oracle-catalog/v1"
ORACLE_REVIEW_SCHEMA = "humanize-generation-oracle-review/v1"
PUBLIC_CONTEXT_SCHEMA = "humanize-generation-public-context/v1"
MANIFEST_V2_SCHEMA = "humanize-generation-qualification-manifest/v2"
REPORT_SCHEMA = "humanize-generation-qualification-report/v2"
GENERATION_RUN_RECORD_SCHEMA = "humanize-generation-run-record/v1"
ROUTE_OBSERVATION_SCHEMA = "humanize-route-observation/v1"
BLINDNESS_ATTESTATION = "CALLER_ATTESTED_STAGED_CONTEXT"
INDEPENDENCE_ATTESTATION = "CALLER_ATTESTED_DISTINCT_RUN_RECORDS"
MANIFEST_SCHEMAS = {
    "humanize-generation-qualification-manifest/v1",
    "humanize-generation-qualification-evidence/v1",
    MANIFEST_V2_SCHEMA,
}
EVIDENCE_RANK = {"E0": 0, "E1": 1, "E2": 2, "E3": 3, "E4": 4}
MACHINE_EXIT = {"PASS": 0, "FAIL": 1, "REVIEW": 2}
QUALIFICATION_EXIT = {"PASS": 0, "FAIL": 1, "NOT_EVALUATED": 2}
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
SAFE_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.:/-]{0,159}$")
ARTIFACT_KEY_RE = re.compile(r"^[A-Za-z][A-Za-z0-9_.-]{0,63}$")
PLACEHOLDER_RE = re.compile(r"^\$\{(?:ARTIFACT:)?([A-Za-z][A-Za-z0-9_.-]{0,63})\}$")
CONTRACT_ID_RE = re.compile(r"`((?:MODE|INT|OUT|DEC|ROUTE|VOICE|ROLE|PATH|LONG)-\d{2})`")

FIXED_CONTRACT_RANGES = {
    "MODE": (1, 6),
    "INT": (1, 7),
    "OUT": (1, 6),
    "DEC": (1, 8),
    "ROUTE": (1, 12),
    "VOICE": (1, 10),
    "ROLE": (1, 9),
    "LONG": (1, 13),
}
FIXED_MATRIX_POLICIES = {
    "MODE": ("E3", "P1", {"MODE-01": "P0", "MODE-06": "P0"}),
    "INT": ("E3", "P1", {"INT-05": "P0", "INT-06": "P0"}),
    "OUT": ("E3", "P1", {"OUT-06": "P0"}),
    "DEC": ("E3", "P1", {}),
    "ROUTE": ("E3", "P1", {"ROUTE-12": "P0"}),
    "VOICE": ("E3", "P1", {}),
    "ROLE": ("E3", "P0", {}),
    "LONG": ("E3", "P0", {}),
}
FIXED_SCENES = ("COURSE", "MODELING", "RESEARCH", "GENERAL")
FIXED_FIXTURE_VARIANTS = ("positive", "negative", "conflict")
FIXED_REPORT_VARIANTS = (
    "unique-mapping",
    "duplicate-mapping",
    "unmappable",
    "score-only",
    "malicious-html",
    "mixed-evasion-request",
)
FIXED_GLOBAL_ATOMS = {
    "STABILITY/route-owner-three-runs": ("route_stability", "E3", "P1"),
    "PROTECTED/hash-zero": ("protected_hash", "E2", "P0"),
}
FIXED_EVIDENCE_BINDING_CONTRACT = {
    "generation_run_record_schema": GENERATION_RUN_RECORD_SCHEMA,
    "qualification_manifest_schema": MANIFEST_V2_SCHEMA,
    "oracle_catalog_schema": ORACLE_CATALOG_SCHEMA,
    "route_observation_schema": ROUTE_OBSERVATION_SCHEMA,
    "blindness_attestation": BLINDNESS_ATTESTATION,
    "independence_attestation": INDEPENDENCE_ATTESTATION,
    "required_run_artifact_roles": ["input", "output", "prompt", "context"],
    "required_current_bindings": [
        "skill_snapshot_sha256",
        "contract_sha256",
        "requirements_sha256",
        "oracle_catalog_sha256",
    ],
}

ORACLE_CHECK_TYPES = {
    "replay_result",
    "json_value",
    "utf8_literal",
    "artifact_relation",
    "structure_relation",
    "measurement_result",
}
REQUIRED_VERTICAL_SLICE = {
    "MODE-02": "MODE-02/basic-rewrite/v1",
    "ROLE-02": "ROLE-02/quoted-span/v1",
    "PATH-05/positive": "PATH-05/positive/v1",
    "LONG-01": "LONG-01/include-manifest/v1",
    "PROTECTED/hash-zero": "PROTECTED/hash-zero/v1",
}
V2_FORBIDDEN_MANIFEST_KEYS = {
    "assertions",
    "assertion_ids",
    "result",
    "expected",
    "expected_exit_code",
    "regex",
    "command",
    "argv",
    "executable",
    "shell",
    "powershell",
    "bash",
    "replays",
    "evaluator",
    "evaluator_parameters",
    "check_ids",
    "blind_review",
    "idempotency",
    "route_stability",
    "protected_spans",
}

TOOL_ALLOWLIST = {
    "validate_humanize_output": {
        "relative_path": "scripts/validate_humanize_output.py",
        "positional_artifacts": ("input", "output"),
        "options": {
            "--scene": 1,
            "--format": 1,
            "--keep-reason": 1,
            "--strict-speech-acts": 0,
            "--propose-warning-resolution": 1,
            "--warning-review-request-sha256": 1,
            "--warning-reviewer-kind": 1,
            "--warning-reviewer-id": 1,
            "--term": 1,
        },
    }
}


class AuditError(ValueError):
    """Raised for a fatal audit input error."""


def _reject_nonfinite(value: str) -> None:
    raise AuditError(f"non-finite JSON number is forbidden: {value}")


def _reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise AuditError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _strict_json_bytes(raw: bytes, label: str) -> Any:
    try:
        text = raw.decode("utf-8-sig")
        return json.loads(
            text,
            object_pairs_hook=_reject_duplicate_keys,
            parse_constant=_reject_nonfinite,
        )
    except (UnicodeError, json.JSONDecodeError) as error:
        raise AuditError(f"{label} is not strict UTF-8 JSON: {error}") from error


def _strict_json_file(path: Path, label: str) -> Any:
    try:
        return _strict_json_bytes(path.read_bytes(), label)
    except OSError as error:
        raise AuditError(f"cannot read {label}: {error}") from error


def _canonical_json(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def _sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _file_sha256(path: Path) -> str:
    return _sha256(path.read_bytes())


def _is_relative_to(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
    except ValueError:
        return False
    return True


def _resolve_inside(root: Path, relative: str, label: str, *, must_exist: bool = True) -> Path:
    if not isinstance(relative, str) or not relative.strip():
        raise AuditError(f"{label} must be a non-empty relative path")
    supplied = Path(relative)
    if supplied.is_absolute() or supplied.drive or "\x00" in relative:
        raise AuditError(f"{label} must stay inside the configured root")
    root_resolved = root.resolve(strict=True)
    try:
        resolved = (root_resolved / supplied).resolve(strict=must_exist)
    except OSError as error:
        raise AuditError(f"cannot resolve {label}: {error}") from error
    if not _is_relative_to(resolved, root_resolved):
        raise AuditError(f"{label} escapes the configured root")
    return resolved


def _as_mapping(value: Any, label: str) -> Mapping[str, Any]:
    if not isinstance(value, dict):
        raise AuditError(f"{label} must be an object")
    return value


def _safe_id(value: Any, label: str) -> str:
    if not isinstance(value, str) or not SAFE_ID_RE.fullmatch(value):
        raise AuditError(f"{label} is missing or contains unsafe characters")
    return value


def _hash_value(value: Any, label: str) -> str:
    if not isinstance(value, str) or not SHA256_RE.fullmatch(value.lower()):
        raise AuditError(f"{label} must be a full SHA-256")
    return value.lower()


@dataclass(frozen=True)
class Atom:
    atom_id: str
    dimension: str
    minimum_evidence: str
    severity: str
    kind: str = "behavior"


@dataclass(frozen=True)
class Artifact:
    key: str
    path: Path
    expected_sha256: str
    actual_sha256: str
    size: int
    raw: bytes


@dataclass(frozen=True)
class OracleCatalog:
    path: Path
    raw_sha256: str
    catalog_version: str
    checks: Mapping[str, Mapping[str, Any]]
    check_sha256: Mapping[str, str]
    rubrics: Mapping[str, Mapping[str, Any]]
    rubric_sha256: Mapping[str, str]
    suites: Mapping[str, Mapping[str, Any]]
    suite_sha256: Mapping[str, str]


def _exact_keys(value: Mapping[str, Any], allowed: set[str], label: str) -> None:
    actual = set(value)
    if actual != allowed:
        missing = sorted(allowed - actual)
        extra = sorted(actual - allowed)
        details: list[str] = []
        if missing:
            details.append("missing " + ", ".join(missing))
        if extra:
            details.append("unknown " + ", ".join(extra))
        raise AuditError(f"{label} fields are invalid ({'; '.join(details)})")


def _canonical_definition_hash(value: Mapping[str, Any]) -> str:
    return _sha256(_canonical_json(value))


def _forbidden_manifest_paths(value: Any, prefix: str = "case") -> list[str]:
    found: list[str] = []
    if isinstance(value, dict):
        for key, nested in value.items():
            path = f"{prefix}.{key}"
            if key in V2_FORBIDDEN_MANIFEST_KEYS:
                found.append(path)
            found.extend(_forbidden_manifest_paths(nested, path))
    elif isinstance(value, list):
        for index, nested in enumerate(value):
            found.extend(_forbidden_manifest_paths(nested, f"{prefix}[{index}]"))
    return found


def _validate_literal_rules(value: Any, label: str, *, forbidden: bool) -> None:
    if not isinstance(value, list) or not value:
        raise AuditError(f"{label} must be a non-empty array")
    for index, rule in enumerate(value):
        item_label = f"{label}[{index}]"
        rule = _as_mapping(rule, item_label)
        allowed = {"literal", "maximum_occurrences"} if forbidden else {
            "literal",
            "minimum_occurrences",
            "maximum_occurrences",
        }
        if forbidden:
            _exact_keys(rule, allowed, item_label)
        elif set(rule) not in (
            {"literal", "minimum_occurrences"},
            {"literal", "minimum_occurrences", "maximum_occurrences"},
        ):
            raise AuditError(f"{item_label} fields are invalid")
        literal = rule.get("literal")
        if not isinstance(literal, str) or not literal or "\x00" in literal:
            raise AuditError(f"{item_label}.literal must be non-empty UTF-8 text")
        minimum = rule.get("minimum_occurrences", 0)
        maximum = rule.get("maximum_occurrences")
        if (
            not isinstance(minimum, int)
            or isinstance(minimum, bool)
            or minimum < 0
            or (
                maximum is not None
                and (
                    not isinstance(maximum, int)
                    or isinstance(maximum, bool)
                    or maximum < minimum
                )
            )
        ):
            raise AuditError(f"{item_label} occurrence bounds are invalid")
        if forbidden and maximum != 0:
            raise AuditError(f"{item_label}.maximum_occurrences must be zero")


def _validate_catalog_check_configuration(
    check_type: str,
    configuration: Any,
    label: str,
) -> None:
    config = _as_mapping(configuration, label)
    if check_type == "replay_result":
        _exact_keys(config, {"tool_id", "args", "expected"}, label)
        declaration_error = _static_replay_declaration_error(config)
        if declaration_error:
            raise AuditError(f"{label} {declaration_error}")
        _expected, expected_error = _expected_machine_result(config)
        if expected_error:
            raise AuditError(f"{label} {expected_error}")
        return
    if check_type == "utf8_literal":
        if set(config) not in (
            {"artifact_role", "required"},
            {"artifact_role", "forbidden"},
            {"artifact_role", "required", "forbidden"},
        ):
            raise AuditError(f"{label} fields are invalid")
        _safe_id(config.get("artifact_role"), f"{label}.artifact_role")
        if "required" in config:
            _validate_literal_rules(config["required"], f"{label}.required", forbidden=False)
        if "forbidden" in config:
            _validate_literal_rules(config["forbidden"], f"{label}.forbidden", forbidden=True)
        return
    if check_type == "artifact_relation":
        _exact_keys(
            config,
            {
                "operator",
                "before_role",
                "after_role",
                "literal",
                "minimum_occurrences",
            },
            label,
        )
        if config.get("operator") != "LITERAL_OCCURRENCES_EQUAL":
            raise AuditError(f"{label}.operator is unsupported")
        _safe_id(config.get("before_role"), f"{label}.before_role")
        _safe_id(config.get("after_role"), f"{label}.after_role")
        if not isinstance(config.get("literal"), str) or not config["literal"]:
            raise AuditError(f"{label}.literal must be non-empty")
        minimum = config.get("minimum_occurrences")
        if not isinstance(minimum, int) or isinstance(minimum, bool) or minimum < 1:
            raise AuditError(f"{label}.minimum_occurrences must be a positive integer")
        return
    if check_type == "structure_relation":
        _exact_keys(
            config,
            {"operator", "input_role", "output_role", "minimum_paragraphs"},
            label,
        )
        if config.get("operator") != "PARAGRAPH_SENTENCE_GRID_CHANGED":
            raise AuditError(f"{label}.operator is unsupported")
        _safe_id(config.get("input_role"), f"{label}.input_role")
        _safe_id(config.get("output_role"), f"{label}.output_role")
        minimum = config.get("minimum_paragraphs")
        if not isinstance(minimum, int) or isinstance(minimum, bool) or minimum < 2:
            raise AuditError(f"{label}.minimum_paragraphs must be at least two")
        return
    if check_type == "json_value":
        _exact_keys(config, {"artifact_role", "path", "operator", "expected"}, label)
        _safe_id(config.get("artifact_role"), f"{label}.artifact_role")
        path = config.get("path")
        if (
            not isinstance(path, list)
            or not path
            or not all(isinstance(item, str) and item for item in path)
        ):
            raise AuditError(f"{label}.path must be a non-empty string array")
        if config.get("operator") not in {"EQUALS", "ARRAY_SET_EQUALS"}:
            raise AuditError(f"{label}.operator is unsupported")
        if config.get("operator") == "ARRAY_SET_EQUALS" and (
            not isinstance(config.get("expected"), list)
            or len(set(config["expected"])) != len(config["expected"])
        ):
            raise AuditError(f"{label}.expected must be a duplicate-free array")
        return
    if check_type == "measurement_result":
        _exact_keys(
            config,
            {"measurement", "annotation_artifact", "expected_status"},
            label,
        )
        if config.get("measurement") != "protected_hash":
            raise AuditError(f"{label}.measurement is unsupported")
        _safe_id(config.get("annotation_artifact"), f"{label}.annotation_artifact")
        if config.get("expected_status") != "PASS":
            raise AuditError(f"{label}.expected_status must be PASS")
        return
    raise AuditError(f"{label} uses unsupported check type {check_type}")


def _validate_public_context(raw: bytes, label: str) -> None:
    payload = _as_mapping(_strict_json_bytes(raw, label), label)
    _exact_keys(
        payload,
        {
            "schema_version",
            "mode",
            "scene",
            "intensity",
            "output",
            "report_context",
            "scope",
            "title_lock",
            "structure_lock",
            "task_options",
        },
        label,
    )
    if payload.get("schema_version") != PUBLIC_CONTEXT_SCHEMA:
        raise AuditError(f"{label}.schema_version must be {PUBLIC_CONTEXT_SCHEMA}")
    if payload.get("mode") not in {"DIAGNOSE", "REWRITE", "DRAFT"}:
        raise AuditError(f"{label}.mode is invalid")
    if payload.get("scene") not in {"COURSE", "MODELING", "RESEARCH", "GENERAL"}:
        raise AuditError(f"{label}.scene is invalid")
    if payload.get("intensity") not in {"LIGHT", "BALANCED", "STRUCTURAL"}:
        raise AuditError(f"{label}.intensity is invalid")
    if payload.get("output") not in {"CLEAN", "ANNOTATED", "PATCH"}:
        raise AuditError(f"{label}.output is invalid")
    if payload.get("report_context") not in {"NONE", "REPORT_INFORMED"}:
        raise AuditError(f"{label}.report_context is invalid")
    if not isinstance(payload.get("scope"), str) or not payload["scope"]:
        raise AuditError(f"{label}.scope must be non-empty")
    if not isinstance(payload.get("title_lock"), bool):
        raise AuditError(f"{label}.title_lock must be boolean")
    if not isinstance(payload.get("structure_lock"), bool):
        raise AuditError(f"{label}.structure_lock must be boolean")
    if not isinstance(payload.get("task_options"), dict):
        raise AuditError(f"{label}.task_options must be an object")
    rendered = _canonical_json(payload).decode("utf-8")
    if re.search(r"(?:MODE|INT|OUT|DEC|ROUTE|VOICE|ROLE|PATH|LONG)-\d{2}", rendered):
        raise AuditError(f"{label} leaks a qualification atom identifier")
    if any(
        key in {"expected", "result", "assertions", "oracle_suite_id", "pathology"}
        for key in payload["task_options"]
    ):
        raise AuditError(f"{label}.task_options leaks grader-owned state")


def _load_oracle_catalog(
    skill_root: Path,
    contract_path: Path,
    requirements_path: Path,
    requirements: Mapping[str, Any],
    atoms: Mapping[str, Atom],
) -> OracleCatalog:
    expected_path = skill_root / "references" / "generation-qualification-oracles.json"
    if expected_path.is_symlink():
        raise AuditError("oracle catalog path must not be a symlink")
    path = expected_path.resolve(strict=True)
    if not _is_relative_to(path, skill_root) or path != expected_path:
        raise AuditError("oracle catalog must use the fixed Skill references path")
    raw = path.read_bytes()
    payload = _as_mapping(_strict_json_bytes(raw, "oracle catalog"), "oracle catalog")
    _exact_keys(
        payload,
        {
            "schema_version",
            "catalog_version",
            "grader_engine_version",
            "contract_binding",
            "requirements_binding",
            "policy",
            "fixture_provenance",
            "checks",
            "review_rubrics",
            "suites",
        },
        "oracle catalog",
    )
    if payload.get("schema_version") != ORACLE_CATALOG_SCHEMA:
        raise AuditError(f"oracle catalog schema must be {ORACLE_CATALOG_SCHEMA}")
    catalog_version = payload.get("catalog_version")
    if not isinstance(catalog_version, str) or not re.fullmatch(r"\d+\.\d+\.\d+", catalog_version):
        raise AuditError("oracle catalog version must be SemVer")
    if payload.get("grader_engine_version") != "1":
        raise AuditError("oracle catalog grader_engine_version must be 1")
    if payload.get("policy") != {
        "unknown_fields": "REJECT",
        "text_encoding": "UTF-8",
        "unicode_normalization": "NONE",
    }:
        raise AuditError("oracle catalog policy was weakened or changed")
    provenance = _as_mapping(
        payload.get("fixture_provenance"), "oracle catalog.fixture_provenance"
    )
    expected_bindings = (
        (
            "contract_binding",
            requirements.get("contract_version"),
            _file_sha256(contract_path),
        ),
        (
            "requirements_binding",
            requirements.get("requirements_version"),
            _file_sha256(requirements_path),
        ),
    )
    for field, version, digest in expected_bindings:
        binding = _as_mapping(payload.get(field), f"oracle catalog.{field}")
        _exact_keys(binding, {"version", "sha256"}, f"oracle catalog.{field}")
        if binding.get("version") != version or binding.get("sha256") != digest:
            raise AuditError(f"oracle catalog {field} is stale")

    checks_raw = payload.get("checks")
    if not isinstance(checks_raw, list):
        raise AuditError("oracle catalog.checks must be an array")
    checks: dict[str, Mapping[str, Any]] = {}
    check_hashes: dict[str, str] = {}
    for index, raw_check in enumerate(checks_raw):
        label = f"oracle catalog.checks[{index}]"
        check = _as_mapping(raw_check, label)
        _exact_keys(check, {"id", "atom_id", "type", "source", "configuration"}, label)
        check_id = _safe_id(check.get("id"), f"{label}.id")
        if check_id in checks:
            raise AuditError(f"duplicate oracle check id: {check_id}")
        atom_id = check.get("atom_id")
        if atom_id not in atoms:
            raise AuditError(f"{check_id} references unknown atom: {atom_id}")
        check_type = check.get("type")
        if check_type not in ORACLE_CHECK_TYPES:
            raise AuditError(f"{check_id} uses unsupported check type: {check_type}")
        if not isinstance(check.get("source"), str) or not check["source"]:
            raise AuditError(f"{check_id}.source must be non-empty")
        _validate_catalog_check_configuration(
            str(check_type), check.get("configuration"), f"{check_id}.configuration"
        )
        checks[check_id] = dict(check)
        check_hashes[check_id] = _canonical_definition_hash(check)

    rubrics_raw = payload.get("review_rubrics")
    if not isinstance(rubrics_raw, list):
        raise AuditError("oracle catalog.review_rubrics must be an array")
    rubrics: dict[str, Mapping[str, Any]] = {}
    rubric_hashes: dict[str, str] = {}
    for index, raw_rubric in enumerate(rubrics_raw):
        label = f"oracle catalog.review_rubrics[{index}]"
        rubric = _as_mapping(raw_rubric, label)
        _exact_keys(
            rubric,
            {
                "id",
                "atom_id",
                "reviewer_kinds",
                "minimum_distinct_reviewers",
                "questions",
                "aggregation",
            },
            label,
        )
        rubric_id = _safe_id(rubric.get("id"), f"{label}.id")
        if rubric_id in rubrics:
            raise AuditError(f"duplicate oracle rubric id: {rubric_id}")
        if rubric.get("atom_id") not in atoms:
            raise AuditError(f"{rubric_id} references unknown atom")
        kinds = rubric.get("reviewer_kinds")
        if (
            not isinstance(kinds, list)
            or not kinds
            or not set(kinds).issubset({"MODEL", "HUMAN"})
            or len(set(kinds)) != len(kinds)
        ):
            raise AuditError(f"{rubric_id}.reviewer_kinds is invalid")
        minimum = rubric.get("minimum_distinct_reviewers")
        if not isinstance(minimum, int) or isinstance(minimum, bool) or minimum < 1:
            raise AuditError(f"{rubric_id}.minimum_distinct_reviewers is invalid")
        questions = rubric.get("questions")
        if not isinstance(questions, list) or not questions:
            raise AuditError(f"{rubric_id}.questions must be non-empty")
        question_ids: set[str] = set()
        for question_index, raw_question in enumerate(questions):
            question = _as_mapping(
                raw_question, f"{rubric_id}.questions[{question_index}]"
            )
            _exact_keys(
                question,
                {"id", "answer_type"},
                f"{rubric_id}.questions[{question_index}]",
            )
            question_id = _safe_id(
                question.get("id"), f"{rubric_id}.questions[{question_index}].id"
            )
            if question_id in question_ids:
                raise AuditError(f"{rubric_id} repeats question {question_id}")
            question_ids.add(question_id)
            if question.get("answer_type") != "PASS_FAIL":
                raise AuditError(f"{rubric_id}.{question_id} must use PASS_FAIL")
        if rubric.get("aggregation") != "ALL_PASS":
            raise AuditError(f"{rubric_id}.aggregation must be ALL_PASS")
        rubrics[rubric_id] = dict(rubric)
        rubric_hashes[rubric_id] = _canonical_definition_hash(rubric)

    suites_raw = payload.get("suites")
    if not isinstance(suites_raw, list):
        raise AuditError("oracle catalog.suites must be an array")
    suites: dict[str, Mapping[str, Any]] = {}
    suite_hashes: dict[str, str] = {}
    for index, raw_suite in enumerate(suites_raw):
        label = f"oracle catalog.suites[{index}]"
        suite = _as_mapping(raw_suite, label)
        _exact_keys(
            suite,
            {
                "id",
                "atom_id",
                "qualification_stage",
                "runner_compatible",
                "fixture_bindings",
                "required_checks",
                "required_reviews",
            },
            label,
        )
        suite_id = _safe_id(suite.get("id"), f"{label}.id")
        if suite_id in suites:
            raise AuditError(f"duplicate oracle suite id: {suite_id}")
        atom_id = suite.get("atom_id")
        if atom_id not in atoms:
            raise AuditError(f"{suite_id} references unknown atom: {atom_id}")
        if suite.get("qualification_stage") != "SHADOW":
            raise AuditError(f"{suite_id}.qualification_stage must remain SHADOW in catalog v1")
        if suite.get("runner_compatible") is not False:
            raise AuditError(f"{suite_id}.runner_compatible must remain false in catalog v1")
        fixtures = _as_mapping(suite.get("fixture_bindings"), f"{suite_id}.fixture_bindings")
        if not fixtures:
            raise AuditError(f"{suite_id}.fixture_bindings must be non-empty")
        for role, raw_descriptor in fixtures.items():
            _safe_id(role, f"{suite_id}.fixture role")
            descriptor = _as_mapping(raw_descriptor, f"{suite_id}.fixture_bindings.{role}")
            _exact_keys(
                descriptor,
                {"path", "sha256"},
                f"{suite_id}.fixture_bindings.{role}",
            )
            digest = _hash_value(
                descriptor.get("sha256"), f"{suite_id}.fixture_bindings.{role}.sha256"
            )
            fixture_path = _resolve_inside(
                skill_root,
                descriptor.get("path"),
                f"{suite_id}.fixture_bindings.{role}.path",
            )
            if fixture_path.is_symlink() or not fixture_path.is_file():
                raise AuditError(f"{suite_id} fixture {role} must be a regular non-symlink file")
            if _file_sha256(fixture_path) != digest:
                raise AuditError(f"{suite_id} fixture {role} hash drift")
            if role == "public_context":
                _validate_public_context(
                    fixture_path.read_bytes(), f"{suite_id}.public_context"
                )
        required_checks = suite.get("required_checks")
        required_reviews = suite.get("required_reviews")
        if (
            not isinstance(required_checks, list)
            or not isinstance(required_reviews, list)
            or not all(isinstance(item, str) for item in required_checks + required_reviews)
        ):
            raise AuditError(f"{suite_id} required checks/reviews must be arrays")
        if not required_checks and not required_reviews:
            raise AuditError(f"{suite_id} is empty")
        if len(set(required_checks)) != len(required_checks):
            raise AuditError(f"{suite_id} repeats a required check")
        if len(set(required_reviews)) != len(required_reviews):
            raise AuditError(f"{suite_id} repeats a required review")
        for check_id in required_checks:
            check = checks.get(check_id)
            if check is None:
                raise AuditError(f"{suite_id} references missing check {check_id}")
            if check.get("atom_id") != atom_id:
                raise AuditError(f"{suite_id} check {check_id} belongs to another atom")
        for rubric_id in required_reviews:
            rubric = rubrics.get(rubric_id)
            if rubric is None:
                raise AuditError(f"{suite_id} references missing rubric {rubric_id}")
            if rubric.get("atom_id") != atom_id:
                raise AuditError(f"{suite_id} rubric {rubric_id} belongs to another atom")
        suites[suite_id] = dict(suite)
        suite_hashes[suite_id] = _canonical_definition_hash(suite)

    for atom_id, suite_id in REQUIRED_VERTICAL_SLICE.items():
        suite = suites.get(suite_id)
        if suite is None or suite.get("atom_id") != atom_id:
            raise AuditError(f"oracle catalog lacks required vertical suite {suite_id}")
    if set(provenance) != set(suites):
        raise AuditError("oracle fixture provenance must cover exactly every suite")
    for suite_id, raw_entry in provenance.items():
        entry = _as_mapping(raw_entry, f"oracle fixture provenance.{suite_id}")
        _exact_keys(
            entry,
            {"sources", "derivation"},
            f"oracle fixture provenance.{suite_id}",
        )
        sources = entry.get("sources")
        if not isinstance(sources, list) or not sources:
            raise AuditError(f"oracle fixture provenance.{suite_id}.sources must be non-empty")
        for index, raw_source in enumerate(sources):
            source = _as_mapping(
                raw_source, f"oracle fixture provenance.{suite_id}.sources[{index}]"
            )
            _exact_keys(
                source,
                {"path", "sha256"},
                f"oracle fixture provenance.{suite_id}.sources[{index}]",
            )
            if not isinstance(source.get("path"), str) or not source["path"]:
                raise AuditError(f"oracle fixture provenance.{suite_id} source path is empty")
            _hash_value(
                source.get("sha256"),
                f"oracle fixture provenance.{suite_id}.sources[{index}].sha256",
            )
        if not isinstance(entry.get("derivation"), str) or not entry["derivation"]:
            raise AuditError(f"oracle fixture provenance.{suite_id}.derivation is empty")
    return OracleCatalog(
        path=path,
        raw_sha256=_sha256(raw),
        catalog_version=str(catalog_version),
        checks=checks,
        check_sha256=check_hashes,
        rubrics=rubrics,
        rubric_sha256=rubric_hashes,
        suites=suites,
        suite_sha256=suite_hashes,
    )


def _validate_level(value: Any, label: str) -> str:
    if value not in EVIDENCE_RANK:
        raise AuditError(f"{label} must be one of {sorted(EVIDENCE_RANK)}")
    return str(value)


def _validate_severity(value: Any, label: str) -> str:
    if value not in {"P0", "P1", "P2"}:
        raise AuditError(f"{label} must be P0, P1, or P2")
    return str(value)


def _expand_requirements(requirements: Mapping[str, Any]) -> tuple[dict[str, Atom], list[str]]:
    """Validate the non-shrinkable compact matrix and expand it into atoms."""

    errors: list[str] = []
    atoms: dict[str, Atom] = {}

    def add(atom: Atom) -> None:
        if atom.atom_id in atoms:
            errors.append(f"requirements duplicate atom: {atom.atom_id}")
        else:
            atoms[atom.atom_id] = atom

    if requirements.get("schema_version") != REQUIREMENTS_SCHEMA:
        errors.append(f"requirements schema must be {REQUIREMENTS_SCHEMA}")
    if requirements.get("evidence_levels") != {
        "E0": "CLAIM_ONLY",
        "E1": "ARCHIVED_ARTIFACT",
        "E2": "DETERMINISTIC_REPLAY",
        "E3": "BLIND_FORWARD",
        "E4": "BLIND_HUMAN_REVIEW",
    }:
        errors.append("requirements evidence level definitions were weakened or changed")
    if requirements.get("status_mapping") != MACHINE_EXIT:
        errors.append("requirements machine status mapping must remain PASS=0, FAIL=1, REVIEW=2")
    if requirements.get("qualification_exit_codes") != QUALIFICATION_EXIT:
        errors.append("requirements qualification exit mapping must remain PASS=0, FAIL=1, NOT_EVALUATED=2")
    if requirements.get("evidence_binding_contract") != FIXED_EVIDENCE_BINDING_CONTRACT:
        errors.append("requirements evidence binding contract was weakened or changed")

    matrices = requirements.get("contract_matrices")
    if not isinstance(matrices, dict) or set(matrices) != set(FIXED_CONTRACT_RANGES):
        errors.append("contract_matrices must define exactly MODE/INT/OUT/DEC/ROUTE/VOICE/ROLE/LONG")
        matrices = matrices if isinstance(matrices, dict) else {}
    for prefix, (fixed_first, fixed_last) in FIXED_CONTRACT_RANGES.items():
        entry = matrices.get(prefix)
        if not isinstance(entry, dict):
            continue
        if (entry.get("first"), entry.get("last")) != (fixed_first, fixed_last):
            errors.append(f"{prefix} range must remain {fixed_first}..{fixed_last}")
            continue
        try:
            minimum = _validate_level(entry.get("minimum_evidence"), f"{prefix}.minimum_evidence")
            default_severity = _validate_severity(entry.get("severity"), f"{prefix}.severity")
        except AuditError as error:
            errors.append(str(error))
            continue
        overrides = entry.get("severity_overrides", {})
        if not isinstance(overrides, dict):
            errors.append(f"{prefix}.severity_overrides must be an object")
            overrides = {}
        fixed_minimum, fixed_severity, fixed_overrides = FIXED_MATRIX_POLICIES[prefix]
        if minimum != fixed_minimum or default_severity != fixed_severity or overrides != fixed_overrides:
            errors.append(f"{prefix} evidence/severity policy was weakened or changed")
        valid_ids = {f"{prefix}-{number:02d}" for number in range(fixed_first, fixed_last + 1)}
        if not set(overrides).issubset(valid_ids):
            errors.append(f"{prefix}.severity_overrides contains an unknown contract ID")
        for contract_id in sorted(valid_ids):
            try:
                severity = _validate_severity(
                    overrides.get(contract_id, default_severity), f"{contract_id}.severity"
                )
            except AuditError as error:
                errors.append(str(error))
                continue
            add(Atom(contract_id, prefix.lower(), minimum, severity))

    pathology = requirements.get("pathology_matrix")
    if not isinstance(pathology, dict):
        errors.append("pathology_matrix is required")
    else:
        shape = (pathology.get("prefix"), pathology.get("first"), pathology.get("last"))
        if shape != ("PATH", 1, 16):
            errors.append("pathology_matrix must cover PATH-01..PATH-16")
        variants = pathology.get("variants")
        if variants != list(FIXED_FIXTURE_VARIANTS):
            errors.append("each PATH ID must retain positive/negative/conflict variants")
        try:
            minimum = _validate_level(pathology.get("minimum_evidence"), "PATH.minimum_evidence")
            severity = _validate_severity(pathology.get("severity"), "PATH.severity")
        except AuditError as error:
            errors.append(str(error))
        else:
            if minimum != "E3" or severity != "P1":
                errors.append("PATH evidence/severity policy must remain E3/P1")
            if shape == ("PATH", 1, 16) and variants == list(FIXED_FIXTURE_VARIANTS):
                for number in range(1, 17):
                    for variant in FIXED_FIXTURE_VARIANTS:
                        add(Atom(f"PATH-{number:02d}/{variant}", "pathology", minimum, severity))

    scene_matrix = requirements.get("scene_matrix")
    if not isinstance(scene_matrix, dict):
        errors.append("scene_matrix is required")
    else:
        if scene_matrix.get("scenes") != list(FIXED_SCENES):
            errors.append("scene_matrix must cover COURSE/MODELING/RESEARCH/GENERAL")
        if scene_matrix.get("variants") != list(FIXED_FIXTURE_VARIANTS):
            errors.append("each scene must retain positive/negative/conflict variants")
        try:
            minimum = _validate_level(scene_matrix.get("minimum_evidence"), "scene.minimum_evidence")
            severity = _validate_severity(scene_matrix.get("severity"), "scene.severity")
        except AuditError as error:
            errors.append(str(error))
        else:
            if minimum != "E3" or severity != "P1":
                errors.append("scene evidence/severity policy must remain E3/P1")
            for scene in FIXED_SCENES:
                for variant in FIXED_FIXTURE_VARIANTS:
                    add(Atom(f"SCENE/{scene}/{variant}", "scene", minimum, severity))

    report_matrix = requirements.get("report_informed_matrix")
    if not isinstance(report_matrix, dict):
        errors.append("report_informed_matrix is required")
    else:
        if report_matrix.get("variants") != list(FIXED_REPORT_VARIANTS):
            errors.append("REPORT_INFORMED must retain all six adversarial variants")
        try:
            minimum = _validate_level(report_matrix.get("minimum_evidence"), "report.minimum_evidence")
            default_severity = _validate_severity(report_matrix.get("severity"), "report.severity")
        except AuditError as error:
            errors.append(str(error))
        else:
            overrides = report_matrix.get("severity_overrides", {})
            if not isinstance(overrides, dict):
                errors.append("report severity_overrides must be an object")
                overrides = {}
            valid_ids = {f"REPORT/{variant}" for variant in FIXED_REPORT_VARIANTS}
            if not set(overrides).issubset(valid_ids):
                errors.append("report severity_overrides contains an unknown atom")
            fixed_report_overrides = {
                "REPORT/malicious-html": "P0",
                "REPORT/mixed-evasion-request": "P0",
            }
            if minimum != "E3" or default_severity != "P1" or overrides != fixed_report_overrides:
                errors.append("REPORT evidence/severity policy was weakened or changed")
            for atom_id in sorted(valid_ids):
                try:
                    severity = _validate_severity(
                        overrides.get(atom_id, default_severity), f"{atom_id}.severity"
                    )
                except AuditError as error:
                    errors.append(str(error))
                    continue
                add(Atom(atom_id, "report_informed", minimum, severity))

    repeated = requirements.get("repeated_evaluations")
    if not isinstance(repeated, dict) or set(repeated) != {"idempotency", "blind_review"}:
        errors.append("repeated_evaluations must define exactly idempotency and blind_review")
        repeated = repeated if isinstance(repeated, dict) else {}
    for name, fixed_prefix, fixed_level in (
        ("idempotency", "IDEMPOTENCY", "E3"),
        ("blind_review", "BLIND_REVIEW", "E4"),
    ):
        entry = repeated.get(name)
        if not isinstance(entry, dict):
            continue
        if entry.get("atom_prefix") != fixed_prefix:
            errors.append(f"{name}.atom_prefix must remain {fixed_prefix}")
        if entry.get("scenes") != list(FIXED_SCENES):
            errors.append(f"{name} must cover all four scenes")
        if entry.get("cases_per_scene") != 3:
            errors.append(f"{name} must retain three cases per scene")
        if entry.get("minimum_evidence") != fixed_level:
            errors.append(f"{name}.minimum_evidence must remain {fixed_level}")
        try:
            severity = _validate_severity(entry.get("severity"), f"{name}.severity")
        except AuditError as error:
            errors.append(str(error))
            continue
        if name == "blind_review":
            if entry.get("minimum_distinct_human_reviewers") != 2:
                errors.append("blind_review requires at least two distinct HUMAN reviewers")
            if entry.get("identity_verified") is not False:
                errors.append("blind_review.identity_verified must remain false")
        if (
            entry.get("atom_prefix") == fixed_prefix
            and entry.get("scenes") == list(FIXED_SCENES)
            and entry.get("cases_per_scene") == 3
            and entry.get("minimum_evidence") == fixed_level
        ):
            for scene in FIXED_SCENES:
                for number in range(1, 4):
                    add(
                        Atom(
                            f"{fixed_prefix}/{scene}/{number:02d}",
                            name,
                            fixed_level,
                            severity,
                            kind=name,
                        )
                    )

    globals_raw = requirements.get("global_atoms")
    if not isinstance(globals_raw, list):
        errors.append("global_atoms must be an array")
        globals_raw = []
    global_ids = [
        item.get("id")
        for item in globals_raw
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    ]
    if len(global_ids) != len(set(global_ids)):
        errors.append("requirements duplicate atom in global_atoms")
    global_by_id = {
        item.get("id"): item
        for item in globals_raw
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }
    if set(global_by_id) != set(FIXED_GLOBAL_ATOMS):
        errors.append("global_atoms must retain route stability and protected hash atoms")
    for atom_id, (kind, minimum, severity) in FIXED_GLOBAL_ATOMS.items():
        item = global_by_id.get(atom_id)
        if not isinstance(item, dict):
            continue
        if (item.get("kind"), item.get("minimum_evidence"), item.get("severity")) != (
            kind,
            minimum,
            severity,
        ):
            errors.append(f"{atom_id} contract was weakened or changed")
            continue
        if kind == "route_stability" and item.get("minimum_runs") != 3:
            errors.append("route stability must retain three independent runs")
            continue
        if kind == "protected_hash" and item.get("minimum_spans") != 1:
            errors.append("protected hash evidence must contain at least one real span")
            continue
        add(Atom(atom_id, "global", minimum, severity, kind=kind))

    if len(atoms) != 163:
        errors.append(f"expanded atom count must be 163, got {len(atoms)}")
    return atoms, errors


def _contract_alignment(contract_text: str, atoms: Mapping[str, Atom]) -> list[str]:
    errors: list[str] = []
    found = set(CONTRACT_ID_RE.findall(contract_text))
    expected: set[str] = set()
    for prefix, (first, last) in FIXED_CONTRACT_RANGES.items():
        expected.update(f"{prefix}-{number:02d}" for number in range(first, last + 1))
    expected.update(f"PATH-{number:02d}" for number in range(1, 17))
    missing = sorted(expected - found)
    extra = sorted(found - expected)
    if missing:
        errors.append("evaluation contract is missing IDs: " + ", ".join(missing))
    if extra:
        errors.append("evaluation contract has unregistered IDs: " + ", ".join(extra))
    for contract_id in expected:
        if contract_id.startswith("PATH-"):
            if not all(f"{contract_id}/{variant}" in atoms for variant in FIXED_FIXTURE_VARIANTS):
                errors.append(f"requirements do not expand all variants for {contract_id}")
        elif contract_id not in atoms:
            errors.append(f"requirements do not contain contract ID {contract_id}")
    return errors


def _skill_snapshot(skill_root: Path) -> tuple[str, list[dict[str, Any]]]:
    root = skill_root.resolve(strict=True)
    entries: list[dict[str, Any]] = []
    for path in sorted(root.rglob("*"), key=lambda item: item.relative_to(root).as_posix()):
        relative = path.relative_to(root)
        if any(part in {"__pycache__", ".git"} for part in relative.parts):
            continue
        if path.suffix.lower() in {".pyc", ".pyo"}:
            continue
        if path.is_symlink():
            resolved = path.resolve(strict=True)
            if not _is_relative_to(resolved, root):
                raise AuditError(f"skill snapshot symlink escapes root: {relative.as_posix()}")
        if not path.is_file():
            continue
        raw = path.read_bytes()
        entries.append(
            {
                "path": relative.as_posix(),
                "size": len(raw),
                "sha256": _sha256(raw),
            }
        )
    if not entries:
        raise AuditError("skill snapshot contains no files")
    return _sha256(_canonical_json(entries)), entries


def _current_bindings(skill_root: Path, contract: Path, requirements: Path) -> dict[str, str]:
    skill_hash, _ = _skill_snapshot(skill_root)
    oracle_catalog = skill_root / "references" / "generation-qualification-oracles.json"
    return {
        "skill_snapshot_sha256": skill_hash,
        "contract_sha256": _file_sha256(contract),
        "requirements_sha256": _file_sha256(requirements),
        "oracle_catalog_sha256": _file_sha256(oracle_catalog),
    }


def _binding_state(
    declared: Any,
    current: Mapping[str, str],
    label: str,
    integrity_errors: list[str],
) -> bool:
    if declared is None:
        return False
    if not isinstance(declared, dict):
        integrity_errors.append(f"{label} must be an object")
        return False
    required = set(current)
    if set(declared) != required:
        integrity_errors.append(f"{label} must contain exactly {sorted(required)}")
        return False
    valid = True
    for key, actual in current.items():
        try:
            claimed = _hash_value(declared.get(key), f"{label}.{key}")
        except AuditError as error:
            integrity_errors.append(str(error))
            valid = False
            continue
        if claimed != actual:
            integrity_errors.append(f"{label}.{key} does not bind the current artifact")
            valid = False
    return valid


def _load_artifacts(
    case: Mapping[str, Any],
    artifact_root: Path,
    case_label: str,
    integrity_errors: list[str],
) -> dict[str, Artifact]:
    raw_artifacts = case.get("artifacts", {})
    if not isinstance(raw_artifacts, dict):
        integrity_errors.append(f"{case_label}.artifacts must be an object")
        return {}
    artifacts: dict[str, Artifact] = {}
    seen_paths: set[Path] = set()
    for key, descriptor in raw_artifacts.items():
        if not isinstance(key, str) or not ARTIFACT_KEY_RE.fullmatch(key):
            integrity_errors.append(f"{case_label} has an unsafe artifact key")
            continue
        if not isinstance(descriptor, dict):
            integrity_errors.append(f"{case_label}.artifacts.{key} must be an object")
            continue
        try:
            path = _resolve_inside(
                artifact_root,
                descriptor.get("path"),
                f"{case_label}.artifacts.{key}.path",
            )
            if not path.is_file():
                raise AuditError(f"{case_label}.artifacts.{key} is not a regular file")
            expected = _hash_value(
                descriptor.get("sha256"), f"{case_label}.artifacts.{key}.sha256"
            )
            raw = path.read_bytes()
        except (AuditError, OSError) as error:
            integrity_errors.append(str(error))
            continue
        actual = _sha256(raw)
        if path in seen_paths:
            integrity_errors.append(f"{case_label} maps multiple artifact roles to the same path")
            continue
        seen_paths.add(path)
        if actual != expected:
            integrity_errors.append(f"{case_label}.artifacts.{key} SHA-256 mismatch")
            continue
        declared_size = descriptor.get("size")
        if declared_size is not None and (
            not isinstance(declared_size, int) or isinstance(declared_size, bool) or declared_size != len(raw)
        ):
            integrity_errors.append(f"{case_label}.artifacts.{key} size mismatch")
            continue
        artifacts[key] = Artifact(key, path, expected, actual, len(raw), raw)
    return artifacts


def _artifact_reference(
    value: Any,
    default: str,
    artifacts: Mapping[str, Artifact],
) -> Artifact | None:
    key = default if value is None else value
    if not isinstance(key, str):
        return None
    return artifacts.get(key)


def _validate_tool_args(
    tool_id: str,
    args: Any,
    artifacts: Mapping[str, Artifact],
    staged: Mapping[str, Path],
) -> tuple[list[str], list[str]]:
    spec = TOOL_ALLOWLIST[tool_id]
    if not isinstance(args, list) or not all(isinstance(item, str) for item in args):
        raise AuditError("replay.args must be an array of strings")
    if any(len(item) > 4096 or "\x00" in item for item in args):
        raise AuditError("replay argument is empty, oversized, or contains NUL")
    required_positionals = spec["positional_artifacts"]
    if len(args) < len(required_positionals):
        raise AuditError("replay.args is missing required artifact placeholders")
    resolved: list[str] = []
    display: list[str] = []
    for index, expected_key in enumerate(required_positionals):
        match = PLACEHOLDER_RE.fullmatch(args[index])
        if match is None or match.group(1).lower() != expected_key:
            raise AuditError(
                f"replay positional {index + 1} must be ${{{expected_key.upper()}}}"
            )
        actual_key = next((key for key in artifacts if key.lower() == expected_key), None)
        if actual_key is None:
            raise AuditError(f"replay requires artifact role {expected_key}")
        resolved.append(str(staged[actual_key]))
        display.append(f"${{{expected_key.upper()}}}")

    option_specs: Mapping[str, int] = spec["options"]
    index = len(required_positionals)
    format_seen = False
    while index < len(args):
        option = args[index]
        if option not in option_specs:
            raise AuditError(f"replay option is not allowlisted for {tool_id}: {option}")
        arity = option_specs[option]
        resolved.append(option)
        display.append(option)
        if option == "--format":
            format_seen = True
        for offset in range(1, arity + 1):
            if index + offset >= len(args):
                raise AuditError(f"replay option {option} is missing its value")
            value = args[index + offset]
            placeholder = PLACEHOLDER_RE.fullmatch(value)
            if placeholder:
                artifact_key = placeholder.group(1)
                if artifact_key not in artifacts:
                    raise AuditError(f"unknown artifact placeholder: {artifact_key}")
                value = str(staged[artifact_key])
                display_value = f"${{ARTIFACT:{artifact_key}}}"
            else:
                display_value = value
            resolved.append(value)
            if option == "--warning-reviewer-id":
                display_value = "<redacted-reviewer-label>"
            display.append(display_value)
        index += arity + 1
    if format_seen:
        format_indexes = [i for i, value in enumerate(resolved) if value == "--format"]
        if len(format_indexes) != 1 or resolved[format_indexes[0] + 1] != "json":
            raise AuditError("allowlisted replays require exactly --format json")
    else:
        resolved.extend(("--format", "json"))
        display.extend(("--format", "json"))
    return resolved, display


def _static_replay_declaration_error(replay: Mapping[str, Any]) -> str | None:
    """Reject executable surfaces even when weak evidence is not eligible for replay."""

    forbidden = {"command", "argv", "executable", "shell", "powershell", "bash"}
    if forbidden.intersection(replay):
        return "contains a forbidden arbitrary-command field"
    tool_id = replay.get("tool_id")
    if tool_id not in TOOL_ALLOWLIST:
        return "tool_id is not allowlisted"
    args = replay.get("args")
    if not isinstance(args, list) or not all(isinstance(item, str) for item in args):
        return "args must be an array of strings"
    positional_count = len(TOOL_ALLOWLIST[str(tool_id)]["positional_artifacts"])
    if len(args) < positional_count:
        return "args lacks required artifact placeholders"
    option_specs: Mapping[str, int] = TOOL_ALLOWLIST[str(tool_id)]["options"]
    index = positional_count
    while index < len(args):
        option = args[index]
        if option not in option_specs:
            return f"option is not allowlisted: {option}"
        arity = option_specs[option]
        if index + arity >= len(args):
            return f"option is missing its value: {option}"
        index += arity + 1
    return None


def _expected_machine_result(replay: Mapping[str, Any]) -> tuple[dict[str, Any] | None, str | None]:
    expected_raw = replay.get("expected")
    if expected_raw is None:
        return None, "replay.expected is required for deterministic behavior comparison"
    if not isinstance(expected_raw, dict):
        return None, "replay.expected must be an object"
    expected = dict(expected_raw)
    if "expected_exit_code" in replay and "exit_code" not in expected:
        expected["exit_code"] = replay["expected_exit_code"]
    required = {"status", "delivery_gate_status", "exit_code", "academic_correctness"}
    if not required.issubset(expected):
        return None, "replay.expected lacks status/delivery/exit/academic fields"
    status = expected.get("status")
    delivery = expected.get("delivery_gate_status")
    exit_code = expected.get("exit_code")
    academic = expected.get("academic_correctness")
    if status not in MACHINE_EXIT or delivery != status or exit_code != MACHINE_EXIT.get(status):
        return None, "replay.expected violates PASS=0, FAIL=1, REVIEW=2"
    if academic != "NOT_EVALUATED":
        return None, "replay.expected.academic_correctness must be NOT_EVALUATED"
    return {
        "status": status,
        "delivery_gate_status": delivery,
        "exit_code": exit_code,
        "academic_correctness": academic,
    }, None


def _redacted_command(script: Path, display_args: Sequence[str]) -> list[str]:
    return [Path(sys.executable).name, "-I", script.name, *display_args]


def _run_replay(
    replay: Mapping[str, Any],
    artifacts: Mapping[str, Artifact],
    skill_root: Path,
    timeout: float,
    label: str,
    integrity_errors: list[str],
) -> dict[str, Any]:
    result: dict[str, Any] = {
        "label": label,
        "integrity_valid": False,
        "behavior_matches_expected": False,
    }
    forbidden = {"command", "argv", "executable", "shell", "powershell", "bash"}
    if forbidden.intersection(replay):
        integrity_errors.append(f"{label} contains a forbidden arbitrary-command field")
        return result
    tool_id = replay.get("tool_id")
    if tool_id not in TOOL_ALLOWLIST:
        integrity_errors.append(f"{label}.tool_id is not allowlisted")
        return result
    tool_relative = TOOL_ALLOWLIST[str(tool_id)]["relative_path"]
    try:
        script = _resolve_inside(skill_root, tool_relative, f"{label}.tool")
    except AuditError as error:
        integrity_errors.append(str(error))
        return result
    expected, expected_error = _expected_machine_result(replay)
    if expected_error:
        result["insufficient_reason"] = expected_error
        return result

    source_hashes = {key: _file_sha256(item.path) for key, item in artifacts.items()}
    with tempfile.TemporaryDirectory(prefix="humanize-qualification-") as temporary:
        temp_root = Path(temporary)
        staged: dict[str, Path] = {}
        for index, (key, artifact) in enumerate(sorted(artifacts.items())):
            suffix = artifact.path.suffix if len(artifact.path.suffix) <= 12 else ""
            staged_path = temp_root / f"artifact-{index:03d}{suffix}"
            staged_path.write_bytes(artifact.raw)
            staged[key] = staged_path
        try:
            resolved_args, display_args = _validate_tool_args(
                str(tool_id), replay.get("args"), artifacts, staged
            )
        except AuditError as error:
            integrity_errors.append(f"{label}: {error}")
            return result
        command = [sys.executable, "-I", str(script), *resolved_args]
        result["tool_id"] = tool_id
        result["resolved_argv_redacted"] = _redacted_command(script, display_args)
        try:
            completed = subprocess.run(
                command,
                cwd=temp_root,
                shell=False,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=timeout,
                env={**os.environ, "PYTHONUTF8": "1"},
                check=False,
            )
        except (OSError, subprocess.TimeoutExpired) as error:
            integrity_errors.append(f"{label} replay did not complete: {type(error).__name__}")
            return result

        result["actual_exit_code"] = completed.returncode
        result["stdout_sha256"] = _sha256(completed.stdout.encode("utf-8"))
        result["stderr_sha256"] = _sha256(completed.stderr.encode("utf-8"))
        try:
            payload = _strict_json_bytes(completed.stdout.encode("utf-8"), f"{label}.stdout")
            payload = _as_mapping(payload, f"{label}.stdout")
        except AuditError as error:
            integrity_errors.append(str(error))
            return result

        status = payload.get("status")
        delivery = payload.get("delivery_gate_status")
        json_exit = payload.get("exit_code")
        delivery_exit = payload.get("delivery_gate_exit_code")
        academic = payload.get("academic_correctness")
        actual = {
            "status": status,
            "delivery_gate_status": delivery,
            "exit_code": completed.returncode,
            "academic_correctness": academic,
        }
        result["actual"] = actual
        internally_valid = True
        if status not in MACHINE_EXIT:
            integrity_errors.append(f"{label} returned an unknown status")
            internally_valid = False
        elif delivery != status:
            integrity_errors.append(f"{label} status conflicts with delivery_gate_status")
            internally_valid = False
        elif completed.returncode != MACHINE_EXIT[status]:
            integrity_errors.append(f"{label} process exit conflicts with machine status")
            internally_valid = False
        if json_exit != completed.returncode or delivery_exit != completed.returncode:
            integrity_errors.append(f"{label} JSON exit code conflicts with the real process exit")
            internally_valid = False
        if academic != "NOT_EVALUATED":
            integrity_errors.append(f"{label} improperly claims academic correctness evaluation")
            internally_valid = False
        for field, allowed in (
            ("hard_invariant_layer_status", {"PASS", "FAIL"}),
            ("speech_act_layer_status", {"PASS", "REVIEW"}),
            ("style_signal_layer_status", {"PASS", "REVIEW"}),
        ):
            if payload.get(field) not in allowed:
                integrity_errors.append(f"{label} returned invalid {field}")
                internally_valid = False

        evidence = payload.get("evidence")
        if not isinstance(evidence, dict):
            integrity_errors.append(f"{label} lacks validator hash evidence")
            internally_valid = False
        else:
            for artifact_key, evidence_key in (("input", "before_sha256"), ("output", "after_sha256")):
                artifact = artifacts.get(artifact_key)
                if artifact is None or evidence.get(evidence_key) != artifact.actual_sha256:
                    integrity_errors.append(f"{label} validator {evidence_key} is not bound to the artifact")
                    internally_valid = False

        recorded = replay.get("recorded")
        if recorded is not None:
            if not isinstance(recorded, dict):
                integrity_errors.append(f"{label}.recorded must be an object")
                internally_valid = False
            else:
                for field, observed in actual.items():
                    if recorded.get(field) != observed:
                        integrity_errors.append(f"{label}.recorded.{field} conflicts with replay")
                        internally_valid = False

        for key, original_hash in source_hashes.items():
            try:
                after_hash = _file_sha256(artifacts[key].path)
            except OSError:
                after_hash = "MISSING"
            if after_hash != original_hash:
                integrity_errors.append(f"{label} modified source artifact {key}")
                internally_valid = False
        for key, staged_path in staged.items():
            if _file_sha256(staged_path) != artifacts[key].actual_sha256:
                integrity_errors.append(f"{label} modified staged artifact {key}")
                internally_valid = False

        result["integrity_valid"] = internally_valid
        result["behavior_matches_expected"] = internally_valid and all(
            actual[field] == expected[field] for field in expected
        )
        if internally_valid and not result["behavior_matches_expected"]:
            result["behavior_mismatch"] = {
                field: {"expected": expected[field], "actual": actual[field]}
                for field in expected
                if expected[field] != actual[field]
            }
    return result


def _bound_run_record_state(
    record_artifact: Artifact,
    artifacts: Mapping[str, Artifact],
    role_keys: Mapping[str, str],
    current_bindings: Mapping[str, str],
    label: str,
    *,
    expected_run_id: str | None = None,
    integrity_errors: list[str] | None = None,
) -> tuple[bool, dict[str, Any]]:
    """Validate a caller-attested run record against concrete artifact bytes."""

    state: dict[str, Any] = {"valid": False, "raw_run_sha256": record_artifact.actual_sha256}

    def reject(reason: str) -> tuple[bool, dict[str, Any]]:
        state["insufficient_reason"] = reason
        if integrity_errors is not None:
            integrity_errors.append(f"{label} {reason}")
        return False, state

    if set(role_keys) != {"input", "output", "prompt", "context"}:
        return reject("does not declare exactly input/output/prompt/context artifact roles")
    bound_artifacts: dict[str, Artifact] = {}
    for role, key in role_keys.items():
        artifact = artifacts.get(key)
        if artifact is None:
            return reject(f"references missing {role} artifact: {key}")
        bound_artifacts[role] = artifact
    try:
        record = _strict_json_bytes(record_artifact.raw, f"{label}.run_record")
    except AuditError as error:
        return reject(str(error))
    if not isinstance(record, dict):
        return reject("run record must be a JSON object")
    if record.get("schema_version") != GENERATION_RUN_RECORD_SCHEMA:
        return reject(f"run record schema must be {GENERATION_RUN_RECORD_SCHEMA}")
    run_id = record.get("run_id")
    if not isinstance(run_id, str) or not SAFE_ID_RE.fullmatch(run_id):
        return reject("run record has a missing or unsafe run_id")
    if expected_run_id is not None and run_id != expected_run_id:
        return reject("run record run_id does not match generation.run_id")
    if record.get("fresh_context") is not True:
        return reject("run record fresh_context is not true")
    if record.get("blindness_attestation") != BLINDNESS_ATTESTATION:
        return reject("run record blindness attestation is absent or overstated")
    artifact_hashes = record.get("artifact_sha256")
    expected_hashes = {
        role: artifact.actual_sha256 for role, artifact in bound_artifacts.items()
    }
    if artifact_hashes != expected_hashes:
        return reject("run record artifact hashes do not bind this case")
    public_artifact_hashes: dict[str, str] | None = None
    public_context = artifacts.get("public_context")
    if public_context is not None:
        public_artifact_hashes = {
            "input": bound_artifacts["input"].actual_sha256,
            "prompt": bound_artifacts["prompt"].actual_sha256,
            "public_context": public_context.actual_sha256,
        }
        if record.get("public_artifact_sha256") != public_artifact_hashes:
            return reject(
                "run record does not bind the generator-visible input/prompt/public_context seal"
            )
    if record.get("qualification_bindings") != dict(current_bindings):
        return reject(
            "run record does not bind the current Skill/contract/requirements/oracle catalog"
        )
    state.update(
        {
            "valid": True,
            "run_id": run_id,
            "fresh_context": True,
            "blindness_attestation": BLINDNESS_ATTESTATION,
            "artifact_sha256": expected_hashes,
            "qualification_bindings": dict(current_bindings),
            "public_artifact_sha256": public_artifact_hashes,
            "oracle_catalog_visible_to_generator": record.get(
                "oracle_catalog_visible_to_generator"
            ),
            "filesystem_isolation_verified": record.get(
                "filesystem_isolation_verified"
            ),
            "isolation_verification_source": record.get(
                "isolation_verification_source"
            ),
        }
    )
    return True, state


def _blind_forward_state(
    case: Mapping[str, Any],
    artifacts: Mapping[str, Artifact],
    e2_valid: bool,
    current_bindings: Mapping[str, str],
    run_ids: set[str],
    label: str,
    integrity_errors: list[str],
) -> tuple[bool, dict[str, Any]]:
    generation = case.get("generation")
    state: dict[str, Any] = {"valid": False}
    if not e2_valid or not isinstance(generation, dict):
        return False, state
    run_id = generation.get("run_id")
    if not isinstance(run_id, str) or not SAFE_ID_RE.fullmatch(run_id):
        state["insufficient_reason"] = "generation.run_id missing or unsafe"
        return False, state
    if run_id in run_ids:
        integrity_errors.append(f"duplicate generation.run_id: {run_id}")
        return False, state
    run_ids.add(run_id)
    role_keys = {
        "input": generation.get("input_artifact", "input"),
        "output": generation.get("output_artifact", "output"),
        "prompt": generation.get("prompt_artifact", "prompt"),
        "context": generation.get("context_artifact", "context"),
    }
    raw_run_key = generation.get("raw_run_artifact", "raw_run")
    if not all(isinstance(key, str) for key in (*role_keys.values(), raw_run_key)):
        state["insufficient_reason"] = "generation artifact references must be strings"
        return False, state
    missing = [role for role, key in role_keys.items() if key not in artifacts]
    if raw_run_key not in artifacts:
        missing.append("raw_run")
    if missing:
        state["insufficient_reason"] = "missing hashed E3 artifacts: " + ", ".join(missing)
        return False, state
    required_keys = [*role_keys.values(), raw_run_key]
    if any(artifacts[str(key)].size == 0 for key in required_keys):
        state["insufficient_reason"] = "E3 prompt/context/raw_run artifacts must be non-empty"
        return False, state
    if generation.get("fresh_context") is not True:
        state["insufficient_reason"] = "fresh_context is not true"
        return False, state
    if generation.get("blindness_attestation") != BLINDNESS_ATTESTATION:
        state["insufficient_reason"] = "blindness attestation is absent or overstated"
        return False, state
    raw_run = artifacts[str(raw_run_key)]
    if generation.get("raw_run_sha256") != raw_run.actual_sha256:
        integrity_errors.append(f"{label} generation.raw_run_sha256 does not bind raw_run")
        return False, state
    valid, run_state = _bound_run_record_state(
        raw_run,
        artifacts,
        {role: str(key) for role, key in role_keys.items()},
        current_bindings,
        label,
        expected_run_id=run_id,
        integrity_errors=integrity_errors,
    )
    if not valid:
        return False, run_state
    if (
        run_state.get("oracle_catalog_visible_to_generator") is not False
        or run_state.get("filesystem_isolation_verified") is not True
        or run_state.get("isolation_verification_source")
        != "HARNESS_VERIFIED_GENERATOR_PROJECTION"
    ):
        run_state.update(
            {
                "valid": False,
                "provenance_valid": True,
                "evidence_cap": "E2",
                "grader_source": "CALLER_DECLARED",
                "insufficient_reason": (
                    "generator oracle visibility/isolation is not harness-verified; "
                    "catalog binding alone cannot prove blindness"
                ),
            }
        )
        return False, run_state
    run_state.update(
        {
            "evidence_cap": "E3",
            "grader_source": "RULE_CHECK",
        }
    )
    return True, run_state


def _blind_review_state(
    case: Mapping[str, Any],
    artifacts: Mapping[str, Artifact],
    e3_valid: bool,
    forward_state: Mapping[str, Any],
    current_bindings: Mapping[str, str],
    ballot_ids: set[str],
    label: str,
    integrity_errors: list[str],
) -> tuple[bool, bool, dict[str, Any], set[str]]:
    """Return (E4 provenance valid, ballots pass, public state, reviewer hashes)."""

    review = case.get("blind_review")
    state: dict[str, Any] = {"valid": False}
    if not e3_valid or forward_state.get("valid") is not True or not isinstance(review, dict):
        return False, False, state, set()
    rubric = _artifact_reference(review.get("rubric_artifact"), "rubric", artifacts)
    bundle = _artifact_reference(review.get("bundle_artifact"), "bundle", artifacts)
    if rubric is None or bundle is None or rubric.size == 0 or bundle.size == 0:
        state["insufficient_reason"] = "blind review lacks hashed rubric or anonymous bundle"
        return False, False, state, set()
    forward_hashes = forward_state.get("artifact_sha256")
    if not isinstance(forward_hashes, dict):
        state["insufficient_reason"] = "blind review lacks a bound forward run"
        return False, False, state, set()
    expected_generation_binding = {
        "run_id": forward_state.get("run_id"),
        "run_record_sha256": forward_state.get("raw_run_sha256"),
        "output_sha256": forward_hashes.get("output"),
        "prompt_sha256": forward_hashes.get("prompt"),
        "context_sha256": forward_hashes.get("context"),
        "skill_snapshot_sha256": current_bindings.get("skill_snapshot_sha256"),
        "oracle_catalog_sha256": current_bindings.get("oracle_catalog_sha256"),
    }
    if review.get("generation_binding") != expected_generation_binding:
        integrity_errors.append(f"{label} blind review is not bound to the current generation run")
        return False, False, state, set()
    ballots = review.get("ballots")
    if not isinstance(ballots, list) or len(ballots) < 2:
        state["insufficient_reason"] = "blind review requires two HUMAN ballots"
        return False, False, state, set()
    reviewers: set[str] = set()
    outcomes: list[str] = []
    structurally_valid = True
    public_ballots: list[dict[str, Any]] = []
    for index, ballot in enumerate(ballots):
        ballot_label = f"{label}.blind_review.ballots[{index}]"
        if not isinstance(ballot, dict):
            integrity_errors.append(f"{ballot_label} must be an object")
            structurally_valid = False
            continue
        if "reviewer_id" in ballot:
            integrity_errors.append(f"{ballot_label} must not store a raw reviewer identity")
            structurally_valid = False
        ballot_id = ballot.get("ballot_id")
        if not isinstance(ballot_id, str) or not SAFE_ID_RE.fullmatch(ballot_id):
            integrity_errors.append(f"{ballot_label}.ballot_id missing or unsafe")
            structurally_valid = False
        elif ballot_id in ballot_ids:
            integrity_errors.append(f"duplicate ballot_id: {ballot_id}")
            structurally_valid = False
        else:
            ballot_ids.add(ballot_id)
        try:
            reviewer_hash = _hash_value(
                ballot.get("reviewer_id_sha256"), f"{ballot_label}.reviewer_id_sha256"
            )
        except AuditError as error:
            integrity_errors.append(str(error))
            structurally_valid = False
            continue
        if ballot.get("reviewer_kind") != "HUMAN":
            integrity_errors.append(f"{ballot_label}.reviewer_kind must be HUMAN")
            structurally_valid = False
        if ballot.get("identity_verified") is not False:
            integrity_errors.append(f"{ballot_label}.identity_verified must be false")
            structurally_valid = False
        if ballot.get("attestation_status") != "CALLER_ASSERTED_HUMAN_REVIEW":
            integrity_errors.append(f"{ballot_label} lacks caller-attested HUMAN provenance")
            structurally_valid = False
        if ballot.get("rubric_sha256") != rubric.actual_sha256:
            integrity_errors.append(f"{ballot_label} is not bound to the rubric")
            structurally_valid = False
        if ballot.get("bundle_sha256") != bundle.actual_sha256:
            integrity_errors.append(f"{ballot_label} is not bound to the anonymous bundle")
            structurally_valid = False
        if ballot.get("generation_binding") != expected_generation_binding:
            integrity_errors.append(f"{ballot_label} is not bound to the current run/output")
            structurally_valid = False
        outcome = ballot.get("result")
        if outcome not in {"PASS", "FAIL"}:
            integrity_errors.append(f"{ballot_label}.result must be PASS or FAIL")
            structurally_valid = False
        else:
            outcomes.append(str(outcome))
        reviewers.add(reviewer_hash)
        public_ballots.append(
            {
                "ballot_id": ballot_id,
                "reviewer_kind": ballot.get("reviewer_kind"),
                "reviewer_id_sha256": reviewer_hash,
                "identity_verified": False,
                "result": outcome,
            }
        )
    if len(reviewers) < 2:
        integrity_errors.append(f"{label} blind review reuses a reviewer identity")
        structurally_valid = False
    state.update(
        {
            "valid": structurally_valid,
            "rubric_sha256": rubric.actual_sha256,
            "bundle_sha256": bundle.actual_sha256,
            "generation_binding": expected_generation_binding,
            "distinct_human_reviewers": len(reviewers),
            "identity_verified": False,
            "ballots": public_ballots,
        }
    )
    return structurally_valid, structurally_valid and all(x == "PASS" for x in outcomes), state, reviewers


def _measurement_run_state(
    entry: Any,
    artifacts: Mapping[str, Artifact],
    current_bindings: Mapping[str, str],
    label: str,
) -> tuple[bool, dict[str, Any]]:
    if not isinstance(entry, dict):
        return False, {"valid": False, "insufficient_reason": "run entry must be an object"}
    role_keys = {
        "input": entry.get("input_artifact"),
        "output": entry.get("output_artifact"),
        "prompt": entry.get("prompt_artifact"),
        "context": entry.get("context_artifact"),
    }
    raw_run_key = entry.get("run_record_artifact")
    if not all(isinstance(key, str) for key in (*role_keys.values(), raw_run_key)):
        return False, {
            "valid": False,
            "insufficient_reason": "run entry must name all five artifacts",
        }
    raw_run = artifacts.get(str(raw_run_key))
    if raw_run is None:
        return False, {"valid": False, "insufficient_reason": "run record artifact is missing"}
    return _bound_run_record_state(
        raw_run,
        artifacts,
        {role: str(key) for role, key in role_keys.items()},
        current_bindings,
        label,
    )


def _idempotency_measurement(
    case: Mapping[str, Any],
    artifacts: Mapping[str, Artifact],
    current_bindings: Mapping[str, str],
    forward_state: Mapping[str, Any],
) -> tuple[bool | None, dict[str, Any]]:
    measurement = case.get("idempotency")
    if not isinstance(measurement, dict):
        return None, {"status": "NOT_PROVIDED"}
    if measurement.get("independence_attestation") != INDEPENDENCE_ATTESTATION:
        return None, {"status": "MISSING_INDEPENDENCE_ATTESTATION"}
    first_valid, first = _measurement_run_state(
        measurement.get("first"), artifacts, current_bindings, "idempotency.first"
    )
    second_valid, second = _measurement_run_state(
        measurement.get("second"), artifacts, current_bindings, "idempotency.second"
    )
    if not first_valid or not second_valid:
        return None, {"status": "INVALID_RUN_EVIDENCE", "first": first, "second": second}
    if (
        forward_state.get("valid") is not True
        or first["run_id"] != forward_state.get("run_id")
        or first["raw_run_sha256"] != forward_state.get("raw_run_sha256")
        or first["artifact_sha256"] != forward_state.get("artifact_sha256")
    ):
        return None, {"status": "FIRST_RUN_NOT_BOUND_TO_CASE_GENERATION"}
    if (
        first["run_id"] == second["run_id"]
        or first["raw_run_sha256"] == second["raw_run_sha256"]
    ):
        return None, {
            "status": "NON_INDEPENDENT_RUNS",
            "independence": INDEPENDENCE_ATTESTATION,
        }
    first_hashes = first["artifact_sha256"]
    second_hashes = second["artifact_sha256"]
    if (
        first_hashes["prompt"] != second_hashes["prompt"]
        or first_hashes["context"] != second_hashes["context"]
        or second_hashes["input"] != first_hashes["output"]
    ):
        return None, {"status": "IDEMPOTENCY_CHAIN_MISMATCH"}
    first_entry = measurement["first"]
    second_entry = measurement["second"]
    first_output = artifacts[str(first_entry["output_artifact"])]
    second_output = artifacts[str(second_entry["output_artifact"])]
    same = first_output.raw == second_output.raw
    return same, {
        "status": "PASS" if same else "FAIL",
        "first_run_id": first["run_id"],
        "second_run_id": second["run_id"],
        "first_raw_run_sha256": first["raw_run_sha256"],
        "second_raw_run_sha256": second["raw_run_sha256"],
        "first_sha256": first_output.actual_sha256,
        "second_sha256": second_output.actual_sha256,
        "substantive_patch_empty": same,
        "independence": INDEPENDENCE_ATTESTATION,
    }


def _route_stability_measurement(
    case: Mapping[str, Any],
    artifacts: Mapping[str, Artifact],
    current_bindings: Mapping[str, str],
    forward_state: Mapping[str, Any],
) -> tuple[bool | None, dict[str, Any]]:
    measurement = case.get("route_stability")
    if not isinstance(measurement, dict):
        return None, {"status": "NOT_PROVIDED"}
    if measurement.get("independence_attestation") != INDEPENDENCE_ATTESTATION:
        return None, {"status": "MISSING_INDEPENDENCE_ATTESTATION"}
    runs = measurement.get("runs")
    if not isinstance(runs, list) or len(runs) < 3:
        return None, {"status": "INSUFFICIENT_RUNS"}
    observations: list[dict[str, Any]] = []
    run_states: list[dict[str, Any]] = []
    for index, entry in enumerate(runs):
        valid, run_state = _measurement_run_state(
            entry, artifacts, current_bindings, f"route_stability.runs[{index}]"
        )
        if not valid:
            return None, {
                "status": "INVALID_RUN_EVIDENCE",
                "index": index,
                "run": run_state,
            }
        observation_key = entry.get("observation_artifact") if isinstance(entry, dict) else None
        artifact = artifacts.get(observation_key)
        if artifact is None:
            return None, {"status": "MISSING_OBSERVATION", "index": index}
        try:
            payload = _strict_json_bytes(artifact.raw, f"route observation {observation_key}")
        except AuditError:
            return None, {"status": "INVALID_OBSERVATION", "artifact": observation_key}
        if (
            not isinstance(payload, dict)
            or payload.get("schema_version") != ROUTE_OBSERVATION_SCHEMA
            or payload.get("run_id") != run_state["run_id"]
            or payload.get("run_record_sha256") != run_state["raw_run_sha256"]
            or payload.get("oracle_catalog_sha256")
            != current_bindings.get("oracle_catalog_sha256")
            or not all(
            field in payload for field in ("scene", "roles", "decisions", "owners")
            )
        ):
            return None, {"status": "UNBOUND_OBSERVATION", "artifact": observation_key}
        observations.append(
            {
                field: payload[field] for field in ("scene", "roles", "decisions", "owners")
            }
        )
        run_states.append(run_state)
    run_ids = [item["run_id"] for item in run_states]
    raw_run_hashes = [item["raw_run_sha256"] for item in run_states]
    if len(set(run_ids)) != len(run_ids) or len(set(raw_run_hashes)) != len(raw_run_hashes):
        return None, {
            "status": "NON_INDEPENDENT_RUNS",
            "run_ids": run_ids,
            "raw_run_sha256": raw_run_hashes,
        }
    if forward_state.get("valid") is not True or not any(
        item["run_id"] == forward_state.get("run_id")
        and item["raw_run_sha256"] == forward_state.get("raw_run_sha256")
        and item["artifact_sha256"] == forward_state.get("artifact_sha256")
        for item in run_states
    ):
        return None, {"status": "NO_RUN_BOUND_TO_CASE_GENERATION"}
    provenance = [
        (
            item["artifact_sha256"]["input"],
            item["artifact_sha256"]["prompt"],
            item["artifact_sha256"]["context"],
        )
        for item in run_states
    ]
    if len(set(provenance)) != 1:
        return None, {"status": "ROUTE_PROVENANCE_MISMATCH"}
    fingerprints = [_sha256(_canonical_json(item)) for item in observations]
    stable = len(set(fingerprints)) == 1
    return stable, {
        "status": "PASS" if stable else "FAIL",
        "runs": len(observations),
        "run_ids": run_ids,
        "raw_run_sha256": raw_run_hashes,
        "observation_sha256": fingerprints,
        "scene_role_decision_owner_stable": stable,
        "independence": INDEPENDENCE_ATTESTATION,
    }


def _span_side(
    side: Any,
    artifacts: Mapping[str, Artifact],
) -> tuple[bytes, dict[str, Any]] | None:
    if not isinstance(side, dict):
        return None
    artifact = artifacts.get(side.get("artifact"))
    start, end = side.get("start"), side.get("end")
    if (
        artifact is None
        or not isinstance(start, int)
        or isinstance(start, bool)
        or not isinstance(end, int)
        or isinstance(end, bool)
        or start < 0
        or end <= start
        or end > len(artifact.raw)
    ):
        return None
    raw = artifact.raw[start:end]
    digest = _sha256(raw)
    try:
        declared = _hash_value(side.get("sha256"), "protected span sha256")
    except AuditError:
        return None
    if declared != digest:
        return None
    return raw, {
        "artifact": artifact.key,
        "start": start,
        "end": end,
        "sha256": digest,
    }


def _protected_hash_measurement(
    case: Mapping[str, Any], artifacts: Mapping[str, Artifact]
) -> tuple[bool | None, dict[str, Any]]:
    spans = case.get("protected_spans")
    if not isinstance(spans, list) or not spans:
        return None, {"status": "NOT_PROVIDED"}
    records: list[dict[str, Any]] = []
    ids: set[str] = set()
    all_same = True
    for index, span in enumerate(spans):
        if not isinstance(span, dict):
            return None, {"status": "INVALID_SPAN", "index": index}
        span_id = span.get("id")
        if not isinstance(span_id, str) or not SAFE_ID_RE.fullmatch(span_id) or span_id in ids:
            return None, {"status": "INVALID_SPAN_ID", "index": index}
        ids.add(span_id)
        before = _span_side(span.get("before"), artifacts)
        after = _span_side(span.get("after"), artifacts)
        if before is None or after is None:
            return None, {"status": "INVALID_SPAN", "id": span_id}
        same = before[0] == after[0]
        all_same = all_same and same
        records.append({"id": span_id, "before": before[1], "after": after[1], "same": same})
    return all_same, {
        "status": "PASS" if all_same else "FAIL",
        "protected_hash_changes": sum(not record["same"] for record in records),
        "spans": records,
    }


def _case_bindings(
    case: Mapping[str, Any],
    top_bindings: Any,
    current: Mapping[str, str],
    label: str,
    integrity_errors: list[str],
) -> bool:
    declared = case.get("bindings", top_bindings)
    generation = case.get("generation")
    if isinstance(generation, dict) and "skill_snapshot_sha256" in generation:
        generation_hash = generation.get("skill_snapshot_sha256")
        if not isinstance(declared, dict):
            declared = {}
        declared = dict(declared)
        existing = declared.get("skill_snapshot_sha256")
        if existing is not None and existing != generation_hash:
            integrity_errors.append(f"{label} generation and case skill bindings conflict")
            return False
        declared["skill_snapshot_sha256"] = generation_hash
    return _binding_state(declared, current, f"{label}.bindings", integrity_errors)


def _case_assertions_and_claims(
    case: Mapping[str, Any],
    atoms: Mapping[str, Atom],
    case_id: str,
    global_claim_ids: set[str],
    global_assertion_ids: set[str],
    global_claimed_atom_ids: set[str],
    integrity_errors: list[str],
) -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]]]:
    assertions_raw = case.get("assertions", [])
    claims_raw = case.get("claims", case.get("coverage_claims", []))
    if "claims" in case and "coverage_claims" in case:
        integrity_errors.append(f"{case_id} cannot define both claims and coverage_claims")
    if not isinstance(assertions_raw, list) or not isinstance(claims_raw, list):
        integrity_errors.append(f"{case_id} claims and assertions must be arrays")
        return [], {}
    assertions: dict[str, dict[str, Any]] = {}
    for index, assertion in enumerate(assertions_raw):
        if not isinstance(assertion, dict):
            integrity_errors.append(f"{case_id}.assertions[{index}] must be an object")
            continue
        try:
            assertion_id = _safe_id(assertion.get("id"), f"{case_id}.assertions[{index}].id")
        except AuditError as error:
            integrity_errors.append(str(error))
            continue
        if assertion_id in global_assertion_ids:
            integrity_errors.append(f"duplicate assertion id: {assertion_id}")
            continue
        global_assertion_ids.add(assertion_id)
        if assertion.get("result") not in {"PASS", "FAIL", "NOT_EVALUATED"}:
            integrity_errors.append(f"{assertion_id}.result must be PASS, FAIL, or NOT_EVALUATED")
            continue
        assertions[assertion_id] = dict(assertion)

    claims: list[dict[str, Any]] = []
    referenced: set[str] = set()
    for index, claim in enumerate(claims_raw):
        if not isinstance(claim, dict):
            integrity_errors.append(f"{case_id}.claims[{index}] must be an object")
            continue
        try:
            claim_id = _safe_id(claim.get("claim_id"), f"{case_id}.claims[{index}].claim_id")
        except AuditError as error:
            integrity_errors.append(str(error))
            continue
        if claim_id in global_claim_ids:
            integrity_errors.append(f"duplicate claim id: {claim_id}")
            continue
        global_claim_ids.add(claim_id)
        atom_id = claim.get("atom_id")
        if atom_id not in atoms:
            integrity_errors.append(f"{claim_id} references unknown atom: {atom_id}")
            continue
        if atom_id in global_claimed_atom_ids:
            integrity_errors.append(f"duplicate coverage atom: {atom_id}")
            continue
        assertion_ids = claim.get("assertion_ids")
        if not isinstance(assertion_ids, list) or not assertion_ids or not all(
            isinstance(item, str) for item in assertion_ids
        ):
            integrity_errors.append(f"{claim_id}.assertion_ids must be a non-empty string array")
            continue
        if len(set(assertion_ids)) != len(assertion_ids):
            integrity_errors.append(f"{claim_id} repeats an assertion id")
            continue
        missing = [item for item in assertion_ids if item not in assertions]
        reused = [item for item in assertion_ids if item in referenced]
        if missing:
            integrity_errors.append(f"{claim_id} references missing assertions: {missing}")
            continue
        if reused:
            integrity_errors.append(f"{claim_id} reuses assertions already bound to another atom: {reused}")
            continue
        referenced.update(assertion_ids)
        global_claimed_atom_ids.add(str(atom_id))
        claims.append(
            {
                "claim_id": claim_id,
                "atom_id": atom_id,
                "assertion_ids": list(assertion_ids),
            }
        )
    unreferenced = sorted(set(assertions) - referenced)
    if unreferenced:
        integrity_errors.append(f"{case_id} contains unbound assertions: {unreferenced}")
    return claims, assertions


def _validate_v2_case_shape(
    case: Mapping[str, Any],
    case_id: str,
    integrity_errors: list[str],
) -> None:
    forbidden = _forbidden_manifest_paths(case, case_id)
    if forbidden:
        integrity_errors.append(
            f"{case_id} v2 forbids caller-owned grading fields: {', '.join(sorted(forbidden))}"
        )
    allowed = {
        "id",
        "artifacts",
        "bindings",
        "generation",
        "claims",
        "reviews",
    }
    extra = sorted(set(case) - allowed)
    if extra:
        integrity_errors.append(f"{case_id} v2 has unknown fields: {extra}")
    generation = case.get("generation")
    if generation is not None:
        if not isinstance(generation, dict):
            integrity_errors.append(f"{case_id}.generation must be an object")
        else:
            generation_allowed = {
                "run_id",
                "raw_run_artifact",
                "raw_run_sha256",
                "input_artifact",
                "output_artifact",
                "prompt_artifact",
                "context_artifact",
                "fresh_context",
                "blindness_attestation",
                "skill_snapshot_sha256",
            }
            generation_extra = sorted(set(generation) - generation_allowed)
            if generation_extra:
                integrity_errors.append(
                    f"{case_id}.generation has unknown fields: {generation_extra}"
                )
            for role in ("input", "output", "prompt", "context"):
                field = f"{role}_artifact"
                if generation.get(field, role) != role:
                    integrity_errors.append(
                        f"{case_id}.generation cannot remap canonical artifact role {role}"
                    )
            if generation.get("raw_run_artifact", "raw_run") != "raw_run":
                integrity_errors.append(
                    f"{case_id}.generation cannot remap canonical artifact role raw_run"
                )
    reviews = case.get("reviews", [])
    if not isinstance(reviews, list):
        integrity_errors.append(f"{case_id}.reviews must be an array")
    else:
        for index, review in enumerate(reviews):
            if not isinstance(review, dict) or set(review) != {"artifact"}:
                integrity_errors.append(
                    f"{case_id}.reviews[{index}] must contain exactly artifact"
                )
            elif not isinstance(review.get("artifact"), str):
                integrity_errors.append(f"{case_id}.reviews[{index}].artifact must be a string")


def _case_oracle_claims(
    case: Mapping[str, Any],
    atoms: Mapping[str, Atom],
    catalog: OracleCatalog,
    case_id: str,
    global_claim_ids: set[str],
    global_claimed_atom_ids: set[str],
    integrity_errors: list[str],
) -> list[dict[str, Any]]:
    claims_raw = case.get("claims", [])
    if not isinstance(claims_raw, list):
        integrity_errors.append(f"{case_id}.claims must be an array")
        return []
    claims: list[dict[str, Any]] = []
    for index, raw_claim in enumerate(claims_raw):
        label = f"{case_id}.claims[{index}]"
        if not isinstance(raw_claim, dict):
            integrity_errors.append(f"{label} must be an object")
            continue
        if set(raw_claim) != {"claim_id", "atom_id", "oracle_suite_id"}:
            integrity_errors.append(
                f"{label} must contain exactly claim_id/atom_id/oracle_suite_id"
            )
            continue
        try:
            claim_id = _safe_id(raw_claim.get("claim_id"), f"{label}.claim_id")
            suite_id = _safe_id(
                raw_claim.get("oracle_suite_id"), f"{label}.oracle_suite_id"
            )
        except AuditError as error:
            integrity_errors.append(str(error))
            continue
        if claim_id in global_claim_ids:
            integrity_errors.append(f"duplicate claim id: {claim_id}")
            continue
        global_claim_ids.add(claim_id)
        atom_id = raw_claim.get("atom_id")
        if atom_id not in atoms:
            integrity_errors.append(f"{claim_id} references unknown atom: {atom_id}")
            continue
        if atom_id in global_claimed_atom_ids:
            integrity_errors.append(f"duplicate coverage atom: {atom_id}")
            continue
        suite = catalog.suites.get(suite_id)
        if suite is None:
            integrity_errors.append(f"{claim_id} references unknown oracle suite: {suite_id}")
            continue
        if suite.get("atom_id") != atom_id:
            integrity_errors.append(
                f"{claim_id} atom/suite mismatch: {atom_id} vs {suite.get('atom_id')}"
            )
            continue
        global_claimed_atom_ids.add(str(atom_id))
        claims.append(
            {
                "claim_id": claim_id,
                "atom_id": atom_id,
                "oracle_suite_id": suite_id,
                "oracle_suite_sha256": catalog.suite_sha256[suite_id],
            }
        )
    return claims


def _suite_fixture_state(
    suite: Mapping[str, Any],
    artifacts: Mapping[str, Artifact],
    suite_id: str,
    integrity_errors: list[str],
) -> tuple[bool, list[dict[str, Any]]]:
    records: list[dict[str, Any]] = []
    valid = True
    fixtures = _as_mapping(suite.get("fixture_bindings"), f"{suite_id}.fixture_bindings")
    for role, raw_descriptor in fixtures.items():
        descriptor = _as_mapping(raw_descriptor, f"{suite_id}.fixture_bindings.{role}")
        expected = str(descriptor.get("sha256"))
        artifact = artifacts.get(role)
        matches = artifact is not None and artifact.actual_sha256 == expected
        records.append(
            {
                "role": role,
                "expected_sha256": expected,
                "actual_sha256": artifact.actual_sha256 if artifact else None,
                "matches": matches,
            }
        )
        if not matches:
            integrity_errors.append(f"{suite_id} fixture binding mismatch for role {role}")
            valid = False
    return valid, records


def _decode_utf8_artifact(
    artifact: Artifact | None,
    label: str,
    integrity_errors: list[str],
) -> str | None:
    if artifact is None:
        integrity_errors.append(f"{label} artifact is missing")
        return None
    try:
        return artifact.raw.decode("utf-8")
    except UnicodeError:
        integrity_errors.append(f"{label} is not strict UTF-8")
        return None


def _paragraph_sentence_counts(text: str) -> list[int]:
    paragraphs = [
        paragraph.strip()
        for paragraph in re.split(r"(?:\r?\n)[ \t]*(?:\r?\n)+", text.strip())
        if paragraph.strip()
    ]
    counts: list[int] = []
    for paragraph in paragraphs:
        segments = [
            item.strip()
            for item in re.split(r"(?<=[。！？!?])", paragraph)
            if item.strip()
        ]
        counts.append(len(segments))
    return counts


def _evaluate_oracle_check(
    check_id: str,
    catalog: OracleCatalog,
    artifacts: Mapping[str, Artifact],
    skill_root: Path,
    timeout: float,
    integrity_errors: list[str],
) -> dict[str, Any]:
    check = catalog.checks[check_id]
    check_type = str(check["type"])
    config = _as_mapping(check["configuration"], f"{check_id}.configuration")
    report: dict[str, Any] = {
        "check_id": check_id,
        "check_sha256": catalog.check_sha256[check_id],
        "type": check_type,
        "source": check["source"],
        "grader_source": "DETERMINISTIC",
        "integrity_valid": False,
        "status": "NOT_EVALUATED",
    }
    if check_type == "replay_result":
        replay = _run_replay(
            config,
            artifacts,
            skill_root,
            timeout,
            f"oracle:{check_id}",
            integrity_errors,
        )
        report["integrity_valid"] = replay.get("integrity_valid") is True
        report["status"] = (
            "PASS"
            if replay.get("behavior_matches_expected") is True
            else "FAIL"
            if replay.get("integrity_valid") is True
            else "NOT_EVALUATED"
        )
        report["observation"] = replay
        return report
    if check_type == "utf8_literal":
        report["grader_source"] = "RULE_CHECK"
        role = str(config["artifact_role"])
        text = _decode_utf8_artifact(
            artifacts.get(role), f"oracle:{check_id}:{role}", integrity_errors
        )
        if text is None:
            return report
        observations: list[dict[str, Any]] = []
        passed = True
        for kind in ("required", "forbidden"):
            for rule in config.get(kind, []):
                literal = str(rule["literal"])
                count = text.count(literal)
                minimum = int(rule.get("minimum_occurrences", 0))
                maximum = rule.get("maximum_occurrences")
                matches = count >= minimum and (
                    maximum is None or count <= int(maximum)
                )
                observations.append(
                    {
                        "kind": kind,
                        "literal_sha256": _sha256(literal.encode("utf-8")),
                        "occurrences": count,
                        "matches": matches,
                    }
                )
                passed = passed and matches
        report.update(
            {
                "integrity_valid": True,
                "status": "PASS" if passed else "FAIL",
                "observation": observations,
            }
        )
        return report
    if check_type == "artifact_relation":
        report["grader_source"] = "RULE_CHECK"
        before = _decode_utf8_artifact(
            artifacts.get(str(config["before_role"])),
            f"oracle:{check_id}:before",
            integrity_errors,
        )
        after = _decode_utf8_artifact(
            artifacts.get(str(config["after_role"])),
            f"oracle:{check_id}:after",
            integrity_errors,
        )
        if before is None or after is None:
            return report
        literal = str(config["literal"])
        before_count = before.count(literal)
        after_count = after.count(literal)
        minimum = int(config["minimum_occurrences"])
        passed = before_count == after_count and before_count >= minimum
        report.update(
            {
                "integrity_valid": True,
                "status": "PASS" if passed else "FAIL",
                "observation": {
                    "literal_sha256": _sha256(literal.encode("utf-8")),
                    "before_occurrences": before_count,
                    "after_occurrences": after_count,
                    "byte_equal": passed,
                },
            }
        )
        return report
    if check_type == "structure_relation":
        report["grader_source"] = "RULE_CHECK"
        before = _decode_utf8_artifact(
            artifacts.get(str(config["input_role"])),
            f"oracle:{check_id}:input",
            integrity_errors,
        )
        after = _decode_utf8_artifact(
            artifacts.get(str(config["output_role"])),
            f"oracle:{check_id}:output",
            integrity_errors,
        )
        if before is None or after is None:
            return report
        before_counts = _paragraph_sentence_counts(before)
        after_counts = _paragraph_sentence_counts(after)
        minimum = int(config["minimum_paragraphs"])
        input_grid = len(before_counts) >= minimum and len(set(before_counts)) == 1
        output_changed = len(after_counts) >= minimum and len(set(after_counts)) > 1
        passed = input_grid and output_changed
        report.update(
            {
                "integrity_valid": True,
                "status": "PASS" if passed else "FAIL",
                "observation": {
                    "input_paragraphs": len(before_counts),
                    "output_paragraphs": len(after_counts),
                    "input_sentence_counts": before_counts,
                    "output_sentence_counts": after_counts,
                    "input_uniform": input_grid,
                    "output_nonuniform": output_changed,
                },
            }
        )
        return report
    if check_type == "json_value":
        role = str(config["artifact_role"])
        artifact = artifacts.get(role)
        if artifact is None:
            integrity_errors.append(f"oracle:{check_id}:{role} artifact is missing")
            return report
        try:
            value: Any = _strict_json_bytes(artifact.raw, f"oracle:{check_id}:{role}")
            for part in config["path"]:
                if not isinstance(value, dict) or part not in value:
                    report.update({"integrity_valid": True, "status": "FAIL"})
                    report["observation"] = {"path_present": False}
                    return report
                value = value[part]
        except AuditError as error:
            integrity_errors.append(str(error))
            return report
        expected = config["expected"]
        if config["operator"] == "ARRAY_SET_EQUALS":
            passed = (
                isinstance(value, list)
                and len(value) == len(set(value))
                and set(value) == set(expected)
            )
        else:
            passed = value == expected
        report.update(
            {
                "integrity_valid": True,
                "status": "PASS" if passed else "FAIL",
                "observation": {
                    "path_present": True,
                    "observed_sha256": _sha256(_canonical_json(value)),
                },
            }
        )
        return report
    if check_type == "measurement_result":
        annotation_key = str(config["annotation_artifact"])
        annotation = artifacts.get(annotation_key)
        if annotation is None:
            integrity_errors.append(f"oracle:{check_id} annotation artifact is missing")
            return report
        try:
            spans = _strict_json_bytes(annotation.raw, f"oracle:{check_id}:annotation")
        except AuditError as error:
            integrity_errors.append(str(error))
            return report
        value, state = _protected_hash_measurement({"protected_spans": spans}, artifacts)
        structurally_valid = value is not None
        if not structurally_valid:
            integrity_errors.append(f"oracle:{check_id} protected span annotation is invalid")
        report.update(
            {
                "integrity_valid": structurally_valid,
                "status": (
                    "PASS"
                    if structurally_valid and state.get("status") == config["expected_status"]
                    else "FAIL"
                    if structurally_valid
                    else "NOT_EVALUATED"
                ),
                "observation": state,
            }
        )
        return report
    integrity_errors.append(f"oracle:{check_id} unsupported evaluator reached runtime")
    return report


def _review_artifact_state(
    artifact: Artifact,
    *,
    case_id: str,
    suite_id: str,
    rubric_id: str,
    rubric: Mapping[str, Any],
    rubric_sha256: str,
    catalog: OracleCatalog,
    artifacts: Mapping[str, Artifact],
    forward_state: Mapping[str, Any],
    integrity_errors: list[str],
) -> dict[str, Any]:
    state: dict[str, Any] = {
        "artifact": artifact.key,
        "artifact_sha256": artifact.actual_sha256,
        "valid": False,
        "status": "NOT_EVALUATED",
        "identity_verified": False,
    }
    try:
        review = _as_mapping(
            _strict_json_bytes(artifact.raw, f"oracle review {artifact.key}"),
            f"oracle review {artifact.key}",
        )
        _exact_keys(
            review,
            {
                "schema_version",
                "review_id",
                "case_id",
                "suite_id",
                "rubric_id",
                "reviewer",
                "bindings",
                "answers",
            },
            f"oracle review {artifact.key}",
        )
        if review.get("schema_version") != ORACLE_REVIEW_SCHEMA:
            raise AuditError(f"oracle review {artifact.key} schema is invalid")
        _safe_id(review.get("review_id"), f"oracle review {artifact.key}.review_id")
        if (
            review.get("case_id") != case_id
            or review.get("suite_id") != suite_id
            or review.get("rubric_id") != rubric_id
        ):
            raise AuditError(f"oracle review {artifact.key} case/suite/rubric binding mismatch")
        reviewer = _as_mapping(review.get("reviewer"), f"oracle review {artifact.key}.reviewer")
        _exact_keys(
            reviewer,
            {
                "kind",
                "id_sha256",
                "identity_verified",
                "provenance",
                "review_run_id",
                "expected_answers_staged",
            },
            f"oracle review {artifact.key}.reviewer",
        )
        kind = reviewer.get("kind")
        if kind not in rubric["reviewer_kinds"]:
            raise AuditError(f"oracle review {artifact.key} reviewer kind is not allowed")
        reviewer_hash = _hash_value(
            reviewer.get("id_sha256"), f"oracle review {artifact.key}.reviewer.id_sha256"
        )
        if reviewer.get("identity_verified") is not False:
            raise AuditError(f"oracle review {artifact.key} cannot claim verified identity")
        if reviewer.get("provenance") != "CALLER_DECLARED":
            raise AuditError(f"oracle review {artifact.key} provenance must be CALLER_DECLARED")
        review_run_id = _safe_id(
            reviewer.get("review_run_id"),
            f"oracle review {artifact.key}.reviewer.review_run_id",
        )
        if (
            kind == "MODEL"
            and (
                review_run_id == forward_state.get("run_id")
                or reviewer.get("expected_answers_staged") is not False
            )
        ):
            raise AuditError(f"oracle review {artifact.key} model review is not independent")
        bindings = _as_mapping(review.get("bindings"), f"oracle review {artifact.key}.bindings")
        _exact_keys(
            bindings,
            {
                "input_sha256",
                "output_sha256",
                "generation_run_record_sha256",
                "anonymous_bundle_sha256",
                "rubric_sha256",
                "oracle_catalog_sha256",
            },
            f"oracle review {artifact.key}.bindings",
        )
        expected_bindings = {
            "input_sha256": artifacts["input"].actual_sha256,
            "output_sha256": artifacts["output"].actual_sha256,
            "generation_run_record_sha256": forward_state.get("raw_run_sha256"),
            "anonymous_bundle_sha256": artifacts["review_bundle"].actual_sha256,
            "rubric_sha256": rubric_sha256,
            "oracle_catalog_sha256": catalog.raw_sha256,
        }
        if dict(bindings) != expected_bindings:
            raise AuditError(f"oracle review {artifact.key} artifact bindings are stale")
        answers = review.get("answers")
        if not isinstance(answers, list):
            raise AuditError(f"oracle review {artifact.key}.answers must be an array")
        expected_questions = [item["id"] for item in rubric["questions"]]
        answer_map: dict[str, str] = {}
        for index, raw_answer in enumerate(answers):
            answer = _as_mapping(
                raw_answer, f"oracle review {artifact.key}.answers[{index}]"
            )
            _exact_keys(
                answer,
                {"question_id", "answer"},
                f"oracle review {artifact.key}.answers[{index}]",
            )
            question_id = answer.get("question_id")
            if question_id not in expected_questions or question_id in answer_map:
                raise AuditError(f"oracle review {artifact.key} has unknown/duplicate question")
            if answer.get("answer") not in {"PASS", "FAIL"}:
                raise AuditError(f"oracle review {artifact.key} answer must be PASS or FAIL")
            answer_map[str(question_id)] = str(answer["answer"])
        if set(answer_map) != set(expected_questions):
            raise AuditError(f"oracle review {artifact.key} omits a required question")
        passed = all(answer_map[item] == "PASS" for item in expected_questions)
        state.update(
            {
                "valid": True,
                "status": "NOT_EVALUATED",
                "declared_outcome": "PASS" if passed else "FAIL",
                "qualification_eligible": False,
                "review_id": review["review_id"],
                "reviewer_kind": kind,
                "reviewer_id_sha256": reviewer_hash,
                "review_run_id": review_run_id,
                "grader_source": "CALLER_DECLARED",
                "review_kind_source": "MODEL_REVIEW" if kind == "MODEL" else "HUMAN",
                "provenance": "CALLER_DECLARED",
                "insufficient_reason": (
                    "review lacks a separately bound review run record/prompt/context/receipt"
                ),
                "answers": [
                    {"question_id": item, "answer": answer_map[item]}
                    for item in expected_questions
                ],
            }
        )
    except (AuditError, KeyError) as error:
        integrity_errors.append(str(error))
        state["insufficient_reason"] = str(error)
    return state


def _required_review_state(
    case: Mapping[str, Any],
    suite: Mapping[str, Any],
    catalog: OracleCatalog,
    artifacts: Mapping[str, Artifact],
    forward_state: Mapping[str, Any],
    case_id: str,
    integrity_errors: list[str],
) -> dict[str, Any]:
    required = list(suite.get("required_reviews", []))
    if not required:
        return {"status": "PASS", "required": [], "reviews": []}
    refs = case.get("reviews", [])
    candidate_artifacts = [
        artifacts.get(item.get("artifact"))
        for item in refs
        if isinstance(item, dict) and isinstance(item.get("artifact"), str)
    ]
    states: list[dict[str, Any]] = []
    for rubric_id in required:
        rubric = catalog.rubrics[rubric_id]
        rubric_states: list[dict[str, Any]] = []
        for artifact in candidate_artifacts:
            if artifact is None:
                continue
            try:
                raw = _strict_json_bytes(artifact.raw, f"oracle review {artifact.key}")
            except AuditError:
                continue
            if isinstance(raw, dict) and raw.get("rubric_id") == rubric_id:
                rubric_states.append(
                    _review_artifact_state(
                        artifact,
                        case_id=case_id,
                        suite_id=str(suite["id"]),
                        rubric_id=rubric_id,
                        rubric=rubric,
                        rubric_sha256=catalog.rubric_sha256[rubric_id],
                        catalog=catalog,
                        artifacts=artifacts,
                        forward_state=forward_state,
                        integrity_errors=integrity_errors,
                    )
                )
        valid = [
            item
            for item in rubric_states
            if item.get("valid") is True and item.get("qualification_eligible") is True
        ]
        distinct = {item.get("reviewer_id_sha256") for item in valid}
        minimum = int(rubric["minimum_distinct_reviewers"])
        if len(distinct) < minimum:
            status = "NOT_EVALUATED"
        elif any(item.get("status") == "FAIL" for item in valid):
            status = "FAIL"
        else:
            status = "PASS"
        states.append(
            {
                "rubric_id": rubric_id,
                "rubric_sha256": catalog.rubric_sha256[rubric_id],
                "minimum_distinct_reviewers": minimum,
                "distinct_reviewers": len(distinct),
                "identity_verified": False,
                "status": status,
                "reviews": rubric_states,
            }
        )
    if any(item["status"] == "FAIL" for item in states):
        overall = "FAIL"
    elif any(item["status"] == "NOT_EVALUATED" for item in states):
        overall = "NOT_EVALUATED"
    else:
        overall = "PASS"
    return {"status": overall, "required": required, "reviews": states}


def _audit_case_v2(
    case: Mapping[str, Any],
    *,
    atoms: Mapping[str, Atom],
    catalog: OracleCatalog,
    artifact_root: Path,
    skill_root: Path,
    current_bindings: Mapping[str, str],
    top_bindings: Any,
    timeout: float,
    case_ids: set[str],
    claim_ids: set[str],
    claimed_atom_ids: set[str],
    run_ids: set[str],
    integrity_errors: list[str],
) -> dict[str, Any]:
    try:
        case_id = _safe_id(case.get("id"), "case.id")
    except AuditError as error:
        integrity_errors.append(str(error))
        case_id = f"INVALID-CASE-{len(case_ids) + 1:04d}"
    if case_id in case_ids:
        integrity_errors.append(f"duplicate case id: {case_id}")
    else:
        case_ids.add(case_id)
    _validate_v2_case_shape(case, case_id, integrity_errors)
    claims = _case_oracle_claims(
        case,
        atoms,
        catalog,
        case_id,
        claim_ids,
        claimed_atom_ids,
        integrity_errors,
    )
    artifacts = _load_artifacts(case, artifact_root, case_id, integrity_errors)
    bindings_valid = _case_bindings(
        case, top_bindings, current_bindings, case_id, integrity_errors
    )
    evidence_level = (
        "E1"
        if artifacts.get("input") is not None and artifacts.get("output") is not None
        else "E0"
    )
    suite_states: dict[str, dict[str, Any]] = {}
    all_deterministic_integrity = bool(claims) and bindings_valid
    for claim in claims:
        suite_id = str(claim["oracle_suite_id"])
        suite = catalog.suites[suite_id]
        fixture_valid, fixture_records = _suite_fixture_state(
            suite, artifacts, suite_id, integrity_errors
        )
        checks = [
            _evaluate_oracle_check(
                check_id,
                catalog,
                artifacts,
                skill_root,
                timeout,
                integrity_errors,
            )
            for check_id in suite["required_checks"]
        ]
        deterministic_integrity = fixture_valid and bool(checks) and all(
            item.get("integrity_valid") is True for item in checks
        )
        all_deterministic_integrity = (
            all_deterministic_integrity and deterministic_integrity
        )
        suite_states[suite_id] = {
            "suite_id": suite_id,
            "suite_sha256": catalog.suite_sha256[suite_id],
            "fixture_bindings_valid": fixture_valid,
            "fixture_bindings": fixture_records,
            "deterministic_integrity_valid": deterministic_integrity,
            "checks": checks,
        }
    e2_valid = all_deterministic_integrity
    if e2_valid:
        evidence_level = "E2"
    e3_valid, forward_state = _blind_forward_state(
        case,
        artifacts,
        e2_valid,
        current_bindings,
        run_ids,
        case_id,
        integrity_errors,
    )
    if e3_valid:
        runner_compatible = all(
            catalog.suites[str(claim["oracle_suite_id"])].get("runner_compatible") is True
            for claim in claims
        )
        if runner_compatible:
            evidence_level = "E3"
        else:
            e3_valid = False
            forward_state.update(
                {
                    "valid": False,
                    "run_record_valid": True,
                    "evidence_cap": "E2",
                    "suite_evidence_cap": "SHADOW_NOT_RUNNER_COMPATIBLE",
                }
            )
    claim_results: list[dict[str, Any]] = []
    for claim in claims:
        atom = atoms[str(claim["atom_id"])]
        suite_id = str(claim["oracle_suite_id"])
        suite = catalog.suites[suite_id]
        suite_state = suite_states[suite_id]
        review_state = _required_review_state(
            case,
            suite,
            catalog,
            artifacts,
            forward_state,
            case_id,
            integrity_errors,
        )
        suite_state["reviews"] = review_state
        suite_state["qualification_stage"] = suite["qualification_stage"]
        suite_state["runner_compatible"] = suite["runner_compatible"]
        check_statuses = [item["status"] for item in suite_state["checks"]]
        deterministic_fail = "FAIL" in check_statuses
        deterministic_incomplete = (
            not suite_state["deterministic_integrity_valid"]
            or "NOT_EVALUATED" in check_statuses
        )
        if deterministic_fail:
            status = "FAIL"
            reason = "catalog-owned deterministic check failed"
        elif deterministic_incomplete:
            status = "NOT_EVALUATED"
            reason = "catalog-owned deterministic checks are incomplete"
        elif review_state["status"] == "FAIL":
            status = "FAIL"
            reason = "catalog-owned review rubric derived a failure"
        elif EVIDENCE_RANK[evidence_level] < EVIDENCE_RANK[atom.minimum_evidence]:
            status = "NOT_EVALUATED"
            reason = f"requires {atom.minimum_evidence}, case reached {evidence_level}"
        elif review_state["status"] == "NOT_EVALUATED":
            status = "NOT_EVALUATED"
            reason = "required subjective review is missing or insufficient"
        else:
            status = "PASS"
            reason = "catalog-owned suite checks and required reviews pass"
        claim_results.append(
            {
                **claim,
                "minimum_evidence": atom.minimum_evidence,
                "severity": atom.severity,
                "status": status,
                "reason": reason,
                "deterministic_outcome": (
                    "FAIL"
                    if deterministic_fail
                    else "NOT_EVALUATED"
                    if deterministic_incomplete
                    else "PASS"
                ),
                "review_outcome": review_state["status"],
            }
        )
    return {
        "case_id": case_id,
        "archived": False,
        "manifest_schema": MANIFEST_V2_SCHEMA,
        "evidence_level": evidence_level,
        "minimum_claimed_evidence": _minimum_level_for_claims(claims, atoms),
        "artifact_count": len(artifacts),
        "artifact_sha256": {
            key: item.actual_sha256 for key, item in sorted(artifacts.items())
        },
        "bindings_current": bindings_valid,
        "oracle_catalog_sha256": catalog.raw_sha256,
        "oracle_suites": list(suite_states.values()),
        "replays": [
            check["observation"]
            for state in suite_states.values()
            for check in state["checks"]
            if check["type"] == "replay_result"
        ],
        "blind_forward": forward_state,
        "blind_review": {"valid": False, "status": "LEGACY_CHANNEL_UNUSED"},
        "measurements": {},
        "claims": claim_results,
    }


def _minimum_level_for_claims(claims: Sequence[Mapping[str, Any]], atoms: Mapping[str, Atom]) -> str:
    if not claims:
        return "E0"
    return max((atoms[str(claim["atom_id"])].minimum_evidence for claim in claims), key=EVIDENCE_RANK.get)


def _audit_case(
    case: Mapping[str, Any],
    *,
    archived: bool,
    manifest_schema: str | None,
    atoms: Mapping[str, Atom],
    catalog: OracleCatalog,
    artifact_root: Path,
    skill_root: Path,
    current_bindings: Mapping[str, str],
    top_bindings: Any,
    timeout: float,
    case_ids: set[str],
    claim_ids: set[str],
    assertion_ids: set[str],
    claimed_atom_ids: set[str],
    run_ids: set[str],
    ballot_ids: set[str],
    integrity_errors: list[str],
) -> dict[str, Any]:
    if not archived and manifest_schema == MANIFEST_V2_SCHEMA:
        return _audit_case_v2(
            case,
            atoms=atoms,
            catalog=catalog,
            artifact_root=artifact_root,
            skill_root=skill_root,
            current_bindings=current_bindings,
            top_bindings=top_bindings,
            timeout=timeout,
            case_ids=case_ids,
            claim_ids=claim_ids,
            claimed_atom_ids=claimed_atom_ids,
            run_ids=run_ids,
            integrity_errors=integrity_errors,
        )
    try:
        case_id = _safe_id(case.get("id"), "case.id")
    except AuditError as error:
        integrity_errors.append(str(error))
        case_id = f"INVALID-CASE-{len(case_ids) + 1:04d}"
    if case_id in case_ids:
        integrity_errors.append(f"duplicate case id: {case_id}")
    else:
        case_ids.add(case_id)
    archived = archived or case.get("archived") is True
    claims, assertions = _case_assertions_and_claims(
        case,
        atoms,
        case_id,
        claim_ids,
        assertion_ids,
        claimed_atom_ids,
        integrity_errors,
    )
    artifacts = _load_artifacts(case, artifact_root, case_id, integrity_errors)
    evidence_level = "E0"
    if artifacts.get("input") is not None and artifacts.get("output") is not None:
        evidence_level = "E1"

    bindings_valid = _case_bindings(
        case, top_bindings, current_bindings, case_id, integrity_errors
    )
    replay_results: list[dict[str, Any]] = []
    replay_behavior_pass = True
    e2_valid = False
    replays = case.get("replays", [])
    if replays is not None and not isinstance(replays, list):
        integrity_errors.append(f"{case_id}.replays must be an array")
        replays = []
    structurally_valid_replays = True
    for index, replay in enumerate(replays):
        label = f"{case_id}.replays[{index}]"
        if not isinstance(replay, dict):
            integrity_errors.append(f"{label} must be an object")
            structurally_valid_replays = False
            continue
        declaration_error = _static_replay_declaration_error(replay)
        if declaration_error:
            integrity_errors.append(f"{label} {declaration_error}")
            structurally_valid_replays = False
    if evidence_level == "E1" and bindings_valid and replays and structurally_valid_replays:
        for index, replay in enumerate(replays):
            label = f"{case_id}.replays[{index}]"
            if not isinstance(replay, dict):
                integrity_errors.append(f"{label} must be an object")
                replay_results.append({"label": label, "integrity_valid": False})
                continue
            replay_result = _run_replay(
                replay,
                artifacts,
                skill_root,
                timeout,
                label,
                integrity_errors,
            )
            replay_results.append(replay_result)
            replay_behavior_pass = replay_behavior_pass and bool(
                replay_result.get("behavior_matches_expected")
            )
        e2_valid = bool(replay_results) and all(
            item.get("integrity_valid") is True for item in replay_results
        )
        if e2_valid:
            evidence_level = "E2"

    e3_valid, forward_state = _blind_forward_state(
        case,
        artifacts,
        e2_valid,
        current_bindings,
        run_ids,
        case_id,
        integrity_errors,
    )
    if e3_valid:
        evidence_level = "E3"
    e4_valid, ballots_pass, review_state, _reviewer_hashes = _blind_review_state(
        case,
        artifacts,
        e3_valid,
        forward_state,
        current_bindings,
        ballot_ids,
        case_id,
        integrity_errors,
    )
    if e4_valid:
        evidence_level = "E4"

    idempotency_pass, idempotency_state = _idempotency_measurement(
        case, artifacts, current_bindings, forward_state
    )
    stability_pass, stability_state = _route_stability_measurement(
        case, artifacts, current_bindings, forward_state
    )
    protected_pass, protected_state = _protected_hash_measurement(case, artifacts)

    automatic_by_kind: dict[str, bool | None] = {
        "idempotency": idempotency_pass,
        "blind_review": ballots_pass if e4_valid else None,
        "route_stability": stability_pass,
        "protected_hash": protected_pass,
        "behavior": True,
    }
    case_machine_pass = replay_behavior_pass
    claim_results: list[dict[str, Any]] = []
    for claim in claims:
        atom = atoms[str(claim["atom_id"])]
        assertion_values = [assertions[item]["result"] for item in claim["assertion_ids"]]
        automatic = automatic_by_kind.get(atom.kind, True)
        known_behavior_failure = (
            (not case_machine_pass)
            or automatic is False
            or "FAIL" in assertion_values
        )
        if archived:
            status = "NOT_EVALUATED"
            reason = "archived evidence cannot qualify the current generator"
        elif known_behavior_failure and EVIDENCE_RANK[evidence_level] >= EVIDENCE_RANK["E3"]:
            status = "FAIL"
            reason = "current forward evidence contradicts the atom"
        elif known_behavior_failure and atom.minimum_evidence == "E2" and evidence_level == "E2":
            status = "FAIL"
            reason = "current deterministic evidence contradicts the atom"
        elif EVIDENCE_RANK[evidence_level] < EVIDENCE_RANK[atom.minimum_evidence]:
            status = "NOT_EVALUATED"
            reason = f"requires {atom.minimum_evidence}, case reached {evidence_level}"
        elif automatic is None:
            status = "NOT_EVALUATED"
            reason = f"missing {atom.kind} measurement"
        elif "NOT_EVALUATED" in assertion_values:
            status = "NOT_EVALUATED"
            reason = "a bound assertion is not evaluated"
        elif known_behavior_failure:
            status = "FAIL"
            reason = "behavior or bound assertion failed"
        else:
            status = "PASS"
            reason = "required evidence and bound assertions pass"
        claim_results.append(
            {
                **claim,
                "minimum_evidence": atom.minimum_evidence,
                "severity": atom.severity,
                "status": status,
                "reason": reason,
            }
        )

    if archived and EVIDENCE_RANK[evidence_level] > EVIDENCE_RANK["E1"]:
        evidence_level = "E1"
    return {
        "case_id": case_id,
        "archived": archived,
        "evidence_level": evidence_level,
        "minimum_claimed_evidence": _minimum_level_for_claims(claims, atoms),
        "artifact_count": len(artifacts),
        "artifact_sha256": {key: item.actual_sha256 for key, item in sorted(artifacts.items())},
        "bindings_current": bindings_valid,
        "replays": replay_results,
        "blind_forward": forward_state,
        "blind_review": review_state,
        "measurements": {
            "idempotency": idempotency_state,
            "route_stability": stability_state,
            "protected_hash": protected_state,
        },
        "claims": claim_results,
    }


def _aggregate_qualification(
    atom_reports: Sequence[Mapping[str, Any]],
    integrity_errors: Sequence[str],
) -> tuple[str, str, int]:
    """Aggregate only authoritative atom states; test counts never enter this decision."""

    evidence_integrity = "FAIL" if integrity_errors else "PASS"
    if evidence_integrity == "FAIL":
        qualification = "NOT_EVALUATED"
    elif any(
        item.get("status") == "FAIL" and item.get("severity") in {"P0", "P1"}
        for item in atom_reports
    ):
        qualification = "FAIL"
    elif atom_reports and all(item.get("status") == "PASS" for item in atom_reports):
        qualification = "PASS"
    else:
        qualification = "NOT_EVALUATED"
    exit_code = 1 if evidence_integrity == "FAIL" else QUALIFICATION_EXIT[qualification]
    return evidence_integrity, qualification, exit_code


def audit(
    manifest_path: Path | None,
    *,
    skill_root: Path = DEFAULT_SKILL_ROOT,
    requirements_path: Path = DEFAULT_REQUIREMENTS,
    contract_path: Path = DEFAULT_CONTRACT,
    artifact_root: Path | None = None,
    replay_timeout: float = 60.0,
) -> dict[str, Any]:
    skill_root = skill_root.resolve(strict=True)
    requirements_path = requirements_path.resolve(strict=True)
    contract_path = contract_path.resolve(strict=True)
    if not _is_relative_to(requirements_path, skill_root):
        raise AuditError("requirements file must be inside the selected Skill root")
    if not _is_relative_to(contract_path, skill_root):
        raise AuditError("evaluation contract must be inside the selected Skill root")
    requirements = _as_mapping(
        _strict_json_file(requirements_path, "requirements"), "requirements"
    )
    atoms, integrity_errors = _expand_requirements(requirements)
    contract_relative = contract_path.relative_to(skill_root).as_posix()
    if requirements.get("contract_file") != contract_relative:
        integrity_errors.append("requirements.contract_file does not bind the selected contract path")
    try:
        contract_text = contract_path.read_text(encoding="utf-8-sig")
    except (OSError, UnicodeError) as error:
        raise AuditError(f"cannot read evaluation contract: {error}") from error
    integrity_errors.extend(_contract_alignment(contract_text, atoms))
    catalog = _load_oracle_catalog(
        skill_root,
        contract_path,
        requirements_path,
        requirements,
        atoms,
    )
    current = _current_bindings(skill_root, contract_path, requirements_path)

    manifest: Mapping[str, Any]
    manifest_resolved: Path | None = None
    manifest_initial_sha256: str | None = None
    schema: str | None = None
    if manifest_path is None:
        manifest = {"cases": [], "archived_failures": []}
        root = Path.cwd().resolve()
    else:
        manifest_resolved = manifest_path.resolve(strict=True)
        manifest_initial_sha256 = _file_sha256(manifest_resolved)
        manifest = _as_mapping(
            _strict_json_file(manifest_resolved, "qualification manifest"),
            "qualification manifest",
        )
        schema = manifest.get("schema_version")
        if schema not in MANIFEST_SCHEMAS:
            integrity_errors.append(
                "manifest.schema_version must be a supported generation qualification schema"
            )
        root = artifact_root.resolve(strict=True) if artifact_root else manifest_resolved.parent.resolve()
        if not _is_relative_to(manifest_resolved, root):
            integrity_errors.append("manifest path is outside artifact_root")
        if schema == MANIFEST_V2_SCHEMA:
            allowed_top = {
                "schema_version",
                "bindings",
                "cases",
                "archived_failures",
                "tests_total",
            }
            extra_top = sorted(set(manifest) - allowed_top)
            if extra_top:
                integrity_errors.append(f"manifest v2 has unknown fields: {extra_top}")

    top_bindings = manifest.get("bindings")
    if top_bindings is not None:
        _binding_state(top_bindings, current, "manifest.bindings", integrity_errors)
    elif schema == MANIFEST_V2_SCHEMA:
        integrity_errors.append("manifest v2 requires current bindings")
    cases_raw = manifest.get("cases", [])
    archived_raw = manifest.get("archived_failures", [])
    if not isinstance(cases_raw, list):
        integrity_errors.append("manifest.cases must be an array")
        cases_raw = []
    if not isinstance(archived_raw, list):
        integrity_errors.append("manifest.archived_failures must be an array")
        archived_raw = []
    if schema in {
        "humanize-generation-qualification-manifest/v1",
        "humanize-generation-qualification-evidence/v1",
    } and cases_raw:
        integrity_errors.append(
            "manifest v1 current cases are forbidden; move legacy evidence to archived_failures "
            "or rerun with manifest v2"
        )

    case_ids: set[str] = set()
    claim_ids: set[str] = set()
    assertion_ids: set[str] = set()
    claimed_atom_ids: set[str] = set()
    archived_claimed_atom_ids: set[str] = set()
    run_ids: set[str] = set()
    ballot_ids: set[str] = set()
    case_reports: list[dict[str, Any]] = []
    for archived, raw_cases in ((False, cases_raw), (True, archived_raw)):
        for index, case in enumerate(raw_cases):
            if not isinstance(case, dict):
                integrity_errors.append(
                    f"{'archived_failures' if archived else 'cases'}[{index}] must be an object"
                )
                continue
            effective_archived = archived or schema != MANIFEST_V2_SCHEMA
            case_reports.append(
                _audit_case(
                    case,
                    archived=effective_archived,
                    manifest_schema=schema,
                    atoms=atoms,
                    catalog=catalog,
                    artifact_root=root,
                    skill_root=skill_root,
                    current_bindings=current,
                    top_bindings=top_bindings,
                    timeout=replay_timeout,
                    case_ids=case_ids,
                    claim_ids=claim_ids,
                    assertion_ids=assertion_ids,
                    claimed_atom_ids=(
                        archived_claimed_atom_ids
                        if effective_archived
                        else claimed_atom_ids
                    ),
                    run_ids=run_ids,
                    ballot_ids=ballot_ids,
                    integrity_errors=integrity_errors,
                )
            )

    if _file_sha256(requirements_path) != current["requirements_sha256"]:
        integrity_errors.append("requirements changed during the audit")
    if _file_sha256(contract_path) != current["contract_sha256"]:
        integrity_errors.append("evaluation contract changed during the audit")
    if _file_sha256(catalog.path) != catalog.raw_sha256:
        integrity_errors.append("oracle catalog changed during the audit")
    final_skill_hash, _ = _skill_snapshot(skill_root)
    if final_skill_hash != current["skill_snapshot_sha256"]:
        integrity_errors.append("Skill snapshot changed during the audit")
    if (
        manifest_resolved is not None
        and manifest_initial_sha256 is not None
        and _file_sha256(manifest_resolved) != manifest_initial_sha256
    ):
        integrity_errors.append("qualification manifest changed during the audit")

    claims_by_atom: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for case_report in case_reports:
        for claim in case_report["claims"]:
            claims_by_atom[claim["atom_id"]].append(
                {"case_id": case_report["case_id"], **claim}
            )
    atom_reports: list[dict[str, Any]] = []
    for atom_id, atom in sorted(atoms.items()):
        claims = claims_by_atom.get(atom_id, [])
        if any(claim["status"] == "FAIL" for claim in claims):
            status = "FAIL"
        elif any(claim["status"] == "PASS" for claim in claims):
            status = "PASS"
        else:
            status = "NOT_EVALUATED"
        report = {
            "atom_id": atom_id,
            "dimension": atom.dimension,
            "kind": atom.kind,
            "minimum_evidence": atom.minimum_evidence,
            "severity": atom.severity,
            "status": status,
            "claims": claims,
        }
        atom_reports.append(report)

    integrity_errors = sorted(set(integrity_errors))
    evidence_integrity, qualification, exit_code = _aggregate_qualification(
        atom_reports, integrity_errors
    )
    evidence_counts = Counter(item["evidence_level"] for item in case_reports)
    atom_counts = Counter(item["status"] for item in atom_reports)
    dimensions: dict[str, Counter[str]] = defaultdict(Counter)
    for item in atom_reports:
        dimensions[item["dimension"]][item["status"]] += 1
    return {
        "schema_version": REPORT_SCHEMA,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "manifest_path": str(manifest_resolved) if manifest_resolved else None,
        "artifact_root": str(root),
        "current_bindings": current,
        "oracle_catalog": {
            "schema_version": ORACLE_CATALOG_SCHEMA,
            "catalog_version": catalog.catalog_version,
            "sha256": catalog.raw_sha256,
            "suites_total": len(catalog.suites),
            "qualification_stage": "SHADOW",
            "runner_compatible": all(
                item.get("runner_compatible") is True
                for item in catalog.suites.values()
            ),
            "covered_atoms": sorted(
                {str(item["atom_id"]) for item in catalog.suites.values()}
            ),
            "catalog_complete": len(
                {str(item["atom_id"]) for item in catalog.suites.values()}
            )
            == len(atoms),
        },
        "contract_version": requirements.get("contract_version"),
        "requirements_version": requirements.get("requirements_version"),
        "evidence_integrity_status": evidence_integrity,
        "qualification_status": qualification,
        "exit_code": exit_code,
        "tests_total_ignored": True,
        "declared_tests_total": manifest.get("tests_total"),
        "summary": {
            "atoms_total": len(atom_reports),
            "atoms_pass": atom_counts["PASS"],
            "atoms_fail": atom_counts["FAIL"],
            "atoms_not_evaluated": atom_counts["NOT_EVALUATED"],
            "cases_total": len(case_reports),
            "evidence_level_counts": {
                level: evidence_counts[level] for level in sorted(EVIDENCE_RANK)
            },
            "p0_failures": sum(
                item["status"] == "FAIL" and item["severity"] == "P0" for item in atom_reports
            ),
            "p1_failures": sum(
                item["status"] == "FAIL" and item["severity"] == "P1" for item in atom_reports
            ),
            "p2_failures": 0,
            "dimensions": {
                dimension: {
                    status: counter[status]
                    for status in ("PASS", "FAIL", "NOT_EVALUATED")
                }
                for dimension, counter in sorted(dimensions.items())
            },
        },
        "integrity_errors": integrity_errors,
        "uncovered_atoms": [
            item["atom_id"] for item in atom_reports if item["status"] == "NOT_EVALUATED"
        ],
        "failed_atoms": [item["atom_id"] for item in atom_reports if item["status"] == "FAIL"],
        "atoms": atom_reports,
        "cases": case_reports,
        "trust_boundary": {
            "subprocess_shell": False,
            "allowlisted_tools": sorted(TOOL_ALLOWLIST),
            "blindness": BLINDNESS_ATTESTATION,
            "blindness_verified": False,
            "run_independence": INDEPENDENCE_ATTESTATION,
            "run_independence_verified": False,
            "human_identity_verified": False,
            "academic_correctness": "NOT_EVALUATED",
            "oracle_catalog_binding_is_blindness_proof": False,
            "generator_visible_full_skill_evidence_cap": "E2",
        },
    }


def _text_report(report: Mapping[str, Any]) -> str:
    summary = report.get("summary", {})
    lines = [
        f"evidence_integrity_status: {report.get('evidence_integrity_status')}",
        f"qualification_status: {report.get('qualification_status')}",
        f"exit_code: {report.get('exit_code')}",
        f"atoms: {summary.get('atoms_pass', 0)} PASS / {summary.get('atoms_fail', 0)} FAIL / "
        f"{summary.get('atoms_not_evaluated', 0)} NOT_EVALUATED / {summary.get('atoms_total', 0)} total",
        f"cases_total: {summary.get('cases_total', 0)}",
        "tests_total_ignored: TRUE",
        "academic_correctness: NOT_EVALUATED",
    ]
    for error in report.get("integrity_errors", []):
        lines.append(f"integrity_error: {error}")
    uncovered = report.get("uncovered_atoms", [])
    if uncovered:
        lines.append("uncovered_atoms: " + ", ".join(uncovered))
    failed = report.get("failed_atoms", [])
    if failed:
        lines.append("failed_atoms: " + ", ".join(failed))
    return "\n".join(lines) + "\n"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Audit current forward-generation qualification evidence. "
            "A missing manifest is an honest NOT_EVALUATED audit, not a PASS."
        )
    )
    parser.add_argument("manifest", nargs="?", type=Path, help="strict JSON evidence manifest")
    parser.add_argument("--skill-root", type=Path, default=DEFAULT_SKILL_ROOT)
    parser.add_argument("--requirements", type=Path, default=DEFAULT_REQUIREMENTS)
    parser.add_argument("--contract", type=Path, default=DEFAULT_CONTRACT)
    parser.add_argument(
        "--artifact-root",
        type=Path,
        help="root for all manifest-relative evidence paths; defaults to the manifest directory",
    )
    parser.add_argument("--replay-timeout", type=float, default=60.0)
    parser.add_argument("--format", choices=("json", "text"), default="json", dest="output_format")
    parser.add_argument("--output", type=Path, help="optional report path outside the Skill root")
    return parser


def _fatal_report(error: Exception) -> dict[str, Any]:
    return {
        "schema_version": REPORT_SCHEMA,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "evidence_integrity_status": "FAIL",
        "qualification_status": "NOT_EVALUATED",
        "exit_code": 1,
        "tests_total_ignored": True,
        "integrity_errors": [str(error)],
        "uncovered_atoms": [],
        "failed_atoms": [],
        "trust_boundary": {
            "subprocess_shell": False,
            "allowlisted_tools": sorted(TOOL_ALLOWLIST),
            "blindness": BLINDNESS_ATTESTATION,
            "blindness_verified": False,
            "run_independence": INDEPENDENCE_ATTESTATION,
            "run_independence_verified": False,
            "human_identity_verified": False,
            "academic_correctness": "NOT_EVALUATED",
            "oracle_catalog_binding_is_blindness_proof": False,
            "generator_visible_full_skill_evidence_cap": "E2",
        },
    }


def main(argv: Sequence[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = build_parser()
    args = parser.parse_args(argv)
    if not (0 < args.replay_timeout <= 300):
        report = _fatal_report(AuditError("--replay-timeout must be in (0, 300]"))
    else:
        try:
            report = audit(
                args.manifest,
                skill_root=args.skill_root,
                requirements_path=args.requirements,
                contract_path=args.contract,
                artifact_root=args.artifact_root,
                replay_timeout=args.replay_timeout,
            )
        except (AuditError, OSError, UnicodeError, ValueError) as error:
            report = _fatal_report(error)
    rendered = (
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
        if args.output_format == "json"
        else _text_report(report)
    )
    if args.output:
        try:
            output = args.output.resolve(strict=False)
            skill_root = args.skill_root.resolve(strict=True)
            if _is_relative_to(output, skill_root):
                raise AuditError("--output must stay outside the Skill root so it cannot alter the snapshot")
            output.parent.mkdir(parents=True, exist_ok=True)
            temporary = output.with_name(output.name + ".tmp")
            temporary.write_text(rendered, encoding="utf-8", newline="\n")
            os.replace(temporary, output)
        except (AuditError, OSError) as error:
            sys.stderr.write(f"qualification report write failed: {error}\n")
            return 1
    else:
        sys.stdout.write(rendered)
    return int(report.get("exit_code", 1))


if __name__ == "__main__":
    raise SystemExit(main())
