# v42：位置 scope 门、run-scoped amend 与 v3 血缘复盘

## 1. 本轮从真实回归开始

v41.1 的 `modeling-r3/review-final` 在冻结 policy 下 mechanical/hard/speech/style/coverage 均 PASS，但新的
独立盲读逐处比较 source 与 candidate 后，把第 13 行判为 `WORSE`：

```text
因此，正文里既要保留粗扫结果……
    ->
因此，既要保留粗扫结果……
```

“正文里”不是无功能后台词。它限定粗扫和加密扫描结果应出现的位置；候选只删位置范围，却保留其余
“既要……也要……”编辑要求，既没有把句子真正正文化，也改变了要求的适用位置。

本轮因此同时处理两个问题：

1. 语义门不能静默放过这种窄 scope 删除；
2. warning 修复不应要求使用者重新登记所有 span、selection、reason 和未变 hunk。

## 2. `SPEECH_ACT_EDITORIAL_SCOPE_DROPPED`

新增门只覆盖一个可审计的窄转换：来源句含 `正文里/正文中/文中`，同时含编辑动作；改后对应句逐字保留
其余编辑动作，只删除位置 marker。命中时返回：

```text
SPEECH_ACT_EDITORIAL_SCOPE_DROPPED
required_action=PRESERVE_OR_EXPLICITLY_RELOCATE_EDITORIAL_SCOPE
semantic_judgment=NOT_EVALUATED
detector_scope=VERBATIM_RETAINED_EDITORIAL_ACTION_ONLY
```

该门不会因以下情况触发：

- 原句本来没有位置范围；
- “正文里”改成“正文中”或范围移到句内其他位置；
- 只是描述“正文中展示了……”，没有 `要/需/应` 编辑动作；
- 更宽的自然语言重写不满足该窄门的逐字条件。

后两类仍需连续阅读；`NOT_TRIGGERED` 不等于语义安全。新增 3 项正反回归，并保留既有 v41
`EDITORIAL_TO_EVIDENCE` 与第一人称门。

当前 unified validator 对旧 postfix final 的结果为：

```text
mechanical=REVIEW
speech_act=REVIEW
warning=SPEECH_ACT_EDITORIAL_SCOPE_DROPPED
```

旧 evidence 目录仍逐工件 hash 自洽；verifier 现在正确输出：

```text
record_integrity_status=PASS
current_policy_status=DRIFT
current_policy_replay_status=NOT_RUN
delivery=REVIEW/2
```

policy 变化不再被误报成“历史 review.md 损坏”。

## 3. 为什么 amend 必须从 verified review 开始

authoring scaffold 位于调用方可写边界，hunk 和 selection 尚未被实际应用；直接在旧 authoring 上“局部修改”
不能证明它来自哪个已组装候选。verified review 则具有闭集：

```text
source.snapshot.bin
candidate.review.*
patch.bundle.json
coverage.json
patch.diff
validation.json
result.json
review.md
evidence-manifest.json
```

只有父 review 同时满足 record integrity、current-policy replay、coverage replay，才允许建立子 revision。
父候选的交付仍可为 REVIEW，因为修订机械 warning 正是 amend 的主要用途。

## 4. 两阶段 amend 接口

先冻结要改的既有 hunk：

```powershell
python scripts/amend_humanize_short_patch.py create <base-review> `
  --hunk H003 --hunk H005 `
  --output amendment.authoring.json `
  --live-source source.tex --format text
```

create 返回：

```text
PENDING AMENDMENT exit=0 hunks=2
```

`humanize-short-patch-amend-authoring/v1` 的可编辑面只有每个 change 的：

```text
after.decision
after.replacement
after.reason
```

`before` 保存父 bundle 的完整 hunk。authoring 不提供 scene、intensity、protected terms、source text、offset、
selection、KEEP、conflict 或增删/重排 hunk 的字段。列入 changes 却没有实际变化固定失败：

```text
SELECTED_HUNK_NOT_CHANGED
```

编辑后运行：

```powershell
python scripts/amend_humanize_short_patch.py apply <base-review> `
  --amendment amendment.authoring.json `
  --output <new-review> `
  --live-source source.tex --format text
```

成功候选仍固定：

```text
DELIVERY REVIEW exit=2
```

## 5. bundle v3 与不可变父子关系

