from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from statistics import median


ROOT = Path(__file__).resolve().parents[1]
PDF_PATH = ROOT / "道法.pdf"
TMP_ROOT = ROOT / "tmp" / "pdfs" / "daofa_ocr"
PAGES_DIR = TMP_ROOT / "pages"
RAW_DIR = TMP_ROOT / "raw"
TXT_DIR = TMP_ROOT / "txt"
OUT_TEX = ROOT / "ocr.tex"

LATEX_SPECIALS = {
    "\\": r"\textbackslash{}",
    "%": r"\%",
    "#": r"\#",
    "&": r"\&",
    "_": r"\_",
    "{": r"\{",
    "}": r"\}",
    "$": r"\$",
    "^": r"\textasciicircum{}",
    "~": r"\textasciitilde{}",
}
CIRCLED_DIGITS = set("①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳")
SYMBOL_CHARS = CIRCLED_DIGITS | set("★☆")
SYMBOL_MACROS = {
    "‧": "·",
    "△": r"\ensuremath{\triangle}",
}

GRADE_RE = re.compile(r"^[七八九][上下]$")
UNIT_RE = re.compile(r"^第[一二三四五六七八九十0-9]+单元")
LESSON_RE = re.compile(r"^第[一二三四五六七八九十0-9]+课")

HANDWRITTEN_NOTES = {
    1: "页面顶部有手写批注，疑似补充核心素养或法治观念相关内容；（此处有手写笔记但无法识别）。",
    15: "页面右侧和正文周围有多处手写批注；（此处有手写笔记但无法识别）。",
    30: "页面顶部有手写批注；（此处有手写笔记但无法识别）。",
    31: "页面右侧有手写批注，可辨识片段：打造清朗的网络空间；其余（此处有手写笔记但无法识别）。",
    45: "页面中部有手写批注；（此处有手写笔记但无法识别）。",
    90: "页面中下部有大段手写整理；（此处有手写笔记但无法识别）。",
}

PAGE_REPLACEMENTS: dict[int, list[tuple[str, str]]] = {
    1: [
        ("七上然务 认同，法说见贵低意识", "七上"),
    ],
    15: [
        ("有的先长高。丽计青后期生理受化", "有的先长高。"),
        ("见①反抗与依赖②闭锁与开放勇敢与祛儒。", "：①反抗与依赖②闭锁与开放③勇敢与怯懦。"),
        ("但也为我们的成长提供子契机", "但也为我们的成长提供了契机"),
        ("6.怎样调节童春期的矛盾心理？", "6.怎样调节青春期的矛盾心理？"),
        ("还可以学匀自我调节", "还可以学习自我调节"),
        ("7.怎样正确认识思维的独立（思维的独立要求我们如何做）？  创特", "7.怎样正确认识思维的独立（思维的独立要求我们如何做）？"),
        ("人云亦去", "人云亦云"),
        ("接纳他父合理", "接纳他人合理"),
    ],
    30: [
        ("效育均衔发展", "教育均衡发展"),
        ("观看新间", "观看新闻"),
        ("个人与种会的关系", "个人与社会的关系"),
        ("发居", "发展"),
        ("老师的教和社会", "老师的教诲和社会"),
    ],
    31: [
        ("1.。 网络的影响", "1. 网络的影响"),
        ("网络是一把双刃有利有弊", "网络是一把双刃剑，有利有弊"),
        ("网络信息良莠不齐", "网络信息良莠不齐"),
        ("要提高媒介养、", "要提高媒介素养，"),
        ("社会主义核必价值观", "社会主义核心价值观"),
        ("如何建立安垒(健康、充满正能量的网络空间？", "如何建立安全、健康、充满正能量的网络空间？"),
        ("有关万联网", "有关互联网"),
        ("完善白我", "完善自我"),
        ("恶怖等不良信息", "恐怖等不良信息"),
        ("自觉避守道德和法律", "自觉遵守道德和法律"),
        ("网络谣言的危害？  绝身国家安全", "网络谣言的危害？"),
        ("Q扰乱人们的思想和行起", "①扰乱人们的思想和行为"),
        ("法律筹", "法律等"),
    ],
    45: [
        ("实行宪法宣普制度的意义", "实行宪法宣誓制度的意义"),
        ("对完法的了解", "对宪法的了解"),
        ("一全国人大常委会", "全国人大常委会"),
        ("谁保证本行政区内宪法的实施——地方各级人方", "谁保证本行政区内宪法的实施——地方各级人大"),
    ],
    60: [
        ("法治与自的关系", "法治与自由的关系"),
        ("非法于涉", "非法干涉"),
        ("法治是自山的保障", "法治是自由的保障"),
    ],
}

