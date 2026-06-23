# 批次 022 整改复审记录

生成时间：2026-06-23

## 0. 执行边界

- 批次范围：全局 `#674-682`
- 源码范围：`elegantbook2.tex:29714-30183`
- PDF 复核页：物理页 `472-480`，对应印刷页 `422-430`
- 本批主题：平面 Green 第二公式应用、调和函数 Poisson 型公式、平面流量通量形式、Green 面积公式、奇点挖洞法、非单连通路径无关性判断、Stokes 公式换面与定向。
- 本轮原则：内容复核与排版复核并重。先核对奇点、边界取向、外法向、Green 符号链、Stokes 右手定则、旋度、面积和最终结果，再按用户指定的 `3/4\textwidth` 口径处理真正过长的行内公式。硬阈值为 `52.5/70` 折算单位，`45-52.5` 只人工复核，不机械拆分。

## 1. 已完成的主要整改

- `#674`：把调和函数公式的适用点明确为 `D` 的任意内点；在解答中补齐 `P_0` 为内点、挖小圆区域 `D_\varepsilon`、边界分解 `\partial D_\varepsilon=\Gamma^+-C_\varepsilon^+`，并说明内边界的外法向指向圆心，从而保证小圆极限符号正确。
- `#676`：椭圆题补充 `a,b>0`；将逆时针参数、微分和面积代入分段写清，结果 `S=\pi ab`。
- `#678`：把题设从笼统“包含原点”改成“原点位于内部但不在曲线上”；解答按挖洞法写明环域、内边界方向、`P,Q,Q_x-P_y` 和与小圆积分等值的步骤，避免误把奇点吞进 Green 公式。
- `#679`：同样修正原点条件；补齐 `Q_x-P_y=0` 的偏导计算、环域边界 `C^+-C_\varepsilon^+`、小圆参数化和非单连通导致路径无关性失效的结论链。另修正英文标题贴连，使 PDF 中显示为“例题 5.31  Green ...”。
- `#680`：将第一卦限平面片题改为直接 Stokes 解法，写出 `\nabla\times\vec F=(-2z,-2x,-2y)`、上侧法向 `\frac1{\sqrt3}(1,1,1)`、三角形面积 `\frac{\sqrt3}{2}`，结果 `W=-1`。
- `#681`：把“从 `x` 轴正向看逆时针”翻译为法向的 `x` 分量为正，配合 `\nabla\times(y,z,x)=(-1,-1,-1)` 和圆盘面积 `\pi a^2`，结果 `-\sqrt3\pi a^2`。
- `#682`：把“从 `z` 轴正向看逆时针”翻译为法向的 `z` 分量为正；写出旋度 `(-2,-2,-2)`、圆盘面积 `\pi`，结果 `-2\sqrt3\pi`。另修正英文标题贴连，使 PDF 中显示为“例题 5.35  Stokes 换面法”。

## 2. 逐题内容复核摘要

| 全局号 | 复核结论 |
| ---: | --- |
| 674 | `\Delta\ln r=0` 的一、二阶偏导链完整；第二问未直接在含奇点区域套公式，而是先挖去 `P_0` 的小圆。内边界外法向取向、`\partial/\partial n=-\partial/\partial r`、小圆积分趋于 `-2\pi u(x_0,y_0)`，最终外边界积分给出 `2\pi u(x_0,y_0)`，符号正确。 |
| 675 | 平面流量题的正向边界与外法向 `\vec n=(dy/ds,-dx/ds)` 对应正确，边界通量 `\oint_C P\,dy-Q\,dx` 与区域散度积分 `\iint_D(P_x+Q_y)\,dxdy` 一致。 |
| 676 | 椭圆参数方向为逆时针，`xdy-ydx=ab(\cos^2t+\sin^2t)dt`，面积结果 `\pi ab` 正确。 |
| 677 | `P=2xy+\cos x,\ Q=x^2+\sin y`，有 `Q_x=P_y=2x`，定义域全平面无奇点，闭曲线可直接用 Green 公式，积分为 `0`。 |
| 678 | 经典奇点积分中原点已被小圆挖掉，环域上 `Q_x-P_y=0`；内边界在正向边界中体现为 `-C_\varepsilon^+`，最终等于小圆逆时针积分 `2\pi`。 |
| 679 | 先证去原点平面上 `Q_x-P_y=0`，再用挖洞法得闭曲线积分 `2\pi`；第三问明确指出去原点平面非单连通，因此不能由局部 `Q_x=P_y` 推出全局路径无关。 |
| 680 | Stokes 公式、旋度、上侧法向和三角形面积均核算通过，结论 `-1` 与方向约定一致。 |
| 681 | 观察方向到法向的翻译核算通过；平面过球心，交线圆盘半径为 `a`，面积 `\pi a^2`，结果 `-\sqrt3\pi a^2` 正确。 |
| 682 | 观察方向到法向的翻译核算通过；旋度点乘法向为 `-2\sqrt3`，单位球大圆圆盘面积为 `\pi`，结果 `-2\sqrt3\pi` 正确。 |

