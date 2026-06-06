from __future__ import annotations

import argparse
import csv
import json
import re
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PDF_DIR = ROOT / "cet 6" / (
    "Some PDF files do not have a text layer, and in such cases, "
    "OCR (Optical Character Recognition) will fail"
)
OUT_DIR = ROOT / "cet 6" / "_listening_analysis_output"
TEXT_DIR = OUT_DIR / "texts"
OCR_PAGE_DIR = OUT_DIR / "ocr_pages"


CHINESE_SET_NUMBERS = {
    "一": 1,
    "二": 2,
    "三": 3,
    "四": 4,
}


@dataclass
class PdfRecord:
    key: str
    kind: str
    set_no: int | None
    year: int | None
    month: int | None
    name: str
    path: str
    pages: int
    text_method: str
    text_chars: int
    ascii_words: int
    listening_markers: int
    original_name: str = ""
    original_method: str = ""
    note: str = ""


def run(args: list[str], *, timeout: int = 120) -> subprocess.CompletedProcess:
    return subprocess.run(
        args,
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=timeout,
        check=False,
    )


def safe_stem(path: Path) -> str:
    return re.sub(r"[^\w\u4e00-\u9fff.-]+", "_", path.stem).strip("_")


def pdf_pages(path: Path) -> int:
    proc = run(["pdfinfo", str(path)], timeout=60)
    match = re.search(r"^Pages:\s+(\d+)", proc.stdout, re.MULTILINE)
    if not match:
        return 0
    return int(match.group(1))


def poppler_text(path: Path, out_path: Path) -> str:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    if not out_path.exists():
        proc = run(["pdftotext", "-layout", "-enc", "UTF-8", str(path), str(out_path)], timeout=180)
        if proc.returncode != 0:
            out_path.write_text("", encoding="utf-8")
    return out_path.read_text(encoding="utf-8", errors="replace")


def text_stats(text: str) -> tuple[int, int]:
    words = re.findall(r"\b[A-Za-z][A-Za-z'-]{2,}\b", text)
    markers = sum(
        marker in text
        for marker in [
            "Listening Comprehension",
            "Conversation One",
            "Conversation Two",
            "Passage One",
            "Passage Two",
            "Recording One",
            "Recording Three",
            "Questions 1 to 4",
        ]
    )
    return len(words), markers


def is_good_parse_text(text: str) -> bool:
    words, markers = text_stats(text)
    return words >= 700 and markers >= 3 and ("Conversation One" in text or "Section A" in text)


def is_good_exam_text(text: str) -> bool:
    words, markers = text_stats(text)
    return words >= 350 and markers >= 2 and "Questions 1 to 4" in text


def load_rapid_ocr():
    try:
        from rapidocr_onnxruntime import RapidOCR
    except ImportError as exc:
        raise SystemExit(
            "rapidocr_onnxruntime is required. Install it with: "
            "python -m pip install rapidocr_onnxruntime"
        ) from exc
    return RapidOCR()


def render_pdf_pages(path: Path, target_dir: Path, first: int, last: int, dpi: int) -> list[Path]:
    target_dir.mkdir(parents=True, exist_ok=True)
    existing = sorted(target_dir.glob("page-*.png"))
    expected = [target_dir / f"page-{i:02d}.png" for i in range(first, last + 1)]
    if all(p.exists() for p in expected):
        return expected

    prefix = target_dir / "page"
    proc = run(
        [
            "pdftoppm",
            "-f",
            str(first),
            "-l",
            str(last),
            "-png",
            "-r",
            str(dpi),
            str(path),
            str(prefix),
        ],
        timeout=240,
    )
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or f"pdftoppm failed for {path.name}")
    rendered = sorted(target_dir.glob("page-*.png"))
    return [p for p in rendered if first <= int(p.stem.split("-")[-1]) <= last]


def ocr_images(images: list[Path], out_text: Path, ocr) -> str:
    if out_text.exists():
        return out_text.read_text(encoding="utf-8", errors="replace")

    pages: list[str] = []
    for image in images:
        result, _elapsed = ocr(str(image))
        lines: list[str] = []
        if result:
            rows = []
            for box, text, _score in result:
                xs = [point[0] for point in box]
                ys = [point[1] for point in box]
                rows.append((min(ys), min(xs), text))
            rows.sort(key=lambda item: (round(item[0] / 8), item[1]))
            lines = [text for _y, _x, text in rows]
        pages.append("\n".join(lines))
    out_text.parent.mkdir(parents=True, exist_ok=True)
    out_text.write_text("\n\f\n".join(pages), encoding="utf-8")
    return out_text.read_text(encoding="utf-8", errors="replace")


