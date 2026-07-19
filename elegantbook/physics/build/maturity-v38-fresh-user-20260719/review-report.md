# 短 PATCH 复核报告

## 处理范围与配置

- 源文件：`tests/fixtures/humanize_forward_v10/course_before.tex`
- 配置：`mode=REWRITE; scene=COURSE; intensity=BALANCED`
- 输出：`requested_output=CLEAN; effective_output=PATCH`
- 来源类型：`source_kind=DOCUMENT; scan_scene=AUTO`
- 声线：`voice_profile=NONE; voice_disclosure=SCENE_DEFAULT`
- 报告上下文：`report_context=NONE`

未修改源文件、Skill 或 tests。所有新工件均位于
`build/maturity-v38-fresh-user-20260719`。本次未读取任务明令排除的既有工件。

## Authoring 与流水线

1. `scaffold create` 生成 `selection.authoring.json`，冻结 4 个 candidate high finding。
2. authoring 文件中登记 5 个 hunk source span；每个精确 `{start_byte, source_text}` 只登记一次，hunk 和 selection 均通过 `span_id` 引用，不重复抄录原文。
3. 4 个 high finding 全部以 `HUNK` resolution 处置：`LEX-EMPH-01 -> H001`、`LEX-COACH-01 -> H002`、`LEX-MARKET-01 -> H004`、`LEX-FOUNDATION-01 -> H004`。
4. `scaffold finalize` 成功生成 `humanize-short-patch-selection/v2`：5 个 hunk、5 个 selection、1 个显式 conflict pair。
5. `build` 返回 `BUNDLED/0`，bundle SHA-256 为 `56681c760bfeecbdaeacc1c07e60333b8a94dc7a4eb1835d81bb420768617db1`。
6. `apply` 发布 `short-patch-review`，候选状态为 `DELIVERY REVIEW/2`。
7. `verify --live-source` 返回 verifier `PASS/0`；闭集完整性、coverage replay、current-policy replay 均为 `PASS`，live source 为 `MATCH`。

## 候选与 Verifier 状态

必须区分以下两层结果：

- 候选交付：`delivery_gate_status=REVIEW`、`delivery_gate_exit_code=2`。`result.json` 同时记录 `status=REVIEW`、`exit_code=2`；候选不是正式终稿。
- Verifier：`status=PASS`、`exit_code=0`，范围仅为 `integrity_scope=SELF_CONSISTENCY_ONLY`。它证明闭集工件在当前 policy 下可重放且与 live source 匹配，不会把候选升级为交付 PASS。

候选硬不变量层为 `PASS`，文风 high 层为 `PASS`；统一验证器因删除“必须”触发
`SPEECH_ACT_MODALITY_SCOPE_CHANGED`，故言语行为层与机械验证保持 `REVIEW`，成对质量状态为
`BLOCKED_BY_MECHANICAL_GATE`。`humanize_quality_claim_allowed=false`，
`academic_correctness=NOT_EVALUATED`。

## 中文 Review 可见性

已完整阅读自动生成的 `short-patch-review/review.md`，以下内容可以直接看到：

- `已变化 hunk`：H001 删除空重点提示壳，H002 把无条件记忆口令改为检查适用条件，H004 删除泛化意义与后续基础桥接。
- `未变化的未决 hunk`：H003 和 H005 均逐字回显，分别保留“可以直接套用”与条件不满足时“不能……直接代入”的原始主张。
- `显式冲突对`：C001 使用 `OPPOSING_PERMISSION`，左右为 H003/H005，处置为 `UNRESOLVED_PAIR`。
- `覆盖范围与限制`：`PASS` 仅覆盖 `ENUMERATED_HIGH_AND_BOUND_DECLARATIONS_ONLY`；任务/扫描场景为 `COURSE/AUTO`，计数为 high 4、selection 5、conflict 1。
- 限制字段明确为 `semantic_completeness_claim_allowed=false` 和 `humanize_quality_claim_allowed=false`，并明示不证明完整语义发现、学术正确性、作者身份或外部成对质量 clearance。

## 未决项

H003 与 H005 的公式适用许可互相形成来源内部张力。纯文风层没有裁决哪一条物理主张正确，
两侧因此保持原样 `UNRESOLVED`。需要用户或独立学科复核先裁决并更新来源，才能继续处理该对主张。
