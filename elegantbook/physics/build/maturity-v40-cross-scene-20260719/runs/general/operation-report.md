# Operation Report

## 任务与边界

- 配置：`mode=REWRITE`，`scene=GENERAL`，`intensity=BALANCED`，`requested_output=PATCH`，`effective_output=PATCH`，`voice_profile=NONE`，`voice_disclosure=SCENE_DEFAULT`，`report_context=NONE`。
- 范围：指定 `general.md` 全文；`source_kind=DOCUMENT`；标题文字与层级、表格结构、引语、内联代码、数字、术语、模态、事实关系和证据标注均锁定。
- 来源角色：按用户要求视为 `MODEL_ORIGIN_UNRESOLVED` 压力输入，仅用于本次负向文风审阅，不作为正向 Voice 或可复制句库；`corpus_action_support=NONE`。
- 编码：严格 UTF-8 读取通过，无需编码回退。源文件未修改。
- 源快照：`size_bytes=3818`；`sha256=5f9999451a0f460a2e51bd4b625ca0e704a8ce4ed5da4786dca68f1ec17c1ce8`。

## Authoring 与 Coverage

- AUTO high 总数：`1`；其中 `candidate high=0`、`PROTECTED=1`、`EXCLUDED=0`。
- 唯一 high 是 blockquote 保护区内 `收口`，范围 `bytes [213,219)`，`signal_id=LEX-MGMT-01`，处置为 `PROTECTED/markdown-quote`；未进入 hunk。
- authoring suggestions：`AVAILABLE=0`，`SUPPRESSED=0`。原因是没有 candidate high，scaffold 未发放建议 span。
- 最终 registry spans：`11`，即 high registry span `1` + manual spans `10`。
- 最终 selection：`10`；hunks：`10`；suggested-span hunks：`0`；manual-range hunks：`10`。
- 决策计数：`REWRITE=9`，`DELETE_STYLE_SHELL=1`，`UNRESOLVED=0`；显式 conflict：`0`；lexical KEEP：`0`。
- 分区：`patch_hunks_source_partition=NON_OVERLAPPING`；未列范围：`COPY_EXACT`。
- Coverage：`PASS`，`coverage_completion_claim_allowed=true`，但范围仅为 `ENUMERATED_HIGH_AND_BOUND_DECLARATIONS_ONLY`；`semantic_completeness_claim_allowed=false`。

## Hunk Source Ranges

以下 byte range 均为严格 UTF-8 半开区间，行列范围也按半开终点记录。全部 hunk 均不来自 authoring scaffold 的 `AVAILABLE` suggestion，而是连续阅读后登记的 manual range。

| Hunk | Decision | Exact source range | Source text | Scaffold provenance |
|---|---|---|---|---|
| H001 | REWRITE | `bytes [323,343); L7:C4-L7:C12` | `**项目定位应是` | `MANUAL A002; AVAILABLE=NO` |
| H002 | DELETE_STYLE_SHELL | `bytes [445,448); L7:C46-L7:C49` | `**<SPACE>` | `MANUAL A003; AVAILABLE=NO` |
| H003 | REWRITE | `bytes [931,995); L8:C4-L8:C30` | `**零新增FE主线与主动数学确认分支必须分账。**<SPACE>` | `MANUAL A004; AVAILABLE=NO` |
| H004 | REWRITE | `bytes [1173,1221); L8:C108-L8:C124` | `只能作为低置信样例的预算受控确认` | `MANUAL A005; AVAILABLE=NO` |
| H005 | REWRITE | `bytes [1309,1380); L9:C4-L9:C31` | `**主输出应服务于决策，而非强行恢复完整交互图。**<SPACE>` | `MANUAL A006; AVAILABLE=NO` |
| H006 | REWRITE | `bytes [1713,1758); L10:C4-L10:C25` | `**Loss不能只使用期望类别距离。**<SPACE>` | `MANUAL A007; AVAILABLE=NO` |
| H007 | REWRITE | `bytes [2096,2146); L11:C4-L11:C24` | `**最终价值必须用下游总收益验收。**<SPACE>` | `MANUAL A008; AVAILABLE=NO` |
| H008 | REWRITE | `bytes [2146,2158); L11:C24-L11:C28` | `统一比较` | `MANUAL A009; AVAILABLE=NO` |
| H009 | REWRITE | `bytes [2744,2789); L17:C89-L17:C104` | `同时满足样本顺序和坐标顺序不变` | `MANUAL A010; AVAILABLE=NO` |
| H010 | REWRITE | `bytes [3716,3815); L20:C70-L20:C103` | `输出路由动作与依据；按共享总预算比较最终目标值，不只比较分类准确率` | `MANUAL A011; AVAILABLE=NO` |

