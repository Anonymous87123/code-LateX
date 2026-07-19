# v41/v41.1 Fresh FOCUS、语义红队与 postfix 复盘

## 1. 复盘范围与状态口径

本复盘覆盖三组原始 fresh short-PATCH、三份独立评估、additive FOCUS 探针、v41 两条窄语义门、
`modeling-r3` postfix 失败链，以及 v41.1 投影和测试 checkpoint。它还记录 checkpoint 之后由独立盲读
发现的残余回归，但不把后续尚未封版的改动倒写成 v41.1 当时已经具备的能力。

证据根目录：

- [fresh fixtures 与运行](.)
- [postfix modeling-r3](../maturity-v41-postfix-20260719/runs/modeling-r3)
- [v41.1 final projection](../generator-projection-maturity-v41.1-final-20260719)
- [v41.1 repro projection](../generator-projection-maturity-v41.1-repro-20260719)

全文严格区分三类状态：

1. `v41.1 checkpoint`：当时固定 policy、测试和投影共同绑定的历史结果；
2. `postfix candidate`：机械组装和自洽可重放的待审候选，不是文风质量 clearance；
3. `checkpoint 后发现`：后续盲读或新门揭示的缺口，不能被旧 PASS 覆盖。

GPT 生成或来源未解决的 TeX/MD 只作负向压力材料，不作真人 Voice、事实来源或可复制正向句库。
本轮没有读取 `CET6.tex`。对话中曾报告过外部 502，但指定目录没有可复核日志；这些失败不计 Skill 证据。

## 2. fixture 来源与冻结身份

[source manifest](fixtures/source-manifest.md) 记录了三份 fixture 的精确来源、行范围和 SHA-256。审计按
LF 结尾逐行、逐字符复核，三份均与来源一致：

| 场景 | 来源 | SHA-256 | 角色 |
|---|---|---|---|
| COURSE | `physics1.tex:824-830` | `5ae03ae68826d5d93c2cf4e3135ce55607c16bc0946af08f2e8eb97e6b6261cd` | GPT 生成压力材料 |
| MODELING | 微信 `main.tex:50-68` | `6d1657bb1e296b130a325340728ca9b4ecc8fd574ac1911a0a1d114589d975ad` | GPT 生成压力材料 |
| GENERAL | `大创项目参考文献逐篇精读分析与会议总结.md:1225-1235` | `9e32f2099d4ed90d5ce8564f319aaf68ecf0ea82f663382cebe97d4832825b70` | 来源未解决压力材料 |

这些 hash 证明本轮 fixture 与登记来源字节一致，不证明来源作者身份、学术正确性或自然读感。

## 3. 三组原始 fresh 结果

### 3.1 COURSE

完整过程见 [COURSE operation report](runs/course/operation-report.md)。

最终配置和结果：

- `scene=COURSE`；
- 3 个 FOCUS、3 个 hunk、0 个 `UNRESOLVED`；
- 共 3 次 create，经历 2 个 recovery cycle；
- 第一次配置在 create 后被修改，finalize 以 `inventory_sha256 mismatch` 拒绝；
- 第一版候选删除条件标记，触发 `SPEECH_ACT_CONDITION_CHANGED`；
- 最终 candidate SHA：`79db57b25d22f3266aa2f2a3236567e2e6b155d871364c4eeaae9f97bc9fe16c`。

[blind style](evaluations/blind-style.md) 对 C1/C2/C3 均判为 `BETTER`；[blind semantic](evaluations/blind-semantic.md)
没有报告可定位语义漂移。这个结果只支持“该三处在本次盲读中更好”，不外推到 COURSE 全场景。

### 3.2 MODELING

完整过程见 [MODELING operation report](runs/modeling/operation-report.md)。

原始链条：

- AUTO scanner high：3；
- authoring suggestion：6 个 AVAILABLE、4 个 SUPPRESSED；
- 最终 8 个 hunk：7 个改写、1 个 `UNRESOLVED`；
- 首轮手填 UTF-8 offset 与 source 不一致，builder 拒绝；
- 后续删除直接引语，触发 `DIRECT_QUOTATION_CHANGED`；
- 再次恢复时仍经历 speech-act 与 high finding 修订；
- 最终 candidate SHA：`2b810dda5de41e9383dfb6b1de8c5a282c22858dcf660791561a970e6047acbc`。

盲读逐项为：

```text
M1 BETTER
M2 SAME
M3 BETTER
M4 WORSE
```

语义红队报告 1 项高严重度和 3 项低严重度。最关键的高风险不是词项残留，而是来源角色被改写：
“正文应保留粗扫/加密结果”的编辑要求，被写成“两类结果共同支持结论”的证据断言。机械保护项未漂移
并不能覆盖这种谓词角色变化。

