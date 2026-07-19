# v34 fresh forward root review

## 1. 评测目的与隔离

本轮不是为已有测试补一句规则，而是用三个普通用户任务检查当前
`humanize-academic-chinese` 是否会在内容权限、DRAFT 来源约束和输出形态上产生错误完成态。

三条路径固定为：

- COURSE TeX REWRITE：`tests/fixtures/humanize_forward_v10/course_before.tex`；
- MODELING DRAFT：`build/maturity-v20-postfix-20260717/cases/draft/facts.tex`；
- GENERAL REWRITE：`build/maturity-v20-postfix-20260717/cases/general/input.md`。

每一轮均使用新的 subagent 线程，只读取当时安装版 Skill、任务所需引用和原始输入。代理不得读取
本目录、历史候选、测试、报告或预期修复。三个原始输入均是压力材料；没有把它们当作真人 Voice
正例或事实来源扩展到其他任务。

## 2. 第一轮：旧合同暴露的两个主缺口

### 2.1 COURSE 擅自选边

源文同时含：

```text
若已知速度随时间减小，就可以直接套用匀变速公式。
```

以及：

```text
先确认题目给出的量是否满足匀变速条件……若条件不满足……不能直接代入。
```

第一轮代理删除前一条许可，保留后一条限制，并写：

```text
原文两处适用条件互相冲突，本稿按纠偏段的判断链组织
```

它虽然识别出冲突，却仍把自己选择的学科判断作为 `CLEAN` 候选交付。这不是文风收益问题，而是纯
文风层越过职责边界。当前旧 validator 若实际运行，已会因 negation/modality/condition 漂移返回
`REVIEW/2`；但代理标记 `NOT_RUN` 后仍给完整 CLEAN，说明仅有通用 marker warning 不能替代生成合同。

### 2.2 DRAFT 伪精确分类

第一轮 DRAFT 正文保留了所有数值、公式、物种关系和认识论边界，表面载荷没有新增；问题在摘要：

```text
FACT_PAYLOAD=11
EDITORIAL_REQUIREMENT=5
FACT_BOUNDARY=0
```

`FACT_BOUNDARY=0` 与材料中的“不构成独立外部验证”“不是本问的直接观测目标”直接矛盾。更根本的
问题是，输出没有任何能回放这三个数字的 unit ledger。原合同要求“列出三类计数”，却没有要求每个
计数绑定 source span，诱导模型生成看似专业但无法复核的数字。

GENERAL 第一轮只做局部措辞调整，保留标题、列表、强调、判断范围和事实关系，作为通过对照。

## 3. 第一组 TDD 修复

先新增 RED，证明以下行为在旧实现中不存在：

1. 同一词汇锚附近的正反直接许可被候选单边保留时，产生
   `SPEECH_ACT_SOURCE_POLARITY_TENSION_SELECTED`；
2. 诊断细节同时回显 source 正/负 span、rewrite 正/负 span、共同锚点和
   `academic_correctness=NOT_EVALUATED`；
3. 无关对象的“可以直接读取数据/不能直接给出结论”不误报；
4. 引语、代码和数学保护区中的同类词形不参与检测；
5. strict 模式把同一问题升级为硬错误；
6. Skill、操作合同、工作流、快速清单和可移植 Prompt 均要求保留双方并降级输出；
7. DRAFT 计数必须绑定 `unit_id + source_span + category`。

实现后，源文冲突只被描述为“有共同词汇锚的直接许可/禁止张力”，不叫学科矛盾。机械层不判断
哪个命题正确；只要 rewrite 仅保留一种表面极性，就要求 `PRESERVE_BOTH_AND_ESCALATE`。

DRAFT 分类改为：

```text
classification_status=NOT_UNITIZED
classification_counts=OMITTED_UNUNITIZED
```

只有 `supplied_unit_ledger` 无遗漏、无重叠地覆盖全部原材料，才允许输出三类数量。显式认识论、适用
范围和观测目标限制固定归 `FACT_BOUNDARY`；外层 `% FACT_PAYLOAD` 注释不能覆盖最小 unit 的边界角色。

## 4. 第二轮：规则方向正确，交付结构仍有漏洞

第二轮 COURSE 已经拒绝选边、声明 CLEAN 降级 PATCH，也回显了两个冲突 span。但它先用一个大
`REWRITE` hunk 覆盖整段，再把其中许可句重复列为 `UNRESOLVED`。同一 source span 同时属于两个
决策，读者无法知道实际要应用哪个 patch。

因此新增：

```text
patch_hunks_source_partition=NON_OVERLAPPING
```

同一 source span 只能属于一个 hunk；`REWRITE hunk` 不能包住另一个 `UNRESOLVED span`。冲突句必须
先从周围可删除的强调壳、教练壳和价值尾句中切出。

第二轮 DRAFT 不再给伪精确计数，也保留了两类边界，但根据材料中的数值自行新增：

- “长江鲟的降幅更大”；
- “两者降幅高于另一情景”；
- “进一步侵蚀”。

这些关系可以通过算术推得，不等于用户已经 supplied。DRAFT 是材料约束起草，不是数值分析器。
新增 `DRAFT_DERIVED_COMPARISON_NOT_SUPPLIED` 窄词形门：只要草稿首次引入降幅/末值的更大、更高、
跨情景高低或“进一步侵蚀”等表面关系，就保持 `REVIEW`，并明确
`semantic_entailment=NOT_EVALUATED`。若 source 已明确给出同类比较，控制样例不报警。