## 首次机械失败与回退

首次 applicator 尝试保留在 `candidate-review/`。该次 `structural_validation=PASS`、`coverage=PASS`、`hard_invariant_layer_status=PASS`、`speech_act_layer_status=PASS`，但 `style_signal_layer_status=REVIEW`，统一 validator 为 `REVIEW`。具体原因为 `introduced_style_signal`：4 个改写后的加粗结论句被重新识别为 `LEX-FORMAT-BOLD-01/low`。这是机械门 REVIEW，不是硬 FAIL；applicator 发布待审目录，未执行 staging 回滚。

回退未修改或重封旧证据，而是建立新 scaffold/bundle，将 5 个同构加粗结论改为普通列表正文。第二次机械层通过后，模型成对自检发现移除加粗留下了句间空格，故再次用全新 manual ranges 把相邻空格纳入同一变更。最终交付绑定第三次工件 `selection.authoring.delivery.json`、`selection.delivery.v2.json`、`patch.delivery.bundle.json` 和 `candidate-review-delivery/`；前两次候选与证据均保留。

## 最终状态

| Layer | Status |
|---|---|
| validator candidate assembly | `PASS` |
| validator mechanical validation | `PASS` |
| hard invariant layer | `PASS` |
| speech-act layer | `PASS` |
| style-signal layer | `PASS` |
| unexplained high / introduced findings / pending warnings | `0 / 0 / 0` |
| validator top level | `REVIEW exit=2` |
| applicator structural / patch application / coverage | `PASS / PASS / PASS` |
| applicator top level | `DELIVERY REVIEW exit=2` |
| paired quality | `PENDING_EXTERNAL_REVIEW` |
| verifier integrity | `PASS exit=0; scope=SELF_CONSISTENCY_ONLY` |
| current-policy replay | `PASS` |
| coverage replay | `PASS` |
| live source | `MATCH`，expected/observed SHA 均为 `5f9999451a0f460a2e51bd4b625ca0e704a8ce4ed5da4786dca68f1ec17c1ce8` |
| semantic judgment | `NOT_EVALUATED` |
| academic correctness | `NOT_EVALUATED` |
| humanize quality claim | `false` |

最终 source/bundle/candidate SHA-256 分别为：

- source: `5f9999451a0f460a2e51bd4b625ca0e704a8ce4ed5da4786dca68f1ec17c1ce8`
- bundle: `f0cfab6543318444d81492cdfe0d9e0502badf76d3e6516e82a6aeeb75201fa3`
- candidate: `8edfd4e45b84f3e82c8ef76a1ad2f6aa2576002dafacbe1cb46cf66c82c778f4`

## DELIVERY 边界

权威交付边界为 `DELIVERY REVIEW exit=2`。verifier 的 `PASS exit=0` 只证明闭集工件在当前 policy 下可重放、自洽，且 live source 仍与冻结源匹配；它不把候选升级为正式终稿，也不证明文风收益、语义完整性、学术正确性、作者身份或个人声线。由于没有代理不可伪造的外部 paired-quality clearance，`humanize_quality_claim_allowed=false`，候选只能作为待审稿交付。

## 保留工件

- 最终 scaffold/selection/PATCH：`selection.authoring.delivery.json`、`selection.delivery.v2.json`、`patch.delivery.bundle.json`。
- 最终 applicator 闭集：`candidate-review-delivery/`，含 `source.snapshot.bin`、`candidate.review.md`、`review.md`、`patch.diff`、`patch.bundle.json`、`coverage.json`、`validation.json`、`result.json`、`evidence-manifest.json`。
- 最终 applicator/verifier 摘要：`applicator.delivery.txt`、`verifier.delivery.txt`。
- 首次机械 REVIEW 工件：`selection.authoring.json`、`selection.v2.json`、`patch.bundle.json`、`candidate-review/`。
- 中间机械 PASS、成对自检回退工件：`selection.authoring.final.json`、`selection.final.v2.json`、`patch.final.bundle.json`、`candidate-review-final/`。

