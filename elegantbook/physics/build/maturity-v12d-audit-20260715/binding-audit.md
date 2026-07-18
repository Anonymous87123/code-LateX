# humanize-academic-chinese v12d Voice 绑定独立审计

审计日期：2026-07-15（Asia/Shanghai）  
审计方式：只读代码审计、现有测试检查、临时目录最小复现；未修改 Skill 生产文件。  
审计范围：`build_humanize_voice_profile.py`、`validate_humanize_voice_profile.py`、`prepare_humanize_long_document.py`、`finalize_humanize_long_document.py`，以及四组直接相关单元测试。

## 1. 结论

当前版本还不能把 Voice Profile 子链称为生产稳定。独立复现得到 1 个 P0、2 个 P1 和 1 个 P2：

| ID | 严重度 | 结论 |
|---|---:|---|
| V12D-01 | P0 | near-dedup 是依赖样本顺序的贪心 representative 聚类；同一证据集合仅交换 spec 顺序，即可从 `MEDIUM/REVIEW` 变成 `HIGH/PASS` |
| V12D-02 | P1 | finalize 不校验冻结 sample spec 与 manifest/Profile 的绑定；把 AUTHOR 声明改为 `MODEL_GENERATED` 并自行重封完整性清单后，仍得到 `PASS/PASS` |
| V12D-03 | P1 | builder 允许把纯 COURSE 样本直接重标为 RESEARCH Profile，且 Profile 与 prepare 均为 PASS/READY |
| V12D-04 | P2 | 独立 validator 在不验证 manifest、不重建证据时仍可输出顶层 `status=PASS` 和退出码 0，状态语义容易被下游误用 |

其中 V12D-01 会直接改变 `unique_analysis_units`、`readable_author_chars`、`unique_complete_units`、置信等级、feature 支持数和最终 `validation_status`，属于可制造错误 PASS 的门禁缺陷。V12D-02 说明 Voice 冻结证据目前没有达到长文主链已经声明的“即使调用方同时修改工件并重算封条，也不能伪造完成态”的强度。V12D-03 说明新加入的请求场景绑定只检查 Profile 标签是否相同，没有检查该标签是否由对应场景证据产生。

完成声明方面，当前 finalize 仍把 `voice_conformance_status` 固定为 `NOT_EVALUATED`，并把 `humanize_completion_claim_allowed/full_completion_claim_allowed` 固定为 false；这一边界是正确的。当前主要风险不是伪造“全文 Humanize 完成”，而是伪造或错误升级 `PERSONAL/PASS`、`HIGH`、`REBUILT_PASS` 与 `voice_binding_status=PASS`。

## 2. 审计快照

发现复现对应以下文件字节：

```text
5126ce7145b4b6beab2197b09d5cd31962ef97d0defccdf4e193ecd766be16ad  build_humanize_voice_profile.py
2e60f39eb757d7e74142549b1c7885aea7072b3fb87c12e54f4cdefc63076cc7  validate_humanize_voice_profile.py
3c748c4fe5a580044581a37f69e854c42022db5cf4a09ea265a09c28d3491e43  prepare_humanize_long_document.py
18a51d16fe9515f48f6e6b9c1dde163686f23b4cebcfff605269b73630112f1d  finalize_humanize_long_document.py
```

定向测试运行结果：相关四个测试模块共 75 项，全部通过。该结果说明现有断言没有覆盖下述攻击面，不能反证这些漏洞。

```text
python -m unittest \
  tests.test_humanize_voice_profile \
  tests.test_long_document_voice_binding \
  tests.test_prepare_humanize_long_document \
  tests.test_finalize_humanize_long_document -v

Ran 75 tests
OK
```

## 3. V12D-01：near-dedup 非传递且依赖输入顺序，可把同一证据集升级为 HIGH/PASS

严重度：P0。

### 3.1 根因

`build_humanize_voice_profile.py:767` 的 `_near_duplicate_clusters` 只把新 unit 与“当前已选 representative”比较。一个 unit 若与某个 representative 近重复，就不会进入 representative 集合，也不会成为后续 unit 的近重复邻居。

这不是对 near-duplicate 图求连通分量，也不是一个与输入排列无关的聚类算法。它是顺序敏感的贪心独立集。完整文本使用同一个函数，所以问题同时影响段落去重和 complete-unit 去重。

后续 `unique_complete_units` 直接数 `is_representative`，并用它决定 HIGH 门；feature 也只在这些 representative analysis units 上构建。因此同一文件集合在 sample spec 中换序，可以同时改变：

- 去重后作者汉字数；
- 独立分析单元数；
- 独立完整文本单元数；
- feature 的 support/opportunity/counterexample；
- `confidence`；
- `validation_status`。

