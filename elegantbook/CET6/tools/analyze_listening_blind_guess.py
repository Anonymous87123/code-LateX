from __future__ import annotations

import csv
import argparse
import json
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "cet 6" / "_listening_analysis_output"
TEXT_PARSE = OUT / "texts" / "parse"
OCR_PARSE = OUT / "ocr_pages" / "parse"


def safe_stem(path: Path) -> str:
    return re.sub(r"[^\w\u4e00-\u9fff.-]+", "_", path.stem).strip("_")


CHINESE_SET_NUMBERS = {"一": 1, "二": 2, "三": 3}


def parse_key_from_name(name: str) -> str:
    year = month = set_no = None
    m = re.search(r"(20\d{2})[.年](\d{1,2})", name)
    if m:
        year, month = int(m.group(1)), int(m.group(2))
    m = re.search(r"第\s*([123])\s*套", name)
    if m:
        set_no = int(m.group(1))
    if set_no is None:
        for han, num in CHINESE_SET_NUMBERS.items():
            if f"第{han}套" in name or f"{han}套" in name:
                set_no = num
                break
    return f"{year or 0:04d}.{month or 0:02d}.set{set_no or 0}"


def load_ocr():
    from rapidocr_onnxruntime import RapidOCR

    return RapidOCR()


def page_text_by_columns(image: Path, ocr) -> str:
    result, _elapsed = ocr(str(image))
    if not result:
        return ""

    rows = []
    for box, text, score in result:
        xs = [float(point[0]) for point in box]
        ys = [float(point[1]) for point in box]
        rows.append(
            {
                "x": min(xs),
                "x2": max(xs),
                "y": min(ys),
                "text": str(text),
                "score": float(score),
            }
        )
    if not rows:
        return ""

    max_x = max(row["x2"] for row in rows)
    mid = max_x / 2
    answer_y = min(
        (row["y"] for row in rows if "\u7b54\u6848" in row["text"]),
        default=None,
    )
    if answer_y is not None:
        rows = [row for row in rows if row["y"] > answer_y + 10]

    left: list[dict] = []
    right: list[dict] = []
    full: list[dict] = []
    for row in rows:
        # Full-width transcript lines are not explanation text. Keep them last,
        # so answer blocks are mostly parsed column by column.
        if row["x"] < mid * 0.65 and row["x2"] > mid * 1.25:
            full.append(row)
        elif row["x"] < mid:
            left.append(row)
        else:
            right.append(row)

    def join(part: list[dict]) -> str:
        return "\n".join(row["text"] for row in sorted(part, key=lambda r: (r["y"], r["x"])))

    return "\n".join(chunk for chunk in [join(left), join(right), join(full)] if chunk)


Q_HEAD = re.compile(
    r"(?m)(^|\n)\s*(\d{1,2})[.．]\s*(?:What|Why|How|When|Where|Who|Which|Whatis|Whatdo|Whatdoes|Whatdid)",
    re.IGNORECASE,
)

ANSWER_PATTERNS = [
    re.compile(r"(?:因此|故|所以|由此可知|这表明|可知)?\s*\u7b54\u6848\s*(?:为|是)?\s*([ABCD])\s*[)）]?", re.I),
    re.compile(r"([ABCD])\s*[)）]\s*【\u7cbe\u6790】"),
]


def extract_answers_from_text(text: str, key: str, source: str) -> list[dict[str, str]]:
    matches = list(Q_HEAD.finditer(text))
    rows = []
    for i, match in enumerate(matches):
        question = int(match.group(2))
        if not 1 <= question <= 25:
            continue
        start = match.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        block = text[start:end]
        answers: list[str] = []
        for pattern in ANSWER_PATTERNS:
            answers.extend(pattern.findall(block))
        answers = [a.upper() for a in answers if a and a.upper() in "ABCD"]
        if not answers:
            continue
        # In a column-clean block, the explicit conclusion is usually the last
        # answer-like token; the leading "A)【精析】" agrees in clean cases.
        answer = answers[-1]
        confidence = "high" if len(set(answers)) == 1 else "medium"
        rows.append(
            {
                "key": key,
                "question": str(question),
                "section": "A" if question <= 8 else "B" if question <= 15 else "C",
                "answer": answer,
                "confidence": confidence,
                "source": source,
                "answers_seen": "".join(answers),
                "evidence": re.sub(r"\s+", " ", block[:400]).strip(),
            }
        )
    return rows


