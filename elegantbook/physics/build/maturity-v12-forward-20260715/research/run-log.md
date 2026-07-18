# RESEARCH 长文 Humanize 运行记录

- 源文件：C:\Users\Lenovo\Documents\xwechat_files\wxid_kngort9edhrs22_6b6f\msg\file\2026-05\main.tex
- 配置：mode=REWRITE、scene=RESEARCH、intensity=BALANCED、output=PATCH、voice=SCENE_DEFAULT、report_context=NONE
- 正式运行目录：current/
- rewrite bundle：rewrites/U-b1bcaa2c520d.json
- 源文件 SHA-256：f97c5dc63e66d094e2ec73fbd2c935393a3370229db1d46baae9772bdacd0625
- prepare/finalize 脚本 SHA-256：944ae958df6cdf94f7d0365860eee1d4b8f928c7923050c6e2106b57df12b6ff / 32c41fc0d91d54a28d766b6ea60033aeb686a83cddcebab066bc6ae1401a0bc

## Prepare

- snapshot_id=266e59b6eab82802
- status=READY
- 文件 1 个，单元 36 个：PENDING=28、SKIPPED_PROTECTED=8
- 可处理可编辑单元 28 个，保护跨度 821 个
- voice_evidence_status=DETERMINISTIC_DEFAULT
- 未发现 SKIPPED_GARBLED；未猜测或恢复字符

## 本轮唯一处理单元

- unit_id=U-b1bcaa2c520d
- 章节：问题二的模型建立与求解 / 情景结果与机制讨论
- 原始范围：258--283 行
- 动作卡：RESEARCH-SCOPE-01、RESEARCH-EVIDENCE-01
- 主要动作：保留当前参数组、归一化口径和非独立外部验证的主张范围；把结果观察放在导览前；删除“收口”施工词；压缩表后重复结论
- 保护占位符：42 个，数量、顺序与哈希回显一致
- 谓词来源：仅使用 COPY 与 ENTAILED_PARAPHRASE；未增加数字、来源、机制或外部验证结论

## Finalize

- 顶层状态：REVIEW，真实进程退出码 2
- 单元状态：DONE=1、PENDING=27、SKIPPED_PROTECTED=8
- U-b1bcaa2c520d：style_validation=PASS、protected_hashes_ok=PASS
- 精确 diff：current/diffs/U-b1bcaa2c520d.diff
- 派生稿：current/rendered_partial/
- 组装幂等重放：PASS
- 源文件修改数：0；当前源哈希与快照一致
- TeX 全文形式错误：0；外部编译命令未运行（compile_check=NOT_RUN）
- coverage_completion_claim_allowed=false
- humanize_completion_claim_allowed=false
- voice_conformance_status=NOT_EVALUATED
- cross_unit_repetition_status=NOT_EVALUATED
- 未运行学术正确性或内容质控

## 审计说明

第一次 prepare 后，Skill 脚本在磁盘上更新，旧快照缺少新版 finalize 要求的 voice_evidence_status，因此根目录保留了该失败尝试。没有修改其 prepare 封条。current/ 是在上述固定脚本哈希下重新 prepare 并完成 finalize 的正式结果。
