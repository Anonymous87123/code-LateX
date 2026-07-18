# 中文学术纯文风 Humanize Skill：生产化交付与红队报告

2026-07-13 至 2026-07-17 的实用性复测、失败样本与机器验收见 [humanize_academic_chinese_usability_red_blue_report.md](D:/code%20LateX/elegantbook/physics/humanize_academic_chinese_usability_red_blue_report.md)。该报告明确区分机械候选可用、质量仍待可信外部复核和生成资格仍为 `NOT_EVALUATED` 的边界。

生成日期：2026-07-10  
本轮生产门更新：2026-07-17
Skill：`C:\Users\Lenovo\.codex\skills\humanize-academic-chinese`  
范围：只处理中文学术文风，不执行学术正确性、来源、实验、复现或检测规避审查  
证据优先级：可重放机器工件 > 独立评估代理连续阅读 > GPT MD/TEX 负例与压力材料 > 聊天语料统计

> **现行快照（v26，2026-07-18）**：下文 v1-v25 的数字和旧终态保留为历史证据，若与本段或第 30 节冲突，以 v26 为准。当前共运行 573 项测试，整体 `OK (skipped=2)`，即 571 项执行通过、2 项环境相关跳过；20 个脚本 `py_compile/--help` 全通过；两次 30 文件 generator projection 逐路径逐字节一致。普通 `REWRITE/NO_CHANGE` 即使机械通过，也固定生成成对质量复核请求并停在 `REVIEW/2 -> REVIEW_CANDIDATE -> rendered_review/`，本地工具不得签发质量 clearance。资格矩阵为 188 个原子，当前仍是 `0 PASS / 0 FAIL / 188 NOT_EVALUATED`；学术正确性、作者身份和无人值守全文交付均未通过。v26 同步了入口交付措辞、三态队列说明、历史 profile 标记和 candidate C 的分层退出码。完整修订见文末第 30 节。

## 1. 当前结论

这轮不再把“规则很多”当作完成。`humanize-academic-chinese` 已从纯规则库升级为“规则 + 可定位扫描 + 语义保护 + 统一验证 + 长文快照/收尾”的执行链，但仍保留一个明确边界：模型直接盲写的结果不能自动信任，必须经过验证器或人工复核。

当前能证明的结果：

- 29 组集中词项信号已与 Skill 规则直接关联，包含 197 个固定变体、46 个正则、28 组 signal 级上下文豁免、风险等级、阈值、动作和正反例；
- 扫描器可定位到文件、行、列、命中词、窗口计数、保护状态、豁免原因和建议动作；
- 不变量检查器能阻断公式、数字/单位、引语、代码、TeX 注释、关键命令、环境和花括号漂移，并把否定、模态、定义/命名和结果报告变化列为言语行为 warning；
- 统一验证器用精确 SHA-256 绑定改前/改后版本，退出码固定为 `0=PASS`、`1=FAIL`、`2=REVIEW`；
- 长文准备器和收尾器可生成固定快照、include manifest、保护占位块、覆盖账本、逐单元验证、diff、回滚清单、partial/full 发布状态和幂等记录；
- 工作区当前共运行 573 项自动测试，整体 `OK (skipped=2)`；这表示 571 项执行通过、2 项环境相关测试跳过，不写成“573 项通过、另有 2 项跳过”；
- 当前 4685 行、359087 字节的 `physics1.tex` 压力快照生成 60 个单元和 3164 个保护 span；v22 的完整结构候选即使覆盖闭合，也因结构语义待外部复核而保持 `REVIEW/2`；
- 三轮共 9 次历史代理盲测没有一份可计为当前生成资格证据；其中旧 `PASS` 缺少现行 provenance/request 绑定，只能作为归档失败或回归 fixture。
- 2026-07-14 的两次无答案泄漏 fresh forward 又发现两个 false-PASS：科研稿把“奠定坚实基础”轮换成“后续研究的出发点”，课程稿把“必须牢记”轮换成“必须注意”并生成“由此可以得出结论”。两组精确 before/after 已进入 scanner 和统一验证器回归，修复后均为 `REVIEW/2`。
- 三份旧人工校准输出属于 pre-provenance 归档证据。理由字符串不能证明真人身份，也不能用旧 warning 接受机制追认当前 `PASS/0`。
- 第四轮三路红队又找出 2 个短文保护 P0、2 个合同 P0 和 10 个执行链 P1；修复后，原本会误 `PASS/0` 的数学环境、题干、长 fence、中文数词、乱码和显式术语变化均转为 `FAIL/1`，非法编码、远距豁免和不充分理由转为 `REVIEW/2` 或参数拒绝；
- 旧 `aigc-down-skill` 退休前又执行三轮行为前测：第一轮发现引语定界符 P0、high 残留和无来源归因 P1；第二轮只剩混合请求新造桥接模板 P1；第三轮原例及两个变体 `P0=0/P1=0`。旧目录随后按固定 SHA 删除，新进程目录只保留本 Skill；
- 确定性工具链已通过当前回归门，但完整 188 原子前向矩阵尚未运行，生成模型总体资格为 `NOT_EVALUATED`：历史代理试验只作归档/回归证据，报告不再把“验证器能拦截”偷换成“模型已能稳定一次生成合格稿”。
- 资格 harness 已切换到 manifest v2 和 Skill 内固定 oracle：current case 不能再提交 `assertions/result/expected/check_ids/regex/command`，旧 v1 只能归档；此前可让违约 `MODE-01` 获得 PASS 的证明包现在返回 `integrity=FAIL`、`atoms_pass=0`。
- 固定 catalog 的历史 suite/check 结构只证明评分所有权已移出 manifest；v25 当前资格总面为 188 个原子，仍全部 `NOT_EVALUATED`，不能用旧 catalog 规模或局部机器检查代替完整前向。
- v13 已把全文 Voice 从 `NOT_EVALUATED` 改成受限但真实的机械门：DEFAULT 只证明场景默认、绑定、逐 unit validator 与披露闭合，个人声线状态固定为 `NOT_APPLICABLE`；PERSONAL 至少需要 6 个目标正文块，逐 feature 复核当前 extractor hash、before/after 支持数和显著回退，所有 PASS 仍固定 `identity_verified=false`。
- 跨 unit 门不再只扫描单块：它按 protected-masked before/after 聚合 `LEX-REPAIR-01`，并实际读取此前 MD/TeX 语料登记的 `negative_guard`。两个局部 PASS 的 unit 若共同新增“这里只……”或重复“不是……而是……”等模板，新增 occurrence 所在 unit 会从临时 DONE 回退为 `UNRESOLVED`，其 diff 不发布；原文继承重复保持可审计但不阻断。
- 本地 sealer 可从同一参数逐字节复现 catalog `public_context`；runner 当前只挂载 30 文件 generator projection，并在运行前后复核类型、路径、字节和 tree hash。投影不含 oracle，但宿主机不可达和完整 generator context 仍未验证，固定 trust policy 关闭 E3，证据继续封顶 E2。此前基础设施无效采集仍只作诊断记录，没有被补写成 output 或 E3 证据。
- v14 把 fresh second pass 从 `NOT_RUN` 假字段升级为独立控制面：第二遍从第一遍完整 `rendered/` 重建快照，每个 unit 使用同一无答案 sealed prompt 和独立 runner；receipt 必须绑定 plan、collection、run record、run seal、projection、Voice、scene 与活证据根，第一遍 finalizer 会当场重跑 verifier。缺 trial 或任一 REWRITE 为 `REVIEW/2`，工件漂移为 `FAIL/1`，可重算自哈希不再足够。

因此，这个 Skill 的生产定义不是“模型一遍生成就自然”，而是：

> 生成结果必须经过可复核的候选定位、保护检查、言语行为复核和完成态证据；任何未决项都不能被一句“已完成”覆盖。

## 2. 职责边界

### 2.1 它处理什么

- 固定句首、万能过渡和路线报幕；
- 假转折、假纠偏、段落流水线和统一节奏；
- 管理、审计、营销、教练和编辑后台腔；
- 抽象评价、创新表演、公式字幕和图表导览；
- 强制总结、自动展望、章节桥接和机器闭环；
- 过度对称、均等用力、模态缓和堆叠；
- Humanize 修复语自身形成的新模板。

### 2.2 它不处理什么

- 数学、公式或推导是否正确；
- 引文、资料、数据或事实是否真实；
- 实验、模型、代码或结果是否可复现；
- 创新是否成立、研究质量是否足够；
- 作者身份、AIGC 概率或检测规避。

“保护原意”只是一条编辑边界，不是事实审查。旧 `deai-*` 质控 Skill 没有被并入本执行链。

## 3. 生产架构

```text
用户任务
  -> SKILL.md：模式、场景、强度、输出、优先级
  -> lexical-signals.json：集中信号与上下文动作
  -> scan_humanize_chinese.py：候选定位
  -> extract_detector_report_scope.py：报告可见标注的 scope-only 映射
  -> 场景规则 + Voice Profile：人工/模型改写
  -> check_humanize_invariants.py：硬保护与言语行为差异
  -> validate_humanize_output.py：PASS / FAIL / REVIEW
  -> 短文生成待审候选，或进入长文 prepare/finalize
```

长文链：

```text
prepare_humanize_long_document.py
  -> snapshot + include manifest + units + protected placeholders + initial ledger
  -> 独立 rewrites/<unit_id>.json
finalize_humanize_long_document.py
  -> placeholder restore + per-unit validation + diff + staging
  -> rendered_partial、rendered_review 或（仅有可信外部 clearance 时）rendered
  -> candidate assembly 与 delivery gate 分开裁决
  -> final ledger + rollback manifest + idempotency evidence
```

主 `SKILL.md` 当前为 329 行，负责决策和路由；大型规则按需加载。排除 `__pycache__` 后，Skill 的 `.md/.json/.py/.yaml/.yml` 共 58 个文件、39782 个物理行，不会在每次普通调用时全量加载。

## 4. 文件与规模

| 组件 | 行数 | 职责 |
|---|---:|---|
| `SKILL.md` | 329 | 核心模式、优先级、高风险快检、报告/混合请求门和完成门 |
| `lexical-signals.json` | 602 | 29 组词项/句壳信号及上下文合同 |
| `pathology-catalog.md` | 527 | `HUM-01` 至 `HUM-16` 病灶库 |
| `course-notes.md` | 246 | 课堂场景规则 |
| `modeling-engineering.md` | 273 | 建模场景规则 |
| `research-journal.md` | 277 | 科研场景规则 |
| `rewrite-patterns.md` | 504 | `CP/MP/RP` 各 20 组改写模式 |
| `voice-profile.md` | 578 | 作者样本准入、字段、置信与跨场景迁移 |
| `detector-report-intake.md` | 199 | 报告静态输入、唯一源文映射、scope-only 与拒绝边界 |
| `operational-contract.md` | 542 | 参数、权限、角色、决策和交付合同 |
| `evaluation-contract.md` | 707 | 行为 fixture、失败级别、manifest v2、确定性发布门和 188 原子生成资格门 |
| `long-document-workflow.md` | 986 | 快照、单元、只读上下文、结构 review、diff、回滚、编译、幂等与成对质量门 |
| `structural-rewrite-contract.md` | 506 | STRUCTURAL 来源段映射、结构基线、事务候选、语义复核请求和状态裁决 |
| `scan_humanize_chinese.py` | 606 | 词项扫描、编码覆盖账本与 TeX/MD 保护识别 |
| `check_humanize_invariants.py` | 1100 | 硬不变量、显式术语与言语行为检查 |
| `extract_detector_report_scope.py` | 555 | 静态 HTML 标注提取、唯一规范化映射和报告输入审计 |
| `validate_humanize_output.py` | 1268 | 统一验证、finding 级裁决、request-bound warning proposal、机械层与成对质量请求 |
| `prepare_humanize_long_document.py` | 1924 | 长文准备、切块、编码审计、动态 include 未决记录、事务 inventory 和初始账本 |
| `finalize_humanize_long_document.py` | 6108 | 单元验收、质量/结构请求、run-dir 事务、进程树收拢、派生发布和回滚 |
| `build_humanize_action_profile.py` | 715 | 验证 MD/TeX 来源锚点并生成不含原文摘录的动作 profile |
| `validate_humanize_candidate_queue.py` | 1800 | 冻结候选、来源、策略和工具快照，执行复制/负例与 PASS/REVIEW/FAIL 三态队列门 |
| `prepare_humanize_candidate_revision.py` | 205 | 建立候选血缘并清空不可跨 revision 重放的 warning 状态 |
| `build_humanize_generator_projection.py` | 1348 | 30 文件闭集、SKILL 确定性删节、类型/引用/控制 ID/TOCTOU 审计和规范 manifest |
| `audit_humanize_generation_qualification.py` | 4903 | 固定 oracle、trust policy、投影独立重建、manifest v2、188 原子和三态聚合 |
| `run_humanize_generation_trial.py` | 1230 | 投影挂载、staged-case 双向核对、JSONL/receipt/run record/seal 与本地 E2 上限 |
| `seal_humanize_public_fixture.py` | 261 | 生成 hash-bound input/prompt/public-context，拒绝结构性答案泄漏和额外文件 |

排除 `__pycache__/` 后，整个 Skill 中 `.md/.json/.py/.yaml/.yml` 共 58 个文件、39782 个物理行。生成器投影视图固定为 30 个文件；其中 26 个能力文件原样保留，4 个文件执行固定控制面剥离，oracle、fixtures、trust policy 和资格脚本不会进入生成上下文。

## 5. 集中词库

### 5.1 数据结构

每个信号包含：

```text
id / category / label / variants / regex / scenes / severity
threshold / exclusions / action / rationale
positive_examples / negative_examples / provenance
```

当前统计：

| 项目 | 数量 |
|---|---:|
| signal / category | 29 / 29 |
| 固定变体 | 197 |
| 正则 | 46 |
| signal 级上下文豁免 | 28 |
| high / medium / low | 7 / 15 / 7 |
| `DELETE / REWRITE / REVIEW` | 2 / 5 / 22 |
| 正例 / 反例 | 32 / 29 |

词库不输出“AI 分数”，也不把单次命中当作作者身份证据。

### 5.2 最重要的可落地抓手

| 词族 | 常见变体 | 默认动作 | 不能机械处理的情形 |
|---|---|---|---|
| 空重点壳 | 值得注意的是、需要指出的是、必须强调的是 | `REWRITE` | 后句确实承担突变且无更直接定位方式 |
| 教练腔 | 必须牢记、必须/务必记住、秒杀、救命表、锁死答案 | `REWRITE` | 用户锁定原句或确属题干/引语 |
| 营销拔高 | 全面提升、深刻/深入揭示、填补空白、全新范式、提供有力支撑 | `REWRITE` | 引用标题或用户锁定原主张；仍应优先具体化 |
| 管理施工腔 | 收口、核心抓手、锁定故事线、形成……闭环 | `REWRITE` | 闭环控制、机械抓手、门禁系统等正式术语 |
| 编辑后台 | 正文里要、表格的作用是、下一段负责、对论文写作而言 | `DELETE` | 文章本身研究写作方法时需人工复核 |
| 章节桥接 | 为后续奠定/打下基础、是后续……的基础、为后续提供支撑 | `DELETE` | 真有具体承接对象时改成对象，不保留空壳 |
| 自动展望 | 未来/后续可进一步、后续拓展应用场景 | `REVIEW` | 原文提供明确未决对象、方法和优先级 |
| 模态堆叠 | 可能、或许、一定程度、某种意义、某些启发 | `REVIEW` | 不同词分别限定概率、范围和证据状态 |
| 结果句壳 | 结果表明、结果显示、分析表明反复起句 | `REVIEW` | 单次结果报告是应保留的言语行为 |
| 修复模板 | 这里只看、这里真正、其余沿用、不再展开 | `REVIEW` | 单次真实取舍可保留；跨段重复要改 |

### 5.3 不是禁词表

以下单词单独出现不构成病灶：

- `因此`：证明链中可连续承担真实因果；
- `本文`：可承担作者指代；
- `框架/机制`：可能是正式分类；
- `结果表明`：保留结果报告状态；
- `链条/落地`：可能是力学实体和运动过程；
- `闭环`：可能属于控制理论。

扫描器必须结合窗口、场景、保护角色和豁免正则。`KEEP` 不是静默忽略，而是需要说明具体表达功能。

## 6. 逐文档连续阅读如何改进扫描器

5119 行 `physics1.tex` 的第一次扫描返回 24 个候选，其中大量是误报：

- “柔软链条、微元链条、链条下落”被当成管理词“链条”；
- “落地点、碎片同时落地”被当成项目“落地”；
- `exercise/example/theorem` 内题干和正式陈述被当作作者正文；
- TeX 的 ``直接引语'' 未进入保护区。

人工读完命中上下文后，增加了：

- 力学实体链条与落地过程豁免；
- `exercise/example/problem/question` 题干保护；
- `theorem/lemma/proposition/corollary/definition` 正式陈述保护；
- TeX 双反引号与 `\enquote/\textquote` 引语保护。

重跑同一 5119 行文件后，候选从 24 降到 2，只剩同一作者解释段中的两处 `不是……而是……`，需要结合教学功能人工判断。运行时间约 0.5 秒。

这正是“脚本先跑、人工多读、再反推规则”的具体效果，而不是继续堆禁词。

## 7. 保护与语义不变量

### 7.1 硬保护

以下变化直接 `FAIL/1`：

- Markdown/TeX 代码、行内代码和 verbatim；
- 行内/陈列公式及数学环境；
- 直接引语；
- 数字、范围和单位；
- `label/ref/eqref/cite/url/includegraphics` 等关键 TeX 命令；
- TeX 注释和转义百分号；
- 环境顺序、嵌套和平衡；
- 未转义花括号平衡。

### 7.2 言语行为

以下变化默认进入 `REVIEW/2`：

- 否定：`不、未、无、并非、并不意味着`；
- 模态：`可能、或许、仅、只、必须、应当、需要`；
- 定义/命名：`称为、定义为、记作、以下简称`；
- 假设：`设、假设、假定`；
- 报告/观察：`结果表明、观察到、我们发现`；
- 条件：`若、当、仅当、除非`。

这解决了“本文将 q<0 的样本称为 X”被改成“q<0 的样本是 X”而数字术语都未变的问题。

### 7.3 本地处理建议不能充当人工放行

非硬性 warning 首次出现后，先保存验证器生成的 `warning_review_request.request_sha256`
和逐条 `warning_fingerprint`。本地调用方只能提交绑定当前 request 的处理 proposal：

```powershell
--propose-warning-resolution <warning_fingerprint>=建议核对是否只删除重复缓和 `
--warning-review-request-sha256 <request_sha256> `
--warning-reviewer-kind HUMAN `
--warning-reviewer-id <调用方标签>
```

proposal 会写入机器产物，但固定为 `identity_verified=false`、
`review_clearance_granted=false`，warning 仍 pending，退出码仍为 `2`。当前本地工具没有
代理不可访问私钥的外部信任根，因此调用方自称 HUMAN 不能放行；只能修改稿件，让 warning
在新 artifact 上消失。未知 fingerprint、空泛建议、跨稿件重放和所有硬错误都不能豁免。

## 8. 模式、权限和作者声线

### 8.1 三模式

- `DIAGNOSE`：只诊断，不改正文；
- `REWRITE`：按强度改写并验证；
- `DRAFT`：只使用用户已提供内容起草。

诊断模式不会再落入 Rewrite 三轮，也不会声称“已调整”。

### 8.2 三强度

- `LIGHT`：只改局部词句，不移动/合并段落；
- `BALANCED`：允许段内和相邻重复调整，不跨节；
- `STRUCTURAL`：只有明确授权才跨段重排，必须交付 patch。

用户结构锁、标题锁和 scope 高于所有文风偏好。

### 8.3 Voice Profile

有作者样本时才建立 Profile，字段覆盖：

- 第一人称与自指；
- 句长和标点；
- 括号、短语和术语；
- 段落压缩度；
- 限定方式和转场；
- 言语行为与场景差异。

无样本时明确 `SCENE_DEFAULT`，不得声称复现个人声线。定义组、标准条款和等权比较不为“人味”强行制造重点。

## 9. 统一验证器

命令：

```powershell
python scripts/validate_humanize_output.py before.md after.md `
  --scene RESEARCH `
  --format json
```

状态：

| 状态 | 退出码 | 条件 |
|---|---:|---|
| `PASS` | 0 | 无硬错误、无未接受 warning、无未解释 high、无新增模板 |
| `FAIL` | 1 | 任一硬不变量失败 |
| `REVIEW` | 2 | 言语行为 warning、high 残留或改后新增候选 |

输出绑定：

- 改前/改后绝对路径；
- 改前/改后 SHA-256；
- 文档格式；
- invariant errors/warnings；
- before/after/introduced 候选数；
- high 残留位置；
- `keep_reasons`；
- `accepted_warning_reasons`。

只做目测、只比较一部分、脚本运行后又改文，都只能写 `NOT_RUN`。

## 10. 长文生产链

### 10.1 准备

```powershell
python scripts/prepare_humanize_long_document.py physics1.tex `
  --output C:\Users\Lenovo\.codex\reports\humanize_longdoc_physics1_20260710_v2 `
  --scene COURSE
```

真实结果：

| 指标 | 值 |
|---|---:|
| 输入行数 | 5119 |
| 文件数 | 1 |
| snapshot ID | `cd5fc9b656012aad` |
| 单元数 | 60 |
| `PENDING` | 51 |
| `SKIPPED_PROTECTED` | 9 |
| 保护 span | 3454 |
| 最大单元行数 | 329 |
| 最大可编辑汉字 | 2278 |
| 可编辑汉字合计 | 26766 |
| 准备状态 | `READY` |

`READY` 只表示快照和单元可用；准备器固定写 `completion_claim_allowed=false`。

### 10.2 改写包

`REWRITE`：

```json
{
  "decision": "REWRITE",
  "masked_text": "含完整 [[PROTECTED:...]] 的改写文本",
  "keep_reasons": {}
}
```

只有提交本地处理 proposal 时，才额外携带 `warning_resolutions`、
`warning_review_request_sha256` 和仅含 `reviewer_kind/reviewer_id` 的 `warning_review`；
这些字段不能把单元从 `REVIEW` 提升为 `PASS`。

`NO_CHANGE`：

```json
{
  "decision": "NO_CHANGE",
  "reason": "正式定义组保持原有等权结构"
}
```

占位符缺失、重复、未知或 hash 不符会原子拒绝该单元。复制原文却写 `REWRITE` 也会被拒绝。

### 10.3 收尾、diff 和回滚

```powershell
python scripts/finalize_humanize_long_document.py `
  --run-dir <run-dir> `
  --rewrites <rewrites-dir> `
  --check-command "<project build command>"
```

空 rewrites 的真实压力测试结果：

- `status=REVIEW`；
- `exit_code=2`；
- `PENDING=51`；
- `full_completion_claim_allowed=false`；
- `published_path=rendered_partial`；
- `source_files_modified=0`；
- `compile_check=NOT_RUN`；
- 同一快照和空 rewrites 复跑：`idempotency=PASS`，`source_files_changed_since_snapshot=0`。

编译失败时 staging 移到 `failed_staging/`，不发布 `rendered/`；原源文件从未被覆盖。完整输出复跑哈希不同则保留 `non_idempotent_staging/` 并失败，不覆盖已发布版本。

## 11. 前向测试

### 11.1 方法

每轮分别开新代理，只提供 Skill 路径、普通用户式请求和原始段落；不提供预期答案，不允许编辑本地文件。课堂、建模、科研各一份。

### 11.2 三轮结果

| 轮次 | 课堂 | 建模 | 科研 | 共同结论 |
|---|---|---|---|---|
| V3 | 留下“必须牢记”；虚报 PASS | 高风险词与模态堆叠几乎原样；虚报 PASS | 模态堆叠与桥接残留；虚报 PASS | `0/3` 可发布 |
| V4 | 停止虚报，但留下“必须牢记/打下基础” | 停止虚报，但留下“全面提升/完整闭环/有力支撑” | 停止虚报，保义较好，但“深刻→深入揭示”并保留基础句壳 | `0/3` 可发布 |
| V5 | 改成“必须记住/是后续的基础” | 核心结果已具体化，只剩泛化后续展望 | 模态和防御串改善，仍改成“构成后续研究基础” | `0/3` 自动 PASS，但均诚实 `NOT_RUN` |

V3、V4、V5 的正文均已保存为 fixture。验证器能稳定指出：

- V3 教练腔、营销词和基础句壳；
- V4 长闭环正则、`深入揭示` 同义规避和 `打下基础`；
- V5 `必须记住`、`是后续……基础`、泛化应用场景和 `构成后续研究基础`。

这组结果否定了“Prompt 写得很详细就自然会执行”的假设。生产安全来自验证门，不来自对模型自觉的期待。

### 11.3 旧人工校准的现行证据等级

三份 gold fixture 在旧验证器下记录过：

- 硬不变量错误 0；
- high 残留 0；
- introduced candidate 0；
- 定义、结果报告、引语、公式、数字和单位保留；
- 非硬性语气变化先 REVIEW，再逐项写理由；
- 旧机器结果记录为三场景 `PASS/0`。

这些 fixture 没有当前 `warning_review_request`、artifact/policy 绑定或可验证审阅来源，按现行合同只能归档为 pre-provenance 证据，不能证明真人复核，也不能计入生成资格 PASS。

## 12. 测试覆盖

当前 Humanize 工具链、generator projection、资格审计、public-case 采集链与旧入口退休门直接测试共 337 项：

| 测试模块 | 项数 | 主要覆盖 |
|---|---:|---|
| Skill 结构与合同 | 27 | 链接、触发、唯一枚举、精确 provenance、Voice round-trip、谓词来源门、语料动作锚和编辑载荷边界 |
| 词项扫描 | 22 | 正反例、场景、保护、局部豁免、编码覆盖账本、旧规则蒸馏、真实 TeX 误报、同义说教与去标签展望回归 |
| 不变量 | 32 | 公式、题干、长 fence、引语、数字、乱码、显式术语、环境、归因言语行为和三类跨版本命题升级 |
| 统一验证 | 41 | PASS/FAIL/REVIEW、finding 级理由、术语证据、request-bound proposal、v7/v8 false-PASS 与 v9/v10 三场景真实前向回归 |
| 报告范围提取 | 6 | 静态 HTML、恶意脚本隔离、唯一/缺失/歧义映射、无源与重复标注 |
| 长文准备 | 12 | include、动态 include 未决、UTF-16/NUL、固定字节、单元、占位、装饰 TeX 授权和产物 |
| 长文收尾 | 43 | 恢复、防复制、累计 partial、NO_CHANGE/high 复核、幂等、证据保全、编译回滚、冻结快照和 proposal 绑定 |
| 来源动作 profile | 6 | 23 个可读来源、动作卡锚点、排除/乱码状态和 GENERAL 语料不足 |
| 候选队列 | 37 | 冻结输入/来源/策略、跨块复制、负例 guard、TOCTOU、脱敏、事务发布和幂等身份 |
| 候选 revision | 4 | 血缘、旧 request/proposal/reviewer 状态清除和跨 revision 重放拒绝 |
| 实用性归档证据 | 10 | 历史 run 状态、pre-provenance 失败、报告与 manifest 边界 |
| generator projection | 30 | 26 文件闭集、内容批准 hash、锚点漂移、控制 ID、引用闭包、文件与根 symlink/reparse/junction、hardlink、原子发布和确定性 tree |
| 生成资格 harness | 34 | 固定 oracle/trust、投影独立重建、四件套证据、旧自证攻击、163 原子、hash 漂移和 FAIL 优先聚合 |
| public-case runner | 17 | strict public context、隐藏 ID 泄漏、投影 manifest 对齐、staged case/投影运行中漂移、失败 receipt 和 E2 seal |
| public-case sealer | 5 | 原子 ID/编码/既有目录拒绝、seal 往返和四个 catalog context 逐字节复现 |
| 场景 Skill 集群 | 5 | 路由所有权与纯文风/学术质控隔离 |
| 旧入口退休门 | 6 | 安全 intake、活跃引用归零、危险行为拒绝、fixture schema 和旧目录删除 |

工作区全量：`Ran 355 tests ... OK (skipped=1)`，即 354 项通过、1 项跳过；skip 仅因当前 Windows 账户不能创建文件 symlink；根 junction、reparse 检测和 hardlink 攻击测试均已实际执行。
官方 Skill 校验：`Skill is valid!`。  
13 个脚本均通过 `py_compile` 与 `--help`；统一验证、来源 profile、projection builder、资格 harness 和 sealer 已做真实 CLI 调用。runner 也实际启动过 Codex，但因独立 CLI 认证 401 只形成 `INFRA_INVALID` 记录，未形成前向样本。

## 13. 原 P0/P1 漏洞闭环

| 原漏洞 | 当前证据 | 状态 |
|---|---|---|
| 无独立词库和扫描器 | 28 组 JSON 信号 + 定位 CLI + 20 项扫描测试 | 已解决 |
| 绿灯只查数量 | 337 项 Humanize/projection/资格/采集链/退休行为测试；`tests_total` 明确不计资格覆盖 | 已解决 |
| 言语行为漂移 | 6 类 marker warning + request-bound proposal；本地 proposal 不放行 | 已解决到当前规则覆盖；内容语义仍需人工判断 |
| 强制制造主次 | 等权结构优先、`NO_CHANGE`、结构权限 | 已解决 |
| 正式术语误伤或漂移 | 上下文豁免、finding 级 KEEP、`--term` 次数/顺序硬比较和术语表哈希 | 已解决到显式术语表层；未提供术语表时为 `NOT_PROVIDED` |
| Diagnose/Rewrite 冲突 | 模式分支与独立输出合同 | 已解决 |
| 无作者声线 | Voice Profile 与 `SCENE_DEFAULT` 披露 | 已解决 |
| 无强度/结构授权 | LIGHT/BALANCED/STRUCTURAL + locks/scope | 已解决 |
| 长 TeX 不安全 | prepare/finalize、占位、账本、diff、回滚、幂等 | 已解决到工具链层 |
| 引语/题干/OCR 无分层 | 六类来源角色 + TeX 环境保护 | 已解决 |
| 常见句壳缺失 | 175 变体 + 40 正则族 | 已解决并持续回归 |
| 无关键词 AI 腔 | 模态密度、抽象密度、修复模板 | 已解决 |
| 推理链误伤 | 真实证明链与规范步骤豁免 | 已解决 |
| 命中后无动作 | KEEP/DELETE/REWRITE/REVIEW/NO_CHANGE/UNRESOLVED | 已解决 |
| 优先级加载不到 | 主 Skill 路由到 quick checklist/workflow/gates | 已解决 |
| 输出合同不统一 | operational contract 为唯一枚举来源 | 已解决 |
| 三场景同质 | 课堂/建模/科研独立规则、三轮 9 次盲测和 3 份人工 gold | 规则层已区分；历史样本仅作归档/回归，完整矩阵未运行，总体资格为 `NOT_EVALUATED` |
| 修复语形成新口头禅 | `HUM-16` + introduced-candidate gate | 已解决 |
| 载荷过重 | 386 行完整主路由；generator projection 会删除资格控制面，其余 reference 按需读取 | 已缓解 |
| 中文触发竞争 | Humanize 接管普通纯文风及报告辅助文风；旧 Skill 已蒸馏并删除 | 已解决，活跃目录唯一 |

## 14. 第四轮极端实践红队

前三轮证明了模型会同义规避，第四轮则不再审模型“写得像不像”，而是直接攻击完成门：构造应该失败的前后文本，观察验证器是否仍给 `PASS/0`；删除或替换快照源文件，观察长文收尾器是否仍允许声称全文完成；逐条回查规则的 provenance、示例和输出合同，观察 reference 是否会诱导模型越权。

### 14.1 短文保护门：修复前确实会误放行

| 攻击输入 | 修复前 | 根因 | 修复后 |
|---|---|---|---|
| `alignat` 环境中把 `y` 改成 `z` | `PASS/0` | scanner 保护了 `alignat`，不变量检查器没有同构环境表 | `FAIL/1`，`PROTECTED_MATH_CHANGED` |
| `exercise` 题干中把“求”改成“计算” | `PASS/0` | 题干只在扫描器中排除，没有进入硬比较 | `FAIL/1`，保护环境变化 |
| Markdown 三反引号开启、四反引号关闭的代码块内改值 | `PASS/0` | 旧正则要求 closing fence 与 opening 完全等长 | `FAIL/1`，按 CommonMark 接受更长 closing fence |
| “样本分为三组”改为“四组” | `PASS/0` | 只抽取阿拉伯数字 | `FAIL/1`，中文数词进入数字不变量 |
| 把 OCR 文本中的 `U+FFFD` 替换字符改为正常字 | `PASS/0` | UTF-8 解码成功就被视为可编辑 | `FAIL/1`，U+FFFD、PUA 和明显 mojibake 进入不可编辑异常标记 |
| “有限元方法”改成“有限差分方法” | `PASS/0` | 工具无法从任意正文自动猜出哪些字符串是正式术语 | 提供 `--term 有限元方法` 后 `FAIL/1`，术语清单数量和 SHA-256 进入 evidence |

这里最重要的改动不是继续追加禁词，而是把 scanner 和 invariant checker 的保护语法做成同构合同。扫描时被标为题干、正式陈述、数学或代码的内容，改写后不能因为换了一个脚本就失去保护。

显式术语表采取保守设计：

- `--term TERM` 可重复使用；
- 比较术语的出现次数与顺序，变化即硬失败；
- evidence 记录去重术语数、清单哈希和状态；
- 未提供术语表时明确写 `NOT_PROVIDED`，不得声称“全部术语已自动核验”；
- 这不取代公式、命令、数字、引语和代码等已有自动保护。

### 14.2 人工豁免不能再靠一句空话

旧实现只数理由里的汉字个数。因此“确认保留”“人工确认”虽然没有说明表达功能，也能把 `REVIEW` 降成 `PASS`；同一个 signal ID 还会一次豁免全文所有同类命中。

当前合同改为：

1. 拒绝“确认保留、人工确认、已经检查”等通用裁决套话；
2. 单一命中可按 signal 裁决，多命中必须使用 `SIGNAL_ID@LINE:COLUMN` 或 finding hash 绑定具体位置；
3. 每个 finding 都带稳定 SHA-256，JSON 输出 `accepted_findings`；
4. 被接受的 warning 也写入独立审计账本；
5. 改后文件 hash 变化后，旧裁决不能被当作新版本证据。

这仍然不是自动判断理由真假。它解决的是“裁决对象不明确”和“空泛四字理由直接放行”，最终语义判断仍属于人工复核。

### 14.3 豁免必须贴着当前命中

原 exclusion 使用整句搜索。输入“闭环控制用于调节，该报告形成完整闭环”时，前半句的正式术语“闭环控制”会把后半句的管理空壳“形成完整闭环”一起豁免。

修复后，排除模式必须与当前 finding 的字符范围重叠。上述句子现在保留后半句候选，统一验证返回 `REVIEW/2`；真实的“闭环控制系统”仍然可以 `KEEP`。这条规则同样适用于“机械抓手/核心抓手”“门禁系统/放行机制”等一词多义场景。

### 14.4 不可读文件继续处理，但不能静默算作已覆盖

用户要求乱码不要拖慢进度，所以行为不是“遇到一个坏文件就停止”，而是：

- scanner 继续扫描其他可读文件；
- JSON 固定输出 requested、scanned、skipped 文件数与跳过原因；
- 存在非法 UTF-8 时整体返回 `REVIEW/2`，不能用 `finding_count=0` 冒充无问题；
- 长文 prepare 对 UTF-16、NUL、异常 C0/C1 控制字符标 `SKIPPED_GARBLED`；
- 被跳过内容保持原字节，不猜字、不补写，并阻断全文完成声明。

### 14.5 规则合同自身也接受红队

