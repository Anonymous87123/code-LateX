# v43：短 PATCH AUTO 场景预冻结与低分歧义修复

## 1. 本轮目标

v42 已解决局部 warning 修订需要整链重建的问题，但 v41 的真实 GENERAL fixture 仍暴露另一条重复劳动链：调用方先按 `GENERAL` 建 authoring、finalize、bundle 和 review，之后才单独运行 route，发现实际应为 `MODELING`，只能重建同一批 span、hunk 和 selection。

本轮目标不是提高 route 的自然语言正确率，而是建立一条可重放、可拒绝歧义、不会覆盖用户显式场景的机械合同：

1. `--scene AUTO` 在任何 hunk/selection authoring 前解析；
2. requested/resolved scene、score、margin、reason、source 与 policy 绑定进入 scaffold；
3. finalize 不信任记录值，必须从当前 source/policy 重放；
4. 歧义 route 不得借 GENERAL 占位继续 authoring；
5. 显式用户场景保持最高优先级；
6. 旧 v1/v2/v3 authoring 保持只读兼容；
7. 低分正证据平局不能被 GENERAL fallback 或 document prior 静默掩盖。

## 2. 可复现基线

输入：

- `build/maturity-v41-fresh-focus-20260719/fixtures/general.md`
- source SHA-256：`9e32f2099d4ed90d5ce8564f319aaf68ecf0ea82f663382cebe97d4832825b70`

升级前，同一 source 的两个入口产生矛盾状态：

```text
route_humanize_scene.py --scene AUTO
  -> resolved_scene=MODELING
  -> scores COURSE=0, MODELING=8, RESEARCH=0
  -> margin=8

scaffold_humanize_short_patch.py create --scene AUTO
  -> schema=v3
  -> configuration.scene=AUTO
  -> scene_route missing
  -> NO_HIGH_FINDINGS/0
```

这不是模型判断波动，而是接口根本没有调用 route。调用方只有在 authoring 后另跑 route，v41 因而留下 GENERAL 初次、GENERAL retry、MODELING rebuild 三条链。

## 3. authoring v4 合同

新 schema：

```text
humanize-short-patch-selection-authoring/v4
humanize-short-patch-scene-route/v1
```

旧 `configuration.scene` 在 v4 中拆为：

```text
requested_scene
resolved_scene
```

route record 冻结：

- 完整 source SHA 与 size；
- document format；
- 保护内容屏蔽后的 full-source routing view SHA；
- requested/resolved scene；
- route status 与 reason code；
- COURSE/MODELING/RESEARCH scores、top score 和 margin；
- ambiguous scenes；
- 只含 rule ID、scope、occurrence、contribution 的 evidence；
- route policy schema/revision/canonical SHA；
- router executable SHA；
- `authoring_allowed`；
- route record 自哈希。

reason code 为闭集：

```text
USER_EXPLICIT_SCENE
AUTO_UNIQUE_SCORE_ABOVE_THRESHOLD
AUTO_DOCUMENT_PRIOR_WITH_LOCAL_SUPPORT
AUTO_INSUFFICIENT_SCENE_EVIDENCE
AUTO_LOW_MARGIN_OR_TIE
```

短 PATCH 不使用 document prior；该 reason 仅与共享 router 合同对齐。

## 4. 路由输入与隐私

AUTO route 不直接扫描未处理的完整原文。authoring 先复用保护索引与 TeX command span，把引语、数学、代码围栏、TeX 控制序列及参数替换为空格，同时保留换行，再将该 routing view 交给 router。

route evidence 不保存匹配文本，也不保存 source path。测试把不可导出的项目代号放入命中句，序列化 route record 中没有该代号，也没有 `matched_text` 字段。

这只限制工件泄漏面，不证明模型上下文没有见过 source。

## 5. 显式场景、AUTO fallback 与歧义

### 5.1 显式场景

`--scene GENERAL|COURSE|MODELING|RESEARCH` 固定：

```text
status=EXPLICIT
requested_scene=resolved_scene
scores=0/0/0
reason=USER_EXPLICIT_SCENE
```

即使 source 含强 MODELING 信号，显式 GENERAL 也不会被启发式覆盖。该规则只表示配置优先级，不证明本地 caller 标签来自独立用户授权。

### 5.2 唯一弱证据与无证据

真正无专属证据，或只有一个场景的唯一弱证据且未达到强路由阈值时，允许：

```text
FALLBACK_GENERAL
AUTO_INSUFFICIENT_SCENE_EVIDENCE
authoring_allowed=true
```

### 5.3 两个正分场景竞争

红队发现旧 router 先执行 `top_score < minimum_route_score -> GENERAL`，导致：

```text
本题需要说明。本研究需要说明。
COURSE=2, RESEARCH=2, margin=0
```

被错误写成 `FALLBACK_GENERAL`；若 document prior 为 COURSE，还会静默变成 `ROUTED_DOCUMENT_PRIOR/COURSE`。

revision 3 改为：

- `top_score=0` 才直接 GENERAL；
- 两个正分场景平局，或竞争场景 margin 低于阈值，先判 `AMBIGUOUS`；
- 之后才处理唯一弱证据 GENERAL fallback；
- document prior 只能补全唯一 top 且 second score 为 0 的弱证据，不能替平局选边。

长文 prepare 对新的低分平局同样生成 `UNRESOLVED` unit，顶层 `scene_routing_status=REVIEW`。

## 6. finalize 的确定性重放

v4 finalize 执行：

