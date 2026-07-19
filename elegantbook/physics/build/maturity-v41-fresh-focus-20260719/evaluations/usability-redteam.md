# v41 Fresh Short-PATCH 可用性红队审计

## 范围与计数口径

本审计只读取本运行的三份 `operation-report.md`、`humanize-academic-chinese/SKILL.md` 和 `references/short-patch-workflow.md`。没有读取 tests、既有成熟度报告或根代理结论。

“最终候选字段数”指最终 source-bound selection/bundle 中需要表达的字段；“总录入/重算”还包括报告明确记载的失败尝试。`reason` 按 short-PATCH v2 的两个位置计数：每个 hunk 一个 `hunk.reason`，每个 selected span 一个 `selection.reason`。`ID` 分开统计 focus、selection、hunk；报告没有单独暴露 registry span ID 时不臆测。offset 分为人工填写和工具确定性生成。

## 逐候选成本

| fresh 使用者/最终候选 | 最终 scaffold | focus | span | hunk | selection | reason | 可见 ID | offset | 额外重试/重建 |
|---|---:|---:|---:|---:|---:|---:|---|---|---|
| COURSE `candidate-review-retry2` | 1 个最终 scaffold；共 `3` 次 `create` | `3` 个精确 focus 字符串 | `3` | `3` | `3` | `6`（3 hunk + 3 selection） | `3 focus + 3 selection + 3 hunk = 9`；conflict `0` | 人工 `0`；工具确定性定位 `3`（起点 `0,716,848`） | `2` 个 recovery cycle；其中 1 次 inventory hash 失败、1 次 speech-act warning 修复；最终链前共 3 次 scaffold create |
| MODELING `short-patch-review-v6` | `1` | `0`（非 FOCUS；scanner high `3`，可用建议 `6`，suppressed `4`） | `8` | `8` | `8` | `16`（8 hunk + 8 selection） | `8 selection + 8 hunk = 16`；conflict `0` | 最终 `8`；首次 builder 的起点不匹配后重算全部 `8`，按写入事件计为最多 `16` 个 offset 值 | `3` 个 recovery cycle：offset mismatch、DIRECT_QUOTATION_CHANGED、speech-act/high warning；至少 4 次 bundle/apply 迭代 |
| GENERAL（最终实际路由为 MODELING）`short-patch-review.modeling.final` | `1` 个最终 MODELING scaffold；共 `3` 次 scaffold（GENERAL 初次、GENERAL retry、MODELING final） | `3` 个 focus 字符串 | `3` | `3` | `3` | `6`（3 hunk + 3 selection） | `3 focus + 3 selection + 3 hunk = 9`；conflict `0` | 人工 `0`；工具确定性生成 `3`（`682,1534,2086`） | `3` 个 recovery/rebuild：恢复 negation/modality、actual-scene reroute、最终 semantic boundary 修正；host wrapper 将预期 `REVIEW/2` 当脚本错误，不计为语义重试 |

### 录入劳动与语义劳动的边界

必要的语义判断包括：

- 选择哪些词句确实是本次要处理的 prose surface（COURSE/GENERAL 各 3 个 focus；MODELING 从 3 个 high 中展开为 8 个 source span）。
- 每个 hunk 的 `DELETE_STYLE_SHELL`、`REWRITE` 或 `UNRESOLVED` 决策，以及不可自动生成的 replacement 内容。
- 为每个 hunk 和 selection 给出实际理由，判断是否保留条件、否定、模态、引语、术语和技术关系。MODELING 的 8 个 hunk 中有 1 个必须保持 `UNRESOLVED`；COURSE 的 H003 也因条件标记被 warning 后重新判断。
- 选择显式保护项（COURSE 4 个术语，MODELING 15 个保护绑定，GENERAL 的事实/方法/预算/路由账本）。这属于领域和范围判断，不应由工具默默授权。

可以由确定性工具消除或显著降低的录入劳动包括：

- 唯一 `source_text` 的 UTF-8 byte offset、source SHA、半开区间和 grapheme/CRLF 边界检查。COURSE/GENERAL 已由工具定位；MODELING 的 8 个 offset mismatch 说明当前接口仍把修复成本推给使用者。
- focus/span/selection/hunk 的稳定 ID、引用关系、非重叠分区、`COPY_EXACT` 尾部和 coverage inventory。用户不应在每次重建后重新编号或手工重连。
- 配置、protected-term 列表和 route 的一致性检查。COURSE 因 create 后改 `intensity/protected_terms` 被迫重建；GENERAL 在 GENERAL 产物完成后才发现实际场景是 MODELING。
- 同一语义理由在 `hunk.reason` 与 `selection.reason` 的重复抄录。理由内容仍需人决定，但接口可以允许一个明确的 `reason_ref` 被两个字段引用，并由工具展开/校验。
- warning 发生后的局部重跑、bundle hash 重算和 closed artifact 重新装配。当前流程通常要求整条 scaffold -> finalize -> build -> apply 链重新走一遍。

