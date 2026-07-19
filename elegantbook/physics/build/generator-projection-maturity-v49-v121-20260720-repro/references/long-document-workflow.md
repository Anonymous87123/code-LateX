# TeX、Markdown 与纯文本长文工作流

## 目录

1. 适用范围
2. 长文完成定义
3. 固定输入快照
4. 文件清单
5. TeX 感知解析
6. Markdown 感知解析
7. 来源角色保护
8. 文档单元清单
9. 分块预算
10. 重叠上下文
11. 场景与 Voice Profile
12. 覆盖账本
13. 分节编辑
14. Diff 与回滚
15. 合并与冲突
16. 幂等重跑
17. 编译与格式检查
18. 乱码与异常
19. 完成交付
20. 长文检查表

## 1. 适用范围

在以下任一条件成立时使用本工作流：

- 单文件超过 1200 行；
- 可编辑作者正文超过 20000 个汉字；
- 文档包含 10 个以上一级或二级章节；
- TeX 文档通过 `\input` 或 `\include` 引用多个文件；
- 用户要求“全文”“整本”“所有章节”Humanize；
- 单次上下文无法连续阅读完整文档。

只处理文风、节奏、句式、模板和语态。`.txt` 按无标题的纯文本段落处理：空行是默认单元边界，
没有 TeX/Markdown 结构保护；数字、单位、引语、代码样式和用户锁定范围仍按统一验证器保护。
目录输入会递归纳入 `.txt`、`.md`、`.markdown`、`.tex`、`.ltx`，乱码文件记录后跳过，不中断其他文件。
不要在长文流程中加入内容审查。

## 2. 长文完成定义

先区分两个完成态：

- `coverage_completion_claim_allowed`：只证明快照、单元覆盖、局部保护和格式/编译门闭合；
- `humanize_completion_claim_allowed`：还必须证明 Voice 绑定、逐单元场景裁决、全文声线与跨块重复门、以及 fresh second-pass convergence。

只有后者为 true 时才声明“全文 Humanize 已完成”。在当前没有外部 paired-quality/结构语义审批
适配器的安装路径中，正常可交付态是 `publish_state=REVIEW_CANDIDATE`：它表示机械候选已组装、
但仍待外部复核，不是失败，也不是正式终稿。它至少要求：

- 输入文件均已进入固定快照；
- 每个文档单元均出现在 manifest；
- 每个可编辑单元均有覆盖状态；
- 所有可编辑 `author` 单元均为 `DONE` 或 `NO_CHANGE`，且不存在 `PENDING`、`IN_PROGRESS` 或 `UNRESOLVED`；
- 文件级不存在 `SKIPPED_GARBLED` 或 `CHANGED_AFTER_SNAPSHOT`；
- 每个修改单元均有 diff 和回滚依据；
- 重叠区没有重复编辑；
- TeX/Markdown 结构检查通过，或失败位置已明确报告；
- 同一输出重跑不再产生无意义措辞漂移。
- STRUCTURAL 的逐段 plan 机械门通过；若发生实际移动/合并，结构语义映射不能停在 `NOT_EVALUATED`。
- `ADJACENT_PAIR` inventory 中每个 `STX-*` 均有精确绑定的 `EXECUTED` 或 `DECLINED`
  disposition，不存在候选 `PENDING`；普通 unit `NO_CHANGE` 不替代这项覆盖。
- 每个可编辑 `REWRITE/NO_CHANGE` unit 都有 paired-quality request，且全部当前 request 已由可信外部
  复核链清除；机械 PASS、request 覆盖 PASS 和模型 second pass 都不能替代质量 clearance。
- 每个可编辑 unit 的 `rewrite_intent_coverage_status=PASS`：standalone unit 使用
  `humanize-unit-rewrite-bundle/v3` 并通过 authoring binding 重放；transaction member 使用
  `humanize-structural-transaction-bundle/v2` 的 fragment `local_rewrite_intent`。声明理由、冻结
  source/evidence span 与实际局部 diff 双向覆盖，并有 bundle/before/after/diff/request hash 证据；
  该 PASS 不证明理由真实、结构语义正确或读感收益成立。


不要用抽样阅读支持“全文完成”。抽样只能用于预诊断和确定规则优先级。

## 3. 固定输入快照

在编辑前固定以下信息：

```yaml
snapshot_id:
created_at:
root:
files:
  - path:
    bytes:
    readable_bytes:
    encoding:
    sha256:
    modified_at:
```

按字节读取并计算 SHA-256。记录开始时可读长度。若活动文件在处理期间追加内容，不把新增字节混入本轮；将文件标为 `CHANGED_AFTER_SNAPSHOT`。

不要覆盖源文件来制造快照。优先使用副本、版本控制 diff 或独立 patch 记录。

### 3.1 使用准备器固定快照

没有作者样本、直接使用场景 DEFAULT：

```powershell
python scripts/prepare_humanize_long_document.py <main.tex|document.md> `
  --output <empty-run-dir> `
  --scene <AUTO|GENERAL|COURSE|MODELING|RESEARCH> `
  --intensity <LIGHT|BALANCED|STRUCTURAL>
```

默认 `--structural-transaction-scope NONE`。只有用户明确授权同一文件、同一 heading 内相邻双 unit
原子结构事务时，才对 STRUCTURAL 追加：

```powershell
python scripts/prepare_humanize_long_document.py <main.tex|document.md> `
  --output <empty-run-dir> `
  --scene <AUTO|GENERAL|COURSE|MODELING|RESEARCH> `
  --intensity STRUCTURAL `
  --structural-transaction-scope ADJACENT_PAIR
```

该参数不自动改变分块预算，也不把一个完整小节强拆成 pair；没有候选时 inventory 为 `EMPTY`。
确需更细分块时，显式调整 `--max-author-chars/--min-author-chars` 并生成全新快照，不能手改旧 run。

显式提交代码注册表产生的、零样本的确定性场景 DEFAULT：

```powershell
python scripts/prepare_humanize_long_document.py <main.tex|document.md> `
  --output <empty-run-dir> `
  --scene <GENERAL|COURSE|MODELING|RESEARCH> `
  --intensity <LIGHT|BALANCED|STRUCTURAL> `
  --voice-profile <scene-default-profile.json> `
  --voice-profile-sha256 <64-lowercase-hex>
```

提交 PERSONAL，或 builder 由样本产生的证据绑定 DEFAULT：

```powershell
python scripts/prepare_humanize_long_document.py <main.tex|document.md> `
  --output <empty-run-dir> `
  --scene <GENERAL|COURSE|MODELING|RESEARCH> `
  --intensity <LIGHT|BALANCED|STRUCTURAL> `
  --voice-profile <voice-profile.json> `
  --voice-profile-sha256 <64-lowercase-hex> `
  --voice-manifest <voice-manifest.json> `
  --voice-sample-spec <samples.spec.json> `
  --voice-allowed-root <sample-root>
```

supplied Profile 必须为 `validation_status=PASS`，且其 `binding_scene` 必须与本次
prepare 的有效绑定场景相同。`AUTO` 不接受单一 supplied Profile；它按完整 unit 独立路由，
并物化 `GENERAL/COURSE/MODELING/RESEARCH` 四个确定性 DEFAULT 及 Profile set。PERSONAL 与
证据绑定 DEFAULT 只能用于显式单场景；缺少上述任一证据参数时必须拒绝，不得退化成只校验
Profile 自哈希。

证据 manifest 使用 `humanize-voice-sample-manifest/v2`，并绑定冻结 sample spec 的
canonical SHA-256。finalize 不把可重算的 `prepare_integrity.json` 当成该绑定的替代品：
即使 spec 修改后重新封装，来源角色、场景或范围与 manifest 不一致仍须失败。

TeX 正文需要清理装饰性样式包装时，只有用户明确授权后才追加
`--editable-style-wrapper textbf`（也支持 `emph/textit`，可重复）。默认不传时仍保护全部命令；该参数只开放包装命令本身，不开放标题、引用、数学、标签或内部文字的语义改写。

准备器只读源文件，并在读取开始时固定字节长度。它先尝试 UTF-8/UTF-8-SIG，再尝试 GB18030；仍不可读的文件标 `SKIPPED_GARBLED`，不会阻断其他 include。输出目录必须为空，避免旧 manifest 与新快照混合。

固定产物：

