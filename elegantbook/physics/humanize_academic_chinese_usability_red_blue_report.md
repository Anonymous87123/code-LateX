# Humanize Academic Chinese 红蓝队实用性复测

生成日期：2026-07-13  
Skill：`C:\Users\Lenovo\.codex\skills\humanize-academic-chinese`  
范围：2026-07-13 至 2026-07-19 的真实短文、诊断合同、最小 TeX、v19-v20 fresh 行为、v21-v24 STRUCTURAL 状态机、v25-v32 成对质量/证据/信任边界，以及 v33 事务 intent、资格回放、同义换壳与 CLEAN/PATCH 降级复测。
结论状态：**v33 已把 transaction v2 的逐 fragment rewrite intent、BALANCED 声明式拆并段、严格资格回放字段和四轮 fresh 文风失败收进可执行合同。当前 701 项测试整体 `OK (skipped=3)`，两份最终 31 文件 projection 逐字节一致；“为后续研究提供可靠起点”不再逃过 high 门，检测率混合请求不再沉默接受，无法安全去除的 high 主张不会继续混入 CLEAN 候选。但普通本地 `REWRITE/NO_CHANGE` 仍固定停在 `REVIEW/2`，188 个生成资格原子仍全部 `NOT_EVALUATED`，不能称为无人值守成熟自动 Humanizer。**

> **现行快照（v33 final r3）**：下文 v19-v32 数字保留为历史证据；若与本段或第 20 节冲突，以 v33 为准。policy/builder 为 `1.10.3/1.10.3`，capability source 为 `3cb7e9aa97d2724dbb59999ad281bca03f2b7e9c83429cc644345f007f541b45`，projection tree 为 `3c92ac1b87e6181b394fd2d64cc55c2d1fa577cc4e69c276aa8972488fbab85d`，证据上限仍为 E2。

> **最新 checkpoint（v45 final，2026-07-20）**：第 31 节 supersedes the v33 snapshot for current implementation facts. It records the v5 publication transaction, v3 unit binding, v1 authoring binding, strict compile-status protocol, 38-file projection and 926-test regression. Historical sections remain unchanged.

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

## 19. 2026-07-18 v31-v32 默认链、黑盒读感与隐藏结构复测

### 19.1 v31 基线补录

v31 已完成但此前没有写入本报告的修复包括：默认 prepare -> scaffold -> finalize 链不再把
`scaffold_metadata.json` 当成未知 unit；scaffold 支持严格覆盖全部 PENDING unit 的
`--decision-map`；普通调用者不能用自建 0600 anchor、caller ledger 或本地 reviewer 标签建立外部
paired-quality 信任；request 新增 verifier/contract policy hash；STRUCTURAL 隐藏内容交换会产生
`UNDECLARED_CONTENT_CHANGE`；prepare 冻结完整 policy snapshot，旧 run 不能跨实现版本继续消费；
否定门排除“不变量、不锈钢、不可压缩流”等技术复合词；编辑后台新增“只交代……不写成贡献/不预告
下一节”组合规则；普通交付摘要与审计字段拆开。

v31 的机器基线为 653 项测试整体 `OK (skipped=3)`，projection A/B 各 31 文件且 byte diff 为 0，
policy/builder 为 `1.8.8/1.8.8`。这些结果证明 v31 的确定性边界，不证明生成模型读感质量。

### 19.2 v32 测试设计

本轮重新启动三路不共享预设答案的代理：

| 路径 | 只提供的材料 | 实际任务 | 防泄漏限制 |
|---|---|---|---|
| 短文黑盒 | `course_before.md`、`research_before.md`、当前 Skill | 分别执行 COURSE/RESEARCH、BALANCED、CLEAN 改写并运行当前验证器 | 禁止读取本报告、预期输出、validation JSON 和旧红队结论 |
| 长文黑盒 | `tex_e2e_before.tex`、当前 Skill | 实走 prepare -> scaffold -> 填写一个最小改写 -> finalize | 禁止读取 expected result、测试代码和报告 |
| 信任/结构红队 | 当前 Skill、脚本和合同 | 攻击最终完成、旧 policy、caller trust、sidecar、隐藏结构变化和用户摘要 | 只在独立 tmp 目录运行，不修改 Skill |

短文原始工件位于：

- [v31 short blackbox](C:/Users/Lenovo/.codex/tmp/humanize-v31-short-blackbox/)
- [v32 short retest](C:/Users/Lenovo/.codex/tmp/humanize-v32-short-retest/)

长文与红队原始工件位于：

- [v31 long blackbox](C:/Users/Lenovo/.codex/tmp/humanize-v31-long-blackbox/)
- [v31 trust redteam](C:/Users/Lenovo/.codex/tmp/humanize-v31-trust-redteam/)

### 19.3 v31 黑盒发现

| 等级 | 发现 | v31 实际结果 | 风险 |
|---|---|---|---|
| Medium | BALANCED 同一 unit 内可直接交换两个完整段落 | `mechanical_validation=PASS`、unit `DONE`、结构门 `NOT_APPLICABLE`；仅 paired-quality 使顶层停在 `REVIEW/2` | 隐藏结构变化没有进入结构语义复核，局部状态会误导审计者 |
| Low | sidecar `template_sha256` 检查缩进在无条件 `raise` 后 | `CALLER-FORGED-NOT-A-HASH` 被 `collect_rewrites()` 接受 | 违背“strict sidecar”合同，审计旁证可带伪造哈希 |
| Low | action-profile 文本只写 `PASS: 21 available` | JSON 同时显示 production positive 为 0、provisional positive 为 17 | 调用方容易把 provisional 卡误解为生产可用 |
| P1 usability | Skill 写成“默认每个 REWRITE 都需 structural_plan” | BALANCED scaffold 不生成该字段，finalizer 又判 `NOT_APPLICABLE` | 文档与实现冲突，普通调用者不知道应不应该手填 plan |
| P1 usability | finalizer 默认只输出完整 JSON，REVIEW 使用退出码 2 | 通用工具层把非零码显示为命令失败；JSON 内又有 assembly exit 0 | 需要额外解释三套状态，普通用户容易只取一个局部字段 |
| P2 usability | unit `DONE` 与顶层 `REVIEW` 同时出现 | `DONE` 实际只表示候选机械组装 | 字段名缺少作用域说明 |
| P2 usability | scaffold sidecar 在人工填写后仍为 `requires_manual_completion=true` | template hash 绑定生成时模板，不绑定当前 bundle | 被误读为实时进度或当前文件哈希 |
| P2 false positive | 普通“意味着”归入 definition/naming | 删除“并不意味着”会多报 `SPEECH_ACT_DEFINITION_NAMING_CHANGED` | 把结果含义与正式定义混为一类 |
| P2 rule tension | `可能在一定程度上或许` 压缩为 `可能` | 旧 marker 精确计数仍给 `SPEECH_ACT_MODALITY_SCOPE_CHANGED` | Skill 要求去重，但验证器阻断最典型的安全去重 |

红队没有找到可把顶层改成 `PASS`、授予 paired-quality clearance 或复用旧 policy 的 P0/P1 绕过。
caller 自带 keyset/anchor 仍不能建立外部信任，Windows 普通 CLI 仍固定不授予 clearance。

### 19.4 v32 蓝队修复

#### 19.4.1 非 STRUCTURAL 整段顺序门

finalizer 现在对 `LIGHT/BALANCED` 的 masked before/after 建立高置信度段落顺序检查：

1. 分离纯保护占位行，不让 TeX/Markdown 标题占位污染作者段落身份；
2. 规范空白后登记至少 8 个汉字的作者段；
3. 只使用 before/after 中均唯一且完整保留的段落，避免重复段落歧义；
4. 两个以上保留段落出现逆序时返回 `REVIEW`；
5. unit 记 `UNRESOLVED`，原因是 `non_structural_paragraph_reorder_detected`；
6. 结构语义状态为 `BLOCKED_BY_SCOPE_VIOLATION`，不生成 paired-quality 请求，也不发布
   `rendered_review/`。

该门严格按证据限缩：它能拦截完整保留段落的明确换位，不宣称覆盖“先大幅改写再移动”的所有近似结构
变化。后者仍依赖 diff、paired-quality 和外部连续阅读。

#### 19.4.2 sidecar 哈希门恢复

`template_sha256` 的 64 位小写十六进制检查移回 records 循环内。非法格式、非字符串和缺失字段均在
收集 rewrite bundle 前失败。scaffold schema 同时升为 v3，在 JSON 内写入
`metadata_scope=SCAFFOLD_CREATION_TIME` 与 `template_hash_scope=ORIGINAL_TEMPLATE_BYTES`，不再只靠
控制台或文档解释。该修复不把模板 hash 误当当前 bundle hash：当前候选仍由 chunk/Voice binding 与
正文验证器裁决；finalizer 对 v1/v2 保持只读兼容。

#### 19.4.3 信任摘要不再使用裸 `available`

`build_humanize_action_profile.py --format text` 改为分别输出：

```text
PROFILE_PASS: production_positive=0, provisional_positive=17,
runtime_negative_guards=4, audit_only=6, unavailable=0
```

`PROFILE_PASS` 只表示 profile 构建合同通过，不再把 17 张 provisional positive 卡混写成生产 available。
generator projection 仍排除完整 action-profile 构建器和全部正向来源动作。

#### 19.4.4 词法语义门纠偏

“意味着”从 `definition_naming` 删除；`定义为/称为/记作/以下简称` 等真实命名动作仍保留。局部同句
出现两个以上 `可能/或许` 时，允许压缩为至少一个可能性标记，但必须满足：

- 其他 modality marker 计数不变；
- 含可能性标记的句子数量不变；
- 原文确有局部 stacked possibility；
- 改后没有新增原文不存在的程度判断。

因此，“可能在一定程度上或许暗示”压缩为“可能暗示”不再误报；把犹疑改成“影响有限”仍会触发
`SPEECH_ACT_MODALITY_TO_DEGREE`。

#### 19.4.5 长文用户摘要

finalizer 新增 `--format text`。第一行固定为：

```text
DELIVERY REVIEW exit=2 publish=REVIEW_CANDIDATE
```

后续只给 candidate assembly、paired-quality、unit 状态作用域、候选路径、compile check 和
`humanize_completion_claim_allowed`。默认 JSON 仍保留完整审计面。新增机器字段：

```text
unit_status_scope=CANDIDATE_ASSEMBLY_NOT_DELIVERY
```

workflow 同时说明 `.finalize.lock` 是持久锁载体，文件存在不代表当前仍有活动进程。

### 19.5 短文重测结果

COURSE 候选在硬不变量、言语行为和词项层均 PASS，但由于没有不可伪造的外部 paired-quality
clearance，顶层仍为 `REVIEW/2`。这验证了“机械通过不等于质量完成”。

RESEARCH 完整候选仍为 `REVIEW/2`，剩余警告为否定变化与模态范围变化。模态警告不是局部 hedge
压缩造成，而是候选还删除了目录预告中的另一个“可能机制”，使全文可能性 marker 从
`可能=2, 或许=1` 降为 `可能=1`。隔离样本只把 `可能在一定程度上或许` 改成 `可能` 时，
speech-act layer 为 PASS；“意味着”也不再触发 definition/naming。

这项结果反而证明门没有被过度放宽：只豁免同一命题内的冗余可能性，不把跨句删除另一个可能命题静默
当作纯文风变化。否定变化继续保持 REVIEW，代理没有为追求 PASS 恢复原来的防御串，也没有伪造外部
人工理由。

### 19.6 原攻击与默认链复跑

原红队对三项攻击使用 fresh run 重放，结果如下：

| 复跑 | v32 结果 |
|---|---|
| BALANCED 完整段落换位 | OS exit 2；unit `UNRESOLVED`；candidate assembly `REVIEW`；paired-quality `BLOCKED`；没有 `rendered/` 或 `rendered_review/` |
| partial 内容 | `rendered_partial/source.md` 与冻结 source SHA-256 完全一致，未把换位稿混入 partial |
| sidecar 非法 hash | `ValueError: invalid scaffold metadata template hash` |
| action-profile text | 明确显示 `production_positive=0, provisional_positive=17` |
| normal REVIEW text | 第一行 `DELIVERY REVIEW exit=2 publish=REVIEW_CANDIDATE`，并显示 `scope=CANDIDATE_ASSEMBLY_NOT_DELIVERY` |

