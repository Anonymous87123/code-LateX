# 批次 056 整改复审记录

生成时间：2026-06-23

## 0. 执行边界

- 批次范围：全局 `#838-842`
- 源码范围：`elegantbook2.tex:38910-39014`
- PDF 复核页：物理页 `612-613`
- 当前 PDF 页数：`740`
- 本轮主题：第 7 章 B 卷单项选择题 7.20-7.24
- 本轮复核口径：先核验选项真假、积分区域与方向、幂级数半径；再处理长句和长行内公式，避免把短定义机械改成行间公式。

## 1. 已完成的主要整改

- `#838`：拆开 A、B、D 三个选项的判定说明，明确 B 项使用方向导数公式时隐含“函数在该点可微”的常用语境。
- `#842`：将新旧系数根值的比较单独列出，说明除以 \(n(n-1)\) 不改变指数级增长速度，因此收敛半径不变。
- `#839-841`：逐题复核后结论正确，未发现需改正文内容的问题。

## 2. 逐题内容复核摘要

| 全局号 | 复核结论 |
| ---: | --- |
| 838 | A 项由连续函数与绝对值函数复合仍连续，正确。B 项在可微语境下方向导数为梯度在方向上的投影，正确。D 项是一阶偏导在邻域存在并在点处连续推出可微的充分判据，正确。C 项漏掉偏导数存在条件，反例 \(f(x,y)=\sqrt{x^2+y^2}\) 在原点取极小值但偏导数不能按零处理，故不正确的是 C。 |
| 839 | \(z_x=2x/(1+x^2+y^2)\)，\(z_y=2y/(1+x^2+y^2)\)。代入 \((1,2)\) 得 \(z_x=1/3,\ z_y=2/3\)，全微分为 \(\frac13\,\mathrm dx+\frac23\,\mathrm dy\)，选 D 正确。 |
| 840 | 投影为单位圆盘，竖向范围为 \(x^2+y^2\le z\le1\)。D 项给出完整投影和正确上下限；B 项不能因第一象限乘 \(4\) 处理任意函数，A 上下限反向，C 下界错误，故选 D 正确。 |
| 841 | 对逆时针正向，Green 公式给出 \(\iint_D(Q_x-P_y)\,\mathrm d\sigma=-18\pi\)。题设为顺时针方向，方向相反后积分变号，结果 \(18\pi\)，选 D 正确。 |
| 842 | 原收敛域为 \([-8,8]\)，半径 \(R_0=8\)。新系数 \(b_n=a_n/[n(n-1)]\)，且 \(\sqrt[n]{n(n-1)}\to1\)，所以 \(\limsup\sqrt[n]{|b_n|}=\limsup\sqrt[n]{|a_n|}\)，收敛半径仍为 \(8\)，选 C 正确。 |

## 3. 公式排版复核

- 重建索引：`python solution_quality_audit/build_solution_index.py`
  - `long_inline_flagged` 从 `148` 降为 `146`
- 本批索引结果：
  - `#838`: `inline_long_count = 0`, `display_count = 0`, `short_display_count = 0`
  - `#839`: `inline_long_count = 0`, `display_count = 0`, `short_display_count = 0`
  - `#840`: `inline_long_count = 0`, `display_count = 1`, `short_display_count = 1`
  - `#841`: `inline_long_count = 0`, `display_count = 1`, `short_display_count = 1`
  - `#842`: `inline_long_count = 0`, `display_count = 1`, `short_display_count = 1`
- `#838` 通过拆句清除长行风险，未增加不必要 display。
- `#842` 的 display 是半径判定的核心根值公式，地位足够；短定义如 \(R_0=8\)、\(b_n=a_n/[n(n-1)]\) 仍保持行内。

## 4. PDF 版面复核

已渲染并目检：

- `tmp/pdfs/batch_056_838_842/page-612.png`
- `tmp/pdfs/batch_056_838_842/page-613.png`

检查结果：

- `page-612`：B 卷章节入口、`#838` 逐项判断和 `#839` 全微分计算显示正常。
- `page-613`：`#840` 三重积分选项、`#841` Green 公式方向变号、`#842` 根值判定显示清楚，无长行挤压或压边。

## 5. 验证记录

- 编译：`latexmk -xelatex -interaction=nonstopmode -halt-on-error elegantbook2.tex`
  - 结果：成功生成 `elegantbook2.pdf`
- 日志扫描：`Overfull \hbox|Underfull \hbox|LaTeX Warning|Package .* Warning|Undefined control sequence|Fatal|^!`
  - 结果：无输出
- PDF 页数：`740`

## 6. 放行结论

批次 `#838-842` 可放行。放行依据包括：五题选项判定、计算方向和半径结论均已核对；长行内候选清零；新增 display 只用于核心根值判定；PDF 渲染页 `612-613` 无拥挤、错位、压边或异常留白。
