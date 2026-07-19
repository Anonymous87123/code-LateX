# v37 final coverage-aware short PATCH forward review

## 1. 任务与隔离条件

本次 fresh forward 只给执行代理以下输入：安装版 `humanize-academic-chinese`、原始课程 TeX、用户式
PATCH 请求和新输出目录。代理被明确禁止读取任何名称含 `maturity-v37-coverage-fresh`、
`generator-projection` 或 `root-review` 的旧工件，因此不能复用上一轮 selection、预期 hash 或结论。
源文件、Skill 和测试均未修改。

```text
source=tests/fixtures/humanize_forward_v10/course_before.tex
source_sha256=9805eab8480836f942078c112dfcd4160c293cd18bfd79ae0e308c02db956b65
mode=REWRITE
scene=COURSE
intensity=BALANCED
requested_output=PATCH
effective_output=PATCH
source_kind=DOCUMENT
scan_scene=AUTO
```

用户要求删除可定位的空重点、教练命令和泛化意义/后续铺垫，但不允许纯文风层裁决两条关于能否
直接套用匀变速公式的相对主张。后两句必须逐字保留并形成显式 conflict pair。

## 2. 两轮候选及第一轮的有效失败

第一轮把“遇到这类题目时必须牢记公式”整句删除。patch 能应用，high signal 也归零，但统一验证器
检出 `SPEECH_ACT_MODALITY_SCOPE_CHANGED`：原句中的“必须”被整体移除。该结果没有被误写成完成，而是
保存在 `attempt-1/`，状态保持 `REVIEW/2`。

第二轮没有简单豁免 warning，也没有删除模态，而是把同一 source span 改为：

```text
遇到这类题目时，必须判断公式能否直接套用。
```

这个改句只复用原文已经出现的“公式”“直接套用”和必须性，不补造新的物理结论；它把无对象的记忆
命令落到判断动作。机械层由此转为 PASS。该 PASS 只表示已编码不变量和 warning 未阻断，不证明改句
在读感上必然优于原句。

## 3. 最终 hunk

| Hunk | 决策 | 处置 |
|---|---|---|
| `H001` | `REWRITE` | 合并空重点壳与教练命令，保留“必须”，改成对公式适用性的判断动作 |
| `H002` | `UNRESOLVED` | “速度随时间减小即可直接套用”逐字保留 |
| `H003` | `DELETE_STYLE_SHELL` | 删除“具有重要意义/为后续学习奠定基础”整句空出口 |
| `H004` | `UNRESOLVED` | “先核对匀变速条件、条件不满足不得直接代入”逐字保留 |

`H002/H004` 绑定为一组 `OPPOSING_PERMISSION` conflict pair。coverage 只证明调用方显式声明的这组
pair 由两个不同、未复用、原样复制的 UNRESOLVED hunk 承载；不证明工具自动发现了全部语义冲突，
也不证明这两条物理主张谁对谁错。

## 4. Coverage inventory

```text
selection_schema=humanize-short-patch-selection/v2
bundle_schema=humanize-short-patch/v2
coverage_schema=humanize-short-patch-coverage/v2
lexical_high_total=4
selected_spans_total=5
explicit_conflicts_total=1
mechanical_coverage_status=PASS
coverage_completion_claim_allowed=true
coverage_claim_scope=ENUMERATED_HIGH_AND_BOUND_DECLARATIONS_ONLY
semantic_completeness_claim_allowed=false
humanize_quality_claim_allowed=false
academic_correctness=NOT_EVALUATED
```

四个 AUTO high 是空重点、教练命令、泛化意义和后续铺垫。五个 selection span 包含四个实际 hunk
覆盖与一个更窄的 high/选择绑定；coverage v2 将 scanner 的确定性 high inventory、调用方选择和显式
冲突分别登记，未用一个笼统的“已覆盖”布尔值替代明细。

## 5. Apply、验证与发布状态

applicator 的父进程实际观察退出码为 `2`，这是合法的交付 REVIEW，不是崩溃：

```text
patch_application_status=PASS
structural_validation_status=PASS
unified_validator_status=PASS
hard_invariant_layer_status=PASS
style_signal_layer_status=PASS
speech_act_layer_status=PASS
paired_quality_review_status=PENDING_EXTERNAL_REVIEW
delivery_gate_status=REVIEW
delivery_gate_exit_code=2
unresolved_total=2
```

review 目录为八项闭集：source snapshot、candidate、diff、bundle、coverage、validation、result 和
manifest。候选名为 `candidate.review.tex`，没有覆盖源文件。

## 6. 独立重放

主代理在子代理停止后重新运行安装版 verifier，并绑定 live source，得到：

```text
verification_schema=humanize-short-patch-verification/v2
record_integrity_status=PASS
coverage_policy_status=PASS
coverage_replay_status=PASS
current_policy_status=MATCH
current_policy_replay_status=PASS
live_source_status=MATCH
integrity_scope=SELF_CONSISTENCY_ONLY
verifier_status=PASS
verifier_exit_code=0
candidate_delivery=REVIEW/2
```

verifier PASS 与 candidate REVIEW 同时成立：前者只证明当前 policy 下闭集可重放，后者说明两个冲突
span 和外部成对质量门仍未清除。candidate 按 `AUTO --include-protected --include-excluded` 复扫为
`finding_count=0`，这同样不是完整自然语言质量证明。

## 7. 关键工件 hash

| 工件 | SHA-256 |
|---|---|
| `selection.v2.json` | `b41d710bf4a466e72e3415658e21781020634a40d158f355a1c3a4c6fbc22338` |
| `patch.bundle.json` | `f9f109de153ef6067ab0436afb3710f729bf70201b80c1e67c194ea3ed4eb7c9` |
| `candidate.review.tex` | `fedca8f7f6abe7e6b5c4db1cf992f62887dad33ac14972efbcfc2b324b255cf9` |
| `coverage.json` 文件 | `f4a0b1708671bfdf17b9c15746fb0fcce6e624c798e252e7775b182b80a4775d` |
| `validation.json` | `ac118fae2ccf3aef7e50aa7f69278df5d563244993d636a90f11b3f27cf26497` |
| `result.json` | `ae1aedcb99b202eef271dbf54ee027bd81583a4929b13e413becd382989c88a4` |
| `evidence-manifest.json` | `b80895f44ab99424011e97711fa3722997bbb2c6634a9d3f9ec3297f96db022f` |

## 8. 可用性结论

v37 最终链能够阻止三类旧假闭环：漏列 scanner high、把 KEEP/PROTECTED/EXCLUDED span 暗中改掉、
以及在 result/verifier 摘要中丢失 coverage 的窄作用域。fresh 代理也确实根据 warning 回退并形成更
小的第二轮候选，而不是申请一个空泛豁免。

代价同样明确：手写 v2 selection 仍然冗长，hunk 与 selected span 的独立绑定会重复 source text；
未变化的 UNRESOLVED hunk 不会出现在普通 diff 中，审阅者必须同时读 bundle/coverage；终端包装层对
预期非零退出码可能显示成通用失败，因此调用方必须读取结构化 JSON 或显式保存 `$LASTEXITCODE`。
这些是下一轮 CLI/作者体验问题，不应通过放宽 hash、删除独立绑定或把 REVIEW 改成 PASS 来掩盖。