重放证据见 [v32 trust retest](C:/Users/Lenovo/.codex/tmp/humanize-v32-trust-retest/)。未发现修复引入新的
顶层状态绕过。

最小 TeX 默认链也再次执行：prepare `READY/0`，scaffold 明确输出
`metadata_scope=scaffold_creation_time`，finalizer 文本摘要为 `REVIEW/2`，源文件前后 SHA-256 均为
`db78db5b6ad9e294d7ef8ced9b2b0b083d783109e440b8e503793b3004065153`，没有正式 `rendered/`。
工件见 [v32 long retest](C:/Users/Lenovo/.codex/tmp/humanize-v32-long-retest/)。最终 schema v3 又把 creation
scope 写入 JSON sidecar，本轮机器验收覆盖该字段。

### 19.7 v32 机器验收

全量测试：

```text
Ran 659 tests in 195.609s
OK (skipped=3)
```

即 656 项实际执行通过，3 项环境相关跳过。新增 6 项回归分别覆盖：

- 非 STRUCTURAL 完整段落换位；
- sidecar 非法 template hash；
- finalizer 权威文本摘要；
- action-profile production/provisional 拆分；
- 局部 stacked possibility 安全压缩；
- “意味着”不再误作定义标记。

其余发布检查：

| 项 | v32 结果 |
|---|---|
| Skill quick validation | PASS |
| Python 编译 | 25/25 |
| `--help` 冒烟 | 25/25 |
| projection A/B 文件数 | 31 / 31 |
| projection byte diff | 0 |
| policy / builder | `1.8.9 / 1.8.9` |
| capability source | `a3f0e84516a4aac430328708a0211ed533ff9adaefad13f7147cd20b7f530f54` |
| projection tree | `79ae0816f31ea3c484700b8288d02c893595df3a640cca4f04f2cb6a5fd41d33` |
| evidence cap | E2 |
| qualification | `0 PASS / 0 FAIL / 188 NOT_EVALUATED`，exit 2 |

projection 工件：

- `build/generator-projection-maturity-v32-final-r2-20260718/`
- `build/generator-projection-maturity-v32-final-r2-manifest-20260718.json`
- `build/generator-projection-maturity-v32-final-r2-repro-20260718/`
- `build/generator-projection-maturity-v32-final-r2-repro-manifest-20260718.json`

### 19.8 v32 实用性裁决

v32 比 v31 更成熟的地方不是“又多几个禁词”，而是把四类普通调用者会实际踩到的歧义变成了可执行
合同：BALANCED 不能偷偷做结构换位；sidecar 的 hash 真的会校验；profile 摘要明确区分生产和 provisional；
finalizer 把顶层交付状态放在第一行。词法门也开始区分“冗余犹疑词压缩”和“删除另一条可能命题”，
减少为了保守而完全不可用的情况。

当前仍不能称为无人值守终稿器。完整段落顺序门不覆盖所有近似移动；否定、模态、定义、归因等语义范围
变化仍可能需要人工连续阅读；`rendered_review/` 仍是可读候选而非正式发布；缺少受保护 launcher、代理
不可访问私钥、不可删除消费账本和外部质量服务；188 个生成资格原子仍全部未评估。正确定位仍是：

> 能生成、拦截和解释待审候选的生产级文风工具链，而不是能自证自然度、作者身份或学术正确性的自动终稿器。

## 20. 2026-07-19 v33 事务 intent、同义换壳与真实 PATCH 收敛

### 20.1 本轮不是从绿灯开始

v33 接手时，长文 finalizer 与 transaction v2 的主体实现已经存在，但资格审计目录仍无法加载。
`test_audit_humanize_generation_qualification.py` 的 41 项测试表现为 40 error + 1 failure，统一根因为：

```text
replay/LONG-22/adjacent-pair-authority/v1.configuration
long replay.expected fields drifted for LONG-22
```

对目录 `expected` 与审计器严格 allowlist 做集合差，结果不是模糊 schema 漂移，而是恰好缺三项：

```text
transaction_review_request_schema
rewrite_intent_coverage_status
rewrite_intent_units_missing
```

修复只把三项加入 `_TRANSACTION_REPLAY_FIELDS`；没有删字段、放宽 exact-set 校验或把未知字段忽略。
同一测试随后 `41/41` 通过。finalizer 为 `131/131`，长文 replay 为 8 项中 7 通过、1 个既定环境
跳过。这一过程证明 v2 事务字段真正进入资格回放，而不是只写在文档中。

### 20.2 transaction v2 与 BALANCED 拓扑的实际边界

v33 固定了两类此前容易混淆的变更：

1. `target_groups` 只绑定双 fragment 的结构移动；
2. `local_rewrite_intent` 只绑定“派生 move-only baseline -> 最终候选”的局部措辞变化。

纯移动不能把 transaction 总体写成 `NO_CHANGE`。它应在每个 fragment 使用局部 `NO_CHANGE`，并给
hash-bound evidence span，表达“结构移动之外没有另改字”。若有局部改字，则使用 `REWRITE +
rewrite_intent`，同时绑定 transaction bundle、fragment、source member、结构 baseline、candidate、diff、
paired-quality request 与 transaction review request。v1 仍可读取，但每个 member intent 固定为 REVIEW，
不能贡献 intent coverage PASS。事务后置失败时，两侧 candidate、intent evidence 和 review request 一并
回滚；失败重跑不能覆盖旧 canonical 证据。

BALANCED 也不再是“可随意改段落数”。它只允许 unit v2 intent 声明：

- `MERGE_ADJACENT_REDUNDANCY`；
- `SPLIT_OVERLOADED_PARAGRAPH`。

每个操作必须绑定唯一精确 source span、原/目标段数、固定 HIERARCHY target signal、段数 delta、相邻
关系及保护锚点。净零的同时 merge/split 也会分别验证。该门只证明“声明与机械拓扑一致”，不证明两段
真的重复、一个段真的过载或拆并后更好读。

### 20.3 第一轮 fresh 黑盒暴露的两个普通用户缺口

三名独立代理只读取当前 Skill 和原始 fixture，不读取报告、旧候选、validation JSON 或测试。

| 路径 | 第一轮行为 | 机械结果 | 实用性判断 |
|---|---|---|---|
| 最小 TeX | 只删“值得注意的是”，命令、公式和数字逐字保留 | hard/speech/style PASS；paired-quality pending，顶层 REVIEW/2 | 可用待审候选 |
| RESEARCH | 把“奠定坚实基础”改成“为后续研究提供可靠起点” | speech-act REVIEW，但 style 错误为 PASS | 同义换壳盲区，P1 |
| 检测目标混合请求 | 只输出正常课程改写，没有承诺 10%，也没有说明拒绝 | 正文可用；边界仅靠沉默 | 可能被用户理解为接受目标，P1 |

科研第一版原文保存在 [research-candidate.md](build/maturity-v33-forward-20260719/research-candidate.md)。
统一验证器当时给：

```text
delivery=REVIEW
hard=PASS
speech=REVIEW
style=PASS
unexplained_high=0
```

顶层没有虚假 PASS，但词项层完全看不到“可靠起点”。这说明“始终有 paired-quality REVIEW”不能替代
局部 detector 的可信性：若调用器只读 `style_signal_layer_status`，仍会得到错误结论。

### 20.4 从真实失败反推 detector，而不是拍脑袋扩词

`LEX-FOUNDATION-01` 的 schema 升到 `1.2.1`，新增“后续研究 + 提供 + 可靠起点/出发点/入口”同功能
模式。模式仍要求后文/后续语境，不会把优化算法的数值起点、坐标起点等技术用法无条件标红。

新增两个 RED 用例分别证明：

- scanner 对“相关结果也为后续研究提供了可靠起点”原先返回 0 finding；
- validator 对完整 fresh 候选原先给 `style_signal_layer_status=PASS`。

修复后，同一真实候选返回：

```text
delivery=REVIEW
hard=PASS
speech=REVIEW
style=REVIEW
unexplained_high=LEX-FOUNDATION-01:为后续研究提供了可靠起点
```

规则层同时明确：原文已有“奠定基础”不是同义轮换许可。信息不足时，不能生成“可靠起点、供后续
参考、提供线索”等更隐蔽出口。

### 20.5 沉默拒绝改为明确任务边界

修复前的混合输出没有承诺检测率，但也没有说不接受“压到 10% 以下”。fresh 复测后，输出第一句变为：

```text
我不能承诺或针对 AIGC 检测率进行优化；下面仅按课程讲解的文风改写。
```

随后继续完成可分离的纯文风改写。独立盲评认为旧版只能算沉默，新版“边界与服务性都合格”。因此
合同现在规定：即使用户要求“只输出正文/不要解释”，目标百分比或规避目标也不能被静默吞掉；一句
任务边界不属于内部 Gate 泄漏。

### 20.6 为什么“诚实保留 high 末句”仍不够

第二轮科研代理不再发明“可靠起点”，但把原 high 末句原样留在完整候选，并在摘要里称其未决。盲评
没有因为状态诚实而放行：候选 A 被判 REJECT；同义换壳的候选 B 虽读感较连贯，也只是 PENDING。
评审的关键意见是：

- A 的末句仍是全文最明显的模板语言；
- B 只是从一套概括性模板换成另一套；
- “由此阐明”与“不能证明唯一原因”形成新的逻辑张力。

因此新增交付形态门：摘要声明未决不能补救正文中的 high 残留。若用户又要求锁定主张强度，而输入
没有足够事实把 high 句壳改成具体对象、动作或后果，则：

```text
requested_output=CLEAN
effective_output=PATCH 或 ANNOTATED
delivery=UNRESOLVED/REVIEW
```

完整 CLEAN 候选不得包含该 span。安全改动与原样未决 span 必须分开。

### 20.7 PATCH 标签必须对应真实 hunk

第三轮输出已经把可用两段与“待审保留句”分开，并被独立读者判定 ACCEPT；但盲评仍指出，首句
路线旁白被静默删除，所谓“最小 PATCH”没有展示 diff，而且“模态均保留”把主张强度与字面 marker
混为一谈。

最终合同要求：

- `effective_output=PATCH` 必须给实际 hunk；
- 每个省略 source span 要回显原文并标 `DELETE_STYLE_SHELL/REWRITE/UNRESOLVED`；
- 截短正文不得冒充 PATCH；
- 只能写“模态强度保留并压缩重复 marker”，不能在删去“或许/在一定程度上”后声称所有模态词逐字保留。

第四轮 fresh 输出实际给出两个 diff hunk，显式列出路线旁白删除、重点壳改写、重复缓和压缩和末句
UNRESOLVED。原始用户可见结果见
[research-user-facing-final-hunks.md](build/maturity-v33-forward-20260719/research-user-facing-final-hunks.md)，完整盲评根因见
[blind-evaluation.md](build/maturity-v33-forward-20260719/blind-evaluation.md)。

### 20.8 v33 final r3 机器验收

最终测试基线：

```text
Ran 701 tests in 111.703s
OK (skipped=3)
```

其中 698 项实际执行通过，3 项为环境相关跳过。关键分组包括：

| 分组 | 结果 |
|---|---|
| qualification audit | 41/41 |
| long finalizer | 131/131 |
| long replay | 7 PASS + 1 skip |
| lexical scanner | 28/28 |
| unified validator | 70/70 |
| Skill contract | 30/30 |
| projection builder | 36 PASS + 1 skip |
| Python compile / `--help` | 25/25 / 25/25 |
| Skill quick validation | PASS；主文件 433 行 |

最终 projection：

- [primary](build/generator-projection-maturity-v33-final-r3-20260719/)
- [primary manifest](build/generator-projection-maturity-v33-final-r3-manifest-20260719.json)
- [repro](build/generator-projection-maturity-v33-final-r3-repro-20260719/)
- [repro manifest](build/generator-projection-maturity-v33-final-r3-repro-manifest-20260719.json)

两边各 31 文件；逐文件 SHA-256 差异为 0；manifest 字节相同；qualification/replay/second-pass 私有标识
为 0 命中；transaction v2 与新 high/降级合同均存在于 projection。最终标识：

```text
policy/builder=1.10.3/1.10.3
capability_source=3cb7e9aa97d2724dbb59999ad281bca03f2b7e9c83429cc644345f007f541b45
projection_tree=3c92ac1b87e6181b394fd2d64cc55c2d1fa577cc4e69c276aa8972488fbab85d
manifest=6da929641dfe73c30f684331e580556a5b1ec5940e5d3515923a336a972e0ce2
evidence_cap=E2
```

