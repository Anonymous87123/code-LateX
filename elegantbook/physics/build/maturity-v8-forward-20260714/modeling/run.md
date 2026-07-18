# Humanize Academic Chinese 运行记录

运行时间：`2026-07-14T21:16:25.9971323+08:00`

## 配置

```yaml
mode: REWRITE
scene: MODELING
intensity: BALANCED
output: CLEAN
voice: SCENE_DEFAULT
report_context: NONE
scope: 完整 input.md
locked_structure: no
title_lock: true
protected_roles: math, numbers, units, result-report status, modality
```

未提供作者样本，因此使用 `voice=SCENE_DEFAULT`，不声明保留个人声线。

## 输入与输出

```yaml
before_path: D:\code LateX\elegantbook\physics\build\maturity-v7-forward-20260714\modeling\input.md
before_sha256: 71f58df11175b1419c455a142878492642c5ee8cfe6fd3bfffd5fcc45adb0f45
after_path: D:\code LateX\elegantbook\physics\build\maturity-v8-forward-20260714\modeling\output.md
after_sha256: 2bda262c6a6d006f56b029fbdcbba63b0fa54f1157250b11afaeb7799fae1b46
document_format: markdown
```

正文写入后未再修改；统一验证器针对上述精确 SHA-256 版本运行。

## 改写动作

- 删除无信息的章节路线预告、`首先` 和 `进一步而言`。
- 将“表格的作用在于”压缩为直接用途陈述；“正文里要保留”仍保持要求状态，没有改写成表格已经列出数据。
- 保留温度响应模型、参数扫描范围、误差与计算时间的取舍，以及“结果表明”的报告状态。
- 删除空重点壳、营销拔高、完整闭环和泛化工程支撑。
- 将同一命题上的多重缓和压缩为一个 `可能`，没有新增程度判断。
- 删除没有具体对象的自动展望，正文停在传感器漂移这一已给限制。

谓词来源门使用 `COPY`、`ENTAILED_PARAPHRASE` 和 `DELETE_STYLE_SHELL`；未引入新谓词、工程采用事实、数字、公式、来源或未来工作。

## 保护核对

- 4 个内联数学跨度逐字保留：`$R(T)=aT+b$`、`$a$`、`$[0.8,1.2]$`、`$a=1.06$`。
- 7 个非数学数字/单位组合保留：`20 ℃`、`25 ℃`、`30 ℃`、`8.1%`、`5.4%`、`31 s`、`44 s`。
- `结果表明` 的言语行为保留；传感器漂移命题仍保留可能性模态。

## 词项扫描

初始扫描命令：

```powershell
python C:\Users\Lenovo\.codex\skills\humanize-academic-chinese\scripts\scan_humanize_chinese.py D:\code LateX\elegantbook\physics\build\maturity-v7-forward-20260714\modeling\input.md --scene MODELING --format text
```

初始扫描退出码为 `0`，共返回 11 个上下文候选：`LEX-OUTLINE-01` 1 个、`LEX-META-01` 2 个、`LEX-EMPH-01` 1 个、`LEX-MARKET-01` 2 个、`LEX-MGMT-01` 1 个、`LEX-HEDGE-01` 3 个、`LEX-FUTURE-01` 1 个。

改后复扫使用同一脚本与 `--scene MODELING --format text`，退出码为 `0`，未返回候选。模型上下文快检未发现空重点壳、教练腔、营销拔高、泛化意义、学术包装成束、管理闭环、强制桥接、自动展望、多重缓和或批量修复模板。该项是模型自检，不是人工复核。

## 统一验证

```powershell
python C:\Users\Lenovo\.codex\skills\humanize-academic-chinese\scripts\validate_humanize_output.py D:\code LateX\elegantbook\physics\build\maturity-v7-forward-20260714\modeling\input.md D:\code LateX\elegantbook\physics\build\maturity-v8-forward-20260714\modeling\output.md --scene MODELING --format json
```

```yaml
status: REVIEW
delivery_gate_status: REVIEW
process_exit_code: 2
delivery_gate_exit_code: 2
hard_invariant_layer_status: PASS
speech_act_layer_status: REVIEW
style_signal_layer_status: PASS
academic_correctness: NOT_EVALUATED
before_candidates: 11
after_candidates: 0
introduced_candidates: 0
unexplained_high_candidates: 0
accepted_warnings: 0
pending_warnings: 2
```

待复核 warning：

1. `SPEECH_ACT_NEGATION_CHANGED`
   - fingerprint: `0d7d4a1b4a655e0c9953f595d1830fce0072499b5ef355dac9bf5dcab8fd1e50`
   - before: `不=1`；after: 无。
   - 来源：删除“该模型不仅全面提升……”所在的营销/闭环句后，验证器按否定标记计数发现变化。
2. `SPEECH_ACT_MODALITY_SCOPE_CHANGED`
   - fingerprint: `69b8330e709a3b97a4ce4dd891d3e8b3b641b4ea8a6ebb4dd05926e69149a0de`
   - before: `仅=1, 可以=1, 可能=1, 或许=1`；after: `可能=1`。
   - 来源：`仅` 位于“不仅”，`可以` 位于已删除的泛化展望；传感器漂移命题的 `可能/或许/在一定程度上` 被压缩为一个 `可能`。

验证器生成的 warning review request：

```yaml
request_sha256: 31e316df093649a2d24407ed0dddf3d4f35d7d202d460ff1abd0888fadafa7bc
warning_proposals_submitted: false
reviewer_kind: NONE
identity_verified: false
review_clearance_granted: false
attestation_status: NOT_PROVIDED
```

未为追逐状态反复同义替换，也未提交本地 `HUMAN` 声明或 warning proposal。最终交付门如实保持 `REVIEW/2`；硬不变量层 `PASS` 不覆盖该裁决。

## 未解决项

- 验证器保留上述两条言语行为 warning，需外部人工结合语义范围复核。
- 未运行学术正确性、证据、来源、公式推导或实验质量检查。
