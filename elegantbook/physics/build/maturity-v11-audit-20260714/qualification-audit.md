# Humanize 生成资格固定 Oracle 下一批审计

## 审计范围与结论

本次只审计 `evaluation-contract.md`、三个 generation qualification JSON，以及 `audit_humanize_generation_qualification.py`、`seal_humanize_public_fixture.py`、`run_humanize_generation_trial.py`。未读取 tests、build 既有内容或历史报告，也未执行资格 harness。

当前 catalog 只有 5 个 `SHADOW` suite，覆盖 `MODE-02`、`ROLE-02`、`PATH-05/positive`、`LONG-01`、`PROTECTED/hash-zero`，即 5/163 atoms。维度覆盖为：MODE 1/6、ROLE 1/9、PATH 1/48、LONG 1/13、global 1/2，其余维度均为 0。下一批建议先增加 11 个可由现有 grader engine v1 固定承载的 vertical suite，使 catalog 达到 16/163；真实长文 owner、全保护 unit 和 partial/full 发布门另列为 harness 升级后的固定 suite，不能先用生成者自报 JSON 冒充机器证据。

这 11 个 suite 仍必须保持：

- `qualification_stage=SHADOW`；
- `runner_compatible=false`；
- 本地 runner 证据上限 `E2`；
- 确定性检查失败可形成 `FAIL`，确定性检查通过只能形成 shadow observation；因相应 atoms 最低要求 `E3`，不得写资格 `PASS`；
- 带主观 rubric 的 suite 在当前实现中固定 `qualification_eligible=false`，因为 review 只有 `CALLER_DECLARED`，没有独立 review receipt 或外部身份信任根。

## 为什么不会让提交者自评分

现有 v2 manifest 的边界是正确的：提交者只能提供 artifact、bindings、generation/review 引用，以及 `{claim_id, atom_id, oracle_suite_id}`。`assertions/result/expected/check_ids/regex/command` 等评分字段在任意嵌套位置都会被拒绝。固定 fixture hash、required checks、expected machine result 和 rubric 只来自 Skill 内 oracle catalog；replay 只能调用 allowlist 中的 `validate_humanize_output`，并以 `shell=False` 执行。

仍须坚持两点：

1. 不把 caller-declared `MODEL/HUMAN` rubric 答案计入资格。当前 auditor 已将其固定为 `NOT_EVALUATED`，这一点不能放宽。
2. 每个 suite 都增加动态 `context.public_context_sha256 == 固定 public-context fixture SHA-256` 检查。仅有 suite 的静态 fixture binding 不足以证明 fresh run 使用了同一 public context。

## 建议立即加入的 11 个固定 suite

下表中的 `CTX` 均指一条 catalog-owned `json_value` 检查：artifact=`context`，path=`["public_context_sha256"]`，operator=`EQUALS`，expected 为对应固定 public-context fixture 的 SHA-256。所有 `validator` 检查均固定 expected 为 `status=delivery_gate_status=PASS`、`exit_code=0`、`academic_correctness=NOT_EVALUATED`；提交 manifest 不得覆盖这些值。

