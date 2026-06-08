# 六级听力做题规律与选项推理完整手册

## 研究口径

本手册来自对 `Some PDF files do not have a text layer, and in such cases, OCR (Optical Character Recognition) will fail` 文件夹内六级真题与解析 PDF 的整理。

已生成的结构化底稿包括：

- `listening_manifest.csv`：30 份解析 PDF 的文本/OCR 状态。
- `answer_marker_records.csv`：433 个听力原文答案定位点，如 `[9]`、`(9)`。
- `question_option_records.csv`：419 道原卷听力选项，其中 413 道能稳定拆成 A/B/C/D。
- `answer_explanation_records.csv`：186 条解析抽取记录。

注意：不少解析 PDF 是双栏扫描版，OCR 会把左右栏串在一起，因此 `answer_explanation_records.csv` 的答案字母不能直接当绝对金标准。本手册更依赖“原文答案定位点 + 原卷选项 + 可读解析样本”的交叉规律。

## 总原则

六级听力不是平均考全文，而是集中考“题点句”。正确项通常不是听起来最耳熟的选项，而是把原文题点句的逻辑关系换一种说法。

真正要抓的是：

> 谁 + 做什么 + 对谁/什么 + 为什么 + 程度/时间/范围 + 转折/比较/因果

常见错误项不是凭空编造，而是借用原文附近的词，再偷换：

- 主语
- 动作
- 时间阶段
- 因果方向
- 程度强弱
- 范围大小
- 说话人立场
- 例子与结论

## 最强答案信号

听到以下功能词附近，要立刻提高注意力：

- 转折修正：`but`, `however`, `actually`, `in fact`, `no`, `not...but`, `instead`, `rather than`
- 因果解释：`because`, `why`, `reason`, `this is why`, `due to`, `lead to`, `result in`
- 研究发现：`researchers found`, `studies show`, `one study found`, `the study suggests`
- 建议计划：`should`, `suggest`, `advise`, `recommend`, `always`, `make sure`, `try to`, `need to`
- 总结换言：`essentially`, `in other words`, `that means`, `in short`, `finally`
- 比较数字：`more than`, `less than`, `higher`, `lower`, `doubled`, `twice`, `compared with`

浓缩口诀：

> 转折听后半，比较听方向，因果听关系，建议听动作，结尾听总结。

## Section A：长对话

### 题号规律

- Q1/Q5：常问身份、关系、场景、谈话主题，答案多在开头 1-3 轮。
- Q2/Q6：常问某人的看法、行为、细节，答案紧跟上一题后。
- Q3/Q7：常问原因、态度、问题本质，常在 `why`, `how`, `what` 追问后。
- Q4/Q8：常问下一步计划、最终结论、最后担忧，答案常在对话末尾。

### 做题抓手

Section A 的关键是“跟人”。

- 题问男士，就跟男士立场。
- 题问女士，就跟女士立场。
- 不要把另一人的评价、反问、铺垫拿来答。

听到这些结构要特别注意：

- `So what are your plans?`
- `Why did you...?`
- `How did you...?`
- `Do you intend to...?`
- `Actually...`
- `No...`
- `I mean...`

### 常见陷阱

1. 男士观点套到女士身上，或反过来。
2. 听到原词就选，但题问的是具体动作。
3. 原文说 `less important than encouragement`，选项却写成 `editorial guidance`。
4. 原文列举多个未来动作，正确项可能是上位概括。
5. 过去失败、现在状态、未来计划被混在一起。
6. 相邻题串线，把 Q6 的信息拿去答 Q8。

### 例子

`2022.06.set1 Q3`：

原文核心是 `editorial guidance is less important than encouragement`。选项里 `editorial guidance` 是听到了，但正确方向是 `encouragement`。

`2022.06.set1 Q8`：

原文说不打算开实体店，而是继续 online，并增加儿童服装、男装设计。细节上听到 `add`，但题若问未来计划，概括方向是 `expand her business`。

## Section B：短文

### 题号规律

- Q9/Q12：常问主题、争议、首个研究发现，答案常在开头。
- Q10/Q13：常问原因、机制、数据、比较，答案常在 `because`, `reason`, `this is why` 附近。
- Q11/Q15：常问结论、影响、建议、转折后的真实结论，答案多在后半段或结尾。

### 高频题点

- 研究发现：`researchers found`, `studies show`, `one study found`
- 数据比较：`doubled`, `80%`, `more than`, `less than`
- 限定词：`short periods`, `chronic`, `moderate`, `excessive`
- 因果链：广告导致儿童购买要求、技术缺陷导致低效、工作控制权影响幸福感等

### 常见陷阱

