# v37 root review: enumerated short-PATCH coverage

## 裁决

v37 工程验收通过。它把 v36 的“列出的 hunk 可重放”扩展为“当前 scanner 的全部 AUTO high finding、
调用方绑定 selection 和调用方显式 conflict pair 均有且只有一个可复核 disposition”。该结论只在
`ENUMERATED_HIGH_AND_BOUND_DECLARATIONS_ONLY` 范围内成立。

本轮不授予文风质量、语义完整性、学术正确性、作者身份或生成资格 PASS。最终 candidate 仍为
`REVIEW/2`，生成资格仍为 `NOT_EVALUATED`，投影证据能力上限仍为 `E2`。

## 1. v36 没有证明什么

v36 verifier 已能核对闭集、当前 validator policy、完整 validation JSON 与可选 live source，但 coverage
universe 仍由调用方的 hunk 列表定义。攻击者可以只列一个安全 hunk，完全不登记同一 source 中其他
high signal 或用户要求保留的 span，然后得到“列出的内容自洽”。因此 current-policy replay PASS 不能
回答以下问题：

1. scanner 可确定的 high finding 是否全部有处置；
2. 调用方声称要处理或保留的 selection 是否真的与 hunk 精确绑定；
3. 调用方声明的冲突两侧是否都由不同 UNRESOLVED hunk 原样承载；
4. PROTECTED、EXCLUDED 或 KEEP span 是否被另一个大 hunk 暗中覆盖。

## 2. 新合同

新增或升级三个 schema：

```text
humanize-short-patch-selection/v2
humanize-short-patch/v2
humanize-short-patch-coverage/v2
```

coverage 固定使用 `scan_scene=AUTO` 建立 high audit view，另行披露任务 scene。它覆盖三类冻结对象：

- scanner 当前 policy 下全部 high finding；
- 调用方精确绑定的 selected spans；
- 调用方明确声明的 conflict pairs。

每个 lexical high 只能落到 `HUNK/KEEP/PROTECTED/EXCLUDED`；每个 selection 只能是精确 `HUNK` 或
不与任何 hunk 重叠的 `KEEP`；每个 conflict pair 必须引用两个不同、未复用、原样复制的
`UNRESOLVED` hunk。REPORT_SELECTION 仍不能自填，必须由 detector extractor/report-scope 管线建立
外部 selection 绑定。

## 3. 红队发现与修复

两名独立红队分别攻击 coverage 计算和 evidence/verifier 状态面，去重后确认九类缺口：

| 缺口 | 旧错误完成路径 | v37 处置 |
|---|---|---|
| selection KEEP 与 hunk 重叠 | coverage 写 KEEP，candidate 实际改写同一 span | 构建期拒绝任意 overlap |
| PROTECTED/EXCLUDED 与 hunk 重叠 | finding 被登记为保护/排除，整块仍被改写 | 两类 finding span 均不得与 hunk 相交 |
| policy key-set drift | 新增合法 policy component 被误报为 record corruption | key-set 变化进入 `REVIEW/2 DRIFT` |
| partial protected match | 只检查 match 起点，跨出引语的 finding 仍算 PROTECTED | 只有完整 finding span 位于保护区才标保护 |
| task scene 漏扫 | GENERAL 可漏掉 COURSE high | coverage scanner 固定 AUTO，任务 scene 单独披露 |
| result 伪声明/路径注入 | 重封 manifest 后可塞入 PASS、绝对路径或重复 artifact | result 严格闭集、枚举、相对路径和唯一 artifact 校验 |
| malformed record + drift | 畸形 nested inventory 被 policy drift 提前遮蔽 | 先做完整结构/值域完整性，再裁决 drift |
| builder stdout 错 schema | v2 文件写成后控制台仍报 v1 | stdout 动态回显真实 bundle/coverage schema |
| `.ltx` 格式分裂 | scanner 按 TeX，candidate/validator 按 TXT/Markdown | `.ltx` 发布为 `candidate.review.tex` 并按 TeX 验证 |

对应 RED/GREEN 主要位于
`tests/test_humanize_short_patch.py`：KEEP overlap、protected/excluded overlap、AUTO scene、policy key-set
drift、legacy v1、malformed nested inventory、scope broadening、result 注入、`.ltx` 路由和 v2 CLI schema
均有单独测试。`tests/test_humanize_lexical_scan.py` 覆盖完整 span 保护判定，投影测试覆盖新脚本进入
generator 闭集。

## 4. 记录完整性与 policy replay

`coverage.json` 进入八项 evidence 闭集。verifier 先做 strict JSON、字段闭集、artifact 唯一性、hash/size、
bundle application、diff 和 result 绑定，再处理 coverage：

