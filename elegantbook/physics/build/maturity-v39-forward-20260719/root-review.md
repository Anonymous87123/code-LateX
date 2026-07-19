# v39 root review: source-bound span suggestions and adversarial closure

## 裁决

v39 的确定性工具链验收通过。它把 v38 留下的“实际改写仍需手工登记更宽 span”改造成
source-bound 建议面，并在真实科研短文上把最终 hunk 的手工 span 数从 2 降为 0。最终默认值为：

```text
span_suggestion_mode=CLAUSE_AND_SENTENCE
paragraph suggestion=EXPLICIT_ONLY
authoring_integrity_scope=CALLER_CONTROLLED_SELF_CONSISTENCY_ONLY
```

该结论只表示 authoring、coverage、应用与闭集重放的确定性合同通过。最终 fresh candidate 仍为
`DELIVERY REVIEW/2`，paired-quality 仍为 `PENDING_EXTERNAL_REVIEW`，学术正确性、语义完整性、
用户授权与文风质量均未由本地工具证明。生成资格继续为 `NOT_EVALUATED`，证据上限继续为 `E2`。

## 1. v39 实际改进

### 1.1 Authoring v2 建议面

`humanize-short-patch-selection-authoring/v2` 在 v38 registry 上增加：

- `span_suggestion_policy` 与 source-bound `span_suggestions`；
- `NONE/CLAUSE/CLAUSE_AND_SENTENCE/SENTENCE/PARAGRAPH/SENTENCE_AND_PARAGRAPH/ALL`；
- clause core、左分隔符附着、右分隔符附着三类边界；
- 同一边界内多个 high 共用一个 suggestion；
- 保护重叠、TeX 控制序列、超长范围与 finding 跨边界时的确定性 SUPPRESSED 记录；
- create/finalize 对建议 inventory、authoring tool hash、source 和当前 policy 的重算。

建议只提供可引用 byte span，不填写 hunk、replacement、reason、selection、conflict 或授权。调用方仍须
逐项决定 `HUNK/KEEP`，并由正式 builder、coverage、validator 和 verifier 重验。默认同时给 clause 与
完整句，是因为前者适合删除局部句壳，后者适合保留谓词和模态的整句重写；段级范围过宽，继续只在
显式请求时生成。

### 1.2 authoring 鲁棒性修复

本轮早期红队确认并关闭了七类既有问题：

1. 不再把同一调用方可重封的 JSON 写成“不可篡改”；固定披露
   `CALLER_CONTROLLED_SELF_CONSISTENCY_ONLY`。
2. create 在落盘前执行与 finalize 相同的 `MAX_JSON_BYTES` 门，不能生成自己读不回的 scaffold。
3. 非 `UNRESOLVED` hunk 与普通保护跨度重叠时在 finalize 早拒绝，不拖到 apply。
4. `.txt` 可由 create/finalize/build 显式统一指定 `--document-format TEX`。
5. reason 先剥离中英文句末标点，再拒绝 `TODO。/保持原样。` 等空泛变体。
6. conflict rule 收口到固定枚举，selection/conflict ID 按 casefold 防碰撞且引用大小写精确。
7. 零 high 的 create 返回 `NO_HIGH_FINDINGS/0`；空 scaffold finalize 返回 `NO_PATCH_HUNKS`，不再用
   PENDING 或 spans 结构错误混淆调用方。

这些门没有把 authoring scaffold 升级成 evidence，也没有证明 reason、KEEP 或 conflict 判断真实。

## 2. 默认组合模式的 RED/GREEN

最初两项 RED 分别从 Python API 和 CLI 调用 create，要求默认同时给 clause 与完整句。两项均实际执行，
且只因 `expected=CLAUSE_AND_SENTENCE; actual=CLAUSE` 失败。最小 GREEN 增加组合枚举、同步 API/CLI 默认
值和文档；显式 `CLAUSE/SENTENCE/PARAGRAPH/ALL/NONE` 保持兼容。

初版 GREEN 后，独立红队没有停在“测试已过”，而是用最小文本继续攻击建议合同，得到五类有效缺口：

| 缺口 | 最小反例 | 修复 |
|---|---|---|
| suggestion 未完整覆盖所绑定 finding | `形成证据；分析闭环。` | 任一 AVAILABLE 必须包住 finding 全跨度；跨边界视图固定 `FINDING_NOT_FULLY_COVERED` |
| TeX 命令参数内 clause 可编辑 | `\textbf{标签，值得注意的是，结论}。` | 控制序列、嵌套 `[]/{}` 参数在 Markdown/TeX 中进入完整命令保护 |
| 完全相同 range 跨 kind 重复计数 | `值得注意的是；` | AVAILABLE 按 byte range 去重并保留最局部视图；SUPPRESSED 仍分视图审计 |
| 同一位置选用多个重叠边界 | clause KEEP + full-sentence KEEP | authoring finalize 固定 `SELECTED_SPANS_OVERLAP` |
| CLI/API AUTO 不一致 | API `document_format="AUTO"` | create/finalize/build 的 `AUTO/auto` 均按后缀推断 |

复攻上述五项后全部为 FIXED，但红队又发现 TeX 注释续接：

```tex
\textbf% keep
{标签，值得注意的是，结论}。
```