实际把第二轮 DRAFT 候选交给新版 validator 后得到：

```text
delivery_gate_status=REVIEW
speech_act_layer_status=REVIEW
draft_surface_source_check=PASS
semantic_source_check=NOT_EVALUATED
warning=DRAFT_DERIVED_COMPARISON_NOT_SUPPLIED
native_exit=2
```

这里的 surface PASS 只说明数字、数学和其他已编码载荷来自材料；专用 warning 与语义来源待审不能
被它覆盖。

## 5. 第三轮：COURSE/DRAFT 收敛，GENERAL 找到窄漂移

### 5.1 COURSE

第三轮输出形成四个互不重叠的真实块：

1. 删除“值得注意的是/必须牢记”句壳；
2. 原样保留许可句并标 `UNRESOLVED`；
3. 删除“具有重要意义/奠定基础”尾句；
4. 原样保留限制句并标 `UNRESOLVED`。

标题、公式环境和“不要只看公式的形式”原样保留，输出明确记录
`patch_hunks_source_partition=NON_OVERLAPPING`。该结果位于 `course/response-v34c.md`。

### 5.2 DRAFT

第三轮不再自行比较降幅，不报告无台账分类数，并完整保留：

- 当前参数组与公报口径的内部投影范围；
- “不构成独立外部验证”；
- `M/V` 不是直接观测目标。

它仍诚实写 `semantic_source_check=NOT_EVALUATED`。该结果是待审草稿，不是语义蕴含证明。

### 5.3 GENERAL

GENERAL 候选把：

```text
缺少成本、政策执行和外部验证层
```

改成：

```text
缺少成本、政策执行和外部验证层面的衔接
```

前者说内容层缺失，后者说层间关系缺失，缺失对象发生变化。新增
`SPEECH_ACT_MISSING_CONTENT_TO_LINKAGE`，作为现有 predicate-transition 门的一条窄规则：source
首次说缺少层/内容/分析，而 rewrite 首次把衔接/联系/过渡作为缺失对象时 REVIEW；source 原本就在谈
衔接的控制样例不报警。

实际 GENERAL c 候选同时被既有 `NUMBER_OR_UNIT_CHANGED`（“每一节”改成“各节”）硬门和新
transition warning 拦截，因此不能把这轮 GENERAL 候选作为通过稿。它的价值是证明新门能定位 fresh
语义漂移，而不是证明该输出自然。

## 6. 最终工具链证据

版本：

```text
policy/builder=1.10.4/1.10.4
capability_source=f7b2c28e0297a1ff669ffbc7a053ed1fce326c6c6aa612641f2ee9fadfe38502
projection_tree=670e58a62e56fbfbee0901e809fa388ac3beecee8e6698a850f4a79a0f092c12
manifest_file_sha256=b93536853f7229c5facc77d9773418266ee0930ad309c2687ffeb2f4157c6a3c
evidence_cap=E2
```

回归：

```text
full suite: 714 tests, OK (skipped=3)
qualification tests: 41/41
long finalizer: 131/131
unified validator: 73/73
invariant checker: 53/53
Skill contract: 33/33
projection builder: 37 PASS + 1 environment skip
scripts: compile 25/25; --help 25/25
quick_validate: PASS
SKILL.md: 443 lines
```

独立 projection：

- `build/generator-projection-maturity-v34-final-20260719/`
- `build/generator-projection-maturity-v34-final-repro-20260719/`

两边各 31 文件，逐路径字节差异 0，manifest 字节相同。资格/replay/second-pass 私有标识 0 命中；
三个新机械码与新生成合同均进入 projection。

生成资格仍为：

```text
evidence_integrity_status=PASS
qualification_status=NOT_EVALUATED
0 PASS / 0 FAIL / 188 NOT_EVALUATED
exit_code=2
```

fresh 输出、单元测试和 E2 projection 不能替代隔离签名的 188 原子资格证据。

## 7. 当前裁决与残余风险

v34 修复了五条具体错误路径：

1. 识别源文冲突后仍由纯文风层选边；
2. 没有 unit ledger 却输出 DRAFT 分类数字；
3. PATCH 用重叠 hunk 同时宣称改写与原样保留；
4. DRAFT 根据 supplied 数字新增比较和机制强度；
5. 把内容缺失改成关系缺失。

仍不能夸大为自动终稿器：

- polarity detector 只覆盖共享词汇锚的“正反直接许可”，不是通用矛盾检测；
- derived-comparison detector 只覆盖少量高风险词形，不证明其他 DRAFT 分句受材料蕴含；
- 短文用户可见 PATCH 的不重叠分区目前主要由生成合同约束，没有独立结构化 patch parser；
- predicate transition 规则不覆盖所有缺失对象轮换；
- paired-quality、作者身份、学术正确性和来源真实性仍未获得本地 clearance；
- 188 个生成资格原子仍全部未评估。

因此 v34 的准确定位是：对普通短文的权限拒绝、材料边界和错误完成态又增加了五个可复核抓手；
COURSE/DRAFT forward 行为明显收敛，GENERAL 的新漂移可被机器拦截。但它仍是生产级待审候选层，
不是无需复核的最终作者或学科裁判。