validator 的 evidence rebuild 会调用同一个 builder，因而会稳定复现同一个错误结果，不能独立发现该问题。

### 3.2 最小复现构造

构造 5 份长度为 5004 汉字的完整样本：

```python
prefix = "本文说明"
base = list("".join(chr(0x4E00 + i) for i in range(5000)))
texts = [prefix + "".join(base)]

for k, start in enumerate((100, 1100, 2100, 3100), 1):
    for j in range(150):
        base[start + j] = chr(0x4E00 + 6000 + k * 200 + j)
    texts.append(prefix + "".join(base))
```

每相邻版本只累计替换一个新的 150 字区间。实测相邻版本字符 5-gram：

```text
Jaccard       = 0.9401941747572815
containment   = 0.9691753402722177
```

因此每一对相邻版本都满足当前 near 阈值。隔一个版本时：

```text
Jaccard       = 0.8838612368024132
containment   = 0.9383506805444356
```

把五个文件均声明为：

```json
{
  "origin": "USER_CONFIRMED_AUTHOR",
  "scene": "RESEARCH",
  "complete_unit": true,
  "default_role": "author",
  "role_ranges": []
}
```

只改变 sample spec 数组顺序，结果为：

| 顺序 | unique complete | 去重汉字 | confidence | validation |
|---|---:|---:|---|---|
| `[0,1,2,3,4]` | 3 | 15012 | HIGH | PASS |
| `[0,1,3,2,4]` | 2 | 10008 | MEDIUM | REVIEW |

自然顺序的 complete/analysis relation 为：

```text
UNIQUE, NEAR, UNIQUE, NEAR, UNIQUE
```

同一证据集合因此可以通过排列顺序解锁 `HIGH/PASS`。这不只是“聚类边界有争议”：任何证据度量都不应仅因 JSON 数组顺序变化而改变独立样本数和完成门状态。

### 3.3 修复要求

至少满足以下不变量：

1. 同一带身份样本集合的任意排列产生相同 dedup partition、代表数、字符数、置信等级和验证状态；
2. exact 先形成确定性簇；
3. near 关系必须使用顺序无关算法。若采用连通分量，要明确防止 revision chain 被当成独立作品；若不采用单链接连通分量，也必须声明并实现确定性的 complete-link/medoid 策略；
4. cluster ID 从稳定成员身份派生，不能从首次出现顺序派生；
5. complete-unit 和 analysis-unit 使用同一明确的独立性策略，或分别版本化并解释差异；
6. manifest 中记录 clustering algorithm/version，而不只记录阈值。

### 3.4 缺失测试

- near chain：A~B、B~C，但 A!~C；
- 五节点 revision chain 能否错误形成三个代表；
- 对同一 spec 做 20 个固定排列，核心 aggregate/Profile 语义必须一致；
- 顺序变化不能把 `REVIEW` 升成 `PASS` 或把 `MEDIUM` 升成 `HIGH`；
- exact/near 混合链；
- complete-unit 和 paragraph-unit 的 cluster 一致性；
- validator rebuild 应拒绝旧的、顺序敏感的 dedup policy 产物。

现有“三份都接近同一个 base”的测试只能覆盖星形重复，无法覆盖链式和排列攻击。

## 4. V12D-02：冻结 sample spec 未绑定，AUTHOR 可改成 MODEL_GENERATED 后继续 PASS

严重度：P1。

### 4.1 根因

prepare 会当场重建 PERSONAL 或 evidence-bound DEFAULT，并冻结：

- `voice_profile.json`；
- `voice_sample_manifest.json`；
- `voice_sample_spec.json`。

但 manifest/Profile 中没有 sample spec 的 canonical SHA。finalize 在 PERSONAL 分支只执行：

1. Profile 自哈希与 schema；
2. manifest 自哈希与 schema；
3. Profile/manifest aggregate 绑定；
4. `voice_sample_spec.json` 的 `_validate_spec` schema 检查。

它没有把 spec 与 manifest 的 sample_id、locator、origin、scene、complete_unit、default_role、role_ranges 做绑定，也没有重新构建证据。对应代码位于 `finalize_humanize_long_document.py:248/262`。

普通篡改会被 `prepare_integrity.json` 发现，但长文主链明确不把这个清单当独立信任根，并已为 units/ledger/chunks 实现“修改工件并同步重算封条仍失败”的独立重建。Voice spec 没有达到同一标准。

### 4.2 最小复现