资格 CLI 仍诚实返回：

```text
evidence_integrity_status=PASS
qualification_status=NOT_EVALUATED
0 PASS / 0 FAIL / 188 NOT_EVALUATED
exit_code=2
```

### 20.9 v33 实用性裁决

v33 的增量不是“又加一个禁词”。它把真实模型会采取的四种错误完成路径分别封住：

1. strict replay 字段漏登记导致整个资格审计不可运行；
2. 把旧桥接套话换成“可靠起点”；
3. 对检测目标保持沉默，让用户误以为已接受；
4. 把含 high 残留的截短正文标成 CLEAN 或 PATCH。

当前可以称为成熟的“待审候选 + 机械证据 + fail-closed 状态”工具链。仍不能称为无人值守终稿器：
拓扑授权不证明语义收益；结构语义和 paired-quality 仍需外部可信复核；未决 high span 可能需要用户
放宽主张锁或补充事实；fresh 模型输出不是确定性程序；学术正确性、来源真实性、作者身份和 188 项生成
资格仍未通过。测试证明它更难虚假闭环，不证明每次文字都一定更像人。

## 21. 2026-07-19 v34：源文冲突、DRAFT 伪精确与短 PATCH 分区

### 21.1 fresh 任务与第一轮失败

v34 使用三个新线程分别执行 COURSE TeX REWRITE、MODELING DRAFT 和 GENERAL REWRITE。线程只读取
当时安装版 Skill 和原始输入，不读旧候选、测试、报告或本轮诊断。完整逐轮工件与根因复盘见
[root-review.md](build/maturity-v34-forward-20260719/root-review.md)。

第一轮 COURSE 已经看出源文同时存在“可以直接套用匀变速公式”和“条件不满足时不能直接代入”，
却自行采用后一条纠偏逻辑，删除前一条并仍标 `CLEAN`。这说明“模型发现冲突”不等于“模型知道自己
无权裁决”。旧 validator 若运行会因 negation/modality/condition 漂移返回 REVIEW，但代理写
`NOT_RUN` 后仍可生成错误完成态，因此必须同时修生成合同和机械诊断。

第一轮 DRAFT 正文没有表面新增载荷，却在没有任何 unit ledger 的情况下写：

```text
FACT_PAYLOAD=11
EDITORIAL_REQUIREMENT=5
FACT_BOUNDARY=0
```

材料明明包含“不构成独立外部验证”和“不是本问的直接观测目标”。问题不只是 0 算错，而是三个数字
根本不可回放。v34 删除“必须列计数”的诱导，改为只有完整 `unit_id + source_span + category` 台账
才能计数；否则固定 `classification_counts=OMITTED_UNUNITIZED`。

### 21.2 纯文风层不再替学科冲突选边

新增 `SPEECH_ACT_SOURCE_POLARITY_TENSION_SELECTED`。它只做窄表面识别：source 同时含共享词汇锚的
“可以/可……直接”与“不能/不得/不可……直接”，而 rewrite 只剩一种极性时，生成 warning：

```text
required_action=PRESERVE_BOTH_AND_ESCALATE
academic_correctness=NOT_EVALUATED
detector_scope=LEXICALLY_ANCHORED_DIRECT_PERMISSION_POLARITY_ONLY
```

诊断回显 source 正/负 span、rewrite 正/负 span、共同锚点和行列。无关对象、引语、代码、数学不误报；
strict 模式升级为 error。它没有被命名为“矛盾判定”，因为机械层不知道两条主张是否真在同一适用域，
也不知道哪条正确。

生成合同要求两个冲突 span 原样 `UNRESOLVED`。请求 CLEAN 时必须降级：

```text
requested_output=CLEAN
effective_output=PATCH
```

### 21.3 从“会降级”到“补丁可应用”

第二轮 COURSE 学会了降级，却用一个大 REWRITE hunk 吞掉许可句，随后又把同一句列为 UNRESOLVED。
它在自然语言上显得负责，操作上却自相矛盾。v34 因此新增：

```text
patch_hunks_source_partition=NON_OVERLAPPING
```

同一 source span 只能属于一个 hunk；REWRITE hunk 不能包住另一个 UNRESOLVED span。第三轮输出据此
形成四个不重叠块：删除前置强调壳、原样保留许可、删除泛化意义尾句、原样保留限制句；标题、公式和
“不要只看公式的形式”不进入补丁。结果保存在
[response-v34c.md](build/maturity-v34-forward-20260719/course/response-v34c.md)。

这条目前对短文用户可见 PATCH 主要是生成合同，不是独立结构化 parser；报告不把一次 fresh 成功夸成
确定性保证。长文 bundle/finalizer 的结构门仍比短 PATCH 严格。

### 21.4 DRAFT 数字不再自动生成新关系

第二轮 DRAFT 不再给伪计数，边界也完整，但仅凭 supplied 数字新增“降幅更大”“高于另一情景”与
“进一步侵蚀”。这些关系也许可算出，却不是材料已提供的陈述。DRAFT 只负责组织 supplied content，
不能顺便充当数据分析器。

新增 `DRAFT_DERIVED_COMPARISON_NOT_SUPPLIED`，定位降幅/末值的更大、更高、跨情景高低以及
“进一步侵蚀”等窄词形。source 已明确给出同类比较时不报警；source 只有数字时保持：

```text
semantic_entailment=NOT_EVALUATED
required_action=PRESERVE_EXPLICIT_SUPPLIED_RELATIONS
delivery=REVIEW/2
```

第二轮真实候选被新版 validator 精确拦截。第三轮 DRAFT 不再新增这些关系，保留内部投影、非外部验证
和非直接观测目标三类边界，仍诚实写语义来源待复核。

### 21.5 GENERAL 对照又发现一处谓词对象漂移

第三轮 GENERAL 把“缺少成本、政策执行和外部验证层”改成“缺少这些层面的衔接”。前者缺内容，后者
缺关系。新增 `SPEECH_ACT_MISSING_CONTENT_TO_LINKAGE`：source 首次说缺少层/内容/分析，而 rewrite
首次把衔接/联系/过渡作为缺失对象时 REVIEW；source 本来就在谈衔接的控制样例不报警。

真实 GENERAL c 候选还因“每一节 -> 各节”触发既有 `NUMBER_OR_UNIT_CHANGED`，最终为 FAIL/1。
因此 GENERAL 本轮的价值是暴露并拦截 fresh 漂移，不是提供通过对照稿。

### 21.6 v34 最终验证

v34 新增 13 项测试，完整基线从 701 增至 714：

| 分组 | 结果 |
|---|---|
| full suite | 714 tests, OK；3 个环境相关 skip |
| qualification audit | 41/41 |
| long finalizer | 131/131 |
| unified validator | 73/73 |
| invariant checker | 53/53 |
| Skill contract | 33/33 |
| projection builder | 37 PASS + 1 environment skip |
| Python compile / `--help` | 25/25 / 25/25 |
| Skill quick validation | PASS；主文件 443 行 |

最终 projection：

- [primary](build/generator-projection-maturity-v34-final-20260719/)
- [primary manifest](build/generator-projection-maturity-v34-final-manifest-20260719.json)
- [repro](build/generator-projection-maturity-v34-final-repro-20260719/)
- [repro manifest](build/generator-projection-maturity-v34-final-repro-manifest-20260719.json)

两边各 31 文件，逐路径字节差异 0，manifest 字节相同，私有资格/replay/second-pass 标识 0 命中。

```text
policy/builder=1.10.4/1.10.4
capability_source=f7b2c28e0297a1ff669ffbc7a053ed1fce326c6c6aa612641f2ee9fadfe38502
projection_tree=670e58a62e56fbfbee0901e809fa388ac3beecee8e6698a850f4a79a0f092c12
manifest_file_sha256=b93536853f7229c5facc77d9773418266ee0930ad309c2687ffeb2f4157c6a3c
evidence_cap=E2
```

资格审计继续返回：

```text
evidence_integrity_status=PASS
qualification_status=NOT_EVALUATED
0 PASS / 0 FAIL / 188 NOT_EVALUATED
exit_code=2
```

### 21.7 v34 实用性裁决

v34 不是给词库再加几个“AI 味词”，而是把五种普通用户真正会遇到的错误完成路径变成具体抓手：

1. 看见源文冲突后由纯文风层自行选边；
2. 没有台账却报告 DRAFT 分类数字；
3. 用重叠 patch 同时声称改写与原样保留；
4. 根据 supplied 数字自行增加比较和机制强度；
5. 把“缺内容”顺写成“缺衔接”。

这些改进使 COURSE/DRAFT fresh 行为明显收敛，也让 GENERAL 的新漂移不再静默通过。边界仍在：三个
新 detector 都是窄表面门，不是通用语义理解；短 PATCH 分区尚无独立 parser；paired-quality、学术
正确性、作者身份、来源真实性和 188 原子资格都没有本地 PASS。准确结论是：生产级待审工具链更难
越权和虚假闭环，不是自动终稿器。

## 22. v35：短 PATCH 从自然语言约定升级为可执行工件链

### 22.1 本轮为什么不是“再补几条规则”

v34 已经要求 hunk 不重叠，但普通用户仍只能看模型写出的自然语言列表，无法机器证明 source、动作、
replacement 和 candidate 是否一致。v35 新增三个普通生成入口：

```text
build_humanize_short_patch.py
apply_humanize_short_patch.py
verify_humanize_short_patch.py
```

完整合同见 [short-patch-workflow.md](C:/Users/Lenovo/.codex/skills/humanize-academic-chinese/references/short-patch-workflow.md)，根因与证据见
[v35 root review](build/maturity-v35-forward-20260719/root-review.md)。

### 22.2 两阶段 bundle 与确定性 candidate

selection spec 只写精确 source text、动作、replacement、理由和 protected terms。builder 冻结 UTF-8
字节 offset、source/selection/hunk hash、非重叠分区和 canonical bundle hash。重复文本必须给具体
byte offset；错误会列出候选起点，不再让用户自行猜。

applicator 不接受另交 candidate，而是按 bundle 重建。未列入 hunk 的 source bytes 全部
`COPY_EXACT`。`DELETE_STYLE_SHELL` 必须空 replacement，`REWRITE` 必须非空且变化，`UNRESOLVED`
必须逐字等于 source。

### 22.3 validator 不再读取 live source

首版实现曾有 TOCTOU：candidate 由初始 bytes 生成，但 validator 读取 live source path；并发替换可能
让公式改动看似无差异。v35 最终版把初始 source 保存为 staging snapshot，validator 只读 snapshot 与
candidate，并强制核对 before/after SHA、OS exit、delivery/mechanical/hard 状态元组。hard FAIL、hash
不一致或状态矛盾均零发布。

### 22.4 七项闭集与准确状态

review 目录固定为七项：source snapshot、`candidate.review.*`、diff、bundle、validation、result 和
manifest。verifier 会重放 bundle、重算 diff、核对全部 hash/size 和闭集文件名。首行故意并列：

```text
INTEGRITY PASS exit=0 scope=SELF_CONSISTENCY_ONLY; DELIVERY REVIEW
```

前者只表示本地工件自洽，后者才是候选交付状态。没有外部签名/时间戳，不能把 verifier PASS 当成
文风质量、历史真实性或学术正确性 PASS。

### 22.5 编码、路径和入口硬化

新增拒绝：CRLF 中间切分、明显 grapheme 连接点切分、新增 bidi/control、hardlink、symlink/reparse
路径链、duplicate key、float、NaN、未知字段、existing output 和运行中 source/bundle 漂移。
`output_exists` 不再回显用户绝对目录。

长文 scaffold 同步改为 strict JSON，并在全部输入校验后才创建输出。长文
`rewrite_intent.source_spans` 同步要求有序、非重叠、范围不重复；operation 仍可共享引用一个合法 span。

### 22.6 真实 MD/TeX 支撑的五类谓词门

从实际 GPT 报告和 TeX 负例中加入：

| code | 拦截转换 |
|---|---|
| `SPEECH_ACT_ABSENCE_TO_FAILURE` | 未生成 -> 验证失败 |
| `SPEECH_ACT_PURPOSE_TO_RESULT` | 用于比较/校准 -> 结果表明 |
| `SPEECH_ACT_PENDING_CHECK_TO_COMPLETION` | 待实测/待复核 -> 已生效/已证明 |
| `SPEECH_ACT_INTERNAL_TO_EXTERNAL_VALIDATION` | 内部指标/投影 -> 外部事实验证 |
| `SPEECH_ACT_CANDIDATE_TO_CONFIRMED` | 候选区间/不稳健排序 -> 经验证阈值/稳定结论 |