普通 builder 继续只生产 v1/v2；只有 amend 工具可生成 `humanize-short-patch/v3`。v3 在完整 v2 数据上嵌入：

```text
schema=humanize-short-patch-amendment-lineage/v1
integrity_scope=SELF_CONSISTENCY_ONLY
parent_bundle=<完整父 bundle>
parent_manifest_sha256
parent_candidate_sha256
amendment_spec_sha256
amendment_depth
changed_hunks[{hunk_id,before_hunk_sha256,after_hunk_sha256}]
amendment_sha256
```

validator/verifier 逐层强制父子相等：

- source hash、size、encoding 和 offset unit；
- requested/effective output、mode、scene、intensity；
- protected terms 与 document format；
- coverage source kind、scan scene 和全部 declarations；
- hunk 数量、顺序、ID、start/end、source text/source hash；
- 未列入 changed set 的 hunk 全字段；
- 列入 changed set 的 before/after hunk hash 与实际变化集合。

唯一允许变化的是声明 hunk 的 `decision/replacement/reason`。coverage 不从父记录手改，而是以冻结 declarations
和新 hunks 重建；显式 conflict 成员若不再是 UNRESOLVED，原 coverage 门继续拒绝。

最大 amendment depth 为 8。超过深度或 2 MiB JSON 上限时返回：

```text
AMENDMENT_CHAIN_LIMIT_REQUIRES_NEW_AUTHORING_RUN
```

工具不会静默压平或截断父链。

## 6. 原子发布与失败分级

apply 的顺序为：

1. verify 父 review；
2. 严格读取 amendment authoring；
3. 核对 base、policy、before hunk 与 live source；
4. 从父 coverage declarations 重建 selection v2；
5. 构造 v3 bundle；
6. 在最终目录旁的临时目录运行原 applicator；
7. verify 新 review；
8. 再读父工件、amendment、live source 和 current policy；
9. 全部一致后原子 rename。

状态分级：

- policy、coverage policy、live source 或执行中 policy 漂移：`REVIEW/2`，不发布；
- strict JSON、base/before 篡改、非法动作、hard invariant 或闭集错误：`FAIL/1`，不发布；
- 既有输出目录：拒绝覆盖；
- 成功组装：新 closed review，交付仍 `REVIEW/2`。

## 7. 12 项聚焦 amend 攻击测试

新增 `tests/test_humanize_short_patch_amend.py`，覆盖：

1. v2→v3 成功，未改 hunk 逐字段不变；
2. 多 hunk 按父 source 顺序冻结；
3. no-op 与 before anchor 篡改；
4. stale base 和父 record 篡改；
5. 非法 topology/config 字段；
6. policy 和 live source drift；
7. apply 中途 policy 变化并原子回滚；
8. applicator 失败与既有 output 不覆盖；
9. CLI `create=0/apply=2/fail=1`；
10. v3→v3 链式 amend，depth 递增。
11. 攻击者修改未声明 hunk 并重封顶层 bundle，coverage/lineage 仍拒绝；
12. depth 1-8 可验证，第 9 层固定要求新开普通 authoring run。

结果：

```text
Ran 12 tests
OK
```

## 8. 真实 modeling 回放

证据目录为本目录。父 review 不是直接复用旧 v41 evidence，而是用 current policy 重新 apply
`patch.bundle.revised.json`，得到 [base-review](base-review)：

```text
record/current-policy/coverage replay=PASS
candidate delivery=REVIEW/2
mechanical=REVIEW
```

### 8.1 第一轮：v2→v3，修改 H003/H005

[amendment.authoring.json](amendment.authoring.json) 只修改 H003 和 H005。新 [amended-review](amended-review)：

```text
amendment_depth=1
changed_hunks=H003,H005
lineage/current-policy/coverage replay=PASS
candidate_sha256=357528668d91fb5d4e42fd509c6437012db170d5e005dac19b9e9498d57539b5
mechanical=REVIEW
warnings=NEGATION_CHANGED, MODALITY_SCOPE_CHANGED
```

工具链成功不等于候选通过；该轮保留为失败证据。

### 8.2 第二轮：v3→v3，只改 H003

从 depth=1 的父 review 生成 [amendment2.authoring.json](amendment2.authoring.json)，只修改 H003。最终
[amended-review-v2](amended-review-v2) 的 H003 为：

