# 短 PATCH 复核报告

## 1. 任务边界与配置

- source: `tests/fixtures/humanize_forward_v10/research_before.md`
- source SHA-256: `348026b7b26c646e67e809285ea11881865a3d35193a4131ff850813582c4d71`
- mode: `REWRITE`
- scene: `RESEARCH`
- scan scene: `AUTO`
- intensity: `BALANCED`
- requested output: `PATCH`
- effective output: `PATCH`
- source kind: `DOCUMENT`
- document format: `MARKDOWN`
- report context: `NONE`
- voice profile: `NONE`
- voice disclosure: `SCENE_DEFAULT`，不声称复现个人文风
- protected terms: `[]`
- structure: 标题、段序和第二段锁定为原样；补丁只处理第一段局部跨度
- source 修改: 未修改；verifier 的 `--live-source` 检查通过
- authoritative record: `short-patch-review-current/`
- 读取边界: 仅读取当前 Skill、给定 source 和本次新建输出目录；未读取其他 build 工件、成熟度报告、测试文件或期望

本报告只说明待审候选的机械结构、覆盖与本地 A/B 复核。它不判断学术正确性、作者身份、检测结果或完整自然语言语义。

## 2. AUTO 扫描与 create 结果

source 的 AUTO audit view 共枚举 3 个 candidate high：

| finding | signal | UTF-8 bytes | source text | disposition |
|---|---|---:|---|---|
| `LF-6d7e1ab9737ae26025600b57` | `LEX-MARKET-01` | `199:217` | `具有重要意义` | `H002 / DELETE_STYLE_SHELL` |
| `LF-c65c481b9b6b8d96ce5b3aa3` | `LEX-EMPH-01` | `220:238` | `值得注意的是` | `H003 / REWRITE` |
| `LF-3d4311d0221fde3bd287e0d7` | `LEX-FOUNDATION-01` | `310:337` | `为后续研究奠定基础` | `H003 / REWRITE` |

另有 `系统梳理`、`深入探讨` 两个 medium 候选。它们不属于 coverage high 计数，但位于 `H003` 的完整句义范围内，随成束包装一并压缩。

`create` 状态：`PENDING high=3 resolutions=3 suggestions=6 suppressed=0`。

### create 自动建议 inventory

| suggestion | status | variant | span | UTF-8 bytes | source text | 实际引用 |
|---|---|---|---|---:|---|---|
| `SG001` | `AVAILABLE` | `LEFT_DELIMITER` | `A004` | `193:217` | `，也具有重要意义` | 是，`H002/S002` |
| `SG002` | `AVAILABLE` | `CORE` | `A005` | `196:217` | `也具有重要意义` | 否 |
| `SG003` | `AVAILABLE` | `CORE` | `A002` | `220:238` | `值得注意的是` | 否 |
| `SG004` | `AVAILABLE` | `RIGHT_DELIMITER` | `A006` | `220:241` | `值得注意的是，` | 否 |
| `SG005` | `AVAILABLE` | `LEFT_DELIMITER` | `A007` | `307:337` | `，为后续研究奠定基础` | 否 |
| `SG006` | `AVAILABLE` | `CORE` | `A003` | `310:337` | `为后续研究奠定基础` | 否 |

`SUPPRESSED` 建议为 0；没有 protected overlap、技术豁免或 byte 上限导致的抑制。

实际只引用 `SG001/A004`。`H003` 没有分别引用 `A006/A007`，因为分别删除会留下割裂的作者动作句；改用一个手工完整句 span，在同一 hunk 内同时保留作者动作和“可能”模态。调用方没有把多个 boundary variant 同时用于同一 finding。

### 手工新增 span

| span | UTF-8 bytes | source text | 用途 |
|---|---:|---|---|
| `A008` | `142:193` | `这个结果说明参数变化会影响系统表现` | `H001/S001`；将证据强度问题原样登记为 `UNRESOLVED` |
| `A009` | `220:340` | `值得注意的是，本文系统梳理了相关现象，并深入探讨了可能原因，为后续研究奠定基础。` | `H003/S003`；以完整句义边界改写 |

两个手工 span 均使用 `finding_ids=[]`，没有伪装成自动 high span。

## 3. Hunk、selection、reason 与 conflict

`patch_hunks_source_partition=NON_OVERLAPPING`，hunk 按 source byte 起点递增。

### H001 / S001

- span: `A008`, bytes `142:193`
- decision: `UNRESOLVED`
- before/after: `这个结果说明参数变化会影响系统表现`
- hunk reason: 该影响主张的证据强度不能由纯文风层裁定；原样保留，不改成相关性描述或更强结论。
- selection reason: 连续阅读发现该影响主张涉及证据强度，纳入补丁并原样保留为语义未决。
- predicate source: `COPY`

