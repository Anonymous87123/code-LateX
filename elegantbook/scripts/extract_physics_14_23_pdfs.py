from __future__ import annotations

import json
import re
import subprocess
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TMP_ROOT = ROOT / "tmp" / "pdfs" / "physics_14_23"
WORD_DIR = ROOT / "word"
EXTRACTED_MD = WORD_DIR / "physics_14_23_extracted.md"
AUDIT_MD = WORD_DIR / "physics_14_23_extraction_audit.md"
MANIFEST_JSON = TMP_ROOT / "manifest.json"
PDFINFO = Path(r"E:\Program Files\LateX\texlive\2025\bin\windows\pdfinfo.exe")
PDFTOTEXT = Path(r"E:\Program Files\LateX\texlive\2025\bin\windows\pdftotext.exe")


PDFS = [
    ("14-1_coulomb", "14-1 库仑定律", Path(r"C:\Users\Lenovo\Desktop\学习资料\大物\14-1库仑定律.pdf")),
    ("14-2_electric_field", "14-2 电场 电场强度", Path(r"C:\Users\Lenovo\Desktop\学习资料\大物\14-2电场 电场强度.pdf")),
    ("14-3_gauss", "14-3 电通量与高斯定理", Path(r"C:\Users\Lenovo\Desktop\学习资料\大物\14-3电通量与高斯定理.pdf")),
    ("14-4_potential", "14-4 静电场的环路定理与电势", Path(r"C:\Users\Lenovo\Desktop\学习资料\大物\14-4 静电场的环路定理与电势.pdf")),
    ("14-5_equipotential", "14-5 等势面 场强与电势的微分关系", Path(r"C:\Users\Lenovo\Desktop\学习资料\大物\14-5等势面 场强与电势的微分关系.pdf")),
    ("15-1_conductor", "15-1 静电场中的导体", Path(r"C:\Users\Lenovo\Desktop\学习资料\大物\15-1 静电场中的导体.pdf")),
    ("15-2_dielectric", "15-2 静电场中的电介质", Path(r"C:\Users\Lenovo\Desktop\学习资料\大物\15-2 静电场中的电介质.pdf")),
    ("15-3_capacitor", "15-3 电容和电容器", Path(r"C:\Users\Lenovo\Desktop\学习资料\大物\15-3 电容和电容器.pdf")),
    ("15-4_electric_energy", "15-4 电场的能量", Path(r"C:\Users\Lenovo\Desktop\学习资料\大物\15-4 电场的能量.pdf")),
    ("16-1_current", "16-1 稳恒电流", Path(r"C:\Users\Lenovo\Desktop\学习资料\大物\16-1稳恒电流.pdf")),
    ("16-2_B", "16-2 磁场 磁感强度", Path(r"C:\Users\Lenovo\Desktop\学习资料\大物\16-2磁场 磁感强度.pdf")),
    ("16-3_biot_savart_motion", "16-3 毕萨定律 & 16-4 运动电荷的磁场", Path(r"C:\Users\Lenovo\Desktop\学习资料\大物\16-3毕萨定律&16-4运动电荷的磁场.pdf")),
    ("16-5_ampere", "16-5 磁场的高斯定理和安培环路定理", Path(r"C:\Users\Lenovo\Desktop\学习资料\大物\16-5磁场的高斯定理和安培环路定理.pdf")),
    ("17-1_lorentz", "17-1 磁场对运动电荷的作用", Path(r"C:\Users\Lenovo\Desktop\学习资料\大物\17-1磁场对运动电荷的作用.pdf")),
    ("17-2_wire_force", "17-2 磁场对载流导线的作用", Path(r"C:\Users\Lenovo\Desktop\学习资料\大物\17-2 磁场对载流导线的作用.pdf")),
    ("17-3_loop_work", "17-3 均匀磁场对载流线圈的作用 & 17-4 磁力做功", Path(r"C:\Users\Lenovo\Desktop\学习资料\大物\17-3均匀磁场对载流线圈的作用&17-4磁力做功.pdf")),
    ("18-1_magnetization", "18-1 磁介质及其磁化", Path(r"C:\Users\Lenovo\Desktop\学习资料\大物\18-1磁介质及其磁化.pdf")),
    ("18-2_magnetic_media_ampere", "18-2 磁介质中的安培环路定理", Path(r"C:\Users\Lenovo\Desktop\学习资料\大物\18-2磁介质中的安培环路定理.pdf")),
    ("18-3_ferromagnet", "18-3 铁磁质", Path(r"C:\Users\Lenovo\Desktop\学习资料\大物\18-3铁磁质.pdf")),
    ("19-1_induction", "19-1 电磁感应定律", Path(r"C:\Users\Lenovo\Desktop\学习资料\大物\19-1电磁感应定律.pdf")),
    ("19-2_emf", "19-2 动生与感生电动势", Path(r"C:\Users\Lenovo\Desktop\学习资料\大物\19-2动生与感生电动势.pdf")),
    ("19-3_inductance", "19-3 自感与互感", Path(r"C:\Users\Lenovo\Desktop\学习资料\大物\19-3自感与互感.pdf")),
    ("19-4_magnetic_energy", "19-4 磁场的能量", Path(r"C:\Users\Lenovo\Desktop\学习资料\大物\19-4磁场的能量.pdf")),
    ("20_maxwell", "20 麦克斯韦方程组", Path(r"C:\Users\Lenovo\Desktop\学习资料\大物\20麦克斯韦方程组.pdf")),
    ("21-1_sr_postulates", "21-1 狭义相对论基本原理", Path(r"C:\Users\Lenovo\Desktop\学习资料\大物\21-1 狭义相对论基本原理.pdf")),
    ("21-2_4_sr_space_time", "21-2&3&4 狭义相对论时空观 & 动力学", Path(r"C:\Users\Lenovo\Desktop\学习资料\大物\21-2&3&4 狭义相对论时空观&动力学.pdf")),
    ("22-1_blackbody", "22-1 黑体辐射与能量量子化", Path(r"C:\Users\Lenovo\Desktop\学习资料\大物\22-1 黑体辐射与能量量子化.pdf")),
    ("22-2_photoelectric", "22-2 光电效应", Path(r"C:\Users\Lenovo\Desktop\学习资料\大物\22-2 光电效应.pdf")),
    ("22-3_compton", "22-3 康普顿效应", Path(r"C:\Users\Lenovo\Desktop\学习资料\大物\22-3 康普顿效应.pdf")),
    ("22-4_bohr", "22-4 氢光谱和波尔氢原子模型", Path(r"C:\Users\Lenovo\Desktop\学习资料\大物\22-4 氢光谱和波尔氢原子模型.pdf")),
    ("23-1_debroglie", "23-1 德布罗意波 & 不确定关系", Path(r"C:\Users\Lenovo\Desktop\学习资料\大物\23-1 德布罗意波&不确定关系.pdf")),
    ("23-2_schrodinger", "23-2 波函数与薛定谔方程", Path(r"C:\Users\Lenovo\Desktop\学习资料\大物\23-2 波函数与薛定谔方程.pdf")),
    ("23-3_schrodinger_examples", "23-3 薛定谔方程应用举例", Path(r"C:\Users\Lenovo\Desktop\学习资料\大物\23-3 薛定谔方程应用举例.pdf")),
    ("23-4_hydrogen_quantum", "23-4 氢原子的量子态", Path(r"C:\Users\Lenovo\Desktop\学习资料\大物\23-4 氢原子的量子态.pdf")),
]

