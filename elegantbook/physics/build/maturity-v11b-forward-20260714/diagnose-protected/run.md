# 运行记录

## 配置与范围

```yaml
mode: DIAGNOSE
intensity: BALANCED
output: ANNOTATED
scene: RESEARCH
voice_profile: scene-default
report_context: NONE
scope: input.md 全文件
protected_audit: RUN
excluded_audit: RUN
unified_rewrite_validator: NOT_RUN
```

本次只读取并诊断 `build/maturity-v11b-forward-20260714/diagnose-protected/input.md`。未读取其他 build、tests、历史报告或资格材料。扫描范围为单个完整文件，不是抽样。

## 实际扫描命令

文本审计视图：

```powershell
python 'C:\Users\Lenovo\.codex\skills\humanize-academic-chinese\scripts\scan_humanize_chinese.py' 'D:\code LateX\elegantbook\physics\build\maturity-v11b-forward-20260714\diagnose-protected\input.md' --scene AUTO --format text --include-protected --include-excluded
```

JSON 覆盖视图：

```powershell
python 'C:\Users\Lenovo\.codex\skills\humanize-academic-chinese\scripts\scan_humanize_chinese.py' 'D:\code LateX\elegantbook\physics\build\maturity-v11b-forward-20260714\diagnose-protected\input.md' --scene AUTO --format json --include-protected --include-excluded
```

## 状态与计数

- 两次扫描进程退出码：`0`。
- 扫描覆盖状态：`PASS`；`requested_count=1`，`scanned_count=1`，`skipped_count=0`。
- `finding_count=4`，`candidate_count=1`。
- 作者正文候选命中：1；quoted/protected 命中：3；excluded 命中：0。
- protected 命中均保留为 `KEEP/protected`，未进入作者正文病灶计数。
- `DG-01`：`PASS`，正文未改，交付中无改写完成态声明。
- `DG-02`：`PASS`，已披露完整单文件覆盖与审计计数。
- `DG-03`：`PASS`，作者正文单一位置按 `Local` 处理，未把 scanner 的 `high` 映射为覆盖严重度。
- `DG-04`：`PASS`，命中经来源角色与上下文裁决；引语命中未被判作作者模板。
- `DG-05`：`PASS`，输出使用固定九列表头并披露 protected/excluded 审计结果。

`--scene AUTO` 用于扫描全部词项信号；结合访谈研究语境，诊断表的文档场景裁决为 `RESEARCH`。扫描结果仅作为上下文候选，不用于作者身份或概率判断。

## 未评估项

- `academic_correctness=NOT_EVALUATED`。
- 事实真伪、访谈材料真实性、证据质量、引文与来源准确性：`NOT_EVALUATED`。
- 作者身份、AIGC 概率、检测分数及检测规避效果：`NOT_EVALUATED`。
- 统一改写验证器：`NOT_RUN`；本任务没有改后正文，因此不声明“保护检查=PASS”。本记录中的 `PASS` 仅指扫描覆盖或对应的 DIAGNOSE 门。
- 作者个人声线：未提供样本，使用 `voice=SCENE_DEFAULT`，不声称保留或识别了个人声线。
