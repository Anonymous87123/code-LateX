# 批次 060 整改复审记录

生成时间：2026-06-23

## 0. 执行边界

- 批次范围：全局 `#858-862`
- 源码范围：`elegantbook2.tex:39449-39543`
- PDF 复核页：物理页 `618-620`
- 当前 PDF 页数：`740`
- 本轮主题：2007--2008 A 卷填空题 7.40-7.43、选择题 7.44
- 本轮复核口径：先核验换序积分、幂级数端点、Laplace 计算、约束极值和距离最小化；再处理实际渲染中压缩过度的行内计算。

## 1. 已完成的主要整改

- `#860`：补出梯度与二阶偏导两层计算，并将 \(u_x,u_y\) 与 \(u_{xx},u_{yy}\) 分别列为 display，消除原来一段内连续塞入多个分式的拥挤问题。
- `#861`：将由约束化为一元二次函数并配方的主干公式拆为 display，使最大值判断更清楚。
- `#858`、`#859`、`#862`：逐题复核后内容正确；既有 display 或行内公式位置可接受，未作正文修改。

## 2. 逐题内容复核摘要

| 全局号 | 复核结论 |
| ---: | --- |
| 858 | 原积分区域为 \(0\le x\le2,\ x\le y\le2\)，换序后为 \(0\le y\le2,\ 0\le x\le y\)。积分化为 \(\int_0^2 ye^{-y^2}\,dy=(1-e^{-4})/2\)，并已保留题面校勘说明，结论正确。 |
| 859 | 令 \(t=(x-2)/4\)，原级数为 \(\sum t^n/n\)，半径为 1。端点 \(x=-2\) 时为交错调和级数收敛，\(x=6\) 时为调和级数发散，故收敛域 \([-2,6)\) 正确。 |
| 860 | \(u=\ln\sqrt{x^2+y^2}=\frac12\ln(x^2+y^2)\)，在 \((x,y)\ne(0,0)\) 上有 \(u_x=x/(x^2+y^2),u_y=y/(x^2+y^2)\)。继续求得 \(u_{xx}=(y^2-x^2)/(x^2+y^2)^2,u_{yy}=(x^2-y^2)/(x^2+y^2)^2\)，相加为 0，通常函数意义下结论正确。 |
| 861 | 由 \(x+y=1\) 令 \(y=1-x\)，得 \(z=x(1-x)=-(x-\frac12)^2+\frac14\)。二次函数开口向下，最大值在 \(x=y=1/2\) 处取得，极大值 \(1/4\) 正确。 |
| 862 | 抛物线点写为 \((y^2/4,y)\)，到直线距离由 \(|x-y+4|/\sqrt2\) 给出。代入后 \(x-y+4=(y-2)^2/4+3>0\)，最小时 \(y=2,x=1\)，最近点为 \((1,2)\)，选 C 正确。 |

## 3. 公式排版复核

- 重建索引：`python solution_quality_audit/build_solution_index.py`
  - `total_solutions = 1322`
  - `long_inline_flagged = 140`
  - `short_display_flagged = 800`
- 本批索引结果：
  - `#858`: `inline_long_count = 0`, `display_count = 1`, `short_display_count = 1`
  - `#859`: `inline_long_count = 0`, `display_count = 0`, `short_display_count = 0`
  - `#860`: `inline_long_count = 0`, `display_count = 2`, `short_display_count = 2`
  - `#861`: `inline_long_count = 0`, `display_count = 1`, `short_display_count = 1`
  - `#862`: `inline_long_count = 0`, `display_count = 0`, `short_display_count = 0`
- `#860` 的两个 display 是 Laplace 计算骨架，`#861` 的 display 是约束极值的配方主干，均不是低地位小公式。
- 本批未保留接近 `3/4\textwidth` 的拥挤行内公式。

## 4. PDF 版面复核

已渲染并目检：

- `tmp/pdfs/batch_060_858_862/page-618.png`
- `tmp/pdfs/batch_060_858_862/page-619.png`
- `tmp/pdfs/batch_060_858_862/page-620.png`

检查结果：

- `page-618`：`#858` 换序积分和 `#859` 端点判别显示正常，未见公式压边。
- `page-619`：`#860` 的梯度与二阶偏导分层后清晰；`#861` 配方显示不拥挤；`#862` 距离最小化过程行内/行间比例合适。
- `page-620`：作为后续内容边界页检查，未见由本批修改造成的异常错位、拥挤或大块留白。

## 5. 验证记录

- 编译：`latexmk -xelatex -interaction=nonstopmode -halt-on-error elegantbook2.tex`
  - 结果：成功生成 `elegantbook2.pdf`
- 日志扫描：`Overfull \hbox|Underfull \hbox|LaTeX Warning|Package .* Warning|Undefined control sequence|Fatal|^!`
  - 结果：无输出
- PDF 页数：`740`

## 6. 放行结论

批次 `#858-862` 可放行。放行依据包括：五题计算结论和逻辑链条均已人工复核；`#860/#861` 的拥挤行内主干已按必要性拆为 display；短定义、端点结论和选择题答案仍保留行内；PDF 渲染页 `618-620` 无压边、错位、重叠或异常留白。
