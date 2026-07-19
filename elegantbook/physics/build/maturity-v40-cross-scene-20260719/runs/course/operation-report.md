# Course Short PATCH Operation Report

## 1. 配置与边界

```text
mode=REWRITE
scene=COURSE
intensity=BALANCED
requested_output=PATCH
effective_output=PATCH
voice_profile=NONE
voice_disclosure=SCENE_DEFAULT
report_context=NONE
source_kind=DOCUMENT
document_format=TEX
corpus_action_support=NONE
```

源文件按显式 UTF-8 成功读取，未修改。来源按用户要求视为 `MODEL_ORIGIN_UNRESOLVED` 压力输入，只用于本次负向审阅，不作为个人 Voice、真人范文或正向句库。源文件 SHA-256 为 `167a12d4d3a0a0e1a1cf6a5e6ecd13eb2bac5cae95b8d88820c256637360b6f9`，共 5142 个 UTF-8 字节。

本次只调整课程讲解文风：减少路线主持、重复回指、第一人称操作旁白和相邻短句的机械分割。标题、公式、TeX 命令/环境、数字和 definition 环境正文均未列入可变 hunk；学术正确性与自然语言语义完整性不在本流程的证明范围内。

## 2. Scaffold 与覆盖计数

| 项目 | 数量/状态 |
|---|---:|
| source `AUTO` candidate high | 0 |
| final candidate high | 0 |
| authoring `AVAILABLE` suggestions | 0 |
| authoring `SUPPRESSED` suggestions | 0 |
| registry spans | 18 |
| selected spans | 18 |
| final hunks | 17 |
| suggested-span hunks | 0 |
| manual-range hunks | 17 |
| manual selected `KEEP` | 1 (`M003/S003`) |
| explicit conflicts | 0 |
| unresolved hunks | 0 |

`scaffold create` 返回 `NO_HIGH_FINDINGS high=0 suggestions=0`。这不等于 `NO_CHANGE`；连续阅读发现的词库外病灶均登记为 `finding_ids=[]` 的手工 registry span。由于 suggestion inventory 为空，下面每个最终 hunk 都不是 authoring scaffold 的 `AVAILABLE` suggestion。

Coverage 为 `PASS`，但其范围严格限于 `ENUMERATED_HIGH_AND_BOUND_DECLARATIONS_ONLY`；`coverage_completion_claim_allowed=true` 不证明 scanner 找全了所有文风问题，也不证明语义完整或改后质量已放行。

## 3. Hunk 来源范围

范围单位均为原始 source 的 UTF-8 字节，使用半开区间 `[start_byte,end_byte)`。

| Hunk | 精确 source range | 决策 | Authoring suggestion 来源 | 原跨度 |
|---|---:|---|---|---|
| H001 | `[126,135)` | `DELETE_STYLE_SHELL` | 否，manual range | `因此，` |
| H002 | `[409,430)` | `REWRITE` | 否，manual range | `乘积求导法则：` |
| H004 | `[904,935)` | `REWRITE` | 否，manual range | `，接下来我们需要求出 ` |
| H005 | `[977,999)` | `REWRITE` | 否，manual range | ` 具体等于什么。` |
| H006 | `[1014,1027)` | `REWRITE` | 否，manual range | `为了看清 ` |
| H007 | `[1049,1093)` | `REWRITE` | 否，manual range | ` 的几何本质，我们引入路程微元 ` |
| H008 | `[1106,1144)` | `REWRITE` | 否，manual range | ` 进行链式展开，提取出速率 ` |
| H009 | `[1350,1376)` | `REWRITE` | 否，manual range | ` 时间内走过了弧长 ` |
| H010 | `[1389,1423)` | `REWRITE` | 否，manual range | `。对应的切向单位矢量从 ` |
| H011 | `[1435,1446)` | `REWRITE` | 否，manual range | ` 变到了 ` |
| H012 | `[1879,1910)` | `REWRITE` | 否，manual range | `，也就是法向单位矢量 ` |
| H013 | `[2240,2277)` | `REWRITE` | 否，manual range | `根据数学上对轨道曲率半径 ` |
| H014 | `[2467,2506)` | `REWRITE` | 否，manual range | `代入前面的大小公式，得到：` |
| H015 | `[2642,2661)` | `REWRITE` | 否，manual range | `我们可以写出 ` |
| H016 | `[2846,2859)` | `REWRITE` | 否，manual range | `现在，把 ` |
| H017 | `[2925,2959)` | `REWRITE` | 否，manual range | ` 代回前面的链式法则中：` |
| H018 | `[3112,3176)` | `REWRITE` | 否，manual range | ` 最后，将这个结果填入最初的加速度展开式里：` |

`M003/S003` 的范围为 `[618,675)`，原文是“这一步非常直观地把加速度分成了两部分：”。它在首次机械失败后改为 selection `KEEP`，不再形成 hunk；原因是窄规则把“非常”中的“非”计入否定 marker，改写该跨度会产生 `SPEECH_ACT_NEGATION_CHANGED`。

