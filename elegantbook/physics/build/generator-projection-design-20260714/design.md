# Humanize Academic Chinese 生成器投影视图设计

## 0. 结论

当前 Skill 不能直接作为生成资格运行时的可见目录。生产 `SKILL.md` 明确链接了资格
oracle、requirements、fixture 封存器、runner 和 auditor；现有 runner 又把完整 Skill
复制到执行目录。因此，即使 prompt 要求模型不要寻找评测材料，生成器仍然可以直接读取
答案面。

本设计采用闭集投影：生成器只获得经明确允许的写作能力文件；`SKILL.md` 经过一种可复现、
只删除资格说明的结构化转换；所有资格 oracle、requirements、fixtures、grader、auditor、
runner、sealer、测试与派生审计产物均留在投影之外。投影 manifest、policy、builder 和隔离
receipt 也不能放入生成器目录。

投影只能证明“本次 staged Skill 中没有答案面”，不能证明宿主机其他路径不可读。没有独立、
可验证的文件系统隔离时，即便投影本身完全正确，证据等级仍必须封顶为 E2；不得把
`projection_clean=true` 改写成 `filesystem_isolation_verified=true`。

## 1. 当前泄漏面的实证

当前文件的以下事实决定了投影不能只是 `copytree(..., ignore=...)`：

1. `SKILL.md:162-163` 的“引用路由”直接告诉生成器 `evaluation-contract.md`、oracle 文件以及
   三个资格脚本的名称。
2. `SKILL.md:195-209` 的“生成资格采集边界”公开 manifest schema、`oracle_suite_id`、当前
   suite 状态、fixture 封存流程和证据等级。
3. `run_humanize_generation_trial.py:377-388` 当前复制完整 Skill snapshot，只排除
   `__pycache__` 和字节码。
4. 同一 runner 在 prompt 中主动提到 tests、gold、qualification atoms 和 evaluator。即使这些
   句子是禁止指令，也向生成器披露了评测面的存在和类别。
5. runner 当前正确记录了 `oracle_catalog_visible_to_generator=true` 和
   `filesystem_isolation_verified=false`。投影落地后只能改变前者的“投影内存在性”事实，不能
   自动改变后者。
6. oracle catalog 的 provenance 又指向工作区 `tests/fixtures/...`。仅从 staged Skill 删除
   catalog，而宿主机仍可读工作区 tests，仍不构成盲测。

## 2. 目标、非目标与信任声明

### 2.1 必须达到

- 生成器能读取当前全部写作规范、场景差异、作者声线、词项表、病灶、范例、长文流程、
  语料动作卡和生产验证工具。
- 生成器看不到具体 qualification atom、suite、check、rubric、expected、fixture、gold、
  requirements 矩阵、grader 实现和资格运行编排。
- 投影由 harness 根据固定 policy 生成，调用方不能自选文件、删掉困难规则或自报投影完整。
- runner、auditor 和最终报告同时绑定源快照、投影 policy、转换器、投影文件树、public case、
  生成输出及隐藏 oracle。
- 任一未知文件、引用断裂、敏感引用残留、hash 漂移、源文件竞态或隔离声明缺证均 fail closed。

### 2.2 明确不声称

- 投影存在不等于宿主机不可读。
- Windows `chmod/read-only` 不等于访问控制，也不等于沙箱。
- prompt 中写“不要读取外部路径”不构成隔离证明。
- 没观察到模型读取 oracle 的工具事件，不证明它无法读取。
- 生成器知道公开写作规范并不构成答案泄漏。`lexical-signals.json`、`style-gates.md`、
  `operational-contract.md` 和生产验证器属于要交付给模型的能力规格；隐藏的是具体测试实例和
  评分控制面，而不是正确行为本身。

## 3. 投影文件闭集

policy 必须使用规范化的、区分大小写的 POSIX 相对路径。Windows 上还要拒绝 case-fold 或
Unicode NFC 后发生冲突的文件名。除下面列出的 exact path、明确的目录排除规则和 housekeeping
规则外，源 Skill 中出现任何新文件都使构建失败，直到 policy 被人工更新。

### 3.1 原样包含（25 个文件）

