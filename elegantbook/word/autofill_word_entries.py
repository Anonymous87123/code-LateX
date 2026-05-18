from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass, field
from difflib import SequenceMatcher
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
WORD_TEX_PATH = BASE_DIR / "word.tex"
OCR_PATH = BASE_DIR / "ocr.md"
REPORT_PATH = BASE_DIR / "tmp" / "autofill_word_report.json"
BACKUP_PATH = BASE_DIR / "tmp" / "word.before_autofill.tex"

POS_PREFIXES = (
    "n.",
    "v.",
    "vi.",
    "vt.",
    "a.",
    "adj.",
    "adv.",
    "ad.",
    "prep.",
    "conj.",
    "pron.",
    "int.",
    "num.",
    "aux.",
    "phr.",
    "pl.",
    "pp.",
)
POS_PREFIX_RE = re.compile(
    r"^(n\.|v\.|vi\.|vt\.|a\.|adj\.|adv\.|ad\.|prep\.|conj\.|pron\.|int\.|num\.|aux\.|phr\.|pl\.|pp\.)",
    flags=re.I,
)
CIRCLED_DIGITS = (
    "\u2460\u2461\u2462\u2463\u2464\u2465\u2466\u2467\u2468\u2469"
    "\u246A\u246B\u246C\u246D\u246E\u246F\u2470\u2471\u2472\u2473"
)
LATIN_WORD_RE = re.compile(r"[A-Za-z]+(?:'[A-Za-z]+)?")
HEADER_HEAD_RE = re.compile(r"^([A-Za-z][A-Za-z0-9' .,/()\\-]*)")
COMMAND_RE = re.compile(
    r"^\s*\\(wordbreakdown|wordsense|wordfamily|wordcognate|wordphrase|wordexample)\{(.*)\}\s*$"
)
WORD_BEGIN_RE = re.compile(
    r"^\s*\\begin\{word\}(?:\[([^\]]*)\])?\{([^}]*)\}\{([^}]*)\}\s*$"
)
CHAPTER_RE = re.compile(r"^\s*\\chapter\{(.*)\}\s*$")
SECTION_RE = re.compile(r"^\s*\\section\{(.*)\}\s*$")


def collapse_spaces(text: str) -> str:
    return re.sub(r"\s+", " ", text.replace("\u3000", " ")).strip()


def normalize_word_key(text: str) -> str:
    return re.sub(r"[^a-z]", "", text.lower())


def normalize_text_key(text: str) -> str:
    text = tex_to_plain(text)
    text = text.lower()
    text = text.replace("\uFF08", "(").replace("\uFF09", ")")
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"(?<=[\u4e00-\u9fff])\s+(?=[\u4e00-\u9fff])", "", text)
    text = re.sub(r"\s+\(", "(", text)
    return text.strip()


def normalize_sense_key(text: str) -> str:
    text = clean_sense_plain(text).lower()
    return re.sub(r"\s+", "", text)

