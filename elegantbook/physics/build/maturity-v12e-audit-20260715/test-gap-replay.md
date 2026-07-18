# Voice Profile v12e 最小复现独立重放

日期：2026-07-15  
方式：不调用新增单元测试，不依赖测试断言；直接导入当前生产脚本，并对 finalize / validator 的 CLI 入口做独立临时目录重放。除本报告外未修改生产脚本、测试或固定工件。

## 结论

上一轮发现的三条 `PASS` 旁路在当前最新版均已关闭：

1. 正常 UTF-8 BOM rewrite bundle 仍被 strict JSON 正常接受，最终 `PASS/0`；
2. 重复 `voice_profile_sha256` 键不再采用 last-key-wins，错误 hash 在前、正确 hash 在后也会被直接拒绝，不会降格为 `PASS`；
3. COURSE 证据显式重标为 RESEARCH 现在保持 `REVIEW/2`，prepare 拒绝消费；
4. near-duplicate 传递链现在归为一个连通分量，正序/逆序结果一致，不再解锁 `HIGH/PASS`。

## 重放版本固定

开始与结束时分别计算四个生产脚本的 SHA-256；前后完全一致，说明重放期间实现未漂移。

| 脚本 | SHA-256 |
|---|---|
| `build_humanize_voice_profile.py` | `4bac5595c0fedf17bca7a790446f9cab37e7baef3f96663c6b78d3e6255ef7a0` |
| `validate_humanize_voice_profile.py` | `ead741fe5209ce150a7b51497d2eb3ce6cfec9e87fb052c86800607d0bb83c22` |
| `prepare_humanize_long_document.py` | `3c748c4fe5a580044581a37f69e854c42022db5cf4a09ea265a09c28d3491e43` |
| `finalize_humanize_long_document.py` | `eedf48d3cdb5d3631e0807cb5d12299e4cff26f18ab8290d435292e0d0d31ee4` |

`script_hashes_stable_during_replay=true`。

## 1. 正常 BOM bundle：strict JSON 未误伤

### 工件

从 prepare 产生一个 RESEARCH / DEFAULT 的 `PENDING` Markdown unit，写入标准 `NO_CHANGE` JSON，并用 `utf-8-sig` 保存，确认文件前三字节为 `EF BB BF`：

```json
{
  "decision": "NO_CHANGE",
  "reason": "该段保持原有的简短判断",
  "voice_profile_sha256": "<chunk 中的精确 hash>"
}
```

随后直接运行：

```text
python finalize_humanize_long_document.py --run-dir <temp-run> --rewrites <temp-rewrites>
```

### 当前结果

```text
has_utf8_bom=true
returncode=0
status=PASS
voice_binding_status=PASS
unit_statuses={NO_CHANGE: 1}
rendered_exists=true
stderr=""
```

结论：`utf-8-sig` 解码仍兼容 PowerShell 常见 BOM 输出；strict JSON 修复没有误拒绝正常 BOM bundle。

## 2. 重复 Voice hash key 攻击：已拒绝，不再 PASS

### 攻击工件

原样重放“错误 hash 在前、正确 hash 在后”的攻击：

```json
{
  "decision": "NO_CHANGE",
  "reason": "该段保持原有的简短判断",
  "voice_profile_sha256": "0000000000000000000000000000000000000000000000000000000000000000",
  "voice_profile_sha256": "27bc2f98075de1183522db6025dd20899d4fd0a2ab2383887b987a691c08fe78"
}
```

### 生产加载路径结果

直接调用 finalize 实际使用的 `_rewrite_bundle()`：

```text
accepted=false
error_type=ValueError
error=invalid strict JSON ...: duplicate JSON key: voice_profile_sha256
```

再走 finalize CLI：

```text
returncode=2
stdout_json=false
status=<none>
stderr contains "duplicate JSON key: voice_profile_sha256"
rendered_exists=false
finalization_metadata_exists=false
```

