# 纯文风执行工作流

## 目录

1. 先固定合同
2. DIAGNOSE
3. REWRITE
4. DRAFT
5. 三种强度
6. 场景差异
7. 交付与声明

本文件只定义执行顺序。字段、优先级和冲突状态以 [operational-contract.md](operational-contract.md) 为准。长文另读 [long-document-workflow.md](long-document-workflow.md)。

## 1. 先固定合同

任务开始时记录：

```text
mode: DIAGNOSE | REWRITE | DRAFT
scene: AUTO | COURSE | MODELING | RESEARCH | GENERAL
intensity: LIGHT | BALANCED | STRUCTURAL
output: CLEAN | ANNOTATED | PATCH
voice_profile: NONE | INLINE | FILE:<profile-id>
report_context: NONE | REPORT_INFORMED
locked_structure: yes/no + scope
protected_roles: quoted/exam-original/OCR/code/math/report-metadata/other
```

缺省使用 `REWRITE/AUTO/BALANCED/CLEAN/voice_profile=NONE`，并在交付中披露
`voice_disclosure=SCENE_DEFAULT`。显式用户格式覆盖默认输出；旧的 `voice=SCENE_DEFAULT`
或 `voice=PROFILE:<id>` 只作为输入兼容别名，不写入新工件。

先处理编码：按 UTF-8 读取；失败后再尝试可识别的本地编码；仍不可读才跳过并记录范围。不得因一次默认编码失败把整个文件当乱码。

### 1.1 REPORT_INFORMED 输入

用户提供检测报告或标红片段时，读取 [detector-report-intake.md](detector-report-intake.md)：

1. 用 `extract_detector_report_scope.py` 忽略脚本、样式、链接和报告 UI，只提取可见标注原文；
2. 有原稿时只接受唯一映射；重复、缺失或动态渲染片段标 `REVIEW/UNRESOLVED`；
3. 检测分数和标签只用于说明输入来源，不进入候选严重度和正文；
4. 映射后的每个片段重新识别 `author/quoted/exam-original/OCR/code/math`，报告标注不改变保护权限；
5. 按用户意图进入 `DIAGNOSE` 或 `REWRITE`，不因报告存在而增加确认轮次；粘贴标红片段没有
   本地 HTML 时使用 `source_kind=INLINE_SELECTION`，固定 `report_scope_check=REVIEW`，不伪造
   extractor PASS；
6. 拒绝目标百分比、预测分数、噪声预算、随机化和检测规避，但继续处理可明确分离的纯文风范围。

## 2. DIAGNOSE

只诊断，不改正文。该模式不执行 Rewrite 的三轮改写、保护后比对或完成声明。

### 2.1 读取

1. 运行词项扫描器或使用 `quick-checklist.md`。正式诊断扫描使用
   `--include-protected --include-excluded` 审计视图；最终病灶仍只裁决作者正文，
   但覆盖摘要必须记录扫描、保护和排除计数。
   若为 `REPORT_INFORMED`，只在已唯一映射的候选 scope 内运行，不能把报告未标注部分冒充已诊断范围。
2. 根据文档用途选择场景；不确定时用 `GENERAL`。
3. 只读取命中的病灶节和场景相关规则。

诊断不需要建立完整语义保留清单，也不执行改写三轮。

### 2.2 排序

| 级别 | 判定 |
|---|---|
| `Dominant` | 跨章节或多段复用，决定整体机器感 |
| `Recurring` | 在同一节多次出现，持续影响节奏 |
| `Local` | 单处词句问题，不改变整体结构 |

这套覆盖等级与扫描器的 `high/medium/low` 风险等级正交：单一 high finding 仍只能是
`Local`，除非另有跨单元复用证据。默认只输出 3-8 个最高价值的病灶类型，而不是只
抽 3-8 个位置；每一行在 `Location/Trigger` 中给作者正文 occurrence 数和全部位置或
可审计附录。一个位置只列一个主病灶；次病灶只有在改变动作时才保留。