本轮复核未发现本批残留的计算错误、结论偏差、奇点误用、定向错误或与本章 Green/Stokes 方法口径冲突的问题。

## 3. 公式排版复核

按校准后的折算扫描源码范围 `29714-30183`：

- `inline_math_candidates_ge45 = 1`
- `hard_ge52_5 = 0`
- 本批 `#674-682` 的 `inline_long_count` 均为 `0`

唯一 near 项位于 `elegantbook2.tex:30020`，为 Green 面积证明中的短推导链：

```tex
\displaystyle \oint_C x\,\mathrm{d}y = \iint_D \frac{\partial x}{\partial x}\,\mathrm{d}x\,\mathrm{d}y = \iint_D 1\,\mathrm{d}x\,\mathrm{d}y = S(D)
```

该项低于 `52.5` 硬阈值，且属于证明中的小代入链；PDF 视觉检查无拥挤或越界，按用户口径保留行内。

## 4. PDF 版面复核

已重新渲染并检查：

- `tmp/pdfs/batch_022_674_682/page-472.png` 至 `page-480.png`

检查结果：

- `page-472`：Green 第二公式证明起段显示正常，公式骨架未挤压。
- `page-473`：调和函数题题干与第 (1) 问显示正常。
- `page-474`：挖小圆准备、偏导和边界导数改写显示正常。
- `page-475`：内边界外法向、小圆极限和边界拆分显示正常。
- `page-476`：流量题、椭圆面积题和闭曲线 Green 题显示正常。
- `page-477`：奇点挖洞题和路径无关性题显示正常；标题贴连已修复。
- `page-478`：变量替换证明和 Stokes 定理入口显示正常。
- `page-479`：Stokes 三角形题与球面平面交线题显示正常。
- `page-480`：Stokes 换面法题显示正常；标题贴连已修复，后续定义盒未受影响。

## 5. 验证记录

- 重建索引：`python solution_quality_audit/build_solution_index.py`
  - `total_solutions = 1322`
  - `long_inline_flagged = 238`
- 编译：`latexmk -xelatex -interaction=nonstopmode -halt-on-error elegantbook2.tex`
  - 结果：成功生成 `elegantbook2.pdf`
- 日志扫描：`Overfull|Underfull|LaTeX Warning|Package .* Warning|Undefined control sequence|Fatal|^!`
  - 结果：无输出
- PDF 页数：`724`
- `git diff --check -- elegantbook2.tex solution_quality_audit/solution_index.csv solution_quality_audit/summary.json solution_quality_audit/solution_quality_ledger.md`
  - 结果：仅有既有 Windows 换行提示，无空白错误

## 6. 放行结论

批次 `#674-682` 可放行进入下一批。放行依据包括：逐题内容复算通过、Green 奇点挖洞与内边界符号闭合、Stokes 观察方向到法向的翻译正确、推导步骤完整、与前文方法口径一致、硬长行内公式清零、PDF 目检通过。