| 类型 | 相对路径 | 原因 |
|---|---|---|
| UI 元数据 | `agents/openai.yaml` | 保留正式 Skill 身份和默认调用入口 |
| 生产引用 | `references/corpus-action-sources.json` | 保留既有 MD/TeX 抽象动作卡和负例 detector |
| 生产引用 | `references/course-notes.md` | COURSE 写作能力 |
| 生产引用 | `references/detector-report-intake.md` | 报告只作 scope 线索的生产合同 |
| 生产引用 | `references/lexical-signals.json` | 明确、可执行的 AI 风味词项抓手 |
| 生产引用 | `references/long-document-workflow.md` | 长文、TeX、分块和完成声明能力 |
| 生产引用 | `references/modeling-engineering.md` | MODELING 场景能力 |
| 生产引用 | `references/operational-contract.md` | 模式、状态、输出字段的生产合同 |
| 生产引用 | `references/pathology-catalog.md` | 复杂病灶定位能力 |
| 生产引用 | `references/quick-checklist.md` | 快速分诊能力 |
| 生产引用 | `references/research-journal.md` | RESEARCH 场景能力 |
| 生产引用 | `references/rewrite-patterns.md` | 场景改写动作范例；不是 gold output |
| 生产引用 | `references/style-gates.md` | 生产交付门；不是资格 grader |
| 生产引用 | `references/system-prompt-contract.md` | 可移植生产 prompt |
| 生产引用 | `references/voice-profile.md` | 作者样本建档与声线保护 |
| 生产引用 | `references/workflow.md` | DIAGNOSE/REWRITE/DRAFT 工作流 |
| 生产脚本 | `scripts/build_humanize_action_profile.py` | 构建语料动作 profile |
| 生产脚本 | `scripts/check_humanize_invariants.py` | 公式、数字、引语、TeX 等硬保护 |
| 生产脚本 | `scripts/extract_detector_report_scope.py` | 检测报告安全映射 |
| 生产脚本 | `scripts/finalize_humanize_long_document.py` | 长文收尾与完成门 |
| 生产脚本 | `scripts/prepare_humanize_candidate_revision.py` | 候选修订血缘 |
| 生产脚本 | `scripts/prepare_humanize_long_document.py` | 长文快照与分块 |
| 生产脚本 | `scripts/scan_humanize_chinese.py` | 词项扫描 |
| 生产脚本 | `scripts/validate_humanize_candidate_queue.py` | 语料动作、复制和负例门 |
| 生产脚本 | `scripts/validate_humanize_output.py` | 统一生产交付验证器 |

`references/corpus-action-sources.json` 当前含若干宿主机绝对来源路径。这些路径是语料来源审计
的一部分，不是资格答案，因此 v1 原样保留；但隔离后端不得挂载这些宿主机路径。投影检查应把
它们记录为 `declared_external_capability_refs`，不能把“路径字符串可见”误报为“目标文件可读”。
若 qualification case 需要来源 profile 的实时可用性，应由生成结束后的 harness 服务验证，
不应为此把整套原始语料挂入生成器环境。

### 3.2 结构化转换（1 个文件）

| 相对路径 | transform ID | 输出路径 |
|---|---|---|
| `SKILL.md` | `strip-qualification-surface/v1` | `SKILL.md` |

### 3.3 明确排除的答案面

| 类别 | 相对路径或规则 | 理由 |
|---|---|---|
| 资格合同 | `references/evaluation-contract.md` | fixture 设计、矩阵和资格完成门 |
| 原子要求 | `references/generation-qualification-requirements.json` | 163 原子与覆盖合同 |
| oracle | `references/generation-qualification-oracles.json` | suite/check/rubric/expected/fixture hash |
| 信任策略 | `references/generation-qualification-trust.json` | E3/E4 信任根、receipt scheme 与本地证据上限 |
| 资格 fixtures | `references/generation-qualification-fixtures/**` | 具体输入、prompt、context、review bundle 与 expected artifacts |
| grader/auditor | `scripts/audit_humanize_generation_qualification.py` | 隐藏评分逻辑 |
| runner | `scripts/run_humanize_generation_trial.py` | 资格编排、bindings 和证据结构 |
| sealer | `scripts/seal_humanize_public_fixture.py` | fixture 结构和资格输入编排 |
| 派生产物 | `build/**` | 运行产物、旧 profile、审计状态，不是运行能力源 |
| 缓存 | `**/__pycache__/**`, `**/*.pyc`, `**/*.pyo` | 非源文件；不进入任何能力 hash |

工作区的 `tests/**`、`tests/fixtures/**`、各次 `build/qualification-*`、历史红蓝队输出、报告和
源 Skill 完整目录本来就在 Skill 根之外，绝不能复制进 execution root。隔离 policy 还必须让
这些宿主机路径不可达；“不复制”本身不够。

