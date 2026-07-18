# Voice Profile v1：最小生产契约审计

## 1. 结论

建议把 Voice Profile 做成两个强绑定、可独立验证的产物：

1. `voice_sample_manifest.json`：冻结样本字节、来源角色范围、保护区剔除结果、去重结果和逐证据锚点；
2. `voice_profile.json`：只保存结构化风格特征、逐 feature 证据索引和 DEFAULT 语义，不保存样本文本。

Profile 必须绑定 manifest、提取策略和 feature registry 的 SHA-256。消费端只有在 schema、哈希、角色隔离、去重、阈值和逐 feature evidence 全部通过时，才可应用个人 Profile。样本不足是合法的 `DEFAULT`，不是低置信个人声线；来源归属不明、保护区无法可靠切分或样本在构建期间变化则是 `REVIEW/FAIL`，不能伪装成 DEFAULT/PASS。

## 2. 审计边界与现状

本审计只读取：

- 正式 Skill 的 `SKILL.md`“作者声线”段；
- `references/voice-profile.md`；
- 正式 `scripts/` 目录的文件名。

未读取脚本内容、tests、build、历史报告或 qualification 材料。

从文件名可观察到通用扫描、保护检查和输出验证入口，例如 `scan_humanize_chinese.py`、`check_humanize_invariants.py`、`validate_humanize_output.py`；未观察到名称明确的 Voice Profile builder 或独立 validator。下文只把这些现有入口列为集成候选，不假定其内部 API 或当前行为。

正式合同已经给出以下不可降级约束：

- 只从 `author` 内容学习，排除 quoted、题干、OCR、代码、数学、模板和归属不明的多作者文本；
- 少于 300 个可读作者汉字时使用 DEFAULT；300/1000/5000 字分别对应 LOW/MEDIUM/HIGH 边界，HIGH 还要求至少 3 个完整文本单元；
- 同一段重复不能增加样本量，候选习惯须跨至少 3 个位置出现；
- 优先保留第一人称、节奏、标点、括号、压缩度、限定方式、术语和允许短语；
- 高频词不直接等于声线，保护区优先于 Profile；
- 不把模型输出自动回灌为作者样本；
- DEFAULT 不得声称复现个人文风。

## 3. 产物与信任边界

最小产物集：

```text
voice_samples.spec.json          # 调用方声明；不可信输入
voice_sample_manifest.json       # builder 冻结、过滤和去重后的审计清单
voice_profile.json               # 可消费档案；不含样本文本
voice_profile.validation.json    # validator 结果；可选但建议持久化
```

`voice_samples.spec.json` 只能表达“调用方确认此范围为作者文本”，不能证明作者身份。公开状态固定保留 `identity_verified=false`。样本文本始终按数据处理，不能作为 prompt、命令、配置或动态脚本执行。

## 4. `voice_profile.json` 最小 schema

### 4.1 顶层字段

```json
{
  "schema_version": "humanize-voice-profile/v1",
  "profile_id": "author-style-001",
  "revision": 1,
  "supersedes_profile_sha256": null,
  "profile_kind": "PERSONAL",
  "validation_status": "PASS",
  "confidence": "MEDIUM",
  "sample_binding": {
    "manifest_sha256": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
    "readable_author_chars": 2180,
    "unique_analysis_units": 17,
    "unique_complete_units": 2,
    "sample_scenes": ["RESEARCH"]
  },
  "policy_binding": {
    "role_policy_sha256": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
    "dedup_policy_sha256": "cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc",
    "feature_registry_sha256": "dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd",
    "scene_default_policy_sha256": "eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee"
  },
  "features": [
    {
      "feature_key": "voice.first_person.0001",
      "feature_type": "voice.first_person",
      "scope": ["RESEARCH"],
      "disposition": "PREFER",
      "confidence": "MEDIUM",
      "value": {
        "kind": "CATEGORY",
        "code": "EXPLICIT_METHOD_CHOICE_ONLY"
      },
      "evidence": {
        "extractor_id": "first-person/v1",
        "extractor_sha256": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
        "opportunity_count": 12,
        "support_count": 9,
        "counterexample_count": 3,
        "support_ratio_ppm": 750000,
        "distinct_analysis_units": 6,
        "distinct_complete_units": 2,
        "anchors": [
          {
            "unit_id": "unit-01",
            "byte_start": 210,
            "byte_end": 216,
            "span_sha256": "1111111111111111111111111111111111111111111111111111111111111111",
            "judgment": "SUPPORT"
          },
          {
            "unit_id": "unit-09",
            "byte_start": 85,
            "byte_end": 91,
            "span_sha256": "2222222222222222222222222222222222222222222222222222222222222222",
            "judgment": "COUNTEREXAMPLE"
          }
        ]
      }
    }
  ],
  "negative_controls": [
    {
      "feature_key": "transition.shell.0001",
      "feature_type": "transition.shell",
      "scope": ["GLOBAL"],
      "disposition": "DO_NOT_AMPLIFY",
      "confidence": "LOW",
      "value": {
        "kind": "CATEGORY",
        "code": "EMPTY_EMPHASIS_SHELL"
      },
      "evidence": {
        "extractor_id": "style-signal/v1",
        "extractor_sha256": "3333333333333333333333333333333333333333333333333333333333333333",
        "opportunity_count": 3,
        "support_count": 3,
        "counterexample_count": 0,
        "support_ratio_ppm": 1000000,
        "distinct_analysis_units": 3,
        "distinct_complete_units": 2,
        "anchors": []
      }
    }
  ],
  "defaults": {
    "use_scene_default": false,
    "scene": "RESEARCH",
    "reason": null,
    "disclosure_required": false,
    "personal_voice_claim_allowed": true
  },
  "claims": {
    "identity_verified": false,
    "author_personality_inferred": false,
    "academic_correctness": "NOT_EVALUATED",
    "sample_text_embedded": false
  },
  "profile_sha256": "4444444444444444444444444444444444444444444444444444444444444444"
}
```