### H002 / S002

- span: `A004`, bytes `193:217`
- decision: `DELETE_STYLE_SHELL`
- before: `，也具有重要意义`
- after: 空字符串
- hunk reason: 删除未提供具体对象、后果或范围的空泛价值宣告，同时保留前面的结果主张。
- selection reason: 用户要求覆盖全部 AUTO high；该 span 精确包含空泛价值宣告及其左分隔符。
- predicate source: `DELETE_STYLE_SHELL`

### H003 / S003

- span: `A009`, bytes `220:340`
- decision: `REWRITE`
- before: `值得注意的是，本文系统梳理了相关现象，并深入探讨了可能原因，为后续研究奠定基础。`
- after: `本文梳理了相关现象，讨论了可能原因。`
- hunk reason: 保留梳理现象、讨论可能原因的作者动作与可能性模态，删除空重点壳、成束学术包装和无具体信息的后续桥接。
- selection reason: 该整句同时覆盖两个 AUTO high 与相邻成束包装，按最小完整句义边界改写。
- predicate source: `ENTAILED_PARAPHRASE + DELETE_STYLE_SHELL`

### Conflict inventory

- `explicit_conflicts=[]`
- conflict pair count: 0
- 未发现可确定的正反许可、互斥条件、相反结论或不兼容 scope 对，因此没有填写 `rule_code/left_hunk_id/right_hunk_id`。
- `H001` 是证据强度的语义未决，不是调用方声明的源文冲突对。

## 4. A/B 复核

原第一段承担三项职责：报告两组差异、保留参数影响主张、说明本文对现象和可能原因的处理。候选保留了三项职责；只删除空泛价值宣告、重点提示壳和无具体信息的后续桥接。

- 数字、组别、比较方向和观察均未变化。
- `这个结果说明参数变化会影响系统表现` 原样保留并显式标记 `UNRESOLVED`，没有擅自改写其因果或证据强度。
- `可能原因` 的可能性模态保留。
- 第二段逐字复制；`只`、`没有`、`不能` 及边界条件/初始状态两个备选原因均未变化。
- 未新增作者、机构、年份、引文、数据、实验条件、工程用途或未来工作。
- 未新增主语错位、硬被动、动宾不搭配、同构短句串或修复模板。
- 每个改动对应已登记病灶，不以“更正式/更书面/更短”作为独立收益。
- candidate 的独立 AUTO 复扫为 0 findings；统一验证器记录 `after_candidates=0`、`unexplained_high_candidates=0`、`introduced_candidates=0`。

本地 A/B 复核只能否决或回退候选，不能签发 paired-quality clearance。本次未回退 `H002/H003`，但交付仍保持 `PENDING_EXTERNAL_REVIEW`。

## 5. 命令与状态

路径别名：

```powershell
$skill = 'C:\Users\Lenovo\.codex\skills\humanize-academic-chinese'
$source = 'D:\code LateX\elegantbook\physics\tests\fixtures\humanize_forward_v10\research_before.md'
$out = 'D:\code LateX\elegantbook\physics\build\maturity-v39-fresh-user-final-20260719'
```

### Source AUTO 扫描

```powershell
python "$skill\scripts\scan_humanize_chinese.py" $source --scene AUTO --format json --output "$out\scan.auto.json"
python "$skill\scripts\scan_humanize_chinese.py" $source --scene AUTO --format text
```

状态：进程 `0`；3 个 high、2 个 medium candidate。

### Authoring create

```powershell
python "$skill\scripts\scaffold_humanize_short_patch.py" create $source --requested-output PATCH --scene RESEARCH --intensity BALANCED --source-kind DOCUMENT --suggest-spans CLAUSE --document-format MARKDOWN --output "$out\selection.authoring.current.json" --format text
```

状态：进程 `0`；`PENDING high=3 resolutions=3 suggestions=6 suppressed=0`。这是待填写 scaffold，不是 bundle 或交付 PASS。

### Authoring finalize

```powershell
python "$skill\scripts\scaffold_humanize_short_patch.py" finalize $source --authoring "$out\selection.authoring.current.json" --document-format MARKDOWN --output "$out\selection.v2.current.json" --format text
```

current 运行状态：进程 `0`，`FINALIZED hunks=3 selected=3`。

初始 policy 下曾有一次 authoring 校验失败：进程 `1`，`lexical_resolutions[0].reason must be null for HUNK`。未生成 selection；随后只把三个 HUNK resolution 的冗余 reason 改为 `null`，具体理由仍保留在 hunk/selection。安装版随后更新，该初始记录不作为最终 current 记录。

### Bundle build

