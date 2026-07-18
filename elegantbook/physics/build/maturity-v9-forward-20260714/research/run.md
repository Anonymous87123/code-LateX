# Humanize 运行记录

## 配置

```yaml
mode: REWRITE
scene: RESEARCH
intensity: BALANCED
output: CLEAN
voice: SCENE_DEFAULT
report_context: NONE
scope: 完整输入
locked_structure: 标题、章节顺序与两段结果讨论骨架
protected_counts: 0
corpus_action: RESEARCH-SCOPE-01
unresolved_locations: []
```

未提供作者样本，因此使用 `voice=SCENE_DEFAULT`，不声明保留个人声线。

## 文风决策

- 输入扫描：5 个候选，其中 high 3 个、medium 2 个。
- 删除空泛意义宣告“具有重要意义”和空重点壳“值得注意的是”。
- 删除“系统梳理—深入探讨—为后续研究奠定基础”的作者动作与强制桥接链；未以近义套话替换。
- 保留当前实验设置、两组比较、采样方法未变、额外测量缺失，以及尚不能区分两种可能原因的主张范围。
- `RESEARCH-SCOPE-01` 输入锚点：当前实验设置、两组数据、现有结果的因果区分边界。
- 谓词来源关系仅使用 `COPY`、`ENTAILED_PARAPHRASE` 和 `DELETE_STYLE_SHELL`；未新增事实、数字、来源、机制或未来工作。

## 验证轨迹

首次候选验证结果：

```yaml
status: REVIEW
delivery_gate_status: REVIEW
exit_code: 2
hard_invariant_layer_status: PASS
speech_act_layer_status: REVIEW
style_signal_layer_status: PASS
warning: SPEECH_ACT_MODALITY_SCOPE_CHANGED
warning_fingerprint: f9242e0bf86bd0f22211ef69736fa219152b3e1ddf5ca2cd13368ba2baa24876
warning_review_request_sha256: 25c761b4420574b06014bc7fada775149da999751c6ba400c1ac1914886444e6
```

该候选删除元话语时一并移除了原文中的“可能”模态。未提交本地 warning proposal，也未把 `REVIEW` 降格为 `PASS`。修订仅将该模态收回余留问题，写为“波动的可能原因是边界条件还是初始状态”，随后对精确新版本重新验证。

最终验证结果：

```yaml
status: PASS
delivery_gate_status: PASS
exit_code: 0
hard_invariant_layer_status: PASS
speech_act_layer_status: PASS
style_signal_layer_status: PASS
academic_correctness: NOT_EVALUATED
before_sha256: 348026b7b26c646e67e809285ea11881865a3d35193a4131ff850813582c4d71
after_sha256: 103e7f5e892174f11591369346ae9e5ea02b2260c9b64ef2b5ed1ae62690576b
before_candidates: 5
after_candidates: 0
introduced_candidates: 0
unexplained_high_candidates: 0
pending_warnings: 0
```

改后词项复扫无候选；高风险快检未见空重点壳、营销拔高、学术包装链、强制桥接、自动展望或新增修复模板。保护检查=`PASS`，只表示统一验证器对上述精确前后版本以退出码 0 完成；未运行学术正确性、证据、来源、实验或结论质量评估。