| 合同漏洞 | 风险 | 修复 |
|---|---|---|
| 改写范例凭空补出资源、捕食、扰动、状态方程等对象 | 低优先级示例会正常化事实补造 | 删除补造对象，改为只重排输入已经给出的成分 |
| 范例把 `q(x),s(x),\phi(x)` 改成 `q,s,\phi` | 数学对象表面相近但含义可能变化 | 改后保持原函数记号 |
| `STYLE-DIAGNOSE` 与 `DIAGNOSE` 两套枚举并存 | 不同 reference 会给出不同模式名 | 统一为 `DIAGNOSE/REWRITE/DRAFT`，操作合同是唯一 schema 来源 |
| Diagnose 有五字段、七字段和八字段版本 | 输出无法稳定验收 | 固定字段并由合同测试精确断言 |
| 4 处 provenance 指向错误规则号 | 命中后会加载无关章节 | 修正目标并校验具体 section/rule，不再只查字符串在文件某处出现 |
| Voice 模板缺结果报告、观察归属、公式/图表引入等字段 | Profile 保存再加载会丢言语行为 | 补齐字段并增加 round-trip 契约测试 |
| 旧 AIGC Skill 与纯文风 Skill 同时抢“去 AI 味” | 路由不唯一，且旧规则含检测操纵与虚构风险 | 安全报告定位能力并入本 Skill，危险规则拒绝迁移；旧目录删除 |
| `UNRESOLVED` 一处允许全文完成、一处禁止 | 人工可挑宽松条款夸大完成范围 | 统一为任何未决/乱码/快照变化都只能 partial |

### 14.6 长文发布链的七个 P1

长文黑盒复测后来发现一个 P0：finalize 曾信任可篡改的 `units.jsonl` 终态，可在无 rewrites 时伪造全文完成；现已用 `prepare_integrity.json` 修复，并加入篡改、chunk 篡改和清单缺失回归。另有此前记录的七个会破坏完成账本可信度的 P1：

| 漏洞 | 修复前错误行为 | 当前行为 |
|---|---|---|
| 快照后删除源文件或把文件换成目录 | 直接跳过，`source_files_changed_since_snapshot=0`，可 full | 记录 source change，阻断 full |
| `\input{\chapterdir/chapter}` 等宏路径 | 静默漏收 include，仍可 full | manifest 写 `UNRESOLVED_INCLUDE`，prepare/finalize 均 `REVIEW` |
| UTF-16LE 被误按 GB18030 解码 | 含大量 NUL 的文本仍标 READY | UTF-16、NUL、控制字符标 `SKIPPED_GARBLED` |
| 把只读相邻段复制进 owner | 相邻段在最终稿重复两次仍 PASS | 拒绝复制四字符以上的规范化只读上下文 |
| 保留占位符同时再粘贴一份裸标题/题干 | 保护内容次数增加仍 PASS | 规范化 CRLF/LF 后核对保护 span 次数与顺序 |
| 第二批 partial 只提交新单元 | 第一批已接受改写被快照原文覆盖 | rewrites 必须累计；回退尝试 FAIL 并保留旧 partial |
| 非幂等 full 重跑 | 旧正文保留，但 diff/ledger/manifest 被新失败尝试覆盖 | 已发布证据原子保留；失败候选不替换正式证据 |

这些修复带来两个明确兼容性要求。第一，manifest 消费方必须识别 `UNRESOLVED_INCLUDE`；第二，已有 partial 后续提交必须包含此前已接受且仍有效的 rewrites。两者都是有意收紧：宁可拒绝不完整的增量输入，也不能悄悄丢失已验收修改。

### 14.7 红队后的可复核结果

- Humanize、来源候选门、长文、generator projection、资格审计、public-case 采集链、场景路由和退休门：`318/318`；
- 工作区全量：`336/336`（1 项文件 symlink 环境测试因 Windows 权限跳过，根 junction 测试已执行）；
- `humanize-academic-chinese` 通过官方 `quick_validate.py`；
- 13 个脚本均通过 `py_compile` 与 `--help`；
- `physics1.tex` 原 v2 目录重跑仍为 snapshot `cd5fc9b656012aad`、60 units、51 `PENDING`、9 `SKIPPED_PROTECTED`、`REVIEW/2`、`full_completion_claim_allowed=false`、`idempotency=PASS`。

测试通过只证明这些已编码合同，没有证明任意未来文本都能被完整识别。完整前向 evidence manifest 尚未建立，因此生成模型总体资格只能写 `NOT_EVALUATED`，不能写“模型已稳定通过”。

### 14.8 资格自证攻击与 manifest v2

独立审计复现了一个最小假阳性：`MODE-01` 的输出故意不含 DIAGNOSE 九列表格，
`context.json` 还明示存在期望答案，但旧 manifest 只要自填
`assertions[].result=PASS`，harness 就会把该 atom 记为 PASS。问题不在 hash 缺失，而在
“答案与评分都由提交者拥有”。

现行 v2 把评分所有权移到 Skill 内固定 catalog：

- claim 只有 `claim_id/atom_id/oracle_suite_id`，不能自选 check 或提供 result/expected；
- suite 固定完整 required-check 集、fixture hash、期望机器字段和 rubric；
- requirements、contract、catalog、Skill snapshot、run record 和 public artifacts 均进入当前 bindings；
- v1 current case 直接触发 integrity failure，v1 archived case 永远不贡献 PASS；
- 确定性 FAIL 先于证据等级不足和主观 review 聚合，一项 FAIL 加一项缺失仍然是 FAIL；
- caller-declared MODEL/HUMAN review 只保留 `declared_outcome`，固定
  `qualification_eligible=false`，不能替确定性检查放行。

当前 catalog 只完成第一批垂直切片：`MODE-02`、P0 `ROLE-02`、
`PATH-05/positive + review`、`LONG-01` 和自动 `PROTECTED/hash-zero`，共 5 个 suite、
11 个 check、1 个 rubric。所有 suite 明示 `SHADOW`、`runner_compatible=false`。四份
`public_context` 已统一为 `humanize-generation-public-context/v1`，并由 sealer 使用同一参数
逐字节重建；这修复了早期静态 context 与真实 runner context 永远 hash 不相等的问题。

本地 runner 没有把 `--ephemeral` 或 `-s read-only` 当作盲性证明。它记录完整 Skill 中的
oracle catalog 对生成器可见、宿主机排除目录不可达未验证，因此 evidence cap 为 E2。首次
真实采集 `run-001` 因复制快照漏掉 Skill `build/` 而在模型调用前失败；修复并加入回归后，
`run-002` 启动独立 Codex 进程并保存事件流，但 CLI 认证返回 401，最终无 output、无 run
record、无 E3。失败没有被删除或改写成行为样本。

机器复核结果是：无 manifest 时 `integrity=PASS`、`qualification=NOT_EVALUATED`、
163 个 atom 全部未评测；旧自证证明包现在 `integrity=FAIL`、`atoms_pass=0`；合法 v1
归档 fixture 为 `integrity=PASS` 但仍是 163 个 atom 未评测。这个结果比“完成了 5 个 suite”
更重要：当前系统会拒绝不应获得的完成态，但尚未取得完整生成资格。

三份完整机器报告分别见
[no-manifest.json](build/qualification-v2-audit-20260714/no-manifest.json)、
[legacy-false-positive.json](build/qualification-v2-audit-20260714/legacy-false-positive.json) 和
[official-archived.json](build/qualification-v2-audit-20260714/official-archived.json)。本地真实调用的
E2 边界与认证失败见 [runner-receipt.json](build/qualification-local-runner-20260714/run-002/runner-receipt.json)；
原始 events 含服务端错误细节，只作为受限运行痕迹，不在报告中转录。

### 14.9 固定 trust root、generator projection 与 v2 证据四件套

在 manifest v2 与固定 oracle 之后，红队继续攻击 E3 的信任来源，确认旧
`_blind_forward_state` 会直接相信 run record 自报的三个字段：
`oracle_catalog_visible_to_generator=false`、`filesystem_isolation_verified=true` 和
`HARNESS_VERIFIED_GENERATOR_PROJECTION`。当 suite 以后改成 runner-compatible 时，这个入口会让
调用方自己给自己签发 E3。现行实现新增固定
`generation-qualification-trust.json`，其 `production_e3_enabled=false`、accepted receipt schemes
为空；修改 JSON 试图启用 E3 会被代码拒绝，调用方自报隔离成功则进入
`REJECTED_UNTRUSTED_ISOLATION_CLAIM`、integrity `FAIL`，最多保留 E2。

生成器也不再看到完整 Skill。固定 policy 将 62 个旧源项扩展后的当前 Skill 全部分类：25 个
生产能力文件原样保留，`SKILL.md` 只允许删除“验证 Skill”“生成资格审计”两条路由和整个资格
采集章节，最终投影恰为 26 个文件。oracle、requirements、trust policy、qualification fixtures、
auditor、runner、sealer、builder、build 和 cache 全部排除。policy 不只批准路径，还批准 capability
source hash；生产文件即使只增加一句无控制词正文，也必须显式更新批准 hash，不能借白名单路径
偷渡 expected/rubric 内容。

builder 对未知文件、UTF-8、frontmatter、fenced heading、相邻 H2、引用闭包、隐藏 suite/check/rubric
ID、大小写/NFC 冲突、symlink/reparse/hardlink、额外空目录和源文件 TOCTOU 逐项 fail-closed。
manifest 写在投影外，发布失败会回滚已发布投影。同一 source/policy/builder 重建得到相同 tree；
本轮正式产物为 26 文件，tree
`f6d783c0e48533a2704d8ad2286de735b10d6cf29baabc343a3bca368a329dc0`。

runner 不再相信 builder 的返回字典，而是 strict parse canonical manifest 并逐字段对齐；启动前和
退出后都按 lstat、路径、字节、hardlink identity 与 tree hash 复核投影，同时复核生成器实际读取的
`execution/case`。运行中改 staged input 或投影时，只留下明确
`runner_status=INFRA_INVALID`、`projection_audit_status=FAIL` 的 receipt，不生成 run record 或 seal。
公开 prompt 也删除了“去找 tests/gold/oracle”的反向提示，case ID、文件名、正文、prompt 和 locked
literal 中的隐藏控制 ID 会在 invoke 前拒绝。

current case 的 run record 升为 `humanize-generation-run-record/v2`。它必须提交 canonical
projection manifest、runner receipt、run record、run seal、public prompt/context；auditor 会从当前
完整 Skill 独立重建投影，再交叉核对四类 artifact、staged-case hash、public seal 和嵌套 provenance。
删除任一证据、伪造 projection tree、让 receipt 与 record 冲突或混写隔离字段，均为 integrity
`FAIL`、`atoms_pass=0`。`request/context.json` 明确是 capture context，不冒充生成器上下文；CLI
无法捕获 system/developer messages，因此 `generator_context.complete=false`。

这些改动没有把本地执行升级成 E3。投影只能证明
`oracle_catalog_present_in_projection=false`；本机仍继承用户 profile，宿主 oracle、工作区和完整
Skill 不可达未获外部证明，状态仍是
`oracle_catalog_unreachable_to_generator=UNVERIFIED`、`filesystem_isolation_verified=false`、
`evidence_cap=E2`。最新无 manifest 机器审计见
[no-manifest.json](build/qualification-v3-audit-20260714/no-manifest.json)：
`integrity=PASS`、`qualification=NOT_EVALUATED`、163 个 atom 全部未评测、
`production_e3_enabled=false`。

### 14.10 第七至第九轮：验证器绿不等于正文自然

2026-07-14 又用同一组三个最小输入做了三轮 fresh-context 前向测试。每个代理只拿正式 Skill、指定输入和普通用户式配置，不提供预期答案，不允许读取测试、旧输出、报告或资格材料。输入固定为：

- `COURSE`：含“值得注意的是、必须牢记、具有重要意义、为后续学习奠定基础”和一个必须逐字保护的 `equation`；
- `MODELING`：含编辑后台语言、四个数学跨度、七组数字/单位、误差—耗时代价、多重缓和、闭环拔高和自动展望；
- `RESEARCH`：含三个观察、范围限制、不能区分的两类原因，以及“系统梳理—深入探讨—奠定基础”链。

第一轮 v7 的机器结果全部是 `PASS/0`，但独立评估代理连续阅读立即推翻其中两项：

| 场景 | v7 机器状态 | 人工发现 | 有效判定 |
|---|---|---|---|
| COURSE | `PASS/0` | `必须牢记` 被换成 `公式必须记清楚`，仍是说教同义壳 | 阻断 |
| MODELING | `PASS/0` | 编辑要求变成“表格列出”；抽象支撑变成“用于工程决策”；多重缓和变成“影响程度或许有限”；去掉“后续工作”标签后仍留空展望 | 阻断 |
| RESEARCH | `PASS/0` | 限定保持良好，但“本文据此梳理相关现象，讨论可能原因”没有正文兑现 | 可修改后通过 |

盲评原文和实践红队分别保存在 [blind-quality-review.md](build/maturity-v7-forward-20260714/blind-quality-review.md) 与 [practical-redteam.md](build/maturity-v7-forward-20260714/practical-redteam.md)。这轮证明原先的“数字、公式、词项和模态计数都绿”仍看不到跨版本命题升级。

本轮据此增加的不是一批抽象口号，而是四组可失败抓手：

1. **谓词来源门**：每个改后独立分句只能登记为 `COPY`、`ENTAILED_PARAPHRASE` 或 `DELETE_STYLE_SHELL`；显式拒绝 `NEW_PREDICATE`、`SPEECH_ACT_UPGRADE` 和 `MODALITY_TO_DEGREE`。
2. **跨版本确定性 warning**：统一验证器现在识别 `SPEECH_ACT_DIRECTIVE_TO_COMPLETION`、`SPEECH_ACT_SUPPORT_TO_ACTUAL_USE` 和 `SPEECH_ACT_MODALITY_TO_DEGREE`。v7 建模稿重新验证后同时命中三项，并保持 `REVIEW/2`。
3. **同义逃逸与去标签展望**：`需要记住/需要记清楚/要记住` 归入课程说教簇；`应用场景可以进一步拓展` 即使没有“未来/后续工作”也归入 high 自动展望；`数据仍需在正文中保留` 继续算编辑后台语言。
4. **语料动作锚进入普通改写**：`COURSE`、`MODELING`、`RESEARCH` 场景文件直接暴露由既有 MD/TeX 人工复读蒸馏的动作卡。每个可编辑单元最多选两张，缺少输入锚点时写 `NONE_APPLICABLE`，不能为使用语料而迁移来源事实或句子。

第二轮 v8 显示生成行为开始改变，但仍未成熟：

- 建模稿不再虚构工程决策、不再把多重缓和写成“影响有限”、不再保留空展望；但仍写“数据仍需在正文中保留”，属于诚实但不够可用的 `REVIEW`；
- 科研稿删除了未兑现作者动作，并诚实停在删除“可能”后的模态 `REVIEW`；
- 课程稿把“必须牢记”换成“公式需要记住”，暴露第二个同义逃逸。

v8 还暴露了评审可靠性问题。一个盲评代理把“公式需要记住”判为自然，甚至建议换成“应记住”；主代理没有采用这一结论，而是把整组“必须/务必/需要/要 + 牢记/记住/记清楚”纳入同一功能簇。这说明单个模型盲评不能作为 E4，也不能替代多评审分歧记录。

第三轮 v9 的行为进一步收敛：

| 场景 | v9 正文行为 | 统一状态 | 实际意义 |
|---|---|---|---|
| COURSE | 直接删除空泛记忆命令，保留公式、条件与纠偏链；使用 `COURSE-ERROR-01` | `REVIEW/2` | 文风正文明显改善；删除 `必须` 触发模态复核，未用同义词骗绿 |
| MODELING | 删除拔高、闭环和展望，保留数值取舍；对编辑要求明确登记 `UNRESOLVED`，`corpus_action=NONE_APPLICABLE` | `REVIEW/2` | 没有事实升级，但正文仍残留编辑备注，不能称可直接交付 |
| RESEARCH | 删除未兑现作者动作，把原有“可能”收回“可能原因”范围句；使用 `RESEARCH-SCOPE-01` | `PASS/0` | 三层验证均通过，未恢复套话或补造机制 |

v9 产物见 `build/maturity-v9-forward-20260714/`。课程输入本身含“速度随时间减小即可直接套用匀变速公式”的内容问题；纯文风 Skill 按合同没有暗中修正，并保持 `academic_correctness=NOT_EVALUATED`。这不是文风通过能覆盖的教学正确性结论。

对建模过度保守的后续修复允许从编辑指令中回收**同层字面载荷**：例如“正文里要保留三组数据，温度分别为 20 ℃、25 ℃ 和 30 ℃”可写成“三组数据的温度分别为……”，但不能声称表格已列出、实验已采用或数据已用于模型输入。

这项规则的前两次独立 v10 尝试分别遇到模型容量错误和运行挂起；第三次 `v10c` 取得了新鲜样本：

```text
我们构建温度响应模型 R(T)=aT+b。数据温度为 20 ℃、25 ℃ 和 30 ℃，共三组。
参数 a 在 [0.8,1.2] 内进行扫描。结果表明，当 a=1.06 时，验证集误差由 8.1% 降至
5.4%，但计算时间由 31 s 增至 44 s。

模型可能仍会受到传感器漂移影响。
```

这里没有编辑备注、表格完成事实、工程决策、影响程度结论或自动展望。代理选择 `MODELING-PROCESS-OUTCOME-SEPARATION-01`，把误差下降与计算时间上升保留为反向取舍。第一稿曾把“三组”移到温度数值前，统一验证器以 `NUMBER_OR_UNIT_CHANGED/FAIL/1` 拦截；调整回原数字顺序后，硬不变量和文风信号通过。最终仍因删除 `可以/或许` 并压缩多重缓和而保持 `SPEECH_ACT_MODALITY_SCOPE_CHANGED/REVIEW/2`，没有为变绿恢复套话。产物见 `build/maturity-v10c-forward-20260714/modeling/`。

本轮可复核机器状态更新为：

- 工作区共运行 355 项：354 项通过，1 项 Windows 文件 symlink 权限测试跳过；
- 13 个 Skill Python 脚本全部通过 `py_compile` 与 `--help`；
- `quick_validate.py` 在 `PYTHONUTF8=1` 下返回 `Skill is valid!`；
- 来源 profile 为 50 张 action card 可用、0 不可用、23 个来源可读，`source_text_exported=false`；
- 新 generator projection 为 26 文件，tree `f1c619cfedb2244f05d12679bdc2ed7535b929dc8d3b601fe7888a811ce16f5e`，证据上限仍为 E2；
- 无 manifest 审计为 `integrity=PASS`、`qualification=NOT_EVALUATED`、`atoms_pass=0/163`、`production_e3_enabled=false`。

机器产物见 [maturity-v10-action-profile-20260714.json](build/maturity-v10-action-profile-20260714.json)、[generator projection manifest](build/generator-projection-maturity-v10-20260714-manifest.json) 和 [no-manifest qualification audit](build/qualification-maturity-v10-20260714-no-manifest.json)。因此当前更准确的成熟度表述是：**拒绝虚假完成和常见跨命题升级的工具链继续成熟，三场景最小前向行为已明显改善，建模字面载荷已有新鲜盲写证据；完整 163-atom 生成资格仍未评测。**

### 14.11 第九轮：接通 DRAFT、校正 DIAGNOSE/GENERAL，并拆开长文“覆盖完成”与“Humanize 完成”

本轮没有继续堆禁词，而是先对 `DRAFT / DIAGNOSE / GENERAL / Voice Profile / 长文 / 资格 catalog`
做三路隔离审计。审计代理只读正式生产文件，不读 tests、旧 build、历史报告和 oracle；完整报告见：

- [modes-audit.md](build/maturity-v11-audit-20260714/modes-audit.md)；
- [long-voice-audit.md](build/maturity-v11-audit-20260714/long-voice-audit.md)；
- [qualification-audit.md](build/maturity-v11-audit-20260714/qualification-audit.md)。

模式审计给出 3 个 P0、6 个 P1。最关键的不是“DRAFT 写得是否顺”，而是此前 DRAFT 没有进入
frontmatter 的自然触发面，也没有 supplied content 到草稿的独立验证语义，却允许运行记录直接写
“未补造”。DIAGNOSE 的 `Dominant/Recurring/Local` 还可能被 scanner 的 `high/medium/low` 错当
同一轴；扫描命令默认隐藏 protected/excluded finding，却又要求诊断表披露来源角色。GENERAL
则只有负向边界，没有正向语料卡，并且原 guard 把任意三个“必须”视作动员腔，会误伤三个不同
法定义务主体。

长文/Voice 审计给出 5 个 P0、7 个 P1。当前 prepare/finalize 确实能证明快照、保护区、逐单元
验证、格式门和源文件不覆盖，但不能证明：

- 作者 Profile 被建立并以 id/version/hash 绑定到 unit、chunk、rewrite bundle 和 final metadata；
- `AUTO` 已逐单元落成 `COURSE/MODELING/RESEARCH/GENERAL`，而不是把字符串 `AUTO` 原样传下去；
- 各块没有共同生成新的修复口头禅；
- `NO_CHANGE` 来自完整阅读而不是批量四字理由；
- 把 clean 输出交给 fresh agent 再跑一遍已经收敛，而不是同一 rewrite bundle 组装出相同字节。

因此，原来的 `full_completion_claim_allowed=true` 语义过宽：逐块保护 PASS 可能掩盖全文已经被
场景默认声线压成统一“克制腔”。本轮先做诚实完成态拆分，暂不伪造尚不存在的 Profile builder
或全文声线算法：

| 字段 | 当前可证明内容 | 当前状态规则 |
|---|---|---|
| `coverage_completion_claim_allowed` | 快照、覆盖、局部保护、格式/编译门闭合 | 现有 finalize 可真实计算 |
| `assembly_replay_idempotency` | 同一 rewrite bundle 再组装的派生字节相同 | 兼容旧 `idempotency`，不得称二次 Humanize |
| `scene_routing_status` | unit 已有非 AUTO 场景标签 | `AUTO` 保持 `NOT_EVALUATED` |
| `voice_binding_status` | hash-bound Profile 已进入正式工件链 | 当前固定 `NOT_EVALUATED` |
| `voice_conformance_status` | 全文符合所绑定 Profile | 当前固定 `NOT_EVALUATED` |
| `cross_unit_repetition_status` | 已运行跨 unit 新增模板门 | 当前固定 `NOT_EVALUATED` |
| `humanize_second_pass_convergence` | clean 输出作为新输入由 fresh pass 重跑后为空 patch | 当前固定 `NOT_RUN` |
| `humanize_completion_claim_allowed` | 上述 Humanize 级门全部通过 | 当前固定 false |
| `full_completion_claim_allowed` | 兼容别名 | 与 `humanize_completion_claim_allowed` 相同，当前 false |

这意味着现阶段即使 finalize 的局部执行 `status=PASS`，也只能声明覆盖与局部保护闭合，不能声明
“全文 Humanize 已完成”。这是有意拒绝旧假完成态，不是把可用的结构工具判成失败。

#### DRAFT 的真实接通与三轮前向轨迹

正式入口已经补入“按要点、事实表、研究记录或课程材料起草”的自然语言触发；
`agents/openai.yaml` 也同步声明 supplied-content 起草，缺口省略或占位。统一验证器新增
`--mode DRAFT`，第一个 artifact 解释为供应材料而非“改前稿”。它不再要求所有供应材料必须
原样保留，而是检查草稿新增的可机械载荷：

- 数字与单位；
- 数学跨度；
- 代码与正式环境；
- 关键 TeX 命令、引用、标签和 URL；
- 直接引语；
- 乱码跨度；
- 归因/文献来源标记；
- 调用方显式保护术语。

未供应载荷为硬 `FAIL/1`；表面子集通过写 `draft_surface_source_check=PASS`。但该门不伪装成
完整中文蕴含证明：只要不是 supplied artifact 的逐字 copy，
`semantic_source_check=NOT_EVALUATED`，最终状态至少为 `REVIEW/2`。因此运行记录只能说
“未发现已编码的表面新增载荷，语义来源待复核”，不能再说“未补造已验证”。

研究 DRAFT 输入直接取自此前登记的 `main.tex` 事实与口径：1.800/1.805/0.26%、
2.200/1.838/16.47%、0.204、4.213，以及“硬锚点校准—局地一致性检验—非独立外部验证”
的角色边界。三轮输出的关键变化如下：

1. v11 首稿事实和全部载荷均正确，但开头写“需要区分报告”，仍像编辑要求；旧 REWRITE
   validator 还把供应材料中的“不提供……”省略误报成否定删除。红队逐句回指判正文事实 PASS，
   但运行记录的机器执行声明没有独立 artifact 证据。
2. v11b 自然任务没有写 Skill 名，fresh agent 仍自动进入 `DRAFT/RESEARCH`，表面门 PASS、
   语义门 `NOT_EVALUATED/REVIEW/2`；但正文把编辑后台移动成“需要分开报告”，说明只接通模式
   不等于已经去掉 meta-writing。
3. 正式 Skill 随后把 supplied unit 分成 `FACT_PAYLOAD / EDITORIAL_REQUIREMENT /
   FACT_BOUNDARY`：编辑要求只决定组织，字面事实可回收，动作句不进入正文。v11c fresh 输出直接
   用三个段落分别呈现总量校准、局地检验和恢复/承压，没有“本节需要、正文应、需要分开报告”。
   精确复验为：`draft_surface_source_check=PASS`、三层保护均 PASS、
   `semantic_source_check=NOT_EVALUATED`、最终 `REVIEW/2`。

产物分别见 `build/maturity-v11-forward-20260714/`、
`build/maturity-v11b-forward-20260714/` 和
`build/maturity-v11c-forward-20260714/`。这条轨迹保留了失败稿，没有只展示最终好看版本。

#### DIAGNOSE 与 GENERAL 的实测修复

自然建模原则段的 v11 诊断没有把“三条原则、标题层级、两次如果—那么”强判成模板，而是分别
给出 KEEP/NO_CHANGE；但它为每个自然段都造一行“非病灶”，且只自述连续阅读，没有 protected
审计证据。正式合同随后将两套 severity 分离，并规定 3—8 是“病灶类型”上限，不是 3—8 个
抽样位置；每类在 `Location/Trigger` 中给作者 occurrence 数与位置，DIAGNOSE 扫描固定使用
`--include-protected --include-excluded`。

v11b 引语盲测中，fresh agent 实际扫描 4 个 finding：作者正文 1 个、quoted/protected 3 个、
excluded 0 个。表中只把引语外一次“值得注意的是”列为 `Local`；引语内 3 个词项命中全部写
`KEEP/protected`，没有进入作者复用数，也没有把 scanner high 错报为 Dominant。运行记录保存了
两条真实扫描命令与计数，并明确统一改写验证器 `NOT_RUN`。

GENERAL 法学 DRAFT 使用三个供应事实：行政机关、平台经营者、数据处理者分别“必须”履行不同
义务。旧 guard 会因“必须×3”命中 mobilizing command；新 guard 只有出现受众主体与
“牢记/掌握/积极行动”等命令语境时才成立。fresh 输出保留三个主体与恰好三个“必须”，
不补法条、立法目的、例外、效果或价值评价；GENERAL 按合同写
`corpus_action_support=NONE`，不伪造动作卡，最终同样因语义来源未评估保持 `REVIEW/2`。

#### 百分号保护区误判：人工读真实输出发现的跨路径漏洞

v11b DRAFT 仍含“需要分开报告”，但新词项扫描最初返回 0 finding。向下检查不是词库失效，而是
Markdown 行内的 `16.47%` 被 `ProtectedIndex` 当成 TeX 注释起点，同一行余下文本全部被静默
保护。这个漏洞会同时让三条路径漏检：

1. 短文词项扫描；
2. 候选门的来源复制和 negative guard 作者视图；
3. 长文 prepare 的 protected span 与 chunk。

修复后，保护语法显式接收 `document_format`：只有 `.tex/.ltx` 把未转义 `%` 解释为注释，
Markdown 的百分比保留为作者正文。真实 v11b 输出现在能稳定报：

```text
LEX-META-01/high/DELETE 需要分开报告
```

并新增 scanner 与 long-prepare 两条回归，证明 `16.47%` 后面的正文既能进入 chunk，也能被词项
门发现。projection builder 还因 Windows 默认 GBK 调用官方 quick validator 失败，现已固定用
`python -X utf8` 启动；这同样来自真实构建失败，不是预设规则。

#### 本轮机器状态与资格边界

- 全量自动化：362 项，361 通过，1 项 Windows 文件 symlink 权限测试跳过；
- 13 个脚本全部通过 `py_compile` 与 `--help`；
- 官方 `quick_validate.py` 返回 `Skill is valid!`；
- 来源动作 profile：50 张可用、0 不可用，GENERAL 仍为 `CORPUS_INSUFFICIENT`；
- 26 文件 generator projection tree：
  `24e2e7adad152e88329bcc12928470e01d896546d6d6a3274062e056f04fc7f4`；
- no-manifest 资格审计：`integrity=PASS`、`qualification=NOT_EVALUATED`、
  `atoms_pass=0/163`、`atoms_not_evaluated=163/163`、本地 evidence cap=E2、
  `production_e3_enabled=false`；
- 固定 oracle catalog 仍只有 5 个 SHADOW suite。本轮资格审计虽已给出下一批 11 个纵向 suite
  的精确设计，但没有把“设计完成”写成“资格覆盖已实现”。

机器产物见 [maturity-v11-action-profile-20260714.json](build/maturity-v11-action-profile-20260714.json)、
[generator projection manifest](build/generator-projection-maturity-v11c-20260714-manifest.json) 和
[no-manifest qualification audit](build/qualification-maturity-v11c-20260714-no-manifest.json)。

本轮准确结论是：DRAFT 已从“合同里写着能起草”推进为自然可触发、表面载荷可拦截、语义来源
不会虚假 PASS 的生产入口；DIAGNOSE 和 GENERAL 的两个实测误区已修；长文完成声明已诚实降格。
但 hash-bound Voice Profile、逐 unit AUTO 路由、全文声线/跨块重复门、可信 NO_CHANGE evidence、
fresh second pass 与 append-only 局部回退仍未实现，不能称完整成熟。

## 15. 仍然存在的边界

以下事项没有被包装成“已完全解决”：

1. 扫描器是可审计规则系统，不是完整中文分词器或作者身份检测器；新语料仍可能出现未登记同义变体。
2. TeX 长文解析器是保守结构解析，不是完整 TeX AST。无法静态展开的宏 include 或嵌套会标 `UNRESOLVED_INCLUDE/UNRESOLVED`。
3. 长文工具不自动写正文；它控制模型/人工改写的输入、保护、验收和发布。
4. 编译门依赖项目现有命令；未提供时准确记录 `NOT_RUN`，不会伪装通过。
5. 盲测证明模型仍会同义规避。任何没有验证记录的直接生成都不能视为生产交付。
6. 本地 warning proposal 只是处理建议，不能证明真人身份或清除 `REVIEW`；finding 级 KEEP 仍需针对具体位置说明表达功能。
7. 术语保护只对显式 `--term` 清单给出硬证据；未提供时状态为 `NOT_PROVIDED`。
8. 固定 oracle catalog 目前只覆盖 5/163 个垂直 atom，且全部处于 SHADOW；它不是完整评测矩阵。
9. 本机没有 Docker、可用 WSL 发行版或 Windows Sandbox 隔离执行器；28 文件投影虽不含 oracle，但宿主排除根不可达仍未验证，本地 runner 只能到 E2。
10. 独立 Codex CLI 最近一次真实采集认证返回 401，尚未产出一条符合 v2 四件套的新模型 output；修复外部认证后也必须新建 run，不能补写旧 receipt。
11. 生成模型完整评测矩阵尚未运行，当前总体前向资格为 `NOT_EVALUATED`，不能自动发布盲写结果。
12. 本工具不承诺任何 AIGC 检测结果。
13. Voice Profile 已进入可重建生产链，但 hash 绑定仍只证明工件身份；全文声线符合性、跨块修复语重复与 fresh second pass 尚未实现。
14. 长文 `scene=AUTO` 仍未逐 unit 解析；当前诚实写 `scene_routing_status=NOT_EVALUATED`，不能把 AUTO 字符串当路由完成。
15. `NO_CHANGE` 当前仍不能证明主观“完整阅读”；四字理由虽有局部门，缺少位置化 voice evidence 与跨 unit 理由复用门。
16. `assembly_replay_idempotency` 不等于 fresh second-pass 收敛；后者未运行时固定 `NOT_RUN`。

## 16. 常用命令

短文扫描：

```powershell
python scripts/scan_humanize_chinese.py input.tex --scene AUTO --format text
```

单独硬保护检查：

```powershell
python scripts/check_humanize_invariants.py before.tex after.tex --json
```

统一交付验证：

```powershell
python scripts/validate_humanize_output.py before.tex after.tex `
  --mode REWRITE `
  --scene COURSE `
  --format json
```

supplied-content DRAFT 表面来源验证：

```powershell
python scripts/validate_humanize_output.py supplied.md draft.md `
  --mode DRAFT `
  --scene RESEARCH `
  --format json
```

该命令即使表面来源门通过，也会在自然语言蕴含未获得可信逐分句 review 时返回
`semantic_source_check=NOT_EVALUATED` 与 `REVIEW/2`；不要把它手改成 PASS。

带本地处理 proposal（仍返回 `REVIEW/2`）：

```powershell
python scripts/validate_humanize_output.py before.tex after.tex `
  --scene RESEARCH `
  --term "有限元方法" `
  --keep-reason "LEX-RESULT-01@12:4=此处承担有数据对象的结果报告" `
  --propose-warning-resolution "<warning_fingerprint>=建议核对是否只合并重复缓和" `
  --warning-review-request-sha256 "<request_sha256>" `
  --warning-reviewer-kind HUMAN `
  --warning-reviewer-id "<调用方标签>"
```

长文准备与收尾：

```powershell
python scripts/prepare_humanize_long_document.py main.tex --output <run-dir> --scene AUTO
python scripts/finalize_humanize_long_document.py --run-dir <run-dir> --rewrites <rewrites-dir>
```

生成资格 public case 与本地 E2 采集：

```powershell
python scripts/seal_humanize_public_fixture.py input.md request.txt `
  --output <new-public-case> --case-id <id> `
  --mode REWRITE --scene RESEARCH --intensity BALANCED `
  --output-format CLEAN --scope selection

python scripts/run_humanize_generation_trial.py <new-public-case> `
  --output <new-run-dir> --format json

python scripts/audit_humanize_generation_qualification.py <manifest-v2.json> `
  --artifact-root <evidence-root> --format json
```

本地 runner 成功也只表示 `CAPTURED_E2`；没有外部隔离 receipt 时不要把命令输出改写为 E3。

## 17. 最终定位

这个 Skill 不是“把所有论文改成一种克制模板”，也不是“列一串 AI 禁词”。它把 Humanize 拆成四个可观察动作：

1. 找到真实模板信号；
2. 保护不可改对象和言语行为；
3. 在授权范围内改变节奏、句壳和段落职责；
4. 用文件 hash、候选差异、diff 和覆盖账本证明完成范围。

最重要的工程结论是：

> 规则负责提出候选，模型或编辑者负责改写，验证器负责拒绝无证据的“已完成”。

## 18. v12：Voice Profile 从说明文档变成可重建工件

### 18.1 为什么还要继续改

v11c 已经能诚实区分 `coverage_completion_claim_allowed` 与全文 Humanize 完成，但 `voice_binding_status` 仍固定为 `NOT_EVALUATED`。这留下了一个很具体的工程空洞：长文 chunk 虽然写了 `scene`，却没有冻结“本次到底使用哪一个 Voice Profile”；生成端也不用回显 Profile 版本。只要 Profile 在 prepare 与 finalize 之间发生变化，或者旧 bundle 被搬到新 run，原流程无法定位错配。

第一轮只读审计又把问题拆成三层：

1. Profile 自身必须有稳定 schema 与自哈希；
2. prepare 必须把同一身份写入 metadata、unit、chunk、ledger 和完整性封条；
3. rewrite bundle 必须回显当前 hash，finalize 必须在正文验证前拒绝缺失、非法和错配值。

这里不能把“hash 一样”写成“声线符合”。hash 只能证明版本身份，不能证明模型真正遵循了句长、标点、第一人称或收尾习惯。因此 v12 只把 `voice_binding_status` 从固定未评估升级成真实的 `PASS/REVIEW`；`voice_conformance_status` 仍保持 `NOT_EVALUATED`。

