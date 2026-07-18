# 生成资格可观测性审计

审计对象：

- `references/evaluation-contract.md`
- `references/generation-qualification-requirements.json`
- `scripts/audit_humanize_generation_qualification.py`

审计日期：2026-07-14。本文只描述当前 grader 的证据来源和文档语义，不修改 Skill，也不提供可执行的对抗性材料。

## 结论

当前 requirements 展开为 163 个资格原子。真正由 harness 对 artifact 内容执行专属测量的只有 14 个原子：12 个幂等原子、1 个路由稳定原子和 1 个保护跨度原子；这些测量仍依赖调用方声明运行独立性、观察值或跨度选择。137 个 `behavior` 原子的语义结果来自 manifest 中的 `assertions[].result`，harness 不计算这些断言。另有 12 个 `BLIND_REVIEW` 原子使用 manifest 票据；代码校验票据结构与哈希绑定，但明确不验证评审者身份，因此当前不是可验证的人工盲评证据。

代码没有模型 grader。唯一允许重放的工具是 `validate_humanize_output.py`，它提供通用交付门和不变量状态，不逐项判定 MODE、INT、OUT、DEC、ROUTE、VOICE、ROLE、LONG、PATH、SCENE 或 REPORT 原子。

## 原子到 grader 来源映射

| 资格维度 | 精确原子集合 | 数量 | 最低证据 | 当前语义 grader 来源 | 机器实际重算 | 调用方声明或选择 | 是否要求盲人评 |
|---|---|---:|---|---|---|---|---|
| Mode | `MODE-01..06` | 6 | E3 | `assertions[].result` | 通用 validator 的实际状态、退出码及 artifact 哈希 | 断言 PASS/FAIL/NOT_EVALUATED；claim 到 atom 的映射；E3 新上下文与盲性声明 | 否 |
| Intensity | `INT-01..07` | 7 | E3 | `assertions[].result` | 同上 | 同上；没有段落移动、scope 或结构锁的专属 grader | 否 |
| Output | `OUT-01..06` | 6 | E3 | `assertions[].result` | 同上 | 同上；没有输出 schema 的 atom 专属解析 | 否 |
| Decision | `DEC-01..08` | 8 | E3 | `assertions[].result` | 同上 | 同上；KEEP/DELETE/REWRITE 等决策不由 harness 从输出推导 | 否 |
| Route | `ROUTE-01..12` | 12 | E3 | `assertions[].result` | 同上 | 同上；不要与全局路由稳定原子混淆 | 否 |
| Voice | `VOICE-01..10` | 10 | E3 | `assertions[].result` | 同上 | 同上；没有样本长度、场景迁移或声线保持的专属 grader | 否；部分读感按合同适合盲评，但 requirements 未要求 E4 |
| Role | `ROLE-01..09` | 9 | E3 | `assertions[].result` | 同上 | 同上；全局 `PROTECTED/hash-zero` 不自动证明九个 ROLE 原子 | 否 |
| Long document | `LONG-01..13` | 13 | E3 | `assertions[].result` | 同上 | 同上；allowlist 不含 prepare/finalize，未重放覆盖账本、回滚或编译 | 否 |
| Pathology | `PATH-01..16/{positive,negative,conflict}` | 48 | E3 | `assertions[].result` | 通用 validator 重放，不判定每种病灶及三种变体 | 每个变体的结果和 atom 归属均由 manifest 声明 | 否；合同 4.4 中的自然节奏、等重、口头禅等读感适合盲评，但这里未要求 E4 |
| Scene | `SCENE/{COURSE,MODELING,RESEARCH,GENERAL}/{positive,negative,conflict}` | 12 | E3 | `assertions[].result` | 通用 validator 重放 | 场景/变体覆盖由 claim 的 atom ID 表示；case 内容与该 ID 未做专属匹配 | 否 |
| Report informed | `REPORT/{unique-mapping,duplicate-mapping,unmappable,score-only,malicious-html,mixed-evasion-request}` | 6 | E3 | `assertions[].result` | 通用 validator 重放 | 报告变体及处理结果由 claim 声明；allowlist 不含 report extractor | 否 |
| Idempotency | `IDEMPOTENCY/{四场景}/01..03` | 12 | E3 | 确定性字节比较 + 运行记录规则检查 | 两个所选 output artifact 是否逐字节相等；prompt/context/input-output 链哈希是否一致 | `CALLER_ATTESTED_DISTINCT_RUN_RECORDS`；run ID；记录确实来自独立生成的事实 | 否 |
| Blind review | `BLIND_REVIEW/{四场景}/01..03` | 12 | E4 | 调用方提交的 ballot 结果 + 结构/绑定规则检查 | rubric、bundle、generation binding 的哈希一致性；两份 reviewer hash 是否不同 | `reviewer_kind=HUMAN`、reviewer hash、`CALLER_ASSERTED_HUMAN_REVIEW`、每票 PASS/FAIL | 是，规范上要求；当前实现不验证人类身份、盲性或实际评审行为 |
| Global route stability | `STABILITY/route-owner-three-runs` | 1 | E3 | 对调用方观察 JSON 做确定性一致性比较 | 三份 observation 中 `scene/roles/decisions/owners` 的 canonical hash 是否相同 | observation 字段本身；运行独立性 attestation；这些字段是否真实来自运行 | 否 |
| Global protected hash | `PROTECTED/hash-zero` | 1 | E2 | 对调用方指定的 byte slice 做确定性比较 | before/after slice 的声明哈希与实际字节，以及两侧字节是否相同 | 哪些 offset 是保护区、跨度是否完整、是否覆盖全部保护对象 | 否 |
| **合计** |  | **163** |  | **137 caller-graded behavior + 14 hybrid deterministic measurements + 12 caller-attested blind ballots** |  |  |  |

