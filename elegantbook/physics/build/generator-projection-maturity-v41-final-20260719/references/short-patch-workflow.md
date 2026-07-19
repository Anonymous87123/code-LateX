# 短 PATCH 工件合同

## 目录

1. 适用范围
2. 两阶段工作流
3. selection spec
4. bundle 绑定
5. 严格应用与验证
6. 输出工件
7. 状态与退出码
8. 失败处理
9. 已知边界

## 1. 适用范围

当短文或单个可连续阅读的 TeX/Markdown/TXT 范围因未决主张、来源冲突或 high signal 无法交付完整 `CLEAN` 时，使用本合同生成最小 `PATCH`。它解决以下机械问题：

- 把每个动作绑定到精确 UTF-8 来源字节；
- 强制 hunk 有序且互不重叠；
- 强制 `DELETE_STYLE_SHELL/REWRITE/UNRESOLVED` 与 replacement 一致；
- 原样复制未列入 hunk 的全部来源字节；
- 从 bundle 确定性派生候选，不接受调用方另交一份 candidate；
- 在发布前强制运行统一验证器；
- 保留 `UNRESOLVED`、机械状态和 paired-quality 缺口，不制造完成态。

本工具不用于长文 unit、STRUCTURAL 调序、REPORT_INFORMED selection、候选队列、生成资格或外部审批。长文继续使用 `prepare_humanize_long_document.py`、`scaffold_humanize_rewrites.py` 和 `finalize_humanize_long_document.py`。检测报告 selection 继续使用 extractor 和 `--report-scope`。

## 2. 两阶段工作流

优先先生成 source/policy-bound authoring scaffold，避免人工在 hunk 与 selected span 中重复抄写原文：

```powershell
python scripts/scaffold_humanize_short_patch.py create source.tex `
  --scene COURSE --source-kind DOCUMENT `
  --suggest-spans CLAUSE_AND_SENTENCE `
  --output selection.authoring.json --format text
```

scaffold 把 AUTO high inventory、精确 UTF-8 span registry 和所有 candidate high 的 `PENDING`
resolution 绑定到当前 source/policy。authoring v3 默认同时提出 clause 与完整句候选：clause 包含 core、
左分隔符附着和右分隔符附着三种边界，完整句用于避免调用方为句级改写重复手工登记 span；段级边界仍须
显式请求。可用 `NONE/CLAUSE/CLAUSE_AND_SENTENCE/SENTENCE/PARAGRAPH/SENTENCE_AND_PARAGRAPH/ALL/FOCUS` 调整。
默认模式还为 scanner 的 medium/low candidate 生成 advisory 边界；它们固定 `finding_ids=[]`，只有调用方
显式选入后才成为 bound declaration，不进入 high inventory 或 high 处置率。`--focus-spec <json>` 可以
与任一自动边界模式叠加，保留 high/advisory 视图并追加调用方已诊断的 FOCUS span；只需调用方诊断视图
时才把 `--suggest-spans` 设为 `FOCUS`。
多个 high 位于同一候选边界时共用一个建议 span。与引语、数学、代码、TeX 控制序列等保护内容有任何重叠，或超过固定 byte 上限时，
建议只记 `SUPPRESSED + reason_codes`，不会成为可引用 span。编辑者只在 `spans` 中登记一次其余 source
span；`hunks` 与 `selected_spans` 通过 `span_id` 独立引用。填完每个 high 的 `HUNK/KEEP` disposition、
hunk、selection 和显式 conflict 后运行：

每条 `AVAILABLE` 建议必须完整包住其全部 `finding_ids`；high 跨越 clause/句/段边界时，该视图固定为
`SUPPRESSED/FINDING_NOT_FULLY_COVERED`，不得挂接一个随后无法通过 coverage 的窄 span。不同视图若得到
完全相同的可用 UTF-8 范围，只保留最局部的一个建议并共用 registry span；SUPPRESSED 视图仍分别保留，
以免丢失边界与保护原因。TeX 命令调用从反斜杠控制序列起，连同嵌套的 `[]/{}` 参数整体进入早期保护；
Markdown 与 TeX 均执行该门，只有 `%` 注释等格式专属语法仍由 `--document-format` 决定。API 的
`document_format=AUTO` 与 CLI `--document-format AUTO` 等价，均按 `.tex/.ltx` 后缀推断，否则按 Markdown。
在 TeX 模式中，控制序列与参数之间的未转义 `%` 注释会吞掉换行，因此 `\command% comment` 后下一行的
`{...}` 仍属于同一受保护命令调用；不得把注释后的参数误当成独立可编辑正文。

```powershell
python scripts/scaffold_humanize_short_patch.py finalize source.tex `
  --authoring selection.authoring.json `
  --output selection.v2.json --format text
