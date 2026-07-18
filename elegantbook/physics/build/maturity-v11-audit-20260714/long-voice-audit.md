# Humanize 长文 Voice Profile 生产路径审计

## 0. 审计结论

当前 `humanize-academic-chinese` 已经有一份相当完整的 Voice Profile 书面合同，也有较强的长文快照、保护区、逐单元验证和源文件不覆盖机制；但是，从真实用户交付路径看，作者声线仍停留在“要求模型自行记得遵守”的层面，没有进入长文准备、改写包、收尾验证和全文完成声明的机器可核验合同。

因此，现阶段不能用 `full_completion_claim_allowed=true` 证明以下命题：

- 已使用用户提供的作者样本；
- 已绑定正确的 Profile 版本；
- Profile 没有被 `RESEARCH/COURSE/MODELING` 的场景默认声线覆盖；
- 混合文档的每个单元已从 `AUTO` 路由到具体场景；
- 分块后没有在不同块中形成不同“修复腔”；
- 全文没有把同一句修复模板各写一次、从而在逐块验证中漏过；
- `NO_CHANGE` 代表完整阅读，而不是批量提交四个汉字的理由；
- 所谓幂等是“把上一轮输出再做一次 Humanize 后不再变化”，而不是“用同一批 rewrite bundle 再组装一次得到相同字节”。

这不是细节缺口。它使体系可能出现一种危险完成态：结构、公式、引语、数字和局部词项均通过，覆盖账本也闭合，但全文已经被统一成场景默认的“克制腔”，仍能获得全文完成许可。

本报告按生产风险分为 5 个 P0 和 7 个 P1，并给出 12 个可由 fresh agent 盲跑的前向/变形测试。报告不读取现有测试、历史 build、资格材料或历史报告，也没有修改 Skill。

## 1. 审计范围与方法

### 1.1 实际读取范围

主路径：

- `SKILL.md`
- `references/voice-profile.md`
- `references/long-document-workflow.md`
- `scripts/prepare_humanize_long_document.py`
- `scripts/finalize_humanize_long_document.py`

为理解上述文件的直接合同，只补读：

- `references/workflow.md`
- `references/operational-contract.md` 中任务参数、优先级、谓词来源门、执行状态和完成声明相关章节

明确未读：

- `tests/`
- 既有 `build/` 产物
- 历史报告
- 资格矩阵、oracle、fixture 与资格审计材料

### 1.2 审计视角

不问“文档有没有写到”，而问五件事：

1. 用户给了样本后，哪一个不可伪造的工件证明 Profile 被建立并使用？
2. 用户给同一篇稿子换两个作者 Profile，生产链是否必然产生可解释的差异？
3. 文档切成不同块后，同一段的处理是否保持稳定？
4. 某一块被改坏后，能否恢复到前一版已接受结果，而不只恢复源稿？
5. `full_completion_claim_allowed=true` 究竟证明了什么，又没有证明什么？

### 1.3 当前实际数据流

```text
作者样本 ──> [人工/模型在上下文中临时理解]
                         │
                         │ 没有 profile artifact/hash/version
                         ▼
源 MD/TeX ──prepare──> chunks + units + ledger
                         │
                         │ chunk 只有全局 scene（可仍为 AUTO）
                         │ 没有 voice_profile 字段
                         ▼
                  fresh agent 写 rewrite bundle
                         │
                         │ bundle 合同不接受 profile/scene evidence
                         ▼
                    finalize 逐单元验证
                         │
                         │ validate(before, after, scene, keep/warning)
                         │ 没有 profile 参数，没有全文声线门
                         ▼
             rendered[_partial] + full_completion_claim_allowed
```

这条链可以证明“当前提交的每个单元是否通过现有局部保护门”，不能证明“输出保留了指定作者的声线”。

## 2. 合同与实现对照