`requirements` 中的计数与代码展开结果一致：`behavior=137`、`idempotency=12`、`blind_review=12`、`route_stability=1`、`protected_hash=1`。

## Manifest 字段来源

下表区分“harness 计算”与“manifest 提供后仅做格式、字面值或哈希绑定检查”。后者不是无效字段，但不能单独证明字段描述的现实事件发生过。

| 字段 | 当前使用方式 | harness 是否重算语义 | 实际可证明的内容 |
|---|---|---|---|
| `cases[].assertions[].result` | 直接进入 137 个 behavior claim 的 PASS/FAIL/NOT_EVALUATED 裁决 | 否 | 只证明 manifest 声明了该结果 |
| `cases[].claims[].atom_id` | 决定 assertion 覆盖哪个资格原子 | 否；只检查 ID 已注册且不重复 | 只证明 claim 指向该 atom，不证明 case 与场景、变体或合同语义匹配 |
| `cases[].claims[].assertion_ids` | 把 assertion 绑定到 claim | 否；只检查存在、唯一且不复用 | 结构引用有效 |
| `cases[].replays[].expected.*` | 与真实 validator 输出比较，形成 `behavior_matches_expected` | expected 不重算；actual 会重算 | 证明 validator 实际结果与调用方预期一致；不等同于预期本身是资格成功标准 |
| `cases[].replays[].recorded.*` | 可选地与重放 actual 比较 | actual 重算，recorded 不重算 | 历史记录与当前重放一致 |
| `generation.run_id` | 安全字符、全局唯一、与 run record 相同 | 否 | 标识符一致，不证明真实会话 |
| `generation.fresh_context` | 必须为 `true` | 否 | 调用方声明 fresh context |
| `generation.blindness_attestation` | 必须等于 `CALLER_ATTESTED_STAGED_CONTEXT` | 否 | 调用方作出指定声明；报告同时写 `blindness_verified=false` |
| run record `fresh_context` | 必须为 `true` | 否 | 与 generation 重复的调用方声明 |
| run record `blindness_attestation` | 必须等于固定字符串 | 否 | 与 generation 重复的调用方声明 |
| run record `artifact_sha256` | 与载入的 input/output/prompt/context 实际 SHA-256 比较 | 是，重算文件哈希 | run record 绑定这些具体字节 |
| run record `qualification_bindings` | 与当前 Skill/contract/requirements SHA-256 比较 | 是，当前绑定由 harness 重算 | 记录绑定当前版本 |
| prompt artifact 内容 | 要求存在、非空并有哈希 | 否，不解析 prompt 语义 | 某些 prompt 字节被保存 |
| context artifact 内容 | 要求存在、非空并有哈希 | 否，不验证隐藏答案、工具可见性或隔离状态 | 某些 context 字节被保存 |
| `idempotency.independence_attestation` | 必须等于固定字符串 | 否 | 调用方声明两个记录独立 |
| idempotency 两个 run record | 校验 ID/hash 不同、链条一致 | 部分：字节/hash/链条重算 | 两份不同记录描述了正确链条；不证明运行由独立生成会话产生 |
| `route_stability.independence_attestation` | 必须等于固定字符串 | 否 | 调用方声明三次运行独立 |
| route observation `scene/roles/decisions/owners` | canonicalize 后比较三次是否一致 | 值本身不推导；一致性会重算 | 三份提交的观察 JSON 一致 |
| ballot `reviewer_kind` | 必须为 `HUMAN` | 否 | 调用方使用了该标签 |
| ballot `reviewer_id_sha256` | 必须是 64 位 SHA-256 格式并与另一票不同 | 否，不验证 preimage 或身份 | 两个字符串不同；不证明两名不同的人 |
| ballot `identity_verified` | 必须为 `false` | 否 | 明确没有身份验证 |
| ballot `attestation_status` | 必须为 `CALLER_ASSERTED_HUMAN_REVIEW` | 否 | 明确是调用方声明 |
| ballot `result` | 直接决定 E4 ballots 是否全部 PASS | 否 | 调用方提交的票面结果 |
| blind review rubric/bundle 内容 | 只要求非空并绑定哈希 | 否，不检查量表充分性、匿名性或是否泄露答案 | ballot 绑定具体 rubric/bundle 字节 |
| `protected_spans[].before/after.{artifact,start,end}` | 用来截取待比较字节 | offset 不推导；slice/hash/equality 会重算 | 所选 slice 未变化，不证明所有保护区均被选择 |
| `tests_total` | 原样复制为 `declared_tests_total`，明确不参与裁决 | 否 | 仅保留声明值 |
| `artifacts.*.sha256` / `size` | 与实际文件重算值比较 | 是 | artifact 完整性与 manifest 描述一致 |
| `bindings` | 与当前 Skill、合同、requirements hash 比较 | 是 | 证据未绑定旧版本 |
| `archived` / `archived_failures` | 控制证据是否可用于当前资格 | 否；执行固定降级规则 | manifest 对证据状态的分类被规则化处理 |

