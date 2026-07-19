# Humanize Academic Chinese v35 根因与成熟度复盘

日期：2026-07-19  
版本：`policy/builder=1.10.5/1.10.5`  
范围：短 PATCH 结构化工具链、真实谓词来源门、首入口严格性、长文 intent span 分区  
结论：v35 把 v34 的自然语言 PATCH 约定升级为可构建、可应用、可验证、可重放自洽性的普通生成能力；同时用真实 GPT/TeX 负例扩展五类窄谓词升级门。它仍是待审候选层，不是自动终稿器或学术正确性裁判。

## 1. 证据边界

本轮只把此前登记为 GPT 生成或归属未解决的 MD/TeX 当作负例压力材料。它们没有进入真人 Voice、事实来源或正向句库。读取时继续跳过 `CET6.tex`；严格 UTF-8 失败的材料不参与规则设计。

主要真实证据来自：

- `gpt_chinese_style_report_detailed.md` 中“未生成、待验证、待实测、条件数角色”等 GPT 状态语言；
- 微信 GPT `main.tex` 的负例压力副本，其中明确区分内部指标、外部验证、候选括号和稳健排序；
- `tests/fixtures/humanize_forward_v10/course_before.tex` 的正反直接许可冲突；
- v34 GENERAL fresh 输出产生的“缺内容 -> 缺衔接”漂移；
- v35 subagent 黑盒重写产生的“配置已经写入，热生效仍待实测 -> 已生效”漏检。

## 2. v34 留下的真实缺口

v34 已要求：

```text
patch_hunks_source_partition=NON_OVERLAPPING
```

但它仍是生成合同，没有独立 parser/applicator。调用方可以：

- 用不同描述重复覆盖同一 source span；
- 把一个大 REWRITE hunk 包在 UNRESOLVED 外面；
- 在 source 变化后继续使用旧 patch；
- 写 `UNRESOLVED` 却替换原句；
- 删除公式、引语或显式保护术语后只说“机械验证未运行”；
- 发布 candidate 后单独修改 result、diff 或 validation；
- 把结构 PASS、validator PASS 或 verifier PASS 写成文风完成。

另有两个旁路缺口：

1. `scaffold_humanize_rewrites.py` 使用宽松 `json.loads`，重复 key、NaN 或 float 可先得到假 `SCAFFOLDED`；
2. 长文 `rewrite_intent.source_spans` 只逐项验 ID/range/hash，不验多个 span 是否重复、重叠或乱序。

## 3. TDD 红队链

所有生产改动均先建立可执行 RED。用户禁止提交，因此没有创建 TDD Git checkpoint。

短 PATCH RED 覆盖：

- 合法四 hunk 混合 patch；
- 重复文本唯一定位与显式 UTF-8 byte offset；
- 重复 ID、重复范围、部分重叠、包含和乱序；
- source SHA、bundle 自哈希、hunk hash 漂移；
- `DELETE_STYLE_SHELL/REWRITE/UNRESOLVED` replacement 不一致；
- duplicate key、未知字段、float、NaN、非法 UTF-8；
- CRLF 中间切分、combining grapheme 切分、新增 bidi/control；
- source/bundle/output 覆盖和 hardlink 路径；
- validator hard FAIL、机械/顶层状态矛盾、before/after evidence hash 假配；
- validator 读取 live source 的 TOCTOU；
- post-publish candidate/result/validation/manifest 篡改与额外文件；
- 零 UNRESOLVED 时错误放行质量完成态；
- text 与 JSON 状态摘要不一致；
- generator projection 未包含普通用户工具。

旁路 RED 覆盖：

- scaffold chunk/decision map duplicate key、float、NaN；
- scaffold 失败先留下空输出目录；
- 长文 intent 的 identical range、partial overlap、out-of-order；
- 相邻不重叠 span 的低误报对照。

## 4. 短 PATCH 三段工具链

### 4.1 Builder

入口：

```powershell
python scripts/build_humanize_short_patch.py source.tex `
  --selection-spec selection.json `
  --output patch.bundle.json `
  --format json
```

selection 使用 `humanize-short-patch-selection/v1`，bundle 使用 `humanize-short-patch/v1`。builder 固定：

- `mode=REWRITE`；
- `effective_output=PATCH`；
- `intensity=LIGHT|BALANCED`；
- source/selection 整体 SHA-256；
- `offset_unit=UTF8_BYTES`；
- 每个 source/replacement 的精确文本、字节范围与 SHA-256；
- `protected_terms`；
- `patch_hunks_source_partition=NON_OVERLAPPING`；
- `unlisted_source_policy=COPY_EXACT`；
- `semantic_judgment=NOT_EVALUATED`；
- `completion_claim_allowed=false`。

重复文本不再只报“有歧义”，而会列出至多 16 个 `candidate_start_bytes`。该值是 UTF-8 原始字节位置，不是 Unicode 字符序号。

### 4.2 Applicator

入口：

```powershell
python scripts/apply_humanize_short_patch.py source.tex `
  --bundle patch.bundle.json `
  --output review-dir `
  --format text
```