### 3.4 为什么不排除生产门和词库

`style-gates.md`、`lexical-signals.json`、`quick-checklist.md`、
`validate_humanize_output.py` 等文件公开“怎样写”和“怎样保护正文”，属于 Skill 本体。如果将
它们当作 oracle 一并隐藏，投影虽然更盲，却不再代表真实生产 Skill，得到的 forward result
也不能说明部署时行为。资格 oracle 应使用未公开的 case、组合、边界和评分断言来测泛化，不能
靠剥夺生产规范制造难度。

## 4. `SKILL.md` 确定性删节规则

转换器必须按 Markdown 结构和精确锚点工作，不接受调用方传入正则、起止行、heading 名称或
删除列表。

### 4.1 输入条件

1. 以 UTF-8 strict 解码；拒绝替换字符、NUL 和无法解码字节。
2. 要求恰好一个 YAML frontmatter，且只含当前合法的 `name`、`description`。
3. 要求恰好一个 `## 引用路由`、一个 `## 生成资格采集边界` 和一个紧随其后的
   `## 来源锚定的改写候选`。
4. 要求引用路由表中恰好各有一行首列为 `验证 Skill` 和 `生成资格审计`。缺少、重复、改名或
   表结构损坏一律失败，不作猜测性删节。

### 4.2 唯一允许的编辑

1. 删除引用路由表中首列规范化后等于 `验证 Skill` 的整行。
2. 删除引用路由表中首列规范化后等于 `生成资格审计` 的整行。
3. 删除从 `## 生成资格采集边界` heading 起，到下一个二级 heading
   `## 来源锚定的改写候选` 之前的全部字节。
4. 输出统一为 UTF-8、无 BOM、LF。除此以外，正文只能发生由换行规范化产生的字节变化；不能
   插入免责声明、重新措辞、压缩其他段落或自动修复链接。

转换器记录三个 removed-span 的 source byte range、SHA-256 和 transform ID，但不在投影内
保存被删内容。auditor 必须能从源 `SKILL.md` 和固定转换器独立重算相同 projected hash。

### 4.3 转换后不变量

- `name`、`description`、所有生产 heading 及其相对顺序不变。
- `引用路由` 表仍有合法表头、分隔行和其余生产行。
- 不再出现任一被排除 basename、资格脚本名、`oracle_suite_id` 或资格 section heading。
- 所有 Markdown 本地链接、反引号中的 `references/...` 与 `scripts/...` 均解析到投影闭集。
- 不允许 `..`、绝对本地链接、`file://`、junction、symlink 或 reparse-point 跳出投影。
- 生产依赖图保持闭合：三个 validator 依赖的词库、invariant checker 和生产脚本必须仍存在。

## 5. 投影 policy 与 manifest

### 5.1 policy 归属

policy 是 harness-owned 的控制文件，不进入投影。建议放在资格 harness 包中，例如：

```text
tools/humanize_qualification/generator-projection-policy.json
tools/humanize_qualification/build_generator_projection.py
```

如果暂时仍放在完整 Skill 根内，也必须列为 evaluation surface 并从投影排除。生成器不能提交
或修改 policy；CLI 不提供 `--include`、`--exclude`、`--transform` 等调用方自由参数，只允许
选择已经登记的 policy ID。

policy 最小 schema：

```json
{
  "schema_version": "humanize-generator-projection-policy/v1",
  "policy_id": "humanize-academic-chinese/generator/v1",
  "source_root_basename": "humanize-academic-chinese",
  "include_exact": ["agents/openai.yaml", "references/workflow.md"],
  "transform_exact": {
    "SKILL.md": "strip-qualification-surface/v1"
  },
  "exclude_exact": [
    "references/evaluation-contract.md",
    "references/generation-qualification-oracles.json",
    "references/generation-qualification-requirements.json",
    "references/generation-qualification-trust.json",
    "scripts/audit_humanize_generation_qualification.py",
    "scripts/run_humanize_generation_trial.py",
    "scripts/seal_humanize_public_fixture.py"
  ],
  "exclude_prefixes": [
    "build/",
    "references/generation-qualification-fixtures/"
  ],
  "housekeeping_patterns": ["**/__pycache__/**", "**/*.pyc", "**/*.pyo"],
  "required_entrypoint": "SKILL.md",
  "forbidden_reference_basenames": [
    "evaluation-contract.md",
    "generation-qualification-oracles.json",
    "generation-qualification-requirements.json",
    "generation-qualification-trust.json",
    "audit_humanize_generation_qualification.py",
    "run_humanize_generation_trial.py",
    "seal_humanize_public_fixture.py"
  ]
}
```

