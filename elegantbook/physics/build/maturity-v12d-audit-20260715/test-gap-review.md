# Voice Profile v12 回归测试缺口审查

日期：2026-07-15  
范围：只读审查以下测试及其对应实现：

- `tests/test_humanize_voice_profile.py`
- `tests/test_long_document_voice_binding.py`
- `tests/test_prepare_humanize_long_document.py`
- `tests/test_finalize_humanize_long_document.py`
- `build_humanize_voice_profile.py`
- `validate_humanize_voice_profile.py`
- `prepare_humanize_long_document.py`
- `finalize_humanize_long_document.py`

## 结论

当前四组测试共 75 个用例，全部通过；新增的“默认 Profile 场景错配拒绝”和“`PERSONAL/REVIEW` 不得进入 prepare”已经封住两条直接路径。但仍有三条更深的旁路可在当前实现中真实得到 `PASS`：

1. rewrite bundle 使用非严格 JSON 解析，重复的 `voice_profile_sha256` 键可让错误 hash 被后一个正确 hash 覆盖；
2. Profile 的 `binding_scene` 没有与正向 feature 的适用 scope 建立可消费性约束，COURSE-only 证据可被包装为 RESEARCH Profile 并一路 `PASS`；
3. 近重复聚类只和当前代表样本比较，不计算传递闭包；近重复链可被拆成三个“独立”完整单元，解锁 `HIGH/PASS`。

这三项应作为 v12d 的 P0 回归测试。其余建议主要是状态矩阵和集成层防回退。

## P0：已复现、当前会错误 PASS

### 1. 重复 JSON 键可让错误 Voice hash 冒充正确 hash

建议测试名：`test_duplicate_voice_hash_keys_are_rejected_before_binding`

相关实现：

- `finalize_humanize_long_document.py:141-144` 的 `_load_json()` 直接调用标准 `json.loads`；
- `finalize_humanize_long_document.py:304` 的 `_rewrite_bundle()` 使用该加载器；
- 相比之下，Voice Profile builder 在 `build_humanize_voice_profile.py:243-270` 已有拒绝重复键的严格加载器。

当前测试 `test_missing_or_wrong_bundle_hash_is_reviewed_before_text_validation` 只覆盖“键缺失”和“单个 64 位错误值”，没有提交原始、含重复键的 JSON。

最小复现 bundle：

```json
{
  "decision": "NO_CHANGE",
  "reason": "该段保持原有简短判断",
  "voice_profile_sha256": "0000000000000000000000000000000000000000000000000000000000000000",
  "voice_profile_sha256": "<当前 chunk 的正确 hash>"
}
```

当前实测结果：

```text
status=PASS
voice_binding_status=PASS
voice_profile_bindings_matched=1
voice_profile_bindings_mismatched=0
```

原因是 Python 解析器采用 last-key-wins，错误 hash 在进入 `_bundle_voice_binding_error()` 前已经消失。不同 JSON 解析器还可能选择首值或直接拒绝，形成跨实现歧义。

回归断言应为：

- rewrite bundle 的任意重复键均被视为结构错误；
- 不调用正文 validator；
- 不产生 `rendered/`；
- CLI 不得返回 0，机器结果不得出现 `status=PASS` 或 `voice_binding_status=PASS`。

同一参数化用例还应覆盖重复的 `decision`、`masked_text`、`warning_review` 和 `keep_reasons`，但重复 Voice hash 是必须先锁死的安全断言。

### 2. 只有错场景证据的 PERSONAL Profile 可绑定目标场景并 PASS

建议测试名：`test_personal_profile_requires_positive_feature_applicable_to_binding_scene`

相关实现：

- builder 在 `build_humanize_voice_profile.py:1341` 直接把显式 `--scene` 写成 `binding_scene`；
- feature scope 由支持样本的场景生成；
- `validate_profile_object()` 会分别校验 `binding_scene` 与 feature scope 的合法枚举，却没有要求至少一个正向 feature 对 `binding_scene` 或 `GLOBAL` 可用；
- prepare 目前只比较 `profile.binding_scene == requested_scene`；
- finalize 在 `finalize_humanize_long_document.py:1430` 只因 unit.scene 是合法枚举就写 `scene_routing_status=PASS`。

隔离复现：用三个 `scene=COURSE` 的合格作者样本建立 `scene=RESEARCH` Profile。当前得到：

```text
profile.validation_status=PASS
profile.binding_scene=RESEARCH
sample_binding.sample_scenes=[COURSE]
所有正向 feature.scope=[COURSE]
prepare=成功
finalize.status=PASS
scene_routing_status=PASS
voice_binding_status=PASS
```

