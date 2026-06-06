import csv
import json
import os
import re
from dataclasses import dataclass, asdict
from pathlib import Path
from statistics import mean

import pdfplumber
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


ROOT_DIR = Path(__file__).resolve().parent.parent
BASE_DIR = ROOT_DIR / "cet 6"
OUT_DIR = BASE_DIR / "_analysis_output"
TEXT_DIR = OUT_DIR / "section_b_texts"


SECTION_B_RE = re.compile(
    r"Reading Comprehension.*?Section B\s+Directions:.*?Answer Sheet 2\.(.*?)(?:Section C|Passage One|Part IV Translation)",
    re.S,
)
QUESTION_RE = re.compile(r"\b(3[6-9]|4[0-5])\.\s*(.+?)(?=(?:\b(?:3[6-9]|4[0-5])\.)|$)", re.S)
PARAGRAPH_RE = re.compile(r"([A-K])\)\s*(.+?)(?=(?:\b[A-K]\))|(?:\b(?:3[6-9]|4[0-5])\.)|$)", re.S)


@dataclass
class QuestionRecord:
    file: str
    question_number: int
    statement: str
    answer_letter: str | None
    answer_paragraph: str | None
    paragraph_position_pct: float | None
    paragraph_index: int | None
    paragraph_count: int | None
    paragraph_text_preview: str | None
    method: str


DUPLICATE_FILE_MAP = {
    "2022.06六级真题第3套【可复制可搜索，打印首选】.pdf": "2022.06六级真题第2套【可复制可搜索，打印首选】.pdf",
    "2022.09英语六级真题第2套【可复制可搜索，打印首选】.pdf": "2022.09英语六级真题第1套【可复制可搜索，打印首选】.pdf",
    "2022.09英语六级真题第3套【可复制可搜索，打印首选】.pdf": "2022.09英语六级真题第1套【可复制可搜索，打印首选】.pdf",
    "2023.03英语六级真题第2套.pdf": "2023.03英语六级真题第1套.pdf",
    "2023.03英语六级真题第3套.pdf": "2023.03英语六级真题第1套.pdf",
}


def normalize_text(text: str) -> str:
    text = text.replace("\x00", " ")
    text = text.replace("\u2014", "-")
    text = text.replace("\u2013", "-")
    text = text.replace("\u2019", "'")
    text = text.replace("\u2018", "'")
    text = text.replace("\u201c", '"')
    text = text.replace("\u201d", '"')
    text = text.replace("，", ",")
    text = text.replace("。", ".")
    text = text.replace("：", ":")
    text = text.replace("；", ";")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{2,}", "\n", text)
    return text.strip()


def extract_pages_text(pdf_path: str) -> list[str]:
    pages = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            pages.append(normalize_text(page.extract_text() or ""))
    return pages


def find_section_b_text(full_text: str) -> str | None:
    m = SECTION_B_RE.search(full_text)
    if not m:
        return None
    return normalize_text(m.group(1))


def parse_paragraphs_and_questions(section_text: str):
    start_match = re.search(r"\bA\)\s+", section_text)
    content = section_text[start_match.start() :] if start_match else section_text
    paragraphs = []
    for letter, body in PARAGRAPH_RE.findall(content):
        body = normalize_text(body)
        if len(body) < 20:
            continue
        paragraphs.append((letter, body))
    questions = []
    for qno, body in QUESTION_RE.findall(content):
        questions.append((int(qno), normalize_text(body)))
    return paragraphs, questions


def text_to_tokens(text: str) -> list[str]:
    tokens = re.findall(r"[A-Za-z][A-Za-z'-]{2,}", text.lower())
    stop = {
        "the",
        "and",
        "for",
        "that",
        "with",
        "they",
        "their",
        "this",
        "from",
        "have",
        "were",
        "been",
        "them",
        "into",
        "because",
        "which",
        "about",
        "there",
        "these",
        "those",
        "would",
        "could",
        "should",
        "while",
        "many",
        "much",
        "more",
        "than",
        "what",
        "when",
        "where",
        "your",
        "some",
        "such",
        "also",
        "very",
        "most",
        "will",
        "just",
        "into",
        "over",
        "under",
        "only",
        "other",
        "each",
    }
    return [t for t in tokens if t not in stop]


def sentence_signature(text: str) -> set[str]:
    return set(text_to_tokens(text))


def best_match(question_text: str, paragraphs: list[tuple[str, str]]):
    def norm(s: str) -> str:
        s = s.lower()
        s = s.replace("—", "-").replace("–", "-")
        s = re.sub(r"[\W_]+", " ", s)
        s = re.sub(r"\s+", " ", s).strip()
        return s

    def mix_scores(query: str, candidates: list[str]) -> list[float]:
        docs = [norm(query)] + [norm(x) for x in candidates]
        word_vec = TfidfVectorizer(ngram_range=(1, 3), stop_words="english").fit_transform(docs)
        char_vec = TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 5)).fit_transform(docs)
        word_scores = cosine_similarity(word_vec[0:1], word_vec[1:]).ravel()
        char_scores = cosine_similarity(char_vec[0:1], char_vec[1:]).ravel()
        return list(0.6 * word_scores + 0.4 * char_scores)

    para_texts = [para_text for _, para_text in paragraphs]
    para_scores = mix_scores(question_text, para_texts)
    sentence_scores = []
    for para_text in para_texts:
        sentences = [s.strip() for s in re.split(r"(?<=[\.\?\!;])\s+|\n+", para_text) if len(s.strip()) > 20]
        if not sentences:
            sentences = [para_text]
        sentence_scores.append(max(mix_scores(question_text, sentences)))

    scores = [0.7 * s + 0.3 * p for s, p in zip(sentence_scores, para_scores)]
    best_idx = max(range(len(paragraphs)), key=lambda i: scores[i])
    letter, para_text = paragraphs[best_idx]
    return best_idx, letter, para_text, float(scores[best_idx])


