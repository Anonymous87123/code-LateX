# v12 Voice Profile 绑定正确性审计

审计日期：2026-07-15  
审计方式：只读代码与合同对照；未修改 Skill 生产文件。  
审计对象：Voice Profile builder/validator、长文 prepare/finalize 及对应合同。

## 结论

当前 v12 不能按“生产正确”验收。已确认 1 个 P0、3 个 P1、1 个 P2。最严重的问题不是 hash 算错，而是消费门没有执行 Profile 自己的终态：builder/validator 明确返回 `REVIEW/2` 的 PERSONAL Profile，prepare 仍会接收，并把证据状态写成 `REBUILT_PASS`。此外，Profile 的绑定场景可以与 prepare 请求场景不一致，finalize 仍可能报告 `scene_routing_status=PASS` 和 `voice_binding_status=PASS`。

## P0：`REVIEW` PERSONAL Profile 可进入 prepare，并被改名为 `REBUILT_PASS`

合同要求：`SKILL.md`“只有 validator 返回 `PASS/0` 的 Profile 才能进入长文 prepare”；`voice-profile.md` 14.5 也要求经验证的 Profile 才能冻结。

代码事实：

- builder 在没有足够可发布 feature/negative control 时合法生成 `profile_kind=PERSONAL`、`validation_status=REVIEW`，CLI 退出 2：`build_humanize_voice_profile.py:1333,1440`。
- prepare 只调用 `load_and_validate_profile()` 校验 schema/自哈希，没有断言 `validation_status == "PASS"`：`prepare_humanize_long_document.py:598-601`。
- 只要 manifest/spec/source 能精确重建，任何 PERSONAL 都被写成 `voice_evidence_status=REBUILT_PASS`：`prepare_humanize_long_document.py:623-636`。
- finalize 又只要求 PERSONAL 的该字段等于 `REBUILT_PASS`，同样不检查 Profile 的 `validation_status`：`finalize_humanize_long_document.py:233-243`。

最小复现：

1. 准备 300 字以上、但不足 3 个去重分析段或无法形成可发布 feature 的作者样本。
2. 运行 builder；观察输出文件为 `PERSONAL`，`validation_status=REVIEW`，进程退出 2。
3. 用同一 manifest/spec/root 调用 prepare，并传入该 Profile 的正确 hash。
4. 实际结果：prepare 不拒绝，`run_metadata.json.voice_binding.voice_evidence_status` 为 `REBUILT_PASS`。

影响：一个明确未通过 validator 的个人声线工件进入全部 unit/chunk/ledger；后续 bundle 只需回显其 hash，`voice_binding_status` 就可能成为 `PASS`。这是错误完成态，不是一般文案问题。

修复与验收：

- supplied Profile 进入 prepare 前强制 `validation_status == PASS`；否则以稳定错误码拒绝，且不得创建半成品 run-dir。
- `REBUILT_PASS` 只能在“schema PASS + self-hash PASS + manifest binding PASS + evidence rebuild PASS + profile.validation_status PASS”全部成立时产生。
- finalize 独立重复检查冻结 Profile 的 `validation_status == PASS`。
- 新增真实 builder `REVIEW/2 -> prepare FAIL` 回归，不得用手工伪造 Profile 代替。

## P1：请求场景与 Profile `binding_scene` 可错配，metadata 还会重标场景

代码事实：

- prepare 先从 CLI 得出本次 `binding_scene`（`AUTO` 被改为 `GENERAL`）：`prepare_humanize_long_document.py:584-585`。
- supplied Profile 载入后没有比较 `profile.binding_scene` 与该场景：`598-640`。
- 返回 binding 时写入的是 CLI 推导值，而不是 Profile 自身值：`646`；unit 的 `scene` 也来自 CLI，而 Profile hash 可来自另一场景。
- finalize 的 expected binding 不包含 `binding_scene/requested_scene/scene_binding_status`，因此不会发现这种错配：`finalize_humanize_long_document.py:197-252`。

最小复现 A：生成/取出 `scene-default-general`，以正确 hash 调用 `prepare ... --scene RESEARCH --voice-profile ...`。当前代码接受；冻结 Profile 写 `binding_scene=GENERAL`，metadata 却写 `voice_binding.binding_scene=RESEARCH`，unit 写 `scene=RESEARCH`。

最小复现 B（标准 AUTO 路径）：builder 用 `--scene AUTO` 从单一 COURSE 样本构建，Profile 自动绑定 COURSE；prepare 再用 `--scene AUTO`，metadata 临时绑定 GENERAL，但仍接收 COURSE Profile。

