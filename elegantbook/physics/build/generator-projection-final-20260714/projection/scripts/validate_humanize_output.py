#!/usr/bin/env python3
"""Validate a Chinese academic-style rewrite with reproducible evidence."""

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
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import check_humanize_invariants as invariants  # noqa: E402
import scan_humanize_chinese as lexical  # noqa: E402


VAGUE_REASON_RE = re.compile(
    r"^(?:(?:经过)?(?:人工)?(?:已经|已)?(?:确认|复核|审核)(?:保留|接受|通过|无误|确认)?"
    r"(?:此项|该项|内容|原句)?|(?:这是|此为|属于)?(?:一个)?(?:具体)?理由|"
    r"(?:用户)?(?:要求|同意)?(?:保留|接受))$"
)
SPECIFIC_REASON_ANCHORS = (
    "用户",
    "题面",
    "原句",
    "术语",
    "定义",
    "引用",
    "法规",
    "方法",
    "材料",
    "算法",
    "名称",
    "结论",
    "否定",
    "模态",
    "语气",
    "重复",
    "范围",
    "表达",
    "功能",
    "上下文",
    "证据",
    "锁定",
    "命令",
    "条件",
)
WARNING_REVIEW_REQUEST_SCHEMA = "humanize-warning-review-request/v1"


def _sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def _read_utf8(path: Path) -> tuple[bytes, str]:
    raw = path.read_bytes()
    return raw, raw.decode("utf-8-sig")


def _document_format(before: Path, after: Path) -> str:
    if before.suffix.lower() in {".tex", ".ltx"} or after.suffix.lower() in {".tex", ".ltx"}:
        return "tex"
    return "markdown"


def _validate_reason(reason: str, label: str) -> str:
    reason = reason.strip()
    chinese_count = len(re.findall(r"[\u3400-\u9fff]", reason))
    normalized = re.sub(r"[\s，。！？；：、,.!?;:'\"（）()\[\]{}_-]+", "", reason)
    if (
        chinese_count < 6
        or VAGUE_REASON_RE.fullmatch(normalized)
        or not any(anchor in normalized for anchor in SPECIFIC_REASON_ANCHORS)
    ):
        raise ValueError(f"{label} 必须说明具体位置的表达功能或人工判断依据")
    return reason


def _parse_keep_key(key: str, valid_ids: set[str]) -> tuple[str, str | None]:
    signal_id, separator, binding = key.partition("@")
    if signal_id not in valid_ids:
        raise ValueError(f"未知 signal id: {signal_id}")
    if not separator:
        return signal_id, None
    if re.fullmatch(r"\d+:\d+", binding):
        return signal_id, binding
    if re.fullmatch(r"sha256:[0-9a-fA-F]{12,64}", binding):
        return signal_id, binding.lower()
    raise ValueError(f"{key} 的定位必须是 LINE:COLUMN 或 sha256:HASH")


def _parse_keep_reasons(values: Sequence[str], valid_ids: set[str]) -> dict[str, str]:
    reasons: dict[str, str] = {}
    for value in values:
        if "=" not in value:
            raise ValueError("--keep-reason 必须使用 SIGNAL_ID=具体理由")
        key, reason = (part.strip() for part in value.split("=", 1))
        _parse_keep_key(key, valid_ids)
        reasons[key] = _validate_reason(reason, f"{key} 的 KEEP 理由")
    return reasons


def _parse_reason_pairs(values: Sequence[str], option: str) -> dict[str, str]:
    reasons: dict[str, str] = {}
    for value in values:
        if "=" not in value:
            raise ValueError(f"{option} 必须使用 CODE=具体理由")
        code, reason = (part.strip() for part in value.split("=", 1))
        if not code:
            raise ValueError(f"{option} 缺少 CODE")
        if code in reasons:
            raise ValueError(f"{option} 重复提交 CODE: {code}")
        reasons[code] = _validate_reason(reason, f"{code} 的具体理由")
    return reasons


