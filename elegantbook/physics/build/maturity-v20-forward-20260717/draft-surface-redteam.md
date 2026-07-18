# DRAFT supplied-surface 门红队审计

审计日期：2026-07-17  
范围：只审计 DRAFT supplied-surface 来源门；未修改 Skill、验证器或现有测试。实验 fixture 位于 `build/maturity-v20-forward-20260717/redteam-draft-surface/`。

## 结论

存在一个可稳定复现的 DRAFT 硬失败误报：验证器把“草稿再次使用 supplied artifact 中已经出现过的同一载荷”解释成“新增未提供载荷”。真实 case 中，supplied 只出现一次 `\(R_S=0\)`，草稿在结果段和讨论段各使用一次；当前实现用 `Counter` 消耗 supplied occurrence，因而把第二次使用报成 `DRAFT_MATH_NOT_SUPPLIED`，最终错误地给出 `FAIL/1`。

该行为同时影响 code、math、formal statement、critical command、quotation、garbled span 和显式 protected term。对这七类，DRAFT 表面来源门应采用“来源载荷值集合”语义：

- 重复同一已提供载荷：不属于新载荷，表面来源门应通过；自然语言用途、重复是否得当仍留给 `semantic_source_check=NOT_EVALUATED`，交付保持 `REVIEW/2`。
- 出现任一从未提供过的载荷值：仍是硬 `FAIL/1`，保留现有 `DRAFT_*_NOT_SUPPLIED` 错误码。

不能把这一修复扩展到 REWRITE。REWRITE 的代码、公式、引语、正式环境和保护术语仍要求出现次数、内容与顺序保持，现有逐次保护必须不变。归因标记也不在本次最小修复范围；重复归因可能新增独立来源声称，维持 occurrence-sensitive 更保守。

## 合同依据

合同的措辞是一致的来源集合/子集语义，而不是 occurrence budget：

- `SKILL.md:66`：DRAFT “表面载荷门只检查新增数字、单位、数学、代码、引语、归因和显式保护术语”。
- `references/operational-contract.md:207-213`：只对“草稿中新增”的载荷作“确定性来源子集检查”；自然语言来源另置为 `NOT_EVALUATED`。
- `references/workflow.md:188-190`：表面载荷门只拦截“未提供”的载荷。
- `references/evaluation-contract.md:449-453`：只允许使用供应材料“中已有的”载荷，“新增上述载荷”为硬 FAIL。
- 验证器自己的函数注释 `validate_humanize_output.py:380-385` 也定义为拒绝 draft 中出现但 supplied “nowhere”存在的载荷。

当前实现与上述合同冲突：

- `validate_humanize_output.py:361-370` 的 `_counter_missing` 把 supplied occurrence 当成一次性额度。
- `validate_humanize_output.py:408-470` 对 code/math/formal/critical command/quotation/garbled 传入 `count_sensitive=True`。
- `validate_humanize_output.py:505-508` 对 protected term 直接做 `draft_counter - supplied_counter`。
- 同一函数中的数字/单位已经采用 source set membership，说明 DRAFT 门内存在不一致语义。

## 真实 case 复现

命令：

```powershell
python C:\Users\Lenovo\.codex\skills\humanize-academic-chinese\scripts\validate_humanize_output.py `
  build\maturity-v20-forward-20260717\cases\draft\facts.tex `
  build\maturity-v20-forward-20260717\cases\draft\output.tex `
  --mode DRAFT --scene MODELING --format json