| 合同承诺 | 书面位置 | 当前实现证据 | 审计判断 |
|---|---|---|---|
| 有作者样本时生成并优先使用 Voice Profile | `SKILL.md:101-105`；`voice-profile.md:19-34` | prepare CLI 只有 `--scene`、预算和样式包装；无 `--voice-profile/--author-sample` | 未进入正式长文入口 |
| 每个 unit 记录 Profile 版本与置信等级 | `long-document-workflow.md:261-270,313-327` | `build_units()` 输出字段无 `voice_profile/profile_version/confidence`，ledger 字段也无 | 合同与工件不一致 |
| 混合文档按完整 unit 路由场景 | `long-document-workflow.md:313-327` | prepare 把一个 `scene.upper()` 原样写给所有 unit；`AUTO` 不会被解析 | 未实现逐单元路由 |
| Profile 高于场景默认 | `operational-contract.md:73-83,102` | finalize 不读取 Profile，也不校验场景对 Profile 的覆盖 | 只能靠生成者自觉 |
| 相邻块通过只读上下文保持衔接 | `long-document-workflow.md:122,294-310` | `attach_read_only_context()` 仅按同一物理文件相邻；跨 `\input` 文件断开 | 文档级连续性不成立 |
| 长文幂等是把 clean 输出作为新输入重跑 | `long-document-workflow.md:509-527` | finalize 的 `idempotency=PASS` 只比较已发布目录与当前 staging 字节 | 名称相同，语义不同 |
| 已完整阅读的单元才可 `NO_CHANGE` | `long-document-workflow.md:361,407-420` | finalize 只要求理由至少 4 个汉字，并对 before=after 跑局部 validator | 无法支持“完整阅读”声明 |
| 全文完成包含 Voice、跨块一致性和无 churn | `long-document-workflow.md:39-53,627-639` | 完成布尔值仅依赖 pending、unresolved、格式/编译硬失败 | 完成门范围过窄 |

## 3. P0 缺口

### P0-1：Voice Profile 是说明性合同，不是生产工件

#### 证据

`voice-profile.md` 定义了样本准入、字符阈值、唯一单元、置信等级、场景子档案、`do_not_amplify` 和版本更新。长文合同又要求每个 unit 记录 `voice_profile`、Profile 版本和置信等级。

但实际入口存在四次断链：

1. `prepare_humanize_long_document.py` 的 CLI 无 Profile 参数；
2. `build_units()` 生成的 unit 无 `voice_profile`、profile hash、版本或置信等级；
3. rewrite bundle 的字段白名单只允许 `decision/masked_text/reason/keep_reasons/warning_*`，不能声明所用 Profile；
4. finalize 调用统一 validator 时只传 before、after、scene、keep reasons 和 warning proposal，没有 Profile。

`finalization_metadata.json` 同样不记录 Profile 身份或声线验证结果。

#### 用户后果

- 用户明确说“按我过去的写法润色”，Profile 即使被模型临时读取，最后也没有工件证明它被使用。
- 同一输出可以在 `PROFILE:A`、`PROFILE:B` 和 `SCENE_DEFAULT` 三种声线请求下原样复用，并获得相同完成态。
- 生成者忘记加载 Profile、上下文压缩时丢失 Profile、不同 chunk 使用了不同 Profile 版本，都不会被 finalize 发现。
- `full_completion_claim_allowed=true` 容易被读者误解成“作者声线也已通过”，实际不包含这层含义。

#### 必须修复

引入不可选的 `voice_profile.json` 工件合同，而不是只在提示上下文中放一段描述。至少包含：

```yaml
profile_id:
version:
profile_sha256:
confidence: DEFAULT | LOW | MEDIUM | HIGH
sample_manifest_sha256:
sample_scenes:
readable_author_chars:
unique_units:
feature_evidence:
do_not_amplify:
scene_overrides:
```

prepare 必须冻结该工件，将 `profile_id/version/sha256/confidence` 写入 run metadata、unit、chunk 和 ledger；rewrite bundle 必须回显当前绑定 hash；finalize 必须拒绝缺失、错配、旧版本重放和快照后变更。

没有 Profile 时也应冻结一个显式的 `SCENE_DEFAULT` 工件，而不是让“无字段”同时表示“没提供”“没加载”“被忽略”。

### P0-2：`AUTO` 只是字符串，没有形成逐单元场景裁决

#### 证据

长文合同要求先识别文档用途，再按完整 unit 路由；混合文档允许不同 unit 使用不同场景，并要求记录自动得分、最终场景和平局裁决。

实际代码中，prepare 接收一个全局 `scene`，随后对每个文件调用：

```python
build_units(..., scene=scene.upper(), ...)
```

`build_units()` 又把这个字符串直接写入每个 unit。没有路由函数、得分、平局裁决或 `scene_final`。当用户按默认值传 `AUTO` 时，所有 chunk 的场景仍是 `AUTO`。rewrite bundle 又不能覆盖 unit.scene，finalize 只把 `AUTO` 继续传给局部 validator。

#### 用户后果

