# finalize Voice Profile 绑定只读审计（v12）

## 审计范围与结论

本次只读审计仅检查以下三个生产文件，未读取 tests、其他 build、历史报告或 qualification 材料，也未修改被审计文件：

- `references/long-document-workflow.md`
- `references/voice-profile.md`
- `scripts/finalize_humanize_long_document.py`

当前实现是“安全地不宣称完成”，但还不是 Voice Profile 可绑定实现：长文合同已把 hash-bound Voice Profile 列为全文 Humanize 完成条件，并明确承认当前收尾器尚未实现；脚本则把 `voice_binding_status`、`voice_conformance_status` 固定为 `NOT_EVALUATED`，把 `voice_completion_claim_allowed`、`humanize_completion_claim_allowed` 和兼容字段固定为 `false`。这避免了假阳性完成声明，但 rewrite bundle 还不能回显 Profile 哈希，finalize 也无法拒绝 Profile 版本漂移或跨 unit/跨 run 错配。

v12 的最小安全实现应只闭合“Profile 身份与版本绑定”，不要把哈希回显误当作声线符合性证明：

1. prepare 阶段冻结一个可重建、可哈希的 Profile manifest，并把预期 Profile 哈希写入每个 unit/chunk；
2. `REWRITE` 与 `NO_CHANGE` bundle 都必须回显该哈希；
3. finalize 在接受 bundle 前比较预期值与回显值，并在发布前再次检查 Profile 漂移；
4. metadata 可以把 `voice_binding_status` 升为 `PASS`，但 `voice_conformance_status` 在没有独立全文门时仍为 `NOT_EVALUATED`，因此全文 Humanize 完成门仍必须为 `false`；
5. 无作者样本时使用四个场景各自独立、版本化、可重建的默认 Profile，不能在 finalize 时静默临时回退到一个无哈希的通用默认值。

## 现状证据

| 位置 | 现状 | 审计判断 |
|---|---|---|
| `long-document-workflow.md:39-60` | 区分覆盖完成与 Humanize 完成；后者要求 Voice 绑定，并明示 hash-bound Voice Profile 未实现 | 合同已正确降格完成声明 |
| `long-document-workflow.md:260-339` | unit 合同要求记录 `voice_profile`、Profile 版本、置信等级和默认声明 | 生产脚本尚未承载这些字段 |
| `long-document-workflow.md:393-449` | rewrite bundle 只有正文、理由、keep/warning 字段 | 缺少 Profile 身份回显 |
| `long-document-workflow.md:590-648` | metadata 要报告 `voice_binding_status`、`voice_conformance_status`，只有全部 Humanize 级门通过才可完成 | 可直接作为 v12 完成门依据 |
| `voice-profile.md:53-62` | 少于 300 个汉字时不得建立个人 Profile，应使用场景默认声线 | 默认 Profile 是正式回退，不是“无 Profile” |
| `voice-profile.md:100-214` | Profile 已有 `profile_id`、`version`、置信等级及完整风格字段 | 足以形成稳定哈希载荷，但尚无规范化规则 |
| `voice-profile.md:229-247` | `DEFAULT` 必须披露，并为四个场景定义最小默认声线 | 应物化为四个不同的版本化 Profile |
| `voice-profile.md:342-352` | Profile 更新必须保留版本和变更信息 | 旧哈希跨版本重放必须拒绝 |
| `voice-profile.md:373-443` | 模板包含 `profile_id`、`version`、`confidence: DEFAULT`、`default_disclosure` | 可作为默认 Profile 的最小字段基础 |
| `finalize_humanize_long_document.py:97-128` | prepare 完整性采用固定 artifact 集合，当前没有 Profile artifact | 新 manifest 若不加入集合会被直接视为 artifact 集变化 |
| `finalize_humanize_long_document.py:183-259` | bundle 白名单没有 Profile 哈希；未知字段会被拒绝 | 现在加入 `voice_profile_sha256` 会失败，必须显式扩展合同 |
| `finalize_humanize_long_document.py:261-274` | `.txt` 会被自动包装为无元数据的 `REWRITE` bundle | 在强制哈希回显后不能继续无条件接受 `.txt` |
| `finalize_humanize_long_document.py:520-543` | 最终账本字段没有 `voice_profile`、版本或哈希 | 与长文合同不一致 |
| `finalize_humanize_long_document.py:567-688` | finalize 能从冻结正文重建 prepare 状态，但没有重建 Profile 选择 | 仅把 Profile 哈希塞进可修改 metadata 不足以抵抗重封清单 |
| `finalize_humanize_long_document.py:799-907` | 读取 metadata/chunk/bundle 后直接进入 warning 与正文验证 | Profile manifest 校验与 bundle 绑定比较应插在此处、正文验证之前 |
| `finalize_humanize_long_document.py:1109-1158` | 编译前后会哈希 run artifacts、正文 staging 与 evidence staging | 可复用来发现检查命令篡改 run 内 Profile artifact |
| `finalize_humanize_long_document.py:1279-1324` | Voice 两层固定 `NOT_EVALUATED`，完成门固定 `false` | 当前安全，但无法表达“绑定已通过、符合性未评估” |