1. 旧 `coverage/v1` 只读兼容，但与当前 v2 policy 不同固定 REVIEW；
2. 记录内部结构、枚举、summary、declaration hash 或 coverage hash 损坏固定 FAIL/1；
3. policy 值或 key-set 漂移固定 REVIEW/2，不伪装成 corruption；
4. 同 policy 时重跑 scanner、selection/conflict inventory 和 coverage canonical JSON；
5. 同 policy 重算不一致固定 FAIL/1；
6. current validator replay 与 coverage replay 分开报告，任一不能覆盖 candidate delivery 状态；
7. `--live-source` MATCH 只证明本次同主机读到相同 SHA，不证明历史真实性。

result 与 verifier 均显式携带：

```text
coverage_claim_scope=ENUMERATED_HIGH_AND_BOUND_DECLARATIONS_ONLY
coverage_scene=<task scene>
coverage_scan_scene=AUTO
coverage_source_kind=<DOCUMENT|INLINE_TEXT|INLINE_SELECTION|REPORT_SELECTION>
semantic_completeness_claim_allowed=false
humanize_quality_claim_allowed=false
academic_correctness=NOT_EVALUATED
```

这避免调用方只摘取 `coverage_completion_claim_allowed=true`，丢掉其窄作用域。

## 5. 保持的设计边界

下列行为不是遗漏，而是有意保持：

- conflict pair 的语义真实性由调用方声明；工具只证明声明的两侧绑定，不发现全部自然语言冲突；
- selection 的用户请求真实性没有外部 request anchor，工具只证明本地声明与 source bytes 一致；
- hunk 与 selected span 重复 source text 是两个独立绑定，暂不以引用简写换取较弱的手工可读性；
- 普通 diff 只显示变化，未变化的 UNRESOLVED 必须在 bundle/coverage 中审阅；
- 删除课程记忆命令若改变模态，统一 validator 仍可保守 REVIEW；不能因场景规则许可就静默豁免；
- `coverage_completion_claim_allowed` 不升级 `completion_claim_allowed` 或
  `humanize_quality_claim_allowed`。

## 6. Fresh forward

全新代理在禁止读取旧 v37 工件的条件下处理真实课程 TeX。第一轮整句删除“必须牢记公式”，触发
`SPEECH_ACT_MODALITY_SCOPE_CHANGED`，合法停在 REVIEW。第二轮改为“必须判断公式能否直接套用”，
保留原模态与输入已有对象，机械层通过；两条相对主张仍逐字 UNRESOLVED。

最终证据：

```text
build=BUNDLED/0
bundle=humanize-short-patch/v2
coverage=humanize-short-patch-coverage/v2 PASS
AUTO high=4
selected spans=5
explicit conflicts=1
hunks=4 (REWRITE 1, DELETE_STYLE_SHELL 1, UNRESOLVED 2)
apply=DELIVERY REVIEW/2
mechanical/hard/style/speech-act=PASS/PASS/PASS/PASS
paired_quality=PENDING_EXTERNAL_REVIEW
verify=PASS/0
coverage replay=PASS
current-policy replay=PASS
live source=MATCH
candidate AUTO rescan=0 findings
```

完整 forward 记录见同级目录
`../maturity-v37-final-forward-20260719/review-report.md`。

## 7. 测试与投影

当前最终安装字节的验证结果：

```text
focused short PATCH + lexical scan + projection: 112 tests OK, skipped=2
full suite: 768 tests OK, skipped=4
quick_validate(source/final projection/repro projection): PASS/PASS/PASS
SKILL.md: 449 lines
policy/builder=1.10.8/1.10.8
projection files=36/36
BYTE_DIFFS=0
capability_source=08c6f3ced51426bbcbd1eaf6e48d5f525336a5247c6047114896327ae793a57e
projection_tree=00eea41ec71ed8b8525d843eb5ff69343b5db8aa4c6bf84f87b7c2220abfdb6b
manifest_file_sha256=366c3444ac58cf6fb41501d372cdc752ffec8bbe8457d2b96eaf77393821a76d
projected_private_control_hits=0/36 text files
evidence_cap=E2
```

双投影目录：

- `build/generator-projection-maturity-v37-final-20260719/`
- `build/generator-projection-maturity-v37-final-repro-20260719/`

两份 manifest 逐字节一致。projection builder 的 forbidden-reference、secret-control、Python compile/import
closure、reference closure、case-fold collision、reparse point 和 quick validation 审计全部 PASS。

## 8. 最终成熟度判断

v37 关闭了 v36 明确登记的 coverage P0：现在不能仅靠一份自洽但不完整的 hunk 列表声称已处置
scanner 的全部 high，也不能把 KEEP/PROTECTED/EXCLUDED 或 conflict span 埋进另一个改写块。

它仍是“生产级待审工具链”，不是自动终稿器。最值得继续成熟化的方向是降低 v2 selection 的手工重复
和审阅成本，同时保持两个独立绑定与 fail-closed 语义；其次是为外部 selection/request 建立不可由本地
调用方伪造的锚。两者都不能通过放宽 coverage 或把本地自述当可信请求来实现。