TeX 中未转义 `%` 会吞掉换行，下一行参数仍属于同一命令。修复前建议器给出 AVAILABLE，手工 hunk 也能
通过 finalize；新增两项 RED 分别覆盖建议与手工 hunk。修复后 parser 跳过控制序列后的 TeX 注释与空白，
把参数纳入同一保护 span；两项转为 GREEN。Markdown 不启用 `%` 注释语义，但仍保护显式 TeX 命令调用。

## 3. Fresh 用户路径

### 3.1 无效或过时记录不计通过

- `maturity-v39-r5-fresh-user-20260719` 在最后一轮红队修复前完成，只能作为中间行为记录；
- `maturity-v39-r9-fresh-user-20260719` 因外部 HTTP 400 失败，没有形成可采信 forward 证据；
- 只有最终安装字节上的 `maturity-v39-r10-fresh-user-20260719` 计入本节。

### 3.2 最终 fresh 结果

完全 fresh 的代理只得到当前 Skill 和
`tests/fixtures/humanize_forward_v10/research_before.md`，禁止读取其他 build、测试代码、成熟度报告和
既有期望。它先按 UTF-8 重读乱码终端输出，再完成当前 authoring/build/apply/verify 工作流。

authoring 与最终 hunk 统计为：

```text
mode=CLAUSE_AND_SENTENCE
AUTO candidate high=3
AVAILABLE suggestions=8
SUPPRESSED suggestions=0
registry spans=9
final hunks=2
hunks using suggested spans=2
manual hunk spans=0
```

H001 删除 `，也具有重要意义`；H002 把完整句压缩为“本文梳理了相关现象，并讨论了可能原因。”。
首轮曾把含“可能原因”的整句作为样式壳删除，统一验证器以
`SPEECH_ACT_MODALITY_SCOPE_CHANGED` 保持机械 REVIEW。代理没有豁免或粉饰，而是在 r2 保留“可能”模态
后重建闭集。最终独立重放为：

```text
mechanical/hard/speech-act/style=PASS/PASS/PASS/PASS
coverage=PASS scope=ENUMERATED_HIGH_AND_BOUND_DECLARATIONS_ONLY
current-policy replay=PASS
live source=MATCH
verifier=PASS/0 scope=SELF_CONSISTENCY_ONLY
delivery=REVIEW/2
paired-quality=PENDING_EXTERNAL_REVIEW
academic_correctness=NOT_EVALUATED
```

applicator 的外层命令包装显示 `Script error: Exit code: 1`，而 applicator 文本与归档 result 均声明
`DELIVERY REVIEW exit=2`。本轮没有把包装层显示改写成“已观察 OS exit=2”；只以闭集 result/validation
和独立 verifier 重放说明归档自洽。完整过程见
[operation-report.md](../maturity-v39-r10-fresh-user-20260719/operation-report.md)。

## 4. 最终机器证据

最终安装字节上重新执行：

```text
authoring/suggestion focused=38 total; 38 passed
full suite=812 total; 808 passed, 4 skipped
authoring scaffold executable lines=1008
authoring scaffold executed/missed=904/104
authoring scaffold line coverage=89.68%
quick_validate source/final/repro=PASS/PASS/PASS
SKILL.md=451 lines
policy/builder=1.10.10/1.10.10
projection files=37/37
BYTE_DIFFS=0
capability_source=c1b7af4cb214107a7241b7a7aed157de24868d432f23a6a9dff3a79a39e33f7a
projection_tree=14cc3e25d3bf2c4a7290961b07792f0e674afb2084173b4f19f2944f4e4cce4a
manifest_file_sha256=e38cbc680d61ed226123490a09d5070151ffcd5bc1d70c9702f792b784e619f3
private-control path/content hits=0/0 in each 37-file projection
evidence_cap=E2
```

两份 projection 逐相对路径和 SHA-256 比较为零差异；manifest 文件字节哈希相同。一次较早的全量运行
在 capability 文件已变化但固定 policy 尚未同步时产生 64 个同源 projection fail-closed error；该运行
不计最终通过。稳定 policy 后的最终 812 项结果才是发布证据。

最终投影：

- [primary](../generator-projection-maturity-v39-final-r10-20260719/)
- [primary manifest](../generator-projection-maturity-v39-final-r10-20260719.manifest.json)
- [repro](../generator-projection-maturity-v39-final-r10-repro-20260719/)
- [repro manifest](../generator-projection-maturity-v39-final-r10-repro-20260719.manifest.json)
- [trace](../maturity-v39-trace-final-r10-20260719/)

## 5. 当前边界

v39 证明的是建议边界、引用、保护和闭集状态可以确定性复核，并在一个真实科研短文上消除了手工 hunk
span。它仍不证明：

- scanner 或 suggestion 发现了所有 AI 味与语义冲突；
- suppression、KEEP、reason、conflict 或改写收益判断正确；
- authoring 文件来自不可伪造的用户授权；
- verifier PASS 等于候选质量 PASS；
- 文本的事实、引文、因果、计算或学术结论正确；
- 当前本地 runner 达到 E3，或 188 项生成资格原子已执行通过。

因此本轮可以称为“生产候选工具链更成熟”，不能称为“无人值守 Humanizer 已完成”或“已完全去除 AI
味”。后续最有价值的方向是把建议使用率、手工 span 回退率、SUPPRESSED 原因和外部 paired-quality
结果做成跨场景基准，而不是继续扩大本地 PASS 的文字范围。