| 文件/目录 | 用途 |
|---|---|
| `snapshot.json` | 输入长度、编码、SHA-256、修改时间和快照 ID |
| `source/` | 只读快照副本；作为回滚依据，不是编辑目标 |
| `file_manifest.csv` | seed、include 关系、缺失/乱码/变动状态 |
| `units.jsonl` | 单元锚点、行范围、hash、owner 与初始状态 |
| `coverage_ledger.csv` | 初始覆盖账本；不得出现 `DONE` |
| `protected_spans.jsonl` | 保护区 ID、范围、理由、hash 与恢复内容 |
| `chunks/<unit_id>.json` | 带 `[[PROTECTED:...]]` 占位符的可编辑块 |
| `run_metadata.json` | 预算、状态回加、保护数、完成声明权限和闭集 policy snapshot |
| `voice_profile.json` | 显式单场景下已校验并按 canonical JSON 物化的 supplied 或场景 DEFAULT Profile |
| `voice_profile_set.json`、`voice_profiles/` | AUTO 下四场景 DEFAULT 的精确绑定、逐场景 Profile 与不可越权 claims |
| `scene_routing_policy.json` | 冻结的逐 unit 路由规则；finalizer 还会与当前安装 policy 比较并独立复算 |
| `structural_transaction_inventory.json` | 始终生成的 transaction 候选/禁用清单；绑定 scope、snapshot、pair、边界、chunk/inventory、Voice 与 policy |
| `prepare_integrity.json` | strict schema 2 完整性清单；按规范路径排序，绑定上述状态/结构文件、transaction inventory 与全部 chunk 的 SHA-256 和 bytes |

`run_metadata.json` 在准备阶段固定写 legacy prepare-only 字段 `completion_claim_allowed=false`，并冻结
`policy_snapshot` 与 `policy_snapshot_sha256`：其中包含 validator/保护检查/scanner/lexicon/report
extractor、prepare/finalizer、scene/Voice/negative-guard 实现和 Python runtime 的闭集 hash。finalizer
在读取场景、Voice 或 bundle 前先用当前安装面重建该 snapshot；缺字段、自哈希错误或任一 policy drift
均直接 `FAIL/1`，不能用重算 `prepare_integrity` 或旧 run metadata 继续消费旧候选。
终态不得读取该字段，只能读取 finalization metadata 的分层完成字段。准备成功只表示材料可进入改写，不表示任何正文已处理。若 `processable_editable_units=0`，准备状态必须为 `REVIEW`，并标记 `no_editable_scope=true`；仅有标题、公式、标签、引语或其他保护内容的文件不能进入“可处理长文”状态。

supplied Profile 必须同时提供文件与调用方 pin 的 `profile_sha256`；两者缺一、hash 非 64 位小写十六进制、自哈希无效或实际值不一致都属于全局配置失败。未提供 Profile 时，显式场景物化对应版本化 DEFAULT；`AUTO` 运行独立路由器并为每个 unit 绑定四场景 Profile set 中的对应 DEFAULT。路由 evidence 只记录 rule ID、计数和贡献，不导出命中正文；强信号平局固定 `AMBIGUOUS/UNRESOLVED`。逻辑文档 prior 沿 TeX include 根传播，但只有本 unit 已有同场景、局部最高的弱证据时才能补足阈值；零证据中性块、用途不明的共享标题保持 `GENERAL`。Profile 的 ID、revision、confidence、kind、source、hash 与 disclosure 必须同时进入 metadata、unit、chunk 和 ledger。

`finalize_humanize_long_document.py` 在读取任何终态前必须严格校验 schema 2
`prepare_integrity.json`。重复/未知字段、重复或非规范路径、`..`、非法 SHA、bytes 不一致、
artifact 集合或顺序漂移都必须失败。清单缺失、文件集合变化、`units.jsonl`、初始账本、protected
spans、snapshot、manifest、transaction inventory 或任一 chunk 被修改时，收尾直接失败，不发布
`rendered`、`rendered_partial` 或 `rendered_review`。完整性清单只是审计辅助，不是独立信任根：
收尾器还会从冻结 `source/` 副本、文件范围、预算、保护跨度和 canonical chunk 独立重建初始
units、账本、占位符恢复结果、`author_chars` 与 transaction inventory，并要求它们逐项相等。
即使攻击者同时修改台账/inventory 并重算封条，也不能伪造 DONE、扩大 pair scope 或替换
`STX-*`。终态只能由本次实际提交的 `REWRITE`/`NO_CHANGE`/transaction 和运行时验证产生。

同一个 `run-dir` 的 finalize 通过跨进程锁串行执行，共享 staging 目录不得并发清理或发布。
可选检查命令只在正文 staging 的一次性副本中运行；运行前后同时核对真实正文 staging、
待发布的 validation/diff 证据 staging 和其余 run 产物。任一文件被新增、删除或修改都使
编译门 `FAIL`，受污染证据不得发布。
空文件集或零可处理单元属于 `REVIEW`，不能把“没有待处理内容”解释为全文完成；只有
`finalization_metadata.json` 明确给出 `humanize_completion_claim_allowed=true`（兼容字段
`full_completion_claim_allowed=true`）才能对外声明全文 Humanize 完成。覆盖层单独读取
`coverage_completion_claim_allowed`。

每个 chunk 还包含 `context_before_unit/context_after_unit` 和最多 1200 字符的 `read_only_context_before/read_only_context_after`。这些字段只用于判断衔接，唯一 owner 仍是当前 `unit_id`；改写包只能提交当前 `masked_text`，不得把只读上下文复制进输出。

prepare 还对去掉自身 hash 字段后的 canonical chunk 计算 `chunk_binding_sha256`。该 hash 覆盖 unit 身份、原文 hash、masked text、保护 ID、只读上下文、场景与 Voice 绑定；它进入 chunk、unit 和 ledger。改写包必须回显它，不能只靠文件名指向当前单元。

## 4. 文件清单

递归追踪主文件中的本地引用：

- `\input{...}`；
- `\include{...}`；
- `\subfile{...}`；
- Markdown 相对链接中明确作为正文纳入的文件；
- 用户显式指定的附录和章节文件。

为每个文件记录：

| 字段 | 说明 |
|---|---|
| `file_id` | 稳定短 ID |
| `path` | 规范化绝对路径 |
| `parent` | 引用它的文件 |
| `include_order` | 文档展开顺序 |
| `encoding` | 实际读取编码 |
| `hash_before` | 快照哈希 |
| `role` | 主文件、章节、附录、模板或资产 |
| `editable` | 是否包含可编辑作者正文 |
| `status` | `PENDING/DONE/NO_CHANGE/SKIPPED/UNRESOLVED` |

不要扫描构建目录、生成文件、缓存、第三方模板或用户未纳入正文的备份文件。

## 5. TeX 感知解析

### 5.1 先识别结构，不按空行盲切

识别：

- `\part`、`\chapter`、`\section`、`\subsection`、`\subsubsection`；
- `\paragraph` 和 `\subparagraph`；
- `\begin{...}` / `\end{...}` 环境边界；
- 命令参数和可选参数；
- 注释行与转义百分号；
- `\input`、`\include` 和文件展开顺序；
- 行内与陈列数学边界；
- verbatim 类环境。

保持命令、花括号、方括号、标签、引用键和环境边界原样。

### 5.2 区分结构参数与可编辑文本参数

使用以下固定分类：

| TeX 对象 | 处理方式 |
|---|---|
| 章节标题参数 | 默认受 `title_lock` 保护；解锁后仅改标题文字 |
| `\caption{作者说明}` | 可将文字部分标为 `author`，保留命令结构 |
| `\footnote{作者说明}` | 可编辑文字部分，保持嵌套命令完整 |
| `\textbf/\emph/\textit{作者正文}` | 默认保护包装命令；用户授权格式清理时用 `--editable-style-wrapper` 开放，内部文字仍受不变量和 Voice 约束 |
| `\label{}`、`\ref{}`、`\cite{}` | 全部保护 |
| `\url{}`、`\path{}`、`\verb` | 全部保护 |
| 自定义命令参数 | 默认保护；只有明确知道参数为作者正文时才编辑 |
| 数学环境 | 标 `math`，不编辑内部内容 |
| `verbatim`、`lstlisting`、`minted` | 标 `code`，不编辑内部内容 |
| 注释 | 默认不作为正文改写；用户明确要求时单独处理 |

不要用正则替换穿越嵌套命令边界。若无法可靠解析嵌套范围，标 `UNRESOLVED`，不要猜测。

### 5.3 保存 TeX 锚点

为每个可编辑单元保存：

```yaml
unit_id:
file_id:
heading_path:
start_line:
end_line:
prefix_hash:
content_hash:
suffix_hash:
```

使用标题路径和前后文哈希共同定位。不要只依赖行号；前序编辑会改变行号。

## 6. Markdown 感知解析

识别：