SUSPICIOUS_GLYPHS = ""
TOPIC_KEYS = [
    "高斯",
    "电势",
    "电容",
    "安培",
    "毕奥",
    "毕萨",
    "洛伦兹",
    "电磁感应",
    "麦克斯韦",
    "相对论",
    "光电效应",
    "康普顿",
    "波尔",
    "德布罗意",
    "薛定谔",
]


def run(command: list[str]) -> str:
    completed = subprocess.run(
        command,
        check=True,
        text=True,
        encoding="utf-8",
        errors="ignore",
        capture_output=True,
    )
    return completed.stdout


def extract_text(pdf_path: Path) -> str:
    return run([str(PDFTOTEXT), "-layout", "-enc", "UTF-8", str(pdf_path), "-"])


def page_count(pdf_path: Path) -> int:
    info = run([str(PDFINFO), str(pdf_path)])
    for line in info.splitlines():
        if line.startswith("Pages:"):
            return int(line.split(":", 1)[1].strip())
    raise RuntimeError(f"Could not find page count for {pdf_path}")


def split_pages(text: str) -> list[str]:
    pages = [page.rstrip() for page in text.split("\f")]
    while pages and not pages[-1].strip():
        pages.pop()
    return pages


def suspicious_counter(text: str) -> Counter[str]:
    return Counter(ch for ch in text if ch in SUSPICIOUS_GLYPHS)


