# Humanize Academic Chinese 红蓝队实用性复测

生成日期：2026-07-13  
Skill：`C:\Users\Lenovo\.codex\skills\humanize-academic-chinese`  
范围：2026-07-13 至 2026-07-18 的真实短文、诊断合同、最小 TeX、v19-v20 fresh 行为、v21-v24 STRUCTURAL 状态机、v25 成对质量/发布事务与 v26 入口口径复测。  
结论状态：**确定性保护、拒错、事务恢复和入口状态表达均已收紧；v25/v26 已把机械候选与质量授权拆开，普通本地 `REWRITE/NO_CHANGE` 固定停在 `REVIEW/2` 和 `rendered_review/`。局部盲读已有正证据，但 188 个生成资格原子仍全部 `NOT_EVALUATED`，不能称为无人值守成熟自动 Humanizer。**

## 1. 结论先行

本轮不能得出“Skill 已经能稳定把中文学术稿去 AI 味”的结论。它能证明的是两类能力：

- 课程样本曾由代理自行填写两项“人工核对”理由，使旧验证器产生历史 `PASS/0`；该记录没有 reviewer provenance，现已固定为来源失败证据。其可复核的有效状态是首次运行的 `REVIEW/2`，不能计入生成资格。
- 最小 TeX 流程可以从冻结快照生成派生稿，恢复数学和引用保护区，源文件未被覆盖；PowerShell 写出的带 BOM JSON 改写包已被收尾器接受。

与此同时，至少三份科研直改输出连续暴露问题：首次新造“为后续检验……提供线索”；后续样本新造“已有研究”；最终样本仍保留“值得注意的是”“综上”“深刻揭示”“为后续研究奠定基础”。后两类问题均被统一验证器明确返回 `REVIEW/2`。这说明工具链能阻断若干错误完成态，不说明模型默认直改已经可靠。

## 2. 证据范围

原始样本、正文输出、验证 JSON 与元数据均在：

`tests/fixtures/humanize_usability_red_blue/`

入口清单为 [manifest.json](D:/code%20LateX/elegantbook/physics/tests/fixtures/humanize_usability_red_blue/manifest.json)。该目录保留失败样本，不把它们伪装成 gold answer。

| 面 | 证据 | 结果 | 能证明什么 | 不能证明什么 |
|---|---|---|---|---|
| 课程短改 | `course_postfix_retry_body.md` + `validation/course_postfix_retry.json` | 历史 `PASS/0`，有效资格状态 `REVIEW/2` | 旧门会被代理自填“人工核对”绕过，现可作为 provenance 回归证据 | 有外部人工复核、课程生成通过或该版本可交付 |
| 科研短改，新增来源 | `research_fresh_body.md` + `validation/research_fresh.json` | `REVIEW/2` | 新增“已有研究”会被来源言语行为门拦截 | 所有来源补造均可自动发现 |
| 科研短改，残留模板 | `research_final_body.md` + `validation/research_final.json` | `REVIEW/2` | high 词项和新增总结壳会阻止通过 | 词库覆盖所有人工写作问题 |
| 诊断输出 | `diagnose_fresh_output.md` | 合同格式复现 | 固定九列表头和“不改正文”可被 fixture 约束 | 这是独立蓝队实测 |
| TeX 最小流程 | `tex_e2e_before.tex` + `tex_e2e_result.json` | pre-v25 历史 `PASS/0` | 单元级保护恢复、派生发布、源未改 | 当前合同下已获质量 clearance、全文编译、幂等或真实项目构建已通过 |

诊断条目有一项边界：最初的新鲜蓝队代理超时，未产出可用内容；`diagnose_fresh_output.md` 是按合同做的人工最小复现，故只验证输出合同，**不是**独立生成通过证据。

## 3. 红队量表与本轮发现

使用的红队量表为 14 个维度、每项 `0/1/2`、满分 28；`P0` 关注保护区、数字/公式、诊断误改正文、检测规避和长文虚假完成，`P1` 关注关键维度缺失、输出合同、验证状态伪装及默认直改可用性。独立终审结果为 `15/28`，未确认 P0 静默放行，但科研改写、模板残留和泛化性均为 0，触发 P1；完整评审原文见 [red_team_final_review.md](D:/code%20LateX/elegantbook/physics/tests/fixtures/humanize_usability_red_blue/red_team_final_review.md)。

首轮独立复审的主要问题：

| 等级 | 发现 | 实际证据 | 修复或状态 |
|---|---|---|---|
| P1 | 课程改写删掉“理解而非死记”的纠偏功能 | 首轮课程正文 | 增加课程纠偏保留规则；重试保留了纠偏，但 warning 未获外部人工确认，保持 `REVIEW/2` |
| P1 | 科研改写新造“为后续检验……提供线索” | `research_blue_body.md` | 扩展 `LEX-FOUNDATION-01`，现可稳定标记 `REVIEW` |
| P1 | 诊断表头与合同不一致 | 首轮诊断输出 | Skill 与可移植 Prompt 均锁定九列表头；独立复测因通道超时未完成 |
| P1 | 科研改写新造“已有研究”背景 | `research_fresh_body.md` | 新增 `attribution_source` 标记与回归测试；现返回 `REVIEW` |
| P1 | 最终科研直改仍含 high 模板与总结壳 | `research_final_body.md` | 保留为失败样本；不降低为 PASS |
| P2 | 收尾器不接受 PowerShell UTF-8 BOM 改写包 | 最小 TeX 探针首次失败 | 使用 `utf-8-sig` 读取 JSON/TXT 包，新增回归测试 |

后续黑盒复测发现一个长文完成态 P0：篡改 `units.jsonl` 的终态字段曾可伪造全文 `PASS`。该问题已修复：prepare 生成 `prepare_integrity.json`，finalize 在状态计算前校验 snapshot、manifest、初始账本、保护区和全部 chunk；篡改、缺失或清单变化均直接 `FAIL`。课程重试没有硬不变量错误，但言语行为层仍为 `REVIEW`；代理后来写入的“人工核对”不能清除该状态。TeX 探针数学、命令、百分号和 `\eqref` 均已恢复，且源文件 SHA-256 未变化。这些证据都不能等于默认生成模型通过 P0 全项。

## 4. 实施的修复

### 4.1 课程纠偏和数学补写

Skill 现在要求保留“理解而非死记”“不要只套公式，先辨认条件”这类含学习动作或常见误读的约束；只能压缩动员腔，不能整句删除。同时禁止根据题目或“先减后增”补出输入未逐字给出的区间端点、范围、推导或结论。

课程重试最终正文没有新增 `[0,1]`、`[1,2]` 等端点。验证器首先将言语行为差异保持为 `REVIEW`；随后两条理由由代理自行登记，并不构成外部人工审阅。`course_postfix_retry.json` 中的历史 `PASS` 因此只保留为 pre-provenance 失败样本，不能追认为有效通过。

### 4.2 桥接和来源补造

`LEX-FOUNDATION-01` 已覆盖“为后续研究/工作/检验提供线索”等变体。另一方面，词库不应冒充事实核查器：它不判断“已有研究”是否真实，只把改写前不存在、改写后新出现的文献背景归入 `SPEECH_ACT_ATTRIBUTION_SOURCE_CHANGED`。因此，模型新增“已有研究”会得到 `REVIEW`，人工必须删除或给出输入锚点；不能以“语境中应当有文献”为由接受。

Skill 的 `REWRITE` 合同也已明确禁止新增作者、机构、年份、引文、数据来源、实验条件、研究路径和未来工作。

### 4.3 Windows 改写包兼容性

`finalize_humanize_long_document.py` 的 JSON 和 TXT 改写包读取改为 `utf-8-sig`。PowerShell 常规 `Set-Content -Encoding utf8` 写出的 BOM 不再导致收尾器在验证前报“Unexpected UTF-8 BOM”。

