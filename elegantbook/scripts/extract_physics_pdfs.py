from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "tmp" / "pdfs" / "physics_bridge"
PDFINFO = Path(r"E:\Program Files\LateX\texlive\2025\bin\windows\pdfinfo.exe")
PDFTOTEXT = Path(r"E:\Program Files\LateX\texlive\2025\bin\windows\pdftotext.exe")


PDFS = [
    {
        "slug": "ch01_kinematics",
        "title": "第一章 质点运动学",
        "path": Path(r"C:\Users\Lenovo\Desktop\学习资料\大物\1第一章 质点运动学.pdf"),
    },
    {
        "slug": "ch02_dynamics",
        "title": "第二章 质点动力学基础",
        "path": Path(r"C:\Users\Lenovo\Desktop\学习资料\大物\2第二章 质点动力学基础.pdf"),
    },
    {
        "slug": "ch03_conservation",
        "title": "第三章 三大守恒定律",
        "path": Path(r"C:\Users\Lenovo\Desktop\学习资料\大物\3第三章 三大守恒定律.pdf"),
    },
    {
        "slug": "ch04_rigidbody",
        "title": "第四章 刚体力学",
        "path": Path(r"C:\Users\Lenovo\Desktop\学习资料\大物\4第四章 刚体力学.pdf"),
    },
    {
        "slug": "ch05_vibration",
        "title": "第六章 机械振动",
        "path": Path(r"C:\Users\Lenovo\Desktop\学习资料\大物\5第六章 机械振动.pdf"),
    },
    {
        "slug": "ch06_wave",
        "title": "第七章 机械波",
        "path": Path(r"C:\Users\Lenovo\Desktop\学习资料\大物\6第七章 机械波.pdf"),
    },
    {
        "slug": "ch07_interference",
        "title": "第八章 光的干涉",
        "path": Path(r"C:\Users\Lenovo\Desktop\学习资料\大物\7第八章  光的干涉.pdf"),
    },
    {
        "slug": "ch08_diffraction",
        "title": "第九章 光的衍射",
        "path": Path(r"C:\Users\Lenovo\Desktop\学习资料\大物\8第九章 光的衍射.pdf"),
    },
    {
        "slug": "ch09_polarization",
        "title": "第十章 光的偏振",
        "path": Path(r"C:\Users\Lenovo\Desktop\学习资料\大物\9第十章 光的偏振.pdf"),
    },
    {
        "slug": "ch10_kinetic_theory",
        "title": "第十一章 气体动理论",
        "path": Path(r"C:\Users\Lenovo\Desktop\学习资料\大物\10第十一章 气体动理论.pdf"),
    },
    {
        "slug": "ch11_first_law",
        "title": "第十二章 热力学第一定律",
        "path": Path(r"C:\Users\Lenovo\Desktop\学习资料\大物\11第十二章 热力学第一定律.pdf"),
    },
    {
        "slug": "ch12_second_law",
        "title": "第十三章 热力学第二定律",
        "path": Path(r"C:\Users\Lenovo\Desktop\学习资料\大物\12第十三章 热力学第二定律.pdf"),
    },
    {
        "slug": "review_final",
        "title": "2024级大学物理1期末复习",
        "path": Path(r"C:\Users\Lenovo\Desktop\学习资料\大物\2024级大学物理1期末复习.pdf"),
    },
]

ADMIN_KEYWORDS = [
    "姓名",
    "学号",
    "作业",
    "提交",
    "考核",
    "要求",
    "课后",
    "课堂纪律",
    "课程安排",
    "考试范围",
    "说明",
]

FIGURE_KEYWORDS = [
    "图",
    "示意图",
    "图样",
    "光路",
    "曲线",
    "条纹",
    "波形",
    "受力图",
]

EXAMPLE_KEYWORDS = [
    "例",
    "例题",
    "解：",
    "解答",
    "思考",
    "讨论",
]

