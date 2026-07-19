# STRUCTURAL 改写合同

## 目录

1. 适用范围
2. 权限与完成态
3. 准备命令
4. 来源段清单
5. 可移动与锁定边界
6. 改写包格式
7. 映射规则
8. 结构基线与不变量
9. 结构语义复核请求
10. 状态裁决
11. 执行步骤
12. 已知边界

## 1. 适用范围

用户明确要求跨段调整、章节节奏重建、结构性去模板或指定
`intensity=STRUCTURAL` 时读取本文件。普通词句润色、段内重组和相邻重复压缩不读取。

本合同只管理结构权限和结构证据。它不判断物理、数学、法学、史实或引用是否正确，也不把
结构映射理由当作语义证明。

## 2. 权限与完成态

当前长文工具有两层互不替代的自动权限：

- 默认 `structural_transaction_scope=NONE`：只允许同一 unit 内重排机械可移动的完整段落，
  chunk 继续固定 `structural_scope=UNIT`、`title_lock=true`、
  `structural_cross_unit_moves_allowed=false`；
- 显式 `structural_transaction_scope=ADJACENT_PAIR`：prepare 只为同一物理文件、同一 heading、
  源区间物理相邻、part 连续、scene/Voice 相同且 reciprocal context 的两个 `PENDING` unit
  冻结候选。它允许完整来源段在这两个成员之间移动，但不改变普通 unit bundle 的权限；
- 两层都不允许拆分、遗漏或复制来源段，不允许单独移动公式、引语、命令或其他保护占位符；
- 两层都不允许改标题、跨文件、跨 heading、删除整段或把 `STRUCTURAL` 当作随机打散和改动配额。

transaction inventory 只证明“用户显式开放了这个机械 scope，且该 pair 满足冻结谓词”。它不是
执行请求，也不是语义 clearance。只有提交精确绑定某个 `STX-*` 候选的 transaction bundle，
finalizer 才能形成运行态机械执行授权；实际跨 unit 移动后的结构语义固定为
`NOT_EVALUATED`。

inventory 为 `READY` 后还形成独立的候选处置义务。每个冻结 `STX-*` 必须恰好进入：精确绑定的
`EXECUTED`、精确绑定且有两侧证据的 `DECLINED`，或未处置的 `PENDING`。普通 unit 的
`REWRITE/NO_CHANGE` 回答“该 unit 如何处理”，不能回答“这个 pair 候选是否审阅”；因此两个
member 都 `NO_CHANGE` 也不能静默替代 transaction disposition。任一候选 `PENDING` 时，
`structural_transaction_candidate_coverage_status=REVIEW`，正式覆盖声明与 `rendered/` 发布均被阻断。

需要跨非相邻 unit、跨小节/文件、改标题、改层级、删除整个段落或重分章节时，当前自动
finalizer 仍不具备对应证明面。可以给人工审阅的拟议 patch，但状态保持
`REVIEW/UNRESOLVED`；不得写 `humanize_completion_claim_allowed=true`。

结构权限门与措辞质量门正交。无论是 standalone unit 还是 transaction fragment，只要最终决策为
`REWRITE/NO_CHANGE`，机械 validator 都必须为实际 before/after 生成 paired-quality request。
结构语义 request 回答“段落移动后的篇章关系是否成立”；paired-quality request 回答“逐处措辞变化
是否有独立收益、是否新增搭配/主语/节奏缺陷”。任何一类 request pending 都不能被另一类 PASS 覆盖。

## 3. 准备命令

```powershell
python scripts/prepare_humanize_long_document.py manuscript.tex `
  --output run-structural `
  --scene AUTO `
  --intensity STRUCTURAL
```

只在用户明确授权相邻双 unit 原子事务时追加：

```powershell
python scripts/prepare_humanize_long_document.py manuscript.tex `
  --output run-structural-pair `
  --scene AUTO `
  --intensity STRUCTURAL `
  --structural-transaction-scope ADJACENT_PAIR
