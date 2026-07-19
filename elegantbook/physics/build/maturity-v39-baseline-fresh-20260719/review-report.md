# Short PATCH baseline review report

## 范围与配置

- source：`tests/fixtures/humanize_forward_v10/research_before.md`
- 配置：`mode=REWRITE; scene=RESEARCH; intensity=BALANCED; requested_output=PATCH; effective_output=PATCH`
- 来源：`source_kind=DOCUMENT; report_context=NONE`
- 声线：`voice_profile=NONE; voice_disclosure=SCENE_DEFAULT; corpus_action_support=NONE`
- 结构：标题与段落骨架锁定；数字、比较方向、否定、模态、因果不确定性、结果报告状态受保护。
- 边界：未读取任何既有 `build` 工件、成熟度报告或测试期望；未修改 source、Skill 或 tests。

## 结果

- AUTO source scan：3 个 high，分别为 `LEX-MARKET-01`、`LEX-EMPH-01`、`LEX-FOUNDATION-01`。
- disposition：3 个 high 全部映射到唯一 hunk；无 lexical KEEP；4 个 caller-bound selection；0 个显式 conflict pair。
- patch：3 个 `DELETE_STYLE_SHELL`，1 个原样 `UNRESOLVED`；`patch_hunks_source_partition=NON_OVERLAPPING`。
- candidate AUTO rescan：0 个 high；剩余 2 个 medium 均位于原样未决 H003。
- applicator：`DELIVERY REVIEW exit=2`；`structural_validation=PASS`；`unified_validator=PASS`；`coverage=PASS`。
- verifier：`INTEGRITY PASS exit=0 scope=SELF_CONSISTENCY_ONLY; CURRENT_POLICY_REPLAY PASS; COVERAGE PASS; DELIVERY REVIEW`。
- 边界状态：`paired_quality_review_status=PENDING_EXTERNAL_REVIEW`，`semantic_judgment=NOT_EVALUATED`，`humanize_quality_claim_allowed=false`。

## 手工填写字段

scaffold 自动生成 A001-A003 和 3 条 high inventory；以下才是实际手工编辑。手工 span 的 `start_byte` 均填 `null`，finalize 后确定性展开为括号中的 UTF-8 半开范围。

| span | 手工 source_text | finding_ids | finalize byte range |
|---|---|---|---|
| A004 | `，也具有重要意义` | `[]` | `193:217` |
| A005 | `值得注意的是，` | `[]` | `220:241` |
| A006 | `本文系统梳理了相关现象，并深入探讨了可能原因` | `[]` | `241:307` |
| A007 | `，为后续研究奠定基础` | `[]` | `307:337` |

| hunk | span | decision | replacement | 手工 reason |
|---|---|---|---|---|
| H001 | A004 | `DELETE_STYLE_SHELL` | empty | 删除与前句具体结果重复且不新增对象、动作或后果的泛化价值判断。 |
| H002 | A005 | `DELETE_STYLE_SHELL` | empty | 删除不承载独立命题的重点提示壳，后续作者动作主张另行保留为未决。 |
| H003 | A006 | `UNRESOLVED` | 逐字等于 source | 当前来源未给出足以核对“系统梳理/深入探讨”完成状态的对应材料，纯文风层不裁决，逐字保留。 |
| H004 | A007 | `DELETE_STYLE_SHELL` | empty | 删除未提供具体对象、动作或待回答问题的自动后续研究桥接出口。 |

| selection | span / hunk | decision | 手工 reason |
|---|---|---|---|
| S001 | A004 / H001 | `HUNK` | 把泛化价值尾语绑定为本次最小 PATCH 的删除选区。 |
| S002 | A005 / H002 | `HUNK` | 把空重点提示壳绑定为本次最小 PATCH 的删除选区。 |
| S003 | A006 / H003 | `HUNK` | 把语义完成状态不足以裁决的作者动作主张绑定为原样未决选区。 |
| S004 | A007 / H004 | `HUNK` | 把无具体内容的后续研究桥接出口绑定为本次最小 PATCH 的删除选区。 |

