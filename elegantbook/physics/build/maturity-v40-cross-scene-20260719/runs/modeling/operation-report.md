# Modeling short PATCH operation report

## 1. 任务边界与配置

- `mode=REWRITE`
- `scene=MODELING`
- `intensity=BALANCED`
- `requested_output=PATCH; effective_output=PATCH`
- `voice_profile=NONE; voice_disclosure=SCENE_DEFAULT`
- `report_context=NONE`
- `source_kind=DOCUMENT; document_format=TEX; scan_scene=AUTO`
- `corpus_action_support=NONE`
- 来源角色：`MODEL_ORIGIN_UNRESOLVED` 压力输入；未作为真人范文、个人 Voice、事实来源或正向句库。
- 读取隔离：只读取指定 fixture、Skill 目录中的当前任务说明/脚本，以及本次 run 自己生成的工件；未读取 tests、其他 fixture、同级 build、历史 run、历史报告或原始文档。
- UTF-8 严格读取：`PASS`；source bytes=`4662`。
- source SHA-256：`b21e3cd3f0e215aaaa2528a0beffa6c94d01f23cfdcedd9f278ff050dddfd876`。
- 源文件未修改；verifier 的 live-source expected/observed SHA-256 相同，状态为 `MATCH`。
- 标题、引语、公式、数字、TeX 命令/环境、引用均未进入可变 hunk。学术正确性、建模正确性与引用真实性未评估。

## 2. Scanner、authoring 与 coverage 计数

| 项目 | 实际值 |
|---|---:|
| scanner 全部 candidate | 1（`LEX-TABLE-ROLE-01`，medium） |
| candidate high | 0 |
| authoring `AVAILABLE` suggestions | 0 |
| authoring `SUPPRESSED` suggestions | 0 |
| registry spans | 9 |
| selected spans | 9 |
| hunks | 9 |
| suggested-span hunks | 0 |
| manual-range hunks | 9 |
| explicit conflicts | 0 |
| unresolved hunks | 1 |

`create` 返回 `NO_HIGH_FINDINGS high=0 suggestions=0`。这只表示 AUTO high inventory 为空，不表示 `NO_CHANGE`。连续阅读后登记了 9 个 manual range；coverage 最终为 `PASS`，其声明范围严格限于 `ENUMERATED_HIGH_AND_BOUND_DECLARATIONS_ONLY`。`semantic_completeness_claim_allowed=false`。

## 3. Hunk source ranges

以下 UTF-8 byte range 均为半开区间 `[start,end)`；行列为 1-based，末端列同样是 exclusive。authoring 没有 `AVAILABLE` suggestion，因此每个 hunk 都准确记为 `MANUAL_RANGE`。

| Hunk | Decision | UTF-8 bytes | Source range | Range origin |
|---|---|---:|---|---|
| H001 | `REWRITE` | `[49,94)` | `3:1-3:16` | `MANUAL_RANGE` |
| H002 | `REWRITE` | `[442,517)` | `6:1-6:26` | `MANUAL_RANGE` |
| H003 | `DELETE_STYLE_SHELL` | `[985,1003)` | `8:1-8:7` | `MANUAL_RANGE` |
| H004 | `REWRITE` | `[1623,1683)` | `10:1-10:21` | `MANUAL_RANGE` |
| H005 | `REWRITE` | `[2100,2115)` | `10:160-10:165` | `MANUAL_RANGE` |
| H006 | `REWRITE` | `[2237,2261)` | `12:1-12:9` | `MANUAL_RANGE` |
| H007 | `REWRITE` | `[3512,3743)` | `17:175-17:252` | `MANUAL_RANGE` |
| H008 | `UNRESOLVED` | `[4358,4493)` | `21:1-21:46` | `MANUAL_RANGE` |
| H009 | `REWRITE` | `[4493,4661)` | `21:46-21:102` | `MANUAL_RANGE` |

机器可读台账见 `hunk-range-provenance.json`。H008 原样保留：当前 fixture 未呈现实际表格，纯文风层无法确认该句是现有表格的读者功能说明，还是尚未执行的编辑计划，因此不得改写为完成事实。