## 最小绑定协议

### 1. Profile 的规范化哈希

新增一个明确的 Profile schema version，并规定：

```text
profile_sha256 = SHA-256(UTF-8(canonical_json(profile_payload)))
canonical_json = sort_keys=true, separators=(",", ":"), ensure_ascii=false
```

哈希载荷不包含 `profile_sha256` 自身，但必须包含以下会影响绑定语义的字段：

- `profile_schema_version`
- `profile_id`
- `version`
- `confidence`
- `binding_scene`
- 完整的节奏、句法、语气、衔接、版式、词语、言语行为和场景覆盖字段
- `default_disclosure`
- 默认 Profile 的 `source_kind=SCENE_DEFAULT`；作者 Profile 的 `source_kind=AUTHOR_PROFILE`

脚本已有 `_canonical_json()` 与 `sha256()`，可直接复用。必须对解析后的对象做规范化哈希，不能对 YAML/JSON 原始排版字节做语义身份哈希，否则键序、缩进或换行会产生无意义版本漂移。原始文件字节仍可另存 `source_sha256` 用于发现源文件变化。

### 2. prepare 必须提供的冻结接口

虽然 prepare 脚本不在本次可读范围内，但 finalize 无法单独安全发明“当时使用的是哪个 Profile”。最小生产者接口应新增一个 `voice_profiles.json`，并将其加入 `prepare_integrity.json`；每个 profile entry 至少包含：

```json
{
  "profile_id": "scene-default-research",
  "version": 1,
  "confidence": "DEFAULT",
  "source_kind": "SCENE_DEFAULT",
  "binding_scene": "RESEARCH",
  "default_disclosure": true,
  "profile_sha256": "<64 lowercase hex>",
  "profile": {"...": "canonical payload"}
}
```

每个 unit/chunk 和初始账本再写入：

```text
voice_profile_id
voice_profile_version
voice_profile_confidence
voice_profile_source_kind
voice_profile_sha256
voice_default_disclosure
```

Profile 选择必须发生在 unit 的最终场景确定之后；最终 unit 不得以 `AUTO` 绑定 Profile。manifest、chunk 和账本三处值必须能互相重建，不能只信任其中一处。作者 Profile 还应记录其冻结源副本与 `source_sha256`；若原 Profile 文件在 finalize 前或期间变化，按漂移处理，不自动升级到新版本。

### 3. rewrite bundle 回显

在 `_validate_rewrite_bundle_fields()` 的公共字段中仅增加：

```json
"voice_profile_sha256": "<64 lowercase hex>"
```

该字段对 `REWRITE` 与 `NO_CHANGE` 同样必填。bundle 不得提交 Profile 正文、Profile ID 覆盖值、版本覆盖值或“采用默认 Profile”的布尔开关；这些权威值只能来自冻结 manifest/chunk。这样可以避免 bundle 自己定义再自己证明。

兼容性需要明确失败闭合：现有 `.txt` bundle 无法回显哈希。Profile 绑定启用的 run 应拒绝 `.txt`，要求使用 JSON；不要由 finalize 自动替它补入预期哈希，因为那会取消“生成端实际看见并回显版本”的审计意义。

### 4. finalize 漂移与错配拒绝

建议在 `_finalize_locked()` 读取 `run_metadata` 和 chunks 后、收集/验证正文 bundle 前执行以下顺序：