def rebuild_answer_key(*, cached_only: bool = False) -> list[dict[str, str]]:
    cache = OUT / "rebuilt_answer_pages"
    cache.mkdir(exist_ok=True)
    ocr = None
    answer_rows: list[dict[str, str]] = []

    for text_file in sorted(TEXT_PARSE.glob("*.ocr_p*.txt")):
        stem = re.sub(r"\.ocr_p\d+-\d+_r\d+$", "", text_file.stem)
        key = parse_key_from_name(stem)
        text = text_file.read_text(encoding="utf-8", errors="replace")
        pages = text.split("\n\f\n")
        image_dir = OCR_PARSE / stem
        if not image_dir.exists():
            continue

        for idx, page in enumerate(pages, start=1):
            if idx > 8 and "25." not in page and "(25)" not in page and "[25]" not in page:
                # Listening answer explanations usually finish early; keep a
                # small exception for late Section C pages.
                continue
            if "\u7b54\u6848" not in page and "【\u7cbe\u6790】" not in page:
                continue
            image = image_dir / f"page-{idx:02d}.png"
            if not image.exists():
                continue
            page_cache = cache / f"{stem}.page-{idx:02d}.columns.txt"
            if page_cache.exists():
                column_text = page_cache.read_text(encoding="utf-8", errors="replace")
            elif cached_only:
                continue
            else:
                if ocr is None:
                    ocr = load_ocr()
                column_text = page_text_by_columns(image, ocr)
                page_cache.write_text(column_text, encoding="utf-8")
            answer_rows.extend(extract_answers_from_text(column_text, key, f"{stem}/page-{idx:02d}"))

    # Merge duplicates. Prefer high confidence and the majority answer.
    grouped: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for row in answer_rows:
        grouped[(row["key"], row["question"])].append(row)

    final = []
    for (key, question), rows in sorted(grouped.items(), key=lambda item: (item[0][0], int(item[0][1]))):
        counts = Counter(row["answer"] for row in rows)
        answer, count = counts.most_common(1)[0]
        confidence = "high" if count == len(rows) and any(row["confidence"] == "high" for row in rows) else "medium"
        sample = next(row for row in rows if row["answer"] == answer)
        final.append(
            {
                "key": key,
                "question": question,
                "section": sample["section"],
                "answer": answer,
                "confidence": confidence,
                "votes": json.dumps(counts, ensure_ascii=False),
                "sources": "; ".join(row["source"] for row in rows[:4]),
                "evidence": sample["evidence"],
            }
        )
    return final


def split_options(raw: str) -> dict[str, str]:
    raw = re.sub(r"\s+", " ", raw).strip()
    raw = re.sub(r"\bQuestions \d+ to \d+ are based on.*$", "", raw).strip()
    raw = re.sub(r"\bSection [ABC]\b.*$", "", raw).strip()
    match = re.match(r"\s*\d+\.\s*(.*)", raw)
    text = match.group(1) if match else raw
    labels = list(re.finditer(r"\b([ABCD])\)\s*", text))
    options: dict[str, str] = {}
    for i, label in enumerate(labels):
        letter = label.group(1)
        start = label.end()
        end = labels[i + 1].start() if i + 1 < len(labels) else len(text)
        value = re.sub(r"\s+", " ", text[start:end]).strip(" ;. ")
        value = re.sub(r"\s*20\d{2}年.*$", "", value).strip()
        if value:
            options[letter] = value
    return options


def words(text: str) -> list[str]:
    return re.findall(r"[A-Za-z][A-Za-z'-]{1,}", text.lower())


def has(pattern: str, text: str) -> bool:
    return re.search(pattern, text, re.I) is not None