1. 动物实验、人类结论、消费者建议、研究者发现互相偷换。
2. 背景概念被写成全文主旨。
3. 因果反转：A 导致 B 写成 B 导致 A。
4. 限定词偷换：`chronic` 换成 `short periods`。
5. 程度放大：`slightly higher` 写成 `excelled`。
6. 范围扩大：局部研究结论写成所有人群。

### 例子

`2022.12.set1 Q9`：

原文是老鼠在短期压力下新脑细胞增长翻倍。真正关系是 `doubled the growth`，不是只听到 rats、stress、memory test。

`2022.12.set1 Q11`：

原文先说 `chronic stress` 有害，后转折说 `short periods of stress` 可能有保护作用。若题问短期压力，不能选慢性压力的危害。

## Section C：讲座/讲话/录音

### 题号规律

- Q16/Q19/Q22：常问开场主旨、讲话目的、问题背景。
- Q17/Q20/Q23：常问具体建议、实验过程、分类依据、中间发现。
- Q18/Q21/Q24：常问推论、影响、核心特征。
- Q25：高概率在最后总结，尤其是 `essentially`, `in short`, `instead`, `finally` 后。

### 做题抓手

Section C 的选项更抽象。预读时先判断四个选项共同主题：

- 建议
- 研究发现
- 人物特质
- 社会现象
- 问题解决方案
- 主旨或目的

### 常见陷阱

1. 把例子当主旨，如 Boston、医院、老鼠、百万富翁、app、bear。
2. 中间信息显眼，但题问结尾总结。
3. 原文说某行为不好，选项把它写成建议。
4. 抽象同义替换不明显。

### 例子

`2022.06.set1 Q17`：

原文建议 `Always bring an advocate... write down every single question and the answer, the name of every doctor and nurse.` 正确方向是记下医生护士姓名/带人陪同，而不是只抓“不要说负面话”。

`2022.06.set1 Q25`：

原文结尾说 `they don't yield to pressure... to keep up with others... Instead... long-term wealth-building plan`。正确方向是“不试图跟别人攀比”。

## 只看选项的预判法

播放前不要急着猜字母，先判断题型。

### 四个选项主语一样

多半问行为、态度、原因、结果。

重点听：

- 谁的立场
- 动词关系
- 时间阶段
- 限定词

### 四个选项动词不同

动词就是答案核心。不要只圈名词。

例如同样都讲 millionaires，真正答案可能在：

`do not try to keep up with others`

核心不是 millionaire，而是 `do not keep up`。

### 四个选项都有研究/实验/发现

不要听到 `study` 就选。真正要听：

- found what
- showed what
- suggested what
- compared with what

### 四个选项都是建议/计划

等：

- `should`
- `need to`
- `plan`
- `intend`
- `make sure`
- `always`
- `recommend`

### 四个选项都是抽象名词

多半问主旨、争议、结论。

优先听开头主题句、争议句、结尾总结句。

### 四个选项混有例子和概括

如果题问主旨、目的、说明了什么，优先怀疑概括项。

如果题问具体细节，才优先考虑具体例子。

## 选项形态规律

在 413 道可稳定拆分的四选项题中，表面特征大致如下：

- 比较词类约 84 题：`more`, `less`, `higher`, `lower`, `doubled`
- 否定词类约 60 题：`not`, `no`, `cannot`, `avoid`, `refrain`
- 绝对词类约 57 题：`only`, `all`, `always`, `never`
- 建议计划类约 43 题：`should`, `plan`, `recommend`, `make sure`
- 研究发现类约 43 题：`research`, `study`, `found`, `showed`

这些特征不是“答案加成”，而是“题眼暴露器”。它们告诉你听什么维度，但不能直接替你选答案。

## 相反项规律

常见说法是：“ABCD 里如果有两个相反选项，答案就在其中一个。”

更准确的说法是：

> 相反项不是答案保证，而是考点预警。

### 常见对立类型

- 正负评价：`beneficial` vs `harmful`
- 趋势方向：`increase` vs `decrease`
- 数量比较：`more` vs `less`
- 能力判断：`can` vs `cannot`
- 效果判断：`effective` vs `ineffective`
- 态度立场：`accept` vs `reject`
- 理论好处 vs 现实风险
- 说话人 A 立场 vs 说话人 B 立场
- 对象效率对立，如 house plants vs natural ventilation

### 为什么有用

两个选项如果在同一维度上正反对立，题目大概率考这个维度。听的时候重点判断：

- 原文最后落在哪边
- 题目问谁
- 题目问哪个时间阶段
- 是理论设想还是现实问题
- 是转折前还是转折后

### 容易误伤