| Suite ID / atom | 固定 fixture 输入与配置 | 固定机器检查 | 不能机器判的 rubric 边界 |
|---|---|---|---|
| `MODE-01/diagnose-only/v1` → `MODE-01` | 4 段 Markdown；存在重复句首、等长网格及一处应保留的正式术语。`DIAGNOSE/GENERAL/BALANCED/ANNOTATED`，scope=document | `CTX`；`utf8_literal` 要求唯一表头 `Severity | Location | Source role | Scene | Signal/Pathology | Trigger | Reading effect | Decision | Action`；禁止 `已调整`、`改写后` 和任一完整原段落被当作改后正文重印 | `style/MODE-01/grounded-diagnosis/v1`：定位是否真的对应上下文；Action 是否可执行。只接受未来独立、可信 review，caller 自答不计资格 |
| `MODE-04/diagnose-clean-conflict/v1` → `MODE-04` | 同类多段 Markdown，但 public context 显式给 `DIAGNOSE + CLEAN` | `CTX`；要求上述 ANNOTATED 唯一表头；禁止完整改后正文和“已调整”声明 | 无。该 atom 只验证确定性冲突裁决，可由机器完全判定 |
| `MODE-03/draft-from-points/v1` → `MODE-03` | Markdown 闭集要点，含 3 个不透明事实 token、1 个公式和固定数字顺序；没有背景和总结。`DRAFT/COURSE/BALANCED/CLEAN` | `CTX`；validator(COURSE)；`utf8_literal` 要求 3 个事实 token 各保留 1 次，禁止预置的自动背景、泛化意义和未来展望壳 | `style/MODE-03/supply-only/v1`：每个事实谓词能否回指 supplied points；是否用套话补造原因、背景或结论。开放世界“无新增事实”不能靠禁词穷举证明 |
| `MODE-05/draft-gap-honesty/v1` → `MODE-05` | Markdown 要点含锁定 `[待补：成因]`，其余事实完整。`DRAFT/GENERAL/BALANCED/CLEAN` | `CTX`；validator(GENERAL)；`artifact_relation/LITERAL_OCCURRENCES_EQUAL` 锁定占位符；禁止 `已经证明/由此可知/原因在于` 等完成状态升级 | `style/MODE-05/gap-not-filled/v1`：缺口是否仍诚实可见或自然省略；未用新的因果句替代占位 |
| `SCENE-GENERAL/positive/v1` → `SCENE/GENERAL/positive` | 普通社科 Markdown，多段包含模板路标、抽象拔高和自动收尾，但无课程、建模或同行讨论职责。`REWRITE/GENERAL/BALANCED/CLEAN` | `CTX`；validator(GENERAL)；要求各段唯一事实锚仍在；禁止固定 high 壳及其 fixture 内已列出的同义修复壳 | `style/SCENE-GENERAL/positive/v1`：是否保持普通学位论文正式度；是否避免套成课程、工程或期刊防御声线 |
| `SCENE-GENERAL/negative/v1` → `SCENE/GENERAL/negative` | Markdown 定义/规范段；“框架、机制、因此”为正式对象或真实因果，原文已自然 | `CTX`；validator(GENERAL)；以整段为 literal 做 `LITERAL_OCCURRENCES_EQUAL`，minimum=1；禁止新增默认声线模板 | `style/SCENE-GENERAL/negative/v1`：是否存在不必要的外围改动。现有 engine 没有整文件 `BYTE_EQUAL`，故附加文字仍须 review |
| `SCENE-GENERAL/conflict/v1` → `SCENE/GENERAL/conflict` | Markdown 中直接引语含 high 短语，外围作者句重复同一短语且为空壳 | `CTX`；validator(GENERAL)；引语 literal 改前改后次数相等；输出中该 high 短语总次数固定为 1，从而只留下引语内受保护实例 | `style/SCENE-GENERAL/conflict/v1`：外围删除后衔接是否自然，未把通用场景改成其他专属场景 |
| `VOICE-01/short-sample-default/v1` → `VOICE-01` | target 为 Markdown；public prompt 内封存少于 300 汉字的短作者样本。`REWRITE/GENERAL/BALANCED/CLEAN` | `CTX`；validator(GENERAL)；要求 `voice=SCENE_DEFAULT` 恰好 1 次；禁止“已复现/保留作者个人风格”等声明 | 无。该 atom 的关键是阈值回退与披露，可精确机器判定；不评价文本是否“像该作者” |
| `VOICE-03/protected-sample-exclusion/v1` → `VOICE-03` | target 为 Markdown；public prompt 内作者样本含外围叙述、直接引语、公式和代码，保护区各放一个唯一 nonce | `CTX`；validator(目标场景)；output 禁止所有 quote/math/code nonce；要求 target 的事实锚仍在 | `style/VOICE-03/outer-only-transfer/v1`：稳定习惯是否来自外围叙述、而非仅仅避开 nonce；是否发生真正但不过度的 voice transfer |
| `VOICE-05/real-self-reference/v1` → `VOICE-05` | target 多段重复“本文”，其中只有 `本文所称…` 是真实定义性指代；prompt 内同场景样本确认作者常用“本文” | `CTX`；validator(目标场景)；要求 `本文所称` 恰好 1 次；output 中 `本文` 总计 minimum=1、maximum=2；禁止把所有段首机械保留 | `style/VOICE-05/function-before-count/v1`：保留的是功能性指代而不是偶然满足计数；重复句壳确实下降 |
| `LONG-04/protected-dense-chapter/v1` → `LONG-04` | 单文件长 TeX，含多处行内/陈列公式、代码环境、引语与可编辑作者段落。`REWRITE/RESEARCH/BALANCED/PATCH` | `CTX`；validator(RESEARCH)；`measurement_result/protected_hash` 使用 grader-owned span annotation，要求全部保护跨度 hash 变化为 0；关键嵌套引语再做 literal relation | 无。该 suite 只判保护区字节、TeX/代码结构和 validator 状态，不判章节内容正确性或润色质量 |

建议所有需要 rubric 的 suite 使用 `reviewer_kinds=["HUMAN"]`、`minimum_distinct_reviewers=2`、`ALL_PASS`。在当前 review schema 下，这些答案仍只作 shadow 诊断，不能清除 `NOT_EVALUATED`；不要为了让 suite 变绿而把 rubric 改成 submitter-owned literal、自然语言自证或模型自评。

## 长文：必须先扩 harness，不能先造“会答 JSON”的伪 oracle

当前 public fixture 只允许一个 input 文件、prompt 和 public context，拒绝额外目录；runner 把 generator 放在 read-only execution root；auditor replay allowlist 只有统一验证器。因而它不能真实证明 include 递归、chunk owner、快照后变化、回滚或 finalization 发布门。现有 `LONG-01` 只能检查生成结果里的 include manifest JSON，不等价于真实长文工作流。

