# v14 fresh second-pass 真实试跑审计

## 1. 结论

本次真实试跑没有取得模型输出，因此不产生 convergence receipt，也不支持“全文 Humanize 已完成”。最终状态为：

- 第一遍完整 clean run：`PASS`；
- fresh runner retry：`INFRA_INVALID`，`timed_out=true`；
- collect：`FAIL`，原因是缺少 trial output；
- 第二遍 finalizer：`REVIEW/2`，1 个初始 PENDING unit 仍为 PENDING；
- verifier：`REVIEW/2`，原因是 second pass incomplete；
- `humanize_second_pass_convergence=NOT_RUN`；
- `humanize_completion_claim_allowed=false`；
- receipt 文件不存在。

自动化测试证明控制链能拒绝错误完成态，但不能替代本次缺失的真实模型输出。

## 2. 输入与第一遍

输入使用现有研究类真实前向 fixture：

`tests/fixtures/humanize_forward_v10/research_after.md`

第一遍目录：`first-run/`。prepare 得到 1 个 PENDING unit、111 个作者汉字、1 个保护 span；scene 为 RESEARCH，Voice 为确定性 `SCENE_DEFAULT`。第一遍以 `NO_CHANGE` 完整发布，结果为：

- `status=PASS`；
- `coverage_completion_claim_allowed=true`；
- scene、rewrite binding、Voice binding、Voice conformance、cross-unit repetition 均为 PASS；
- source modified 为 0；
- 由于尚无 second pass，Humanize completion 两字段为 false。

## 3. Sealed case

控制面从第一遍唯一完整 `rendered/` 建立 `second-run/` 和 `cases/`：

- second-pass plan SHA-256：`f8b03906ae5b9a54c2ac845d36c48e6e325661883e56bc5c269a546f99490d75`；
- unit：`U-095dbdc63a18`；
- second chunk binding：`c5538b4b120ad96981739ebf181f82496119c0dbd37644083f14f4c1e3b33fee`；
- Voice Profile SHA-256：`18887ba292c25e48d8f9fc598e1a33fa721d1fa8795b3d78f9964af0773b39e0`。

sealed prompt 只要求模型重新审阅当前 masked chunk，并独立返回 REWRITE 或 NO_CHANGE；不包含第一遍 bundle、diff、decision、验收 atom 或期望答案。

## 4. 首次真实调用暴露的 runner 缺陷

首次调用设置内部 timeout 120 秒。外层在 184 秒终止命令，说明旧 `_invoke_codex` 只终止父进程，node/codex 子进程继续持有 stdout/stderr 管道，后续无 timeout 的 `communicate()` 仍会阻塞。检查发现本次调用留下一个 Python 父进程、一个 node 进程和一个 codex 进程；三者按 PID 与启动时间精确终止，未影响已有 VS Code/Codex 进程。

修复后，runner 在 Windows 使用新进程组，并在 timeout 时执行整棵进程树的强制终止；POSIX 路径使用独立 session/process group。真实孙进程回归测试从约 8.06 秒等待自然退出降到约 1.38 秒内收口。

## 5. Retry 与失败证据

retry 使用内部 timeout 45 秒，并在 46.3 秒内正常返回 `INFRA_INVALID`。权威证据为：

`trials-retry/U-095dbdc63a18/runner-receipt.json`

关键字段：

- `runner_status=INFRA_INVALID`；
- `exit_status.timed_out=true`；
- `exit_status.returncode=1`；
- `exit_status.output_present=false`；
- `generator_projection.projection_audit_status=NOT_COMPLETED`；
- `evidence_cap=E2`，但该 E2 只表示本地执行记录层级，不表示 trial 成功；
- `filesystem_isolation_verified=false`；
- `oracle_catalog_unreachable_to_generator=UNVERIFIED`。

retry 结束后按启动时间复查，没有遗留新的 Python、node 或 codex 进程。

## 6. 下游拒绝链

collect 因 `response/output.txt` 不存在返回 `FAIL`，没有复制 rewrite bundle，也没有生成 collection。第二遍 finalizer 使用空 rewrites 运行，返回：

- `status=REVIEW`、exit code 2；
- `unit_statuses.PENDING=1`；
- `rewrite_binding_status=REVIEW`；
- `voice_binding_status=REVIEW`；
- `voice_conformance_status=REVIEW`；
- `cross_unit_repetition_status=REVIEW`、scope PARTIAL；
- `coverage_completion_claim_allowed=false`；
- `humanize_completion_claim_allowed=false`。

verifier 随后返回 `REVIEW/2`：`second pass is incomplete or unresolved: status='REVIEW'`。它没有写出 `second-pass-receipt.json`。第一遍 finalizer因此没有 receipt 可消费，继续保持 `humanize_second_pass_convergence=NOT_RUN`。

## 7. 能证明与不能证明

本次真实试跑证明：控制面能生成不泄漏预期答案的 sealed case；runner 超时能留下明确失败 receipt 并收掉进程树；collect/finalizer/verifier 不会把无输出 trial 冒充收敛。

本次不能证明：真实模型能稳定返回 strict bundle；真实 second pass 会得到 NO_CHANGE；宿主文件系统或 oracle 对模型不可达；学术内容正确；作者身份真实。后续真实 campaign 必须从新的空 trial 目录启动，不能复用本次 `INFRA_INVALID` 工件冒充 fresh run。
