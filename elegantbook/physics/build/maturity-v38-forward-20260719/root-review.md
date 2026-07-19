# v38 root review: source-bound authoring and deterministic review

## 裁决

v38 工程验收通过。它关闭 v37 明确保留的两项作者体验缺口：同一 source span 不再需要在 hunk 与
selection 中重复抄录；普通 diff 看不到的 unchanged `UNRESOLVED` 与显式 conflict pair 进入确定性
`review.md`。这两项改进没有扩大证明范围，也没有把 authoring 文件、review 视图或 verifier PASS
包装成用户授权、语义完整性、文风质量或学术正确性。

最终 fresh candidate 仍为 `DELIVERY REVIEW/2`。生成资格保持 `NOT_EVALUATED`，投影证据能力上限
保持 `E2`。

## 1. Authoring 合同

新增两阶段 authoring 工具：

```text
create   -> humanize-short-patch-selection-authoring/v1
finalize -> humanize-short-patch-selection/v2
```

`create` 冻结 source SHA/size/format、任务配置、AUTO high inventory，以及 scanner、lexicon、coverage
builder 和 Python/Unicode runtime policy。每个 high occurrence 先登记到唯一 span registry；hunk、selected
span 与 lexical resolution 通过 ID 独立引用。需要更宽句级 span 时只在 registry 新增一次，不再分别向
hunk 和 selection 抄两份 source text。

`finalize` 重新读取 source、重跑 AUTO high、核对 policy 与 inventory，并拒绝：

- `PENDING` lexical resolution；
- source、authoring 或 policy 在执行前后漂移；
- 悬空、大小写重复或错误类型的 span/hunk/selection 引用；
- 同一 exact source span 重复登记，或一个 finding 被多个 span 绑定；
- high inventory 漏项、非法 KEEP、selection/hunk span 不一致；
- 非法 replacement、空泛理由和错误 conflict pair。

finalize 内部先调用正式 short-patch builder 重验 v2 coverage，成功后才原子写出 selection；正式 build
阶段还会再次重算。authoring scaffold 自身不是 evidence，也不证明 selection 来自真实用户请求。

## 2. Review 工件与闭集

当前 applicator 使用：

```text
humanize-short-patch-result/v2
humanize-short-patch-verification/v3
```

成功发布时 evidence 闭集固定包含 `review.md`。该文件由 bundle、coverage、validation 与 result
确定性渲染，并显示：

1. 已变化的 hunk；
2. diff 中不可见、但 candidate 原样保留的 `UNRESOLVED` hunk；
3. 显式 conflict pair 的左右绑定和 caller-declared 限制；
4. coverage task scene、`scan_scene=AUTO`、source kind 与窄 scope；
5. mechanical、paired-quality、semantic completeness 与 academic correctness 的独立状态。

source、replacement 和 reason 全部 HTML escape，不能借 Markdown/HTML 注入改变 review 结构。verifier
重算 review 的精确字节；即使攻击者同步重封 manifest，review 漂移仍为 `FAIL/1`。旧 result v1 没有
review 时只读兼容，固定 `review_artifact_status=NOT_PROVIDED`，不会静默升级。

## 3. TDD 与已知证据边界

本轮先写 RED，再进入生产实现。RED 覆盖 source text 重复录入、PENDING、source/policy race、错误引用、
INLINE_SELECTION 无绑定、非法参数退出码、review 中 unchanged UNRESOLVED/conflict 不可见，以及 review
被改写或重新封装后的 verifier 拒绝。GREEN 后 authoring 定向测试为 11 项。

两个面向异常输入的独立子代理在平台侧被分类器拦截，没有形成可采信的最终裁决，因此不计入红队
通过数，也不用于支持“异常输入已覆盖”的结论。现存 `maturity-v38-authoring-attack-20260719` 是失败
快照：`all_expected_failures_structured=false`，且后续 r2 没有 summary/result；
`maturity-v38-review-attack-20260719` 只有 PENDING scaffold，没有 harness、oracle、result 或 summary。
两者都不是通过证据。有效 forward 证据只包括可复核的 fresh 用户工件、本地 RED/GREEN 测试、trace
与投影复现。

## 4. Fresh 用户路径

全新代理只读取原始课程 TeX 和当前 Skill，生成：

```text
AUTO high=4
span registry=9
hunks=5
selected spans=5
explicit conflicts=1
pending=0
finalize=selection/v2
build=BUNDLED/0
apply=DELIVERY REVIEW/2
verify=PASS/0 SELF_CONSISTENCY_ONLY
coverage replay/current-policy replay=PASS/PASS
live source=MATCH
```

`review.md` 正确展示 H003/H005 两个 unchanged `UNRESOLVED` 和 C001 conflict pair。但候选删除“必须”
后仍触发 `SPEECH_ACT_MODALITY_SCOPE_CHANGED`：hard/style 层通过，speech-act 与 mechanical 保持 REVIEW，
paired-quality 为 `BLOCKED_BY_MECHANICAL_GATE`。这说明新的可读 review 没有遮蔽原有语义风险门。

完整 fresh 记录见
[review-report.md](../maturity-v38-fresh-user-20260719/review-report.md)。

## 5. 最终复验

2026-07-19 在最终 v38 安装字节上重新执行：

```text
authoring tests: 11 total; 11 passed
full suite: 781 total; 777 passed, 4 skipped
authoring scaffold script line coverage: 87%
quick_validate: source/final projection/repro projection PASS/PASS/PASS
SKILL.md: 449 lines
policy/builder=1.10.9/1.10.9
projection files=37/37
BYTE_DIFFS=0
capability_source=60e326974d022c1c9d659780769277aec985d29f3a378d55b0540f9d9f358645
projection_tree=802b971d25252caccbd19a30bce644b3c883329ef3e44a5113c80652a555b6e3
manifest_file_sha256=8eb5d81e5f5f676bad48109a158b5c69c1fa41ae227acba18ad4d972e0be8ba5
evidence_cap=E2
```

两份 manifest 文件 SHA-256 相同；两棵 projection 各 37 文件，逐相对路径和 SHA-256 比较差异为 0。
投影继续隔离 qualification oracle、完整 replay 审计、外部审批私有面和 second-pass 控制面。
上述结论绑定当前工作区字节；Skill、tests 与 build 证据当前未形成 Git commit，本轮按用户要求不提交。

## 6. 下一成熟度缺口

v38 去掉了跨结构重复抄写，却没有消除“为每个实际改写手工新增更宽 hunk span”的成本。fresh 任务中
9 个 registry span 有 4 个来自 high inventory，另有 5 个由调用方手工补入。下一步应由冻结 source 与
保护范围确定性提出句级/段级候选 span，但只能作为建议：不得自动填写 replacement、KEEP reason、
selection、conflict 或用户授权，也不得让建议 span 绕开 protection/coverage 门。