### 2.3 输出

输出字段和顺序直接使用 [operational-contract.md](operational-contract.md) 第 5.1 节的唯一 `DIAGNOSE` schema，本文件不再重复定义缩减版。

`Decision` 使用 `KEEP/DELETE/REWRITE/REVIEW/NO_CHANGE/UNRESOLVED`。不要输出改写正文，不要使用“已调整、已完成改写”的声明。

## 3. REWRITE

### 3.1 建保护清单

锁定：用户指定措辞、直接引语、题干、法规/标准原文、OCR、代码、数学、TeX 命令、数字、单位、专名、术语、否定、模态、焦点权重、定义/命名/假设/观察/结果报告状态。尤其保留“重点/主要/优先”的作用域；“重点不是比较”不得改成绝对的“不比较”。

结构锁和强度权限决定是否可以合并、移动或删除段落。风格规则不得改变“谁称为什么、谁观察到什么、什么只是可能、什么尚未完成”。

随后按 [operational-contract.md](operational-contract.md) 第 4.3 节建立谓词来源门。每个拟写分句只能是 `COPY`、`ENTAILED_PARAPHRASE` 或 `DELETE_STYLE_SHELL` 的结果。尤其不得把“要求/应当/作用在于”改成工件已完成，不得把“提供支撑”具体化成已经用于决策，也不得把缓和词拆成新的程度结论。

逐项核对否定句的缺失对象：内容缺失不能改写成关系缺失。原句“缺少 X 层/内容/分析”不能顺手变成“缺少 X 的衔接/联系/过渡”；`缺少 X 层 -> 缺少 X 的衔接` 命中 `SPEECH_ACT_MISSING_CONTENT_TO_LINKAGE`，应回退到原缺失对象。来源本来就在谈衔接时保持其关系，不作该转换。

再为每个可编辑段落写一个内部“段落职责”：它是在定义对象、解释机制、交代引入图表的理由、比较结果、限定范围，还是展开另一条并列分支。段落职责不是正文标签，但属于改写不变量。不能因为某句看起来像元话语，就删除其承担的图表引介、问题量化、论证分层或范围切换；无法判断它是编辑后台还是读者所需说明时，保留原句或标 `UNRESOLVED`。

在改写前另做源文内部张力检查。若同一对象附近同时出现“可以直接……”与“不能直接……”等正反许可，或出现其他未经用户裁决的互斥主张，源文内部冲突不属于纯文风层的裁决权限：不判断哪一条主张正确，不得自行选择其中一条主张。两个冲突 span 都必须原样回显为 `UNRESOLVED`；请求 CLEAN 时改用 `requested_output=CLEAN; effective_output=PATCH`，只对其余安全跨度提交真实 hunk。统一验证器的 `SPEECH_ACT_SOURCE_POLARITY_TENSION_SELECTED` 只覆盖有共同词汇锚的直接许可/禁止选择性删除，不是通用矛盾检测器，也不是学科正确性判断。

降级后的 PATCH 先冻结来源跨度分区：`patch_hunks_source_partition=NON_OVERLAPPING`。同一 source span 只能属于一个 patch hunk，`REWRITE hunk 不得包住另一个 UNRESOLVED span`；冲突句必须从周围可安全删除的强调壳、教练壳和价值尾句中切开，不能用整段改写块与后续未决块重复覆盖。

短文实际落盘时按 [short-patch-workflow.md](short-patch-workflow.md) 使用 `humanize-short-patch-selection/v1 -> humanize-short-patch/v1` 两阶段工件；先构建 byte-bound bundle，再由 applicator 从冻结 source 确定性派生 candidate 并强制运行统一验证器。发布后 verifier 还要核对闭集并执行当前 policy replay；需要判断记录是否仍对应工作文件时显式传 `--live-source`。不要把自然语言 hunk 列表、builder `BUNDLED/0`、candidate assembly PASS 或 `SELF_CONSISTENCY_ONLY` verifier PASS 当成交付完成。