这不是放宽保护：占位符、逐单元验证、diff、源文件保护和完成态判断均不变。对应单测在 `tests/test_finalize_humanize_long_document.py::test_utf8_bom_rewrite_bundle_is_accepted`。

## 5. 最小 TeX 端到端探针

输入仅一个单元，含 `\section`、`50\%`、`正文`、`\eqref`、`equation` 和 `\label`。流程：

1. `prepare_humanize_long_document.py` 固定快照并产生保护占位块。
2. 通过 PowerShell BOM JSON 删除唯一的空重点壳“值得注意的是”。
3. `finalize_humanize_long_document.py` 恢复全部占位区并发布 `rendered/`（pre-v25 历史行为；不代表当前质量 clearance）。

结果为 pre-v25 历史 `PASS`、`units_total=1`、`DONE=1`、`source_files_modified=0`、`full_completion_claim_allowed=true`。该结论严格限于这个一个单元的收尾流程，不能迁移为 v25 当前质量交付。`compile_check=NOT_RUN`，`idempotency=NOT_RUN`，因此报告不称其为“项目编译通过”或“长文幂等通过”。

## 6. 自动化验收

本轮追加的回归文件是 [test_humanize_usability_red_blue.py](D:/code%20LateX/elegantbook/physics/tests/test_humanize_usability_red_blue.py)。它锁定：

- 证据清单中每个前后文件和 JSON 产物均存在；
- 课程旧 `PASS` 即使携带两条具体理由，只要没有可审计的外部 reviewer provenance，也必须固定为失败证据；
- 新增“已有研究”必须处于 `SPEECH_ACT_ATTRIBUTION_SOURCE_CHANGED` 的 `REVIEW`；
- 最终科研输出必须保留为 `REVIEW`，并命中三类 high 风险项；
- 诊断 fixture 必须使用唯一九列表头，不得出现“改后正文”或“已调整”；
- TeX 探针不得因 `compile_check=NOT_RUN`、`idempotency=NOT_RUN` 被扩写成更大的完成声明。

执行结果：

```text
python -m unittest discover -s tests
Ran 153 tests in 1.681s
OK

python C:\Users\Lenovo\.codex\skills\.system\skill-creator\scripts\quick_validate.py C:\Users\Lenovo\.codex\skills\humanize-academic-chinese
Skill is valid!
```

新增 fixture 的 U+FFFD 审计为空。没有提交或推送任何文件。

## 7. 发布判断

| 发布面 | 判断 | 原因 |
|---|---|---|
| 词项扫描、保护检查、统一验证器 | 可用 | 当前回归与全仓测试通过；错误完成态会被阻断或降为 `REVIEW` |
| 长文完整性与虚假闭环防护 | 已修复并回归 | `prepare_integrity.json` 防止篡改 units/chunk/初始账本伪造 `DONE` 或全文 `PASS` |
| 长文 prepare/finalize | 最小流程可用 | BOM 兼容、源未改和保护恢复已实测；尚未复测真实项目编译与幂等 |
| 课程短文，代理自填人工复核 | provenance 失败 | 历史 JSON 为 `PASS/0`，但缺少外部 reviewer provenance；有效资格状态仍为 `REVIEW/2` |
| 科研短文，默认直接生成 | `REVIEW` | 两次修复后新鲜输出仍分别出现来源补造或多项 high 残留 |
| 生成模型前向资格 | 尚未取得资格（`NOT_EVALUATED`） | 尚未完成全部模式、强度、场景、报告输入与长文矩阵；`NOT_EVALUATED` 不是行为 `FAIL` |
| 独立最终红队分数 | `15/28`，不具备默认直改资格 | 无确认 P0 静默放行，但科研改写、模板残留和泛化性为 0，构成 P1；完整矩阵仍未运行 |

后续使用应保持同一原则：文件任务先走验证器；返回 `REVIEW` 时继续人工裁决或 `UNRESOLVED`，不把“没有硬错误”误写成“文风已经合格”。

## 8. 2026-07-16 v18 后验红队补充

本报告早期的可用性结论仍成立，但 v18 又收紧了一层：负例规则本身也必须有执行权限。此前完整
catalog 的 10 张 `negative_guard` 都会进入 production 扫描，实际有 6 张来自 `UNKNOWN`、
`THIRD_PARTY` 或 `OCR_INHERITED`，固定来源 policy 并未授权这些来源形成生产 guard。

修复后的实际行为是：

- GPT 明确生成或模型来源未解析的文本可以形成带 detector 的 runtime 负例；
- UNKNOWN、人类本地声明、第三方和 OCR 文本中的负例观察保留为 `AUDIT_ONLY`；
- `AUDIT_ONLY` 不会因词面命中而自动阻断用户正文；
- generator projection 只得到 4 张已授权 guard，且只看到 `id/scene/detector`；
- registry 缺失、坏正则、重复键、未知字段或本地扩大 trust 权限时，长文门为 `REVIEW`。

这提高的是“误拦截可控性”，不是模型改写质量分数。真实 fresh runner 本轮仍没有输出，不能据此
把本报告早期 `15/28` 的独立红队分数改成合格。当前实用性应分开写：确定性保护、拒错、长文覆盖、
detector registry 和证据绑定可运行；默认科研直改的生成能力仍缺 E3/E4 前向证据。

v18 回归为 481 项通过、1 项 Windows symlink 权限跳过；19 个脚本 compile/help 通过；两次
generator projection manifest 与 tree 分别稳定为 `1328011e...f4c6a` 与 `42eacd2c...b9b1`。
这些数据证明工具链工件一致，不证明模型已经能一次写出自然、准确且无需复核的学术稿。

## 9. 2026-07-17 v19 真实成对红蓝复测

### 9.1 pre-fix：机械 PASS 与可交付性脱钩

三个 clean-context 代理分别处理课程、建模和科研 TeX，旧 validator 全部返回 `PASS/0`。独立盲评
没有接受这种完成态：课程偏好改后；建模平局且不可直接交付；科研偏好原文且不可直接交付。

| Case | 旧机器门 | 盲评 | 失败原因 |
|---|---|---|---|
| COURSE | PASS/0 | B 8.8，可交付 | 只有轻微收益 |
| MODELING | PASS/0 | 平局，B 8.3/忠实度 9.2 | 表格功能被删、主语错位、路径壳 |
| RESEARCH | PASS/0 | 偏好 A，B 7.8/忠实度 9.7 | 首句搭配不成立、论证层级拆平 |

这一轮是生成质量 P1，不是基础设施问题。公式和 TeX 保护通过，但输出本身没有稳定优于输入。

### 9.2 修复

- `workflow.md` 新增逐段成对质量门：职责/层级保留、至少一项具体收益、零新增缺陷，否则回退；
- 建模规则把 `表格的作用` 分成后台指令和读者说明，不再无条件删除；
- 科研规则禁止按标点平均拆长句，保留唯一校准依据、排除项和并列反事实的关系；
- validator 新增 `SPEECH_ACT_FOCUS_SCOPE_CHANGED`，阻止“重点不是比较 -> 不比较”；
- `LEX-MGMT-01` 新增“实证闭环”和抽象路径壳；`LEX-TABLE-ROLE-01` 只要求上下文 REVIEW；
- `SKILL.md` 从 443 行/24,193 字符压到 280 行/15,579 字符，把审计控制面移到按需 reference。

### 9.3 post-fix：三组均得到盲评偏好

修复后的三个 fresh 候选均为真实 validator `PASS/0`（v25 paired-quality 上线前的机械历史结果），保存结果与当前 artifact 精确一致。第一次
post-fix 盲评发现建模限定绝对化后，正文和门禁继续修正；最终额外 modeling 盲评确认风险已消失。

