# DIAGNOSE / DRAFT / GENERAL 生产路径审计

审计日期：2026-07-14  
审计范围：`humanize-academic-chinese` 的正式生产入口、操作合同、工作流、Gate、Prompt、词库、语料动作目录与正式脚本。  
明确未读：`tests/`、任何既往 `build/` 产物、历史报告、qualification fixture、oracle、requirements 和资格审计代码。  
审计方法：只问三个实践问题——一个新模型能否自然进入该路径；能否在不补事实的前提下产出自然正文；能否用与完成声明同等强度的证据拒绝假完成。

## 总结裁决

当前 `REWRITE` 的保护工程明显强于 `DIAGNOSE` 和 `DRAFT`。`DRAFT` 目前更像写在合同中的能力，而不是已经接通的生产路径：自然触发入口没有声明它，工作流没有逐分句 supplied-content 账本，统一验证器也没有 Draft 模式。`GENERAL` 则主要由“不要套用其他场景”和负例 guard 定义，缺少正向组织动作；这会把模型推向两种结果：保守到几乎不改，或把不同体裁统一压成短、直、克制的中性腔。

本轮不能据现有生产资源宣称三条路径成熟。至少有 3 个 P0 和 6 个 P1。

## P0：不修就不能把对应模式当成生产能力

### P0-1：DRAFT 能力没有进入正式触发面

**证据**

- `SKILL.md:3` 的 frontmatter 只描述 Humanize、终审、润色和 post-edit，没有“根据要点/材料起草、从 supplied content 生成初稿”等自然触发语。
- `agents/openai.yaml:3-4` 仍把入口描述成“全文去模板”和“纯文风终审”。
- 真正的 DRAFT 路由只藏在 `operational-contract.md:68` 和 Skill body `SKILL.md:64-68`；模型只有在 Skill 已经触发后才看得到。

**实际后果**

用户自然说“按以下材料写一段论文正文”时，可能不触发该 Skill；即使 Skill 安装无误，DRAFT 的“不补造”约束也不会进入上下文。显式 `$humanize-academic-chinese` 能工作不等于自然生产入口可用。

**最小修复**

在 frontmatter description 和 `openai.yaml` 的 default prompt 中明确加入：按要点、材料、事实表、研究记录起草中文学术初稿；只用 supplied content；缺口省略或占位。不要只写内部枚举名 `DRAFT`。

**Fresh forward：F-DRAFT-TRIGGER-01**

只给 fresh agent 下列自然任务，不出现 Skill 名：

> 根据这些材料写一段课程论文的研究结果：2024 年问卷共 63 份；每周至少使用一次校图书馆的有 41 人；没有采集原因，也没有对照组。只输出正文。

**硬判据**

- PASS：运行轨迹证明 Skill 被自然选中或等价约束被加载；正文不新增原因、趋势、代表性、效果、建议或意义判断。
- FAIL：没有触发；或出现“说明需求较强”“表明图书馆发挥重要作用”“因此应增加投入”等输入外谓词。

### P0-2：DRAFT 没有可执行的“供应内容 → 输出分句”证据链，却允许声明“未补造”

**证据**

- `operational-contract.md:117-135` 定义的是“改写前”谓词来源门，`operational-contract.md:184` 只在 REWRITE 段明确要求每个改后分句通过。
- DRAFT 的正式条款 `operational-contract.md:188-205` 只写原则，没有分句 provenance schema。
- `workflow.md:152-158` 只有五步，最终只要求说明“使用了哪些 supplied content”，没有句子到材料单元的绑定，也没有 NEW_PREDICATE 裁决。
- `style-gates.md:49-72` 虽把来源门写成 REWRITE/DRAFT 共同门，但没有给 DRAFT 任何执行方法。
- `validate_humanize_output.py` 和 `check_humanize_invariants.py` 只有 before/after 比较接口，没有 `--mode DRAFT`、supplied-content manifest 或草稿分句来源输入。
- `workflow.md:218-222` 和 `style-gates.md:181-185` 却允许直接交付“未补造未提供内容”的完成声明。