- 一份同时包含课程解释、模型结果和同行讨论的 TeX，会把所有单元交给同一个未决 `AUTO` 标签。
- fresh agent 只能自行猜场景；不同 chunk 可以作出不同且不可追溯的猜测。
- 若 agent 为求稳定统一采用 `RESEARCH` 的“克制正式”，课程段和工程段会被压成同一种腔调。
- 完成元数据没有 `AUTO unresolved` 门，因此这种未路由文档仍可能获得全文完成许可。

#### 必须修复

prepare 应产生以下不可变字段：

```yaml
scene_requested: AUTO
scene_final: COURSE | MODELING | RESEARCH | GENERAL
scene_evidence: [heading-role, paragraph-function, user-declaration]
scene_score:
scene_tie_break:
scene_router_version:
```

`scene_final=AUTO` 必须是 `REVIEW`，不能进入可完成态。显式全局场景也要记录为 `user-declared`，以便区分“用户锁定”与“路由器猜测”。

### P0-3：全文完成门对作者声线和跨块模板化完全失明

#### 证据

finalize 的局部接收条件是统一 validator 返回 `PASS`。随后全文只运行结构不变量检查；最终完成布尔值为：

```python
complete and unresolved == 0 and not hard_failure
```

其中没有：

- Profile 是否绑定；
- Profile 是否被应用；
- `scene_final` 是否已经解析；
- 全文句长、第一人称、标点、转场和收尾是否偏离 Profile；
- 同一个“修复短语”是否在每个 chunk 各新增一次；
- 同类章节是否被写成不同声线；
- 场景默认是否覆盖了作者稳定习惯。

局部 validator 每次只看到一个 unit 的 before/after。同一句新修复模板若在每块只出现一次，单块内部未必构成重复；全文却可能出现十几次。

#### 用户后果

“每块都不坏”被错误提升成“全文声线一致”。最典型的失败不是明显病句，而是所有块都变得干净、克制、短结尾，但作者原本偏好的长句、第一人称、括号补充和段尾展开全部消失。

#### 必须修复

在发布前新增文档级 `voice_and_churn_gate`，至少比较：

- Profile 允许的第一人称、对象主语和无主句分布；
- 句长分布和停顿设备，而不是机械均值配额；
- 标点、括号、冒号、分号和列表使用条件；
- 章节收尾方式与显式小结密度；
- 新增 4-12 字修复短语的跨 unit 覆盖率；
- 同类 unit 的场景声线离散度；
- `do_not_amplify` 在全文是否被放大；
- 与原文、Profile 和场景默认三者的冲突裁决。

输出必须区分：

```yaml
voice_binding_status:
voice_conformance_status:
cross_unit_repetition_status:
scene_routing_status:
```

任何一项 `NOT_EVALUATED/REVIEW` 都不能被全文完成布尔值覆盖。

### P0-4：`NO_CHANGE` 可以提交理由，不能证明完整阅读

#### 证据

合同写的是“已连续阅读且无需改写”。实际收尾器只检查：

1. `reason` 至少包含 4 个汉字；
2. `keep_reasons` 结构合法；
3. before 与 after 相同的局部 validator 返回 `PASS`。

于是“无需修改”“保持原文”“本段可用”都满足理由长度。对于没有 high 词项命中的普通正文，调用者可以为所有 PENDING unit 批量生成同一种 `NO_CHANGE` 包。代码没有要求：

- 识别该 unit 的主导节奏；
- 说明它为何符合当前 Profile；
- 给出覆盖全文的观察位置；
- 证明 read-only context 被用于衔接判断；
- 区分真正阅读和脚本批量填充。

#### 用户后果

覆盖账本可以从 PENDING 全部变成 NO_CHANGE，随后 `processable_scope_complete=true`，甚至 `full_completion_claim_allowed=true`，但这只能证明“所有 unit 都提交了合法包”，不能证明“所有 unit 都被完整阅读”。

#### 必须修复

不要声称机器能证明主观的“阅读发生过”。应把合同改成可证明的状态：

- `NO_CHANGE_EVIDENCE_SUBMITTED`：提交了 hash-bound 的范围证据；
- `NO_CHANGE_VALIDATED`：局部保护门与全局声线门均通过；
- `HUMAN_REVIEWED`：只有外部可验证的人类审批才能使用。

NO_CHANGE 包至少应绑定：

```yaml
unit_sha256:
profile_sha256:
scene_binding_sha256:
observed_voice_features: [至少两个带位置的观察，或显式 NONE_WITH_REASON]
candidate_decisions_summary:
context_continuity_decision:
```