```

finalize 会重新读取 source、重跑当前 AUTO high inventory、比较 scanner/lexicon/runtime policy，拒绝
`PENDING`、source/policy 漂移、悬空/重复 span ID、未覆盖 high、错误 hunk/selection 引用和非法 conflict，
并重算 authoring tool hash、建议 inventory 和建议 span。非 `UNRESOLVED` hunk 与任意保护 span 重叠时
要求拆分，不能等到 apply 才发现。create 在写出前执行与 finalize 相同的 JSON 大小上限，不能生成
自身无法消费的 scaffold。finalize 再确定性展开为现有 `humanize-short-patch-selection/v2`。
scaffold/finalize 成功都不是 bundle 或交付 PASS。

source 没有任何 AUTO high 时 create 返回 `NO_HIGH_FINDINGS/0`，但这既不是 `NO_CHANGE`，也不证明没有
词库外病灶。连续阅读后若有其他可定位问题，优先写 focus spec，让工具做唯一定位、UTF-8 offset、registry
和保护区检查；不能形成精确 focus 时再手工新增 span/hunk。否则停止并由调用方作出 `NO_CHANGE` 候选决策。
原样 finalize 空 scaffold 固定 `NO_PATCH_HUNKS/FAIL`，不使用含混的 spans 结构错误。

focus spec 使用 strict JSON；`source_text` 唯一时 `start_byte` 可为 `null`，重复出现时必须给原始 UTF-8
字节起点：

```json
{
  "schema_version": "humanize-short-patch-focus/v1",
  "spans": [
    {"focus_id": "F001", "source_text": "为了看清 ", "start_byte": null}
  ]
}
```

```powershell
python scripts/scaffold_humanize_short_patch.py create source.tex `
  --scene COURSE --source-kind DOCUMENT `
  --suggest-spans CLAUSE_AND_SENTENCE --focus-spec focus.json `
  --output selection.authoring.json --format text
```

只需要 FOCUS 时仍可使用 `--suggest-spans FOCUS --focus-spec focus.json`。FOCUS 是 additive caller input：
它只把调用方已经诊断的精确片段注册为 suggestion，不扫描全篇生成候选洪水；与数学、引语、代码、TeX
命令调用或其他保护跨度重叠时只生成 `SUPPRESSED`，不发放可引用 `span_id`。focus spec、authoring
scaffold 和选择动作都在调用方可写边界内，因此不证明诊断真实、用户授权或改写收益。

`.txt` 默认按 Markdown 保护语法处理。内容实际为 TeX 时，create、finalize、build 三步都传
`--document-format TEX`；不能依赖文件名猜测 `%` 注释、数学或控制序列。

也可由模型或人工直接写精确 selection spec。随后构建不可歧义的 bundle：

```powershell
python scripts/build_humanize_short_patch.py source.tex `
  --selection-spec selection.json `
  --output patch.bundle.json `
  --format json
```

builder 成功只表示 `BUNDLED/0`，不是候选交付，也不是文风质量 PASS。随后应用 bundle：

```powershell
python scripts/apply_humanize_short_patch.py source.tex `
  --bundle patch.bundle.json `
  --output short-patch-review `
  --format text
```

合法待审候选的文本首行固定为：

```text
DELIVERY REVIEW exit=2
```

不得覆盖源文件、selection spec、bundle 或已有输出目录。任何输入漂移都重建 bundle，不手改 hash 或 offset。

## 3. selection spec

selection spec 使用 `humanize-short-patch-selection/v1` 或 coverage-aware v2；v1 只接受下列闭集字段：

