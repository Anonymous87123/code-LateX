# Humanize Academic Chinese 运行记录

## 配置

```yaml
mode: REWRITE
scene: COURSE
intensity: BALANCED
output: CLEAN
voice: SCENE_DEFAULT
report_context: NONE
scope: 指定 input.tex 的完整 9 行片段
```

未提供作者样本，因此使用课程场景默认声线。标题层级、TeX 命令与 equation 环境中的公式源码按保护区处理。

## 执行

1. 改前词项扫描：

   ```powershell
   python scripts\scan_humanize_chinese.py <input.tex> --scene COURSE --format text
   ```

   退出码为 `0`。共得到 4 个 high 候选：`LEX-EMPH-01`、`LEX-COACH-01`、`LEX-MARKET-01`、`LEX-FOUNDATION-01`。

2. 统一验证：

   ```powershell
   python scripts\validate_humanize_output.py <input.tex> <output.tex> --scene COURSE --format json
   ```

   进程退出码为 `2`。

3. 改后词项复扫：

   ```powershell
   python scripts\scan_humanize_chinese.py <output.tex> --scene COURSE --format text
   ```

   退出码为 `0`，未返回词项候选。模型上下文高风险快检也未发现空重点壳、教练腔、营销拔高、泛化意义、强制桥接或自动展望残留。

## 验证结果

```yaml
status: REVIEW
delivery_gate_status: REVIEW
process_exit_code: 2
protection_check: REVIEW
hard_invariant_layer_status: PASS
speech_act_layer_status: REVIEW
style_signal_layer_status: PASS
academic_correctness: NOT_EVALUATED
before_sha256: 9805eab8480836f942078c112dfcd4160c293cd18bfd79ae0e308c02db956b65
after_sha256: f5e0d2e66f7d2dc0e336fe635c9442ddecfd4637a2adc09e6e31c7f3cfd80d33
warning_review_request_sha256: 3f256d2ea72702fbf43a5ef38d6c29c20ee12fa46cf11c7b81a9d26b691811ee
warning_review: NOT_PROVIDED
```

`hard_invariant_layer_status=PASS` 仅表示验证器未发现公式、数字、关键 TeX 等硬保护项失败，不覆盖最终 `REVIEW/2`。未运行学术质控。

## Pending warnings

- `SPEECH_ACT_NEGATION_CHANGED`：原稿含 `不=2, 不能=1`，改后为 `不=1, 不能=1`。fingerprint：`ccf6b6e0532b4040bfc3e5259089a62373a7fda7da5d55c2a1ed154d4a6cf1ba`。
- `SPEECH_ACT_MODALITY_SCOPE_CHANGED`：原稿含 `只=1, 可以=1, 必须=1`，改后为 `可以=1, 需要=1`。fingerprint：`1fa471167c88d4d118ae1a40415f481af97849992a1892611aacc18548add30b`。

两条 warning 均保持 pending/unaccepted；未提交本地 caller proposal，也未声称人工复核或外部 clearance。按任务要求，不为改变状态继续进行同义替换。

## 主要动作

- 删除无信息的重点提示、价值宣告与后续学习桥接。
- 将空泛记忆命令降为低刺激课程表述，保留记忆公式这一学习要求。
- 合并重复纠偏，把条件检查、加速度方向和代入限制放在同一判断链中。
- 原样保留章节标题命令与 equation 环境中的公式源码；保留“速度随时间减小即可套用公式”这一输入命题，不判断其学术正确性。

## 未解决项

统一验证器要求对否定标记与模态范围变化进行复核，因此本次交付状态为 `REVIEW`，不是 `PASS` 或 `FAIL`。
