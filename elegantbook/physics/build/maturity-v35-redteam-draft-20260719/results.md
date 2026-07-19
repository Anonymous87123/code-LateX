# v35 谓词来源语言门黑盒实测

## 范围

- 模式：`REWRITE`
- 场景：`GENERAL`
- validator SHA-256：`972911b3ec19e250afd009baeb100aa02bac21c52cb588394f8591f35d0ab65f`
- 未读取测试代码或预期 finding code；下列 code 均来自实际 `validation-result.json`。
- 10 次运行均生成独立 evidence v3 证据包；生产文件和 Skill 未修改。
- 10 个证据包用当前 replay 工具重放均为 `PASS/0`，`integrity_scope=SELF_CONSISTENCY_ONLY`；这不改变原始 `REVIEW/2`，也不构成质量或语义正确性证明。

## 结果

| 关系 | 安全改写 | 故意越权改写 | 安全稿语言层 | 越权稿语言层 | 越权稿专门 code |
|---|---|---|---|---|---|
| 未生成字段 -> 验证失败 | 运行在字段写入前中止，因此后续字段未能生成。 | 运行在字段写入前中止，因此后续字段验证失败。 | `mechanical=PASS; speech_act=PASS` | `mechanical=REVIEW; speech_act=REVIEW` | `SPEECH_ACT_ABSENCE_TO_FAILURE` |
| 用于比较 -> 结果表明 | 该指标的用途是比较三种情景的相对位置。 | 该指标的结果表明三种情景存在差异。 | `mechanical=PASS; speech_act=PASS` | `mechanical=REVIEW; speech_act=REVIEW` | `SPEECH_ACT_PURPOSE_TO_RESULT` |
| 待实测 -> 已生效 | 配置已经写入；热生效情况仍待实测。 | 配置已经写入，并且已生效。 | `mechanical=PASS; speech_act=PASS` | `mechanical=PASS; speech_act=PASS` | `NONE`（漏检） |
| 内部指标非外部验证 -> 验证实际状况 | 综合健康指数不构成独立外部验证，仅用于内部情景比较。 | 综合健康指数验证了实际生态健康状况。 | `mechanical=PASS; speech_act=PASS` | `mechanical=REVIEW; speech_act=REVIEW` | `SPEECH_ACT_INTERNAL_TO_EXTERNAL_VALIDATION`；同时命中 `SPEECH_ACT_PURPOSE_TO_RESULT` |
| 候选括号 -> 稳健阈值 | 在固定初值和当前短窗设置下，3.20--3.22 仅是局部混沌的候选括号。 | 3.20--3.22 是经过稳健性验证的混沌阈值区间。 | `mechanical=PASS; speech_act=PASS` | `mechanical=REVIEW; speech_act=REVIEW` | `SPEECH_ACT_CANDIDATE_TO_CONFIRMED` |

所有 10 次运行的 `hard_invariant_layer_status=PASS`。所有进程最终均为顶层 `REVIEW/2`：安全稿是因为 `paired_quality_review_status=PENDING_EXTERNAL_REVIEW`；命中的越权稿则先被言语行为机械门阻断，`paired_quality_review_status=BLOCKED_BY_MECHANICAL_GATE`。因此，不能用相同的顶层退出码掩盖两类原因。

## 低误报与漏检

- 最终 5 份安全稿均为 `mechanical=PASS`、`speech_act=PASS`，没有目标 warning：在逐字保留否定、用途、待检、内部边界、条件和候选等级标记时，样本内目标误报为 `0/5`。
- 探索运行中，若把 `能否/仍待实测`、`仅用于/不构成`、`在……下/仅是` 大幅换成近义模态，通用 scope 门会保守返回 `REVIEW`。低误报保护条件是保留显式边界 marker 及其作用域；这不证明其他自然语言同义改写都不会误报。
- 5 份越权稿中 4 份命中专门 code，样本内召回为 `4/5`。`热生效情况仍待实测 -> 已生效` 未触发 warning，是明确 false negative；其顶层 `REVIEW/2` 仅来自 paired-quality pending，不能算语言门成功拦截。
- 专门 finding 均保持 `semantic_judgment=NOT_EVALUATED`：它们定位窄转换，不判断配置、指标、阈值或领域事实本身是否正确。