```

实际结果：

```text
process exit                  1
delivery_gate_status         FAIL
hard_invariant_layer_status  FAIL
draft_surface_source_check   FAIL
semantic_source_check        NOT_EVALUATED
supplied math spans          5
draft math spans             6
not_supplied                 ["\\(R_S=0\\)"]
```

artifact SHA-256 与既有 `validation.json` 一致：

```text
facts.tex   4e94d11b552350290c0c7e363969c8f64c449519685a4dcab88dca8f7102e28c
output.tex  eec31d02d870742cbadb0f2e0ae045388875f59bdcbe55ef2d47c319cb461bd9
```

`facts.tex:10` 含一次 `\(R_S=0\)`；`output.tex:1` 和 `output.tex:3` 各含一次。载荷值没有新增，只有已提供值的重复使用。`validation.json:35-40` 却把 count 差额转换成 `not_supplied`。

若按合同使用 source set membership，`\(R_S=0\)` 在 supplied set 中，表面门应为 PASS；由于正文并非逐字复制，最终状态仍是 `REVIEW/2`，不会误升为 PASS。

## 七类实验

每类使用一份 supplied、一个重复同值 draft、一个新增异值 draft。当前验证器对 14 个 case 全部返回 `FAIL/1`，即没有区分重复与新增。

| 类别 | supplied 载荷 | repeat draft | new draft | repeat 当前结果 | new 当前结果 | 应采用 |
|---|---|---|---|---|---|---|
| code | `` `alpha()` `` | 同值 2 次 | `` `beta()` `` | `DRAFT_CODE_NOT_SUPPLIED` | 同错误码 | 集合来源 |
| math | `\(x=y\)` | 同值 2 次 | `\(x=z\)` | `DRAFT_MATH_NOT_SUPPLIED` | 同错误码 | 集合来源 |
| formal statement | theorem“命题甲成立” | 同 span 2 次 | theorem“命题乙成立” | `DRAFT_FORMAL_STATEMENT_NOT_SUPPLIED` | 同错误码 | 集合来源 |
| critical command | `\cite{sourceA}` | 同命令 2 次 | `\cite{sourceB}` | `DRAFT_CRITICAL_COMMAND_NOT_SUPPLIED` | 同错误码 | 集合来源 |
| quotation | `“边界保持不变”` | 同引语 2 次 | `“边界已经改变”` | `DRAFT_QUOTATION_NOT_SUPPLIED` | 同错误码 | 集合来源 |
| garbled | `�字` | 同乱码 span 2 次 | `�词` | `DRAFT_GARBLED_TEXT_NOT_SUPPLIED` | 同错误码 | 集合来源 |
| protected term | `有限元法` | 同术语 2 次 | 未供应术语 `谱方法` | `DRAFT_PROTECTED_TERM_NOT_SUPPLIED` | 同错误码 | 集合来源 |

逐类理由：

1. **Code**：重复同一 snippet 不产生新的代码字节载荷。重复是否冗余是文风/语义问题，不是 `NOT_SUPPLIED`。
2. **Math**：同一公式可以在结果与讨论中回指；真实 case 已证明 occurrence budget 会误杀正常结构。
3. **Formal statement**：同一正式 span 的重复不改变载荷来源。重复 theorem 是否造成编号或结构问题可由独立 TeX/结构检查处理，不能伪装成未供应内容。
4. **Critical command**：`\cite`、`\ref`、`\url` 的重复很常见，因此整个类别不能按次数消费。重复 `\label` 可能无效，应另设 duplicate-label/compile 诊断，而不是复用 `NOT_SUPPLIED`。
5. **Quotation**：重复逐字引语没有新增引语内容；引用用途与密度留给语义/文风复核。
6. **Garbled**：放大乱码不理想，但同一乱码值仍有供应来源。若要禁止放大，应使用独立的 garbled-repeat/skip 规则，不能错误声称载荷未供应。
7. **Protected term**：术语在学术草稿中自然需要复现。DRAFT 可省略、重排和选择详略，不应继承 REWRITE 的术语 occurrence equality。

修复后预期矩阵：所有 repeat case 的 `draft_surface_source_check=PASS`、`hard_invariant_layer_status=PASS`，在没有其他硬错误时顶层为 `REVIEW/2`；所有 new case 保持相应 `DRAFT_*_NOT_SUPPLIED`、`FAIL/1`。

## 最小兼容修复

只改变 DRAFT source lookup，不改变提取器、错误码、JSON 字段、状态映射或 REWRITE：

```python
source_set = set(source_items)
missing = [item for item in output_items if item not in source_set]
```

将 `_draft_surface_source_invariants` 中 code/math/formal/critical command/quotation/garbled 六类 checks 统一走上述逻辑，删除或停止使用 `count_sensitive` / `_counter_missing`。保留 `supplied_count` 和 `draft_count` 作为观测数据；它们不再充当供应额度。

protected term 分支同步改为：

```python
supplied_term_set = set(invariants._term_occurrences(supplied_text, terms))
draft_term_items = invariants._term_occurrences(draft_text, terms)
term_missing = [term for term in draft_term_items if term not in supplied_term_set]
```

这样，新载荷即使在 draft 中重复多次仍会硬失败；已供应载荷重复任意次数不会被误报。为最小化 schema 风险，`not_supplied` 可继续按 draft occurrence 顺序保留重复项，不必在本修复中改成唯一值列表。

不要修改：

- `check_humanize_invariants.check_documents` 的 REWRITE sequence/count 比较；
- 顶层 `semantic_source_check` 和 `REVIEW/2` 裁决；
- attribution marker 的 occurrence-sensitive 逻辑；
- 现有 `DRAFT_*_NOT_SUPPLIED` 错误码与 JSON 结构。

## 回归用例

建议在 `tests/test_validate_humanize_output.py` 增加以下真实前后 fixture/断言：

1. `test_draft_mode_allows_reuse_of_supplied_surface_payloads`：表驱动覆盖上述七类。supplied 1 次、draft 同值 2 次；断言 surface/hard layer 为 PASS、semantic 为 NOT_EVALUATED、顶层 `REVIEW`、exit 2，且无对应 `DRAFT_*_NOT_SUPPLIED`。
2. `test_draft_mode_rejects_new_surface_payload_values`：表驱动覆盖七类。draft 使用异值；断言对应错误码、surface/hard/top 为 FAIL、exit 1。
3. `test_draft_mode_real_modeling_case_reused_math_is_not_new_payload`：直接使用本次 `facts.tex`/`output.tex`；断言 `DRAFT_MATH_NOT_SUPPLIED` 消失，surface PASS、semantic NOT_EVALUATED、顶层 REVIEW/2。
4. `test_draft_mode_repeated_unsupplied_payload_still_fails`：supplied 为 `\(x=y\)`，draft 两次 `\(x=z\)`；断言仍为 `DRAFT_MATH_NOT_SUPPLIED`/FAIL，防止错误实现为“只忽略第二次”。
5. `test_rewrite_occurrence_preservation_is_unchanged`：REWRITE 中 source 1 次公式/术语、output 2 次；断言现有 `PROTECTED_MATH_CHANGED` / `PROTECTED_TERM_CHANGED` 仍硬失败。
6. 若另行处理 `\label`，增加 `test_duplicate_label_has_distinct_structural_diagnostic`，确保它不再借用 `DRAFT_CRITICAL_COMMAND_NOT_SUPPLIED`。

现有 DRAFT 测试只覆盖：普通表面通过、未供应数字、未供应归因。三项通过（`unittest`：3 tests, OK），但没有任一“已供应载荷重复”用例，也没有 DRAFT code/math/formal/command/quotation/garbled/protected-term 的成对正反 fixture。环境未安装 `pytest`，因此使用测试文件自带的 `unittest` 入口运行。

## 风险判断

严重度：P1（交付阻断型误报）。它不会放过新载荷，但会把合同允许的正常 DRAFT 组织误判为硬错误，真实 maturity-v20 case 已被阻断。修复的放宽面有限：只把“同值第二次出现”从表面硬失败移交给既有的语义 `REVIEW/2`；新值、REWRITE 漂移和语义未评估状态均不放宽。