### 4.2 规范约束

实现时应提供 JSON Schema Draft 2020-12，所有对象固定 `additionalProperties=false`，并执行以下约束：

| 字段 | 类型与约束 |
|---|---|
| `schema_version` | 固定为 `humanize-voice-profile/v1` |
| `profile_id` | `^[A-Za-z0-9][A-Za-z0-9._-]{2,127}$`；不是作者身份标识 |
| `revision` | 1 至 2^31-1 的整数 |
| `supersedes_profile_sha256` | `null` 或 64 位小写十六进制；修订时必填旧档哈希 |
| `profile_kind` | `PERSONAL` 或 `DEFAULT` |
| `validation_status` | `PASS`、`REVIEW` 或 `FAIL`；只有 PASS 可消费 |
| `confidence` | `LOW`、`MEDIUM`、`HIGH`、`DEFAULT` |
| `features` | feature_key 唯一；只允许 feature registry 登记的 `feature_type/value.code` 组合 |
| `scope` | 非空且只含 `GLOBAL/COURSE/MODELING/RESEARCH/GENERAL`；`GLOBAL` 不与其他值并存 |
| `disposition` | `PREFER/ALLOW/RARE/AVOID/DO_NOT_AMPLIFY` |
| `value.kind` | 只允许 `CATEGORY/ORDERED_SET/DISTRIBUTION/LEXEME`；前三类值由 registry 枚举，不能放自由文本指令 |
| 计数与比例 | 非负整数；比例使用 `support_ratio_ppm`，不用浮点数、NaN 或 Infinity |
| `anchors` | 只保存 unit、原始字节偏移、span hash 和 SUPPORT/COUNTEREXAMPLE；不保存原句 |
| `claims` | `identity_verified=false`、`author_personality_inferred=false`、`academic_correctness=NOT_EVALUATED`、`sample_text_embedded=false` 均为常量 |
| `profile_sha256` | 对去掉该字段后的 canonical profile 计算，算法见第 6 节 |

`PERSONAL` 的额外不变量：

- `confidence` 不能是 DEFAULT；`defaults.use_scene_default=false`；
- `features` 至少 1 项；
- `negative_controls` 至少 1 项，或至少一个已接受 feature 含可定位 counterexample；
- 每个 feature 都必须有独立 evidence，不能用 profile 总字数替代逐 feature 证据；
- 不允许把相同 anchor 同时计为 support 与 counterexample；锚点不得重叠 protected/excluded 范围。

`DEFAULT` 的额外不变量见第 9 节。

## 5. `voice_sample_manifest.json` schema

Manifest 只保存定位、哈希、角色图和计数，不保存整段样本文本：