实际 `include_exact` 必须列出第 3.1 节全部 25 个文件，不能使用 `references/**` 或
`scripts/**` 宽泛 glob。上例仅为 schema 缩写，不是可直接运行的完整 policy。

### 5.2 manifest 必须在投影外

投影目录中不写 `.projection.json`、policy 副本、exclusion list 或 hidden hashes。完整 manifest
由 runner 保存到 run evidence 目录，生成器仅看到 26 个能力文件。

建议 schema：

```json
{
  "schema_version": "humanize-generator-projection-manifest/v1",
  "projection_policy": {
    "id": "humanize-academic-chinese/generator/v1",
    "sha256": "<canonical-policy-sha256>"
  },
  "builder": {
    "version": "1.0.0",
    "executable_sha256": "<builder-sha256>",
    "transform_registry_sha256": "<registry-sha256>"
  },
  "source": {
    "root_id": "humanize-academic-chinese",
    "inventory_sha256": "<all-classified-source-files-sha256>",
    "capability_source_sha256": "<include-plus-transform-input-sha256>",
    "evaluation_surface_sha256": "<excluded-evaluation-files-sha256>"
  },
  "files": [
    {
      "path": "SKILL.md",
      "disposition": "TRANSFORM",
      "source_sha256": "<sha256>",
      "projected_sha256": "<sha256>",
      "size": 12345,
      "transform_id": "strip-qualification-surface/v1"
    },
    {
      "path": "references/workflow.md",
      "disposition": "INCLUDE",
      "source_sha256": "<sha256>",
      "projected_sha256": "<same-sha256>",
      "size": 9736,
      "transform_id": null
    }
  ],
  "excluded": [
    {
      "path": "references/generation-qualification-oracles.json",
      "class": "EVALUATION_SURFACE",
      "source_sha256": "<sha256>"
    }
  ],
  "transformations": [
    {
      "path": "SKILL.md",
      "transform_id": "strip-qualification-surface/v1",
      "removed_span_sha256": ["<sha256>", "<sha256>", "<sha256>"],
      "source_sha256": "<sha256>",
      "projected_sha256": "<sha256>"
    }
  ],
  "audits": {
    "unknown_paths": [],
    "reference_closure": "PASS",
    "forbidden_reference_scan": "PASS",
    "secret_control_identifier_scan": "PASS",
    "casefold_collision_scan": "PASS",
    "reparse_point_scan": "PASS",
    "python_compile": "PASS",
    "skill_quick_validate": "PASS"
  },
  "projection_tree_sha256": "<deterministic-tree-sha256>"
}
```

`manifest_sha256` 不写入 manifest 自身，避免递归。runner 对 canonical manifest bytes 计算并写入
run receipt。时间戳、临时目录、mtime、Windows ACL 展示字符串不得进入 deterministic core；
它们放在单独的 build receipt 中。

### 5.3 规范 hash

- JSON 使用 UTF-8、无 BOM、键排序、紧凑分隔符、拒绝 duplicate key。
- 路径统一 `/`，禁止空段、`.`、`..`、尾随空格、ADS `:` 和保留设备名。
- 文件按 UTF-8 path bytes 升序。
- `projection_tree_sha256` 定义为：

```text
SHA256(canonical_json({
  "schema_version": "humanize-generator-projection-tree/v1",
  "files": [{"path": ..., "sha256": ..., "size": ...}, ...]
}))
```

路径、内容 hash 和长度都被绑定；同字节换名也会改变 root。目录时间、复制时间和只读位不参与
能力树 hash，因为它们不是内容身份，也不能证明隔离。

`source.inventory_sha256` 应覆盖所有非 housekeeping 源文件及其 disposition，保证新增文件不会
静默漏过。`evaluation_surface_sha256` 只供 auditor 绑定隐藏答案面，不进入 generator context。
其中必须覆盖 `generation-qualification-trust.json`；projection tree 可以在 trust policy 变化时
保持不变，但任何资格 run 的信任判定都必须因独立 trust-policy hash 漂移而重新审计。

## 6. 构建器算法