### 3.3 GENERAL 输入与晚路由

完整过程见 [GENERAL operation report](runs/general/operation-report.md)。

route 脚本最终给出：

```text
resolved_scene=MODELING
MODELING score=8
margin=8
```

但实际使用先按 GENERAL 建 scaffold，恢复一次后才重建为 MODELING。最终结果：

- 3 个 FOCUS、3 个 hunk；
- 经过 GENERAL 初次、GENERAL retry、MODELING rebuild 和最后一次语义边界修正；
- candidate SHA：`f7669aecd306bca8f1827eb579be565186557fcd2a87948e5a4a9f4384524c41`；
- 盲读：G1 `SAME`、G2 `WORSE`、G3 `BETTER`。

高严重度回归是把集体/项目计划：

> 工程上，下一阶段先完成三件事

改成个人承诺：

> 下一阶段我先做三件事

中风险还包括删除“下一阶段”后扩大否定命题时域。原 operation report 对 H002 的“保留 first-person action
subject”理由也经不起来源核对，因为 source 中没有单数第一人称“我”。红队不仅检查正文，也检查理由是否
与原文相符。

## 4. 可用性成本：问题不只在 offset

[usability redteam](evaluations/usability-redteam.md) 把必要语义劳动与可消除录入劳动分开。三组最终候选为：

| 场景 | hunk | selection | hunk + selection reason | 明显恢复成本 |
|---|---:|---:|---:|---|
| COURSE | 3 | 3 | 6 | 3 次 create，2 次恢复 |
| MODELING | 8 | 8 | 16 | offset、引语、speech/high 三轮 |
| GENERAL→MODELING | 3 | 3 | 6 | 晚路由导致 scaffold 重建 |

不可自动化的是 span 是否真的有病灶、replacement、decision、真实 reason、保护词和 conflict 判断。
可以确定性处理的是 offset、稳定 ID、引用关系、未变 hunk 复用、hash/coverage 重算和局部恢复后的重新装配。

因此最高优先级缺口被定为：

1. P0：局部修订却被迫重建 immutable authoring→finalize→build→apply 全链；
2. P1：AUTO scene 在 authoring 后才冻结；
3. P1：offset/ID/linkage 和重复 reason 仍有不必要录入成本。

## 5. Additive FOCUS

v40 的 FOCUS 是“只 FOCUS”入口；v41 将其改成 additive caller input，可与默认 scanner/advisory 视图同时
存在。实际 CLI 产物为 [modeling additive probe](probes/modeling-additive.authoring.json)：

| kind | total | AVAILABLE | SUPPRESSED |
|---|---:|---:|---:|
| FOCUS | 1 | 1 | 0 |
| CLAUSE | 7 | 4 | 3 |
| SENTENCE | 3 | 2 | 1 |
| 合计 | 11 | 7 | 4 |

这证明调用方连续阅读定位的 span 不再要求放弃 scanner high 和 advisory 视图。它仍不证明 FOCUS 诊断真实、
用户授权存在或 replacement 有收益。与引语、数学、代码和 TeX 命令重叠时继续只发 SUPPRESSED。

## 6. v41 两条窄语义门

### 6.1 `SPEECH_ACT_EDITORIAL_TO_EVIDENCE`

拦截下列窄转换：

```text
正文应保留/呈现材料
    ->
材料支持/表明/证明结论
```

它准确命中原始 MODELING 的高严重度问题。该门只覆盖已编码的谓词组合，不证明其他自然语言蕴含安全。

### 6.2 `SPEECH_ACT_FIRST_PERSON_REFERENCE_INTRODUCED`

当改写新增 source 中没有的显式“我/我们”时进入 REVIEW；删除主持语中的“我们”不触发。它准确命中 GENERAL
候选把项目计划改成个人承诺的问题。

两条门回放三组原 fresh 候选：

- COURSE：未命中，机械层仍可 PASS；
- MODELING：命中 `EDITORIAL_TO_EVIDENCE`；
- GENERAL：命中 `FIRST_PERSON_REFERENCE_INTRODUCED`。

它们没有覆盖“下一阶段”时域丢失、用途限定丢失和所有编辑目的删除。因此不能写成“全部语义问题闭环”。

## 7. modeling-r3 postfix 失败链

完整报告见 [modeling-r3 operation report](../maturity-v41-postfix-20260719/runs/modeling-r3/operation-report.md)。

### 7.1 `review/`

- 5 个 hunk，其中 3 DELETE、2 UNRESOLVED；
- coverage PASS；
- style REVIEW；
- 2 个 high 没有具体解释。