### 3.1.1 选择语料动作锚

普通生产改写不加载 action profile，也不读取正向语料卡；固定记录
`corpus_action_support=NONE`。只有明确进入“来源动作候选审计”开发任务，才读取 action profile
和场景文件，并使用安装版审计命令。这样可避免普通短文把审计面误当成生成器依赖。
只有该独立审计路径的 `SUPPORTED` 场景才可为每个可编辑单元选择至多两张
`origin_assurance=PRODUCTION` 的 `positive_action` 卡，且卡片列出的对象、条件、证据角色或比较关系必须已经出现在输入中。选择只控制信息组织，不授权复制来源句子、事实、数字、变量或领域对象。

`SUPPORTED_PROVISIONAL` 和 `CORPUS_INSUFFICIENT` 的生产改写都填写 `corpus_action_support=NONE`，不选择卡片。前者的 `UNKNOWN` 或未获外部证明的 `HUMAN_CONFIRMED` 卡只可用于完整安装版的独立候选审计；一旦选择，候选门固定 `REVIEW/2`，不得把它当成正常改写完成。generator projection 会删除全部 positive 卡、动作描述、候选 revision/queue 入口及来源路径，只保留 detector registry。非安装默认路径的外部 catalog 固定 `EXTERNAL_UNVERIFIED`，其中自填的 `HUMAN_CONFIRMED` 卡也不能进入 accepted。当前所有场景均没有生产级 action-card 支持。

安装版候选队列把 `accepted/`、`review/`、`rejected/` 作为三个互斥 head。action contract、来源复制
和模板门通过但 paired-quality 仍 pending 时，顶层是 `REVIEW/2`，工件只能进入 `review/`；合同
硬失败才进入 `rejected/`。只有未来顶层真实 `PASS/0` 才进入 `accepted/`。修订候选在三类 head
之间原子替换，旧 head 与不可变历史不得同时丢失或出现双 head。

没有任何卡满足输入锚点时记录 `corpus_action=NONE_APPLICABLE`，继续按原稿与场景规则处理；不得为了证明使用了 MD/TeX 语料而补造锚点。若选择卡片，运行记录写卡片 ID 和输入锚点，不写来源正文。负例卡只用于拦截结构，不作为正向句式模板。

### 3.2 先定位，不全量套规则

1. 扫描词项和句壳，得到候选行与上下文。
   `REPORT_INFORMED` 先以标注片段排序，但每个片段仍按同一词库和上下文合同裁决。
2. 连续阅读候选前后完整段落，判断是否为真实复用。
3. 标出句间关系：总论到细节、因果、排除、并列分支、条件、让步或回指。`具体而言/与此同时/因此` 等连接词只有在不承担这些关系时才删除。
4. 识别一个主病灶；读取相应 `HUM-*` 节。
5. 对照所选语料动作锚，确认所需对象均来自当前输入；不满足时撤销该卡。
6. 仅在需要范例时读取当前场景的改写范式。

`GENERAL` 在本步建立最小改写面：逐项记录病灶原跨度、读感后果和允许动作。没有可定位病灶时直接 `NO_CHANGE`；不得因强度为 `BALANCED` 就清扫段内全部近义词。修改未登记跨度，只能在解决原病灶所必需时发生，并须在成对质量门单独证明收益。

### 3.3 三轮改写

#### 第一轮：删除无功能脚手架

处理无信息路线预告、编辑提示、重复纠偏、错位管理/营销/教练腔和自动收尾。若词是术语、讨论对象或真实关系，使用 `KEEP`。

自动展望若只有“进一步拓展/提升/研究/应用”而没有具体对象、动作、条件或待回答问题，删除整个命题。不得只删“未来/后续工作”后保留同义展望。作者动作必须在当前交付范围内有正文兑现；只有“本文梳理/讨论/探讨”而没有对应材料时，删除作者动作壳，不把它降调成另一句未兑现承诺。

