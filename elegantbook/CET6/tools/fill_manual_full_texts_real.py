from pathlib import Path


ROOT = Path(__file__).resolve().parent
SOURCE_DIR = ROOT / "manual_full_texts_real_src"
OUT = ROOT / "manual_full_texts_real.py"


def parse_blocks(text: str) -> dict[str, str]:
    blocks: dict[str, str] = {}
    current_name = None
    current_lines: list[str] = []
    for line in text.splitlines():
        if line.startswith("### FILE: "):
            if current_name is not None:
                blocks[current_name] = "\n".join(current_lines).rstrip() + "\n"
            current_name = line.removeprefix("### FILE: ").strip()
            current_lines = []
        else:
            current_lines.append(line)
    if current_name is not None:
        blocks[current_name] = "\n".join(current_lines).rstrip() + "\n"
    return blocks


def main() -> None:
    texts: dict[str, str] = {}
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    for path in sorted(SOURCE_DIR.glob("*.txt")):
        texts.update(parse_blocks(path.read_text(encoding="utf-8")))

    lines = ["MANUAL_FULL_TEXTS_REAL = {"]
    for name, text in texts.items():
        escaped = text.replace('"""', '\\"""')
        lines.append(f'    "{name}": """{escaped}""",')
    lines.append("}")
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
