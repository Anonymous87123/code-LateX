已完成只读复核，未修改任何文件。

**总体结论**
- `solution_quality_audit/summary.json:2`、`solution_quality_audit/solution_index.csv:1`、`solution_quality_audit/solution_quality_ledger.md:1` 可以作为“初稿台账”进入人工逐题审校阶段。
- 但它不能直接作为“最终整改台账”或“自动放行依据”：目前强在定位与排版/跳步启发式，弱在数学正确性、方法口径一致性、未超阈值但视觉压缩的公式识别。
- 建议先补充少量人工审校字段，再从全书第 1 个 `solution` 开始小批量校准标准。

**字段充分性判断**
- **过度压行/排版风险：部分足够。** 已有 `inline_long_count`、`inline_long_lines`、`short_display_count`、`short_display_samples`，能抓 170 字以上长行和短 display；但抓不到 170 字以下的复杂公式、行内嵌套分式、行内长 Taylor/级数/积分链。
- **跳步推导：部分足够。** 已有 `jump_keywords` 和 `defect_flags`，能把“可得、直接、于是、计算得”等列入人工队列；但无法判断该“直接”是否合理，也抓不到无关键词但实际跳步的题。
- **方法口径不一致：不足。** 目前只有 `risk_tags`，没有 `expected_method`、`method_used`、`method_mismatch_reason`。例如曲线积分题应优先 Green/Stokes/路径无关还是参数化，台账现在不能自动判断。
- **答案/演算错误：不足。** 没有 `final_answer`、`normalized_answer`、`independent_check`、`domain_condition`、`orientation_check`、`convergence_interval` 等字段，无法支撑系统发现符号、常数、端点、方向、收敛域错误。

**抽查发现**
- 首题 `elegantbook2.tex:1273` 已被标记，确实存在多段长等式链和“直接/可得”语境，适合人工复核；但其中部分“直接”前后有解释，说明关键词标记会有假阳性。
- 未标记样本 `elegantbook2.tex:1397` 排版相对规范，说明 `AUTO_INDEXED_NO_HEURISTIC_FLAG` 不等于安全，只能代表未触发当前规则。
- 尾部级数证明 `elegantbook2.tex:40158` 将 Taylor、比较判别、结论压在很少行内，属于“即使不全靠 170 字阈值，也应拆 display”的典型。
- 级数/函数项级数样本 `elegantbook2.tex:40181` 多个关键不等式、逐项积分、交错级数估计都偏压缩，容易漏掉“定理适用条件”和“绝对/一致收敛”说明。
- Stokes/曲面积分样本 `elegantbook2.tex:39477` 这类题必须检查方向、法向、边界正向，当前台账只能打标签，不能验算方向约定是否正确。

**建议补充字段**
- `defect_categories_manual`: `layout` / `jump` / `method` / `math` 多选。
- `severity`: `A_必须改` / `B_建议改` / `C_可保留`。
- `problem_type` 与 `subtype`: 如 `曲线积分-第二类-闭曲线`、`微分方程-一阶线性`、`Fourier-半区间正弦级数`。
- `expected_method_ref`: 前文口径或章节锚点，如 Green、Gauss、Stokes、Lagrange、Rayleigh、M-test。
- `method_used`、`method_mismatch`、`method_exception_reason`。
- `final_answer`、`normalized_answer`、`independent_check_result`。
- `condition_check`: 定义域、积分常数、方向、边界、收敛域、端点、参数范围。
- `layout_decision`: `split_align` / `display_keep` / `inline_ok` / `cases_needed`。
- `review_status`: `待审` / `已改待复核` / `复核通过` / `退回`。
- `batch_id`、`reviewer_note`、`release_gate`.

**统一整改标准**
- **必须行间公式：** 两个以上等号的推导链；含 `\int`、`\iint`、`\iiint`、`\sum`、`\lim`、矩阵、行列式、Jacobian、Taylor 展开、Fourier 系数、微分方程通解、Green/Gauss/Stokes 转换的主计算。
- **可行内公式：** 单个短定义、变量替换、简单结论，如 `令 \(t=x^2+1\)`、`\(\lambda_{\min}\le f\le\lambda_{\max}\)`；但不得连续塞多个逻辑步骤。
- **曲线/曲面积分：** 先判类型、方向、奇点；闭曲线优先 Green，闭曲面通量优先 Gauss，边界线积分优先 Stokes；非闭曲面先考虑补面再扣除，必须写清法向/正向。
- **级数/Fourier：** 数项级数先判正项/交错/任意项；函数项级数必须说明一致收敛依据；幂级数写半径和端点；Fourier 先定周期、延拓方式、系数归一化和间断点取左右极限平均。
- **微分方程：** 先分类，再选可分离、齐次、一阶线性、恰当方程、积分因子、特征根或常数变易；通解必须保留常数，必要时注明定义区间。
- **极值：** 无约束题用驻点加 Hessian/二阶微分；约束题用 Lagrange；紧致区域题必须查内部与边界；二次型球面题可用 Rayleigh/谱定理，但应说明与特征值极值口径一致。
- **重积分：** 先写区域或投影，再换序/换元；极坐标、柱坐标、球坐标必须写 Jacobian；利用对称性前必须说明区域和被积函数奇偶性。

**分批修改建议**
- **校准批：** 全局 `1–10`，即从 `elegantbook2.tex:1273` 开始的第一节有理分式分解题。目标是统一“模法/多项式逆元”的排版、补步和行间公式模板。
- **第一章后续：** `11–155` 按小节切，每批约 `15–25` 题；根式和三角代换题可缩小到 `10–15` 题。
- **章节批次：** 微分方程 `156–315`，多元微分 `316–555`，重积分 `556–643`，曲线曲面积分 `644–763`，级数 `764–818`，真题 `819–1322` 按试卷或题型切。
- **高风险批：** 曲线/曲面积分、Fourier、极值、重积分换元、微分方程综合题每批不宜超过 `10–15` 个 solution。
- **放行条件：** 每题四类缺陷均有人工结论；长行/短 display 均有保留或整改理由；数学答案独立验算通过；方法口径与前文一致或注明例外；无新增压行；批次复核人确认通过。