#### 第二轮：按授权调整结构

- `LIGHT`：跳过本轮。
- `BALANCED`：只在段内或相邻重复段之间调整。
- `STRUCTURAL`：可跨段重建，但必须保留 patch 和行映射。

只恢复原文可确认的主次。正式等权列表、定义组和标准条款不得为了“人味”被人为倾斜。
拆句必须跟随对象或论证分支变化。若一个长句共同界定“唯一依据—排除项—软约束”，不要按分号平均切成若干同构短句；拆分后仍要保留总论、细节和另一分支的层级。

#### 第三轮：校准句子与声线

让对象、动作或观察在适当位置承担主句，但保留“本文定义、结果表明、我们观察到”等言语行为。调整句长、连接和解释密度，不批量生成“这里真正、只需、其余沿用”。

逐句朗读改后稿，检查主语是否在对举两端偷偷切换、修饰语是否能支配后面的中心词、动词与宾语是否搭配。出现“参数……而不是把变量……”“按……闭环收紧”这类结构时，不以更短为由放行；修不好就回退原句。

同一命题叠加 `可能/或许/在一定程度上` 时，先判断它们是否共同限定同一命题。可以保留一个不增强确定性的可能性标记；不得把剩余缓和词拆成新分句，也不得新造“有限、较小、轻微、显著”等程度判断。若无法确认各标记的范围，保持原句并让验证器返回 `REVIEW`，不要追逐表面 `PASS`。

### 3.4 保护检查

对文件改写运行 `validate_humanize_output.py <before> <after> --scene <SCENE>`。`REPORT_INFORMED` 必须追加 `--report-scope <extractor-json>`；验证器会绑定源文 SHA、全部 UNIQUE 区间和 selection 外不可变文本。统一验证器把硬不变量、言语行为警告、改后高风险残留、新增模板与 paired-quality 待审状态合并为一次可复现检查：退出码 `0=PASS`、`1=FAIL`、`2=REVIEW`。只有对交付所对应的精确版本实际运行且 `mechanical_validation_status=PASS`，才能记录 `机械验证=PASS`；`REWRITE` 因 paired-quality 待外部复核而返回 `REVIEW/2` 时，不得把机械 PASS 写成顶层 PASS。脚本未运行、只做目测、未给报告任务绑定 scope，或检查后正文又有改动时记录 `NOT_RUN`。

对 `REVIEW` 中的高严重度候选和新增候选逐项裁决：能够说明其正式功能则用 `--keep-reason SIGNAL_ID=具体理由` 登记，否则继续改写。不得只检查“这里真正”等修复模板。内联短文统一按 `source_kind=INLINE_TEXT` 写入临时 before/after 工件后运行验证器；不必污染用户工作目录，但必须保留输入/输出 SHA 和成对请求的绑定。若当前环境无法创建临时工件或运行验证器，只能报告 `mechanical_validation_status=NOT_RUN`、`delivery_gate_status=REVIEW`、退出码 `2`，不能用人工比对冒充 `PASS`。粘贴检测标红片段使用 `INLINE_SELECTION`，没有本地报告 extractor JSON 时固定 `report_scope_check=REVIEW`。

需要可复核记录时追加 `--evidence-dir`。证据目录必须作为一个事务包含归档输入、完整语义参数、六项
policy 快照、验证结果、适用 request、精确 stdout/stderr、execution record 与闭集 manifest；报告任务
还要归档 scope/report。完全相同的目录重跑是幂等，不同 run 或字节冲突不得覆盖。v3 direct evidence 使用
`humanize-direct-validation-evidence/v3`、`humanize-validation-invocation/v2` 和 `hvr2-*` run ID；不归档
绝对源路径、basename、path SHA 或 reviewer 标识，v2 只读兼容。安装版独立 replay 只有在记录完整、当前
policy 未漂移且归档输入重算核心结果一致时才返回 `PASS/0`；legacy proposal 元数据不可恢复、policy drift
或可选 live-source 检查失败为 `REVIEW/2`，内部篡改/缺件/多件/重算不一致为 `FAIL/1`。identity-free
proposal 可重放，但 replay 只证明 `SELF_CONSISTENCY_ONLY`，不能清除本节后续的成对质量门。