```json
{
  "schema_version": "humanize-short-patch-selection/v1",
  "requested_output": "CLEAN",
  "mode": "REWRITE",
  "scene": "COURSE",
  "intensity": "BALANCED",
  "protected_terms": ["匀变速直线运动"],
  "hunks": [
    {
      "hunk_id": "H001",
      "decision": "DELETE_STYLE_SHELL",
      "source_text": "值得注意的是，",
      "start_byte": null,
      "replacement": "",
      "reason": "删除没有新增信息的重点提示壳。"
    },
    {
      "hunk_id": "H002",
      "decision": "UNRESOLVED",
      "source_text": "若条件冲突，保留原句。",
      "start_byte": null,
      "replacement": "若条件冲突，保留原句。",
      "reason": "来源主张冲突，纯文风层不能裁决。"
    }
  ]
}
```

顶层规则：

- `requested_output` 只用 `CLEAN` 或 `PATCH`；实际输出固定为 `PATCH`；
- `mode` 固定为 `REWRITE`；
- `scene` 使用 `AUTO/GENERAL/COURSE/MODELING/RESEARCH`；
- `intensity` 只用 `LIGHT/BALANCED`，短 PATCH 不开放结构调序；
- `protected_terms` 显式绑定用户要求逐字保留的方法名、材料名和术语；没有时写空数组；
- `hunks` 至少一项；`NO_CHANGE` 不伪装成空 PATCH。

每个 hunk 只接受六个字段。`source_text` 必须是精确原文；同一文本只出现一次时把 `start_byte` 写为 `null`，builder 自动定位。出现多次时必须给 UTF-8 原始字节上的显式 `start_byte`；不得用“第几个相似句”或 Unicode 字符序号猜测。

动作规则：

| decision | replacement | 状态含义 |
|---|---|---|
| `DELETE_STYLE_SHELL` | 必须为空字符串 | 只删除不承载独立命题的句壳 |
| `REWRITE` | 必须非空且不同于 source | 保留输入已有命题后改写 |
| `UNRESOLVED` | 必须逐字等于 source | 候选中原样保留，并使交付保持 REVIEW |

`reason` 必须定位实际原因；`TODO/待定/保持原样/无需修改/已经自然/没有问题` 不合格。reason 不是学术正确性裁决，也不能作为外部 quality clearance。

## 4. bundle 绑定

builder 输出 `humanize-short-patch/v1`。它固定记录：

- 完整 source SHA-256 与字节数；
- 原 selection spec 的原始字节 SHA-256；
- `source_encoding=utf-8` 与 `offset_unit=UTF8_BYTES`；
- requested/effective output、scene、intensity 和 protected terms；
- 每个 hunk 的半开字节范围、source/replacement SHA-256、原文、动作和理由；
- `patch_hunks_source_partition=NON_OVERLAPPING`；
- `unlisted_source_policy=COPY_EXACT`；
- `semantic_judgment=NOT_EVALUATED`；
- 规范 JSON 自哈希 `bundle_sha256`；
- `completion_claim_allowed=false`。

builder 不排序调用方写乱的 hunks。hunk 必须按 source 起点递增；重复 ID、重复 span、包含或部分重叠一律 `FAIL/1`。`REWRITE` 不能包住另一个 `UNRESOLVED`。

字节边界必须同时满足：

- 起止点落在完整 UTF-8 code point 边界；
- 不从 `CRLF` 中间切开；
- 不在 combining mark、ZWJ、variation selector 或 emoji modifier 等明显 grapheme 连接点切开；
- replacement 不新增 NUL、bidi override/isolate 或其他不可见 format control。

这些门只避免确定性编码损坏；不声称实现完整 Unicode grapheme 语义分析。

### 4.1 coverage-aware selection/bundle v2

v1 保持只读和生产兼容，但固定：

```text
coverage_status=NOT_PROVIDED
coverage_completion_claim_allowed=false
```

需要证明可机械枚举范围已逐项处置时，把 selection 升为 `humanize-short-patch-selection/v2`，在 v1 字段外增加：