FEATURES = {
    "absolute": r"\b(all|always|never|only|completely|entirely|none|every|must)\b",
    "negation": r"\b(no|not|never|cannot|can't|without|lack|avoid|prevent|refrain|resist|unable|impossible|inefficient|unwilling|unaware|unhappy|unhealthy)\b",
    "comparison": r"\b(more|less|higher|lower|better|worse|fewer|larger|smaller|increase|decrease|reduce|reduced|double|doubled|twice|than|above|below|decline|growth)\b",
    "advice_plan": r"\b(should|need|needs|plan|plans|intend|intends|advise|advice|suggest|recommend|try to|make sure|bring|take|leave|prepare|always)\b",
    "research": r"\b(research|researchers|experiment|scientist|scientists|survey|data|finding|findings)\b|\bstudies\b|\bstudy found\b|\bstudy showed\b",
    "future": r"\b(future|will|would|plan|plans|intend|intends|hope|going to|next|add|expand|open)\b",
    "example": r"\b(Boston|rats?|mice|hospital|doctor|millionaires?|apps?|bears?|students?|children|parents|workers)\b",
    "cause": r"\b(because|reason|cause|causes|caused|lead|leads|result|results|due to|owing to|stem|stems)\b",
    "moderate": r"\b(may|might|can|could|tend|tends|likely|some|often|usually|mostly|partly|slightly|tiny|small)\b",
    "extreme_bad": r"\b(all|always|never|only|completely|entirely|none|every|must|impossible|cannot|can't)\b",
}


def option_features(option: str) -> set[str]:
    return {name for name, pattern in FEATURES.items() if has(pattern, option)}


def blind_rule_predictions(options: dict[str, str], section: str, question: int) -> dict[str, str]:
    """Return rule -> predicted letter. These rules use only option text."""
    predictions: dict[str, str] = {}
    letters = list("ABCD")

    lens = {letter: len(words(options[letter])) for letter in letters}
    max_len = max(lens.values())
    min_len = min(lens.values())
    max_letters = [k for k, v in lens.items() if v == max_len]
    min_letters = [k for k, v in lens.items() if v == min_len]
    if len(max_letters) == 1:
        predictions["choose_longest"] = max_letters[0]
    if len(min_letters) == 1:
        predictions["choose_shortest"] = min_letters[0]

    for feature, pattern in FEATURES.items():
        labs = [letter for letter in letters if has(pattern, options[letter])]
        if len(labs) == 1:
            predictions[f"choose_unique_{feature}"] = labs[0]
            # Also evaluate elimination-style rules by picking the first
            # remaining letter. Accuracy of elimination is computed separately.

    # Prefer moderate over extreme if exactly one moderate option and exactly
    # one or more extreme options exist.
    moderate = [letter for letter in letters if "moderate" in option_features(options[letter])]
    extreme = [letter for letter in letters if "extreme_bad" in option_features(options[letter])]
    if len(moderate) == 1 and moderate[0] not in extreme:
        predictions["choose_unique_moderate"] = moderate[0]

    # Section-position priors, based only on question number and option surface.
    if section == "A" and question in {4, 8}:
        labs = [letter for letter in letters if has(FEATURES["future"], options[letter]) or has(FEATURES["advice_plan"], options[letter])]
        if len(labs) == 1:
            predictions["A_last_choose_plan_future"] = labs[0]

    if section == "B" and question in {9, 12}:
        labs = [letter for letter in letters if has(FEATURES["research"], options[letter]) or has(r"\b(issue|problem|debate|question|main|topic|purpose)\b", options[letter])]
        if len(labs) == 1:
            predictions["B_first_choose_research_or_issue"] = labs[0]

    if section == "C" and question in {18, 21, 25}:
        labs = [letter for letter in letters if has(r"\b(essential|overall|main|long-term|in general|attitude|characteristic|focus|meaning|purpose)\b", options[letter])]
        if len(labs) == 1:
            predictions["C_late_choose_abstract_summary"] = labs[0]

    # Opposite-pair rules: if a positive and negative option coexist on one
    # dimension, do not blindly choose; score both directions as separate rules.
    pos_pat = r"\b(benefit|beneficial|advantage|improve|support|accept|successful|popular|effective|help|protect|respect|cooperative|healthy|appealing|opportunit(?:y|ies))\b"
    neg_pat = r"\b(harm|harmful|disadvantage|worse|oppose|reject|failure|unpopular|ineffective|hurt|risk|threat|conflict|passive|unhealthy|adversely|problem|crisis)\b"
    pos = [letter for letter in letters if has(pos_pat, options[letter])]
    neg = [letter for letter in letters if has(neg_pat, options[letter])]
    if len(pos) == 1 and len(neg) == 1:
        predictions["opposition_choose_positive"] = pos[0]
        predictions["opposition_choose_negative"] = neg[0]

    more = [letter for letter in letters if has(r"\b(more|higher|increase|larger|grow|growth|double|doubled|above)\b", options[letter])]
    less = [letter for letter in letters if has(r"\b(less|lower|decrease|reduce|reduced|smaller|decline|below|fewer)\b", options[letter])]
    if len(more) == 1 and len(less) == 1:
        predictions["opposition_choose_more"] = more[0]
        predictions["opposition_choose_less"] = less[0]

    return predictions