1. 读取 `voice_profiles.json`，校验 schema、字段类型和 64 位小写十六进制哈希。
2. 对每个 canonical profile 重算 `profile_sha256`。
3. 对 `SCENE_DEFAULT` Profile 用代码内版本化默认构造器独立重建，并比较完整 canonical payload；这样即使攻击者同时修改 manifest 和 `prepare_integrity.json`，也不能把另一个默认声线重封成合法默认 Profile。
4. 对作者 Profile 核对冻结源副本哈希，并在存在外部源路径时核对当前源字节；任何变化均为 Profile drift。
5. 逐 unit 验证 scene、profile ID、version、confidence 和 hash 与 manifest 一致；`AUTO`、未知 profile、跨 scene default 或重复 ID/不同内容均拒绝。
6. 对每个 `REWRITE/NO_CHANGE` bundle 校验回显字段：缺失、格式错误或与 unit 预期哈希不一致时，不调用正文 validator，不进入 `DONE/NO_CHANGE`，将该 unit 标为 `UNRESOLVED`，notes 使用独立原因码，例如 `voice_profile_hash_missing`、`voice_profile_hash_invalid`、`voice_profile_hash_mismatch`。不要继续沿用当前笼统的 `invalid_warning_review` 标签。
7. 编译/格式检查后、发布前再次核对 Profile artifact 和外部 Profile 源。run 内 artifact 的变化可由现有 `_run_state_hashes()` 捕获；外部 Profile 源需像正文 `_source_changes()` 一样做前后两次哈希比较。

错误分级：

- Profile manifest、冻结 Profile 或 Profile 源发生漂移：属于 prepare 身份失真，必须在发布前硬拒绝；不创建/覆盖 rendered，也不发布本轮 evidence。
- 单个 bundle 缺失或错配回显：属于候选不满足合同，该 unit 进入 `UNRESOLVED`，本轮为 `REVIEW/2`，不接受该 unit。
- bundle 试图携带 Profile 正文或覆盖 ID/version：按未知字段拒绝。

### 5. metadata 完成门

新增或落实以下机器可读字段：

```text
voice_profile_manifest_sha256
voice_profile_bindings_total
voice_profile_bindings_matched
voice_profile_bindings_missing
voice_profile_bindings_mismatched
voice_profile_default_units
voice_profile_default_scenes
voice_default_disclosure_required
voice_binding_status
voice_conformance_status
voice_completion_claim_allowed
humanize_completion_claim_allowed
full_completion_claim_allowed
```

`voice_binding_status=PASS` 只表示每个可处理 unit 的冻结 Profile 身份有效，且其终态 bundle 精确回显了相同哈希；它不证明正文符合该声线。建议完成公式固定为：

```text
voice_completion_claim_allowed =
  coverage_completion_claim_allowed
  and scene_routing_status == PASS
  and voice_binding_status == PASS
  and voice_conformance_status == PASS

humanize_completion_claim_allowed =
  voice_completion_claim_allowed
  and cross_unit_repetition_status == PASS
  and humanize_second_pass_convergence == PASS

full_completion_claim_allowed = humanize_completion_claim_allowed
```

因此，v12 若只实现 Profile 哈希绑定，可以把 `voice_binding_status` 从 `NOT_EVALUATED` 提升为真实的 `PASS/REVIEW/FAIL`，但 `voice_conformance_status` 仍应为 `NOT_EVALUATED`，`voice_completion_claim_allowed=false`，全文 Humanize 两个完成字段仍为 `false`。这是正确的阶段性结果，不应为了“完成 Profile 功能”而跳过全文符合性、跨块重复或 fresh second pass。

### 6. 默认 Profile 的最小实现

为 `COURSE`、`MODELING`、`RESEARCH`、`GENERAL` 各定义一个独立 canonical Profile，不建立一个可跨场景复用的 generic default。每个默认 Profile 至少具有：

```text
profile_id=scene-default-<scene>
version=1
confidence=DEFAULT
source_kind=SCENE_DEFAULT
binding_scene=<concrete scene>
sample_scope=[]
sample_scenes=[]
readable_author_chars=0
unique_units=0
default_disclosure=true
```

其 `voice`/场景字段分别承载 `voice-profile.md:237-247` 的四条最小声线。默认构造器必须确定性、版本化，且 finalize 能独立重建；修改默认声线内容必须递增 `version` 并改变哈希。metadata 必须列出使用默认 Profile 的 unit 数与场景，并设置 `voice_default_disclosure_required=true`。这只能声明“使用场景默认声线”，不能声称复现作者个人文风。

## 攻击测试设计（12 项）

以下测试针对拟议的 v12 合同，均要求验证 unit 状态、进程状态、发布目录和 `finalization_metadata.json`，不能只断言异常字符串。

