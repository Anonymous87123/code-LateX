# Humanize 运行记录

- 配置：`mode=REWRITE`，`scene=COURSE`，`intensity=BALANCED`，长文交付使用 `PATCH` 证据，`voice=SCENE_DEFAULT`，`report_context=NONE`。未提供作者样本，不声称复现个人文风。
- 源文件：`D:\code LateX\elegantbook\cet6\test.tex`。严格 UTF-8 可读，430 行，无替换字符或乱码跳过；快照 SHA-256 为 `55a8e3e331b9e71a2e57cc7973d3e1d3813774557086a6d3c9c2a08386843367`，`snapshot_id=a688f25acc329d45`。
- Prepare：状态 `READY`；1 个文件，26 个单元，其中 10 个初始 `PENDING`、16 个 `SKIPPED_PROTECTED`，保护跨度 643。prepare 产物位于 `prepare/`。
- 本轮范围：仅处理完整单元 `U-b24ef5a3242e`（`开头段 / 观点 / 平衡双轨`，源行 138–162，148 个作者汉字，34 个保护跨度）。其余 9 个可编辑单元未提交 bundle，保持 `PENDING`。
- 语料动作锚：`NONE_APPLICABLE`。该单元不同时具备任一 COURSE 正向卡要求的全部对象、条件、工具/误读/推导依赖和检查锚点，未为使用卡片补造信息。
- Rewrite：决策 `REWRITE`；压缩“适用题目”和“逻辑链条”两段中文说明，删除包装腔并保持原有适用范围、否定强度与并列主题。英文例句未改；34 个保护占位符的 ID、hash、顺序和数量均保持一致。bundle 位于 `rewrites/U-b24ef5a3242e.json`。
- Finalize：所选单元状态 `DONE`，统一验证器 `PASS/0`，`hard_invariant_layer_status=PASS`、`speech_act_layer_status=PASS`、`style_signal_layer_status=PASS`，保护跨度检查 `PASS`。diff 位于 `prepare/diffs/U-b24ef5a3242e.diff`，逐单元验证位于 `prepare/validation/`。
- 总体收尾：`status=REVIEW`、`exit_code=2`；单元统计为 `DONE=1`、`PENDING=9`、`SKIPPED_PROTECTED=16`。`rendered_partial` 位于 `prepare/rendered_partial/test.tex`。同一 bundle 的组装重放为 `assembly_replay_idempotency=PASS`。
- 源文件：`source_files_modified=0`，收尾后 SHA-256 与快照一致。未覆盖源文件。
- 未运行项目编译命令，`compile_check=NOT_RUN`；收尾器报告 `full_format_errors=[]`，不得将其表述为 TeX 编译通过。
- v12 完成门：`coverage_completion_claim_allowed=false`，`humanize_completion_claim_allowed=false`，`voice_binding_status=REVIEW`，`voice_conformance_status=NOT_EVALUATED`，`cross_unit_repetition_status=NOT_EVALUATED`，`humanize_second_pass_convergence=NOT_RUN`。本记录只声明所选单元完成，不声明全文 Humanize 完成。
- `academic_correctness=NOT_EVALUATED`；未执行内容、引文、计算或学术正确性审查。
