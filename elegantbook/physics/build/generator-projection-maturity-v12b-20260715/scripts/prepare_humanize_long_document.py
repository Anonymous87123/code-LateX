#!/usr/bin/env python3
"""Prepare auditable Markdown/TeX units for long-document humanization.

This command never edits the source document. It freezes readable bytes,
discovers TeX includes, creates conservative units, masks protected spans, and
initializes a coverage ledger whose entries are never falsely marked DONE.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import shutil
import sys
from collections import Counter, deque
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Sequence


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import scan_humanize_chinese as lexical  # noqa: E402
import build_humanize_voice_profile as voice_profiles  # noqa: E402


TEXT_SUFFIXES = {".tex", ".ltx", ".md", ".markdown"}
EXCLUDED_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".cache",
    ".pytest_cache",
    "__pycache__",
    "build",
    "dist",
    "node_modules",
}
INCLUDE_RE = re.compile(r"\\(?P<kind>input|include|subfile)\s*\{(?P<path>[^{}]+)\}")
TEX_HEADING_RE = re.compile(
    r"(?m)^\s*\\(?P<level>part|chapter|section|subsection|subsubsection|paragraph)"
    r"\*?\s*(?:\[[^\]\n]*\]\s*)?\{(?P<title>[^{}\n]*)\}[^\n]*"
)
MD_HEADING_RE = re.compile(r"(?m)^(?P<marks>#{1,6})[ \t]+(?P<title>[^\n]+?)\s*$")
TEX_ENV_RE = re.compile(r"\\(?P<kind>begin|end)\s*\{(?P<name>[^{}\s]+)\}")
CRITICAL_TEX_RE = re.compile(
    r"\\(?:label|(?:auto|c|C|eq|page)?ref|"
    r"cite(?:alp|alt|author|p|t|year|yearpar)?|"
    r"(?:auto|foot|full|no|paren|smart|super|text)cite|"
    r"url|path|verb|input|include|subfile|includegraphics)\*?"
    r"(?:\s*\[[^\]\n]*\])*\s*\{[^{}\n]*\}"
)
TEX_COMMAND_TOKEN_RE = re.compile(r"\\[A-Za-z@]+\*?|\\[^A-Za-z\s]")
EDITABLE_STYLE_WRAPPERS = {"emph", "textbf", "textit"}
YAML_FRONTMATTER_RE = re.compile(r"\A---\s*\n.*?\n---\s*(?:\n|\Z)", re.DOTALL)
MD_LINK_TARGET_RE = re.compile(r"!?\[[^\]\n]*\]\((?P<target>[^)\n]+)\)")
HAN_RE = re.compile(r"[\u3400-\u9fff]")
IGNORED_CONTAINER_ENVS = {"document"}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def build_integrity_manifest(output: Path) -> dict[str, Any]:
    """Fingerprint every prepare artifact that finalize must treat as a snapshot."""
    paths = [
        output / "snapshot.json",
        output / "file_manifest.csv",
        output / "protected_spans.jsonl",
        output / "units.jsonl",
        output / "coverage_ledger.csv",
        output / "run_metadata.json",
        output / "voice_profile.json",
    ]
    paths.extend(sorted((output / "chunks").glob("*.json"), key=lambda item: item.name.casefold()))
    artifacts: list[dict[str, Any]] = []
    for path in paths:
        if not path.is_file():
            raise FileNotFoundError(path)
        artifacts.append({
            "path": str(path.relative_to(output)).replace("\\", "/"),
            "sha256": sha256(path.read_bytes()),
            "bytes": path.stat().st_size,
        })
    return {
        "schema_version": 1,
        "purpose": "Integrity seal for prepare artifacts; finalize must verify before trusting unit state.",
        "artifacts": artifacts,
    }


def read_fixed_bytes(path: Path, length: int) -> bytes:
    """Read no more than the byte length captured before the read began."""
    with path.open("rb") as handle:
        return handle.read(length)


def decode_snapshot(raw: bytes) -> tuple[str | None, str | None, str | None]:
    def control_problem(text: str) -> str | None:
        disallowed = [
            (index, ord(char))
            for index, char in enumerate(text)
            if (ord(char) < 32 and char not in "\t\n\r") or 0x7F <= ord(char) <= 0x9F
        ]
        if not disallowed:
            return None
        index, codepoint = disallowed[0]
        return f"control_characters:{len(disallowed)}:first={index}:U+{codepoint:04X}"

    if raw.startswith((b"\xff\xfe", b"\xfe\xff")):
        return None, None, "unsupported_utf16_bom"
    try:
        encoding = "utf-8-sig" if raw.startswith(b"\xef\xbb\xbf") else "utf-8"
        text = raw.decode("utf-8-sig")
        problem = control_problem(text)
        return (None, None, problem) if problem else (text, encoding, None)
    except UnicodeDecodeError as utf8_error:
        try:
            text = raw.decode("gb18030")
            problem = control_problem(text)
            if problem:
                return None, None, f"utf8_failed:{utf8_error.start};{problem}"
            return text, "gb18030", f"utf8_failed:{utf8_error.start}"
        except UnicodeDecodeError as local_error:
            return None, None, f"utf8_failed:{utf8_error.start};gb18030_failed:{local_error.start}"


def _strip_tex_comments(text: str) -> str:
    output: list[str] = []
    for line in text.splitlines(keepends=True):
        cut = None
        for index, char in enumerate(line):
            if char != "%":
                continue
            backslashes = 0
            cursor = index - 1
            while cursor >= 0 and line[cursor] == "\\":
                backslashes += 1
                cursor -= 1
            if backslashes % 2 == 0:
                cut = index
                break
        if cut is None:
            output.append(line)
        else:
            ending = "\n" if line.endswith("\n") else ""
            output.append(line[:cut] + ending)
    return "".join(output)


def discover_tex_includes(path: Path, text: str) -> list[tuple[str, Path]]:
    discovered: list[tuple[str, Path]] = []
    for match in INCLUDE_RE.finditer(_strip_tex_comments(text)):
        raw_target = match.group("path").strip()
        if not raw_target or "\\" in raw_target or "#" in raw_target:
            continue
        target = Path(raw_target)
        if not target.suffix:
            target = target.with_suffix(".tex")
        if not target.is_absolute():
            target = path.parent / target
        discovered.append((match.group("kind"), target.resolve()))
    return discovered


def discover_unresolved_tex_includes(text: str) -> list[tuple[str, str]]:
    unresolved: list[tuple[str, str]] = []
    for match in INCLUDE_RE.finditer(_strip_tex_comments(text)):
        raw_target = match.group("path").strip()
        if not raw_target or "\\" in raw_target or "#" in raw_target:
            unresolved.append((match.group("kind"), raw_target))
    return unresolved


def _path_key(path: Path) -> str:
    return str(path.resolve()).casefold()


def _directory_inputs(root: Path) -> Iterable[Path]:
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        relative_parts = path.relative_to(root).parts[:-1]
        if any(part.casefold() in EXCLUDED_DIRS for part in relative_parts):
            continue
        yield path.resolve()


def collect_seed_paths(values: Sequence[Path]) -> list[Path]:
    seeds: set[Path] = set()
    for value in values:
        path = value.resolve()
        if path.is_file():
            seeds.add(path)
        elif path.is_dir():
            seeds.update(_directory_inputs(path))
        else:
            raise FileNotFoundError(value)
    return sorted(seeds, key=lambda item: str(item).casefold())


def _line_starts(text: str) -> list[int]:
    starts = [0]
    starts.extend(match.end() for match in re.finditer(r"\n", text))
    return starts


def _offset_to_line(starts: Sequence[int], offset: int) -> int:
    import bisect

    return bisect.bisect_right(starts, offset)


def _extra_protected_spans(
    text: str,
    suffix: str,
    editable_style_wrappers: frozenset[str] = frozenset(),
) -> list[tuple[int, int, str]]:
    spans: list[tuple[int, int, str]] = []
    if suffix in {".tex", ".ltx"}:
        spans.extend((m.start(), m.end(), "critical-tex-command") for m in CRITICAL_TEX_RE.finditer(text))
        spans.extend((m.start(), m.end(), "locked-heading") for m in TEX_HEADING_RE.finditer(text))
        for match in TEX_COMMAND_TOKEN_RE.finditer(text):
            command = match.group(0)
            name_match = re.fullmatch(r"\\([A-Za-z@]+)\*?", command)
            if name_match and name_match.group(1) in editable_style_wrappers:
                continue
            spans.append((match.start(), match.end(), "tex-command-token"))
    else:
        frontmatter = YAML_FRONTMATTER_RE.match(text)
        if frontmatter:
            spans.append((frontmatter.start(), frontmatter.end(), "yaml-frontmatter"))
        for match in MD_LINK_TARGET_RE.finditer(text):
            spans.append((match.start("target"), match.end("target"), "markdown-link-target"))
        spans.extend((m.start(), m.end(), "locked-heading") for m in MD_HEADING_RE.finditer(text))
    return spans


def protected_spans(
    text: str,
    suffix: str,
    file_id: str,
    editable_style_wrappers: frozenset[str] = frozenset(),
) -> list[dict[str, Any]]:
    document_format = "tex" if suffix.lower() in {".tex", ".ltx"} else "markdown"
    raw = lexical._raw_protected_spans(
        text,
        document_format=document_format,
    )  # Reuse the scanner's tested protection grammar without treating Markdown % as TeX comments.
    merged = lexical._merge_spans(
        [*raw, *_extra_protected_spans(text, suffix, editable_style_wrappers)]
    )
    starts = _line_starts(text)
    output: list[dict[str, Any]] = []
    for index, (start, end, reason) in enumerate(merged, 1):
        content = text[start:end]
        output.append(
            {
                "protected_id": f"{file_id}-P{index:05d}",
                "file_id": file_id,
                "start": start,
                "end": end,
                "start_line": _offset_to_line(starts, start),
                "end_line": _offset_to_line(starts, max(start, end - 1)),
                "reason": reason,
                "sha256": sha256(content.encode("utf-8")),
                "content": content,
            }
        )
    return output


def _mask_text(text: str, start: int, end: int, spans: Sequence[dict[str, Any]]) -> tuple[str, list[str], bool]:
    local: list[tuple[int, int, str, str]] = []
    crossing = False
    for span in spans:
        if span["end"] <= start or span["start"] >= end:
            continue
        if span["start"] < start or span["end"] > end:
            crossing = True
            continue
        placeholder = f"[[PROTECTED:{span['protected_id']}:{span['sha256'][:12]}]]"
        local.append((span["start"] - start, span["end"] - start, placeholder, span["protected_id"]))
    masked = text[start:end]
    for local_start, local_end, placeholder, _ in reversed(local):
        masked = masked[:local_start] + placeholder + masked[local_end:]
    return masked, [item[3] for item in local], crossing


def _visible_author_chars(masked: str, suffix: str) -> int:
    without_placeholders = re.sub(r"\[\[PROTECTED:[^\]]+\]\]", "", masked)
    if suffix in {".tex", ".ltx"}:
        without_placeholders = TEX_COMMAND_TOKEN_RE.sub("", without_placeholders)
        without_placeholders = re.sub(r"[{}\[\]$&_^~]", " ", without_placeholders)
    else:
        without_placeholders = re.sub(r"[#>*_`|~-]", " ", without_placeholders)
    return len(HAN_RE.findall(without_placeholders))


def _environment_problems(text: str, suffix: str) -> list[str]:
    if suffix not in {".tex", ".ltx"}:
        return []
    stack: list[str] = []
    problems: list[str] = []
    for match in TEX_ENV_RE.finditer(_strip_tex_comments(text)):
        name = match.group("name")
        if name in IGNORED_CONTAINER_ENVS:
            continue
        if match.group("kind") == "begin":
            stack.append(name)
        elif not stack:
            problems.append(f"end{{{name}}} without begin")
        elif stack[-1] != name:
            problems.append(f"end{{{name}}} closes begin{{{stack[-1]}}}")
            stack.pop()
        else:
            stack.pop()
    problems.extend(f"begin{{{name}}} without end" for name in reversed(stack))
    return problems[:20]


def _heading_regions(text: str, suffix: str) -> list[dict[str, Any]]:
    pattern = TEX_HEADING_RE if suffix in {".tex", ".ltx"} else MD_HEADING_RE
    matches = list(pattern.finditer(text))
    boundaries = [0, *(match.start() for match in matches), len(text)]
    boundaries = sorted(set(boundaries))
    heading_by_start = {match.start(): match for match in matches}
    hierarchy: list[str] = []
    level_map = {
        "part": 1,
        "chapter": 2,
        "section": 3,
        "subsection": 4,
        "subsubsection": 5,
        "paragraph": 6,
    }
    regions: list[dict[str, Any]] = []
    for start, end in zip(boundaries, boundaries[1:]):
        match = heading_by_start.get(start)
        if match:
            if suffix in {".tex", ".ltx"}:
                level = level_map[match.group("level")]
            else:
                level = len(match.group("marks"))
            title = re.sub(r"\s+", " ", match.group("title")).strip()
            hierarchy = hierarchy[: level - 1]
            hierarchy.extend([""] * max(0, level - len(hierarchy) - 1))
            hierarchy.append(title)
            heading_path = " / ".join(item for item in hierarchy if item)
        else:
            heading_path = "(front-matter)"
        if end > start:
            regions.append({"start": start, "end": end, "heading_path": heading_path})
    return regions


def _safe_split_offsets(text: str, start: int, end: int, spans: Sequence[dict[str, Any]], suffix: str) -> list[int]:
    protected_ranges = [(span["start"], span["end"]) for span in spans]

    def inside_protected(offset: int) -> bool:
        return any(a < offset < b for a, b in protected_ranges)

    segment = text[start:end]
    offsets: list[int] = []
    depth = 0
    cursor = start
    for line in segment.splitlines(keepends=True):
        clean = _strip_tex_comments(line) if suffix in {".tex", ".ltx"} else line
        if suffix in {".tex", ".ltx"}:
            for match in TEX_ENV_RE.finditer(clean):
                name = match.group("name")
                if name in IGNORED_CONTAINER_ENVS:
                    continue
                depth += 1 if match.group("kind") == "begin" else -1
                depth = max(0, depth)
        cursor += len(line)
        if not clean.strip() and depth == 0 and not inside_protected(cursor):
            offsets.append(cursor)
    return sorted(set(offsets))


def _split_region(
    text: str,
    region: dict[str, Any],
    spans: Sequence[dict[str, Any]],
    suffix: str,
    max_author_chars: int,
    max_lines: int,
    min_author_chars: int,
) -> list[tuple[int, int, bool]]:
    start, end = region["start"], region["end"]
    starts = _line_starts(text)
    safe = _safe_split_offsets(text, start, end, spans, suffix)
    chunks: list[tuple[int, int, bool]] = []
    cursor = start
    while cursor < end:
        candidates = [value for value in safe if cursor < value < end]
        chosen = None
        exceeded = False
        for boundary in [*candidates, end]:
            masked, _, _ = _mask_text(text, cursor, boundary, spans)
            author_chars = _visible_author_chars(masked, suffix)
            line_count = _offset_to_line(starts, max(cursor, boundary - 1)) - _offset_to_line(starts, cursor) + 1
            if author_chars > max_author_chars or line_count > max_lines:
                exceeded = True
                break
            if author_chars >= min_author_chars or boundary == end:
                chosen = boundary
        if not exceeded:
            chunks.append((cursor, end, False))
            break
        if chosen is not None and chosen > cursor:
            chunks.append((cursor, chosen, False))
            cursor = chosen
            continue
        next_safe = candidates[0] if candidates else end
        chunks.append((cursor, next_safe, True))
        cursor = next_safe
    return chunks


def build_units(
    file_record: dict[str, Any],
    text: str,
    spans: Sequence[dict[str, Any]],
    *,
    scene: str,
    voice_binding: dict[str, Any],
    max_author_chars: int,
    max_lines: int,
    min_author_chars: int,
) -> list[dict[str, Any]]:
    suffix = Path(file_record["path"]).suffix.lower()
    starts = _line_starts(text)
    units: list[dict[str, Any]] = []
    for region in _heading_regions(text, suffix):
        parts = _split_region(
            text,
            region,
            spans,
            suffix,
            max_author_chars,
            max_lines,
            min_author_chars,
        )
        for part_index, (start, end, over_limit) in enumerate(parts, 1):
            raw = text[start:end]
            masked, protected_ids, crossing = _mask_text(text, start, end, spans)
            author_chars = _visible_author_chars(masked, suffix)
            problems = _environment_problems(raw, suffix)
            start_line = _offset_to_line(starts, start)
            end_line = _offset_to_line(starts, max(start, end - 1))
            seed = f"{file_record['file_id']}:{start}:{end}:{region['heading_path']}"
            unit_id = "U-" + hashlib.sha1(seed.encode("utf-8")).hexdigest()[:12]
            if crossing or problems or over_limit:
                status = "UNRESOLVED"
            elif author_chars == 0:
                status = "SKIPPED_PROTECTED"
            else:
                status = "PENDING"
            notes: list[str] = []
            if crossing:
                notes.append("protected_span_crosses_unit_boundary")
            if problems:
                notes.append("environment:" + " | ".join(problems))
            if over_limit:
                notes.append("no_safe_split_before_budget")
            units.append(
                {
                    "unit_id": unit_id,
                    "file_id": file_record["file_id"],
                    "heading_path": region["heading_path"],
                    "part": part_index,
                    "start": start,
                    "end": end,
                    "start_line": start_line,
                    "end_line": end_line,
                    "line_count": end_line - start_line + 1,
                    "scene": scene,
                    "voice_profile_id": voice_binding["voice_profile_id"],
                    "voice_profile_revision": voice_binding["voice_profile_revision"],
                    "voice_profile_confidence": voice_binding["voice_profile_confidence"],
                    "voice_profile_kind": voice_binding["voice_profile_kind"],
                    "voice_profile_source": voice_binding["profile_source"],
                    "voice_profile_sha256": voice_binding["voice_profile_sha256"],
                    "voice_default_disclosure": voice_binding["voice_default_disclosure"],
                    "mode": "REWRITE",
                    "intensity": "BALANCED",
                    "owner_chunk": unit_id,
                    "author_chars": author_chars,
                    "protected_spans": len(protected_ids),
                    "protected_ids": protected_ids,
                    "status": status,
                    "hash_before": sha256(raw.encode("utf-8")),
                    "hash_after": "",
                    "diff_path": "",
                    "protected_hashes_ok": "NOT_RUN",
                    "style_validation": "NOT_RUN",
                    "notes": "; ".join(notes),
                    "masked_text": masked,
                }
            )
    return units


def _write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _write_jsonl(path: Path, rows: Iterable[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def _write_csv(path: Path, rows: Sequence[dict[str, Any]], fields: Sequence[str]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def _context_tail(masked_text: str, limit: int = 1200) -> str:
    paragraphs = [item.strip() for item in re.split(r"(?:\r?\n\s*){2,}", masked_text) if item.strip()]
    return (paragraphs[-1] if paragraphs else masked_text.strip())[-limit:]


def _context_head(masked_text: str, limit: int = 1200) -> str:
    paragraphs = [item.strip() for item in re.split(r"(?:\r?\n\s*){2,}", masked_text) if item.strip()]
    return (paragraphs[0] if paragraphs else masked_text.strip())[:limit]


def attach_read_only_context(units: Sequence[dict[str, Any]]) -> None:
    by_file: dict[str, list[dict[str, Any]]] = {}
    for unit in units:
        by_file.setdefault(unit["file_id"], []).append(unit)
    for file_units in by_file.values():
        file_units.sort(key=lambda item: int(item["start"]))
        for index, unit in enumerate(file_units):
            previous = file_units[index - 1] if index else None
            following = file_units[index + 1] if index + 1 < len(file_units) else None
            unit["context_before_unit"] = previous["unit_id"] if previous else ""
            unit["context_after_unit"] = following["unit_id"] if following else ""
            unit["read_only_context_before"] = _context_tail(previous["masked_text"]) if previous else ""
            unit["read_only_context_after"] = _context_head(following["masked_text"]) if following else ""


def resolve_voice_binding(
    scene: str,
    voice_profile: Path | None,
    expected_sha256: str | None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Resolve one validated Voice Profile and the fields frozen on every unit.

    This command has no independent scene router. ``AUTO`` therefore uses the
    conservative GENERAL default while remaining ``AUTO`` on the unit itself;
    downstream scene-completion gates continue to report that routing is not
    evaluated.
    """
    if (voice_profile is None) != (expected_sha256 is None):
        raise ValueError("voice_profile_arguments_incomplete")
    requested_scene = scene.upper()
    binding_scene = "GENERAL" if requested_scene == "AUTO" else requested_scene
    if voice_profile is None:
        profile = voice_profiles.build_scene_default_profile(binding_scene)
        profile_source = "SCENE_DEFAULT"
        source_path = ""
    else:
        expected = str(expected_sha256).strip()
        if not re.fullmatch(r"[0-9a-f]{64}", expected):
            raise ValueError("voice_profile_sha256_invalid")
        profile_path = Path(voice_profile).resolve()
        profile = voice_profiles.load_and_validate_profile(profile_path)
        if profile["profile_sha256"] != expected:
            raise ValueError("voice_profile_sha256_mismatch")
        profile_source = "SUPPLIED"
        source_path = str(profile_path)
    defaults = profile.get("defaults", {})
    binding = {
        "profile_source": profile_source,
        "source_path": source_path,
        "binding_scene": binding_scene,
        "requested_scene": requested_scene,
        "scene_binding_status": "UNRESOLVED_AUTO" if requested_scene == "AUTO" else "BOUND",
        "voice_profile_id": profile["profile_id"],
        "voice_profile_revision": profile["revision"],
        "voice_profile_confidence": profile["confidence"],
        "voice_profile_kind": profile["profile_kind"],
        "voice_profile_sha256": profile["profile_sha256"],
        "voice_default_disclosure": bool(defaults.get("disclosure_required", False)),
    }
    return profile, binding


