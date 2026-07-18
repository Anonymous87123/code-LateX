# COURSE 中文学术文风终审运行记录

## 实际配置

```text
mode=REWRITE
scene=COURSE
intensity=BALANCED
output=CLEAN
voice=SCENE_DEFAULT
report_context=NONE
source_roles=AUTO
scope=document（仅指定的 input.tex）
structure_lock=false
title_lock=true
academic_correctness=NOT_EVALUATED
```

未提供作者样本，因此使用 `SCENE_DEFAULT`，不声明保留个人声线。处理边界仅包括指定输入、Skill 正式生产资源以及本轮由输入生成的快照与验证产物；未读取既往测试输出、报告或资格材料。

## 主要动作

1. 以 UTF-8 读取 9 行、487 字节的 `input.tex`，建立独立快照；准备器识别 1 个可编辑单元和 2 个保护跨度。
2. 原样保护 `\section{判断方法}` 与完整 `equation` 环境，包括命令、空格、公式和环境边界。
3. 输入扫描定位 4 个高风险候选：`值得注意的是`、`必须牢记`、`具有重要意义`、`为后续学习奠定基础`。
4. 删除空重点壳、泛化价值判断和后续桥接；把固定教练搭配改为“公式必须记清楚”，保留原句中的“必须”及其模态强度。
5. 原样保留“若已知速度随时间减小，就可以直接套用匀变速公式”的条件判断；保留末段关于适用条件、加速度方向和条件不满足时不能直接代入的纠偏链。
6. 首轮候选因删除“必须”触发 `SPEECH_ACT_MODALITY_SCOPE_CHANGED`，状态为 `REVIEW/2`；未作豁免，修订后重新收尾并通过。
7. 未新增事实、公式、数字、题设条件、来源或结论；未评价物理内容、推导或学术正确性。

## 验证命令

输入词项扫描：

```powershell
python "C:\Users\Lenovo\.codex\skills\humanize-academic-chinese\scripts\scan_humanize_chinese.py" "D:\code LateX\elegantbook\physics\build\maturity-v7-forward-20260714\course\input.tex" --scene COURSE --format text
```

TeX 快照准备：

```powershell
python "C:\Users\Lenovo\.codex\skills\humanize-academic-chinese\scripts\prepare_humanize_long_document.py" "D:\code LateX\elegantbook\physics\build\maturity-v7-forward-20260714\course\input.tex" --output "C:\Users\Lenovo\AppData\Local\Temp\humanize-course-d93ff13786b34db989aadbff38c2d624" --scene COURSE
```

收尾与相同版本幂等复跑（同一命令执行两次）：

```powershell
python "C:\Users\Lenovo\.codex\skills\humanize-academic-chinese\scripts\finalize_humanize_long_document.py" --run-dir "C:\Users\Lenovo\AppData\Local\Temp\humanize-course-d93ff13786b34db989aadbff38c2d624" --rewrites "C:\Users\Lenovo\AppData\Local\Temp\humanize-course-d93ff13786b34db989aadbff38c2d624\rewrites"
```

交付文件统一验证：

```powershell
python "C:\Users\Lenovo\.codex\skills\humanize-academic-chinese\scripts\validate_humanize_output.py" "D:\code LateX\elegantbook\physics\build\maturity-v7-forward-20260714\course\input.tex" "D:\code LateX\elegantbook\physics\build\maturity-v7-forward-20260714\course\output.tex" --scene COURSE --format json
```

交付文件词项复扫：

```powershell
python "C:\Users\Lenovo\.codex\skills\humanize-academic-chinese\scripts\scan_humanize_chinese.py" "D:\code LateX\elegantbook\physics\build\maturity-v7-forward-20260714\course\output.tex" --scene COURSE --format text
```

## 验证结果

```text
prepare.status=READY
prepare.snapshot_id=cdb3645d942a8ff7
prepare.processable_editable_units=1
prepare.protected_spans_total=2
finalize.status=PASS
finalize.exit_code=0
finalize.full_completion_claim_allowed=true
finalize.idempotency=PASS
finalize.full_format_errors=[]
validator.delivery_gate_status=PASS
validator.delivery_gate_exit_code=0
validator.hard_invariant_layer_status=PASS
validator.speech_act_layer_status=PASS
validator.style_signal_layer_status=PASS
validator.before_candidates=4
validator.after_candidates=0
validator.introduced_candidates=0
validator.warnings=0
output_scan.candidates=0
unresolved=0
```

正式 TeX 编译为 `NOT_RUN`：输入是没有导言区和 `\documentclass` 的片段，未指定可用于该派生片段的项目编译命令。收尾器的 TeX 结构与保护检查为 `PASS`，但这里不把它表述为编译通过。

## 机器状态

```text
time=2026-07-14T20:55:41.5126641+08:00
host=LAPTOP-P1JTH4QP
os=Microsoft Windows 10.0.26100
architecture=X64
powershell=5.1.26100.3624
python=3.13.7
cwd=D:\code LateX\elegantbook\physics
run_dir=C:\Users\Lenovo\AppData\Local\Temp\humanize-course-d93ff13786b34db989aadbff38c2d624
input_bytes=487
input_sha256=9805eab8480836f942078c112dfcd4160c293cd18bfd79ae0e308c02db956b65
output_bytes=400
output_sha256=ea903cd3d0f37d7c7eb3d9fa8bf96e25ea02863c1b23e500ec6f25640743cb55
source_files_modified_by_finalizer=0
```