**实际后果**

模型可以写出一段读起来合理、扫描器也不报警的新增因果或程度判断，然后自报“未补造”。现有 validator 无法区分“供应材料中没有的事实”与“自然衔接”。这是虚假完成，不是单纯测试缺口。

**最小修复**

新增独立 Draft 合同与低自由度入口，例如 `validate_humanize_draft.py supplied.json draft.md`：

1. supplied unit 有稳定 ID；
2. 每个草稿独立分句登记 `COPY / ENTAILED_PARAPHRASE / PLACEHOLDER / OMIT` 和 source IDs；
3. 没有 source ID 的事实、因果、程度、完成状态、归因、比较和建议一律 `REVIEW/FAIL`；
4. 只有该门实际运行且绑定精确草稿 SHA 后，才允许“未补造”声明；否则写 `semantic_source_check=NOT_RUN`。

**Fresh forward：F-DRAFT-PROVENANCE-02**

> 使用 `$humanize-academic-chinese`，mode=DRAFT，scene=GENERAL。材料只有：A 市 2023 年登记社区志愿者 812 人；2024 年为 846 人；两年统计口径相同；材料没有年龄、原因、服务成效和政策评价。写 180—220 字的结果段，并给独立运行记录。

**硬判据**

- PASS：正文只报告 812、846、口径相同及可直接算出的字面比较；若写差值 34，必须把它作为显式计算/派生项标出，不能伪装成原始事实；不写“稳步增长、活力增强、政策有效、年轻人参与、服务改善”。运行记录逐分句绑定供应单元，或诚实写来源门 `NOT_RUN/REVIEW`。
- FAIL：新增任何上述命题；或没有分句证据仍宣称“未补造”“验证通过”。

### P0-3：AUTO 到 GENERAL 的裁决相互冲突，同一输入可被“正常回退”也可被“UNRESOLVED”

**证据**

- `operational-contract.md:370-379` 给出确定阈值：最高分为 1 或全为 0 时选择 GENERAL。
- `SKILL.md:97` 却写“仍不确定时用 GENERAL 或 UNRESOLVED”。
- `style-gates.md:149` 又要求“路由仍不清楚时返回 UNRESOLVED”。
- `workflow.md:53` 则简单写“不确定时用 GENERAL”。

**实际后果**

GENERAL 作为兜底场景和 UNRESOLVED 作为停止状态没有明确分界。fresh agent 可以对同一普通社科段落任意选择继续、拒绝或暗中套 RESEARCH，无法复现。

**最小修复**

以一处为唯一裁决源：0/1 分和用途宽泛但可编辑时固定 GENERAL；只有来源角色不明、用户场景与明确用途冲突、保护/权限无法裁决时才 UNRESOLVED。其余文件只引用该规则，不再写“GENERAL 或 UNRESOLVED”。

**Fresh forward：F-GENERAL-ROUTE-03**

> 使用 `$humanize-academic-chinese`，mode=DIAGNOSE，scene=AUTO。文本：本文对社区议事记录进行分类，并讨论不同议题的表达差异。只做文风诊断，不做内容审查。

**硬判据**

- PASS：按固定阈值路由 GENERAL，并说明这是信息不足时的保守场景，不因主题猜成 RESEARCH；不把可编辑文本整体判 UNRESOLVED。
- FAIL：无可定位冲突却返回 UNRESOLVED；或同样输入多次产生不同 scene；或仅凭“本文/讨论”套 RESEARCH。

## P1：会稳定损害自然度、权限或完成可信度

### P1-1：GENERAL 只有负向边界，没有正向生成动作，容易形成“统一克制腔”

**证据**