```powershell
python "$skill\scripts\build_humanize_short_patch.py" $source --selection-spec "$out\selection.v2.current.json" --document-format MARKDOWN --output "$out\patch.bundle.current.json" --format text
```

状态：进程 `0`；`BUNDLED hunks=3`；bundle SHA-256 `2ff143ebdb3930fb89ae485d1e8ff5ab4d9700d57cbadab1c70be5148fdd21cc`。这不是交付 PASS。

### Strict apply

```powershell
python "$skill\scripts\apply_humanize_short_patch.py" $source --bundle "$out\patch.bundle.current.json" --output "$out\short-patch-review-current" --format text
```

实际观察到子进程 `2`；脚本权威首行：`DELIVERY REVIEW exit=2`。闭集 `result.json` 同时记录 `delivery_gate_status=REVIEW`、`delivery_gate_exit_code=2`、`exit_code=2`。

### Verify + live source

```powershell
python "$skill\scripts\verify_humanize_short_patch.py" "$out\short-patch-review-current" --live-source $source --format text
```

状态：实际观察到子进程 `0`；`INTEGRITY PASS scope=SELF_CONSISTENCY_ONLY`、`CURRENT_POLICY_REPLAY PASS`、`COVERAGE PASS`、live source match；候选交付仍为 `DELIVERY REVIEW`。

初始闭集 `short-patch-review/` 曾在生成时通过 verifier；本轮中 `SKILL.md`、`short-patch-workflow.md` 和 builder 被外部更新后，它被 verifier 正确降为 `POLICY_DRIFT/REVIEW/2`，闭集与 coverage replay 仍自洽但 current-policy replay 未运行。按合同保留该旧记录且不改写 validation/manifest，随后从 source 重建了本报告的 current 权威闭集。

### Candidate AUTO 复扫

```powershell
python "$skill\scripts\scan_humanize_chinese.py" "$out\short-patch-review-current\candidate.review.md" --scene AUTO --format json --output "$out\scan.candidate.auto.json"
python "$skill\scripts\scan_humanize_chinese.py" "$out\short-patch-review-current\candidate.review.md" --scene AUTO --format text
```

状态：进程 `0`；0 findings。

## 6. 逐层最终状态

| layer | status | scope / note |
|---|---|---|
| scaffold create | `PENDING` | 3 high、6 available、0 suppressed |
| scaffold finalize | `FINALIZED/0` | 3 hunk、3 selection |
| bundle build | `BUNDLED/0` | source/selection/coverage 冻结 |
| structural validation | `PASS` | 3 hunk 非重叠、有序 |
| patch application | `PASS` | unlisted source `COPY_EXACT` |
| candidate assembly | `PASS/0` | candidate 由 bundle 确定性派生 |
| hard invariant | `PASS` | 无 errors/warnings/advisories |
| speech act | `PASS` | `可能/只/没有/不能` 未漂移 |
| style signal | `PASS` | after candidate 0，unexplained high 0 |
| mechanical validation | `PASS/0` | 不等于交付或质量 PASS |
| coverage | `PASS` | `ENUMERATED_HIGH_AND_BOUND_DECLARATIONS_ONLY` |
| current-policy replay | `PASS` | 同 policy 核心结果可重放 |
| integrity verifier | `PASS/0` | `SELF_CONSISTENCY_ONLY` |
| live source | `MATCH` | source 仍对应归档记录 |
| semantic judgment | `NOT_EVALUATED` | `H001` 原样 `UNRESOLVED` |
| semantic completeness | `false` | 不证明完整语义发现 |
| academic correctness | `NOT_EVALUATED` | 未运行学术质控 |
| paired quality | `PENDING_EXTERNAL_REVIEW` | 无可信外部 clearance |
| delivery gate | `REVIEW/2` | 合法待审 PATCH 候选 |
| humanize quality claim | `false` | 不得声称已完成 Humanize |

## 7. 工件

顶层 authoring/audit 工件：

- `scan.auto.json`
- `selection.authoring.current.json`
- `selection.v2.current.json`
- `patch.bundle.current.json`
- `selection.authoring.json`
- `selection.v2.json`
- `patch.bundle.json`
- `scan.candidate.auto.json`
- `review-report.md`

`short-patch-review-current/` 是当前安装版 verifier 校验过的权威闭集：

- `source.snapshot.bin`
- `candidate.review.md`
- `review.md`
- `patch.diff`
- `patch.bundle.json`
- `coverage.json`
- `validation.json`
- `result.json`
- `evidence-manifest.json`

`short-patch-review/` 是保留不动的旧 policy 闭集；当前状态为 `POLICY_DRIFT/REVIEW/2`，不作为最终权威候选。

最终候选只供复核；正式状态为 `DELIVERY REVIEW/2`。