现有 `test_default_profiles_are_rejected_when_request_scene_differs` 和 PERSONAL 的 request/profile 直接错配测试只验证 Profile 声明的 scene；它们没有验证“声明的 RESEARCH 是否有任何 RESEARCH/GLOBAL 正向证据”。

回归断言不宜简单禁止所有跨场景样本，因为合同允许保守使用跨场景稳定习惯。应要求：

- `PERSONAL/PASS` 至少有一个正向 feature 的 scope 含 `binding_scene` 或 `GLOBAL`；
- 只有 COURSE-scoped 正向 feature 的 RESEARCH Profile 必须为 `REVIEW`，或在 validator/prepare 被明确拒绝；
- negative control 不能代替目标场景正向证据；
- finalize 不得把这种运行写成 `scene_routing_status=PASS`。

建议再加一个正例：混合样本重建出 `GLOBAL` feature 时，允许供目标场景消费，防止修复过度收紧。

### 3. 近重复链未做传递闭包，可解锁 HIGH/PASS

建议测试名：`test_near_duplicate_chain_is_one_component_and_cannot_unlock_high`

相关实现：`build_humanize_voice_profile.py:767-821`。当前 `_near_duplicate_clusters()` 只把新 unit 与“代表 unit”比较；一旦 B 被判为 A 的近重复，B 不会进入后续候选索引。因此若 `A~B`、`B~C`、但 `A!~C`，C 会成为新的代表。

当前 `test_three_near_duplicate_complete_files_do_not_unlock_high` 使用三个都直接接近同一 base 的样本，无法覆盖该传递性缺口。

隔离复现使用五个约 2010 汉字的完整样本，连续版本每次只替换一个 60 字区间，使相邻版本 Jaccard 均高于 0.90，而隔一个版本低于 0.90。五个样本属于一个连通近重复链。当前结果：

```text
analysis relation = [UNIQUE, NEAR, UNIQUE, NEAR, UNIQUE]
complete relation = [UNIQUE, NEAR, UNIQUE, NEAR, UNIQUE]
unique_analysis_units=3
unique_complete_units=3
readable_author_chars=6030
validation_status=PASS
confidence=HIGH
```

回归断言应为：

- 近重复关系按连通分量归簇，或采用等价的不会被代表选择绕过的算法；
- 上述五个样本只形成一个去重簇；
- `unique_complete_units=1`，不得解锁 `HIGH`；
- 对 sample spec 顺序做至少三种排列，簇数、置信度和 PASS/REVIEW 结果保持不变。

该用例应同时跑 analysis-unit 与 complete-unit 两条聚类路径，因为二者共用同一缺陷函数。

## P1：当前实现大体正确，但缺少关键防回退测试

### 4. REVIEW 状态应做 validator / prepare / finalize 三层消费矩阵

建议用例：

- `test_validator_review_profile_returns_review_and_exit_2`
- `test_prepare_rejects_review_and_fail_profiles_before_writing_run`
- `test_finalize_rejects_integrity_sealed_non_pass_profile`

现状：builder 的近重复用例验证了 builder 返回码 2；新增测试验证了 prepare 拒绝 `PERSONAL/REVIEW`。仍未直接验证：

- 独立 validator 在 `--rebuild-evidence` 后必须输出顶层 `status=REVIEW`、退出码 2，而不是仅看 schema/self-hash 后返回 0；
- finalize 自己的 `validation_status == PASS` 检查不能被未来重构为“自哈希有效即通过”；
- `FAIL` 与 `REVIEW` 都不可消费，且不能创建可发布派生目录。

finalize 的独立测试可从合法 run 出发，构造一个自哈希正确、完整性清单也重算过的非 PASS Profile，断言仍在 bundle 处理前失败。这样才真正测试消费门，而不是只测试“改 Profile 后旧完整性封条失效”。

### 5. hash 错误三分支应完整覆盖，并证明发生在正文验证前

建议参数化用例：`test_bundle_hash_error_taxonomy_precedes_text_validation`

现有测试覆盖：missing、64 位但不相等。缺少：

- 63/65 位十六进制；
- 大写十六进制；
- 非字符串；
- 非十六进制 64 字符；
- 重复键歧义（P0-1）。

断言应分别落到：

- missing -> `voice_profile_hash_missing`；
- 格式错误 -> `voice_profile_hash_invalid`；
- 合法格式但值不同 -> `voice_profile_hash_mismatch`；
- unit 保持 `UNRESOLVED`，不存在该 unit 的 validation artifact；
- `voice_profile_bindings_matched=0`，`voice_binding_status=REVIEW`。

当前公开计数把 invalid 与 mismatch 合并到 `mismatched`，测试至少应固定这一既有语义，或推动增加独立 invalid 计数，避免以后被静默算成 matched。