言语行为 warning 使用两阶段、只读 proposal 流程。首次 `REVIEW` 读取 JSON 结果中的
`warning_review_request.request_sha256` 与每条 `warning_fingerprint`；处理建议只能针对
当前 request 提交：

```powershell
python scripts/validate_humanize_output.py <before> <after> `
  --scene <SCENE> --format json `
  --propose-warning-resolution <WARNING_FINGERPRINT>=<具体处理建议> `
  --warning-review-request-sha256 <REQUEST_SHA256>
```

proposal 固定为 `UNVERIFIED_CALLER_PROPOSAL`，不采集 reviewer 身份，结果固定为
`reviewer_identifier_collected=false`、`identity_verified=false`、`review_clearance_granted=false`、
`attestation_status=NOT_APPLICABLE`；warning 仍在 pending/unaccepted 列表，退出码仍为 `2`。
`--warning-reviewer-kind`、`--warning-reviewer-id` 等旧字段已退役，非空值拒绝且不回显值；没有
proposal 时不得附带 request hash；旧 request 不能跨稿件、跨 warning、跨场景/保护术语或跨 policy 重放。
模型可以整理证据和 proposal，但不得把自身判断称为人工复核。

当前本地流程没有外部信任根。`VERIFIED_HUMAN` 只保留给代理无法访问私钥的外部审批
服务；必须在可信边界验证签名、artifact/request 绑定和审批范围，本地 CLI 不产生这种
clearance。未接入外部服务时，只有继续改稿并让 warning 在新版本上消失，才能使 speech-act
机械层恢复 `PASS`；`REWRITE` 仍因 paired-quality pending 保持
`delivery_gate_status=REVIEW, exit_code=2`。

保留原主张的语义方向不等于保留其营销或桥接句壳。优先用输入已有对象具体化；禁止“深刻揭示 -> 深入揭示”“奠定坚实基础 -> 打下良好基础”之类同义轮换。输入不足以具体化时保留原文并标 `UNRESOLVED`，不要假装修复完成。

### 3.5 成对质量门

validator 通过后仍须逐段比较改前与改后；它不能判断病句、段落职责或论证层级。每个发生变化的段落依次回答：

1. 原段落的职责是否仍在，尤其是图表引介、问题量化、范围限定和并列分支？
2. 改后是否有可指出的读感收益，而不只是字数变少、句子变短或连接词变少？
3. 是否新增主语错位、搭配不当、机械短句序列或“由……出发，经……最终落到……”式修复模板？
4. 原有因果、排除、并列和总分层级是否仍能从句法中读出？
5. 每个改句是否对应 3.2 节登记的病灶？“更正式、更书面、换个说法”以及 `让 -> 使`、主动因果改成 `使 + 抽象对象 + 被动` 等形式化轮换不算独立收益。

只有“每个保留改句至少一项明确收益、没有新增缺陷、职责与层级均保留”时，模型才可把候选提交给成对质量复核。先局部恢复无收益或劣化句；改后不能稳定优于原文时恢复整段并记 `NO_CHANGE`。这一步是文风成对复核，不评价事实、模型或学术正确性，也不得被机械 PASS、词项减少或压缩率替代。

统一验证器对每次 `REWRITE` 自动生成 `humanize-paired-quality-review-request/v1`。请求绑定精确
before/after SHA、`REWRITE/NO_CHANGE` 决策、逐 hunk 行区间与 hash、场景、文档范围以及
validator/invariant/scanner/lexicon/report-extractor/runtime 六项 policy hash。`NO_CHANGE` 的 `changes=[]` 只证明字节未变，不能
证明原文没有可行动病灶。模型可以依据请求发现退步并重写或局部回退；模型自己的全 ACCEPT、
调用方 `HUMAN` 标签、理由长度、普通盲读笔记或 fresh second pass 都不能形成 clearance。

当前本地工具只签发请求，不消费可信质量 response。机械层为 PASS 时固定输出：

```text
candidate_assembly_status=PASS
mechanical_validation_status=PASS
paired_quality_review_status=PENDING_EXTERNAL_REVIEW
delivery_gate_status=REVIEW
exit_code=2
humanize_quality_claim_allowed=false
```

只有未来由代理无法访问私钥的外部复核服务，把逐 change verdict、无新增缺陷、职责/层级保留、
request/policy/artifact 绑定和签名一起验证后，才能另行形成质量 clearance。在此之前只能称为
“机械验证通过的待审候选”，不能称为“已完成 Humanize”。

## 4. DRAFT

1. 按 [operational-contract.md](operational-contract.md) 5.3.1 的固定词形和优先级列出用户已
   提供的内容单元，标为 `FACT_PAYLOAD`、`EDITORIAL_REQUIREMENT` 或 `FACT_BOUNDARY`。编辑
   要求只决定组织方式；其中的事实载荷可按同一语义层级回收，但“本节需要/正文应/需要分开
   报告”等动作句不进入成稿。“不构成独立外部验证”“不是本问的直接观测目标”等显式认识论、
   适用范围或观测目标限制归 `FACT_BOUNDARY`，即使外层注释把整段称为 payload 也不能计为零。
   只有 `supplied_unit_ledger` 以 `unit_id + source_span + category` 无遗漏绑定全部输入时才报告三类
   数量；否则写 `classification_counts=OMITTED_UNUNITIZED`，不得输出 `FACT_PAYLOAD=n`、
   `EDITORIAL_REQUIREMENT=n` 或 `FACT_BOUNDARY=n`。无法拆分时保留原 span 并标
   `classification_status=REVIEW`。
2. 选择场景、Voice Profile 和强度；Draft 的强度只控制组织幅度。
3. 普通 Draft 不读取 action profile 或正向动作卡，固定写
   `corpus_action_support=NONE`。只有用户明确要求开发审计时，才进入安装版 action-profile
   路径；该路径的结果不能进入普通草稿或 generator projection。
4. 以用户内容建立顺序和详略，不创建“改前问题清单”。
5. 缺失信息保留为占位、问题或省略，不用套话填满。
   数字在材料中出现不等于授权自行比较；只复述 supplied material 已明确给出的比较方向和跨情景
   关系，不得新增“更大/更高/低于另一情景/进一步侵蚀”，也不得把“用于比较”改成“结果反映出”。
   `DRAFT_DERIVED_COMPARISON_NOT_SUPPLIED` 只定位窄词形候选；未命中不证明自然语言蕴含。
6. 把 supplied artifact 与草稿交给统一验证器的 `--mode DRAFT`。表面载荷门按值集合只拦截
   从未提供的数字、单位、数学、代码、引语和显式保护术语；同一个已提供公式、引语、命令或术语可在结果与讨论中复用。归因标记仍保守按出现次数检查；
   `semantic_source_check=NOT_EVALUATED` 不得改写成“未补造已验证”。
7. 输出起草正文和实际使用的 supplied content；不要声称完成改写。

## 5. 三种强度

### LIGHT

- 保留标题、段序、句序和信息位置。
- 只删无功能路标，修局部句壳和错位词。
- 默认编辑比例应最低；不为了减少重复移动信息。

### BALANCED

- 保持章节顺序。
- 允许段内重排、拆分超载句、合并相邻同义说明。
- 只有原文已显示主次时才调整解释密度。

### STRUCTURAL

- 要求用户明确授权。
- 先给拟议结构或 patch，不直接覆盖长文。
- 长文默认按 `structural-rewrite-contract.md` 在同一 unit 重排或合并相邻同职责段。
- 只有用户显式授权 `ADJACENT_PAIR`，才可把同一文件/heading 内物理相邻、scene/Voice 一致的两个
  PENDING unit 提升为原子 transaction；bundle 必须绑定 prepare `STX-*`，并用
  `{unit_id, paragraph_id}` 覆盖联合来源清单一次。
- 非相邻/跨标题/跨文件/三个以上 unit、改标题、拆段或整段删除只能给人工审阅 patch，保持
  `REVIEW`。
- 公式和其他保护项只可随其来源段整体移动，不得单独换段。
- transaction 的两侧 FRAGMENT gate 和 DOCUMENT gate 全 PASS 才共同提交；任一 member、保护、
  repetition 或全文门失败时共同回滚，不留单边 DONE/diff。
- 完成后必须运行保护检查和幂等 dry-run。
- 实际移动后披露 `structural_semantic_mapping=NOT_EVALUATED`，不得声称全文完成。
- 长文实际移动后读取结构语义 review request；`candidate_assembly_status=PASS` 不覆盖
  `delivery_gate_status=REVIEW, exit_code=2`。只把 `rendered_review/` 交给外部人工复核，不自填 clearance；
  review candidate 不进入 fresh second pass。

## 6. 场景差异

### COURSE

让读者能定位学习难点：简单内容短写，关键选择放慢，第二解从分叉处开始。同一知识只保留一个完整汇总。不得把教师提示写成审稿限定。

### MODELING

让已给出的模型操作、比较对象或方案后果获得合适篇幅。方案后果不是必填项：输入只给出模型、数值比较或耗时取舍时，停在这些具体结果仍是合格的 `MODELING`；只有输入明确写出采用、选择、部署或实际使用，才写结果如何影响方案选择。不要只做通用“对象先行”，也不要引入期刊式防御串。

### RESEARCH

保留定义、报告和主张的言语状态；压缩预演审稿人的多重否定；观察先于图表导览；结论回收核心研究判断而不是验收目录。

### GENERAL

以 Voice Profile 和原结构为主。先记录原稿内生的第一人称、括注/破折号、句法展开、
法学平行结构和段尾方式，只修复实际重复窗口；不同体裁不得统一压成对象先行短句。
只应用高置信通用病灶，不强制“课堂松弛、工程决策或期刊克制”。当前没有合格的
GENERAL 正向语料卡，固定披露 `corpus_action_support=NONE`。

## 7. 交付与声明

### DIAGNOSE

只给诊断表和覆盖范围：

```text
已完成纯文风诊断；未修改正文。覆盖：<scope>。未覆盖：<scope/reason>。
```

### REWRITE

按用户输出模式给正文、注释或 patch。摘要列配置、主要动作、保护检查结果和未解决项；没有动作时写
`actions=0（未改动）`，不凑数：

```text
已生成授权范围内的纯文风待审候选；mode=REWRITE, scene=<...>, intensity=<...>,
voice_profile=<NONE|INLINE|FILE:...>, voice_disclosure=<...>。机械验证=<PASS/FAIL/REVIEW/NOT_RUN>；paired-quality=<PENDING_EXTERNAL_REVIEW/NOT_RUN>。
未运行学术质控。
```

### DRAFT

```text
已根据用户提供内容起草；scene=<...>, voice_profile=<NONE|INLINE|FILE:...>, voice_disclosure=<...>。
draft_surface_source_check=<PASS/FAIL/NOT_RUN>；semantic_source_check=<PASS_COPY_ONLY/NOT_EVALUATED>。
只有 PASS_COPY_ONLY 才能声明逐字来源已确定；NOT_EVALUATED 时写“未发现已编码的表面新增载荷，语义来源待复核”。
```

若用户要求只输出正文，省略所有声明。不得把抽样处理写成全文完成。