1. 用 3 个合格 RESEARCH 作者样本建立 `PERSONAL/PASS`；
2. 正常 prepare，得到 `voice_evidence_status=REBUILT_PASS`；
3. 只修改 run 中冻结的 `voice_sample_spec.json`：

```python
for sample in frozen_spec["samples"]:
    sample["origin"] = "MODEL_GENERATED"
```

4. 只重算 `prepare_integrity.json` 中 artifact 的 bytes/SHA；
5. 不修改冻结 manifest、Profile、metadata、unit、chunk 或 ledger；
6. 给唯一 PENDING unit 提交 hash 正确的 NO_CHANGE bundle；
7. 运行 finalize。

实测：

```text
frozen spec origins                 = [MODEL_GENERATED, MODEL_GENERATED, MODEL_GENERATED]
finalization_metadata.status        = PASS
voice_binding_status                = PASS
coverage_completion_claim_allowed   = true
```

该结果使冻结证据自己声明“全部为模型生成”，而 PERSONAL Profile 与 `REBUILT_PASS` 仍被信任。

### 4.3 修复要求

优先做不可歧义的内容绑定：

- builder 对 canonical sample spec 计算 `sample_spec_sha256`；
- manifest 顶层保存该 hash；
- Profile 的 `sample_binding` 同时保存 manifest hash 和 spec hash；
- prepare metadata、完整性清单与 final metadata 贯穿该 hash；
- finalize 必须验证 frozen spec 的 canonical hash 与 manifest/Profile 均一致；
- policy hash 中加入 spec canonicalization/version；
- 对旧 schema 明确 FAIL 或迁移，不默默兼容成 PASS。

若目标是抵抗“Profile、manifest、spec 与封条一起重写”的强攻击，仅增加自哈希仍不够。需要把 prepare 的证据收据绑定到代理无法自行伪造的信任根，或冻结可独立重建所需的来源字节/外部签名 receipt。当前至少应先关闭“只改 spec 即通过”的明显缺口。

### 4.4 缺失测试

- spec origin AUTHOR -> MODEL_GENERATED 后自重封必须 FAIL；
- spec locator、scene、complete_unit、default_role、role_ranges 分别漂移；
- spec 文件替换但 schema 合法；
- evidence-bound DEFAULT 的同类攻击；
- manifest/Profile 不变、spec 顺序变化时的 canonical 绑定；
- final metadata 中 spec hash、manifest hash、Profile hash 三者均可追踪；
- 同时修改 spec 与 integrity manifest 的红队用例。

## 5. V12D-03：纯 COURSE 样本可重标为 RESEARCH/PASS

严重度：P1。

### 5.1 根因

builder 的 `binding_scene` 逻辑是：

```python
binding_scene = scene
if scene == "AUTO":
    binding_scene = sample_scenes[0] if len(sample_scenes) == 1 else "GENERAL"
```

当调用方显式给 `--scene RESEARCH` 时，样本实际场景不会限制 binding scene。`validate_profile_object` 只检查：

- `binding_scene` 是合法枚举；
- `defaults.scene == binding_scene`；
- feature scope 自身是合法枚举。

它不检查 `binding_scene` 是否在 `sample_binding.sample_scenes` 中，也不检查 `feature.scope` 与目标 binding scene 是否兼容。prepare 新增的 `voice_profile_scene_mismatch` 只比较“请求 RESEARCH”和“Profile 标签 RESEARCH”，因此无法发现标签本身是由 COURSE 证据重标得到的。

### 5.2 最小复现

使用 3 个 400 汉字样本：

```text
本文说明 + 甲/乙/丙重复 396 次
```

每个 sample 均声明：

```json
{
  "origin": "USER_CONFIRMED_AUTHOR",
  "scene": "COURSE",
  "complete_unit": true,
  "default_role": "author"
}
```

构建时显式传 `scene="RESEARCH"`。实测 Profile：

```text
validation_status      = PASS
binding_scene          = RESEARCH
sample_scenes          = [COURSE]
feature scopes         = [[COURSE], [COURSE]]
```

随后 prepare 使用 `scene=RESEARCH`，结果：

```text
status                 = READY
voice_evidence_status  = REBUILT_PASS
profile_binding_scene  = RESEARCH
```

这使“场景绑定”退化为调用方可写标签，而不是证据支持的属性。

### 5.3 修复要求

建议将“Profile 的证据场景”和“本次目标场景”分开：

- `evidence_scenes`：从 manifest 重建，不受 CLI 覆盖；
- `target_scene`：调用场景；
- `scene_transfer_status`：`SAME_SCENE/GLOBAL_STABLE/REVIEW/REJECTED`；
- 每个 feature 的 scope 必须决定它能否在目标场景应用；
- 纯 COURSE feature 不得因 CLI 标签变成 RESEARCH feature；
- 跨场景迁移若被允许，只能发布已在至少两个场景独立支持的 GLOBAL feature，其余进入 REVIEW 或被剔除；
- builder 不得把没有目标场景证据的 Profile 标为目标场景 `PASS`。