TOPIC_KEYWORDS = [
    "质点",
    "位移",
    "速度",
    "加速度",
    "牛顿",
    "动量",
    "角动量",
    "动能",
    "机械能",
    "转动惯量",
    "简谐",
    "机械波",
    "干涉",
    "衍射",
    "偏振",
    "麦克斯韦",
    "自由度",
    "压强",
    "温度",
    "卡诺",
    "熵",
    "绝热",
    "等温",
    "等压",
    "自由膨胀",
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


def page_count(pdf_path: Path) -> int:
    info = run([str(PDFINFO), str(pdf_path)])
    for line in info.splitlines():
        if line.startswith("Pages:"):
            return int(line.split(":", 1)[1].strip())
    raise RuntimeError(f"Could not find page count for {pdf_path}")


def extract_text(pdf_path: Path) -> str:
    return run([str(PDFTOTEXT), "-layout", str(pdf_path), "-"])


def split_pages(text: str) -> list[str]:
    pages = [page.rstrip() for page in text.split("\f")]
    while pages and not pages[-1].strip():
        pages.pop()
    return pages


def detect_topics(text: str) -> list[str]:
    topics = [kw for kw in TOPIC_KEYWORDS if kw in text]
    return topics[:6]


def count_keyword_hits(text: str, keywords: list[str]) -> int:
    return sum(1 for kw in keywords if kw in text)


def count_formula_signals(text: str) -> int:
    return len(re.findall(r"[=\\\^\_\+\-∫∂Δλθπ\(\)]", text))


def classify_page(text: str) -> tuple[str, str]:
    stripped = text.strip()
    admin_hits = count_keyword_hits(stripped, ADMIN_KEYWORDS)
    figure_hits = count_keyword_hits(stripped, FIGURE_KEYWORDS)
    example_hits = count_keyword_hits(stripped, EXAMPLE_KEYWORDS)
    formula_hits = count_formula_signals(stripped)
    topics = detect_topics(stripped)

    if admin_hits >= 2 and formula_hits < 8 and example_hits == 0:
        return "admin-only-excluded", "行政/说明性内容为主，知识正文可排除。"
    if figure_hits >= 2 and formula_hits < 12 and example_hits == 0:
        return "deferred-figure-detail", "页面以图示/图题为主，先保留文字说明，图形本体留待下一轮。"
    if formula_hits >= 10 or example_hits > 0 or topics:
        return "used-needs-formula-check", "知识内容已进入正文草稿，但符号与推导仍建议逐页复核。"
    return "used-finalized", "以讲解型段落为主，当前版本已足以作为初稿正文。"


def write_page_bundle(slug: str, pages: list[str]) -> None:
    page_dir = OUT_DIR / slug / "pages"
    page_dir.mkdir(parents=True, exist_ok=True)
    for index, page in enumerate(pages, start=1):
        (page_dir / f"{index:03d}.txt").write_text(page + "\n", encoding="utf-8")


def build_manifest() -> list[dict[str, object]]:
    manifest: list[dict[str, object]] = []
    for spec in PDFS:
        pages = page_count(spec["path"])
        text = extract_text(spec["path"])
        split = split_pages(text)
        bundle_dir = OUT_DIR / spec["slug"]
        bundle_dir.mkdir(parents=True, exist_ok=True)
        (bundle_dir / "full.txt").write_text(text, encoding="utf-8")
        write_page_bundle(spec["slug"], split)
        manifest.append(
            {
                "slug": spec["slug"],
                "title": spec["title"],
                "source_pdf": str(spec["path"]),
                "page_count_pdfinfo": pages,
                "page_count_extracted": len(split),
            }
        )
    return manifest


def write_reports(manifest: list[dict[str, object]]) -> None:
    (OUT_DIR / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    lines = [
        "# Physics PDF Extraction Ledger",
        "",
        "| Slug | Title | PDF pages | Extracted pages |",
        "| --- | --- | ---: | ---: |",
    ]
    total_pages = 0
    for item in manifest:
        total_pages += int(item["page_count_pdfinfo"])
        lines.append(
            f"| {item['slug']} | {item['title']} | "
            f"{item['page_count_pdfinfo']} | {item['page_count_extracted']} |"
        )
    lines.extend(
        [
            "",
            f"- Total PDF pages: {total_pages}",
            f"- Source bundle root: `{OUT_DIR}`",
        ]
    )
    (OUT_DIR / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_processing_checklist(manifest: list[dict[str, object]]) -> None:
    lines = [
        "# Physics PDF Processing Checklist",
        "",
        "Status meanings:",
        "- `extracted`: page text has been extracted and stored.",
        "- `needs-symbol-cleanup`: page likely contains formula/symbol cleanup work because PDF private-use glyphs may remain.",
        "- `drafted-into-book`: content from this PDF has been incorporated into the current `physics.tex` draft at chapter level, but not necessarily line-by-line finalized.",
        "",
    ]

    for item in manifest:
        slug = str(item["slug"])
        title = str(item["title"])
        page_count = int(item["page_count_extracted"])
        bundle_dir = OUT_DIR / slug / "pages"
        lines.append(f"## {title} (`{slug}`)")
        lines.append("")
        lines.append("| Page | Status | Notes |")
        lines.append("| ---: | --- | --- |")
        for page in range(1, page_count + 1):
            page_text = (bundle_dir / f"{page:03d}.txt").read_text(encoding="utf-8", errors="ignore")
            status, note = classify_page(page_text)
            topics = detect_topics(page_text)
            topic_note = f"Topics: {'、'.join(topics)}." if topics else "Topics: general knowledge page."
            lines.append(
                f"| {page:03d} | {status} | {topic_note} {note} |"
            )
        lines.append("")

    (OUT_DIR / "processing_checklist.md").write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    manifest = build_manifest()
    write_reports(manifest)
    write_processing_checklist(manifest)


if __name__ == "__main__":
    main()
