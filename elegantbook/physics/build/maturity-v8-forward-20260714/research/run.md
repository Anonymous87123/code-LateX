# Humanize 运行记录

- 运行时间：2026-07-14 21:14:21 +08:00
- 输入：`D:\code LateX\elegantbook\physics\build\maturity-v7-forward-20260714\research\input.md`
- 输出：`D:\code LateX\elegantbook\physics\build\maturity-v8-forward-20260714\research\output.md`
- 输入 SHA-256：`348026b7b26c646e67e809285ea11881865a3d35193a4131ff850813582c4d71`
- 输出 SHA-256：`3b466d44ae3608b28b9ea55d179d47d40a3e16b8f1bb3c1688c4eaebd349663b`

## 配置

```text
mode=REWRITE
scene=RESEARCH
intensity=BALANCED
output=CLEAN
voice=SCENE_DEFAULT
report_context=NONE
scope=完整输入
title_lock=true
structure_lock=false（受 BALANCED 权限约束）
```

未提供作者样本，使用 `SCENE_DEFAULT`，不作个人声线保留声明。输入中没有引语、题干、OCR、代码、数学或 TeX 保护跨度；数字、术语、否定、模态、观察和结果报告状态按语义不变量处理。

## 改写动作

- 保留标题、段落顺序、两组比较、峰值与波动观察。
- 保留采样方法未改变、没有额外测量以及两类原因尚不能区分的限定。
- 删除无具体信息增量的意义拔高、重点提示、学术包装和后续研究桥接。
- 决策计数：`KEEP=5`，`DELETE_STYLE_SHELL=2`，`UNRESOLVED=0`。

## 实际运行

1. 改前词项扫描

```powershell
python C:\Users\Lenovo\.codex\skills\humanize-academic-chinese\scripts\scan_humanize_chinese.py D:\code LateX\elegantbook\physics\build\maturity-v7-forward-20260714\research\input.md --scene RESEARCH --format text
```

进程退出码：`0`。扫描得到 5 个上下文候选：`LEX-MARKET-01` 1 个、`LEX-EMPH-01` 1 个、`LEX-ACADEMIC-PACKAGE-01` 2 个、`LEX-FOUNDATION-01` 1 个。候选仅用于文风定位。

2. 统一验证器

```powershell
python C:\Users\Lenovo\.codex\skills\humanize-academic-chinese\scripts\validate_humanize_output.py D:\code LateX\elegantbook\physics\build\maturity-v7-forward-20260714\research\input.md D:\code LateX\elegantbook\physics\build\maturity-v8-forward-20260714\research\output.md --scene RESEARCH --format json
```

真实进程退出码：`2`。

```text
status=REVIEW
delivery_gate_status=REVIEW
delivery_gate_exit_code=2
hard_invariant_layer_status=PASS
speech_act_layer_status=REVIEW
style_signal_layer_status=PASS
academic_correctness=NOT_EVALUATED
```

词项层统计：改前候选 `5`，改后候选 `0`，新增候选 `0`，未解释 high 候选 `0`。

待复核 warning：

```text
code=SPEECH_ACT_MODALITY_SCOPE_CHANGED
category=modality_scope
before={只: 1, 可能: 1}
after={只: 1}
warning_fingerprint=f9242e0bf86bd0f22211ef69736fa219152b3e1ddf5ca2cd13368ba2baa24876
warning_review_request_sha256=b54c4248a32efa74e32aa3acae01ba8b6021b255b2f22b741275196df1e0fd2d
```

该 warning 来自删除的元话语中含有“可能”这一模态标记。未提交 warning resolution proposal；`reviewer_kind=NONE`、`identity_verified=false`、`review_clearance_granted=false`。按统一验证器顶层状态保留 `REVIEW/2`，不以硬不变量层的 `PASS` 覆盖最终裁决。

3. 改后词项扫描

```powershell
python C:\Users\Lenovo\.codex\skills\humanize-academic-chinese\scripts\scan_humanize_chinese.py D:\code LateX\elegantbook\physics\build\maturity-v8-forward-20260714\research\output.md --scene RESEARCH --format text
```

进程退出码：`0`。没有词项候选。

4. 高风险短语上下文快检

对 Skill 列出的空重点壳、教练腔、营销拔高、泛化意义、学术包装、强制桥接、自动展望和修复模板执行精确短语复扫，结果为 `NO_MATCH`。该步骤是模型自检，不是人工复核。

## 交付状态

`保护检查=REVIEW`，最终状态为 `REVIEW/2`。硬不变量层通过，文风信号层通过；言语行为层存在上述待复核 warning。未运行学术正确性、来源、证据、实验或结论质量审查。