```json
{
  "coverage": {
    "source_kind": "DOCUMENT",
    "lexical_keeps": [],
    "selected_spans": [
      {
        "selection_id": "S001",
        "source_text": "值得注意的是，",
        "start_byte": null,
        "decision": "HUNK",
        "hunk_id": "H001",
        "reason": "用户把该空重点句壳列入本次处理范围。"
      }
    ],
    "explicit_conflicts": [
      {
        "conflict_id": "C001",
        "rule_code": "OPPOSING_PERMISSION",
        "left_hunk_id": "H010",
        "right_hunk_id": "H011",
        "reason": "两处给出相反许可，纯文风层必须成对保留。"
      }
    ]
  }
}
```

`source_kind` 只接受 `DOCUMENT/INLINE_TEXT/INLINE_SELECTION`。`INLINE_SELECTION` 至少绑定一个精确 selected span。`REPORT_SELECTION` 不接受调用方自填；报告标注必须继续使用 extractor 生成的 report scope 和统一验证器 `--report-scope`。

builder 固定使用 scanner 的 `AUTO` audit view 枚举 source 中全部 high finding，不允许用较窄任务 scene 漏掉其他场景的 high；coverage 同时保存任务 `scene` 与 `scan_scene=AUTO`。inventory 包括候选、保护区和技术豁免：

- candidate high 必须完整落入唯一 hunk，或在 `lexical_keeps` 中以 `signal_id + source_text + UTF8 start_byte + 具体理由` 精确 KEEP；
- protected/excluded high 分别登记 `PROTECTED/EXCLUDED`，不能伪装成已改写；
- protected/excluded high 与任一 hunk 有任何字节重叠时固定 `NON_EDITABLE_HIGH_OVERLAPS_HUNK/FAIL`；
- 不对应真实 high occurrence 的 keep 固定 `UNKNOWN_LEXICAL_KEEP/FAIL`；
- 未处置 high 固定 `UNCOVERED_LEXICAL_HIGH/FAIL`；
- selected span 的 `HUNK` 必须与指定 hunk 精确同 span；`KEEP` 必须令 `hunk_id=null`；
- authoring scaffold 中的 selected spans 必须两两不重叠；同一 finding 的 clause/句/段边界只能显式选择一个；
- selected `KEEP` 与任一 hunk 重叠时固定 `SELECTION_KEEP_OVERLAPS_HUNK/FAIL`；
- explicit conflict 的左右 hunk 必须不同、不得跨 pair 复用，且都为逐字原样的 `UNRESOLVED`。

`rule_code` 只接受 `OPPOSING_PERMISSION/MUTUALLY_EXCLUSIVE_CONDITION/CONTRADICTORY_CONCLUSION/
INCOMPATIBLE_SCOPE/OTHER_DECLARED_CONFLICT`。最后一项只说明调用方声明了其他冲突，不证明该判断真实。
ID 引用大小写必须与声明完全一致；只在大小写上不同的 selection/conflict ID 也视为重复。reason 去除
尾部空白和中英文句末标点后仍为 `TODO/待定/保持原样/无需修改/已经自然/没有问题` 时固定拒绝。

v2 bundle 内嵌当前 `humanize-short-patch-coverage/v2`，bundle 自哈希绑定完整 coverage。coverage 又绑定 source、任务 scene、`scan_scene=AUTO`、document format、resolved declarations、scanner/lexicon/coverage builder/runtime policy、三个 inventory、逐项 disposition 和自哈希。早期 coverage/v1 仅只读兼容；通过自身完整性检查后因旧 policy 保持 `REVIEW/2`，不按 v2 语义静默升级。apply 发布前按当前 coverage policy 重算；verifier 在不破坏旧记录的前提下把 policy value 或 key-set drift 分为 `REVIEW/2`，同 policy inventory 不一致为 `FAIL/1`。

coverage PASS 的固定范围是：

```text
coverage_claim_scope=ENUMERATED_HIGH_AND_BOUND_DECLARATIONS_ONLY
coverage_completion_claim_allowed=true
semantic_completeness_claim_allowed=false
NO_COMPLETE_NATURAL_LANGUAGE_SEMANTIC_DISCOVERY
CONFLICT_INVENTORY_IS_CALLER_DECLARED_ONLY
```