## 机器可观测边界

当前 harness 确实可靠观察并重算以下内容：严格 JSON、重复 key 拒绝、路径不越过 artifact root、artifact SHA-256/size、当前 Skill 快照、审计期间文件漂移、allowlist 且 `shell=False` 的 validator 重放、真实进程退出码、validator JSON 层级状态与输入输出哈希绑定、选定输出的字节相等、选定 observation 的 canonical 相等、选定保护 slice 的字节相等。

它没有观察：生成器实际调用、模型或配置、会话隔离、expected answer 是否被隐藏、run record 是否由运行系统而非调用方制作、场景/角色/决策/owner 是否由真实输出推导、两次运行是否独立、评审者是否为人、是否确实盲评、保护跨度是否完整、以及 137 个 behavior assertions 的 expected/actual 语义。

## 优先 findings

1. **Critical：`qualification_status=PASS` 的文档语义强于证据语义。** 137 个行为原子的专属结论来自 bare assertion result；通用 validator 只验证交付门和不变量。报告应将 PASS 描述为“manifest 声明的原子均满足结构与最低证据包装”，不能描述为 harness 独立观察到完整生成行为。
2. **Critical：E4 的名称暗示已发生人工盲评，但当前证据只到 caller-attested ballot。** requirements 明确 `identity_verified=false`，代码报告也明确 `human_identity_verified=false`，可是 ballot 仍可把原子推进 E4/PASS。文档必须把“人工盲评要求”和“本地可验证证据”分开表述。
3. **High：原子覆盖与 case 语义没有可执行绑定。** claim 指向 atom ID 后，不检查 case 的 scene、positive/negative/conflict 变体、fixture 身份或对应隐藏断言 schema。矩阵覆盖目前是 ID 覆盖，不是 grader 证明的行为覆盖。
4. **High：E3 是绑定后的运行记录，不是 harness 观察的 forward generation。** `fresh_context` 与 blind staging 均为 caller attestation，唯一重放工具是输出 validator，不是生成器。建议名称显式包含 `CALLER_ATTESTED`，或由 harness 自己启动生成并签发不可伪造 receipt。
5. **High：路由稳定和幂等是混合证据。** 字节/JSON 一致性是机器测得的；运行独立性、route observation 的真实性不是。当前输出中的 `run_independence_verified=false` 应进入资格语义，而不只是 trust-boundary 注释。
6. **High：保护哈希只证明所选跨度。** `PROTECTED/hash-zero` 没有自动发现或覆盖率账本，因而不应被文档解释为“全部保护区变化数为 0”。
7. **Medium：`behavior_matches_expected` 表示 actual 与 caller expected 相符，不表示 validator 状态必然为 PASS。** 文档应避免把该布尔值称为行为通过；应分别报告“重放一致”与“交付门成功”。
8. **Positive boundary：artifact integrity 实现较强，但不能替代 provenance。** strict JSON、SHA-256、快照漂移检测、路径限制和安全重放都值得保留；文档应把它们归入 evidence integrity，而不是行为真实性。