```json
{
  "schema_version": "humanize-voice-sample-manifest/v1",
  "allowed_root_id": "workspace-root",
  "hash_spec": {
    "algorithm": "SHA-256",
    "json_canonicalization": "RFC8785-JCS",
    "text_integrity_view": "UTF8-NFC-LF/v1",
    "dedup_view": "VOICE-DEDUP/v1"
  },
  "policy_binding": {
    "role_policy_sha256": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
    "dedup_policy_sha256": "cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc",
    "unitizer_sha256": "5555555555555555555555555555555555555555555555555555555555555555"
  },
  "samples": [
    {
      "sample_id": "sample-01",
      "locator": "samples/chapter-01.md",
      "origin": "USER_CONFIRMED_AUTHOR",
      "scene": "RESEARCH",
      "encoding": "UTF-8",
      "file_size": 8432,
      "file_sha256": "6666666666666666666666666666666666666666666666666666666666666666",
      "role_map_sha256": "7777777777777777777777777777777777777777777777777777777777777777",
      "author_view_sha256": "8888888888888888888888888888888888888888888888888888888888888888",
      "complete_unit_ids": ["complete-01"],
      "analysis_unit_ids": ["unit-01", "unit-02"],
      "readable_author_chars_before_dedup": 912,
      "readable_author_chars_after_dedup": 846
    }
  ],
  "role_ranges": [
    {
      "sample_id": "sample-01",
      "byte_start": 0,
      "byte_end": 580,
      "role": "author",
      "range_sha256": "9999999999999999999999999999999999999999999999999999999999999999"
    },
    {
      "sample_id": "sample-01",
      "byte_start": 580,
      "byte_end": 700,
      "role": "quoted",
      "range_sha256": "0000000000000000000000000000000000000000000000000000000000000000"
    }
  ],
  "analysis_units": [
    {
      "unit_id": "unit-01",
      "sample_id": "sample-01",
      "byte_start": 0,
      "byte_end": 310,
      "canonical_author_sha256": "1212121212121212121212121212121212121212121212121212121212121212",
      "dedup_sha256": "1313131313131313131313131313131313131313131313131313131313131313",
      "dedup_cluster_id": "cluster-01",
      "is_representative": true,
      "readable_author_chars": 168
    }
  ],
  "aggregate": {
    "requested_samples": 1,
    "accepted_samples": 1,
    "rejected_samples": 0,
    "readable_author_chars": 846,
    "unique_analysis_units": 2,
    "unique_complete_units": 1,
    "protected_ranges": 1,
    "excluded_ranges": 0
  },
  "manifest_sha256": "1414141414141414141414141414141414141414141414141414141414141414"
}
```

补充约束：

- `locator` 必须是相对 `--allowed-root` 的 POSIX 形式路径；不在公开 Profile 中重复保存；
- `origin` 只允许 `USER_CONFIRMED_AUTHOR`、`USER_CONFIRMED_ADOPTED`、`UNKNOWN`、`MODEL_GENERATED`；后两类不得进入学习语料；`USER_CONFIRMED_ADOPTED` 仅用于用户确认且实际采用的文本；
- 字节区间使用半开区间 `[byte_start, byte_end)`，按原始文件字节定位；
- `role_ranges` 排序、无重叠；嵌套区域在生成角色图前按保护优先级切成不重叠片段；
- 未能确定角色的范围标为 excluded/unknown，不得默认升级成 author；
- manifest 中的计数必须可由冻结字节、角色图、unitizer 和 dedup policy 重建。

## 6. 哈希规范

所有哈希使用域分离：

```text
H(tag, payload) = SHA256(UTF8(tag) || 0x00 || payload)
```

建议 tag：

```text
humanize-voice-file/v1
humanize-voice-role-map/v1
humanize-voice-author-view/v1
humanize-voice-dedup-view/v1
humanize-voice-range/v1
humanize-voice-manifest/v1
humanize-voice-profile/v1
```

规则：

1. `file_sha256` 对原始文件字节计算，不做换行或编码规范化；
2. `role_map_sha256` 对排序后的非重叠角色区间 JCS 计算；
3. `author_view_sha256` 对剔除保护/排除跨度后的特征视图计算：严格解码、Unicode NFC、CRLF/CR 统一为 LF，但保留标点、括号、空格和段落结构；
4. `dedup_sha256` 对独立 dedup 视图计算，不能把 dedup 规范化后的文本用于风格提取；
5. manifest/profile 的 self hash 对移除 self-hash 字段后的 JCS 字节计算；
6. JSON 解析器必须拒绝重复 key、非 UTF-8、浮点非有限值和超深嵌套；
7. SHA-256 是完整性绑定，不是隐私保护。公开产物不得依赖“只有哈希所以不会泄漏”的假设。