它证明当前 scanner high、调用方给出的 selected spans 和调用方声明的 conflict pairs 都有且只有可复核处置；不证明 scanner 发现了所有 AI 味，不证明调用方没有漏报 selection/冲突，也不证明 KEEP 理由真实、改后更自然或学术内容正确。

### 4.2 authoring scaffold v1/v2/v3

`humanize-short-patch-selection-authoring/v1|v2|v3` 都不是 builder 输入或 evidence。v1/v2 只读兼容；v2 新增
`authoring_tool_sha256`、`span_suggestion_policy`、`span_suggestions` 与
`authoring_integrity_scope=CALLER_CONTROLLED_SELF_CONSISTENCY_ONLY`。source、configuration、policy、
high inventory 和建议 inventory 会被 finalize 重算。v3 再加入 source-bound `focus_spans`，把 strict
focus spec 的唯一定位结果纳入 inventory hash，并在 finalize 时重放。可发现普通编辑、漂移和错误引用；但所有内容及
摘要都位于同一调用方可写边界，调用方仍能协同改值并重封，故不得称“不可篡改”或“用户授权已证明”。

自动 high span 必须保留 `finding_ids` 精确绑定，不得改宽。可用的建议 span 已以 `finding_ids=[]` 进入
registry，调用方可直接引用；medium/low advisory 与 FOCUS suggestion 同样保持 `finding_ids=[]`，不能冒充
high coverage。SUPPRESSED suggestion 没有 span_id。建议不含 decision、replacement、
reason、hunk_id、selection_id、conflict_id 或 authorized 字段。需要其他边界时新增一个
`finding_ids=[]` 的手工 span，不复制到 hunk/selection。finalize 输出显式 byte offset 的 v2 selection，
再由正式 builder 重验完整 coverage。任何本地 authoring 文件都不能证明 selection 来自外部用户请求。
同一可用 byte range 跨视图只发放一个 suggestion；`kind/boundary_variant` 表示保留下来的最局部视图，
不是丢失了另一份可编辑文本。调用方需要更宽且不同的范围时，使用对应非重复建议或登记手工 span。

## 5. 严格应用与验证

applicator 必须执行以下顺序：

1. 重新读取 source 与 bundle，严格拒绝非法 UTF-8、重复 JSON key、浮点/非有限数、未知字段和过深结构；
2. 重算 bundle 自哈希、source hash、每个 span/hash、动作/replacement 和非重叠分区；
3. 按字节把所有未列出区间 `COPY_EXACT`，确定性生成 candidate；
4. 在 staging 内保存初始 source 冻结快照，统一验证器只读取该快照和派生 candidate，不读取可并发替换的 live source；
5. 把 bundle 中的 `protected_terms` 逐项传给统一验证器；
6. 核对 validator 的实际进程退出码、顶层状态、机械状态、hard layer 以及 before/after SHA；
7. validator `FAIL/1`、hash 不一致、状态元组矛盾或任何运行时异常时删除整个 staging；
8. 发布前再次读取 live source 和 bundle；任一字节漂移都回滚；
9. 只把完整闭集目录重命名到一个原先不存在的输出路径。

统一验证器的 `PASS` 只表示已编码的机械门通过；它不能证明学术正确性、语义蕴含、作者身份或文风收益。applicator 即使收到 mechanical PASS，也因 paired-quality 未获可信外部 clearance 而保持顶层 REVIEW。

## 6. 输出工件

一次成功组装发布以下工件：

```text
source.snapshot.bin
candidate.review.<tex|md|txt>
review.md
patch.diff
patch.bundle.json
validation.json
result.json
evidence-manifest.json
```

coverage-aware v2 另增加 `coverage.json`，其内容必须与 bundle 内嵌 coverage 逐字段相同；删项、增项或单独重封 manifest 都会被 verifier 拒绝。

当前 applicator 使用 `humanize-short-patch-result/v2` 并固定发布 `review.md`。该视图由 bundle、result 和
validation 确定性生成，同时列出 changed hunk、普通 diff 看不到的 unchanged UNRESOLVED、显式 conflict
pair、coverage scope 和质量/学术边界；所有 source/replacement 均 HTML escape，不执行其中的 Markdown
或 HTML。verifier 会重算整份字节，篡改后即使重封 manifest 仍为 `FAIL/1`。旧 result v1 没有
`review.md` 时只读兼容，显示 `review_artifact_status=NOT_PROVIDED`。