| Case | A 自然度 | 最终 B 自然度 | B 忠实度 | 最终判断 |
|---|---:|---:|---:|---|
| COURSE | 8.4 | 8.8 | 10.0 | 偏好 B；仅为历史盲评，不构成现行 clearance |
| MODELING | 7.8 | 8.8 | 9.7 | 偏好 B；仅为历史盲评，不构成现行 clearance |
| RESEARCH | 7.3 | 8.7 | 9.8 | 明确偏好 B；仅为历史盲评，不构成现行 clearance |

这轮正证据来自句法减负、段落职责保留和论证层级重建，不是词项数下降。对应原始评审见：

- [pre-fix blind](build/maturity-v19-forward-20260717/blind-pair-evaluation.md)
- [post-fix blind](build/maturity-v19-postfix-20260717/blind-pair-evaluation.md)
- [final modeling blind](build/maturity-v19-postfix-20260717/modeling-final-blind.md)

### 9.4 发布状态

- 487 项测试全绿，1 项 Windows symlink 权限跳过；
- 19 个脚本 compile/help、quick validation 全部通过；
- 两次 29 文件投影 manifest/tree 一致；
- action profile 仍为 0 production positive、17 provisional positive、4 runtime guard；
- 资格仍为 `integrity=PASS / NOT_EVALUATED / 0 of 179`。

因此 v19 改变了“默认直改完全没有正证据”的旧判断：三个有代表性的短 TeX 场景现在都有 fresh
盲评正结果。它仍不足以授予总体默认直改资格；GENERAL、检测报告、STRUCTURAL、真实长文和 E3/E4
矩阵尚未覆盖。生产使用应继续保留 validator 与成对复核，不能只看 PASS 数量。

## 10. 2026-07-17 v20 GENERAL/DRAFT/REPORT/NO_CHANGE 红蓝复测

### 10.1 蓝队初始结果与红队否决

| Case | 初始机器态 | 独立评审/攻击 | 裁决 |
|---|---|---|---|
| GENERAL | PASS/0 | 改后 8.3，原文 8.7 | 失败：无收益正式化轮换和新硬被动 |
| DRAFT | FAIL/1 | 逐句来源审计 9.2，可交付 | 基础设施误报：已给 `R_S=0` 被正常复用 |
| REPORT | PASS/0 | 合法稿仅改 selection | 当前样本守约，但 validator 未绑定 scope |
| NO_CHANGE | PASS/0 | input/output SHA 相同 | 通过：没有制造差异 |

REPORT 红队另造 selection 外改动，旧普通 REWRITE 验证仍为 `PASS/0`，证明初始合法样本不能覆盖
恶意/失误路径。DRAFT 再扩成七类 repeat/new 14 case，旧门全部硬失败，证明不是单个公式特例。

### 10.2 修复后的可执行差异

- GENERAL：先冻结具体病灶跨度；无病灶 `NO_CHANGE`；每个改句须有独立收益；形式化同义轮换和
  新增抽象硬被动不算收益；逐句回退后再做整段比较。
- DRAFT：code/math/formal/command/quotation/garbled/protected term 按 supplied 值集合检查；同值复用
  不硬失败，新值继续失败；归因 occurrence、REWRITE 次数与顺序保护不变。
- REPORT：新增 `--report-scope`，绑定 extractor `PASS/0`、source SHA、UNIQUE 区间和 selection 外
  不可变块；范围外变化给 `REPORT_SCOPE_OUTSIDE_SELECTION_CHANGED/FAIL/1`。

### 10.3 post-fix fresh

| Case | fresh 输出 | 自动门 | 独立质量 |
|---|---|---|---|
| GENERAL | 逐字 NO_CHANGE | PASS/0 | 原 8.7 稿被保留 |
| NO_CHANGE | 再次逐字 NO_CHANGE | PASS/0 | 裁决合适 |
| DRAFT | 两段结果与讨论 | REVIEW/2 | 8.6，事实与边界准确，可内容交付 |
| REPORT | 只改 1 个 selection | PASS/0，scope PASS | 改后 9.1 > 原文 8.7 |

### 10.4 发布证据与保留边界

- 496 项测试通过，1 项 Windows symlink 权限跳过；
- 19 个脚本 compile/help 与官方 quick validation 通过；
- 两次 29 文件 projection 逐文件一致，manifest/tree 为 `f32e68ce...8344` / `a3ad65d7...0039`；
- action profile 仍是 0 production positive、17 provisional positive、4 runtime guard；
- 资格审计为 `integrity=PASS / NOT_EVALUATED / 0 PASS / 0 FAIL / 179 NOT_EVALUATED`。

v20 支持“普通短文调用更成熟”的判断，不支持“所有长文、STRUCTURAL 和跨学科任务一次生成稳定
合格”。尤其 DRAFT 的模型语义审计尚未接入不可伪造的外部审批，不能因为本轮独立审计认为内容可用
就回写机器 `PASS/0`。

## 11. 2026-07-17 v21 STRUCTURAL 实物红蓝复测

### 11.1 pre-fix：合同中有强度，CLI 中没有能力

红队直接对完整 `physics1.tex` 调用 `--intensity STRUCTURAL`，旧 prepare 返回
`unrecognized arguments`；不带参数时所有 unit 又被硬编码成 `BALANCED`。第二遍固定
`structure_lock=true`，因此即使 fresh 代理输出 `NO_CHANGE`，也不是同权限收敛。这个缺口属于
执行链 P0：文档声称有结构改写能力，实际入口不存在。

旧统一验证器还有相反问题：它要求数字、公式和命令的全文出现顺序不变。带公式的完整段落合法移动
也会 `FAIL/1`。若直接放宽顺序，公式又可能脱离原论证段。修复不能是一个宽松开关，必须引入来源段
映射。

### 11.2 修复后的结构权限

- prepare 显式冻结 `LIGHT/BALANCED/STRUCTURAL`；
- STRUCTURAL chunk 冻结来源段 ID、ordinal、SHA-256、职责、保护 span、可移动状态和 inventory hash；
- 每个 REWRITE 必须提交 `humanize-structural-plan/v1`；
- 所有来源段须恰好覆盖一次；未知、重复、遗漏均拒绝；
- 只允许 unit 内、标题锁定、相邻同职责段合并；不跨 unit、不拆段、不整段删除；
- 公式和其他保护项只可随来源段整体移动；
- finalizer 先生成“只移动原段”的结构基线，再验证候选；
- 发生真实移动后固定 `structural_semantic_mapping=NOT_EVALUATED`，不得声明全文完成；
- second pass 继承 STRUCTURAL，不再靠降成 BALANCED 制造假收敛。

### 11.3 完整材料 prepare 压力面

| 输入 | 全部 units / PENDING | 全文保护跨度 | 全 unit 段总数 | PENDING unit 来源段 | PENDING 内可移动 / 锁定 |
|---|---:|---:|---:|---:|---:|
| `physics1.tex` | 60 / 50 | 3,164 | 527 | 507 | 51 / 456 |
| 微信 `main.tex` | 36 / 28 | 821 | 74 | 65 | 4 / 61 |
| 详细 GPT 风格报告 | 163 / 42 | 730 | 235 | 114 | 7 / 107 |
| Skill 长报告冻结快照 | 130 / 117 | 1,632 | 449 | 436 | 73 / 363 |

这些材料只作复杂测试输入或 GPT 负例，不作真人 Voice 正例。四个工件当时只运行了 prepare 与
inventory，没有完成全文改写；来源段、可移动和锁定以 PENDING unit 为分母，保护跨度是全文口径。
Skill 报告行绑定 170357 字节、SHA-256 `e33c01dd...7852` 的旧冻结快照。建模 `main.tex` 只有 4 个
来源段可机械移动，说明新门没有为了提高成功率而把公式、列表和正式环境降级。

### 11.4 独立子代理 fresh trial：机械结构成功，最终仍正确拒绝

