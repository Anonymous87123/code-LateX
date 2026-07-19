# Humanize Academic Chinese v36 根因与成熟度复盘

日期：2026-07-19  
版本：`policy/builder=1.10.6/1.10.6`  
范围：短 PATCH 当前策略重放、live-source 新鲜度、CLI 三态与投影发布  
结论：v36 关闭了“旧 validation 只要目录内部自洽就永久得到 verifier PASS”的假完成路径。verifier 现在先证明闭集记录完整，再比较当前 policy，并在同 policy 下重新运行统一验证器；显式 live source 只作为独立 currentness 观察，不能清除 policy drift 或 paired-quality 缺口。

## 1. 旧实现的可复现缺口

v35 verifier 会重放 bundle application、重算 diff、核对 manifest/result/validation 的部分绑定，但不重新运行当前 validator。攻击者可以修改 `validation.json` 中未被 result 单独绑定的层级状态，再同步重算 artifact 与 manifest hash；旧 verifier 仍返回 `PASS/0`。

本轮先把该路径写成 RED：修改 `speech_act_layer_status` 后重封 manifest，旧实现没有抛出 `CURRENT_POLICY_REPLAY_MISMATCH`。另外三个 RED 分别证明旧输出没有 current-policy 字段、函数不接受 live source、也没有 policy snapshot 比较入口。

## 2. 新三层裁决

| 层 | 证明范围 | 失败语义 |
|---|---|---|
| record integrity | 闭集、hash、bundle application、diff、result/validation 基础绑定 | 损坏或矛盾为 `FAIL/1` |
| current-policy replay | recorded policy 与当前一致时，用归档 source/candidate/bundle 重跑完整 validator 并比较完整 JSON | policy drift 为 `REVIEW/2 + NOT_RUN`；同 policy 不一致为 `FAIL/1` |
| live source currentness | 用户显式提供的当前文件是否仍与 source snapshot 同 hash | 未提供为 `NOT_PROVIDED`；匹配为 `MATCH`；漂移/不可用为 `REVIEW/2` |

记录完整性优先检查，因此 policy drift 不能掩盖工件损坏。current-policy replay 比较完整结构化结果，不只比较顶层状态；finding、warning fingerprint、分层状态、evidence、paired-quality/warning request SHA 任一漂移都会失败。

## 3. 状态拆分

verifier JSON 现在分别保存：

- `record_integrity_status`；
- `current_policy_status`；
- `current_policy_replay_status`；
- `live_source_status`；
- verifier 自身 `status/exit_code`；
- 候选 `delivery_gate_status=REVIEW/delivery_gate_exit_code=2`。

这避免把 verifier 的 `PASS/0` 误读成候选交付 PASS。参数错误也不再沿用 argparse 的退出码 2，而是结构化 `FAIL/1`，不与合法 `REVIEW/2` 混同。live-source 输出不保存或回显绝对路径。

## 4. 独立黑盒结果

fresh agent 对旧 v35 证据目录运行新版 verifier：

```text
record_integrity=PASS
current_policy=DRIFT
current_policy_replay=NOT_RUN
delivery=REVIEW
exit=2
```

追加与 snapshot 完全同 hash 的 `--live-source` 后，`live_source=MATCH`，但 policy 仍为 `DRIFT`，replay 仍为 `NOT_RUN`。这证明 currentness 门没有越权清除 policy 门。

## 5. 验证证据

```text
targeted short PATCH: 24 tests, OK (skipped=1)
expanded contracts/projection: 112 tests, OK (skipped=2)
full suite: 747 tests, OK (skipped=4)
quick_validate: PASS
```

双投影：

```text
files=35/35
BYTE_DIFFS=0
manifest bytes equal=true
capability_source_sha256=037dc2567803cbf738b87d9cfa6699817626035faf9b1e456cb4dcf08f87c785
projection_tree_sha256=cf43ee41113ca4515389379f6ca4ace61d5482ca7a855b8facacdfab5d2e94ca
manifest_sha256=2a6da6aafef7f047eb83a75388eb7bd95830ca74f574f4a35224055d74275423
evidence_cap=E2
private replay/qualification/second-pass identifiers=0 hits
```

## 6. 明确保留的边界

v36 仍不证明 selection 列全了所有 high finding、用户选择或显式冲突。`unlisted_source_policy=COPY_EXACT` 只证明未列文本被原样复制，不是 coverage completion。下一 P0 是建立独立、可重放的 coverage inventory；它最多证明冻结 scanner high inventory、绑定用户 selection 和显式声明 conflict pair 已逐项处置，不能证明所有自然语言语义冲突都已被发现。

同样没有改变以下边界：

- `humanize_quality_claim_allowed=false`；
- `academic_correctness=NOT_EVALUATED`；
- paired-quality 仍需可信外部复核；
- qualification 仍受 E2 上限约束，不能由本轮测试升级；
- GPT 生成的 MD/TeX 仍只作为负例压力材料。