### 5.4 缺失测试

- COURSE-only samples + explicit RESEARCH；
- RESEARCH-only samples + explicit COURSE；
- COURSE-only + explicit GENERAL；
- 多场景 sample 中 feature 只由单场景支持；
- `AUTO` 多场景回退 GENERAL 时，非 GLOBAL feature 不得静默进入 PASS；
- prepare 不能只靠伪造后的 binding label 放行。

## 6. V12D-04：validator 顶层 PASS 与证据重建状态混在一起

严重度：P2；当前 prepare 主链有额外防护，未复现为主链绕过。

`validate_humanize_voice_profile.py` 允许只传 Profile，不传 manifest/spec/root/rebuild。此时只要 Profile 自哈希/schema 有效且内部 `validation_status=PASS`，输出仍是：

```json
{
  "status": "PASS",
  "manifest_validated": false,
  "evidence_rebuilt": false
}
```

进程退出码仍为 0（`validate_humanize_voice_profile.py:442`）。对熟悉合同的调用方，这可以解释为“Profile 工件结构有效”；但字段名 `status=PASS` 与文档中“只有 validator PASS/0 才进入 prepare”的表述容易让下游只读一个状态位。

prepare 当前会对 PERSONAL 和 evidence-bound DEFAULT 强制重建，因此主链未被这一点直接绕过。仍建议把状态拆分为：

```text
artifact_validation_status
manifest_binding_status
evidence_rebuild_status
delivery_gate_status
```

对于 PERSONAL：未传 manifest 或未重建时，顶层 delivery gate 应为 `REVIEW`/退出码 2；只有明确的 `--structural-only` 模式才允许结构检查成功但不形成可消费 PASS。

缺失测试：

- PERSONAL/PASS profile-only 调用不得形成可消费的顶层 PASS；
- `manifest_validated=false` 与 `evidence_rebuilt=false` 时退出码语义；
- 结构验证与生产准入状态不可复用同一字段；
- 调用方只读取 `status` 的契约测试。

## 7. 已确认正确的边界

以下部分在本轮代码和定向测试中表现正确：

- prepare 拒绝 `validation_status != PASS` 的 supplied PERSONAL；
- prepare 拒绝请求场景与 Profile 标签的直接错配；
- PERSONAL 与 evidence-bound DEFAULT 缺 manifest/spec/root 时拒绝；
- deterministic scene DEFAULT 无证据时可重建并保持披露；
- Profile 自哈希、manifest 自哈希和 Profile/manifest aggregate 绑定存在；
- rewrite bundle 缺失、非法或错配 Profile hash 时 unit 保持 UNRESOLVED；
- finalize 输出的 `voice_profile_manifest_sha256` 已读取 Profile 中真实 manifest hash，不再误写 Profile hash；
- `voice_binding_status=PASS` 不会把 `voice_conformance_status` 升成 PASS；
- `humanize_completion_claim_allowed/full_completion_claim_allowed` 仍固定为 false；
- AUTO 在长文链中仍为 `scene_routing_status=NOT_EVALUATED`；
- PENDING、UNRESOLVED、乱码、活动文件变化和硬失败仍阻止 coverage 完成声明。

## 8. 建议修复顺序

1. 先修 V12D-01。它是当前唯一已复现、无需篡改 run 工件即可把 REVIEW/HIGH 门改变为 PASS 的问题。
2. 再修 V12D-02，把 sample spec hash 纳入 manifest/Profile/run/final metadata，并加入自重封回归测试。
3. 修 V12D-03，拆开 evidence scene 与 target scene，禁止 CLI 对证据场景进行无条件重标。
4. 修 V12D-04，拆分 validator 的结构状态与生产准入状态。
5. 修复后同时运行顺序性质测试、三类最小红队复现、四个定向模块和全量测试；不要只增加单个 happy-path 断言。

## 9. 生产准入判定

当前判定：`NOT_READY`。

可以诚实声称：

> supplied Profile 的自哈希、直接场景标签、prepare 冻结和 rewrite hash 回显已经接通；Humanize 完成字段仍被保守关闭。

暂时不能声称：

> complete-unit 独立性与 HIGH 置信门已经可靠；PERSONAL 证据在 prepare 后不可伪造；Profile binding scene 一定由同场景语料支持；validator 的 PASS 一定表示生产可消费。

