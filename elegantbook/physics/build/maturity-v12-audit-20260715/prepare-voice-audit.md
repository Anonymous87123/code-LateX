# prepare 阶段 hash-bound Voice Profile 接线审计

## 范围与结论

本审计只依据 `references/long-document-workflow.md` 与 `scripts/prepare_humanize_long_document.py`。未检查 finalize 或其他脚本，因此下文能确定 prepare 侧应写出的合同，不能证明下游已经消费或复核这些字段。

当前工作流要求每个 unit 绑定 Voice Profile，并将 `voice_binding_status` 作为 Humanize 完成门的一部分；同时明确当前尚未实现 hash-bound Voice Profile。prepare 实现目前没有 Voice CLI、Voice 快照或 Voice 字段：`build_parser()` 只有输入、输出、场景、预算和样式包装参数；`prepare()` 与 `build_units()` 不接收 Voice；`run_metadata.json`、`units.jsonl`、chunk、`coverage_ledger.csv` 均未记录 Voice；`build_integrity_manifest()` 也未封存 Voice 字节。故当前只能继续保持 `humanize_completion_claim_allowed=false`，不得把 scene-default 或调用方路径描述为已绑定 Profile。

## 最小接线面

### 1. CLI 与单次冻结

在 `build_parser()` 增加一对必须同时出现的参数：

- `--voice-profile <path>`
- `--voice-profile-sha256 <64 位十六进制摘要>`

不应只接受路径后自行计算摘要：那只能标识“prepare 当时读到的内容”，不能证明读到的是调用方指定版本。`main()` 应先校验参数成对出现、摘要格式合法，再传入 `prepare()`。未提供二者时合法回退 `SCENE_DEFAULT`。

新增 `freeze_voice_profile(path, expected_sha256, allowed_roots, output)`（名称可调整），职责固定为：解析并校验路径、拒绝非普通文件和输出目录内路径、通过同一已打开句柄取得文件身份与长度、完整读取、复核短读和读前/读后文件身份、计算 SHA-256、与期望摘要比较，最后把同一批内存字节写入 run staging 下的 Voice 快照。不得在校验后重新按路径读取一次。

`prepare()` 签名最少增加 `voice_profile: Path | None` 与 `voice_profile_sha256: str | None`；安全模式还应增加可重复的 `allowed_roots: Sequence[Path]`。Voice 冻结失败属于全局配置硬失败，不能像单个源文件乱码那样继续生成 `READY` run。

### 2. 统一绑定对象与精确字段

由冻结结果建立唯一 `voice_binding`，摘要本身作为不可变版本，不再信任独立的自由文本版本号：

```json
{
  "voice_profile_mode": "SUPPLIED",
  "voice_profile_id": "VP-<sha256前16位>",
  "voice_profile_version": "sha256:<完整摘要>",
  "voice_profile_sha256": "<完整摘要>",
  "voice_profile_bytes": 123,
  "voice_profile_snapshot": "voice/profile.bin",
  "voice_profile_source_path": "<规范化绝对路径>",
  "voice_profile_confidence": "NOT_EVALUATED",
  "voice_binding_status": "BOUND"
}
```

未提供 Profile 时统一写：`voice_profile_mode=SCENE_DEFAULT`、`voice_profile_id=SCENE_DEFAULT`、`voice_profile_version=NONE`、`voice_profile_sha256=NONE`、`voice_profile_confidence=NOT_EVALUATED`、`voice_binding_status=SCENE_DEFAULT`。prepare 不负责判断声线符合性，因此不能把 confidence 或 conformance 写成 `PASS`。

接线位置如下：

| 位置 | 最小改动 |
|---|---|
| `build_units()` | 增加 `voice_binding` 参数；每个 unit 写 `voice_profile_id`、`voice_profile_version`、`voice_profile_sha256`、`voice_profile_confidence`、`voice_binding_status`。 |
| chunk 写出循环 | chunk 目前复制 unit 字段；unit 加字段后会自然进入 `chunks/<unit_id>.json`，无需第二套拼装逻辑。应保留全长摘要，不能只用 12/16 位短 ID 作安全比较。 |
| `units.jsonl` | `public_units` 由 unit 复制，字段会自然进入；不得在 public projection 中删掉 Voice 绑定字段。 |
| `coverage_ledger.csv` | 在 `ledger_fields` 明确加入上述五个 unit 级字段，否则 CSV 会因 `extrasaction="ignore"` 静默丢弃它们。 |
| `run_metadata.json` | 写入完整 `voice_binding` 对象，并另写 `voice_binding_status`；`completion_claim_allowed` 仍为 false。绝对源路径只需出现在 metadata，不要在每个 unit 重复。 |
| Voice 快照 | 写入固定相对路径，例如 `voice/profile.bin`；内容必须是计算期望摘要时的同一字节串。 |
| `build_integrity_manifest()` | 增加显式 `extra_artifacts`/`voice_snapshot` 参数，把 Voice 快照列入 `artifacts`。`run_metadata.json`、units、ledger 和 chunks 已在现有封条范围内，因而其重复字段也被逐文件封存。 |

`prepare_integrity.json` 中 Voice 快照条目至少包含 `path`、`sha256`、`bytes`。下游还必须从 Voice 快照重新计算摘要，并要求它与 run metadata、每个 unit、对应 chunk、ledger 行完全一致；只验证这些文件各自与封条一致，不足以发现攻击者同时改写全部产物并重算封条。

