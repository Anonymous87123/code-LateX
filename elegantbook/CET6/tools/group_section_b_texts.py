import hashlib
import json
import re
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent
TEXT_DIR = ROOT_DIR / "cet 6" / "_analysis_output" / "section_b_texts"
OUT_FILE = ROOT_DIR / "cet 6" / "_analysis_output" / "section_b_groups.json"


def normalize(text: str) -> str:
    text = text.lower()
    text = text.replace("\r\n", "\n")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


groups = {}
for path in sorted(TEXT_DIR.glob("*.txt")):
    text = path.read_text(encoding="utf-8")
    key = hashlib.md5(normalize(text).encode("utf-8")).hexdigest()
    groups.setdefault(key, []).append(path.name)

report = [{"group_id": i + 1, "files": files, "count": len(files)} for i, files in enumerate(groups.values())]
OUT_FILE.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"groups={len(report)} files={sum(x['count'] for x in report)}")