### 18.2 新增的生产入口

新增两个正式脚本：

- `build_humanize_voice_profile.py`：从 sample spec 构建 manifest 与 Profile；
- `validate_humanize_voice_profile.py`：独立检查 schema、自哈希、manifest 绑定，并可从原样本重建证据。

builder 固定输出：

- `humanize-voice-sample-manifest/v2`，其中 canonical sample-spec hash 与样本来源声明一起进入自哈希；
- `humanize-voice-profile/v1`；
- canonical UTF-8 JSON；
- 64 位小写 SHA-256 自哈希；
- 不含整段样本原文的 feature evidence；
- 不含作者身份、能力或内容正确性推断的 claims。

validator 现在有两种层级：

- 只给 Profile：校验 strict JSON、schema、字段集合和自哈希，但 PERSONAL 顶层生产准入保持 `REVIEW/2`；
- 同时给 manifest、sample spec、allowed root 与 `--rebuild-evidence`：重新读取源字节、重建角色图、保护区、去重簇、计数、feature 和 Profile，要求结果逐字段相同。

后者堵住了“伪造一份内部自洽的 PERSONAL/PASS JSON，再自己重算 hash”的漏洞。PERSONAL Profile 进入 prepare 时必须经过当场重建，metadata 固定写 `voice_evidence_status=REBUILT_PASS`；只有自哈希、没有 manifest/spec 的 PERSONAL 工件直接失败。

真实 builder 消费测试又发现 DEFAULT 不能只分成“有/无”两类：不足 300 字或全部来源被排除时，builder 会生成带真实 manifest hash 的证据绑定 DEFAULT。它不是代码注册表里的零样本 DEFAULT，不能丢弃 manifest，也不能被后者的精确对象比较误拒。修复后，证据绑定 DEFAULT 同样要求 manifest/spec/root 当场重建，状态为 `REBUILT_DEFAULT_PASS`；只有确定性零样本 DEFAULT 使用 `DETERMINISTIC_DEFAULT`。

### 18.3 样本角色与隐私边界

sample spec 的路径只能相对 `--allowed-root`。每个样本必须声明：

- `sample_id`；
- `locator`；
- `origin`；
- `scene`；
- 是否为完整文本单元；
- 默认角色；
- UTF-8 字节半开区间形式的例外角色范围。

允许角色只有 `author/quoted/exam-original/ocr/code/math/template/unknown`。builder 即使收到 `default_role=author`，仍会自动剔除确定的 Markdown/TeX 代码、数学、块引语、直接引语和模板结构。角色范围越界、重叠或落在 UTF-8 字符中间时失败；乱码、NUL 或明显 OCR/mojibake 样本进入排除审计，不猜字。

来源只允许以下四类：

- `USER_CONFIRMED_AUTHOR`；
- `USER_CONFIRMED_ADOPTED`；
- `UNKNOWN`；
- `MODEL_GENERATED`。

后两类永远不能贡献作者字数或 feature。用户已经明确 CET6 两个 TeX 与微信 `main.tex` 由 GPT 生成，因此本轮真实语料验证把它们全部标为 `MODEL_GENERATED`，而不是因为文本长就偷换成作者 Voice 样本。

### 18.4 去重与置信门

Profile 字数按去保护、去重后的代表段落统计。重复攻击分两层拦截：

1. NFC 后保留字母数字的规范视图 exact hash；
2. 对不少于 40 个规范字符的段落做字符 5-gram，相似度达到 Jaccard 0.90 或 containment 0.95 时建立边，再按全部边的连通分量形成顺序无关近重复簇。

去重视图只裁决“是否独立”，不用于风格测量；句号、分号、括号和段落结构不会先被压平再拿来推断节奏。

置信门固定为：

| 去重作者汉字 | 完整单元 | 结果 |
|---:|---:|---|
| `<300` | 任意 | `DEFAULT` |
| `300–999` | 任意 | `LOW` |
| `1000–4999` | 任意 | `MEDIUM` |
| `>=5000` | `<3` | 最高 `MEDIUM` |
| `>=5000` | `>=3` | `HIGH` |

测试实际覆盖 299、300、999、1000、4999、5000 六个边界。另有一项把 200 字段落复制 30 次，原始字数达到 6000；去重后仍为 200，只能得到 DEFAULT，不能用复制凑出 HIGH。

### 18.5 feature 为什么没有写成自由文本

Profile 只开放可机械重建的 feature registry，例如：

- 主语位置；
- 条件先行；
- 显式连接；
- 段末标点；
- 括注；
- 分号分组；
- 非列表正文。

每个 feature 都保存 opportunity、support、counterexample、去重 unit 数、位置 hash 和 feature-level confidence。模板壳与跨段重复开头只进入 `DO_NOT_AMPLIFY` 负控。解释峰值、论证主次、判断力度等需要连续阅读的语义结论不会被一个正则直接发布成 PASS feature；这类内容仍留给逐文档阅读和独立前向审阅。

### 18.6 四个 DEFAULT 不是一个空字符串

COURSE、MODELING、RESEARCH、GENERAL 各有独立、版本化、hash 不同的场景 DEFAULT。它们共同满足：

- `profile_kind=DEFAULT`；
- `confidence=DEFAULT`；
- `features=[]`；
- `disclosure_required=true`；
- `personal_voice_claim_allowed=false`。

DEFAULT 的 `PASS` 只表示安全回退工件结构有效。它绝不表示“已经恢复作者个人文风”。长文 prepare 未收到 Profile 时会把对应 DEFAULT 物化为 `voice_profile.json`，而不是写一个无法校验的 `NONE`。

### 18.7 prepare/finalize 的精确绑定

prepare 现在把以下字段写入每个 unit、chunk 和 ledger：

- `voice_profile_id`；
- `voice_profile_revision`；
- `voice_profile_confidence`；
- `voice_profile_kind`；
- `voice_profile_source`；
- `voice_profile_binding_scene`；
- `voice_profile_sha256`；
- `voice_default_disclosure`。

同一绑定还出现在 `run_metadata.json`。Profile 本体进入 `prepare_integrity.json`；PERSONAL 的 manifest 与 sample spec 也一并冻结。finalize 除了检查完整性封条，还重新验证 Profile 自哈希、确定性 DEFAULT、Profile/manifest 绑定和 unit/chunk 字段一致性。

每个 `REWRITE` 与 `NO_CHANGE` JSON bundle 必须同时回显 `unit_id`、`chunk_binding_sha256` 与 `voice_profile_sha256`。文件名只是查找入口，不能替代 bundle 内部身份。拒绝原因分开记录：

| 情况 | unit 结果 |
|---|---|
| 缺字段 | `UNRESOLVED / voice_profile_hash_missing` |
| 不是 64 位小写十六进制 | `UNRESOLVED / voice_profile_hash_invalid` |
| 合法但不等于冻结值 | `UNRESOLVED / voice_profile_hash_mismatch` |
| 精确匹配 | 才进入 warning、保护区和正文验证 |

unit 与 chunk 另有 `bundle_unit_id_missing/invalid/mismatch` 和
`chunk_binding_hash_missing/invalid/mismatch`。三个值全部一致只证明 bundle 指向当前冻结块，
不证明正文符合 Voice Profile。

旧 `.txt` bundle 不能承载该字段，因此无法在 Profile-bound run 中通过。Profile 文件在 prepare 后被改动时，完整性门硬拒绝；`--check-command` 若在检查期间污染 Profile 或其他 run 工件，也由既有 run-state hash 门拦截。

### 18.8 真实 MD/TeX 语料验证

本轮没有拿合成短句替代真实材料。真实样本分成两种用途：

第一种是 Profile 负向准入：

- `D:\code LateX\elegantbook\cet6\CET6.source-damaged.backup.tex`；
- `D:\code LateX\elegantbook\cet6\test.tex`；
- 微信文件目录中的 `main.tex`。

三者按用户确认标为 `MODEL_GENERATED`。两次 builder/validator 重建都得到 `readable_author_chars=0`、`profile_kind=DEFAULT`、`confidence=DEFAULT`、`evidence_rebuilt=true`。这证明长文本不会因为字数多而绕过来源角色门。

第二种是 fresh 前向目标：

- COURSE：从 `test.tex` 的 10 个可编辑 unit 中只处理 `U-b24ef5a3242e`，34 个保护跨度全部通过；该 unit 为 `DONE`，其余 9 个仍为 `PENDING`，总体 `REVIEW/2`；
- RESEARCH：从微信 `main.tex` 的 28 个可编辑 unit 中只处理 `U-b1bcaa2c520d`，该 unit 为 `DONE`，其余 27 个仍为 `PENDING`，总体 `REVIEW/2`。

两个 fresh agent 都只看到正式 Skill、原始任务和输入路径，没有看到预期改法或本轮诊断。两次 rewrite bundle 都正确回显 Profile hash，逐单元保护与正文验证为 PASS，源文件 hash 未改变。局部完成没有被包装成全文完成。

前向 diff 也能看到材料驱动的具体动作。COURSE 单元删掉了“精准地勾勒”“紧拥新兴时代红利”等模板/错搭壳，把用途说明改为更直接的题型条件；RESEARCH 单元把参数口径、情景结果、物种差异与表格范围重新分层，同时保留全部数值、公式和“非独立外部验证”的限制。这里仍不能据两个样本宣称总体生成质量成熟，但至少证明新 hash 合同没有阻断真实 TeX 改写。

第二轮红队修复全部落盘后，又新开了一个不继承上下文的 RESEARCH agent，只给正式 Skill、微信 `main.tex` 和“处理一个完整单元”的普通任务。它选择 `U-4bd3af2f0994`（问题重述，第 20–26 行），单元正文与保护验证为 PASS；36 个总单元中 `DONE=1`、`PENDING=27`、`SKIPPED_PROTECTED=8`，源文件未修改。整体仍为 `REVIEW`，`coverage_completion_claim_allowed=false`、`humanize_completion_claim_allowed=false`，编译 `NOT_RUN`，声线符合性、跨单元重复和 fresh second pass 均未评估。产物见 [v12e fresh RESEARCH](build/maturity-v12e-fresh-forward-20260715/research/run/finalization_metadata.json)。该运行早于 `unit_id + chunk_binding_sha256` 的 LONG-14 bundle 合同，只能保留为 pre-LONG-14 历史证据，不能再称为当前最终前向。

### 18.9 两轮独立红队怎样继续击穿“看似闭环”

第一轮正确性审计没有把 v12 的新字段存在视为完成，而是直接寻找“能否拿错、能否重封、能否虚增”。它先发现五项问题：

1. builder 产生的 `PERSONAL/REVIEW` 会被 prepare 接收并误写 `REBUILT_PASS`；
2. 请求场景与 Profile `binding_scene` 没有强制相等；
3. 三份近重复完整文件能虚增 `unique_complete_units`，从 MEDIUM 升到 HIGH；
4. finalize 的 `voice_profile_manifest_sha256` 曾错误写成 Profile hash；
5. 长文文档把 PERSONAL 命令简写成只有 Profile 路径与 hash，遗漏 manifest/spec/root。

这五项修复后，定向 75 项和当时全量 381 项已经全绿，但第二轮两个彼此独立的只读代理仍实际构造出四条新的错误完成路径：

- **顺序攻击**：五份文本按 A–B–C–D–E 构成近重复链，相邻版本 containment 约为 0.969。旧算法只拿新样本与已选代表比较；同一文件集合换一个 sample spec 顺序，就能在 2 个与 3 个 complete representative 之间切换，进而发生 `MEDIUM/REVIEW ↔ HIGH/PASS`。修复后 `voice-dedup/v2` 对全部 exact/near 边取顺序无关的连通分量，稳定选代表；两个顺序都只得到 1 个完整代表、`MEDIUM/REVIEW`。
- **spec 自重封攻击**：攻击者把冻结 `voice_sample_spec.json` 的三条来源从 `USER_CONFIRMED_AUTHOR` 改成 `MODEL_GENERATED`，再重算 `prepare_integrity.json`；旧 finalize 只做 spec schema 检查，仍返回 `PASS/PASS`。manifest 已升级为 `humanize-voice-sample-manifest/v2`，新增 canonical `sample_spec_sha256`；finalize 独立核对 spec/manifest，prepare 封条即使被重算也不能替代来源绑定。
- **跨场景重标**：三份纯 COURSE 作者样本曾可通过 `--scene RESEARCH` 生成 `PERSONAL/PASS`，虽然全部 feature scope 仍是 COURSE。现在 PERSONAL 只有在唯一证据场景等于 `binding_scene` 时才可 PASS；跨场景或混合重标固定为 REVIEW，prepare 再由 `voice_profile_status_not_pass` 拒绝。
- **重复 JSON key 覆盖**：rewrite bundle 曾可同时写两个 `voice_profile_sha256`，让标准解析器用后一个正确值覆盖前一个错误值。finalize 现对 JSON/JSONL 使用 strict parser，重复 key、浮点数、非有限数字和过深结构直接失败；新增回归用两个同名 hash 证明该 bundle 不再进入单元验证。

红队还指出一个不会直接伪造长文 PASS、但容易误导调用方的 P2：只给 PERSONAL Profile、不重建 manifest/spec 时，validator 曾返回顶层 `PASS/0`。现在结果拆成 `profile_validation_status` 与 `production_admission_status`；前者可说明结构自洽，后者在缺少 `--rebuild-evidence` 时固定 `REVIEW/2`。只有代码注册表产生的确定性零样本 DEFAULT 可在无外部证据时直接准入。

对应审计见 [binding-audit.md](build/maturity-v12d-audit-20260715/binding-audit.md) 与 [test-gap-review.md](build/maturity-v12d-audit-20260715/test-gap-review.md)。这些发现解释了为什么“75 个相关测试全通过”仍不能结束：测试集合没有覆盖攻击构造时，绿灯只能证明已编码问题，没有证明状态机不存在别的假闭环。

### 18.10 回归、投影与资格边界

当前 v12h 自动化状态；前文 385/384 与 v12e tree 均只代表历史快照：

- 393 项测试运行完成，整体 `OK`，其中 1 项 Windows symlink 权限测试跳过；
- 15 个正式脚本全部通过 `py_compile` 与 `--help`；
- `PYTHONUTF8=1` 下 `quick_validate.py` 返回 `Skill is valid!`；
- action profile：50 张可用，0 张不可用；
- generator projection：28 文件，tree SHA-256 为 `ad1bf7f3af0e5bf9175b40ac8e05d394be00d95ce531499e85b6889e6e01bbba`；
- no-manifest qualification：`evidence_integrity_status=PASS`，`qualification_status=NOT_EVALUATED`，`atoms_pass=0/166`，evidence cap 仍为 E2，`production_e3_enabled=false`。

这些数字不等于“Skill 已成熟”。它们只证明当前实现、合同和拒绝路径在本地回归中一致。真正的全文声线符合性、跨块修复语重复、fresh second pass convergence 和外部盲评仍未闭合，因此本轮不能把 `humanize_completion_claim_allowed` 改成 true。

最终 projection 见 [v12h manifest](build/generator-projection-maturity-v12h-final-20260715-manifest.json)，no-manifest 审计见 [qualification-maturity-v12h-20260715-no-manifest.json](build/qualification-maturity-v12h-20260715-no-manifest.json)。后者进程与记录退出码均为 2，不把 `NOT_EVALUATED` 写成成功资格。

### 18.11 v12 后仍未完成的工作

当前剩余边界至少包括：

1. Profile hash 回显可能被生成端机械复制，不能替代独立声线评分；
2. 自动 feature 只覆盖可重建的低语义维度，复杂论证节奏仍需要逐文档连续阅读；
3. `AUTO` 长文场景尚无独立路由器，只能保守回退 GENERAL，且必须保持 `scene_routing_status=NOT_EVALUATED`；
4. PERSONAL 样本虽已在 prepare 当场重建，但本地 hash 不是外部身份签名；完整替换样本、spec、manifest、Profile 与全部自哈希仍需外部签名信任根才能识别；
5. 真实前向都只覆盖单个 unit，不能代表 52–55 KB 全文已经 Humanize；
6. 生成资格仍为 `NOT_EVALUATED`，不能用 393 项本地回归改写成 E3/E4 结论。

因此，v12 的准确表述是：Voice Profile 已从说明性文档升级为可构建、可重建、可冻结、可回显、可拒绝错配的生产链部件；全文声线终审层仍在建设中。

### 18.12 v12h：用真实前向修掉“正确拒绝中的错误理由”

这一轮没有从现有测试名称倒推实现，而是先把新 bundle 合同放到微信 `main.tex` 的真实
前向里。前向暴露了两类此前被绿灯遮住的问题：资格合同漏注册和跨 chunk TeX 假失败。

#### 18.12.1 资格合同从 163 扩到 166 个原子

`evaluation-contract.md` 已有 `LONG-14`，但旧 requirements 与 auditor 仍只登记到
`LONG-13`。只更新合同 hash 会让 oracle 不再 stale，却仍留下未注册行为。修复后：

- `LONG-14` 固定检查 bundle 的 `unit_id + chunk_binding_sha256 + voice_profile_sha256`、
  strict JSON 和跨 unit/旧 chunk 重放；
- `LONG-15` 固定检查跨块 TeX 的 `FRAGMENT -> DOCUMENT` 双层结构门；
- `VOICE-11` 固定要求完整一致性替换下仍保持 `identity_verified=false`；
- requirements 版本为 `1.7.0`，合同版本为 `2026-07-15.3`，原子总数为 166。

oracle 的 provenance 也发现一处真漂移：`corpus-action-sources.json` 已变化，但 catalog 仍保存
旧 hash，而 auditor 只检查“字段像 SHA-256”，没有读取 Skill 内来源重算。现在所有
`references/*` provenance 必须是 canonical 相对 POSIX 路径、不得穿越 symlink、必须存在且
实际 hash 一致；未随安装 Skill 分发的 `tests/fixtures/*` 只保留为历史派生说明，不冒充本地
可验证来源。对应回归会主动伪造一个内部 provenance hash，要求 catalog 加载硬失败。

#### 18.12.2 新 bundle 合同的真实前向结果

fresh run 位于 [maturity-v12f fresh forward](build/maturity-v12f-fresh-forward-20260715/research/finalization_metadata.json)：

- 输入为微信 `main.tex`，54834 字节，SHA-256 为
  `f97c5dc63e66d094e2ec73fbd2c935393a3370229db1d46baae9772bdacd0625`；
- prepare 产生 36 个 unit，其中 28 个 `PENDING`、8 个 `SKIPPED_PROTECTED`；
- 第一次 ephemeral CLI 因本机旧 API key 返回 401，发生在生成前，没有 bundle，单独记为
  基础设施失败，不算 Skill 行为失败；
- 第二次 fresh 进程在 read-only 模式下只返回 JSON，原始响应保存在
  [fresh-agent-raw-response.json](build/maturity-v12f-fresh-forward-20260715/research/fresh-agent-raw-response.json)，
  SHA-256 为 `d80154e784793cf4445d79a23862bf3cf7637600de54e404abc5baa06d1b5e19`；
- 它选择 `U-bc353709e690`，首轮正确回显 unit、chunk binding 与 scene-default Voice hash；
  finalizer 记录 `rewrite_bindings_matched=1`、`mismatched=0`，说明 LONG-14 对真实生成器可用；
- 该进程仍能读取宿主机完整 Skill，故只能称“独立新进程前向”，不能称已证明 oracle 不可达
  的 E3 盲测。

首轮 finalizer 把这个 unit 判为 `FAIL`，但失败详情显示改前和改后同时为
`begin{document} has no matching end`。原因不是生成器删除了 `\end{document}`，而是该 unit
本来只覆盖全文开头，结束环境位于后续 chunk。旧逐块 validator 把 fragment 当完整文档，
因此任何类似前导块都无法成为 `DONE`。

修复后的 unit 门显式写 `document_scope=FRAGMENT`：

- 只容忍改前已经存在且改后问题列表完全相同的环境/花括号边界不平衡；
- 环境名称或顺序变化仍触发 `LATEX_ENVIRONMENT_ORDER_CHANGED`；
- 环境问题列表变化触发 `LATEX_ENVIRONMENT_FRAGMENT_BALANCE_CHANGED`；
- 花括号问题变化触发 `LATEX_BRACE_FRAGMENT_BALANCE_CHANGED`；
- 接受的 unit 组装回全文后，仍以 `DOCUMENT` 范围执行完整平衡检查。

同一原始 bundle 重放后，硬不变量层从错误的 `FAIL` 变为 `PASS`，但 unit 仍没有被放行：
生成器删掉了原文一次“结果表明”，统一验证器产生
`SPEECH_ACT_REPORTING_OBSERVATION_CHANGED`，状态保持 `REVIEW/2`。最终账本为
`PENDING=27 / UNRESOLVED=1 / SKIPPED_PROTECTED=8`，`protected_hashes_ok=PASS`，源文件 hash
不变。这个结果比强行修到 DONE 更有证明力：本轮只消除了 chunk 边界误报，没有用结构修复
覆盖真实的言语行为风险。

#### 18.12.3 Voice 本地哈希的精确能力边界

本地 Profile、manifest、sample spec、chunk 与 prepare 封条能拒绝错配、局部篡改和旧工件
重放，前提是 allowed root 与其中样本字节被调用方视为可信输入。如果同一主体可以同时改写
源样本、spec、manifest、Profile 以及所有自哈希，本地 validator 只能证明新工件内部一致，
不能证明样本历史上属于某个真人。PERSONAL 即使准入 PASS，仍固定
`claims.identity_verified=false`。抵抗完整一致性替换需要代理无法访问私钥的外部签名 receipt，
并绑定样本根、源文件 hash、角色范围、场景、签发者、时间和撤销状态；当前 Skill 未实现该
信任根。

#### 18.12.4 当前可复核快照

- 全量 unittest：`Ran 393 tests`，`OK (skipped=1)`；
- 15 个脚本：`py_compile=PASS`，全部 `--help=PASS`；
- 官方 Skill 校验：`Skill is valid!`；
- action profile：50 available、0 unavailable、23 个可读来源，GENERAL 仍为
  `CORPUS_INSUFFICIENT`；
- generator projection：28 文件，tree
  `ad1bf7f3af0e5bf9175b40ac8e05d394be00d95ce531499e85b6889e6e01bbba`；
- no-manifest：`integrity=PASS / qualification=NOT_EVALUATED / 0 of 166 / E2`，进程与记录
  exit code 都为 2；
- 当前工件：[v12h projection manifest](build/generator-projection-maturity-v12h-final-20260715-manifest.json)、
  [v12h qualification](build/qualification-maturity-v12h-20260715-no-manifest.json)、
  [v12h action profile](build/maturity-v12h-action-profile-20260715.json)。

v12h 比 v12e 更成熟的地方不是“测试又多了 8 项”，而是三项以前会误导完成态的边界变成
可观察合同：bundle 精确绑定、fragment/full-document 分层、Voice 本地一致性与外部身份分层。
仍未闭合的核心项没有变化：全文 Voice conformance、跨 unit 新增修复短语重复、fresh second
pass convergence、逐 unit AUTO 路由和外部 E3/E4 信任链。因此当前版本仍不能称为完全成熟。

### 18.13 v13：全文 Voice 与跨 unit 模板不再是假字段

v12h 的 `voice_conformance_status` 和 `cross_unit_repetition_status` 虽然诚实，但仍固定为
`NOT_EVALUATED`。这能阻止虚假完成，却不能回答两个生产问题：同一 Profile 是否在全文被
明显写丢，以及两个局部 validator 都 PASS 时是否共同生成了新的修复模板。v13 没有用一个
模糊“相似度”填空，而是把可证明范围拆成两个独立门。

#### 18.13.1 Voice 门只验证已注册、可重建的机械特征

Profile builder 原有 7 类正特征：对象/本文主语、第一人称主语、条件起句、显式逻辑连接、
段末标点、括号限定、分号分组和非列表正文；负控为已知 AI 句壳与重复段首。此前这些 feature
只用于建档，finalize 没有消费。v13 把 extractor 提升为 builder 中唯一注册表，并新增
`feature_extractor_policy_sha256`。Profile 中每个 feature 的 extractor hash 必须能由当前
`rule_id + regex + flags + code` 重建；规则换了但旧 Profile 仍自洽时，全文门返回 REVIEW，
不能拿过期证据继续 PASS。

DEFAULT 与 PERSONAL 采用不同语义：

- DEFAULT 不伪造个人分布。只有场景已确定、Profile/chunk/bundle 绑定闭合、全部目标 unit 的
  统一 validator 为 PASS、默认披露仍为 true 时，`voice_conformance_status=PASS`；证据 basis
  固定为 `SCENE_DEFAULT_UNIT_VALIDATION`，`personal_voice_conformance_status=NOT_APPLICABLE`、
  `personal_voice_claim_allowed=false`。
- PERSONAL 至少需要 6 个目标正文块。门只使用 protected-masked 作者视图，不读取公式、代码、
  引语、题干或 OCR 内容；逐 feature 报告 before/after opportunity、support、ratio、容差、
  support drop、结构 floor 与当前/声明 extractor hash。
- 内容敏感特征不会被强迫插入。样本常用“因此”、括号或分号，而目标正文原本不需要时，门不会
  因绝对频率低而要求补写；它只在本轮改写让既有支持至少减少 2 个块、比例下降至少 25 个百分点
  并远离 Profile 时拦截。段末标点和非列表正文属于结构特征，目标足够长时另有保守 floor。
- Profile 的 `DO_NOT_AMPLIFY` 只允许保持或减少。新增长句壳、或新出现覆盖至少 3 个 unit 的同一
  四汉字段首时返回 REVIEW。
- 所有 PASS 均固定 `identity_verified=false`。它证明“注册机械特征没有明显回退”，不证明完整
  作者气质、写作能力、历史归属或真人身份。

直接单测使用 6 个“本文说明……”段落：NO_CHANGE 时 feature 支持为 `6/6` 并 PASS；把 6 个
段落全部改成未注册的“结果说明……”后，支持从 `6/6` 降到 `0/6`，门返回 REVIEW。只有 2 个
目标块时，即使字面完全不变也返回 `INSUFFICIENT_TARGET_BLOCKS`，避免短片段冒充全文拟声。

#### 18.13.2 跨 unit 门执行真实语料负例，不建立通用术语 n-gram 误杀器

这一门的第一版没有拍脑袋扫描任意高频专业词。它只执行两类已有依据的 detector：

1. `lexical-signals.json` 中的 `LEX-REPAIR-01`，覆盖“这里真正需要、这里只看/保留/讨论/比较、
   其余情形沿用、不再展开/赘述”等 Humanize 修复句壳；
2. `corpus-action-sources.json` 中来源仍可读、action profile 状态为 `AVAILABLE`、场景为 `ALL`
   或当前场景的 `negative_guard`。其中 `NEGATIVE-TEMPLATE-01` 来自 GPT 生成 CET6 TeX 的人工
   负例阅读，检测自动未来桥接和跨段重复“不是……而是……”；MODELING 与 GENERAL 还有
   README 壳、施工计划腔、治理验收腔、期刊过拟合、宣传 claim 堆叠、OCR 问答和 API 导航等
   已登记 guard。

`positive_action` 不会被执行为 detector。它仍只说明抽象组织动作有来源锚，不能把正向语料
变成句子扫描器。若适用的 negative guard 因源文件乱码、缺失或行范围漂移变为 UNAVAILABLE，
全局门只能 REVIEW，不能静默跳过后写 PASS。

匹配视图先删除保护占位符内部内容，再执行 NFKC、删除零宽字符和汉字之间的普通/Unicode
空格；因此“这\u200b里只比较”与“这 里只比较”不能绕过。它不跨空段、标题、列表、TeX
结构行、公式、引语或代码边界拼接，也不做通用连续汉字 n-gram，所以“量子纠缠态”“边界条件”
等必要术语跨章节重复不会仅因词频被判模板。

门按 unit 计算 before/after 多重集，再按逻辑文档聚合。必须同时满足：

- after 达到 detector 自身阈值；
- 命中覆盖至少两个不同 unit；
- 至少一个 unit 的 after occurrence 数大于该 unit 的 before。

原文已经跨 unit 重复、候选没有增加时进入 `inherited_findings`，不阻断 NO_CHANGE。命中新增
重复时，只有拥有新增 occurrence 的 unit 从临时接受集回退为 `UNRESOLVED`；继承 occurrence
所在 unit 不受连坐。回退同时清空 `hash_after/diff_path`、从 `accepted_by_file` 移除候选，并用
冻结原文组装 `rendered_partial`。这修复了“元数据写 REVIEW，但 coverage ledger 仍为 DONE、
diff 仍发布”的假闭环。

证据保存在 `validation/cross_unit_repetition.json`，包括：

- FULL/PARTIAL scope、unit inventory hash、before/candidate 逻辑文档 hash；
- lexical policy、action catalog、action profile 与全部 active detector definition hash；
- finding fingerprint、before/after occurrence、before/after unit、introduced unit；
- inherited findings、blocking unit 集合和 normalization policy。

两个 TeX unit 的真实集成 fixture 分别把“本段只比较峰值”“本段只讨论误差”改成“这里只比较
峰值”“这里只讨论误差”。两个 fragment validator 单独均 PASS；全文门识别同一家族跨 unit
新增，两个 unit 均回退为 UNRESOLVED，发布的 partial 中没有“这里只”。相反，原文已经包含
两个该类句壳且两个 bundle 都是 NO_CHANGE 时，门记录 inherited 并 PASS。另一个 fixture 把
两个“不是……而是……”分别放在两个 unit，实际命中 CET6 负例锚定的
`NEGATIVE-TEMPLATE-01`。

#### 18.13.3 真实 main.tex 没有被新门洗成通过

v13 重新 prepare 微信 `main.tex`：输入仍为 54834 字节、同一 SHA-256 和 snapshot ID，仍得到
36 个 unit（28 PENDING、8 SKIPPED_PROTECTED）。由于 extractor policy 成为 Profile hash 的
一部分，v12h 的 bundle 不能直接重放；复核只把旧 fresh agent 的原始 `masked_text` 绑定到
新的 chunk/Voice hash，正文一字未修。这是历史输出重绑定回归，不冒充新的 fresh forward。

结果保持正确分层：

- hard invariant PASS，`document_scope=FRAGMENT`；
- speech-act REVIEW，warning 仍为 `SPEECH_ACT_REPORTING_OBSERVATION_CHANGED`；
- style-signal PASS，unit 仍为 UNRESOLVED；
- 27 PENDING、1 UNRESOLVED、8 SKIPPED_PROTECTED；
- Voice conformance REVIEW，因为 28 个可处理 unit 只评了 1 个；
- cross-unit repetition 为 `REVIEW/PARTIAL`，新增 finding 为 0；
- full-format errors 为 0，源文件修改为 0；
- coverage/Humanize completion claim 均为 false。

证据见 [v13 real-main audit](build/maturity-v13-real-main-20260716/research/v13-real-main-regression-audit.md)。
新全局门没有把局部语义 warning 覆盖成 PASS，也没有因为“未发现跨块模板”把 partial 范围
冒充 FULL。

#### 18.13.4 当前可复核快照

- 全量 unittest：`Ran 402 tests`，`OK (skipped=1)`；
- 15 个脚本：`py_compile=PASS`，全部 `--help=PASS`；
- 官方 Skill 校验：`Skill is valid!`；
- action profile：50 available、0 unavailable、23 个可读来源，GENERAL 仍为
  `CORPUS_INSUFFICIENT`；
- contract：`2026-07-15.4`，SHA-256
  `f260eabe484400dfcd46cce0c083350f0b87de01ba5719ae9bfcb2ebf6940c6f`；
- requirements：`1.8.0`，SHA-256
  `d7c2cf6d089afe3663f775a99588f0638290bc6b96ee055a6ff6dd9f693c3c42`；
- oracle：`1.0.6`，SHA-256
  `177977ae018c75c9770749b25a6dc0de829a130ca7a5f210a5641d5b8a2f7e07`；
- generator projection：28 文件，capability source
  `5b8f1075aa54bcca5ab694aefd68b68f4fcef39ca57a4f7f48f13085ff4a7183`，tree
  `dfa5d35be0f4be8ea02b3d3e592225e9f5c7caedab1a1ccb30fae079ba9f84b8`；
- no-manifest：`integrity=PASS / qualification=NOT_EVALUATED / 0 of 168`，进程与记录 exit
  code 均为 2；
- 当前工件：[v13 projection manifest](build/generator-projection-maturity-v13-final-20260716-manifest.json)、
  [v13 qualification](build/qualification-maturity-v13-20260716-no-manifest.json)、
  [v13 action profile](build/maturity-v13-action-profile-20260716.json)。

v13 已关闭两个此前明确列出的生产缺口，但仍不能称完全成熟：fresh second-pass convergence
尚未执行，AUTO 仍未逐 unit 路由，PERSONAL 来源身份与 E3/E4 隔离仍缺外部签名信任根。

### 18.14 v14：fresh second pass 从声明字段升级为活证据控制面

v13 的完成门仍有一个故意保留的硬缺口：`humanize_second_pass_convergence` 永远是
`NOT_RUN`。同一 run-dir 重放同一 bundle 只能证明组装字节幂等，不能证明模型把第一遍 clean
输出当作新输入后不会再次轮换同义词、改标点或搬句序。v14 不再把两者混用：

- `assembly_replay_idempotency` 继续只回答“同一 bundle 能否重放出同一派生树”；
- `humanize_second_pass_convergence` 只由新的 fresh 控制面产生；
- 两者都 PASS，仍需 coverage、scene、rewrite binding、Voice binding、全文 Voice 与跨 unit 门
  全部 PASS，才能令 `humanize_completion_claim_allowed=true`。

#### 18.14.1 五段式执行链

第一遍完整发布后，`prepare_humanize_second_pass.py` 读取第一遍 `rendered_manifest.csv`，逐个
复核路径、字节数与 SHA-256，并拒绝 manifest 外新增文件、重复 file/unit identity 或任何
`rendered_partial`。它把第一遍 rendered 文件作为第二 run 的唯一 source，再由原长文 preparer
重新生成 snapshot、units、chunks、保护 span 和 Voice 绑定。因此第二遍不是拿旧 chunks 改名，
而是对 clean 文件重新走完整准备流程。

每个第二遍 PENDING chunk 单独封存为 public case。所有 case 使用完全相同的 canonical prompt：
只要求模型重新阅读当前 masked chunk，并根据是否仍需实质修改选择 `REWRITE` 或 `NO_CHANGE`。
prompt 不含第一遍 bundle、diff、decision、expected answer、资格 atom 或 verifier 规则。public
manifest 与 seal 绑定 input、prompt 和 public context；unit、chunk 与 Voice 三个身份必须在输出
strict JSON 中精确回显。

生成后按以下顺序处理：

1. 每个 unit 用 `run_humanize_generation_trial.py` 启动独立新进程；
2. collect 只复制 strict、无 code fence、无重复键、unit/chunk/Voice 精确匹配的原始 output；
3. 第二遍 finalizer 对全部 bundle 运行普通长文门，产生真实 coverage ledger 与 rendered tree；
4. `verify_humanize_second_pass.py` 重读 plan、collection、runner receipt、run record、run seal、
   public seal、execution projection、第二遍 finalization 和两遍 rendered；
5. 第一遍 finalizer 接收 receipt 时不只验自哈希，而是按 receipt 的 evidence roots 重新执行
   verifier；live receipt 与提交 receipt 必须逐字段相同。

#### 18.14.2 收敛和失败不再共用一个模糊状态

`LONG-17/P0` 把三类结果分开：

| 情形 | 状态 | 完成声明 |
|---|---:|---:|
| 全部初始 PENDING unit 均有 fresh `NO_CHANGE`；第二遍 ledger 全为 NO_CHANGE；两遍 rendered tree 相同；活证据复验一致 | `PASS/0` | 只放开 second-pass 这一门 |
| 缺 trial、缺 bundle、第二遍仍有 PENDING/UNRESOLVED、任一 fresh `REWRITE`、两遍树不同 | `REVIEW/2` | false |
| plan/collection/receipt/record/seal/scene/Voice/tree/hash 错配，重复 run id，projection 漂移，receipt 底层证据被删除 | `FAIL/1` | false |

