# 批次 061 整改复审记录

生成时间：2026-06-23

## 0. 执行边界

- 批次范围：全局 `#863-867`
- 源码范围：`elegantbook2.tex:39551-39647`
- PDF 复核页：物理页 `619-621`
- 当前 PDF 页数：`740`
- 本轮主题：2007--2008 A 卷选择题 7.45-7.48、计算题 7.49
- 本轮复核口径：先核验选择题判别依据、反例排除、线性方程特解性质和隐函数代入计算；再按长行内公式标准处理计算主干。

## 1. 已完成的主要整改

- `#865`：补充 A、B、C 三个选项不能保证收敛的具体反例，尤其为 B 项给出偶数项反例，避免只凭“没有单调性”作不充分说明。
- `#867`：将直接解出 \(z\)、代入 \(u\) 后的表达式，以及 \(u_y,(u_y)_x\) 的计算拆为 display，消除长行内公式并补足计算层次。
- `#863`、`#864`、`#866`：逐题复核后内容正确，未发现需改正文内容的问题。

## 2. 逐题内容复核摘要

| 全局号 | 复核结论 |
| ---: | --- |
| 863 | 区域 \(D\) 为 \(0\le x\le\pi,0\le y\le x\)。在该区间 \(\sqrt{1-\cos^2x}=|\sin x|=\sin x\)，积分化为 \(\int_0^\pi x\sin x\,dx=\pi\)，故选 D 正确。 |
| 864 | \(\sum \sin(n\alpha)/n^2\) 由比较判别法绝对收敛；\(\sum 1/\sqrt n\) 是 \(p=1/2\) 的发散 \(p\) 级数。因此原级数等于收敛级数减去发散到 \(+\infty\) 的级数，必发散且与 \(\alpha\) 无关，选 B 正确。 |
| 865 | D 项中 \(0\le a_n^2<1/n^2\)，所以 \(\sum a_n^2\) 收敛，进而 \(\sum(-1)^na_n^2\) 绝对收敛。A 可取 \(a_n=1/(2n)\) 发散；B 可取 \(a_{2k}=1/(4k),a_{2k-1}=0\) 发散；C 仍可取 \(a_n=1/(2n)\) 使 \(\sum\sqrt{a_n}\) 发散。选 D 的论证完整。 |
| 866 | 设线性算子 \(L[y]=y''+ay'+by\)。若 \(L[y_1]=L[y_2]=f(x)\)，则 \(L[y_1-y_2]=0\)，所以差是对应齐次方程解；而 \(L[y_1+y_2]=2f(x)\)，一般不是非齐次或齐次方程解。选 D 正确。 |
| 867 | 由约束得 \(z=-x-y\)，代入 \(u=x+yz\) 得 \(u=x-xy-y^2\)。先对 \(y\) 再对 \(x\) 求偏导，\(u_y=-x-2y,(u_y)_x=-1\)，故 \(\partial^2u/\partial x\partial y=-1\) 正确。 |

## 3. 公式排版复核

- 重建索引：`python solution_quality_audit/build_solution_index.py`
  - `total_solutions = 1322`
  - `long_inline_flagged = 139`
  - `short_display_flagged = 801`
- 本批索引结果：
  - `#863`: `inline_long_count = 0`, `display_count = 1`, `short_display_count = 1`
  - `#864`: `inline_long_count = 0`, `display_count = 0`, `short_display_count = 0`
  - `#865`: `inline_long_count = 0`, `display_count = 0`, `short_display_count = 0`
  - `#866`: `inline_long_count = 0`, `display_count = 0`, `short_display_count = 0`
  - `#867`: `inline_long_count = 0`, `display_count = 2`, `short_display_count = 2`
- `#863` 的 display 是积分计算主干；`#867` 的两个 display 是代入化简与混合偏导主干，均不是低地位短公式。
- 本批未保留接近 `3/4\textwidth` 的拥挤行内公式。

## 4. PDF 版面复核

已渲染并目检：

- `tmp/pdfs/batch_061_863_867/page-619.png`
- `tmp/pdfs/batch_061_863_867/page-620.png`
- `tmp/pdfs/batch_061_863_867/page-621.png`

检查结果：

- `page-619`：`#863` 的积分计算清楚，页底过渡到 `#864` 正常。
- `page-620`：`#864-866` 选择题判别依据显示正常；`#865` 新增反例未造成压边；`#867` 的代入与求偏导 display 层次清楚。
- `page-621`：作为后续内容边界页检查，未见由本批修改造成的异常错位、拥挤或大块留白。

## 5. 验证记录

- 编译：`latexmk -xelatex -interaction=nonstopmode -halt-on-error elegantbook2.tex`
  - 结果：成功生成 `elegantbook2.pdf`
- 日志扫描：`Overfull \hbox|Underfull \hbox|LaTeX Warning|Package .* Warning|Undefined control sequence|Fatal|^!`
  - 结果：无输出
- PDF 页数：`740`

## 6. 放行结论

批次 `#863-867` 可放行。放行依据包括：五题的结论、反例和计算链条均已人工复核；`#865` 的选项排除补充完整；`#867` 的长行内计算主干已拆为必要 display；PDF 渲染页 `619-621` 无压边、错位、重叠或异常留白。