fresh trial 由独立子代理选择 `physics1.tex` 的“机械波 / 弦振动的简正模式”，把末尾两个相邻
`EXPOSITION` 题解段合并。工件没有 sealed prompt、runner receipt 或外部隔离证明，因此 blindness
未验证，不计入生成资格。

| 检查 | 结果 |
|---|---|
| 5 个来源段覆盖、4 个目标段、相邻合并 | `PASS` |
| 标题锁、职责、来源段 hash、保护归属 | `PASS` |
| 公式、TeX、数字、保护 span | `PASS` |
| 新增 high 风险词项/修复模板 | 无，style signal `PASS` |
| 相同 bundle 重放 | `assembly_replay_idempotency=PASS` |
| 模态范围 | `必须` 3 -> 2，`SPEECH_ACT_MODALITY_SCOPE_CHANGED` |
| 结构语义 | `NOT_EVALUATED` |
| unit 最终状态 | `REVIEW/2`，未发布 |

独立评估代理连续阅读认为，候选让边界条件、波速、基频和谐频成为一个连续题解，并未发现表面新增
载荷；这不是人工审批，学术正确性和结构语义仍未评估。系统
无法仅靠计数证明被删的“必须”属于重复教学收尾，所以没有接受模型自己的语义判断。整次 run 还因
其余 49 个 PENDING unit 没有 bundle 而保持 `REVIEW`；`rendered_partial/physics1.tex` 与源文件
逐字节一致。编译钩子未运行，明确记录为 `NOT_RUN`。

原始结果见 [fresh trial 评估](build/maturity-v21-20260717/postfix-structural-blind/evaluation.md)、
[结构 plan](build/maturity-v21-20260717/postfix-structural-blind/run/validation/U-b325e0f1a375.structural.json) 和
[unit validation](build/maturity-v21-20260717/postfix-structural-blind/run/validation/U-b325e0f1a375.validation.json)。

### 11.5 发布判定

共运行 504 项，整体 `OK (skipped=1)`；19 个脚本 compile/help 通过；两次 30 文件 projection 完全一致。
这些结果支持以下有限结论：STRUCTURAL 已经是可调用、可追溯、可拒错的 unit 级候选管线，适合
生成审核 patch。它仍不适合无人值守发布；跨 unit、小节重排、标题解锁、拆段、整段删除和结构语义
认证均未实现，生成资格继续是 `NOT_EVALUATED / 0 of 179`。

## 12. 2026-07-17 v22 STRUCTURAL 假完成态红蓝复测

### 12.1 红队找到的不是措辞问题，而是顶层状态冲突

v21 的结构语义字段会诚实写 `NOT_EVALUATED`，但覆盖闭合时顶层仍可能是 `PASS/0`，候选还会进入
正式 `rendered/`。只看顶层状态、退出码或发布目录的集成方会把待审候选当成交付稿。这个缺口按 P0
处理：不能依赖调用方“记得再读一个布尔字段”。

### 12.2 蓝队修复

- 新增 `candidate_assembly_status` 与 `delivery_gate_status`，顶层 `status` 必须与后者一致；
- 真实结构变化且语义未评估时固定 `REVIEW/2`；
- 完整待审候选只发布到 `rendered_review/`，正式 `rendered/` 不出现；
- 逐 unit 生成 hash-bound `humanize-structural-semantic-review-request/v1`；
- request 使用稳定 `validation/...` 证据引用，不保留失效 staging 路径；
- 模型 reason、warning proposal、调用方 HUMAN 标签和 bundle 自填 clearance 都不能放行；
- STRUCTURAL `NO_CHANGE` 的 per-unit semantic mapping 单独保持 PASS，不因同一 run 的其他结构候选
  被错误降级。

### 12.3 两条真实控制链

| 检查 | 完整 review candidate | warning control |
|---|---|---|
| 50 个可编辑 unit bundle | 50/50 绑定 | 50/50 绑定 |
| 终态 | 1 DONE、49 NO_CHANGE、10 protected | 1 UNRESOLVED、49 NO_CHANGE、10 protected |
| 目标 unit | validator PASS | speech-act REVIEW |
| candidate assembly | PASS | REVIEW |
| delivery / exit | `REVIEW/2` | `REVIEW/2` |
| 结构语义 | `NOT_EVALUATED` | `NOT_EVALUATED` |
| request | `9d1ba735...ff403` | `cac4b652...51cb8`，含 `必须: 3 -> 2` |
| 发布 | `REVIEW_CANDIDATE -> rendered_review/` | `PARTIAL -> rendered_partial/` |
| compile / second pass | `NOT_RUN / NOT_RUN` | `NOT_RUN / NOT_RUN` |
| source modified | 0 | 0 |

完整候选的实质 diff 只是删除两个题解段之间的空行。它足以攻击并验证状态机，但不足以评价大范围
文风收益。warning partial 与源文件 SHA 相同，说明未决改写没有进入派生稿。两条 run 都没有外部
人工语义复核、TeX 编译、物理正确性检查或个人 Voice 证明。

### 12.4 当前发布判定

共运行 507 项测试，整体 `OK (skipped=1)`；19 个脚本 compile/help 通过；两次 docfix projection
均为 30 文件且逐文件一致。资格新增 `LONG-20/21` 后是
`0 PASS / 0 FAIL / 181 NOT_EVALUATED / exit 2`。这证明错误完成态能被稳定拦截，不能改写成“生成模型
已经合格”。

证据见 [review metadata](build/maturity-v22-20260717/real-physics-structural-review/finalization_metadata.json)、
[review request](build/maturity-v22-20260717/real-physics-structural-review/validation/U-b325e0f1a375.structural-semantic-review-request.json)、
[warning metadata](build/maturity-v22-20260717/real-physics-structural-warning/finalization_metadata.json) 和
[qualification](build/qualification-maturity-v22-docfix-20260717-no-manifest.json)。

## 13. 2026-07-17 v23 相邻双 unit 原子事务红蓝复测

### 13.1 红队问题：跨 unit 权限最容易被三个假等价击穿

v22 仍把每个 unit 当作结构边界。要处理分块边界上的重复小段，最危险的实现会把三组不同概念
混成一件事：

1. 把“扫描到候选”等价为“用户已经授权执行”；
2. 把“一侧 fragment 验证通过”等价为“整对事务可以提交”；
3. 把“机械 source mapping 通过”等价为“结构语义与最终交付通过”。

红队据此攻击共享 member、standalone/transaction 双占、两个 transaction 重复占用、单侧 warning、
DOCUMENT failure、repetition 后置失败、partial 覆盖缺口、旧 review candidate 覆盖、compile failure、
second-pass seed 和 generator projection 降级。目标不是让合法路径更多，而是确保任何局部成功都不能
越过整对原子门。

### 13.2 蓝队权限模型

prepare 新增 `--structural-transaction-scope NONE|ADJACENT_PAIR`，默认 `NONE`。候选只接受恰好两个
`PENDING` unit，且必须同文件、同 heading、`left.end == right.start`、reciprocal context、part 连续、
scene 与完整 Voice 一致。inventory 明确区分：

```text
mechanical_scope_permission_granted=true
candidate_inventory_is_execution_request=false
inventory_alone_execution_authorized=false
bound_transaction_bundle_required=true
semantic_clearance_granted=false
```

这意味着 CLI 开关只授予机械候选范围，不授权某个 `STX-*` 自动执行。真正的 transaction bundle 还要
精确绑定 inventory SHA、transaction binding、两个 chunk/Voice binding 和两个 fragment。

### 13.3 原子提交与失败语义

finalizer 从 frozen source 独立重建 inventory，并建立全局 member claim。来源段使用复合
`{unit_id, paragraph_id}` 引用；联合 refs 必须恰好覆盖一次。保护项只能随完整来源段移动，不能拆离。