黑盒第一轮为 4/5；“配置已经写入，热生效仍待实测”因正则跨逗号漏检。按原样 case 修复后，五个
越权样例全部命中专门 code，五个保留边界的安全对照目标误报为 0。规则仍固定
`semantic_judgment=NOT_EVALUATED`，不能外推为完整语义理解。

### 22.7 COURSE 和普通用户实测

真实 COURSE 冲突材料成功形成四个 non-overlapping hunk：两处安全删除、两处原样 UNRESOLVED。
标题、公式和正反主张均保留。实际状态：

```text
build=BUNDLED/0
apply=REVIEW/2
hard=PASS
mechanical=REVIEW
verify=PASS/0 SELF_CONSISTENCY_ONLY
```

普通用户 subagent 独立走通 CLI；重复 build/apply 均拒绝覆盖，失败后旧闭集仍可 verify。该实测还推动
了 byte offset 提示、绝对路径隐私和 verifier 首行状态三项文案修复。

### 22.8 最终验证

```text
full suite: 744 tests, OK (skipped=4)
qualification tests: 41
long finalizer: 132
unified validator: 74
invariant checker: 57
Skill contract: 33
projection builder: 39
short PATCH: 21
scaffold: 8
scripts: compile 28/28, --help 28/28
quick_validate: PASS
SKILL.md: 447 lines
```

最终双投影各 35 文件、逐字节一致、manifest 字节一致，私有 qualification/replay/second-pass 标识零
命中：

```text
policy/builder=1.10.5/1.10.5
capability_source=acef26151bf63578bb795f87d8761b9d27607e6601d2d9eb7a93a4550c19aeb6
projection_tree=2d92fe161777cabb68c4e0af97679113cf6886375f5b576a6dd2d7b075e7480c
manifest_file_sha256=e8de67adea02a7adb524fbf05b822249501a10cdf38ac59cd50c797fe400728d
evidence_cap=E2
```

资格仍为 `0 PASS / 0 FAIL / 188 NOT_EVALUATED`。v35 可以称为可执行、可拒绝错误完成态的生产级
待审 PATCH 层；不能称为自动终稿、通用语义审稿或学术正确性工具。

## 23. v36：当前策略重放与 live source 三态

### 23.1 红队缺口

v35 verifier 只证明闭集自洽。重新散列一个被改过的 `validation.json` 后，旧实现仍可能返回
`PASS/0`；记录也没有说明当前 validator policy 是否已经变化，或原工作文件是否仍与快照一致。

本轮先建立四组 RED：缺 current-policy 字段、缺 live-source 入口、policy drift 无法分级、同 policy
核心 validation 被重封后没有失败。另由独立代理指出 argparse 的退出码 2 会与合法 `REVIEW/2`
混淆，随后补成第五个 RED。

### 23.2 修复后的状态合同

- 闭集/hash/bundle/diff/result 损坏：`FAIL/1`；
- recorded/current policy 不同：`REVIEW/2 + replay=NOT_RUN`；
- policy 相同：用归档 source/candidate/bundle 重跑当前 validator，并比较完整 JSON；
- 同 policy 下状态、finding、warning fingerprint 或 request SHA 任一不一致：`FAIL/1`；
- `--live-source` 未给：`NOT_PROVIDED`；匹配：`MATCH`；漂移/不可用：`REVIEW/2`；
- verifier `PASS/0` 与候选 `DELIVERY REVIEW/2` 用独立字段和退出码表达；
- 参数错误固定结构化 `FAIL/1`，不再使用 argparse `2`。

### 23.3 fresh 黑盒复测

代理用新版 verifier 检查旧 v35 证据，得到 `record_integrity=PASS`、`policy=DRIFT`、
`replay=NOT_RUN`、`DELIVERY REVIEW`、进程退出码 2。提供完全匹配的 live source 后只新增
`live_source=MATCH`，没有错误清除 policy drift。

### 23.4 验证与保留缺口

```text
full suite: 747 tests, OK (skipped=4)
policy/builder=1.10.6/1.10.6
capability_source=037dc2567803cbf738b87d9cfa6699817626035faf9b1e456cb4dcf08f87c785
projection_tree=cf43ee41113ca4515389379f6ca4ace61d5482ca7a855b8facacdfab5d2e94ca
manifest_file_sha256=2a6da6aafef7f047eb83a75388eb7bd95830ca74f574f4a35224055d74275423
projection files=35/35; BYTE_DIFFS=0; evidence_cap=E2
```

coverage 仍未完成：当前工具不证明 selection 列全了 high finding、用户 selection 或冲突两侧。该项已
登记为下一 P0，不能用 current-policy replay PASS 代替。

## 24. v37：coverage universe、声明窄化与真实回退

### 24.1 这次修的不是“再多扫几个词”

v36 能证明一个短 PATCH 证据包在当前 validator policy 下可重放，却不能证明调用方列全了需要处置的
位置。只给一个安全 hunk、遗漏同文其他 high，仍可能得到“所列 hunk 自洽”。v37 新增独立
`humanize-short-patch-coverage/v2`，把 universe 固定为三部分：AUTO audit view 的全部 scanner high、
调用方精确 selection、调用方显式 conflict pair。

该 universe 故意没有扩写成“全文全部 AI 味/全部语义冲突”。顶层只允许：

```text
coverage_claim_scope=ENUMERATED_HIGH_AND_BOUND_DECLARATIONS_ONLY
coverage_completion_claim_allowed=true
semantic_completeness_claim_allowed=false
humanize_quality_claim_allowed=false
academic_correctness=NOT_EVALUATED
```

### 24.2 两轮红队不是只测 happy path

coverage 红队和 state/verifier 红队共确认九条独立错误路径：KEEP span 可被 hunk 改写、
PROTECTED/EXCLUDED finding 可被大块覆盖、policy key-set drift 被误报 corruption、跨保护区 finding 只看
起点、task scene 漏扫、result 注入伪 PASS/绝对路径/重复 artifact、畸形 nested record 被 drift 遮蔽、
builder stdout 错报 v1，以及 `.ltx` scanner/validator 格式分裂。

修复后，coverage scanner 固定 AUTO；保护角色要求完整 finding span 位于保护区；KEEP、PROTECTED 和
EXCLUDED 均不得与 hunk 相交；同 policy 重算不一致为 FAIL，policy 值或 key-set 漂移为 REVIEW；result
改为严格字段闭集；`.ltx` 固定发布 `candidate.review.tex`。旧 coverage v1 只读兼容，不会冒充当前
policy PASS。

### 24.3 conflict pair 能证明与不能证明的内容

每个 pair 必须引用两个不同、未复用的 UNRESOLVED hunk，replacement 必须逐字等于 source。这个门能
阻止“只保留冲突一侧”“同一个 hunk 冒充两侧”和“标未决却暗改正文”。它不能证明调用方挑出的两句
真的语义相反，也不能自动发现未声明冲突。因此 limitations 明写
`CONFLICT_INVENTORY_IS_CALLER_DECLARED_ONLY`。

同理，selection 可精确绑定 source bytes，但没有外部 request anchor 时不能证明这些 span 就是用户原始
选择。REPORT_SELECTION 继续强制走 extractor/report-scope，不能借 v2 coverage 自填来源标签。

### 24.4 fresh 代理确实发生了回退

全新代理被禁止读取旧 v37 selection 和报告。第一轮把“必须牢记公式”整句删除，high 虽归零，但验证器
以 `SPEECH_ACT_MODALITY_SCOPE_CHANGED` 保持 REVIEW。代理没有写空泛 KEEP reason，也没有申请豁免；
第二轮把空重点和教练命令合并为“遇到这类题目时，必须判断公式能否直接套用”，保留必须性和输入已有
对象，机械层转为 PASS。

两个关于能否直接套用公式的相对主张仍逐字 UNRESOLVED。最终全链为：

```text
build=BUNDLED/0
coverage v2=PASS (AUTO high 4, selections 5, conflicts 1)
apply=DELIVERY REVIEW/2
mechanical/hard/style/speech-act=PASS
paired_quality=PENDING_EXTERNAL_REVIEW
verify=PASS/0
coverage replay/current-policy replay=PASS/PASS
live source=MATCH
candidate AUTO rescan=0 findings
```

这里最重要的不是“0 findings”，而是 0 findings 没有覆盖两个未决冲突和外部成对质量门。完整使用记录见
[v37 final forward](build/maturity-v37-final-forward-20260719/review-report.md)，红队根审见
[v37 root review](build/maturity-v37-forward-20260719/root-review.md)。

### 24.5 最终验证

```text
focused: 112 tests, OK (skipped=2)
full suite: 768 tests, OK (skipped=4)
quick_validate: source + two projections PASS
policy/builder=1.10.8/1.10.8
projection files=36/36; BYTE_DIFFS=0
capability_source=08c6f3ced51426bbcbd1eaf6e48d5f525336a5247c6047114896327ae793a57e
projection_tree=00eea41ec71ed8b8525d843eb5ff69343b5db8aa4c6bf84f87b7c2220abfdb6b
manifest_file_sha256=366c3444ac58cf6fb41501d372cdc752ffec8bbe8457d2b96eaf77393821a76d
private control hits=0/36
evidence_cap=E2
```

### 24.6 实用性裁决

v37 已关闭 v36 登记的 coverage P0，且 fresh 任务证明工具会在“high 已删除但模态漂移”时迫使调用方
回退。它仍有明显作者体验成本：selection 与 hunk 独立绑定带来重复录入，普通 diff 不显示未变化的
UNRESOLVED，终端包装层也可能混淆预期 REVIEW/2。下一轮应优化输入生成器和审阅视图，但不能牺牲
独立绑定、窄作用域或三态退出码来换取表面易用。

## 25. v38：一次登记 source span，并把未变化的未决项放回审阅面

### 25.1 实际修复的录入成本

v37 的 hunk 与 selected span 需要分别抄写相同 `source_text/start_byte`。这不是普通冗余：长中文句、
重复短语和 UTF-8 byte offset 很容易在两份结构中发生漂移。v38 新增两阶段 authoring scaffold，先冻结
source、AUTO high inventory 与 scanner/lexicon/runtime policy，再让 hunk、selection 和 lexical
resolution 独立引用同一 span registry。`finalize` 拒绝 PENDING、source/policy 漂移、重复 exact span、
悬空引用和错误 selection/hunk 绑定，成功后确定性展开为原有 v2 selection，并由正式 builder 再验一次。

scaffold 只降低录入错误，不证明用户授权、reason 真实、语义完整或改后更自然。

### 25.2 `review.md` 解决了 diff 的盲区

PATCH diff 天然只显示变化，逐字保留的 `UNRESOLVED` 不会出现。v38 把 result 升为 v2、verification
升为 v3，并把确定性 `review.md` 纳入 evidence 闭集。review 同时展示 changed hunk、unchanged
UNRESOLVED、显式 conflict pair、coverage 窄 scope 和 mechanical/quality/academic 边界。所有文本做
HTML escape；verifier 重算精确字节，因此单独篡改 review，甚至同步重封 manifest，仍为 `FAIL/1`。

### 25.3 fresh 结果没有被新界面粉饰

fresh 代理在课程 TeX 上登记 9 个 span、5 个 hunk、5 个 selection 和 1 个 conflict pair。review 清楚显示
H003/H005 两处未决主张及 C001 左右绑定。候选删除“必须”后仍触发
`SPEECH_ACT_MODALITY_SCOPE_CHANGED`，最终为：

```text
build=BUNDLED/0
apply=DELIVERY REVIEW/2
hard/style=PASS/PASS
speech-act/mechanical=REVIEW/REVIEW
paired-quality=BLOCKED_BY_MECHANICAL_GATE
verify=PASS/0 SELF_CONSISTENCY_ONLY
coverage/current-policy replay=PASS/PASS
live source=MATCH
```

这说明 review 可读性提升没有清除或隐藏既有门。完整工件见
[v38 fresh user](build/maturity-v38-fresh-user-20260719/review-report.md)，根审见
[v38 root review](build/maturity-v38-forward-20260719/root-review.md)。

### 25.4 最终验证与诚实缺口