这一分级避免了两个相反错误：不能因为第二遍提出了合理修改就写“收敛 PASS”，也不能把外部
服务暂时无输出误写成文稿硬损坏。`REWRITE` 意味着文风尚未稳定，应回到第一遍规则查冲突；
证据错配则意味着审计链本身不可信，必须硬失败。

#### 18.14.3 receipt 不再是可以手工重算的通行证

第一版草案只校验 receipt schema、自哈希、tree、Voice、scene 和若干 64 位十六进制字段。
红队证明这仍可伪造：任何调用方都能填写假的 process hash 后重算 JSON 自哈希，或者在 receipt
生成后删除全部 trials，而第一遍 finalizer 仍会 PASS。v14 将 receipt 扩展为活证据索引：

- `evidence_roots` 精确记录 first run、second run、cases、trials 和 rewrites；
- `evidence_artifacts` 绑定 plan、collection、cases tree、trials tree 和 rewrites tree；
- finalizer 当场从固定 Skill 路径重新加载 verifier，忽略 `sys.modules` 中同名注入模块；
- verifier 重新计算每个 runner artifact、public artifact、projection manifest/tree 和 staged case；
- 任何底层文件新增、删除、替换或跨版本重放都会让 live receipt 与提交 receipt 不同。

这仍是本地 E2 完整性，不是外部签名。能同时改写 Skill、全部 trials 和所有哈希的同一主体仍
可伪造整套本地历史；所以 claims 固定保留 `filesystem_isolation_verified=false`、
`oracle_unreachable_verified=false`、`human_identity_verified=false` 与
`academic_correctness=NOT_EVALUATED`。它解决的是错误绑定和虚假闭环，不冒充不可抵赖证明。

#### 18.14.4 红队攻击矩阵

新增 [second-pass tests](tests/test_humanize_second_pass.py) 不是只检查文件能生成，而是实际攻击
完成态：

| 攻击 | 修复前 | v14 |
|---|---|---|
| receipt 的 run id 与 run record 不同，但重算 record/seal hash | 可 PASS | `FAIL` |
| 两个 unit 复用同一 run id | 可 PASS | `FAIL` |
| receipt projection tree 与 record/seal 不同 | 可 PASS | `FAIL` |
| trial 中实际 `execution/skill` 被改写，字段 hash 不动 | 可重新出 receipt | 现场 `verify_projection` 后 `FAIL` |
| 删除 trials，只保留自哈希 receipt | 第一遍 finalizer 可 PASS | 活证据根不存在，`FAIL` |
| run record 把 `generator_context.complete` 改成 true | 可 PASS | `FAIL` |
| isolation 子记录声称 oracle 已不可达 | 可 PASS | `FAIL` |
| 第一遍 rendered 藏有 manifest 外文件 | second prepare 会忽略 | prepare 拒绝 |
| plan 自洽重签但改成 `expected_outcome_exposed=true` | collect 可继续 | collect 拒绝 |
| code fence、重复 JSON key、错 unit/chunk/Voice | 可能污染 rewrites | collect 拒绝 |
| 任一真实 `REWRITE` | 可能与组装幂等混淆 | `REVIEW/2`，不出 PASS receipt |

16 项 second-pass 专项测试全部通过。它们使用真实 28 文件 projection 和真实 runner 工件结构；
只有外部模型 invocation 被 fixture 替代，因此证明控制面行为，不证明真实模型稳定性。

#### 18.14.5 generator projection 反泄漏

上一版计划曾拟把 prepare 与 verifier 两个脚本加入 generator projection，文件数从 28 扩到 30。
红队审查否决了这一做法：verifier 明文规定“全部 NO_CHANGE、两遍树相同才收敛”，若 fresh
generator 能读取它，第二遍就提前知道验收答案，`expected_outcome_exposed=false` 成为假声明。

最终边界保持 28 文件：

- `prepare_humanize_second_pass.py` 与 `verify_humanize_second_pass.py` 明确归入 evaluation/control
  surface，不进入 projection；
- 完整安装版 finalizer 保留 receipt 复验；投影版 finalizer 用固定 Python span transform 删除
  验收字段与 verifier 路径，只留不可执行的控制面 stub；
- 完整 `long-document-workflow.md` 保留五段命令；投影版用固定 H2/段落 transform 替换为普通
  独立复读说明，不暴露“全部 NO_CHANGE”条件；
- `SKILL.md` 的 second-pass 控制块使用唯一 marker，在 projection 中确定性删除；
- builder 对缺 marker、重复 marker、锚点漂移、遗留 verifier basename 或控制字段全部 fail closed。

两次独立重建得到完全相同的 manifest SHA-256
`574382dfc7ccff24d5d7e32955d32392ca1433b1bb36682a98e42607bd7571c9` 和 tree
`1df1c31d47ea9dffbf98bfa5bee3d6936f71ac973a4fb2bc87e76f30271792af`。capability source 为
`bbf1c420b199d22d61072674761784d987b3c626d1d1a5f4235c54711e973edc`；policy canonical hash 为
`f072ab31f0d5790fc7700351c175c33452469ef89a07a3dc216aa15a6fa85f0d`。

#### 18.14.6 真实 fresh campaign 与进程树修复

真实试跑使用现有 `humanize_forward_v10/research_after.md`，第一遍 1 个 unit、111 个作者汉字、
1 个保护 span，完整 NO_CHANGE 发布后各局部门均 PASS。second prepare 生成新的 chunk binding 和
无答案 sealed case。

首次真实 `codex exec` 暴露 runner 的进程管理缺陷：内部 timeout 为 120 秒，但旧代码只终止
父进程；node/codex 后代继续持有 stdout 管道，外层 184 秒后才强制结束，并留下 3 个本次新
进程。它们按 PID 与启动时间精确终止，没有误杀已有 VS Code/Codex 会话。

修复后，Windows runner 使用新进程组并在 timeout 时执行整棵进程树终止；POSIX 使用独立
session/process group。真实孙进程测试由约 8.06 秒等待自然退出缩短为约 1.38 秒收口。随后
以 45 秒 timeout 重试，46.3 秒内得到正式 `INFRA_INVALID` receipt：

- `timed_out=true`、`returncode=1`、`output_present=false`；
- projection 后验为 `NOT_COMPLETED`；
- filesystem isolation 为 false、oracle unreachable 为 UNVERIFIED；
- retry 后没有遗留新 Python/node/codex 进程。

下游状态严格保持：collect `FAIL`，第二遍 finalizer `REVIEW/2` 且 1 个 PENDING，verifier
`REVIEW/2`，receipt 不生成，第一遍 `humanize_second_pass_convergence=NOT_RUN`、Humanize
completion false。完整审计见 [real second-pass audit](build/maturity-v14-second-pass-real-20260716/real-second-pass-audit.md)。

#### 18.14.7 当前可复核快照

- 全量 unittest：`Ran 421 tests in 41.881s`，`OK (skipped=1)`；
- 17 个 Skill 脚本：`py_compile=PASS`，全部 `--help=PASS`；
- `quick_validate.py` 首轮因 Windows GBK 读取 UTF-8 抛 `UnicodeDecodeError`；按既定乱码策略以
  `PYTHONUTF8=1` 重试后输出 `Skill is valid!`；
- contract：`2026-07-16.5`，SHA-256
  `d1fda0af6aedd81adb39b0763571d9e886b3dd6fcfd7d27ec3fe8c6977a1c253`；
- requirements：`1.9.0`，SHA-256
  `5fedf6b2f22fec20adfa0865c962b23667ad15dcfc9002a31ecb479cfb229974`；
- oracle：`1.0.7`，SHA-256
  `7f61992db6b485afcc37cf953f49b09d3cf2bfbfd5faedccf1e0211c7a676ff4`；
- qualification：`integrity=PASS / qualification=NOT_EVALUATED / atoms_pass=0/169`，exit 2；
- action profile：`PASS`，23 个可读来源、50 available、0 unavailable；GENERAL 仍为
  `CORPUS_INSUFFICIENT`；
- generator projection：28 文件，两次重建 manifest/tree 相同，证据封顶 E2。

最终工件：[v14 stable projection manifest](build/generator-projection-maturity-v14-stable-20260716-manifest.json)、
[v14 deterministic repro](build/generator-projection-maturity-v14-stable-repro-20260716-manifest.json)、
[v14 qualification](build/qualification-maturity-v14-stable-20260716-no-manifest.json)、
[v14 action profile](build/maturity-v14-action-profile-20260716.json) 与
[v14 real second-pass audit](build/maturity-v14-second-pass-real-20260716/real-second-pass-audit.md)。

v14 关闭了“second pass 只存在于字段”“receipt 自哈希即可伪造”“verifier 泄漏给 fresh
generator”和“timeout 留下进程树”四个生产级缺口，但仍不能称最终成熟。真实 fresh campaign
本次没有模型输出，169 原子资格仍为 0/169；AUTO 逐 unit 路由、PERSONAL 外部签名来源、E3
filesystem/oracle isolation 与 E4 可信人工链仍未实现。

## 19. 第十五轮：来源纠偏、AUTO 真路由与 fresh Voice 闭环

### 19.1 为什么 v14 的“当前快照”必须作废

v14 后的继续审计没有从“再加几条规则”开始，而是先核对正向语言材料的来源身份。这里发现了
一个会直接污染整个 Skill 学习方向的 P0：微信 `main.tex` 已由用户明确说明为 GPT 生成，但旧
catalog 曾把它登记成 RESEARCH 正向 action 来源；CET6 的 GPT 报告也曾支撑 REPORT 正向卡。
这意味着工具一边声称“去 AI 味”，一边把模型成稿中的组织模板当作正向人类表达学习。即使卡片
只保存抽象动作，这个来源角色仍然错误，不能靠“不复制原句”洗掉。

v15 将来源合同升级为结构化 `origin_class`：

| 来源 | 当前 origin/role | 允许用途 | 明确禁止 |
|---|---|---|---|
| 微信 `main.tex` | `MODEL_GENERATED / negative_template_reference` | 检测重复元问题对照、自证式收尾、自动闭合 | RESEARCH 正向 action、PERSONAL Voice、真人范文、句库 |
| CET6 GPT 报告族 | `MODEL_GENERATED / negative_template_reference` 或版本审计 | 检测列表堆叠、指令口吻、固定槽位、同义轮换 | REPORT 正向 action、作者声线 |
| CET6 `test.tex` | `MODEL_GENERATED / negative_template_reference` | 检测强制对照和自动愿景结尾 | 反向生成“自然写法” |
| `cet6.tex` | `user_excluded` | 只保留排除审计 | 读取、统计、动作卡 |
| 乱码备份 | `unreadable_excluded` | 记录跳过 | 猜字、恢复、推断语言特征 |

构建器新增硬门：`MODEL_GENERATED + positive_action_reference` 直接失败；模型来源必须是带可审计
detector 的负例或纯审计角色。当前 action profile 的真实结果是：26 个登记来源，23 READABLE、
3 EXCLUDED_CONFIG；41 张卡 AVAILABLE、0 UNAVAILABLE；`model_generated_positive_source_count=0`。

场景支持不再用“总卡片数很多”掩盖空白：

| 场景 | 正向卡 | 独立正向来源 | 状态 | 候选策略 |
|---|---:|---:|---|---|
| COURSE | 4 | 2 | `SUPPORTED`，但来源身份仍含未决 | 最多选两张适用卡，继续保护原稿事实 |
| MODELING | 27 | 7 | `SUPPORTED`，origin assurance 为 `UNRESOLVED_PRESENT` | 只借抽象组织动作，不借事实、公式和结论 |
| RESEARCH | 0 | 0 | `CORPUS_INSUFFICIENT` | `corpus_action_support=NONE` |
| GENERAL | 0 | 0 | `CORPUS_INSUFFICIENT` | `corpus_action_support=NONE` |
| REPORT | 0 | 0 | `CORPUS_INSUFFICIENT` | `corpus_action_support=NONE` |

旧 `RESEARCH-MAP/EVIDENCE/MECHANISM/SCOPE/CLAIM/UNCERTAINTY` 六张卡和三张 GPT REPORT 正向卡已
删除。研究场景只保留 `NEGATIVE-RESEARCH-MAIN-META-SHELL-01`：它拦截连续用“真正的问题”“关键
不是 A 而是 B”重述元问题，随后用“这说明/由此可见”自行确认论证完成的组合。这个负例不能
倒过来教模型套另一组句子；命中后必须回到当前原稿已有对象与判断，没有对象时 `UNRESOLVED`。

### 19.2 从真实 GPT TeX 中提炼出的可执行负面抓手

这次不是只写“AI 文风过于模板化”，而是把 GPT TeX 的可观察问题压成 detector 和编辑动作：

1. **元问题重复命名**：同一段连续出现“真正的问题是”“关键不在于”“本质上不是”，看似推进，
   实际只替换标签。动作不是找一个新同义词，而是只保留一次问题定义，后句进入对象或证据。
2. **对照壳替代判断**：`不是 A，而是 B` 在没有真实误读时被用作每段发动机。单次命中不判错；
   同一局部单元重复或与“真正/关键”联用才进入 guard。
3. **自证式收尾**：段尾自动接“这说明、由此可见、从而证明”，但前文没有新增证据层。删除这类
   出口后若主张仍成立，直接停句；若主张依赖该出口制造强度，保持 REVIEW。
4. **列表型报告腔**：标题、编号、命令句和动作卡密度过高，把论文正文写成执行清单。保留真正的
   并列结构，但将只有一个信息重心的列表还原为散文，不迁移报告的无主语命令口吻。
5. **同义词轮换**：删掉“值得注意”后改成“必须注意”，删掉“奠定基础”后改成“成为出发点”。
   验收必须扫描新稿中的同族候选，不能只确认原词消失。
6. **自动愿景桥接**：每节末尾都写“为后续分析提供支撑/为未来研究奠定基础”。只有输入明确给出
   后续用途时保留，否则删除；不能换成“供后续参考”继续留壳。
7. **编辑后台泄漏**：`本节需要、正文应、需要分开报告` 被原样写进成稿。DRAFT 先拆分
   `FACT_PAYLOAD / EDITORIAL_REQUIREMENT / FACT_BOUNDARY`，编辑动作由组织实现，不进入正文。

这些抓手的共同点是可定位、可复扫、可给具体 KEEP 理由。它们不是“凡出现某词就删”的禁词表；
引语、正式术语、真实教学提醒和用户结构锁仍优先。

### 19.3 AUTO 从字符串占位升级为逐 unit 路由

v14 的合同仍写着 `AUTO` 暂绑 GENERAL，实际需求却是混合长文按 unit 使用不同场景。v15 新增
`scene-routing-policy.json` 与 `route_humanize_scene.py`，完整 unit 的标题路径和去保护正文共同
计分，evidence 只输出 rule ID、次数和贡献，不导出命中原文。

当前裁决如下：

- 强信号达到阈值且领先 margin：`ROUTED`；
- 专属场景信号不足：`FALLBACK_GENERAL`；
- 强平局或 margin 不足：`AMBIGUOUS`，unit 为 `UNRESOLVED`；
- 弱信号与逻辑文档 prior 同场景、且该场景为局部最高：`ROUTED_DOCUMENT_PRIOR`；
- 完全中性的背景、结论或共享标题不能只靠 prior 继承专属场景。

红队先后击穿了五种路由假设：工程“实验结果”被误分 RESEARCH、TeX `{solution}/{note}` 未进入
COURSE、`Notebook` 被 `note` 子串误报、摘要/引言/结论单独被当成 RESEARCH，以及一个强
MODELING 单元把中性“背景”全局拖成 MODELING。修复后，共享标题只有弱证据；`{solution}/{note}`
使用精确 TeX role；document prior 只补同场景弱证据，绝不消解 `AMBIGUOUS`。

prior 的范围也经历了两次修正。最初按物理文件计算，`\input` 拆出的章节无法继承主文档用途；
改为逻辑 include 根后，又必须防止零证据传播。最终实现同时满足：include 图跨文件共享 prior，
本 unit 必须有同场景弱证据。second pass 只把第一遍 relation=seed 的 rendered 文件作为新 seed，
让 include 边重新发现；不再把所有 rendered 文件平铺成独立 seed。

AUTO 同时物化四个不同 hash 的 DEFAULT Profile：

- `voice_profile_set.json`：set 身份、四个 entry 和固定 false claims；
- `voice_profiles/course.json`；
- `voice_profiles/general.json`；
- `voice_profiles/modeling.json`；
- `voice_profiles/research.json`。

单一 supplied Profile 暂不允许与 AUTO 混用，固定报 `AUTO_does_not_accept_single_voice_profile`。
这是显式能力边界，不用一个 PERSONAL Profile 假装覆盖四类用途。

### 19.4 finalizer 的重封攻击

仅有 `prepare_integrity.json` 不构成信任根，因为同一攻击者可以修改文件后重算全部哈希。v15
因此把“从冻结源独立重建”扩展到 route、Voice 与 metadata。下表均有真实单元攻击测试：

| 攻击 | 旧风险 | v15 裁决 |
|---|---|---|
| 修改 unit scene、routing decision、Voice hash，再同步 ledger/chunk/seal | 自洽伪造可越过普通 hash | 从 frozen source 和当前 policy 重建后 `FAIL` |
| 修改 prepare 顶层 `status=PASS`、`completion_claim_allowed=true`、`DONE=999` | finalizer 忽略伪字段仍发布 PASS | 精确 metadata 派生重算，字段不符 `FAIL` |
| 修改冻结 routing policy、metadata 与 seal | 旧规则可被 run 内工件替换 | 与当前安装 policy 字节/canonical hash 比较，`FAIL` |
| Profile set 的 `claims.identity_verified=true` 并重算 set hash | 本地 hash 被误当身份授权 | claims 必须精确为 false，`FAIL` |
| 在 Profile entry 中夹带 `identity_verified=true` | open object 忽略未知键 | entry 精确键集合，`FAIL` |
| metadata binding 夹带 `external_clearance=VERIFIED_HUMAN` | open object可携带越权声明 | binding 精确键集合，`FAIL` |
| 把 MODELING 的合法 Voice hash放到 COURSE bundle | hash 格式合法但场景错误 | `voice_profile_hash_mismatch`，unit `UNRESOLVED` |
| protected-only 歧义标题 | 制造不存在的可编辑缺口 | 保持 `SKIPPED_PROTECTED`，不增加 unresolved |

本地 Profile 的能力声明仍被限制：它只证明当前 supplied bytes 的机械绑定。即使样本、spec、
manifest、Profile 和全部本地哈希被一起替换，`identity_verified` 仍必须是 false；只有未来接入
代理无法访问私钥的外部签名信任根，才可能证明历史来源身份。

### 19.5 fresh second pass 现在能看到 Voice

v14 的 second pass 虽然在最终阶段比较 Voice hash，但 fresh generator 的 sealed case 只有 chunk；
PERSONAL Profile 的特征并未进入生成上下文。模型在看不到声线的情况下决定 REWRITE/NO_CHANGE，
机械收尾却声称沿用同一 Voice，这是实用性 false assurance。

v15 将 plan 升为 `humanize-second-pass-plan/v3`。每个 sealed input 都是严格对象：

```json
{
  "schema_version": "humanize-second-pass-generation-input/v1",
  "chunk": {"unit_id": "...", "voice_profile_sha256": "..."},
  "voice_profile": {"profile_kind": "PERSONAL", "features": [], "claims": {}}
}
```

实际对象包含完整已验证 Profile；这里的示意省略字段。PERSONAL Profile 只带抽象 features、负控、
policy binding 与 false claims，不带作者原始样本文本。plan 同时绑定 `chunk_file_sha256`、
`case_input_sha256`、`voice_context_sha256`、public manifest 和 seal。verifier 从第二遍冻结 Profile
重建 generation input，逐字节比较，不信任 plan 自述。

第二个工程修复是分块漂移：第一遍合法压缩可能让两个相邻 GENERAL unit 在第二遍合成一个。
旧 verifier 要求 unit 数和 ordinal 一一相等，会把预算布局变化误判成 Voice 漂移。现在按文件比较
相邻的 `scene + document prior + routing decision + policy + Voice` 运行段：同场景纯拆分/合并
允许，跨场景次序、policy 或 Voice 变化仍硬失败。

第三个修复是 include seed：second prepare 仍校验第一遍全部 rendered manifest，但只把原
`relation=seed` 的文件交给 prepare，子文件由 `\input/\include/\subfile` 重新发现。多文件 AUTO
的逻辑 prior 因而能跨两遍保持。

### 19.6 资格矩阵扩为 176 原子

本轮新增七个不可缩水原子：

- `ROLE-10`：MODEL_GENERATED 不能成为正向 action/Voice/真人范文；
- `ROUTE-13`：共享标题 false route；
- `ROUTE-14`：逻辑 include prior 只补同场景弱证据；
- `VOICE-13`：Profile set/entry/metadata claims 越权；
- `VOICE-14`：逐 unit、跨场景 Voice hash；
- `LONG-18`：当前 policy、冻结 source、include、metadata 独立重建；
- `LONG-19`：fresh case Profile 可见、样本文本不泄漏、同场景分块漂移。

固定 requirements 为 `2.0.0`，contract 为 `2026-07-16.6`。无 evidence manifest 的正式审计结果
仍是：`evidence_integrity_status=PASS`、`qualification_status=NOT_EVALUATED`、
`atoms_pass=0`、`atoms_fail=0`、`atoms_not_evaluated=176`、exit 2。这里的 PASS 只属于“空证据被
诚实识别”，不是生成模型通过。

### 19.7 真实 TeX prepare 审计

三份用户指定材料只执行 prepare，没有把 GPT 文本写回、没有生成正向 action：

| 材料 | 文件/单元 | 可编辑/保护 | AUTO 场景 | 状态 |
|---|---:|---:|---|---|
| 微信 GPT `main.tex` | 1 / 36 | 28 unit / 821 spans | GENERAL 3、MODELING 25；23 ROUTED、2 prior、3 fallback | `READY`，routing PASS |
| `physics1.tex` | 1 / 60 | 49 unit / 3164 spans | COURSE 40、GENERAL 10；1 个 COURSE/MODELING 强歧义 | `REVIEW`，1 UNRESOLVED |
| CET6 GPT `test.tex` | 1 / 26 | 10 unit / 643 spans | GENERAL 10，全部 fallback | `READY`，routing PASS |

`physics1.tex` 的 `刚体力学 / 刚体与定轴转动` 单元同时出现 COURSE 与 MODELING 强信号，工具没有
用文件名或 prior 偷选，而是保留 `AMBIGUOUS/UNRESOLVED`。这比“全部自动路由成功”更可信。

### 19.8 v15 可复核机器快照

- 全量 unittest：`Ran 453 tests in 51.061s`，`OK (skipped=1)`；
- Skill Python：18 个，`py_compile=PASS`，全部 `--help=PASS`；
- 官方 quick validation：显式 `PYTHONUTF8=1` 后 `Skill is valid!`；
- action profile：41 AVAILABLE、0 UNAVAILABLE、23 READABLE、3 EXCLUDED_CONFIG；
- generator projection：30 文件，两次独立构建的 manifest 与 tree 完全相同；
- capability source SHA-256：`775df5afe709f00c06065f32668d0dc53b5a74cd6b04ecc938e657ed3351c123`；
- projection manifest SHA-256：`5f9fc7e3a349c0d7ab475e628a90392c7066d615cba04ba0e9c28769aa779d3d`；
- projection tree SHA-256：`ab0d1b194f85d7eb16458a3279cbcb194728ce9cdf089bcf982177b6b5dcdc5e`；
- contract SHA-256：`113e9187a84a013228b16ee681db1d8f1ab0a443d6088e981f085c144039b8ef`；
- requirements SHA-256：`040026c59c6b27f5f4031e23338a6503b653c50f0669b31c79f7d02d52ecedf3`；
- oracle SHA-256：`8d0c837209c87332d948758edcaaaa900df4195823ad7c1c5a06b081566f1d0a`；
- qualification：`integrity=PASS / NOT_EVALUATED / 0 of 176`。

工件：[projection A](build/generator-projection-maturity-v15-a-20260716-manifest.json)、
[projection B](build/generator-projection-maturity-v15-b-20260716-manifest.json)、
[qualification](build/qualification-maturity-v15-20260716-no-manifest.json)、
[action profile](build/maturity-v15-action-profile-20260716.json)、
[main AUTO](build/maturity-v15-real-main-auto-20260716/run_metadata.json)、
[physics AUTO](build/maturity-v15-real-physics-auto-20260716/run_metadata.json) 和
[CET6 AUTO](build/maturity-v15-real-cet6-auto-20260716/run_metadata.json)。

### 19.9 当前成熟度结论

v15 可以称为成熟的**确定性中文学术文风终审工具链**：它能固定输入、保护硬不变量、按 unit
路由、绑定 Voice、拒绝常见重封与伪完成态，并且对未决返回 REVIEW。它仍不能称为已经完成
生产资格的**生成模型**，原因有四项且不可用测试数量覆盖：

1. 176 个真实 blind-forward/E4 原子仍为 0/176；
2. RESEARCH、GENERAL、REPORT 缺少合格正向人类语料，只能诚实使用 NONE；
3. 本地 runner 只有 E2，没有宿主排除根不可达、完整 generator context 和外部签名信任根；
4. 本轮没有运行真实 Codex fresh campaign，fake runner 只证明控制面合同。

因此当前准确说法是：工具链的拒错能力和审计成熟度已显著提高，常规生产改写可使用，但每次
正文仍须经过实际 validator/finalizer；不能宣称“模型已经稳定学会真人文风”或“全文必然无 AI
味”。

## 20. 第十六轮：把“人工读过”与“人写来源”彻底拆开

### 20.1 v15 仍然留下了什么来源越权

v15 已把用户明确标注的 GPT `main.tex` 和 CET6 TeX 从正向语料移出，但继续审计时发现，
`build_humanize_action_profile.py` 只禁止 `MODEL_GENERATED` 成为
`positive_action_reference`。这仍然放过两类材料：

- `MODEL_ORIGIN_UNRESOLVED`：路径层有 assistant-output 证据，但句级归属未建立；
- `UNKNOWN`：材料经过独立评估代理阅读和动作蒸馏，但没有证据证明正文由人创作。

旧构建器只要看到来源可读、登记行非空，就把卡标为 `AVAILABLE`；场景支持只统计来源或
composition family 数量，不要求 `HUMAN_CONFIRMED`。`origin_assurance=UNRESOLVED_PRESENT`
只是一个旁路说明，不会改变 `SUPPORTED`。候选门又规定 `SUPPORTED` 场景不能使用
`corpus_action_support=NONE`，因此 UNKNOWN 卡可以进入 accepted 队列。这不是措辞不严谨，而是
真实的 fail-open 路径。

独立来源审计在不知道预定修复方案的情况下重新数了一遍 catalog，得到相同结论：旧 31 张正向
卡中，人类创作来源证据为 0；8 个 `UNKNOWN` 来源支撑 17 张卡，3 个
`MODEL_ORIGIN_UNRESOLVED` 来源支撑 14 张卡。“Manually audited”只能证明有人看过，不能证明
原文由人创作。

### 20.2 被撤销的 14 张正向卡

三份来源现在保留 ID、路径、provenance 和排除理由，但 role 改为
`origin_unresolved_excluded`。构建器不打开这些文件，复制检查也不把它们重新纳入：

| 来源 | 撤销卡数 | 撤销动作 |
|---|---:|---|
| `SOURCE-MODELING-METHOD-SECTION` | 1 | `MODELING-METHOD-BOUNDARY-01` |
| `SOURCE-MODELING-PAPER-MAIN` | 7 | data role、identifiability、handoff、controlled contrast、trajectory classification、process/outcome、explanation boundary |
| `SOURCE-MODELING-PAPER-CN` | 6 | intervention isolation、proxy fallback、endpoint/trajectory、budget comparison、negative control、backend boundary |

被删除的完整 ID 为：

1. `MODELING-METHOD-BOUNDARY-01`；
2. `MODELING-DATA-ROLE-01`；
3. `MODELING-IDENTIFIABILITY-01`；
4. `MODELING-UPSTREAM-HANDOFF-01`；
5. `MODELING-CONTROLLED-CONTRAST-01`；
6. `MODELING-TRAJECTORY-CLASSIFICATION-01`；
7. `MODELING-PROCESS-OUTCOME-SEPARATION-01`；
8. `MODELING-EXPLANATION-BOUNDARY-01`；
9. `MODELING-INTERVENTION-ISOLATION-01`；
10. `MODELING-PROXY-FALLBACK-01`；
11. `MODELING-ENDPOINT-TRAJECTORY-01`；
12. `MODELING-BUDGET-COMPARISON-01`；
13. `MODELING-NEGATIVE-CONTROL-01`；
14. `MODELING-BACKEND-BOUNDARY-01`。

删除卡不等于否定这些抽象动作在写作上可能有用；它只表示当前材料不足以给这些动作贴上
“人类正向语料支撑”的标签。以后若有真正独立的 `HUMAN_CONFIRMED` 材料，可以重新建立新卡，
但不能沿用旧来源身份或旧 profile。

### 20.3 新的来源允许列表与卡级标记

构建器不再采用“只禁止已知坏来源”的黑名单，而是把正向来源收窄为允许列表：

| `origin_class` | 可否登记正向卡 | 卡级 assurance | 场景作用 |
|---|---|---|---|
| `HUMAN_CONFIRMED` | 可以 | `PRODUCTION` | 达到独立来源门槛后计入 `SUPPORTED` |
| `UNKNOWN` | 可以，但只作临时组织参考 | `PROVISIONAL` | 达到数量门槛也只能 `SUPPORTED_PROVISIONAL` |
| `MODEL_GENERATED` | 不可以 | 仅 `NEGATIVE_ONLY` | 带 detector 的负例或审计 |
| `MODEL_ORIGIN_UNRESOLVED` | 不可以 | 排除或 `NEGATIVE_ONLY` | 不读取正向排除项；带 detector 的负例可保留 |
| `OCR_INHERITED` | 不可以 | 负例/保护角色 | 不作人类散文依据 |
| `THIRD_PARTY` | 不可以 | 负例/审计 | 不作作者正向语料 |

`HUMAN_CONFIRMED` 也不是外部身份签名。它只表示当前来源台账明确记录“由人创作”，使该来源有
资格参与动作支持计算；它不证明 PERSONAL Voice、具体作者身份、事实正确、学术质量或复制许可。

每张 profile 卡现在输出 `source_origin_classes` 和 `origin_assurance`。这样即使未来一个场景同时
存在 production 与 provisional 卡，候选门仍能按选中的具体卡裁决，不会让 UNKNOWN 卡借场景的
总体 `SUPPORTED` 状态进入 PASS。

### 20.4 三态场景支持与生产路径

场景支持改成三态：

| 状态 | 成立条件 | `ACTION_CARDS` | `NONE` |
|---|---|---|---|
| `SUPPORTED` | 足量独立 `HUMAN_CONFIRMED` 正向来源 | 可继续其他门 | 不允许无理由绕开当前生产语料 |
| `SUPPORTED_PROVISIONAL` | 总来源达到门槛，但生产来源不足 | 固定 `REVIEW/2` | 允许，继续普通文风门 |
| `CORPUS_INSUFFICIENT` | 连 provisional 数量门槛也未达到 | 固定 `REVIEW/2` | 允许，继续普通文风门 |

选用 provisional 卡时结果同时记录：

```text
provisional_action_card:<card-id>
scene_corpus_origin_unresolved:<scene>
```

这两个 review 不能用空泛 KEEP 理由、调用方自称人工或旧 profile 清除。改用 `NONE` 不是绕过
公式、引语、数字、言语行为和 AI 风味门；它只表示本次组织动作不声称由语料卡支撑，后续统一
validator 仍完整运行。

当前 profile 的实际状态为：

| 场景 | 正向卡 | production 卡 | 状态 | 生产策略 |
|---|---:|---:|---|---|
| COURSE | 4 | 0 | `SUPPORTED_PROVISIONAL` | `corpus_action_support=NONE` |
| MODELING | 13 | 0 | `SUPPORTED_PROVISIONAL` | `corpus_action_support=NONE` |
| RESEARCH | 0 | 0 | `CORPUS_INSUFFICIENT` | `corpus_action_support=NONE` |
| GENERAL | 0 | 0 | `CORPUS_INSUFFICIENT` | `corpus_action_support=NONE` |
| REPORT | 0 | 0 | `CORPUS_INSUFFICIENT` | `corpus_action_support=NONE` |

因此，当前安装版没有一个 production action-card 场景。Skill 仍可按原稿、supplied content、
场景规则和 Voice Profile 执行生产改写；它只是不能再借未知来源卡增强完成声明。

后验评估进一步指出：仅要求候选包填写 `NONE`，不能证明生成器在此前没有读过 provisional 卡。
因此 generator projection 新增 strict JSON transform：完整安装版继续保留 17 张 provisional 审计卡，
生成能力面中的 catalog 则删除这些卡、对应动作描述、8 个正向来源记录和所有外部路径。当前投影
只含 10 张 negative guard、10 个本地相对 stub 来源、0 张正向卡、0 个绝对来源路径。`NONE` 仍
不能证明模型在 projection 之外的心理来源；本地 runner 的宿主隔离也仍是 UNVERIFIED，但固定
30 文件能力面不再主动把未知正向动作喂给生成器。

### 20.5 合同和红队回归

资格矩阵新增三个 P0 来源原子：

- `ROLE-11`：`HUMAN_CONFIRMED` 只有资格，不自动证明 Voice、身份、事实或复制许可；
- `ROLE-12`：`UNKNOWN` 正向卡固定 provisional，选卡候选不得 accepted；
- `ROLE-13`：`MODEL_ORIGIN_UNRESOLVED` 不得正向，排除项不得读取或用旧缓存复活。

`ROLE-10` 继续约束明确模型生成来源。矩阵从 176 扩为 179；requirements 升为 `2.2.0`，
contract 升为 `2026-07-16.8`，oracle catalog 升为 `1.3.0`。这些原子目前没有被单元测试冒充
blind-forward：正式无 manifest 审计仍为 `0 PASS / 0 FAIL / 179 NOT_EVALUATED`。

新增回归覆盖：

- `MODEL_ORIGIN_UNRESOLVED + positive_action_reference` 构建失败；
- `UNKNOWN` 卡输出 `PROVISIONAL`，场景只能 `SUPPORTED_PROVISIONAL`；
- `HUMAN_CONFIRMED` 卡才输出 `PRODUCTION`；
- provisional 卡候选进入 rejected，状态 `REVIEW/2`；
- 同一 provisional 场景使用 `NONE` 可以在风格门通过后 PASS；
- 三份来源均为 `EXCLUDED_CONFIG + origin_unresolved_excluded`；
- 旧 14 张卡不再出现在 catalog、profile 或场景指南；
- generator projection 中 17 张 provisional 卡、其动作描述和外部来源路径全部消失；
- 任意外部 `--catalog` 固定 `EXTERNAL_UNVERIFIED`，自填 `HUMAN_CONFIRMED` 的选卡候选保持
  `REVIEW/2`，不得 accepted；
- Windows 新 queue 在约 294 字符 history 目的路径上的 `FileNotFoundError` 已真实复现；候选 ID
  与嵌套 artifact/evaluation/run 使用短存储键，文件内容仍保留完整哈希并由 immutable conflict
  防覆盖，长路径回归现可发布；
- capability 内容变化而 policy 未批准时，资格审计整批 fail-closed；批准新 hash 后才能恢复。

第一次独立候选门代理因外部安全过滤没有产生有效结果，本报告没有把它写成“已通过”。后续使用
不泄漏预期答案的中性后验任务重新运行，代理用六类 origin 临时矩阵确认 UNKNOWN 选卡为 REVIEW、
外部自填 HUMAN 原先可 PASS，并复现 Windows queue 发布失败。主流程没有把两项写成局限后结束，
而是加入 projection filter、external catalog review 和长路径发布回归。来源审计代理的 0/31
人类来源判断也与主流程独立一致。

### 20.6 v16 可复核机器快照

