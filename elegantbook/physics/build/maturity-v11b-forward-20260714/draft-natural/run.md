# 运行记录

- `mode=DRAFT`
- `scene=RESEARCH`
- `intensity=BALANCED`（仅控制材料组织幅度）
- `output=CLEAN`
- `voice=SCENE_DEFAULT`（未提供作者样本）
- `report_context=NONE`
- `scope=section`
- `corpus_action_support=ACTION_CARDS`
- 采用的抽象动作卡：`RESEARCH-EVIDENCE-01`、`RESEARCH-ROLE-01`。两张卡仅用于区分校准、一致性检验、独立验证以及硬锚点与内部局地指标的角色；未读取或迁移来源语料中的事实、数值或措辞。

## 来源检查状态

- 统一验证器：`delivery_gate_status=REVIEW`，进程退出码 `2`。
- `draft_surface_source_check=PASS`：未发现已编码的表面新增载荷。
- `semantic_source_check=NOT_EVALUATED`：自然语言分句的语义来源待复核，不能据此声明“未补造已验证”。
- `hard_invariant_layer_status=PASS`
- `speech_act_layer_status=PASS`
- `style_signal_layer_status=PASS`
- 改后词项复扫退出码为 `0`；`after_candidates=0`，`introduced_candidates=0`，`unexplained_high_candidates=0`。
- 输入 SHA-256：`f4c9c5fa3ea976a6cc49cb077f498c61cf7ba1584710e73323df45c078532f78`
- 输出 SHA-256：`9caefc8275a150cfbb9721eaf07f5c86693f519d3ff2910ff99023224d871b01`

## 事实边界

正文只组织输入给出的年份、对象、倍数、百分比、数学标记、口径层级、指标角色、否定与结论范围。未加入额外因果机制、统计检验、资料来源、管理含义、未来工作或其他事实；材料未提供的解释予以省略。

## 未评估项

- 自然语言分句的完整语义蕴含关系：`NOT_EVALUATED`
- 学术内容正确性：`NOT_EVALUATED`
- 事实真伪、资料来源、计算与统计有效性、因果机制和研究价值：`NOT_EVALUATED`

未解决状态：`semantic_source_not_evaluated`；除此之外，统一验证器未报告硬不变量错误或言语行为、文风信号警告。