同一理由跨多个 unit 复用应进入 `REVIEW`。这仍不能证明人真的读了，但能阻止最廉价的批量假闭环，并让完成声明准确降格为“提交与验证覆盖完成”。

### P0-5：幂等状态验证的是组装字节，不是文风收敛

#### 证据

书面合同把幂等定义为：把上一轮 clean 输出固定为新输入，使用相同参数、规则和 Profile 重跑，第二次 patch 应为空或仅含格式规范化。

实际 finalize 的幂等逻辑是：若发布目录已存在，比较当前 staging 与已发布目录的文件哈希。使用同一份 rewrites 重新 finalize，自然会得到相同字节，从而记 `idempotency=PASS`。这没有再次执行 Humanize，也没有检验模型是否会继续同义词轮换、重新拆句或改变段尾。

更严重的是，第一次完整发布时 `idempotency` 可以是 `NOT_RUN`，但 `full_completion_claim_allowed` 不依赖 idempotency。

#### 用户后果

一个首轮仍会在第二次 Humanize 中大幅变化的稿件，也能第一次就获得全文完成许可。用户看到 `idempotency=PASS` 时还可能误以为做过语义上的二次收敛验证。

#### 必须修复

把状态拆成：

```yaml
assembly_replay_idempotency: PASS | FAIL | NOT_RUN
humanize_second_pass_convergence: PASS | REVIEW | FAIL | NOT_RUN
```

只有第二项由独立 fresh pass 证明所有 unit 为 `NO_CHANGE` 或空 patch，才能支持“文风已收敛”。若产品不愿把二次生成设为全文完成硬门，就必须从完成定义中删除该承诺，不能继续用同名 `idempotency` 替代。

## 4. P1 缺口

### P1-1：短样本容易误学，Profile 本身没有验证器

`voice-profile.md` 规定 300/1000/5000 汉字阈值、规范化唯一段落和至少三个位置，但没有可执行 builder、schema 或 validator。当前没有工件能验证：

- `readable_author_chars` 是否排除了引语、公式、代码和模板；
- `unique_units` 是否去重；
- 某个 feature 的三次出现是否来自三个独立位置；
- LOW Profile 是否只启用了显著习惯；
- `confidence: HIGH` 是否被调用者手写伪造；
- `do_not_amplify` 是否至少有一项并有证据；
- 300 字附近的一句新增文本是否导致整套句法/词汇偏好突然启用。

尤其是 LOW/MEDIUM 只要求“出现 3 次”，没有要求跨独立文本单元。一个窄段中重复三次的口头禅可能被误判为作者稳定声线。

建议新增 `build_humanize_voice_profile.py` 与 JSON schema。每个 feature 都要记录支持位置、反例位置、适用场景和可用置信等级；Profile 总体置信高不代表每个 feature 都是高置信。

### P1-2：跨文件文档顺序和相邻上下文丢失

`attach_read_only_context()` 先按 `file_id` 分组，再只连接同一物理文件中的前后 unit。于是：

- `chapter-a.tex` 的最后一段不会成为 `chapter-b.tex` 首段的只读前文；
- `main.tex` 中 `\input{a}\input{b}` 的展开顺序没有进入 unit adjacency；
- nested include 使用队列遍历，而不是严格的 TeX 文档深度优先展开；
- file manifest 没有书面合同承诺的 `include_order` 字段。

章节交界处恰恰最需要维持称谓、第一人称、回指和收尾节奏。当前这些位置上下文为零，fresh agent 最容易回退到场景默认。

建议建立 canonical document expansion order，并让 `context_before_unit/context_after_unit` 跨文件连接。多 seed 输入必须明确是多个独立文档还是一个组合文档，不能按路径排序暗中拼接。

### P1-3：没有真正的 overlap owner，也没有临时合并单元入口

合同描述了 overlap ID、owner、reader 和“跨块衔接必须同时改两侧时提升为临时合并单元”。prepare 实际只给相邻块各附一段只读字符串，没有 overlap manifest，也没有创建 merged unit 的命令。rewrite bundle 只能提交当前 masked text。

这导致两种坏选择：

- 各块独立修自己的首尾，产生重复转场或语气断裂；
- 为避免越界，两个块都不处理真正需要双侧调整的衔接。

建议将重叠段建成独立、唯一 owner 的 span，或提供 hash-bound 的 `merge_units` 准备步骤。任何临时合并必须重算 chunk、保护跨度和完整性清单，不能手改原 run-dir。

