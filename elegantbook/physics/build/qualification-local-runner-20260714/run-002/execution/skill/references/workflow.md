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
voice: SCENE_DEFAULT | PROFILE:<id>
report_context: NONE | REPORT_INFORMED
locked_structure: yes/no + scope
protected_roles: quoted/exam-original/OCR/code/math/report-metadata/other
```

缺省使用 `REWRITE/AUTO/BALANCED/CLEAN/SCENE_DEFAULT`。显式用户格式覆盖默认输出。

先处理编码：按 UTF-8 读取；失败后再尝试可识别的本地编码；仍不可读才跳过并记录范围。不得因一次默认编码失败把整个文件当乱码。

### 1.1 REPORT_INFORMED 输入

用户提供检测报告或标红片段时，读取 [detector-report-intake.md](detector-report-intake.md)：

1. 用 `extract_detector_report_scope.py` 忽略脚本、样式、链接和报告 UI，只提取可见标注原文；
2. 有原稿时只接受唯一映射；重复、缺失或动态渲染片段标 `REVIEW/UNRESOLVED`；
3. 检测分数和标签只用于说明输入来源，不进入候选严重度和正文；
4. 映射后的每个片段重新识别 `author/quoted/exam-original/OCR/code/math`，报告标注不改变保护权限；
5. 按用户意图进入 `DIAGNOSE` 或 `REWRITE`，不因报告存在而增加确认轮次；
6. 拒绝目标百分比、预测分数、噪声预算、随机化和检测规避，但继续处理可明确分离的纯文风范围。

## 2. DIAGNOSE

只诊断，不改正文。该模式不执行 Rewrite 的三轮改写、保护后比对或完成声明。

### 2.1 读取

1. 运行词项扫描器或使用 `quick-checklist.md`。
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

默认只输出 3-8 个最高价值问题。一个位置只列一个主病灶；次病灶只有在改变动作时才保留。

### 2.3 输出

输出字段和顺序直接使用 [operational-contract.md](operational-contract.md) 第 5.1 节的唯一 `DIAGNOSE` schema，本文件不再重复定义缩减版。

`Decision` 使用 `KEEP/DELETE/REWRITE/REVIEW/NO_CHANGE/UNRESOLVED`。不要输出改写正文，不要使用“已调整、已完成改写”的声明。

## 3. REWRITE

### 3.1 建保护清单

锁定：用户指定措辞、直接引语、题干、法规/标准原文、OCR、代码、数学、TeX 命令、数字、单位、专名、术语、否定、模态、定义/命名/假设/观察/结果报告状态。

结构锁和强度权限决定是否可以合并、移动或删除段落。风格规则不得改变“谁称为什么、谁观察到什么、什么只是可能、什么尚未完成”。

### 3.2 先定位，不全量套规则

1. 扫描词项和句壳，得到候选行与上下文。
   `REPORT_INFORMED` 先以标注片段排序，但每个片段仍按同一词库和上下文合同裁决。
2. 连续阅读候选前后完整段落，判断是否为真实复用。
3. 识别一个主病灶；读取相应 `HUM-*` 节。
4. 仅在需要范例时读取当前场景的改写范式。

### 3.3 三轮改写

#### 第一轮：删除无功能脚手架

处理无信息路线预告、编辑提示、重复纠偏、错位管理/营销/教练腔和自动收尾。若词是术语、讨论对象或真实关系，使用 `KEEP`。

#### 第二轮：按授权调整结构

- `LIGHT`：跳过本轮。
- `BALANCED`：只在段内或相邻重复段之间调整。
- `STRUCTURAL`：可跨段重建，但必须保留 patch 和行映射。

只恢复原文可确认的主次。正式等权列表、定义组和标准条款不得为了“人味”被人为倾斜。

#### 第三轮：校准句子与声线

让对象、动作或观察在适当位置承担主句，但保留“本文定义、结果表明、我们观察到”等言语行为。调整句长、连接和解释密度，不批量生成“这里真正、只需、其余沿用”。

### 3.4 保护检查

对文件改写运行 `validate_humanize_output.py <before> <after> --scene <SCENE>`。统一验证器把硬不变量、言语行为警告、改后高风险残留和新增模板合并为一次可复现检查：退出码 `0=PASS`、`1=FAIL`、`2=REVIEW`。只有对交付所对应的精确改前/改后版本实际运行且退出码为 0，才能记录 `PASS`。脚本未运行、只做目测或检查后正文又有改动时记录 `NOT_RUN`。

对 `REVIEW` 中的高严重度候选和新增候选逐项裁决：能够说明其正式功能则用 `--keep-reason SIGNAL_ID=具体理由` 登记，否则继续改写。不得只检查“这里真正”等修复模板。内联短文若没有实际落盘运行验证器，只能报告 `NOT_RUN`，不能用人工比对冒充 `PASS`。

言语行为 warning 使用两阶段、只读 proposal 流程。首次 `REVIEW` 读取 JSON 结果中的
`warning_review_request.request_sha256` 与每条 `warning_fingerprint`；处理建议只能针对
当前 request 提交：

```powershell
python scripts/validate_humanize_output.py <before> <after> `
  --scene <SCENE> --format json `
  --propose-warning-resolution <WARNING_FINGERPRINT>=<具体处理建议> `
  --warning-review-request-sha256 <REQUEST_SHA256> `
  --warning-reviewer-kind HUMAN `
  --warning-reviewer-id <调用方标签>
```