def tex_to_plain(text: str) -> str:
    replacements = {
        r"\textasciitilde{}": "~",
        r"\textasciicircum{}": "^",
        r"\textbackslash{}": "\\",
        r"\%": "%",
        r"\&": "&",
        r"\#": "#",
        r"\_": "_",
        r"\{": "{",
        r"\}": "}",
        r"\$": "$",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


def escape_tex(text: str) -> str:
    replacements = {
        "\\": r"\textbackslash{}",
        "{": r"\{",
        "}": r"\}",
        "$": r"\$",
        "&": r"\&",
        "#": r"\#",
        "_": r"\_",
        "%": r"\%",
        "^": r"\textasciicircum{}",
        "~": r"\textasciitilde{}",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


def looks_like_sentence(text: str) -> bool:
    plain = collapse_spaces(tex_to_plain(text))
    tokens = LATIN_WORD_RE.findall(plain)
    if len(tokens) >= 5 and re.search(r"[.?!。！？]", plain):
        return True
    if len(tokens) >= 6 and plain.startswith(
        (
            "The ",
            "A ",
            "An ",
            "He ",
            "She ",
            "It ",
            "They ",
            "We ",
            "I ",
            "In ",
            "Our ",
            "His ",
            "Her ",
            "This ",
            "That ",
            "These ",
            "Those ",
            "Once ",
            "During ",
            "Life ",
            "Thanks ",
            "Doctors ",
            "Please ",
            "Don't ",
        )
    ):
        return True
    return False


def split_support_segments(text: str) -> list[str]:
    plain = collapse_spaces(tex_to_plain(text))
    if not plain:
        return []

    buffer = plain
    for marker in CIRCLED_DIGITS:
        buffer = buffer.replace(marker, "|")
    buffer = re.sub(r"\s*@+\s*", "|", buffer)
    major_parts = [part.strip(" |") for part in buffer.split("|") if part.strip(" |")]

    segments: list[str] = []
    for part in major_parts:
        subparts = [part]
        changed = True
        while changed:
            changed = False
            next_round: list[str] = []
            for subpart in subparts:
                pieces = re.split(
                    r"(?<=[\u4e00-\u9fff\uFF09)])\s+(?=[A-Za-z])|(?<=\uFF09)(?=[A-Za-z])|(?<=\))(?=[A-Za-z])|"
                    r"(?<=\uFF1B)(?=[A-Za-z])|(?<=;)(?=[A-Za-z])|"
                    r"\s{2,}(?=[A-Za-z])",
                    subpart,
                )
                pieces = [collapse_spaces(piece) for piece in pieces if collapse_spaces(piece)]
                if len(pieces) > 1:
                    changed = True
                next_round.extend(pieces)
            subparts = next_round
        segments.extend(subparts)
    return segments

def classify_support_segment(segment: str, lemma: str) -> str:
    plain = collapse_spaces(segment)
    if not plain:
        return "ignore"
    if looks_like_sentence(plain):
        return "example"

    english_words = LATIN_WORD_RE.findall(plain)
    if not english_words:
        return "ignore"

    english_head = re.split(r"[\uFF08(\u3010\[]", plain, maxsplit=1)[0].strip()
    english_head_words = LATIN_WORD_RE.findall(english_head)
    english_lower = english_head.lower()

    if len(english_head_words) > 1 and english_lower.startswith(lemma.lower() + " "):
        return "phrase"
    if len(english_head_words) <= 2 and not re.search(r"\b(of|to|for|in|on|with|from|into|over|under|at|by)\b", english_lower):
        return "family"
    if len(english_words) >= 3:
        return "phrase"
    if english_lower.startswith(lemma.lower() + " "):
        return "phrase"
    return "family"

def strip_inline_phonetic(text: str) -> str:
    cleaned = collapse_spaces(text)
    cleaned = re.sub(r"^\[[^\]]+\]\s*", "", cleaned)
    cleaned = re.sub(
        r"^((?:n\.|v\.|vi\.|vt\.|a\.|adj\.|adv\.|ad\.|prep\.|conj\.|pron\.|int\.|num\.|aux\.|phr\.|pl\.|pp\.))\s*\[[^\]]+\]\s*",
        r"\1 ",
        cleaned,
        flags=re.I,
    )
    return collapse_spaces(cleaned)


def is_support_line(text: str) -> bool:
    return any(marker in text for marker in CIRCLED_DIGITS) or "@" in text


def clean_sense_plain(text: str) -> str:
    plain = strip_inline_phonetic(tex_to_plain(text))
    return collapse_spaces(plain)


def sense_gloss_and_pos(text: str) -> tuple[str, str]:
    plain = clean_sense_plain(text)
    pos = ""
    match = POS_PREFIX_RE.match(plain)
    if match:
        pos = match.group(1).lower()
        plain = plain[match.end():].strip()
    plain = re.sub(r"\s+\*.*$", "", plain)
    plain = re.sub(r"^\u3010[^\u3011]+\u3011\s*", "", plain)
    plain = re.sub(r"^\[[^\]]+\]\s*", "", plain)
    plain = plain.split("\uFF1B")[0].split(";")[0].strip()
    plain = plain.strip("\uFF0C,\u3002\uFF1B;\uFF1A:")
    plain = re.sub(r"^\uFF08[^\uFF09]+\uFF09", "", plain).strip()
    return pos, plain

def article_for(word: str) -> str:
    return "an" if word[:1].lower() in {"a", "e", "i", "o", "u"} else "a"


def sense_to_usage(word: str, sense: str) -> str:
    pos, gloss = sense_gloss_and_pos(sense)
    gloss = gloss or tex_to_plain(sense)
    if pos in {"n.", "pl."}:
        return f"{article_for(word)} {word}" + "\uFF08" + f"{gloss}" + "\uFF09"
    if pos in {"v.", "vi.", "vt."}:
        return f"to {word}" + "\uFF08" + f"{gloss}" + "\uFF09"
    if pos in {"a.", "adj."}:
        return f"be {word}" + "\uFF08" + f"{gloss}" + "\uFF09"
    if pos in {"adv.", "ad."}:
        return f"{word}" + "\uFF08" + f"{gloss}" + "\uFF09"
    return f"{word}" + "\uFF08" + f"{gloss}" + "\uFF09"

def token_matches_lemma(token: str, lemma: str) -> bool:
    token = re.sub(r"^[^A-Za-z]+|[^A-Za-z]+$", "", token.lower())
    lemma = lemma.lower()
    if not token or not lemma:
        return False
    if token == lemma:
        return True
    variants = {
        lemma + "s",
        lemma + "es",
        lemma + "ed",
        lemma + "ing",
        lemma[:-1] + "ies" if lemma.endswith("y") else "",
        lemma[:-1] + "ied" if lemma.endswith("y") else "",
        lemma[:-1] + "ing" if lemma.endswith("e") else "",
    }
    return token in variants


def derive_phrase_from_example(lemma: str, example: str) -> str:
    plain = collapse_spaces(tex_to_plain(example))
    english_part = re.split(r"[\uFF08(]", plain, maxsplit=1)[0].strip()
    english_part = english_part.split("\u3002")[0].strip()
    if not english_part:
        return ""
    raw_tokens = english_part.split()
    if not raw_tokens:
        return ""

    for index, token in enumerate(raw_tokens):
        if token_matches_lemma(token, lemma):
            phrase_tokens = [re.sub(r"[,:;.!?]+$", "", raw_tokens[index])]
            for next_token in raw_tokens[index + 1 :]:
                cleaned = re.sub(r"[,:;.!?]+$", "", next_token)
                if not cleaned:
                    break
                if len(phrase_tokens) >= 2 and cleaned.lower() in {
                    "of",
                    "to",
                    "for",
                    "in",
                    "on",
                    "with",
                    "from",
                    "into",
                    "at",
                    "by",
                    "as",
                }:
                    break
                phrase_tokens.append(cleaned)
                if len(phrase_tokens) >= 4:
                    break
            phrase = " ".join(token for token in phrase_tokens if token)
            return collapse_spaces(phrase)

    prefix = raw_tokens[: min(4, len(raw_tokens))]
    return collapse_spaces(" ".join(re.sub(r"[,:;.!?]+$", "", token) for token in prefix))


@dataclass
class WordBlock:
    index: int
    start_line: int
    end_line: int
    chapter: str
    section: str
    subsection: str
    header_line: str
    word: str
    stars: str
    phonetic: str
    breakdown_raw: str = ""
    sense_raws: list[str] = field(default_factory=list)
    family_raws: list[str] = field(default_factory=list)
    phrase_raws: list[str] = field(default_factory=list)
    example_raws: list[str] = field(default_factory=list)


def parse_word_tex(lines: list[str]) -> list[WordBlock]:
    blocks: list[WordBlock] = []
    current_chapter = ""
    current_section = ""
    current_subsection = ""
    line_index = 0
    while line_index < len(lines):
        line = lines[line_index]
        chapter_match = CHAPTER_RE.match(line)
        if chapter_match:
            current_chapter = chapter_match.group(1)
        section_match = SECTION_RE.match(line)
        if section_match:
            current_section = section_match.group(1)
        subsection_match = re.match(r"^\s*\\subsection\{(.*)\}\s*$", line)
        if subsection_match:
            current_subsection = subsection_match.group(1)

        begin_match = WORD_BEGIN_RE.match(line)
        if not begin_match:
            line_index += 1
            continue

        stars = begin_match.group(1) or ""
        word = begin_match.group(2)
        phonetic = begin_match.group(3)
        start_line = line_index
        block_lines = [line]
        line_index += 1
        while line_index < len(lines):
            block_lines.append(lines[line_index])
            if lines[line_index].strip() == r"\end{word}":
                break
            line_index += 1

        block = WordBlock(
            index=len(blocks),
            start_line=start_line,
            end_line=line_index,
            chapter=current_chapter,
            section=current_section,
            subsection=current_subsection,
            header_line=block_lines[0],
            word=word,
            stars=stars,
            phonetic=phonetic,
        )
        for body_line in block_lines[1:-1]:
            command_match = COMMAND_RE.match(body_line)
            if not command_match:
                continue
            command_name, payload = command_match.groups()
            if command_name == "wordbreakdown":
                block.breakdown_raw = payload
            elif command_name == "wordsense":
                block.sense_raws.append(payload)
            elif command_name in {"wordfamily", "wordcognate"}:
                block.family_raws.append(payload)
            elif command_name == "wordphrase":
                block.phrase_raws.append(payload)
            elif command_name == "wordexample":
                block.example_raws.append(payload)
        blocks.append(block)
        line_index += 1
    return blocks


def header_matches_word(line: str, word: str) -> bool:
    stripped = collapse_spaces(line)
    if not stripped or not stripped[:1].isalpha():
        return False
    head_match = HEADER_HEAD_RE.match(stripped)
    if not head_match:
        return False
    head_key = normalize_word_key(head_match.group(1))
    word_key = normalize_word_key(word)
    return bool(head_key) and head_key.startswith(word_key)


def header_match_score(lines: list[str], index: int, word: str) -> float:
    stripped = collapse_spaces(lines[index])
    if not stripped or not stripped[:1].isalpha():
        return 0.0
    head_match = HEADER_HEAD_RE.match(stripped)
    if not head_match:
        return 0.0

    head_key = normalize_word_key(head_match.group(1))
    word_key = normalize_word_key(word)
    if not head_key or not word_key:
        return 0.0
    if head_key == word_key:
        score = 1.0
    elif head_key.startswith(word_key) or word_key.startswith(head_key):
        score = 0.96
    else:
        if head_key[:4] != word_key[:4]:
            return 0.0
        ratio = SequenceMatcher(None, head_key, word_key).ratio()
        if ratio < 0.72:
            return 0.0
        score = ratio

    if "*" in stripped[:48]:
        score += 0.08
    if re.search(r"\[[^\]]+\]", stripped):
        score += 0.03
    stripped_no_phonetic = strip_inline_phonetic(stripped)
    if POS_PREFIX_RE.match(stripped_no_phonetic):
        score += 0.02
    if stripped.startswith("@") or " @" in stripped:
        score -= 0.12
    if len(head_key) > len(word_key) + 5:
        score -= 0.08
    if index + 1 < len(lines):
        next_line = collapse_spaces(lines[index + 1])
        if next_line.startswith("["):
            score += 0.04
        if POS_PREFIX_RE.match(strip_inline_phonetic(next_line)):
            score += 0.02
    return score


def align_ocr_blocks(lines: list[str], words: list[str]) -> list[tuple[int | None, int | None]]:
    starts: list[int | None] = []
    cursor = 0
    for word in words:
        found = None
        for window in (80, 200, 500):
            best_index = None
            best_score = 0.0
            end = min(len(lines), cursor + window)
            for index in range(cursor, end):
                score = header_match_score(lines, index, word)
                if score > best_score:
                    best_score = score
                    best_index = index
                    if score >= 0.99:
                        break
            if best_index is not None:
                found = best_index
                cursor = best_index + 1
                break
        starts.append(found)

    ranges: list[tuple[int | None, int | None]] = []
    next_valid_start = None
    for index in range(len(starts) - 1, -1, -1):
        start = starts[index]
        if start is None:
            ranges.append((None, None))
            continue
        end = next_valid_start if next_valid_start is not None else len(lines)
        ranges.append((start, end))
        next_valid_start = start
    ranges.reverse()
    return ranges


def parse_ocr_senses(block_lines: list[str]) -> list[str]:
    cleaned = [collapse_spaces(line) for line in block_lines if collapse_spaces(line)]
    if not cleaned:
        return []

    body = cleaned[1:]
    senses: list[str] = []
    for line in body:
        if is_support_line(line):
            break
        if line.startswith("[") and line.endswith("]") and not re.search(r"[\u4e00-\u9fff]", line):
            continue
        stripped = strip_inline_phonetic(line)
        if not stripped:
            continue
        if stripped.startswith("[") and stripped.endswith("]"):
            continue
        if POS_PREFIX_RE.match(stripped):
            senses.append(stripped)
            continue
        if senses:
            senses[-1] = collapse_spaces(f"{senses[-1]} {stripped}")
    return senses


def parse_ocr_support(block_lines: list[str], lemma: str) -> tuple[list[str], list[str], list[str]]:
    cleaned = [collapse_spaces(line) for line in block_lines if collapse_spaces(line)]
    if not cleaned:
        return [], [], []

    support_start = None
    for index, line in enumerate(cleaned):
        if is_support_line(line):
            support_start = index
            break
    if support_start is None:
        return [], [], []

    support_lines = [strip_inline_phonetic(line) for line in cleaned[support_start:]]
    support_lines = [line for line in support_lines if line]
    support_text = " ".join(support_lines)
    segments = split_support_segments(support_text)
    families: list[str] = []
    phrases: list[str] = []
    examples: list[str] = []
    seen: set[str] = set()
    for segment in segments:
        if re.fullmatch(r"\[[^\]]+\]", segment):
            continue
        key = normalize_text_key(segment)
        if not key or key in seen:
            continue
        seen.add(key)
        kind = classify_support_segment(segment, lemma)
        if kind == "family":
            families.append(segment)
        elif kind == "phrase":
            phrases.append(segment)
        elif kind == "example":
            examples.append(segment)
    return families, phrases, examples

def add_unique(target: list[str], seen: set[str], text: str) -> bool:
    text = collapse_spaces(text).strip("；;")
    key = normalize_text_key(text)
    if not key or key in seen:
        return False
    seen.add(key)
    target.append(text)
    return True


def group_blocks_by_root(blocks: list[WordBlock]) -> dict[str, list[WordBlock]]:
    groups: dict[str, list[WordBlock]] = {}
    for block in blocks:
        root = normalize_text_key(block.breakdown_raw) or normalize_text_key(block.chapter)
        groups.setdefault(root, []).append(block)
    return groups


def group_blocks_by_chapter(blocks: list[WordBlock]) -> dict[str, list[WordBlock]]:
    groups: dict[str, list[WordBlock]] = {}
    for block in blocks:
        chapter = normalize_text_key(block.chapter)
        groups.setdefault(chapter, []).append(block)
    return groups


def group_blocks_by_subsection(blocks: list[WordBlock]) -> dict[str, list[WordBlock]]:
    groups: dict[str, list[WordBlock]] = {}
    for block in blocks:
        subsection = normalize_text_key(block.subsection)
        if subsection:
            groups.setdefault(subsection, []).append(block)
    return groups


def nearest_same_root_words(
    block: WordBlock,
    root_groups: dict[str, list[WordBlock]],
    subsection_groups: dict[str, list[WordBlock]],
    chapter_groups: dict[str, list[WordBlock]],
) -> list[str]:
    root = normalize_text_key(block.breakdown_raw) or normalize_text_key(block.chapter)
    siblings = root_groups.get(root, [])
    if len(siblings) <= 1:
        subsection = normalize_text_key(block.subsection)
        if subsection:
            siblings = subsection_groups.get(subsection, [])
            if len(siblings) <= 1:
                return []
        else:
            siblings = chapter_groups.get(normalize_text_key(block.chapter), [])
    ranked = sorted(
        (sibling for sibling in siblings if sibling.word != block.word),
        key=lambda sibling: abs(sibling.index - block.index),
    )
    return [sibling.word for sibling in ranked[:4]]

def render_block(
    block: WordBlock,
    base_senses: list[str],
    extra_senses: list[str],
    families: list[str],
    phrases: list[str],
    examples: list[str],
) -> list[str]:
    header = rf"\begin{{word}}{'[' + block.stars + ']' if block.stars else ''}{{{block.word}}}{{{block.phonetic}}}"
    rendered = [header]
    rendered.append(rf"  \wordbreakdown{{{block.breakdown_raw}}}")
    for sense in base_senses:
        rendered.append(rf"  \wordsense{{{sense}}}")
    for sense in extra_senses:
        rendered.append(rf"  \wordsense{{{escape_tex(sense)}}}")
    for family in families:
        rendered.append(rf"  \wordfamily{{{escape_tex(family)}}}")
    for phrase in phrases:
        rendered.append(rf"  \wordphrase{{{escape_tex(phrase)}}}")
    for example in examples:
        rendered.append(rf"  \wordexample{{{escape_tex(example)}}}")
    rendered.append(r"\end{word}")
    return rendered


def collect_existing_support(block: WordBlock) -> tuple[list[str], list[str], list[str]]:
    families: list[str] = []
    phrases: list[str] = []
    examples: list[str] = []

    seen_family: set[str] = set()
    seen_phrase: set[str] = set()
    seen_example: set[str] = set()

    for raw_family in block.family_raws:
        for segment in split_support_segments(raw_family) or [collapse_spaces(tex_to_plain(raw_family))]:
            add_unique(families, seen_family, segment)

    for raw_phrase in block.phrase_raws:
        for segment in split_support_segments(raw_phrase) or [collapse_spaces(tex_to_plain(raw_phrase))]:
            kind = classify_support_segment(segment, block.word)
            if kind == "family":
                add_unique(families, seen_family, segment)
            else:
                add_unique(phrases, seen_phrase, segment)

    for raw_example in block.example_raws:
        segments = split_support_segments(raw_example) or [collapse_spaces(tex_to_plain(raw_example))]
        for segment in segments:
            kind = classify_support_segment(segment, block.word)
            if kind == "family":
                add_unique(families, seen_family, segment)
            elif kind == "phrase":
                add_unique(phrases, seen_phrase, segment)
                add_unique(examples, seen_example, segment)
            elif kind == "example":
                add_unique(examples, seen_example, segment)
            else:
                add_unique(examples, seen_example, segment)

    return families, phrases, examples


def build_output(args: argparse.Namespace) -> dict[str, int]:
    text = WORD_TEX_PATH.read_text(encoding="utf-8")
    lines = text.splitlines()
    blocks = parse_word_tex(lines)
    ocr_lines = OCR_PATH.read_text(encoding="utf-8").splitlines()
    ocr_ranges = align_ocr_blocks(ocr_lines, [block.word for block in blocks])
    root_groups = group_blocks_by_root(blocks)
    subsection_groups = group_blocks_by_subsection(blocks)
    chapter_groups = group_blocks_by_chapter(blocks)

    report = {
        "total": len(blocks),
        "ocr_aligned": 0,
        "missing_ocr_alignment": 0,
        "filled_family": 0,
        "filled_phrase": 0,
        "filled_example": 0,
        "filled_sense": 0,
    }

    transformed_blocks: list[list[str]] = []
    for block, (ocr_start, ocr_end) in zip(blocks, ocr_ranges):
        if ocr_start is not None:
            report["ocr_aligned"] += 1
            ocr_block_lines = ocr_lines[ocr_start:ocr_end]
        else:
            report["missing_ocr_alignment"] += 1
            ocr_block_lines = []

        existing_families, existing_phrases, existing_examples = collect_existing_support(block)
        family_seen = {normalize_text_key(item) for item in existing_families if normalize_text_key(item)}
        phrase_seen = {normalize_text_key(item) for item in existing_phrases if normalize_text_key(item)}
        example_seen = {normalize_text_key(item) for item in existing_examples if normalize_text_key(item)}

        families = existing_families[:]
        phrases = existing_phrases[:]
        examples = existing_examples[:]

        base_senses: list[str] = []
        seen_base_senses: set[str] = set()
        for sense in block.sense_raws:
            sense_key = normalize_sense_key(sense)
            if sense_key and sense_key in seen_base_senses:
                continue
            if sense_key:
                seen_base_senses.add(sense_key)
            base_senses.append(sense)

        extra_senses: list[str] = []
        current_sense_keys = {normalize_sense_key(sense) for sense in base_senses}
        for ocr_sense in parse_ocr_senses(ocr_block_lines):
            key = normalize_sense_key(ocr_sense)
            if key and key not in current_sense_keys:
                current_sense_keys.add(key)
                extra_senses.append(ocr_sense)
                report["filled_sense"] += 1

        ocr_families, ocr_phrases, ocr_examples = parse_ocr_support(ocr_block_lines, block.word)
        for item in ocr_families:
            if add_unique(families, family_seen, item):
                report["filled_family"] += 1
        for item in ocr_phrases:
            if add_unique(phrases, phrase_seen, item):
                report["filled_phrase"] += 1
        for item in ocr_examples:
            if add_unique(examples, example_seen, item):
                report["filled_example"] += 1

        if not families and ocr_start is not None:
            for sibling_word in nearest_same_root_words(block, root_groups, subsection_groups, chapter_groups):
                if add_unique(families, family_seen, sibling_word):
                    report["filled_family"] += 1
        if not families:
            add_unique(families, family_seen, block.word)
        if len(families) > 1:
            self_key = normalize_text_key(block.word)
            families = [family for family in families if normalize_text_key(family) != self_key] or families

        if not phrases:
            for example in examples:
                derived = derive_phrase_from_example(block.word, example)
                if derived and add_unique(phrases, phrase_seen, derived):
                    report["filled_phrase"] += 1
                    break
            if not phrases and base_senses:
                fallback_phrase = sense_to_usage(block.word, tex_to_plain(base_senses[0]))
                if add_unique(phrases, phrase_seen, fallback_phrase):
                    report["filled_phrase"] += 1

        target_sense_count = max(1, len(base_senses) + len(extra_senses))
        for phrase in phrases:
            if len(examples) >= target_sense_count:
                break
            if add_unique(examples, example_seen, phrase):
                report["filled_example"] += 1

        all_senses_plain = [tex_to_plain(sense) for sense in base_senses] + extra_senses
        sense_index = 0
        while len(examples) < target_sense_count and sense_index < len(all_senses_plain):
            fallback_example = sense_to_usage(block.word, all_senses_plain[sense_index])
            if add_unique(examples, example_seen, fallback_example):
                report["filled_example"] += 1
            sense_index += 1

        if len(examples) < target_sense_count and examples:
            while len(examples) < target_sense_count:
                examples.append(examples[-1])
                report["filled_example"] += 1

        transformed_blocks.append(render_block(block, base_senses, extra_senses, families, phrases, examples))

    output_lines: list[str] = []
    block_index = 0
    line_index = 0
    while line_index < len(lines):
        if block_index < len(blocks) and line_index == blocks[block_index].start_line:
            output_lines.extend(transformed_blocks[block_index])
            output_lines.append("")
            line_index = blocks[block_index].end_line + 1
            block_index += 1
            continue
        output_lines.append(lines[line_index])
        line_index += 1

    output_text = "\n".join(output_lines) + "\n"
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    if args.write:
        BACKUP_PATH.parent.mkdir(parents=True, exist_ok=True)
        if not BACKUP_PATH.exists():
            BACKUP_PATH.write_text(text, encoding="utf-8")
        WORD_TEX_PATH.write_text(output_text, encoding="utf-8")

    return report


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    report = build_output(args)
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