### P1-4：只读上下文复制检测只拦完整上下文，拦不住局部搬运

`_copied_read_only_context()` 对 before/after 和 context 去空白后，只检查“完整 context 字符串是否出现在改后 unit”。若生成者复制 context 中间 8-20 个汉字、把一整句拆成两段，或只搬运前半句，该门不会命中。

这既可能造成跨块重复，也可能把上一块的作者事实误搬进下一块。建议使用保护边界感知的新增 n-gram 比较，并区分“原 unit 已有”和“改后新增”。不能跨公式、引语、标题或列表边界拼接。

### P1-5：跨块修复模板没有全文级重复门

每个 unit 独立 validator 看不到其他 chunk 的改后文本。假设 12 个 chunk 各新增一次“就这一结果而言”，单块都可能自然，全文却形成新的机器口头禅。

建议在 rendered staging 上运行全文级新增短语覆盖率：报告短语出现次数、涉及 unit 数和相对 before 的增量；重点检查由改写引入而非原文已有的 4-12 字片段。只在跨至少 3 个 unit 或超过 Profile 基线时升级，避免把正式术语误判为模板。

### P1-6：局部修订会覆盖上一版 partial 与逐节 diff，回退证据不足

当 `rendered_partial` 已存在且新 staging 不同，finalize 把它视为 `additional_or_revised_unit_bundles`：记录旧/新目录哈希后删除旧 partial，并用新 partial 替换。随后 validation 和 diffs 目录也用本轮 staging 替换。

`partial_history.jsonl` 只有整目录哈希，没有保存：

- 被修订 unit 的上一版正文；
- 上一版逐节 diff；
- 新版本 supersedes 哪个 unit hash；
- 修订理由；
- 一键恢复旧已接受版本所需的不可变对象。

因此“源文件不被覆盖”是成立的，但“回到上一版已接受 Humanize 结果”没有完整证据。建议使用 append-only 的 run revision 目录，按 `unit_id/hash_after` 保存正文、diff、validation 和 parent hash；发布 head 只更新指针，不删除历史对象。

### P1-7：Markdown 正文链接的递归范围承诺没有实现

长文合同称会追踪“Markdown 相对链接中明确作为正文纳入的文件”。prepare 只实现 TeX 的 input/include/subfile 发现；Markdown 文件不会从 `main.md` 的正文链接递归纳入。若用户只把 `main.md` 作为入口，链接章节可能完全不进 manifest，工具仍可对已看到的一个文件闭合覆盖。

建议不要把所有链接自动当正文；应提供显式 `--markdown-body-link` 规则或清单文件。用户明确声明链接章节属于全文而工具未纳入时，必须 `UNRESOLVED_SCOPE`，不能给全文完成许可。

## 5. 可执行 fresh forward / 变形测试

### 5.1 盲测纪律

所有含生成模型的测试都采用同一纪律：

1. fresh agent 只看到正式安装的 Skill、原始输入、用户任务和允许的作者样本；
2. 不给 agent 本报告、失败预期、oracle、历史输出或拟修规则；
3. agent 完成后，独立 evaluator 再读取输出与机器产物；
4. 事实、公式、数字和保护跨度先做硬不变量比较；
5. 声线比较只检查允许的风格维度，不把内容正确性混进 oracle；
6. 测试失败不能靠在 prompt 中追加答案式提示修复，必须回到正式生产文件。

### FWD-V01：Profile 绑定前向测试

**Fixture**

- `author-samples/`：3 个可确认作者单元，共 1200-1800 汉字，RESEARCH 场景；
- `target.tex`：含 3 个可编辑小节、一个公式和一个引语；
- 样本中稳定使用第一人称报告选择、分号连接条件、括号作短限定，且不使用显式“综上”。

**用户任务**

> 按这些确认由我写的样本保留我的声线，对 target.tex 做 BALANCED 全文润色。

**执行**

1. fresh agent 建 Profile；
2. prepare 长文；
3. 改写所有 PENDING chunk；
4. finalize；
5. evaluator 只在结束后检查 artifacts。

**通过 oracle**

- run metadata、每个 unit 和 rewrite bundle 均绑定同一 profile id/version/hash；
- sample manifest 的去保护、去重字符数支持 MEDIUM；
- final metadata 有 `voice_binding_status=PASS`；
- Profile 文件在 prepare 后改一个字，finalize 必须 FAIL；
- 若删除 Profile 参数重新跑，必须显式变为 SCENE_DEFAULT，不能悄悄复用旧声线声明。