1. 解析 source root 和新建的空 staging root；两者必须互不包含。
2. 枚举 source root 的每个目录项，不跟随 symlink/junction/reparse point。拒绝非常规文件、
   Alternate Data Stream、case-fold/NFC 冲突和多路径同一 file ID 的硬链接。
3. 按 exact include/transform/exclude 和 housekeeping 规则分类。任何 `UNKNOWN` 立即失败。
4. 为全部非 housekeeping 文件建立冻结快照：读取前后核对 file ID、长度、mtime 和 SHA-256；
   变化则失败，不能用旧 hash 配新字节。
5. 原样复制 include 文件；使用内建 transform registry 转换 `SKILL.md`。转换函数不接受外部规则。
6. 对 staging 做第二次完整枚举，要求它精确等于 26 个 expected paths；不得存在 manifest、日志、
   临时文件或源目录的额外副本。
7. 执行本地引用闭包：Markdown link、反引号路径、Python AST 中指向 Skill 内文件的 string literal
   均必须落在投影内；声明为 external corpus source 的绝对路径单独登记，不误当本地闭包。
8. 扫描全部 projected text，拒绝被排除 basename、资格脚本名、suite/check/rubric/claim/atom 控制
   ID 和已登记 gold/fixture 文件名。控制 ID 集由 harness 从隐藏 catalog/requirements 提取，不能
   把 ID 清单写入 projection。
9. 不得把 oracle 中所有普通中文 literal 都列为禁词。公开写作规范与预期行为本来就可以重合；
   只拦截评测控制 ID、fixture/gold 特有片段、hash 和路径。
10. 对 9 个生产 Python 脚本执行 `py_compile`，并在投影 root 上运行 Skill quick validation。
11. 可运行无隐藏答案的 smoke：各 CLI `--help`；scanner 对内建中性短句；统一 validator 对相同的
    before/after 文本。smoke artifact 放在投影外并在结束后删除。
12. 计算 manifest 和 tree hash，再次核对 staging 文件 hash；最后原子发布到 run execution root。
13. 发布后只读标记仅作为误写保护。manifest 必须明确
    `read_only_marking_is_isolation_proof=false`。

## 7. runner 绑定方式

### 7.1 必须修改的运行顺序

现有 `_copy_skill_snapshot()` 应由 harness-owned projection builder 替代：

```text
冻结完整源 Skill
  -> 构建并审计 generator projection
  -> staging 只放 projection + public case
  -> 启动 fresh generator
  -> generator 退出并封存 output/trace
  -> 隐藏 grader 才读取 output + oracle
```

grader、oracle、requirements、fixture manifest 和 projection manifest 在 generator 退出前不得出现
于它的 mount namespace、工作目录、环境变量、prompt、stdin、stdout 目标或可读父目录。

### 7.2 prompt 与 context 最小化

删除当前 effective prompt 中“不要找 tests/gold/qualification atoms/evaluator material”的枚举，
因为它本身提示了答案面。改成不带评测词汇的运行边界：

```text
Use the humanize-academic-chinese Skill at skill/SKILL.md for this task.
Read the source artifact under case/ and return the requested deliverable only.
Operate only on resources provided in this execution root.
```

`qualification_bindings`、oracle hash、requirements hash、projection exclusion list 和 isolation probes
不得进入 generator-visible `context.json`。这些值只进入 runner receipt。公开 context 只保留完成
任务必需的 `mode/scene/intensity/output/voice/report_context`、locks 和 task options。

### 7.3 run receipt 的新绑定

run receipt 至少增加：

```json
{
  "generator_projection": {
    "manifest_sha256": "<sha256>",
    "tree_sha256": "<sha256>",
    "policy_sha256": "<sha256>",
    "builder_sha256": "<sha256>",
    "source_inventory_sha256": "<sha256>",
    "evaluation_surface_present_in_projection": false,
    "projection_audit_status": "PASS"
  },
  "isolation": {
    "filesystem_isolation_verified": false,
    "host_excluded_roots_unreachable_verified": false,
    "oracle_catalog_present_in_projection": false,
    "oracle_catalog_unreachable_to_generator": "UNVERIFIED",
    "verification_source": "LOCAL_COPY_ONLY",
    "evidence_cap": "E2"
  }
}
```

字段名必须区分“投影内不存在”和“生成器不可达”。不要继续使用一个含混的
`oracle_catalog_visible_to_generator=false` 来同时表达两者。

### 7.4 获得 E3 所需的隔离 receipt