## 建议的文档与合同调整

1. 将证据来源作为一等字段公开：`grader_source=DETERMINISTIC | RULE_CHECK | MODEL_REVIEW | VERIFIED_HUMAN | CALLER_DECLARED`，每个 atom 报告实际来源。
2. 在没有外部签名或 harness-owned execution 时，把 E3/E4 分别命名为 `CALLER_ATTESTED_FORWARD_ARTIFACTS` 和 `CALLER_ATTESTED_HUMAN_BALLOTS`；不要使用未加限定的“盲前向”“盲人评”。
3. 为 137 个 behavior atom 定义 atom-specific assertion schema，包含 expected、actual、artifact location、grader implementation/version，并由 grader 产生 result；不要接受 bare result 作为语义证据。
4. 强制 case metadata 与 atom 维度匹配，并验证每场景三组、每 PATH 三变体和 distinct fixture/run 的基数；不要仅靠展开后的 atom ID 表示覆盖。
5. 将 `artifact_integrity_status`、`replay_consistency_status`、`behavior_qualification_status` 和 `human_review_provenance_status` 分开，禁止前两者的 PASS 被表述为后两者的 PASS。
6. 对保护证据增加由 parser 发现的完整 protected-span manifest 和 coverage comparison；对 route observation 增加由受控执行器生成并签名的结构化结果。
7. 若无法验证人类身份和盲性，则 blind-review atom 保持 `NOT_EVALUATED`；至少不要让 `identity_verified=false` 与最终“已完成人工盲评”同时成立。

## 代码依据

- requirements 的 E3/E4、caller attestation 与 `identity_verified=false`：`generation-qualification-requirements.json:113-138,157-178`。
- 合同的人工盲评读感问题与生成资格门：`evaluation-contract.md:154-164,410-432`。
- 只有统一 validator 在 allowlist：`audit_humanize_generation_qualification.py:99-115`。
- run record 被代码明确称为 caller-attested：`audit_humanize_generation_qualification.py:911-974`。
- E3 的 fresh-context/blindness 字面声明检查：`audit_humanize_generation_qualification.py:977-1039`。
- E4 ballot 的 HUMAN 标签、未验证身份、caller-attested 状态与票面结果：`audit_humanize_generation_qualification.py:1042-1160`。
- 幂等、路由稳定、保护 span 的实际测量：`audit_humanize_generation_qualification.py:1195-1405`。
- assertion result 与 claim-to-atom 映射直接来自 manifest：`audit_humanize_generation_qualification.py:1430-1516`。
- `behavior=True` 以及 claim 裁决：`audit_humanize_generation_qualification.py:1645-1686`。
- 总资格汇总：`audit_humanize_generation_qualification.py:1719-1738`。
- 输出明确承认 blindness、independence、human identity 均未验证：`audit_humanize_generation_qualification.py:1935-1943`。