**当前预期**

正式 prepare CLI 不接收 Profile；现有工件无法满足 oracle。

### META-V02：Profile 交换变形测试

**Fixture**

同一 `target.md`，准备两个同场景、同置信度 Profile：

- A：保留已有第一人称，普通说明偏长，常用分号，段尾停在限制条件；
- B：对象主语优先，短句较多，括号补充少，段尾停在观察结果。

目标文本同时包含可合法保留/重排的作者动作、对象观察和限制，不要求新增任何事实。

**变形**

只交换 Profile，输入正文、场景、强度和保护项完全不变。

**通过 oracle**

- 两次输出的事实谓词、数字、公式、否定和模态完全一致；
- A/B 在已声明风格维度上产生方向一致、可解释的差异；
- A/B 不能输出完全相同的场景默认腔；
- 不允许用复制样本句子来制造差异；
- final metadata 分别绑定 A/B hash。

**当前预期**

finalize 对 Profile 不可见，同一输出可在 A/B 下均通过。

### META-V03：重复样本扩容攻击

**Fixture**

一个 260 汉字作者段落，其中某个句首出现 2 次。构造变体：

- S1：原始段落；
- S2：把同一段复制 25 次；
- S3：只改变空格、换行和全半角标点后复制 25 次。

**通过 oracle**

- S1/S2/S3 的规范化唯一作者单元数相同；
- 三者都不得升级为 HIGH；
- 复制不能使某个 feature 从不足支持变成稳定偏好；
- profile report 明确给出 duplicate family 和被排除字符数。

**当前预期**

文档写了“不要复制凑样本量”，但没有 builder/validator 可执行该规则。

### META-V04：299/300/999/1000 字阈值与窄样本误学

**Fixture**

从同一作者文本构造四个真实唯一前缀：299、300、999、1000 个可读汉字。每份样本只让一个习惯跨 3 个独立位置出现，其他习惯均不足 3 次。

**通过 oracle**

- 299 为 DEFAULT；300/999 为 LOW；1000 为 MEDIUM；
- 从 299 增至 300 只允许启用有三处证据的那个 feature，不能突然填满词语、收尾、版式和句法字段；
- 每个启用 feature 都有 3 个位置和至少一次反例检查；
- 删除其中一个支持位置后，该 feature 自动降级或停用；
- 同一窄段内的三次口头禅不能自动变成跨文档稳定偏好。

**当前预期**

现有 Profile 模板无逐 feature 证据，也无机器阈值门。

### FWD-L05：混合文档 `AUTO` 路由前向测试

**Fixture**

`main.tex` 含三个完整小节：

1. 课程题解：读者要判断适用条件；
2. 建模结果：给出方案比较与耗时取舍；
3. 研究讨论：报告观察并保留一个限制。

**执行**

```powershell
python scripts/prepare_humanize_long_document.py main.tex `
  --output run --scene AUTO