> 因此，粗扫结果和加密扫描结果在正文中都要保留，结论要写成区间性的观测判断，而不是把一个网格点直接升格为硬边界。

它保留位置范围、两个要求槽位和“而不是”否定关系，同时消除“正文里既要……”的句首后台感。机械结果：

```text
amendment_depth=2
changed_hunks=H003
candidate_sha256=54281967ba4049dfddf7e25d7496ff71c45a08b3698b5a220a7ff028808a2b00
record_integrity=PASS
amendment_lineage=PASS
lineage_policy=PASS
current_policy_replay=PASS
coverage_replay=PASS
live_source=MATCH
mechanical/hard/speech/style=PASS/PASS/PASS/PASS
unaccepted_warnings=0
unexplained_high=0
delivery=REVIEW/2
paired_quality=PENDING_EXTERNAL_REVIEW
```

这组证据证明局部修订可以保留未变 hunk、selection 和 coverage declarations，并支持 v3→v3 继续修订。
它不证明读感最终优于 source；独立 paired review 仍只有否决/建议权，不能签发可信外部 clearance。

### 8.3 Fresh paired review

新的只读代理只收到 source、最终 candidate 和 Skill 路径，没有读取旧报告、bundle、测试或预期问题。它逐处
核对 4 个变化行、5 个独立改动跨度：

```text
BETTER 5
SAME 0
WORSE 0
overall=BETTER_WITH_RESIDUALS
document_state=NEEDS_FURTHER_REVISION
```

其中 H003 被判为 BETTER：对象提前出现，“既要—也要—并”的工整指令链被压缩，同时保留粗扫、加密扫、
正文位置、区间判断和排除硬边界四项关系。没有发现本轮引入的语义、模态、因果或段落职责回退。

盲读仍列出文档级残留：L6 的“最小闭环/这一问更适合”，L8 的验收式“完成问题三的任务”，L13 的正文
写法指令，L15 的“把这段写成/提醒读者/核心不是而是”，L17 的自动展望与泛化严谨评价，以及 L19 未改的
条件式图示计划。故这份结果支持本轮 changed spans，而不支持“全文文风清理完成”。

## 9. 测试、版本与双投影

当前 source checkpoint：

```text
focused 6 modules=209 total; 207 passed; 2 skipped
full unittest=838 total; 834 passed; 4 skipped
quick_validate source/final/repro=PASS/PASS/PASS
SKILL.md=453 physical lines; 324 non-empty
builder/policy=1.13.0/1.13.0
approved capability=29e8a24f73fbd2a7348d8330e78e4538ef4269dd28bd550e08753349605cccb0
projection files=38/38
projection BYTE_DIFFS=0
projection tree=0eb86180c4a3deb7cbe9d17f930488c38808df8a67038360b6afea3b892eca9e
manifest file SHA=c2844657bc92baf68d7bae97c856b4d6c8b7b0bdbac45bd7eb8970aadf2b728e
evidence_cap=E2
generation qualification=NOT_EVALUATED
```

双投影：

- [final projection](../generator-projection-maturity-v42-final-20260719)
- [repro projection](../generator-projection-maturity-v42-final-repro-20260719)

两份投影相对路径、38 个文件内容 SHA 和 manifest 字节一致。新 amend 工具属于 production generator
surface；qualification oracle、完整外部审批和私有 replay 审计仍被排除。

## 10. 能证明与不能证明

本轮能证明：

- 旧 postfix scope 回归可被当前窄门机械发现；
- verified parent review 可以形成不可变、可重放的局部 revision；
- 未列入 changed set 的 hunk 和全部 coverage declarations 会被强制保持；
- v2→v3、v3→v3、policy/live drift、篡改和原子回滚已有测试；
- 当前 source、全量测试和双投影处于同一 1.13.0 checkpoint。

本轮不能证明：

- scanner 或语义门发现全部自然语言问题；
- 最终 candidate 获得外部 paired-quality clearance；
- 学术正确性、证据真实性、作者身份或检测结果；
- AUTO route freeze、`reason_ref` 和 registry repair 已完成；
- generation qualification 已评估。

下一项高价值成熟化仍是 authoring 前冻结 AUTO resolved scene，并在 route 变化时提供明确的新 run 迁移，
而不是让使用者完成 GENERAL 候选后才发现应重建为 MODELING。