| 攻击面 | 预期裁决 |
|---|---|
| standalone rewrite 与 transaction 同占 member | 拒绝，零发布 |
| 一个 member 进入两个 transaction | 拒绝，零发布 |
| 任一 fragment validator FAIL/REVIEW | 整对回滚 |
| DOCUMENT gate 失败 | 整对回滚 |
| 后置 repetition 命中任一侧 | 整对回滚 |
| 全文覆盖不完整 | transaction 不进入 partial |
| compile FAIL | 不发布 review candidate |
| 失败重跑 | 保留旧 review candidate，不以空失败覆盖 |
| transaction + second-pass receipt | 拒绝，不把待审候选当 fresh seed |
| 合法真实移动 | 只进入 `rendered_review/`，顶层 `REVIEW/2` |

transaction warning proposal 当前没有独立 schema。不能拿两个 unit 级 proposal 拼成 pair clearance；
任一侧 warning 都使整对保持未决并回滚。这是功能边界，不包装成“自动复核已完成”。

### 13.4 真实材料压力与局部 smoke

| 来源 | 默认预算 pair | `1200/0` pair | 小预算 units / PENDING |
|---|---:|---:|---:|
| `physics1.tex` | 0 | 7 | 67 / 57 |
| 微信 `main.tex` | 0 | 0 | 36 / 28 |
| GPT 风格重整报告冻结稿 | 0 | 0 | 127 / 112 |

默认预算为 `max_author_chars=7000/min_author_chars=1200`。三份默认 run 都合法返回 `EMPTY`；减小
预算后也只有 physics 出现候选。该结果攻击了“开了功能就必须产出候选”的错误期待。微信稿和 GPT
报告仍只作模型负例/复杂压力输入，不作真人 Voice 正例；本轮未读取 `CET6.tex`。

真实 smoke 从完整 physics 冻结快照抽取 9,462 字节局部片段，重新 prepare 后产生一个相邻 pair。
候选把一个完整 `EXPOSITION` 段从右 unit 搬到左 unit，段内不改字：

| 检查 | 结果 |
|---|---|
| 两个 fragment / DOCUMENT / atomic gate | `PASS / PASS / PASS` |
| 真实跨 unit move | 1 |
| candidate assembly | `PASS` |
| delivery / exit | `REVIEW/2` |
| semantic mapping | `NOT_EVALUATED` |
| external review | `PENDING_EXTERNAL_REVIEW` |
| publish | `REVIEW_CANDIDATE -> rendered_review/` |
| compile / source modified | `NOT_RUN / 0` |
| completion claim | false |

review request 绑定全部 source-to-target mapping、跨 unit delta、compound refs、边界和内外 context hash；
canonical request SHA 为 `ba119dcc03d3b161a0c0b83400102473d35593d8a4a4dccaba04c5bd6c486c08`。
这条结果只证明原子状态机和待审工件成立，不是全文改写，不证明物理正确性或自然度。

### 13.5 隔离前向行为

三条 fresh 子代理请求没有获得已知候选、transaction ID 或预期结果，并被禁止读取 tests、旧 build
与报告。它们给出三种不同裁决：

| 请求 | 结果 | 实用性判断 |
|---|---|---|
| physics 局部稿，允许相邻 pair | 新快照有 2 units / 1 candidate，但跨块移动会打乱题干-解答对应；提交 2 `NO_CHANGE`，空 PATCH | 候选不是改动配额 |
| 微信 `main.tex`，自行找 pair | 36 units / 28 PENDING / 28 个不同 heading，`EMPTY/0`，不降低预算硬造候选 | 无候选时能停止 |
| `physics1.tex`，要求跨 3 units 并标完成 | `UNRESOLVED/NOT_RUN`，无输出目录，completion claim=false | 越权请求未被偷换成 pair |

physics `NO_CHANGE` run 的 finalizer 为 `PASS/0`、assembly replay `PASS`，源与 rendered SHA 相同，
但 `humanize_completion_claim_allowed=false`，compile 与 fresh second pass 均 `NOT_RUN`。这说明
finalizer 的工件 PASS 没有被代理扩写成“全文 Humanize 已完成”。

这些任务是独立上下文的实用性测试，不是 sealed public case，也没有外部签名隔离证明；三 unit
拒绝甚至没有文件工件。因此它们可补充行为证据，不能进入 E3 或把 184 个资格原子写成 PASS。

证据：[physics forward metadata](build/maturity-v23-20260717/forward-real-pair/pair-run/finalization_metadata.json) 和
[微信 forward decision](build/maturity-v23-20260717/forward-wechat/structural_candidate_decision.json)。

### 13.6 回归与最终裁决

最终共运行 540 项测试，整体 `OK (skipped=2)`；20 个脚本 `py_compile/--help` 全通过；官方 quick
validator 通过。两份 30 文件 generator projection 逐路径逐字节一致，且保留 transaction 能力、移除
资格控制面。资格原子增至 184 个，无 manifest 审计仍为
`integrity=PASS / NOT_EVALUATED / 0 PASS / 0 FAIL / 184 NOT_EVALUATED / exit 2`。

当前发布判定：相邻双 unit 事务的权限、绑定、原子回滚和 REVIEW-only 发布已形成可重放证据；仍不
支持超过两个 unit、非相邻、跨文件、跨标题、标题解锁、拆段或整段删除，也没有外部可信语义签名链。
因此本轮提高的是拒错成熟度，不是生成资格。

证据：[真实 pair metadata](build/maturity-v23-20260717/real-physics-pair-run/finalization_metadata.json)、
[transaction review request](build/maturity-v23-20260717/real-physics-pair-run/validation/STX-5990571b2b6d7f38849461b0.structural-transaction-review-request.json)、
[physics 小预算 inventory](build/maturity-v23-20260717/stress-physics-adjacent-small/structural_transaction_inventory.json)、
[final unittest log](build/maturity-v23-20260717/final-unittest.log) 和
[qualification](build/qualification-maturity-v23-20260717-no-manifest-final.json)。

## 14. 2026-07-17 v24 候选 disposition 红蓝复测

### 14.1 红队复现：两个节点完成，边却被静默删除

v23 第 13.5 节的 physics fresh run 是本轮的 pre-fix 反例。冻结状态为：

```text
structural_transaction_inventory.status=READY
structural_transaction_candidates=1
unit bundles=2 NO_CHANGE
submitted transactions=0
```

旧 finalizer 没有以冻结 inventory 为全集统计候选，只看提交目录中是否存在 transaction。于是未提交的
`STX-*` 没有进入任何机器状态，最终却得到 `PASS/0`、`FINAL` 和正式 `rendered/`。代理在会话里说
“移动会打乱题干-解答”，但没有绑定当前候选，也没有双侧来源证据。红队因此把旧结果重新定性为：

| 层 | 是否闭合 |
|---|---|
| 左 unit 文本 | 是，`NO_CHANGE` |
| 右 unit 文本 | 是，`NO_CHANGE` |
| pair candidate | 否，无 execution/decline |
| v23 顶层状态 | 错误地闭合 |

这不是一般报告措辞问题，而是调用方只读顶层状态就会接受未审候选的 fail-open。v23 真正提交
transaction bundle、成功后降级到 `rendered_review/` 的 smoke 不受这项纠正影响；漏洞只在
“READY candidate + 2 NO_CHANGE + 0 transaction”的路径。

### 14.2 蓝队修复：冻结候选逐 ID 三态闭集

v24 不再从 rewrites 目录反推候选总数，而是从冻结 inventory 构造全集：

```text
EXECUTED = execution envelope 合法，候选已被尝试
DECLINED = decline envelope、理由与双侧 evidence 合法
PENDING  = 其余所有冻结候选
```