def extract_text(path: Path, kind: str, pages: int, ocr, force_ocr: bool, dpi: int) -> tuple[str, str]:
    stem = safe_stem(path)
    text_path = TEXT_DIR / kind / f"{stem}.txt"
    text = "" if force_ocr else poppler_text(path, text_path)

    good = is_good_parse_text(text) if kind == "parse" else is_good_exam_text(text)
    if good:
        return text, "text"

    # Some answer PDFs contain only writing/translation for duplicate tests.
    # If there is usable text but no listening section and the PDF is short, avoid slow OCR.
    if kind == "parse":
        words, markers = text_stats(text)
        if words >= 700 and markers == 0 and pages <= 8 and not force_ocr:
            return text, "text-no-listening"

    page_limit = min(pages, 16 if kind == "parse" else 5)
    first = 1
    last = max(first, page_limit)
    page_dir = OCR_PAGE_DIR / kind / stem
    images = render_pdf_pages(path, page_dir, first, last, dpi)
    ocr_text_path = TEXT_DIR / kind / f"{stem}.ocr_p{first:02d}-{last:02d}_r{dpi}.txt"
    return ocr_images(images, ocr_text_path, ocr), "ocr"


def parse_key(path: Path) -> tuple[str, int | None, int | None, int | None]:
    name = path.stem
    year = None
    month = None
    set_no = None

    match = re.search(r"(20\d{2})[.年](\d{1,2})", name)
    if match:
        year = int(match.group(1))
        month = int(match.group(2))
    match = re.search(r"第\s*([123])\s*套", name)
    if match:
        set_no = int(match.group(1))
    if set_no is None:
        for han, num in CHINESE_SET_NUMBERS.items():
            if f"第{han}套" in name or f"{han}套" in name:
                set_no = num
                break

    key = f"{year or 0:04d}.{month or 0:02d}.set{set_no or 0}"
    return key, year, month, set_no


def is_parse_pdf(path: Path) -> bool:
    return path.suffix.lower() == ".pdf" and ("解析" in path.name or "详解" in path.name)


def is_exam_pdf(path: Path) -> bool:
    if path.suffix.lower() != ".pdf":
        return False
    if "解析" in path.name or "详解" in path.name or "答案" in path.name:
        return False
    return "真题" in path.name or "原题" in path.name


def find_original(parse_path: Path, exams_by_key: dict[str, list[Path]]) -> Path | None:
    key, _year, _month, _set_no = parse_key(parse_path)
    candidates = exams_by_key.get(key, [])
    if candidates:
        return sorted(candidates, key=lambda p: len(p.name))[0]
    return None