### 6. AUTO 场景必须贯穿保持未裁决，不能在 finalize 升级为 PASS

建议测试名：`test_auto_scene_binding_remains_not_evaluated_after_finalize`

现有默认 Profile 测试只使用显式 RESEARCH。缺少完整 AUTO 流程。应断言：

- prepare 暂时物化 GENERAL DEFAULT；
- metadata 的 `requested_scene=AUTO`、`scene_binding_status=UNRESOLVED_AUTO`；
- unit.scene 仍为 AUTO；
- 正确回显 Profile hash 后，`voice_binding_status` 可为 PASS；
- 但 `scene_routing_status=NOT_EVALUATED`、`humanize_completion_claim_allowed=false`、`full_completion_claim_allowed=false`。

该测试能防止未来把“GENERAL 临时绑定”误写成 AUTO 路由完成。

### 7. prepare 集成层应重测源样本漂移，PERSONAL 与证据绑定 DEFAULT 都要覆盖

建议参数化用例：`test_prepare_rejects_stale_rebuild_evidence`

现有 `test_validator_rebuilds_pinned_evidence_and_rejects_source_drift` 只直接调用 validator；长文绑定测试只验证干净证据可消费。缺少以下集成序列：

1. builder 生成 Profile/manifest/spec；
2. 修改一个样本源文件；
3. 直接调用 prepare 并提交旧 Profile/manifest/spec；
4. 断言 prepare 因现场 rebuild 不一致而失败，输出目录未形成可消费 run。

需要分别覆盖 `PERSONAL` 和 `<300` 字的证据绑定 DEFAULT，防止未来只保留 PERSONAL 的 rebuild 门。

## P2：建议的合同强化测试

### 8. rewrite bundle 只绑定 Profile hash，尚未绑定当前 unit/chunk 身份

当前 JSON bundle 不含 `unit_id`、`hash_before` 或 canonical chunk hash；同一 run 内所有 unit 共用一个 Voice hash。于是一个通用 `NO_CHANGE` bundle 改名后可以跨 unit 或跨同 Profile 的 run 重放，finalize 无法证明该 bundle 针对当前 chunk 形成。现有“四个汉字理由”门也允许“该段保持自然表达”一类通用理由。

建议先增加一个红灯测试：

- 在两个 unit 间重放完全相同的 `NO_CHANGE` bundle；
- 期望 bundle 必须精确回显 `unit_id` 与 `hash_before`（或单一 `chunk_sha256`）；
- 错 unit、旧 chunk、源快照变化后的重放不得成为 `NO_CHANGE/PASS`。

这超出 v12 当前最小合同，但它是“Profile hash 正确，却绑定了错误正文”的剩余入口，适合列入 v13 或 v12d 强化项。

## 已覆盖、不应重复列为首要缺口

当前测试已经覆盖：

- 四个场景 DEFAULT 工件互异、自哈希有效；
- 299/300/999/1000/4999/5000 字阈值；
- 少于三个完整单元时不能 HIGH；
- 直接近重复同一 base 的样本不能解锁 HIGH；
- 重复段落不能膨胀字数；
- code/math/quoted 范围不计作者字数；
- Profile 自哈希漂移与样本源漂移；
- 默认 Profile 与请求场景直接错配；
- PERSONAL Profile 缺 manifest/spec/root 时拒绝；
- `PERSONAL/REVIEW` 在 prepare 前拒绝；
- bundle hash 缺失或单一错误值时 unit 保持未决；
- 正确 hash 只使 `voice_binding_status=PASS`，不会使 `voice_conformance_status` 变成 PASS；
- prepare 工件漂移、账本/封条共同伪造、检查命令污染、partial/full 发布回退。

## 建议落地顺序

1. 先加 P0-1 重复键测试；它是最小、确定且当前直接返回 `PASS` 的 hash 绕过。
2. 再加 P0-2 目标场景正向 feature 可用性测试；同时保留 GLOBAL 正例。
3. 再加 P0-3 近重复链与 sample-order permutation 测试。
4. 补 P1-4 REVIEW 三层状态矩阵和 P1-5 hash 错误分类。
5. 补 AUTO 与 prepare 样本漂移集成测试。
6. 将 unit/chunk 身份回显列为下一版 bundle schema 的红灯测试。

## 本次验证记录

执行：

```text
python -m unittest \
  tests.test_humanize_voice_profile \
  tests.test_long_document_voice_binding \
  tests.test_prepare_humanize_long_document \
  tests.test_finalize_humanize_long_document -v
```

结果：75 tests，全部通过，耗时约 3.5 秒。另用临时目录做了三项只读实现复现，观测值已分别记录在 P0-1、P0-2、P0-3。未修改被审脚本或测试文件。
