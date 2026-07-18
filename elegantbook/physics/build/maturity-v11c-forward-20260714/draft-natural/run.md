# 起草运行记录

## 实际配置

- `mode=DRAFT`
- `scene=RESEARCH`
- `intensity=BALANCED`（仅控制材料组织幅度）
- `output=CLEAN`
- `voice=SCENE_DEFAULT`（未提供作者样本）
- `report_context=NONE`
- `scope=根据 input.md 的写作要点形成可直接放入“结果与讨论”小节的段落组`
- `corpus_action_support=ACTION_CARDS`
- 场景动作锚：`RESEARCH-EVIDENCE-01`、`RESEARCH-SCOPE-01`；仅用于区分校准、一致性检验与独立验证，并使结论继承已给口径，不提供新的事实或措辞。

## 材料分类与实际采用内容

### `FACT_PAYLOAD`

- 2025 年四大家鱼总量的 1.800 倍题面硬锚点、1.805 倍校准结果及 0.26% 相对误差。
- 湖北段单网次捕获量提升 120%、局地口径 2.200 倍、模型 $\mathrm{CPUE}^*$ 为 1.838 倍及 16.47% 相对误差。
- $\mathrm{CPUE}^*$ 没有进入目标函数，只用于校准后的局地一致性检验，不能称为独立外部验证。
- 底层资源末值为初值的 0.204 倍，食压指数由初值附近升至 4.213 倍。
- 鱼群恢复与底层资源承压同时出现。

### `EDITORIAL_REQUIREMENT`

- 将“总量硬锚点校准”与“局地一致性检验”分开组织；该动作要求已由段落分工落实，未作为后台指令写入正文。

### `FACT_BOUNDARY`

- 不补原因或额外因果机制。
- 不补统计检验、来源、管理含义、未来工作或其他事实。
- 输入不足以支持的解释均省略，不以套话或占位扩充。

## 来源与验证状态

- `status=REVIEW`
- `delivery_gate_status=REVIEW`
- `validator_process_exit_code=2`
- `draft_surface_source_check=PASS`
- `hard_invariant_layer_status=PASS`
- `speech_act_layer_status=PASS`
- `style_signal_layer_status=PASS`
- `semantic_source_check=NOT_EVALUATED`
- `academic_correctness=NOT_EVALUATED`
- 改后词项复扫：退出码 0；`after_candidates=0`，`introduced_candidates=0`，`unexplained_high_candidates=0`。
- 输入 SHA-256：`f4c9c5fa3ea976a6cc49cb077f498c61cf7ba1584710e73323df45c078532f78`
- 输出 SHA-256：`4b51e19aa372a617a82dc3a2c1d325285b87a0e41dd3be86b3d70118bffde26a`

未发现已编码的表面新增载荷，语义来源待复核。统一验证器没有评估事实、引文、计算、因果或学术正确性；因此最终状态按合同保持 `REVIEW/2`，不将表面来源检查的 `PASS` 扩大为内容层结论。