另外手工把 3 条 `lexical_resolutions[].decision/hunk_id` 从 `PENDING/null` 分别改为 `HUNK/H001`、`HUNK/H002`、`HUNK/H004`；合同要求其 `reason` 保持 `null`。`explicit_conflicts` 没有手工条目，保持空数组，因为 source 中未发现可由纯文风层登记为正反许可或互斥结论的真实 conflict pair。上述 selection 是本次 caller-bound 声明，不证明外部用户逐字选区或质量授权。

## 命令与状态

下列 `$SKILL`、`$SOURCE`、`$OUT` 分别代表 Skill 根、给定 source 和本工件目录的绝对路径。并行读取命令逐项均返回所列状态。

| # | 命令/操作 | 状态 |
|---:|---|---|
| 1 | `Get-Content -Raw $SKILL/SKILL.md` | exit 0；终端默认编码造成 mojibake，且输出截断，不据此执行。 |
| 2 | `Get-Content -Encoding utf8 $SKILL/SKILL.md \| Select-Object -First 140/-Skip 140` | 均 exit 0；聚合输出仍截断。 |
| 3 | `Get-Content -Raw -Encoding utf8 $SKILL/references/short-patch-workflow.md` | exit 0；完整读取。 |
| 4 | `Get-Content -Encoding utf8 $SKILL/SKILL.md \| Select-Object -Skip 140/180/220/260 -First 40/40/40/80` | 均 exit 0。 |
| 5 | `(Get-Content -Encoding utf8 $SKILL/SKILL.md).Count` | exit 0；449 行。 |
| 6 | `Get-Content -Encoding utf8 $SKILL/SKILL.md \| Select-Object -Skip 340/395 -First 55/60` | 均 exit 0；主文件读取至 EOF。 |
| 7 | `Get-Content -Raw -Encoding utf8 $SOURCE` | exit 0。 |
| 8 | `rg -n '^#{1,4} ' operational-contract.md workflow.md quick-checklist.md style-gates.md research-journal.md` | exit 0；用于只路由相关章节。 |
| 9 | `Get-Content` 读取 operational 4.3/5.2/6.2/7.3、workflow 1/3/5/6/7、quick checklist、REWRITE/RESEARCH gates、research journal | 均 exit 0；一次聚合输出截断后对 workflow/quick/gates 重新分段读取，均 exit 0。 |
| 10 | `Test-Path -LiteralPath $OUT` | exit 0；`False`。 |
| 11 | `python $SKILL/scripts/scan_humanize_chinese.py $SOURCE --scene AUTO --format text` | exit 0；3 high + 2 medium。 |
| 12 | `python scaffold/build/apply/verify_humanize_short_patch.py --help` | 四项均 exit 0。 |
| 13 | `python scaffold_humanize_short_patch.py create/finalize --help` | 两项均 exit 0。 |
| 14 | `New-Item -ItemType Directory -Path $OUT` | exit 0。 |
| 15 | `python scaffold_humanize_short_patch.py create $SOURCE --requested-output PATCH --scene RESEARCH --intensity BALANCED --source-kind DOCUMENT --output $OUT/selection.authoring.json --format text` | exit 0；`PENDING high=3 resolutions=3`。 |
| 16 | `Get-Content -Raw -Encoding utf8 $OUT/selection.authoring.json` | exit 0。 |
| 17 | `rg -n -C 5 'selected_spans\|explicit_conflicts\|lexical_resolutions\|span_id\|hunk_id' scaffold_humanize_short_patch.py` | exit 0；核对 authoring 字段闭集。 |
| 18 | `apply_patch` 编辑 `selection.authoring.json` | 工具返回成功；随后 JSON 解析证明写入有效。 |
| 19 | `Get-Content ... \| ConvertFrom-Json` 统计 authoring | exit 0；`spans=7 hunks=4 selections=4 pending=0 conflicts=0`。 |
| 20 | `python scaffold_humanize_short_patch.py finalize $SOURCE --authoring $OUT/selection.authoring.json --output $OUT/selection.v2.json --format text` | exit 0；`FINALIZED hunks=4 selected=4`。 |
| 21 | 首次通过 orchestration 读取 `selection.v2.json` | JS `SyntaxError`，shell 未启动、文件未变；改用相对路径重试。 |
| 22 | `Get-Content -Raw -Encoding utf8 $OUT/selection.v2.json` | exit 0；核对 byte offset 与展开字段。 |
| 23 | `python build_humanize_short_patch.py $SOURCE --selection-spec $OUT/selection.v2.json --output $OUT/patch.bundle.json --format text` | exit 0；`BUNDLED hunks=4`。 |
| 24 | `python apply_humanize_short_patch.py $SOURCE --bundle $OUT/patch.bundle.json --output $OUT/short-patch-review --format text` | 合同状态 `REVIEW/2`，闭集已发布；外层执行封装把预期非零码显示为 script failure。 |
| 25 | `Get-ChildItem -LiteralPath $OUT/short-patch-review -File` | exit 0；闭集 9 个文件。 |
| 26 | `python verify_humanize_short_patch.py $OUT/short-patch-review --live-source $SOURCE --format text` | exit 0；integrity/current-policy/coverage PASS，delivery 仍 REVIEW。 |
| 27 | `Get-Content` 读取新生成的 candidate/review/diff/result | 均 exit 0。 |
| 28 | `python scan_humanize_chinese.py $OUT/short-patch-review/candidate.review.md --scene AUTO --format text` | exit 0；0 high，2 medium unresolved。 |
| 29 | `(Get-FileHash -Algorithm SHA256 $SOURCE).Hash` | exit 0；`348026b7b26c646e67e809285ea11881865a3d35193a4131ff850813582c4d71`，与 bundle source hash 相同。 |
| 30 | `git diff -- tests/fixtures/humanize_forward_v10/research_before.md` | exit 0；无输出。 |
| 31 | `git status --short -- $SOURCE $OUT`（仓库相对路径） | exit 0；仅 `$OUT` 为未跟踪。 |
| 32 | `apply_patch` 新建本 `review-report.md` | 成功；报告置于闭集目录外，未改写 evidence manifest。 |
| 33 | `Get-Content`/`Get-Item`/`rg` 检查本报告 | exit 0；写入后为 95 行、9247 bytes，5 个必需二级标题齐全。 |
| 34 | `Get-ChildItem -LiteralPath $OUT -Recurse -File` | exit 0；共 13 个文件，全部位于指定新目录。 |
| 35 | 再次运行 `verify_humanize_short_patch.py ... --live-source $SOURCE --format text` | exit 0；integrity/current-policy/coverage 仍 PASS，delivery 仍 REVIEW。 |
| 36 | 再次运行限定路径的 `git status --short` | exit 0；仍只有 `$OUT` 为未跟踪。 |
| 37 | `apply_patch` 追加本轮自检记录 | 成功；未改写 `short-patch-review/` 闭集。 |

## 实际摩擦

1. PowerShell 首次读取 Skill 时默认编码显示乱码；显式 `-Encoding utf8` 后解决。
2. 多文件/大文件聚合输出触发工具截断，需要按行范围重读；这增加了路由与完整读取成本。
3. authoring scaffold 的 high span 不可加宽。为删除连同标点的自然句壳，必须保留 A001-A003，再新增 A004-A007，并分别维护 hunk、lexical resolution 和 selection 引用。
4. `UNRESOLVED` 不出现在普通 diff 中，必须同时查看 `review.md`/bundle；本次 H003 正是这种情况。
5. applicator 的合法候选固定返回 `REVIEW/2`，外层工具把非零码渲染成 script failure，容易与真正 `FAIL/1` 混淆；权威首行、已发布闭集和 verifier PASS 共同确认这是预期待审状态。
6. coverage PASS 只覆盖枚举 high 与绑定声明。词库外病灶、未声明语义冲突、文风收益、学术正确性和外部 paired-quality 不在其证明范围内。