def figure_heavy(page: str) -> bool:
    stripped = re.sub(r"\s+", "", page)
    if not stripped:
        return False
    han = len(re.findall(r"[\u4e00-\u9fffA-Za-z0-9]", stripped))
    return han < 120 and any(key in page for key in ("图", "示意", "光路", "环路", "场线", "实验"))


def formula_heavy(page: str) -> bool:
    return len(re.findall(r"[=+\-∫∮∂πλθμνρσφψω^_]", page)) >= 8 or any(
        ch in page for ch in SUSPICIOUS_GLYPHS
    )


def pick_flagged_lines(page: str, limit: int = 5) -> list[str]:
    lines: list[str] = []
    for raw_line in page.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if any(ch in line for ch in SUSPICIOUS_GLYPHS) or re.search(r"[=∫∮∂πλθμνρσφψω]", line):
            lines.append(line)
        if len(lines) >= limit:
            break
    return lines


def write_page_bundles(slug: str, pages: list[str]) -> None:
    page_dir = TMP_ROOT / slug / "pages"
    page_dir.mkdir(parents=True, exist_ok=True)
    for index, page in enumerate(pages, start=1):
        (page_dir / f"{index:03d}.txt").write_text(page + "\n", encoding="utf-8")


def topic_hits(text: str) -> list[str]:
    return [key for key in TOPIC_KEYS if key in text]