- ATX 与 Setext 标题；
- YAML frontmatter；
- fenced code block 与缩进代码；
- blockquote；
- 表格；
- 列表层级；
- HTML 块；
- 链接目标、图片和引用定义；
- 行内代码和公式；
- 脚注定义。

默认保护 YAML、代码、HTML 属性、链接目标、图片路径和引用键。根据来源角色决定是否编辑 blockquote；直接引语标 `quoted`，作者自写的提示块可标 `author`。

保持表格列数、分隔行和列表层级。只编辑确认属于作者正文的单元格或列表项。

## 7. 来源角色保护

为每个文本 span 标记：

- `author`；
- `quoted`；
- `exam-original`；
- `OCR`；
- `code`；
- `math`。

使用最内层保护优先。不要编辑 `quoted`、`exam-original`、`OCR`、`code` 和 `math` 内部内容。

建立保护区清单：

```yaml
protected_id:
unit_id:
role:
start_anchor:
end_anchor:
hash_before:
reason:
```

编辑后再次计算保护区哈希。任何保护区哈希变化都必须回滚该单元并重新处理。

## 8. 文档单元清单

按最小完整写作功能建立 unit，不逐句切块：

1. 优先使用完整小节；
2. 小节过长时按段落组切分；
3. 保持列表、表格、引语和公式邻接说明完整；
4. 不跨文件引用边界生成一个可编辑 unit；
5. 不把标题与其首段分开；
6. 不把公式与紧随其后的作者解释无故分开。

记录：

| 字段 | 说明 |
|---|---|
| `unit_id` | 稳定 ID |
| `file_id` | 所属文件 |
| `heading_path` | 章节路径 |
| `scene` | 场景路由 |
| `voice_profile` | 使用的声线档案 |
| `author_chars` | 可编辑正文规模 |
| `protected_spans` | 保护区数量 |
| `owner_chunk` | 唯一编辑分块 |
| `status` | 覆盖状态 |

## 9. 分块预算

按可见作者正文字符而不是文件字节控制分块：

| 项目 | 预算 |
|---|---|
| 目标分块 | 4000 至 7000 个可见正文字符 |
| 硬上限 | 8000 个可见正文字符 |
| 最小分块 | 1200 个可见正文字符，除非完整小节更短 |
| 上下文重叠 | 前后各 1 个完整段落，合计不超过 1200 字符 |
| 单次结构重排 | 不跨越一个授权章节 |

若一个不可拆结构超过硬上限，保留完整结构并标记超限原因。不要在表格、列表、数学环境、引语或 TeX 命令中间硬切。

对密集 TeX 命令的分块，额外限制总行数，避免保护区吞噬上下文。每块最多 600 行；超出时在完整段落边界继续切分。

## 10. 重叠上下文

只把重叠段用于理解衔接，不重复编辑。

为每个重叠段指定唯一 owner：

```yaml
overlap_id:
owner_chunk:
reader_chunks: []
hash_before:
```

执行以下规则：

- owner chunk 可编辑重叠段；
- reader chunk 只读，不输出该段改写；
- 合并时只接受 owner 版本；
- owner 版本变化后，更新相邻块的衔接检查；
- 相邻块不得各自生成一份竞争改写。

若跨块衔接必须同时改两侧，将两块提升为一个临时合并单元；不要分别猜测。

## 11. 场景与 Voice Profile

先在文档级识别主要用途，再按完整 unit 路由。不要逐句切换场景。

为每个 unit 记录：

- 显式用户场景；
- 自动路由得分；
- 最终场景；
- 平局裁决；
- Voice Profile 版本；
- Profile 置信等级；
- 未提供作者样本时的默认声明。

混合文档允许不同 unit 使用不同场景。共享摘要或总引言用途不明时使用 `GENERAL`，不要拼接三种声线。document prior 按 include 根覆盖逻辑文档，而不按物理文件割裂；它只补全与本 unit 唯一弱信号一致、且其他场景得分为零的场景，不得把完全中性的“背景/结论”静默改成邻近强场景。两个正分场景平局或 margin 不足时，无论 top score 是否达到强路由阈值都属于 `AMBIGUOUS`；document prior 不得替低分或强分歧义作隐藏裁决。

## 12. 覆盖账本

为每个 unit 使用且只使用一个状态：

| 状态 | 含义 |
|---|---|
| `PENDING` | 已列入但尚未处理 |
| `IN_PROGRESS` | 当前唯一正在处理的单元 |
| `DONE` | 改写候选机械验证通过，变化与 diff 已登记；作用域只是候选组装，不代表 paired-quality clearance 或交付完成 |
| `NO_CHANGE` | 已完整阅读且未提交变化；仍需 paired-quality request，不证明原文自然 |
| `SKIPPED_PROTECTED` | 全单元均为保护角色 |
| `SKIPPED_GARBLED` | 可读性不足，按规则跳过 |
| `UNRESOLVED` | 角色、权限、解析或冲突无法解决 |
| `CHANGED_AFTER_SNAPSHOT` | 源文件在快照后变化，未混入本轮 |

账本至少包含：

```yaml
unit_id:
status:
scene:
mode:
intensity:
decisions:
hash_before:
hash_after:
diff_path:
protected_hashes_ok:
style_gates:
notes:
```

不要把只抽查了首尾的 unit 标为 `DONE` 或 `NO_CHANGE`。

## 13. 分节编辑

对每个 owner unit 执行：

1. 核对快照哈希；
2. 加载前后重叠只读上下文；
3. 标记保护区；
4. 加载场景规则和 Voice Profile；
5. 连续阅读完整 unit；
6. 给候选位置分配 `KEEP/DELETE/REWRITE/REVIEW/NO_CHANGE/UNRESOLVED`；
7. 按强度改写；
8. 比较改前改后；
9. 核对保护区哈希；
10. 运行机械验证并生成 paired-quality request；
11. 生成 diff；
12. 更新覆盖账本。

一次只把一个 unit 标为 `IN_PROGRESS`。发生中断时从该状态恢复，不重复改写已完成单元。

### 13.1 改写包合同

只读取 `chunks/<unit_id>.json` 中状态为 `PENDING` 的块。`masked_text` 中的每个保护占位符必须原样、恰好保留一次；不得改 ID、12 位 hash、顺序或数量。

不要手写 binding 骨架。先用安装版脚本从冻结 run 生成模板：

```powershell
python scripts/scaffold_humanize_rewrites.py `
  --run-dir <run-dir> `
  --output <empty-rewrites-dir> `
  --decision REWRITE `
  --format text
```

若不同单元需要不同处置，使用严格覆盖全部 `PENDING` unit 的 UTF-8 JSON 映射，不能把未列出的
unit 默认为 `REWRITE` 或 `NO_CHANGE`：

```powershell
python scripts/scaffold_humanize_rewrites.py `
  --run-dir <run-dir> `
  --output <empty-rewrites-dir> `
  --decision-map <unit-decisions.json> `
  --format text
```

映射值只能是 `REWRITE` 或 `NO_CHANGE`；大小写碰撞、缺失 unit 和多余 unit 均整体拒绝。

脚本只读取 `PENDING` chunk，逐个回显 `unit_id`、`chunk_binding_sha256`、
`voice_profile_sha256` 和 masked text；`scaffold_metadata.json`（`humanize-rewrite-scaffold/v5`）明确
`completion_claim_allowed=false`。`REWRITE` 模板默认复制冻结 masked text，未产生真实变化时
finalizer 会拒绝并要求改成带具体理由的 `NO_CHANGE`；`NO_CHANGE` 模板的 `reason=TODO` 故意不满足
理由门，必须由调用者替换。模板输出不等于执行包、机械 PASS 或质量 clearance。

v5 骨架发布采用两阶段标记。目录进入最终名称时只含
`.humanize-scaffold-uncommitted`；普通成员与 marker 均由句柄冻结并复验后，才把同一 marker 原子改名为
`.humanize-scaffold-committed`。commit marker 以 strict JSON 绑定 `scaffold_metadata.json` 的原始字节
SHA-256，并固定 `completion_claim_allowed=false`。目录存在、metadata 可读或模板齐全都不表示发布完成：
finalizer 必须拒绝缺 committed marker、残留 uncommitted marker、marker link/hardlink、非法 schema、
metadata hash 错配或 legacy metadata 携带 marker。发布后复验失败会先按 pinned parent handle 回滚；
若回滚也失败，骨架器返回 `FAIL_DIRTY/1` 与 `output_may_exist=true`，调用方必须隔离该目录，不能把它
当作 `SCAFFOLDED`。安全发布当前只支持本地 NTFS；ReFS、FAT/exFAT、SMB 和非 Windows 平台明确
fail closed，不退化为按路径先检查再 rename。