def _policy_hashes() -> dict[str, str]:
    paths = {
        "validator_sha256": Path(__file__).resolve(),
        "invariant_checker_sha256": Path(invariants.__file__).resolve(),
        "scanner_sha256": Path(lexical.__file__).resolve(),
        "lexicon_sha256": Path(lexical.DEFAULT_LEXICON).resolve(),
    }
    return {name: _sha256(path.read_bytes()) for name, path in paths.items()}


def _canonical_warning(warning: Any) -> dict[str, Any]:
    return {
        "code": warning.code,
        "severity": warning.severity,
        "message": warning.message,
        "details": warning.details,
    }


def _warning_fingerprint(warning: Any) -> str:
    return _sha256(_canonical_json_bytes(_canonical_warning(warning)))


def _public_warning(warning: Any) -> dict[str, Any]:
    public = _canonical_warning(warning)
    public["warning_fingerprint"] = _warning_fingerprint(warning)
    return public


def _build_warning_review_request(
    warnings: Sequence[Any],
    *,
    before_sha256: str,
    after_sha256: str,
    scene: str,
    document_format: str,
    protected_terms: dict[str, Any],
    strict_speech_acts: bool,
) -> dict[str, Any] | None:
    if not warnings:
        return None
    request_body = {
        "schema": WARNING_REVIEW_REQUEST_SCHEMA,
        "artifact": {
            "before_sha256": before_sha256,
            "after_sha256": after_sha256,
        },
        "validation_context": {
            "scene": scene.upper(),
            "document_format": document_format,
            "strict_speech_acts": strict_speech_acts,
            "protected_terms": protected_terms,
        },
        "policy_hashes": _policy_hashes(),
        "warnings": [_public_warning(item) for item in warnings],
    }
    return {
        **request_body,
        "request_sha256": _sha256(_canonical_json_bytes(request_body)),
    }


def _warning_review_attestation(
    warning_resolutions: dict[str, str],
    warning_review_request_sha256: str,
    reviewer_kind: str,
    reviewer_id: str,
    current_request: dict[str, Any] | None,
) -> dict[str, Any]:
    kind = reviewer_kind.strip().upper() or "NONE"
    identity = reviewer_id.strip()
    request_sha256 = warning_review_request_sha256.strip().lower()
    if warning_resolutions:
        if not re.fullmatch(r"[0-9a-f]{64}", request_sha256):
            raise ValueError(
                "warning_resolutions require a 64-character "
                "warning_review_request_sha256 from the current REVIEW result"
            )
        if current_request is None or request_sha256 != current_request["request_sha256"]:
            raise ValueError(
                "warning_review_request_sha256 does not match the current artifact, "
                "warning details, validation context, or policy hashes"
            )
        current_fingerprints = {
            item["warning_fingerprint"] for item in current_request["warnings"]
        }
        unknown = sorted(set(warning_resolutions) - current_fingerprints)
        if unknown:
            raise ValueError(
                "warning resolution fingerprint not present in current request: "
                + ",".join(unknown)
            )
        if kind != "HUMAN":
            raise ValueError(
                "warning resolution proposals require warning_reviewer_kind=HUMAN; "
                "the caller assertion is recorded but grants no warning clearance"
            )
        if len(identity) < 3 or len(identity) > 128 or any(char in identity for char in "\r\n"):
            raise ValueError("warning_reviewer_id must be a 3-128 character human reviewer label")
        return {
            "reviewer_kind": "HUMAN",
            "reviewer_id_sha256": _sha256(identity.encode("utf-8")),
            "identity_verified": False,
            "review_clearance_granted": False,
            "attestation_status": "CALLER_ASSERTED_HUMAN_REVIEW",
            "warning_review_request_sha256": request_sha256,
            "proposed_warning_fingerprints": sorted(warning_resolutions),
        }
    if kind != "NONE" or identity or request_sha256:
        raise ValueError(
            "warning reviewer metadata and request hash are only valid with "
            "warning_resolutions proposals"
        )
    return {
        "reviewer_kind": "NONE",
        "reviewer_id_sha256": None,
        "identity_verified": False,
        "review_clearance_granted": False,
        "attestation_status": "NOT_PROVIDED",
        "warning_review_request_sha256": None,
        "proposed_warning_fingerprints": [],
    }