## 7. 去保护与样本冻结算法

建议固定为以下确定性流程：

1. **路径闭合**：将 locator 解析到 `allowed_root`；拒绝绝对路径、`..` 越界、符号链接/结点重解析越界、设备文件和非普通文件。
2. **一次性冻结**：以 no-follow 方式打开，限制单文件和总字节数，一次读取成不可变快照并计算 `file_sha256`。发布前重新核对路径、文件身份和哈希；变化返回 `CHANGED_AFTER_SNAPSHOT/FAIL`。
3. **严格解码**：使用 manifest 声明编码严格解码；乱码、NUL、非法序列或 OCR 不确定区域不得猜测为作者文本。
4. **角色切分**：先在完整文件上识别 quoted、exam-original、OCR、code、math、模板固定区和 unknown，再产生不重叠 role map；保护区识别不能从截断片段中间开始。
5. **保护优先**：嵌套冲突按最内层保护角色优先；只保留作者对公式、引语、题干和代码的外围叙述。
6. **模板排除**：模板标题、固定声明和格式样例应由显式 selector/hash 清单排除；启发式命中只能进入 REVIEW，不能静默删除。
7. **单元化**：完整文件或用户指定完整章节形成 `complete_unit`；作者段落形成 `analysis_unit`。空段、纯结构行和保护区不计作者字数。
8. **审计计数**：同时记录 author、protected、excluded 字节/字符/区间数量及排除原因。

角色识别可评估是否复用现有保护检查或长文准备逻辑，但在读取和核对其真实接口前，不应直接宣称两者语义一致。

## 8. 去重、阈值与逐 feature evidence

### 8.1 去重

去重只影响样本计数和证据独立性，不改变用于风格测量的文本：

1. 为每个 analysis unit 构造 dedup 视图：NFC、统一换行、折叠空白；只在 dedup 视图中去掉普通标点和空白，保留汉字、字母、数字顺序；
2. 完全相同 `dedup_sha256` 归入同一 cluster；
3. 对不少于 40 个规范字符的单元计算字符 5-gram；以确定性 MinHash/LSH 产生候选，再做精确 Jaccard/containment；
4. `Jaccard >= 0.90` 或较短单元被较长单元 `containment >= 0.95` 时归为近重复；不足 40 字只做 exact dedup，避免短段误并；
5. 每个 cluster 只取一个代表单元计入作者字数、unit 数和 feature 支持数；其他成员保留 manifest 记录但标 `is_representative=false`；
6. 同一单元内重叠 occurrence 不能伪装成多个独立位置。

### 8.2 Profile 总体置信阈值

严格沿用正式合同：

| 去保护、去重后的可读作者正文 | Profile |
|---|---|
| `< 300` 汉字 | `DEFAULT`；不建立个人特征 |
| `300–999` 汉字 | `LOW`；只采用显著且无明显反例的特征 |
| `1000–4999` 汉字 | `MEDIUM` |
| `>= 5000` 汉字且 `unique_complete_units >= 3` | `HIGH` |
| `>= 5000` 但完整单元少于 3 | 最高仍为 `MEDIUM` |

字数只计代表 analysis units，不计保护区、模板、unknown、重复 cluster 和模型生成样本。

### 8.3 逐 feature 门

总体字数不自动授权任何 feature。每个 feature 必须由 registry 定义“机会、支持、反例、值域和 extractor”，并通过：

1. `support_count >= 3`；
2. 支持来自至少 3 个去重后的 `distinct_analysis_units`；
3. 每个锚点不重叠，且全部落在 author role；
4. `support_count + counterexample_count <= opportunity_count`；
5. LOW Profile：`counterexample_count=0` 才可用；
6. MEDIUM/HIGH：`support_ratio_ppm >= 700000`；不足则登记为可选变体或省略，不能写成稳定偏好；
7. 分布型节奏特征还需至少 20 个句子、5 个段落、3 个 analysis units；只保存整数分位数/比例，不只报均值；
8. 场景子档案只允许 HIGH Profile，并要求该场景自身至少 1000 个唯一作者汉字、2 个 complete units 和该 feature 的完整证据门；
9. `LEXEME` 值只允许短功能词或短连接语，连续汉字不得超过 7 个；更长习惯只保存 registry 功能码，避免把样本片段变成句库；
10. 任何 feature 新增的可消费字符串若与样本形成 8 个及以上连续汉字的唯一重合，validator 返回 REVIEW/FAIL；证据锚点本身不保存原文。