## 4. 首次机械失败与回退

1. 初版 authoring/finalize/build 均成功；初版 applicator 的 structural、coverage 与 hard invariant 为 `PASS`，但统一 validator 返回 `REVIEW/2`。首个机械 finding 为 `SPEECH_ACT_NEGATION_CHANGED`：H001、H002 共删去两个“不”，计数由 `11` 变为 `9`。
2. 第一次回退把 H001/H002 改为含“并不”与“不只”的版本，恢复否定标记。该版本随后触发 `SPEECH_ACT_MODALITY_SCOPE_CHANGED`，原因是 H002 新增一个“只”，模态计数由 `8` 变为 `9`。
3. 第二次回退仅把 H002 调整为“不单比较……还要说明”，保留原有“不”和“要”且不新增“只”。最终 validator 达到 mechanical `PASS/0`。

初版与两次回退工件均保留：`selection.v2.json`、`patch.bundle.json`、`applicator/`，`selection.fallback.v2.json`、`patch.fallback.bundle.json`、`applicator-fallback/`，以及最终 `selection.fallback2.v2.json`、`patch.fallback2.bundle.json`、`applicator-final/`。

## 5. 最终状态

| Layer | Status |
|---|---|
| validator | `mechanical_validation_status=PASS`, `mechanical_validation_exit_code=0` |
| hard invariant | `PASS` |
| speech-act layer | `PASS`；unaccepted warnings=`0` |
| style-signal layer | `PASS`；unexplained high=`0` |
| applicator structure | `PASS` |
| patch application | `PASS` |
| coverage | `PASS`；selected spans=`9`，lexical high=`0` |
| paired quality | `PENDING_EXTERNAL_REVIEW` |
| applicator delivery | `REVIEW/2`；unresolved=`1` |
| verifier record integrity | `PASS/0`，scope=`SELF_CONSISTENCY_ONLY` |
| verifier coverage replay | `PASS` |
| current policy | `MATCH`; replay=`PASS` |
| live source | `MATCH` |
| academic correctness | `NOT_EVALUATED` |
| semantic judgment | `NOT_EVALUATED` |

最终候选 SHA-256：`ea512f5d6a7e77c159135803a25add3a0013c898a113bf164b05c3dd8def2b17`。

## 6. DELIVERY 边界

权威候选是 `applicator-final/candidate.review.tex`，权威 PATCH 是 `applicator-final/patch.diff`。准确交付状态为：

```text
DELIVERY REVIEW exit=2
```

verifier 自身的 `PASS exit=0` 只证明闭集工件、coverage 与当前 policy replay 在 `SELF_CONSISTENCY_ONLY` 范围内自洽，并且 live source 仍匹配；它不把候选升级为正式交付。由于 H008 仍为 `UNRESOLVED`，且没有可信外部 paired-quality clearance，固定保持：

- `completion_claim_allowed=false`
- `humanize_quality_claim_allowed=false`
- `semantic_completeness_claim_allowed=false`
- `academic_correctness=NOT_EVALUATED`
- `delivery_gate_status=REVIEW; delivery_gate_exit_code=2`

因此，本次只能称为“机械验证通过的纯文风待审 PATCH 候选”，不能称为 Humanize 完成、学术正确、建模正确或已正式发布。

## 7. 保留工件

- Scanner：`scan.auto.json`
- Scaffold：`selection.authoring.initial.json`、`selection.authoring.fallback1.json`、`selection.authoring.json`
- Selection：`selection.v2.json`、`selection.fallback.v2.json`、`selection.fallback2.v2.json`
- PATCH bundles：`patch.bundle.json`、`patch.fallback.bundle.json`、`patch.fallback2.bundle.json`
- 初次与回退 applicator：`applicator/`、`applicator-fallback/`
- 最终 applicator 闭集：`applicator-final/`，含 candidate、`patch.diff`、`review.md`、`coverage.json`、`validation.json`、`result.json`、source snapshot 与 evidence manifest
- Verifier：`verifier.current.json`
- Hunk range/provenance：`hunk-range-provenance.json`
- 本报告：`operation-report.md`