当前 `result.json` 使用严格字段闭集，并把 `review_path`、`coverage_claim_scope`、任务 `coverage_scene`、`coverage_scan_scene=AUTO` 与 `coverage_source_kind` 和布尔值一起输出。未知路径字段、伪 `semantic_judgment=PASS`、伪 paired-quality PASS 或重复 artifact 即使重封 manifest 也为 `FAIL/1`。旧 v1 和早期 v2 result 只在各自固定旧字段集内只读兼容。

`.ltx` source 与 `.tex` 一样按 TeX 扫描和验证，候选统一发布为 `candidate.review.tex`；不得出现 coverage 记录 `tex`、validator 却按 Markdown 运行的格式分裂。

`source.snapshot.bin` 是本次 validator 实际读取的冻结 before bytes；`candidate.review.*` 的文件名明确表示它不是正式终稿。`patch.diff` 只显示变化，不能替代 bundle 中原样未决的 hunk。`validation.json` 保存统一验证器原始结构化输出；`result.json` 汇总 structural/application/validator/paired-quality 状态。

`evidence-manifest.json` 绑定其余六个工件的闭集路径、字节数和 SHA-256。发布后运行：

```powershell
python scripts/verify_humanize_short_patch.py short-patch-review --format text
```

verifier 先重放 bundle application、重算 diff，并核对 validation/result/hash；随后比较归档 `validation.evidence.policy_hashes` 与当前安装 policy。hash 一致时，用闭集中的 source snapshot、candidate 和 bundle 重新运行当前统一验证器，并比较完整结构化结果；因此顶层/分层状态、退出码、finding、warning fingerprint、paired-quality/warning request SHA 或证据绑定任一不一致均为 `CURRENT_POLICY_REPLAY_MISMATCH` 和 `FAIL/1`。policy drift 不等于记录损坏，固定为 `REVIEW/2 + current_policy_replay_status=NOT_RUN`。

需要确认记录是否仍对应当前工作文件时运行：

```powershell
python scripts/verify_humanize_short_patch.py short-patch-review `
  --live-source source.tex --format json