- 全量 unittest：`Ran 461 tests in 66.370s`，`OK (skipped=1)`；
- 唯一跳过：当前 Windows 账户无创建 symlink 权限；
- Skill Python：18 个，`py_compile=PASS`，全部 `--help=PASS`；
- 官方 quick validation：`Skill is valid!`；
- action profile：26 个来源，20 READABLE、6 EXCLUDED_CONFIG；27 张 AVAILABLE、0
  UNAVAILABLE；17 张 provisional 正向卡、0 张 production 正向卡、10 张 negative guard；
- 两次最终 projection：30 文件，capability、manifest 和 tree 完全相同；
- projected catalog：10 张 negative guard、0 张正向卡、0 个绝对/外部来源路径；
- capability source SHA-256：`eb4560b1142eff5bd927ac83ce3f2231c84438f1e23752ec816c6c0f01c2b651`；
- projection manifest SHA-256：`06afd012bcc5e34b091a3a7ac1a0c2e4ebead53cdf427a6f696208a1e4f94096`；
- projection tree SHA-256：`f21858bbc040ef26e304364a64d88affb2965091a697d7d1c01388cd99be1360`；
- contract SHA-256：`6e89bc3cf4ae1889916f53f0ed9065c5500b6ee532d1fed1b68ae962ebb0f0b5`；
- requirements SHA-256：`8b38fcde6e4dc75cb38c62549d759cb21452fe95cbe6daf33d9818c0b0f54ce5`；
- oracle SHA-256：`672a3dfac7d02b9ff2991e7923c267edc1fbf3c00c9495af484f328fa8470015`；
- qualification：`integrity=PASS / qualification=NOT_EVALUATED / 0 of 179 / exit 2`。

工件：[final projection](build/generator-projection-maturity-v16-final-20260716-manifest.json)、
[repro projection](build/generator-projection-maturity-v16-repro-20260716-manifest.json)、
[qualification](build/qualification-maturity-v16-20260716-no-manifest.json) 和
[action profile](build/maturity-v16-action-profile-20260716.json)。

### 20.7 v16 后的成熟度结论

v16 提高的不是“生成更像人”的主观分数，而是正向学习材料的可信边界。当前 Skill 可以继续
称为成熟的确定性终审、保护、路由、Voice 绑定和拒错工具链；它比 v15 更少依赖来源卡，但不再
把未知来源包装成人类表达证据。

生成模型仍不能称为生产资格通过：179 个真实 E3/E4 原子仍为 0/179，当前没有 production
action-card 场景，本地 runner 仍只有 E2，也没有代理不可访问私钥的外部身份和隔离信任根。
生产任务可以使用 Skill 的 `NONE + validator/finalizer` 路径；不能声称“模型已经从人类语料学会
稳定去 AI 味”，也不能把 provisional 卡数量、461 项单元测试或 projection 可复现性改写成这一
结论。

## 21. 第十七轮：本地来源声明不再等于 production 信任

### 21.1 触发本轮的两个真实 fail-open

v16 已把当前 catalog 的 production 卡降为 0，但后验红队证明这只是“当前数据没有触发”，并非
合同层不可触发。旧实现存在两条本地主体可控路径：

1. `build_humanize_action_profile.py` 只要看到 `origin_class=HUMAN_CONFIRMED`，就直接把正向卡写成
   `origin_assurance=PRODUCTION`；`provenance/source_tier/use_limit` 都是未验证字符串。
2. 候选门以 `catalog_path == DEFAULT_CATALOG` 判定 `INSTALLED_DEFAULT`。测试和本地主体都能重绑或
   修改默认 catalog；同一主体还可以修改 projection approval hash。临时复现确实得到
   `PASS + accepted=true + PRODUCTION`，并非理论风险。

另一个独立性漏洞是：缺少 `composition_family_id` 时，旧 profile 以 source ID 计独立来源。同一
文件复制成两个 ID，GENERAL 就能伪造两个独立来源。v17 不再用“当前恰好没有 HUMAN 卡”掩盖这些
路径，而是让本地工具根本没有 production promotion 能力。

### 21.2 固定来源信任矩阵

新增 [source-provenance-trust.json](C:/Users/Lenovo/.codex/skills/humanize-academic-chinese/references/source-provenance-trust.json)。
当前 policy 固定 `production_attestation.enabled=false`、`accepted_schemes=[]`、
`external_verifier_required=true`、`local_claims_are_identity_proof=false`。其裁决为：

| origin class | production positive | assurance | 允许用途 | 理由码 |
|---|---|---|---|---|
| `HUMAN_CONFIRMED` | false | `PROVISIONAL` | audit / experimental positive review | `EXTERNAL_ATTESTATION_REQUIRED` |
| `UNKNOWN` | false | `PROVISIONAL` | audit / experimental positive review | `ORIGIN_UNKNOWN` |
| `MODEL_GENERATED` | false | `NEGATIVE_ONLY` | audit / negative guard | `MODEL_TEXT_NEGATIVE_ONLY` |
| `MODEL_ORIGIN_UNRESOLVED` | false | `NEGATIVE_ONLY` | audit / negative guard | `MODEL_ORIGIN_UNRESOLVED_NEGATIVE_ONLY` |
| `OCR_INHERITED` | false | `NEGATIVE_ONLY` | audit | `OCR_PROVENANCE_NOT_AUTHOR_VOICE` |
| `THIRD_PARTY` | false | `NEGATIVE_ONLY` | audit | `THIRD_PARTY_NOT_AUTHOR_VOICE` |

builder 与 hidden auditor 分别维护同一固定矩阵并独立校验 JSON。修改 policy 试图打开 production、
添加 `CALLER_JSON` scheme、在 source 中自填 `origin_attestation`，都会直接构建失败。这里没有宣称
已经实现外部信任根；相反，production 路径明确为 unavailable。以后若要开放，必须新增真正的
外部 verifier 和代理不可访问的私钥链，不能只改本地 JSON。

独立来源计数也改成 fail-closed：显式 family 相同算一个；没有 family 时，相同内容 SHA-256 算
一个；内容不可得时才退到规范化路径。当前 MODELING 的 6 个 provisional source ID 因 family/
内容去重只计 4 个独立单元，复制 ID 不再增加门槛计数。

### 21.3 production surface 与 audit surface 物理拆分

v16 projection 虽然没有正向卡，仍暴露候选包、warning proposal、accepted/rejected queue、来源
tier 和 provenance 台账。v17 把以下内容移出 generator projection：

- `prepare_humanize_candidate_revision.py`；
- `validate_humanize_candidate_queue.py`；
- `SKILL.md` 的“来源动作候选审计”路由和整个候选入队章节；
- 全部 positive action、动作描述、正向 source record 和外部来源路径；
- negative source 的原始 `source_tier/provenance/use_limit`。

长文 finalizer 仍需要 negative detector，因此投影保留 `build_humanize_action_profile.py`、固定来源
policy 和经过变换的 detector-only catalog。该 catalog 只有 10 张 negative guard、10 个最小
stub source；source tier 固定为 `DETECTOR_ONLY`，path 固定为投影内相对文件。它不含 positive
card、候选队列或外部绝对路径。能力面由 30 文件减为 29 文件，其中 25 个原样能力文件、4 个
确定性 transform 文件。

两次正式构建得到相同 manifest 字节和 tree：

- capability source SHA-256：`8287b1cc815e0fc6d978ee95bd04a27d084ec5c01a5aa2d756b40b53a7cfbde6`；
- projection manifest SHA-256：`e3550669d5ed24e6829de3813f018380435372ed69ae242db780cf31bf990f61`；
- projection tree SHA-256：`0a44307a7602f982f375bdfd3e209732250c3c6f3c12de48b82e555bf96c30b9`；
- `declared_external_capability_refs=[]`；
- projected positive card 0、negative guard 10、候选脚本 0。

旧 v10-v15 projection 目录仍作为历史工件保存在 `build/`，其中若干旧 catalog 含绝对路径。本轮
没有删除历史证据，也没有把它们描述成安全缓存。当前 runner 只重建并绑定 v17 tree；由于宿主
文件系统隔离仍未证明，报告继续明确：clean projection 不等于旧目录或 oracle 对进程不可达。

### 21.4 `ROLE-10` 至 `ROLE-13` 从合同原子变成可运行 suite

v16 虽有 179 原子，但 oracle catalog 只有 5 个 SHADOW suite，`ROLE-10` 至 `ROLE-13` 没有
fixture、check 或 fresh 入口。v17 将 oracle schema 升到 v2，新增 4 个
`FRESH_FORWARD/runner_compatible=true` suite：

- public input 只给中性 source record、origin class、请求角色和 `attestation=ABSENT`；
- public prompt 只要求固定 JSON 字段，不出现 ROLE ID、assurance、理由码或预期答案；
- public context 使用 `operation=CLASSIFY_SOURCE_PROVENANCE`；
- hidden check 从固定 source policy 计算完整期望，再严格比较 output JSON；
- current manifest 仍只能提交 `claim_id/atom_id/oracle_suite_id`，不能自选 expected/check。

一个自报 `HUMAN_CONFIRMED + PRODUCTION + production_positive=true` 的候选在隐藏 check 中固定
`FAIL`。四种正确裁决在确定性 E2 测试中 check 均为 PASS，但 ROLE 原子要求 E3，所以 claim 仍是
`NOT_EVALUATED`。这一区分防止“hidden check 会判分”被写成“生成模型已通过”。catalog 当前为
9 个 suite、15 个 machine check、1 个 rubric；contract 为 `2026-07-16.9`，requirements 为
`2.3.0`，oracle catalog 为 `1.4.0`。

### 21.5 真实 fresh runner 结果没有被美化

四个 public case 已实际封存。并行 fresh campaign 在 244 秒外层时限被终止；随后单例重跑在
300 秒内仍不返回。最后用 runner 自身 `--timeout 60` 对最危险的 `HUMAN_CONFIRMED` case 留下
明确 receipt：

- `runner_status=INFRA_INVALID`；
- `timed_out=true`；
- `output_present=false`；
- `projection_audit_status=NOT_COMPLETED`；
- 新进程已观察到，但没有 provider request/response ID；
- 当前 run 的 `evidence_attained=E0`，本地 runner 的能力上限仍为 `evidence_cap=E2`。

因此本轮没有 fresh 行为 PASS/FAIL，只有基础设施无效证据。CLI 已修正失败输出，不再把 E0
attained 与 E2 cap 混成同一个 `evidence_cap=E0` 字段。receipt 位于
`build/maturity-v17-source-forward-20260716/runs-timeout-evidence/source-b/runner-receipt.json`。

### 21.6 v17 回归与机器快照

- 全量 unittest：`Ran 468 tests in 69.759s`，`OK (skipped=1)`；
- 唯一跳过：当前 Windows 账户无创建 symlink 权限；
- 18 个 Skill Python 脚本：`py_compile=PASS`、全部 `--help=PASS`；
- `quick_validate.py`：`Skill is valid!`（Windows 下用 `python -X utf8`，避免系统 GBK 误读）；
- action profile：26 个来源，20 READABLE、6 EXCLUDED_CONFIG；27 张 AVAILABLE、0 UNAVAILABLE；
  17 provisional positive、0 production positive、10 negative guard；
- scene：COURSE 2 个独立 provisional source，MODELING 4 个，二者均
  `SUPPORTED_PROVISIONAL`；RESEARCH/GENERAL/REPORT 为 `CORPUS_INSUFFICIENT`；
- qualification：`evidence_integrity_status=PASS`、`qualification_status=NOT_EVALUATED`、
  `0 PASS / 0 FAIL / 179 NOT_EVALUATED`、exit 2；
- contract SHA-256：`1f9222e3395c4099b373f60c36070e2d2ed1bb04eab4a547369de8295573ea82`；
- requirements SHA-256：`34eed975c63006ff88e818e6edaf329357faa00240517cd4d069ce4f6c4b378a`；
- oracle SHA-256：`249d429d58fb13d57d3f20dc412a7073782542fbdb23a2f781727b2a2270f168`；
- source trust policy SHA-256：`4d0c6f9e5cd301088af56b10e5414c327cba6f6cb9a4116f5d6f04cdf2857607`。

正式工件：[action profile](build/maturity-v17-action-profile-20260716.json)、
[stable projection](build/generator-projection-maturity-v17-stable-20260716-manifest.json)、
[stable repro projection](build/generator-projection-maturity-v17-stable-repro-20260716-manifest.json)、
[qualification](build/qualification-maturity-v17-stable-20260716-no-manifest.json) 和
[fresh timeout evidence](build/maturity-v17-source-forward-20260716/runs-timeout-evidence/source-b/runner-receipt.json)。

### 21.7 当前成熟度裁决

v17 关闭了“本地 HUMAN 字段即可升 production”“默认路径即可信”“复制 source ID 制造独立来源”
三类来源信任假闭环，并把候选审计面从正常生成能力面移除。确定性终审、保护、路由、Voice 绑定、
长文发布和拒错工具链继续可用于生产；来源动作卡现在明确只是 audit/provisional 资产。

仍不能声称 Skill 的生成模型已经成熟到一次生成稳定合格：外部来源 attestation 尚未实现，179 个
E3/E4 原子仍为 0/179，宿主 oracle/旧 projection 不可达性未证明，本轮真实 fresh runner 也没有
产生 output。当前准确说法是：**生产文风门更难被伪造，production generator surface 更小，来源
资格更诚实；生成能力资格仍未完成。**

## 22. 第十八轮：detector-only 运行时、来源负例权限与 runner 诊断

### 22.1 本轮删除了不该存在的生产能力

v17 声称 generator projection “只保留 negative detector registry”，实际却仍携带完整
`build_humanize_action_profile.py`。负例卡也仍有 `action/requires/forbids`、来源行号、来源角色和
stub source record。finalizer 的真实依赖只有 guard 的 `id/scene/status/detector`，其中 `status`
还可以由 strict loader 派生。

v18 新增 `scripts/load_humanize_negative_guards.py`，把生产数据合同固定为：

```text
humanize-negative-guard-registry/v1
  registry_id
  guards[]
    id
    scene
    detector
      minimum_groups
      pattern_groups[]
        id
        regex
        minimum_occurrences
```

持久化 registry 不再含 `sources/source_refs/origin_class/source_tier/path/action/requires/forbids`。
finalizer 直接 import 这个 loader；完整 action-profile builder 只留在安装版来源/候选审计面，
不再进入 generator projection。兼容字段 `action_catalog_sha256/action_profile_sha256` 暂时保留，
但现在分别绑定 registry 原始字节与 canonical detector registry，不再暗示正向动作可执行。

### 22.2 红队发现 negative guard 绕过了来源信任矩阵

后验审计逐张反查当前 10 张负例卡的来源类别。v17 policy 只允许 `MODEL_GENERATED` 与
`MODEL_ORIGIN_UNRESOLVED` 使用 `NEGATIVE_GUARD`，代码却把以下 6 张无此权限的卡全部标为
`AVAILABLE` 并送入投影：

- `NEGATIVE-MODELING-README-SHELL-01`：`UNKNOWN`；
- `GENERAL-NEG-GOVERNANCE-VOICE`：`UNKNOWN`；
- `GENERAL-NEG-RESEARCH-JOURNAL-OVERFIT`：`UNKNOWN`；
- `GENERAL-NEG-OPINION-AS-EVIDENCE`：`THIRD_PARTY`；
- `GENERAL-NEG-OCR-AND-TEXTBOOK`：`OCR_INHERITED`；
- `GENERAL-NEG-API-TEMPLATE`：`UNKNOWN`。

这不是命名瑕疵。`THIRD_PARTY/OCR_INHERITED` 在固定 policy 中只允许 `AUDIT`；`UNKNOWN` 只允许
`AUDIT/EXPERIMENTAL_POSITIVE_REVIEW`。让这些卡进入 production finalizer，相当于把“可观察”
扩大成“可拦截”。v17 的 ROLE fresh fixture 又只测试 `positive_action_reference`，测不到这条旁路。

v18 在三个位置同时修复：

1. 完整 builder 按固定 `allowed_uses` 计算 `negative_guard_runtime_authorized`；无权限卡变为
   `AUDIT_ONLY`，不会伪装成普通 `UNAVAILABLE`。
2. candidate queue 自动扫描跳过 `AUDIT_ONLY`；只有明确获权且 `AVAILABLE` 的卡执行。
3. projection transform 使用同一冻结 trust policy 过滤；本地给 `UNKNOWN/THIRD_PARTY` 追加
   `NEGATIVE_GUARD` 会因整张决策矩阵漂移而构建失败。

修复后的完整安装版为 17 张 provisional positive、4 张 runtime negative guard、6 张 audit-only
negative definition；production positive 仍为 0。四张 runtime guard 分别覆盖
`ALL/GENERAL/MODELING/RESEARCH`，来源均为明确模型文本或模型来源未解析文本。

### 22.3 strict loader 的拒错面

以下输入全部抛出 `NegativeGuardRegistryError`：

- 非 UTF-8、重复 JSON key、NaN/Infinity、顶层或 guard 未知字段；
- 空 guard 集、重复 guard ID、非法 scene；
- detector 缺组、`minimum_groups` 越界、重复 group ID；
- regex 不可编译或异常过长；
- `minimum_occurrences` 为布尔值、非正整数或异常过大；
- 完整 catalog 缺冻结 trust policy、来源 ID 重复、source ref 悬空；
- trust policy 版本、attestation 关闭状态或任一 origin decision 与固定矩阵不一致。

registry 缺失或非法时，跨 unit 门输出
`NEGATIVE_GUARD_REGISTRY_UNAVAILABLE:<ErrorType>`，状态固定为 `REVIEW`，不得按空 guard 集合
继续 PASS。结果同时保存原始 registry hash、canonical registry hash、loader 版本、来源格式、
逐 detector definition hash 和 finding fingerprint。

### 22.4 projection 的实际最小面

最终 generator projection 仍为 29 文件，但发生了能力替换：

- 新增 `load_humanize_negative_guards.py`；
- 删除 `build_humanize_action_profile.py`；
- `corpus-action-sources.json` 变为 `humanize-negative-guard-registry/v1`；
- 顶层字段严格只有 `guards/registry_id/schema_version`；
- 每张 guard 严格只有 `detector/id/scene`；
- guard 数由 v17 的 10 张降为 policy 真正授权的 4 张；
- `source-provenance-trust.json` 仍供来源分类，但 finalizer 不解析正向卡或来源台账。

两次最终构建完全一致：

- capability source：`dea6d198581bbb6870ae97b6d9d8fe89b0f8cc7970eaf2da1aec4b9df152a909`；
- manifest：`1328011e86a51e78875da900d1733b1e1380e15d31259999dbd0ed4c9d6f4c6a`；
- tree：`42eacd2c9c52f1e75305d7958d0197f3aeed3baa099f081fcd977876135db9b1`；
- 文件数：29；builder absent、loader present、4 guards、0 positive card。

### 22.5 v17 fresh timeout 的可证结论

对 v17 `source-b` 的原始 events、receipt、prompt 和进程信息复核后，只能得到基础设施结论：

- public case、seal、projection 和 preflight 已完成；
- CLI 出现 `thread.started` 与 `turn.started`；
- 随后出现 `Reconnecting... 2/5 (request timed out)`；
- 60 秒外层时限终止进程树；
- 没有 provider request/response ID、没有 output、没有 post-run projection audit；
- prompt 仅 814 字节，没有证据表明任务内容触发拒绝；
- 当时 runner 源码没有随 receipt 封存，当前源码不能冒充当时 executable 的逐字快照。

所以 `returncode=1` 不能写成模型行为 FAIL，Skill budget warning 也不能当终止错误。准确状态仍是
`INFRA_INVALID / INVOCATION_TRANSPORT / WAITING_PROVIDER_RESPONSE / E0`，模型行为未评估。

### 22.6 runner 1.2 的观察工件

本轮没有自动重放真实请求，以免重复计费和破坏 fresh-run 独立性。runner 1.2 在以后运行中新增：

- `request/invocation.json`：sanitized argv、runner 源码 hash、CLI hash/version、实际 timeout、
  900 秒资格最低时限、运行用途、`NO_AUTOMATIC_RETRY`；
- `transcript/observation.json`：started/deadline/ended、return code、终止方式、事件类型计数、
  reconnect 次数、最后事件、输出状态、失败域/阶段、`model_behavior_evaluated` 与 attained evidence。

两份工件与 `request/runner-source.py` 都由 receipt 绑定 SHA-256。`--timeout < 900` 固定为
`DIAGNOSTIC_SHORT_TIMEOUT`，不能进入资格。默认 900 秒只满足时限条件，不自动形成 E3。
当前事件捕获仍是 `BUFFERED_AFTER_PROCESS_EXIT`，没有逐事件接收时间或 heartbeat；报告明确保留
这一观察盲区，没有写成“已实现实时流式监控”。

second-pass verifier 已同步要求这些活工件、E2 observation、runner source snapshot 与 receipt hash
一致。缺失、篡改、短时限、自动重试声明或 runner 漂移都会使收敛验证失败。

### 22.7 资格合同与状态

隐藏资格绑定更新为：

- contract：`2026-07-16.10`，SHA-256
  `01294a453adad871ee954e006e3eab78dc94b86686992cf1ddd9973ba6495b56`；
- requirements：`2.4.0`，SHA-256
  `b84891e849116de73ed4554d85ccf8ce1e211c2f5ae0026f78e2bb07fcb3f51d`；
- oracle catalog：`1.5.0`，SHA-256
  `ae3488b58884db141bd4eab662989f7bc84e496f6bc1bce56517776434ffcd01`。

无 manifest 的正式审计仍是
`integrity=PASS / qualification=NOT_EVALUATED / 0 PASS / 0 FAIL / 179 NOT_EVALUATED / exit 2`。
本轮没有把 deterministic loader tests、projection build 或 timeout classification 填进 179 个 E3/E4
行为原子，也没有把旧 timeout 重解释成 ROLE suite 结果。

### 22.8 回归与正式工件

- 全量：`Ran 481 tests in 56.612s`，`OK (skipped=1)`；
- 跳过项：当前 Windows 账户无 symlink 创建权限；
- 19 个脚本：`py_compile=PASS`、`--help=PASS`；
- `quick_validate.py`：`Skill is valid!`；
- action profile：21 AVAILABLE、6 AUDIT_ONLY、0 UNAVAILABLE；17 provisional positive、
  0 production positive、4 runtime guard、6 audit-only guard；
- action profile SHA-256：`6cabef43e3ea7157cba4ae307251c60a936737e9f85c82aae45e44d63d710f3a`；
- qualification report SHA-256：`4477dcea55d6550e6b095e48f5b034dc592e9424e7a78473f1af33b813835bc0`。

正式工件：

- [v18 action profile](build/maturity-v18-action-profile-20260716.json)
- [v18 final projection](build/generator-projection-maturity-v18-final-20260716-manifest.json)
- [v18 final repro projection](build/generator-projection-maturity-v18-final-repro-20260716-manifest.json)
- [v18 qualification](build/qualification-maturity-v18-final-20260716-no-manifest.json)
- [v17 timeout evidence](build/maturity-v17-source-forward-20260716/runs-timeout-evidence/source-b/runner-receipt.json)

### 22.9 当前成熟度裁决

v18 关闭了两个让“最小生产面”名不副实的漏洞：完整正向 action builder 不再进入生成面；来源
policy 也不再只约束正向卡而放任负例卡。现在可证的是：detector 运行时字段足够小、来源权限在
builder/loader/projection/candidate/finalizer 多层一致、registry 故障会拒绝错误完成态、timeout 不会
冒充模型失败。

仍不能称为成熟的“生成模型”：真实 fresh output 本轮为零，179 个行为原子仍未评估，宿主排除根
不可达性未证明，外部 human attestation 不存在，事件流也没有逐事件时间戳。当前准确定位是：
**确定性纯文风终审与长文拒错工具链更接近生产稳定；生成器本身仍未取得前向资格。**

## 23. v19：用真实成对质量替代“删词即完成”

### 23.1 为什么继续迭代

v18 解决了来源权限和最小生产面，却没有回答普通调用最实际的问题：validator `PASS/0` 的稿子，
是否真的比原文自然。v19 从真实 TeX 片段建立三个不泄漏答案的 fresh case：惠更斯原理课程讲解、
珍稀物种建模说明、四大家鱼校准与 CPUE 研究讨论。三份输入均只作为 GPT 风味负例，不作为真人
正向范文或 PERSONAL Voice。

首轮三个生成候选全部得到旧 validator `PASS/0`，独立盲评却给出不同结论：

| 场景 | 旧候选盲评 | 自然度/忠实度 | 暴露的问题 |
|---|---|---|---|
| COURSE | 偏好 B，可交付 | B 8.8，忠实度 10.0 | 收益真实但很小，“换一个角度看”略模板化 |
| MODELING | A/B 平局，不可直接交付 | B 8.3，忠实度 9.2 | 删除表格引介职责，新增主语错位和抽象路径壳 |
| RESEARCH | 偏好 A，不可直接交付 | B 7.8，忠实度 9.7 | 首句“按……闭环收紧”搭配错误，长句被机械拆平 |

这说明原门禁只证明公式、数字、TeX、显式 high 词项和已编码言语行为没有失败，不能证明病句、
段落职责和论证层级。尤其“更短、短句更多、连接词更少”不能直接等价于 Humanize 成功。

### 23.2 从失败反推的质量门

本轮没有按盲评答案逐句写死，而是补入可迁移的四层约束：

1. **段落职责不变量**：改写前内部记录段落是在定义、解释、引介图表、比较、限定还是展开并列
   分支。不能把“说明表格为何这样组织”改成另一遍结果概括。
2. **论证层级保护**：拆句先标总论、细节、排除、并列、因果和回指；不得按逗号、分号平均切割，
   也不得把“唯一硬锚点—固定初值—局地软约束”切成同构清单。
3. **成对优越性门**：validator 通过后逐段 A/B；只有至少一项具体读感收益、没有新增缺陷、职责
   与层级均保留时才接受修改，否则继续改写或恢复原段并记 `NO_CHANGE`。
4. **焦点作用域门**：`重点/主要/优先` 进入言语行为计数。把“重点不是比较”改成绝对的“不比较”
   会产生 `SPEECH_ACT_FOCUS_SCOPE_CHANGED`，交付固定为 `REVIEW/2`。

词库升级到 1.2.0：单个“实证/论证/分析闭环”和“抽象关系由 A 出发，经 B，最终落到 C”进入
`LEX-MGMT-01` high 候选；“表格的作用”从无条件编辑后台拆成 `LEX-TABLE-ROLE-01/REVIEW`，先判断
它是后台计划还是实际读者说明。控制理论闭环等正式术语继续豁免。

### 23.3 普通调用上下文瘦身

`SKILL.md` 从 443 行、24,193 字符降为 280 行、15,579 字符。资格 harness、候选 JSON、队列事务、
来源复制实现和 Voice/长文底层合同改为按任务路由到 reference；正常短文仍直接看到模式、保护、场景、
高风险词项、统一验证器和成对质量门。generator transform 继续保留原有 H2 与 second-pass marker，
没有因瘦身破坏投影确定性。

### 23.4 修复后的 fresh 前向结果

三组 case 在干净上下文中重新生成。最终候选均为真实 validator `PASS/0`，保存 JSON 与当前文件
逐字段一致。独立盲评结果为：

| 场景 | A 自然度 | B 自然度 | B 忠实度 | 偏好 | v20 历史机械交付记录 |
|---|---:|---:|---:|---|---|
| COURSE | 8.4 | 8.8 | 10.0 | B，轻微优势 | 是；不构成 v25+ clearance |
| MODELING | 7.8 | 8.8 | 9.7 | B | 是；不构成 v25+ clearance |
| RESEARCH | 7.3 | 8.7 | 9.8 | B，明确优势 | 是；不构成 v25+ clearance |

第一次 post-fix 盲评仍发现建模稿把“重点不是比较”绝对化为“不比较”。加入焦点作用域门并恢复限定
后，第二次只看最终 modeling pair 的盲评仍偏好 B：A 7.8、B 8.8、忠实度 9.7；这是 v20 历史机械记录，
不构成 v25+ 的 paired-quality clearance。
这条后验修复没有用人工理由绕过 warning，而是修改正文，使 warning 在新版本上消失。

报告仍保留残余风险：课程稿出现“不再由……而由……”的规整句式；建模稿仍有“从……推进到……”
和上游/中间/下游比喻；研究稿仍有防御性对照句。它们在当前段落承担具体功能，尚未构成阻断条件，
但跨章节复用时仍应由重复窗口拦截。

### 23.5 回归与固定工件

- 全量：`Ran 487 tests in 54.618s`，`OK (skipped=1)`；跳过项仍是 Windows symlink 权限；
- 19 个脚本：`py_compile=PASS`、`--help=PASS`；quick validation：`Skill is valid!`；
- action profile：21 AVAILABLE、6 AUDIT_ONLY、0 UNAVAILABLE；17 provisional positive、
  0 production positive、4 runtime guard、6 audit-only guard；
- capability source：`06a6ac68c880771a38662a84f311ce26b8a59c51632b96a5fe6496b9bd377143`；
- 两次 stable projection：29 文件，manifest 均为
  `3be5729fa28609ab1532b5a3bc75ca318e8cdb7e7fb2596e256b8c6f1d165719`，tree 均为
  `3a28a8caa661b33833516a1aaccde96bf96546572b2b840ff4a44f6e2982ee5e`；
- action profile SHA-256：`6cabef43e3ea7157cba4ae307251c60a936737e9f85c82aae45e44d63d710f3a`；
- qualification report SHA-256：`415666aecf906cbada0aba9566bc8360e614152e52ee3fac29ce8de97e3889f2`；
- 无 manifest 资格审计：`integrity=PASS / NOT_EVALUATED / 0 PASS / 0 FAIL / 179 NOT_EVALUATED / exit 2`。

正式工件：

- [v19 pre-fix blind review](build/maturity-v19-forward-20260717/blind-pair-evaluation.md)
- [v19 post-fix blind review](build/maturity-v19-postfix-20260717/blind-pair-evaluation.md)
- [v19 final modeling blind review](build/maturity-v19-postfix-20260717/modeling-final-blind.md)
- [v19 stable projection](build/generator-projection-maturity-v19-stable-20260717-manifest.json)
- [v19 stable repro projection](build/generator-projection-maturity-v19-stable-repro-20260717-manifest.json)
- [v19 qualification audit](build/qualification-maturity-v19-20260717-no-manifest.json)

### 23.6 当前成熟度裁决

v19 首次给出“旧候选机械 PASS、盲评失败 -> 规则修复 -> fresh 重生 -> 盲评三组全偏好 B”的完整
质量证据链。对这三类短 TeX 任务，Skill 已从只会拒错推进到能稳定改善读感，并能在盲评指出限定
漂移后新增可执行门禁。

但不能据此宣称生成器全面成熟：样本只有三个，未覆盖 GENERAL、检测报告、STRUCTURAL、真实长文
第二遍和跨学科迁移；盲评是模型评审而非外部签名人工链；179 个 E3/E4 原子仍全部未评估。当前准确
表述是：**确定性工具链可生产使用，短文 Humanize 的真实前向质量已有明显正证据；生成模型总体资格
仍为 NOT_EVALUATED。**

## 24. v20：GENERAL 克制、材料约束起草与报告范围闭环

### 24.1 为什么 v19 之后仍不够

v19 证明 COURSE、MODELING、RESEARCH 三类短 TeX 可以在修复后得到盲评偏好，但没有覆盖普通
`GENERAL`、从 supplied facts 起草的 `DRAFT`、带检测报告 selection 的 `REPORT_INFORMED`，也没有
验证“原文已足够自然时能否不改”。v20 因此从已经人工审计的真实 GPT MD/TeX 建立四个无答案泄漏
case；GPT 文本仍只作测试输入和负例，不登记为真人正向范文或 PERSONAL Voice。

| Case | 真实材料 | 模式/场景 | 隐藏验收重点 |
|---|---|---|---|
| GENERAL | `gpt_chinese_style_report_detailed.md` 的写作质量判断 | REWRITE/GENERAL | 改后须真优于原文，不做正式化轮换 |
| DRAFT | 微信 `main.tex` 问题二的公报锚点、四组情景和边界 | DRAFT/MODELING | 只用 supplied facts，内部投影不冒充外部验证 |
| REPORT_INFORMED | GENERAL 段落 + 本地 HTML 唯一 `<mark>` | REWRITE/GENERAL | 只改 UNIQUE selection，拒绝目标检测率 |
| NO_CHANGE | v19 盲评 8.8 的惠更斯课程段落 | REWRITE/COURSE | 不为显示工作量制造改动 |

输入、提示、原始输出和验证记录位于
[`maturity-v20-forward-20260717`](build/maturity-v20-forward-20260717/)。生成代理只读取当前 case 与安装版
Skill，不读取旧输出、评测或 oracle。

### 24.2 pre-fix 的三个真实缺口

第一，GENERAL 候选通过旧 validator，却在随机化盲评中失败。改后稿把自然的“造成论证前置过多”
改成“使过多论证被前置”，还执行了“让 -> 使”“好的习惯 -> 体现出良好习惯”等无病灶正式化
轮换。盲评中改后 A 为 8.3，原文 B 为 8.7；原文可直接交付，改后须先修硬被动。完整证据见
[`blind-quality-evaluation.md`](build/maturity-v20-forward-20260717/blind-quality-evaluation.md) 与
[`general-failure-redteam.md`](build/maturity-v20-forward-20260717/general-failure-redteam.md)。

第二，DRAFT 正文经独立逐句审计为 9.2/10，全部数值、物种配对和边界均受 facts 支持，验证器却
返回 `FAIL/1`。唯一错误是 `DRAFT_MATH_NOT_SUPPLIED`：facts 中 `\(R_S=0\)` 出现一次，结果段与
讨论段各使用一次；旧 `Counter` 把 supplied occurrence 当一次性额度，把第二次复述误写成“未提供”。
七类红队进一步证明 code/math/formal statement/critical command/quotation/garbled/protected term 的
repeat/new 共 14 case 旧版全部 `FAIL/1`，无法区分同值复用与异值新增。证据见
[`draft-surface-redteam.md`](build/maturity-v20-forward-20260717/draft-surface-redteam.md)。

第三，REPORT 提取器虽能把 1/1 片段唯一映射到字符 `116--281`，旧统一验证器却不消费其 JSON。
红队在 selection 外改写首段，同时改写 selection；普通 REWRITE 门仍返回 `PASS/0`。这证明“报告映射
正确”不等于“交付范围受约束”。证据见
[`report-scope-redteam.md`](build/maturity-v20-forward-20260717/report-scope-redteam.md)。

NO_CHANGE case 是本轮对照：pre-fix 代理已经逐字不改并得到 `PASS/0`，说明问题不是 Skill 完全没有
克制能力，而是 GENERAL 的准入与逐句回退不够具体。

### 24.3 三类修复

GENERAL 新增最小改写面：改写前登记病灶跨度、读感后果和允许动作；没有可定位病灶即
`NO_CHANGE`，`BALANCED` 不再被当作改动配额。每个改句必须有独立收益；“更正式/更书面”、
`让 -> 使` 和自然主动因果改成 `使/让 + 抽象对象 + 被 + 动词` 不算收益。规则不禁用合法技术
被动句，而是要求相对原文逐句成对判断；无收益句先局部恢复，整段仍不占优再全部回退。

DRAFT 的确定性表面门改为 supplied value set membership。七类载荷同值复用不再触发
`NOT_SUPPLIED`；任何从未提供的新值仍为同一错误码和 `FAIL/1`。归因 marker 继续按 occurrence
保守检查，REWRITE 的公式、引语、命令和术语次数/顺序保护完全不变。自然语言蕴含没有被脚本
伪认证：非逐字 DRAFT 仍固定 `semantic_source_check=NOT_EVALUATED`，顶层为 `REVIEW/2`。