applicator 重新验证全部结构，不接受调用方另交 candidate。未列入 hunk 的 source bytes 全部逐字复制。初始 source 先写入 staging 的 `source.snapshot.bin`；统一 validator 只读取冻结快照和确定性 candidate，不读取可能在子进程运行期间被替换的 live source。

validator 返回后必须满足：

- OS exit 与 JSON exit 一致；
- `PASS/0, REVIEW/2, FAIL/1` 元组一致；
- `mechanical=FAIL` 或 `hard=FAIL` 不得伪装为 REVIEW；
- `evidence.before_sha256` 命中 bundle source；
- `evidence.after_sha256` 命中派生 candidate；
- bundle 中的 protected terms 已传入；
- 发布前 live source 与 bundle 再读仍不漂移。

hard FAIL、hash 不一致或状态矛盾均删除整个 staging。正常待审首行为：

```text
DELIVERY REVIEW exit=2
```

### 4.3 Verifier

入口：

```powershell
python scripts/verify_humanize_short_patch.py review-dir --format text
```

发布目录包含七项闭集：

```text
source.snapshot.bin
candidate.review.<ext>
patch.diff
patch.bundle.json
validation.json
result.json
evidence-manifest.json
```

manifest 记录其余六项工件的 path/size/SHA-256 和自身规范 hash。verifier 拒绝额外文件、缺件、hardlink、hash/size 漂移，并重新应用 bundle、重算 diff、核对 validation/result。

文本首行同时显示两种状态：

```text
INTEGRITY PASS exit=0 scope=SELF_CONSISTENCY_ONLY; DELIVERY REVIEW
```

`INTEGRITY PASS` 不证明历史真实性、文风收益、学术正确性、作者身份或外部复核。目录没有外部签名/时间戳；SELF_CONSISTENCY_ONLY 不能被升级成 production trust anchor。

## 5. Unicode、路径与隐私门

v35 拒绝：

- 从 CRLF 中间切 hunk；
- 在 combining mark、ZWJ、variation selector 或 emoji modifier 等明显连接点切 hunk；
- replacement 新增 NUL、bidi override/isolate 或其他 format/control；
- source/spec/bundle 为 hardlink；
- 输入路径链或输出父链含 symlink/reparse point；
- 已存在的 bundle 或 review 输出目录。

当前 Windows 无创建文件 symlink 的权限，因此真实 symlink 测试 skip；hardlink 门已实际运行。该 skip 不能被描述为所有 reparse 情景已通过。

`output_exists` 只输出稳定错误码，不再回显绝对用户目录。bundle、manifest 与报告均不保存 source 绝对路径。

## 6. 五类真实谓词来源门

v35 没有写通用语义理解器，而是从真实负例中加入五个窄 warning：

| code | source 角色 | 错误 rewrite | 低误报控制 |
|---|---|---|---|
| `SPEECH_ACT_ABSENCE_TO_FAILURE` | 字段未生成/未得到 | 字段验证失败、生成逻辑有误 | 保持“仍未生成”不报 |
| `SPEECH_ACT_PURPOSE_TO_RESULT` | 用于比较、校准、检验 | 结果表明、验证了 | 保持“仍用于比较”不报；source 已有结果谓词不报 |
| `SPEECH_ACT_PENDING_CHECK_TO_COMPLETION` | 待实测、待复核、需要重跑 | 已生效、已完成、已证明 | 保持“仍待实测”不报；完成态不跨逗号/分号/冒号取词 |
| `SPEECH_ACT_INTERNAL_TO_EXTERNAL_VALIDATION` | 内部指标/情景投影，明确非外部验证 | 验证了实际、真实或长期状况 | 保留内部/非外部边界不报 |
| `SPEECH_ACT_CANDIDATE_TO_CONFIRMED` | 候选括号/区间、排序不稳健 | 经验证阈值、稳定排序 | 保持候选和条件限定不报 |

每个 finding 固定：

```text
semantic_judgment=NOT_EVALUATED
required_action=PRESERVE_SOURCE_PREDICATE_AND_STATUS
```

它们只定位谓词、对象、完成状态或证据角色升级，不判断配置是否真的生效、模型是否正确、阈值是否成立或指标是否有效。

## 7. Fresh 黑盒结果

### 7.1 COURSE 全链

来源：`tests/fixtures/humanize_forward_v10/course_before.tex`。

四 hunk：

1. 删除重点/教练壳；
2. 原样 `UNRESOLVED` 直接许可；
3. 删除意义/桥接尾句；
4. 原样 `UNRESOLVED` 条件限制。

