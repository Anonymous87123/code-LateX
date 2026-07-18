# v25 paired-quality 红队根因与门禁

## 反例

v24 候选在公式、数字、TeX、词项和言语行为门上均可通过，但独立盲读仍指出“但求解先要确定”
搭配紧缩。该反例证明开放式自然度不能由封闭词表或硬不变量穷尽，也不能通过给这一句话新增禁词
解决。

## 旧错误链

```text
删掉显眼主持壳
-> 为补齐句法引入新搭配或抽象桥接
-> 词项数量下降、硬不变量不变
-> validator PASS
-> finalizer DONE/rendered
-> fresh second pass NO_CHANGE
-> 错误声称全文质量完成
```

## v25 分层

```text
candidate assembly / mechanical validation
-> paired-quality request coverage
-> external paired-quality clearance
-> second-pass stability
-> delivery gate
```

当前本地工具只实现 request 签发和 fail-closed 状态，不实现可信 response 验签。每次 `REWRITE`，
包括 `NO_CHANGE`，都生成 `humanize-paired-quality-review-request/v1`，绑定 before/after SHA、逐 hunk
行区间/hash、决策、场景、范围和 policy hash。机械 PASS 后顶层仍为 `REVIEW/2`，长文只发布
`rendered_review/`。

## 本轮新增故障注入

测试 monkeypatch `_persist_paired_quality_review_request` 令一个已接受 unit 的 request 消失。旧 v25
中间实现虽然写出 `paired_quality_gate_status=BLOCKED` 和 `missing=1`，仍可能返回 `PASS/0` 并发布
正式 `rendered/`。根因是 delivery block 只识别 `PENDING_EXTERNAL_REVIEW`，漏掉 `BLOCKED`。

修复后：

- `PENDING_EXTERNAL_REVIEW` 与 `BLOCKED` 都阻断正式交付；
- candidate bytes 可保持 assembly PASS，但 delivery 固定 REVIEW/2；
- 只能发布 `REVIEW_CANDIDATE -> rendered_review/`；
- request 缺失同样禁止 second-pass receipt；
- partial 补齐为完整 review candidate 后删除旧 `rendered_partial/`，避免目录猜测歧义。

对应回归位于 `tests/test_finalize_humanize_long_document.py`。本门仍不证明候选自然，只保证质量证据
缺失时不能静默冒充正式完成。