DROP_LINE_EXACT_BY_PAGE: dict[int, set[str]] = {
    15: {"空理现务", "瑕璃心"},
    30: {"更质敏"},
    45: {"。 )足(2甲克身比库("},
    90: {"无上", "么做"},
}

DROP_LINE_CONTAINS_BY_PAGE: dict[int, list[str]] = {
    31: ["打造清网务", "深汽/权剂"],
    90: ["?顾通势"],
}


@dataclass
class OcrEntry:
    text: str
    score: float
    x_min: float
    y_min: float
    x_max: float
    y_max: float

    @property
    def x_center(self) -> float:
        return (self.x_min + self.x_max) / 2

    @property
    def y_center(self) -> float:
        return (self.y_min + self.y_max) / 2

    @property
    def height(self) -> float:
        return max(1.0, self.y_max - self.y_min)

    def to_json(self) -> dict:
        return {
            "text": self.text,
            "score": self.score,
            "bbox": [self.x_min, self.y_min, self.x_max, self.y_max],
        }


def run(cmd: list[str]) -> None:
    print("+ " + " ".join(cmd), flush=True)
    subprocess.run(cmd, cwd=ROOT, check=True)


def ensure_tools() -> None:
    missing = [tool for tool in ("pdftoppm",) if shutil.which(tool) is None]
    if missing:
        raise SystemExit(f"Missing required tool(s): {', '.join(missing)}")
    try:
        from rapidocr_onnxruntime import RapidOCR  # noqa: F401
    except Exception as exc:  # pragma: no cover - environment check
        raise SystemExit(f"rapidocr_onnxruntime is not available: {exc}") from exc


def page_number_from_image(path: Path) -> int:
    match = re.search(r"-(\d+)\.png$", path.name)
    if not match:
        raise ValueError(f"Cannot parse page number from {path.name}")
    return int(match.group(1))


def existing_images(page_count: int) -> list[Path]:
    images = sorted(PAGES_DIR.glob("page-*.png"), key=page_number_from_image)
    expected = set(range(1, page_count + 1))
    found = {page_number_from_image(path) for path in images}
    if expected.issubset(found):
        return [path for path in images if page_number_from_image(path) in expected]
    return []


def render_pages(page_count: int, dpi: int, force: bool) -> list[Path]:
    PAGES_DIR.mkdir(parents=True, exist_ok=True)
    if force:
        for image in PAGES_DIR.glob("page-*.png"):
            image.unlink()

    images = existing_images(page_count)
    if not images:
        run(
            [
                "pdftoppm",
                "-f",
                "1",
                "-l",
                str(page_count),
                "-png",
                "-r",
                str(dpi),
                str(PDF_PATH),
                str(PAGES_DIR / "page"),
            ]
        )
        images = existing_images(page_count)

    if len(images) != page_count:
        raise RuntimeError(f"Expected {page_count} rendered pages, got {len(images)}.")
    return images


def normalize_result_item(item) -> OcrEntry | None:
    if not item or len(item) < 3:
        return None
    box, text, score = item[0], str(item[1]).strip(), float(item[2])
    if not text:
        return None
    xs = [float(point[0]) for point in box]
    ys = [float(point[1]) for point in box]
    return OcrEntry(
        text=text,
        score=score,
        x_min=min(xs),
        y_min=min(ys),
        x_max=max(xs),
        y_max=max(ys),
    )