| ID | 攻击/变异 | 预期拒绝与断言 |
|---|---|---|
| V12-VP-01 | `REWRITE` JSON 删除 `voice_profile_sha256` | unit=`UNRESOLVED`，原因 `voice_profile_hash_missing`；不进入 diff/accepted；`voice_binding_status=REVIEW`，不得发布完整 rendered |
| V12-VP-02 | 回显 63 位、非十六进制或带空白的 Profile 哈希 | 在正文 validator 前拒绝，原因 `voice_profile_hash_invalid`；不得容错截断或大小写猜测 |
| V12-VP-03 | 回显格式合法但内容错误的 64 位哈希 | unit=`UNRESOLVED`，原因 `voice_profile_hash_mismatch`；不能因正文 validator PASS 而接受 |
| V12-VP-04 | 混合文档中把 COURSE unit 的默认 Profile 哈希重放到 RESEARCH unit | 跨 scene default 错配被拒；两个 unit 的预期哈希必须不同；metadata 不能把错配计入 matched |
| V12-VP-05 | 同一 `profile_id` 的旧 `version`/旧哈希从上一 run 重放到新 run | 即使 unit_id 与正文相同也拒绝；绑定以当前冻结 version/hash 为准，禁止跨 run 重放 |
| V12-VP-06 | `NO_CHANGE` bundle 不回显或回显错误哈希 | 与 `REWRITE` 同样拒绝；不能用 NO_CHANGE 绕过 Voice 绑定；原文 validator PASS 也不得把 unit 标为 `NO_CHANGE` |
| V12-VP-07 | 提交旧式 `.txt` rewrite | Profile-bound run 明确拒绝，要求 JSON；finalize 不得自动注入预期哈希后继续 |
| V12-VP-08 | bundle 增加 `profile`、`profile_id`、`profile_version` 等自定义权威字段，并配一个自算哈希 | 未授权字段被拒；权威 Profile 只能来自冻结 manifest/chunk，候选不能自定义 Profile 后自证 |
| V12-VP-09 | prepare 后修改 `voice_profiles.json`，不更新 `prepare_integrity.json` | `_verify_prepare_integrity` 阶段硬拒绝；不创建 staging 发布，不覆盖既有 rendered/evidence |
| V12-VP-10 | 同时修改默认 Profile manifest 与 `prepare_integrity.json` 中对应哈希 | finalize 的确定性默认构造器重建结果不一致，仍硬拒绝；证明完整性清单不是默认 Profile 的唯一信任根 |
| V12-VP-11 | 作者 Profile 源在 finalize 前变化，或由 `--check-command` 在校验与发布之间改动 | 前置变化在处理 bundle 前拒绝；中途变化触发硬失败并丢弃本轮 staging/evidence；不得发布基于旧 Profile 的结果 |
| V12-VP-12 | 所有 bundle 哈希都正确，覆盖也闭合，但 `voice_conformance_status`、跨块重复门或 fresh second pass 仍为 `NOT_EVALUATED/NOT_RUN`；另尝试在 prepare metadata 中伪造完成布尔值 | `voice_binding_status` 可为 PASS，但 `voice_completion_claim_allowed=false`、`humanize_completion_claim_allowed=false`、`full_completion_claim_allowed=false`；finalize 必须重算完成字段，忽略/拒绝调用方预置值 |

建议再设一个非攻击基线：同一 concrete scene、同一冻结默认 Profile、`REWRITE` 与 `NO_CHANGE` 均回显精确哈希时，两类决策都能进入既有正文验证流程；metadata 报告 binding PASS、default disclosure required，同时继续保持 conformance 与 Humanize 完成门未通过。

## 验收顺序与残余边界

最小落地顺序应为：canonical/default Profile 定义 → prepare 冻结接口 → chunk/ledger 绑定字段 → bundle 回显字段 → finalize 前置和发布前复核 → metadata 公式 → 上述攻击测试。若只先改 bundle 白名单而没有 prepare 冻结身份，回显值没有可信预期；若只在 metadata 中写 Profile 哈希而不要求 bundle 回显，也不能发现生成端使用了旧版本。

Profile 哈希回显仍不是“模型确实遵循了 Profile”的证明：生成端可以机械复制哈希。它只闭合版本、场景和 artifact 身份。声线符合性必须由独立、面向全文的 `voice_conformance_status` 门负责；跨 unit 复用与 fresh second pass 仍由现有独立字段负责。

本地 SHA-256 也不是外部签名信任根。能同时改写代码、全部 prepare artifact、外部 Profile 源和完整性清单的攻击者不在单机哈希协议可证明的范围内；若未来需要跨主机或不可信调用方证明，应引入外部签名 receipt，而不是继续叠加调用方自报字段。