影响：场景默认风格和个人 feature 的适用域可能被跨场景使用；finalize 仍可能给出 `scene_routing_status=PASS`、`voice_binding_status=PASS`。hash 完整性没有阻止语义错配。

修复与验收：

- 明确并编码唯一规则：显式场景必须等于 `profile.binding_scene`；AUTO 若不能真正逐单元路由，只允许 GENERAL Profile，或保持 `UNRESOLVED_AUTO` 并拒绝非 GENERAL supplied Profile。
- metadata 同时冻结 `profile_binding_scene` 与 `requested_scene`，不得用一个字段覆盖两种语义。
- finalize 独立比较 Profile、metadata、unit/chunk 的场景绑定。
- 增加 GENERAL→RESEARCH、COURSE→AUTO、PERSONAL/DEFAULT 两类错配测试。

## P1：`unique_complete_units` 未执行近重复去重，可把一个长样本变成 HIGH

合同要求：HIGH 需要 `>=5000` 个去重作者汉字且至少 3 个“去重完整文本单元”；同一内容的复制或近重复不得抬高阈值。

代码事实：

- 分析段使用 exact + 5-gram near dedup：`build_humanize_voice_profile.py:751-806`。
- 但完整文本单元只按 `complete_unit_sha256` 的精确集合计数：`1238-1246`；validator 也只重算精确 hash 集合。
- 因此三个 5000 字文件只需各改极少字符，就可让段落在 near-dedup 中归为一个代表段（作者字数仍约 5000），同时让三个完整文件 hash 不同，得到 `unique_complete_units=3` 和 `confidence=HIGH`。

最小复现：建立三个 `complete_unit=true` 的单段文件，每篇约 5000 汉字，第二、三篇只替换 1 个汉字；三者 5-gram Jaccard 仍高于 0.90。预期应为 1 个去重完整单元、最高 MEDIUM；当前实现会把三个不同的 `complete_unit_sha256` 计为 3，可能升级 HIGH。

修复与验收：完整单元必须使用与分析单元一致、可审计的 exact/near cluster（或由代表分析单元簇集合构造完整单元身份），manifest 公布 complete-unit cluster；新增“三份近重复 5000 字不得 HIGH”测试。

## P1：finalize 把 Profile hash 错报为 manifest hash

`finalization_metadata.json` 同时写：

```text
voice_profile_sha256          = expected_voice_sha256
voice_profile_manifest_sha256 = expected_voice_sha256
```

位置：`finalize_humanize_long_document.py:1455-1456`。

对 PERSONAL 或证据绑定 DEFAULT，`profile_sha256` 与 `sample_binding.manifest_sha256` 本来是两个不同身份。当前字段会稳定地产生错误的机器可读审计信息，调用方无法据此定位实际样本 manifest。

修复与验收：第二字段必须来自冻结 Profile 的 `sample_binding.manifest_sha256`（或冻结 manifest 的 `manifest_sha256`），确定性零样本 DEFAULT 明确输出 64 个零或另设 `null`，并做字段语义测试。

## P2：长文 CLI 示例会诱导 PERSONAL 调用缺参数

`long-document-workflow.md` 3.1 的 prepare 示例只展示 `--voice-profile` 和 `--voice-profile-sha256`；PERSONAL 实际还强制要求 `--voice-manifest --voice-sample-spec --voice-allowed-root`。后文虽有解释，但读者按最近的可复制示例执行会得到 `personal_voice_profile_requires_rebuild_evidence`。

修复：把示例拆成“无样本默认”“supplied DEFAULT”“PERSONAL”三条完整命令，并明确 AUTO/绑定场景规则。

## 现有测试缺口

当前测试覆盖了默认 Profile 物化、正确/错误 hash、Profile 工件漂移、PERSONAL 缺 manifest/spec/source、证据绑定 DEFAULT、阈值边界和重复段落；未见以下回归：

- builder `REVIEW/2` Profile 必须被 prepare 拒绝；
- requested scene 与 `profile.binding_scene` 错配；
- 三个完整文件近重复但 hash 不同；
- `voice_profile_manifest_sha256` 等于真实 manifest hash。

## 验收结论

在 P0 和三个 P1 修复并增加上述回归前，不能把 v12 Voice Profile 链路称为生产稳定。当前可确认的能力是“工件自哈希、manifest 精确绑定、prepare 产物封存和 bundle hash 回显已经存在”；不能确认“只有合格 Profile 可被消费”“场景绑定语义正确”或“HIGH 阈值不可被近重复样本抬高”。
