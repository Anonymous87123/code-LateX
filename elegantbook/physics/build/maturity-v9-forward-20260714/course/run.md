# 运行记录

## 配置

```yaml
mode: REWRITE
scene: COURSE
intensity: BALANCED
output: CLEAN
voice: SCENE_DEFAULT
report_context: NONE
scope: 完整 input.tex（10 行，487 字节）
structure_lock: 章节标题及层级不变
academic_correctness: NOT_EVALUATED
```

未提供作者样本，因此使用 `voice=SCENE_DEFAULT`，不声明保留个人声线。

## 输入与保护范围

- 输入：`build/maturity-v7-forward-20260714/course/input.tex`
- 输入 SHA-256：`9805eab8480836f942078c112dfcd4160c293cd18bfd79ae0e308c02db956b65`
- 保护范围：章节标题及 TeX 命令、`equation` 环境与公式源码。
- 输出：`build/maturity-v9-forward-20260714/course/output.tex`
- 输出 SHA-256：`6bc3cebbd0a570c33aafd0aa5fd1463e557fa3e8b24c96f415b742b868fe2861`

## 改写决策

- 语料动作锚：`COURSE-ERROR-01`。输入已包含“只看公式形式”的具体误读，以及“先检查匀变速条件和加速度方向”的对应纠正。
- `DELETE_STYLE_SHELL`：删除 2 个只承担强调、教练动员、价值宣告或后续桥接功能的句子。
- `COPY`：保留 3 个承载条件、模态和纠偏动作的正文句子。
- 未新增公式、数字、条件、结论、来源或学习动作。

词项扫描结果：

- 改前：4 个 high 候选，分别为 `值得注意的是`、`必须牢记`、`具有重要意义`、`为后续学习奠定基础`。
- 改后：0 个候选。
- 新增候选：0。
- 未解释 high 候选：0。

## 验证结果

```yaml
status: REVIEW
delivery_gate_status: REVIEW
process_exit_code: 2
hard_invariant_layer_status: PASS
speech_act_layer_status: REVIEW
style_signal_layer_status: PASS
academic_correctness: NOT_EVALUATED
```

统一验证器已对上述精确前后版本运行。硬不变量未失败；章节标题、公式、数字、TeX 结构、否定、条件和保留句中的模态未发生漂移。

待复核项：删除空泛教练句“遇到这类题目时必须牢记公式”后，`必须` 的计数由 1 变为 0，触发 `SPEECH_ACT_MODALITY_SCOPE_CHANGED`。该句按 `COURSE` 规则整体删除，不改写为“务必记住”等同义教练句，因此如实保留 `REVIEW/2`。

- warning fingerprint：`3d6081e35699725d4e53ec47f876096ff675debf1e18383a8ecb42d507841044`
- warning review request SHA-256：`63b5632ba3d3920e79316afab9bcc306f8549d58c0e5b1a70cc49c4999cebb7e`
- 本地 warning proposal：未提交。
- 人工审批或外部 `VERIFIED_HUMAN` clearance：未提供。

最终裁决：`REVIEW`。这不表示硬保护失败，也不构成学术内容正确性结论。