本地 `codex exec -s read-only` 加投影仍只到 E2。E3 至少要求：

- 独立 container/VM/AppContainer 或远程执行后端，仅挂载 projection、public case、空 output 和
  必需运行时；不挂载 `C:\Users\Lenovo\.codex`、D 盘工作区、tests、build、完整 Skill、session
  history 或宿主用户目录。
- generator 与同身份 preflight probe 共享相同 security token、mount namespace/container ID；
  不能用一个受限 probe 替一个权限更高的 generator 作证。
- receipt 列出镜像/后端 digest、mount allowlist、network policy、进程身份、父子 PID、启动命令
  hash、projection tree、case seal 和 output hash。
- receipt 由 generator 无法访问私钥的外部执行服务签名。runner 自己写
  `filesystem_isolation_verified=true` 不被 auditor 接受。
- 对若干 harness 随机生成、仅宿主存在的 canary path 做同身份 deny probe；probe 是补充证据，
  仍需 mount/policy 证明。单次 `Test-Path=false` 不足以证明整个宿主树不可读。

没有这些条件时，报告可以写“投影内未包含 oracle”，不能写“生成器看不到 oracle”。

## 8. auditor 绑定与判定顺序

auditor 不能信任 manifest 中的自报 PASS。它应执行以下独立检查：

1. 从 run receipt 绑定的 source snapshot 和固定 policy 重新构建投影，比较每个文件字节、
   manifest hash 和 tree hash。
2. 独立扫描投影内容和引用闭包；runner 的 `projection_audit_status` 只作观测值。
3. 校验 builder、policy、transform registry、完整源 Skill、hidden requirements、oracle catalog、
   qualification trust policy、fixture seal 和 grader 自身 hash。
4. 校验 generator command、public input/prompt/context、events、stderr、output 和 raw run seal。
5. 验证 external isolation receipt 的签名、scope、同身份绑定、mount allowlist、projection tree、case
   seal 和 output hash。没有可信 receipt 时强制 E2。
6. 生成过程结束后才运行 hidden deterministic checks；主观 review 不能覆盖 projection/integrity/
   deterministic FAIL。
7. 若当前源 Skill 已漂移，而 auditor 没有 run 时的内容寻址 source snapshot，则该 run 只能
   `STALE/REVIEW`，不能拿当前文件重算后宣称一致。

资格 case binding 建议增加：

```json
{
  "source_skill_snapshot_sha256": "...",
  "generator_projection_manifest_sha256": "...",
  "generator_projection_tree_sha256": "...",
  "generator_projection_policy_sha256": "...",
  "generator_projection_builder_sha256": "...",
  "oracle_catalog_sha256": "...",
  "requirements_sha256": "...",
  "qualification_trust_policy_sha256": "...",
  "fixture_seal_sha256": "...",
  "generation_run_record_sha256": "...",
  "isolation_receipt_sha256": null,
  "output_sha256": "..."
}
```

`oracle_catalog_sha256` 等隐藏 binding 只存在于外部 evidence，不写入 effective prompt 或 staging
context。projection tree 与 oracle catalog 是两个独立 hash：前者证明给了模型什么，后者证明
评分用了什么。

### 8.1 fail-closed 优先级

```text
投影/源/fixture/receipt 完整性 FAIL
  > 确定性 oracle FAIL
  > 隔离或身份证据不足
  > 主观 review 缺失/失败
  > PASS
```

投影污染必须是 `INFRA_INVALID` 或 integrity `FAIL`，不能因生成文本恰好符合 expected 而获得
atom PASS。隔离不足则保留实际 deterministic 观测，但证据等级封顶，不能形成 E3 资格。

## 9. 拒绝、漂移与攻击测试

以下测试均应成为自动回归；前 25 项为投影 builder/auditor 的最低门，后续项覆盖 runner 和
隔离声明。每个测试都要断言状态、退出码和具体 finding，不能只断言“抛异常”。