该目录证明“coverage 已闭合”不能代替改后 high 复扫。

### 7.2 `review-revised/`

- 6 个 hunk、1 个 UNRESOLVED；
- style PASS；
- speech-act REVIEW；
- 三个未接受 warning：
  - `SPEECH_ACT_NEGATION_CHANGED`
  - `SPEECH_ACT_MODALITY_SCOPE_CHANGED`
  - `SPEECH_ACT_CONDITION_CHANGED`

没有提交 caller proposal 冒充人工 clearance。失败状态和 warning request 均保留。

### 7.3 `review-final/` 在 v41.1 checkpoint 下的结果

- 6 个 hunk：3 DELETE、2 REWRITE、1 UNRESOLVED；
- 5 个 changed hunk；
- candidate SHA：`99eb9f94d88cf3018729b966f66ca66eda09838ddc86a2b6e8bf4b3aca5dca6f`；
- v41.1 mechanical/hard/speech/style/coverage 均 PASS；
- verifier/current-policy replay/live source 均 PASS；
- 顶层仍为 `DELIVERY REVIEW/2`；
- `paired_quality_review_status=PENDING_EXTERNAL_REVIEW`；
- `semantic_judgment=NOT_EVALUATED`；
- `academic_correctness=NOT_EVALUATED`。

旧的“编辑要求变证据断言”和条件/预期丢失确实得到修正，但这不是最终质量通过。

## 8. checkpoint 后的独立盲读推翻了一个局部改动

新的独立 paired review 只读取 source 与 `review-final/candidate.review.tex`，没有读取既有诊断。五个实际变化
被判为：

```text
BETTER 3
SAME   1
WORSE  1
```

唯一明确 `WORSE` 位于第 13 行：

```text
因此，正文里既要保留粗扫结果……
    ->
因此，既要保留粗扫结果……
```

候选删掉“正文里”这一位置限定，却保留“既要……也要……”的编辑要求。结果既没有真正正文化，又缩小了
来源信息。这个缺口不属于数字、公式、否定或现有谓词升级门，因此 v41.1 当时的机械 PASS 没有抓住它。

checkpoint 后新增的窄门 `SPEECH_ACT_EDITORIAL_SCOPE_DROPPED` 已能把该候选降为：

```text
mechanical=REVIEW
speech_act=REVIEW
warning=SPEECH_ACT_EDITORIAL_SCOPE_DROPPED
```

因此 `review-final` 只能称为“v41.1 snapshot 下机械 PASS，后续盲读发现残余回归”，不能称为当前 PASS。

## 9. v41.1 冻结测试与投影

历史 checkpoint：

```text
focused=268 total; 266 passed; 2 skipped
full=823 total; 819 passed; 4 skipped
scaffold trace=1095/1218 = 89.90%
SKILL.md=451 physical lines
builder/policy=1.12.0/1.12.0
approved capability=b4b23a95bf86508c178947d8d917a0c5f86b9808f584ace4442c56385f992d89
projection files=37/37
BYTE_DIFFS=0
projection tree=2c10ddaba1a942be31c1c6408db9da63752074977ba0f92f7656f9d1aa22e482
manifest file SHA=7cb79ed086319fc86b598fa02691e84aca2b86bbe5684b34d274160b0b0bf4ae
quick_validate source/final/repro=PASS/PASS/PASS
evidence_cap=E2
generation qualification=NOT_EVALUATED
```

这些数值绑定 v41.1 冻结字节，不代表其后的 current source。后续 capability 文件变化时，projection gate
按设计 fail closed；必须更新固定 capability approval、重新运行全量测试和双投影后，才能形成新 checkpoint。

## 10. 当前审计边界与下一步

本轮最重要的负面结论有四项：

1. 两条新语义门能抓住两个高严重度案例，但不是完整语义审查器；
2. v41.1 postfix final 仍有独立盲读可见的局部回归；
3. 一个局部 warning 修复仍要求重建整条 short-PATCH 链；
4. AUTO route、registry/ID/linkage 和 `reason_ref` 仍未完成。

下一项生产改进应优先实现 run-scoped amend：从已通过闭集与 current-policy replay 的 parent review 出发，
只允许改变列出的既有 hunk 的 `decision/replacement/reason`；source、配置、coverage declarations、hunk 拓扑、
selection 和其他 hunk 必须保持。父子关系需要可重放血缘，policy/live-source drift 必须在发布前阻断。

后续仍不得宣称：

- 文风质量已经外部通过；
- 学术正确性已评估；
- 作者身份已确认；
- 生成资格已获得；
- scanner 或语义门已经发现全部自然语言问题。