四项计数必须回加。`EMPTY` 可直接 coverage PASS；`READY` 只有 `pending=0` 才 PASS。任一
`PENDING` 同时阻断 candidate assembly、delivery、覆盖声明和正式 `rendered/`。这使以下两条
非对称规则都成立：

- decline 不能替代 member 自身的 `REWRITE/NO_CHANGE`；
- member 自身的 `NO_CHANGE` 也不能替代 candidate decline。

decline 使用 `humanize-structural-transaction-decline/v1`，绑定 transaction/inventory、pair 顺序、
两个 chunk/Voice、枚举 reason code、至少 8 个汉字的具体理由，以及两个 member 各至少一个冻结
paragraph ref。规范化结果进入 `structural_transaction_decline_results`，候选全集进入
`structural_transaction_candidate_dispositions`。

### 14.3 攻击矩阵

| 红队输入 | 预期/实际裁决 | 防止的假闭环 |
|---|---|---|
| 2 个普通 `NO_CHANGE`，无 candidate disposition | `PENDING`、`REVIEW/2`、无正式 rendered | 节点完成冒充边已审 |
| 合法 decline，但没有 unit bundle | candidate 可 `DECLINED`，unit 仍 PENDING | decline 冒充正文完成 |
| stale transaction ID | 拒绝，不占 disposition | 旧工件清除新候选 |
| stale inventory SHA | 拒绝 | 跨快照重放 |
| stale transaction binding | 拒绝 | 同 ID 异 pair |
| unit 顺序错位 | 拒绝 | 左右 member 调包 |
| chunk binding 漂移 | 拒绝 | 对旧正文作新裁决 |
| Voice hash 漂移 | 拒绝 | 对不同声线工件重放 |
| “已经审阅，无需调整，结构合理” | reason 不具体，拒绝 | 用审稿腔代替证据 |
| evidence 只命中一个 member | 拒绝 | 单侧观察冒充 pair 审阅 |
| evidence 指向未知 paragraph | 拒绝 | 伪造定位 |
| evidence 重复 | 拒绝 | 用重复引用凑数量 |
| 同一 ID 同时 execution 与 decline | 前置冲突拒绝 | 互相矛盾的双完成态 |
| 两条重叠边只处置一条 | 另一条保持 PENDING | 共享 member 自动清相邻边 |
| execution envelope 合法，后置 fragment/DOCUMENT/repetition 失败 | disposition 仍 EXECUTED，member 原子回滚 UNRESOLVED | 已尝试被伪装成未审，或失败被伪装成成功 |
| 伪造 execution envelope | 不计 EXECUTED | 无效工件占据 disposition |

测试还验证了 decline 重放确定性：同一冻结输入与同一 bundle 产生相同 disposition、规范化记录和顶层
状态。合法 decline 不 claim member，因此三 unit 链的两条重叠候选可以分别 decline；但不能只写一条
然后让共享 unit 自动清除另一条。

### 14.4 真实 physics 前向

fresh 代理只拿正式 Skill 与真实局部 TeX，不拿预期 transaction ID 或已知答案。prepare 结果为：

| 指标 | 值 |
|---|---|
| scene | `AUTO -> COURSE` |
| intensity/scope | `STRUCTURAL / ADJACENT_PAIR` |
| budget | `1000/200` |
| units | 2 PENDING |
| candidates | 1 READY |
| protected spans | 119 |

代理没有为展示 STRUCTURAL 而移动段落。它提交左 unit `NO_CHANGE`、右 unit 局部 `REWRITE`，并用
`QUESTION_ANSWER_PAIRING_RISK` decline pair。理由明确指出左末段题干、右开头题解及跨 unit 后的
顺序风险；证据覆盖两个 member。最终状态：

| 层 | 结果 |
|---|---|
| unit | `1 DONE + 1 NO_CHANGE` |
| candidate | `1 total / 0 executed / 1 declined / 0 pending` |
| candidate coverage/scope | `PASS / true` |
| structural changes | 0 |
| assembly/delivery/top/exit | `PASS/PASS/PASS/0` |
| publish | `FINAL -> rendered/` |
| compile/second pass | `NOT_RUN/NOT_RUN` |
| coverage claim | true |
| Humanize completion claim | false |
| source modified | 0 |

`PASS/0` 在此只说明这个 2-unit 局部 run 的 unit 与 candidate 证据闭合；它没有被写成整个 physics
文档完成。见 [metadata](build/maturity-v24-20260717/forward-real-pair/pair-run/finalization_metadata.json)、
[raw decline](build/maturity-v24-20260717/forward-real-pair/pair-run/rewrites/STX-d302740e480cf116946db684.decline.json) 和
[validated decline](build/maturity-v24-20260717/forward-real-pair/pair-run/validation/STX-d302740e480cf116946db684.decline.json)。

### 14.5 文风实用性：轻微净收益，不掩盖新病句

右 unit 的 diff 只涉及一个金属丝直径题解：删去“看上去……其实真正……也就是说”的主持壳，删去
“这里空气劈尖取”的无功能指示词，并把“这里不能把”定位为“计算时不能把”。独立盲读只比较
A/B 两稿，给出：

| 版本 | 自然度 | 清晰度 | 信息忠实度 |
|---|---:|---:|---:|
| before | 8.8 | 9.1 | 10.0 |
| after | 9.0 | 9.2 | 10.0 |

盲读轻微偏好 after，同时指出“但求解先要确定”略显紧缩，建议“但求解时须先确定”。这说明当前
Skill 已能减少一部分主持式 AI 壳，但仍可能在压缩中制造搭配生硬。该残余没有触发硬不变量，也不
应被机器 PASS 隐藏；它应进入下一轮质量改写样本。

盲读没有查教材、复算物理或验证公式，只能说明 A/B 内部信息保持与语言偏好。工件见
[diff](build/maturity-v24-20260717/forward-real-pair/pair-run/diffs/U-89353ebada63.diff) 和
[blind evaluation](build/maturity-v24-20260717/forward-real-pair/blind_reader_evaluation.md)。

### 14.6 回归、资格与发布判断

v24 最终运行 549 项测试，整体 `OK (skipped=2)`；20 个脚本 `py_compile/--help` 与 UTF-8 quick
validator 通过。`LONG-25` 将未处置、合法 decline、execution+decline 冲突和 stale decline 接入
固定 replay。资格合同链为 `2026-07-17.14 / 2.7.0 / 1.7.0`，无 manifest 结果仍为：

```text
integrity=PASS
qualification=NOT_EVALUATED
0 PASS / 0 FAIL / 185 NOT_EVALUATED
exit=2
```

两份 generator projection 各 30 文件、逐字节一致；decline/disposition 能力保留，LONG-25、oracle、
auditor 和 replay 控制面不进入生成上下文。见
[qualification](build/qualification-maturity-v24-20260717-no-manifest-final.json)。

当前发布裁决是：candidate disposition 的拒错面已达到可审计、可重放、可阻断虚假闭环的工程形态；
真实局部稿有轻微文风净收益；但 185 个生成资格原子仍全部未评估，compile、外部学术正确性、作者
身份、个人 Voice 和无人值守全文收敛均未完成。因此不能把“状态机成熟”写成“生成模型成熟”。

## 15. 2026-07-17 v25 成对质量与发布事务红蓝复测

### 15.1 红队重新定义“可用”：能生成候选不等于敢交正式稿

v24 的局部 physics run 曾得到 `PASS/0 -> FINAL/rendered`，盲读却发现“但求解先要确定”搭配偏硬。
这说明实用性测试不能只问“是否删掉 AI 壳、是否通过公式和 TeX 检查”，还要问：

- 改后是否出现原稿没有的新病句；
- 每处变化是否有独立读感收益；
- 图表引介、范围限定和并列分支职责是否仍在；
- NO_CHANGE 是否因为无稳定收益，而不是模型偷懒；
- 失败后交给用户的目录和 metadata 是否仍属于同一候选。