| ID | 攻击或漂移 | 必须结果 |
|---|---|---|
| PROJ-01 | 当前闭集构建两次 | 26 个文件逐字节相同，tree/manifest core hash 相同 |
| PROJ-02 | Skill 根新增普通 `references/new.md` | `UNKNOWN_PATH/FAIL`，不得静默忽略或自动包含 |
| PROJ-03 | 把 oracle 加进 include list，但不改其他规则 | forbidden class `FAIL` |
| PROJ-04 | 将 oracle 重命名为 `references/helpful.json` | unknown path 或 hidden control-ID scan `FAIL` |
| PROJ-05 | 大小写变体 `Evaluation-Contract.md` | case-fold sensitive-name scan `FAIL` |
| PROJ-06 | NFC/NFD 两个视觉相同路径 | Unicode collision `FAIL` |
| PROJ-07 | include 文件是指向 oracle 的 symlink/junction | reparse-point `FAIL`，不得跟随复制 |
| PROJ-08 | include 文件与 hidden file 是 hardlink | duplicate file ID / link-count policy `FAIL` |
| PROJ-09 | policy 路径含 `..`、绝对盘符或 ADS `:` | policy validation `FAIL` |
| PROJ-10 | 构建中途修改 `SKILL.md` 或引用文件 | snapshot race `FAIL`，不发布 projection |
| PROJ-11 | 删除 `## 生成资格采集边界` heading | transform anchor `FAIL`，不能输出未删节原文 |
| PROJ-12 | 复制第二个同名资格 heading | duplicate anchor `FAIL` |
| PROJ-13 | 把“验证 Skill”表行改名但仍链接 evaluation contract | required row/forbidden reference `FAIL` |
| PROJ-14 | 把下一个 heading 改成别名，诱使转换器多删一节 | boundary anchor `FAIL`，不得吞掉写作能力 |
| PROJ-15 | 删节后留下对 hidden basename 的 Markdown 链接 | forbidden reference `FAIL` |
| PROJ-16 | 在 HTML comment、代码围栏或反引号里写 suite/fixture 控制 ID | 全文本 control-ID scan `FAIL` |
| PROJ-17 | 生产 Markdown 链接到未投影本地文件 | reference closure `FAIL` |
| PROJ-18 | Python string literal 指向被排除资格脚本 | dependency/reference scan `FAIL` |
| PROJ-19 | 投影内额外出现 manifest、日志或临时文件 | exact staged inventory `FAIL` |
| PROJ-20 | 只改一个 included 文件的一个字节 | projected file/tree/manifest hash 全部变化；旧 run binding `FAIL` |
| PROJ-21 | 文件内容不变但重命名 | tree hash 变化；expected path 缺失 `FAIL` |
| PROJ-22 | policy 改一个 include/exclude 项 | policy hash 漂移，旧 run `STALE/FAIL` |
| PROJ-23 | builder 或 transform registry 改动 | executable/registry hash 漂移，旧 binding 不接受 |
| PROJ-24 | 篡改外部 manifest 的 audit 字段为 PASS | auditor 重算发现不一致，不能信自报 |
| PROJ-25 | 只增加/删除 `__pycache__` 和 `.pyc` | deterministic capability/tree hash 不变 |
| PROJ-26 | 仅把源 CRLF 改 LF | source hash 变化；转换输出按 v1 规范重算，旧 source binding 失效 |
| PROJ-27 | hidden oracle 改动而 projection 不变 | projection hash可不变，但 oracle binding 漂移使旧 grade 失效 |
| PROJ-28 | qualification fixture 改动而 projection 不变 | fixture seal 漂移，case integrity `FAIL` |
| PROJ-29 | E3/E4 trust policy 改动而 projection 不变 | projection hash可不变，但 trust-policy binding 漂移；旧隔离资格失效 |
| RUN-01 | runner 误把完整 Skill 复制到 projection 旁 | execution-root inventory `FAIL`，生成器不启动 |
| RUN-02 | effective prompt 出现 `gold/oracle/atom/evaluator` 等隐藏控制词 | prompt contamination `FAIL` |
| RUN-03 | generator-visible context 含 qualification/oracle hash | context schema `FAIL` |
| RUN-04 | 只有 clean projection，没有外部隔离 receipt | 可运行但 `evidence_cap=E2`，不可 E3 |
| RUN-05 | runner 自填 `filesystem_isolation_verified=true` | auditor 拒绝 caller assertion |
| RUN-06 | 自签或签名 key 对 generator 可读的 receipt | trust-root `FAIL` |
| RUN-07 | receipt mount list包含完整 `.codex`、workspace、tests 或 full Skill | isolation `FAIL` |
| RUN-08 | probe 与 generator 的 token/container/mount namespace 不同 | isolation identity binding `FAIL` |
| RUN-09 | 原始 Skill 通过用户 skill auto-discovery 另行挂载 | mount/inventory `FAIL` |
| RUN-10 | 观察到 generator 尝试读取 execution root 外路径 | contamination finding；该 run 不进入资格 |
| RUN-11 | 没观察到外读事件但没有 mount proof | 仍为 E2；禁止以“无事件”升级 |
| RUN-12 | hidden grader 在 generator 退出前启动或将 rubric 放进 staging | ordering/inventory `FAIL` |
| AUD-01 | runner receipt 的 projection tree 与保留目录实际字节不符 | integrity `FAIL` |
| AUD-02 | output 在运行结束后被改动 | output/run seal `FAIL` |
| AUD-03 | subjective ballot PASS，但 projection 中含 oracle | integrity `FAIL` 优先，atom 不得 PASS |
| AUD-04 | deterministic check FAIL，但 reviewer PASS | deterministic `FAIL` 优先 |
| AUD-05 | run 时 source snapshot 已丢失，只剩当前漂移后的 Skill | `STALE/REVIEW`，不得重构为 PASS |
| AUD-06 | manifest 省略一个困难 include 文件但自称“完整能力” | exact policy coverage `FAIL` |
| AUD-07 | hidden control ID 扫描列表由 caller 自选为空 | schema/ownership `FAIL`；必须由 harness 从 catalog 提取 |
| AUD-08 | 同一 projected tree 绑定到另一 public case/output | case/output hash binding `FAIL` |