sidecar 用 `metadata_scope=SCAFFOLD_CREATION_TIME` 和
`template_hash_scope=ORIGINAL_TEMPLATE_BYTES` 明确 `requires_manual_completion=true` 与
`template_sha256` 都描述骨架生成时刻：前者不是动态进度，后者绑定原始模板字节，人工填写后自然不再
等于当前 bundle。finalizer 只把 sidecar 作为严格审计旁证，
仍以每个 bundle 的当前 binding、正文和验证结果裁决，不把 sidecar 当完成台账。v5 只从 strict
schema 2 `prepare_integrity.json` 签发；合法历史 schema 1 运行返回
`legacy_prepare_requires_reprepare / REVIEW/2`，要求重新 prepare，不把旧闭集静默升级成新 authoring
权限。preflight 的 `run_state_sha256` 只绑定 manifest 明列的 immutable prepare closure；后来生成的
rendered、validation、ledger 与 metadata 不改变该值，但任何明列 prepare artifact 漂移仍整体拒绝。
每个 v3 模板还冻结完整 `humanize-long-authoring-binding/v1`：source span、chunk、scene route、Voice、
snapshot 和 policy 均由 finalizer 从准备工件重建，调用方修改 binding 并同步改 sidecar hash 也不能通过。
骨架器把 `unit_id` 当作文件名使用，只接受由 ASCII 字母/数字开头、总长不超过 128 且仅含
字母、数字、`.`、`_`、`-` 的 ID；路径分隔符、保留路径段、空白和控制字符均在写入前拒绝。
同一 run 中不区分大小写的重复 ID 也必须整体拒绝，避免 Windows 文件名碰撞或覆盖另一单元。

改写结果写到独立 `<rewrites-dir>/<unit_id>.json`：

下例只展示人工可编辑字段；`authoring_binding` 必须原样保留 v5 模板中的完整对象，省略它、手写它或
修改其中任一值都会失败。

```jsonc
{
  "schema_version": "humanize-unit-rewrite-bundle/v3",
  "unit_id": "<chunk.unit_id>",
  "chunk_binding_sha256": "<chunk.chunk_binding_sha256>",
  "decision": "REWRITE",
  "voice_profile_sha256": "<chunk.voice_profile_sha256>",
  "authoring_binding": { /* 原样保留 scaffold 生成的完整对象 */ },
  "masked_text": "改写后的完整占位文本",
  "rewrite_intent": {
    "summary": "删除空泛收尾并保留材料范围",
    "operations": [{
      "id": "O1",
      "kind": "REWRITE_STYLE_SHELL",
      "source_span_ids": ["S1"],
      "target_signals": ["STYLE-EMPTY-ENDING"],
      "summary": "删除空泛收尾并保留材料范围"
    }],
    "source_spans": [{
      "id": "S1",
      "start_line": 2,
      "end_line": 2,
      "sha256": "<冻结 masked chunk 第 2 行（保留行尾）的 SHA-256>"
    }],
    "target_signals": ["STYLE-EMPTY-ENDING"]
  },
  "keep_reasons": {
    "LEX-RESULT-01": "此处承担结果报告言语行为"
  },
  "warning_resolutions": {
    "<warning_fingerprint>": "建议恢复原句模态以保留结论范围"
  },
  "warning_review_request_sha256": "<current_request_sha256>"
}
```

上例是 warning proposal 包，不是可完成的 `DONE/PASS` 包。首次运行没有 warning 时，或尚未
提交 proposal 时，同时省略 `warning_resolutions` 与 `warning_review_request_sha256`，不得单独携带
其中任一字段。`warning_review`、`reviewer_kind`、`reviewer_id`、`reviewer_id_sha256` 等身份字段已
退役；出现即拒绝，不回显调用方标签，也不把标签或其 hash 写入队列、ledger 或 validation 工件。

已连续阅读且无需改写的单元必须显式提交：

```jsonc
{
  "schema_version": "humanize-unit-rewrite-bundle/v3",
  "unit_id": "<chunk.unit_id>",
  "chunk_binding_sha256": "<chunk.chunk_binding_sha256>",
  "decision": "NO_CHANGE",
  "voice_profile_sha256": "<chunk.voice_profile_sha256>",
  "authoring_binding": { /* 原样保留 scaffold 生成的完整对象 */ },
  "reason": "正式定义组保持原有等权结构",
  "evidence_spans": [{
    "id": "S1",
    "start_line": 2,
    "end_line": 2,
    "sha256": "<冻结 masked chunk 第 2 行（保留行尾）的 SHA-256>"
  }],
  "keep_reasons": {}
}
```

`REWRITE` 与 `NO_CHANGE` 都必须从当前 chunk 精确回显 `unit_id`、`chunk_binding_sha256` 与 `voice_profile_sha256`。文件名与内部 unit 不同、chunk hash 缺失/非法/错配、Voice hash 缺失/非法/错配时，在正文 validator 之前分别拒绝，不得由 finalize 自动补值。旧式 `.txt` bundle 无法承载这些字段，因此 Profile-bound run 只接受 strict JSON；重复 key、浮点数、非有限数字和过深结构直接拒绝，不能依赖解析器“最后一个 key 生效”的覆盖行为。

v3 的 `REWRITE` 必须形成完整 intent 图：每个 source span 和 target signal 都至少被一个 operation 引用；
source span 使用 normalized-LF 后、保留行尾的 frozen masked chunk 行字节计算 SHA-256。`source_spans` 清单必须按行递增、互不重叠，不能用不同 ID 重复登记同一范围；多个 operation 可以引用同一个已登记 span。每个声明 span
必须与实际 masked diff 相交，实际变化的每一 source line 也必须被声明 span 覆盖；另改一处未申报文本
固定拒绝。`NO_CHANGE` 理由至少含 8 个汉字、指向定义/段落/原句/结构/职责/对象/范围/条件/指代/
模态等具体功能，并至少有一个 hash-bound evidence span；“保持原样、无需修改、符合要求、已经自然、
没有问题”及其空泛改写固定拒绝。若单元含 high 表面命中，仍必须在 `keep_reasons` 中逐 signal 说明
正式功能或用户锁定依据。不要用空改写包或复制原文冒充处理；`REWRITE` 与原文完全相同时，收尾器会
拒绝并要求改用带理由的 `NO_CHANGE`。

v2 与无 `schema_version` 的旧 bundle 只读兼容。v2 仍可产生 intent 机械证据，但缺少完整 v3
`authoring_binding`，因此 `authoring_binding_status=REVIEW`；无 schema bundle 的 intent 证据状态另为
`REVIEW`、`rewrite_intent_coverage_status=REVIEW`。两者都不得形成正式交付或 Humanize 完成声明。显式 null、未知 schema、
TODO、空数组、span hash/行范围错配、operation 覆盖不全或未申报 diff 都不是 legacy，必须拒绝。

`LIGHT/BALANCED` 只允许其强度表中列出的局部编辑，不提交 `structural_plan`，也不得交换完整段落。
finalizer 对非 STRUCTURAL 候选执行高置信度整段顺序检查：两个以上唯一、完整保留的作者段落出现逆序时，
登记 `non_structural_paragraph_reorder_detected`，单元固定为 `UNRESOLVED`，不进入 paired-quality 或
`rendered_review/`。该门只声称拦截可机械确认的完整段落换位，不把它夸大成所有近似结构移动检测器。

BALANCED 的段落拓扑变化另走声明式窄门，不等于开放任意拆并段。只有 v3 `REWRITE` operation 精确使用
`MERGE_ADJACENT_REDUNDANCY` 或 `SPLIT_OVERLOADED_PARAGRAPH`，每个 operation 只引用一个与冻结
masked source 精确对齐的 span，且对应 target signal 分别为
`HIERARCHY-ADJACENT-REDUNDANCY` / `HIERARCHY-OVERLOADED-PARAGRAPH` 时才进入验证。合并 span 必须
恰好覆盖两个相邻作者段，拆分 span 必须恰好覆盖一个作者段；目标分别恰好为一段/两段，多个操作的
source/target 范围不得重叠，独立保护占位符不能夹在拓扑 span 内。段数净差与 operation kind 必须回加；
净差为零时仍以唯一句子-段落 membership 检测同时发生的 merge/split，缺唯一证据才回退行级 diff。
LIGHT、legacy、generic operation、错 signal、过宽 span、未申报拓扑或 scope 外变化固定阻断。
`topology_authorization_status=PASS` 只证明上述机械关系，不证明相邻两段确实语义重复或原段确实职责过载；
paired-quality 与人工读感复核仍保持 pending。