### 3. 明确失败态

建议使用稳定错误码，并把下列情况作为 `FAIL`（CLI 退出码 1），不发布可用 run：

- `VOICE_PROFILE_ARGUMENT_INCOMPLETE`：路径与期望摘要未成对提供；
- `VOICE_PROFILE_HASH_INVALID`：摘要不是规范的 64 位 SHA-256；
- `VOICE_PROFILE_NOT_REGULAR_FILE`：缺失、目录、设备或不允许的链接/重解析点；
- `VOICE_PROFILE_PATH_OUTSIDE_ALLOWED_ROOT`：规范路径或句柄最终路径越出授权根；
- `VOICE_PROFILE_OUTPUT_OVERLAP`：Profile 位于输出/staging 树内；
- `VOICE_PROFILE_SHORT_READ`：读取字节数与固定长度不等；
- `VOICE_PROFILE_CHANGED_DURING_READ`：文件身份、长度或时间戳在冻结窗口变化；
- `VOICE_PROFILE_HASH_MISMATCH`：实际摘要与调用方期望摘要不同；
- `VOICE_PROFILE_SNAPSHOT_MISMATCH`：写出的快照回读摘要或长度不符；
- `VOICE_PROFILE_INTEGRITY_OMITTED`：Voice 快照未进入 `prepare_integrity.json`。

当前 `main()` 通过 `parser.error()` 把配置/IO 硬错误也变成退出码 2，而正常 `REVIEW` 同样返回 2。Voice 接线若要提供可机读失败态，应单独捕获带错误码的异常，输出 `status=FAIL` 并返回 1，避免把全局绑定失败混同为可继续复核的 `REVIEW`。

## TOCTOU 与路径越界攻击面

1. **`stat -> open/read -> stat` 不是稳定文件身份。** `prepare()` 先 `path.stat()`，再由 `read_fixed_bytes()` 重新按路径打开，最后再次 `stat()`；链接、目录重解析点或目标可在窗口内切换。相同大小且恢复 mtime 的替换也可能逃过当前 `changed` 判定。Voice 必须基于同一句柄的读前/读后 `fstat`/文件 ID，并由调用方期望 SHA 作最终内容绑定。
2. **短读未失败。** `read_fixed_bytes()` 只调用一次 `read(length)`；当前代码会记录 `readable_bytes`，但不要求等于固定长度。对 Voice 必须循环读满或以 `VOICE_PROFILE_SHORT_READ` 失败。
3. **seed/include 可越出文档根。** `collect_seed_paths()` 对显式文件/目录直接 `resolve()`；`_directory_inputs()` 接受解析后位于根外的文件链接；`discover_tex_includes()` 将文档控制的相对路径 `resolve()` 后直接入队，没有根包含检查，也没有对显式后缀再次限制。恶意 TeX 可借 `../`、符号链接或 Windows junction 把任意可读文件带入 `source/`。应由一个共同的 `allowed_roots` 策略约束 seed、递归发现、include 与 Voice；未提供根时记录 `path_isolation_status=UNVERIFIED`，不得宣称隔离。
4. **只做字符串 `resolve()` 不足以阻断重解析点竞态。** 检查 containment 后到打开之间仍可更换中间目录链接。需在支持的平台使用 no-follow/目录句柄逐段打开，或至少比较打开句柄的最终规范路径与文件 ID；Windows 上应显式拒绝未授权 reparse point。
5. **输出目录存在检查有竞态。** `prepare()` 先检查空目录，再以 `exist_ok=True` 创建；并发进程可在检查后注入 `source`、`chunks` 或目标文件。安全最小实现应在同级创建独占随机 staging 目录，所有写入、复核和封条完成后原子发布；目标输出已存在即拒绝。
6. **完整性清单生成期间可被改写。** `build_integrity_manifest()` 顺序读取并哈希各产物，但没有 run 锁或原子发布；较早哈希的文件可在封条写出前改变。staging 独占与原子发布是必要边界，封条写完后还应保持目录不可被并发 prepare 复用。
7. **封条不是外部信任根。** 工作流已明确 `prepare_integrity` 只是审计辅助。若攻击者可同时修改 Voice 快照、metadata、units、chunks、ledger 并重算封条，纯本地自封不能证明最初调用方意图；必须保留 CLI 的 expected SHA，并由下游从冻结 Voice 字节重建全部绑定关系。更高信任等级需要外部签名/receipt，不应由 prepare 自称。
8. **路径信息扩散。** 当前 snapshot/manifest 已保存绝对源路径；Voice 的绝对路径只应在 run metadata 保留一次。unit/chunk/ledger 使用内容 ID 与摘要，减少路径泄漏和路径字符串差异造成的伪不一致。

## 接受条件

- supplied Profile 的实际字节、调用方期望 SHA、Voice 快照 SHA 完全一致；
- 所有 unit、chunk、ledger 行与 run metadata 引用同一完整 SHA 和版本；
- `prepare_integrity.json` 同时封存 Voice 快照及所有含绑定字段的产物；
- 任一绑定字段缺失或不一致均为全局 `FAIL`，不能产生 `READY`；
- 未提供 Profile 时所有产物一致声明 `SCENE_DEFAULT`，不得伪称 hash-bound；
- prepare 仍固定 `completion_claim_allowed=false`；在下游实际完成 Voice 绑定复核、声线符合性和其他全局门前，`humanize_completion_claim_allowed` 必须保持 false。