v25 因此把所有本地正常 REWRITE 改为“机械通过的待审候选”，不再直接称正式交付。这个变化会让
顶层 PASS 数减少，但对真实使用更诚实：用户拿到的是 `rendered_review/` 和可复核 request，而不是
一个状态过度乐观的 `rendered/`。

### 15.2 paired-quality 蓝队门

每个 `REWRITE/NO_CHANGE` 都有 `humanize-paired-quality-review-request/v1`。request 绑定完整 artifact、
逐 hunk、场景/范围和 validator/invariant/scanner/lexicon policy。当前本地模型只能：

1. 根据 request 找到无收益或劣化改句；
2. 局部回退或重写；
3. 把剩余候选提交外部复核。

它不能签发质量 clearance。正常状态为：

```text
mechanical=PASS
paired_quality=PENDING_EXTERNAL_REVIEW
delivery=REVIEW/2
publish=REVIEW_CANDIDATE
```

NO_CHANGE 的 request 使用相同 before/after SHA 与 `changes=[]`，只证明没有改动，不证明原文无病灶。

### 15.3 发布层红队矩阵

| 红队场景 | 旧风险 | v25 固定裁决 |
|---|---|---|
| paired request 持久化返回 None | `BLOCKED` 仍可能正式发布 | `REVIEW/2`，只进 review namespace |
| transaction 一侧 fragment 失败 | 留下另一侧孤儿 request | 两侧 request/diff/DONE 全回滚 |
| A 已发布，B 编译失败 | B metadata 指向 A validation | A canonical 原样恢复；B path 清空并单列失败记录 |
| rendered 已替换，validation 第一个 commit 抛错 | 半发布 rendered | run-dir 事务恢复旧状态 |
| validation 已提交，diff 第二个 commit 抛错 | 新旧 evidence 混合 | 两个 evidence commit 一并回滚 |
| check command 绝对路径改旧 review 稿 | 检测 FAIL 但旧字节已污染 | 外层备份恢复旧字节 |
| shell 启动延迟后台 child | 返回前 hash PASS，返回后污染 | Windows Job Object 清理整个进程树 |
| malformed rewrite JSON | argparse 2 与 REVIEW/2 混淆 | 结构化 `FAIL/1`，旧工件恢复 |
| run-dir 内 symlink/junction/hardlink | 备份可能指向外部/共享目标 | 备份前拒绝 |

finalizer 新增专门故障注入，不靠 happy path 推断：首次/替换发布 × 第一/第二 evidence commit 四种
组合均逐字节比较调用前后 run state；失败记录必须含 `failed_attempt=true`、恢复标志和
`failed_attempt_evidence_paths_reusable=false`。

### 15.4 候选队列三态对实际使用的影响

paired-quality 上线后，原队列把所有 REVIEW 候选放进 `rejected/`，会让使用者误以为候选存在硬
错误。v25 最终拆成：

```text
PASS   -> accepted/
REVIEW -> review/
FAIL   -> rejected/
```

三个 head 互斥，并发/idempotency、lineage、reviewer label 脱敏、短 storage key 和 immutable history
都继续生效。现在可以清楚区分：

- `review/`：机械候选有效，但等待外部质量判断；
- `rejected/`：合同、绑定、保护或复制/模板门硬失败；
- `accepted/`：只为未来真实顶层 PASS 保留，不由本地 caller label 或 action contract 自行进入。

这比“所有未正式通过都算 rejected”更符合实际工作流，也防止把 REVIEW 偷换成 accepted。

### 15.5 真实文风收益：C 修掉 B 的紧缩搭配

同一劈尖题解的 fresh C 与 v24 A/B 做盲读，排序 `C > B > A`。C 的主要收益不是继续删连接词，而是
改写问题进入方式：从“求细丝直径时”直接说明先确定劈尖厚度斜率，再由几何关系和条纹间距反求，
避免 A 的“看上去/其实真正/也就是说”主持壳，也避免 B 的“但求解先要确定”紧缩搭配。

盲读仍建议把“这里不能”定位成“计算时不能”，并提出公式展开和空气折射率措辞建议。后两项不在
纯文风正确性权限内，因此没有被模型自动补写。机器结果保持 mechanical PASS、paired-quality
pending、delivery REVIEW/2。证据见 [validation summary](build/maturity-v25-20260717/forward-clean/paired-quality-validation-summary.json)
与 [blind A/B/C](build/maturity-v25-20260717/forward-clean/blind-local-abc-evaluation.md)。

### 15.6 资格、回归与当前实用性裁决

最终回归为：

| 项 | 结果 |
|---|---|
| 全套测试 | 572，`OK (skipped=2)` |
| validator + finalizer | 158/158 |
| finalizer | 96/96 |
| scripts py_compile | 20/20 |
| scripts `--help` | 20/20 |
| quick validator | `Skill is valid!` |
| qualification atoms | 188 |
| no-manifest qualification | `0 PASS / 0 FAIL / 188 NOT_EVALUATED / exit 2` |
| generator projection | 两份 30 文件、逐字节一致 |

最终 projection capability/manifest/tree 分别为 `95694c8d...a74eb`、`a25442bf...5fb2`、
`c68dd710...16ee`。无 manifest 资格报告见
[qualification](build/qualification-maturity-v25-20260717-no-manifest-final2.json)。

从实用性看，v25 比 v24 更适合真实长文生产的“候选终审层”：它能保护正文、给出 diff、保留
review candidate、在失败时恢复上一版，并明确告诉调用方哪里只是机械 PASS。它仍不适合作为无人
值守自动发布器，因为外部 paired-quality 签名链、E3 隔离、188 原子真实前向、学术正确性和更广
文体真实样本都没有完成。

因此本轮结论是：**实用性从“能改、能检查”提升为“能生成可恢复、可追踪、不会冒充正式完成的
待审候选”；质量授权仍必须留给当前不存在的可信外部复核链。**

## 16. 2026-07-18 v26 入口与证据权威性复测

v26 没有把旧 v19-v25 的盲评分数重新包装成新质量证据，而是检查调用者是否会被入口文案和旁路工件
误导。结果如下：

| 检查 | 结果 |
|---|---|
| `CLEAN` 输出说明 | 改为“无批注待审候选”，不再说可直接使用 |
| 默认 `REWRITE` 说明 | 改为候选生成，明确 mechanical 与 paired-quality 分层 |
| 队列维护语义 | `PASS -> accepted/`、`REVIEW -> review/`、`FAIL -> rejected/` |
| candidate C decision | mechanical exit `0` 与 delivery exit `2` 分字段，并绑定权威 summary |
| 全套回归 | 573，`OK (skipped=2)` |
| qualification | `0 PASS / 0 FAIL / 188 NOT_EVALUATED / exit 2` |
| projection | v26 policy/builder `1.8.3`，A/B 各 30 文件且字节一致 |

这轮修复提高了“调用方不会把候选当成终稿”的实用性，但没有改变质量边界：没有外部签名
paired-quality clearance、完整 candidate C request 原件或可独立复放的原始全套测试日志。因此当前正确
定位仍是“可复核待审候选终审层”，不是无人值守发布器。

## 17. 2026-07-18 v27 外部 clearance 与证据包红蓝队

v27 针对两个可操作的证据缺口展开红队，而不是继续增加泛化文风规则。

第一，短文 validator 的完整 paired-quality request 原先主要存在于 stdout。现在
`--evidence-dir <不存在目录>` 原子保存 validation result、request 和 manifest，并绑定来源 SHA、状态、
退出码及每个证据文件的 SHA。目录抢占、来源漂移、reparse point 和中途写入失败均为 `FAIL/1`，staging
会清理，不把半包当证据。