def prepare(
    inputs: Sequence[Path],
    output: Path,
    *,
    scene: str = "AUTO",
    max_author_chars: int = 7000,
    max_lines: int = 600,
    min_author_chars: int = 1200,
    editable_style_wrappers: Sequence[str] = (),
    voice_profile: Path | None = None,
    voice_profile_sha256: str | None = None,
) -> dict[str, Any]:
    profile, voice_binding = resolve_voice_binding(
        scene,
        voice_profile,
        voice_profile_sha256,
    )
    if output.exists() and any(output.iterdir()):
        raise FileExistsError(f"output directory must be empty: {output}")
    output.mkdir(parents=True, exist_ok=True)
    source_dir = output / "source"
    chunk_dir = output / "chunks"
    source_dir.mkdir()
    chunk_dir.mkdir()
    _write_json(output / "voice_profile.json", profile)

    unknown_wrappers = sorted(set(editable_style_wrappers) - EDITABLE_STYLE_WRAPPERS)
    if unknown_wrappers:
        raise ValueError("unsupported editable style wrapper: " + ", ".join(unknown_wrappers))
    editable_wrappers = frozenset(editable_style_wrappers)

    queue: deque[tuple[Path, str, str]] = deque((path, "", "seed") for path in collect_seed_paths(inputs))
    seen: set[str] = set()
    files: list[dict[str, Any]] = []
    texts: dict[str, str] = {}
    all_spans: list[dict[str, Any]] = []

    while queue:
        path, parent_id, relation = queue.popleft()
        key = _path_key(path)
        if key in seen:
            continue
        seen.add(key)
        file_id = f"F{len(files) + 1:05d}"
        record: dict[str, Any] = {
            "file_id": file_id,
            "path": str(path),
            "parent_file_id": parent_id,
            "relation": relation,
            "suffix": path.suffix.lower(),
            "exists": path.is_file(),
            "bytes": 0,
            "readable_bytes": 0,
            "encoding": "",
            "sha256": "",
            "modified_at": "",
            "changed_after_snapshot": False,
            "snapshot_copy": "",
            "status": "UNRESOLVED",
            "reason": "missing_file",
        }
        if not path.is_file():
            files.append(record)
            continue

        stat_before = path.stat()
        frozen_length = stat_before.st_size
        raw = read_fixed_bytes(path, frozen_length)
        text, encoding, decode_note = decode_snapshot(raw)
        stat_after = path.stat()
        changed = stat_after.st_size != frozen_length or stat_after.st_mtime_ns != stat_before.st_mtime_ns
        record.update(
            {
                "bytes": frozen_length,
                "readable_bytes": len(raw),
                "encoding": encoding or "",
                "sha256": sha256(raw),
                "modified_at": datetime.fromtimestamp(stat_before.st_mtime, timezone.utc).isoformat(),
                "changed_after_snapshot": changed,
                "reason": decode_note or "",
            }
        )
        copy_name = f"{file_id}{path.suffix.lower() or '.txt'}"
        copy_path = source_dir / copy_name
        copy_path.write_bytes(raw)
        record["snapshot_copy"] = str(copy_path.relative_to(output))
        if text is None:
            record["status"] = "SKIPPED_GARBLED"
            files.append(record)
            continue
        record["status"] = "CHANGED_AFTER_SNAPSHOT" if changed else "READY"
        texts[file_id] = text
        files.append(record)
        if path.suffix.lower() in {".tex", ".ltx"}:
            for include_kind, raw_target in discover_unresolved_tex_includes(text):
                unresolved_id = f"F{len(files) + 1:05d}"
                files.append(
                    {
                        "file_id": unresolved_id,
                        "path": f"{path}::include::{raw_target}",
                        "parent_file_id": file_id,
                        "relation": include_kind,
                        "suffix": "",
                        "exists": False,
                        "bytes": 0,
                        "readable_bytes": 0,
                        "encoding": "",
                        "sha256": "",
                        "modified_at": "",
                        "changed_after_snapshot": False,
                        "snapshot_copy": "",
                        "status": "UNRESOLVED_INCLUDE",
                        "reason": f"dynamic_include_target:{raw_target}",
                    }
                )
            for include_kind, included in discover_tex_includes(path, text):
                queue.append((included, file_id, include_kind))

    units: list[dict[str, Any]] = []
    for record in files:
        text = texts.get(record["file_id"])
        if text is None:
            continue
        spans = protected_spans(
            text,
            record["suffix"],
            record["file_id"],
            editable_wrappers,
        )
        all_spans.extend(spans)
        file_units = build_units(
            record,
            text,
            spans,
            scene=scene.upper(),
            voice_binding=voice_binding,
            max_author_chars=max_author_chars,
            max_lines=max_lines,
            min_author_chars=min_author_chars,
        )
        if record["changed_after_snapshot"]:
            for unit in file_units:
                unit["status"] = "CHANGED_AFTER_SNAPSHOT"
                unit["notes"] = (unit["notes"] + "; " if unit["notes"] else "") + "source_changed_after_snapshot"
        units.extend(file_units)

    attach_read_only_context(units)

    for unit in units:
        chunk_payload = {
            key: value
            for key, value in unit.items()
            if key not in {"masked_text", "read_only_context_before", "read_only_context_after"}
        }
        chunk_payload["masked_text"] = unit["masked_text"]
        chunk_payload["read_only_context_before"] = unit["read_only_context_before"]
        chunk_payload["read_only_context_after"] = unit["read_only_context_after"]
        _write_json(chunk_dir / f"{unit['unit_id']}.json", chunk_payload)

    snapshot_files = [
        {
            key: record[key]
            for key in (
                "file_id",
                "path",
                "bytes",
                "readable_bytes",
                "encoding",
                "sha256",
                "modified_at",
                "changed_after_snapshot",
                "snapshot_copy",
                "status",
                "reason",
            )
        }
        for record in files
    ]
    snapshot = {"created_at": utc_now(), "inputs": [str(path.resolve()) for path in inputs], "files": snapshot_files}
    snapshot["snapshot_id"] = sha256(
        json.dumps(snapshot_files, ensure_ascii=False, sort_keys=True).encode("utf-8")
    )[:16]
    _write_json(output / "snapshot.json", snapshot)

    manifest_fields = (
        "file_id",
        "path",
        "parent_file_id",
        "relation",
        "suffix",
        "exists",
        "bytes",
        "readable_bytes",
        "encoding",
        "sha256",
        "modified_at",
        "changed_after_snapshot",
        "snapshot_copy",
        "status",
        "reason",
    )
    _write_csv(output / "file_manifest.csv", files, manifest_fields)
    _write_jsonl(output / "protected_spans.jsonl", all_spans)
    public_units = [
        {
            key: value
            for key, value in unit.items()
            if key not in {"masked_text", "read_only_context_before", "read_only_context_after"}
        }
        for unit in units
    ]
    _write_jsonl(output / "units.jsonl", public_units)
    ledger_fields = (
        "unit_id",
        "file_id",
        "heading_path",
        "part",
        "start_line",
        "end_line",
        "line_count",
        "scene",
        "voice_profile_id",
        "voice_profile_revision",
        "voice_profile_confidence",
        "voice_profile_kind",
        "voice_profile_source",
        "voice_profile_sha256",
        "voice_default_disclosure",
        "mode",
        "intensity",
        "owner_chunk",
        "context_before_unit",
        "context_after_unit",
        "author_chars",
        "protected_spans",
        "status",
        "hash_before",
        "hash_after",
        "diff_path",
        "protected_hashes_ok",
        "style_validation",
        "notes",
    )
    _write_csv(output / "coverage_ledger.csv", public_units, ledger_fields)

    file_statuses = Counter(record["status"] for record in files)
    unit_statuses = Counter(unit["status"] for unit in units)
    processable_editable_units = unit_statuses.get("PENDING", 0)
    run_status = "REVIEW" if any(
        status in unit_statuses
        for status in ("UNRESOLVED", "SKIPPED_GARBLED", "CHANGED_AFTER_SNAPSHOT")
    ) or any(
        status in file_statuses
        for status in ("UNRESOLVED", "UNRESOLVED_INCLUDE", "SKIPPED_GARBLED", "CHANGED_AFTER_SNAPSHOT")
    ) or processable_editable_units == 0 else "READY"
    metadata = {
        "tool": "prepare_humanize_long_document.py",
        "created_at": utc_now(),
        "snapshot_id": snapshot["snapshot_id"],
        "status": run_status,
        "scene": scene.upper(),
        "voice_binding": voice_binding,
        "budgets": {
            "max_author_chars": max_author_chars,
            "max_lines": max_lines,
            "min_author_chars": min_author_chars,
        },
        "editable_style_wrappers": sorted(editable_wrappers),
        "files_total": len(files),
        "units_total": len(units),
        "protected_spans_total": len(all_spans),
        "file_statuses": dict(sorted(file_statuses.items())),
        "unit_statuses": dict(sorted(unit_statuses.items())),
        "processable_editable_units": processable_editable_units,
        "no_editable_scope": processable_editable_units == 0,
        "completion_claim_allowed": False,
        "next_action": "Rewrite only PENDING chunk files, then validate and finalize them.",
        "integrity_manifest": "prepare_integrity.json",
    }
    _write_json(output / "run_metadata.json", metadata)
    _write_json(output / "prepare_integrity.json", build_integrity_manifest(output))
    return metadata


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="冻结长 MD/TEX 输入并生成 manifest、保护占位块和初始覆盖账本；不修改源文。"
    )
    parser.add_argument("inputs", nargs="+", type=Path, help="一个或多个主文件或目录")
    parser.add_argument("--output", type=Path, required=True, help="必须为空的新输出目录")
    parser.add_argument(
        "--scene",
        type=str.upper,
        choices=("AUTO", "GENERAL", "COURSE", "MODELING", "RESEARCH"),
        default="AUTO",
    )
    parser.add_argument("--max-author-chars", type=int, default=7000)
    parser.add_argument("--max-lines", type=int, default=600)
    parser.add_argument("--min-author-chars", type=int, default=1200)
    parser.add_argument("--voice-profile", type=Path)
    parser.add_argument("--voice-profile-sha256")
    parser.add_argument(
        "--editable-style-wrapper",
        action="append",
        default=[],
        choices=sorted(EDITABLE_STYLE_WRAPPERS),
        help="显式授权移除的非语义 TeX 样式包装命令；可重复，默认全部保护",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.max_author_chars < 1000 or args.max_lines < 50 or args.min_author_chars < 0:
        parser.error("invalid chunk budget")
    try:
        metadata = prepare(
            args.inputs,
            args.output,
            scene=args.scene,
            max_author_chars=args.max_author_chars,
            max_lines=args.max_lines,
            min_author_chars=args.min_author_chars,
            editable_style_wrappers=args.editable_style_wrapper,
            voice_profile=args.voice_profile,
            voice_profile_sha256=args.voice_profile_sha256,
        )
    except (OSError, UnicodeError, ValueError, json.JSONDecodeError) as error:
        parser.error(str(error))
    print(json.dumps(metadata, ensure_ascii=False, indent=2, sort_keys=True))
    return 2 if metadata["status"] == "REVIEW" else 0


if __name__ == "__main__":
    raise SystemExit(main())