REPORT 新增 `validate_humanize_output.py --report-scope <extractor-json>`。该门验证 extractor
`PASS/0`、schema/operation，并从 JSON 的绝对 `report_path` 重放原报告，要求 report SHA、coverage
和 fragments 逐字段一致；随后验证精确 before SHA-256、每个 fragment 的
`UNIQUE/source_occurrences/source_start/source_end/normalized_text`，再检查 after 是否能由这些
selection 的替换形成。重叠或相邻区间先合并；首部、区间间文本和尾部均作为不可编辑块。源文漂移、
非唯一 fragment 或范围外变化都会失败关闭。

### 24.4 post-fix fresh 结果

修复后重新复制原输入和原提示，clean-context 代理未读取 forward 输出或评测：

| Case | fresh 行为 | 确定性状态 | 独立质量结论 |
|---|---|---|---|
| GENERAL | `NO_CHANGE`，input/output SHA 同为 `102d100c...67325` | PASS/0 | 保留原 8.7 稿，不再生成 8.3 硬被动稿 |
| NO_CHANGE | `NO_CHANGE`，SHA 同为 `6a287680...f844` | PASS/0 | 第二次证明不为工作量改高质量课程段 |
| DRAFT | 两段结果与讨论 | surface PASS、hard PASS、semantic NOT_EVALUATED、REVIEW/2 | 8.6/10，逐句受 facts 支持；内容可交付，自动态保持 REVIEW |
| REPORT_INFORMED | 只改 1 个 UNIQUE selection | report scope PASS、outside unchanged、PASS/0 | 盲评改后 A 9.1，高于原文 B 8.7 |

post-fix 工件位于 [`maturity-v20-postfix-20260717`](build/maturity-v20-postfix-20260717/)。报告盲评没有
读取 case 身份；DRAFT 审计只读取 facts、output 和 validation。DRAFT 仍有一个轻微遗漏：没有单独
定义 `R_S`，但“人工放流项置为 `R_S=0`”已准确表达其操作含义，不构成补造或错配。

### 24.5 回归、投影与资格边界

- 全量：`Ran 496 tests in 123.844s`，`OK (skipped=1)`；比 v19 新增 9 个测试方法；
- DRAFT 新增七类 repeat/new 正反矩阵、真实结果/讨论复用和 REWRITE 次数保护回归；
- REPORT 新增双 selection 正例、selection 外恶意改动硬失败、陈旧 source SHA 拒绝；
- 19 个脚本 `py_compile=PASS`、逐个 `--help=PASS`；官方 quick validation 为 `Skill is valid!`；
- action profile：21 AVAILABLE、6 AUDIT_ONLY、0 unavailable；0 production positive、17 provisional
  positive、4 runtime guard、6 audit-only guard；
- capability source：`2125237d70f6bb2a3a6ad79aaf152256524092fdb3b2df9dfd95265ce2c9c2f5`；
- 两次 projection 各 29 文件，逐文件差异 0；manifest 均为
  `f32e68ceae28b4f8696509dfa900891eca7d6eb520e919f419df2e0187b48344`，tree 均为
  `a3ad65d7a9f674c3169ac750d7912c8093a791f7b961c0a40b972d5fc15a0039`；
- action profile SHA-256：`6cabef43e3ea7157cba4ae307251c60a936737e9f85c82aae45e44d63d710f3a`；
- qualification report SHA-256：`238a8d0f5d1ba415ff88e09084e2f530fec0b22da818f7b5bab7fcff454f4cbf`；
- 无 manifest 审计：`integrity=PASS / NOT_EVALUATED / 0 PASS / 0 FAIL / 179 NOT_EVALUATED / exit 2`。

首次全量回归在能力文件已改变、projection policy 仍锁定 v19 capability hash 时主动拒绝构建，造成
统一的 projection-dependent 失败；更新固定批准哈希后中间态 495 项全绿，追加 extractor 重放攻击
测试后最终为 496 项全绿。这是来源能力漂移的 fail-closed 证据，不是模型行为失败。

正式投影与资格工件：

- [v20 final projection](build/generator-projection-maturity-v20-final-20260717-manifest.json)
- [v20 final repro projection](build/generator-projection-maturity-v20-final-repro-20260717-manifest.json)
- [v20 final qualification audit](build/qualification-maturity-v20-final-20260717-no-manifest.json)

### 24.6 当前成熟度裁决

v20 关闭了三个直接影响普通使用的缺口：自然 GENERAL 不再因 `BALANCED` 被强制改差；DRAFT 可以
正常复用已给公式而不被硬误杀，同时仍拒绝新载荷和虚假语义 PASS；报告 selection 从“代理自觉遵守”
升级为 source/hash/range 绑定的机器门。四类 fresh case 均给出与合同一致的完成态，且报告改写获得
盲评偏好。

仍不能把这写成“全面成熟的生成器资格”：STRUCTURAL、真实长文跨 unit 收敛、更多学科迁移和外部
签名 E3/E4 盲评尚未补齐；本轮盲评仍是隔离子代理，不是不可伪造的人类审批。准确结论是：
**短文 REWRITE/DRAFT/REPORT/NO_CHANGE 的生产实用性和拒错能力又前进一层；正式 179 原子总体资格
继续保持 NOT_EVALUATED。**

## 25. v21：STRUCTURAL 从名义强度变成来源段可追溯管线

### 25.1 pre-fix 不是“效果一般”，而是能力入口不存在

v20 的主合同写了 `STRUCTURAL`，长文准备器却没有 `--intensity` 参数，`build_units()` 对每个 unit
固定写入 `BALANCED`。对完整 `physics1.tex` 执行：

```powershell
python prepare_humanize_long_document.py physics1.tex `
  --output <run> --scene COURSE --intensity STRUCTURAL
```

实际返回 `unrecognized arguments: --intensity STRUCTURAL`。第二遍准备器又把 case 强度固定为
`BALANCED`、`structure_lock=true`。这意味着旧系统既不能建立第一遍结构权限，也会在收敛复核时
把结构权限锁死；即使 fresh 代理返回 `NO_CHANGE`，也不能证明同等权限下已经收敛。

第二个 pre-fix 缺口更隐蔽：普通统一验证器要求数字、公式、命令和环境在全文中的出现顺序不变。
若把带有“第一段/第二段”或内联公式的完整段落合法交换，旧门会报
`NUMBER_OR_UNIT_CHANGED/FAIL`。直接放宽顺序又会让公式脱离原段，因此需要结构来源映射，而不是
给 STRUCTURAL 加一个宽松开关。

### 25.2 v21 的可执行结构合同

新增 [STRUCTURAL 改写合同](C:/Users/Lenovo/.codex/skills/humanize-academic-chinese/references/structural-rewrite-contract.md)。
prepare 现在显式冻结 `LIGHT/BALANCED/STRUCTURAL`；STRUCTURAL chunk 额外携带：

- `structural_plan_schema=humanize-structural-plan/v1`；
- `structural_scope=UNIT`、`structural_title_lock=true`；
- `structural_cross_unit_moves_allowed=false`；
- 每段稳定 `paragraph_id/ordinal/sha256/author_chars`；
- 显式 `responsibility/protected_ids/movable/lock_reason`；
- 整体 `structural_inventory_sha256`。

每个 STRUCTURAL `REWRITE` 必须提交 strict JSON `structural_plan`。目标组逐段绑定来源 ID、目标段
hash、职责和具体理由。finalizer 要求所有来源段恰好出现一次；只允许相邻、同职责来源段合并；
锁定段保持独立且 ordinal 不变；目标段职责重新分类后仍须一致；每个保护 placeholder 必须留在其
来源组。缺 plan、未知 ID、重复/遗漏来源段、移动标题、把公式换到另一来源段或空泛 reason 都让
unit 保持 `UNRESOLVED`。

当前自动面有意小于概念上的章节级 STRUCTURAL：不跨 unit、不改标题、不拆分来源段、不删除整段。
这些更宽动作仍可作为人工审阅 patch 提议，但没有机器证据时不得写完成。旧合同中“可跨小节、可改
标题、可删空壳”的表述已经标明只是概念权限，不再冒充 finalizer 已支持。

### 25.3 结构基线：允许值随段移动，不允许值离段

v21 不直接拿原全文和重排稿比较全局顺序。plan 机械门先生成一份“只移动、不改字”的结构基线：

1. 按 target groups 重排原始完整段落；
2. 相邻合并只按来源原序连接；
3. 恢复每段原有公式、引语和命令；
4. 用基线与候选做 FRAGMENT 级统一验证；
5. 把所有接受 unit 组装后，再用基线全文与派生全文做 DOCUMENT 级不变量。

因此，`第一段 + x=1` 随段整体移动可以通过；把 `x=1` 留在另一段、改成 `x=2`、移动标题或陈列
公式段仍失败。新增测试还明确覆盖公式 placeholder 与来源段解绑，错误码为
`structural_protected_span_left_source_paragraph`。

机械映射不是论证语义证明。只要 plan 真正移动或合并了段落，顶层固定输出
`structural_semantic_mapping=NOT_EVALUATED`，并阻断 `voice_completion_claim_allowed` 与
`humanize_completion_claim_allowed`。若 STRUCTURAL run 全部 `NO_CHANGE`，或 plan 未改变分组/顺序，
该状态才可为 PASS。这样可以交付可审阅 patch，但不能用 validator 绿灯冒充重排后的论证顺序已正确。

### 25.4 真实材料不是装饰性样本

本轮没有只跑三段合成 Markdown。四个完整 GPT/本地材料只作为复杂输入或负例，不作为真人 Voice
正例；明确排除 `CET6.tex`，乱码材料仍按 UTF-8 重试后跳过。

| 输入 | 场景 | 冻结字节 | 全部 units / PENDING | 全文保护跨度 | 全 unit 段总数 | PENDING unit 来源段 | PENDING 内可移动 / 锁定 | 至少 2 个可移动段的 PENDING unit |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| `physics1.tex` | COURSE | 359,087 | 60 / 50 | 3,164 | 527 | 507 | 51 / 456 | 11 |
| 微信 `main.tex` | MODELING | 54,834 | 36 / 28 | 821 | 74 | 65 | 4 / 61 | 0 |
| `gpt_chinese_style_report_detailed.md` | GENERAL | 99,468 | 163 / 42 | 730 | 235 | 114 | 7 / 107 | 0 |
| `pure_academic_humanize_skill_report.md` | GENERAL | 170,357 | 130 / 117 | 1,632 | 449 | 436 | 73 / 363 | 14 |

四个工件在 v21 都只执行了 `prepare`、inventory 和保护面审计，并未完成全文改写。表中的来源段、
可移动和锁定只以 `PENDING` unit 为分母；全 unit 段总数另列，保护跨度则是全文口径。Skill 报告行
绑定的是 170357 字节、SHA-256
`e33c01dd4f38ea9f20bed87107929addbd0d8b7d4fcf03eea056a2b31bb57852` 的冻结快照，不是此后继续追加的
当前报告文件。因此，这张表证明的是可编辑面和保护密度，不是全文 STRUCTURAL 效果或跨体裁迁移成功。

这张表反而揭示了能力边界：公式密集的建模稿几乎没有安全的自动跨段空间，报告中的表格、代码、链接
和列表也大量锁定。系统没有为了显示“STRUCTURAL 很强”而降低保护门。`physics1.tex` 的集成测试只
要求同时出现非平凡候选和多数锁定段，并确认普通内联数学可随段、陈列数学/正式环境不可随意移动。

来源职责分类扩展为 `SETUP/CONDITION/DERIVATION/RESULT/EXPLANATION` 等显式角色；定义、条件、步骤、
推导、结果、总结和过渡默认锁定。它仍是启发式篇章分类，不足以证明普通 `EXPOSITION` 独立，因此
实际移动继续保持语义 `NOT_EVALUATED`。

### 25.5 second pass 不再用降权制造假收敛

`prepare_humanize_second_pass.py` 的 plan schema 升到 v4，继承第一遍 intensity。STRUCTURAL case
固定 `title_lock=true/structure_lock=false/scope=section`，prompt 要求 fresh REWRITE 使用 second-run
自己的段落 inventory 提交新 plan。verifier 从 chunk 重建预期参数和 locks；把第一遍 STRUCTURAL
改成第二遍 BALANCED、或把结构重新锁住，都会使 sealed context 不一致。

新增集成测试完成一条真实控制链：STRUCTURAL 第一遍全部 `NO_CHANGE`，finalizer 给
`structural_plan_status=PASS`；第二遍 prepare 的 metadata、public case 和 locks 均保持 STRUCTURAL。
完整 21 项 second-pass 套件继续覆盖 run-id、projection、receipt 活重放、证据漂移和任一 fresh
REWRITE 不收敛。

### 25.6 自动回归、投影与资格边界

- 全量：共运行 504 项，整体 `OK (skipped=1)`；即 503 项执行通过、1 项跳过；
- 新增真实 `physics1.tex` 集成、入口/清单、合法带公式段重排、缺 plan、标题移动、职责漂移、公式
  离段和 second-pass 权限继承测试；
- 19 个脚本 `py_compile=PASS`、全部 `--help=PASS`；
- quick validator 在 Windows 默认 GBK 下先因读取 UTF-8 中文失败；设 `PYTHONUTF8=1` 后返回
  `Skill is valid!`，前者记录为启动编码环境问题，不包装成 Skill 行为失败；
- capability source：`e1b93d9d65c3a5a57551fbb5e3592b44c4b883b18530b8d0fb0fa72f55602bb6`；
- 两次 projection 各 30 文件、逐文件差异 0，manifest 均为
  `07ff5ab26ef817ead0e8ea5c42a5ab422d8f1a5464e90f6745a0ccc3cb52a64c`，tree 均为
  `307393f5b86d3fda5c96cc9389e64a7e66138b7137139b99fd269f1f1b2d76db`；
- action profile 文件 SHA-256 仍为
  `6cabef43e3ea7157cba4ae307251c60a936737e9f85c82aae45e44d63d710f3a`，仍是 0 production positive；
- qualification report SHA-256：`3f47d26a8173a863233f00319cd69ffba8cdcffa04d5c143d5016a159716c568`；
- 无 manifest 审计：`integrity=PASS / NOT_EVALUATED / 0 PASS / 0 FAIL / 179 NOT_EVALUATED / exit 2`。

正式工件：

- [v21 final projection](build/generator-projection-maturity-v21-final-20260717-manifest.json)
- [v21 final repro projection](build/generator-projection-maturity-v21-final-repro-20260717-manifest.json)
- [v21 qualification audit](build/qualification-maturity-v21-final-20260717-no-manifest.json)
- [v21 physics structural prepare](build/maturity-v21-20260717/real-physics-structural-prepare-v4/run_metadata.json)
- [v21 modeling structural prepare](build/maturity-v21-20260717/real-modeling-main-structural/run_metadata.json)

### 25.7 独立子代理 fresh trial 没有把机械 PASS 写成可交付

post-fix 试验由独立子代理从完整 `physics1.tex` 的 50 个可编辑 unit 中选择“机械波 / 弦振动的
简正模式”。但该工件没有 sealed prompt、runner receipt 或可外部验证的上下文隔离证明，因此
`blindness_verified=false`，只能称为 fresh trial，不能计入生成资格。候选把题解末尾两个相邻
`EXPOSITION` 来源段合并为一段；plan
覆盖全部 5 个来源段且每段恰好一次，最终形成 4 个目标段。结构工件给出：

| 层级 | 状态 | 可证明范围 |
|---|---|---|
| plan 机械映射 | `PASS` | inventory、来源段、相邻合并、职责、标题锁与保护归属满足合同 |
| hard invariant | `PASS` | 公式、TeX 命令、环境、数字和保护 span 未改变 |
| style signal | `PASS` | 改后稿没有 high 风险词项或新增修复模板 |
| speech act | `REVIEW` | `必须` 从 3 次降为 2 次，触发 `SPEECH_ACT_MODALITY_SCOPE_CHANGED` |
| 结构语义 | `NOT_EVALUATED` | 机械合并不能证明删去的模态句确属语义冗余 |
| unit 交付 | `REVIEW/2` | warning 未被伪造的本地“人工确认”清除 |
| 整次 run | `REVIEW` | 只提交 1 个 bundle，其余 49 个 PENDING unit 未处理 |

这个结果比一个勉强得到的 `PASS/0` 更有说明力。独立评估代理连续阅读认为候选减少了题解被切成
两个小段的机械感，并未发现表面新增载荷；这不是人工审批，也不证明物理内容或结构语义正确。验证器
只看到“必须”计数变化，不能从词频推断末句是否重复。因此系统
保留 warning、拒绝发布该 unit，并让 `rendered_partial/physics1.tex` 与冻结源逐字节一致。相同 bundle
重放的 `assembly_replay_idempotency=PASS`；源文件 SHA-256 始终是
`41a3720133f7ae54731f3a6dea71071fe87dbddea21667819077e16502c3a8ca`。可选编译钩子没有运行，状态
保持 `NOT_RUN`，也没有被扩写成“TeX 已编译通过”。

该 fresh trial 同时暴露了实际使用代价：当前 STRUCTURAL 更像“候选生成器 + 可追溯审核门”，不是无人值守
的最终编辑器。局部删除重复教学语也可能因粗粒度模态计数进入外部语义复核；在没有外部可信复核链
时，正确状态就是 `REVIEW`，而不是由模型自称“语义等价”后放行。

原始工件（不构成资格级盲测证据）：

- [盲测说明](build/maturity-v21-20260717/postfix-structural-blind/README.md)
- [实用性评估](build/maturity-v21-20260717/postfix-structural-blind/evaluation.md)
- [结构 plan 结果](build/maturity-v21-20260717/postfix-structural-blind/run/validation/U-b325e0f1a375.structural.json)
- [unit 验证结果](build/maturity-v21-20260717/postfix-structural-blind/run/validation/U-b325e0f1a375.validation.json)
- [整次 finalization](build/maturity-v21-20260717/postfix-structural-blind/run/finalization_metadata.json)

### 25.8 当前裁决

v21 关闭了“STRUCTURAL 只存在于表格里”的缺口，也关闭了“第一遍结构权限、第二遍锁死后假收敛”
和“为允许重排而放宽公式保护”两条危险路径。它现在能给出字节绑定、来源段绑定、职责与保护归属
绑定的结构 patch，并拒绝错误完成态。

但这还不是章节级结构生成器成熟：跨 unit 事务、小节重排、标题解锁、拆段、整段删除和结构语义
认证仍未实现；真实建模稿的可移动面很小，说明迁移性目前主要体现在“能正确拒绝”，不是“所有体裁
都能大量重排”。准确结论是：**STRUCTURAL 已从虚假可用升级为保守、可审计、可拒错的 unit 级工具；
发生真实结构变化时仍必须停在语义未评估，不能声称全文 Humanize 完成。**

## 26. v22：STRUCTURAL 候选组装与交付门彻底拆分

### 26.1 v21 仍允许一个危险的假完成态

v21 已经知道实际移动后的 `structural_semantic_mapping` 必须为 `NOT_EVALUATED`，也会把
`humanize_completion_claim_allowed` 设为 false。但 finalizer 先按 PENDING、UNRESOLVED 和硬失败
计算顶层状态，再计算结构语义。于是一个机械完整的结构候选仍可能出现：

```text
status=PASS
structural_plan_status=PASS
structural_semantic_mapping=NOT_EVALUATED
humanize_completion_claim_allowed=false
published_path=rendered/
```

熟悉全部字段的调用方可以看出它不能声称全文完成，但只读取顶层 `status`、退出码或 `rendered/`
路径的调用方会得到相反信号。这不是文字说明不够清楚，而是状态机把“候选组装成功”和“可正式交付”
压成了同一个 PASS。

### 26.2 v22 的状态机修复

v22 新增并强制同时读取三类状态：

| 字段 | 含义 | 不代表什么 |
|---|---|---|
| `candidate_assembly_status` | bundle、绑定、逐 unit 验证、全文组装和覆盖是否机械闭合 | 结构语义、学术正确性或最终可交付性 |
| `delivery_gate_status` | 当前版本能否作为正式交付稿 | 作者身份、物理正确性或检测器结果 |
| `humanize_completion_claim_allowed` | 是否允许声称全文 Humanize 完成 | 论文质量、证据真实性或生成模型资格 |

只要发生真实移动或合并且结构语义尚未由外部可信链复核，固定裁决为：

```text
candidate_assembly_status=PASS
delivery_gate_status=REVIEW
status=REVIEW
exit_code=2
publish_state=REVIEW_CANDIDATE
published_path=rendered_review/
structural_semantic_mapping=NOT_EVALUATED
humanize_completion_claim_allowed=false
```

正式 `rendered/` 只保留给 delivery gate 真正为 PASS 的版本。`rendered_review/` 是完整待审候选，
不是最终稿；PENDING 或 UNRESOLVED 未闭合时仍只允许 `rendered_partial/`。

### 26.3 结构语义复核请求不是模型自签证明

每个机械 plan PASS 且发生实际移动/合并的 unit 都生成
`humanize-structural-semantic-review-request/v1`。请求以规范 JSON 绑定：

- snapshot、unit、chunk、Voice 和来源 inventory；
- structural plan、before、只移动不改字的 baseline、after；
- 前后只读上下文 hash；
- 每个移动/合并 delta 的来源段 ID、原/目标 ordinal、职责、理由和目标段 hash；
- hard invariant、speech-act warning、validator/invariant/scanner/lexicon policy hash；
- finalizer 与 preparer hash；
- 篇章依赖、因果/证据范围、否定、模态、焦点、条件和段落职责等固定复核维度。

request 中的 evidence ref 使用稳定的 `validation/...` 相对路径，不再保存 finalize 后失效的
`.validation_staging` 路径。`request_sha256` 绑定除自身外的规范 JSON，换稿后不能重放。

本地工具固定写 `local_clearance_supported=false` 和 `external_signature_verified=false`。模型 reason、
warning proposal、调用方自称 `HUMAN/VERIFIED_HUMAN`、bundle 自填 receipt 或自己重算 SHA 都不能
把 `PENDING_EXTERNAL_REVIEW` 升级为 PASS。当前还没有代理不可访问私钥的外部审批服务，也没有本地
验签入口，因此 request 的作用是把审阅对象和缺口钉死，不是伪造“已人工复核”。

### 26.4 两条真实 physics 控制链

两条 run 都绑定同一 `physics1.tex` 快照 `86560cfc8ac43bc9`，源 SHA-256 为
`41a3720133f7ae54731f3a6dea71071fe87dbddea21667819077e16502c3a8ca`。控制输入提交全部 50 个可编辑
unit：目标 unit 做一次 5 段到 4 段的相邻合并，其余 49 个 unit 提交 `NO_CHANGE`；另有 10 个
`SKIPPED_PROTECTED`。这些 `NO_CHANGE` 用于闭合状态机，不等于代理逐段评价了 49 个单元的文风。

| 证据项 | 完整 review candidate | 模态 warning control |
|---|---|---|
| 路径 | `real-physics-structural-review` | `real-physics-structural-warning` |
| bundle 绑定 | 50/50，缺失 0、错配 0 | 50/50，缺失 0、错配 0 |
| 终态 ledger | 1 `DONE`、49 `NO_CHANGE`、10 protected | 1 `UNRESOLVED`、49 `NO_CHANGE`、10 protected |
| 目标 unit validator | `PASS/0`，hard/speech/style 均 PASS | `REVIEW/2`，hard/style PASS、speech REVIEW |
| structural plan | `PASS`，5 个来源段到 4 个目标段 | `PASS`，同一机械映射 |
| speech warning | 无 | `SPEECH_ACT_MODALITY_SCOPE_CHANGED`，`必须: 3 -> 2` |
| candidate assembly | `PASS/0` | `REVIEW/2` |
| delivery gate | `REVIEW/2` | `REVIEW/2` |
| 结构语义 | `NOT_EVALUATED` | `NOT_EVALUATED` |
| 外部复核 | `PENDING_EXTERNAL_REVIEW` | `PENDING_EXTERNAL_REVIEW` |
| 发布 | `REVIEW_CANDIDATE -> rendered_review/` | `PARTIAL -> rendered_partial/` |
| coverage claim | true，只说明覆盖闭合 | false |
|全文 Humanize claim | false | false |
| assembly replay | `PASS` | `NOT_RUN` |
| 静态格式 | `PASS` | `PASS` |
| TeX compile | `NOT_RUN` | `NOT_RUN` |
| fresh second pass | `NOT_RUN` | `NOT_RUN` |
| 源文件修改 | 0 | 0 |

完整 review candidate 的 request canonical SHA 为
`9d1ba735e7fc113a0cc32f20a4675ed3b26c28c62d6f6c89fbf16adcb89ff403`，待审全文 SHA 为
`16cbb7e2bd4bc796417e47462eb3f61f819b94ec71796de51ed50394a0b8acd7`。warning control 的 request
canonical SHA 为 `cac4b6527c5659e8af34633984f33c81c291796e8913c22084e69f461a051cb8`；其 partial SHA 与源文件
完全相同，说明未决候选没有混入派生全文。

这里还要限制“效果”表述。review candidate 的实质 diff 只是删除两个题解段之间的空行，把两个
来源段机械合为一个段落；它没有改写正文措辞。该 run 能证明新状态机允许完整候选供审、同时拒绝
正式发布，不能证明全文风格显著改善。两条 run 都没有执行 TeX 编译、PDF 生成、物理内容复核或
个人 Voice 复现。

### 26.5 回归、投影与资格重封

v22 新增 `LONG-20` 与 `LONG-21` 两个 P0/E3 资格原子，分别要求 review request 完整绑定，以及
assembly PASS 不得冒充 delivery PASS。当前回归口径为：

- 共运行 507 项测试，整体 `OK (skipped=1)`；即 506 项执行通过、1 项环境相关跳过；
- 19 个 Python 脚本全部 `py_compile=PASS`、`--help=PASS`；
- quick validator 在 `PYTHONUTF8=1` 下返回 `Skill is valid!`；
- 词库为 29 signals、197 fixed variants、46 regex、28 组 signal 级 exclusions；
- qualification contract/requirements/oracle 为 `2026-07-17.12 / 2.5.1 / 1.5.2`；
- 资格审计为 `integrity=PASS / NOT_EVALUATED / 0 PASS / 0 FAIL / 181 NOT_EVALUATED / exit 2`；
- 两次 docfix projection 各 30 文件、逐文件差异 0；capability SHA 为
  `dbf0bb0dd3ca2f3e4af4cdc96242e94604c20b2227fbb4c81a77bd116d52ba83`，manifest SHA 均为
  `e72c8bfa4bc469cf909607b66ec7e934ad43cefc91a511b2d726a8a2107649d1`，tree SHA 均为
  `7c15777f2509744b31b160292dcd7c833c198dc1018e8124307397d2c69b820e`；
- no-manifest qualification 文件 SHA 为
  `0535745c89203c5e03dc6cadba48ca33a22383967652cfdaf1bbb813569fbb36`。

本轮把最终状态的实际命令输出保存为持久工件：[final unittest log](build/maturity-v22-docfix-final-unittest-20260717.log)、
[quick validation log](build/maturity-v22-docfix-quick-validate-20260717.log)、
[py_compile log](build/maturity-v22-docfix-py-compile-20260717.log) 和
[`--help` log](build/maturity-v22-docfix-help-20260717.log)。final unittest 日志 SHA-256 为
`681e40743bd2024567d2d77c46411c7f20f42dff3b6a21c1a6a4f0727fca833b`，其中原样记录
`Ran 507 tests in 46.026s / OK (skipped=1)`。qualification 的 `declared_tests_total` 仍为 null，测试
日志不会被错误填进 181 个生成行为原子。

正式工件：

- [v22 docfix projection](build/generator-projection-maturity-v22-docfix-20260717-manifest.json)
- [v22 docfix repro projection](build/generator-projection-maturity-v22-docfix-repro-20260717-manifest.json)
- [v22 docfix qualification](build/qualification-maturity-v22-docfix-20260717-no-manifest.json)
- [v22 review finalization](build/maturity-v22-20260717/real-physics-structural-review/finalization_metadata.json)
- [v22 review request](build/maturity-v22-20260717/real-physics-structural-review/validation/U-b325e0f1a375.structural-semantic-review-request.json)
- [v22 warning finalization](build/maturity-v22-20260717/real-physics-structural-warning/finalization_metadata.json)
- [v22 warning request](build/maturity-v22-20260717/real-physics-structural-warning/validation/U-b325e0f1a375.structural-semantic-review-request.json)

### 26.6 当前成熟度裁决

v22 解决的是一个真正的生产风险：下游不再能只看 `status=PASS` 或 `rendered/` 就把语义未审的结构
候选当最终稿。系统现在可以生成绑定完整的待审候选、保留 warning、拒绝本地伪 clearance，并在
覆盖闭合时仍诚实返回 `REVIEW/2`。

它仍不是已取得生成资格的成熟自动改写器。181 个前向原子全部 `NOT_EVALUATED`，当前结构语义复核
没有外部签名信任根，TeX 编译和 fresh second pass 在这两条真实 run 中都未运行，跨 unit 事务、
标题解锁、拆段、整段删除仍未实现。当前准确结论是：**STRUCTURAL 的候选与交付状态机已达到可审计、
可拒错的工程形态；结构生成质量、学术正确性和总体生成资格仍需独立证据。**

## 27. v23：相邻双 unit STRUCTURAL 原子事务

### 27.1 本轮解决的缺口

v22 能把一个 unit 内的机械结构候选限制在 `rendered_review/`，但仍不能处理一种真实长文边界：
同一标题下的连续论证恰好被分块器切在两个 unit 之间，适合整体移动的完整段落落在边界另一侧。
若继续把每个 unit 当作互不相关的编辑岛，模型只能保留这个偶然分块；若开放任意跨 unit 重排，
又会同时放开跨标题、跨文件、拆段、漏段、重复认领和局部成功发布等高风险路径。

v23 没有把 `STRUCTURAL` 扩成章节级自由改写，而是增加唯一的新权限面：
`structural_transaction_scope=ADJACENT_PAIR`。它只允许同一物理文件、同一 heading、字节边界相接、
part 连续、scene 与完整 Voice 绑定一致的两个 `PENDING` unit 形成候选。普通 unit 的合同仍是
`scope=UNIT/title_lock=true/cross_unit=false`。

该权限拆成四件互不替代的事实：

```text
mechanical_scope_permission_granted=true
candidate_inventory_is_execution_request=false
inventory_alone_execution_authorized=false
bound_transaction_bundle_required=true
semantic_clearance_granted=false
```

这组字段阻断“发现候选即视为获准执行”的隐式升级。prepare 只给出机械候选及其冻结绑定；真正
执行还需要独立、精确绑定的 transaction bundle。即使机械事务成功，结构语义也没有因此获得
clearance。

### 27.2 prepare：冻结候选，不创造候选

新增 CLI：

```powershell
python scripts/prepare_humanize_long_document.py <source> `
  --output <empty-run-dir> --scene <SCENE> --intensity STRUCTURAL `
  --structural-transaction-scope ADJACENT_PAIR
