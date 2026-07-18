# REPORT_INFORMED selection 范围红队

## 结论

v20 修复前，提取器能把报告标注唯一映射到源文，但统一验证器不读取 `report_scope.json`。因此，“映射范围正确”与“改后只动该范围”之间没有机器绑定。红队在唯一 selection 外改写首段，同时把 selection 本身换成合格候选；旧验证器返回 `PASS/0`。这是可复现的虚假定点完成态。

修复后，统一验证器新增 `--report-scope`：校验提取器 `PASS/0`、schema/operation，并从 JSON 记录的绝对 `report_path` 重新静态解析报告；report SHA、coverage 和 fragments 必须逐字段重放一致。随后再校验精确 source SHA-256、全部 fragment 的 `UNIQUE/source_occurrences=1/source_start/source_end/normalized_text`，以及改后文本能否由这些区间的替换形成。相邻或重叠区间先合并，多 selection 之间的不可编辑文本、首部和尾部必须逐字保留。

## 攻击样本

源文与报告：

- `cases/report-informed/source.md`
- `cases/report-informed/report_scope.json`
- 唯一可编辑区间：字符 `116--281`，源文第 5 行

恶意稿 `redteam-report-scope/malicious-after.md` 同时执行两处变化：

1. 合法范围内：改写第 5 行 selection；
2. 非法范围外：把第 3 行末句从“这些都是好的学术表达习惯”改成“这些做法体现了较成熟的学术表达习惯”。

旧命令未携带 scope：

```powershell
python validate_humanize_output.py source.md malicious-after.md --scene GENERAL --format json
```

旧结果：

```text
delivery_gate_status=PASS
exit_code=0
hard_invariant_layer_status=PASS
speech_act_layer_status=PASS
style_signal_layer_status=PASS
```

这只能证明普通 REWRITE 门未发现漂移，不能证明报告 selection 被遵守。

## 修复后复现

```powershell
python validate_humanize_output.py source.md malicious-after.md `
  --scene GENERAL `
  --report-scope report_scope.json `
  --format json
```

结果保存在 `redteam-report-scope/malicious-validation-v20-fixed.json`：

```text
delivery_gate_status=FAIL
exit_code=1
hard_invariant_layer_status=FAIL
report_scope_check=FAIL
outside_selection_unchanged=false
error=REPORT_SCOPE_OUTSIDE_SELECTION_CHANGED
```

同一门对合法 `cases/report-informed/output.md` 返回：

```text
delivery_gate_status=PASS
exit_code=0
report_scope_check=PASS
outside_selection_unchanged=true
```

## 失败关闭边界

以下输入不会进入范围 PASS：

- extractor 状态不是 `PASS/0`；
- scope JSON 的 report SHA、coverage 或 fragments 与原报告静态重放不一致；
- JSON schema 或 operation 不匹配；
- `source_sha256` 与当前 before 字节不一致；
- 任一 fragment 缺失、歧义、非 `UNIQUE` 或 source occurrence 不为 1；
- 区间越界、空区间或区间切片的规范化文本与 fragment 不一致；
- selection 外前缀、区间间文本或后缀发生变化；
- `DRAFT` 或 fragment validation 试图绑定 report scope。

本门只证明范围遵守，不证明检测率变化、作者身份、学术正确性或改后质量；后者仍由普通不变量、言语行为、词项复扫和成对质量门分别处理。
