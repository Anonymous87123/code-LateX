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

当前长文工具的自动 STRUCTURAL 面固定为：

- `scope=UNIT`；
- `title_lock=true`；
- `cross_unit_moves_allowed=false`；
- 允许重排同一 unit 内机械可移动的完整段落；
- 允许把来源中相邻、同职责、均可移动的段落合成一个目标段；
- 不允许拆分一个来源段；
- 不允许遗漏、复制或跨 unit 搬运来源段；
- 不允许单独移动公式、引语、命令或其他保护占位符；
- 不允许把 `STRUCTURAL` 当作随机打散、追求段长差异或改动配额。

需要跨 unit、跨小节、改标题、改层级、删除整个段落或重分章节时，当前自动 finalizer 不具备
对应证明面。可以给人工审阅的拟议 patch，但状态保持 `REVIEW/UNRESOLVED`；不得写
`humanize_completion_claim_allowed=true`。

## 3. 准备命令

```powershell
python scripts/prepare_humanize_long_document.py manuscript.tex `
  --output run-structural `
  --scene AUTO `
  --intensity STRUCTURAL
```

准备器把强度冻结到 `run_metadata.json`、`units.jsonl`、初始账本和每个 chunk。后续修改这些
字段并重算普通文件哈希不能升级权限；finalizer 会从冻结 source 重建同一清单。

没有 `--intensity STRUCTURAL` 的 run 不接受 `structural_plan`。STRUCTURAL run 的
`REWRITE` 又必须带 plan；`NO_CHANGE` 不带 plan，只给具体理由。

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

## 9. 结构语义复核请求

机械 plan 通过且实际移动或合并时，finalizer 必须生成
`humanize-structural-semantic-review-request/v1`。请求至少绑定：

- snapshot、unit、chunk 与 Voice hash；
- 来源 inventory、structural plan、原 unit、结构基线和候选 hash；
- 前后只读上下文 hash；
- 每个移动/合并 delta 的来源段 ID、原 ordinal、目标 ordinal、职责、理由和目标段 hash；
- hard invariant 状态、言语行为 warning 与 validator/invariant/scanner/lexicon policy hash；
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

## 10. 状态裁决

| 条件 | plan | 结构语义 | 顶层交付 / 发布 |
|---|---|---|---|
| 非 STRUCTURAL run | `NOT_APPLICABLE` | `NOT_APPLICABLE` | 按其他门裁决 |
| STRUCTURAL + `NO_CHANGE` | `PASS` | `PASS` | 仍需其他门 |
| 合法 plan，未改变分组/顺序 | `PASS` | `PASS` | 仍需其他门 |
| 合法 plan，实际移动或合并，候选组装成功 | `PASS` | `NOT_EVALUATED` | assembly `PASS`，但交付 `REVIEW/2`；只发布 `rendered_review/` |
| 合法 plan，但普通 validator 为 REVIEW | `PASS` | `NOT_EVALUATED` | unit `UNRESOLVED`、总体 `REVIEW/2`；请求保留 warning |
| plan 缺失、伪造或越权 | `REVIEW` | `NOT_EVALUATED` | unit `UNRESOLVED` |

`structural_plan_status=PASS` 的含义是“plan 与字节、段落、职责和保护归属合同一致”。不得缩写成
“结构语义正确”。实际移动后，即使候选组装没有硬失败，`status` 与 `delivery_gate_status` 也必须
一致保持 `REVIEW/2`；不能只读取 `candidate_assembly_status=PASS`。`rendered_review/` 是完整待审
候选，不是最终 `rendered/`。

## 11. 执行步骤

1. 确认用户明确授权 STRUCTURAL 和实际 scope；
2. 运行 prepare 并读取全部 PENDING chunk；
3. 连续阅读完整 unit 与只读前后文；
4. 先决定是否需要结构变化，`BALANCED` 已足够时不要强行移动；
5. 只从 `movable=true` 段中提出组；
6. 逐组登记来源 ID、职责和具体理由；
7. 生成完整 `masked_text` 后计算每个目标段 hash；
8. 运行 finalizer，读取结构证据、unit validator 和全文门；
9. 实际移动时读取 `.structural-semantic-review-request.json`，披露
   `structural_semantic_mapping=NOT_EVALUATED/delivery_gate_status=REVIEW`；
10. 需要全文完成声明时按长文工作流执行独立收敛检查，但它不能清除未评估的结构语义。

## 12. 已知边界

- 当前不支持跨 unit 事务式搬运；
- 当前不支持标题解锁、章节增删或层级变化；
- 当前不支持来源段拆分和整段删除的可机械映射；
- 职责分类只覆盖显式句式，不是完整篇章分析；
- 本地模型生成的 reason 不是人工审批或语义认证；
- 当前没有外部签名 receipt 验证入口，故实际结构变化只能到 `rendered_review/`；
- `semantic_mapping=NOT_EVALUATED` 不能由 validator PASS、测试通过或模型自述升级；
- GPT 语料可用于负例和测试输入，不能作为结构正例或作者 Voice 证据。