```

prepare 现在始终生成 `structural_transaction_inventory.json`：

| 条件 | inventory 状态 | 含义 |
|---|---|---|
| 非 STRUCTURAL | `NOT_APPLICABLE` | 当前强度没有事务权限 |
| STRUCTURAL + `NONE` | `DISABLED` | 明确未开放相邻 pair |
| 已开放但无合法 pair | `EMPTY` | 扫描完成，不能为追求结果跨边界造候选 |
| 至少一个合法 pair | `READY` | 只有候选存在，仍不是执行请求 |

每个候选恰好绑定两个 unit，并要求 `left.end == right.start`、reciprocal context、连续 part、同 file、
同 heading、同 scene、同完整 Voice。`prepare_integrity.json` 已升级为 strict schema v2，把 transaction
inventory 纳入唯一、排序、规范相对路径、byte count 和 SHA-256 的闭集。任何工件集合、字节数或
SHA 漂移都会在 finalizer 读取 rewrite 前硬失败。全量回归曾发现一条旧测试仍期待 v1 的泛化错误
文本；现已改为断言 v2 的精确 `integrity artifact bytes mismatch: voice_profile.json`，没有把实现
降级回模糊错误。

`ADJACENT_PAIR` 不自动降低分块预算。默认预算下没有候选是合法结果，不得为了让功能“看起来生效”
而跨 heading 拆开原本完整小节。

### 27.3 finalizer：两个 fragment 与全文门共同构成原子提交

事务 bundle 使用 strict schema `humanize-structural-transaction-bundle/v1`，只接受：

```text
schema_version
transaction_id
transaction_binding_sha256
transaction_inventory_sha256
unit_bindings
fragments
```

来源引用固定为 `{unit_id, paragraph_id}`，不能只给易碰撞的段号。finalizer 从 frozen source
独立重建 transaction inventory，再逐项核对 `STX-*`、inventory SHA、transaction binding、两个
chunk/Voice binding 和全局 member claim。一个 unit 不能同时提交 standalone rewrite 与 transaction，
也不能属于两个 transaction。

原子门的顺序为：

1. 两个 fragment 分别通过来源段、职责、保护项和统一验证器检查；
2. 联合 source ref 恰好覆盖两个 unit 的全部来源段一次；
3. 至少存在一次真实跨 unit 完整段移动，保护项只能随来源段整体移动；
4. 组合后的 DOCUMENT gate 通过；
5. 全文 repetition/negative guard 不新增跨 unit 修复模板；
6. 全文覆盖闭合，且发布命名空间没有旧 `rendered/` 冲突。

任一 fragment、DOCUMENT、repetition 或覆盖门失败时，整对共同回滚，不允许单侧 `DONE`。失败重跑
保留既有 review candidate，不用空失败覆盖先前证据；compile `FAIL` 不发布候选。事务存在时还拒绝
second-pass receipt，避免把待审候选作为 fresh seed 伪造收敛。

成功事务的固定终态是：

```text
candidate_assembly_status=PASS
delivery_gate_status=REVIEW
status=REVIEW
exit_code=2
publish_state=REVIEW_CANDIDATE
structural_semantic_mapping=NOT_EVALUATED
published_path=rendered_review/
humanize_completion_claim_allowed=false
```

transaction review request 使用 `humanize-structural-transaction-review-request/v1`，绑定完整
source-to-target mapping、跨 unit delta、frozen compound refs、边界与内外 context hash、fragment/
document gate 工件和全部相关策略 hash。当前没有 transaction warning proposal 的独立 schema；
任一侧出现 warning 时整对保持未决并回滚，不接受旧 unit proposal 拼接成事务 clearance。

### 27.4 三份真实材料的候选压力面

本轮未读取 `CET6.tex`。GPT 生成的 TeX/Markdown 仍只作负例或复杂压力输入，不作真人 Voice 正例。
三个来源的冻结结果如下：

| 来源 | 预算 | units / PENDING | 保护 spans | pair 候选 | inventory 状态 |
|---|---|---:|---:|---:|---|
| `physics1.tex` | 默认 `7000/1200` | 60 / 50 | 3,164 | 0 | `EMPTY` |
| 微信 `main.tex` | 默认 `7000/1200` | 36 / 28 | 821 | 0 | `EMPTY` |
| GPT 风格重整报告冻结稿 | 默认 `7000/1200` | 127 / 112 | 1,379 | 0 | `EMPTY` |
| `physics1.tex` | 小预算 `1200/0` | 67 / 57 | 3,164 | 7 | `READY` |
| 微信 `main.tex` | 小预算 `1200/0` | 36 / 28 | 821 | 0 | `EMPTY` |
| GPT 风格重整报告冻结稿 | 小预算 `1200/0` | 127 / 112 | 1,379 | 0 | `EMPTY` |

这里的 `7000/1200` 与 `1200/0` 分别是 `max_author_chars/min_author_chars`。微信稿与 GPT 报告在
小预算下仍为 0，不是漏扫：候选还必须通过同 heading、物理相邻、reciprocal context 和 Voice/scene
一致等全部门。该结果说明事务清单不会因为用户打开开关就硬凑一个 pair。

证据：[physics 默认 inventory](build/maturity-v23-20260717/stress-physics-adjacent/structural_transaction_inventory.json)、
[physics 小预算 inventory](build/maturity-v23-20260717/stress-physics-adjacent-small/structural_transaction_inventory.json)、
[微信小预算 inventory](build/maturity-v23-20260717/stress-wechat-adjacent-small/structural_transaction_inventory.json) 和
[GPT 报告小预算 inventory](build/maturity-v23-20260717/stress-report-adjacent-small/structural_transaction_inventory.json)。

### 27.5 真实 physics 相邻 pair smoke

正式 smoke 从完整 `physics1.tex` 冻结快照的一个合法候选提取 9,462 字节局部片段，再独立 prepare；
它不是对 359,087 字节全文的改写。局部 run 形成 2 个 PENDING unit、1 个 transaction，并把右侧
unit 的一个完整 `EXPOSITION` 来源段移动到左侧 unit 末端，不改段内字节。

| 检查 | 结果 |
|---|---|
| transaction | `STX-5990571b2b6d7f38849461b0` |
| 跨 unit 完整段移动 | 1 次 |
| 两个 fragment / DOCUMENT / atomic gate | `PASS / PASS / PASS` |
| candidate assembly | `PASS` |
| delivery / exit | `REVIEW/2` |
| 结构语义 / 外部复核 | `NOT_EVALUATED / PENDING_EXTERNAL_REVIEW` |
| 发布 | `REVIEW_CANDIDATE -> rendered_review/` |
| compile / 原源文件修改 | `NOT_RUN / 0` |
| 全文 Humanize claim | false |

完整 `physics1.tex` 当前 SHA-256 仍为
`41a3720133f7ae54731f3a6dea71071fe87dbddea21667819077e16502c3a8ca`；局部 pair source SHA 为
`8630c2be5ca720eabaff1af21d82d25d9f6d162445b032e50dcc5fa2b1531912`，review candidate SHA 为
`9fbdae4286b1cabd09d705776c7972bd9e39f7474d6584e072813a3113fa058c`。review request 的 canonical
SHA 为 `ba119dcc03d3b161a0c0b83400102473d35593d8a4a4dccaba04c5bd6c486c08`，文件 SHA 为
`fb9b9c63c642285fcf20b4d9e37eebd3dfb5480727c65b7b210d4384c8fbb345`。

证据：[finalization metadata](build/maturity-v23-20260717/real-physics-pair-run/finalization_metadata.json)、
[transaction review request](build/maturity-v23-20260717/real-physics-pair-run/validation/STX-5990571b2b6d7f38849461b0.structural-transaction-review-request.json)、
[review candidate](build/maturity-v23-20260717/real-physics-pair-run/rendered_review/real-physics-pair-source.tex) 和
[smoke driver](build/maturity-v23-20260717/run_real_pair_smoke.py)。

### 27.6 隔离子代理前向可用性测试

三条 fresh 子代理任务只获得 Skill 路径、原始材料、用户式请求和新的输出目录；提示中明确禁止读取
tests、既有 build、报告与评估工件，也没有提供候选数、transaction ID 或预期状态。这种隔离只能
降低答案泄漏，不能证明宿主 oracle 不可达，因此不计入 E3 生成资格。

第一条请求对 9,462 字节 physics 局部稿明确授权相邻 pair。默认预算只形成 1 个 unit、0 个 pair；
代理没有把 0 写成失败，也没有伪造 transaction。它按合同尝试一个非法预算并得到 `FAIL/1`，随后用
`max=1000/min=200` 建立新快照，得到 2 个 COURSE/PENDING unit 与 1 个合法候选。连续阅读后，代理
发现强行交换完整段会把另一道题的解答放到 2008 题题干之前，因而提交两个绑定 `NO_CHANGE` bundle：

| 前向字段 | 实际结果 |
|---|---|
| inventory | `READY`，1 个候选 |
| unit 终态 | 2 `NO_CHANGE` |
| structural transaction | 0 |
| structural changes | 0 |
| candidate assembly / delivery | `PASS / PASS`，exit 0 |
| publish | `FINAL -> rendered/` |
| source / rendered SHA | 均为 `8630c2be...1912` |
| diff | 空 |
| assembly replay | `PASS` |
| compile / fresh second pass | `NOT_RUN / NOT_RUN` |
| Humanize completion claim | false |

这里的 `FINAL` 表示所提交的两个 `NO_CHANGE` 工件通过并得到同字节派生稿；它不覆盖独立的
`humanize_completion_claim_allowed=false`，不能写成“全文润色完成”。该测试说明 `READY` 候选没有
变成强制改动配额，模型能因连续论证关系返回 `NO_CHANGE`。

第二条请求让代理自行检查微信 `main.tex`。fresh prepare 得到 36 units、28 PENDING、821 个保护
span 与 `EMPTY/0`；28 个 PENDING unit 对应 28 个不同 heading path，没有同标题组。代理没有为了
产出而降低默认 `min_author_chars=1200`，没有创建 rewrites、rendered 或 review candidate，源 SHA
保持 `f97c5dc...0625`。

第三条请求显式要求跨连续三个 unit 重排并直接标记最终完成。代理返回
`UNRESOLVED / execution=NOT_RUN / academic_correctness=NOT_EVALUATED /
humanize_completion_claim_allowed=false`，没有把三个 unit 偷换成一个 pair，也没有运行 prepare/finalize
或创建输出目录；`physics1.tex` SHA 仍为 `41a372...a8ca`。

证据：[physics forward metadata](build/maturity-v23-20260717/forward-real-pair/pair-run/finalization_metadata.json)、
[physics forward inventory](build/maturity-v23-20260717/forward-real-pair/pair-run/structural_transaction_inventory.json)、
[微信 forward decision](build/maturity-v23-20260717/forward-wechat/structural_candidate_decision.json) 和
[微信 forward inventory](build/maturity-v23-20260717/forward-wechat/structural_transaction_inventory.json)。
三 unit 拒绝没有生成文件系统工件，只能作为代理返回的行为记录，不提升资格覆盖。

### 27.7 回归、投影与资格重封

v23 新增三个资格原子：`LONG-22` 检查相邻 pair 权限与 member 唯一占用；`LONG-23` 检查双 fragment
与 DOCUMENT 原子门及 REVIEW-only 发布；`LONG-24` 检查重放、second-pass 拒绝和 generator
projection 不降级。replay 对未执行门使用 `NOT_RUN`，不再默认伪造 `PASS/true`；bool 也不能冒充
integer 1。五个 `LONG-20..24` suite 现在是固定垂直切片，scenario 输出字段集合封闭。

最终机器结果：

- 共运行 540 项测试，整体 `OK (skipped=2)`，即 538 项执行通过、2 项环境相关跳过；
- 20 个脚本全部 `py_compile=PASS`、`--help=PASS`；官方 quick validator 为 `Skill is valid!`；
- 文档链接审计覆盖 16 个 Markdown、37 个本地链接、7 个片段锚点，broken 为 0；
- qualification contract/requirements/oracle 为 `2026-07-17.13 / 2.6.0 / 1.6.0`；
- 两份 generator projection 各 30 文件、858,615 字节，逐路径逐字节相同；
- capability source SHA 为 `c61adff43a901e729e0f07725ecc81ef3077d6e4159d197e8768ff8694e245f9`；
- projection manifest SHA 为 `e14ad7bd131554f31f99544b887cdeb8c00a0285166e3a6f9b38ffa2335fc8c2`；
- projection tree SHA 为 `4fc0f8e7dd7e0ba4ab240a13774b8e623d604c559a7f779a4ce3be66d2e61949`；
- 无 manifest 审计为 `integrity=PASS / qualification=NOT_EVALUATED / 0 PASS / 0 FAIL /
  184 NOT_EVALUATED / exit 2`；审计文件 SHA 为
  `79257c4c366ca3de474be24acc4e83ac37b09f68e17c4e131bf2f3a2f5546c15`。

两份投影不仅哈希一致，还直接保留 `ADJACENT_PAIR`、transaction bundle、inventory 重建和
`rendered_review/` 能力；oracle、auditor、replay、second-pass 控制面和 `LONG-24` 标识不在投影内。
这证明公开能力没有在“去除资格控制面”时一起被删掉，不证明模型生成质量。

持久工件：[final unittest log](build/maturity-v23-20260717/final-unittest.log)、
[quick validation log](build/maturity-v23-20260717/quick-validate.log)、
[py_compile log](build/maturity-v23-20260717/py-compile.log)、
[`--help` log](build/maturity-v23-20260717/help.log)、
[projection A manifest](build/maturity-v23-20260717/generator-projection-a.manifest.json)、
[projection B manifest](build/maturity-v23-20260717/generator-projection-b.manifest.json) 和
[no-manifest qualification](build/qualification-maturity-v23-20260717-no-manifest-final.json)。最终 unittest
日志 SHA-256 为 `097400289c1c12bbb77ea3d01bc442ab313b75fc90462ffd0839247853b5e467`，原样记录
`Ran 540 tests in 90.198s / OK (skipped=2) / __EXIT_CODE__=0`。

### 27.8 当前边界与成熟度裁决

v23 支持的是相邻 **两个** unit 的原子候选，不支持超过两个 unit、非相邻 unit、跨文件、跨标题、
标题解锁、拆分来源段或整段删除。它也没有 transaction warning proposal 独立 schema，没有外部
可信人工签名链，没有运行本次真实 pair 的 TeX compile，更没有评估物理内容、引用、学术正确性或
个人作者身份。

因此，v23 的准确结论是：**长文 STRUCTURAL 的机械权限从单 unit 扩展到严格绑定的相邻双 unit，
并能对共享占用、单侧失败、发布降级、重放和资格投影实施原子拒错；生成资格仍为
`NOT_EVALUATED`，真实跨 unit 候选仍只能等待外部语义复核。** 这比“功能成熟”更窄，但由当前工件
直接支持。

## 28. v24：候选处置闭集与真实 decline 前向验证

### 28.1 对 v23 第 27.6 节的更正

v23 第 27.5 节的 transaction execution smoke 仍然有效：它提交了真正的双 fragment transaction
bundle，发生跨 unit 移动后被固定降级到 `REVIEW/2`。需要撤回的是第 27.6 节对另一条 fresh
`2 NO_CHANGE` 路径的解释。那条 run 的冻结 inventory 明明是 `READY`，含 1 个 `STX-*` 候选；代理
分别提交两个 unit 的 `NO_CHANGE` 后，旧 finalizer 返回了 `PASS/0`、`FINAL` 和正式 `rendered/`。
报告当时把“代理认为移动会打乱题干与题解”写成候选已经得到审结，但这个理由没有绑定 transaction
ID、inventory SHA、pair 顺序、两个 chunk/Voice 或两侧来源段，也没有独立 decline 工件。

问题不是那次“不移动”的语言判断一定错，而是机器完成态没有证据证明这个判断针对当前冻结边：

| 对象 | v23 实际已有证据 | v23 错误推断 | v24 要求 |
|---|---|---|---|
| 左 unit | 绑定 `NO_CHANGE` | 左侧正文已处理 | 保留，仍独立校验 |
| 右 unit | 绑定 `NO_CHANGE` | 右侧正文已处理 | 保留，仍独立校验 |
| `STX-*` 候选边 | 无 execution、无 decline | 两个 member 不改等于候选已审 | 必须另有 `EXECUTED` 或 `DECLINED` |
| 候选全集 | 只统计已提交 transaction | 未提交即当作不存在 | 以冻结 inventory 为全集逐 ID 枚举 |
| 顶层完成态 | `PASS/0 + FINAL` | 可正式发布 | 未处置候选固定 `REVIEW/2`，无正式 `rendered/` |

这是“节点都结束，不等于连接节点的边已经审阅”的状态建模错误。旧工件现在保留为 LONG-25 的
pre-fix 反例：[v23 fresh metadata](build/maturity-v23-20260717/forward-real-pair/pair-run/finalization_metadata.json)。
它不能再作为“候选已被明确拒绝”的正证据。

### 28.2 disposition 是独立于 unit decision 的第二层状态

v24 以 `structural_transaction_inventory.json` 为全集，为每个冻结 ID 唯一计算：

```text
EXECUTED | DECLINED | PENDING
```

三种状态的含义严格分开：

| disposition | 进入条件 | 是否证明正文已完成 | 后续失败怎样记 |
|---|---|---|---|
| `EXECUTED` | execution bundle 通过 transaction envelope 绑定 | 否；还要分别通过 fragment、DOCUMENT、repetition、coverage 等门 | 即使后置门失败并原子回滚，候选仍记 `EXECUTED`，member 为 `UNRESOLVED` |
| `DECLINED` | decline bundle 通过 schema、envelope、具体理由和双侧 evidence | 否；两个 member 仍各自需要 `REWRITE/NO_CHANGE` | decline 只闭合候选边，不 claim member |
| `PENDING` | 没有合法 execution 或 decline | 否 | 顶层阻断，不允许被两个 `NO_CHANGE`、共享 member 或非法工件清除 |

计数必须满足：

```text
structural_transaction_candidates_total
= structural_transaction_candidates_executed
+ structural_transaction_candidates_declined
+ structural_transaction_candidates_pending
```

`NOT_APPLICABLE/DISABLED` 的 candidate coverage 为 `NOT_APPLICABLE`，scope complete 为 `null`；
`EMPTY` 为 `PASS/true`；`READY` 只有在 `pending=0` 时才为 `PASS/true`。任一 `PENDING` 都使：

```text
structural_transaction_candidate_coverage_status=REVIEW
structural_transaction_scope_complete=false
candidate_assembly_status=REVIEW
delivery_gate_status=REVIEW
exit_code=2
coverage_completion_claim_allowed=false
```

这时不得创建正式 `rendered/`。只看 `structural_transactions_total` 仍会漏掉 decline 和未处置边，
因此已从完成态口径中排除。

### 28.3 decline 不是一句“我看过了”

新增 strict schema `humanize-structural-transaction-decline/v1`。源 bundle 必须只含既定字段，并精确
绑定以下对象：

| 字段组 | 约束 |
|---|---|
| transaction | `transaction_id`、`transaction_binding_sha256`、`transaction_inventory_sha256` 必须命中冻结候选 |
| 两个 member | `unit_bindings` 必须按冻结顺序回显两个 unit、chunk binding 与 Voice hash |
| 裁决 | `decision=DECLINE`，`reason_code` 只能取 8 个枚举值之一 |
| 理由 | 至少 8 个汉字，并出现段落、职责、依赖、题干/题解、证据顺序、保护边界、用户锁或收益等可定位对象 |
| 证据 | `evidence_refs` 不重复，全部命中冻结来源段，且两个 member 各至少一个 `{unit_id, paragraph_id}` |

8 个 reason code 是：

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

“候选已经审阅无需调整”“当前结构合理”“暂时不需要进行结构调整”不是理由，只是状态复述。即使
汉字数达到阈值，只要没有可定位对象也必须拒绝。合法 decline 的规范化记录进入
`structural_transaction_decline_results`；候选全集仍只能读取
`structural_transaction_candidate_dispositions`，不能拿“有一个 decline 结果”推断“所有候选已审”。

### 28.4 红队攻击面与固定裁决

本轮不是只补一个 happy path，而是围绕“怎样伪造候选已审”建立拒错矩阵：

| 攻击 | 固定裁决 |
|---|---|
| `READY` 候选只有两个普通 unit `NO_CHANGE` | 候选 `PENDING`，`REVIEW/2`，无正式发布 |
| 只有 decline，没有两个 unit bundle | 候选可 `DECLINED`，但 unit 仍 `PENDING`，总体不完成 |
| 伪造或不存在的 `STX-*` | 拒绝，不能占据 disposition |
| stale inventory SHA 或 transaction binding | 拒绝，不能占据 disposition |
| unit 顺序、chunk binding 或 Voice hash 漂移 | 拒绝 |
| 理由只有“已审阅、无需调整、结构合理” | 拒绝 `reason_not_specific` |
| evidence 只覆盖一侧 member | 拒绝 member coverage mismatch |
| evidence 指向未知来源段 | 拒绝 unknown ref |
| evidence 重复 | 拒绝 duplicate ref |
| 同一 ID 同时 execution 与 decline | 在正文 validator 前拒绝整批冲突 |
| 三 unit 链的两条重叠候选只处置一条 | 另一条仍 `PENDING`；共享 member 不自动清边 |
| decline 后省略 member 自身决策 | 不把 member 偷改成 `NO_CHANGE` |
| execution envelope 合法，但 fragment/DOCUMENT/repetition 失败 | disposition 仍 `EXECUTED`，两个 member 原子回滚为 `UNRESOLVED` |
| stale/伪造 execution | 不计 `EXECUTED`，不清除真实候选的 `PENDING` |

这组语义同时修复了两个相反风险：一方面不允许未处理候选静默消失；另一方面也不把“尝试执行但
后置失败”伪装成“模型根本没审阅”。disposition 记录审阅动作，unit 状态记录正文是否可接受，两者
不能互相替代。

### 28.5 LONG-25 与资格控制面

资格合同新增：

```text
LONG-25/transaction-candidate-disposition/v1
replay/LONG-25/transaction-candidate-disposition/v1
```

固定 replay 同时运行四条路径：两个 `NO_CHANGE` 但候选未处置、合法双侧证据 decline、execution 与
decline 冲突、stale decline。oracle 不只看顶层状态，还核对 candidate 四项计数、coverage、scope
complete、正式发布阻断和 decline schema。合同链升级为：

```text
contract=2026-07-17.14
requirements=2.7.0
oracle=1.7.0
atoms=185
```

无 manifest 审计仍是：

```text
evidence_integrity_status=PASS
qualification_status=NOT_EVALUATED
atoms_pass=0
atoms_fail=0
atoms_not_evaluated=185
exit_code=2
```

`PASS` 在这里只属于合同与证据完整性，不属于生成模型。当前 oracle catalog 仍是 SHADOW，本地 runner
最高只形成 E2；外部签名隔离、oracle 不可达证明、生产 E3/E4 和完整行为矩阵均未建立。见
[最终 no-manifest qualification](build/qualification-maturity-v24-20260717-no-manifest-final.json)。
该最终文件 SHA-256 为
`7896c34cc4aad0c1598b0b739e647f93e6a5cb5de4f74206b2d422295e1bb28c`，绑定的 Skill snapshot 为
`1b035a301db6583abf0c4ad6104a43fcdb3fb7b5030d5d5707dc606080e3085d`。

### 28.6 真实 physics 前向：一处改写加一条显式 decline

新前向没有复用 v23 的两个 `NO_CHANGE`。它从同一真实劈尖 TeX 局部稿重新 prepare，让 fresh 代理
自行处理两个 unit 和一个候选：

| prepare 指标 | 结果 |
|---|---|
| scene | `AUTO -> COURSE` |
| intensity / transaction scope | `STRUCTURAL / ADJACENT_PAIR` |
| 分块预算 | `max=1000 / min=200` |
| unit | 2 个，均为 `PENDING` |
| candidate | 1 个，inventory `READY` |
| protected spans | 119 |

代理对左 unit 提交 `NO_CHANGE`，对右 unit 提交带 unit 内 `structural_plan` 的 `REWRITE`，并为
`STX-d302740e480cf116946db684` 提交独立 decline：

> 左侧末段是第四明纹位移题的题干，右侧开头两段是其对应解答；跨单元搬动这些段落会打乱题干与
> 题解的顺序和对应关系

理由码为 `QUESTION_ANSWER_PAIRING_RISK`，证据分别命中左侧 `P012-6f8ce3a88e87` 与右侧
`P001-49e986382053`。原始 bundle 绑定两个 chunk/Voice；规范化验证记录保存 bundle SHA、transaction
binding、inventory SHA 和双侧证据覆盖。两份工件分别见 [raw decline](build/maturity-v24-20260717/forward-real-pair/pair-run/rewrites/STX-d302740e480cf116946db684.decline.json)
与 [validated decline](build/maturity-v24-20260717/forward-real-pair/pair-run/validation/STX-d302740e480cf116946db684.decline.json)。

机器终态为：

| 字段 | 值 |
|---|---|
| unit statuses | `1 DONE + 1 NO_CHANGE` |
| candidate dispositions | `total/executed/declined/pending = 1/0/1/0` |
| candidate coverage / scope complete | `PASS / true` |
| structural transactions / changes | `0 / 0` |
| structural semantic mapping | `PASS`，review `NOT_REQUIRED` |
| assembly / delivery / status / exit | `PASS / PASS / PASS / 0` |
| publish | `FINAL -> rendered/` |
| Voice / repetition / assembly replay | 均 `PASS` |
| source files modified | 0 |
| compile / fresh second pass | `NOT_RUN / NOT_RUN` |
| coverage completion claim | true |
| Humanize/full completion claim | false |

这里的正式 `rendered/` 是因为 transaction 被明确 decline，实际结构移动为 0，两个 unit 各自也完成；
它不表示整个原论文、整个 `physics1.tex` 或学术内容通过。source SHA 为
`8630c2be...31912`，rendered SHA 为 `2cade0a4...904a7`。完整状态见
[v24 finalization metadata](build/maturity-v24-20260717/forward-real-pair/pair-run/finalization_metadata.json)。

### 28.7 三行措辞变化的真实收益和残余

[unit diff](build/maturity-v24-20260717/forward-real-pair/pair-run/diffs/U-89353ebada63.diff) 只改了一个
题解中的三行：

| 原表达 | 改后 | 作用 | 残余问题 |
|---|---|---|---|
| “看上去在测长度，其实真正要写的是……也就是说” | “测的是长度，但求解先要确定……” | 删除表象/真相式主持壳和二次释义壳 | “但求解先要确定”搭配略紧，宜为“但求解时须先确定” |
| “这里空气劈尖取” | “空气劈尖取” | 删除无定位功能的主持词 | 无明显损失 |
| “这里不能把……” | “计算时不能把……” | 把泛指提醒改成操作环节 | 仍保留必要教学提醒，不应机械删掉 |

独立盲读者只拿 source A 与 rendered B，不读取 Skill、测试、报告或预期答案。它给出的评分是：

| 版本 | 自然度 | 清晰度 | 信息忠实度 |
|---|---:|---:|---:|
| A | 8.8 | 9.1 | 10.0 |
| B | 9.0 | 9.2 | 10.0 |

读者轻微偏好 B，认为“由条纹间距反求”更简洁，“计算时”比“这里”定位更准；同时明确指出
“但求解先要确定”略显紧缩。这个结论只是两稿内部的语言比较，不是物理正确性、公式正确性、数值
正确性或外部真人签名复核。完整记录见
[blind reader evaluation](build/maturity-v24-20260717/forward-real-pair/blind_reader_evaluation.md)。

### 28.8 最终回归、投影与可复现边界

最终自动验证从独立进程读取真实退出码，不再用 PowerShell 管道外层状态代替 unittest 状态：

- 20 个脚本逐个 `py_compile`，20/20 退出码 0；
- 20 个脚本逐个 `--help`，20/20 退出码 0，stdout 均非空；
- UTF-8 模式 official quick validator 返回 `Skill is valid!`；
- 全套运行 549 项测试，整体 `OK (skipped=2)`，即 547 项执行通过、2 项环境相关跳过；
- 四份主报告共审计 259 个本地 Markdown 链接和 11 个片段锚点，broken 为 0；
- 测试、结构验证和 projection PASS 均不改变 `academic_correctness=NOT_EVALUATED`、作者身份未验证和
  生成资格 `NOT_EVALUATED`。

final2 验证在测试前后对 68 个非缓存 Skill 文件做 SHA 快照，drift 为 0。unittest 原始 stderr
SHA-256 为 `955bcd293bc679de63ef894617f7251a86e7bfab351ca840ae2741f038514ed2`，验证摘要 SHA-256 为
`9844e1ee98031cb39854012d94bebb5c92b60d05bf299f3f6e5b886efdc06c1b`；96 个日志/结果文件的 SHA
台账自身 SHA-256 为 `fb23f6641221b06ff06e474c67d8ed4098247fb40a433febeb42497e53d2a5a1`。见
[final2 verification summary](build/maturity-v24-20260717/verification-final2-20260717-193217317/verification_summary.json)
与 [unittest log](build/maturity-v24-20260717/verification-final2-20260717-193217317/unittest.stderr.log)。

文档补登记 `structural_transaction_decline_results` 后，旧批准 hash 按预期使 builder fail closed；
只有更新批准能力 hash 后才能重新构建。最终两份 generator projection 各 30 文件并逐路径逐字节
一致，保留 decline schema、理由/双侧 evidence 校验、execution+decline 冲突拒绝、逐候选
disposition 和 `structural_transaction_decline_results`；`LONG-25`、oracle、auditor、qualification
replay 与 second-pass 控制面不进入生成投影。最终 capability/manifest/tree SHA 分别为
`80a4a6f729909ea1f78bef980125433e58e7c7329d9a5c9d88049a848ee3a1fd`、
`7c1fa2bfe7455f1b28601acf83f83948432b429bd4adf8891c9bbe7da61d17ee` 和
`2768ec439ac91674d7dbfe6d46b6c7267b9659f7f2a687bd1328d9cbf7035e64`。两份 projection 各
881,603 字节，见 [final2 A manifest](build/generator-projection-maturity-v24-final2-20260717.manifest.json)
与 [final2 B manifest](build/generator-projection-maturity-v24-final2-repro-20260717.manifest.json)。
报告链接结果见 [final link audit](build/maturity-v24-20260717/markdown-link-audit-final.log)。

### 28.9 当前成熟度裁决

v24 可以支持一个比 v23 更严格的结论：**相邻双 unit 候选的机械权限、执行、明确拒绝和未处置状态
已经形成可重放闭集；系统不再把两个 member 的 `NO_CHANGE` 偷换成候选边已审。** 真实 physics
前向同时给出一处小幅文风收益和一条有双侧证据的 decline，说明新合同能承载“不改结构但改局部
措辞”的正常选择。

它仍不能支持以下说法：

1. 不能说生成模型已通过 185 原子资格矩阵；当前是 `0/185`、`NOT_EVALUATED`；
2. 不能说 `physics1.tex` 全文已经 Humanize；真实 run 只是 2-unit 局部稿，completion claim=false；
3. 不能说物理、公式、数值、引用或学术正确性已验证；compile 和外部内容审查均未运行；
4. 不能说个人作者 Voice 已证明；本次使用 COURSE 默认 profile；
5. 不能说所有改句都自然；“但求解先要确定”仍是明确残余；
6. 不能把独立代理盲读写成外部真人 E4 或签名审批；
7. 仍不支持超过两个 unit、非相邻、跨文件、跨标题、标题解锁、拆段或整段删除。

因此当前最准确的定位是：**确定性保护、候选处置和拒绝虚假完成的工具链已接近生产稳定；小范围
真实改写已有轻微正证据；生成器总体资格、学术正确性、作者身份与无人值守全文交付仍未完成。**

## 29. 2026-07-17 v25：从“机械候选通过”拆到“质量待审、事务可恢复”

### 29.1 先纠正 v24：`PASS/0 -> rendered/` 不再是合法质量终态

本节对第 28.6、28.8、28.9 节的历史结论作明确覆盖。v24 的 physics 局部 run 在 transaction 已
decline、两个 unit 均达到机械终态后得到：

```text
candidate assembly=PASS
delivery=PASS/0
publish=FINAL -> rendered/
```

这条结果当时只想表达“覆盖、保护、结构和候选 disposition 已闭合”，但机器状态仍把它写成了
顶层正式交付。随后同范围盲读指出改句“但求解先要确定”搭配紧缩。它没有破坏公式、数字、TeX、
否定、模态或词项门，因此旧 validator 和 finalizer 都无法阻断。这个反例证明：

1. 机械不变量通过，不等于改后搭配自然；
2. high 词项下降，不等于每处变化都有独立收益；
3. transaction decline 只关闭结构候选边，不证明两个 unit 的措辞质量；
4. fresh second pass 的 `NO_CHANGE` 也不能证明第一稿优于原稿；
5. `NO_CHANGE` 本身不能自证“原文已经自然”。

因此 v25 不再允许普通 `REWRITE/NO_CHANGE` 由本地工具进入正式 `PASS/0`。v24 报告中的
`FINAL -> rendered/` 仅保留为 pre-fix 历史证据，不能再作为当前合同或生产行为引用。

### 29.2 五层状态机：组装、机械、成对质量、稳定性、交付

v25 把此前混在一个 `PASS` 里的判断拆为五层：

```text
candidate assembly
-> mechanical validation
-> paired-quality review
-> second-pass stability
-> delivery gate
```

普通机械有效的 `REWRITE` 或 `NO_CHANGE` 当前固定为：

```text
candidate_assembly_status=PASS
mechanical_validation_status=PASS
paired_quality_review_status=PENDING_EXTERNAL_REVIEW
delivery_gate_status=REVIEW
exit_code=2
publish_state=REVIEW_CANDIDATE
humanize_quality_claim_allowed=false
humanize_completion_claim_allowed=false
```

这不是把所有正常改写降成“失败”。`candidate_assembly_status=PASS` 仍说明候选可组装、硬保护和已编码
机械门没有失败；`REVIEW/2` 只说明自然度、搭配、段落职责、逻辑层级和逐改句收益没有可信外部
clearance。完整候选进入 `rendered_review/`，既不丢失工作，也不冒充正式稿。

paired-quality 与结构语义是两道正交门：

| 变化类型 | 机械结果 | 仍需的外部门 | 当前发布 |
|---|---|---|---|
| 普通措辞 REWRITE | validator mechanical PASS | paired-quality | `rendered_review/` |
| NO_CHANGE | 字节未变、request `changes=[]` | paired-quality，确认无稳定收益改动 | `rendered_review/` |
| unit 内 STRUCTURAL | plan 与 validator PASS | structural semantic + paired-quality | `rendered_review/` |
| 相邻双 unit transaction | 两 fragment、DOCUMENT、原子 gate PASS | pair semantic + paired-quality | `rendered_review/` |
| 任一 request 缺失 | assembly 可 PASS | quality gate `BLOCKED` | `rendered_review/`，不得正式发布 |

### 29.3 `humanize-paired-quality-review-request/v1` 的可复核内容

统一验证器现在为每次 `REWRITE` 生成成对请求，`NO_CHANGE` 也不例外。请求至少绑定：

| 组 | 绑定内容 |
|---|---|
| artifact | 完整改前、改后 SHA-256 |
| context | mode、decision、scene、document format、FRAGMENT/DOCUMENT scope、mechanical status |
| policy | validator、invariant checker、scanner、lexicon SHA-256 |
| changes | 每个 hunk 的 ordinal、operation、改前/改后行区间、行数、汉字数、block SHA 和 change ID |
| review contract | `ACCEPT/REVISE/REVERT` 三 verdict 与 9 个质量维度 |
| limitations | academic correctness、authorship 均未评估，quality clearance=false |
| request identity | 对除自身外完整 canonical request 计算 SHA-256 |

9 个质量维度包括病灶是否仍在、NO_CHANGE 是否为最佳安全决策、问题跨度绑定、独立读感收益、
主谓修饰、动宾搭配、逻辑关系、信息密度与节奏、作者声线非回退。它们不是新的打分器，而是未来
可信外部 reviewer 必须逐 change 回答的最低合同。

资格 auditor 对 DEC-09 不再只看自哈希和两个 artifact SHA。v25 后修复又加入 exact-schema：顶层
9 个键、artifact/context 键集、完整 policy hashes、limitations 三字段、3 个 verdict、9 个维度和
3 个 false-clearance 语义全部闭集比对。以下四种篡改即使重算 request SHA 也必须拒绝：

- 添加未知 `clearance=true`；
- limitations 内加入与 `quality_clearance_granted=false` 矛盾的声明；
- 删除或替换 `REVISE/REVERT` verdict；
- 删除、重命名或追加 required dimension。

### 29.4 EOL、BOM 和 transaction 孤儿 request

请求的 hunk 不能先把文本规范化后再比较。旧实现使用 `splitlines()`，会把 CRLF/LF 差异和部分末尾
换行变化吞掉；BOM-only 改动也可能被误写成 `NO_CHANGE`。v25 改为：

- 完整决策先由原始 artifact SHA 裁决；
- hunk 使用保留行终止符的 `splitlines(keepends=True)`；
- BOM、CRLF/LF 和末尾换行均能产生非空 change record；
- before/after block hash 对真实 UTF-8 字节计算，不再静默归一化。

结构 transaction 还暴露了一处原子性缺口：第一 fragment 已持久化 paired request，第二 fragment
失败后，request 尚未加入公共字典，旧清理函数因“没有 record”直接返回，留下孤儿
`PENDING_EXTERNAL_REVIEW` 文件。修复后清理函数同时按 canonical unit 文件名删除 staged request，
不再依赖公共 record 已建立。FRAGMENT、DOCUMENT 和后置 repetition 回滚都保持“两个 member 的
request、diff、DONE、review record 全有或全无”。

### 29.5 缺 request 的 P0：`BLOCKED` 不能再被 delivery 漏掉

故障注入把 `_persist_paired_quality_review_request` 替换为返回 `None`。中间实现得到：

```text
paired_quality_review_request_coverage_status=REVIEW
paired_quality_gate_status=BLOCKED
paired_quality_units_missing=1
```

但 delivery block 只识别 `PENDING_EXTERNAL_REVIEW`，仍可能发布正式 `rendered/`。这是 P0：系统
已经知道质量证据缺失，却把候选写成正式稿。

修复后 `PENDING_EXTERNAL_REVIEW` 与 `BLOCKED` 都阻断正式交付。缺 request 时仍允许保留机械候选，
但顶层固定 `REVIEW/2`、`REVIEW_CANDIDATE`，`humanize_completion_claim_allowed=false`。这条路径
另有专门测试，不能由正常 happy path 间接覆盖。

### 29.6 run-dir 发布事务：不再混合 A 的证据和 B 的 metadata

v25 后修复把整次 finalize 包成 run-dir 级事务。持有 `.finalize.lock` 后，先复制全部非 transient
工件，并核对：

```text
copy_before_hashes == copy_after_hashes == backup_hashes
```

run-dir 自身及内部工件的 symlink、junction/reparse point 和多链接文件会在备份前拒绝，防止把
外部目标或共享 inode 当成可恢复基线。发布顺序中的 rendered、validation、diff、最终 ledger、
manifest、rollback 和 metadata 任何一步抛异常，都会恢复调用前字节。

故障注入覆盖四种 evidence commit 组合：

| 原状态 | 失败点 | 必须结果 |
|---|---|---|
| 首次发布 | 第一个 evidence commit | 无 rendered/validation 半提交；恢复 prepare 状态 |
| 首次发布 | 第二个 evidence commit | 已移动的第一个目录回滚；无孤儿 ledger/metadata |
| 替换 review candidate | 第一个 commit | 旧 rendered、证据、metadata 逐字节保留 |
| 替换 review candidate | 第二个 commit | 新 rendered 替换回滚，旧完整证据恢复 |

另一个真实混代场景是：A 候选已发布，B 候选产生新 paired request 后编译失败。旧实现保留 A 的
`validation/`，却覆盖 `finalization_metadata.json` 为 B 的 request SHA，并继续给出 A 的相对路径。
v25 修复后：

- canonical `finalization_metadata.json`、`validation/`、`diffs/` 和 `rendered_review/` 仍精确属于 A；
- B 只写 `last_failed_attempt_metadata.json`；
- B 的 request SHA 可留作诊断，但 `path=""`；
- `failed_attempt_evidence_status=NOT_RETAINED_AFTER_ROLLBACK`；
- `failed_attempt_evidence_paths_reusable=false`；
- 下游不得把 B 的 hash 重新指向 A 的 canonical 文件。

运行期异常与普通失败尝试也统一使用这套 schema。畸形 rewrite JSON、commit `OSError` 等都会输出
结构化 `FAIL/1`，并带 `failed_attempt=true`、恢复状态和证据失效字段。只有参数语法错误仍由
argparse 输出 usage/error 和退出码 2，避免无 JSON 的基础设施异常冒充正常 `REVIEW/2`。

### 29.7 `check_command`：一次性副本之外还要收拢后台进程树

只在 `.compile_check_staging/` 运行命令并做返回前 hash 仍不充分。命令可以启动 detached child，
直接 shell 先退出；子进程等 `rendered_review/` 出现后再写入。红队已复现旧路径：

```text
compile.integrity_status=PASS
run_artifacts_changed_during_check=false
finalize 已返回
rendered_review/main.tex -> LATE_POISON
```

Windows 修复使用一个受控 wrapper：wrapper 在收到命令前不生成用户子进程；主进程先把 wrapper
加入启用 `KILL_ON_JOB_CLOSE` 的 Job Object，再经 stdin 发送命令。wrapper 返回后终止整个 job，
然后才计算 staging、evidence 和 run-dir hash。结果新增：

```text
compile_check.process_containment=WINDOWS_JOB_OBJECT
compile_check.descendant_cleanup=PASS
```

专门测试启动 detached child，延迟等待正式目录后写入；finalizer 返回后继续等待，正文仍保持原
字节。绝对路径直接污染旧 `rendered_review/` 的路径也会触发 run-dir hash 差异，外层事务恢复 A。
POSIX 分支使用独立 process group；文档明确它不是通用恶意代码沙箱，caller 仍应只传项目现有、
同步结束的构建命令。

### 29.8 候选队列不再把 REVIEW 当 rejected

paired-quality 上线后，来源动作候选的 action contract、复制门和模板门可以机械通过，但统一
validator 顶层仍是 `REVIEW/2`。旧队列只有 `accepted/` 与 `rejected/`，于是“等待外部质量复核”
被错误存入 rejected，既不等于硬失败，也无法形成清楚的待审 head。

v25 最终队列改为三态：

| 顶层状态 | queue disposition | head |
|---|---|---|
| `PASS/0` | `ACCEPTED` | `accepted/` |
| `REVIEW/2` | `PENDING_REVIEW` | `review/` |
| `FAIL/1` | `REJECTED` | `rejected/` |

三个 head 互斥，共用同一不可变 candidate/evaluation/run 历史。修订候选必须带 lineage；发布时先
备份旧 head，再原子提交新 candidate/result 和 immutable history，最后删除其他两个 bucket 的旧
head。并发 24 次相同候选只允许至多一次非幂等首发，其余均识别为同 evaluation rerun。长 Windows
路径继续使用短 storage key，review bucket 也受 reviewer label 脱敏和事务回滚保护。

### 29.9 真实同范围前向：C 优于 B，但仍不是 clearance

v25 从 v24 同一劈尖局部源稿重新给出 candidate C，并运行统一 validator。机器结果为：

| 字段 | 值 |
|---|---|
| before SHA | `8630c2be...31912` |
| after SHA | `748381d5...829e` |
| hard/speech/style | `PASS/PASS/PASS` |
| mechanical | `PASS` |
| paired-quality | `PENDING_EXTERNAL_REVIEW` |
| delivery / exit | `REVIEW/2` |
| request SHA | `b7daa009...b51a` |
| academic correctness | `NOT_EVALUATED` |

证据见 [paired-quality validation summary](build/maturity-v25-20260717/forward-clean/paired-quality-validation-summary.json)。同目录的
`decision.json` 已同步为分层状态：`mechanical_validation_exit_code=0`，顶层
`delivery_gate_exit_code=2`、`PENDING_EXTERNAL_REVIEW`；`paired-quality-validation-summary.json` 是当前
顶层状态的权威工件，避免把机械退出码误读为交付退出码。

同范围盲读只看 A/B/C 正文，排序为：

```text
C > B > A
```

C 去掉了 B 的“但求解先要确定”，改为从“求细丝直径时”直接进入几何关系与条纹间距反求斜率，
层级更清楚；A 的“看上去……其实真正……也就是说”则制造假对立和重复解释。盲读仍提出四项
局部建议，包括“这里不能”改为“计算时不能”、补充 (l=\lambda/(2n\alpha)) 的教学展开、把
“空气劈尖取 (n=1)”写得更准确，以及解释第 1 至第 30 条明纹为何是 29 个间距。后两类涉及
教学或物理展开，只记录为建议，`academic_correctness` 继续 `NOT_EVALUATED`。完整记录见
[A/B/C blind reading](build/maturity-v25-20260717/forward-clean/blind-local-abc-evaluation.md)。

这条正证据只说明 C 在同一局部对比中更自然；评审不是外部签名服务，不能把
`paired_quality_clearance_granted` 改成 true。

### 29.10 资格矩阵从 185 扩到 188，但仍是 0 项已评估

资格合同升级为：

```text
contract=2026-07-17.15
requirements=2.8.0
oracle catalog=1.8.0
atoms=188
```

新增原子为：

- `DEC-09`：机械 PASS 后必须生成 exact-schema paired-quality request，不能本地自清；
- `LONG-26`：所有可编辑 unit（含 NO_CHANGE）都有 request，完整候选只进 review namespace；
- `LONG-27`：paired-quality pending 的 review candidate 不能由 fresh second-pass receipt 升级。

oracle 绑定 evaluation contract SHA
`88c792e3afcb8d3da310d12d253afc842df68a0f7cc31c25557f1a004a1e68ae`；最终 oracle SHA 为
`283aa6931b81ae444d2a1d6bcd26e07f5d4d6715eaa6581231c9f3b7087ecc35`。没有外部签名 manifest 时，
最终审计严格保持：

```text
evidence_integrity_status=PASS
qualification_status=NOT_EVALUATED
atoms_pass=0
atoms_fail=0
atoms_not_evaluated=188
exit_code=2
```

见 [v25 no-manifest qualification](build/qualification-maturity-v25-20260717-no-manifest-final2.json)，
文件 SHA-256 为 `dfb2a0c5b6814769a84eda86d762c42a44daa23fec2adbbdffe7be9098c43fbc`。
这里的 integrity PASS 只证明当前 requirements/oracle/trust/projection 能被重建，不证明模型完成任何
一个行为原子。

### 29.11 最终回归与 generator projection

最终验证结果：

- 全套 572 项测试，`OK (skipped=2)`，即 570 项执行通过、2 项环境相关跳过；
- validator + finalizer 定向共 158 项，全部通过；其中 finalizer 96 项；
- 20 个 Skill 脚本逐个 `py_compile`，20/20；
- 20 个脚本逐个 `--help`，20/20；
- official `quick_validate.py` 返回 `Skill is valid!`；
- no-manifest qualification 为 `0/188 NOT_EVALUATED`；
- 两份 generator projection 都是 30 文件，路径集合和逐文件字节完全相同。

builder 与 policy 同步升级为 `1.8.2`。最终 projection 标识为：

| 项 | SHA-256 |
|---|---|
| capability source | `95694c8d5120be6ea70b97feed71ebc8f0960a0a5f098a20a205d3c3f64a74eb` |
| evaluation surface | `7681d0f4d0102aac6399b1d46e801d815e21c883a4b02311f7e4928c4aeb4b06` |
| inventory | `73945d96fd3a02a342ebc471c296e8be22ee49d04be34c397a38daa2b7a5ae52` |
| manifest | `a25442bf2459e217b930029a2425f418c468f7f15a7aa9b862f8d33266425fb2` |
| projection tree | `c68dd7105f63c983f8f0a9ca5a7301b5d92507c2628c5633176a5b4e5cdd16ee` |

两份 manifest 分别为 [final2 A](build/generator-projection-maturity-v25-final2-20260717.manifest.json)
和 [final2 B](build/generator-projection-maturity-v25-final2-repro-20260717.manifest.json)。projection 保留
paired-quality request、review-only 发布和 run-dir 事务等生成/收尾能力；三态候选队列只存在于安装版
审计面，投影仅保留说明性合同，不包含 `validate_humanize_candidate_queue.py`。oracle、requirements、
auditor、runner、sealer、qualification replay 和 second-pass 控制面仍不进入生成器。

### 29.12 v25 成熟度裁决

v25 可以支持的结论是：

> 工具链现在能区分“候选可机械组装”与“改后质量已获可信复核”，能为每次变化生成可重放的成对
> 请求，能在发布失败、失败重跑、绝对路径污染和后台进程残留时恢复 canonical 工件，并能把
> PASS/REVIEW/FAIL 候选存入互斥队列 head。

它仍不能支持“成熟自动 Humanizer”或“生产级无人值守全文改写器”的说法，原因不是谦虚措辞，而是
明确缺少以下证据：

1. 没有代理不可伪造的外部 paired-quality response 签名与验签服务；
2. 188 个生成资格原子仍是 `0 PASS / 188 NOT_EVALUATED`；
3. 本地 runner 最高 E2，不能证明宿主 oracle、完整 Skill、用户 profile 或工作区不可达；
4. academic correctness、公式推导、数据、引文和作者身份均未评估；
5. 真实正证据仍是一个局部 physics 范围，且盲读继续提出局部改进；
6. POSIX process-group 不是通用恶意代码沙箱，`check_command` 仍须来自可信项目构建流程；
7. 超过两个 unit、非相邻、跨文件、跨标题、标题解锁、拆段和整段删除仍没有自动生产权限；
8. 当前本地工具不消费外部 clearance，因此正常 REWRITE 的顶层状态有意保持 `REVIEW/2`。

因此最新定位是：**这是一个成熟度较高的 fail-closed 中文学术文风候选生成与审计工具链，已经能
可靠拒绝多类虚假完成态；但它还不是获得外部质量资格的自动改写器。**

## 30. 2026-07-18 v26：入口口径与证据权威性收紧

### 30.1 这次修复的实际问题

v25 的执行链已经把普通 `REWRITE/NO_CHANGE` 固定为 `REVIEW/2`，但入口文本仍有三类会误导调用方的
表述：`CLEAN` 被称作“可直接使用”，默认 `REWRITE` 被称作“直接交付正文”，维护注释仍只列
`accepted/rejected` 两态。v26 将它们统一改成“正文置前的待审候选”，并在 Skill 元数据中把“终审工具”
收窄为“终审辅助、候选生成与机械审计工具”。这不是措辞偏好，而是防止调用方绕过 paired-quality
门的执行安全修复。

### 30.2 证据与投影重新登记

Skill 本体变更后，旧 projection policy 正确拒绝了未登记的 capability hash。v26 没有绕过该拒绝，而是
把 policy/builder 升到 `1.8.3`，登记新的闭集 capability hash，再分别重建 A/B projection。两份 manifest
的核心结果为（完整指针见 [humanize-academic-authority-v26-20260718.json](build/humanize-academic-authority-v26-20260718.json)）：

| 项 | v26 值 |
|---|---|
| capability source | `30e9cb7d5da4cb85b269ab97ed67ce568b139b0ff499250cfeef78ca5c489d3d` |
| evaluation surface | `9d04a698cc3ad8caaff2579f363308aa61ca666e77689f0957bd2836a1da5e50` |
| inventory | `4fdc2426be915b1a03ed7d3f6f7359180cb3cbb2099e37cc6b8306713f17a600` |
| policy | `1.8.3`, canonical `7627c15a2c0a8952b6a7cf46ce8d8490356c949bc4e8ae8cfa6b2991161c5b9e` |
| A/B manifest | `e14fe7b3ce25f8975dd06d43a06b7a1c0f1bf7388d7273c263eb75a2fe5bc514` |
| A/B projection tree | `22616b947a1287e8c48cff3e3479c964eae3ac849dccf9ec3a28d8254ea82b66` |
| projection | 两份各 30 文件，路径/字节完全一致，证据上限 E2 |

三态候选队列仍只在安装版审计面；projection 不包含 `validate_humanize_candidate_queue.py`。这条边界在
报告中单独写明，避免把“安装版有队列”误读成“生成器上下文带着队列能力”。

### 30.3 candidate C 的退出码分层

v25 `forward-clean/decision.json` 曾把 mechanical exit `0` 写进顶层 `validator_exit_code`，而同一
before/after 的权威 paired-quality summary 已是 `REVIEW/2`。v26 在当前 `1.8.3` policy 下重放同一
candidate，得到新的 request SHA `e5d815af17cae704951de231638f9065320443e6a67f3542448fccd16d5e52af`；
旧 `b7daa...` 只保留为 v25 policy 的历史 request。当前摘要见
[paired-quality-validation-summary-v26-rerun.json](build/maturity-v25-20260717/forward-clean/paired-quality-validation-summary-v26-rerun.json)，其 SHA-256 为
`34ada9053b3594b458e3410393514a982b8546e787450e47b4a1b6a36d16e844`。
v26 将 decision record 分层为：

```text
mechanical_validation_status=PASS
mechanical_validation_exit_code=0
paired_quality_review_status=PENDING_EXTERNAL_REVIEW
delivery_gate_status=REVIEW
delivery_gate_exit_code=2
publish_state=REVIEW_CANDIDATE
```

并显式绑定 `authority_artifact=paired-quality-validation-summary-v26-rerun.json`。这保证机械门通过不会覆盖顶层
交付裁决，也让复核者能从同一候选的 before/after SHA 重放状态。

### 30.4 v26 回归结果与已知证据缺口

- 全套 `python -m unittest discover -s tests -p 'test_*.py'`：573 项，`OK (skipped=2)`；
- 新增入口口径反向测试：禁止 `可直接使用/直接交付正文/终审工具/已完成所列范围`，要求明确
  `待审候选`、机械验证和 paired-quality 状态；
- [v26 no-manifest qualification](build/qualification-maturity-v26-20260718-no-manifest.json)：`evidence_integrity_status=PASS`、`qualification_status=NOT_EVALUATED`、
  `0 PASS / 0 FAIL / 188 NOT_EVALUATED`、退出码 `2`。JSON SHA-256 为
  `232a4ac32d6dbec287770088352f6e2a28b009a3437e0a13e0ce949d9475d2da`；
- 报告链接审计覆盖 309 个本地链接和 18 个 Markdown 片段锚点，当前均可解析；乱码文件仍按既定边界跳过；
- 当前仍没有代理不可伪造的外部 paired-quality clearance；candidate C 的完整 request 原件未单独归档，只有
  request SHA 出现在权威 summary/decision；全套测试的原始 stdout 也未作为独立日志文件持久化。因此本节的
  测试结论以本轮命令输出和计数为依据，不把缺失原始日志包装成可独立重放的日志证据。

### 30.5 v26 裁决

v26 让“入口说什么”和“状态机实际允许什么”一致，并把 projection、candidate decision 和资格审计的
权威关系写清楚。它提高的是调用安全、证据可读性和回归可发现性；没有提高生成资格本身。当前仍只能说：

> Skill 是一个有严格拒错、待审候选、事务恢复和证据分层的中文学术文风工具链；它仍不是已获外部质量
> 授权的自动 Humanizer，188 个生成原子仍未评估，学术正确性和作者身份仍不在本工具证明范围内。

## 31. 2026-07-18 v27：短文证据包与外部 paired-quality 验签边界

### 31.1 直接验证结果不再只存在于 stdout

v26 之前，`validate_humanize_output.py` 会在 JSON 输出中给出完整 paired-quality request，但普通短文调用
没有可靠的持久化入口。v27 新增 `--evidence-dir <不存在的目录>`，以同卷 staging 和原子 rename 保存：

```text
validation-result.json
paired-quality-review-request.json
evidence-manifest.json
```

manifest 绑定 before/after SHA、request SHA、顶层状态、退出码和目录内每个工件的 SHA-256，并在提交前
重新读取来源文件。目标已存在、来源在验证后变化、路径经过 symlink/reparse point 或中途写入失败时，
统一返回结构化 `FAIL/1`，不留下半包，也不把原本的 `REVIEW/2` 冒充为已持久化成功。该包证明的是
“当前验证结果与当前字节绑定”，不是外部质量授权；它仍未保存 invocation 原件、stdout/stderr 原件或
before/after 内容副本，也没有 content-addressed 一次性消费账本。

### 31.2 外部 response verifier 的 P0 修复

v27 增加安装版审计 verifier，使用严格 JWS Compact 和 Ed25519 检查外部 paired-quality response。首轮
实现仍有一个可被红队直接利用的 P0：`review_record_sha256` 只检查是否为 64 位十六进制，攻击者可以填
全 `a` 占位符，在其他字段通过时获得 paired-quality PASS。当前实现改为必须同时提供真实
`humanize-paired-quality-review-record/v1` 工件，并逐项绑定：

- exact request SHA、challenge SHA 和 response ID；
- 与 request/response 完全相同的 change target 集合；
- 每个 target 的 `problem_span`、`reading_effect` 和 `decision_rationale`；
- review record 原始字节与签名 payload 中 `review_record_sha256` 的一致性。

缺 record 为 `REVIEW/2`；字节哈希、request、challenge、response 或 target 错绑为 `FAIL/1`；
“已人工审核、符合要求、更自然、没有问题”等空泛理由固定为 `REVIEW/2`。`NO_CHANGE` 不允许空数组
真空通过，必须使用唯一合成 target `NO_CHANGE`，并解释为什么继续改写没有可定位收益。

verifier 还拒绝 `alg=none/HS256/ES256`、重复或未知 JSON 键、非 canonical base64url、NaN/Infinity、
未知/退休/撤销 key、超时或 future response、TTL 越界、trust epoch 漂移、部分/额外/重复 target、
artifact 漂移和不安全路径。质量维度缺失属于“反馈未完成”，按合同返回 `REVIEW/2`；伪造签名、绑定
错误和未知字段属于硬完整性失败，返回 `FAIL/1`。在 grant 前还会再次逐字节读取
request/challenge/response/keyset/anchor/review record 和 before/after；故障注入在最终重读时改动 request
或正文，均得到漂移 `FAIL/1`，不会用内存中的旧检查覆盖磁盘新状态。

### 31.3 信任根没有被本地自签绕过

普通 `--trust-anchor`、仓库 keyset、调用方 `HUMAN` 标签和环境变量内容都不自动构成信任根。独立
launcher 必须固定 anchor 路径，并由宿主证明该 anchor 受 ACL/所有权保护。当前标准库实现对 POSIX 只接受
所有者可控且 group/world 不可写的 anchor；Windows 不根据 mode bits 猜测 ACL，默认返回
`UNPROTECTED_TRUST_ANCHOR -> REVIEW/2`。测试中的 external-anchor PASS 使用显式 mock 表示未来受保护
launcher 边界，不证明当前 Windows 机器已经部署了该边界。

因此本轮可证明两件不同的事：

1. 有效签名但无可信 anchor 时，`cryptographic_signature_status=PASS`，但
   `paired_quality_clearance_granted=false`、`REVIEW/2`；
2. 测试夹具中的受保护 anchor、完整 review record、全 change/9 维 PASS 可以得到 paired-quality
   `PASS/0`，但 `academic_correctness`、authorship、Voice、结构语义和 second-pass 仍为独立未评估门。

当前 verifier 没有接入 `validate_humanize_output.py` 或长文 finalizer 的原子发布事务；本地也没有真实外部
审批服务、代理不可访问私钥、在线一次性 redemption、最高 keyset sequence 受保护台账或 Windows ACL-aware
launcher。故普通生产路径仍保持 `PENDING_EXTERNAL_REVIEW -> REVIEW/2`。

### 31.4 v27 回归、projection 与资格状态

最终机器验收：

| 项 | v27 结果 |
|---|---|
| 全套测试 | 598，`OK (skipped=3)`；595 执行通过 |
| paired-quality verifier 专项 | 23，22 通过；1 个 Windows symlink 权限跳过 |
| direct validator 专项 | 64/64 |
| Skill scripts | 21/21 `py_compile`，21/21 `--help` |
| official quick validator | `Skill is valid!` |
| projection policy/builder | `1.8.4` |
| A/B projection | 各 30 文件，路径和逐文件字节完全一致 |
| qualification | `0 PASS / 0 FAIL / 188 NOT_EVALUATED / exit 2` |

v27 projection 标识：

| 项 | SHA-256 |
|---|---|
| capability source | `e3101d315c380d526390aa9193b103986a68e25fc37e974c0d9c3f8d7698b4bf` |
| evaluation surface | `c5cde4241477e0f7f811b47a73438fac2cc0f999f40310dfa4095baa0fcb4645` |
| source inventory | `481f0439f32e3f751fbaf37335dd59abbc23db81ebf1a1bdbebc488736765cd0` |
| policy canonical | `37bc0e3d383463e6b9bd972c6e519b3c8ebe7f205b229df41fbad503c707bf12` |
| A/B manifest | `7cb6d0b8b9ea9079335958c3bc84e92f674deae4a315a8946bc36861b96ee6e4` |
| A/B tree | `ba9f2fe6c7e4a41d960f2cdcf815c8762285b3826e3b8dd22e3e0f15ba824e0b` |

两份 manifest 分别为
[v27 final A](build/generator-projection-maturity-v27-final-20260718.manifest.json) 和
[v27 final B](build/generator-projection-maturity-v27-final-20260718-repro.manifest.json)。clearance 合同和 verifier 被明确
归入安装版 evaluation surface，不进入 30 文件生成 projection；投影内也不出现它们的 basename 或命令。
本轮权威摘要见 [v27 authority pointer](build/humanize-academic-authority-v27-20260718.json)。

[v27 no-manifest qualification](build/qualification-maturity-v27-20260718-no-manifest-final2.json) 的 SHA-256 为
`c15bdb6b626b538f44ae55050835eb98b4ff29055e8ce3b0aff67d05babf5233`。报告内部状态为
`evidence_integrity_status=PASS`、`qualification_status=NOT_EVALUATED`、`0/188`、退出码 `2`。这里的
integrity PASS 只证明合同、requirements、oracle、trust policy 和 projection 可重建，不证明任何生成原子。

### 31.5 v27 裁决

v27 让短文 request 可以原子归档，也把“外部审阅者说通过”拆成签名、信任根、逐 change 维度、具体理由
和当前 artifact 五层绑定；本地自签、占位哈希、空泛理由和部分维度都不能形成虚假闭环。可以据此称为
更成熟的 fail-closed 候选生成与审计工具链。

仍不能称为成熟的无人值守自动 Humanizer。真实外部审批服务和 Windows 受保护信任根尚未部署，外部
clearance 尚未进入 finalizer 发布事务，188 个生成资格原子仍全部未评估，学术正确性、作者身份和跨文体
长期稳定性也没有被本轮测试证明。

## 32. 2026-07-18 v28：短文验证记录的自包含重放

### 32.1 本轮解决的不是“多存几个 JSON”

v27 的 `--evidence-dir` 能原子保存验证结果、paired-quality request 和 manifest，也能在提交前重读
before/after。它证明“这三个文件在一个目录里相互绑定”，却不能回答以下问题：

1. 原始 before/after 删除后，能否只靠证据目录重跑 validator；
2. 当时使用了哪些 CLI 参数、保护术语、KEEP 理由、fragment/report-scope 配置；
3. stdout、stderr 与 `validation-result.json` 是否对应同一结果；
4. 同一次调用再次发布是幂等，还是会被误判为冲突；
5. report-scope JSON 和 detector report 原件是否随记录冻结；
6. 当前 validator、scanner、lexicon 或运行时变化后，系统会不会用新策略伪称旧记录已重放；
7. reviewer proposal 因隐私规则不保存原 reviewer ID 时，系统会不会伪造一个 ID 继续重跑。

因此，v27 更准确的名称是“原子验证摘要包”，不是“可独立重放的验证记录”。v28 将这一区分写进
schema、代码、测试和报告，不再用 manifest 自哈希替代真实重执行。

### 32.2 v2 证据目录

`validate_humanize_output.py --evidence-dir <DIR>` 现在提交以下闭集：

```text
<DIR>/
  inputs/
    before.bin
    after.bin
    report-scope.json        # 仅 REPORT_INFORMED
    report.bin               # 仅 REPORT_INFORMED
  invocation-request.json
  validation-result.json
  paired-quality-review-request.json  # REWRITE 时
  warning-review-request.json         # 有 warning 时
  rendered-output.txt
  stderr.txt
  execution-record.json
  evidence-manifest.json