writer bundle 不得自填 paired-quality PASS、reviewer 身份或 clearance。普通 warning proposal 固定
为 identity-free `UNVERIFIED_CALLER_PROPOSAL`。finalizer 从实际恢复后的
before/after 与当前 validator policy 独立生成
`validation/<unit_id>.paired-quality-review-request.json`；`REWRITE` 登记逐 hunk 变化，`NO_CHANGE`
也生成 `changes=[]` 请求。机械验证通过的 unit 可进入候选组装，但在可信外部复核接入前，unit 的
`paired_quality_review_status` 固定为 `PENDING_EXTERNAL_REVIEW`，不能因理由具体或原文未变而升级。
同时生成 `validation/<unit_id>.rewrite-intent.json`，内容寻址绑定规范 bundle、before/after、实际落盘
diff 字节和 paired-quality request SHA；final metadata 中的 paired-quality record 反向给出 intent
evidence path/hash。该双向索引仍不是外部质量 clearance。

### 13.2 STRUCTURAL 包

STRUCTURAL 先读 [structural-rewrite-contract.md](structural-rewrite-contract.md)。prepare 固定输出
逐段来源 ID、职责、保护 ID、移动资格和 inventory hash。默认 `NONE` 只接受普通 unit
`structural_plan`，且每个来源段恰好映射一次。显式 `ADJACENT_PAIR` 还会生成
`structural_transaction_inventory.json`，但 inventory 只是候选：它给出机械 scope permission，
不等于执行请求或语义 clearance。正式 transaction bundle 必须以
`humanize-structural-transaction-bundle/v2` 精确回显某个冻结 `STX-*` 的 ID、binding、inventory
hash、两个 chunk/Voice binding 和两个完整 target fragment。普通 unit bundle 不能拼接成
transaction。两种模式都不解锁标题、不拆分或删除来源段；普通内联数学只可随完整来源段移动，
陈列数学、正式环境、引语和关键命令所在段锁定。

v2 每个 fragment 还必须提交 `local_rewrite_intent`。其 source/evidence span 绑定 finalizer 根据
`target_groups` 重放得到的“只移动、不改字”结构基线，而不是原 member chunk：

- `decision=REWRITE`：使用与普通 unit 相同的 `rewrite_intent` 图；所有局部变化行都被声明 span 覆盖，
  每个 span 都实际命中局部 diff；
- `decision=NO_CHANGE`：候选 masked fragment 必须逐字等于结构基线，并提供具体 reason 与至少一个
  hash-bound evidence span；它表示“只执行已声明的结构移动，不另改措辞”，不是整个 transaction
  没有变化。

`humanize-structural-transaction-bundle/v1` 仅只读兼容：仍执行全部结构、保护、FRAGMENT、DOCUMENT、
repetition 与 paired-quality 门，但两个 member 只生成 legacy intent `REVIEW` evidence，整篇
`rewrite_intent_coverage_status=REVIEW`。显式 null、未知 transaction schema、v2 缺
`local_rewrite_intent`、NO_CHANGE 偷改、span hash 错配或声明外第二处变化均拒绝/原子回滚，不按 v1
降级。

transaction 的来源段使用 `{unit_id, paragraph_id}` 复合 ref；两个 fragment 的联合 ref 必须恰好
覆盖两个 member 的全部来源段一次。允许 `movable=true` 的完整段在 pair 内换 target unit；锁定段
留在原 unit。一个 unit 不能同时有 standalone bundle 和 transaction，也不能属于两个 transaction。
prepare 可以列出三 unit 链中的两条重叠候选边，但同一次 finalize 必须先做全局 member claim，
在正文验证前拒绝共享 member 的提交。

v5 scaffold 与 transaction execution 的替换步骤固定为：先把预定 member 以 `REWRITE` 生成普通 v3
模板；完成绑定同一冻结 `STX-*` 的 transaction bundle；删除且只删除这些 member 的 standalone JSON；
保留 `scaffold_metadata.json` 中的原记录和原始 template hash；再 finalize。sidecar 的 record 全集仍须
等于冻结 PENDING 全集，而本次 submission coverage 等于剩余 standalone unit 与 execution member 的
不相交并集。member 同时有 standalone 和 transaction、缺失其他 PENDING、transaction 替换的 record
原决策为 `NO_CHANGE`、未知 member 或绑定漂移都在正文处理前拒绝。decline 不进入这个替换并集：它只
关闭候选 disposition，两个 member 仍各自需要 standalone `REWRITE/NO_CHANGE`。

inventory 为 `READY` 时，每个候选必须另有 disposition。执行使用上面的 transaction bundle；
不执行使用 `humanize-structural-transaction-decline/v1`，精确回显 transaction/inventory hash、
冻结顺序的两个 chunk/Voice binding、枚举 reason code、至少 8 个汉字的具体理由，以及两个 member
各至少一个、不重复且命中冻结来源段的 `{unit_id, paragraph_id}` 证据。合法 decline 不 claim
member，所以重叠候选可以逐边 decline；但共享 member 不能让相邻另一条边自动完成。一个 ID 同时
execution/decline、stale binding、空泛理由、单侧/未知/重复证据均须拒绝。

decline 与 unit 覆盖正交：两个 member 仍分别提交 `REWRITE/NO_CHANGE`；只有 decline 而没有 unit
bundle 时，候选 coverage 可以 PASS，但 unit 仍 `PENDING`。反过来，两个 unit 都 `NO_CHANGE`
但没有 execution/decline 时，该 `STX-*` 为 `PENDING`，
`structural_transaction_candidate_coverage_status=REVIEW`、
`structural_transaction_scope_complete=false`、`candidate_assembly_status=REVIEW`、
`delivery_gate_status=REVIEW`、`exit_code=2`、`coverage_completion_claim_allowed=false`，不得发布正式
`rendered/`。绑定正确但后续原子 gate 失败的 execution 仍记 `EXECUTED`，同时两 member 按原有
规则共同 `UNRESOLVED`。

finalizer 先按 plan 重放“只移动、不改字”的结构基线，再以该基线执行 FRAGMENT 与 DOCUMENT
不变量，避免把随段移动的数字/公式误报为改值。plan PASS 只证明机械映射；发生实际移动或合并时
`structural_semantic_mapping=NOT_EVALUATED`，并生成
`humanize-structural-semantic-review-request/v1`。transaction 则对两个 fragment 分别运行 FRAGMENT
validator，再运行联合 DOCUMENT gate；三项全 PASS 才能一次性提交两侧，并生成一个
transaction v2 对应的 `humanize-structural-transaction-review-request/v2`。该请求反向索引两个
fragment intent 的 canonical hash 与 diff-binding hash；每个
`humanize-transaction-fragment-rewrite-intent-evidence/v1` 又绑定 transaction request、paired-quality
request、bundle/fragment、结构基线、候选和 member diff。v1 bundle 继续生成 v1 request。
任一 member、保护、fragment、DOCUMENT 或
后置 repetition 门失败时，双方共同回滚，零 member diff/发布。请求绑定 before/baseline/after、
复合来源 ref、内外边界、member claim、plan/transaction、上下文、warning 和 policy hash；证据
路径使用提交后的 `validation/...` 相对引用。当前不消费本地或模型自填 clearance。完整候选的机械
组装可以是 `candidate_assembly_status=PASS`，但顶层必须为 `delivery_gate_status=REVIEW`、`exit_code=2`，候选
只进入 `rendered_review/`，不得据此声明全文完成。

`warning_resolutions` 只记录统一验证器非硬性言语行为 warning 的处理 proposal。每个 key
必须是当前 `warning_review_request` 中的完整 fingerprint，且
`warning_review_request_sha256` 必须精确绑定当前 unit 的 before/after SHA、warning details、
场景/格式/保护术语和 validator/invariant/scanner/lexicon/report-extractor/runtime 六项 policy hash。模型或执行代理可以
生成建议，但不得把自身复核描述为人工审批。bundle 不采集 reviewer kind、label 或稳定假名；proposal
固定写 `proposal_source=UNVERIFIED_CALLER_PROPOSAL`、`reviewer_identifier_collected=false`、
`identity_verified=false`、`review_clearance_granted=false`、`attestation_status=NOT_APPLICABLE`。
proposal 对应 warning 仍是 pending，unit
保持 `UNRESOLVED/REVIEW`，不得成为 `DONE/PASS`。跨 unit、跨 artifact 或 policy 变化后的
request 重放必须拒绝。

