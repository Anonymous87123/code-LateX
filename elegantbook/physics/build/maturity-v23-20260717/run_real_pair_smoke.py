import csv
import hashlib
import json
import sys
from pathlib import Path


SKILL = Path(r"C:\Users\Lenovo\.codex\skills\humanize-academic-chinese")
SCRIPTS = SKILL / "scripts"
sys.path.insert(0, str(SCRIPTS))

import finalize_humanize_long_document as finalizer
import prepare_humanize_long_document as preparer


ROOT = Path(__file__).resolve().parent
SOURCE_RUN = ROOT / "stress-physics-adjacent-small"
SOURCE_TRANSACTION = "STX-59191b72b031f31b3162bb2c"
SOURCE = ROOT / "real-physics-pair-source.tex"
RUN = ROOT / "real-physics-pair-run"
REWRITES = ROOT / "real-physics-pair-rewrites"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


inventory = load_json(SOURCE_RUN / "structural_transaction_inventory.json")
candidate = next(
    item for item in inventory["transactions"]
    if item["transaction_id"] == SOURCE_TRANSACTION
)
source_units = {item["unit_id"]: item for item in load_jsonl(SOURCE_RUN / "units.jsonl")}
left_id, right_id = [item["unit_id"] for item in candidate["compound_refs"]]
left_source = source_units[left_id]
right_source = source_units[right_id]

with (SOURCE_RUN / "file_manifest.csv").open("r", encoding="utf-8-sig", newline="") as handle:
    records = list(csv.DictReader(handle))
record = next(item for item in records if item["file_id"] == left_source["file_id"])
raw = (SOURCE_RUN / record["snapshot_copy"]).read_bytes()
text = raw.decode("utf-8-sig") if record["encoding"] in {"utf-8", "utf-8-sig"} else raw.decode("gb18030")
SOURCE.write_text(
    text[int(left_source["start"]):int(right_source["end"])],
    encoding="utf-8",
    newline="\n",
)

preparer.prepare(
    [SOURCE],
    RUN,
    scene="COURSE",
    intensity="STRUCTURAL",
    structural_transaction_scope="ADJACENT_PAIR",
    max_author_chars=1200,
    min_author_chars=0,
)

run_inventory = load_json(RUN / "structural_transaction_inventory.json")
if run_inventory["status"] != "READY":
    raise RuntimeError("real pair slice did not reproduce an adjacent transaction")
run_candidate = run_inventory["transactions"][0]
unit_ids = [item["unit_id"] for item in run_candidate["compound_refs"]]
chunks = [load_json(RUN / "chunks" / f"{unit_id}.json") for unit_id in unit_ids]
paragraphs = [chunk["structural_paragraphs"] for chunk in chunks]
blocks = [preparer.structural_paragraph_blocks(chunk["masked_text"]) for chunk in chunks]

if paragraphs[1][-1]["movable"] and len(paragraphs[1]) > 1:
    target_specs = [
        [(0, index) for index in range(len(paragraphs[0]))] + [(1, len(paragraphs[1]) - 1)],
        [(1, index) for index in range(len(paragraphs[1]) - 1)],
    ]
elif paragraphs[0][-1]["movable"] and len(paragraphs[0]) > 1:
    target_specs = [
        [(0, index) for index in range(len(paragraphs[0]) - 1)],
        [(1, index) for index in range(len(paragraphs[1]))] + [(0, len(paragraphs[0]) - 1)],
    ]
else:
    raise RuntimeError("real pair has no movable terminal paragraph")

fragments = []
for target_chunk, refs in zip(chunks, target_specs):
    target_blocks = [blocks[side][index] for side, index in refs]
    masked_text = "\n\n".join(target_blocks) + "\n"
    fragments.append({
        "target_unit_id": target_chunk["unit_id"],
        "masked_text": masked_text,
        "keep_reasons": {},
        "target_groups": [
            {
                "source_refs": [{
                    "unit_id": chunks[side]["unit_id"],
                    "paragraph_id": paragraphs[side][index]["paragraph_id"],
                }],
                "target_paragraph_sha256": hashlib.sha256(block.encode("utf-8")).hexdigest(),
                "responsibility": paragraphs[side][index]["responsibility"],
                "reason": "保持原段说明职责，仅调整相邻分块边界位置",
            }
            for (side, index), block in zip(refs, target_blocks)
        ],
    })

bundle = {
    "schema_version": "humanize-structural-transaction-bundle/v1",
    "transaction_id": run_candidate["transaction_id"],
    "transaction_binding_sha256": run_candidate["transaction_binding_sha256"],
    "transaction_inventory_sha256": run_inventory["inventory_sha256"],
    "unit_bindings": [
        {
            "unit_id": chunk["unit_id"],
            "chunk_binding_sha256": chunk["chunk_binding_sha256"],
            "voice_profile_sha256": chunk["voice_profile_sha256"],
        }
        for chunk in chunks
    ],
    "fragments": fragments,
}
REWRITES.mkdir()
(REWRITES / f"{bundle['transaction_id']}.json").write_text(
    json.dumps(bundle, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
    encoding="utf-8",
)

result = finalizer.finalize(RUN, REWRITES)
transaction = result["structural_transaction_results"][bundle["transaction_id"]]
print(json.dumps({
    "status": result["status"],
    "exit_code": result["exit_code"],
    "candidate_assembly_status": result["candidate_assembly_status"],
    "publish_state": result["publish_state"],
    "structural_semantic_mapping": result["structural_semantic_mapping"],
    "transaction_atomic_gate_status": transaction["atomic_gate_status"],
    "cross_unit_moves_applied": transaction["cross_unit_moves_applied"],
    "rendered_review_exists": (RUN / "rendered_review").is_dir(),
    "rendered_exists": (RUN / "rendered").exists(),
    "source_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
}, ensure_ascii=False, indent=2, sort_keys=True))