实际结果：

```text
build=BUNDLED/0
apply=REVIEW/2
hard_invariant=PASS
mechanical=REVIEW
paired_quality=BLOCKED_BY_MECHANICAL_GATE
verify=PASS/0 SELF_CONSISTENCY_ONLY
```

标题、公式源码和两条冲突主张均保留；validator 因删除“必须”登记模态 scope warning，没有误报纯文风层已裁决冲突。

### 7.2 普通用户 CLI

subagent 独立建立 selection 并完整运行 build/apply/verify。重复 build/apply 均 `output_exists/1`，旧 evidence 仍可 verify。源 fixture、snapshot 和 bundle source hash 一致。

subagent 指出的三个文案问题已修：

- ambiguous 错误现在列候选 byte offsets；
- output_exists 不再泄漏绝对路径；
- verifier 首行把 INTEGRITY PASS 与 DELIVERY REVIEW 并列。

### 7.3 谓词黑盒

第一轮 5 个越权样例命中 4 个；“配置已经写入，热生效仍待实测 -> 已生效”因完成态正则跨逗号误认为 source 已含完成谓词，形成真实 false negative。

修复后：

```text
overreach dedicated-code recall = 5/5
safe-control target false positives = 0/5
```

安全稿仍可能因 paired-quality pending 返回顶层 REVIEW/2；不能只比较顶层退出码，必须读取 `mechanical_validation_status`、`speech_act_layer_status` 和 paired-quality 原因。

## 8. 其他工程修复

### 8.1 Scaffold strict ingress

`scaffold_humanize_rewrites.py` 现在在首入口拒绝 duplicate key、float、NaN、非法 UTF-8 和过深 JSON。chunk、decision map、coverage 和 unit-id collision 全部验证后才创建输出目录；失败不再留下假 scaffold。

### 8.2 长文 intent span partition

`rewrite_intent.source_spans` 现在必须：

- 按 source 行递增；
- 范围互不重叠；
- 不得用不同 ID 重复同一范围。

多个 operation 仍可引用同一个已登记 span。该修复没有把合法共享引用误判成 span 重叠。

## 9. 最终回归

```text
full suite: 744 tests, OK (skipped=4)
qualification tests: 41
long finalizer: 132
unified validator: 74
invariant checker: 57
Skill contract: 33
projection builder: 39
short PATCH: 21 (1 symlink environment skip)
scaffold: 8
scripts: compile 28/28; --help 28/28
quick_validate: PASS
SKILL.md: 447 lines
```

资格审计继续诚实返回：

```text
evidence_integrity_status=PASS
qualification_status=NOT_EVALUATED
0 PASS / 0 FAIL / 188 NOT_EVALUATED
exit_code=2
```

## 10. 最终投影

最终工件：

- `build/generator-projection-maturity-v35-final-r2-20260719/`
- `build/generator-projection-maturity-v35-final-r2-manifest-20260719.json`
- `build/generator-projection-maturity-v35-final-r2-repro-20260719/`
- `build/generator-projection-maturity-v35-final-r2-repro-manifest-20260719.json`

两边各 35 文件，逐路径字节差异 0，manifest 字节相同，私有 qualification/replay/second-pass 标识 0 命中。

```text
policy/builder=1.10.5/1.10.5
capability_source=acef26151bf63578bb795f87d8761b9d27607e6601d2d9eb7a93a4550c19aeb6
projection_tree=2d92fe161777cabb68c4e0af97679113cf6886375f5b576a6dd2d7b075e7480c
manifest_file_sha256=e8de67adea02a7adb524fbf05b822249501a10cdf38ac59cd50c797fe400728d
evidence_cap=E2
```

## 11. 准确成熟度裁决

v35 已关闭 v34 明确留下的“短 PATCH 无独立 parser”缺口，并额外关闭一组真实工程旁路。现在可以证明：

- 列出的 hunk 与精确 source bytes 绑定；
- candidate 由 bundle 确定性派生；
- hard invariant 失败不会发布；
- 本地 evidence 被单独修改可由 verifier 发现；
- 五类已登记谓词升级会进入 REVIEW；
- scaffold 与长文 span 首入口不再宽松接受歧义结构。

仍不能证明：

- 调用方列全了所有病灶/冲突/high span；
- 所有自然语言谓词升级都能被正则捕获；
- candidate 比 source 更自然；
- 学术内容、引用、模型、参数或结论正确；
- 作者身份或来源真实性；
- 外部 paired-quality clearance；
- 188 原子生成资格。

因此 v35 的准确定位是：可机器解析、可 fail closed、可自洽重放的生产级中文学术文风待审层。它更难产生虚假闭环，但仍不冒充无需外部复核的最终作者。