第二，首版外部 verifier 可被 `review_record_sha256="aaaa..."` 占位符绕过，因为只验证字符串格式。
红队将其升级为 P0 并补入真实 review-record 工件：exact request/challenge/response/target 绑定，逐 target
记录问题跨度、读感后果和决策理由。缺工件、维度不全或空泛理由为 `REVIEW/2`；哈希、签名、artifact、
target 或 trust epoch 错绑为 `FAIL/1`。

专项攻击覆盖：

| 攻击面 | 当前裁决 |
|---|---|
| `alg=none/HS256/ES256` | `FAIL/1` |
| 重复/未知 JSON 键、JWK/JKU 注入 | `FAIL/1` |
| future/expired/超长 TTL | `FAIL/1` |
| unknown/retired/revoked key | `FAIL/1` |
| keyset sequence/trust epoch 漂移 | `FAIL/1` |
| 漏 change、额外 change、NO_CHANGE 空数组 | `FAIL/1` |
| 少一个质量维度 | `REVIEW/2` |
| 缺 review record | `REVIEW/2` |
| review record 占位哈希或错绑 | `FAIL/1` |
| “已人工审核/符合要求/更自然” | `REVIEW/2` |
| 有效签名但仅有本地 keyset | `REVIEW/2`，保留 crypto PASS 诊断 |
| caller 自带 anchor 或未证明 ACL 保护 | `REVIEW/2` |
| 当前 artifact 漂移 | `FAIL/1` |

grant 前还会对 request、challenge、response、keyset、anchor、review record 和 before/after 做最终字节重读；
故障注入在该窗口修改 request 或正文时均为 `FAIL/1`，不允许验签后的 TOCTOU 漂移。

本轮专项 23 项，22 通过，1 项因 Windows 无创建 symlink 权限跳过；全套 598 项为
`OK (skipped=3)`。A/B projection 各 30 文件并逐字节一致，clearance 控制面未泄漏进生成器；资格仍为
`0 PASS / 0 FAIL / 188 NOT_EVALUATED / exit 2`。

实用性提升在于：外部质量结论已经有明确、可攻击、可拒绝的接入合同，不再接受“有人说通过”或一个
占位哈希。但当前 Windows 没有 ACL-aware protected launcher，真实审批服务、私钥、一次性消费账本和
finalizer 原子接线也不存在。因此普通改写仍是 `REVIEW_CANDIDATE`，不能把测试夹具中的 external-anchor
PASS 描述成现网质量授权。

## 18. 2026-07-18 v28 短文 evidence replay 红蓝队

### 18.1 红队起点

红队没有继续增加“AI 味词表”，而是攻击 v27 的证据声明：只保存 result/request/manifest 时，删除原文就
无法复跑；同一记录第二次写入被当作失败；report-scope 与原报告没有归档；stdout/stderr、调用参数和
reviewer 隐私没有形成闭集合同。manifest 自哈希只能证明 JSON body 内部一致，不能替代执行重放。

三路独立审计共同确认：

- v27 短文 evidence 测试只有 2 项，原子故障只覆盖第二个 staged write；
- 外部 verifier 的 request fixture 使用空 `policy_hashes` 仍可进入验签；
- report scope 只做 live replay，没有离线依赖归档；
- 相同 invocation 没有内容寻址 ID，也没有“相同字节幂等、不同字节冲突”的裁决；
- reviewer label 虽未出现在 stdout，但没有递归扫描整个 evidence tree；
- policy 只绑定四个文件，漏掉 report extractor 与 Python/Unicode runtime。

### 18.2 蓝队实现

蓝队将 evidence schema 升为 v2，增加 `inputs/`、invocation、精确 stdout/stderr、execution record、
warning request、content-addressed run ID 和 record hash。REPORT_INFORMED 归档 scope/report；发布前二次
重读四类来源。相同目录逐字节一致时允许幂等，不同调用或内容冲突时保持旧记录并 `FAIL/1`。

独立 replay verifier 执行两层门：

1. integrity：strict JSON、规范字节、闭集 inventory、路径、hardlink/reparse、自哈希和跨工件一致性；
2. reexecution：比较当前六项 policy，从归档输入 subprocess 重跑 validator，核对核心状态、findings、
   request SHA、退出码与 text stdout，并在返回前重读整包。

记录损坏固定 `FAIL/1`；policy drift、proposal 无原 reviewer ID或 live-source strict 不满足固定
`REVIEW/2`；同 policy 重算一致才是 replay `PASS/0`。所有状态都固定
`academic_correctness=NOT_EVALUATED`、`paired_quality_clearance_granted=false`。

### 18.3 攻击结果

| 红队动作 | 蓝队结果 |
|---|---|
| 任一归档工件单字节篡改 | `FAIL/1`，reexecution `NOT_RUN` |
| 篡改 result 后重算普通 SHA/manifest | 跨工件 status/expected 不一致，`FAIL/1` |
| 篡改 stdout 后重算普通 SHA/manifest | stdout/result 不一致，`FAIL/1` |
| invocation 未知字段、路径穿越、后缀注入 | strict schema/path `FAIL/1` |
| extra file 或 hardlink | inventory/path `FAIL/1` |
| 所有 staged write/manifest/rename 故障 | 无半包、无残留 lock |
| manifest 写完后 source 漂移 | 提交前重读 `FAIL/1` |
| 同 invocation 重发 | 幂等，目录 SHA 不变 |
| 不同 scene 写同目录 | conflict `FAIL/1`，旧目录不变 |
| policy 漂移 | integrity PASS，reexecution NOT_RUN，`REVIEW/2` |
| 删除原 before/after/report/scope | 默认归档 replay PASS，live source 标 NOT_CURRENT |
| reviewer proposal | 原标签全目录零出现；明确不可重执行 `REVIEW/2` |
| DRAFT term / fragment strict | invocation 恢复后 replay PASS |

### 18.4 实战中发现的测试盲点

首轮临时测试全部通过后，持久化真实 research fixture 的 text replay 仍失败。finding 行输出了原绝对路径，
而 replay 使用临时路径，导致 stdout 逐字节不一致。蓝队没有把 text stdout 比较降级为“忽略路径”，而是
将公开 finding 定位收敛为稳定 basename，并让 replay 使用归档原文件名，再新增专门回归。

最终样本中原 validator 仍为 `REVIEW/2`，因为“为后续研究提供了基础”及新增风格信号未解决；replay
为 `PASS/0`，只证明这个 REVIEW 可重复。该例验证了两类 PASS 不得混写。

### 18.5 最终证据

- 全量：`617` 项，`OK (skipped=3)`；原始日志 SHA
  `0d0f412741435d63b2e579371c9cf312ed3aa5dce5959be4239a54b72a7af629`；
- validator/replay/external verifier：`66 / 16 / 24` 项，external verifier 有 1 项 Windows symlink 跳过；
- 脚本：`22/22 py_compile`、`22/22 --help`；Skill UTF-8 模式 quick validation PASS；
- projection：A/B 各 30 文件、byte diff 0、manifest
  `695a49a3129c486a8440b92aada6b1d2bd8b5f857dd6cddfa930cc6825145213`；
- qualification：integrity PASS、qualification NOT_EVALUATED、`0/0/188`、exit 2；
- 持久 replay run：`hvr1-1db531017fda5ad6b69ea778abfcfb611ede8fbe1dfebf46ef4320fe8bdc7e16`。

机器摘要见 [v28 authority pointer](build/humanize-academic-authority-v28-20260718.json)。pointer 只聚合可复核
路径与哈希，不替代 manifest、测试日志或外部信任根。

### 18.6 实用性裁决

短文机械验证现在可以脱离原路径复核，也能明确告诉调用方“为什么不能重放”。这解决的是证据可信度和
错误完成态，不直接改善某一段文字的读感。真实文风收益仍由 paired-quality 外部复核决定；当前没有受
保护 launcher、不可访问私钥、在线消费账本或 finalizer 原子接线，故普通改写仍是待审候选。