本地 `HUMAN` 只是调用方自述。结果固定为 `identity_verified=false`、
`review_clearance_granted=false`、`attestation_status=CALLER_ASSERTED_HUMAN_REVIEW`，warning
仍在 pending/unaccepted 列表，退出码仍为 `2`。没有 proposal 时不得附带 reviewer metadata
或 request hash；旧 request 不能跨稿件、跨 warning、跨场景/保护术语或跨 policy 重放。
模型可以整理证据和 proposal，但不得把自身判断称为人工复核。

当前本地流程没有外部信任根。`VERIFIED_HUMAN` 只保留给代理无法访问私钥的外部审批
服务；必须在可信边界验证签名、artifact/request 绑定和审批范围，本地 CLI 不产生这种
clearance。未接入外部服务时，只有继续改稿并让 warning 在新版本上消失，才能进入 `PASS/0`。

保留原主张的语义方向不等于保留其营销或桥接句壳。优先用输入已有对象具体化；禁止“深刻揭示 -> 深入揭示”“奠定坚实基础 -> 打下良好基础”之类同义轮换。输入不足以具体化时保留原文并标 `UNRESOLVED`，不要假装修复完成。

## 4. DRAFT

1. 列出用户已提供的内容单元和不可补造项。
2. 选择场景、Voice Profile 和强度；Draft 的强度只控制组织幅度。
3. 以用户内容建立顺序和详略，不创建“改前问题清单”。
4. 缺失信息保留为占位、问题或省略，不用套话填满。
5. 输出起草正文和“使用了哪些 supplied content”；不要声称完成改写。

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
- 允许跨段重排和删除重复出口，但逐项保留信息映射。
- 完成后必须运行保护检查和幂等 dry-run。

## 6. 场景差异

### COURSE

让读者能定位学习难点：简单内容短写，关键选择放慢，第二解从分叉处开始。同一知识只保留一个完整汇总。不得把教师提示写成审稿限定。

### MODELING

让模型选择落到操作与后果：说明改变了什么、比较看什么、结果如何影响方案选择。不要只做通用“对象先行”，也不要引入期刊式防御串。

### RESEARCH

保留定义、报告和主张的言语状态；压缩预演审稿人的多重否定；观察先于图表导览；结论回收核心研究判断而不是验收目录。

### GENERAL

以 Voice Profile 和原结构为主。只应用高置信通用病灶，不强制“课堂松弛、工程决策或期刊克制”。

## 7. 交付与声明

### DIAGNOSE

只给诊断表和覆盖范围：

```text
已完成纯文风诊断；未修改正文。覆盖：<scope>。未覆盖：<scope/reason>。
```

### REWRITE

按用户输出模式给正文、注释或 patch。摘要列配置、3-8 个主要动作、保护检查结果和未解决项：

```text
已完成授权范围内的纯文风改写；mode=REWRITE, scene=<...>, intensity=<...>,
voice=<...>。硬保护检查=<PASS/FAIL/NOT_RUN>。未运行学术质控。
```

### DRAFT

```text
已根据用户提供内容起草；scene=<...>, voice=<...>。未补造未提供的学术内容。
```

若用户要求只输出正文，省略所有声明。不得把抽样处理写成全文完成。