下一步最值得做的三个长文 suite 如下，但应在 harness 具备多文件 sealed bundle、受控 scratch 和固定 prepare/finalize replay 后再进入 catalog：

| Suite ID / atom | Fixture 输入类型 | 必须固定的机器 oracle | Rubric 边界 |
|---|---|---|---|
| `LONG-03/unique-owner/v1` → `LONG-03` | 多文件 TeX bundle；同一逻辑段跨 chunk 边界 | grader 调用固定 `prepare_humanize_long_document`；检查 unit ranges 无重叠/无空洞、每个 source span 仅一个 owner、同一段不出现两份 rewrite slot | 无；owner 和范围关系应完全机器判定 |
| `LONG-11/all-protected-unit/v1` → `LONG-11` | 单章 TeX，unit 仅含数学/代码/引语保护跨度 | prepare replay 后检查 `processable_editable_units=0`、unit=`SKIPPED_PROTECTED`，不得出现 `DONE`，不得允许 full completion claim | 无；状态与计数应完全机器判定 |
| `LONG-13/partial-publication-gate/v1` → `LONG-13` | 多文件 TeX/Markdown bundle，固定含一个 `UNRESOLVED` 或 `SKIPPED_GARBLED` unit；另设受控快照变更变体 | prepare + finalize 固定 replay；检查覆盖账本恒等式、`PENDING=IN_PROGRESS=0`、`full_completion_claim_allowed=false`、发布物为 partial；受控变更须得到 `CHANGED_AFTER_SNAPSHOT` | 无；不能让生成者在输出中自填这些状态后由 literal 检查放行 |

为此必须新增 grader-owned 工具 allowlist 项和 evaluator：固定 prepare/finalize 工具 ID、文件树/ledger 检查、source-range unique-owner 检查、发布物存在性检查及受控 mutation plan。命令、expected、mutation plan 仍只存在 oracle catalog/harness，绝不能回到 v2 manifest。

## 机器与 rubric 的明确边界

机器可以固定判定：配置/上下文绑定、精确表头和字段、required/forbidden literal 计数、保护跨度字节、公式数字引语结构、统一验证器四元状态、JSON 固定字段、段句网格是否变化、真实长文 ledger/owner/partial 状态（前提是 harness 实际运行工具）。

机器不能据现有 engine 可靠判定：DRAFT 是否完全没有新增事实谓词；诊断是否抓住真正主病灶；GENERAL 是否保持合适而非模板化的正式度；Voice 是否迁移了外围稳定习惯而没有只做表面词频；段落是否自然详略有别。以上只能进入 grader-owned rubric，且当前无可信 review receipt 时必须保持 `NOT_EVALUATED`。

## 需要同步更新的版本与哈希

加入 11 个 ready suite 时至少同步：

1. `generation-qualification-oracles.json` 的 `catalog_version`（建议 `1.1.0`）、checks、review_rubrics、suites 和 `fixture_provenance`；provenance 的键集合必须与 suites 完全相同。
2. 每个新 fixture 的 input、prompt、public-context、可选 review-bundle/protected-annotation SHA-256；每个 CTX check 中的 expected public-context SHA-256。
3. `audit_humanize_generation_qualification.py` 的 `REQUIRED_VERTICAL_SLICE`。若不把新 suite 加入这个固定集合，它们虽然可被 catalog 加载，却仍可被以后静默删除，不算“固定下一批”。这会改变 auditor executable hash。
4. catalog 变化会改变 `oracle_catalog_sha256` 和 `skill_snapshot_sha256`。所有新 run 的 qualification bindings、runner receipt、run record、run seal、v2 manifest top bindings 都必须使用新值；旧 current case 不能重放为新 catalog 的证据。
5. auditor/Skill snapshot 或 evaluation surface 变化后，重新生成并绑定 generator projection manifest；复核 `manifest_sha256`、`source_inventory_sha256`、`evaluation_surface_sha256` 及相关 receipt/seal hash。即使 generator projection 的 25 个能力文件字节未变，也不能沿用旧 projection manifest 绑定。
6. 若 contract、requirements、trust 未修改，则三者版本与 SHA-256 不应为了凑版本而变化；oracle 顶层 binding 继续绑定现值。若为真实长文 suite 扩展 grader engine、public fixture schema 或 tool allowlist，则应显式升级相应 schema/engine/runner 版本并重封全部受影响 fixture，不可只改 catalog 文本。

## 最终建议

先落 11 个 ready suite，目标是把 DRAFT、DIAGNOSE、GENERAL、Voice 和长文保护行为各建立至少一个不可由提交者定义 expected 的固定 vertical slice；不要宣称 16/163 意味着生成资格提升。随后优先扩长文 harness，依次落 `LONG-03`、`LONG-11`、`LONG-13`。在外部 E3 isolation receipt 与可信 review identity 仍未实现前，所有确定性 PASS 继续停在 shadow/E2，主观 rubric 继续 `NOT_EVALUATED`。