1. 严格读取 source 与 authoring；
2. 校验 source record；
3. 校验 requested/resolved configuration；
4. 校验 route record 闭集和自哈希；
5. 从当前 source、保护规则、router 和 policy 重新生成完整 route record；
6. 逐字段比较；不一致为 `SCENE_ROUTE_DRIFT/FAIL`；
7. 重算包含 route record 的 inventory hash；
8. 若 `authoring_allowed=false`，返回 `SCENE_ROUTE_AMBIGUOUS/FAIL`，不写 selection；
9. 只有合法 route 才继续原有 span/hunk/coverage 门；
10. 最终 v2 selection 的 `scene` 使用 `resolved_scene`，不再把 `AUTO` 传给 bundle/validator。

攻击测试先修改 MODELING score，再协调重算 route record hash 与 inventory hash；finalize 仍因 source/current-policy 重放不一致拒绝，说明它不是只验调用方自哈希。

## 7. CLI 三态

```text
AUTO unique/fallback + high findings -> PENDING/0
AUTO unique/fallback + no high -> NO_HIGH_FINDINGS/0
AUTO tie/low margin -> ROUTE_REVIEW/2
malformed/hash/source/policy/route drift -> FAIL/1
```

`ROUTE_REVIEW/2` 会写出 route-bound 审计 scaffold，便于查看 scores/margin；但 `authoring_allowed=false`，任何 hunk、selection 或本地重封都不能 finalize。它不是一个可继续编辑的 GENERAL scaffold。

## 8. 真实 GENERAL fixture 单链前向回放

工件：

- [v4 authoring](runs/general-auto/selection.authoring.v4.json)
- [resolved v2 selection](runs/general-auto/selection.v2.json)
- [bundle](runs/general-auto/patch.bundle.json)
- [closed review](runs/general-auto/review/review.md)

create 当场得到：

```text
schema=humanize-short-patch-selection-authoring/v4
requested=AUTO
resolved=MODELING
status=ROUTED
reason=AUTO_UNIQUE_SCORE_ABOVE_THRESHOLD
scores={COURSE:0, MODELING:8, RESEARCH:0}
top=8; margin=8
policy revision=3
policy SHA=fa460a93142173f1a89f343f5aeb771db0a19933c4b04785c823ea7181e12e81
route record SHA=ce4a75bb6db1b97dec0550f5293d981e98ab6690c98aa57a42b2c0c63bdd95d0
```

v4 产生的 3 个 focus span、registry 与 suggestion inventory 和旧 MODELING rebuild 逐字相同。把旧最终 selection 的 3 个真实语义决策映射到这些 source-bound span 后，只运行一次 finalize→build→apply：

```text
selection.scene=MODELING
bundle=2f763ca9d54ef8ecb1579920566a2bb405214b3fbe10efede3de98775788d561
candidate=f7669aecd306bca8f1827eb579be565186557fcd2a87948e5a4a9f4384524c41
```

新候选与 v41 `short-patch-review.modeling.final/candidate.review.md` 字节完全相同。说明 scene 预冻结没有改变语义决策或候选，只删除了先做 GENERAL、再按 MODELING 重建的错误工作流。

当前 policy 下该候选仍触发：

```text
SPEECH_ACT_FIRST_PERSON_REFERENCE_INTRODUCED
mechanical=REVIEW
hard/speech/style=PASS/REVIEW/PASS
delivery=REVIEW/2
```

这条 warning 没有被 route 成功掩盖。verifier 结果：

```text
record/current-policy/coverage/live-source=PASS/PASS/PASS/MATCH
verifier=PASS/0 scope=SELF_CONSISTENCY_ONLY
candidate delivery=REVIEW/2
```

## 9. 测试与投影

```text
route + short authoring/span + prepare focused=67/67
short-PATCH + route + prepare focused=156/156, skipped=1
projection tests=42/42, skipped=1
full unittest=851 total; 847 passed; 4 skipped
SKILL.md=453 lines; 324 non-empty
quick_validate source/final/repro=PASS/PASS/PASS
policy/builder=1.14.0/1.14.0
scene routing policy revision=3
approved capability=8e17aafa6aa949c2a851f2b637afb828813f329c5d55432c31b2600223e0af2a
projection files=38/38; BYTE_DIFFS=0
projection tree=3bf19755676806c2393367c3c7cdc916b39b356f8f799433c1500cd5cd7784e2
manifest=3c6796ed71398f19e83e5fa9db8e9101b76a24a6f0edc67145d617b5a4ade3fe
evidence_cap=E2
generation qualification=NOT_EVALUATED
```

## 10. 仍未完成的成熟度项目

本轮闭合的是短 PATCH AUTO route prefreeze 和共享 router 的低分歧义漏洞。仍有独立缺口：

1. 长文 `scaffold_humanize_rewrites.py` 虽然消费已冻结 chunk hash，但 authoring 模板不显式展示 scene/route，也没有在模板生成前重放 prepare integrity、live source 和 route；当前仍是 finalize 事后拦截，属于下一优先级 preflight 工作。
2. 显式场景保持最终权威，但共享 router 的 EXPLICIT 分支不计算只读 observed scores，因此还不能机械提示“用户显式场景与明显用途冲突”；不能让启发式覆盖用户，但应增加 REVIEW 诊断面。
3. registry/offset/ID repair、hunk/selection `reason_ref` 尚未实现。
4. 可信外部 paired-quality clearance、学术正确性、证据真实性、作者身份和 generation qualification 均未建立。

因此不能声称 Skill 已无人值守完成全文 Humanize。准确状态是：短 PATCH 的 AUTO authoring 已从“事后发现 scene”升级为“先冻结、可重放、歧义拒绝”，且真实候选没有被这次工程改动偷偷改写。