def _finding_key(finding: dict[str, Any]) -> tuple[str, str]:
    matched = re.sub(r"\s+", "", str(finding["matched"]))
    return str(finding["signal_id"]), matched


def _finding_hash(finding: dict[str, Any]) -> str:
    stable = {
        key: finding[key]
        for key in ("line", "column", "signal_id", "matched", "context", "severity", "action")
    }
    return _sha256(
        json.dumps(stable, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    )


def _finding_identity(finding: dict[str, Any]) -> tuple[str, int, int, str]:
    return (
        str(finding["signal_id"]),
        int(finding["line"]),
        int(finding["column"]),
        _finding_hash(finding),
    )


def _introduced_findings(
    before: Sequence[dict[str, Any]],
    after: Sequence[dict[str, Any]],
) -> list[dict[str, Any]]:
    remaining = Counter(_finding_key(item) for item in before if item["candidate"])
    introduced: list[dict[str, Any]] = []
    for finding in (item for item in after if item["candidate"]):
        key = _finding_key(finding)
        if remaining[key] > 0:
            remaining[key] -= 1
        else:
            introduced.append(finding)
    return introduced


def _public_finding(finding: dict[str, Any]) -> dict[str, Any]:
    public = {
        key: finding[key]
        for key in (
            "file",
            "line",
            "column",
            "signal_id",
            "severity",
            "action",
            "matched",
            "context",
            "count",
            "rationale",
        )
    }
    public["finding_hash"] = _finding_hash(finding)
    return public


def _resolve_keep_reasons(
    reasons: dict[str, str],
    findings: Sequence[dict[str, Any]],
    valid_ids: set[str],
) -> tuple[set[tuple[str, int, int, str]], list[dict[str, Any]]]:
    accepted: set[tuple[str, int, int, str]] = set()
    records: list[dict[str, Any]] = []
    for key, raw_reason in reasons.items():
        signal_id, binding = _parse_keep_key(key, valid_ids)
        reason = _validate_reason(raw_reason, f"{key} 的 KEEP 理由")
        matches = [item for item in findings if item["signal_id"] == signal_id]
        if binding is None:
            if len(matches) != 1:
                raise ValueError(
                    f"{signal_id} 对应 {len(matches)} 个待复核位置；"
                    "必须使用 SIGNAL_ID@LINE:COLUMN 或 @sha256:HASH"
                )
        elif binding.startswith("sha256:"):
            prefix = binding.removeprefix("sha256:")
            matches = [item for item in matches if _finding_hash(item).startswith(prefix)]
        else:
            line, column = (int(part) for part in binding.split(":", 1))
            matches = [
                item
                for item in matches
                if int(item["line"]) == line and int(item["column"]) == column
            ]
        if len(matches) != 1:
            raise ValueError(f"{key} 未唯一定位待复核 finding（匹配 {len(matches)} 个）")
        finding = matches[0]
        identity = _finding_identity(finding)
        if identity in accepted:
            raise ValueError(f"{key} 重复接受同一 finding")
        accepted.add(identity)
        record = _public_finding(finding)
        record.update({"binding": key, "reason": reason})
        records.append(record)
    return accepted, records


def validate(
    before_path: Path,
    after_path: Path,
    *,
    scene: str = "AUTO",
    keep_reasons: dict[str, str] | None = None,
    accepted_warnings: dict[str, str] | None = None,
    warning_resolutions: dict[str, str] | None = None,
    warning_review_request_sha256: str = "",
    warning_reviewer_kind: str = "NONE",
    warning_reviewer_id: str = "",
    strict_speech_acts: bool = False,
    protected_terms: Sequence[str] = (),
) -> dict[str, Any]:
    before_raw, before_text = _read_utf8(before_path)
    after_raw, after_text = _read_utf8(after_path)
    lexicon = lexical.load_lexicon()
    keep_reasons = keep_reasons or {}
    accepted_warnings = accepted_warnings or {}
    warning_resolutions = warning_resolutions or {}
    if accepted_warnings:
        raise ValueError(
            "accepted_warnings/--accept-warning is retired because a caller assertion "
            "cannot clear warnings; use warning_resolutions/--propose-warning-resolution "
            "with the current review request"
        )
    terms = invariants.normalize_protected_terms(protected_terms)
    valid_signal_ids = {item["id"] for item in lexicon["signals"]}
    for key, reason in keep_reasons.items():
        _parse_keep_key(key, valid_signal_ids)
        _validate_reason(reason, f"{key} 的 KEEP 理由")

    invariant_result = invariants.check_documents(
        before_text,
        after_text,
        document_format=_document_format(before_path, after_path),
        strict_speech_acts=strict_speech_acts,
        protected_terms=terms,
    )
    before_findings = lexical.scan_text(
        before_text,
        file=str(before_path),
        scene=scene,
        lexicon=lexicon,
    )
    after_findings = lexical.scan_text(
        after_text,
        file=str(after_path),
        scene=scene,
        lexicon=lexicon,
    )
    introduced = _introduced_findings(before_findings, after_findings)
    reviewable_by_identity: dict[tuple[str, int, int, str], dict[str, Any]] = {}
    for item in after_findings:
        if item["candidate"] and item["severity"] == "high":
            reviewable_by_identity[_finding_identity(item)] = item
    for item in introduced:
        reviewable_by_identity[_finding_identity(item)] = item
    accepted_identities, accepted_findings = _resolve_keep_reasons(
        keep_reasons,
        list(reviewable_by_identity.values()),
        valid_signal_ids,
    )
    unexplained_high = [
        item
        for item in after_findings
        if item["candidate"]
        and item["severity"] == "high"
        and _finding_identity(item) not in accepted_identities
    ]
    unexplained_introduced = [
        item for item in introduced if _finding_identity(item) not in accepted_identities
    ]
    normalized_resolutions: dict[str, str] = {}
    for fingerprint, reason in warning_resolutions.items():
        if not re.fullmatch(r"[0-9a-fA-F]{64}", fingerprint):
            raise ValueError(
                "warning resolution keys must be full 64-character warning fingerprints"
            )
        normalized_fingerprint = fingerprint.lower()
        if normalized_fingerprint in normalized_resolutions:
            raise ValueError(f"duplicate warning resolution: {normalized_fingerprint}")
        normalized_resolutions[normalized_fingerprint] = _validate_reason(
            reason,
            f"{normalized_fingerprint} 的处理建议",
        )
    warning_resolutions = normalized_resolutions
    before_sha256 = _sha256(before_raw)
    after_sha256 = _sha256(after_raw)
    document_format = _document_format(before_path, after_path)
    protected_term_evidence = invariant_result.evidence["protected_terms"]
    warning_review_request = _build_warning_review_request(
        invariant_result.warnings,
        before_sha256=before_sha256,
        after_sha256=after_sha256,
        scene=scene,
        document_format=document_format,
        protected_terms=protected_term_evidence,
        strict_speech_acts=strict_speech_acts,
    )
    warning_review = _warning_review_attestation(
        warning_resolutions,
        warning_review_request_sha256,
        warning_reviewer_kind,
        warning_reviewer_id,
        warning_review_request,
    )
    unaccepted_warnings = list(invariant_result.warnings)
    proposed_fingerprints = {item.lower() for item in warning_resolutions}
    warnings_without_resolution_proposal = [
        item
        for item in invariant_result.warnings
        if _warning_fingerprint(item) not in proposed_fingerprints
    ]

    if invariant_result.errors:
        status, exit_code = "FAIL", 1
    elif unaccepted_warnings or unexplained_high or unexplained_introduced:
        status, exit_code = "REVIEW", 2
    else:
        status, exit_code = "PASS", 0

    hard_invariant_layer_status = "FAIL" if invariant_result.errors else "PASS"
    speech_act_layer_status = "REVIEW" if unaccepted_warnings else "PASS"
    style_signal_layer_status = (
        "REVIEW" if unexplained_high or unexplained_introduced else "PASS"
    )

    review_reasons: list[str] = []
    if unaccepted_warnings:
        review_reasons.append("speech_act_warning")
    if unexplained_high:
        review_reasons.append("unexplained_high_severity_signal")
    if unexplained_introduced:
        review_reasons.append("introduced_style_signal")

    return {
        "status": status,
        "exit_code": exit_code,
        "delivery_gate_status": status,
        "delivery_gate_exit_code": exit_code,
        "hard_invariant_layer_status": hard_invariant_layer_status,
        "speech_act_layer_status": speech_act_layer_status,
        "style_signal_layer_status": style_signal_layer_status,
        "academic_correctness": "NOT_EVALUATED",
        "scene": scene.upper(),
        "evidence": {
            "checker_executed": True,
            "before_path": str(before_path.resolve()),
            "after_path": str(after_path.resolve()),
            "before_sha256": before_sha256,
            "after_sha256": after_sha256,
            "document_format": document_format,
            "protected_terms": protected_term_evidence,
        },
        "invariants": invariant_result.to_dict(),
        "lexical_summary": {
            "before_candidates": len(before_findings),
            "after_candidates": len(after_findings),
            "introduced_candidates": len(introduced),
            "unexplained_high_candidates": len(unexplained_high),
            "accepted_candidates": len(accepted_findings),
        },
        "review_reasons": review_reasons,
        "keep_reasons": dict(sorted(keep_reasons.items())),
        "accepted_warning_reasons": {},
        "warning_resolutions": dict(sorted(warning_resolutions.items())),
        "warning_review_request": warning_review_request,
        "warning_review": warning_review,
        "accepted_findings": accepted_findings,
        "accepted_warnings": [],
        "proposed_warning_resolutions": [
            {
                **_public_warning(item),
                "reason": warning_resolutions[_warning_fingerprint(item)],
                "review_clearance_granted": False,
            }
            for item in invariant_result.warnings
            if _warning_fingerprint(item) in proposed_fingerprints
        ],
        "pending_warnings": [_public_warning(item) for item in unaccepted_warnings],
        "warnings_without_resolution_proposal": [
            _public_warning(item) for item in warnings_without_resolution_proposal
        ],
        "unaccepted_warnings": [_public_warning(item) for item in unaccepted_warnings],
        "unexplained_high_findings": [_public_finding(item) for item in unexplained_high],
        "introduced_findings": [_public_finding(item) for item in unexplained_introduced],
    }


def _text_output(payload: dict[str, Any]) -> str:
    evidence = payload["evidence"]
    summary = payload["lexical_summary"]
    lines = [
        f"status: {payload['status']}",
        f"delivery_gate_status: {payload['delivery_gate_status']}",
        f"hard_invariant_layer_status: {payload['hard_invariant_layer_status']}",
        f"speech_act_layer_status: {payload['speech_act_layer_status']}",
        f"style_signal_layer_status: {payload['style_signal_layer_status']}",
        f"academic_correctness: {payload['academic_correctness']}",
        f"warning_reviewer_kind: {payload['warning_review']['reviewer_kind']}",
        f"warning_review_attestation_status: {payload['warning_review']['attestation_status']}",
        f"warning_reviewer_identity_verified: {str(payload['warning_review']['identity_verified']).upper()}",
        f"warning_review_clearance_granted: {str(payload['warning_review']['review_clearance_granted']).upper()}",
        f"warning_reviewer_id_sha256: {payload['warning_review']['reviewer_id_sha256'] or 'NONE'}",
        "warning_review_request_sha256: "
        + (
            payload["warning_review_request"]["request_sha256"]
            if payload["warning_review_request"]
            else "NONE"
        ),
        f"before_sha256: {evidence['before_sha256']}",
        f"after_sha256: {evidence['after_sha256']}",
        f"protected_terms: {evidence['protected_terms']['status']}",
        f"protected_term_count: {evidence['protected_terms']['count']}",
        f"protected_term_sha256: {evidence['protected_terms']['sha256'] or 'NONE'}",
        f"invariant_errors: {payload['invariants']['summary']['errors']}",
        f"invariant_warnings: {payload['invariants']['summary']['warnings']}",
        f"after_candidates: {summary['after_candidates']}",
        f"introduced_candidates: {summary['introduced_candidates']}",
        f"unexplained_high_candidates: {summary['unexplained_high_candidates']}",
        f"accepted_candidates: {summary['accepted_candidates']}",
    ]
    for reason in payload["review_reasons"]:
        lines.append(f"review: {reason}")
    for warning in payload["unaccepted_warnings"]:
        lines.append(
            f"warning: {warning['code']} [{warning['severity']}] {warning['message']}"
        )
    for finding in payload["unexplained_high_findings"]:
        lines.append(
            f"[{finding['signal_id']}/{finding['severity']}] "
            f"{finding['file']}:{finding['line']}:{finding['column']} {finding['matched']}"
        )
    return "\n".join(lines) + "\n"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="验证纯文风改写的不变量、残留高风险信号与新增模板。"
    )
    parser.add_argument("before", type=Path, help="改写前 UTF-8 Markdown/TeX")
    parser.add_argument("after", type=Path, help="改写后 UTF-8 Markdown/TeX")
    parser.add_argument(
        "--scene",
        type=str.upper,
        choices=lexical.SCENE_CHOICES,
        default="AUTO",
    )
    parser.add_argument("--format", choices=("json", "text"), default="text", dest="output_format")
    parser.add_argument(
        "--keep-reason",
        action="append",
        default=[],
        metavar="SIGNAL_ID[@LINE:COLUMN]=具体理由",
        help="为唯一高风险命中登记理由；多命中时必须绑定位置或 finding hash；可重复",
    )
    parser.add_argument(
        "--strict-speech-acts",
        action="store_true",
        help="把否定、模态、定义、报告状态等变化升级为硬错误",
    )
    parser.add_argument(
        "--accept-warning",
        action="append",
        default=[],
        metavar="CODE=具体理由",
        help="已停用；任何非空值都会报错，调用方声明不得清除 warning",
    )
    parser.add_argument(
        "--propose-warning-resolution",
        action="append",
        default=[],
        metavar="WARNING_FINGERPRINT=具体处理建议",
        help="对当前 review request 中的 warning 提交处理建议；只记录，不清除 REVIEW",
    )
    parser.add_argument(
        "--warning-review-request-sha256",
        default="",
        metavar="SHA256",
        help="首次 REVIEW 输出的 request_sha256；绑定 artifact、warning、配置与 policy",
    )
    parser.add_argument(
        "--warning-reviewer-kind",
        type=str.upper,
        choices=("HUMAN",),
        default="NONE",
        help="处理建议的声明审阅者类型；仅记录 HUMAN 声明，不验证身份也不授予 clearance",
    )
    parser.add_argument(
        "--warning-reviewer-id",
        default="",
        help="调用方提供的人工审阅者标签；输出只保存 SHA-256，不保存原标签，也不构成身份认证",
    )
    parser.add_argument(
        "--term",
        action="append",
        default=[],
        metavar="TERM",
        help="精确保护方法名、材料名或术语；可重复，未提供时不声称已自动校验",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        lexicon = lexical.load_lexicon()
        valid_ids = {item["id"] for item in lexicon["signals"]}
        keep_reasons = _parse_keep_reasons(args.keep_reason, valid_ids)
        if args.accept_warning:
            raise ValueError(
                "--accept-warning is retired because caller assertions cannot clear warnings; "
                "use --propose-warning-resolution with the current review request"
            )
        warning_resolutions = _parse_reason_pairs(
            args.propose_warning_resolution,
            "--propose-warning-resolution",
        )
        payload = validate(
            args.before,
            args.after,
            scene=args.scene,
            keep_reasons=keep_reasons,
            warning_resolutions=warning_resolutions,
            warning_review_request_sha256=args.warning_review_request_sha256,
            warning_reviewer_kind=args.warning_reviewer_kind,
            warning_reviewer_id=args.warning_reviewer_id,
            strict_speech_acts=args.strict_speech_acts,
            protected_terms=args.term,
        )
    except (OSError, UnicodeError, ValueError, json.JSONDecodeError) as error:
        parser.error(str(error))
    if args.output_format == "json":
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        sys.stdout.write(_text_output(payload))
    return int(payload["exit_code"])


if __name__ == "__main__":
    raise SystemExit(main())