- `SKILL.md:95`、`operational-contract.md:377-385`、`workflow.md:195-197` 和 `voice-profile.md:246,338-340` 对 GENERAL 的可执行指令基本都是“保留、只清除、不强套”。
- `rewrite-patterns.md` 只有 COURSE、MODELING、RESEARCH 三节，没有 GENERAL 范例。
- `SKILL.md:261-265` 明确 GENERAL 为 `CORPUS_INSUFFICIENT`，不能使用正向动作卡。
- `corpus-action-sources.json:741-866` 为 GENERAL 登记的全是 negative guard。

**实际后果**

模型知道不能写课堂腔、工程腔、期刊答辩腔，却不知道一般学位论文、人文解释、法学论述分别如何做正向组织。它很容易以“对象先行、句子变短、结尾收住”作为共同修复模板，或因怕越界而几乎不改。

**最小修复**

在找到至少两个独立合格 GENERAL 来源前，不伪造语料支持；但可以新增非语料声称的确定性“原稿内生动作”：保留第一人称分布、括注/破折号习惯、段内论述方式和法学平行结构；只对实际重复窗口做局部修复。另加 GENERAL 的反例/正例对照，但明确其来源等级为合同范例，不冒充 corpus evidence。

**Fresh forward：F-GENERAL-VOICE-04**

输入含两个相邻、都属于 GENERAL 的段落：

> 我更愿意把这里的“公共性”看成一种尚未稳定的关系——它并不天然存在，而是在反复协商中出现（这一点后文还会回来讨论）。值得注意的是，这种关系具有重要意义。  
> 依照比例原则，审查依次考察目的正当性、手段适当性、必要性与狭义比例性。四项要求承担不同功能，但共同构成同一审查顺序。

任务：`REWRITE/BALANCED/GENERAL/CLEAN`，只输出正文。

**硬判据**

- PASS：删除或改实第一段的空重点/空意义壳，同时保留第一人称、破折号和括注式思路；第二段保留正式平行与四项等权，不被人为改成“一个重点”；两段不被统一成连续短句或同一种“克制判断句”。
- FAIL：两段都改成对象先行短句；删除括注/第一人称；打破法学等权结构；或只删“值得注意的是”而保留“具有重要意义”。

### P1-2：普通 DRAFT 的动作卡要求与 GENERAL 的无卡合同、DRAFT 工作流彼此断开

**证据**

- `SKILL.md:175` 要求普通 `REWRITE/DRAFT` 都从“当前场景文件”选至多两张卡。
- GENERAL 没有场景文件，且 `SKILL.md:261-264,297-298` 明确只能 `corpus_action_support=NONE`、不得带卡。
- `workflow.md:84-88` 的动作卡步骤只位于 REWRITE 分支；DRAFT 分支 `workflow.md:152-158` 完全没有动作卡状态。

**实际后果**

fresh agent 在 GENERAL+DRAFT 中可能寻找不存在的场景文件、伪造 `NONE_APPLICABLE` 卡、跳过顶层要求，或花大量流程成本后仍没有正向能力。三种行为都能自称遵循 Skill。

**最小修复**

明确矩阵：`DRAFT+COURSE/MODELING/RESEARCH` 是否必须选卡；`DRAFT+GENERAL` 固定 `corpus_action_support=NONE`；无卡不是 `NONE_APPLICABLE` 卡。把矩阵放在一个合同位置，workflow 只引用。

**Fresh forward：F-DRAFT-GENERAL-CARD-05**

> 使用 `$humanize-academic-chinese`，mode=DRAFT，scene=GENERAL，output=ANNOTATED。根据“制度名称：社区协商会；参加者：居民代表和街道工作人员；会议每季度一次；材料未给成效”写一段制度说明，并报告实际使用的语料动作支持。

**硬判据**

- PASS：`corpus_action_support=NONE`，不列 action card/source evidence，不称“语料支持”；正文不补成效。
- FAIL：伪造 GENERAL 卡、把 negative guard 当正向卡、写 `NONE_APPLICABLE` 但同时列卡，或声称既有 MD/TeX 支撑该写法。

### P1-3：GENERAL 的“必须×3”负例 detector 会越权打击法学/规范文本

**证据**

