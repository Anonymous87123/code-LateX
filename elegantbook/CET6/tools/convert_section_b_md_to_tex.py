from __future__ import annotations

import argparse
import re
from pathlib import Path


DEFAULT_SOURCE = Path("cet 6") / "_analysis_output" / "section_b_final_conclusions_report.md"


def escape_latex(text: str) -> str:
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    return "".join(replacements.get(ch, ch) for ch in text)


def soften_breaks(text: str) -> str:
    return (
        text.replace("/", r"/\allowbreak{}")
        .replace(",", r",\allowbreak{}")
        .replace("→", r"→\allowbreak{}")
    )


def strip_markdown(text: str) -> str:
    text = re.sub(r"`([^`]*)`", r"\1", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    return text


def render_links(text: str) -> str:
    link_re = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
    parts: list[str] = []
    pos = 0
    for match in link_re.finditer(text):
        parts.append(soften_breaks(escape_latex(text[pos : match.start()])))
        label = render_inline(match.group(1))
        url = escape_latex(match.group(2))
        parts.append(r"\href{" + url + "}{" + label + "}")
        pos = match.end()
    parts.append(soften_breaks(escape_latex(text[pos:])))
    return "".join(parts)


def render_normal_segment(text: str) -> str:
    bold_re = re.compile(r"\*\*(.+?)\*\*")
    parts: list[str] = []
    pos = 0
    for match in bold_re.finditer(text):
        parts.append(render_links(text[pos : match.start()]))
        parts.append(r"\textbf{" + render_normal_segment(match.group(1)) + "}")
        pos = match.end()
    parts.append(render_links(text[pos:]))
    return "".join(parts)


def render_inline(text: str) -> str:
    code_re = re.compile(r"`([^`]*)`")
    placeholders: dict[str, str] = {}

    def replace_code(match: re.Match[str]) -> str:
        key = f"@@CODE{len(placeholders)}@@"
        placeholders[key] = r"\CodeInline{" + escape_latex(match.group(1)) + "}"
        return key

    protected = code_re.sub(replace_code, text)
    rendered = render_normal_segment(protected)
    for key, value in placeholders.items():
        rendered = rendered.replace(key, value)
    return rendered


def split_table_row(line: str) -> list[str]:
    stripped = line.strip()
    if stripped.startswith("|"):
        stripped = stripped[1:]
    if stripped.endswith("|"):
        stripped = stripped[:-1]
    cells: list[str] = []
    current: list[str] = []
    escaped = False
    for ch in stripped:
        if ch == "\\" and not escaped:
            escaped = True
            current.append(ch)
            continue
        if ch == "|" and not escaped:
            cells.append("".join(current).strip())
            current = []
        else:
            current.append(ch)
        escaped = False
    cells.append("".join(current).strip())
    return cells


def is_table_separator(line: str) -> bool:
    if not line.strip().startswith("|"):
        return False
    cells = split_table_row(line)
    if not cells:
        return False
    return all(re.fullmatch(r":?-{3,}:?", cell.strip()) for cell in cells)


def is_table_start(lines: list[str], index: int) -> bool:
    if index + 1 >= len(lines):
        return False
    return lines[index].strip().startswith("|") and is_table_separator(lines[index + 1])


def table_column_spec(column_count: int) -> str:
    if column_count <= 0:
        return "p{0.95\\linewidth}"
    total_width = 0.92 if column_count <= 4 else 0.86
    width = total_width / column_count
    col = rf">{{\raggedright\arraybackslash}}p{{{width:.3f}\linewidth}}"
    return "@{}" + "".join([col for _ in range(column_count)]) + "@{}"


def render_table(header: list[str], rows: list[list[str]]) -> str:
    column_count = len(header)
    spec = table_column_spec(column_count)

    def normalize(row: list[str]) -> list[str]:
        padded = row[:column_count] + [""] * max(0, column_count - len(row))
        return padded[:column_count]

    rendered_header = [r"\textbf{" + render_inline(cell) + "}" for cell in normalize(header)]
    rendered_rows = [
        [render_inline(cell) if cell else r"\ " for cell in normalize(row)]
        for row in rows
    ]

    output: list[str] = [
        r"\begin{center}",
        r"\small",
        r"\setlength{\tabcolsep}{4pt}",
        r"\begin{longtable}{" + spec + "}",
        r"\toprule",
        " & ".join(rendered_header) + r" \\",
        r"\midrule",
        r"\endfirsthead",
        r"\toprule",
        " & ".join(rendered_header) + r" \\",
        r"\midrule",
        r"\endhead",
    ]
    for row in rendered_rows:
        output.append(" & ".join(row) + r" \\")
    output.extend(
        [
            r"\bottomrule",
            r"\end{longtable}",
            r"\normalsize",
            r"\end{center}",
            "",
        ]
    )
    return "\n".join(output)


def heading_command(level: int) -> str:
    if level <= 2:
        return "section"
    if level == 3:
        return "subsection"
    if level == 4:
        return "subsubsection"
    return "paragraph"


def toc_level_for_command(command: str) -> str | None:
    if command in {"section", "subsection", "subsubsection"}:
        return command
    return None


def extract_png_name(heading_text: str) -> str | None:
    match = re.fullmatch(r"`?([^`]+\.png)`?", heading_text.strip())
    if not match:
        return None
    name = match.group(1).strip()
    if "/" in name or "\\" in name:
        return None
    return name


def latex_path(path: str) -> str:
    # File names in \includegraphics should not escape underscores as text macros.
    return path.replace("\\", "/").replace("#", r"\#").replace("%", r"\%")


def extract_image_line(line: str) -> tuple[str, str] | None:
    match = re.fullmatch(r"!\[(.*?)\]\(([^)]+)\)", line.strip())
    if not match:
        return None
    alt_text = match.group(1).strip()
    target = match.group(2).strip()
    if not target or "://" in target:
        return None
    return alt_text, target


def render_image(alt_text: str, target: str, source_dir: Path) -> str:
    image_path = source_dir / target
    if not image_path.exists():
        fallback = escape_latex(f"[missing image: {target}]")
        return fallback + "\n"

    caption = alt_text or Path(target).name
    escaped_caption = escape_latex(strip_markdown(caption))
    return "\n".join(
        [
            r"\begin{figure}[H]",
            r"\centering",
            rf"\includegraphics[width=0.92\linewidth]{{{latex_path(target)}}}",
            rf"\caption{{{escaped_caption}}}",
            r"\end{figure}",
            "",
        ]
    )


def render_heading(level: int, text: str, source_dir: Path) -> str:
    command = heading_command(level)
    rendered = render_inline(text)
    plain = escape_latex(strip_markdown(text))
    output = [r"\phantomsection", rf"\{command}*{{{rendered}}}"]
    toc_level = toc_level_for_command(command)
    if toc_level:
        output.append(rf"\addcontentsline{{toc}}{{{toc_level}}}{{{plain}}}")

    png_name = extract_png_name(text)
    if png_name and (source_dir / png_name).exists():
        caption = escape_latex(png_name)
        output.extend(
            [
                r"\begin{figure}[H]",
                r"\centering",
                rf"\includegraphics[width=0.92\linewidth]{{{latex_path(png_name)}}}",
                rf"\caption{{{caption}}}",
                r"\end{figure}",
            ]
        )
    output.append("")
    return "\n".join(output)


def is_unordered_list(line: str) -> re.Match[str] | None:
    return re.match(r"^\s*[-*+]\s+(.*)$", line)


def is_ordered_list(line: str) -> re.Match[str] | None:
    return re.match(r"^\s*\d+\.\s+(.*)$", line)


def render_list(lines: list[str], index: int) -> tuple[str, int]:
    first_line = lines[index]
    ordered = is_ordered_list(first_line) is not None
    env = "enumerate" if ordered else "itemize"
    output = [rf"\begin{{{env}}}"]
    while index < len(lines):
        match = is_ordered_list(lines[index]) if ordered else is_unordered_list(lines[index])
        if not match:
            break
        output.append(r"\item " + render_inline(match.group(1).strip()))
        index += 1
    output.append(rf"\end{{{env}}}")
    output.append("")
    return "\n".join(output), index


def is_special_block_start(lines: list[str], index: int) -> bool:
    line = lines[index]
    stripped = line.strip()
    if not stripped:
        return True
    if extract_image_line(stripped):
        return True
    if stripped.startswith("```"):
        return True
    if re.match(r"^#{1,6}\s+", line):
        return True
    if is_table_start(lines, index):
        return True
    if is_unordered_list(line) or is_ordered_list(line):
        return True
    if stripped.startswith(">"):
        return True
    if re.fullmatch(r"[-*_]{3,}", stripped):
        return True
    return False


def render_blockquote(lines: list[str], index: int) -> tuple[str, int]:
    quote_lines: list[str] = []
    while index < len(lines) and lines[index].lstrip().startswith(">"):
        quote_lines.append(lines[index].lstrip()[1:].strip())
        index += 1
    body = "\n\n".join(render_inline(line) for line in quote_lines)
    return "\n".join([r"\begin{quote}", body, r"\end{quote}", ""]), index


def convert_markdown_to_tex(source: Path) -> str:
    text = source.read_text(encoding="utf-8")
    lines = text.splitlines()
    source_dir = source.parent

    title = "CET-6 Section B Report"
    output: list[str] = []
    index = 0
    in_code = False
    code_buffer: list[str] = []

    if lines and lines[0].startswith("# "):
        title = strip_markdown(lines[0][2:].strip())
        index = 1

    while index < len(lines):
        line = lines[index]
        stripped = line.strip()

        if in_code:
            if stripped.startswith("```"):
                output.append(r"\begin{CodeBlock}")
                output.extend(code_buffer)
                output.append(r"\end{CodeBlock}")
                output.append("")
                code_buffer = []
                in_code = False
            else:
                code_buffer.append(line)
            index += 1
            continue

        if not stripped:
            output.append("")
            index += 1
            continue

        if stripped.startswith("```"):
            in_code = True
            code_buffer = []
            index += 1
            continue

        heading = re.match(r"^(#{1,6})\s+(.*)$", line)
        if heading:
            level = len(heading.group(1))
            text = heading.group(2).strip()
            if level == 1:
                output.append(render_heading(2, text, source_dir))
            else:
                output.append(render_heading(level, text, source_dir))
            index += 1
            continue

        image = extract_image_line(stripped)
        if image:
            alt_text, target = image
            output.append(render_image(alt_text, target, source_dir))
            index += 1
            continue

        if is_table_start(lines, index):
            header = split_table_row(lines[index])
            index += 2
            rows: list[list[str]] = []
            while index < len(lines) and lines[index].strip().startswith("|"):
                rows.append(split_table_row(lines[index]))
                index += 1
            output.append(render_table(header, rows))
            continue

        if is_unordered_list(line) or is_ordered_list(line):
            rendered, index = render_list(lines, index)
            output.append(rendered)
            continue

        if stripped.startswith(">"):
            rendered, index = render_blockquote(lines, index)
            output.append(rendered)
            continue

        if re.fullmatch(r"[-*_]{3,}", stripped):
            output.append(r"\medskip\hrule\medskip")
            output.append("")
            index += 1
            continue

        paragraph_lines = [stripped]
        index += 1
        while index < len(lines) and not is_special_block_start(lines, index):
            paragraph_lines.append(lines[index].strip())
            index += 1
        output.append(render_inline(" ".join(paragraph_lines)))
        output.append("")

    body = "\n".join(output).strip() + "\n"
    return build_document(title, body)


def build_document(title: str, body: str) -> str:
    escaped_title = escape_latex(title)
    return rf"""% Auto-generated from section_b_final_conclusions_report.md.
% Re-run tools/convert_section_b_md_to_tex.py after editing the Markdown source.
\documentclass[UTF8,12pt]{{ctexart}}

\usepackage[a4paper,margin=2.2cm]{{geometry}}
\usepackage{{amsmath,amssymb}}
\usepackage{{array}}
\usepackage{{booktabs}}
\usepackage{{caption}}
\usepackage{{enumitem}}
\usepackage{{float}}
\usepackage{{fvextra}}
\usepackage{{graphicx}}
\usepackage{{longtable}}
\usepackage{{newunicodechar}}
\usepackage{{seqsplit}}
\usepackage{{titlesec}}
\usepackage{{xcolor}}
\usepackage{{hyperref}}

\graphicspath{{{{./}}}}
\hypersetup{{
  colorlinks=true,
  linkcolor=blue!55!black,
  urlcolor=blue!55!black,
  citecolor=blue!55!black
}}
\setlength{{\parindent}}{{2em}}
\setlength{{\parskip}}{{0.35em}}
\setlength{{\emergencystretch}}{{3em}}
\sloppy
\setcounter{{tocdepth}}{{2}}
\setlist{{leftmargin=2em,itemsep=0.15em,topsep=0.25em}}
\renewcommand{{\arraystretch}}{{1.22}}
\titleformat{{\paragraph}}[block]{{\normalfont\normalsize\bfseries}}{{}}{{0pt}}{{}}
\titlespacing*{{\paragraph}}{{0pt}}{{1.1ex plus .2ex}}{{0.6ex}}
\DefineVerbatimEnvironment{{CodeBlock}}{{Verbatim}}{{breaklines=true,breakanywhere=true,fontsize=\small}}
\newcommand{{\CodeInline}}[1]{{\texttt{{\seqsplit{{#1}}}}}}
\newunicodechar{{≥}}{{\ensuremath{{\ge}}}}
\newunicodechar{{≤}}{{\ensuremath{{\le}}}}
\newunicodechar{{≈}}{{\ensuremath{{\approx}}}}
\newunicodechar{{∈}}{{\ensuremath{{\in}}}}
\newunicodechar{{∧}}{{\ensuremath{{\land}}}}
\newunicodechar{{ρ}}{{\ensuremath{{\rho}}}}
\newunicodechar{{τ}}{{\ensuremath{{\tau}}}}
\newunicodechar{{σ}}{{\ensuremath{{\sigma}}}}
\newunicodechar{{✓}}{{\ensuremath{{\checkmark}}}}
\newunicodechar{{→}}{{\ensuremath{{\to}}}}

\title{{{escaped_title}}}
\author{{Markdown auto-conversion}}
\date{{\today}}

\begin{{document}}
\maketitle
\tableofcontents
\newpage

{body}
\end{{document}}
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Convert the Section B Markdown report to ctexart LaTeX.")
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    source = args.source
    output = args.output or source.with_suffix(".tex")
    tex = convert_markdown_to_tex(source)
    output.write_text(tex, encoding="utf-8", newline="\n")
    print(f"Wrote {output}")


if __name__ == "__main__":
    main()
