# -*- coding: utf-8 -*-
"""Build a whole-book index and heuristic audit ledger for solution environments."""

from __future__ import annotations

import csv
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEX_PATH = ROOT / "elegantbook2.tex"
OUT_DIR = ROOT / "solution_quality_audit"


def has_any(text: str, needles: list[str]) -> bool:
    return any(needle in text for needle in needles)


def esc_md(value: object) -> str:
    return str(value).replace("|", r"\|").replace("\n", " ")


def main() -> None:
    lines = TEX_PATH.read_text(encoding="utf-8", errors="replace").splitlines()

    chapter = section = subsection = ""
    last_ex: dict[str, object] | None = None
    current_sol: dict[str, object] | None = None
    solutions: list[dict[str, object]] = []

    chapter_re = re.compile(r"^\\chapter\{(.+)\}")
    section_re = re.compile(r"^\\section\{(.+)\}")
    subsection_re = re.compile(r"^\\subsection\{(.+)\}")
    problem_envs = "exercise|example|theorem|proposition|property"
    exercise_begin_re = re.compile(rf"^\\begin\{{({problem_envs})\}}(?:\[(.*?)\])?")

    for line_no, line in enumerate(lines, start=1):
        if match := chapter_re.match(line):
            chapter = match.group(1)
            section = subsection = ""
        if match := section_re.match(line):
            section = match.group(1)
            subsection = ""
        if match := subsection_re.match(line):
            subsection = match.group(1)

        if match := exercise_begin_re.match(line):
            last_ex = {
                "env": match.group(1),
                "start": line_no,
                "title": match.group(2) or "",
                "body": [],
            }
        elif last_ex and line.startswith(rf"\end{{{last_ex.get('env')}}}"):
            last_ex["end"] = line_no
        elif last_ex and "end" not in last_ex:
            stripped = line.strip()
            if stripped:
                body = last_ex.setdefault("body", [])
                assert isinstance(body, list)
                body.append(stripped)

        if line.startswith(r"\begin{solution}"):
            body_preview = []
            if last_ex:
                raw_body = last_ex.get("body", [])
                if isinstance(raw_body, list):
                    body_preview = raw_body[:3]
            current_sol = {
                "start": line_no,
                "chapter": chapter,
                "section": section,
                "subsection": subsection,
                "exercise_start": last_ex.get("start") if last_ex else "",
                "exercise_end": last_ex.get("end") if last_ex else "",
                "exercise_title": last_ex.get("title") if last_ex else "",
                "exercise_preview": " ".join(str(x) for x in body_preview)[:240],
                "body": [],
            }
        elif line.startswith(r"\end{solution}") and current_sol:
            current_sol["end"] = line_no
            body = current_sol["body"]
            assert isinstance(body, list)
            text = "\n".join(str(x) for x in body)
            one_line = " ".join(str(x).strip() for x in body if str(x).strip())

            short_displays: list[str] = []
            display_blocks: list[tuple[int, int, str]] = []
            in_display = False
            display_start = 0
            buffer: list[str] = []
            for offset, body_line in enumerate(body, start=int(current_sol["start"]) + 1):
                trimmed = str(body_line).strip()
                if not in_display and trimmed == r"\[":
                    in_display = True
                    display_start = offset
                    buffer = []
                    continue
                if in_display and trimmed == r"\]":
                    block = " ".join(item.strip() for item in buffer)
                    display_blocks.append((display_start, offset, block))
                    if r"\begin{" not in block and len(block) <= 220:
                        short_displays.append(f"{display_start}:{block[:160]}")
                    in_display = False
                    continue
                if in_display:
                    buffer.append(str(body_line))

            display_count = len(display_blocks)
            env_display_count = sum(
                text.count(env)
                for env in [
                    r"\begin{align}",
                    r"\begin{align*}",
                    r"\begin{equation}",
                    r"\begin{equation*}",
                    r"\begin{gather}",
                    r"\begin{gather*}",
                    r"\begin{multline}",
                    r"\begin{multline*}",
                ]
            )

            inline_long_lines: list[str] = []
            for offset, body_line in enumerate(body, start=int(current_sol["start"]) + 1):
                line_text = str(body_line)
                if len(line_text) >= 170 and (
                    r"\(" in line_text or "$" in line_text or r"\displaystyle" in line_text
                ):
                    inline_long_lines.append(f"{offset}:{len(line_text)}")

            jump_keywords = [
                keyword
                for keyword in [
                    "计算得",
                    "可得",
                    "化简得",
                    "代入得",
                    "显然",
                    "同理",
                    "直接",
                    "立即",
                    "容易",
                    "不难",
                    "略",
                    "类似可得",
                    "整理得",
                    "于是",
                ]
                if keyword in one_line
            ]

            combined = str(current_sol["exercise_preview"]) + "\n" + one_line
            tag_keywords = {
                "曲线积分": ["曲线积分", r"\oint", r"\int_L", r"\int_\Gamma", r"\int_C"],
                "曲面积分/通量": [
                    "曲面积分",
                    "曲面",
                    r"\iint_\Sigma",
                    "通量",
                    "法向",
                    "外侧",
                    "上侧",
                    "下侧",
                ],
                "Green/Gauss/Stokes": ["Green", "高斯", "Gauss", "Stokes", "斯托克斯", "格林"],
                "级数/幂级数": ["级数", "收敛", "一致收敛", "幂级数", "Taylor", "泰勒"],
                "微分方程": ["微分方程", "通解", "特解", "特征根", "特征方程"],
                "极值/拉格朗日": ["极值", "最大", "最小", "Lagrange", "拉格朗日", "驻点"],
                "隐函数/偏导": ["偏导", "隐函数", "Jacobian", "雅可比", "链式", "梯度", "方向导数"],
                "重积分/换元": [
                    "重积分",
                    "二重积分",
                    "三重积分",
                    "换元",
                    "极坐标",
                    "柱坐标",
                    "球坐标",
                    r"\iiint",
                    r"\iint_D",
                ],
                "Fourier": ["Fourier", "傅里叶", "正弦级数", "余弦级数"],
            }
            risk_tags = [tag for tag, needles in tag_keywords.items() if has_any(combined, needles)]

            defect_flags: list[str] = []
            if jump_keywords:
                defect_flags.append("跳步关键词")
            if inline_long_lines:
                defect_flags.append("长行内公式/排版风险")
            if short_displays:
                defect_flags.append("短display待判定")
            if len(body) <= 5 and any(
                tag
                in [
                    "曲线积分",
                    "曲面积分/通量",
                    "Green/Gauss/Stokes",
                    "级数/幂级数",
                    "微分方程",
                    "极值/拉格朗日",
                    "隐函数/偏导",
                    "重积分/换元",
                ]
                for tag in risk_tags
            ):
                defect_flags.append("高风险题解过短")
            if display_count + env_display_count >= 4 and len(body) <= 18:
                defect_flags.append("display密度偏高")

            current_sol.update(
                {
                    "line_count": int(current_sol["end"]) - int(current_sol["start"]) + 1,
                    "display_count": display_count,
                    "env_display_count": env_display_count,
                    "short_display_count": len(short_displays),
                    "short_display_samples": " | ".join(short_displays[:3]),
                    "inline_long_count": len(inline_long_lines),
                    "inline_long_lines": "; ".join(inline_long_lines[:6]),
                    "jump_keywords": ",".join(jump_keywords),
                    "risk_tags": ",".join(risk_tags),
                    "defect_flags": ",".join(defect_flags),
                    "audit_status": (
                        "AUTO_FLAGGED_NEEDS_MANUAL"
                        if defect_flags
                        else "AUTO_INDEXED_NO_HEURISTIC_FLAG"
                    ),
                    "suggested_action": (
                        "人工逐题复核；若确认则补推导/改排版/统一方法"
                        if defect_flags
                        else "抽检复核"
                    ),
                }
            )
            current_sol.pop("body", None)
            solutions.append(current_sol)
            current_sol = None
        elif current_sol is not None:
            body = current_sol["body"]
            assert isinstance(body, list)
            body.append(line)

    section_counts: dict[tuple[object, object, object], int] = {}
    for index, solution in enumerate(solutions, start=1):
        key = (solution["chapter"], solution["section"], solution["subsection"])
        section_counts[key] = section_counts.get(key, 0) + 1
        solution["global_no"] = index
        solution["local_no"] = section_counts[key]
        solution["solution_start"] = solution.pop("start")
        solution["solution_end"] = solution.pop("end")

    fields = [
        "global_no",
        "local_no",
        "chapter",
        "section",
        "subsection",
        "exercise_start",
        "exercise_end",
        "solution_start",
        "solution_end",
        "line_count",
        "exercise_title",
        "exercise_preview",
        "risk_tags",
        "audit_status",
        "defect_flags",
        "jump_keywords",
        "display_count",
        "env_display_count",
        "short_display_count",
        "short_display_samples",
        "inline_long_count",
        "inline_long_lines",
        "suggested_action",
    ]
    with (OUT_DIR / "solution_index.csv").open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(solutions)

    summary: dict[str, object] = {
        "total_solutions": len(solutions),
        "auto_flagged": sum(
            1 for solution in solutions if solution["audit_status"] == "AUTO_FLAGGED_NEEDS_MANUAL"
        ),
        "long_inline_flagged": sum(1 for solution in solutions if solution["inline_long_count"] > 0),
        "jump_keyword_flagged": sum(1 for solution in solutions if solution["jump_keywords"]),
        "short_display_flagged": sum(
            1 for solution in solutions if solution["short_display_count"] > 0
        ),
        "by_chapter": {},
        "by_risk_tag": {},
        "by_defect_flag": {},
    }
    for solution in solutions:
        by_chapter = summary["by_chapter"]
        by_risk_tag = summary["by_risk_tag"]
        by_defect_flag = summary["by_defect_flag"]
        assert isinstance(by_chapter, dict)
        assert isinstance(by_risk_tag, dict)
        assert isinstance(by_defect_flag, dict)
        chapter_name = str(solution["chapter"])
        by_chapter[chapter_name] = by_chapter.get(chapter_name, 0) + 1
        for tag in filter(None, str(solution["risk_tags"]).split(",")):
            by_risk_tag[tag] = by_risk_tag.get(tag, 0) + 1
        for flag in filter(None, str(solution["defect_flags"]).split(",")):
            by_defect_flag[flag] = by_defect_flag.get(flag, 0) + 1
    (OUT_DIR / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    flagged = [
        solution
        for solution in solutions
        if solution["audit_status"] == "AUTO_FLAGGED_NEEDS_MANUAL"
    ]
    markdown: list[str] = []
    markdown.append("# 全书 solution 质量整改台账\n")
    markdown.append("## 说明\n")
    markdown.append(
        "- 本台账由当前 `elegantbook2.tex` 自动全域遍历生成，覆盖每一个 `solution` 环境。\n"
    )
    markdown.append(
        "- `AUTO_FLAGGED_NEEDS_MANUAL` 不是最终定罪，只是优先人工复核队列；后续需要逐题审校并交 GPT-5.5 子代理复核。\n"
    )
    markdown.append(
        "- 硬性整改口径：补齐跳步、统一前文方法、修正数学错误、长行内公式回退为规范行间公式，禁止过度压缩。\n"
    )
    markdown.append("\n## 汇总\n")
    for key, value in summary.items():
        if isinstance(value, dict):
            markdown.append(
                f"- `{key}`: " + ", ".join(f"{k}={v}" for k, v in value.items()) + "\n"
            )
        else:
            markdown.append(f"- `{key}`: {value}\n")
    markdown.append("\n## 自动标记缺陷队列\n")
    markdown.append("| 全局序号 | 行号 | 章节 | 小节 | 题目预览 | 标签 | 标记 | 证据 | 建议 |\n")
    markdown.append("|---:|---:|---|---|---|---|---|---|---|\n")
    for solution in flagged[:400]:
        evidence = "; ".join(
            item
            for item in [
                str(solution["jump_keywords"]),
                str(solution["inline_long_lines"]),
                str(solution["short_display_samples"]),
            ]
            if item
        )
        markdown.append(
            f"| {solution['global_no']} | {solution['solution_start']} | "
            f"{esc_md(solution['chapter'])} | "
            f"{esc_md(solution['section'] or solution['subsection'])} | "
            f"{esc_md(solution['exercise_title'] or str(solution['exercise_preview'])[:80])} | "
            f"{esc_md(solution['risk_tags'])} | {esc_md(solution['defect_flags'])} | "
            f"{esc_md(evidence[:180])} | {esc_md(solution['suggested_action'])} |\n"
        )
    if len(flagged) > 400:
        markdown.append(
            f"\n> 自动标记项共 {len(flagged)} 条，Markdown 仅列前 400 条；"
            "完整逐题台账见 `solution_quality_audit/solution_index.csv`。\n"
        )
    markdown.append("\n## 全量逐题索引\n")
    markdown.append("| 全局序号 | 行号 | 章节 | 小节 | 状态 | 标记 |\n")
    markdown.append("|---:|---:|---|---|---|---|\n")
    for solution in solutions:
        markdown.append(
            f"| {solution['global_no']} | {solution['solution_start']} | "
            f"{esc_md(solution['chapter'])} | "
            f"{esc_md(solution['section'] or solution['subsection'])} | "
            f"{solution['audit_status']} | {esc_md(solution['defect_flags'])} |\n"
        )
    (OUT_DIR / "solution_quality_ledger.md").write_text("".join(markdown), encoding="utf-8")

    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