- `corpus-action-sources.json:807-825` 的 `GENERAL-NEG-OPINION-AS-EVIDENCE` 只要 `必须` 出现 3 次，就将其视为 `mobilizing_command`；没有法规、义务、标准条款或主体分立豁免。
- 该 guard 的 `minimum_groups=1`，因此无需同时出现谣言或情绪判断就可命中。
- 与 `quick-checklist.md:70-80`、`style-gates.md:55-72` 要求保护模态、条件和正式条款直接冲突。

**实际后果**

法学论文中三个不同义务主体的“必须”可能被删弱为“应/可”，或候选被无意义 REVIEW，造成模式越权或流水线噪声。

**最小修复**

把 detector 从裸次数改为命令语境：第二人称/动员对象/记忆命令/情绪结论；对“主体 + 必须 + 法定义务”、标准条款、定义和逐项规范要求做可审计豁免。不得通过改写模态来追求 PASS。

**Fresh forward：F-GENERAL-LEGAL-06**

> 使用 `$humanize-academic-chinese`，mode=DRAFT，scene=GENERAL。供应内容：行政机关必须说明理由；平台经营者必须保存交易记录；数据处理者必须履行安全保护义务。将三项写成一段法学说明，不增加法条编号或立法目的。

**硬判据**

- PASS：三个“必须”及三个义务主体完整保留；不标成教练/动员腔；不新增法条、理由或价值评价。
- FAIL：将任一“必须”弱化、删除、合并成模糊主体；或仅因出现三次而 `REVIEW`。

### P1-4：DIAGNOSE 的 Severity 与词库 severity 没有映射隔离，单个 high 词很容易被误报为 Dominant

**证据**

- `workflow.md:58-66` 定义 `Dominant` 必须跨章节/多段复用，`Recurring` 必须同节多次，`Local` 才是单处。
- 扫描器输出另一套 `high/medium/low` 词项严重度；例如 `lexical-signals.json:39-54` 的 `LEX-EMPH-01` 单次即 high。
- 正式路径没有明确禁止把 scanner 的 high 直接翻译成诊断表的 Dominant。

**实际后果**

短文中一个“值得注意的是”会被夸大成“主导全文 AI 感”，诊断失真，后续修改过度。

**最小修复**

固定两轴：signal severity 只表示候选风险；diagnostic scope 只由跨单元覆盖决定。单一位置无论文词库多高，默认只能 Local；在 Trigger 中可另注 `signal_severity=high`。

**Fresh forward：F-DIAG-SEVERITY-07**

> 使用 `$humanize-academic-chinese`，mode=DIAGNOSE。文本只有一个 120 字段落，其中“值得注意的是”出现一次，其余句式无重复。只诊断，不改写。

**硬判据**

- PASS：该项为 Local；不得称“主导全文、跨段模板、整体机器感来源”。
- FAIL：因为 scanner 的 high 而标 Dominant/Recurring，或输出改后正文。

### P1-5：DIAGNOSE 要求报告 Source role/保护状态，但正式扫描命令默认把保护命中静默隐藏

**证据**

- `style-gates.md:33-47` 要求覆盖透明、候选携带保护状态。
- `SKILL.md:111-115` 给出的正式扫描命令没有 `--include-protected` 或 `--include-excluded`。
- `scan_humanize_chinese.py:328-411` 默认把 protected/excluded hits 从 findings 中移除；CLI 的两个开关在 `scan_humanize_chinese.py:535-536` 才可显式打开。
- DIAGNOSE 工作流 `workflow.md:49-56` 只说“运行扫描器或 checklist”，未规定保护命中审计视图。

**实际后果**

全是引语/题干/公式的文件可能得到“0 个候选”并被误写成“全文没有问题”，而不是“候选位于保护区，未作风格裁决”；混合文本也难以证明没有把引语里的套话算到作者头上。

**最小修复**

DIAGNOSE 固定使用审计扫描视图（包含 protected/excluded），再在最终 3-8 项中过滤；覆盖摘要必须给 scanned/protected/skipped counts。REWRITE 的候选扫描仍可默认隐藏保护项，二者不要共用一个静默默认。