def clean_text(text: str) -> str:
    text = text.replace("\u3000", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def listening_block(text: str) -> str:
    start_candidates = [
        text.find("Part II"),
        text.find("Listening Comprehension"),
        text.find("Conversation One"),
        text.find("Section A"),
    ]
    starts = [idx for idx in start_candidates if idx >= 0]
    if not starts:
        return ""
    start = min(starts)
    tail = text[start:]
    end_candidates = []
    for pattern in ["Part III", "Reading Comprehension", "Part IV", "Translation"]:
        idx = tail.find(pattern, 2000)
        if idx >= 0:
            end_candidates.append(idx)
    end = min(end_candidates) if end_candidates else len(tail)
    return clean_text(tail[:end])


def section_for_position(block: str, pos: int) -> str:
    boundaries = [
        ("A", block.rfind("Section A", 0, pos)),
        ("B", block.rfind("Section B", 0, pos)),
        ("C", block.rfind("Section C", 0, pos)),
    ]
    boundaries = [(section, idx) for section, idx in boundaries if idx >= 0]
    if boundaries:
        return max(boundaries, key=lambda item: item[1])[0]

    before = block[:pos]
    if "Recording" in before:
        return "C"
    if "Passage" in before:
        return "B"
    return "A"


def unit_for_position(block: str, pos: int) -> str:
    labels = [
        "Conversation One",
        "Conversation Two",
        "Passage One",
        "Passage Two",
        "Recording One",
        "Recording Two",
        "Recording Three",
    ]
    seen = [(label, block.rfind(label, 0, pos)) for label in labels]
    seen = [(label, idx) for label, idx in seen if idx >= 0]
    return max(seen, key=lambda item: item[1])[0] if seen else ""


def transcript_segments(block: str) -> list[tuple[str, str, str]]:
    unit_pattern = re.compile(
        r"(Conversation One|Conversation Two|Passage One|Passage Two|"
        r"Recording One|Recording Two|Recording Three)"
    )
    matches = list(unit_pattern.finditer(block))
    segments: list[tuple[str, str, str]] = []
    for i, match in enumerate(matches):
        label = match.group(1)
        start = match.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(block)
        chunk = block[start:end]
        for stop in ["答案详解", "绛旀", "1. What"]:
            stop_idx = chunk.find(stop, 200)
            if stop_idx >= 0:
                chunk = chunk[:stop_idx]
                break
        section = "A" if "Conversation" in label else "B" if "Passage" in label else "C"
        segments.append((section, label, chunk))
    if segments:
        return segments

    # Older explanation PDFs often omit Conversation/Passage labels and start
    # each transcript with the English question-range header.
    header_pattern = re.compile(
        r"Questions?\s+(\d{1,2})\s+to\s+(\d{1,2})\s+are based on the "
        r"(conversation|passage|recording)\s+you have just heard[.]?",
        re.IGNORECASE,
    )
    headers = list(header_pattern.finditer(block))
    for i, match in enumerate(headers):
        start_q = int(match.group(1))
        end_q = int(match.group(2))
        media_kind = match.group(3).lower()
        start = match.start()
        end = headers[i + 1].start() if i + 1 < len(headers) else len(block)
        chunk = block[start:end]
        for stop in ["答案详解", "绛旀", "1. What", f"{start_q}. What"]:
            stop_idx = chunk.find(stop, 200)
            if stop_idx >= 0:
                chunk = chunk[:stop_idx]
                break
        section = "A" if start_q <= 8 else "B" if start_q <= 15 else "C"
        label = f"{media_kind.title()} Questions {start_q}-{end_q}"
        segments.append((section, label, chunk))
    return segments


def answer_marker_matches(text: str) -> list[re.Match[str]]:
    marker_pattern = re.compile(r"\[(\d{1,2})\]|[（(]\s*(\d{1,2})\s*[)）]")
    return list(marker_pattern.finditer(text))


def marker_records(key: str, parse_name: str, block: str) -> list[dict[str, str | int]]:
    records: list[dict[str, str | int]] = []
    for section, unit, segment in transcript_segments(block):
        for match in answer_marker_matches(segment):
            number = int(next(group for group in match.groups() if group))
            start = max(0, match.start() - 220)
            end = min(len(segment), match.end() + 420)
            snippet = re.sub(r"\s+", " ", segment[start:end]).strip()
            records.append(
                {
                    "key": key,
                    "parse_file": parse_name,
                    "question": number,
                    "section": section,
                    "unit": unit,
                    "snippet": snippet,
                }
            )
    return records


def question_option_records(key: str, original_name: str, text: str) -> list[dict[str, str | int]]:
    block = listening_block(text)
    if not block:
        return []
    matches = list(re.finditer(r"(?m)^\s*(\d{1,2})\.\s+", block))
    records: list[dict[str, str | int]] = []
    for i, match in enumerate(matches):
        question = int(match.group(1))
        next_start = matches[i + 1].start() if i + 1 < len(matches) else len(block)
        raw = block[match.start() : next_start].strip()
        if question > 25:
            continue
        records.append(
            {
                "key": key,
                "original_file": original_name,
                "question": question,
                "section": "A" if question <= 8 else "B" if question <= 15 else "C",
                "raw_options": re.sub(r"\s+", " ", raw),
            }
        )
    return records


def answer_records_from_explanations(key: str, parse_name: str, block: str) -> list[dict[str, str | int]]:
    # OCR explanations often end with "A项与...相符" or "答案为B".
    question_starts = list(re.finditer(r"(?m)^\s*(\d{1,2})[.．]\s+", block))
    records: list[dict[str, str | int]] = []
    for i, match in enumerate(question_starts):
        question = int(match.group(1))
        if not 1 <= question <= 25:
            continue
        next_start = question_starts[i + 1].start() if i + 1 < len(question_starts) else len(block)
        chunk = block[match.start() : next_start]
        letter = ""
        for pattern in [
            r"答案(?:为|是)?\s*([ABCD])\s*[)）]",
            r"由此可知，?\s*([ABCD])\s*项",
            r"因此[，,]?\s*([ABCD])\s*项",
            r"\b([ABCD])\s*项与",
        ]:
            found = re.findall(pattern, chunk)
            if found:
                letter = found[-1]
                break
        if letter:
            records.append(
                {
                    "key": key,
                    "parse_file": parse_name,
                    "question": question,
                    "section": "A" if question <= 8 else "B" if question <= 15 else "C",
                    "answer": letter,
                    "evidence": re.sub(r"\s+", " ", chunk[:500]).strip(),
                }
            )
    return records


def write_csv(path: Path, records: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not records:
        path.write_text("", encoding="utf-8")
        return
    keys = list(records[0].keys())
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(records)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--force-ocr", action="store_true")
    parser.add_argument("--dpi", type=int, default=180)
    parser.add_argument("--limit", type=int, default=0)
    args = parser.parse_args()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    parse_pdfs = sorted([p for p in PDF_DIR.iterdir() if is_parse_pdf(p)], key=lambda p: p.name)
    if args.limit:
        parse_pdfs = parse_pdfs[: args.limit]
    exams = sorted([p for p in PDF_DIR.iterdir() if is_exam_pdf(p)], key=lambda p: p.name)
    exams_by_key: dict[str, list[Path]] = {}
    for exam in exams:
        key, *_ = parse_key(exam)
        exams_by_key.setdefault(key, []).append(exam)

    ocr = None
    manifest: list[PdfRecord] = []
    markers: list[dict[str, str | int]] = []
    options: list[dict[str, str | int]] = []
    answers: list[dict[str, str | int]] = []
    blocks: dict[str, str] = {}

    for idx, parse_pdf in enumerate(parse_pdfs, start=1):
        key, year, month, set_no = parse_key(parse_pdf)
        original = find_original(parse_pdf, exams_by_key)
        pages = pdf_pages(parse_pdf)
        if ocr is None:
            ocr = load_rapid_ocr()
        print(f"[{idx}/{len(parse_pdfs)}] parse {parse_pdf.name}", flush=True)
        parse_text, method = extract_text(parse_pdf, "parse", pages, ocr, args.force_ocr, args.dpi)
        block = listening_block(parse_text)
        blocks[key] = block
        parse_words, parse_marker_count = text_stats(parse_text)
        markers.extend(marker_records(key, parse_pdf.name, block))
        answers.extend(answer_records_from_explanations(key, parse_pdf.name, block))

        original_name = ""
        original_method = ""
        if original:
            original_name = original.name
            original_pages = pdf_pages(original)
            original_text, original_method = extract_text(original, "exam", original_pages, ocr, False, args.dpi)
            options.extend(question_option_records(key, original.name, original_text))

        note = ""
        if not block:
            note = "no_listening_block_found"
        elif len(answer_marker_matches(block)) < 10:
            note = "few_answer_markers"

        manifest.append(
            PdfRecord(
                key=key,
                kind="parse",
                set_no=set_no,
                year=year,
                month=month,
                name=parse_pdf.name,
                path=str(parse_pdf),
                pages=pages,
                text_method=method,
                text_chars=len(parse_text),
                ascii_words=parse_words,
                listening_markers=parse_marker_count,
                original_name=original_name,
                original_method=original_method,
                note=note,
            )
        )

    manifest_json = [asdict(record) for record in manifest]
    (OUT_DIR / "listening_manifest.json").write_text(
        json.dumps(manifest_json, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    write_csv(OUT_DIR / "listening_manifest.csv", manifest_json)
    write_csv(OUT_DIR / "answer_marker_records.csv", markers)
    write_csv(OUT_DIR / "question_option_records.csv", options)
    write_csv(OUT_DIR / "answer_explanation_records.csv", answers)
    (OUT_DIR / "listening_blocks.json").write_text(
        json.dumps(blocks, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"manifest: {OUT_DIR / 'listening_manifest.csv'}")
    print(f"markers: {len(markers)} options: {len(options)} answers: {len(answers)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