def evaluate_blind_rules(answer_key: list[dict[str, str]]) -> tuple[list[dict[str, str]], list[dict[str, str]], list[dict[str, str]]]:
    with (OUT / "question_option_records.csv").open(encoding="utf-8-sig", newline="") as f:
        option_rows = list(csv.DictReader(f))
    answers = {(row["key"], row["question"]): row for row in answer_key if row["confidence"] in {"high", "medium"}}

    examples: list[dict[str, str]] = []
    pred_stats: dict[str, Counter] = defaultdict(Counter)
    elim_stats: dict[str, Counter] = defaultdict(Counter)

    for row in option_rows:
        question = row["question"]
        key = (row["key"], question)
        if key not in answers:
            continue
        options = split_options(row["raw_options"])
        if len(options) != 4:
            continue
        answer = answers[key]["answer"]
        section = row["section"]
        qnum = int(question)

        predictions = blind_rule_predictions(options, section, qnum)
        for rule, pred in predictions.items():
            pred_stats[rule]["total"] += 1
            pred_stats[rule]["hit"] += int(pred == answer)
            if len([e for e in examples if e["rule"] == rule]) < 5:
                examples.append(
                    {
                        "rule": rule,
                        "key": row["key"],
                        "question": question,
                        "section": section,
                        "prediction": pred,
                        "answer": answer,
                        "hit": str(pred == answer),
                        "options": " | ".join(f"{letter}: {options[letter]}" for letter in "ABCD"),
                    }
                )

        # Elimination rules: if exactly one option has feature, evaluate
        # whether it is safe to eliminate it.
        for feature, pattern in FEATURES.items():
            labs = [letter for letter in "ABCD" if has(pattern, options[letter])]
            if len(labs) == 1:
                rule = f"eliminate_unique_{feature}"
                elim_stats[rule]["total"] += 1
                elim_stats[rule]["safe"] += int(labs[0] != answer)
        if len(max((len(words(options[letter])), letter) for letter in "ABCD")):
            pass

    rows = []
    for rule, stat in sorted(pred_stats.items()):
        total = stat["total"]
        hit = stat["hit"]
        rows.append(
            {
                "rule": rule,
                "type": "choose",
                "total": str(total),
                "hit": str(hit),
                "accuracy": f"{hit / total:.3f}" if total else "",
                "baseline": "0.250",
            }
        )
    for rule, stat in sorted(elim_stats.items()):
        total = stat["total"]
        safe = stat["safe"]
        rows.append(
            {
                "rule": rule,
                "type": "eliminate",
                "total": str(total),
                "hit": str(safe),
                "accuracy": f"{safe / total:.3f}" if total else "",
                "baseline": "0.750",
            }
        )
    return rows, examples, option_rows


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--cached-only",
        action="store_true",
        help="Use already rebuilt column-text pages only; do not run OCR for missing pages.",
    )
    args = parser.parse_args()

    answer_key = rebuild_answer_key(cached_only=args.cached_only)
    write_csv(OUT / "listening_answer_key_rebuilt.csv", answer_key)
    eval_rows, examples, _option_rows = evaluate_blind_rules(answer_key)
    write_csv(OUT / "blind_guess_rule_eval.csv", eval_rows)
    write_csv(OUT / "blind_guess_rule_examples.csv", examples)

    print(f"answer key rows: {len(answer_key)}")
    print(Counter(row["confidence"] for row in answer_key))
    print(f"rule rows: {len(eval_rows)}")
    for row in sorted(eval_rows, key=lambda r: (r["type"], -int(r["total"]), r["rule"]))[:20]:
        print(row)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