```

准备器把强度冻结到 `run_metadata.json`、`units.jsonl`、初始账本和每个 chunk。后续修改这些
字段并重算普通文件哈希不能升级权限；finalizer 会从冻结 source 重建同一清单。

没有 `--intensity STRUCTURAL` 的 run 不接受 `structural_plan` 或
`ADJACENT_PAIR`。STRUCTURAL run 的普通 unit `REWRITE` 必须带 plan；`NO_CHANGE` 不带 plan，
只给具体理由。transaction 使用独立 bundle schema，不能把两个普通 unit bundle 拼成事务；
拒绝执行候选时另交 decline bundle，不能把 unit 理由复制成未绑定的 pair 理由。

## 4. 来源段清单

每个 STRUCTURAL chunk 包含：

```json
{
  "structural_plan_schema": "humanize-structural-plan/v1",
  "structural_scope": "UNIT",
  "structural_title_lock": true,
  "structural_cross_unit_moves_allowed": false,
  "structural_inventory_sha256": "<64-hex>",
  "structural_paragraphs": [
    {
      "paragraph_id": "P002-<12-hex>",
      "ordinal": 2,
      "sha256": "<64-hex>",
      "author_chars": 42,
      "responsibility": "EXPOSITION",
      "protected_ids": ["F00001-P00003"],
      "movable": true,
      "lock_reason": ""
    }
  ]
}
```

`paragraph_id` 绑定来源段精确字节，不是模型可重命名的标签。`protected_ids` 绑定该段原本拥有的
占位符。`movable=true` 只表示编码规则没有发现硬锁；不表示移动后论证必然正确。

### 4.1 相邻 pair inventory

prepare 始终生成 `structural_transaction_inventory.json`：非 STRUCTURAL 为
`NOT_APPLICABLE`，STRUCTURAL + `NONE` 为 `DISABLED`，已授权但没有候选为 `EMPTY`，存在候选为
`READY`。每个候选使用 `humanize-structural-adjacent-pair-transaction/v1`，并绑定：

- snapshot ID 与 snapshot 文件 SHA-256；
- 全部 unit candidate basis hash 与 eligibility policy hash；
- source file SHA-256、heading path、scene 和完整 Voice projection；
- 按物理顺序固定的 `LEFT/RIGHT` compound refs；每个 ref 绑定 unit、part、start/end、
  chunk binding 与 unit structural inventory；
- `left.end == right.start`、双向 context 互指和连续 file-unit ordinal；
- `transaction_id=STX-<binding-prefix>`、完整 `transaction_binding_sha256` 与 inventory 总 hash。

权限字段必须同时读取：

```text
mechanical_scope_permission_granted=true
candidate_inventory_is_execution_request=false
inventory_alone_execution_authorized=false
bound_transaction_bundle_required=true
semantic_clearance_granted=false
```

这五项防止两种相反误读：不能因为 inventory 存在就自动执行，也不能拿
`inventory_alone_execution_authorized=false` 永久否决已经提交了精确绑定 bundle 的合法事务。
finalizer 还必须从冻结 `source/` 独立重建 inventory；攻击者同时修改 JSON 和重算
`prepare_integrity.json` 不能升级 pair 权限。

`ADJACENT_PAIR` 不自动降低 `max_author_chars`、拆开原本完整的小节或跨 heading 制造候选。默认
分块预算下没有满足条件的 pair 时，inventory 合法状态就是 `EMPTY`。只有任务本身需要更细的完整
段落组，并且调用方显式调整分块预算后，才按新快照重新 prepare；不要为提高候选数修改旧 run 的
unit、part 或边界。

## 5. 可移动与锁定边界

以下段落固定锁定：

- 标题或不足以形成独立作者正文的短块；
- 含正式陈述/题干环境、verbatim、整段陈列数学、直接引语、关键 TeX 命令或注释；
- 明确承担 `DEFINITION/SETUP/CONDITION/DERIVATION/PROCEDURE/RESULT/SUMMARY/TRANSITION` 职责；
- 明确依赖前文的“其中、此时、代入、同理、上式、由此、因此、所以、于是”等段首；
- 以冒号结束并引出下一结构块的段落；
- 无法可靠分段或保护跨度穿越 unit 边界的内容。

普通内联数学和普通 TeX 文字命令可以随完整来源段移动。它们不能离开该来源段映射，也不能在
目标段内改值、改命令或改变出现顺序。

规则分类是保守启发式。`EXPOSITION` 仍可能在真实论证中依赖前文；因此发生实际移动时，
`structural_semantic_mapping` 固定为 `NOT_EVALUATED`，不得由模型理由升级为 PASS。

## 6. 改写包格式

### 6.1 单 unit bundle

STRUCTURAL `REWRITE` 使用 strict JSON：

```json
{
  "unit_id": "U-...",
  "chunk_binding_sha256": "<chunk hash>",
  "voice_profile_sha256": "<voice hash>",
  "decision": "REWRITE",
  "masked_text": "目标完整占位文本",
  "keep_reasons": {},
  "structural_plan": {
    "schema_version": "humanize-structural-plan/v1",
    "source_inventory_sha256": "<inventory hash>",
    "target_groups": [
      {
        "source_paragraph_ids": ["P001-..."],
        "target_paragraph_sha256": "<目标段精确 hash>",
        "responsibility": "EXPOSITION",
        "reason": "该段仍承担对象说明，只调整到比较段之前"
      }
    ]
  }
}
```

不要输出代码围栏、批注或 plan 以外的未知字段。每个 `reason` 必须定位该组在目标结构中的职责；
“更自然、更合理、优化结构、降低 AI 味”不是具体理由。

### 6.2 相邻双 unit transaction bundle

transaction 使用独立的 strict JSON schema `humanize-structural-transaction-bundle/v1`：

```json
{
  "schema_version": "humanize-structural-transaction-bundle/v1",
  "transaction_id": "STX-...",
  "transaction_binding_sha256": "<prepare candidate binding>",
  "transaction_inventory_sha256": "<structural_transaction_inventory inventory_sha256>",
  "unit_bindings": [
    {
      "unit_id": "U-left",
      "chunk_binding_sha256": "<left chunk hash>",
      "voice_profile_sha256": "<left Voice hash>"
    },
    {
      "unit_id": "U-right",
      "chunk_binding_sha256": "<right chunk hash>",
      "voice_profile_sha256": "<right Voice hash>"
    }
  ],
  "fragments": [
    {
      "target_unit_id": "U-left",
      "masked_text": "左侧目标完整占位文本",
      "keep_reasons": {},
      "target_groups": [
        {
          "source_refs": [
            {"unit_id": "U-right", "paragraph_id": "P001-..."}
          ],
          "target_paragraph_sha256": "<目标段精确 hash>",
          "responsibility": "EXPOSITION",
          "reason": "完整说明该段移到左侧后仍承担的职责"
        }
      ]
    },
    {
      "target_unit_id": "U-right",
      "masked_text": "右侧目标完整占位文本",
      "keep_reasons": {},
      "target_groups": [
        {
          "source_refs": [
            {"unit_id": "U-left", "paragraph_id": "P002-..."}
          ],
          "target_paragraph_sha256": "<目标段精确 hash>",
          "responsibility": "EXPOSITION",
          "reason": "完整说明该段移到右侧后仍承担的职责"
        }
      ]
    }
  ]
}
```

`transaction_id`、binding 与 inventory hash 必须逐字引用 prepare 候选，不能由 bundle 自创
snapshot、pair 或 source inventory。`unit_bindings` 和 `fragments` 都恰好为 2，顺序由源文件
`(file_id,start)` 固定。来源身份一律使用 `{unit_id, paragraph_id}`；裸 paragraph ID 在跨 unit
范围内有歧义，必须拒绝。两个目标 fragment 都必须非空；若无法让联合来源完整落入两个非空
fragment，应返回 `UNRESOLVED`。

### 6.3 候选 decline bundle

连续阅读 pair 与两侧外部上下文后，若不执行某个冻结候选，提交 strict JSON：

```json
{
  "schema_version": "humanize-structural-transaction-decline/v1",
  "decision": "DECLINE",
  "transaction_id": "STX-...",
  "transaction_binding_sha256": "<prepare candidate binding>",
  "transaction_inventory_sha256": "<inventory hash>",
  "unit_bindings": [
    {
      "unit_id": "U-left",
      "chunk_binding_sha256": "<left chunk hash>",
      "voice_profile_sha256": "<left Voice hash>"
    },
    {
      "unit_id": "U-right",
      "chunk_binding_sha256": "<right chunk hash>",
      "voice_profile_sha256": "<right Voice hash>"
    }
  ],
  "reason_code": "QUESTION_ANSWER_PAIRING_RISK",
  "reason": "两侧段落分别服务于各自题干，跨单元移动会打乱题解对应关系",
  "evidence_refs": [
    {"unit_id": "U-left", "paragraph_id": "P001-..."},
    {"unit_id": "U-right", "paragraph_id": "P001-..."}
  ]
}
```

`reason_code` 只接受：

```text
NO_CROSS_UNIT_STYLE_GAIN
DEPENDENCY_OR_REFERENT_RISK
CLAIM_EVIDENCE_ORDER_RISK
QUESTION_ANSWER_PAIRING_RISK
PROTECTED_BOUNDARY_RISK
USER_SCOPE_LOCK
MEMBER_COMMITTED_TO_OTHER_TRANSACTION
OTHER_REVIEWED_NO_CHANGE
```

理由至少含 8 个汉字，并说明对象、依赖、顺序、保护边界、用户锁或可观察的无收益；“已经审阅、
无需调整、结构合理”之类状态复述不能通过。`evidence_refs` 不得重复，必须命中冻结来源段，并至少
覆盖两个 member 各一个来源段。decline 不占用 member，故重叠边可以分别 decline；但每条边都要
独立工件。一个 transaction ID 同时出现 execution 与 decline 时整批拒绝。decline 只闭合候选
处置，不把 member 从 `PENDING` 变成 `NO_CHANGE`，也不运行正文改写 validator。

## 7. 映射规则

finalizer 逐项执行：

1. 重建来源段清单并核对 inventory hash；
2. 要求每个来源 `paragraph_id` 恰好出现一次；
3. 要求目标组数量等于目标正文实际段落数；
4. 要求每个目标段 hash 与 `masked_text` 精确一致；
5. 合并时只接受来源中相邻且顺序不变的段；
6. 合并来源必须具有同一显式职责；
7. 锁定段必须保持单独成组并处于原 ordinal；
8. 目标段重新分类后必须保留来源显式职责；
9. 目标段的保护 ID 序列必须等于其来源组原有保护 ID 序列；
10. plan 不得映射到 chunk 外部或只读相邻上下文。

任一项失败时，该 unit 为 `UNRESOLVED`，候选不进入派生全文。

### 7.1 transaction 的全局 claim 与联合映射

finalizer 在读取任一正文前先收集全部 bundle 并建立全局 member claim：

1. 一个 unit 不能同时提交 standalone bundle 和 transaction；
2. 一个 unit 不能属于两个 transaction；prepare 可以列出重叠候选边，但一次 finalize 只能选择
   不共享 member 的 transaction 集；
3. transaction 必须精确命中一个冻结 `STX-*`，两个 member、顺序、chunk、Voice、inventory 和
   binding 全部一致；
4. 两个 unit 的全部复合来源 ref 在全部 target group 中全局恰好出现一次；禁止第三 unit、重复、
   遗漏、拆分一个来源段或使用裸 paragraph ID；
5. 一个 target group 合并多个来源段时，它们必须在 pair 联合源序列中连续、顺序不变、职责相同；
6. `movable=false` 的锁定段必须留在原 target unit 和原锚点；可移动段可以在 pair 内换 target unit；
7. 目标段保护 ID 序列必须等于其 `source_refs` 所属完整来源段保护 ID 的串接结果；保护项不能脱离
   来源段，也不能在两个 fragment 间单独交换；
8. 两个 target fragment、目标段 hash 与各自 `masked_text` 必须精确一致且均非空。

collector 发现 member 冲突时，必须在正文 validator 前拒绝整批冲突事务。不能先接受一个普通
bundle，再用后出现的 transaction 覆盖它。

### 7.2 候选处置闭集

finalizer 必须以冻结 inventory 为全集，而不是以 rewrites 目录为全集构造 disposition：

1. transaction ID、inventory、binding、两个 member、chunk 与 Voice 全部通过 envelope 绑定后，
   记 `EXECUTED`；后续 fragment/DOCUMENT/repetition 失败仍属于“已执行并回滚”，unit 保持
   `UNRESOLVED`，但候选不再冒充未审阅；
2. decline 通过同一 envelope 绑定，并通过理由、证据 ref 与双 member 覆盖后，记 `DECLINED`；
3. 其余冻结候选记 `PENDING`。伪造 ID、stale binding 或单侧证据不能占据 disposition；
4. `total = executed + declined + pending` 必须成立。重叠候选逐 ID 计算，不因共享 member 合并；
5. `EMPTY` inventory 的 coverage 为 `PASS`；`NOT_APPLICABLE/DISABLED` 为 `NOT_APPLICABLE`；
   `READY` 且 `pending=0` 为 `PASS`，否则为 `REVIEW`；
6. `structural_transaction_scope_complete` 在非适用 scope 为 `null`，在 `EMPTY` 或全部处置时为
   `true`，存在 `PENDING` 时为 `false`。

机器可读结果必须保存逐 ID `structural_transaction_candidate_dispositions`、四项计数、
`structural_transaction_candidate_coverage_status`、`structural_transaction_scope_complete` 和
`structural_transaction_decline_results`。最后一项只收录已通过 strict schema、冻结 envelope、理由与
双 member 证据门的规范化 decline 验证记录；它不是全部候选清单，也不能替代 disposition 闭集。
只看 `structural_transactions_total` 会漏掉 decline 与未处置候选，不得用于覆盖声明。

## 8. 结构基线与不变量

合法结构变更不能直接用“原全文保护项全局顺序不变”检查，否则随段整体移动的数字、公式和引用
会被误报。finalizer 先按已校验 plan 生成一份结构基线：

1. 只移动来源完整段，不改任何字；
2. 相邻合并组只把原段按原顺序连接；
3. 恢复每个来源段原有保护内容；
4. 用结构基线与候选逐 unit 运行统一验证器；
5. 用结构基线全文与派生全文再次运行 DOCUMENT 级不变量。

因此，“值随段移动”可以通过；“值离开来源段、值被改写、公式被单独搬走、标题或环境被移动”
仍失败。结构基线只证明候选符合声明的机械映射，不证明重排后的论证顺序正确。

transaction 对两个 fragment 分别建立只移动原字节的结构基线，并分别运行 FRAGMENT validator；
再把两个 baseline 与两个 candidate 同时组装回冻结全文，运行一次 DOCUMENT gate。只有

```text
left fragment gate = PASS
right fragment gate = PASS
document gate = PASS
```

三项全部成立时，才能一次性提交两个 replacement、两个 ledger 终态、两份 diff 和一份 transaction
review request。任一项为 `FAIL/REVIEW`、任一保护恢复失败，或后置跨 unit repetition 命中任一
member，都必须扩展到整个 transaction：双方共同回滚、`accepted_member_count=0`、
`published_member_count=0`，不得留下单边 diff、DONE 或派生正文。

## 9. 结构语义复核请求

机械 plan 通过且实际移动或合并时，finalizer 必须生成
`humanize-structural-semantic-review-request/v1`。请求至少绑定：

- snapshot、unit、chunk 与 Voice hash；
- 来源 inventory、structural plan、原 unit、结构基线和候选 hash；
- 前后只读上下文 hash；
- 每个移动/合并 delta 的来源段 ID、原 ordinal、目标 ordinal、职责、理由和目标段 hash；
- hard invariant 状态、言语行为 warning 与 validator/invariant/scanner/lexicon/report-extractor/runtime 六项 policy hash；
- finalizer 与 prepare 脚本 hash；
- 篇章依赖、因果/证据范围、否定/模态/焦点/条件和段落职责复核维度。

artifact ref 使用提交后的 `validation/...` 相对路径，不得保存会在 finalize 后失效的
`.validation_staging` 绝对路径。`request_sha256` 对除自身外的规范 JSON 计算，换稿后不能复用。

当前本地工具只签发请求，不消费语义 clearance。请求固定写
`local_clearance_supported=false/external_signature_verified=false`。模型 reason、warning proposal、
调用方自称 `HUMAN/VERIFIED_HUMAN`、自填 receipt 或可重算哈希均不能升级状态。真正放行需要代理
不可访问私钥的外部审批服务，绑定 request、artifact、逐 delta verdict、篇章连贯性、policy、
有效期和签名；该验签入口当前未实现。

无外部服务时，可继续修改候选，使普通 warning 在新 artifact 上消失；即便 warning 消失，实际
结构移动仍保持 `NOT_EVALUATED`。请求用于明确人工审阅对象，不把模型复核包装成人工审批。

本节 request 不替代 `humanize-paired-quality-review-request/v1`。后者由统一 validator 绑定
before/after、逐 hunk 与 policy，transaction 的两个 fragment 各自生成并由 finalizer 纳入全文
paired-quality coverage。当前本地工具同样不消费 paired-quality clearance；模型 reason、结构
review request、caller 标签和 second pass 均不能把它升级为 PASS。

相邻 pair 生成一个 transaction-level
`humanize-structural-transaction-review-request/v1`，而不是两份可被分别放行的 unit request。它还
必须绑定：

- prepare transaction ID/binding/inventory、pair 顺序、全局 member claims 与内外边界；
- 两个 fragment 的 source/baseline/candidate/validator hash；
- DOCUMENT baseline/candidate/gate hash；
- 全部 `{unit_id, paragraph_id}` 来源 ref、target group、跨 unit delta、保护归属和职责；
- transaction bundle、prepare/finalizer、validator/invariant/scanner/lexicon/report-extractor/runtime 与 transaction policy
  hash。

请求固定写 `semantic_mapping=NOT_EVALUATED`、`local_clearance_supported=false`、
`humanize_completion_claim_allowed=false`。证据文件名由已计算的 bundle hash 派生，不直接信任
调用方 ID，防止路径穿越。换任一 fragment、document gate、policy 或 pair binding 后，旧请求必须
失效。

## 10. 状态裁决

| 条件 | plan | 结构语义 | 顶层交付 / 发布 |
|---|---|---|---|
| 非 STRUCTURAL run | `NOT_APPLICABLE` | `NOT_APPLICABLE` | 按其他门裁决 |
| STRUCTURAL + `NO_CHANGE` | `PASS` | `PASS` | 仍需其他门 |
| 合法 plan，未改变分组/顺序 | `PASS` | `PASS` | 仍需 paired-quality 等其他门 |
| 合法 plan，实际移动或合并，候选组装成功 | `PASS` | `NOT_EVALUATED` | assembly `PASS`，但交付 `REVIEW/2`；只发布 `rendered_review/` |
| 合法 plan，但普通 validator 为 REVIEW | `PASS` | `NOT_EVALUATED` | unit `UNRESOLVED`、总体 `REVIEW/2`；请求保留 warning |
| plan 缺失、伪造或越权 | `REVIEW` | `NOT_EVALUATED` | unit `UNRESOLVED` |
| 合法相邻 pair transaction，双 fragment 与 DOCUMENT gate 全部 PASS，且发生真实跨 unit 移动 | transaction atomic gate `PASS` | `NOT_EVALUATED` | 两 member 原子组装；总体 `REVIEW/2`，只发布完整 `rendered_review/` |
| transaction 任一 member/保护/validator/DOCUMENT/repetition 门失败 | `ROLLED_BACK` | `NOT_EVALUATED` | 两 member 共同 `UNRESOLVED`，零 member diff/发布；其他独立 unit 仍按自身状态处理 |
| transaction 绑定、权限、member claim 或复合 ref 越权 | `REVIEW` 或硬完整性 `FAIL` | `NOT_EVALUATED` | 正文验证前拒绝；不得保留半边结果 |
| `READY` 候选有合法 decline，且 member 分别完成 `REWRITE/NO_CHANGE` | disposition `DECLINED` | `PASS`（未发生移动） | 候选覆盖可 PASS；最终交付仍由 paired-quality、unit、Voice、重复和其他门决定 |
| `READY` 候选只有普通 unit `NO_CHANGE`，无 execution/decline | disposition `PENDING` | `NOT_EVALUATED` | assembly 与 delivery 均 `REVIEW/2`，覆盖声明 false，不发布正式 `rendered/` |
| 重叠候选只处置其中一条 | 已处置边 `EXECUTED/DECLINED`，其余 `PENDING` | 按各边 | scope incomplete；共享 member 不替代逐边 disposition |

`structural_plan_status=PASS` 的含义是“plan 与字节、段落、职责和保护归属合同一致”。不得缩写成
“结构语义正确”。实际移动后，即使候选组装没有硬失败，`status` 与 `delivery_gate_status` 也必须
一致保持 `REVIEW/2`；不能只读取 `candidate_assembly_status=PASS`。`rendered_review/` 是完整待审
候选，不是最终 `rendered/`。transaction 还必须进入 `structural_changes_applied` 和语义 request
计数；不能因为 pair 内全局段序看似连续或两个 fragment 分别 PASS，就漏计真实边界迁移并误发
`rendered/`。

## 11. 执行步骤

1. 确认用户明确授权 STRUCTURAL 和实际 scope；
2. 默认运行 unit scope prepare；只有用户明确授权相邻双 unit 时才追加
   `--structural-transaction-scope ADJACENT_PAIR`；
3. 读取全部 PENDING chunk；transaction 还要读取并核对
   `structural_transaction_inventory.json` 的 scope permission、`STX-*`、binding 与两个 compound refs；
4. 连续阅读完整 unit 与只读前后文；pair 必须同时连续阅读两个 member 和外侧上下文；
5. 先决定是否需要结构变化，`BALANCED` 已足够时不要强行移动；不执行时仍为该 `STX-*` 写
   精确 decline，而不是只给两个 unit 写 `NO_CHANGE`；
6. 只从 `movable=true` 段中提出跨 target unit 的组；锁定段留在原 unit；
7. 普通 plan 使用 unit 内 paragraph ID；transaction 逐组使用 `{unit_id, paragraph_id}`，登记职责和
   具体理由，并确认联合清单恰好一次；
8. 生成一个或两个完整 `masked_text` 后计算每个目标段 hash；transaction 两个 fragment 都非空；
9. 对 inventory 中每个候选核对 disposition；重叠边也逐项提交。运行 finalizer，读取 member
   claim、两个 fragment gate、DOCUMENT gate、原子回滚、candidate coverage 和全文发布状态；
10. 实际移动时同时读取 unit/transaction 结构语义 request 与全部 paired-quality request，披露
   `structural_semantic_mapping=NOT_EVALUATED`、
   `paired_quality_gate_status=PENDING_EXTERNAL_REVIEW` 和 `delivery_gate_status=REVIEW`；
11. review candidate 不能作为 fresh second-pass clean seed；即使两个 member 在另一次运行中都给出
   `NO_CHANGE`，也不能清除第一遍未评估的 transaction 结构语义；
12. 需要全文完成声明时按长文工作流执行独立收敛检查，但它不能清除未评估的结构语义。

## 12. 已知边界

- 当前只支持同一文件、同一 heading 内、物理相邻且满足完整冻结谓词的两个 unit 原子搬运；
- 当前不支持三个以上 unit 的单事务；prepare 可以生成重叠候选边，但一次 finalize 不能让同一
  member 被两个 transaction 占用；未执行的重叠边仍须分别 decline，否则保持 `PENDING`；
- 当前不支持标题解锁、章节增删或层级变化；
- 当前不支持来源段拆分和整段删除的可机械映射；
- 职责分类只覆盖显式句式，不是完整篇章分析；
- 本地模型生成的 reason 不是人工审批或语义认证；
- 当前没有外部签名 receipt 验证入口，故实际结构变化只能到 `rendered_review/`；
- 当前也没有 paired-quality response 的可信验签入口；即使没有实际结构变化，普通
  `REWRITE/NO_CHANGE` 完整候选仍只能到 `rendered_review/`；
- `rendered_review/` 不能进入 fresh second pass，也不能与新正式 `rendered/` 互相覆盖；失败重跑须
  保留已发布的旧 review candidate；
- `semantic_mapping=NOT_EVALUATED` 不能由 validator PASS、测试通过或模型自述升级；
- GPT 语料可用于负例和测试输入，不能作为结构正例或作者 Voice 证据。