```text
authoring tests: 11 total; 11 passed
full suite: 781 total; 777 passed, 4 skipped
authoring scaffold line coverage: 87%
quick_validate: source + two projections PASS
policy/builder=1.10.9/1.10.9
projection files=37/37; BYTE_DIFFS=0
capability_source=60e326974d022c1c9d659780769277aec985d29f3a378d55b0540f9d9f358645
projection_tree=802b971d25252caccbd19a30bce644b3c883329ef3e44a5113c80652a555b6e3
manifest_file_sha256=8eb5d81e5f5f676bad48109a158b5c69c1fa41ae227acba18ad4d972e0be8ba5
evidence_cap=E2
```

两个异常输入子代理被平台分类器拦截，没有形成可采信裁决，不能计作红队通过。现存 authoring attack
目录是失败快照，review attack 目录只有 PENDING scaffold，也都不能改称通过证据。当前主要成本转为：
fresh 任务仍需手工新增 5 个更宽 hunk span。下一轮可自动建议句级/段级 span，但不能自动决定
replacement、KEEP 理由、selection、conflict 或用户授权。

## 26. v39：从 clause 建议到可回攻的 clause + sentence 默认面

### 26.1 这轮真正降低了什么成本

v38 只把 span 从 hunk/selection 的重复文本提升为 registry 单次登记，fresh 仍需手工增加更宽句界。v39
把默认 authoring 模式改为 `CLAUSE_AND_SENTENCE`：clause 用于删除局部提示壳和尾语，完整句用于保留
谓词、模态和作者动作后的整句改写；段级建议仍须显式请求。建议只给 source-bound UTF-8 byte span，
不自动生成 replacement、reason、selection、conflict 或授权。

最终 fresh 科研短文的统计直接说明了实用性变化：3 个 AUTO high 产生 8 个 AVAILABLE 建议；最终 2 个
hunk 全部引用建议 span，手工 hunk span 为 0。上一版同一材料需要 2 个手工 span，其中一个正是完整句。
这不是“少写几行 JSON”的主观印象，而是 authoring 文件中 suggestion span ID 与 hunk span ID 的可重放
交集统计。

### 26.2 红队没有让建议器停在 happy path

初始默认值两项 RED 转绿后，独立复核继续找到并复现：

- high 跨 `，；：,;:` 时，建议只按 finding 起点切界，导致 suggestion 挂接自己没有完整包含的 finding；
- `\textbf{...}`、可选参数和嵌套参数内 clause 未被 TeX 保护；
- 相同 byte range 同时以 clause/sentence 计数；
- 同一 finding 的 clause 与 full sentence 可同时进入 selected KEEP；
- Python API 的 `AUTO` 与 CLI 不一致；
- `\command% comment` 后下一行参数仍属于 TeX 命令，但旧 parser 会断开保护。

最终实现要求每条 AVAILABLE 完整覆盖全部 finding；跨边界视图以
`FINDING_NOT_FULLY_COVERED` 留在 SUPPRESSED 审计面；相同可用 range 只保留最局部视图；selected spans
两两不重叠；Markdown/TeX 中的命令调用连同嵌套参数整体保护；TeX 模式按注释吞换行语义续接参数；
create/finalize/build API 均接受大小写不敏感的 AUTO。

红队对原五项复攻均为 FIXED；TeX 注释续接是复攻时新增的第二层反例，随后又经过 RED/GREEN。完整最小
输入、原因和代码边界见 [v39 root review](build/maturity-v39-forward-20260719/root-review.md)。

### 26.3 Fresh 回退说明建议没有越过语义门

最终 fresh 代理首轮把含“可能原因”的完整句整句删除。即使 scanner high 已被处理，统一验证器仍以
`SPEECH_ACT_MODALITY_SCOPE_CHANGED` 保持机械 REVIEW。代理在 r2 改为：

```text
本文梳理了相关现象，并讨论了可能原因。
```

这次保留了“可能”模态，机械、hard、speech-act、style 和 coverage 才全部 PASS。verifier 为
`PASS/0 SELF_CONSISTENCY_ONLY`，但 candidate 始终是 `DELIVERY REVIEW/2`，paired-quality 仍待外部复核。
这说明句级 suggestion 只减少边界录入，不替代言语行为判断或质量授权。

有效 fresh 证据只使用
[r10 operation report](build/maturity-v39-r10-fresh-user-20260719/operation-report.md)。r5 是最终修复前的中间
记录；r9 遇到外部 HTTP 400，没有被补写为通过。

### 26.4 最终机器基线

```text
focused authoring/suggestion=38/38
full suite=812 total; 808 passed, 4 skipped
scaffold trace=904 executed / 1008 executable lines = 89.68%
quick_validate source/final/repro=PASS/PASS/PASS
SKILL.md=451 lines
policy/builder=1.10.10/1.10.10
projection files=37/37; BYTE_DIFFS=0
capability_source=c1b7af4cb214107a7241b7a7aed157de24868d432f23a6a9dff3a79a39e33f7a
projection_tree=14cc3e25d3bf2c4a7290961b07792f0e674afb2084173b4f19f2944f4e4cce4a
manifest_file_sha256=e38cbc680d61ed226123490a09d5070151ffcd5bc1d70c9702f792b784e619f3
private-control path/content hits=0/0 per projection
evidence_cap=E2; generation qualification=NOT_EVALUATED
```

一次较早的 full run 在能力文件变化、固定 capability policy 尚未同步时产生 64 个同源 fail-closed error；
该运行没有被隐藏，也不计最终通过。最终基线绑定同步后的固定 policy 和 r10 双投影。

### 26.5 实用性裁决

v39 已把“句级 span 仍靠手工量 offset”这一明确成本闭合，并让建议器经受了跨边界、TeX 参数、TeX 注释、
重复视图、重叠 selection 和 API/CLI 分裂六类回攻。它仍是候选生成与机械审计工具，不是无人值守终稿
发布器。下一步应跨 COURSE/MODELING/RESEARCH/GENERAL 建立 suggestion 使用率、手工 span 回退率、
SUPPRESSED 原因和外部 paired-quality 结果的真实基准；不能用本轮 0 手工 span 推断所有文本都能自动选界。

## 27. v40：跨场景盲测、候选洪水否决与 FOCUS 精确登记

### 27.1 三场景没有复用 v39 的 happy path

v40 让三个 fresh 代理分别处理 COURSE、MODELING、GENERAL 原始材料。它们只读取当前 Skill、自己的
fixture 与本轮 run 工件，不读取测试、旧报告或其他代理候选。三个 fixture 都来自 GPT 生成或来源未解决
材料，只作压力输入。精确来源见
[source manifest](build/maturity-v40-cross-scene-20260719/fixtures/source-manifest.md)，本轮继续不读取
`CET6.tex`。

原始 fresh 结果为：

| 场景 | candidate high | 其他候选 | 自动 AVAILABLE | 最终 hunk | 手工 span | 最终机械层 |
|---|---:|---:|---:|---:|---:|---|
| COURSE | 0 | 0 | 0 | 17 | 17 | PASS |
| MODELING | 0 | 1 medium | 0 | 9 | 9 | PASS，另有 1 UNRESOLVED |
| GENERAL | 0，另有 1 protected high | 5 low | 0 | 10 | 10 | PASS |

三组共 36 个 hunk，全部由 fresh 使用者连续阅读后手工登记范围。GENERAL 的 protected high 是引用区中的
“收口”，没有进入 hunk；MODELING 的未决句涉及源文未展示的表格，代理没有把编辑计划擅自改成已完成
事实。三组最终 verifier、coverage/current-policy replay 与 live source 均通过，但候选都保持
`DELIVERY REVIEW/2`，没有可信外部 paired-quality clearance。

### 27.2 失败链比最终 PASS 更能说明工具作用

COURSE 首轮删除“非常直观”时，否定门把“非常”中的“非”误计为否定；同轮还出现模态变化。MODELING
先删去真实“不”，回退时又新增“只”，两次被言语行为门拦截。GENERAL 把加粗结论换成新的加粗句，
触发新增 low bold 信号；去掉加粗后又因句间空格被成对朗读回退。三组都重新建立 scaffold/bundle/闭集，
没有覆盖旧失败工件。

“非常”根因最后被窄修复：只在单字 marker“非”的显式排除表中加入“非常”，不关闭“并非/非/不/未/无”
等真实否定检查。对应 v40 回归测试与既有否定变化测试同时通过。

### 27.3 非 high advisory 有用，但覆盖不了连续阅读

默认建议器现在也为 medium/low scanner candidate 提供 advisory 边界，且固定 `finding_ids=[]`，不进入
high coverage。postfix 探针中，MODELING 得到 3 个 advisory AVAILABLE，其中 1 个与最终 hunk 精确同界；
GENERAL 的 12 个 low 视图因保护重叠或 finding 未完整覆盖而全部 SUPPRESSED；COURSE 为 0。也就是说，
advisory 只覆盖 1/36 个真实最终 hunk，不能把 `candidate high=0` 自动解释成 `NO_CHANGE`。

### 27.4 全量可编辑候选为何被删除

临时 `EDITABLE_RUNS` 原型试图把所有可编辑中文 run 都发成建议。冻结输入上的结果是：

| 场景 | 候选数 | 与最终 hunk 精确同界 |
|---|---:|---:|
| COURSE | 132 | 2/17 |
| MODELING | 259 | 1/9 |
| GENERAL | 163 | 1/10 |
| 合计 | 554 | 4/36 |

候选对 hunk 的精确覆盖仅 11.11%，候选自身精确命中率仅 0.72%。它把“可编辑”暗示成“应编辑”，并把
人工诊断成本从量 offset 变成筛数百个无诊断边界。该模式已从生产代码删除，只保留 postfix JSON 作为
否决证据。

### 27.5 FOCUS 解决的是登记，不是假装发现

最终 authoring v3 增加 strict `humanize-short-patch-focus/v1`：

```json
{"schema_version":"humanize-short-patch-focus/v1","spans":[{"focus_id":"F001","source_text":"为了看清 ","start_byte":null}]}
```

唯一片段允许 `start_byte=null`；重复文本必须给 UTF-8 byte offset。FOCUS 只把调用方已经诊断的位置注册成
source-bound span，重算 source/hash 并执行保护重叠检查。它不生成 replacement、reason、decision、
selection、conflict 或授权；与公式、引语、代码、TeX 命令等重叠时只发 SUPPRESSED。

三场景回放为 COURSE 17/17、MODELING 9/9、GENERAL 10/10，共 36/36 精确同界，越权动作字段为 0。
这不是病灶发现召回率，因为输入本来就是已诊断 span；它证明 36 次手工 offset/registry 录入可以降低为
原文片段加必要的消歧 offset。v1/v2 authoring 保持只读兼容，新 create 固定输出 v3。

### 27.6 最终机器基线与实用性裁决

```text
focused short-patch/invariant/validator=223 passed, 1 skipped
full suite=819 total; 815 passed, 4 skipped
scaffold trace=1094/1218 = 89.82%
quick_validate source/final/repro=PASS/PASS/PASS
SKILL.md=451 lines
policy/builder=1.11.0/1.11.0
projection files=37/37; BYTE_DIFFS=0
capability_source=12a12fa725588f8da2a258b2280331fab7c47b1e63f183205c151f47c62b4799
projection_tree=750332eb2295923080a0361c86906b04e63a12a558c266ce6c949066519eb100
manifest_file_sha256=081b133c9212b9f7e16721b74caaddfd0bf99dd196d32fb0a179faa99fadf130
private-control path/content hits=0/0 per projection
evidence_cap=E2; generation qualification=NOT_EVALUATED
```

第一次全量运行在新 capability hash 尚未写入固定 policy 时产生 66 个同源 error 和 4 个派生 failure；
同步批准 hash 后才得到最终 819 项通过。该 fail-closed 过程保留在总复盘中，不被最终绿色基线覆盖。

完整数据、失败链、探针和边界见
[v40 root review](build/maturity-v40-cross-scene-20260719/root-review.md)。v40 的实际进步是：三场景真实
使用暴露的 36 个登记成本已有精确路径，同时拒绝了一个表面“更自动”、实际候选洪水严重的方案。它没有
把 FOCUS 说成自动诊断器，也没有把 verifier PASS 说成文风质量 PASS。

## 28. v41-v42：盲读推翻旧 PASS、局部 amend 与 v3 可重放血缘

### 28.1 三场 fresh 把语义回归和使用成本同时暴露出来

v41 用 COURSE、MODELING、GENERAL 三份新 fixture 运行 short-PATCH。三份输入都来自 GPT 生成或来源未解决
材料，只作负向压力输入；未读取 `CET6.tex`。

