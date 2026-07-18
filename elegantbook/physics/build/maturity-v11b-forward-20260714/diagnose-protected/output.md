# 纯文风诊断

配置：`mode=DIAGNOSE`，`scene=RESEARCH`，`intensity=BALANCED`（本模式不执行改写），`output=ANNOTATED`，`voice=SCENE_DEFAULT`，`report_context=NONE`。

## 覆盖摘要

- 覆盖范围：`input.md` 全文件；请求 1 个文件，实际扫描 1 个，跳过 0 个。
- 计数口径：下列作者正文、quoted/protected 与 excluded 数量均指扫描器 `findings` 命中数，不是句子数或字符数。
- 作者正文：1 个候选命中，位于第 3 行引语外的句首。
- quoted/protected：3 个命中，均为 `KEEP/protected`；第 1 行直接引语内 2 个，第 3 行内嵌引语内 1 个。
- excluded：0 个命中。
- 扫描合计：4 个命中；进入作者正文病灶表的 occurrence 为 1 个。

## ANNOTATED 诊断表

| Severity | Location | Source role | Scene | Signal/Pathology | Trigger | Reading effect | Decision | Action |
|---|---|---|---|---|---|---|---|---|
| Local | `input.md:3:1`；作者正文 occurrence 1/1 | author | RESEARCH | `LEX-EMPH-01` / 空转的重点提示句壳 | 引语外句首“值得注意的是”出现 1 次；同句已经用“在访谈中出现了三次”报告具体观察。引语中的同词不计入作者模板复用。 | 提示壳先行，使读者先接收抽象强调，再接收真正承载重点的访谈次数，句首多出一层报幕。 | REWRITE | 后续若改写，仅处理引语外的句首提示壳，让访谈出现次数直接承担重点；两处引语均保持原样。 |

## 保护与排除审计

- `input.md:1` 的直接引语“值得注意的是，本研究具有重要意义。”属于 `quoted/protected`；其中 `LEX-EMPH-01` 与 `LEX-MARKET-01` 各命中 1 次，决策均为 `KEEP/protected`，不构成作者正文病灶，也不建议修改。
- `input.md:3` 的内嵌引语“本研究具有重要意义”属于 `quoted/protected`；其中 `LEX-MARKET-01` 命中 1 次，决策为 `KEEP/protected`，不构成作者模板，也不建议修改。
- 未发现 excluded 命中。
- 扫描器的 `high` 是词项风险标签，不是覆盖严重度；表中使用 `Local`，因为该病灶在作者正文中只有一个位置。

已完成纯文风诊断；未修改正文。覆盖=`input.md` 全文件，未覆盖=无。
