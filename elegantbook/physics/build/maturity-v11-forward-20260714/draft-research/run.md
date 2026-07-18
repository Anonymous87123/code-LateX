# 运行记录

- `status`: `REVIEW`
- `delivery_gate_status`: `REVIEW`
- `process_exit_code`: `2`
- `mode`: `DRAFT`
- `scene`: `RESEARCH`
- `intensity`: `BALANCED`
- `output`: `CLEAN`
- `voice_profile`: `scene-default`
- `report_context`: `NONE`
- `scope`: `selection`

## 所用动作卡

- `RESEARCH-EVIDENCE-01`：区分“总量硬锚点校准”、局地一致性检验和独立外部验证三个证据角色。
- `RESEARCH-SCOPE-01`：保留 $\mathrm{CPUE}^*$ 未进入目标函数、仅用于校准后局地一致性检验的范围。

动作卡只用于组织输入信息，没有迁移来源事实、变量、数值或措辞。

## 事实边界

- 正文只使用 `input.md` 已给出的总量硬锚点、局地口径、$\mathrm{CPUE}^*$ 的用途与证据层级、底层资源末值、食压指数及二者同时出现的结果。
- 保留 10 处数字项、2 处 TeX 数学标记及 2 处直接引语；保留“没有进入目标函数”“只用于”“不能称为独立外部验证”的否定和范围限定。
- 未补造因果机制、统计检验、来源、管理含义、未来工作或其他事实。

## 验证与未评估项

- 统一验证器：`hard_invariant_layer_status=PASS`，`speech_act_layer_status=REVIEW`，`style_signal_layer_status=PASS`，故 `保护检查=REVIEW`，退出码为 `2`。
- 待复核项：`SPEECH_ACT_NEGATION_CHANGED`。输入中的写作边界项含“不提供……”等元指令；按 `CLEAN` 正文要求未把该元指令写入研究段落。本地流程未提交 warning proposal，也没有外部 `VERIFIED_HUMAN` clearance。
- 词项扫描器退出码为 `0`，改后正文没有扫描候选；该结果不覆盖统一验证器的 `REVIEW`。
- `academic_correctness=NOT_EVALUATED`。计算准确性、数据来源、因果机制、显著性检验、管理含义和未来工作均未评估。