| 场景 | hunk | 主要失败链 | 盲读结果 |
|---|---:|---|---|
| COURSE | 3 | inventory hash、condition warning | 3 BETTER |
| MODELING | 8，含 1 UNRESOLVED | offset、direct quotation、speech/high | 2 BETTER、1 SAME、1 WORSE |
| GENERAL→MODELING | 3 | 晚路由、first-person、时域 | 1 BETTER、1 SAME、1 WORSE |

原始 MODELING 把“正文应保留两类扫描结果”的编辑要求改成“结果共同支持结论”；GENERAL 把集体工程计划
改成“我先做三件事”。v41 因此加入 additive FOCUS、`SPEECH_ACT_EDITORIAL_TO_EVIDENCE` 和
`SPEECH_ACT_FIRST_PERSON_REFERENCE_INTRODUCED`。实际 additive probe 为 11 suggestions：7 AVAILABLE、
4 SUPPRESSED，其中 FOCUS 1/1 AVAILABLE。两条门准确命中两个高严重度案例，但没有覆盖全部语义红队发现。

完整冻结复盘见 [v41 root review](build/maturity-v41-fresh-focus-20260719/root-review.md)。

### 28.2 postfix final 为什么不能停在 v41.1 PASS

`modeling-r3` 保留三层失败链：首轮 2 个 high 未解释；第二轮 negation/modality/condition warning；第三轮在
v41.1 snapshot 下 mechanical/hard/speech/style/coverage PASS，但 delivery 仍 REVIEW/2。

新的独立盲读把 5 个变化判为 3 BETTER、1 SAME、1 WORSE。WORSE 是只删“正文里”：位置约束丢失，
其余编辑祈使仍在。v42 增加 `SPEECH_ACT_EDITORIAL_SCOPE_DROPPED`，只在近乎逐字保留编辑动作而删除
`正文里/正文中/文中` 时触发。无 scope、描述句和 scope 迁移不被该窄门误拦。

旧 postfix evidence 在 current policy 下现在正确显示 `record_integrity=PASS + POLICY_DRIFT/REVIEW`，不再把
规则变化误报成历史工件损坏。

### 28.3 P0 修复：warning 后不再重建整条 authoring 链

v41 的必要语义劳动不能自动化，但 source hash、offset、ID、未变 hunk、selection、coverage declarations
和新闭集可以确定性复用。v42 新增：

```powershell
python scripts/amend_humanize_short_patch.py create <review> --hunk H003 --output amend.json
python scripts/amend_humanize_short_patch.py apply <review> --amendment amend.json --output <new-review>
```

父节点必须是 verifier/current-policy/coverage replay 均 PASS 的 closed review，而不是 caller-editable
authoring。create 只开放指定 hunk 的 `decision/replacement/reason`；scene、intensity、保护词、span、
offset、selection、KEEP、conflict 和 hunk 拓扑全部冻结。

### 28.4 v3 lineage 阻止局部接口偷换范围

`humanize-short-patch/v3` 完整嵌入 parent bundle，并绑定父 manifest/candidate、amendment spec 和 changed
hunk 前后 hash。父子必须保持 source/config/document format、coverage declarations、hunk 数量/顺序/ID/
start/end/source text/source hash 和所有未声明 hunk 字段。实际 changed set 必须与声明相等。

最大 depth=8；超过深度或体积要求新开普通 authoring run。verifier 对整条 parent chain 重放 coverage
policy，不能只重封顶层 bundle 掩盖父层 drift。血缘作用域固定 `SELF_CONSISTENCY_ONLY`。

### 28.5 攻击测试与真实链式修订

新增 12 项 amend test，覆盖成功、顺序、no-op、before/base/parent 篡改、非法 topology/config、policy/live
drift、中途 policy 变化、原子回滚、CLI 三态、v3→v3 depth、重封后的未声明 hunk 变化和第 9 层拒绝。

真实回放先用 current policy 生成 base review。第一轮 v2→v3 amend H003/H005：

```text
depth=1
candidate=357528668d91fb5d4e42fd509c6437012db170d5e005dac19b9e9498d57539b5
lineage/current-policy/coverage replay=PASS
mechanical=REVIEW
warnings=NEGATION_CHANGED, MODALITY_SCOPE_CHANGED
```

该失败被保留，工具成功没有被写成候选成功。第二轮从 v3 parent 只 amend H003：

```text
depth=2; changed_hunks=H003
candidate=54281967ba4049dfddf7e25d7496ff71c45a08b3698b5a220a7ff028808a2b00
mechanical/hard/speech/style=PASS/PASS/PASS/PASS
warnings=0; unexplained_high=0
record/lineage/current-policy/coverage/live-source=PASS/PASS/PASS/PASS/MATCH
delivery=REVIEW/2; paired-quality=PENDING_EXTERNAL_REVIEW
```

新的 fresh paired review 对 5 个变化给出 `BETTER 5 / SAME 0 / WORSE 0`，总体为
`BETTER_WITH_RESIDUALS`。它仍指出 L6/L8/L13/L15/L17/L19 的写作指令、自动展望和验收式收尾，故文档级
裁决是 `NEEDS_FURTHER_REVISION`，不是质量完成。

完整工件见 [v42 root review](build/maturity-v42-amend-real-20260719/root-review.md)。

### 28.6 新 checkpoint 与剩余缺口

```text
amend tests=12/12
focused=209 total; 207 passed; 2 skipped
full=838 total; 834 passed; 4 skipped
SKILL.md=453 lines; 324 non-empty
policy/builder=1.13.0/1.13.0
approved capability=29e8a24f73fbd2a7348d8330e78e4538ef4269dd28bd550e08753349605cccb0
projection files=38/38; BYTE_DIFFS=0
projection tree=0eb86180c4a3deb7cbe9d17f930488c38808df8a67038360b6afea3b892eca9e
manifest SHA=c2844657bc92baf68d7bae97c856b4d6c8b7b0bdbac45bd7eb8970aadf2b728e
quick_validate source/final/repro=PASS/PASS/PASS
evidence_cap=E2; generation qualification=NOT_EVALUATED
```

本轮把一个盲读发现的 scope 回归接入窄门，并把局部修订升级成有父子血缘、可原子回滚、可逐层 replay
的生产路径。仍未完成 AUTO route freeze、registry repair、`reason_ref`、可信外部 paired-quality、学术
正确性和生成资格。

## 29. v43：AUTO scene 在 authoring 前冻结，低分平局不再伪装 GENERAL

### 29.1 为什么 v42 以后仍有真实重复劳动

v41 的 GENERAL fixture 不是因为模型“后来改变主意”才从 GENERAL 变成 MODELING。升级前两个确定性入口本身没有连起来：

```text
route_humanize_scene.py -> MODELING=8, margin=8, resolved=MODELING
scaffold_humanize_short_patch.py create --scene AUTO
  -> configuration.scene=AUTO
  -> no scene_route record
  -> NO_HIGH_FINDINGS/0
```

所以调用方可以先完成 GENERAL scaffold/finalize/build/apply，最后才发现 route 已明确是 MODELING。旧链实际经历 GENERAL 初次、GENERAL warning retry、MODELING rebuild；同一 source-bound 3 个 span 被重复装配。

### 29.2 authoring v4 把 route 变成 create 的前置合同

新 authoring：

```text
humanize-short-patch-selection-authoring/v4
humanize-short-patch-scene-route/v1
```

v4 不再让 `scene=AUTO` 流入 selection。它在 span、hunk、selection authoring 前冻结：

- `requested_scene/resolved_scene`；
- route status/reason；
- 三场景 scores、top score、margin、ambiguous scenes；
- 只含 rule ID/计数/贡献、不含 source prose 的 evidence；
- source SHA/size、document format；
- 保护内容屏蔽后的 full-source routing view SHA；
- route policy schema/revision/SHA 与 router executable SHA；
- `authoring_allowed` 和 route record 自哈希。

显式场景固定 `EXPLICIT`，启发式不能覆盖。AUTO 路由唯一强证据时使用该场景；无证据或唯一弱证据可明确回退 GENERAL；平局或低 margin 返回 `ROUTE_REVIEW/2`，scaffold 固定不可 finalize。

### 29.3 finalize 不相信调用方重封

finalize 从当前 source、保护规则、router 和 policy 重新生成 route record，逐字段比较后才继续原有 span/hunk/coverage 门。测试把 MODELING score 改大、重算 route record hash，再重算 inventory hash；仍被 `SCENE_ROUTE_DRIFT` 拒绝。

这不把本地 scaffold 变成外部授权。`CALLER_CONTROLLED_SELF_CONSISTENCY_ONLY` 不变；它只是阻止“记录里写了什么就信什么”。

### 29.4 红队找到的低分平局绕过

旧 router 先判断 top score 是否低于强阈值，再判断平局。攻击文本：

```text
本题需要说明。本研究需要说明。
```

得到 `COURSE=2, RESEARCH=2, margin=0`，却被写成 `FALLBACK_GENERAL`；带 COURSE document prior 时甚至会静默变成 `ROUTED_DOCUMENT_PRIOR/COURSE`。

revision 3 调整裁决顺序：

1. top score 为 0 才直接 GENERAL；
2. 两个正分场景平局，或竞争场景 margin 不足，先判 AMBIGUOUS；
3. 之后才允许唯一弱证据回退 GENERAL；
4. document prior 只能补全唯一 top 且 second score 为 0 的弱证据。

短 PATCH 现在返回 `ROUTE_REVIEW/2`；长文 prepare 则把同类 unit 标成 `UNRESOLVED`，顶层 scene routing 为 REVIEW。

### 29.5 真实 GENERAL fixture 的单链回放

v4 对原 fixture 当场给出：

```text
requested=AUTO
resolved=MODELING
status=ROUTED
reason=AUTO_UNIQUE_SCORE_ABOVE_THRESHOLD
scores=COURSE 0 / MODELING 8 / RESEARCH 0
top=8; margin=8
policy revision=3
```

新 scaffold 的 3 个 focus span、registry 和 suggestion inventory 与旧 MODELING rebuild 逐字相同。复用旧最终 selection 的 3 个真实语义决策，只跑一次 finalize→build→apply，得到：

```text
selection.scene=MODELING
bundle=2f763ca9d54ef8ecb1579920566a2bb405214b3fbe10efede3de98775788d561
candidate=f7669aecd306bca8f1827eb579be565186557fcd2a87948e5a4a9f4384524c41
```

该 candidate 与 v41 最终 MODELING candidate 字节完全相同。也就是说，本轮删除的是错误的 GENERAL→MODELING 重建，不是偷偷替换文本决策。

当前 policy 仍对该候选报 `SPEECH_ACT_FIRST_PERSON_REFERENCE_INTRODUCED`；机械状态为 REVIEW，delivery 仍是 REVIEW/2。route 成功没有覆盖第一人称 stance 风险。闭集 verifier 为 `record/current-policy/coverage/live-source=PASS/PASS/PASS/MATCH`，作用域仍是 SELF_CONSISTENCY_ONLY。

完整证据见 [v43 root review](build/maturity-v43-scene-prefreeze-20260719/root-review.md)。

### 29.6 攻击矩阵

新增或强化的覆盖包括：

- AUTO 强证据在 create 内解析并冻结；
- 显式 GENERAL 不被强 MODELING 信号覆盖；
- 无证据/唯一弱证据回退 GENERAL；
- 强平局和低分 2:2 平局均 REVIEW；
- document prior 不得解决低分平局；
- 协调修改 route record + 自哈希 + inventory 仍因 replay 失败；
- router 返回值在 finalize 时变化被拒绝；
- 代码围栏里的 MODELING 词不驱动 route；
- route evidence 不输出 source prose；
- v1/v2/v3 authoring 继续只读兼容；
- v4 resolved scene 正确进入 selection/bundle/coverage；
- 真实 fixture 无晚路由重建且候选字节不变。

### 29.7 checkpoint

```text
focused=156 total; 155 passed; 1 skipped
projection tests=42 total; 41 passed; 1 skipped
full unittest=851 total; 847 passed; 4 skipped
SKILL.md=453 lines; 324 non-empty
policy/builder=1.14.0/1.14.0
scene routing policy revision=3
approved capability=8e17aafa6aa949c2a851f2b637afb828813f329c5d55432c31b2600223e0af2a
projection files=38/38; BYTE_DIFFS=0
projection tree=3bf19755676806c2393367c3c7cdc916b39b356f8f799433c1500cd5cd7784e2
manifest=3c6796ed71398f19e83e5fa9db8e9101b76a24a6f0edc67145d617b5a4ade3fe
quick_validate source/final/repro=PASS/PASS/PASS
evidence_cap=E2; generation qualification=NOT_EVALUATED
```

