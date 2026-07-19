# v40 root review: cross-scene manual-span gap, candidate-flood rejection, and FOCUS

## 裁决

v40 关闭的是一个由真实使用暴露的 authoring 成本缺口：当 scanner 没有 high finding，fresh 使用者仍能在
连续阅读中定位出值得处理的局部病灶，但 v39 的 source-bound 建议面无法登记这些位置。COURSE、MODELING、
GENERAL 三场景共形成 36 个手工 hunk span；原 fresh 运行中，36 个都要手工录入 UTF-8 byte range。

本轮没有把“全篇所有可编辑文字都做成候选”投入生产。该原型在三个 fixture 上产生 554 个 AVAILABLE
建议，却只与 36 个最终 hunk 中的 4 个精确同界，候选洪水与真实编辑面的比例不成立。最终生产方案是
authoring v3 的 `FOCUS`：调用方先完成连续阅读和诊断，只把已经定位的精确原文片段交给确定性工具登记、
消歧、保护和冻结。三场景回放为 36/36 精确命中，且 suggestion 中没有 replacement、decision、reason、
selection、conflict 或授权字段。

该裁决只证明：调用方已定位的 span 可以低成本、可重放地进入短 PATCH 工具链。它不证明 FOCUS 能发现
病灶，也不证明调用方诊断、replacement、KEEP、UNRESOLVED 或文风收益正确。三份最终候选均保持
`DELIVERY REVIEW/2`；paired-quality 仍为 `PENDING_EXTERNAL_REVIEW`，学术正确性和完整语义判断仍为
`NOT_EVALUATED`。生成资格继续为 `NOT_EVALUATED`，本地证据上限继续为 `E2`。

## 1. 证据范围与隔离

### 1.1 三个压力输入

本轮补测 v39 fresh RESEARCH 之外的三个场景。fixture 都是 GPT 生成或来源未解决文本，只作负向/压力输入，
不作真人范文、PERSONAL Voice、事实来源或可复制句库：

| Fixture | Scene | 来源行范围 | 字节角色 |
|---|---|---|---|
| `fixtures/course.tex` | `COURSE` | `physics1.tex` 84-116 | GPT/来源未解决压力材料 |
| `fixtures/modeling.tex` | `MODELING` | 用户提供 `main.tex` 28-48 | GPT/来源未解决压力材料 |
| `fixtures/general.md` | `GENERAL` | 指定项目分析 MD 1156-1175 | GPT/来源未解决压力材料 |

精确来源台账见 [source-manifest.md](fixtures/source-manifest.md)。本轮未读取、未使用 `CET6.tex`。三个 fresh
代理只读取各自 fixture、当前 Skill 和本次 run 工件，禁止读取 tests、旧 build、成熟度报告和其他场景
候选；源 fixture 均未修改。乱码按 UTF-8 重试规则处理，三份源均严格 UTF-8 读取成功。

### 1.2 权威运行记录

- [COURSE operation report](runs/course/operation-report.md)
- [MODELING operation report](runs/modeling/operation-report.md)
- [GENERAL operation report](runs/general/operation-report.md)

每份报告都给出 source SHA、精确 hunk byte range、manual provenance、首次机械失败、回退版本、最终
applicator/verifier 状态和 live-source 绑定。最终 verifier 均为 `PASS/0 SELF_CONSISTENCY_ONLY`，并且
current-policy replay 为 `PASS`、live source 为 `MATCH`；这些状态没有被写成质量 clearance。

## 2. 三场景盲测原始结果

### 2.1 Scanner 与 hunk 统计

| 场景 | candidate high | 其他候选 | 原 fresh AVAILABLE 建议 | 最终 hunk | 手工 hunk span | 未决 hunk |
|---|---:|---:|---:|---:|---:|---:|
| COURSE | 0 | 0 | 0 | 17 | 17 | 0 |
| MODELING | 0 | 1 medium | 0 | 9 | 9 | 1 |
| GENERAL | 0，另有 1 protected high | 5 low | 0 | 10 | 10 | 0 |
| 合计 | 0 candidate high | 1 medium + 5 low + 1 protected high | 0 | 36 | 36 | 1 |