## 4. 首次机械失败与回退

首次 applicator 使用 18 个 hunk。结构应用和 coverage 均为 `PASS`，但统一验证器为 `REVIEW/2`，paired-quality 因此是 `BLOCKED_BY_MECHANICAL_GATE`。首次失败记录保存在 `applicator/validation.json`、`applicator/result.json`、`applicator/review.md` 和 `verifier.attempt1.json`。

首次 warning 为：

- `SPEECH_ACT_NEGATION_CHANGED`：删除含“非常”的句壳后，窄 marker 计数中的“非”减少 1。
- `SPEECH_ACT_MODALITY_SCOPE_CHANGED`：首次替换引入两个“可”，并删除一个“需要”和一个“可以”。

回退动作：

- 将 `M003/S003` 从 hunk 改为原样 `KEEP`，恢复“非”marker 计数。
- H002、H008 不再引入“可”。
- H004 逐字保留“需要”；H015 逐字保留“可以”和“写出”动作，只删除第一人称主持语。
- 成对朗读发现中间稿“由乘积求导法则：”承接残缺，H002 又局部修为“对速度矢量应用乘积求导法则：”，随后重新 finalize/build/apply/verify。

Release 版本没有 pending warning、unexplained high 或 introduced finding。

## 5. 最终状态

| 层 | 状态 | 精确含义 |
|---|---|---|
| validator hard invariant | `PASS` | 已编码的 TeX/公式/数字/术语等硬门未失败 |
| validator speech act | `PASS` | 当前已编码言语行为门无 pending warning |
| validator style signal | `PASS` | 当前 scanner 无未解释 high 或新增候选 |
| validator mechanical | `PASS/0` | 绑定当前 before/after 的机械验证通过 |
| validator delivery | `REVIEW/2` | paired-quality 仍待可信外部复核 |
| applicator structural/application | `PASS` / `PASS` | 17 个 hunk 有序、互不重叠，未列字节 `COPY_EXACT` |
| applicator coverage | `PASS` | 仅限枚举 high 与绑定 declarations 的覆盖闭合 |
| applicator paired-quality | `PENDING_EXTERNAL_REVIEW` | 本地流程不能签发质量 clearance |
| verifier record integrity | `PASS/0` | 闭集与确定性 review 工件自洽 |
| verifier coverage replay | `PASS` | coverage 同 policy 重算一致 |
| current policy | `MATCH`; replay `PASS` | 归档 policy 与当前安装 policy 一致，重放一致 |
| live source | `MATCH` | expected/observed SHA-256 均为 source SHA |
| academic correctness | `NOT_EVALUATED` | 未判断或改动物理正确性 |
| semantic judgment | `NOT_EVALUATED` | 机械门不证明完整自然语言蕴含 |

Release bundle SHA-256 为 `0a77433b50ed5b9d22452c88572b3921747b28fd9f7d946f5aa3dd1664034483`；候选 SHA-256 为 `84e909327237e0375ea7cd81409ce94fe3042cc40165435d337116f796ea6108`；paired-quality request SHA-256 为 `5c6882a21f672f789ea09d57647fa43b387b5f743d207f5dff9166f0c8c71fb5`。

## 6. 工件清单

- Authoring scaffold：`selection.authoring.json`
- 首次 selection/bundle：`selection.v2.json`、`patch.bundle.json`
- 机械回退 selection/bundle：`selection.final.v2.json`、`patch.final.bundle.json`
- Release selection/bundle：`selection.release.v2.json`、`patch.release.bundle.json`
- 首次 applicator 闭集：`applicator/`
- 机械回退 applicator 闭集：`applicator-final/`
- Release applicator 闭集：`applicator-release/`
- Release 待审候选：`applicator-release/candidate.review.tex`
- Release PATCH：`applicator-release/patch.diff`、`applicator-release/review.md`
- Release coverage：`applicator-release/coverage.json`
- Release validator：`applicator-release/validation.json`
- Release applicator result：`applicator-release/result.json`
- Verifier：`verifier.attempt1.json`、`verifier.release.json`

## 7. DELIVERY 边界

```text
DELIVERY REVIEW exit=2
candidate_assembly_status=PASS
mechanical_validation_status=PASS
paired_quality_review_status=PENDING_EXTERNAL_REVIEW
paired_quality_clearance_granted=false
humanize_quality_claim_allowed=false
completion_claim_allowed=false
```

`verifier status=PASS exit=0` 只证明 `SELF_CONSISTENCY_ONLY` 范围内的闭集、coverage/current-policy replay 与 live-source 绑定通过，不会把候选升级为正式终稿。实际交付对象仅为 `applicator-release/candidate.review.tex` 与其 PATCH/审计工件；源文件保持不变。不得据此声称文风质量完成、学术正确、作者身份成立或语义完整性已证明。