def locate_answer_key(pages: list[str]) -> dict[int, str]:
    combined = "\n".join(pages)
    answer_map: dict[int, str] = {}

    patterns = [
        re.compile(r"\b(3[6-9]|4[0-5])\s*[-:：]?\s*([A-K])\b"),
        re.compile(r"\b(3[6-9]|4[0-5])\.\s*([A-K])\b"),
    ]
    for pat in patterns:
        for qno, ans in pat.findall(combined):
            answer_map[int(qno)] = ans

    return answer_map


def process_file(filename: str) -> list[QuestionRecord]:
    source_filename = DUPLICATE_FILE_MAP.get(filename, filename)
    text_path = TEXT_DIR / f"{Path(source_filename).stem}.txt"
    pdf_path = BASE_DIR / source_filename
    pages = extract_pages_text(pdf_path)

    if text_path.exists():
        section_b = normalize_text(text_path.read_text(encoding="utf-8"))
    else:
        full_text = "\n".join(pages)
        section_b = find_section_b_text(full_text)
    if not section_b:
        return []

    paragraphs, questions = parse_paragraphs_and_questions(section_b)
    if len(paragraphs) < 8 or len(questions) != 10:
        return []

    answer_key = locate_answer_key(pages)
    records: list[QuestionRecord] = []
    for qno, statement in questions:
        para_idx = None
        para_letter = None
        para_preview = None
        pos_pct = None
        answer_letter = answer_key.get(qno)
        method = "answer_key" if answer_letter else "heuristic"

        if answer_letter:
            for idx, (letter, ptxt) in enumerate(paragraphs):
                if letter == answer_letter:
                    para_idx = idx
                    para_letter = letter
                    para_preview = ptxt[:140]
                    pos_pct = round(((idx + 0.5) / len(paragraphs)) * 100, 2)
                    break
        else:
            match = best_match(statement, paragraphs)
            if match:
                idx, letter, ptxt, _score = match
                para_idx = idx
                para_letter = letter
                para_preview = ptxt[:140]
                pos_pct = round(((idx + 0.5) / len(paragraphs)) * 100, 2)
                answer_letter = letter

        records.append(
            QuestionRecord(
                file=filename,
                question_number=qno,
                statement=statement,
                answer_letter=answer_letter,
                answer_paragraph=para_letter,
                paragraph_position_pct=pos_pct,
                paragraph_index=para_idx + 1 if para_idx is not None else None,
                paragraph_count=len(paragraphs),
                paragraph_text_preview=para_preview,
                method=f"{method}|source:{source_filename}" if source_filename != filename else method,
            )
        )
    return records


def summarize(records: list[QuestionRecord]) -> dict:
    by_question: dict[int, dict[str, int]] = {}
    by_letter: dict[str, dict[int, int]] = {}
    position_stats: dict[int, dict[str, float | int]] = {}

    for rec in records:
        if not rec.answer_letter:
            continue
        by_question.setdefault(rec.question_number, {})
        by_question[rec.question_number][rec.answer_letter] = (
            by_question[rec.question_number].get(rec.answer_letter, 0) + 1
        )

        by_letter.setdefault(rec.answer_letter, {})
        by_letter[rec.answer_letter][rec.question_number] = (
            by_letter[rec.answer_letter].get(rec.question_number, 0) + 1
        )

    for qno in sorted({r.question_number for r in records}):
        positions = [r.paragraph_position_pct for r in records if r.question_number == qno and r.paragraph_position_pct is not None]
        if positions:
            position_stats[qno] = {
                "count": len(positions),
                "mean_pct": round(mean(positions), 2),
                "min_pct": round(min(positions), 2),
                "max_pct": round(max(positions), 2),
            }

    return {
        "record_count": len(records),
        "files_count": len(sorted({r.file for r in records})),
        "by_question": by_question,
        "by_letter": by_letter,
        "position_stats": position_stats,
    }


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    files = sorted([f.name for f in BASE_DIR.iterdir() if f.is_file() and f.name.lower().endswith(".pdf")])
    all_records: list[QuestionRecord] = []
    skipped = []
    processed = []
    for filename in files:
        try:
            recs = process_file(filename)
            if recs:
                all_records.extend(recs)
                processed.append(filename)
            else:
                skipped.append({"file": filename, "reason": "section_b_not_found_or_parse_failed"})
        except Exception as exc:
            skipped.append({"file": filename, "reason": str(exc)})

    csv_path = OUT_DIR / "paragraph_matching_records.csv"
    with open(csv_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=list(asdict(all_records[0]).keys()) if all_records else [])
        if all_records:
            writer.writeheader()
            for rec in all_records:
                writer.writerow(asdict(rec))

    summary = summarize(all_records)
    with open(OUT_DIR / "summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    with open(OUT_DIR / "skipped.json", "w", encoding="utf-8") as f:
        json.dump(skipped, f, ensure_ascii=False, indent=2)

    with open(OUT_DIR / "processed_files.json", "w", encoding="utf-8") as f:
        json.dump(processed, f, ensure_ascii=False, indent=2)

    print(f"processed_files={summary['files_count']} records={summary['record_count']} skipped={len(skipped)}")


if __name__ == "__main__":
    main()