解释峰值、主次、言语行为等无法由确定性 extractor 复核的候选，不应直接写成 PASS feature。v1 最小生产版可先只发布可重建的节奏、主语位置、第一人称、标点、连接功能、版式和短词项特征；语义型候选保留在非消费审阅报告，状态 `NOT_EVALUATED/REVIEW`。

### 8.4 反例与 `do_not_amplify`

- 每个 feature 都要显式记录 counterexample 数量；没有反例时写 0，不能省略；
- PERSONAL Profile 至少有一个反例锚点或一个 `negative_controls` 项；
- 样本中的模板路标、说教、营销、答辩腔只能进入 `DO_NOT_AMPLIFY`，不能因高频进入 PREFER；
- 现有 `scan_humanize_chinese.py` 可作为风格信号集成候选，但必须先核对真实输出合同、版本绑定和 protected 行为，不能只凭脚本名接入。

## 9. DEFAULT Profile 的精确定义

DEFAULT 表示“没有足量、可安全归属于作者的证据”，不是一种推断出的个人风格。

```json
{
  "profile_kind": "DEFAULT",
  "validation_status": "PASS",
  "confidence": "DEFAULT",
  "features": [],
  "negative_controls": [],
  "defaults": {
    "use_scene_default": true,
    "scene": "RESEARCH",
    "reason": "BELOW_300_AUTHOR_CHARS",
    "disclosure_required": true,
    "personal_voice_claim_allowed": false
  }
}
```

DEFAULT 的强制语义：

- `features=[]`，不得携带个人偏好或 scene override；
- `confidence=DEFAULT`，不能写 LOW；
- `personal_voice_claim_allowed=false`；
- 消费端从当前 Skill 的 `scene_default_policy_sha256` 加载场景默认，不把默认规则复制成“作者特征”；
- 交付必须披露：“未提供足量、可归属于作者本人的写作样本；本次使用对应场景的默认声线，不声称复现作者个人文风。”
- “没有传 profile 文件”和“显式 DEFAULT Profile”分别记录为 `profile_source=ABSENT` 与 `profile_source=EXPLICIT_DEFAULT`，两者都不能声称个人声线；
- 明确无样本或清洁样本不足 300 字可 `DEFAULT/PASS`；作者归属冲突、保护区无法切分、输入变化或 manifest 不完整必须 `REVIEW/FAIL`，不能用 DEFAULT 掩盖。

场景默认保持正式合同语义：COURSE 自然讲解并选择性展开；MODELING 务实直接且对象/结果靠前；RESEARCH 克制正式、论证有主次且不过度闭合；GENERAL 保留原文正式程度，仅清机械模板和均匀节奏。

## 10. 最小 CLI

建议新增两个独立生产入口；builder 不自证通过：

### 10.1 构建

```powershell
python scripts/build_humanize_voice_profile.py `
  --sample-spec voice_samples.spec.json `
  --allowed-root <workspace-root> `
  --profile-id author-style-001 `
  --scene AUTO `
  --manifest-out voice_sample_manifest.json `
  --output voice_profile.json `
  --format json
```

默认在清洁样本不足时生成显式 DEFAULT。建议参数：

- `--max-file-bytes`、`--max-total-bytes`、`--max-units`：资源上限；
- `--source-date-epoch`：需要可重现元数据时由调用方传入；时间戳不参与声线判断；
- `--role-policy`、`--feature-registry`：显式版本化策略；
- 不提供 `--trust-author` 一类会伪造身份验证的开关。

### 10.2 独立验证/重建

```powershell
python scripts/validate_humanize_voice_profile.py `
  voice_profile.json `
  --manifest voice_sample_manifest.json `
  --allowed-root <workspace-root> `
  --rebuild-evidence `
  --format json
```

validator 必须从冻结源文件重建 role map、author view、dedup clusters、总体阈值和逐 feature evidence，不信任 manifest 中的派生计数。

### 10.3 消费端扩展

在核对现有接口后，可为 `validate_humanize_output.py` 增加类似参数：

```powershell
--voice-profile voice_profile.json `
--voice-manifest voice_sample_manifest.json `
--require-voice-profile-status PASS
```

消费结果至少记录 `profile_sha256`、`manifest_sha256`、`profile_kind`、`confidence`、实际应用的 feature_keys、因保护/场景/权限被抑制的 feature_keys，以及 `personal_voice_claim_allowed`。

### 10.4 退出码

