from __future__ import annotations

import json
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
        lines.append(f"## {title} (`{slug}`)")
        lines.append("")
        lines.append("| Page | Status | Notes |")
        lines.append("| ---: | --- | --- |")
        for page in range(1, page_count + 1):
            lines.append(
                f"| {page:03d} | extracted; needs-symbol-cleanup; drafted-into-book | First-pass teaching draft completed; page still needs detailed formula/symbol fidelity review. |"
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