GENERAL 的 high 是 blockquote 保护区中的“收口”，按 `PROTECTED/markdown-quote` 处置，未进入可变 hunk。
MODELING 的 H008 保持 `UNRESOLVED`：源文没有展示所称表格，纯文风层不能把一句可能的编辑计划改写成
已存在表格的读者功能说明。

这组数据说明 v39 的默认建议面在“scanner high 已知”的路径上有效，但不能覆盖连续阅读发现的词库外
搭配、主持语、后台说明、层级句法和局部读感问题。把 `candidate high=0` 解释成 `NO_CHANGE` 会漏掉
36 个 fresh 使用者实际提交的局部编辑跨度；反过来，把整个可编辑正文都列为候选又会产生洪水。

### 2.2 三种不同的机械回退

三场景都没有在首次候选后伪造完成态：

1. COURSE 初版删除“这一步非常直观……”时，旧否定 marker 把“非常”中的单字“非”算作句子否定，
   触发 `SPEECH_ACT_NEGATION_CHANGED`；同轮另有模态 marker 变化。代理先 KEEP 该 span，再局部修正
   “可/需要/可以”等变化，直到机械层通过。
2. MODELING 初版删去两处真实“不”后触发否定变化；第一次回退又新增“只”，触发模态范围变化；
   第二次回退改为“不单……还要……”，保留原有否定和模态后才通过。
3. GENERAL 初版把五个加粗结论改成新的加粗句，产生 4 个新增
   `LEX-FORMAT-BOLD-01/low`。第二版去掉加粗后又留下句间空格，成对朗读发现后建立第三套闭集工件。

这些失败都保留在各 run 的早期 applicator/selection/bundle 中。最终通过不是覆盖或重封旧记录，而是
产生新 scaffold、selection、bundle 和闭集后重新验证。

## 3. 共同缺口与被否决方案

### 3.1 非 high advisory 只解决了一小部分

v40 先让默认 `CLAUSE_AND_SENTENCE` 对 scanner 的 medium/low candidate 也提出 advisory 边界，但所有
advisory 固定 `finding_ids=[]`，不能进入 high finding coverage。postfix 默认探针结果为：

| 场景 | advisory AVAILABLE | advisory SUPPRESSED | 与最终 hunk 精确同界 |
|---|---:|---:|---:|
| COURSE | 0 | 0 | 0/17 |
| MODELING | 3 | 0 | 1/9 |
| GENERAL | 0 | 12 | 0/10 |

MODELING 的 3 个边界来自 1 个 medium 表格功能信号；GENERAL 的 12 个 low 加粗视图因保护重叠或 finding
未被完整包住而全部 SUPPRESSED。advisory 增加了可见性，但只精确覆盖 36 个最终 hunk 中的 1 个，不能
替代连续阅读。

### 3.2 `EDITABLE_RUNS` 候选洪水实验

为验证是否应自动枚举全部可编辑中文 run，本轮曾实现临时 `EDITABLE_RUNS` 原型，并在同一冻结 source
上重放。结果如下：

| 场景 | AVAILABLE 候选 | 与最终 hunk 精确同界 | hunk 覆盖率 | 候选精确命中率 |
|---|---:|---:|---:|---:|
| COURSE | 132 | 2/17 | 11.76% | 1.52% |
| MODELING | 259 | 1/9 | 11.11% | 0.39% |
| GENERAL | 163 | 1/10 | 10.00% | 0.61% |
| 合计 | 554 | 4/36 | 11.11% | 0.72% |

这里的“精确命中”只比较 UTF-8 `[start_byte,end_byte)` 是否与 fresh 最终 hunk 完全相同，不评价改写质量。
即便采用更宽松的重叠指标，调用方仍要从数百个无诊断候选中重新判断边界，失去了 source-bound 建议面
降低录入成本的意义。该方案还会诱导模型把“可编辑”误读成“应编辑”，扩大过度改写风险。