| 退出码 | 状态 | 例子 |
|---|---|---|
| 0 | PASS | PERSONAL 通过；或样本确实不足而安全生成 DEFAULT |
| 1 | FAIL | schema/hash 不一致、路径越界、保护区证据泄漏、TOCTOU、伪造计数 |
| 2 | REVIEW | 作者归属不明、模板边界不明、语义 feature 无可重建 extractor |

`DEFAULT/PASS` 只能表示安全回退；不能覆盖请求样本中已发现的完整性失败。

## 11. P0 攻击面

| P0 攻击 | 必须拦截的结果 | 最小防线 |
|---|---|---|
| 路径穿越、符号链接/结点重解析越界 | 读取工作根外样本 | `allowed_root`、realpath/文件身份核对、no-follow、普通文件限定；越界 FAIL |
| TOCTOU 样本替换 | manifest 验证旧字节，Profile 发布新字节 | 一次性冻结、发布前重新核对文件身份与 hash；变化 FAIL |
| Manifest/Profile 混搭或旧证据重放 | A 样本的 Profile 绑定 B manifest | 双向 SHA-256、policy/registry hash、revision ancestry；不匹配 FAIL |
| 保护区注入 | 引语、公式、代码、题干或 OCR 被学成作者习惯 | 完整文件先分类、保护优先、逐 anchor overlap 检查；命中 FAIL，边界不明 REVIEW |
| 精确/近重复膨胀 | 复制段落把 200 字伪装成 5000 字或制造 3 次 feature | exact hash + 5-gram 近重复 cluster；每 cluster 只计一次 |
| 多作者/身份冒充 | 第三方文本被声明成个人声线 | origin 必填、未知归属排除；固定 `identity_verified=false`，不作身份推断 |
| 模型输出回灌 | Humanize 输出循环强化为“作者习惯” | `MODEL_GENERATED` 永久排除；只有用户确认且实际采用才允许 `USER_CONFIRMED_ADOPTED` |
| 样本文本 prompt injection | 样本中的“忽略规则/执行命令”改变构建器 | 文本只作为数据；registry 枚举值；Profile 禁止自由指令文本、代码块和控制字符 |
| 样本句泄漏/指纹化 | evidence 或 preferred phrase 复制独特原句 | 证据仅 offsets/hash；LEXEME 连续汉字上限 7；8+ 连续唯一重合 REVIEW/FAIL |
| 场景投毒 | 课堂口头禅迁移到研究正文 | feature scope、HIGH 才允许子档案、场景自身阈值；跨场景默认不迁移 |
| 高频缺陷合法化 | 模板/营销/答辩腔因高频变成 PREFER | style signal 负控、`DO_NOT_AMPLIFY` 优先、accepted feature 与负控冲突 FAIL |
| DEFAULT 混淆 | 无样本却声称保留个人风格 | DEFAULT 强制空 features、披露、`personal_voice_claim_allowed=false` |
| JSON/hash 歧义 | 重复 key、浮点/Unicode/换行差异产生不同解释 | JCS、严格 UTF-8、拒绝重复 key/非有限数、完整域分离 hash |
| 资源耗尽 | 巨型文件、海量段落、O(n²) 去重拖垮构建 | 文件/总量/unit 上限，MinHash/LSH 候选化，超限 REVIEW/FAIL |
| 版本回滚/静默覆盖 | 旧 Profile 覆盖新偏好或无审计更新 | immutable artifact、revision、`supersedes_profile_sha256`、显式 pin 当前 profile hash |

P0 发布门应包含至少这些负向用例；任何一个能产生 `PERSONAL/PASS` 都应阻止上线。

## 12. 最小落地顺序

1. 冻结 `voice-profile/v1`、`voice-sample-manifest/v1` JSON Schema 与 JCS/hash 规范；
2. 实现 builder：路径闭合、快照、角色图、去保护、unitizer、dedup、manifest 和 DEFAULT；
3. 实现独立 validator，从源字节重建所有派生计数和 feature evidence；
4. v1 只开放可确定性重建的 feature registry，不急于发布语义型自由描述；
5. 将 profile/manifest hash 接入输出验证记录，但不让 Voice PASS 覆盖保护、言语行为或文风门；
6. 通过 P0 负向矩阵后，再开放 HIGH 分场景子档案与更新链。

该方案的核心取舍是：Profile 宁可少而可证，也不把样本文本、自由总结或总字数包装成个人声线证据。DEFAULT 是显式、可审计的安全结果，`NO_CHANGE` 仍应是应用 Profile 后的合法动作。