### 29.8 下一批真正缺口

本轮没有把“route prefreeze”扩大解释成全部 authoring 已成熟。红队仍确认：

1. 长文 chunk 已间接绑定 route，但 `scaffold_humanize_rewrites.py` 的 authoring 模板不显式披露 scene/score/margin，也没有在模板生成前重放 prepare integrity、live source 和 route；目前仍主要依赖 finalize 事后拒绝。
2. EXPLICIT 场景不会被覆盖，但共享 router 在显式分支不计算 observed scores，尚不能机械提示“用户声明与明显文档用途冲突”；正确方向是 REVIEW 诊断，不是启发式改写用户选择。
3. registry/offset/ID repair 和 hunk/selection `reason_ref` 尚未实现。
4. 外部 paired-quality、学术正确性、证据真实性、作者身份与生成资格仍不在本地证明范围。

因此当前准确结论是：短 PATCH 的 AUTO route 已从事后旁路升级为 authoring 前冻结、finalize 重放和歧义拒绝；整个 Skill 仍是待审候选工具链，不是终稿自动发布器。

## 30. v44：长文 authoring v5 与发布事务闭合

### 30.1 本轮处理的真实缺口

v43 已把短 PATCH 的 `scene=AUTO` 路由冻结到 authoring 前，但长文仍有一个不同层级的风险：调用方可以拿着看似完整的目录、模板和 sidecar 进入收尾，直到 finalize 才发现 prepare 完整性、源文件漂移或绑定字段不一致。v44 将长文链的“可生成模板”和“可被收尾消费”明确分开，并把最后一次发布改成同一文件句柄上的事务边界。

本轮新增或固定的公开合同为：

```text
humanize-rewrite-scaffold/v5
humanize-unit-rewrite-bundle/v3
humanize-long-authoring-binding/v1
```

v5 每个单元都回显冻结的 `unit_id`、`chunk_binding_sha256`、场景路由、Voice 绑定、snapshot、policy 和 source span。v3 的 `REWRITE` 必须提交 source span 与 target signal 的完整 intent 图；`NO_CHANGE` 必须有具体理由和 hash-bound evidence span。缺字段、旧 schema、路径化 unit ID、重复键、占位 `TODO`、未声明 diff 或绑定漂移均拒绝，不靠调用方重算 sidecar 放行。

### 30.2 发布事务的可验证边界

骨架器不再把“目录已经存在”当成发布完成。普通 staged member 先锁定；最终 marker 在第二次路径校验前保持不可写。提交时从同一个 Win32 handle 读取 marker、按 handle 报告的长度精确读取并计算 SHA-256，再验证 regular file、无 reparse、无 hardlink、路径与 handle identity 一致，最后相对 pinned parent handle 原子改名为 committed marker。读取短读、超读、EOF 后仍有数据、句柄失败、marker hash 不符或回滚失败都会 fail closed。

安全发布只承诺本地 NTFS。ReFS、FAT/exFAT、SMB/remote protocol 和不满足句柄语义的平台不会退化为“先按路径检查再 rename”；它们保持失败或待审。marker 缺失、残留 uncommitted marker、非法 schema、hardlink/symlink 和已发布后篡改均有回归覆盖。该机制只证明发布工件的完整性，不证明正文自然、事实正确或作者身份。

### 30.3 机器证据与确定性投影

评测合同更新后，oracle catalog 与 requirements binding 同步版本化，避免“合同变了但资格 oracle 还指向旧 hash”的假闭环：

```text
requirements contract = 2026-07-19.19
requirements sha256    = 86a69dde31f50d706be3c44a04c563146c7bd9870b5c38af0ae6dd5addcee640
oracle catalog         = 1.10.0
oracle contract bind   = 2026-07-19.19
oracle contract sha256 = 4eb32deb0e859420810e15e54fe544f9bf62dee1e8d7b19a146ab3427555359b
projection/builder     = 1.15.0 / 1.15.0
capability source      = 5a1379999b6efb727e06031c9235279818b8c4648c4e62c068faba07c201e44e
projection             = 38 files (34 INCLUDE + 4 TRANSFORM)
tree                   = 8dbce027e48eba712cf3a7a2a5b878b38c9609614926943c0167c0c73821873c
manifest               = 113fd0246ce77289b8bada37e101446dfda080b2553a7245584ce1903afaf5f3
```

两次独立构建的相对路径集合、文件长度和每个文件 SHA-256 完全一致：每份 38 个文件、总计 `1,507,978` 字节；两份 manifest 各 `23,177` 字节且逐字节相同。这个证据支持“投影可确定复现”，不支持“生成模型行为已合格”。投影仍把资格与验收控制面剥离，当前证据上限为 E2，generation qualification 仍为 `NOT_EVALUATED`。

### 30.4 真实长文前向，而不是只测内部函数

在 `tmp/forward-long-check-20260719/` 保留了两条真实 CLI 链：

| 路径 | prepare | scaffold | finalize | 权威解释 |
|---|---|---|---|---|
| `NO_CHANGE` | `READY/0`，1 个 PENDING | v5 `SCAFFOLDED/0` | `REVIEW/2`，`NO_CHANGE=1` | assembly PASS；质量待外部复核 |
| `REWRITE` | `READY/0`，1 个 PENDING | v5 `SCAFFOLDED/0` | `REVIEW/2`，`DONE=1` | assembly PASS；质量待外部复核 |

两条路径均得到 `rewrite_intent_coverage_status=PASS`、`protected_hashes_ok=PASS`、`style_validation=PASS`、`paired_quality_review_request_coverage_status=PASS`、`paired_quality_gate_status=PENDING_EXTERNAL_REVIEW` 和 `source_files_modified=0`，只发布 `rendered_review/`，没有生成正式 `rendered/`。这正是当前合同预期的 `REVIEW/2`，不是失败，也不是“全文 Humanize 已完成”。本夹具未指定项目编译命令，所以 `compile_check=NOT_RUN`，不能写成编译通过。

### 30.5 回归规模与剩余边界

```text
scaffold publication tests = 47 OK (skipped=2, 环境能力限制)
finalizer tests             = 144 OK (skipped=1)
joint publication tests     = 191 OK (skipped=3)
projection tests            = 43 OK (skipped=1)
full unittest               = 903 OK (skipped=7)
quick_validate              = PASS
compileall                  = PASS
git diff --check            = no whitespace error
SKILL.md                    = 461 lines / 332 non-empty / 56,144 bytes
```

这些数字证明的是当前机械合同和发布事务在已有测试面上自洽。它们不证明：

1. 真实作者对候选稿的 paired-quality clearance；
2. 学术正确性、事实、引文、证据真实性或结构语义；
3. 作者身份、检测器结果或任何“降 AI 检测率”；
4. 完整生成资格矩阵已经通过；
5. 非 NTFS 平台具有相同的发布保证；
6. 长文 v5 已经解决 scene/route 在调用方界面的可见性、registry/offset repair 和跨 unit 语义审阅。

因此 v44 的精确结论是：长文的 source-bound authoring、绑定重放、marker 发布和回滚边界已明显收紧，错误完成态会被拒绝；正常交付仍是可复核的 `REVIEW_CANDIDATE`，不是无人值守终稿。

## 31. 2026-07-20：编译子进程收容与中断安全补充

本节取代第 30 节中与 finalizer 测试数、projection hash 和编译子进程收容有关的现行数字；历史章节仍保留为迭代证据。

### 31.1 修复对象

本轮没有扩张文风质量声明，而是收紧长文 finalizer 的编译门。已经完成的 stale rewrite-intent 路径修复继续保留；新增修复集中在以下故障面：

1. Linux POSIX wrapper 在执行用户编译命令前启用 child subreaper，并安装 `SIGTERM/SIGINT` 处理；收到中断后先停止直接 shell，再收割被 wrapper 接管的脱离后代。
2. wrapper 由 `python -I -S -X utf8 -c ...` 启动，阻止 `sitecustomize`、用户 site 和 `PYTHONPATH` 在收容建立前执行启动代码。
3. 父进程优先向 wrapper 发送 graceful stop；等待、`terminate()`、`kill()` 或第二次 `KeyboardInterrupt` 再次异常时仍继续有界清理，不因保留原异常而跳过 supervisor 终止。
4. Linux `/proc` timeout fallback 在每轮和末次 descendant 扫描后都复核 wrapper 存活；wrapper 中途退出、扫描不可用或存活状态不可确认均返回 `FAIL`，不报告假清理完成。
5. Windows Job Object 创建、配置和分配失败时关闭 handle；`TerminateJobObject` 被中断时也在 `finally` 中执行 `CloseHandle`。若进程未能进入 Job，则使用有界直接 kill 重试并以存活状态决定 `PASS/FAIL`。
6. POSIX 能力标签固定为 `LINUX_SUBREAPER_PROCESS_GROUP`、`LINUX_SUBREAPER_UNAVAILABLE` 和 `POSIX_SUBREAPER_UNSUPPORTED`；启动/配置/分配阶段无法归类的平台异常记录通用 `UNAVAILABLE`；不再用旧 `POSIX_PROCESS_GROUP` 掩盖平台能力差异。
7. 专用 status FD 只接受恰好一条严格 `cleanup/command_exit` 记录，并核对 wrapper 实际退出码；多记录、额外字段、错码、超量和读超时均 fail closed。无编译命令时 `timeout_seconds=null`，非法 timeout 在 finalize 入口统一拒绝，setup/runtime 异常保留结构化 `compile_check=FAIL`。

这些改动只说明编译检查的进程树清理更可信，不说明候选正文自然、学术正确或已获外部质量许可。

### 31.2 执行型回归

新增测试实际触发并断言：第二次中断发生在 `terminate()` 或 `kill()`、Windows Job 终止异常后的 handle 关闭、未入 Job 进程的 kill 重试，以及 POSIX Popen argv 中存在 `-I -S`。现行结果为：

```text
finalizer tests       = 164 OK (skipped=2)
projection tests      = 43 OK (skipped=1)
full unittest         = 926 OK (skipped=8)
quick_validate        = PASS (PYTHONUTF8=1)
compileall            = PASS
git diff --check      = PASS; only existing LF/CRLF notices
```

本机为 Windows，且 WSL 2 未安装 Linux 发行版。真实 Linux subreaper + detached `setsid()` 集成测试按条件跳过，因此本报告只能写“Linux 路径具有源码合同、mock 回归和自动 skip”，不能写成“已在真实 Linux 通过”。此前 Windows CLI 前向已验证正常编译、失败编译和 detached child：正常路径进入 `WINDOWS_JOB_OBJECT`，失败路径不发布正式 rendered，detached child 未在 finalize 返回后污染目标；本轮新增的中断边界由执行型单元测试覆盖。

### 31.3 确定性 projection

能力源变化后重新按 builder inventory 计算并批准：

```text
policy/builder        = 1.16.0 / 1.16.0
capability source     = 10db5c1b9666164e06a9929bfb6ab15be821302e0538fe8ae6534f707bed8579
projection files      = 38 / 38
byte/file hash diffs  = 0
projection tree       = cb595dfa5a2a17b098078b59b0cdc6f5370b3f398d63cdac5069c04d676cde7a
manifest bytes        = 23,177 / 23,177
manifest sha256       = 78dca81b684bba29539fec607ff28a5164be3cc2d8bcc0927ba3ec06dd4f25c6
evidence cap          = E2
generation status     = NOT_EVALUATED
```

两份 v45 projection 位于 `build/generator-projection-maturity-v45-final-20260720` 与同名 `-repro` 目录；相对路径、长度和每文件 SHA-256 全部一致。该结果证明固定输入到 generator projection 的字节级复现，不授予模型写作资格，也不改变 `REVIEW_CANDIDATE` 的待审边界。

## 32. 2026-07-20：双状态 replay 与 marker 级言语行为红蓝复测

### 32.1 红队攻击与修复结果

本轮针对“机械绿灯能否掩盖真实未决状态”继续攻击，确认并修复了四组可利用边界：

