import csv
import hashlib
import importlib.util
import io
import json
import os
import sys
import tempfile
import time
import unittest
import concurrent.futures
from pathlib import Path
from unittest import mock


SKILL = Path(
    os.environ.get(
        "HUMANIZE_SKILL_DIR",
        Path.home() / ".codex" / "skills" / "humanize-academic-chinese",
    )
)


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


preparer = load_module(
    "prepare_humanize_long_document",
    SKILL / "scripts" / "prepare_humanize_long_document.py",
)
finalizer = load_module(
    "finalize_humanize_long_document",
    SKILL / "scripts" / "finalize_humanize_long_document.py",
)


def _directory_bytes(root: Path) -> dict[str, bytes]:
    if not root.is_dir():
        return {}
    return {
        str(path.relative_to(root)).replace("\\", "/"): path.read_bytes()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


class LongDocumentFinalizationTests(unittest.TestCase):
    COMPILE_CHECK_FIELDS = {
        "status",
        "command",
        "exit_code",
        "stdout",
        "stderr",
        "cwd",
        "integrity_status",
        "integrity_changes",
        "process_containment",
        "descendant_cleanup",
    }

    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def prepare(
        self, text: str, *, intensity: str = "BALANCED"
    ) -> tuple[Path, Path, dict]:
        source = self.root / "main.tex"
        source.write_text(text, encoding="utf-8")
        run_dir = self.root / "run"
        preparer.prepare(
            [source],
            run_dir,
            scene="COURSE",
            intensity=intensity,
            min_author_chars=0,
        )
        chunks = [json.loads(path.read_text(encoding="utf-8")) for path in (run_dir / "chunks").glob("*.json")]
        pending = next(item for item in chunks if item["status"] == "PENDING")
        return source, run_dir, pending

    def rewrite_dir(self) -> Path:
        path = self.root / "rewrites"
        path.mkdir(exist_ok=True)
        return path

    def voice_bound_bundle(self, unit: dict, payload: dict) -> dict:
        return {
            "unit_id": unit["unit_id"],
            "chunk_binding_sha256": unit["chunk_binding_sha256"],
            "voice_profile_sha256": unit["voice_profile_sha256"],
            **payload,
        }

    def assert_paired_quality_review_candidate(
        self,
        result: dict,
        *,
        units: int | None = None,
    ) -> None:
        self.assertEqual("REVIEW", result["status"])
        self.assertEqual(2, result["exit_code"])
        self.assertEqual("PASS", result["candidate_assembly_status"])
        self.assertEqual("REVIEW", result["delivery_gate_status"])
        self.assertEqual("REVIEW_CANDIDATE", result["publish_state"])
        self.assertEqual("PASS", result["paired_quality_review_request_coverage_status"])
        self.assertEqual("PENDING_EXTERNAL_REVIEW", result["paired_quality_gate_status"])
        self.assertFalse(result["paired_quality_clearance_granted"])
        self.assertFalse(result["paired_quality_local_clearance_supported"])
        self.assertFalse(result["humanize_completion_claim_allowed"])
        self.assertTrue(Path(result["published_path"]).name == "rendered_review")
        if units is not None:
            self.assertEqual(units, result["paired_quality_units_total"])
            self.assertEqual(units, result["paired_quality_units_pending"])
            self.assertEqual(units, len(result["paired_quality_review_requests"]))

    def structural_plan(
        self,
        unit: dict,
        target_text: str,
        target_source_groups: list[list[str]],
    ) -> dict:
        source_by_id = {
            item["paragraph_id"]: item for item in unit["structural_paragraphs"]
        }
        target_blocks = preparer.structural_paragraph_blocks(target_text)
        self.assertEqual(len(target_blocks), len(target_source_groups))
        groups = []
        for block, source_ids in zip(target_blocks, target_source_groups):
            groups.append(
                {
                    "source_paragraph_ids": source_ids,
                    "target_paragraph_sha256": hashlib.sha256(
                        block.encode("utf-8")
                    ).hexdigest(),
                    "responsibility": source_by_id[source_ids[0]]["responsibility"],
                    "reason": "保持该段原有论述职责并调整相邻次序",
                }
            )
        return {
            "schema_version": "humanize-structural-plan/v1",
            "source_inventory_sha256": unit["structural_inventory_sha256"],
            "target_groups": groups,
        }

    def prepare_structural_pair(
        self, *, extra_pending: bool = False
    ) -> tuple[Path, Path, list[dict]]:
        source = self.root / "transaction.tex"
        text = (
            "\\section{讨论}\n\n"
            "值得注意的是，第一段说明当前观察对象。\n\n"
            "第二段补充两种表述之间的差别 $x=1$。\n\n"
            "第三段说明另一组观察对象 $y=2$。\n\n"
            "值得注意的是，第四段补充比较结果。\n"
        )
        if extra_pending:
            text += "\n\\section{附录}\n\n附录中的独立说明仍待处理。\n"
        source.write_text(text, encoding="utf-8")
        run_dir = self.root / "transaction-run"
        preparer.prepare(
            [source],
            run_dir,
            scene="COURSE",
            intensity="STRUCTURAL",
            structural_transaction_scope="ADJACENT_PAIR",
            max_author_chars=35,
            min_author_chars=0,
        )
        pending = sorted(
            (
                json.loads(path.read_text(encoding="utf-8"))
                for path in (run_dir / "chunks").glob("*.json")
                if json.loads(path.read_text(encoding="utf-8"))["status"]
                == "PENDING"
            ),
            key=lambda item: int(item["start"]),
        )
        inventory = json.loads(
            (run_dir / "structural_transaction_inventory.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual("READY", inventory["status"])
        self.assertEqual(1, len(inventory["transactions"]))
        participant_ids = [
            item["unit_id"]
            for item in inventory["transactions"][0]["compound_refs"]
        ]
        pair = [next(item for item in pending if item["unit_id"] == unit_id) for unit_id in participant_ids]
        self.assertEqual(pair[1]["unit_id"], pair[0]["context_after_unit"])
        self.assertEqual(pair[0]["unit_id"], pair[1]["context_before_unit"])
        self.assertEqual(3 if extra_pending else 2, len(pending))
        return source, run_dir, pair

    def prepare_structural_chain(self) -> tuple[Path, Path, list[dict], dict]:
        source = self.root / "transaction-chain.tex"
        paragraphs = [
            "当前观察对象位于比较区间之内。",
            "另一种表述补充两个对象之间的差别。",
            "当前材料还说明另一组观察对象的变化。",
            "比较结果在这里保留原有适用范围。",
            "新的观察对象位于后续讨论区间之内。",
            "相邻说明补充判断过程及其限制。",
            "末组观察对象仍位于给定范围之内。",
            "相关说明补充结论范围和使用条件。",
            "上述观察在末段收束并保留原有边界。",
        ]
        source.write_text(
            "\\section{讨论}\n\n" + "\n\n".join(paragraphs) + "\n",
            encoding="utf-8",
        )
        run_dir = self.root / "transaction-chain-run"
        preparer.prepare(
            [source],
            run_dir,
            scene="COURSE",
            intensity="STRUCTURAL",
            structural_transaction_scope="ADJACENT_PAIR",
            max_author_chars=35,
            min_author_chars=0,
        )
        pending = sorted(
            (
                json.loads(path.read_text(encoding="utf-8"))
                for path in (run_dir / "chunks").glob("*.json")
                if json.loads(path.read_text(encoding="utf-8"))["status"]
                == "PENDING"
            ),
            key=lambda item: int(item["start"]),
        )
        inventory = json.loads(
            (run_dir / "structural_transaction_inventory.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertGreaterEqual(len(pending), 3)
        self.assertGreaterEqual(len(inventory["transactions"]), 2)
        return source, run_dir, pending, inventory

    def structural_transaction_bundle(
        self, run_dir: Path, units: list[dict]
    ) -> dict:
        inventory = json.loads(
            (run_dir / "structural_transaction_inventory.json").read_text(
                encoding="utf-8"
            )
        )
        transaction = inventory["transactions"][0]
        bindings = [
            {
                "unit_id": unit["unit_id"],
                "chunk_binding_sha256": unit["chunk_binding_sha256"],
                "voice_profile_sha256": unit["voice_profile_sha256"],
            }
            for unit in units
        ]
        blocks = [
            preparer.structural_paragraph_blocks(unit["masked_text"])
            for unit in units
        ]
        source = [unit["structural_paragraphs"] for unit in units]
        self.assertEqual([3, 2], [len(item) for item in blocks])
        target_specs = [
            (
                [
                    blocks[0][0],
                    blocks[0][1].replace("值得注意的是，", ""),
                    blocks[1][0],
                ],
                [[(0, 0)], [(0, 1)], [(1, 0)]],
            ),
            (
                [blocks[0][2], blocks[1][1].replace("值得注意的是，", "")],
                [[(0, 2)], [(1, 1)]],
            ),
        ]
        fragments = []
        for target_unit, (target_blocks, target_source_groups) in zip(
            units, target_specs
        ):
            target_text = "\n\n".join(target_blocks) + "\n"
            target_groups = []
            for block, source_group in zip(target_blocks, target_source_groups):
                target_groups.append(
                    {
                        "source_refs": [
                            {
                                "unit_id": units[unit_index]["unit_id"],
                                "paragraph_id": source[unit_index][paragraph_index][
                                    "paragraph_id"
                                ],
                            }
                            for unit_index, paragraph_index in source_group
                        ],
                        "target_paragraph_sha256": hashlib.sha256(
                            block.encode("utf-8")
                        ).hexdigest(),
                        "responsibility": source[source_group[0][0]][
                            source_group[0][1]
                        ]["responsibility"],
                        "reason": "保持该段原有论述职责并调整相邻次序",
                    }
                )
            fragments.append(
                {
                    "target_unit_id": target_unit["unit_id"],
                    "masked_text": target_text,
                    "keep_reasons": {},
                    "target_groups": target_groups,
                }
            )
        return {
            "schema_version": "humanize-structural-transaction-bundle/v1",
            "transaction_id": transaction["transaction_id"],
            "transaction_binding_sha256": transaction[
                "transaction_binding_sha256"
            ],
            "transaction_inventory_sha256": inventory["inventory_sha256"],
            "unit_bindings": bindings,
            "fragments": fragments,
        }

    def structural_transaction_decline(
        self,
        run_dir: Path,
        units: list[dict],
        *,
        transaction_index: int = 0,
        reason_code: str = "QUESTION_ANSWER_PAIRING_RISK",
        reason: str = "两侧段落分别服务于各自题干，跨单元移动会打乱题解对应关系",
    ) -> dict:
        inventory = json.loads(
            (run_dir / "structural_transaction_inventory.json").read_text(
                encoding="utf-8"
            )
        )
        transaction = inventory["transactions"][transaction_index]
        return {
            "schema_version": "humanize-structural-transaction-decline/v1",
            "decision": "DECLINE",
            "transaction_id": transaction["transaction_id"],
            "transaction_binding_sha256": transaction[
                "transaction_binding_sha256"
            ],
            "transaction_inventory_sha256": inventory["inventory_sha256"],
            "unit_bindings": [
                {
                    "unit_id": unit["unit_id"],
                    "chunk_binding_sha256": unit["chunk_binding_sha256"],
                    "voice_profile_sha256": unit["voice_profile_sha256"],
                }
                for unit in units
            ],
            "reason_code": reason_code,
            "reason": reason,
            "evidence_refs": [
                {
                    "unit_id": unit["unit_id"],
                    "paragraph_id": unit["structural_paragraphs"][0][
                        "paragraph_id"
                    ],
                }
                for unit in units
            ],
        }

    def write_pair_no_change(self, directory: Path, units: list[dict]) -> None:
        for unit in units:
            keep_reasons = (
                {
                    "LEX-EMPH-01": "课程原段用该提示明确切换观察对象，保留其教学定位功能"
                }
                if "值得注意的是" in unit["masked_text"]
                else {}
            )
            payload = self.voice_bound_bundle(
                unit,
                {
                    "decision": "NO_CHANGE",
                    "reason": "现有段序和职责对应清楚",
                    "keep_reasons": keep_reasons,
                },
            )
            (directory / f"{unit['unit_id']}.json").write_text(
                json.dumps(payload, ensure_ascii=False), encoding="utf-8"
            )

    def final_ledger(self, run_dir: Path) -> list[dict[str, str]]:
        with (run_dir / "coverage_ledger.final.csv").open("r", encoding="utf-8-sig", newline="") as handle:
            return list(csv.DictReader(handle))

    def warning_proposal_fields(self, before_text: str, after_text: str) -> dict:
        before = self.root / "proposal-before.tex"
        after = self.root / "proposal-after.tex"
        before.write_text(before_text, encoding="utf-8")
        after.write_text(after_text, encoding="utf-8")
        first = finalizer.output_validator.validate(
            before,
            after,
            scene="COURSE",
            fragment_mode=True,
        )
        request = first["warning_review_request"]
        fingerprint = request["warnings"][0]["warning_fingerprint"]
        return {
            "warning_resolutions": {
                fingerprint: "人工建议核对删除的是重复缓和而非结论强度",
            },
            "warning_review_request_sha256": request["request_sha256"],
        }

    def evidence_snapshot(self, run_dir: Path) -> dict[str, bytes]:
        paths = [
            run_dir / "coverage_ledger.final.csv",
            run_dir / "rendered_manifest.csv",
            run_dir / "rollback_manifest.json",
        ]
        for directory in (run_dir / "validation", run_dir / "diffs"):
            paths.extend(path for path in directory.rglob("*") if path.is_file())
        return {
            str(path.relative_to(run_dir)).replace("\\", "/"): path.read_bytes()
            for path in paths
            if path.is_file()
        }

    def assert_compile_check_schema(self, payload: dict) -> None:
        self.assertEqual(self.COMPILE_CHECK_FIELDS, set(payload))
        self.assertIsInstance(payload["status"], str)
        self.assertIsInstance(payload["command"], str)
        self.assertTrue(payload["exit_code"] is None or isinstance(payload["exit_code"], int))
        self.assertIsInstance(payload["stdout"], str)
        self.assertIsInstance(payload["stderr"], str)
        self.assertTrue(payload["cwd"] is None or isinstance(payload["cwd"], str))
        self.assertIn(payload["integrity_status"], {"PASS", "FAIL", "NOT_RUN"})
        self.assertIsInstance(payload["integrity_changes"], dict)
        self.assertIn(
            payload["process_containment"],
            {"NOT_RUN", "WINDOWS_JOB_OBJECT", "POSIX_PROCESS_GROUP"},
        )
        self.assertIn(payload["descendant_cleanup"], {"NOT_RUN", "PASS", "FAIL"})

    def test_valid_rewrite_restores_protected_text_and_writes_diff(self) -> None:
        source, run_dir, unit = self.prepare(
            "\\section{例题}\n值得注意的是，函数 $f(x)=x^2$ 在此处连续。\n"
        )
        rewrites = self.rewrite_dir()
        masked = unit["masked_text"].replace("值得注意的是，", "")
        (rewrites / f"{unit['unit_id']}.json").write_text(
            json.dumps(
                self.voice_bound_bundle(unit, {"decision": "REWRITE", "masked_text": masked}),
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        result = finalizer.finalize(run_dir, rewrites)
        ledger = self.final_ledger(run_dir)
        row = next(item for item in ledger if item["unit_id"] == unit["unit_id"])
        self.assert_paired_quality_review_candidate(result)
        self.assertEqual("DONE", row["status"])
        self.assertTrue((run_dir / row["diff_path"]).is_file())
        rendered = next((run_dir / "rendered_review").rglob("*.tex")).read_text(
            encoding="utf-8"
        )
        self.assertIn("$f(x)=x^2$", rendered)
        self.assertNotIn("值得注意的是", rendered)
        self.assertEqual("值得注意的是，函数 $f(x)=x^2$ 在此处连续。\n", source.read_text(encoding="utf-8").split("\n", 1)[1])

    def test_rewrite_paired_quality_request_is_persisted_and_hash_bound(self) -> None:
        _, run_dir, unit = self.prepare(
            "\\section{例题}\n值得注意的是，该结论保留原有限定。\n"
        )
        rewrites = self.rewrite_dir()
        rewritten = unit["masked_text"].replace("值得注意的是，", "")
        (rewrites / f"{unit['unit_id']}.json").write_text(
            json.dumps(
                self.voice_bound_bundle(
                    unit, {"decision": "REWRITE", "masked_text": rewritten}
                ),
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

        result = finalizer.finalize(run_dir, rewrites)

        self.assert_paired_quality_review_candidate(result, units=1)
        record = result["paired_quality_review_requests"][unit["unit_id"]]
        self.assertEqual("REWRITE", record["decision"])
        self.assertGreater(record["changes_total"], 0)
        request_path = run_dir / record["path"]
        self.assertTrue(request_path.is_file())
        request = json.loads(request_path.read_text(encoding="utf-8"))
        self.assertEqual(
            "humanize-paired-quality-review-request/v1", request["schema"]
        )
        self.assertEqual("PENDING_EXTERNAL_REVIEW", request["status"])
        self.assertEqual("REWRITE", request["validation_context"]["decision"])
        self.assertEqual("PASS", request["validation_context"]["mechanical_validation_status"])
        self.assertEqual(
            {
                "validator_sha256",
                "invariant_checker_sha256",
                "scanner_sha256",
                "lexicon_sha256",
                "report_extractor_sha256",
                "runtime_contract_sha256",
            },
            set(request["policy_hashes"]),
        )
        self.assertTrue(
            all(len(value) == 64 for value in request["policy_hashes"].values())
        )
        validation = json.loads(
            (run_dir / "validation" / f"{unit['unit_id']}.validation.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(
            validation["evidence"]["before_sha256"],
            request["artifact"]["before_sha256"],
        )
        self.assertEqual(
            validation["evidence"]["after_sha256"],
            request["artifact"]["after_sha256"],
        )
        request_body = dict(request)
        request_body.pop("request_sha256")
        expected_request_sha256 = hashlib.sha256(
            json.dumps(
                request_body,
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
            ).encode("utf-8")
        ).hexdigest()
        self.assertEqual(expected_request_sha256, request["request_sha256"])
        self.assertEqual(request["request_sha256"], record["request_sha256"])

    def test_no_change_paired_quality_request_cannot_self_clear(self) -> None:
        _, run_dir, unit = self.prepare(
            "\\section{定义}\n该定义保持原有平行结构。\n"
        )
        rewrites = self.rewrite_dir()
        (rewrites / f"{unit['unit_id']}.json").write_text(
            json.dumps(
                self.voice_bound_bundle(
                    unit,
                    {
                        "decision": "NO_CHANGE",
                        "reason": "正式定义保持原有平行结构",
                    },
                ),
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

        result = finalizer.finalize(run_dir, rewrites)

        self.assert_paired_quality_review_candidate(result, units=1)
        record = result["paired_quality_review_requests"][unit["unit_id"]]
        request = json.loads((run_dir / record["path"]).read_text(encoding="utf-8"))
        self.assertEqual("NO_CHANGE", record["decision"])
        self.assertEqual(0, record["changes_total"])
        self.assertEqual("NO_CHANGE", request["validation_context"]["decision"])
        self.assertEqual([], request["changes"])
        self.assertEqual(
            request["artifact"]["before_sha256"],
            request["artifact"]["after_sha256"],
        )
        self.assertFalse(request["limitations"]["quality_clearance_granted"])
        self.assertFalse(
            request["review_contract"]["validator_pass_is_quality_clearance"]
        )
        self.assertFalse(result["paired_quality_clearance_granted"])
        self.assertFalse(result["humanize_completion_claim_allowed"])

    def test_missing_paired_quality_request_blocks_formal_delivery(self) -> None:
        _, run_dir, unit = self.prepare(
            "\\section{定义}\n该定义保持原有平行结构。\n"
        )
        rewrites = self.rewrite_dir()
        (rewrites / f"{unit['unit_id']}.json").write_text(
            json.dumps(
                self.voice_bound_bundle(
                    unit,
                    {
                        "decision": "NO_CHANGE",
                        "reason": "正式定义保持原有平行结构",
                    },
                ),
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

        with mock.patch.object(
            finalizer, "_persist_paired_quality_review_request", return_value=None
        ):
            result = finalizer.finalize(run_dir, rewrites)

        self.assertEqual("REVIEW", result["status"])
        self.assertEqual(2, result["exit_code"])
        self.assertEqual("PASS", result["candidate_assembly_status"])
        self.assertEqual("REVIEW", result["delivery_gate_status"])
        self.assertEqual("REVIEW_CANDIDATE", result["publish_state"])
        self.assertEqual(
            "REVIEW", result["paired_quality_review_request_coverage_status"]
        )
        self.assertEqual("BLOCKED", result["paired_quality_gate_status"])
        self.assertEqual(1, result["paired_quality_units_total"])
        self.assertEqual(0, result["paired_quality_units_pending"])
        self.assertEqual(1, result["paired_quality_units_missing"])
        self.assertEqual({}, result["paired_quality_review_requests"])
        self.assertFalse(result["paired_quality_clearance_granted"])
        self.assertFalse(result["humanize_completion_claim_allowed"])
        self.assertEqual(
            "rendered_review", Path(result["published_path"]).name
        )
        self.assertTrue((run_dir / "rendered_review").is_dir())
        self.assertFalse((run_dir / "rendered").exists())

    def test_structural_rewrite_requires_bound_plan_and_accepts_plain_paragraph_move(self) -> None:
        _source, run_dir, unit = self.prepare(
            "\\section{讨论}\n\n"
            "值得注意的是，第一段说明当前观察对象 $x=1$。\n\n"
            "第二段解释两种表述之间的差别 $y=2$。\n",
            intensity="STRUCTURAL",
        )
        blocks = preparer.structural_paragraph_blocks(unit["masked_text"])
        source_ids = [item["paragraph_id"] for item in unit["structural_paragraphs"]]
        self.assertEqual(3, len(blocks))
        target_blocks = [blocks[0], blocks[2], blocks[1].replace("值得注意的是，", "")]
        target_text = "\n\n".join(target_blocks) + "\n"
        plan = self.structural_plan(
            unit,
            target_text,
            [[source_ids[0]], [source_ids[2]], [source_ids[1]]],
        )
        rewrites = self.rewrite_dir()
        bundle = self.voice_bound_bundle(
            unit,
            {
                "decision": "REWRITE",
                "masked_text": target_text,
                "structural_plan": plan,
            },
        )
        (rewrites / f"{unit['unit_id']}.json").write_text(
            json.dumps(bundle, ensure_ascii=False), encoding="utf-8"
        )

        result = finalizer.finalize(run_dir, rewrites)
        ledger = self.final_ledger(run_dir)
        row = next(item for item in ledger if item["unit_id"] == unit["unit_id"])
        evidence = json.loads(
            (run_dir / "validation" / f"{unit['unit_id']}.structural.json").read_text(
                encoding="utf-8"
            )
        )

        self.assertEqual("REVIEW", result["status"], result)
        self.assertEqual(2, result["exit_code"])
        self.assertEqual("PASS", result["candidate_assembly_status"])
        self.assertEqual(0, result["candidate_assembly_exit_code"])
        self.assertEqual("REVIEW", result["delivery_gate_status"])
        self.assertEqual("REVIEW_CANDIDATE", result["publish_state"])
        self.assertEqual("PASS", result["structural_plan_status"])
        self.assertEqual(1, result["structural_changes_applied"])
        self.assertEqual("NOT_EVALUATED", result["structural_semantic_mapping"])
        self.assertEqual(
            "PENDING_EXTERNAL_REVIEW",
            result["structural_semantic_review_status"],
        )
        self.assertFalse(result["structural_semantic_review_local_clearance_supported"])
        self.assertFalse(result["voice_completion_claim_allowed"])
        self.assertFalse(result["humanize_completion_claim_allowed"])
        self.assertEqual("DONE", row["status"])
        self.assertEqual("PASS", row["structural_plan_status"])
        self.assertEqual(
            "PENDING_EXTERNAL_REVIEW",
            row["structural_semantic_review_status"],
        )
        self.assertTrue(evidence["change_applied"])
        self.assertEqual("NOT_EVALUATED", evidence["semantic_mapping"])
        self.assertEqual(
            "PENDING_EXTERNAL_REVIEW", evidence["semantic_review_status"]
        )
        self.assertFalse((run_dir / "rendered").exists())
        self.assertTrue((run_dir / "rendered_review").is_dir())
        request_record = result["structural_semantic_review_requests"][unit["unit_id"]]
        request_path = run_dir / request_record["path"]
        request = json.loads(request_path.read_text(encoding="utf-8"))
        request_body = {
            key: value for key, value in request.items() if key != "request_sha256"
        }
        expected_request_sha256 = hashlib.sha256(
            json.dumps(
                request_body,
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
            ).encode("utf-8")
        ).hexdigest()
        self.assertEqual(expected_request_sha256, request["request_sha256"])
        self.assertEqual(request["request_sha256"], request_record["request_sha256"])
        self.assertEqual(
            "humanize-structural-semantic-review-request/v1", request["schema"]
        )
        self.assertEqual("PENDING_EXTERNAL_REVIEW", request["status"])
        self.assertFalse(request["trust_boundary"]["local_clearance_supported"])
        self.assertFalse(request["trust_boundary"]["completion_claim_allowed"])
        self.assertTrue(request["structural_deltas"])
        self.assertNotIn(
            ".validation_staging", json.dumps(request, ensure_ascii=False)
        )
        validation = json.loads(
            (run_dir / "validation" / f"{unit['unit_id']}.validation.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(
            f"validation/{unit['unit_id']}.before.tex",
            validation["evidence"]["before_path"],
        )
        self.assertEqual(
            f"validation/{unit['unit_id']}.after.tex",
            validation["evidence"]["after_path"],
        )

    def test_structural_no_change_does_not_require_semantic_review(self) -> None:
        _source, run_dir, unit = self.prepare(
            "\\section{讨论}\n\n第一段保持职责。\n\n第二段保持职责。\n",
            intensity="STRUCTURAL",
        )
        rewrites = self.rewrite_dir()
        bundle = self.voice_bound_bundle(
            unit,
            {
                "decision": "NO_CHANGE",
                "reason": "现有段序和职责对应清楚",
                "keep_reasons": {},
            },
        )
        (rewrites / f"{unit['unit_id']}.json").write_text(
            json.dumps(bundle, ensure_ascii=False), encoding="utf-8"
        )

        result = finalizer.finalize(run_dir, rewrites)
        row = next(
            item
            for item in self.final_ledger(run_dir)
            if item["unit_id"] == unit["unit_id"]
        )
        self.assert_paired_quality_review_candidate(result)
        self.assertEqual("PASS", result["candidate_assembly_status"])
        self.assertEqual("PASS", result["structural_semantic_mapping"])
        self.assertEqual("NOT_REQUIRED", result["structural_semantic_review_status"])
        self.assertEqual({}, result["structural_semantic_review_requests"])
        self.assertEqual("NOT_REQUIRED", row["structural_semantic_review_status"])
        self.assertFalse((run_dir / "rendered").exists())
        self.assertTrue((run_dir / "rendered_review").is_dir())

    def test_structural_review_request_captures_pending_modality_warning(self) -> None:
        _source, run_dir, unit = self.prepare(
            "\\section{讨论}\n\n"
            "分析时必须保留这一限制。\n\n"
            "另一种表述中也必须保留同一限制。\n",
            intensity="STRUCTURAL",
        )
        blocks = preparer.structural_paragraph_blocks(unit["masked_text"])
        source_ids = [
            item["paragraph_id"] for item in unit["structural_paragraphs"]
        ]
        target_text = "\n\n".join(
            [
                blocks[0],
                "分析时必须保留这一限制。另一种表述沿用同一限制。",
            ]
        ) + "\n"
        plan = self.structural_plan(
            unit,
            target_text,
            [[source_ids[0]], [source_ids[1], source_ids[2]]],
        )
        rewrites = self.rewrite_dir()
        bundle = self.voice_bound_bundle(
            unit,
            {
                "decision": "REWRITE",
                "masked_text": target_text,
                "structural_plan": plan,
            },
        )
        (rewrites / f"{unit['unit_id']}.json").write_text(
            json.dumps(bundle, ensure_ascii=False), encoding="utf-8"
        )

        result = finalizer.finalize(run_dir, rewrites)
        self.assertEqual("REVIEW", result["status"])
        self.assertEqual("REVIEW", result["candidate_assembly_status"])
        self.assertEqual(
            "PENDING_EXTERNAL_REVIEW",
            result["structural_semantic_review_status"],
        )
        request_record = result["structural_semantic_review_requests"][unit["unit_id"]]
        request = json.loads(
            (run_dir / request_record["path"]).read_text(encoding="utf-8")
        )
        self.assertIn(
            "SPEECH_ACT_MODALITY_SCOPE_CHANGED",
            {item["code"] for item in request["speech_act_warnings"]},
        )
        self.assertFalse((run_dir / "rendered_review").exists())
        self.assertTrue((run_dir / "rendered_partial").is_dir())

    def test_structural_bundle_cannot_self_issue_semantic_clearance(self) -> None:
        _source, run_dir, unit = self.prepare(
            "\\section{讨论}\n\n第一段说明对象。\n\n第二段说明差别。\n",
            intensity="STRUCTURAL",
        )
        blocks = preparer.structural_paragraph_blocks(unit["masked_text"])
        source_ids = [
            item["paragraph_id"] for item in unit["structural_paragraphs"]
        ]
        target_text = "\n\n".join([blocks[0], blocks[2], blocks[1]]) + "\n"
        plan = self.structural_plan(
            unit,
            target_text,
            [[source_ids[0]], [source_ids[2]], [source_ids[1]]],
        )
        rewrites = self.rewrite_dir()
        bundle = self.voice_bound_bundle(
            unit,
            {
                "decision": "REWRITE",
                "masked_text": target_text,
                "structural_plan": plan,
                "structural_semantic_clearance": {
                    "reviewer_kind": "VERIFIED_HUMAN",
                    "overall_status": "PASS",
                },
            },
        )
        (rewrites / f"{unit['unit_id']}.json").write_text(
            json.dumps(bundle, ensure_ascii=False), encoding="utf-8"
        )

        result = finalizer.finalize(run_dir, rewrites)
        row = next(
            item
            for item in self.final_ledger(run_dir)
            if item["unit_id"] == unit["unit_id"]
        )
        self.assertEqual("REVIEW", result["status"])
        self.assertEqual("UNRESOLVED", row["status"])
        self.assertIn("structural_semantic_clearance", row["notes"])
        self.assertEqual({}, result["structural_semantic_review_requests"])

    def test_structural_rewrite_without_plan_is_rejected(self) -> None:
        _source, run_dir, unit = self.prepare(
            "\\section{讨论}\n\n"
            "值得注意的是，第一段说明当前观察对象。\n\n"
            "第二段解释两种表述之间的差别。\n",
            intensity="STRUCTURAL",
        )
        rewrites = self.rewrite_dir()
        target = unit["masked_text"].replace("值得注意的是，", "")
        (rewrites / f"{unit['unit_id']}.json").write_text(
            json.dumps(
                self.voice_bound_bundle(
                    unit, {"decision": "REWRITE", "masked_text": target}
                ),
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

        result = finalizer.finalize(run_dir, rewrites)
        row = next(
            item
            for item in self.final_ledger(run_dir)
            if item["unit_id"] == unit["unit_id"]
        )

        self.assertEqual("REVIEW", result["status"])
        self.assertEqual("REVIEW", result["structural_plan_status"])
        self.assertEqual("UNRESOLVED", row["status"])
        self.assertIn("structural_plan_missing", row["notes"])

    def test_structural_plan_cannot_move_locked_heading_paragraph(self) -> None:
        _source, run_dir, unit = self.prepare(
            "\\section{讨论}\n\n第一段保持职责。\n\n第二段保持职责。\n",
            intensity="STRUCTURAL",
        )
        blocks = preparer.structural_paragraph_blocks(unit["masked_text"])
        source_ids = [item["paragraph_id"] for item in unit["structural_paragraphs"]]
        target_text = "\n\n".join([blocks[1], blocks[0], blocks[2]]) + "\n"
        plan = self.structural_plan(
            unit,
            target_text,
            [[source_ids[1]], [source_ids[0]], [source_ids[2]]],
        )
        rewrites = self.rewrite_dir()
        (rewrites / f"{unit['unit_id']}.json").write_text(
            json.dumps(
                self.voice_bound_bundle(
                    unit,
                    {
                        "decision": "REWRITE",
                        "masked_text": target_text,
                        "structural_plan": plan,
                    },
                ),
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

        result = finalizer.finalize(run_dir, rewrites)
        row = next(
            item
            for item in self.final_ledger(run_dir)
            if item["unit_id"] == unit["unit_id"]
        )
        self.assertEqual("REVIEW", result["status"])
        self.assertIn("structural_locked_paragraph_moved_or_merged", row["notes"])

    def test_structural_plan_cannot_detach_formula_from_its_source_paragraph(self) -> None:
        _source, run_dir, unit = self.prepare(
            "\\section{讨论}\n\n第一段说明对象 $x=1$。\n\n"
            "第二段说明差别 $y=2$。\n",
            intensity="STRUCTURAL",
        )
        blocks = preparer.structural_paragraph_blocks(unit["masked_text"])
        source_ids = [item["paragraph_id"] for item in unit["structural_paragraphs"]]
        p2_token = next(
            preparer.PROTECTED_PLACEHOLDER_RE.finditer(blocks[1])
        ).group(0)
        p3_token = next(
            preparer.PROTECTED_PLACEHOLDER_RE.finditer(blocks[2])
        ).group(0)
        detached_p3 = blocks[2].replace(p3_token, p2_token)
        detached_p2 = blocks[1].replace(p2_token, p3_token)
        target_text = "\n\n".join([blocks[0], detached_p3, detached_p2]) + "\n"
        plan = self.structural_plan(
            unit,
            target_text,
            [[source_ids[0]], [source_ids[2]], [source_ids[1]]],
        )
        rewrites = self.rewrite_dir()
        (rewrites / f"{unit['unit_id']}.json").write_text(
            json.dumps(
                self.voice_bound_bundle(
                    unit,
                    {
                        "decision": "REWRITE",
                        "masked_text": target_text,
                        "structural_plan": plan,
                    },
                ),
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

        result = finalizer.finalize(run_dir, rewrites)
        row = next(
            item
            for item in self.final_ledger(run_dir)
            if item["unit_id"] == unit["unit_id"]
        )
        self.assertEqual("REVIEW", result["status"])
        self.assertIn("structural_protected_span_left_source_paragraph", row["notes"])

    def test_structural_plan_rejects_explicit_paragraph_responsibility_drift(self) -> None:
        _source, run_dir, unit = self.prepare(
            "\\section{讨论}\n\n第一段说明当前观察对象。\n\n第二段解释差别。\n",
            intensity="STRUCTURAL",
        )
        blocks = preparer.structural_paragraph_blocks(unit["masked_text"])
        source_ids = [item["paragraph_id"] for item in unit["structural_paragraphs"]]
        target_blocks = [blocks[0], "综上，" + blocks[1], blocks[2]]
        target_text = "\n\n".join(target_blocks) + "\n"
        plan = self.structural_plan(
            unit,
            target_text,
            [[source_ids[0]], [source_ids[1]], [source_ids[2]]],
        )
        rewrites = self.rewrite_dir()
        (rewrites / f"{unit['unit_id']}.json").write_text(
            json.dumps(
                self.voice_bound_bundle(
                    unit,
                    {
                        "decision": "REWRITE",
                        "masked_text": target_text,
                        "structural_plan": plan,
                    },
                ),
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

        result = finalizer.finalize(run_dir, rewrites)
        row = next(
            item
            for item in self.final_ledger(run_dir)
            if item["unit_id"] == unit["unit_id"]
        )
        self.assertEqual("REVIEW", result["status"])
        self.assertIn("structural_target_responsibility_drift", row["notes"])

    def test_ready_candidate_requires_explicit_disposition(self) -> None:
        _source, run_dir, units = self.prepare_structural_pair()
        rewrites = self.rewrite_dir()
        self.write_pair_no_change(rewrites, units)

        result = finalizer.finalize(run_dir, rewrites)

        self.assertEqual("REVIEW", result["status"])
        self.assertEqual(2, result["exit_code"])
        self.assertEqual("REVIEW", result["candidate_assembly_status"])
        self.assertEqual("REVIEW", result["delivery_gate_status"])
        self.assertEqual("PARTIAL", result["publish_state"])
        self.assertEqual(1, result["structural_transaction_candidates_total"])
        self.assertEqual(0, result["structural_transaction_candidates_executed"])
        self.assertEqual(0, result["structural_transaction_candidates_declined"])
        self.assertEqual(1, result["structural_transaction_candidates_pending"])
        self.assertEqual(
            "REVIEW", result["structural_transaction_candidate_coverage_status"]
        )
        self.assertFalse(result["structural_transaction_scope_complete"])
        self.assertFalse(result["coverage_completion_claim_allowed"])
        disposition = next(
            iter(result["structural_transaction_candidate_dispositions"].values())
        )
        self.assertEqual("PENDING", disposition["disposition"])
        self.assertFalse((run_dir / "rendered").exists())
        self.assertTrue((run_dir / "rendered_partial").is_dir())

    def test_bound_decline_closes_candidate_without_replacing_unit_coverage(self) -> None:
        _source, run_dir, units = self.prepare_structural_pair()
        rewrites = self.rewrite_dir()
        decline = self.structural_transaction_decline(run_dir, units)
        (rewrites / "pair.decline.json").write_text(
            json.dumps(decline, ensure_ascii=False), encoding="utf-8"
        )

        result = finalizer.finalize(run_dir, rewrites)

        self.assertEqual("REVIEW", result["status"])
        self.assertEqual(2, result["exit_code"])
        self.assertEqual("PASS", result["structural_transaction_candidate_coverage_status"])
        self.assertTrue(result["structural_transaction_scope_complete"])
        self.assertEqual(1, result["structural_transaction_candidates_declined"])
        self.assertEqual(0, result["structural_transaction_candidates_pending"])
        self.assertEqual(2, result["unit_statuses"]["PENDING"])
        self.assertFalse(result["coverage_completion_claim_allowed"])

    def test_bound_decline_and_unit_no_change_publish_final(self) -> None:
        _source, run_dir, units = self.prepare_structural_pair()
        rewrites = self.rewrite_dir()
        self.write_pair_no_change(rewrites, units)
        decline = self.structural_transaction_decline(run_dir, units)
        (rewrites / "pair.decline.json").write_text(
            json.dumps(decline, ensure_ascii=False), encoding="utf-8"
        )

        result = finalizer.finalize(run_dir, rewrites)

        self.assert_paired_quality_review_candidate(result, units=2)
        self.assertTrue(result["coverage_completion_claim_allowed"])
        self.assertEqual(1, result["structural_transaction_declines_total"])
        self.assertEqual(1, result["structural_transaction_candidates_declined"])
        self.assertEqual(0, result["structural_transaction_candidates_pending"])
        disposition = result["structural_transaction_candidate_dispositions"][
            decline["transaction_id"]
        ]
        self.assertEqual("DECLINED", disposition["disposition"])
        self.assertEqual("PASS", disposition["evidence_member_coverage"])
        self.assertTrue((run_dir / disposition["path"]).is_file())
        self.assertFalse((run_dir / "rendered").exists())
        self.assertTrue((run_dir / "rendered_review").is_dir())

    def test_decline_rejects_stale_authority_bindings(self) -> None:
        attacks = (
            "transaction_id",
            "transaction_binding_sha256",
            "transaction_inventory_sha256",
            "chunk_binding_sha256",
            "voice_profile_sha256",
        )
        original_root = self.root
        for attack in attacks:
            with self.subTest(attack=attack), tempfile.TemporaryDirectory() as temp:
                self.root = Path(temp)
                _source, run_dir, units = self.prepare_structural_pair()
                rewrites = self.rewrite_dir()
                decline = self.structural_transaction_decline(run_dir, units)
                if attack == "transaction_id":
                    decline[attack] = "STX-" + "f" * 24
                elif attack in {
                    "transaction_binding_sha256",
                    "transaction_inventory_sha256",
                }:
                    decline[attack] = "f" * 64
                else:
                    decline["unit_bindings"][0][attack] = "f" * 64
                (rewrites / "pair.decline.json").write_text(
                    json.dumps(decline, ensure_ascii=False), encoding="utf-8"
                )
                with self.assertRaisesRegex(
                    ValueError,
                    "structural_transaction_(?:candidate_not_unique|binding_hash_mismatch|inventory_hash_mismatch|chunk_binding_mismatch|voice_binding_mismatch)",
                ):
                    finalizer.finalize(run_dir, rewrites)
        self.root = original_root

    def test_decline_rejects_generic_reason_and_invalid_evidence(self) -> None:
        attacks = (
            "generic_reason",
            "generic_long_reason",
            "single_member",
            "unknown",
            "duplicate",
        )
        original_root = self.root
        for attack in attacks:
            with self.subTest(attack=attack), tempfile.TemporaryDirectory() as temp:
                self.root = Path(temp)
                _source, run_dir, units = self.prepare_structural_pair()
                rewrites = self.rewrite_dir()
                decline = self.structural_transaction_decline(run_dir, units)
                if attack == "generic_reason":
                    decline["reason"] = "候选已经审阅无需调整"
                elif attack == "generic_long_reason":
                    decline["reason"] = "候选已经完成审阅并且无需进行任何调整"
                elif attack == "single_member":
                    decline["evidence_refs"] = [decline["evidence_refs"][0]] * 2
                    decline["evidence_refs"][1]["paragraph_id"] = units[0][
                        "structural_paragraphs"
                    ][1]["paragraph_id"]
                elif attack == "unknown":
                    decline["evidence_refs"][0]["paragraph_id"] = "P999-unknown"
                else:
                    decline["evidence_refs"].append(
                        dict(decline["evidence_refs"][0])
                    )
                (rewrites / "pair.decline.json").write_text(
                    json.dumps(decline, ensure_ascii=False), encoding="utf-8"
                )
                with self.assertRaisesRegex(
                    ValueError,
                    "structural_transaction_decline_(?:reason_not_specific|evidence_ref_duplicate|evidence_ref_unknown|evidence_member_coverage_mismatch)",
                ):
                    finalizer.finalize(run_dir, rewrites)
        self.root = original_root

    def test_transaction_execution_and_decline_conflict(self) -> None:
        _source, run_dir, units = self.prepare_structural_pair()
        rewrites = self.rewrite_dir()
        transaction = self.structural_transaction_bundle(run_dir, units)
        decline = self.structural_transaction_decline(run_dir, units)
        (rewrites / "pair.transaction.json").write_text(
            json.dumps(transaction, ensure_ascii=False), encoding="utf-8"
        )
        (rewrites / "pair.decline.json").write_text(
            json.dumps(decline, ensure_ascii=False), encoding="utf-8"
        )

        with self.assertRaisesRegex(ValueError, "execution and decline conflict"):
            finalizer.finalize(run_dir, rewrites)

    def test_decline_replay_is_deterministic(self) -> None:
        _source, run_dir, units = self.prepare_structural_pair()
        rewrites = self.rewrite_dir()
        self.write_pair_no_change(rewrites, units)
        decline = self.structural_transaction_decline(run_dir, units)
        (rewrites / "pair.decline.json").write_text(
            json.dumps(decline, ensure_ascii=False), encoding="utf-8"
        )

        first = finalizer.finalize(run_dir, rewrites)
        rendered_before = _directory_bytes(run_dir / "rendered_review")
        decline_before = (run_dir / "validation" / f"{decline['transaction_id']}.decline.json").read_bytes()
        second = finalizer.finalize(run_dir, rewrites)

        self.assert_paired_quality_review_candidate(second, units=2)
        self.assertEqual("PASS", second["assembly_replay_idempotency"])
        self.assertEqual(
            first["structural_transaction_candidate_dispositions"],
            second["structural_transaction_candidate_dispositions"],
        )
        self.assertEqual(
            rendered_before, _directory_bytes(run_dir / "rendered_review")
        )
        self.assertEqual(
            decline_before,
            (run_dir / "validation" / f"{decline['transaction_id']}.decline.json").read_bytes(),
        )

    def test_overlapping_candidates_require_individual_dispositions(self) -> None:
        _source, run_dir, pending, inventory = self.prepare_structural_chain()
        rewrites = self.rewrite_dir()
        self.write_pair_no_change(rewrites, pending)
        unit_by_id = {unit["unit_id"]: unit for unit in pending}

        first_candidate = inventory["transactions"][0]
        first_units = [
            unit_by_id[item["unit_id"]]
            for item in first_candidate["compound_refs"]
        ]
        first_decline = self.structural_transaction_decline(
            run_dir,
            first_units,
            transaction_index=0,
            reason_code="NO_CROSS_UNIT_STYLE_GAIN",
            reason="两侧段落已经各自承担完整说明职责，跨单元移动没有独立文风收益",
        )
        (rewrites / "first.decline.json").write_text(
            json.dumps(first_decline, ensure_ascii=False), encoding="utf-8"
        )

        first = finalizer.finalize(run_dir, rewrites)
        self.assertEqual("REVIEW", first["status"])
        self.assertEqual(1, first["structural_transaction_candidates_declined"])
        self.assertEqual(
            len(inventory["transactions"]) - 1,
            first["structural_transaction_candidates_pending"],
        )

        for index, candidate in enumerate(inventory["transactions"][1:], 1):
            candidate_units = [
                unit_by_id[item["unit_id"]] for item in candidate["compound_refs"]
            ]
            decline = self.structural_transaction_decline(
                run_dir,
                candidate_units,
                transaction_index=index,
                reason_code="DEPENDENCY_OR_REFERENT_RISK",
                reason="相邻说明依赖各自单元中的观察对象，跨单元移动会造成指代范围漂移",
            )
            (rewrites / f"candidate-{index}.decline.json").write_text(
                json.dumps(decline, ensure_ascii=False), encoding="utf-8"
            )

        second = finalizer.finalize(run_dir, rewrites)
        self.assert_paired_quality_review_candidate(second, units=5)
        self.assertEqual(
            len(inventory["transactions"]),
            second["structural_transaction_candidates_declined"],
        )
        self.assertEqual(0, second["structural_transaction_candidates_pending"])
        self.assertTrue(second["structural_transaction_scope_complete"])

    def test_structural_transaction_passes_two_fragments_and_document_gate(self) -> None:
        source, run_dir, units = self.prepare_structural_pair()
        rewrites = self.rewrite_dir()
        bundle = self.structural_transaction_bundle(run_dir, units)
        (rewrites / "pair.transaction.json").write_text(
            json.dumps(bundle, ensure_ascii=False), encoding="utf-8"
        )

        result = finalizer.finalize(run_dir, rewrites)
        ledger = {row["unit_id"]: row for row in self.final_ledger(run_dir)}
        transaction = result["structural_transaction_results"][
            bundle["transaction_id"]
        ]

        self.assertEqual("REVIEW", result["status"], result)
        self.assertEqual(2, result["exit_code"])
        self.assertEqual("PASS", result["candidate_assembly_status"])
        self.assertEqual("REVIEW", result["delivery_gate_status"])
        self.assertEqual("REVIEW_CANDIDATE", result["publish_state"])
        self.assertEqual(1, result["structural_transaction_candidates_executed"])
        self.assertEqual(0, result["structural_transaction_candidates_pending"])
        self.assertEqual(
            "EXECUTED",
            result["structural_transaction_candidate_dispositions"][
                bundle["transaction_id"]
            ]["disposition"],
        )
        self.assertEqual("PASS", transaction["atomic_gate_status"])
        self.assertEqual("PASS", transaction["source_member_claim_status"])
        self.assertEqual(
            {unit["unit_id"]: "PASS" for unit in units},
            transaction["fragment_gate_statuses"],
        )
        self.assertEqual("PASS", transaction["document_gate_status"])
        self.assertTrue(transaction["change_applied"])
        self.assertEqual(
            {"DONE"}, {ledger[unit["unit_id"]]["status"] for unit in units}
        )
        self.assertFalse((run_dir / "rendered").exists())
        self.assertFalse((run_dir / "rendered_partial").exists())
        self.assertTrue((run_dir / "rendered_review").is_dir())
        self.assertEqual(
            source.read_text(encoding="utf-8"),
            "\\section{讨论}\n\n"
            "值得注意的是，第一段说明当前观察对象。\n\n"
            "第二段补充两种表述之间的差别 $x=1$。\n\n"
            "第三段说明另一组观察对象 $y=2$。\n\n"
            "值得注意的是，第四段补充比较结果。\n",
        )
        request_record = result["structural_transaction_review_requests"][
            bundle["transaction_id"]
        ]
        request = json.loads(
            (run_dir / request_record["path"]).read_text(encoding="utf-8")
        )
        self.assertEqual(
            "humanize-structural-transaction-review-request/v1",
            request["schema"],
        )
        self.assertEqual(
            [unit["unit_id"] for unit in units], request["unit_ids"]
        )
        self.assertEqual("NOT_EVALUATED", request["trust_boundary"]["semantic_mapping"])
        self.assertFalse(request["trust_boundary"]["local_clearance_supported"])
        self.assertEqual(2, len(request["source_mapping"]))
        self.assertTrue(
            any(
                "CROSS_UNIT_MOVE" in delta["change_kinds"]
                for delta in request["structural_deltas"]
            )
        )
        self.assertEqual(4, len(request["context_hashes"]))
        self.assertEqual(
            bundle["transaction_binding_sha256"],
            request["transaction_binding_sha256"],
        )
        self.assertEqual(2, len(request["frozen_pair"]["compound_refs"]))

    def test_structural_transaction_single_fragment_failure_rolls_back_both(self) -> None:
        source, run_dir, units = self.prepare_structural_pair()
        source_before = source.read_bytes()
        rewrites = self.rewrite_dir()
        bundle = self.structural_transaction_bundle(run_dir, units)
        second = bundle["fragments"][1]
        protected = next(
            preparer.PROTECTED_PLACEHOLDER_RE.finditer(second["masked_text"])
        ).group(0)
        second["masked_text"] = second["masked_text"].replace(protected, "", 1)
        target_blocks = preparer.structural_paragraph_blocks(second["masked_text"])
        for target, block in zip(second["target_groups"], target_blocks):
            target["target_paragraph_sha256"] = hashlib.sha256(
                block.encode("utf-8")
            ).hexdigest()
        (rewrites / "pair.transaction.json").write_text(
            json.dumps(bundle, ensure_ascii=False), encoding="utf-8"
        )

        result = finalizer.finalize(run_dir, rewrites)
        ledger = {row["unit_id"]: row for row in self.final_ledger(run_dir)}
        transaction = result["structural_transaction_results"][
            bundle["transaction_id"]
        ]

        self.assertEqual("REVIEW", result["status"])
        self.assertEqual("ROLLED_BACK", transaction["atomic_gate_status"])
        self.assertEqual(1, result["structural_transaction_candidates_executed"])
        self.assertEqual(0, result["structural_transaction_candidates_pending"])
        self.assertEqual(
            "EXECUTED",
            result["structural_transaction_candidate_dispositions"][
                bundle["transaction_id"]
            ]["disposition"],
        )
        self.assertEqual("PASS", transaction["fragment_gate_statuses"][units[0]["unit_id"]])
        self.assertEqual("FAIL", transaction["fragment_gate_statuses"][units[1]["unit_id"]])
        self.assertEqual("NOT_RUN", transaction["document_gate_status"])
        self.assertEqual(
            {"UNRESOLVED"},
            {ledger[unit["unit_id"]]["status"] for unit in units},
        )
        self.assertTrue(
            all(not ledger[unit["unit_id"]]["diff_path"] for unit in units)
        )
        self.assertFalse((run_dir / "rendered_review").exists())
        self.assertEqual({}, result["paired_quality_review_requests"])
        self.assertEqual([], list((run_dir / "validation").glob(
            "*.paired-quality-review-request.json"
        )))
        self.assertEqual(source_before, source.read_bytes())
        rollback = json.loads(
            (run_dir / "rollback_manifest.json").read_text(encoding="utf-8")
        )["atomic_transactions"][bundle["transaction_id"]]
        self.assertEqual(0, rollback["accepted_member_count"])
        self.assertEqual(0, rollback["published_member_count"])

    def test_structural_transaction_repetition_block_rolls_back_entire_pair(self) -> None:
        _source, run_dir, units = self.prepare_structural_pair()
        rewrites = self.rewrite_dir()
        bundle = self.structural_transaction_bundle(run_dir, units)
        (rewrites / "pair.transaction.json").write_text(
            json.dumps(bundle, ensure_ascii=False), encoding="utf-8"
        )
        repetition_result = {
            "schema_version": "humanize-cross-unit-repetition/v1",
            "status": "REVIEW",
            "expected_units": 2,
            "evaluated_units": 2,
            "before_blocks": 6,
            "after_blocks": 6,
            "findings": [],
            "finding_count": 1,
            "inherited_findings": [],
            "inherited_finding_count": 0,
            "blocking_unit_ids": [units[0]["unit_id"]],
            "review_reasons": [],
        }

        with mock.patch.object(
            finalizer,
            "_audit_cross_unit_repetition",
            return_value=repetition_result,
        ):
            result = finalizer.finalize(run_dir, rewrites)

        ledger = {row["unit_id"]: row for row in self.final_ledger(run_dir)}
        transaction = result["structural_transaction_results"][
            bundle["transaction_id"]
        ]
        self.assertEqual("ROLLED_BACK", transaction["atomic_gate_status"])
        self.assertEqual("CROSS_UNIT_REPETITION", transaction["rollback_reason"])
        self.assertEqual(
            {"UNRESOLVED"},
            {ledger[unit["unit_id"]]["status"] for unit in units},
        )
        self.assertTrue(
            all(not ledger[unit["unit_id"]]["diff_path"] for unit in units)
        )
        self.assertFalse((run_dir / "rendered_review").exists())

    def test_transaction_inventory_self_reseal_cannot_replace_frozen_rebuild(self) -> None:
        _source, run_dir, _units = self.prepare_structural_pair()
        inventory_path = run_dir / "structural_transaction_inventory.json"
        inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
        inventory["transactions"][0]["constraints"][
            "semantic_clearance_granted"
        ] = True
        inventory.pop("inventory_sha256")
        inventory["inventory_sha256"] = preparer.canonical_sha256(inventory)
        inventory_path.write_text(
            json.dumps(inventory, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        resealed = preparer.build_integrity_manifest(run_dir)
        (run_dir / "prepare_integrity.json").write_text(
            json.dumps(resealed, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

        with self.assertRaisesRegex(
            ValueError, "structural transaction inventory rebuild mismatch"
        ):
            finalizer.finalize(run_dir, self.rewrite_dir())

    def test_finalizer_enforces_strict_v2_integrity_manifest_contract(self) -> None:
        attacks = ("duplicate", "path_traversal", "unknown_field", "invalid_bytes")
        original_root = self.root
        for attack in attacks:
            with self.subTest(attack=attack), tempfile.TemporaryDirectory() as temp:
                self.root = Path(temp)
                _source, run_dir, _units = self.prepare_structural_pair()
                path = run_dir / "prepare_integrity.json"
                manifest = json.loads(path.read_text(encoding="utf-8"))
                if attack == "duplicate":
                    manifest["artifacts"].append(dict(manifest["artifacts"][0]))
                elif attack == "path_traversal":
                    manifest["artifacts"][0]["path"] = "../outside.json"
                elif attack == "unknown_field":
                    manifest["authority"] = "caller"
                else:
                    manifest["artifacts"][0]["bytes"] = True
                path.write_text(
                    json.dumps(manifest, ensure_ascii=False), encoding="utf-8"
                )
                with self.assertRaisesRegex(ValueError, "integrity"):
                    finalizer.finalize(run_dir, self.rewrite_dir())
        self.root = original_root

    def test_legacy_integrity_schema_cannot_authorize_transaction_inventory(self) -> None:
        _source, run_dir, _units = self.prepare_structural_pair()
        path = run_dir / "prepare_integrity.json"
        manifest = json.loads(path.read_text(encoding="utf-8"))
        legacy = {"schema_version": 1, "artifacts": manifest["artifacts"]}
        path.write_text(json.dumps(legacy, ensure_ascii=False), encoding="utf-8")

        with self.assertRaisesRegex(
            ValueError, "legacy prepare integrity cannot authorize transactions"
        ):
            finalizer.finalize(run_dir, self.rewrite_dir())

    def test_transaction_member_cannot_also_have_standalone_bundle(self) -> None:
        _source, run_dir, units = self.prepare_structural_pair()
        rewrites = self.rewrite_dir()
        bundle = self.structural_transaction_bundle(run_dir, units)
        (rewrites / "pair.transaction.json").write_text(
            json.dumps(bundle, ensure_ascii=False), encoding="utf-8"
        )
        standalone = self.voice_bound_bundle(
            units[0],
            {"decision": "NO_CHANGE", "reason": "该段保持原有自然表达"},
        )
        (rewrites / f"{units[0]['unit_id']}.json").write_text(
            json.dumps(standalone, ensure_ascii=False), encoding="utf-8"
        )

        with self.assertRaisesRegex(
            ValueError, "member also has standalone rewrite"
        ):
            finalizer.finalize(run_dir, rewrites)

    def test_transaction_member_cannot_be_claimed_by_two_transactions(self) -> None:
        _source, run_dir, units = self.prepare_structural_pair()
        rewrites = self.rewrite_dir()
        first = self.structural_transaction_bundle(run_dir, units)
        second = json.loads(json.dumps(first))
        second["transaction_id"] = "STX-" + "b" * 24
        (rewrites / "first.transaction.json").write_text(
            json.dumps(first, ensure_ascii=False), encoding="utf-8"
        )
        (rewrites / "second.transaction.json").write_text(
            json.dumps(second, ensure_ascii=False), encoding="utf-8"
        )

        with self.assertRaisesRegex(ValueError, "member claimed twice"):
            finalizer.finalize(run_dir, rewrites)

    def test_transaction_source_ref_attacks_roll_back_both_members(self) -> None:
        attacks = ("duplicate", "unknown", "locked_cross_unit")
        original_root = self.root
        for attack in attacks:
            with self.subTest(attack=attack), tempfile.TemporaryDirectory() as temp:
                self.root = Path(temp)
                _source, run_dir, units = self.prepare_structural_pair()
                rewrites = self.rewrite_dir()
                bundle = self.structural_transaction_bundle(run_dir, units)
                if attack == "duplicate":
                    bundle["fragments"][1]["target_groups"][0]["source_refs"] = [
                        dict(
                            bundle["fragments"][0]["target_groups"][1][
                                "source_refs"
                            ][0]
                        )
                    ]
                elif attack == "unknown":
                    bundle["fragments"][1]["target_groups"][0]["source_refs"] = [
                        {"unit_id": "U-third", "paragraph_id": "P001-unknown"}
                    ]
                else:
                    heading_block = preparer.structural_paragraph_blocks(
                        units[0]["masked_text"]
                    )[0]
                    heading = units[0]["structural_paragraphs"][0]
                    bundle["fragments"][1]["masked_text"] = "\n\n".join(
                        [
                            heading_block,
                            preparer.structural_paragraph_blocks(
                                bundle["fragments"][1]["masked_text"]
                            )[1],
                        ]
                    ) + "\n"
                    target = bundle["fragments"][1]["target_groups"][0]
                    target["source_refs"] = [
                        {
                            "unit_id": units[0]["unit_id"],
                            "paragraph_id": heading["paragraph_id"],
                        }
                    ]
                    target["target_paragraph_sha256"] = hashlib.sha256(
                        heading_block.encode("utf-8")
                    ).hexdigest()
                    target["responsibility"] = heading["responsibility"]
                (rewrites / "pair.transaction.json").write_text(
                    json.dumps(bundle, ensure_ascii=False), encoding="utf-8"
                )

                result = finalizer.finalize(run_dir, rewrites)
                ledger = {
                    row["unit_id"]: row for row in self.final_ledger(run_dir)
                }
                transaction = result["structural_transaction_results"][
                    bundle["transaction_id"]
                ]
                self.assertEqual("ROLLED_BACK", transaction["atomic_gate_status"])
                self.assertEqual(
                    {"UNRESOLVED"},
                    {ledger[unit["unit_id"]]["status"] for unit in units},
                )
                self.assertTrue(
                    all(
                        not ledger[unit["unit_id"]]["diff_path"] for unit in units
                    )
                )
                self.assertFalse((run_dir / "rendered_review").exists())
        self.root = original_root

    def test_transaction_document_gate_failure_rolls_back_two_fragment_passes(self) -> None:
        _source, run_dir, units = self.prepare_structural_pair()
        rewrites = self.rewrite_dir()
        bundle = self.structural_transaction_bundle(run_dir, units)
        (rewrites / "pair.transaction.json").write_text(
            json.dumps(bundle, ensure_ascii=False), encoding="utf-8"
        )
        original_check = finalizer.invariants.check_documents

        def fail_document_only(before, after, **kwargs):
            result = original_check(before, after, **kwargs)
            if not kwargs.get("fragment_mode", False):
                result.errors.append(
                    finalizer.invariants.Diagnostic(
                        code="TEST_DOCUMENT_GATE_FAILURE",
                        severity="error",
                        message="forced document gate failure",
                    )
                )
            return result

        with mock.patch.object(
            finalizer.invariants,
            "check_documents",
            side_effect=fail_document_only,
        ):
            result = finalizer.finalize(run_dir, rewrites)

        transaction = result["structural_transaction_results"][
            bundle["transaction_id"]
        ]
        ledger = {row["unit_id"]: row for row in self.final_ledger(run_dir)}
        self.assertEqual(
            {unit["unit_id"]: "PASS" for unit in units},
            transaction["fragment_gate_statuses"],
        )
        self.assertEqual("FAIL", transaction["document_gate_status"])
        self.assertEqual("ROLLED_BACK", transaction["atomic_gate_status"])
        self.assertTrue(
            all(ledger[unit["unit_id"]]["status"] == "UNRESOLVED" for unit in units)
        )
        self.assertTrue(
            all(not ledger[unit["unit_id"]]["diff_path"] for unit in units)
        )

    def test_transaction_stale_binding_surfaces_roll_back_both_members(self) -> None:
        attacks = (
            "transaction_binding_sha256",
            "transaction_inventory_sha256",
            "chunk_binding_sha256",
            "voice_profile_sha256",
            "transaction_id",
        )
        original_root = self.root
        for attack in attacks:
            with self.subTest(attack=attack), tempfile.TemporaryDirectory() as temp:
                self.root = Path(temp)
                _source, run_dir, units = self.prepare_structural_pair()
                rewrites = self.rewrite_dir()
                bundle = self.structural_transaction_bundle(run_dir, units)
                if attack in {
                    "transaction_binding_sha256",
                    "transaction_inventory_sha256",
                }:
                    bundle[attack] = "f" * 64
                elif attack == "transaction_id":
                    bundle[attack] = "STX-" + "f" * 24
                else:
                    bundle["unit_bindings"][0][attack] = "f" * 64
                (rewrites / "pair.transaction.json").write_text(
                    json.dumps(bundle, ensure_ascii=False), encoding="utf-8"
                )

                result = finalizer.finalize(run_dir, rewrites)
                transaction = result["structural_transaction_results"][
                    bundle["transaction_id"]
                ]
                ledger = {
                    row["unit_id"]: row for row in self.final_ledger(run_dir)
                }
                self.assertEqual("ROLLED_BACK", transaction["atomic_gate_status"])
                self.assertEqual("AUTHORITY_BINDING", transaction["rollback_reason"])
                self.assertTrue(
                    all(
                        ledger[unit["unit_id"]]["status"] == "UNRESOLVED"
                        and not ledger[unit["unit_id"]]["diff_path"]
                        for unit in units
                    )
                )
        self.root = original_root

    def test_transaction_strict_schema_rejects_bare_refs_clearance_and_path_id(self) -> None:
        attacks = ("bare_ref", "self_clearance", "path_id")
        original_root = self.root
        for attack in attacks:
            with self.subTest(attack=attack), tempfile.TemporaryDirectory() as temp:
                self.root = Path(temp)
                _source, run_dir, units = self.prepare_structural_pair()
                rewrites = self.rewrite_dir()
                bundle = self.structural_transaction_bundle(run_dir, units)
                if attack == "bare_ref":
                    bundle["fragments"][0]["target_groups"][0][
                        "source_refs"
                    ] = [units[0]["structural_paragraphs"][0]["paragraph_id"]]
                elif attack == "self_clearance":
                    bundle["structural_semantic_clearance"] = {
                        "reviewer_kind": "VERIFIED_HUMAN",
                        "status": "PASS",
                    }
                else:
                    bundle["transaction_id"] = "../STX-escape"
                (rewrites / "pair.transaction.json").write_text(
                    json.dumps(bundle, ensure_ascii=False), encoding="utf-8"
                )
                with self.assertRaisesRegex(
                    ValueError,
                    "structural_transaction_(?:source_ref_fields|bundle_fields|id)_invalid",
                ):
                    finalizer.finalize(run_dir, rewrites)
        self.root = original_root

    def test_transaction_never_enters_partial_when_other_unit_is_pending(self) -> None:
        source, run_dir, units = self.prepare_structural_pair(extra_pending=True)
        source_before = source.read_text(encoding="utf-8")
        rewrites = self.rewrite_dir()
        bundle = self.structural_transaction_bundle(run_dir, units)
        (rewrites / "pair.transaction.json").write_text(
            json.dumps(bundle, ensure_ascii=False), encoding="utf-8"
        )

        result = finalizer.finalize(run_dir, rewrites)
        transaction = result["structural_transaction_results"][
            bundle["transaction_id"]
        ]
        self.assertEqual("ROLLED_BACK", transaction["atomic_gate_status"])
        self.assertEqual(
            "INCOMPLETE_DOCUMENT_COVERAGE", transaction["rollback_reason"]
        )
        self.assertFalse((run_dir / "rendered_review").exists())
        partial = next((run_dir / "rendered_partial").rglob("*.tex"))
        self.assertEqual(source_before, partial.read_text(encoding="utf-8"))
        rollback = json.loads(
            (run_dir / "rollback_manifest.json").read_text(encoding="utf-8")
        )["atomic_transactions"][bundle["transaction_id"]]
        self.assertEqual(0, rollback["accepted_member_count"])
        self.assertEqual(0, rollback["published_member_count"])

    def test_transaction_review_candidate_replay_is_idempotent(self) -> None:
        _source, run_dir, units = self.prepare_structural_pair()
        rewrites = self.rewrite_dir()
        bundle = self.structural_transaction_bundle(run_dir, units)
        (rewrites / "pair.transaction.json").write_text(
            json.dumps(bundle, ensure_ascii=False), encoding="utf-8"
        )
        first = finalizer.finalize(run_dir, rewrites)
        rendered_before = _directory_bytes(run_dir / "rendered_review")
        request_before = first["structural_transaction_review_requests"][
            bundle["transaction_id"]
        ]["request_sha256"]

        second = finalizer.finalize(run_dir, rewrites)

        self.assertEqual("PASS", second["idempotency"])
        self.assertEqual(rendered_before, _directory_bytes(run_dir / "rendered_review"))
        self.assertEqual(
            request_before,
            second["structural_transaction_review_requests"][
                bundle["transaction_id"]
            ]["request_sha256"],
        )

    def test_failed_transaction_rerun_preserves_previous_review_candidate(self) -> None:
        _source, run_dir, units = self.prepare_structural_pair()
        rewrites = self.rewrite_dir()
        bundle = self.structural_transaction_bundle(run_dir, units)
        path = rewrites / "pair.transaction.json"
        path.write_text(json.dumps(bundle, ensure_ascii=False), encoding="utf-8")
        first = finalizer.finalize(run_dir, rewrites)
        self.assertEqual("REVIEW", first["status"])
        rendered_before = _directory_bytes(run_dir / "rendered_review")
        evidence_before = self.evidence_snapshot(run_dir)

        second_fragment = bundle["fragments"][1]
        protected = next(
            preparer.PROTECTED_PLACEHOLDER_RE.finditer(
                second_fragment["masked_text"]
            )
        ).group(0)
        second_fragment["masked_text"] = second_fragment["masked_text"].replace(
            protected, "", 1
        )
        for target, block in zip(
            second_fragment["target_groups"],
            preparer.structural_paragraph_blocks(second_fragment["masked_text"]),
        ):
            target["target_paragraph_sha256"] = hashlib.sha256(
                block.encode("utf-8")
            ).hexdigest()
        path.write_text(json.dumps(bundle, ensure_ascii=False), encoding="utf-8")

        second = finalizer.finalize(run_dir, rewrites)

        self.assertEqual("FAIL", second["status"])
        self.assertEqual(rendered_before, _directory_bytes(run_dir / "rendered_review"))
        self.assertEqual(evidence_before, self.evidence_snapshot(run_dir))

    def test_transaction_compile_failure_publishes_no_review_candidate(self) -> None:
        source, run_dir, units = self.prepare_structural_pair()
        source_before = source.read_bytes()
        rewrites = self.rewrite_dir()
        bundle = self.structural_transaction_bundle(run_dir, units)
        (rewrites / "pair.transaction.json").write_text(
            json.dumps(bundle, ensure_ascii=False), encoding="utf-8"
        )
        command = f'"{sys.executable}" -c "raise SystemExit(9)"'

        result = finalizer.finalize(run_dir, rewrites, check_command=command)

        self.assertEqual("FAIL", result["status"])
        self.assertEqual(9, result["compile_check"]["exit_code"])
        self.assertFalse((run_dir / "rendered_review").exists())
        self.assertTrue((run_dir / "failed_staging").is_dir())
        self.assertEqual(source_before, source.read_bytes())
        rollback = json.loads(
            (run_dir / "rollback_manifest.json").read_text(encoding="utf-8")
        )["atomic_transactions"][bundle["transaction_id"]]
        self.assertEqual(0, rollback["published_member_count"])

    def test_transaction_revises_previous_quality_review_candidate(self) -> None:
        _source, run_dir, units = self.prepare_structural_pair()
        no_change = self.rewrite_dir()
        self.write_pair_no_change(no_change, units)
        decline = self.structural_transaction_decline(run_dir, units)
        (no_change / "pair.decline.json").write_text(
            json.dumps(decline, ensure_ascii=False), encoding="utf-8"
        )
        first = finalizer.finalize(run_dir, no_change)
        self.assert_paired_quality_review_candidate(first, units=2)
        review_before = _directory_bytes(run_dir / "rendered_review")

        transactions = self.root / "transaction-rewrites"
        transactions.mkdir()
        bundle = self.structural_transaction_bundle(run_dir, units)
        (transactions / "pair.transaction.json").write_text(
            json.dumps(bundle, ensure_ascii=False), encoding="utf-8"
        )
        second = finalizer.finalize(run_dir, transactions)

        self.assert_paired_quality_review_candidate(second, units=2)
        self.assertFalse(second["published_namespace_conflict"])
        self.assertNotEqual(
            review_before, _directory_bytes(run_dir / "rendered_review")
        )
        self.assertEqual("NOT_APPLICABLE_PROGRESS", second["idempotency"])
        self.assertTrue((run_dir / "partial_history.jsonl").is_file())
        self.assertFalse((run_dir / "rendered").exists())

    def test_no_change_revises_previous_transaction_review_candidate(self) -> None:
        _source, run_dir, units = self.prepare_structural_pair()
        transactions = self.rewrite_dir()
        bundle = self.structural_transaction_bundle(run_dir, units)
        (transactions / "pair.transaction.json").write_text(
            json.dumps(bundle, ensure_ascii=False), encoding="utf-8"
        )
        first = finalizer.finalize(run_dir, transactions)
        self.assert_paired_quality_review_candidate(first, units=2)
        review_before = _directory_bytes(run_dir / "rendered_review")

        no_change = self.root / "no-change-rewrites"
        no_change.mkdir()
        self.write_pair_no_change(no_change, units)
        decline = self.structural_transaction_decline(run_dir, units)
        (no_change / "pair.decline.json").write_text(
            json.dumps(decline, ensure_ascii=False), encoding="utf-8"
        )
        second = finalizer.finalize(run_dir, no_change)

        self.assert_paired_quality_review_candidate(second, units=2)
        self.assertFalse(second["published_namespace_conflict"])
        self.assertNotEqual(
            review_before, _directory_bytes(run_dir / "rendered_review")
        )
        self.assertEqual("NOT_APPLICABLE_PROGRESS", second["idempotency"])
        self.assertEqual("PASS", second["structural_semantic_mapping"])
        self.assertEqual("NOT_REQUIRED", second["structural_semantic_review_status"])
        self.assertFalse((run_dir / "rendered").exists())

    def test_transaction_rejects_second_pass_receipt_as_false_convergence(self) -> None:
        _source, run_dir, units = self.prepare_structural_pair()
        rewrites = self.rewrite_dir()
        bundle = self.structural_transaction_bundle(run_dir, units)
        (rewrites / "pair.transaction.json").write_text(
            json.dumps(bundle, ensure_ascii=False), encoding="utf-8"
        )

        result = finalizer.finalize(
            run_dir,
            rewrites,
            second_pass_receipt=self.root / "caller-receipt.json",
        )

        self.assertEqual("FAIL", result["status"])
        self.assertEqual("FAIL", result["humanize_second_pass_convergence"])
        self.assertEqual(
            "second_pass_receipt_not_allowed_for_review_candidate:STRUCTURAL_TRANSACTION",
            result["humanize_second_pass_evidence"]["error"],
        )
        self.assertEqual("INVALID_EVIDENCE", result["second_pass_stability_status"])
        self.assertFalse(result["second_pass_quality_clearance_granted"])
        self.assertFalse(result["humanize_completion_claim_allowed"])
        self.assertFalse((run_dir / "rendered_review").exists())

    def test_paired_quality_candidate_rejects_second_pass_receipt(self) -> None:
        _, run_dir, unit = self.prepare(
            "\\section{定义}\n该定义保持原有平行结构。\n"
        )
        rewrites = self.rewrite_dir()
        (rewrites / f"{unit['unit_id']}.json").write_text(
            json.dumps(
                self.voice_bound_bundle(
                    unit,
                    {
                        "decision": "NO_CHANGE",
                        "reason": "正式定义保持原有平行结构",
                    },
                ),
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

        result = finalizer.finalize(
            run_dir,
            rewrites,
            second_pass_receipt=self.root / "caller-receipt.json",
        )

        self.assertEqual("FAIL", result["status"])
        self.assertEqual(1, result["exit_code"])
        self.assertEqual("FAIL", result["humanize_second_pass_convergence"])
        self.assertEqual(
            "second_pass_receipt_not_allowed_for_review_candidate:PAIRED_QUALITY",
            result["humanize_second_pass_evidence"]["error"],
        )
        self.assertEqual("INVALID_EVIDENCE", result["second_pass_stability_status"])
        self.assertFalse(result["second_pass_quality_clearance_granted"])
        self.assertFalse(result["paired_quality_clearance_granted"])
        self.assertFalse(result["humanize_completion_claim_allowed"])
        self.assertFalse((run_dir / "rendered").exists())
        self.assertFalse((run_dir / "rendered_review").exists())

    def test_cross_chunk_tex_boundary_uses_fragment_validation_then_full_check(self) -> None:
        source, run_dir, unit = self.prepare(
            "\\begin{document}\n"
            "\\begin{abstract}\n"
            "值得注意的是，结论保持不变。\n"
            "\\end{abstract}\n\n"
            "\\section{下一节}\n"
            "下一节正文保持不变。\n"
            "\\end{document}\n"
        )
        source_text = source.read_text(encoding="utf-8")
        chunks = [
            json.loads(path.read_text(encoding="utf-8"))
            for path in (run_dir / "chunks").glob("*.json")
        ]
        unit = next(
            item
            for item in chunks
            if item["status"] == "PENDING"
            and "\\begin{document}"
            in source_text[int(item["start"]):int(item["end"])]
        )
        original = source_text[int(unit["start"]):int(unit["end"])]
        self.assertIn("\\begin{document}", original)
        self.assertNotIn("\\end{document}", original)
        rewrites = self.rewrite_dir()
        masked = unit["masked_text"].replace("值得注意的是，", "")
        (rewrites / f"{unit['unit_id']}.json").write_text(
            json.dumps(
                self.voice_bound_bundle(
                    unit,
                    {"decision": "REWRITE", "masked_text": masked},
                ),
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

        result = finalizer.finalize(run_dir, rewrites)
        ledger = {
            row["unit_id"]: row for row in self.final_ledger(run_dir)
        }
        validation = json.loads(
            (run_dir / "validation" / f"{unit['unit_id']}.validation.json").read_text(
                encoding="utf-8"
            )
        )

        self.assertEqual("DONE", ledger[unit["unit_id"]]["status"])
        self.assertEqual("REVIEW", validation["status"])
        self.assertEqual("PASS", validation["mechanical_validation_status"])
        self.assertEqual(
            "PENDING_EXTERNAL_REVIEW", validation["paired_quality_review_status"]
        )
        self.assertEqual("FRAGMENT", validation["evidence"]["document_scope"])
        self.assertEqual([], result["full_format_errors"])
        self.assertEqual("REVIEW", result["status"])

    def test_utf8_bom_rewrite_bundle_is_accepted(self) -> None:
        source, run_dir, unit = self.prepare(
            "\\section{例题}\n值得注意的是，函数 $f(x)=x^2$ 在此处连续。\n"
        )
        rewrites = self.rewrite_dir()
        payload = json.dumps(
            self.voice_bound_bundle(
                unit,
                {
                    "decision": "REWRITE",
                    "masked_text": unit["masked_text"].replace("值得注意的是，", ""),
                },
            ),
            ensure_ascii=False,
        )
        (rewrites / f"{unit['unit_id']}.json").write_text(payload, encoding="utf-8-sig")

        result = finalizer.finalize(run_dir, rewrites)

        self.assert_paired_quality_review_candidate(result)
        rendered = next((run_dir / "rendered_review").rglob("*.tex")).read_text(
            encoding="utf-8"
        )
        self.assertIn("$f(x)=x^2$", rendered)
        self.assertNotIn("值得注意的是", rendered)

    def test_rewrite_bundle_cannot_be_renamed_across_units(self) -> None:
        source = self.root / "replay.tex"
        source.write_text(
            "\\section{甲}\n甲段保持简洁。\n\n\\section{乙}\n乙段保持简洁。\n",
            encoding="utf-8",
        )
        run_dir = self.root / "replay-run"
        preparer.prepare([source], run_dir, scene="COURSE", min_author_chars=0)
        pending = sorted(
            (
                json.loads(path.read_text(encoding="utf-8"))
                for path in (run_dir / "chunks").glob("*.json")
                if json.loads(path.read_text(encoding="utf-8"))["status"] == "PENDING"
            ),
            key=lambda item: item["start"],
        )
        self.assertGreaterEqual(len(pending), 2)
        first, second = pending[:2]
        rewrites = self.rewrite_dir()
        replayed = self.voice_bound_bundle(
            first,
            {"decision": "NO_CHANGE", "reason": "该段保持原有自然表达"},
        )
        (rewrites / f"{second['unit_id']}.json").write_text(
            json.dumps(replayed, ensure_ascii=False), encoding="utf-8"
        )

        result = finalizer.finalize(run_dir, rewrites)
        ledger = {row["unit_id"]: row for row in self.final_ledger(run_dir)}
        self.assertEqual("REVIEW", result["status"])
        self.assertEqual("REVIEW", result["rewrite_binding_status"])
        self.assertEqual("UNRESOLVED", ledger[second["unit_id"]]["status"])
        self.assertIn("bundle_unit_id_mismatch", ledger[second["unit_id"]]["notes"])
        self.assertEqual("PENDING", ledger[first["unit_id"]]["status"])

    def test_wrong_chunk_binding_hash_is_rejected_before_text_validation(self) -> None:
        _, run_dir, unit = self.prepare("\\section{例题}\n该段保持简洁。\n")
        rewrites = self.rewrite_dir()
        payload = self.voice_bound_bundle(
            unit,
            {"decision": "NO_CHANGE", "reason": "该段保持原有自然表达"},
        )
        payload["chunk_binding_sha256"] = "f" * 64
        (rewrites / f"{unit['unit_id']}.json").write_text(
            json.dumps(payload, ensure_ascii=False), encoding="utf-8"
        )

        result = finalizer.finalize(run_dir, rewrites)
        row = next(item for item in self.final_ledger(run_dir) if item["unit_id"] == unit["unit_id"])
        self.assertEqual("REVIEW", result["rewrite_binding_status"])
        self.assertEqual(1, result["rewrite_bindings_mismatched"])
        self.assertEqual("UNRESOLVED", row["status"])
        self.assertIn("chunk_binding_hash_mismatch", row["notes"])

    def test_authorized_tex_style_wrapper_can_be_removed_without_losing_text(self) -> None:
        source = self.root / "main.tex"
        source.write_text(
            "\\section{结果}\n普通说明与\\textbf{装饰性强调}并列。\n",
            encoding="utf-8",
        )
        run_dir = self.root / "run"
        preparer.prepare(
            [source],
            run_dir,
            scene="GENERAL",
            min_author_chars=0,
            editable_style_wrappers=["textbf"],
        )
        unit = next(
            json.loads(path.read_text(encoding="utf-8"))
            for path in (run_dir / "chunks").glob("*.json")
            if json.loads(path.read_text(encoding="utf-8"))["status"] == "PENDING"
        )
        self.assertIn(r"\textbf{装饰性强调}", unit["masked_text"])

        rewrites = self.rewrite_dir()
        rewritten = unit["masked_text"].replace(r"\textbf{装饰性强调}", "装饰性强调")
        (rewrites / f"{unit['unit_id']}.json").write_text(
            json.dumps(
                self.voice_bound_bundle(unit, {"decision": "REWRITE", "masked_text": rewritten}),
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        result = finalizer.finalize(run_dir, rewrites)

        self.assert_paired_quality_review_candidate(result)
        rendered = next((run_dir / "rendered_review").rglob("*.tex")).read_text(
            encoding="utf-8"
        )
        self.assertNotIn(r"\textbf", rendered)
        self.assertIn("装饰性强调", rendered)
        self.assertIn(r"\textbf{装饰性强调}", source.read_text(encoding="utf-8"))

    def test_missing_placeholder_rejects_unit_atomically(self) -> None:
        _, run_dir, unit = self.prepare("\\section{例题}\n文字与 $x=1$ 同时出现。\n")
        rewrites = self.rewrite_dir()
        masked = re_placeholder = unit["masked_text"]
        import re

        masked = re.sub(r"\[\[PROTECTED:[^\]]+\]\]", "", re_placeholder, count=1)
        (rewrites / f"{unit['unit_id']}.json").write_text(
            json.dumps(
                self.voice_bound_bundle(unit, {"decision": "REWRITE", "masked_text": masked}),
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        result = finalizer.finalize(run_dir, rewrites)
        row = next(item for item in self.final_ledger(run_dir) if item["unit_id"] == unit["unit_id"])
        self.assertEqual("REVIEW", result["status"])
        self.assertEqual("UNRESOLVED", row["status"])
        self.assertEqual("FAIL", row["protected_hashes_ok"])

    def test_no_change_requires_specific_reason(self) -> None:
        _, run_dir, unit = self.prepare("\\section{定义}\n该定义保持平行结构。\n")
        rewrites = self.rewrite_dir()
        bundle_path = rewrites / f"{unit['unit_id']}.json"
        bundle_path.write_text(
            json.dumps(
                self.voice_bound_bundle(unit, {"decision": "NO_CHANGE", "reason": "短"}),
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        result = finalizer.finalize(run_dir, rewrites)
        self.assertEqual("REVIEW", result["status"])
        row = next(item for item in self.final_ledger(run_dir) if item["unit_id"] == unit["unit_id"])
        self.assertEqual("UNRESOLVED", row["status"])

    def test_no_change_with_high_signal_requires_specific_keep_reason(self) -> None:
        _, run_dir, unit = self.prepare("\\section{提示}\n这条规则必须牢记。\n")
        rewrites = self.rewrite_dir()
        bundle = rewrites / f"{unit['unit_id']}.json"
        bundle.write_text(
            json.dumps(
                self.voice_bound_bundle(
                    unit,
                    {"decision": "NO_CHANGE", "reason": "用户明确锁定这条教学原句"},
                ),
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        rejected = finalizer.finalize(run_dir, rewrites)
        self.assertEqual("REVIEW", rejected["status"])
        row = next(item for item in self.final_ledger(run_dir) if item["unit_id"] == unit["unit_id"])
        self.assertEqual("UNRESOLVED", row["status"])

        bundle.write_text(
            json.dumps(
                self.voice_bound_bundle(
                    unit,
                    {
                        "decision": "NO_CHANGE",
                        "reason": "用户明确锁定这条教学原句",
                        "keep_reasons": {"LEX-COACH-01": "用户明确锁定的直接教学提醒"},
                    },
                ),
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        accepted = finalizer.finalize(run_dir, rewrites)
        self.assert_paired_quality_review_candidate(accepted)
        row = next(item for item in self.final_ledger(run_dir) if item["unit_id"] == unit["unit_id"])
        self.assertEqual("NO_CHANGE", row["status"])

    def test_mismatched_warning_proposal_keeps_unit_unresolved(self) -> None:
        source_text = "\\section{结果}\n结果可能变化。\n"
        _, run_dir, unit = self.prepare(source_text)
        rewrites = self.rewrite_dir()
        bundle = self.voice_bound_bundle(
            unit,
            {
                "decision": "REWRITE",
                "masked_text": unit["masked_text"].replace("结果可能变化", "结果发生变化"),
                **self.warning_proposal_fields(
                    source_text[int(unit["start"]):int(unit["end"])],
                    source_text[int(unit["start"]):int(unit["end"])].replace(
                        "结果可能变化", "结果发生变化"
                    ),
                ),
            },
        )
        (rewrites / f"{unit['unit_id']}.json").write_text(
            json.dumps(bundle, ensure_ascii=False),
            encoding="utf-8",
        )

        result = finalizer.finalize(run_dir, rewrites)
        row = next(item for item in self.final_ledger(run_dir) if item["unit_id"] == unit["unit_id"])

        self.assertEqual("REVIEW", result["status"])
        self.assertEqual("UNRESOLVED", row["status"])
        self.assertIn("warning_review_request_sha256 does not match", row["notes"])
        self.assertFalse(result["full_completion_claim_allowed"])

    def test_agent_cannot_attest_long_document_warning_proposal(self) -> None:
        source_text = "\\section{结果}\n结果可能变化。\n"
        _, run_dir, unit = self.prepare(source_text)
        rewrites = self.rewrite_dir()
        bundle = self.voice_bound_bundle(
            unit,
            {
                "decision": "REWRITE",
                "masked_text": unit["masked_text"].replace("结果可能变化", "结果发生变化"),
                **self.warning_proposal_fields(
                    source_text[int(unit["start"]):int(unit["end"])],
                    source_text[int(unit["start"]):int(unit["end"])].replace(
                        "结果可能变化", "结果发生变化"
                    ),
                ),
                "warning_review": {
                    "reviewer_kind": "AGENT",
                    "reviewer_id": "forward-agent",
                },
            },
        )
        (rewrites / f"{unit['unit_id']}.json").write_text(
            json.dumps(bundle, ensure_ascii=False),
            encoding="utf-8",
        )

        result = finalizer.finalize(run_dir, rewrites)
        row = next(item for item in self.final_ledger(run_dir) if item["unit_id"] == unit["unit_id"])

        self.assertEqual("REVIEW", result["status"])
        self.assertEqual("UNRESOLVED", row["status"])
        self.assertIn("warning_reviewer_identity_metadata_retired", row["notes"])
        self.assertNotEqual("PASS", row["style_validation"])

    def test_identity_free_proposal_is_recorded_but_cannot_complete_unit(self) -> None:
        source_text = "\\section{结果}\n结果可能变化。\n"
        _, run_dir, unit = self.prepare(source_text)
        rewrites = self.rewrite_dir()
        bundle = self.voice_bound_bundle(
            unit,
            {
                "decision": "REWRITE",
                "masked_text": unit["masked_text"].replace("结果可能变化", "结果发生变化"),
            },
        )
        bundle_path = rewrites / f"{unit['unit_id']}.json"
        bundle_path.write_text(
            json.dumps(bundle, ensure_ascii=False),
            encoding="utf-8",
        )

        initial_result = finalizer.finalize(run_dir, rewrites)
        initial_validation = json.loads(
            (run_dir / "validation" / f"{unit['unit_id']}.validation.json").read_text(
                encoding="utf-8"
            )
        )
        request = initial_validation["warning_review_request"]
        bundle.update(
            {
                "warning_resolutions": {
                    request["warnings"][0]["warning_fingerprint"]:
                        "人工建议核对删除的是重复缓和而非结论强度",
                },
                "warning_review_request_sha256": request["request_sha256"],
            }
        )
        bundle_path.write_text(json.dumps(bundle, ensure_ascii=False), encoding="utf-8")

        result = finalizer.finalize(run_dir, rewrites)
        row = next(item for item in self.final_ledger(run_dir) if item["unit_id"] == unit["unit_id"])
        validation = json.loads(
            (run_dir / "validation" / f"{unit['unit_id']}.validation.json").read_text(encoding="utf-8")
        )
        proposal = validation["warning_proposal_state"]

        self.assertEqual("REVIEW", initial_result["status"])
        self.assertEqual("REVIEW", result["status"])
        self.assertEqual("UNRESOLVED", row["status"])
        self.assertEqual("UNVERIFIED_CALLER_PROPOSAL", proposal["proposal_source"])
        self.assertFalse(proposal["reviewer_identifier_collected"])
        self.assertFalse(proposal["identity_verified"])
        self.assertFalse(proposal["review_clearance_granted"])
        self.assertNotIn("reviewer_id_sha256", json.dumps(validation, ensure_ascii=False))
        self.assertNotIn("warning_review", validation)

    def test_warning_review_metadata_without_resolution_is_unresolved(self) -> None:
        _, run_dir, unit = self.prepare(
            "\\section{例题}\n值得注意的是，函数 $f(x)=x^2$ 在此处连续。\n"
        )
        rewrites = self.rewrite_dir()
        bundle = self.voice_bound_bundle(
            unit,
            {
                "decision": "REWRITE",
                "masked_text": unit["masked_text"].replace("值得注意的是，", ""),
                "warning_review": {
                    "reviewer_kind": "HUMAN",
                    "reviewer_id": "external-reviewer",
                },
            },
        )
        (rewrites / f"{unit['unit_id']}.json").write_text(
            json.dumps(bundle, ensure_ascii=False),
            encoding="utf-8",
        )

        result = finalizer.finalize(run_dir, rewrites)
        row = next(item for item in self.final_ledger(run_dir) if item["unit_id"] == unit["unit_id"])

        self.assertEqual("REVIEW", result["status"])
        self.assertEqual("UNRESOLVED", row["status"])
        self.assertIn("warning_reviewer_identity_metadata_retired", row["notes"])
        self.assertFalse(result["full_completion_claim_allowed"])

    def test_all_warning_reviewer_ids_are_retired(self) -> None:
        for index, reviewer_id in enumerate(("ab", "x" * 129)):
            with self.subTest(reviewer_id_length=len(reviewer_id)):
                root = self.root / f"case-{index}"
                root.mkdir()
                source = root / "main.tex"
                source.write_text("\\section{结果}\n结果可能变化。\n", encoding="utf-8")
                run_dir = root / "run"
                preparer.prepare([source], run_dir, scene="COURSE", min_author_chars=0)
                unit = next(
                    json.loads(path.read_text(encoding="utf-8"))
                    for path in (run_dir / "chunks").glob("*.json")
                    if json.loads(path.read_text(encoding="utf-8"))["status"] == "PENDING"
                )
                rewrites = root / "rewrites"
                rewrites.mkdir()
                source_text = "\\section{结果}\n结果可能变化。\n"
                proposal = self.warning_proposal_fields(
                    source_text[int(unit["start"]):int(unit["end"])],
                    source_text[int(unit["start"]):int(unit["end"])].replace(
                        "结果可能变化", "结果发生变化"
                    ),
                )
                (rewrites / f"{unit['unit_id']}.json").write_text(
                    json.dumps(
                        self.voice_bound_bundle(
                            unit,
                            {
                                "decision": "REWRITE",
                                "masked_text": unit["masked_text"].replace("结果可能变化", "结果发生变化"),
                                **proposal,
                                "warning_review": {
                                    "reviewer_kind": "HUMAN",
                                    "reviewer_id": reviewer_id,
                                },
                            },
                        ),
                        ensure_ascii=False,
                    ),
                    encoding="utf-8",
                )

                result = finalizer.finalize(run_dir, rewrites)
                with (run_dir / "coverage_ledger.final.csv").open(
                    "r", encoding="utf-8-sig", newline=""
                ) as handle:
                    row = next(
                        item for item in csv.DictReader(handle) if item["unit_id"] == unit["unit_id"]
                    )

                self.assertEqual("REVIEW", result["status"])
                self.assertEqual("UNRESOLVED", row["status"])
                self.assertIn("warning_reviewer_identity_metadata_retired", row["notes"])

    def test_legacy_acceptance_and_authority_field_injection_are_unresolved(self) -> None:
        _, run_dir, unit = self.prepare("\\section{结果}\n结果可能变化。\n")
        rewrites = self.rewrite_dir()
        path = rewrites / f"{unit['unit_id']}.json"
        path.write_text(
            json.dumps(
                self.voice_bound_bundle(
                    unit,
                    {
                        "decision": "REWRITE",
                        "masked_text": unit["masked_text"].replace("结果可能变化", "结果发生变化"),
                        "accepted_warnings": {},
                        "status": "PASS",
                        "identity_verified": True,
                    },
                ),
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

        result = finalizer.finalize(run_dir, rewrites)
        row = next(item for item in self.final_ledger(run_dir) if item["unit_id"] == unit["unit_id"])
        self.assertEqual("REVIEW", result["status"])
        self.assertEqual("UNRESOLVED", row["status"])
        self.assertIn("unknown_rewrite_bundle_fields", row["notes"])

    def test_incomplete_rewrites_leave_pending_and_forbid_completion_claim(self) -> None:
        source = self.root / "main.tex"
        source.write_text("\\section{一}\n第一段。\n\\section{二}\n第二段。\n", encoding="utf-8")
        run_dir = self.root / "run"
        preparer.prepare([source], run_dir, min_author_chars=0)
        rewrites = self.rewrite_dir()
        result = finalizer.finalize(run_dir, rewrites)
        self.assertEqual("REVIEW", result["status"])
        self.assertFalse(result["full_completion_claim_allowed"])
        self.assertGreater(result["unit_statuses"].get("PENDING", 0), 0)
        self.assertTrue((run_dir / "rendered_partial").is_dir())

    def test_tampered_units_ledger_cannot_forge_full_completion(self) -> None:
        _, run_dir, unit = self.prepare("\\section{定义}\n该定义保持平行结构。\n")
        units_path = run_dir / "units.jsonl"
        rows = [json.loads(line) for line in units_path.read_text(encoding="utf-8").splitlines() if line.strip()]
        target = next(row for row in rows if row["unit_id"] == unit["unit_id"])
        target.update({
            "status": "DONE",
            "hash_after": target["hash_before"],
            "style_validation": "PASS",
            "protected_hashes_ok": "PASS",
        })
        units_path.write_text(
            "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows),
            encoding="utf-8",
        )

        with self.assertRaisesRegex(ValueError, "(?:prepare|integrity) artifact .*mismatch"):
            finalizer.finalize(run_dir, self.rewrite_dir())

        self.assertFalse((run_dir / "rendered").exists())

    def test_tampered_units_and_forged_integrity_manifest_still_fail_rebuild(self) -> None:
        _, run_dir, unit = self.prepare("\\section{定义}\n该定义保持平行结构。\n")
        units_path = run_dir / "units.jsonl"
        rows = [json.loads(line) for line in units_path.read_text(encoding="utf-8").splitlines() if line.strip()]
        target = next(row for row in rows if row["unit_id"] == unit["unit_id"])
        target["status"] = "DONE"
        target["hash_after"] = target["hash_before"]
        units_path.write_text(
            "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows),
            encoding="utf-8",
        )
        forged = preparer.build_integrity_manifest(run_dir)
        (run_dir / "prepare_integrity.json").write_text(
            json.dumps(forged, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        with self.assertRaisesRegex(ValueError, "initial prepare state mismatch"):
            finalizer.finalize(run_dir, self.rewrite_dir())

        self.assertFalse((run_dir / "rendered").exists())

    def test_empty_prepare_scope_cannot_claim_full_completion(self) -> None:
        empty = self.root / "empty"
        empty.mkdir()
        run_dir = self.root / "run"
        preparer.prepare([empty], run_dir, scene="COURSE", min_author_chars=0)

        result = finalizer.finalize(run_dir, self.rewrite_dir())

        self.assertEqual("REVIEW", result["status"])
        self.assertFalse(result["full_completion_claim_allowed"])
        self.assertTrue(result["empty_processable_scope"])
        self.assertFalse((run_dir / "rendered").exists())

    def test_concurrent_finalize_same_run_is_serialized(self) -> None:
        source, run_dir, unit = self.prepare("\\section{定义}\n该定义保持平行结构。\n")
        rewrites = self.rewrite_dir()
        (rewrites / f"{unit['unit_id']}.json").write_text(
            json.dumps(
                self.voice_bound_bundle(
                    unit,
                    {"decision": "NO_CHANGE", "reason": "正式定义保持原有平行结构"},
                ),
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            results = list(executor.map(lambda _: finalizer.finalize(run_dir, rewrites), range(2)))

        self.assertEqual(["REVIEW", "REVIEW"], [result["status"] for result in results])
        for result in results:
            self.assert_paired_quality_review_candidate(result)
        self.assertEqual(
            ["NOT_RUN", "PASS"],
            sorted(result["idempotency"] for result in results),
        )
        self.assertFalse((run_dir / "rendered").exists())
        self.assertTrue((run_dir / "rendered_review").is_dir())

    def test_tampered_units_and_self_resealed_integrity_cannot_forge_completion(self) -> None:
        source = self.root / "main.md"
        source.write_text(
            "## \u6807\u9898\n"
            "\u8fd9\u662f\u4e00\u6bb5\u8db3\u591f\u957f\u7684\u4e2d\u6587\u6b63\u6587\uff0c"
            "\u7528\u4e8e\u9a8c\u8bc1\u521d\u59cb\u72b6\u6001\u4e0d\u80fd\u88ab\u4f2a\u9020\u3002\n",
            encoding="utf-8",
        )
        run_dir = self.root / "run"
        preparer.prepare([source], run_dir, scene="GENERAL", min_author_chars=0)

        units_path = run_dir / "units.jsonl"
        rows = [json.loads(line) for line in units_path.read_text(encoding="utf-8").splitlines() if line.strip()]
        target = next(row for row in rows if row["status"] == "PENDING")
        target.update(
            {
                "status": "SKIPPED_PROTECTED",
                "hash_after": "",
                "style_validation": "NOT_RUN",
                "protected_hashes_ok": "NOT_RUN",
            }
        )
        units_path.write_text(
            "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows),
            encoding="utf-8",
        )

        # Model an attacker who also rewrites the self-reported integrity
        # manifest after changing the mutable units ledger.
        integrity_path = run_dir / "prepare_integrity.json"
        integrity = json.loads(integrity_path.read_text(encoding="utf-8"))
        for artifact in integrity["artifacts"]:
            artifact_path = run_dir / artifact["path"]
            artifact["sha256"] = hashlib.sha256(artifact_path.read_bytes()).hexdigest()
            artifact["bytes"] = artifact_path.stat().st_size
        integrity_path.write_text(
            json.dumps(integrity, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

        with self.assertRaisesRegex(ValueError, "initial prepare state mismatch|canonical chunk"):
            finalizer.finalize(run_dir, self.rewrite_dir())
        self.assertFalse((run_dir / "rendered").exists())

    def test_tampered_prepare_completion_metadata_cannot_pass_after_local_reseal(self) -> None:
        _, run_dir, unit = self.prepare("\\section{定义}\n该定义保持原有平行结构。\n")
        metadata_path = run_dir / "run_metadata.json"
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        metadata.update(
            {
                "status": "PASS",
                "completion_claim_allowed": True,
                "processable_editable_units": 0,
                "no_editable_scope": True,
                "unit_statuses": {"DONE": 999},
            }
        )
        metadata_path.write_text(
            json.dumps(metadata, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        (run_dir / "prepare_integrity.json").write_text(
            json.dumps(
                preparer.build_integrity_manifest(run_dir),
                ensure_ascii=False,
                indent=2,
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )
        rewrites = self.rewrite_dir()
        (rewrites / f"{unit['unit_id']}.json").write_text(
            json.dumps(
                self.voice_bound_bundle(
                    unit,
                    {"decision": "NO_CHANGE", "reason": "正式定义保留平行结构"},
                ),
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

        with self.assertRaisesRegex(ValueError, "run metadata derived fields mismatch"):
            finalizer.finalize(run_dir, rewrites)
        self.assertFalse((run_dir / "rendered").exists())

    def test_resealed_frozen_routing_policy_cannot_replace_current_policy(self) -> None:
        _, run_dir, unit = self.prepare("\\section{例题}\n本题先判断方向。\n")
        policy_path = run_dir / "scene_routing_policy.json"
        policy = json.loads(policy_path.read_text(encoding="utf-8"))
        policy["purpose"] = "attacker supplied replacement policy"
        policy_path.write_text(
            json.dumps(policy, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        _, forged_sha = preparer.scene_router.load_policy(policy_path)
        metadata_path = run_dir / "run_metadata.json"
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        metadata["scene_routing_policy_sha256"] = forged_sha
        metadata_path.write_text(
            json.dumps(metadata, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        (run_dir / "prepare_integrity.json").write_text(
            json.dumps(
                preparer.build_integrity_manifest(run_dir),
                ensure_ascii=False,
                indent=2,
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )
        rewrites = self.rewrite_dir()
        (rewrites / f"{unit['unit_id']}.json").write_text(
            json.dumps(
                self.voice_bound_bundle(
                    unit,
                    {"decision": "NO_CHANGE", "reason": "题解表达已经直接"},
                ),
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

        with self.assertRaisesRegex(ValueError, "policy changed after prepare"):
            finalizer.finalize(run_dir, rewrites)

    def test_resealed_unit_route_voice_ledger_and_chunk_forgery_fails_source_rebuild(self) -> None:
        _, run_dir, unit = self.prepare("\\section{例题}\n本题先判断方向。\n")
        units_path = run_dir / "units.jsonl"
        units = [
            json.loads(line)
            for line in units_path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        target = next(item for item in units if item["unit_id"] == unit["unit_id"])
        target["scene"] = "RESEARCH"
        target["scene_routing_decision"] = "ROUTED"
        target["voice_profile_binding_scene"] = "RESEARCH"
        target["voice_profile_sha256"] = "f" * 64
        units_path.write_text(
            "".join(
                json.dumps(item, ensure_ascii=False, sort_keys=True) + "\n"
                for item in units
            ),
            encoding="utf-8",
        )
        chunk_path = run_dir / "chunks" / f"{unit['unit_id']}.json"
        chunk = json.loads(chunk_path.read_text(encoding="utf-8"))
        chunk.update(
            {
                "scene": "RESEARCH",
                "scene_routing_decision": "ROUTED",
                "voice_profile_binding_scene": "RESEARCH",
                "voice_profile_sha256": "f" * 64,
            }
        )
        chunk["chunk_binding_sha256"] = preparer.chunk_binding_sha256(chunk)
        chunk_path.write_text(
            json.dumps(chunk, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        target["chunk_binding_sha256"] = chunk["chunk_binding_sha256"]
        units_path.write_text(
            "".join(
                json.dumps(item, ensure_ascii=False, sort_keys=True) + "\n"
                for item in units
            ),
            encoding="utf-8",
        )
        ledger_path = run_dir / "coverage_ledger.csv"
        with ledger_path.open("r", encoding="utf-8-sig", newline="") as handle:
            rows = list(csv.DictReader(handle))
            fields = list(rows[0])
        for row in rows:
            if row["unit_id"] == unit["unit_id"]:
                row.update(
                    {
                        "scene": "RESEARCH",
                        "scene_routing_decision": "ROUTED",
                        "voice_profile_binding_scene": "RESEARCH",
                        "voice_profile_sha256": "f" * 64,
                        "chunk_binding_sha256": chunk["chunk_binding_sha256"],
                    }
                )
        with ledger_path.open("w", encoding="utf-8-sig", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)
        (run_dir / "prepare_integrity.json").write_text(
            json.dumps(
                preparer.build_integrity_manifest(run_dir),
                ensure_ascii=False,
                indent=2,
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )

        with self.assertRaisesRegex(ValueError, "voice binding unit mismatch|initial prepare state mismatch"):
            finalizer.finalize(run_dir, self.rewrite_dir())

    def test_tampered_chunk_cannot_forge_prepare_integrity(self) -> None:
        _, run_dir, unit = self.prepare("\\section{定义}\n该定义保持平行结构。\n")
        chunk_path = run_dir / "chunks" / f"{unit['unit_id']}.json"
        payload = json.loads(chunk_path.read_text(encoding="utf-8"))
        payload["status"] = "DONE"
        chunk_path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")

        with self.assertRaisesRegex(ValueError, "(?:prepare|integrity) artifact .*mismatch"):
            finalizer.finalize(run_dir, self.rewrite_dir())

    def test_missing_prepare_integrity_refuses_finalize(self) -> None:
        _, run_dir, _ = self.prepare("\\section{定义}\n该定义保持平行结构。\n")
        (run_dir / "prepare_integrity.json").unlink()

        with self.assertRaisesRegex(ValueError, "missing prepare_integrity.json"):
            finalizer.finalize(run_dir, self.rewrite_dir())

        self.assertFalse((run_dir / "rendered").exists())

    def test_repeat_with_same_output_is_idempotent(self) -> None:
        _, run_dir, unit = self.prepare("\\section{定义}\n该定义保持平行结构。\n")
        rewrites = self.rewrite_dir()
        (rewrites / f"{unit['unit_id']}.json").write_text(
            json.dumps(
                self.voice_bound_bundle(
                    unit,
                    {"decision": "NO_CHANGE", "reason": "正式定义保持原有平行结构"},
                ),
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        first = finalizer.finalize(run_dir, rewrites)
        second = finalizer.finalize(run_dir, rewrites)
        self.assert_paired_quality_review_candidate(first)
        self.assert_paired_quality_review_candidate(second)
        self.assertEqual("PASS", second["idempotency"])

    def test_compile_failure_keeps_source_and_does_not_publish_rendered(self) -> None:
        source, run_dir, unit = self.prepare("\\section{定义}\n该定义保持平行结构。\n")
        rewrites = self.rewrite_dir()
        (rewrites / f"{unit['unit_id']}.json").write_text(
            json.dumps(
                self.voice_bound_bundle(
                    unit,
                    {"decision": "NO_CHANGE", "reason": "正式定义保持原有平行结构"},
                ),
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        command = f'"{sys.executable}" -c "raise SystemExit(7)"'
        result = finalizer.finalize(run_dir, rewrites, check_command=command)
        self.assertEqual("FAIL", result["status"])
        self.assert_compile_check_schema(result["compile_check"])
        self.assertEqual(7, result["compile_check"]["exit_code"])
        self.assertEqual("PASS", result["compile_check"]["integrity_status"])
        self.assertEqual({}, result["compile_check"]["integrity_changes"])
        self.assertFalse((run_dir / "rendered").exists())
        self.assertTrue((run_dir / "failed_staging").is_dir())
        self.assertEqual("\\section{定义}\n该定义保持平行结构。\n", source.read_text(encoding="utf-8"))

    def test_progressive_partial_run_publishes_review_candidate_without_formal_output(self) -> None:
        source = self.root / "main.tex"
        source.write_text("\\section{一}\n第一段。\n\\section{二}\n第二段。\n", encoding="utf-8")
        run_dir = self.root / "run"
        preparer.prepare([source], run_dir, min_author_chars=0)
        chunks = [json.loads(path.read_text(encoding="utf-8")) for path in (run_dir / "chunks").glob("*.json")]
        pending = [item for item in chunks if item["status"] == "PENDING"]
        rewrites = self.rewrite_dir()
        first = pending[0]
        (rewrites / f"{first['unit_id']}.json").write_text(
            json.dumps(
                self.voice_bound_bundle(
                    first,
                    {"decision": "NO_CHANGE", "reason": "该段属于自然简短陈述"},
                ),
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        result_one = finalizer.finalize(run_dir, rewrites)
        self.assertEqual("REVIEW", result_one["status"])
        self.assertTrue((run_dir / "rendered_partial").is_dir())
        second = pending[1]
        (rewrites / f"{second['unit_id']}.json").write_text(
            json.dumps(
                self.voice_bound_bundle(
                    second,
                    {"decision": "NO_CHANGE", "reason": "该段属于自然简短陈述"},
                ),
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        result_two = finalizer.finalize(run_dir, rewrites)
        self.assert_paired_quality_review_candidate(result_two)
        self.assertFalse((run_dir / "rendered").exists())
        self.assertTrue((run_dir / "rendered_review").is_dir())
        self.assertFalse((run_dir / "rendered_partial").exists())
        self.assertEqual(
            (run_dir / "rendered_review").resolve(),
            Path(result_two["published_path"]).resolve(),
        )
        history = [
            json.loads(line)
            for line in (run_dir / "partial_history.jsonl")
            .read_text(encoding="utf-8")
            .splitlines()
        ]
        self.assertEqual("full_review_candidate_published", history[-1]["reason"])
        self.assertTrue(history[-1]["old_hashes"])
        self.assertTrue(history[-1]["new_hashes"])

    def test_file_level_garbled_gap_blocks_full_completion(self) -> None:
        main = self.root / "main.tex"
        bad = self.root / "bad.tex"
        main.write_text("\\input{bad}\n", encoding="utf-8")
        bad.write_bytes(b"\x81\x30\xff\xff\x81")
        run_dir = self.root / "run"
        preparer.prepare([main], run_dir, min_author_chars=0)
        rewrites = self.rewrite_dir()
        result = finalizer.finalize(run_dir, rewrites)
        self.assertEqual("REVIEW", result["status"])
        self.assertFalse(result["full_completion_claim_allowed"])
        self.assertEqual(1, result["file_statuses"].get("SKIPPED_GARBLED", 0))
        self.assertTrue((run_dir / "rendered_partial").is_dir())

    def test_dynamic_include_gap_blocks_full_completion(self) -> None:
        main = self.root / "main.tex"
        chapter_dir = self.root / "chapters"
        chapter_dir.mkdir()
        (chapter_dir / "chapter.tex").write_text("\\section{章节}\n章节正文。\n", encoding="utf-8")
        main.write_text(
            "\\newcommand{\\chapterdir}{chapters}\n"
            "\\input{\\chapterdir/chapter}\n"
            "主文件正文。\n",
            encoding="utf-8",
        )
        run_dir = self.root / "run"
        preparer.prepare([main], run_dir, min_author_chars=0)
        rewrites = self.rewrite_dir()
        for path in (run_dir / "chunks").glob("*.json"):
            unit = json.loads(path.read_text(encoding="utf-8"))
            if unit["status"] == "PENDING":
                (rewrites / f"{unit['unit_id']}.json").write_text(
                    json.dumps(
                        self.voice_bound_bundle(
                            unit,
                            {"decision": "NO_CHANGE", "reason": "该段保持原有自然表达"},
                        ),
                        ensure_ascii=False,
                    ),
                    encoding="utf-8",
                )

        result = finalizer.finalize(run_dir, rewrites)

        self.assertEqual("REVIEW", result["status"])
        self.assertFalse(result["full_completion_claim_allowed"])
        self.assertEqual(1, result["file_statuses"].get("UNRESOLVED_INCLUDE", 0))

    def test_source_change_after_snapshot_is_rechecked_at_finalize(self) -> None:
        source, run_dir, unit = self.prepare("\\section{定义}\n该定义保持平行结构。\n")
        rewrites = self.rewrite_dir()
        (rewrites / f"{unit['unit_id']}.json").write_text(
            json.dumps(
                self.voice_bound_bundle(
                    unit,
                    {"decision": "NO_CHANGE", "reason": "正式定义保持原有平行结构"},
                ),
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        source.write_text(source.read_text(encoding="utf-8") + "% external append\n", encoding="utf-8")
        result = finalizer.finalize(run_dir, rewrites)
        self.assertEqual("REVIEW", result["status"])
        self.assertFalse(result["full_completion_claim_allowed"])
        self.assertEqual(1, result["source_files_changed_since_snapshot"])
        self.assertTrue((run_dir / "rendered_partial").is_dir())

    def test_source_deleted_after_snapshot_blocks_full_completion(self) -> None:
        source, run_dir, unit = self.prepare("\\section{背景}\n本段保持原有自然表达。\n")
        rewrites = self.rewrite_dir()
        (rewrites / f"{unit['unit_id']}.json").write_text(
            json.dumps(
                self.voice_bound_bundle(
                    unit,
                    {"decision": "NO_CHANGE", "reason": "该段保持原有自然表达"},
                ),
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        source.unlink()

        result = finalizer.finalize(run_dir, rewrites)

        self.assertEqual("REVIEW", result["status"])
        self.assertFalse(result["full_completion_claim_allowed"])
        self.assertEqual(1, result["source_files_changed_since_snapshot"])
        self.assertEqual("MISSING", result["source_change_details"][0]["current_state"])
        self.assertFalse((run_dir / "rendered").exists())

    def test_source_replaced_by_directory_blocks_full_completion(self) -> None:
        source, run_dir, unit = self.prepare("\\section{背景}\n本段保持原有自然表达。\n")
        rewrites = self.rewrite_dir()
        (rewrites / f"{unit['unit_id']}.json").write_text(
            json.dumps(
                self.voice_bound_bundle(
                    unit,
                    {"decision": "NO_CHANGE", "reason": "该段保持原有自然表达"},
                ),
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        source.unlink()
        source.mkdir()

        result = finalizer.finalize(run_dir, rewrites)

        self.assertEqual("REVIEW", result["status"])
        self.assertFalse(result["full_completion_claim_allowed"])
        self.assertEqual(1, result["source_files_changed_since_snapshot"])
        self.assertEqual("NOT_FILE", result["source_change_details"][0]["current_state"])
        self.assertFalse((run_dir / "rendered").exists())

    def test_copying_read_only_adjacent_context_is_rejected(self) -> None:
        source = self.root / "main.md"
        source.write_text(
            "# 甲节\n甲段文字保持简洁。\n\n# 乙节\n乙段文字保持简洁。\n",
            encoding="utf-8",
        )
        run_dir = self.root / "run"
        preparer.prepare([source], run_dir, scene="GENERAL", min_author_chars=0)
        chunks = sorted(
            (json.loads(path.read_text(encoding="utf-8")) for path in (run_dir / "chunks").glob("*.json")),
            key=lambda item: item["start"],
        )
        first, second = chunks
        rewrites = self.rewrite_dir()
        (rewrites / f"{first['unit_id']}.json").write_text(
            json.dumps(
                self.voice_bound_bundle(
                    first,
                    {
                        "decision": "REWRITE",
                        "masked_text": first["masked_text"] + "\n乙段文字保持简洁。\n",
                    },
                ),
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        (rewrites / f"{second['unit_id']}.json").write_text(
            json.dumps(
                self.voice_bound_bundle(
                    second,
                    {"decision": "NO_CHANGE", "reason": "该段保持原有自然表达"},
                ),
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

        result = finalizer.finalize(run_dir, rewrites)
        row = next(item for item in self.final_ledger(run_dir) if item["unit_id"] == first["unit_id"])
        published = Path(result["published_path"])
        rendered = next(published.rglob("*.md")).read_text(encoding="utf-8")

        self.assertEqual("REVIEW", result["status"])
        self.assertFalse(result["full_completion_claim_allowed"])
        self.assertEqual("UNRESOLVED", row["status"])
        self.assertIn("read_only_context_copied", row["notes"])
        self.assertEqual(1, rendered.count("乙段文字保持简洁。"))

    def test_raw_copy_of_protected_content_is_rejected(self) -> None:
        _, run_dir, unit = self.prepare("\\section{背景}\n本段讨论对象范围。\n")
        rewrites = self.rewrite_dir()
        (rewrites / f"{unit['unit_id']}.json").write_text(
            json.dumps(
                self.voice_bound_bundle(
                    unit,
                    {
                        "decision": "REWRITE",
                        "masked_text": unit["masked_text"] + "\n\\section{背景}\n",
                    },
                ),
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

        result = finalizer.finalize(run_dir, rewrites)
        row = next(item for item in self.final_ledger(run_dir) if item["unit_id"] == unit["unit_id"])

        self.assertEqual("REVIEW", result["status"])
        self.assertFalse(result["full_completion_claim_allowed"])
        self.assertEqual("UNRESOLVED", row["status"])
        self.assertIn("protected_content_count_changed", row["notes"])

    def test_non_cumulative_partial_run_preserves_previous_partial(self) -> None:
        source = self.root / "main.md"
        source.write_text(
            "# 甲节\n值得注意的是，甲段文字自然。\n\n# 乙节\n乙段文字自然。\n",
            encoding="utf-8",
        )
        run_dir = self.root / "run"
        preparer.prepare([source], run_dir, scene="GENERAL", min_author_chars=0)
        chunks = sorted(
            (json.loads(path.read_text(encoding="utf-8")) for path in (run_dir / "chunks").glob("*.json")),
            key=lambda item: item["start"],
        )
        first, second = chunks
        first_rewrites = self.rewrite_dir()
        (first_rewrites / f"{first['unit_id']}.json").write_text(
            json.dumps(
                self.voice_bound_bundle(
                    first,
                    {
                        "decision": "REWRITE",
                        "masked_text": first["masked_text"].replace("值得注意的是，", ""),
                    },
                ),
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        first_result = finalizer.finalize(run_dir, first_rewrites)
        partial_path = next((run_dir / "rendered_partial").rglob("*.md"))
        partial_before = partial_path.read_bytes()
        evidence_before = self.evidence_snapshot(run_dir)

        second_rewrites = self.root / "rewrites-second"
        second_rewrites.mkdir()
        (second_rewrites / f"{second['unit_id']}.json").write_text(
            json.dumps(
                self.voice_bound_bundle(
                    second,
                    {"decision": "NO_CHANGE", "reason": "该段保持原有自然表达"},
                ),
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        second_result = finalizer.finalize(run_dir, second_rewrites)

        self.assertEqual("REVIEW", first_result["status"])
        self.assertEqual("FAIL", second_result["status"])
        self.assertEqual("FAIL", second_result["idempotency"])
        self.assertIn(first["unit_id"], second_result["partial_regression_units"])
        self.assertEqual(partial_before, partial_path.read_bytes())
        self.assertEqual(evidence_before, self.evidence_snapshot(run_dir))

    def test_invalid_revised_bundle_cannot_regress_previous_partial(self) -> None:
        source = self.root / "main.md"
        source.write_text(
            "# 甲节\n值得注意的是，甲段文字自然。\n\n# 乙节\n乙段文字自然。\n",
            encoding="utf-8",
        )
        run_dir = self.root / "run"
        preparer.prepare([source], run_dir, scene="GENERAL", min_author_chars=0)
        first = min(
            (json.loads(path.read_text(encoding="utf-8")) for path in (run_dir / "chunks").glob("*.json")),
            key=lambda item: item["start"],
        )
        rewrites = self.rewrite_dir()
        bundle = rewrites / f"{first['unit_id']}.json"
        bundle.write_text(
            json.dumps(
                self.voice_bound_bundle(
                    first,
                    {
                        "decision": "REWRITE",
                        "masked_text": first["masked_text"].replace("值得注意的是，", ""),
                    },
                ),
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        first_result = finalizer.finalize(run_dir, rewrites)
        partial_path = next((run_dir / "rendered_partial").rglob("*.md"))
        partial_before = partial_path.read_bytes()
        evidence_before = self.evidence_snapshot(run_dir)

        bundle.write_text(
            json.dumps(
                self.voice_bound_bundle(
                    first,
                    {"decision": "REWRITE", "masked_text": first["masked_text"]},
                ),
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        second_result = finalizer.finalize(run_dir, rewrites)

        self.assertEqual("REVIEW", first_result["status"])
        self.assertEqual("FAIL", second_result["status"])
        self.assertIn(first["unit_id"], second_result["partial_regression_units"])
        self.assertEqual(partial_before, partial_path.read_bytes())
        self.assertEqual(evidence_before, self.evidence_snapshot(run_dir))

    def test_revised_review_candidate_replaces_prior_candidate_with_history(self) -> None:
        source = self.root / "main.md"
        source.write_text("# 标题\n值得注意的是，该段文字自然。\n", encoding="utf-8")
        run_dir = self.root / "run"
        preparer.prepare([source], run_dir, scene="GENERAL", min_author_chars=0)
        unit = next(
            json.loads(path.read_text(encoding="utf-8"))
            for path in (run_dir / "chunks").glob("*.json")
            if json.loads(path.read_text(encoding="utf-8"))["status"] == "PENDING"
        )
        rewrites = self.rewrite_dir()
        bundle = rewrites / f"{unit['unit_id']}.json"
        bundle.write_text(
            json.dumps(
                self.voice_bound_bundle(
                    unit,
                    {
                        "decision": "REWRITE",
                        "masked_text": unit["masked_text"].replace("值得注意的是，", ""),
                    },
                ),
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        first_result = finalizer.finalize(run_dir, rewrites)
        rendered_path = next((run_dir / "rendered_review").rglob("*.md"))
        rendered_before = rendered_path.read_bytes()
        evidence_before = self.evidence_snapshot(run_dir)

        bundle.write_text(
            json.dumps(
                self.voice_bound_bundle(
                    unit,
                    {
                        "decision": "REWRITE",
                        "masked_text": unit["masked_text"].replace(
                            "值得注意的是，该段文字自然。",
                            "这段文字保持自然。",
                        ),
                    },
                ),
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        second_result = finalizer.finalize(run_dir, rewrites)

        self.assert_paired_quality_review_candidate(first_result)
        self.assert_paired_quality_review_candidate(second_result)
        self.assertEqual("NOT_APPLICABLE_PROGRESS", second_result["idempotency"])
        self.assertNotEqual(rendered_before, rendered_path.read_bytes())
        self.assertNotEqual(evidence_before, self.evidence_snapshot(run_dir))
        history = [
            json.loads(line)
            for line in (run_dir / "partial_history.jsonl")
            .read_text(encoding="utf-8")
            .splitlines()
        ]
        self.assertEqual("revised_review_candidate", history[-1]["reason"])
        self.assertFalse((run_dir / "rendered").exists())

    def test_compile_command_cannot_modify_source_without_hard_failure(self) -> None:
        source, run_dir, unit = self.prepare("\\section{定义}\n该定义保持平行结构。\n")
        rewrites = self.rewrite_dir()
        (rewrites / f"{unit['unit_id']}.json").write_text(
            json.dumps(
                self.voice_bound_bundle(
                    unit,
                    {"decision": "NO_CHANGE", "reason": "正式定义保持原有平行结构"},
                ),
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        command = (
            f'"{sys.executable}" -c '
            f'"from pathlib import Path; p=Path(r\'{source}\'); p.write_text(p.read_text(encoding=\'utf-8\')+\'% changed\\n\', encoding=\'utf-8\')"'
        )
        result = finalizer.finalize(run_dir, rewrites, check_command=command)
        self.assertEqual("FAIL", result["status"])
        self.assertTrue(result["source_changed_during_compile_or_finalize"])
        self.assertEqual(1, result["source_files_modified"])
        self.assertFalse((run_dir / "rendered").exists())

    def test_check_command_cannot_modify_real_staging_tree(self) -> None:
        source, run_dir, unit = self.prepare("\\section{定义}\n值得注意的是，该段文字自然。\n")
        rewrites = self.rewrite_dir()
        (rewrites / f"{unit['unit_id']}.json").write_text(
            json.dumps(
                self.voice_bound_bundle(
                    unit,
                    {
                        "decision": "REWRITE",
                        "masked_text": unit["masked_text"].replace("值得注意的是，", ""),
                    },
                ),
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        command = (
            f'"{sys.executable}" -c "from pathlib import Path; '
            f'p=Path(r\'{run_dir / ".rendered_staging" / "main.tex"}\'); '
            f'p.write_text(\'MALICIOUS\\n\', encoding=\'utf-8\')"'
        )

        result = finalizer.finalize(run_dir, rewrites, check_command=command)

        self.assertEqual("FAIL", result["status"])
        self.assert_compile_check_schema(result["compile_check"])
        self.assertFalse(result["full_completion_claim_allowed"])
        self.assertTrue(result["staging_artifacts_changed_during_check"])
        self.assertFalse(result["run_artifacts_changed_during_check"])
        self.assertEqual("FAIL", result["compile_check"]["integrity_status"])
        self.assertIn("staging", result["compile_check"]["integrity_changes"])
        self.assertEqual(0, result["source_files_modified"])
        self.assertFalse((run_dir / "rendered").exists())

    def test_check_command_cannot_modify_run_snapshot(self) -> None:
        source, run_dir, unit = self.prepare("\\section{定义}\n值得注意的是，该段文字自然。\n")
        rewrites = self.rewrite_dir()
        (rewrites / f"{unit['unit_id']}.json").write_text(
            json.dumps(
                self.voice_bound_bundle(
                    unit,
                    {
                        "decision": "REWRITE",
                        "masked_text": unit["masked_text"].replace("值得注意的是，", ""),
                    },
                ),
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        command = (
            f'"{sys.executable}" -c "from pathlib import Path; '
            f'p=next(Path(r\'{run_dir / "source"}\').rglob(\'*.tex\')); '
            f'p.write_text(\'MUTATED\\n\', encoding=\'utf-8\')"'
        )

        result = finalizer.finalize(run_dir, rewrites, check_command=command)

        self.assertEqual("FAIL", result["status"])
        self.assert_compile_check_schema(result["compile_check"])
        self.assertFalse(result["full_completion_claim_allowed"])
        self.assertTrue(result["run_artifacts_changed_during_check"])
        self.assertFalse(result["staging_artifacts_changed_during_check"])
        self.assertEqual("FAIL", result["compile_check"]["integrity_status"])
        self.assertIn("run_dir", result["compile_check"]["integrity_changes"])
        self.assertEqual(0, result["source_files_modified"])
        self.assertFalse(result["source_changed_during_compile_or_finalize"])
        self.assertFalse((run_dir / "rendered").exists())

    def test_check_command_cannot_poison_validation_evidence(self) -> None:
        _, run_dir, unit = self.prepare("\\section{定义}\n值得注意的是，该段文字自然。\n")
        rewrites = self.rewrite_dir()
        (rewrites / f"{unit['unit_id']}.json").write_text(
            json.dumps(
                self.voice_bound_bundle(
                    unit,
                    {
                        "decision": "REWRITE",
                        "masked_text": unit["masked_text"].replace("值得注意的是，", ""),
                    },
                ),
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        validation_path = run_dir / ".validation_staging" / f"{unit['unit_id']}.validation.json"
        command = (
            f'"{sys.executable}" -c "from pathlib import Path; '
            f'p=Path(r\'{validation_path}\'); p.write_text(\'{{}}\', encoding=\'utf-8\')"'
        )

        result = finalizer.finalize(run_dir, rewrites, check_command=command)

        self.assertEqual("FAIL", result["status"])
        self.assertFalse(result["full_completion_claim_allowed"])
        self.assertTrue(result["evidence_artifacts_changed_during_check"])
        self.assertEqual("FAIL", result["compile_check"]["integrity_status"])
        self.assertIn("evidence_staging", result["compile_check"]["integrity_changes"])
        self.assertTrue(result["staged_evidence_discarded"])
        self.assertFalse(result["published_evidence_preserved"])
        self.assertFalse((run_dir / "rendered").exists())
        self.assertFalse((run_dir / "validation").exists())

    def test_check_command_cannot_poison_diff_evidence(self) -> None:
        _, run_dir, unit = self.prepare("\\section{定义}\n值得注意的是，该段文字自然。\n")
        rewrites = self.rewrite_dir()
        (rewrites / f"{unit['unit_id']}.json").write_text(
            json.dumps(
                self.voice_bound_bundle(
                    unit,
                    {
                        "decision": "REWRITE",
                        "masked_text": unit["masked_text"].replace("值得注意的是，", ""),
                    },
                ),
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        diff_path = run_dir / ".diffs_staging" / f"{unit['unit_id']}.diff"
        command = (
            f'"{sys.executable}" -c "from pathlib import Path; '
            f'p=Path(r\'{diff_path}\'); p.write_text(\'FORGED\', encoding=\'utf-8\')"'
        )

        result = finalizer.finalize(run_dir, rewrites, check_command=command)

        self.assertEqual("FAIL", result["status"])
        self.assertTrue(result["evidence_artifacts_changed_during_check"])
        self.assertIn("evidence_staging", result["compile_check"]["integrity_changes"])
        self.assertTrue(result["staged_evidence_discarded"])
        self.assertFalse((run_dir / "diffs").exists())

    def test_poisoned_rerun_preserves_previously_published_evidence(self) -> None:
        _, run_dir, unit = self.prepare("\\section{定义}\n值得注意的是，该段文字自然。\n")
        rewrites = self.rewrite_dir()
        (rewrites / f"{unit['unit_id']}.json").write_text(
            json.dumps(
                self.voice_bound_bundle(
                    unit,
                    {
                        "decision": "REWRITE",
                        "masked_text": unit["masked_text"].replace("值得注意的是，", ""),
                    },
                ),
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        first = finalizer.finalize(run_dir, rewrites)
        evidence_before = self.evidence_snapshot(run_dir)
        rendered_before = _directory_bytes(run_dir / "rendered_review")
        validation_path = run_dir / ".validation_staging" / f"{unit['unit_id']}.validation.json"
        command = (
            f'"{sys.executable}" -c "from pathlib import Path; '
            f'p=Path(r\'{validation_path}\'); p.write_text(\'{{}}\', encoding=\'utf-8\')"'
        )

        second = finalizer.finalize(run_dir, rewrites, check_command=command)

        self.assert_paired_quality_review_candidate(first)
        self.assertEqual("FAIL", second["status"])
        self.assertTrue(second["published_evidence_preserved"])
        self.assertTrue(second["staged_evidence_discarded"])
        self.assertEqual(evidence_before, self.evidence_snapshot(run_dir))
        self.assertEqual(
            rendered_before, _directory_bytes(run_dir / "rendered_review")
        )

    def test_failed_rerun_keeps_previous_metadata_and_detaches_new_evidence(self) -> None:
        _, run_dir, unit = self.prepare(
            "\\section{定义}\n值得注意的是，该段文字自然。\n"
        )
        rewrites = self.rewrite_dir()
        path = rewrites / f"{unit['unit_id']}.json"
        path.write_text(
            json.dumps(
                self.voice_bound_bundle(
                    unit,
                    {
                        "decision": "REWRITE",
                        "masked_text": unit["masked_text"].replace(
                            "值得注意的是，", ""
                        ),
                    },
                ),
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        first = finalizer.finalize(run_dir, rewrites)
        old_metadata = (run_dir / "finalization_metadata.json").read_bytes()
        old_evidence = self.evidence_snapshot(run_dir)
        old_request_sha = first["paired_quality_review_requests"][
            unit["unit_id"]
        ]["request_sha256"]

        path.write_text(
            json.dumps(
                self.voice_bound_bundle(
                    unit,
                    {
                        "decision": "REWRITE",
                        "masked_text": unit["masked_text"].replace(
                            "值得注意的是，该段文字自然。",
                            "该段文字保持自然。",
                        ),
                    },
                ),
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        command = f'"{sys.executable}" -c "raise SystemExit(9)"'
        second = finalizer.finalize(run_dir, rewrites, check_command=command)

        self.assertEqual("FAIL", second["status"])
        self.assertTrue(second["run_state_restored_after_failure"])
        self.assertTrue(second["finalization_metadata_preserved"])
        self.assertTrue(second["published_evidence_preserved"])
        self.assertEqual(
            "NOT_RETAINED_AFTER_ROLLBACK",
            second["failed_attempt_evidence_status"],
        )
        new_request = second["paired_quality_review_requests"][unit["unit_id"]]
        self.assertNotEqual(old_request_sha, new_request["request_sha256"])
        self.assertEqual("", new_request["path"])
        self.assertFalse(second["failed_attempt_evidence_paths_reusable"])
        self.assertEqual(
            old_metadata, (run_dir / "finalization_metadata.json").read_bytes()
        )
        self.assertEqual(old_evidence, self.evidence_snapshot(run_dir))
        self.assertEqual(
            second,
            json.loads(
                (run_dir / "last_failed_attempt_metadata.json").read_text(
                    encoding="utf-8"
                )
            ),
        )

    def test_absolute_check_pollution_restores_previous_review_candidate(self) -> None:
        _, run_dir, unit = self.prepare(
            "\\section{定义}\n值得注意的是，该段文字自然。\n"
        )
        rewrites = self.rewrite_dir()
        (rewrites / f"{unit['unit_id']}.json").write_text(
            json.dumps(
                self.voice_bound_bundle(
                    unit,
                    {
                        "decision": "REWRITE",
                        "masked_text": unit["masked_text"].replace(
                            "值得注意的是，", ""
                        ),
                    },
                ),
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        first = finalizer.finalize(run_dir, rewrites)
        self.assert_paired_quality_review_candidate(first)
        rendered_before = _directory_bytes(run_dir / "rendered_review")
        metadata_before = (run_dir / "finalization_metadata.json").read_bytes()
        rendered_path = next((run_dir / "rendered_review").rglob("*.tex"))
        command = (
            f'"{sys.executable}" -c "from pathlib import Path; '
            f'Path(r\'{rendered_path}\').write_text(\'MALICIOUS\\n\', encoding=\'utf-8\')"'
        )

        second = finalizer.finalize(run_dir, rewrites, check_command=command)

        self.assertEqual("FAIL", second["status"])
        self.assertTrue(second["run_artifacts_changed_during_check"])
        self.assertTrue(second["run_state_restored_after_failure"])
        self.assertTrue(second["published_evidence_preserved"])
        self.assertEqual(
            rendered_before, _directory_bytes(run_dir / "rendered_review")
        )
        self.assertEqual(
            metadata_before, (run_dir / "finalization_metadata.json").read_bytes()
        )

    def test_publish_and_evidence_commit_failures_restore_exact_run_state(self) -> None:
        outer_root = self.root
        for replacement in (False, True):
            for failed_commit in (0, 1):
                with self.subTest(
                    replacement=replacement, failed_commit=failed_commit
                ):
                    case_root = outer_root / f"case-{int(replacement)}-{failed_commit}"
                    case_root.mkdir()
                    self.root = case_root
                    try:
                        _, run_dir, unit = self.prepare(
                            "\\section{定义}\n值得注意的是，该段文字自然。\n"
                        )
                        rewrites = self.rewrite_dir()
                        path = rewrites / f"{unit['unit_id']}.json"
                        first_masked = unit["masked_text"].replace(
                            "值得注意的是，", ""
                        )
                        path.write_text(
                            json.dumps(
                                self.voice_bound_bundle(
                                    unit,
                                    {
                                        "decision": "REWRITE",
                                        "masked_text": first_masked,
                                    },
                                ),
                                ensure_ascii=False,
                            ),
                            encoding="utf-8",
                        )
                        if replacement:
                            finalizer.finalize(run_dir, rewrites)
                            path.write_text(
                                json.dumps(
                                    self.voice_bound_bundle(
                                        unit,
                                        {
                                            "decision": "REWRITE",
                                            "masked_text": unit["masked_text"].replace(
                                                "值得注意的是，该段文字自然。",
                                                "该段文字保持自然。",
                                            ),
                                        },
                                    ),
                                    ensure_ascii=False,
                                ),
                                encoding="utf-8",
                            )
                        state_before = finalizer._run_state_hashes(run_dir)
                        error = OSError(f"evidence commit {failed_commit} failed")
                        side_effect = (
                            [error] if failed_commit == 0 else [None, error]
                        )
                        with mock.patch.object(
                            finalizer,
                            "_commit_evidence_directory",
                            side_effect=side_effect,
                        ):
                            with self.assertRaisesRegex(
                                OSError, f"evidence commit {failed_commit} failed"
                            ):
                                finalizer.finalize(run_dir, rewrites)
                        state_after = finalizer._run_state_hashes(run_dir)
                        state_after.pop("last_failed_attempt_metadata.json")
                        self.assertEqual(state_before, state_after)
                        failure = json.loads(
                            (run_dir / "last_failed_attempt_metadata.json").read_text(
                                encoding="utf-8"
                            )
                        )
                        self.assertEqual("FAIL", failure["status"])
                        self.assertEqual(1, failure["exit_code"])
                        self.assertTrue(failure["failed_attempt"])
                        self.assertEqual(
                            "last_failed_attempt_metadata.json",
                            failure["failed_attempt_metadata_path"],
                        )
                        self.assertEqual(
                            "NOT_RETAINED_AFTER_ROLLBACK",
                            failure["failed_attempt_evidence_status"],
                        )
                        self.assertFalse(
                            failure["failed_attempt_evidence_paths_reusable"]
                        )
                        self.assertTrue(
                            failure["run_state_restored_after_failure"]
                        )
                        self.assertEqual(
                            replacement,
                            failure["finalization_metadata_preserved"],
                        )
                    finally:
                        self.root = outer_root

    def test_transaction_backup_rejects_hard_link_artifact(self) -> None:
        _, run_dir, unit = self.prepare(
            "\\section{定义}\n该定义保持原有平行结构。\n"
        )
        rewrites = self.rewrite_dir()
        (rewrites / f"{unit['unit_id']}.json").write_text(
            json.dumps(
                self.voice_bound_bundle(
                    unit,
                    {
                        "decision": "NO_CHANGE",
                        "reason": "正式定义保持原有平行结构",
                    },
                ),
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        os.link(run_dir / "snapshot.json", run_dir / "snapshot-hardlink.json")

        with self.assertRaisesRegex(ValueError, "hard link is not supported"):
            finalizer.finalize(run_dir, rewrites)

        self.assertFalse((run_dir / "rendered_review").exists())
        self.assertFalse((run_dir / "validation").exists())
        self.assertFalse((run_dir / "finalization_metadata.json").exists())

    def test_runtime_error_is_structured_fail_one_not_review_two(self) -> None:
        stdout = io.StringIO()
        stderr = io.StringIO()
        with mock.patch.object(
            finalizer, "finalize", side_effect=OSError("publication failed")
        ), mock.patch.object(sys, "stdout", stdout), mock.patch.object(
            sys, "stderr", stderr
        ):
            exit_code = finalizer.main(
                ["--run-dir", str(self.root / "run"), "--rewrites", str(self.root)]
            )
        payload = json.loads(stdout.getvalue())
        self.assertEqual(1, exit_code)
        self.assertEqual("FAIL", payload["status"])
        self.assertEqual(1, payload["exit_code"])
        self.assertEqual("FAIL", payload["delivery_gate_status"])
        self.assertEqual("FAILED", payload["publish_state"])
        self.assertTrue(payload["runtime_error"])
        self.assertTrue(payload["failed_attempt"])
        self.assertFalse(payload["failed_attempt_evidence_paths_reusable"])
        self.assertEqual("OSError", payload["error_type"])
        self.assertEqual("", stderr.getvalue())

    def test_malformed_rerun_restores_previous_candidate_and_marks_failed_attempt(self) -> None:
        _, run_dir, unit = self.prepare(
            "\\section{定义}\n该定义保持原有平行结构。\n"
        )
        rewrites = self.rewrite_dir()
        path = rewrites / f"{unit['unit_id']}.json"
        path.write_text(
            json.dumps(
                self.voice_bound_bundle(
                    unit,
                    {
                        "decision": "NO_CHANGE",
                        "reason": "正式定义保持原有平行结构",
                    },
                ),
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        finalizer.finalize(run_dir, rewrites)
        state_before = finalizer._run_state_hashes(run_dir)
        path.write_text("{", encoding="utf-8")

        with self.assertRaises(ValueError):
            finalizer.finalize(run_dir, rewrites)

        state_after = finalizer._run_state_hashes(run_dir)
        state_after.pop("last_failed_attempt_metadata.json")
        self.assertEqual(state_before, state_after)
        failure = json.loads(
            (run_dir / "last_failed_attempt_metadata.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual("FAIL", failure["delivery_gate_status"])
        self.assertEqual(1, failure["exit_code"])
        self.assertTrue(failure["failed_attempt"])
        self.assertTrue(failure["run_state_restored_after_failure"])
        self.assertTrue(failure["published_evidence_preserved"])
        self.assertEqual(
            "NOT_RETAINED_AFTER_ROLLBACK",
            failure["failed_attempt_evidence_status"],
        )
        self.assertFalse(failure["failed_attempt_evidence_paths_reusable"])

    def test_argument_syntax_error_keeps_argparse_exit_two(self) -> None:
        stdout = io.StringIO()
        stderr = io.StringIO()
        with mock.patch.object(sys, "stdout", stdout), mock.patch.object(
            sys, "stderr", stderr
        ):
            with self.assertRaises(SystemExit) as raised:
                finalizer.main([])
        self.assertEqual(2, raised.exception.code)
        self.assertIn("usage:", stderr.getvalue())
        self.assertEqual("", stdout.getvalue())

    def test_protected_only_document_cannot_claim_full_completion(self) -> None:
        source = self.root / "only.tex"
        source.write_text(
            "\\section{保护内容}\n\\label{eq:one}\n\\[x^2=1\\]\n",
            encoding="utf-8",
        )
        run_dir = self.root / "run"
        preparer.prepare([source], run_dir, scene="RESEARCH", min_author_chars=0)

        result = finalizer.finalize(run_dir, self.rewrite_dir())

        self.assertEqual("REVIEW", result["status"])
        self.assertFalse(result["full_completion_claim_allowed"])
        self.assertEqual(0, result["processable_editable_units"])
        self.assertFalse((run_dir / "rendered").exists())

    def test_check_command_side_effects_in_disposable_copy_do_not_publish(self) -> None:
        source, run_dir, unit = self.prepare("\\section{定义}\n值得注意的是，该段文字自然。\n")
        rewrites = self.rewrite_dir()
        (rewrites / f"{unit['unit_id']}.json").write_text(
            json.dumps(
                self.voice_bound_bundle(
                    unit,
                    {
                        "decision": "REWRITE",
                        "masked_text": unit["masked_text"].replace("值得注意的是，", ""),
                    },
                ),
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        command = f'"{sys.executable}" -c "from pathlib import Path; Path(\'build-side-effect.txt\').write_text(\'ok\')"'

        result = finalizer.finalize(run_dir, rewrites, check_command=command)

        self.assert_paired_quality_review_candidate(result)
        self.assert_compile_check_schema(result["compile_check"])
        self.assertTrue(result["coverage_completion_claim_allowed"])
        self.assertEqual("PASS", result["voice_binding_status"])
        self.assertEqual("PASS", result["voice_conformance_status"])
        self.assertEqual("PASS", result["cross_unit_repetition_status"])
        self.assertEqual("NOT_RUN", result["humanize_second_pass_convergence"])
        self.assertTrue(result["voice_completion_claim_allowed"])
        self.assertFalse(result["humanize_completion_claim_allowed"])
        self.assertFalse(result["full_completion_claim_allowed"])
        self.assertEqual(result["idempotency"], result["assembly_replay_idempotency"])
        self.assertEqual(
            str((run_dir / ".compile_check_staging").resolve()),
            result["compile_check"]["cwd"],
        )
        self.assertEqual("PASS", result["compile_check"]["integrity_status"])
        self.assertEqual({}, result["compile_check"]["integrity_changes"])
        self.assertFalse(result["evidence_artifacts_changed_during_check"])
        self.assertFalse(result["staged_evidence_discarded"])
        rendered = next((run_dir / "rendered_review").rglob("*.tex")).read_text(
            encoding="utf-8"
        )
        self.assertNotIn("值得注意的是", rendered)
        self.assertFalse(
            (run_dir / "rendered_review" / "build-side-effect.txt").exists()
        )
        self.assertFalse((run_dir / "rendered").exists())
        self.assertFalse((run_dir / ".compile_check_staging").exists())

    def test_check_command_descendants_cannot_poison_after_finalize_returns(self) -> None:
        _, run_dir, unit = self.prepare(
            "\\section{定义}\n值得注意的是，该段文字自然。\n"
        )
        rewrites = self.rewrite_dir()
        (rewrites / f"{unit['unit_id']}.json").write_text(
            json.dumps(
                self.voice_bound_bundle(
                    unit,
                    {
                        "decision": "REWRITE",
                        "masked_text": unit["masked_text"].replace(
                            "值得注意的是，", ""
                        ),
                    },
                ),
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        target = run_dir / "rendered_review" / "main.tex"
        child = self.root / "late-child.py"
        child.write_text(
            "import time\n"
            "from pathlib import Path\n"
            "time.sleep(0.8)\n"
            f"target = Path({str(target)!r})\n"
            "if target.is_file():\n"
            "    target.write_text('LATE_POISON\\n', encoding='utf-8')\n",
            encoding="utf-8",
        )
        spawner = self.root / "spawn-late-child.py"
        spawner.write_text(
            "import os, subprocess, sys\n"
            "kwargs = {}\n"
            "if os.name == 'nt':\n"
            "    kwargs['creationflags'] = subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP\n"
            "else:\n"
            "    kwargs['start_new_session'] = True\n"
            f"subprocess.Popen([sys.executable, {str(child)!r}], "
            "stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, "
            "stderr=subprocess.DEVNULL, close_fds=True, **kwargs)\n",
            encoding="utf-8",
        )
        command = f'"{sys.executable}" "{spawner}"'

        result = finalizer.finalize(run_dir, rewrites, check_command=command)
        time.sleep(1.1)

        self.assert_paired_quality_review_candidate(result)
        self.assertEqual("PASS", result["compile_check"]["descendant_cleanup"])
        self.assertEqual(
            "WINDOWS_JOB_OBJECT" if os.name == "nt" else "POSIX_PROCESS_GROUP",
            result["compile_check"]["process_containment"],
        )
        self.assertNotEqual("LATE_POISON\n", target.read_text(encoding="utf-8"))

    def test_compile_check_schema_is_stable_when_command_is_not_provided(self) -> None:
        _, run_dir, unit = self.prepare("\\section{定义}\n该定义保持平行结构。\n")
        rewrites = self.rewrite_dir()
        (rewrites / f"{unit['unit_id']}.json").write_text(
            json.dumps(
                self.voice_bound_bundle(
                    unit,
                    {"decision": "NO_CHANGE", "reason": "正式定义保持原有平行结构"},
                ),
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

        result = finalizer.finalize(run_dir, rewrites)

        self.assert_paired_quality_review_candidate(result)
        self.assert_compile_check_schema(result["compile_check"])
        self.assertEqual("NOT_RUN", result["compile_check"]["status"])
        self.assertIsNone(result["compile_check"]["cwd"])
        self.assertEqual("PASS", result["compile_check"]["integrity_status"])
        self.assertEqual({}, result["compile_check"]["integrity_changes"])

    def test_compile_check_schema_is_stable_when_format_check_fails(self) -> None:
        _, run_dir, unit = self.prepare(
            "\\section{定义}\n该定义保持{未闭合的平行结构。\n"
        )
        rewrites = self.rewrite_dir()
        (rewrites / f"{unit['unit_id']}.json").write_text(
            json.dumps(
                self.voice_bound_bundle(
                    unit,
                    {"decision": "NO_CHANGE", "reason": "保留输入中的原有形式"},
                ),
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

        result = finalizer.finalize(
            run_dir,
            rewrites,
            check_command=f'"{sys.executable}" -c "raise SystemExit(9)"',
        )

        self.assertEqual("FAIL", result["status"])
        self.assertTrue(result["full_format_errors"])
        self.assert_compile_check_schema(result["compile_check"])
        self.assertEqual("NOT_RUN_DUE_TO_FORMAT_FAILURE", result["compile_check"]["status"])
        self.assertIsNone(result["compile_check"]["cwd"])
        self.assertEqual("NOT_RUN", result["compile_check"]["integrity_status"])
        self.assertEqual({}, result["compile_check"]["integrity_changes"])


if __name__ == "__main__":
    unittest.main()