因此 `EDITABLE_RUNS` 已从生产代码删除，只保留
`postfix-probe/*-editable.authoring.json` 作为被否决实验。当前 CLI/API 不暴露该模式。

## 4. 生产方案：authoring v3 FOCUS

### 4.1 最小输入合同

FOCUS spec 固定为 strict JSON：

```json
{
  "schema_version": "humanize-short-patch-focus/v1",
  "spans": [
    {"focus_id": "F001", "source_text": "为了看清 ", "start_byte": null}
  ]
}
```

调用方式：

```powershell
python scripts/scaffold_humanize_short_patch.py create source.tex `
  --scene COURSE --source-kind DOCUMENT `
  --suggest-spans FOCUS --focus-spec focus.json `
  --output selection.authoring.json
```

`source_text` 在 source 中唯一出现时允许 `start_byte=null`；重复文本必须提供 UTF-8 byte offset 消歧。
工具重新读取 source，验证 byte boundary、原文字节、focus ID、字段闭集与 source hash。找不到、重复而未
消歧、offset 不命中或 create 后 source 漂移都不能静默改绑。

### 4.2 权限边界

FOCUS 做四件事：登记调用方已经诊断的精确片段、生成稳定 span ID、执行保护重叠检查、把 authoring
inventory 绑定到当前 source/policy。它不做下列事情：

- 不扫描或发现新病灶；
- 不判断该片段是否需要改；
- 不生成 replacement、reason、decision、selection、conflict 或用户授权；
- 不把 focus 项计入 scanner high coverage；
- 不让 authoring scaffold 获得不可伪造的外部身份。

因此 FOCUS suggestion 固定 `finding_ids=[]`，带 `CALLER_DIAGNOSIS_REQUIRED`；与公式、引语、代码、
TeX 控制序列或其他保护 span 重叠时只生成 SUPPRESSED，不发放可引用 span。专门回归测试覆盖 `$x$`
保护抑制和重复“这里”在缺 start_byte 时拒绝。

### 4.3 兼容策略

当前生产 authoring schema 为 `humanize-short-patch-selection-authoring/v3`。v1/v2 仍可只读 finalize 为
严格 v2 selection，已有合法归档不因升级失效；新 create 固定输出 v3。兼容只表示旧结构仍能重放，
不把旧记录补写成 FOCUS 证据，也不扩大旧 coverage 声明。

## 5. 36/36 FOCUS 回放

postfix FOCUS 探针直接使用三份最终 bundle 的冻结 source span 作为调用方已诊断输入：

| 场景 | 最终 hunk | FOCUS AVAILABLE | 精确同界 | SUPPRESSED | suggestion 越权动作字段 |
|---|---:|---:|---:|---:|---:|
| COURSE | 17 | 17 | 17/17 | 0 | 0 |
| MODELING | 9 | 9 | 9/9 | 0 | 0 |
| GENERAL | 10 | 10 | 10/10 | 0 | 0 |
| 合计 | 36 | 36 | 36/36 | 0 | 0 |

“36/36”不是发现召回率：focus spec 本来就由已诊断 span 构成。它证明的是原 fresh 路径中 36 次手工
offset/registry 录入可以改为“原文片段 + 必要时 start_byte”，并且工具能准确冻结同一 byte range。
原始工件位于 `postfix-probe/*-focus.authoring.json` 与 `postfix-probe/*.focus.json`。

## 6. “非常”假否定根因与修复

旧 `_marker_counts` 对单字否定 marker“非”做 substring 计数。“非常”中的“非”因此进入 negation
Counter；当 course 代理删除“这一步非常直观地……”时，系统错误地认为一句否定被删除。

修复没有关闭“非”或放松真实否定变化。`SINGLE_MARKER_EXCLUSIONS` 只为 marker“非”增加显式窄排除
`("非常",)`，继续保留“并非/非/不/未/无”等其他否定观察。测试
`test_v40_feichang_is_not_counted_as_sentence_negation` 确认“非常”不再触发
`SPEECH_ACT_NEGATION_CHANGED`；既有真实否定变化测试继续通过。

## 7. 测试、失败优先与投影

### 7.1 当前安装字节测试

本次 root review 写入前在当前安装字节上实际执行：

```text
focused short-patch/invariant/validator=223 tests; 223 passed; 1 skipped
full unittest discovery=819 tests; 815 passed; 4 skipped
scaffold trace=1094 executed / 1218 executable lines = 89.82%
SKILL.md=451 lines
```

定向组包含 short PATCH 主链、authoring、span suggestion、invariant checker 和 unified validator。全量入口为
`python -m unittest discover -s tests -q`，运行 135.068 秒。一次误用 `-t .` 的 discovery 命令因 tests
目录不可导入而在收集前退出，不计测试失败或通过。

### 7.2 capability fail-closed 过程

本轮第一次全量运行发生在 capability 文件已改变、固定 projection policy 仍保存旧批准 hash 时。结果为
66 个同源 capability mismatch error 和 4 个由此派生的 failure；没有把这些错误逐个局部豁免。更新
`approved_capability_source_sha256` 到经审计的新能力树后，才重新运行并得到最终 819 项通过基线。

该早期失败属于预期 fail-closed 证据，不计最终通过，也不能从长期报告中省略。它证明固定批准 hash
确实阻止未经同步的能力面进入 projection；不证明被批准能力的文风质量。

### 7.3 双投影

最终投影：

- [primary](../generator-projection-maturity-v40-final-20260719/)
- [primary manifest](../generator-projection-maturity-v40-final-20260719.manifest.json)
- [repro](../generator-projection-maturity-v40-final-repro-20260719/)
- [repro manifest](../generator-projection-maturity-v40-final-repro-20260719.manifest.json)
- [trace](../maturity-v40-trace-final-20260719/)

机器基线：

```text
quick_validate source/final/repro=PASS/PASS/PASS
policy/builder=1.11.0/1.11.0
projection files=37/37
BYTE_DIFFS=0
capability_source=12a12fa725588f8da2a258b2280331fab7c47b1e63f183205c151f47c62b4799
projection_tree=750332eb2295923080a0361c86906b04e63a12a558c266ce6c949066519eb100
manifest_file_sha256=081b133c9212b9f7e16721b74caaddfd0bf99dd196d32fb0a179faa99fadf130
private-control path/content hits=0/0 per projection
evidence_cap=E2
generation qualification=NOT_EVALUATED
```

两份 manifest 字节哈希相同，37 个相对路径与内容哈希无差异；manifest audits 的 reference closure、
forbidden reference、secret-control identifier、Python compile/import closure 与 Skill quick validate 均为
PASS。projection 继续排除 qualification oracle、完整 replay/审批私有面和 second-pass 控制面。

## 8. 当前成熟度边界

v40 可以准确声称：

- v39 后剩余三个主要场景完成隔离 fresh 使用；
- 36 个词库外人工诊断 span 的录入成本有了确定性 FOCUS 路径；
- 全篇 editable-run 候选洪水经量化后被否决并从生产代码删除；
- 非 high advisory 不污染 high coverage；
- “非常”假否定被窄修复，真实否定门仍在；
- v1/v2 只读兼容、v3 生产写入、双投影和 819 项测试均通过当前机械验收。

v40 仍不能准确声称：

- scanner、advisory 或 FOCUS 自动发现了所有 AI 味；
- 36 个 fresh hunk 都比原文更自然；
- 本地模型可以签发 paired-quality clearance；
- verifier PASS 等于正式终稿、学术正确或个人声线成立；
- FOCUS spec 来自不可伪造的用户授权；
- 本地 E2 runner 已满足 E3 隔离或完成 188 项生成资格矩阵。

下一轮成熟化应攻击 FOCUS 的真实调用成本和误用面：重复片段消歧、过宽 focus、临近保护边界、调用方
把“已定位”冒充“已获授权”，以及普通用户能否在不理解 byte offset 的情况下完成失败恢复。评价标准应是
fresh 工件、错误恢复次数、过宽/错误 span 拒绝率和实际候选读感，不是继续增加规则数量。