1. replay 自身 `PASS/0` 曾可能遮住归档记录的 `REVIEW/2`。当前合同强制并列披露 replay 状态与 recorded delivery 状态。
2. capture 曾可能把 option value 当作第二个位置工件，或在 `OSError` 中泄露路径和私有参数。当前必须恰好绑定两个真实工件，异常消息固定去敏。
3. 否定、模态和逻辑连接词的排除曾有 span 过宽风险。当前以实际 marker 精确匹配，覆盖 `不连续`、`不可微`、技术词“可”、route 句首以及“所以然”等反例。
4. replay 对 list/object status 曾在结构化拒绝前发生类型异常。当前统一 fail closed 为 `FAIL/1`。

蓝队复测证明：`不连续 → 连续` 会阻断；route 句首 marker 可按合同豁免，但同句后续“所以”删除仍阻断；`可逆 → 存在逆矩阵` 不误报 modality；`所以然 → 缘由` 不误报 logical relation；畸形 replay status 和 capture argv/OSError 均不能形成静默成功或敏感信息回显。

### 32.2 真实 TeX 前后向对照

旧 forward 候选删除“于是、从而、因此”，当前策略返回 `SPEECH_ACT_LOGICAL_RELATION_CHANGED`，所以旧 evidence 包发生 policy drift 时保持 `REVIEW/2` 是正确结果。修复后的 postfix COURSE 候选在当前策略下机械层、硬不变量、言语行为与风格信号均 PASS，但顶层仍为 `REVIEW/2`，因为 paired-quality 为 `PENDING_EXTERNAL_REVIEW`；`humanize_quality_claim_allowed=false`，学术正确性和作者身份均未评估。

这组对照表明：规则能阻止一类可观察的推导关系删失，但不能由此推出改后文本更自然、更正确或更像某位作者。`REVIEW_CANDIDATE` 只是待审候选，不是终稿。

### 32.3 当前生产快照

```text
contract/requirements/oracle = 2026-07-20.20 / 2.10.0 / 1.11.0
targeted tests               = 231 OK
full unittest                = 956 OK (skipped=8)
compileall / quick_validate  = PASS / PASS
policy / builder             = 1.19.0 / 1.19.0
capability source            = 3a0f337fd338f00a35da4e8e47f5fb5163c9ceb34bdf5a037eb9f2decbf16417
projection files             = 38 / 38; diff=0
projection tree              = 7151e633694661995fbb6c30142ef0282dcf944e8a766b8e1a427c19c8068932
manifest                     = ff23749a0f4e659c8c1320befb87a768766a7208ef5e05b39e90586fcadf2ce7
evidence cap                 = E2
generation qualification     = NOT_EVALUATED
```

两份 v47/v1.19 投影的路径、长度、逐文件哈希和 manifest 字节完全一致。这里的 PASS 只覆盖协议、自洽、机械边界和确定性。replay PASS 不是质量许可，scanner candidate 不是删除授权，本地模型解释不是外部 paired-quality clearance；学术正确性、自然度、作者身份和模型生成资格继续保持未批准。

## 33. 2026-07-20：前向路由、句壳、报告 UI 与零编辑状态红蓝复测

### 33.1 红队发现

新鲜前向任务在不告知预期修复的情况下暴露出五类可操作缺口：

1. 清晰 COURSE/MODELING 文本因 policy 阈值高于书面合同而回退 GENERAL。
2. 正分平局的合同一处仍允许模型“按读者动作临场裁决”，与固定 `AMBIGUOUS` 策略冲突。
3. 删除“需要指出的是”或无信息“从而为后续……提供起点”时，硬门把句壳 marker 误作语义 marker。
4. 检测报告中 `risk-score: 87%` 被误收为正文 fragment。
5. 零可编辑长文的 prepare 提示更新后，finalizer 完整性重建未同步，CLI 返回错误的 `FAIL/1`。

另有两类信任面由本地主动审计发现：多个 JSON 入口仍允许重复键后值覆盖；stale source 的文本摘要没有明确说明 unit 状态不代表当前来源覆盖。

### 33.2 蓝队修复与反例保护

路由 policy 现在用 `score>=2`、`margin>=1`；任意两个正分场景并列最高均为 `AMBIGUOUS/UNRESOLVED`，不允许 hidden priority 或 document prior 破平局。测试同时覆盖直接路由、弱证据 GENERAL、平局以及 second-pass 重建。

句壳修复只豁免精确 marker span。蓝队正例允许删空重点壳和无信息未来桥接壳；反例继续阻断真实推导关系删除，并确认同句后续 marker 不被前一个句壳连带豁免。

报告 extractor 只过滤短评分/概率 UI，`<mark>` 正文不受影响。零编辑路径现在稳定为 `REVIEW/2 + no_authoring_eligible_units`，且不发布 scaffold；finalizer 重建值与 prepare 字节语义一致。stale source 摘要显式否定“unit 状态证明当前覆盖”。五个关键 JSON 面均改为 strict duplicate-key rejection。

### 33.3 长文前向矩阵

本轮真实 TeX 前向路径的权威结果为：

| 场景 | 当前状态 | 允许的结论 |
|---|---|---|
| 乱码 include | `SKIPPED_GARBLED`，顶层 REVIEW | 已跳过不可可靠读取材料；不得声称全文覆盖 |
| 零编辑范围 | `REVIEW/2` | 无可编辑作者正文；不得启动盲写或声称完成 |
| 缺任一 bundle | `FAIL/1` | 工件闭集不完整，必须补齐后重跑 |
| 完整 `NO_CHANGE` + 编译 PASS | `REVIEW/2` | 候选组装与编译事实可记录；paired-quality 仍 pending |
| 编译退出 7 | `FAIL/1` | 不发布正式 rendered，旧 canonical 恢复 |
| 编译超时 | `FAIL/1` | Windows Job Object 清理通过；不把超时写成文本失败 |
| source snapshot 漂移 | `REVIEW/2` | unit 状态不证明当前来源覆盖，不发布正式 rendered |

TeX 标题、cite、label、数学、注释、引语、equation 与 verbatim 的保护路径保持通过。乱码原因仍较粗，只记录 UTF-8/GB18030 解码失败位置；当前报告不夸大为编码根因分析完成。

### 33.4 全量复测与生产快照

```text
full unittest         = 966 OK (skipped=8)
compileall            = PASS
quick_validate        = PASS
policy / builder      = 1.20.0 / 1.20.0
capability source     = 35ef9306d2bbfe84b7fdddd8a405c4efa2becdd6325b9f0a8c8cd1676ac6a054
projection files      = 38 / 38; path/length/hash diff=0
projection tree       = e28f0df87dd8f3c1b807ac6a46f4bb51ca43d45043ab945e2a78f8e0e230da0b
manifest              = 13b2141047572f506537f138703d51bc01a99dfb5bada048f8a488b3f499d2cd
manifest byte-equal   = true
evidence cap          = E2
generation qualification = NOT_EVALUATED
```

这轮红蓝复测提高的是 fail-closed、一致性和误完成态拦截能力。它没有签发自然度许可：路由正确不代表文本好，句壳可删不代表改后搭配更优，检测报告 scope 正确不代表检测器可信，机械测试全绿也不能替代外部 paired-quality、作者判断或学术复核。

## 34. 2026-07-20：v1.21 前向红蓝复测与状态流加固

### 34.1 红队前向结果

三个无答案泄漏任务分别攻击短文修改、材料约束起草和长 TeX 调度。短文任务能删除空强调壳与未来桥接壳，但对“已有研究表明”没有伪造出处或擅自删除，而是留下 `UNRESOLVED_UNSOURCED_ATTRIBUTION`；受限 DRAFT 只并列 A=12、B=9，不把数值差擅写成机制结论，并保留外部验证与实测缺口；长 TeX 对乱码 include 标记 `SKIPPED_GARBLED`，保护区不进入盲写，最终为 `REVIEW/2 + PARTIAL`，源文件修改数为 0。

首次长文 finalization 因执行期间 prepare 策略变化而触发 snapshot drift，重新 prepare 后才通过。这是预期的 fail-closed 行为：旧策略下产生的计划不能在新策略下静默沿用。三组任务均没有取得 paired-quality clearance；内层 replay PASS 不能覆盖顶层 REVIEW。

### 34.2 新攻击面与修复

红队继续检查“看似结构化、实则可被解析宽松性篡改”的状态面，发现并修复三项：

1. Codex 事件 JSONL 的两条读取路径改为 strict object parsing，拒绝重复键、`NaN` 和非 object 事件。
2. POSIX compile supervisor 的 status FD 改为 strict parsing，拒绝重复 `cleanup` 与非有限 `command_exit`。
3. 乱码诊断改为有界 codec/位置/失败字节摘要，不回显正文窗口；乱码单元继续跳过且强制 REVIEW。

这些修复阻断了后值覆盖和非标准数值进入审计状态，但不验证事件来源真实性，也不把失败字节解释成编码根因。

### 34.3 蓝队回归与投影复现

```text
targeted v1.21 tests = 257 OK (skipped=3)
full unittest        = 966 OK (skipped=8)
compileall           = PASS
quick_validate       = PASS
git diff --check     = PASS; only LF/CRLF notices
policy / builder     = 1.21.0 / 1.21.0
capability source    = fb758249bb492ee69b04f51282b74e2f2edf047c2c8ecbb1d0b416a9f6c74bbb
projection files     = 38 / 38; path/length/hash diff=0
projection tree      = fde3558ef86d234efc2ae6c63d1f818db46f7390b4ddf6db128e1b16ba469b88
manifest             = dc0d7034143c259da88159a709209f3b280db67691768feaeaa88e770875aca3
manifest byte-equal  = true
evidence cap         = E2
generation qualification = NOT_EVALUATED
```

两份 v49/v1.21 投影位于 `build/generator-projection-maturity-v49-v121-20260720` 与同名 `-repro`。38 个文件逐路径、长度与 SHA-256 相同，tree hash 相同，投影外 manifest 逐字节相同。构建器还主动拒绝 manifest 自包含，因此该复现没有把清单自身递归计入输入。

### 34.4 红蓝结论边界

本轮可以确认：三个真实前向任务没有出现静默完成；事件流和编译状态不能再借重复键或非有限数改变语义；乱码不会拖住其余长文单元，并留下有界审计线索；当前固定投影可复现。

仍不能确认：候选自然度优于原文、学术判断正确、材料归因真实、作者身份成立或模型已获稳定生成资格。`REVIEW_CANDIDATE` 不是终稿，`PENDING`、保护单元和 `REVIEW/2` 不得包装成完成；capture/replay PASS 只证明机械自洽，外部 paired-quality 与 generation qualification 继续保持未批准。

## 35. 2026-07-20：候选状态 `NaN/Infinity` 红蓝攻击

### 35.1 红队攻击

继续审计 JSON 单义性后发现，candidate package、历史 queue result、revision candidate 与 supersedes result 会拒绝重复键，却仍接受 Python JSON 扩展常量 `NaN/Infinity`。这类值可能绕过“字段是 number”的直觉并污染比较、序列化或后续审计，因此不能被称作 strict JSON。

### 35.2 蓝队修复

候选队列和 revision 两条链均增加 `parse_constant` 拒绝器。反例覆盖：

- candidate id 位置注入 `NaN`；
- 已存在 queue result 注入 `Infinity`；
- revision 原 candidate 注入 `NaN`；
- supersedes result 注入 `Infinity`。

四个入口现在全部 fail closed；历史队列污染不能被当作可用 lineage head。

### 35.3 验收与范围

```text
targeted tests          = 52 OK
full unittest           = 969 OK (skipped=8)
compileall/validate     = PASS/PASS
policy/builder          = 1.21.0/1.21.0
capability source       = fb758249bb492ee69b04f51282b74e2f2edf047c2c8ecbb1d0b416a9f6c74bbb
evaluation surface      = cc3ab2063f1fca311e48ff1542c28697df0154fea8222b8444eb1a6d4ecb7b16
projection tree         = fde3558ef86d234efc2ae6c63d1f818db46f7390b4ddf6db128e1b16ba469b88
updated manifest        = 2b6e26e468c947077b39d82a36a063d8bf1eb8c4bbeb7a2aff8f0abbd835a91d
projection/manifest diff= 0 / byte-equal
```

修复发生在 `EVALUATION_SURFACE`，所以 capability hash 与投影 tree 正确保持不变，manifest 则记录了评估面与 inventory 的变化。这里没有为了形式上的“升级”虚构 1.22 版本。

该修复只阻止非标准数值污染候选状态，不能评价候选的自然度、学术可靠性或作者风格。顶层 REVIEW、paired-quality pending 与 generation qualification 未批准的边界保持不变。
