# 运行记录

```yaml
mode: REWRITE
scene: MODELING
intensity: BALANCED
output: CLEAN
voice: SCENE_DEFAULT
voice_profile: scene-default
report_context: NONE
scope: 完整输入
structure_lock: false
title_lock: true
corpus_action: NONE_APPLICABLE
protected_counts:
  math_tex_spans: 4
  numeric_unit_spans: 7
decision_counts:
  KEEP: 4
  DELETE: 5
  REWRITE: 1
  UNRESOLVED: 1
unresolved_locations:
  - 第 1 段第 2 句：原文是正文与表格的编辑要求，不能在缺少已完成表格或正文锚点时改成完成事实；为避免同义轮换，原句保留。
status: REVIEW
delivery_gate_status: REVIEW
exit_code: 2
hard_invariant_layer_status: PASS
speech_act_layer_status: REVIEW
style_signal_layer_status: REVIEW
academic_correctness: NOT_EVALUATED
before_sha256: 71f58df11175b1419c455a142878492642c5ee8cfe6fd3bfffd5fcc45adb0f45
after_sha256: 36ce6c14bc7efc2e0811e15b79e9efcada290828e4b6b1d43cd10a833b727977
warning_review_request_sha256: e2fb27bae228757c3ca502d45fc2914d28fc80ab2ad59e7c80d3d8e73e19743d
warning_reviewer_kind: NONE
warning_review_clearance_granted: false
```

## 主要动作

- 删除路线预告、顺序路标、空泛拔高、管理式“闭环”表述和自动展望。
- 保留公式、变量、参数范围、三组温度数据、误差、计算时间、单位及“结果表明”的报告状态。
- 将同一命题上的多重缓和压缩为一个“可能”，未新增程度判断。
- 结果停在验证集误差与计算时间的取舍，不补写采用、部署或工程决策后果。

## 验证结果

统一验证器对交付对应的精确前后版本实际运行，进程退出码为 `2`。顶层 `status` 与 `delivery_gate_status` 均为 `REVIEW`；`hard_invariant_layer_status=PASS` 仅表示已编码的硬保护项未失败，不覆盖以下待复核项：

- `SPEECH_ACT_MODALITY_SCOPE_CHANGED`：删除泛化展望并把“可能/在一定程度上/或许”压缩为一个“可能”后，模态词计数变化。warning fingerprint：`90605dee314deb541dabcb0326363e52167317d9de1a45488809dbb6a537cd29`。
- `LEX-META-01/high` 两处：`表格的作用在于`、`正文里要`。这两处因不能安全升级为已完成事实而保留，故 `style_signal_layer_status=REVIEW`。

改后词项复扫显示 `after_candidates=2`、`introduced_candidates=0`、`unexplained_high_candidates=2`。未提交本地 warning proposal，未声称人工复核或外部 clearance；未运行学术正确性、证据、计算或实验质控。