本地收尾器没有外部信任根，identity-free proposal 也不能升级为 `VERIFIED_HUMAN`。真正的
`VERIFIED_HUMAN` 必须由代理不可访问私钥的外部审批服务签发，并验证签名、unit/artifact、
request hash、审批范围和时效；当前 rewrite bundle 不承载这种 clearance。未接入该服务时，
应按 proposal 继续修改 `masked_text`，直到新版本不再产生 warning。公式、数字、单位、引语、
代码、TeX 命令、环境或结构等硬错误无论如何都不可降级。

## 14. Diff 与回滚

完成一个或一批改写包后运行：

```powershell
python scripts/finalize_humanize_long_document.py `
  --run-dir <run-dir> `
  --rewrites <rewrites-dir> `
  --check-command "<optional project build command>" `
  --check-timeout-seconds 300 `
  --format text
```

`--format text` 的第一行固定为 `DELIVERY <status> exit=<code> publish=<state>`，随后只显示候选组装、
paired-quality、unit 作用域、候选路径和编译状态；默认 `json` 仍保留全部审计字段。进程退出码
`0/1/2` 分别表示 `PASS/FAIL/REVIEW`，因此通用命令包装器可能把正常待审的 `2` 显示成“命令失败”；
调用者必须读取第一行或 `finalization_metadata.json`，不得把包装器的通用错误标签改写成硬失败。
run 目录中的 `.finalize.lock` 是跨进程锁的持久载体；进程退出后文件仍可存在，是否正在占用由操作系统
文件锁决定，不能用 `Test-Path .finalize.lock` 推断仍有活动 finalizer。

收尾器按单元恢复保护占位符，核对单元原始 hash，调用统一输出验证器，再决定是否接受。任何占位缺失、重复、未知或 hash 不符都会把该单元标为 `UNRESOLVED`，不会进入派生稿。

逐单元验证显式使用 `document_scope=FRAGMENT`。chunk 可能只含跨块 TeX 环境或外层花括号
的一侧；此时只允许改前已经存在、且改后问题列表完全相同的边界不平衡。环境名称/顺序变化、
花括号问题变化、保护跨度变化仍为硬失败。`FRAGMENT` 通过后，收尾器还必须把所有接受的
unit 组装回冻结全文，并以 `document_scope=DOCUMENT` 重新检查完整环境与花括号平衡；前一层
不能替代后一层，也不能把源文件本身已有的完整文档错误静默改成通过。

### 14.1 保存每节 diff

每个 `DONE` unit 必须保存：

- 原始内容哈希；
- 修改后内容哈希；
- 上下文锚点；
- 统一 diff 或等价逐段 patch；
- 使用的参数和规则版本；
- 保护区校验结果；
- 回滚内容或可逆 patch。

不要只保存最终整文件 diff；逐节 diff 才能定位回滚。

### 14.2 使用原子回滚

出现以下任一情况时回滚整个 unit：

- 保护区哈希变化；
- TeX/Markdown 结构边界损坏；
- patch 无法在原锚点唯一应用；
- unit 被快照后外部修改；
- 改写越过授权强度；
- 二次阅读发现言语行为被改变。

回滚后将状态设为 `UNRESOLVED` 或重新处理。不要只手工补一个括号后继续宣称通过。

transaction 的原子范围固定为两个 member。任何一侧回滚原因都必须扩展到整个 pair；两侧
`hash_after/diff_path` 清空，均不得进入 accepted replacement 或 invariant baseline。只有两个
FRAGMENT validator 与 DOCUMENT gate 全 PASS，才把两侧 replacement、ledger、diff 和 review
request 一次性从 staging 提交。`rollback_manifest.json.atomic_transactions` 至少记录 transaction
ID、两个 unit、失败 gate、`accepted_member_count=0` 和 `published_member_count=0`。如果同一 run
还有独立非事务进度，可以发布普通 partial，但 pair 对应范围必须与冻结 source 精确相同。

收尾器从不覆盖原源文件。所有接受的单元先写入 `.rendered_staging`；全文不变量和可选编译门通过后，只有全部交付门均有 clearance 的正式终态才发布到 `rendered/`，覆盖未闭合时发布到 `rendered_partial/`。机械候选完整但 STRUCTURAL 结构语义或 paired-quality 任一待外部复核时，完整候选发布到 `rendered_review/`，顶层保持 `REVIEW/2`。编译失败时 staging 改名为 `failed_staging/`，不创建新的正式输出。`rollback_manifest.json` 明确记录源文件未改、快照依据和丢弃失败 staging 的动作。

整次 finalize 还必须是 run-dir 级事务。持锁后先把全部非 transient 工件复制到隔离备份，再依次
提交 rendered namespace、validation、diff、最终账本和 metadata；任一步抛出异常时恢复调用前
字节，不能留下“有 rendered、无 validation/ledger/metadata”的半发布状态。已有发布证据的失败
重跑、或 `check_command` 通过绝对路径改变 run-dir 时，同样恢复上一版 canonical 状态；上一版
`finalization_metadata.json` 不得被本轮候选哈希覆盖。本轮失败只写
`last_failed_attempt_metadata.json`。该记录中的本轮 request hash 可以保留用于诊断，但所有已经
回滚的 `validation/...`、`diffs/...`、rendered 和 staging 路径必须清空，并标
`failed_attempt_evidence_status=NOT_RETAINED_AFTER_ROLLBACK`、
`failed_attempt_evidence_paths_reusable=false`，不得让新 request hash 指向恢复后的旧文件。
备份前还要拒绝 run-dir 自身或内部工件的 symlink、junction/reparse point 与多链接文件，并核对
复制前、复制后和备份树三份文件哈希一致；否则不能把外部目标或漂移快照当成可恢复基线。

逐单元证据保存在：

- `validation/<unit_id>.before.*` 与 `.after.*`；
- `validation/<unit_id>.validation.json`；
- `diffs/<unit_id>.diff`；
- `coverage_ledger.final.csv`；
- `rendered_manifest.csv`；
- `finalization_metadata.json`；
- `last_failed_attempt_metadata.json`：仅在事务恢复或运行时异常时记录失败尝试，不替代 canonical metadata；
- `rollback_manifest.json`。

### 14.3 全文 Voice 与跨 unit 二阶段门

局部 `mechanical_validation_status=PASS` 只进入临时候选，不构成质量完成。finalize 使用冻结 chunk 的
`masked_text` 与候选 bundle 的 `masked_text` 建立成对作者视图，保护占位符内部字节不进入
统计。Voice 门只消费 Profile 注册表中可机械重建的特征和负控：DEFAULT 的 PASS 表示场景
默认工件、逐 unit validator 与披露闭合，个人声线状态固定为 `NOT_APPLICABLE`；PERSONAL
至少需要 6 个目标正文块，逐 feature 核对当前 extractor hash、before/after 支持数和比例，
只拦截显著回退，不因样本常用连接词、括号或分号而强迫目标正文插入这些形式。所有结果均
保持 `identity_verified=false`。

跨 unit 门先运行 `LEX-REPAIR-01`，再由 `load_humanize_negative_guards.py` 严格加载当前
detector-only registry，运行其中适用于当前场景的 `negative_guard`。loader 只返回
`id/scene/detector` 及派生状态，完整 action-profile builder 不进入此运行链，`positive_action`
没有可执行入口。完整安装版 catalog 还必须先执行固定来源权限：只有
`MODEL_GENERATED/MODEL_ORIGIN_UNRESOLVED` 的负例 detector 可进入运行集，`UNKNOWN`、
`HUMAN_CONFIRMED`、`OCR_INHERITED`、`THIRD_PARTY` 的负例记录均为 `AUDIT_ONLY`。匹配视图使用
NFKC，删除零宽字符与汉字内部空格，但不跨保护占位符、段落或结构
边界拼接。只有 after 相比同一 unit 的 before 新增 occurrence，并在至少两个 unit 达到 detector
阈值时才拦截；原文已有且未增加的重复只进入 inherited 证据。命中时只把拥有新增 occurrence
的 unit 从临时接受集回退为 `UNRESOLVED`，删除其待发布 diff，并以原文组装 partial。证据写入
`validation/cross_unit_repetition.json`，包括 finding fingerprint、unit inventory、逻辑文档 hash、
lexicon、registry 原始字节、canonical registry 和 detector 定义 hash。命中 unit 属于 transaction
时，阻断集合必须先扩展到同一 transaction 的全部 member，再共同撤销两侧 diff/replacement；不能
让后置 repetition 门拆开已经通过 fragment validator 的 pair。registry 缺失、非法
UTF-8、重复键、未知字段、schema/scene/regex/threshold 漂移，partial 范围或任一适用负例
guard 不可用时只能 `REVIEW`，不能按空 registry 继续。

## 15. 合并与冲突

按 include 顺序和 unit 顺序合并。使用以下优先级：

1. 用户最新明确修改；
2. 快照后外部修改；
3. owner unit 的已验证 patch；
4. 未修改原文。

若源文件在处理期间变化：

- 不直接覆盖；
- 尝试用锚点做三方定位；
- 只有上下文唯一且保护区未变时才重放 patch；
- 其他情况标 `CHANGED_AFTER_SNAPSHOT` 并保留外部修改。

不要用“最后写入者胜出”覆盖用户变化。

## 16. 独立复读

把当前候选作为唯一正文重新阅读，并按本 Skill 的普通 REWRITE 合同独立决定是否仍需实质修改。不要查找旧 diff、旧 decision、验收条件或控制面工件；这些内容在 generator projection 中不可用。

## 17. 编译与格式检查

这些检查只验证编辑没有破坏文件形式，不评价内容。

### 17.1 TeX 检查

优先使用项目现有构建命令。若没有，至少检查：

- 花括号与环境边界是否平衡；
- `\begin` / `\end` 是否配对；
- 引用键、标签和文件引用是否原样保留；
- verbatim、代码和数学环境哈希是否不变；
- 主文件是否仍能解析 include 图；
- 已存在的编译流程是否成功退出。

只报告由编辑引入的形式错误。不要借编译过程分析公式或论证。

逐 unit 的 `FRAGMENT` 检查只解决 chunk 边界造成的假不平衡；发布前的整文件检查仍按本节
全部条件执行。validation 证据必须公开 `document_scope`，warning request 也必须绑定该字段，
防止把 fragment request 重放到 document 检查或反向重放。

### 17.2 Markdown 检查

检查：

- fenced code block 是否闭合；
- 标题层级是否符合授权；
- 表格列数是否保持；
- 链接目标和引用定义是否不变；
- 列表层级是否未意外漂移；
- YAML frontmatter 是否保持原样。

### 17.3 格式失败处理

定位失败到最小 unit，回滚该 unit，重跑检查。若项目原本就无法编译或格式检查已有失败，记录 baseline，不把它归因于本次编辑，也不要在纯文风任务中修复。

`--check-command` 默认在 `.compile_check_staging/` 的一次性副本中执行，不直接接触待发布的 staging、run/source 快照或原始源文件。命令必须由调用方选用项目现有构建流程；若构建依赖原项目资产，应在命令中显式设置搜索路径或调用能接受派生主文件的现有脚本。检查副本会在命令后删除；命令在副本中产生的辅助文件不进入发布目录。收尾器同时对真实 staging 和 run 产物做前后文件集合/字节哈希核对，任何新增、删除或修改都使 `compile_check=FAIL`。未提供命令时 `compile_check=NOT_RUN`，但全文结构不变量仍会逐文件运行。不得把 `NOT_RUN` 写成编译通过。

检查命令默认有界运行 300 秒，可用正数参数 `--check-timeout-seconds` 缩短或延长；零、负数、`NaN` 与无穷值均拒绝。超时固定输出 `compile_check.status=FAIL`、`exit_code=124`、`timed_out=true` 与实际 `timeout_seconds`，并先走当前平台的完整后代清理，再读取编译输出和专用状态 FD。未超时和未执行检查时 `timed_out=false`；未提供命令时 `timeout_seconds=null`。专用状态 FD 读取也有独立短截止时间和 64 KiB 上限，只接受恰好一条、字段严格为 `cleanup/command_exit` 且退出码与 wrapper 实际退出码一致的记录；写端不关闭、超量、多记录、额外字段、退出码错配、非法编码或非法 JSON 一律使后代清理状态为 `FAIL`，不得让收尾器无限等待或把不完整状态当成成功。

执行检查命令时还要收拢其进程树。Windows 固定先启动不执行用户命令的受控 wrapper，把它加入
启用 `KILL_ON_JOB_CLOSE` 的 Job Object 后才发送命令；wrapper 返回后终止整个 job，再做哈希
复核。wrapper 解释器固定使用 `-I -S -X utf8`，不得让用户 site、`sitecustomize` 或
`PYTHONPATH` 在 containment 建立前执行启动代码。Job Object 创建、配置、分配或终止异常时必须
关闭已经取得的 handle；若分配失败，则不得发送用户命令，并须有界重试直接终止 wrapper，无法
确认退出即记 `FAIL`。结果记录 `process_containment=WINDOWS_JOB_OBJECT` 与
`descendant_cleanup=PASS`。Linux 使用独立 process group 与先于用户命令启用的 child subreaper；
wrapper 正常返回或收到 `SIGTERM/SIGINT` 时，都必须先停止并等待直接 shell，再杀死、收割其收养的
`setsid()` 脱离后代，最后通过专用继承 FD 回报清理状态。父进程中断时先让仍存活的 wrapper 自清理；
第二次中断不得跳过 `terminate/kill/wait` 的剩余有界清理。若超时，必须在 wrapper 仍存活且后代
关系仍可由 `/proc` 观察时先清理全部后代；每轮与末次扫描后都要重新确认 wrapper 存活，再杀 wrapper
和残余 process group。成功记录 `LINUX_SUBREAPER_PROCESS_GROUP`；Linux `prctl` 不可用时记录
`LINUX_SUBREAPER_UNAVAILABLE`，其他 POSIX 记录 `POSIX_SUBREAPER_UNSUPPORTED`。若 wrapper/Job
启动、配置或分配阶段抛出无法归类的平台异常，记录通用 `UNAVAILABLE`；这些标签均不得执行
未受控的用户命令。后代清理失败使 `compile_check=FAIL`。只等待直接 shell、先杀 wrapper、只清理
同组进程，或只在返回前多算一次 hash 都不合格：后台子进程可以脱离 session，并在正式目录发布后
继续写入。

## 18. 乱码与异常

遇到乱码时：

1. 尝试识别已有文件编码，不转换源文件；
2. 若同一段在候选编码下均不可读，标 `OCR` 或 `SKIPPED_GARBLED`；
3. 保存位置、行号范围和哈希；
4. 跳过该段，继续其他单元；
5. 不猜字、不调用上下文补写；
6. 交付时汇总跳过范围。

遇到截断命令、未闭合环境或无法解析的嵌套结构时，标 `UNRESOLVED`。不要为完成覆盖率擅自修复结构。

CLI 参数语法错误仍由 argparse 以 usage/error 和退出码 `2` 表示；finalize 运行期异常必须输出
结构化 JSON `status=FAIL, delivery_gate_status=FAIL, publish_state=FAILED, exit_code=1`。不得让无
JSON 的 argparse 退出码 `2` 冒充正常的交付 `REVIEW/2`。

## 19. 完成交付

输出以下长文交付摘要：

```yaml
snapshot_id:
files_total:
files_changed:
units_total:
units_done:
units_no_change:
units_protected:
units_garbled:
units_unresolved:
units_changed_after_snapshot:
scenes:
voice_profile:
diffs:
assembly_replay_idempotency:
humanize_second_pass_convergence:
second_pass_stability_status:
second_pass_quality_clearance_granted:
scene_routing_status:
voice_binding_status:
voice_conformance_status:
structural_plan_status:
structural_semantic_mapping:
structural_semantic_review_status:
structural_semantic_review_requests:
structural_changes_applied:
structural_transactions_total:
structural_transaction_declines_total:
structural_transaction_candidates_total:
structural_transaction_candidates_executed:
structural_transaction_candidates_declined:
structural_transaction_candidates_pending:
structural_transaction_candidate_coverage_status:
structural_transaction_scope_complete:
structural_transaction_candidate_dispositions:
structural_transaction_decline_results:
structural_transaction_results:
structural_transaction_review_requests:
structural_transaction_rolled_back_ids:
candidate_assembly_status:
mechanical_validation_results:
paired_quality_review_request_coverage_status:
paired_quality_gate_status:
paired_quality_review_requests:
paired_quality_units_total:
paired_quality_units_pending:
paired_quality_units_missing:
paired_quality_clearance_granted:
rewrite_intent_coverage_status:
rewrite_intent_evidence:
rewrite_intent_units_pass:
rewrite_intent_units_review:
rewrite_intent_units_missing:
delivery_gate_status:
publish_state:
cross_unit_repetition_status:
coverage_completion_claim_allowed:
humanize_completion_claim_allowed:
format_check:
compile_process_containment:
compile_descendant_cleanup:
run_state_restored_after_failure:
finalization_metadata_preserved:
failed_attempt_metadata_path:
```

附上：

- 修改文件列表；
- 每节 diff 或其目录；
- 覆盖账本；
- `UNRESOLVED`、乱码和活动文件变化位置；
- 使用场景默认声线的披露；
- 格式检查结果。

只有 `PENDING` 和 `IN_PROGRESS` 均为 0 时，才能结束本轮。存在明确列出的
`UNRESOLVED` 不等于隐瞒未完成；必须准确说“可处理范围已完成”，不要说“全文完成”或
“无遗漏”。任何 `UNRESOLVED`、`SKIPPED_GARBLED` 或 `CHANGED_AFTER_SNAPSHOT` 都使
`coverage_completion_claim_allowed=false`；Voice、全局重复或 fresh second pass 未评估时，
`humanize_completion_claim_allowed=false`。

机器可读完成证据以 `finalization_metadata.json` 为准：

- `candidate_assembly_status=PASS`：没有硬失败、PENDING 或未决单元，只证明候选组装完成；
- `unit_status_scope=CANDIDATE_ASSEMBLY_NOT_DELIVERY`：`DONE/NO_CHANGE` 只属于单元候选账本；
- `status/delivery_gate_status=PASS`：候选组装完成，且结构语义与 paired-quality 均已获得可信 clearance；
- `status/delivery_gate_status=REVIEW`：仍有 PENDING/UNRESOLVED，或完整候选仍待结构语义/paired-quality 外部复核；
- `status=FAIL`：全文形式检查、编译门或完整输出幂等检查失败；
- `processable_scope_complete=true`：PENDING/IN_PROGRESS 为 0，不代表无乱码或未决；
- `coverage_completion_claim_allowed=true`：覆盖终态闭合、无未决且无硬失败，只允许声明
  覆盖与局部保护闭合；
- `scene_routing_status`、`voice_binding_status`、`voice_conformance_status`、
  `cross_unit_repetition_status`：分别报告逐单元场景、Profile 绑定、声线符合性和跨块新增
  模板；`NOT_EVALUATED` 不得改写成 PASS；
- `assembly_replay_idempotency`：同一 rewrite bundle 的派生字节重放；不是二次 Humanize；
- `humanize_second_pass_convergence`：把上一轮 clean 输出作为新输入的 fresh second pass；
- `second_pass_stability_status`：只把 second-pass 结果解释为
  `CONVERGENCE_OBSERVED/DISAGREEMENT_OR_INCOMPLETE/INVALID_EVIDENCE/NOT_RUN`；不承担质量放行；
- `paired_quality_review_request_coverage_status=PASS`：只证明所有可编辑 unit 都有当前 request；
  request 缺失时 coverage 为 `REVIEW`、quality gate 为 `BLOCKED`；齐全但未复核时 quality gate 为
  `PENDING_EXTERNAL_REVIEW`；无适用 unit 时两者为 `NOT_APPLICABLE`。`BLOCKED` 与 pending 都阻断
  正式交付；
- `rewrite_intent_coverage_status=PASS`：只证明所有 standalone unit 使用 unit v3、所有 executed
  transaction 使用 transaction v2，且每个 member 的 local intent/evidence span 与结构基线到候选的
  实际 diff、bundle/fragment、member diff、paired-quality request 和 transaction request 完整绑定；
  legacy、缺件、回滚或任一绑定失败为 `REVIEW`，阻断正式交付；
- `humanize_completion_claim_allowed=true`：上述 Humanize 级门全部通过，才允许“全文
  Humanize 已完成”；兼容字段 `full_completion_claim_allowed` 必须与它相同；
- `publish_state=REVIEW_CANDIDATE` 与 `rendered_review/`：机械完整但结构语义或文风质量待审，不能称为正式输出；
- `publish_state` 只使用 `FAILED/PARTIAL/REVIEW_CANDIDATE/FINAL`；调用方不得由目录存在与否猜状态；
- `structural_transaction_results`：逐 transaction 报告 ID、bundle hash、两个 member、全局 claim、
  两个 fragment gate、DOCUMENT gate、真实变化、原子回滚原因和 review request；其中任一 PASS
  都不能覆盖顶层 delivery gate；
- `structural_transaction_candidate_dispositions`：以冻结 inventory 为全集逐 ID 报告
  `EXECUTED/DECLINED/PENDING`。四项计数必须回加；`READY` 中任一 `PENDING` 都使候选覆盖
  `REVIEW`，即使全部 unit 已是 `NO_CHANGE`；
- `structural_transaction_decline_results`：只保存通过 strict schema、冻结 transaction/inventory、
  两个 chunk/Voice、具体理由和双 member 来源段证据校验的 decline 规范化记录；它是逐 decline
  审计证据，不是 inventory 全集，候选覆盖仍只能读取 dispositions 与四项计数；
- `rollback_manifest.atomic_transactions`：证明单边失败时 accepted/published member 均为 0；
- `source_files_modified=0`：原源文件没有被工具覆盖。
- `run_artifacts_changed_during_check=true`、`staging_artifacts_changed_during_check=true` 或
  `evidence_artifacts_changed_during_check=true`：检查命令通过绝对路径污染了快照、正文
  staging 或 validation/diff 证据；编译门必须 `FAIL`。检测到证据 staging 污染时，
  本轮未发布的 validation/diff 会被丢弃；若已有正式发布证据，必须保留旧证据而不覆盖。
- `staged_evidence_discarded=true`：本轮证据因污染被丢弃，不表示旧证据不存在，也不表示
  新一轮正文或文风验证通过。
- `run_state_restored_after_failure=true`：本轮失败后已恢复调用前 run-dir；此时 canonical
  `finalization_metadata.json` 与 validation/diff/rendered 仍属于上一轮，失败尝试只能读
  `last_failed_attempt_metadata.json`。其中 `failed_attempt_evidence_paths_reusable=false` 时，
  任何空路径都不得回填成 canonical `validation/...`；
- `compile_check.process_containment` 与 `descendant_cleanup`：只有实际执行检查命令且进程树清理
  为 `PASS`，才允许继续读取编译结果；`NOT_RUN` 不表示命令隔离通过。

Voice/Rewrite 绑定固定输出 `voice_profile_sha256`、`voice_profile_bindings_total/matched/missing/mismatched`、`rewrite_binding_status`、`rewrite_bindings_total/matched/missing/mismatched`、`voice_profile_default_units/default_scenes` 与 `voice_default_disclosure_required`。只有所有初始 `PENDING` unit 的最终 bundle 均回显精确 Voice hash 时，`voice_binding_status=PASS`；只有 unit 与 canonical chunk hash 也全部匹配时，`rewrite_binding_status=PASS`。尚未提交、缺失或错配时为 `REVIEW`。这些字段只证明 Profile 与目标块工件身份闭合。`voice_conformance_status=PASS` 另由注册机械特征非回退门产生，并公开 DEFAULT/PERSONAL basis、feature/negative-control 计数和限制；它仍不能证明完整作者气质或作者身份。

不得以 `units_done > 0`、`rendered_partial` 存在或准备器 `status=READY` 代替全文完成门。

## 20. 长文检查表

- [ ] 已固定字节长度、编码和 SHA-256；
- [ ] 已递归列出正文引用文件；
- [ ] 已排除模板、缓存、构建和生成文件；
- [ ] 已识别 TeX/Markdown 结构边界；
- [ ] 已区分作者正文和五类保护角色；
- [ ] 每个 unit 都有稳定锚点和唯一 owner chunk；
- [ ] 分块未切断环境、表格、列表、引语或公式；
- [ ] 重叠段只被 owner 编辑一次；
- [ ] 每个 unit 已路由场景并绑定 Voice Profile；
- [ ] 每个可编辑 unit 均有终态；
- [ ] 每个 `DONE/NO_CHANGE` unit 都有当前 paired-quality request；缺失时 gate 为 `BLOCKED`；
- [ ] 每个 `DONE/NO_CHANGE` unit 都有当前 rewrite-intent evidence；standalone v3 span 与 unit diff、
      transaction v2 fragment span 与结构基线到候选的局部 diff 双向覆盖；
- [ ] 每个修改 unit 均有可逆 diff；
- [ ] 保护区哈希全部通过；
- [ ] 活动文件追加未混入本轮；
- [ ] 幂等重跑没有同义词 churn；
- [ ] `rendered_review/` 未被用作 second-pass seed，second pass 未被当成质量 clearance；
- [ ] TeX/Markdown 形式检查已执行；
- [ ] baseline 失败与本次引入失败已区分；
- [ ] 乱码和未决位置已报告；
- [ ] 未用抽样结果代替全文覆盖；
- [ ] 未输出内容正确性或检测规避结论。