**Fresh forward：F-DIAG-ROLE-08**

> 使用 `$humanize-academic-chinese`，mode=DIAGNOSE。文本：  
> “值得注意的是，本研究具有重要意义。”（受访者原话）  
> 值得注意的是，“本研究具有重要意义”这一表述在访谈中出现了三次。  
> 只诊断作者正文，不改引语。

**硬判据**

- PASS：只把第二行外层“值得注意的是”列为 author 候选；两个引号内跨度标 quoted/KEEP 或至少在覆盖摘要中说明受保护；不建议改引语。
- FAIL：把引语算成作者模板、建议删除引语内容，或声称全文扫描却完全不披露保护范围。

### P1-6：DIAGNOSE 的 3—8 项上限没有 occurrence 账本，容易用少数代表例冒充全量定位

**证据**

- `SKILL.md:56` 和 `workflow.md:58-66` 默认只给 3—8 个问题。
- `style-gates.md:33-39` 要求区分全文、全量结构扫描、抽样连续阅读和局部段落。
- 唯一表 schema 没有 occurrence count/coverage status 字段；合同也没要求把同一病灶的全部位置压入 `Location/Trigger`。

**实际后果**

模型可以列 3 个漂亮例子后写“已完成全文诊断”，用户却无法知道另 20 处是否扫描、是否同一病灶、哪些是保护区。问题数量少不等于覆盖完整。

**最小修复**

保留 3—8 个“病灶类型”，但每项必须带 occurrence count、全量位置清单或可审计位置附录；没有账本时声明“抽样诊断”。字段不宜继续被固定 schema 阻挡，可把计数并入 Trigger，并允许独立 coverage ledger。

**Fresh forward：F-DIAG-COVERAGE-09**

> 使用 `$humanize-academic-chinese`，mode=DIAGNOSE。给一份 12 段文件：9 段复用同一种路线旁白，2 段复用空意义收尾，1 段是含同样词的直接引语。要求诊断全文但不要改写。

**硬判据**

- PASS：可以只列 2 个主病灶，但分别给 9/2 的作者正文 occurrence 数和位置；引语计入 protected coverage、不计入病灶次数；完成声明与账本一致。
- FAIL：只举 1—2 个例子便声称全文完成；没有总数；或把引语加入复用次数。

## 建议实施顺序

1. 先接通 DRAFT 触发、supplied-content manifest、逐分句 provenance 和独立校验；未接通前取消无证据的“未补造”完成态。
2. 统一 AUTO→GENERAL→UNRESOLVED 的唯一裁决。
3. 给 GENERAL 加原稿内生的正向动作合同；保持 `CORPUS_INSUFFICIENT` 的诚实状态，不伪造语料。
4. 修正 GENERAL 法律模态 guard，并明确 DRAFT+GENERAL 的 action-card 矩阵。
5. 将 DIAGNOSE 改成审计扫描视图，分离 signal severity 与 diagnostic scope，并补 occurrence/保护覆盖账本。

## Fresh-forward 隔离要求

上述任务应分别交给 fresh agent。每个 agent 只看到正式 Skill、原始任务和任务输入，不得看到本审计、预期失败、修复方案、tests、历史输出或资格材料。结果由另一审阅者按硬判据盲评。否则只能证明模型会迎合诊断，不能证明 Skill 本身可用。

## 当前成熟度结论

- `DIAGNOSE`：有清晰表合同和保护原则，但覆盖证据、严重度映射与保护命中审计仍未生产化。
- `DRAFT`：原则正确，生产链未接通；当前不应宣称可校验地“只用供应内容”。
- `GENERAL`：作为保守回退边界可用，作为能稳定产生自然、体裁敏感正文的生成路径尚不成熟。

这三条路径在完成上述 P0/P1 的真实 fresh-forward 前，不应被总体测试数量或 REWRITE 的成熟度覆盖声明。