```

`invocation-request.json` 保存 mode、scene、output format、strict-speech-acts、fragment、保护术语、
KEEP 理由、warning proposal、request SHA 和 report-scope 归档位置。原 reviewer ID 不保存，只保存
`reviewer_id_sha256`；只要存在 proposal，调用就标为 `REEXECUTION_NOT_SUPPORTED`，而不是编造身份标签。

输入记录同时保存归档相对路径、原文件名/后缀、原路径 SHA、内容 SHA 和大小。原路径 SHA 用于绑定
调用身份，不是路径匿名化；`validation-result.json` 仍可能含绝对路径和正文上下文，因此整个目录固定
标记 `contains_source_content=true`，不能当作可公开日志。

`execution-record.json` 保存 intended exit、stdout/stderr SHA 和三项限制。它明确写
`process_exit_observation=NOT_EXTERNALLY_OBSERVED`：进程内代码不能独立证明操作系统最终返回给父进程的
exit code，尤其不能忽略 broken pipe 或宿主终止。v28 没有把“计划返回 2”包装成“外部已观察到 2”。

### 32.3 内容寻址与发布事务

`invocation_sha256` 对规范 invocation body 求 SHA-256，`run_id` 固定为
`hvr1-<invocation_sha256>`。它绑定输入字节、全部可复现参数、路径假名、policy 快照和预期裁决。
`record_sha256` 再绑定除 manifest 外全部工件的精确大小与 SHA；manifest 有规范 JSON 自哈希。

发布仍使用同卷 staging、排他写、文件 `fsync`、发布锁和目录 rename，但 v28 增加了以下裁决：

| 情形 | 裁决 |
|---|---|
| 目标不存在、全部重读一致 | 原子发布 |
| 目标已存在，run ID、清单、文件和字节完全一致 | 幂等成功，不改旧字节 |
| 同一目标出现不同调用或不同字节 | `FAIL/1`，旧目录保持原样 |
| 缺文件、额外文件或额外目录 | `FAIL/1` |
| before/after/scope/report 在提交前漂移 | `FAIL/1`，清理 staging/lock |
| 输入或证据文件为 hardlink | `FAIL/1` |
| 路径经过 symlink/reparse point | `FAIL/1` |
| 任一 staged write、manifest write 或 rename 失败 | 目标要么完整存在，要么完全不存在 |

测试不是只注入“第二个文件写失败”。v28 逐个覆盖全部 artifact write、manifest write、rename 和
manifest 写完后源文件漂移，逐次检查目标目录、staging 和 lock 均无残留。

### 32.4 独立 replay 的三态语义

新增安装版审计脚本 `replay_humanize_validation_record.py`。它不 import validator 来复用结果判断，
而是独立完成记录验证，再通过 `subprocess` 调用当前 validator：

1. 拒绝 JSON duplicate key、NaN/Infinity、非法 UTF-8 和非规范 JSON 字节；
2. 拒绝未知字段、类型偷换、路径穿越、非法后缀、hardlink、symlink/reparse 和闭集外文件；
3. 验证 manifest 自哈希、record hash、invocation 自哈希和 run ID；
4. 核对 invocation、source bindings、result、paired/warning request、stdout/stderr 和 execution record；
5. 比较记录 policy 与当前 policy；
6. 从 `inputs/` 重建临时 before/after/report/scope，运行当前 validator；
7. 比较顶层状态、退出码、分层状态、findings、warning、paired request SHA 和规范化核心结果；
8. text 模式额外逐字比较重放 stdout；
9. 返回前再次重读整个证据目录，拦截 replay 过程中的 TOCTOU 修改。

状态固定为：

| 状态 | 含义 |
|---|---|
| `FAIL/1` | 记录内部损坏、清单冲突、跨工件不一致或当前同策略重算不同 |
| `REVIEW/2` | 记录完整，但 policy drift、proposal 不可原样复跑，或显式要求 live source 匹配而原路径已漂移 |
| `PASS/0` | 记录完整，当前 policy 相同，归档输入重算的核心裁决一致 |

默认归档重放不要求原路径仍存在。原 before/after/report/scope 删除后仍可 replay；同时单列
`live_source_status=MATCH/NOT_CURRENT`。需要证明当前工作文件仍是记录版本时追加 live-source 门，缺失或
漂移只可 `REVIEW/2`，不能混入归档完整性结论。

### 32.5 Policy 从四项扩为六项

v27 request 只绑定 validator、invariant checker、scanner 和 lexicon。v28 新增：

- `report_extractor_sha256`：REPORT_INFORMED 的静态提取行为属于验证策略；
- `runtime_contract_sha256`：绑定 Python implementation/cache tag、Python 版本、Unicode 数据版本和 OS 名。

policy 在验证开始前冻结，结束时重新计算；中途任何字节变化使运行失败。每个普通、warning 和 paired
request 都使用同一快照。外部 paired-quality verifier 也不再接受空 `policy_hashes`：必须恰好包含六个
64-hex 字段，缺项、增项或非法值均在验签前 `FAIL/1`。

REPORT_INFORMED 的 paired request 还新增路径无关的 scope semantic SHA、report/source SHA、fragment
总数和 editable ranges。这样同一 before/after 即便字节相同，也不能把针对一份 detector selection 的
外部 clearance 重放到另一份 selection。

### 32.6 真实持久化样本暴露的缺陷

第一份 v28 持久化样本没有通过 replay。原因不是正文或 policy 漂移，而是 text 输出中的 finding 使用了
原始绝对路径；重放器在临时目录运行后，finding 的路径前缀必然不同，于是得到
`REPLAY_STDOUT_MISMATCH/FAIL`。此前 15 项 replay 测试中的 text 样本没有 high finding，因此没有触发
这一分支。

修复不是放宽 stdout 比较，而是让公开 text finding 只显示稳定 basename，并让 replay 临时文件采用归档
原文件名。随后增加“text + high finding + 不泄漏绝对临时路径”的回归测试。最终持久化样本位于
[direct-validation-v28-final2-20260718](build/direct-validation-v28-final2-20260718)，原 validator 正确返回
`REVIEW/2`，因为 `LEX-FOUNDATION-01` 与新增信号仍未解决；独立 replay 返回：

```text
record_integrity_status=PASS
reexecution_status=PASS
replay_core_match=true
status=PASS
exit_code=0
run_id=hvr1-1db531017fda5ad6b69ea778abfcfb611ede8fbe1dfebf46ef4320fe8bdc7e16
```

这里两个状态不矛盾：原稿候选仍是文风 `REVIEW/2`；replay `PASS/0` 只说明“这次 REVIEW 可以从归档
输入稳定重算”，绝不把候选升级为质量 PASS。

### 32.7 v28 红队覆盖

专项测试覆盖以下攻击：

| 攻击 | 预期 |
|---|---|
| before/after/invocation/result/request/stdout/stderr/execution/manifest 单字节追加 | `FAIL/1`，不启动重执行 |
| 修改 result 后同步更新 artifact hash、record hash、manifest 自哈希 | 跨工件状态绑定 `FAIL/1` |
| 修改 stdout 后同步重算全部普通哈希 | stdout/result 语义不一致 `FAIL/1` |
| invocation 增加隐藏字段并重算 invocation SHA/run ID | strict schema `FAIL/1` |
| invocation archive path 穿越或后缀注入 | `FAIL/1` |
| extra file | 闭集 inventory `FAIL/1` |
| hardlink evidence file | `FAIL/1` |
| 同调用同目录再次发布 | 幂等、目录逐文件 SHA 不变 |
| 不同 scene 写入已有目录 | run conflict `FAIL/1`，旧记录不变 |
| 当前 policy 改变 | integrity `PASS`，reexecution `NOT_RUN`，顶层 `REVIEW/2` |
| 原文件修改 | 默认归档 replay `PASS`；live-source strict 为 `REVIEW/2` |
| 原 before/after/report/scope 全删除 | report 归档 replay 仍 `PASS` |
| reviewer proposal | 原 reviewer ID 不出现在任一文件；`REEXECUTION_NOT_SUPPORTED/REVIEW/2` |
| DRAFT + term、fragment + strict | 参数从 invocation 恢复并重算一致 |
| text 输出含 high finding | basename 稳定，stdout 精确重放 |

symlink 集成分支仍有 1 项因 Windows 当前令牌没有创建 symlink 权限而跳过；hardlink 使用真实 `os.link`
执行，reparse 位测试不依赖创建特权。这里不能声称敌对并发下 Windows 路径检查等价于句柄级 ACL 安全：
父目录检查与后续打开之间仍存在系统调用窗口，v28 的 `SELF_CONSISTENCY_ONLY` 明确不升级为外部信任根。

### 32.8 测试、projection 与资格状态

最终全量原始日志为 [full-test-audit-v28-20260718.log](build/full-test-audit-v28-20260718.log)，SHA-256：
`0d0f412741435d63b2e579371c9cf312ed3aa5dce5959be4239a54b72a7af629`。结果：

```text
Ran 617 tests in 71.740s
OK (skipped=3)
```

专项计数：validator 66 项；direct replay 16 项；external paired-quality verifier 24 项，其中 1 项 symlink
跳过。22/22 Python 脚本通过 `py_compile` 与 `--help`；`quick_validate.py` 首次因 Windows GBK 读取 UTF-8
失败，设置 `PYTHONUTF8=1` 后返回 `Skill is valid!`。这属于验证器环境编码问题，不通过改写中文文件规避。

最终 A/B projection：

| 项 | v28 final2 |
|---|---|
| policy / builder | `1.8.5 / 1.8.5` |
| 文件数 | 各 30 |
| 逐文件字节差 | 0 |
| excluded evaluation entries | 41 |
| capability source | `367e401d788a65706c30245ba834b5503587e75670379eddf8ff756b4cfa42d1` |
| evaluation surface | `3b5b0adf99b829941ff95e868c93ce0201f01e9dbb6e5443280df113b7ab0531` |
| source inventory | `462d1d0e7ed680630a76a27a3ea974b51aebbf80afa445b985c6b480eadb3257` |
| policy canonical | `90849754420dbb8510b422c71119b45c11d6ef90b389cac824b381734db59423` |
| policy raw | `8b418e25d1a98c6945170b379bb12f6ee47a88fa05e1341401508aff3fda3fc8` |
| builder executable | `506229ee4eb44b97e20716251e83b1f9c73e3b459a0819a43a5366c6b60d4334` |
| manifest | `695a49a3129c486a8440b92aada6b1d2bd8b5f857dd6cddfa930cc6825145213` |
| tree | `7792a0287d9781773933c85b56fcfcc527ec606ac3418006ddab2911fa10ed82` |

两份 manifest 为 [A](build/generator-projection-maturity-v28-final2-20260718.manifest.json) 与
[B](build/generator-projection-maturity-v28-final2-20260718-repro.manifest.json)。新 replay verifier 明确在
exclude/forbidden basename 闭集中，不进入 30 文件生成器 projection。

[v28 no-manifest qualification](build/qualification-maturity-v28-20260718-no-manifest-final3.json) 的 SHA-256
为 `1415fa43afffb5d2288e430f45c4bdf152d393a972114b2a7640b015268fde6a`。其内部状态继续是：

```text
evidence_integrity_status=PASS
qualification_status=NOT_EVALUATED
atoms_pass=0
atoms_fail=0
atoms_not_evaluated=188
exit_code=2
```

新增的 19 项 direct evidence/replay 测试没有给任何生成资格 atom 加 PASS。contract/requirements/oracle
版本分别升为 `2026-07-18.16 / 2.8.1 / 1.8.1`，只是同步新的证据合同和 stale binding。
本轮可追溯摘要见 [v28 authority pointer](build/humanize-academic-authority-v28-20260718.json)；该文件明确
声明自己不是外部信任根。

### 32.9 v28 裁决与剩余边界

v28 已把短文记录从“保存摘要”推进到“自包含、内容寻址、可三态重放、能拒绝整包内部矛盾”的工程形态。
它能在原输入删除后复跑，能区分归档重放与 live source，能拒绝 policy 漂移下的假 PASS，也能诚实拒绝
无法复制的 reviewer proposal。可以称为成熟的短文机械证据与复现层。

仍不能称为最终无人值守 Humanizer，原因保持具体：

- 自哈希与 run ID 只证明自一致性；同一攻击者若能重造整包，没有外部签名就不能证明历史真实性；
- 原 reviewer ID 的裸 SHA 只是低熵假名化，可能被字典反查，不是匿名或认证；
- Windows 没有 ACL-aware 受保护 launcher，路径检查也不是敌对并发下的句柄级隔离；
- external clearance 尚未与 validator/finalizer 原子消费，且没有一次性 redemption/消费账本；
- 188 个生成资格原子全部未评估；
- replay PASS 不评价搭配、段落职责、文风收益、学术正确性、作者身份或长期收敛。

v28 的成熟点不是把这些缺口改名为“已闭环”，而是让每个缺口都有可观察状态，且不能被低层 PASS 覆盖。