不能自动化的边界是：不自动生成 replacement，不自动选择或扩大 source span，不自动决定 `REWRITE/DELETE_STYLE_SHELL/UNRESOLVED`，不自动编造 reason、protected terms 或 conflict，也不自动授予 paired-quality、学术正确性、作者身份或最终交付授权。确定性工具最多提供定位、完整性检查、稳定引用和局部重算；`DELIVERY REVIEW/2` 与外部复核边界必须保留。

## 最高优先级的三个缺口

### P0：一次局部修订却被迫重建整条 immutable 链

**证据。** COURSE 仅因 create 后配置变化就出现 `inventory_sha256 mismatch`，随后 3 次 create；第一次候选还因一个条件标记 warning 而整链重建。MODELING 在 offset、引语和 speech-act 三个阶段反复构建 bundle。每次重试都重新面对 span、ID、selection 和 reason 的一致性风险。

**最小接口改进。** 增加 run-scoped `amend` 操作：以同一 source/config/policy snapshot 为会话锚点，只接收用户明确修改的 `hunk_id`（包括新的 replacement、decision 或 reason），由工具确定性重算受影响的 hash、offset、coverage 和 artifacts，并保留未改 hunk 的 ID/selection/reason。配置一旦改变，先给出字段级 diff 和“需新会话”的明确提示，不让用户在半成品 JSON 上隐式失效。

**边界。** amend 不得替用户写 replacement、提升 decision 或清除 warning；用户仍需对修改后的语义负责，外部 paired-quality 仍是 REVIEW。

### P1：实际 scene/route 太晚才确定，导致重复 authoring

**证据。** GENERAL 的第一次与 retry 都按 `GENERAL` 生成，之后 route script 才确定实际是 `MODELING`，迫使同一 3 个 span 在新 scene 下再 scaffold/build/apply；这是可在 authoring 前确定的路由信息。

**最小接口改进。** `create --scene AUTO` 先输出并冻结 `resolved_scene`、route margin 和扫描视图，随后在同一命令中生成该 scene 的 scaffold；若调用方显式指定了不同 scene，finalize 在写任何候选前直接返回可读的 route mismatch 和迁移命令，自动复用 source_text、IDs、offsets 与 reasons，不要求重抄。

**边界。** route 只能由既定策略和输入证据确定；工具不能因 route 变化而替用户改变 hunk 范围、replacement 或语义理由，也不能把 route 一致性当作质量授权。

### P1：offset/ID/linkage 的机械脆弱性把可避免错误变成重试

**证据。** MODELING 首次 builder 直接因 `start_byte does not match source_text` 失败，随后必须重算全部 8 个 UTF-8 起点；三个场景都需要维护 focus/span/selection/hunk 的平行引用，虽然这些引用本质上可由 source-bound registry 确定性派生。

**最小接口改进。** 提供只读 `resolve-registry`/`repair-offsets` 预检：以 source SHA + `source_text` 唯一匹配时自动填充 offset、生成稳定 ID、建立 selection↔hunk 引用并报告歧义；重复文本、保护区重叠或跨 grapheme 时只返回待人工选择的候选位置。允许 `reason_ref` 去重理由录入，但不隐藏每个 hunk/selection 的最终展开值。

**边界。** 非唯一 source_text、跨保护区或真正的语义边界不能自动选点；工具只能报告多个合法 occurrence 并要求用户给出 start byte。不得借 offset 修复之名扩大 span、生成 replacement 或推断授权。

## 结论

三个 fresh 使用者的最终候选分别承担了 `3/8/3` 个 hunk 和 `3/8/3` 个 selection；其中 COURSE 与 GENERAL 的人工 offset 已为零，MODELING 的 8 个 offset 因一次 mismatch 被全量重算。最昂贵的不是不可替代的语义决定，而是 immutable 链重建、晚路由和可确定性派生字段的重复录入。优先实现 P0 的局部 amend，再做 route 预检和 registry 修复，能在不自动生成 replacement、不自动授权的前提下直接削掉主要使用成本。
