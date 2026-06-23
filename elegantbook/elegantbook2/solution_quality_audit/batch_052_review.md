# 批次 052 整改复审记录

生成时间：2026-06-23

## 0. 执行边界

- 批次范围：全局 `#819-821`
- 源码范围：`elegantbook2.tex:38410-38505`
- PDF 复核页：物理页 `606-607`
- 当前 PDF 页数：`739`
- 本轮主题：第 7 章往年真题选择题 7.1-7.3
- 本轮复核口径：先核对空间解析几何、二元函数可微性和二重积分对称化的答案正确性，再检查推导是否跳步，最后按“接近 `3/4 \textwidth` 才拆长行内公式”的标准复核排版。

## 1. 已完成的主要整改

- `#819`：保留法向量定义为行内短公式，将交线方向向量的叉乘结果作为关键判定式独立列出，避免把方向向量计算塞入长行。
- `#820`：补足连续性、偏导存在性、不可微性的三段判定链条；用极坐标估计说明连续，用定义验证两个偏导数存在，用路径 `y=x` 反证可微性。
- `#821`：保留原有累次积分推导结构，逐步核对 `xy` 部分为零、`\cos x\sin y` 部分化为偶函数积分并对应到 `D_1`。

## 2. 逐题内容复核摘要

| 全局号 | 复核结论 |
| ---: | --- |
| 819 | 两个给定平面的法向量为 \(\boldsymbol n_1=(1,3,2)\)、\(\boldsymbol n_2=(2,-1,-10)\)，交线方向向量 \(\boldsymbol n_1\times\boldsymbol n_2=(-28,14,-7)\sim(4,-2,1)\)。平面 \(\pi\) 的法向量也是 \((4,-2,1)\)，故直线方向平行于平面法向量，直线垂直于平面，选 C 正确。 |
| 820 | 极坐标代换得 \(f=r\cos^2\theta\sin\theta\)，由 \(|f|\le r\) 得原点连续。按偏导定义得 \(f_x(0,0)=f_y(0,0)=0\)。若可微则余项除以 \(\sqrt{x^2+y^2}\) 应趋于 0；沿 \(y=x\) 得 \(x/(2\sqrt2|x|)\)，左右极限不同且不趋于 0，故偏导存在但不可微，选 A 正确。 |
| 821 | 将积分拆为 \(xy\) 与 \(\cos x\sin y\) 两部分。前者写成 \(\frac12\int_{-a}^{a}x(a^2-x^2)\,\mathrm dx\)，奇函数积分为 0。后者先对 \(y\) 积分得到 \(\int_{-a}^{a}\cos x(\cos x-\cos a)\,\mathrm dx\)， integrand 为偶函数，等于 \(2\int_0^a\cos x(\cos x-\cos a)\,\mathrm dx=2\iint_{D_1}\cos x\sin y\,\mathrm dx\,\mathrm dy\)，选 A 正确。 |

## 3. 公式排版复核

- 重建索引：`python solution_quality_audit/build_solution_index.py`
- 本批索引结果：
  - `#819`: `inline_long_count = 0`, `display_count = 1`, `short_display_count = 1`
  - `#820`: `inline_long_count = 0`, `display_count = 2`, `short_display_count = 2`
  - `#821`: `inline_long_count = 0`, `display_count = 4`, `short_display_count = 4`
- 本批没有接近 `3/4 \textwidth` 的长行内公式。
- `#819` 的叉乘、`#820` 的偏导定义和路径反例、`#821` 的积分拆分与累次积分，虽被脚本标为短 display，但都承担答案判定的推导骨架；强行压回行内会形成分式/积分堆叠或削弱层次，因此保留。
- 短定义和局部结论仍放在行内，例如法向量、选项结论、连续性结论和偶奇性说明。

## 4. PDF 版面复核

已渲染并目检：

- `tmp/pdfs/batch_052_819_821/page-606.png`
- `tmp/pdfs/batch_052_819_821/page-607.png`

检查结果：

- `page-606`：`#819` 空间几何判定和 `#820` 可微性判定层次清晰，无长行挤压；偏导定义与路径反例显示完整。
- `page-607`：`#821` 题干、选项和解答显示正常，积分推导未压边；页面下方后续题目自然接续。

## 5. 验证记录

- 编译：`latexmk -xelatex -interaction=nonstopmode -halt-on-error elegantbook2.tex`
  - 结果：成功生成 `elegantbook2.pdf`
- 日志扫描：`Overfull \hbox|Underfull \hbox|LaTeX Warning|Package .* Warning|Undefined control sequence|Fatal|^!`
  - 结果：无输出
- PDF 页数：`739`

## 6. 放行结论

批次 `#819-821` 可放行。放行依据包括：三题答案均已按对应知识点重新验算，解题链条完整无跳步；公式排版未出现长行内挤压，也未把低地位短公式随意拆成 display；PDF 渲染页 `606-607` 无拥挤、错位、压边或异常留白。