def group_entries(entries: list[OcrEntry]) -> list[dict]:
    if not entries:
        return []

    heights = [entry.height for entry in entries]
    line_tol = max(8.0, median(heights) * 0.55)
    groups: list[list[OcrEntry]] = []

    for entry in sorted(entries, key=lambda item: (item.y_center, item.x_center)):
        for group in groups:
            group_y = median([item.y_center for item in group])
            if abs(entry.y_center - group_y) <= max(line_tol, entry.height * 0.45):
                group.append(entry)
                break
        else:
            groups.append([entry])

    lines = []
    for group in groups:
        ordered = sorted(group, key=lambda item: item.x_min)
        pieces: list[str] = []
        prev: OcrEntry | None = None
        for entry in ordered:
            if prev is not None:
                gap = entry.x_min - prev.x_max
                if gap > max(prev.height, entry.height) * 1.4:
                    pieces.append("  ")
            pieces.append(entry.text)
            prev = entry
        text = "".join(pieces).strip()
        if text:
            lines.append(
                {
                    "text": text,
                    "score": min(item.score for item in ordered),
                    "avg_score": sum(item.score for item in ordered) / len(ordered),
                    "bbox": [
                        min(item.x_min for item in ordered),
                        min(item.y_min for item in ordered),
                        max(item.x_max for item in ordered),
                        max(item.y_max for item in ordered),
                    ],
                }
            )

    return sorted(lines, key=lambda item: (item["bbox"][1], item["bbox"][0]))


def run_ocr(
    images: list[Path],
    text_score: float,
    box_thresh: float,
    force: bool,
) -> dict[int, list[dict]]:
    from rapidocr_onnxruntime import RapidOCR

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    TXT_DIR.mkdir(parents=True, exist_ok=True)
    ocr = RapidOCR()
    pages: dict[int, list[dict]] = {}

    for image in images:
        page_no = page_number_from_image(image)
        raw_path = RAW_DIR / f"page-{page_no:02d}.json"
        txt_path = TXT_DIR / f"page-{page_no:02d}.txt"
        if raw_path.exists() and txt_path.exists() and not force:
            with raw_path.open("r", encoding="utf-8") as fh:
                payload = json.load(fh)
            pages[page_no] = payload.get("lines", [])
            print(f"[skip] OCR page {page_no:02d}", flush=True)
            continue

        print(f"[ocr] page {page_no:02d}: {image.name}", flush=True)
        try:
            result, elapsed = ocr(
                str(image),
                text_score=text_score,
                box_thresh=box_thresh,
            )
        except TypeError:
            result, elapsed = ocr(str(image))

        entries = []
        for item in result or []:
            entry = normalize_result_item(item)
            if entry is not None:
                entries.append(entry)

        lines = group_entries(entries)
        payload = {
            "page": page_no,
            "image": str(image.relative_to(ROOT)),
            "elapsed": elapsed,
            "entries": [entry.to_json() for entry in entries],
            "lines": lines,
        }
        with raw_path.open("w", encoding="utf-8") as fh:
            json.dump(payload, fh, ensure_ascii=False, indent=2)
            fh.write("\n")
        with txt_path.open("w", encoding="utf-8") as fh:
            fh.write(f"PDF第{page_no}页\n")
            for line in lines:
                fh.write(line["text"] + "\n")
        pages[page_no] = lines

    return pages


def latex_escape(text: str) -> str:
    pieces: list[str] = []
    for char in text:
        if char in SYMBOL_MACROS:
            pieces.append(SYMBOL_MACROS[char])
        elif char in SYMBOL_CHARS:
            pieces.append(r"\daofasym{" + char + "}")
        else:
            pieces.append(LATEX_SPECIALS.get(char, char))
    return "".join(pieces)


def is_emphasis_line(text: str) -> bool:
    stripped = text.strip()
    if GRADE_RE.match(stripped) or UNIT_RE.match(stripped) or LESSON_RE.match(stripped):
        return True
    if stripped.startswith("关键词"):
        return True
    if len(stripped) <= 36 and re.search(r"[？?]$", stripped):
        return True
    return False


def tex_line_for_text(text: str) -> list[str]:
    stripped = re.sub(r"\s+", " ", text).strip()
    if not stripped:
        return []
    escaped = latex_escape(stripped)
    if GRADE_RE.match(stripped):
        return [
            rf"\subsection*{{{escaped}}}",
            rf"\addcontentsline{{toc}}{{subsection}}{{{escaped}}}",
        ]
    if UNIT_RE.match(stripped) or LESSON_RE.match(stripped):
        return [
            rf"\subsection*{{{escaped}}}",
            rf"\addcontentsline{{toc}}{{subsection}}{{{escaped}}}",
        ]
    if is_emphasis_line(stripped):
        return [rf"\textbf{{{escaped}}}\par"]
    return [escaped + r"\par"]