该 CLI 返回码来自 argparse 的结构错误出口；关键结果是执行在 bundle 收集阶段终止，没有 unit 进入正文 validator，没有发布派生稿，也没有产生任何 `PASS` 元数据。

### BOM 与重复键组合

把同一重复键攻击文件改为 `utf-8-sig` 后再次调用生产加载路径，结果仍为：

```text
ValueError: invalid strict JSON ...: duplicate JSON key: voice_profile_sha256
```

因此 BOM 兼容不会成为重复键旁路。

## 3. 跨场景最小复现：COURSE 证据不能再冒充 RESEARCH/PASS

### 工件

- 三个合格作者样本；
- 每个 sample spec 项均声明 `scene=COURSE`；
- builder 显式请求 `scene=RESEARCH`；
- 样本文本足以产生正向 feature 与 negative control。

### builder 当前结果

```text
profile.binding_scene=RESEARCH
sample_binding.sample_scenes=[COURSE]
feature scopes=[[COURSE], [COURSE], [COURSE]]
profile.validation_status=REVIEW
personal_voice_claim_allowed=false
```

builder 仍保留请求的绑定场景与原始 feature scope，便于审计，但不会把这组错场景证据升级为可消费的 PERSONAL/PASS。

### 独立 validator 当前结果

使用 manifest、sample spec、allowed root 与 `--rebuild-evidence` 运行生产 validator：

```text
returncode=2
status=REVIEW
production_admission_status=REVIEW
production_admission_reason=PROFILE_STATUS_NOT_PASS
evidence_rebuilt=true
```

这说明即使证据可以按字节完整重建，错场景仍不会被证据完整性覆盖。

### prepare 消费结果

将上述 Profile/manifest/spec 提交给 RESEARCH prepare：

```text
accepted=false
error_type=ValueError
error=voice_profile_status_not_pass
run_created=false
```

结论：跨场景旁路在 builder、validator 生产准入与 prepare 消费三层均保持非 PASS。

## 4. near-chain 最小复现：连通分量聚类生效

### 工件

复用上一轮五个完整样本的链式构造：每个样本约 2010 个作者汉字，相邻版本只替换一个 60 字区间，使 `A~B`、`B~C`、`C~D`、`D~E` 均达到 near 阈值，而非相邻端点不一定直接达到阈值。

分别用正序 `[A,B,C,D,E]` 和逆序 `[E,D,C,B,A]` sample spec 调用当前 builder。

### 正序结果

```text
unique_analysis_units=1
unique_complete_units=1
readable_author_chars=2010
exact_duplicate_units=0
near_duplicate_units=4
all complete-unit cluster IDs=cluster-000001
confidence=MEDIUM
validation_status=REVIEW
feature_count=0
negative_control_count=1
```

当前确定性代表样本为 `s2`；其余四项均为 `NEAR`。代表选择不再依赖最先出现的样本。

### 逆序结果与顺序不变量

```text
aggregate_equal=true
cluster_mapping_equal=true
relation_mapping_equal=true
confidence_equal=true
status_equal=true
```

逆序仍得到同一个 `cluster-000001`、同一个代表映射、`MEDIUM/REVIEW`。上一轮的 `unique_complete_units=3`、`readable_author_chars=6030`、`HIGH/PASS` 已不可复现。

## 最终判定

| 重放项 | 当前判定 |
|---|---|
| 正常 BOM strict JSON bundle | `PASS/0`，兼容性正常 |
| 重复 `voice_profile_sha256`，错误在前正确在后 | strict JSON 拒绝，非 PASS，无发布 |
| BOM + 重复 hash key | strict JSON 拒绝，非 PASS |
| COURSE-only 证据重标 RESEARCH | builder/validator 为 `REVIEW/2`，prepare 拒绝 |
| 五项 near-chain | 单连通簇，顺序无关，`MEDIUM/REVIEW` |

本次独立重放没有发现这三项旧旁路在当前脚本哈希下复发。