```

未提供 live source 时记录 `NOT_PROVIDED`，不暗示当前工作文件仍未变化；hash 一致为 `MATCH`；漂移为 `NOT_CURRENT/REVIEW/2`；显式路径缺失、乱码、hardlink、symlink 或 reparse point 为 `UNAVAILABLE/REVIEW/2`。结果不保存或回显 live source 路径。闭集验证和 current-policy replay 均通过且没有显式 live-source 问题时，文本首行包含 `INTEGRITY PASS exit=0 scope=SELF_CONSISTENCY_ONLY; CURRENT_POLICY_REPLAY PASS; DELIVERY REVIEW`。

完整性/current-policy replay PASS 可以发现本地工件被单独篡改或已经不符合当前相同 policy 的重算结果，但没有外部签名或时间戳，仍不证明历史真实性、文风收益、学术正确性或外部复核。不得从单个 `candidate.review.*`、diff、result、manifest 字段或 verifier PASS 推断完成。

## 7. 状态与退出码

| 场景 | 顶层状态 | 退出码 | 发布 |
|---|---:|---:|---|
| bundle 成功构建 | `BUNDLED` | `0` | 只写 bundle |
| create 未发现 AUTO high | `NO_HIGH_FINDINGS` | `0` | 只写 authoring scaffold；不得声称 NO_CHANGE |
| 严格 JSON、hash、offset、重叠、Unicode 边界或动作合同失败 | `FAIL` | `1` | 不发布候选 |
| 统一验证器 hard invariant 失败 | `FAIL` | `1` | staging 全回滚 |
| 有 `UNRESOLVED` | `REVIEW` | `2` | 发布 partial review candidate |
| 无未决但机械 warning 尚在 | `REVIEW` | `2` | paired-quality blocked |
| mechanical PASS 但 paired-quality 未外部复核 | `REVIEW` | `2` | 发布 review candidate |
| verifier 闭集损坏或同 policy 核心重算不一致 | `FAIL` | `1` | 不改变既有记录 |
| verifier 当前 policy 漂移/不可用 | `REVIEW` | `2` | 不改变既有记录，不运行或不采信 replay |
| 显式 live source 漂移或不可用 | `REVIEW` | `2` | 归档记录仍可独立自洽 |
| 闭集、同 policy replay 通过且 live source 未提供或一致 | verifier `PASS` | `0` | 候选本身仍为 `DELIVERY REVIEW` |
| verifier 参数错误或非法枚举 | `FAIL` | `1` | 输出结构化失败，不使用 argparse 的 `2` 混同 REVIEW |

本地短 PATCH 候选路径不得产生 `FINAL/PASS/0`，不得写 `humanize_quality_claim_allowed=true`。verifier 自身可因闭集和当前 policy 重放成功返回 `PASS/0`，但 JSON 同时固定保留 `delivery_gate_status=REVIEW` 与 `delivery_gate_exit_code=2`。`semantic_judgment` 和 `academic_correctness` 均保持 `NOT_EVALUATED`。

## 8. 失败处理

- `source_text is ambiguous`：给该精确 occurrence 的 UTF-8 `start_byte`，不要换成更宽 span 吞并其他句子；
- `source_sha256 mismatch`：源文件已变化，重新读源并重建 selection/bundle；
- `UNIFIED_VALIDATOR_FAILED`：读取 validator 输出定位公式、引语、TeX、数字、术语或其他硬不变量，不修改 hash 绕过；
- `REVIEW/2`：读取 `validation.json` 的 warning/high signal 和 bundle 的 `UNRESOLVED`，修改候选动作或提交外部复核；
- `POLICY_DRIFT`：记录按旧 policy 生成；保留原记录，使用当前 source 重新 build/apply 新证据，不手改旧 validation；
- `CURRENT_POLICY_REPLAY_MISMATCH`：记录声称的 policy 与当前相同但核心结果不能重现，按损坏或执行不一致处理；
- `LIVE_SOURCE_NOT_CURRENT/LIVE_SOURCE_UNAVAILABLE`：归档记录没有因此损坏，但不能声称它仍对应当前工作文件；
- `output_exists`：使用新的空目标；不清空、不覆盖现有证据目录；
- 乱码：严格 UTF-8 重试仍失败时跳过该文件并记录，不做替换字符修复。

## 9. 已知边界

v1 只证明“列出的 hunk 结构合法且 candidate 由当前 source/bundle 确定性派生”，不证明调用方列全了所有文风病灶、冲突或 high span。`unlisted_source_policy=COPY_EXACT` 只阻止静默删文，不构成 coverage 完成证明。v2 可以把 current scanner high 与已绑定声明机械闭合，但其 scope 固定为 `ENUMERATED_HIGH_AND_BOUND_DECLARATIONS_ONLY`；调用方未声明的语义冲突、词库外病灶和外部请求真实性仍不在证明范围内。

authoring scaffold 只降低重复录入和引用错配风险。v3 可以建议 clause/句/段 byte span、medium/low advisory
边界和调用方精确 FOCUS，但不能决定该建议是否
成为 hunk，更不能自动填写 replacement、KEEP 理由、selection、conflict pair 或用户授权。建议被
SUPPRESSED 不证明该句不可修改，只要求调用方拆分保护区并手工登记更窄 span。`review.md` 只改善
可见性，不是人工复核、外部签名或 paired-quality clearance。

谓词来源门仍需连续阅读。尤其复核 `用途 -> 结果`、`待执行/待验证 -> 已完成/已验证`、`内部指标 -> 外部事实`、`候选区间 -> 稳健阈值`、`缺失内容 -> 关系衔接`。确定性规则未命中不等于语义安全；`semantic_judgment=NOT_EVALUATED` 不得升级。

GPT 生成的 MD/TeX 只能作为负例压力材料，不得作为真人 Voice、事实来源或可复制正向句库。乱码、被排除文件和 `CET6.tex` 不进入来源。