## 10. 验收标准

实现后只有同时满足以下条件，才能把“生成器投影视图已实现”标为完成：

1. baseline projection 恰有 26 个文件，清单与第 3 节完全一致。
2. `SKILL.md` 只发生第 4 节允许的三处删除和换行规范化，其他生产内容均可由 byte mapping 证明
   未改变。
3. 投影中无资格文件、控制 ID、hidden fixture/gold 特有路径或对它们的交叉引用。
4. 9 个生产脚本可编译，投影 Skill 通过 quick validation，生产依赖闭合。
5. 同一 source/policy/builder 重建的 deterministic hashes 一致。
6. runner 不再复制完整 Skill，不在 prompt/context 中提示评测面。
7. auditor 独立重建投影，不信 runner 自报，并同时绑定 projection 与 hidden oracle。
8. 第 9 节至少 PROJ-01 至 PROJ-25、RUN-01 至 RUN-12、AUD-01 至 AUD-08 全部通过。
9. 本地无隔离运行仍明确为 E2；报告只称“答案面未进入投影”，不称“生成器无法读取宿主机答案面”。
10. 至少一次真正隔离运行由外部签名 receipt 证明 mount/token/scope 后，才允许进入 E3 采集；
    投影自身不能替代该 receipt。

## 11. 实施顺序

1. 先新增外部 projection policy、builder 和单元测试，不改资格判断。
2. 让 auditor 能独立构建并审计 baseline projection，完成 PROJ 系列回归。
3. 将 runner 的完整 Skill copy 替换为 projection build；清理 prompt/context 的评测词和 hidden
   bindings；完成 RUN 系列回归。
4. 更新 run/manifest schemas，区分 `present_in_projection` 与 `unreachable_to_generator`。
5. 在没有外部隔离后端时运行一次本地试验，确认仍为 E2，防止错误升级。
6. 接入真正的隔离执行后端和外部签名 receipt，再启用 E3 eligibility。
7. 最后才把 oracle suite 从 `SHADOW` 逐步升级；投影完整并不自动使任何 suite 或 atom PASS。

## 12. 剩余边界

- 公开 Skill 必然透露目标行为，例如哪些套话需要谨慎、怎样保护引语和公式。盲测的价值来自
  未公开的输入组合与独立 grader，而不是让生成器不知道任务规范。
- `corpus-action-sources.json` 中的绝对路径使本地不隔离运行更容易探索宿主文件；因此它再次说明
  projection 不是安全边界。若后续希望在隔离资格运行中实时使用语料 freshness/copy 检查，应
  设计 harness-side RPC 或只读、最小化的内容寻址服务，不能直接挂载整盘原始语料。
- Codex CLI 的 read-only sandbox、`--ephemeral`、`--ignore-user-config` 和 `--ignore-rules` 都有价值，
  但它们分别解决写权限、会话、配置和规则污染；没有任何一项单独证明宿主机读取隔离。
- 投影 policy 更新属于评测基础设施变更。每次新增生产能力文件都应显式评审其分类；不能为了
  让 CI 变绿而把 unknown 自动归入 include 或 exclude。
