# 批次 058 整改复审记录

生成时间：2026-06-23

## 0. 执行边界

- 批次范围：全局 `#848-852`
- 源码范围：`elegantbook2.tex:39143-39306`
- PDF 复核页：物理页 `615-617`
- 当前 PDF 页数：`740`
- 本轮主题：第 7 章 B 卷计算题 7.30-7.34
- 本轮复核口径：先逐题核验敛散性、Gauss 公式、降阶法、链式求导和极坐标积分的数学正确性与步骤完整性；再按“接近 `3/4\textwidth` 才拆”的阈值复核行内/行间公式。

## 1. 已完成的主要整改

- `#848`：将有理化分解和级数拆分改为独立行间公式，明确第一部分由交错级数判别法收敛、第二部分为发散调和级数，从而原级数发散且部分和趋于 `-\infty`。
- `#851`：补足二元函数链式求导的中间步骤，将 `yg(v,w)` 对 `x` 求导、再对 `y` 求导的主干拆成 aligned 结构，避免长行内公式挤压。
- `#852`：将极坐标区域描述拆成较短的行内句式，保留最终积分骨架为行间公式。
- `#849`、`#850`：逐题复核后计算链条和结论正确，未发现需改正文内容的问题。

## 2. 逐题内容复核摘要

| 全局号 | 复核结论 |
| ---: | --- |
| 848 | 有理化得 \(\frac{(-1)^n}{\sqrt n+(-1)^n}=\frac{(-1)^n\sqrt n}{n-1}-\frac1{n-1}\)。前一项级数按交错级数判别法收敛，后一项为调和级数并发散到 \(+\infty\)，故原级数发散到 \(-\infty\)，结论正确。 |
| 849 | 第二类曲面积分取 \(P=x^2,Q=2y^2,R=3z^2-4x^2y^2\)，散度为 \(2x+4y+6z\)。圆锥体关于 \(x,y\) 对称，前两项积分为零；柱坐标区域 \(0\le z\le2,0\le r\le z,0\le\theta\le2\pi\)，得 \(6\pi\int_0^2z^3\,dz=24\pi\)，答案正确。 |
| 850 | 令 \(y=v(x)e^x\)，代入后 \(v\) 项系数相消，得到 \((2x-1)v''+(2x-3)v'=0\)。设 \(w=v'\) 后积分得 \(w=C(2x-1)e^{-x}\)，进一步 \(v=-C(2x+1)e^{-x}+C_1\)，故通解 \(y=C_1e^x+C_2(2x+1)\) 正确。 |
| 851 | 记 \(u=y/x,v=x,w=x/y\)。先求 \(z_x=f(u)-u f'(u)+yg_1(v,w)+g_2(v,w)\)，再对 \(y\) 求偏导，得到 \(-\frac{y}{x^2}f''(y/x)+g_1(x,x/y)-\frac{x}{y}g_{12}(x,x/y)-\frac{x}{y^2}g_{22}(x,x/y)\)。链式法则、下标记号和混合偏导写法一致。 |
| 852 | 区域为上半单位圆盘，极坐标为 \(0\le r\le1,0\le\theta\le\pi\)，且 \(x^2+y^2=r^2,d\sigma=r\,dr\,d\theta\)。积分为 \(\int_0^\pi\int_0^1r^3\,dr\,d\theta=\pi/4\)，答案正确。 |

## 3. 公式排版复核

- 重建索引：`python solution_quality_audit/build_solution_index.py`
  - `total_solutions = 1322`
  - `long_inline_flagged = 141`
  - `short_display_flagged = 795`
- 本批索引结果：
  - `#848`: `inline_long_count = 0`, `display_count = 2`, `short_display_count = 2`
  - `#849`: `inline_long_count = 0`, `display_count = 2`, `short_display_count = 2`
  - `#850`: `inline_long_count = 0`, `display_count = 0`, `short_display_count = 0`
  - `#851`: `inline_long_count = 0`, `display_count = 6`, `short_display_count = 5`
  - `#852`: `inline_long_count = 0`, `display_count = 1`, `short_display_count = 1`
- `#848` 的两个 display 是敛散性判断主干，不是低地位小公式。
- `#849` 的 Gauss 公式与三重积分计算、`#851` 的链式法则主干、`#852` 的极坐标积分骨架均保留为 display；短代入和区域描述尽量压回或保留在行内。
- 本批未保留接近 `3/4\textwidth` 的拥挤行内公式。

## 4. PDF 版面复核

已渲染并目检：

- `tmp/pdfs/batch_058_848_852/page-615.png`
- `tmp/pdfs/batch_058_848_852/page-616.png`
- `tmp/pdfs/batch_058_848_852/page-617.png`

检查结果：

- `page-615`：`#848` 的级数分解和结论层次清楚，`#849` 开始位置自然，无长行内公式压边。
- `page-616`：`#849-852` 主体显示正常；降阶法、链式求导和极坐标积分均无重叠、错位或异常留白。
- `page-617`：`#852` 结尾积分排版正常，后续证明题自然衔接。

## 5. 验证记录

- 编译：`latexmk -xelatex -interaction=nonstopmode -halt-on-error elegantbook2.tex`
  - 结果：成功生成 `elegantbook2.pdf`
- 日志扫描：`Overfull \hbox|Underfull \hbox|LaTeX Warning|Package .* Warning|Undefined control sequence|Fatal|^!`
  - 结果：无输出
- PDF 页数：`740`

## 6. 放行结论

批次 `#848-852` 可放行。放行依据包括：五题的计算结论和推导主线均已人工复核；`#848/#851/#852` 的压缩和拥挤问题已处理；未把低地位短公式机械拆成 display；PDF 渲染页 `615-617` 无压边、错位、重叠或异常留白。