def build_outputs() -> list[dict[str, object]]:
    TMP_ROOT.mkdir(parents=True, exist_ok=True)
    WORD_DIR.mkdir(parents=True, exist_ok=True)

    manifest: list[dict[str, object]] = []
    extracted_lines = [
        "# Physics 14-23 PDF Extracted Text",
        "",
        "说明：",
        "- 本稿使用 `pdftotext -layout` 从原始 PPT 导出的 PDF 中抽取。",
        "- 保留原 PDF 顺序、文件边界与页码边界，公式符号可能含有 PowerPoint 私有字形残留。",
        "- 后续正文写作与公式修正请结合 `physics_14_23_extraction_audit.md` 一并使用。",
        "",
    ]

    audit_lines = [
        "# Physics 14-23 Extraction Audit",
        "",
        "说明：",
        "- 本台账先记录批量抽取后的系统性风险，再列出每个 PDF 的重点疑难页。",
        "- `疑似公式损坏` 指文本能抽出但符号字体被替换或拆散，需要人工重写。",
        "- `图示缺失` 指文字能抽出但核心图形本体没有被文本表达，需要在正文中重建或补图。",
        "- `最终采用写法` 留给正文定稿时回填；本轮先尽量把会出问题的页和行暴露出来。",
        "",
        "## 系统性问题",
        "",
        "- 这些 PDF 多为 PowerPoint 导出，向量符号、积分号、希腊字母、粗体矢量和箭头常混入私有字形。",
        "- `pdftotext` 能较好保留正文，但经常把 `\\vec`、`\\oint`、`\\nabla`、希腊字母和上下标拆散。",
        "- 人物照片、实验照片和示意图本体不会被文本提取，需要靠正文讲解或 TikZ 重建。",
        "- 量子力学、麦克斯韦方程组、磁场积分定律、相对论时空图这几组内容的人工复核优先级最高。",
        "",
    ]

    total_pages = 0
    total_suspicious = Counter()

    for slug, title, path in PDFS:
        page_total = page_count(path)
        text = extract_text(path)
        pages = split_pages(text)
        write_page_bundles(slug, pages)
        (TMP_ROOT / slug / "full.txt").write_text(text, encoding="utf-8")

        pdf_counter = suspicious_counter(text)
        total_suspicious.update(pdf_counter)
        total_pages += page_total
        topics = topic_hits(text)

        manifest.append(
            {
                "slug": slug,
                "title": title,
                "path": str(path),
                "page_count_pdfinfo": page_total,
                "page_count_extracted": len(pages),
                "suspicious_glyphs": dict(pdf_counter),
                "topics": topics,
            }
        )

        extracted_lines.extend(
            [
                f"## {title}",
                "",
                f"- Source PDF: `{path}`",
                f"- PDF pages: {page_total}",
                f"- Extracted pages: {len(pages)}",
                "",
            ]
        )
        for page_no, page in enumerate(pages, start=1):
            extracted_lines.extend(
                [
                    f"### Page {page_no}",
                    "",
                    "```text",
                    page.rstrip(),
                    "```",
                    "",
                ]
            )

        audit_lines.extend(
            [
                f"## {title}",
                "",
                f"- PDF 页数：{page_total}",
                f"- 提取页数：{len(pages)}",
                f"- 主题命中：{'、'.join(topics) if topics else '未自动识别'}",
                f"- 可疑字形统计：{json.dumps(dict(pdf_counter), ensure_ascii=False, sort_keys=True) if pdf_counter else '{}'}",
                "",
                "| 页码 | 风险类型 | 线索 | 提取片段 | 最终采用写法 |",
                "| ---: | --- | --- | --- | --- |",
            ]
        )
        for page_no, page in enumerate(pages, start=1):
            risks: list[str] = []
            if formula_heavy(page):
                risks.append("疑似公式损坏")
            if figure_heavy(page):
                risks.append("图示缺失")
            if not risks:
                continue
            excerpt = " / ".join(pick_flagged_lines(page, limit=3))
            excerpt = excerpt.replace("|", "\\|")
            clue = "；".join(risks)
            audit_lines.append(
                f"| {page_no} | {clue} | 需人工复核符号或示意图 | {excerpt[:180]} | 待回填 |"
            )
        audit_lines.append("")

    extracted_lines.extend(
        [
            "## Summary",
            "",
            f"- Total PDFs: {len(PDFS)}",
            f"- Total PDF pages: {total_pages}",
            f"- Suspicious glyph totals: {json.dumps(dict(total_suspicious), ensure_ascii=False, sort_keys=True)}",
            "",
        ]
    )

    audit_lines.extend(
        [
            "## 总量统计",
            "",
            f"- PDF 数量：{len(PDFS)}",
            f"- 总页数：{total_pages}",
            f"- 全局可疑字形统计：{json.dumps(dict(total_suspicious), ensure_ascii=False, sort_keys=True)}",
            "",
        ]
    )

    EXTRACTED_MD.write_text("\n".join(extracted_lines) + "\n", encoding="utf-8")
    AUDIT_MD.write_text("\n".join(audit_lines) + "\n", encoding="utf-8")
    MANIFEST_JSON.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    return manifest


def main() -> None:
    build_outputs()


if __name__ == "__main__":
    main()