def normalize_spaces(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def line_is_footer_or_watermark(line: dict, max_y: float) -> bool:
    text = normalize_spaces(line.get("text", ""))
    bbox = line.get("bbox", [0, 0, 0, 0])
    y_min = float(bbox[1]) if len(bbox) > 1 else 0.0
    near_bottom = bool(max_y) and y_min >= max_y * 0.86

    if "扫描全能王" in text:
        return True
    if near_bottom and re.fullmatch(r"页\s*\d+", text):
        return True
    if near_bottom and re.fullmatch(r"\d+\]?", text):
        return True
    return False


def apply_replacements(page_no: int, text: str) -> str:
    for old, new in PAGE_REPLACEMENTS.get(page_no, []):
        text = text.replace(old, new)
    return text


def should_drop_line(page_no: int, text: str) -> bool:
    stripped = normalize_spaces(text)
    if stripped in DROP_LINE_EXACT_BY_PAGE.get(page_no, set()):
        return True
    return any(token in stripped for token in DROP_LINE_CONTAINS_BY_PAGE.get(page_no, []))


def make_manual_line(text: str) -> dict:
    return {"text": text, "score": 1.0, "avg_score": 1.0, "bbox": [0, 0, 0, 0]}


def prepare_page_lines(page_no: int, lines: list[dict]) -> list[dict]:
    if page_no == 90:
        return [
            make_manual_line("国情模块（经济、政治、文化、社会、生态、国际)"),
            make_manual_line("①经济：富强与创新（改革开放、共享发展成果、创新）经济制度、关心国家"),
            make_manual_line("发展（我国的成就、劳动成就今天，实干创造未来)"),
            make_manual_line("②政治：政治制度、国家机构"),
            make_manual_line("③文化：守望精神家园（中华文化、传统美德、社会主义核心价值观、中国精神)"),
            make_manual_line("④社会：和谐与梦想（国家统一、民族团结、中国特色社会主义新时代、中国梦)"),
            make_manual_line("⑤生态：美丽中国、人口环境资源"),
            make_manual_line("⑥世界：维护国家利益（安全；构建人类命运共同体、中国担当、中国智慧、"),
            make_manual_line("中国方案、机遇与挑战、走向未来的少"),
        ]

    max_y = max((float(line.get("bbox", [0, 0, 0, 0])[3]) for line in lines), default=0.0)
    prepared: list[dict] = []
    for line in lines:
        if line_is_footer_or_watermark(line, max_y):
            continue
        text = apply_replacements(page_no, line.get("text", ""))
        if should_drop_line(page_no, text):
            continue
        prepared.append({**line, "text": text})

    if page_no == 31:
        inserted: list[dict] = []
        for line in prepared:
            inserted.append(line)
            if "建立健全网络监管、预警机制" in line.get("text", ""):
                inserted.append(
                    make_manual_line(
                        "（2）网络运营商（企业）：要依法经营，切实加强对网络平台和网络从业人员的监督和管理。"
                    )
                )
        prepared = inserted

    if page_no == 45 and not any("如何加强宪法监督工作" in line.get("text", "") for line in prepared):
        inserted = []
        for line in prepared:
            if line.get("text", "").startswith("①要完善全国人大"):
                inserted.append(make_manual_line("※3. 如何加强宪法监督工作？（=如何健全宪法实施和监督机制？）"))
            inserted.append(line)
        prepared = inserted

    return prepared


def tex_note_for_page(page_no: int) -> list[str]:
    note = HANDWRITTEN_NOTES.get(page_no)
    if not note:
        return []
    return [
        r"\begin{note}[手写批注]",
        latex_escape(note) + r"\par",
        r"\end{note}",
        "",
    ]


def tex_preamble() -> str:
    return r"""\documentclass[lang=cn,11pt]{elegantbook}

\title{道德与法治}
\subtitle{OCR整理稿}

\author{夏同}
\institute{华南理工大学}
\date{\today}
\version{1.0}
\bioinfo{说明}{由道法.pdf OCR整理}

\extrainfo{OCR初稿，仍需人工校对}

\setcounter{tocdepth}{3}

\logo{logo-blue.png}
\cover{cover.jpg}

\usepackage{array}
\usepackage{mathtools}
\IfFileExists{esint.sty}{
  \usepackage{esint}
}{
  \providecommand{\oiint}{\iint}
}
\ExplSyntaxOn
\tl_gset:Nn \CJKttdefault { ebtt }
\ExplSyntaxOff
\IfFontExistsTF{FangSong}{
  \setCJKmonofont[BoldFont={FangSong},ItalicFont={FangSong},BoldItalicFont={FangSong}]{FangSong}
  \setCJKfamilyfont{ebfs}[BoldFont={FangSong},ItalicFont={FangSong},BoldItalicFont={FangSong}]{FangSong}
  \renewcommand*{\fangsong}{\CJKfamily{ebfs}}
}{}
\IfFontExistsTF{KaiTi}{
  \setCJKfamilyfont{ebkai}[BoldFont={KaiTi},ItalicFont={KaiTi},BoldItalicFont={KaiTi}]{KaiTi}
  \renewcommand*{\kaishu}{\CJKfamily{ebkai}}
}{}
\IfFontExistsTF{Segoe UI Symbol}{
  \newfontfamily\daofasymbolfont{Segoe UI Symbol}
  \newcommand{\daofasym}[1]{{\daofasymbolfont #1}}
}{
  \newcommand{\daofasym}[1]{#1}
}
\newcommand{\ccr}[1]{\makecell{{\color{#1}\rule{1cm}{1cm}}}}
\newenvironment{shortexenum}
  {\par\noindent\setlength{\tabcolsep}{0pt}\renewcommand{\arraystretch}{1.15}%
   \begin{tabular}{@{}>{\raggedright\arraybackslash}p{0.485\linewidth}@{\hspace{0.03\linewidth}}>{\raggedright\arraybackslash}p{0.485\linewidth}@{}}}
  {\end{tabular}\par}
\newcommand{\shortitem}[2]{#1.\enspace #2}

\begin{document}
"""


def generate_tex(pages: dict[int, list[dict]], page_count: int) -> None:
    chunks: list[str] = [tex_preamble()]
    for page_no in range(1, page_count + 1):
        chunks.extend(
            [
                "",
                rf"\section*{{PDF第{page_no}页}}",
                rf"\addcontentsline{{toc}}{{section}}{{PDF第{page_no}页}}",
                "",
            ]
        )
        chunks.extend(tex_note_for_page(page_no))
        lines = pages.get(page_no, [])
        if not lines:
            chunks.append(r"（本页未识别出文字。）\par")
            continue
        for line in lines:
            chunks.extend(tex_line_for_text(line["text"]))
            chunks.append("")
    chunks.extend(["", r"\end{document}", ""])
    OUT_TEX.write_text("\n".join(chunks), encoding="utf-8")
    print(f"[tex] wrote {OUT_TEX}", flush=True)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render 道法.pdf, OCR all pages, and build ocr.tex.")
    parser.add_argument("--pages", type=int, default=90, help="Number of PDF pages to process.")
    parser.add_argument("--dpi", type=int, default=200, help="pdftoppm rendering DPI.")
    parser.add_argument("--text-score", type=float, default=0.45, help="RapidOCR text score threshold.")
    parser.add_argument("--box-thresh", type=float, default=0.45, help="RapidOCR detection box threshold.")
    parser.add_argument("--force-render", action="store_true", help="Re-render page PNG files.")
    parser.add_argument("--force-ocr", action="store_true", help="Re-run OCR even if JSON/TXT exists.")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    if not PDF_PATH.exists():
        raise SystemExit(f"Missing PDF: {PDF_PATH}")
    ensure_tools()
    images = render_pages(args.pages, args.dpi, args.force_render)
    pages = run_ocr(images, args.text_score, args.box_thresh, args.force_ocr)
    generate_tex(pages, args.pages)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