1. 词面相反，但主体不同。
2. 原文两边都出现，题目只问其中一个说话人。
3. `not` 造成双重否定。
4. 比较句不是绝对否定，`less important than` 只是优先级较低。
5. 第三个选项可能是更精准的上位概括。

### 例子

`2022.06.set1 Q3`：

`editorial guidance` 与 `encouragement` 构成比较两端。原文说前者不如后者重要，答案方向是后者。

`2022.06.set1 Q6`：

`showed her natural talent` 与 `mostly failures` 构成正负结果对立。原文说最初做的大多是 disasters，答案方向是 failure。

`2022.06.set1 Q25`：

原文说他们 resist lifestyle creep，并且 do not yield to pressure to keep up。选项若写成 do not resist novel lifestyles，就是把方向反了。

`2025.12.set2 Q1`：

男方认为价格 absurd，女方认为 perfectly appropriate。题问谁的态度，就跟谁。

## 唯一否定项规律

唯一否定项不一定是答案。它只是提醒你：这题可能考否定、限制、避免、转折。

看到以下词要标记：

- `not`
- `no`
- `never`
- `cannot`
- `avoid`
- `prevent`
- `refrain`
- `resist`
- `without`
- `lack`

正确用法：

1. 标记否定项。
2. 听原文是否有 `not`, `no`, `but`, `instead`, `rather than`。
3. 判断否定的是哪个对象。
4. 判断题目问的是“应该做”还是“不应该做”。

错误用法：

> 看到唯一否定项就直接选。

## 绝对词规律

看到这些词要警惕：

- `only`
- `all`
- `always`
- `never`
- `completely`
- `entirely`
- `every`
- `must`

绝对词常用于过度概括。

判断标准：

- 原文明说绝对，才选绝对。
- 原文只是倾向，就排除绝对。

例外：

如果原文明确说 `Always bring an advocate`，那 `always` 可以是答案。

## 比较词规律

比较词是高价值题眼：

- `more`
- `less`
- `higher`
- `lower`
- `better`
- `worse`
- `doubled`
- `compared with`
- `than`

做比较题不要只听两端名词，要听：

- 比较对象
- 比较方向
- 比较程度
- 比较条件

口诀：

> 比较题死在对象，方向题死在正反，程度题死在强弱。

## 最长项规律

“最长选项容易对”在六级听力里不可靠。很多最长项只是把干扰信息写得更完整。

更准确的说法：

> 不是最长项更对，而是逻辑关系最完整的项更像答案。

完整关系包括：

- 主语
- 动作
- 对象
- 限定条件
- 因果/转折/比较关系

## 原词复现规律

原词复现很危险。六级常把原文附近的词搬进干扰项。

正确项常是同义改写：

- `independent + curiosities` -> `curious and autonomous`
- `disasters` -> `mostly failures`
- `do not yield to pressure to keep up` -> `do not try to keep up with others`
- `reflection` -> `contemplation`
- `take the lead` -> `take the initiative`

看到原词项，要问：

1. 原文是在肯定它吗？
2. 原文是在否定它吗？
3. 它是不是比较中较弱的一端？
4. 它是不是前半句铺垫？
5. 它是不是相邻题的信息？

## 三具体一概括

如果三个选项很具体，一个选项很概括：

- 细节题：具体项更可能对。
- 主旨题：概括项更可疑。
- 计划题：若原文列举多个动作，概括项可能对。
- 结论题：概括项常比局部细节更稳。

例子：

原文列举加儿童服装、加男装设计，题问未来计划，正确方向可能是 `expand her business`。

## 理论好处 vs 现实风险

Section B/C 常见结构：

1. 先说理论好处。
2. 再用转折引出现实风险。

例如：

- 理论上 automation could liberate people。
- 实际上 it puts jobs and wages at risk。

题问 actual concern，就选风险。题问 potential benefit，才选好处。

因此，正负选项同时出现时，不要急着选负面项，要先听题目问的是“可能好处”还是“现实问题”。

## 主语偷换

同一段可能同时出现：

- researchers
- consumers
- parents
- children
- workers
- employers
- technology
- pollution

题问谁，就只跟谁。

原文说“技术 inefficient”，不能选“污染 harmful”。两者可能同段出现，但题问对象不同。

## 例子 vs 结论

具体例子常被放进干扰项：

- Boston
- hospital
- rats/mice
- millionaires
- apps
- bears
- students
- children

如果题问主旨、目的、说明了什么，通常不选例子，而选抽象结论。

## 常见干扰项全集