```

**通过 oracle**

- 三个 unit 的 `scene_final` 分别为 COURSE/MODELING/RESEARCH；
- 每个都有可审计 evidence 与 tie-break；
- 任一 PENDING unit 仍为 `scene_final=AUTO` 时 finalize 至少 REVIEW；
- Profile 在三个场景间使用同一 base hash，只叠加对应 scene override。

**当前预期**

所有 unit 只会保存字符串 `AUTO`。

### META-L06：分块预算不变性测试

**Fixture**

一篇 16000-20000 汉字长文，每个段落有稳定 ID 注释；包含跨段回指，但无跨段事实依赖。

**变形**

分别使用：

```powershell
--max-author-chars 4000
--max-author-chars 7000
```

其他输入、Profile、规则版本和用户任务相同。两个 fresh agent 分别处理，不看到对方结果。

**通过 oracle**

- 对齐同一 paragraph ID 后，非边界段的 KEEP/DELETE/REWRITE 决策一致；
- 同一段不能因落在块首/块尾而改成不同场景声线；
- 句首、标点和收尾差异不能系统性随 chunk 边界变化；
- 两个版本的跨 unit 新增模板排行应近似一致；
- 若必须同时改两侧，两个版本都应触发同一个 merged-unit 机制。

**当前预期**

现有路径没有 profile binding、稳定 paragraph identity、merged-unit 工件或 chunk-boundary invariance gate。

### FWD-L07：跨 `\input` 章节上下文测试

**Fixture**

```tex
% main.tex
\input{chapter-a}
\input{chapter-b}
```

`chapter-a.tex` 末段明确建立局部简称和一个未闭合的讨论边界；`chapter-b.tex` 首段用该简称回指。

**执行**

只把 `main.tex` 作为 seed 运行 prepare。

**通过 oracle**

- canonical document order 为 main -> chapter-a -> chapter-b 的实际展开顺序；
- chapter-b 首个 unit 的 `context_before_unit` 指向 chapter-a 最后 unit；
- read-only context 包含 chapter-a 最后完整作者段，而不是空字符串；
- 改换两条 input 顺序后，邻接关系相应改变；
- nested include 使用文档展开顺序，不使用广度优先文件发现顺序。

**当前预期**

上下文只在同一 `file_id` 内连接，chapter-b 首块没有 chapter-a 的前文。

### FWD-L08：跨块修复口头禅放大测试

**Fixture**

12 个 PENDING unit，每个都有不同事实，但都含一个可删除的轻微模板路标。为每个 unit 提交局部自然、事实不变的 rewrite，并让每个改后块只新增一次相同短语“就这一结果而言”。

**通过 oracle**

- 每个局部 validator 可以先独立给出结果；
- 全文门必须报告该短语新增 12 次、覆盖 12 个 unit；
- 若 Profile 无此偏好，全文至少 REVIEW；
- 把短语分散为不同、由上下文需要的衔接后，global gate 才可 PASS；
- 正式术语跨块重复不得被误报，测试必须使用“新增修复壳”而非领域词。

**当前预期**

finalize 没有 rendered 全文的新增短语覆盖率门；逐块一次可能漏过。

### FWD-L09：批量 `NO_CHANGE` 虚假闭环测试

**Fixture**

一篇没有 high 词项、公式或复杂结构的中性 Markdown，prepare 后产生至少 5 个 PENDING unit。

为每个 unit 自动生成：

```json
{
  "decision": "NO_CHANGE",
  "reason": "无需修改",
  "keep_reasons": {}
}
```

**通过 oracle**

- 同一四字理由跨 5 个 unit 复用必须 REVIEW；
- 没有 profile-fit、候选摘要和 context continuity evidence 时不能形成“完整阅读”或“全文声线已审”声明；
- final metadata 可写 coverage bundle 已提交，但 `voice_conformance_status=NOT_EVALUATED`；
- `full_completion_claim_allowed` 不得因此为 true，除非产品把该布尔值明确重命名为仅覆盖/保护完成。

**当前预期**

只要 unchanged validator 对这些单元 PASS，四字理由就满足现有结构门。

### META-L10：真正的二次 Humanize 收敛测试

**Fixture 与步骤**

1. 完成一次长文改写并发布 `rendered/`；
2. 把 `rendered/` 作为全新的 source，使用相同 Profile、scene route、规则版本和强度启动另一个 run-dir；
3. fresh agent 不读取首轮 rewrite bundle，只读正式 Skill 与第二轮输入；
4. 比较第二轮 patch。

**通过 oracle**

- 第二轮所有 unit 为 NO_CHANGE，或只有事先允许的格式规范化；
- 不能出现同义词轮换、标点往返、句序往返或新的统一短语；
- 第二轮 run 绑定第一轮 rendered manifest hash；
- `humanize_second_pass_convergence=PASS` 与 `assembly_replay_idempotency` 分开记录。

**当前预期**

现有 `idempotency=PASS` 不执行上述第二轮，且首轮 `NOT_RUN` 不阻止全文完成。

### FWD-L11：partial 修订与局部回退测试

**Fixture**

两单元 A/B：

1. run 1 只提交 A-v1，发布 partial；
2. run 2 提交 A-v2 与 B-v1，二者均通过；
3. evaluator 判定 A-v2 虽通过局部门，但声线比 A-v1 更差，要求只回退 A；
4. 不允许重读源文件后凭记忆重写 A-v1。

**通过 oracle**

- A-v1 的正文、diff、validation、profile hash 与 parent revision 仍存在；
- A-v2 声明 `supersedes=A-v1-hash`；
- 可原子移动 head 回 A-v1，同时保留 B-v1；
- 回退后重新计算 rendered manifest 和全局声线门；
- history 不能只有旧/新目录 hash。

**当前预期**

partial 替换会删除旧派生目录，validation/diffs 也被当前轮替换；没有 unit 级不可变历史。

### FWD-L12：Markdown 链接正文范围测试

**Fixture**

`main.md` 明确写“第二章为正文组成部分”，并链接 `chapters/ch2.md`。用户任务明确要求“处理 main 及链接的第二章全文”。只把 `main.md` 传给 prepare。

**通过 oracle**

- 工具要么通过显式 body-link 规则纳入 ch2，要么标 `UNRESOLVED_SCOPE`；
- ch2 未进入 file manifest 时不得给全文完成许可；
- 普通外部链接、参考资料和图片不得被误纳入；
- manifest 记录链接为何被认定为正文。

**当前预期**

prepare 没有 Markdown link discovery，ch2 不会因该入口自动纳入。

## 6. 修复优先级与最小生产闭环

### 第一阶段：先让完成声明诚实

1. 将 `full_completion_claim_allowed` 拆成：
   - `coverage_completion_claim_allowed`
   - `voice_completion_claim_allowed`
   - `humanize_completion_claim_allowed`
2. 在 Profile 未绑定、scene 仍为 AUTO、全局声线门未运行或二次收敛未运行时，后两者不得为 true。
3. `NO_CHANGE` 不再写“已完整阅读”的机器证明，只写可核验的 coverage/evidence 状态。
4. 把当前 `idempotency` 重命名为 `assembly_replay_idempotency`。

这一步应先做，因为它不要求立刻解决全部生成质量，却能立即拦截错误完成态。

### 第二阶段：把 Voice Profile 变成一等工件

1. 新增 profile builder/schema/validator；
2. 样本做角色过滤、保护区剔除、规范化去重和逐 feature 证据；
3. prepare 冻结 Profile 并写入所有 unit；
4. rewrite bundle 绑定 Profile hash；
5. finalize 验证 Profile 未漂移；
6. 默认声线也使用显式工件和披露状态。

### 第三阶段：实现文档级场景与声线门

1. `AUTO` 在 prepare 阶段解析为 final scene；
2. 建 canonical include expansion order；
3. 跨文件提供前后文；
4. 添加跨 unit 新增模板、节奏、收尾和 Profile 偏离检查；
5. 引入 merged-unit 或可审计 overlap owner；
6. 最终声明绑定 global gate 结果。

### 第四阶段：补齐收敛与回退

1. 二次 Humanize 使用独立 run-dir 和 fresh agent；
2. 记录 content-level convergence，而不是重放字节；
3. partial revision 使用 append-only unit object store；
4. 每次修订写 parent/supersedes hash；
5. 支持按 unit 回退后重新发布全文并复跑 global gate。

## 7. 不应采用的伪修复

- 只在 `SKILL.md` 再加一句“务必保留作者声线”；断链发生在工件与门禁，不在提醒强度。
- 只给 chunk 增加一个自由文本 `voice_profile: used`；没有 hash、版本和样本证据时仍可自报。
- 用固定句长、第一人称比例或标点配额代替 Profile；这会制造另一种统一 AI 腔。
- 把所有 `AUTO` 直接变成 `RESEARCH`；这正是场景默认覆盖作者声线的来源。
- 把全局重复门做成无条件禁词表；正式术语和定义必须按新增量、跨 unit 覆盖和功能判断。
- 继续把相同 staging hash 叫做 Humanize 幂等；它最多证明组装确定性。
- 给 NO_CHANGE 理由提高到 20 个汉字；更长套话仍不能证明阅读，必须绑定位置与 Profile evidence。
- 只保存整目录旧 hash；hash 能证明旧对象曾存在，不能恢复旧对象。

## 8. 成熟度判断

当前长文路径在“源文件安全、快照完整、保护区恢复、逐单元局部验证、失败不覆盖源稿”方面已经接近生产工程；在“作者声线可证、混合场景可证、跨块一致性可证、真实二次收敛可证、已接受局部版本可回退”方面仍未形成生产闭环。

准确表述应是：

> 当前工具能够对长文单元执行可审计的结构与局部文风保护流程，但 Voice Profile 尚未进入长文工件和完成门，全文声线保留、跨块一致性与二次 Humanize 收敛仍未被机器验证。

在 P0-1 至 P0-5 未进入正式实现并通过本报告的 fresh forward/变形测试之前，不建议把该 Skill 的长文 Voice Profile 能力称为成熟生产能力，也不建议让 `full_completion_claim_allowed` 单独承担“全文拟人化已完成”的用户语义。
