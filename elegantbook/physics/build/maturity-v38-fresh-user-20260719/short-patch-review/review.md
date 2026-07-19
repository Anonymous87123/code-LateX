# 短 PATCH 审阅视图

## 交付状态

- 候选交付：`REVIEW/2`
- 机械验证：`REVIEW`
- 硬不变量层：`PASS`
- 成对质量复核：`BLOCKED_BY_MECHANICAL_GATE`
- `humanize_quality_claim_allowed=false`
- `academic_correctness=NOT_EVALUATED`

## 已变化 hunk

### H001

- 决策：`DELETE_STYLE_SHELL`
- 来源字节：`24:45`
- 理由：删除没有新增学习对象或判断条件的空重点提示壳。

原文：

<pre>值得注意的是，</pre>

替换文本：

<pre></pre>

### H002

- 决策：`REWRITE`
- 来源字节：`45:87`
- 理由：保留解题提醒，将无条件记忆口令改为原文后段已经给出的条件辨认动作。

原文：

<pre>遇到这类题目时必须牢记公式。</pre>

替换文本：

<pre>遇到这类题目时，先看公式的适用条件。</pre>

### H004

- 决策：`DELETE_STYLE_SHELL`
- 来源字节：`159:228`
- 理由：整句仅作泛化价值拔高和自动后续桥接，删除不损失独立的物理条件或计算命题。

原文：

<pre>这个结论具有重要意义，能够为后续学习奠定基础。</pre>

替换文本：

<pre></pre>

## 未变化的未决 hunk

### H003

- 来源字节：`87:159`
- 理由：该句给出直接套用公式的许可，与后文的条件限制形成来源内部张力，纯文风层不判断其正确性。

<pre>若已知速度随时间减小，就可以直接套用匀变速公式。</pre>

### H005

- 来源字节：`414:486`
- 理由：该句禁止在条件不满足时直接代入，与前文的直接套用许可成对保留，等待学科或用户裁决。

<pre>若条件不满足，不能因为公式看起来相似就直接代入。</pre>

## 显式冲突对

### C001

- 规则：`OPPOSING_PERMISSION`
- 两侧：`H003` 与 `H005`
- 处置：`UNRESOLVED_PAIR`
- 理由：前文允许直接套用匀变速公式，后文要求先核对条件并在条件不满足时禁止直接代入，纯文风层不能裁决两者。

## 覆盖范围与限制

- 状态：`PASS`
- 作用域：`ENUMERATED_HIGH_AND_BOUND_DECLARATIONS_ONLY`
- 任务场景 / 扫描场景：`COURSE` / `AUTO`
- high / selection / conflict：`4` / `5` / `1`
- `semantic_completeness_claim_allowed=false`
- `humanize_quality_claim_allowed=false`
- 本视图不证明完整语义发现、学术正确性、作者身份或外部成对质量 clearance。

## 验证边界

- 交付：`REVIEW/2`
- 言语行为层：`REVIEW`
- 审阅时同时查看 `patch.diff`、`patch.bundle.json`，以及存在时的 `coverage.json`。