1. 原词复现但关系错。
2. 男士/女士角色错位。
3. 过去、现在、未来时间错位。
4. 原因和结果反转。
5. 程度放大。
6. 范围扩大。
7. 例子当主旨。
8. `not...but...` 前半句进干扰项。
9. 并列信息偷换。
10. 相邻题串线。
11. 理论好处和现实风险混淆。
12. 比较对象偷换。
13. 绝对词过强。
14. 说话人态度偷换。
15. 研究对象偷换。
16. 背景信息写成主旨。
17. 后果写成原因。
18. 建议对象偷换。
19. 正负方向反转。
20. 上位概括与局部细节混淆。

## 考场标记系统

预读选项时，给差异点做轻标记：

- 相反项：`↔`
- 否定词：`-`
- 绝对词：`!`
- 比较词：`<>`
- 计划/建议：`P`
- 研究发现：`R`
- 例子词：`ex`
- 概括项：`G`

然后按这个顺序听：

1. 题问谁。
2. 动作是什么。
3. 限定词是否一致。
4. 时间阶段是否一致。
5. 转折、比较、因果方向是否一致。
6. 是否只是原词复现。

## 没听全时的救题优先级

1. 选逻辑关系完整的。
2. 选限定词准确的。
3. 选转折后的。
4. 选结尾总结或明确建议。
5. 排除只复现原词但关系不完整的。
6. 排除范围过大、绝对过强、例子当主旨的。
7. Section A 末题优先回想最后一轮。
8. Section B 优先回想研究发现、因果句、数字比较。
9. Section C 优先回想开头目的和结尾总结。

两个选项都听到过时，不比谁更耳熟，比谁的关系更对。

## 播放前操作流程

1. 快速分段：1-4、5-8、9-11、12-15、16-18、19-21、22-25。
2. 给每题标类型：身份、行为、原因、结果、建议、主旨、态度。
3. 圈差异词：动词、否定词、限定词、时间词。
4. 标出相反项、绝对项、比较项、概括项。
5. 不背完整选项，只记冲突点。

## 听原文时操作流程

1. 按题号顺序等答案，不要因为听到选项词就提前选。
2. 听到转折、因果、研究发现、建议、总结，立刻提高注意力。
3. Section A 跟问答轮次。
4. Section B 跟段落推进。
5. Section C 跟总-分-总结构。
6. 每题只记 1-3 个关键词，优先记动词和限定词。

## 复盘训练法

不要只泛听。更有效的训练流程是：

1. 只看选项，预测题型。
2. 听一遍，只记功能词附近 1-3 个词。
3. 做完后找原文题点句。
4. 对每个错题标错因。
5. 汇总自己最常掉的坑。

### 错题复盘标签

| 标签 | 含义 |
|---|---|
| 角色错 | 男士/女士/研究者/消费者等主语错 |
| 时间错 | 过去、现在、未来混淆 |
| 限定错 | `short`, `chronic`, `only`, `some`, `all` 等错 |
| 因果错 | 原因和结果反了 |
| 范围错 | 局部结论扩大成普遍结论 |
| 例子错 | 把例子当主旨 |
| 转折错 | 选了转折前铺垫 |
| 比较错 | 比较对象或方向错 |
| 串题 | 把相邻题信息拿来答 |
| 原词坑 | 听到原词但关系不对 |

## 高可信规则

这些规则适合考场直接用：

1. 转折后优先。
2. 比较句听方向和对象。
3. 题问谁就跟谁。
4. 主旨题排除具体例子。
5. 结尾题听总结词。
6. 研究题听 found/showed/suggested 后面的内容。
7. 计划题听最后一轮或 `plan/intend/will/hope to`。
8. 两个选项都听到时，选逻辑关系对的。

## 辅助规则

这些规则可以帮助分配注意力，但不能直接决定答案：

1. 相反项常提示考点。
2. 唯一否定项提示可能考否定/限制。
3. 绝对词提示可能过强。
4. 比较词提示要听对象和方向。
5. 概括项在主旨题、计划题、结论题中更可疑。
6. 具体项在细节题中更可疑。

## 不可靠规则

这些不要迷信：

1. 最长选项必对。
2. 最短选项必错。
3. 唯一否定项必对。
4. 有相反项答案必在其中。
5. 听到原词就选。
6. 绝对词一定错。
7. 字母分布能押题。

## 最终口诀

相反项定考点，绝对项防过强；  
最长项别迷信，原词项常设坑；  
比较听方向，转折听后半；  
主旨排例子，细节抓限定；  
题问谁跟谁，别把同段信息乱串。

## 一句话压缩版

六级听力正确项通常不是最耳熟的选项，而是把原文题点句的逻辑关系改写正确的选项。听到转折、因果、研究发现、明确建议和结尾总结时，把那一句当成答案候选；看到相反项、绝对词、比较词和否定词时，把它们当作题眼预警，而不是蒙题依据。
