# Display Width Audit

Estimator: adapted from the user-provided Gemini heuristic; full line is 70 units.

## Summary

- `total_display_blocks`: 2920
- `low_width_lt_0_5`: 110
- `simple_inline_candidates`: 13
- `structural_low_width`: 97
- `threshold_ratio`: 0.5
- `textwidth_units`: 70.0

## Low-Width Simple Inline Candidates

| # | lines | ratio | context | preview |
|---:|---:|---:|---|---|
| 549 | 7060-7062 | 0.46 | 微分方程 / 知识讲解 / 线性理论，特征根，比对系数 | `f(x) = \mathrm{e}^{\lambda x}\bigl[P_m(x)\cos\omega x+Q_n(x)\sin\omega x\bigr]` |
| 550 | 7064-7066 | 0.46 | 微分方程 / 知识讲解 / 线性理论，特征根，比对系数 | `y^*=x^k\,\mathrm{e}^{\lambda x}\bigl[T_M(x)\cos\omega x+G_M(x)\sin\omega x\bigr]` |
| 830 | 10982-10984 | 0.34 | 微分方程 / 习题 / 第六节习题：二阶常系数微分方程 | `\boxed{y = C_1\cos x + C_2\sin x - \frac{1}{2}x\cos x}.` |
| 2028 | 30251-30253 | 0.43 | 曲线积分与曲面积分 / 习题 / 第四节习题：第二类曲面积分 | `I=-\iint_D x^2y^2\sqrt{x^2+y^2}\,\mathrm{d}x\,\mathrm{d}y.` |
| 2148 | 32030-32032 | 0.43 | 级数 / 知识讲解 / 数项级数判敛：定理依据、常见阶与估阶方法 | `\boxed{\text{选估阶操作}\quad\longrightarrow\quad \text{读出标准阶}\quad\longrightarrow\quad \text{用标准阶表判断敛散}.}` |
| 2566 | 39439-39441 | 0.31 | 往年真题整理 / 2013级工科数学分析下 A卷 | `\sum_{n=1}^{\infty}n a_n(x-1)^{n+1}` |
| 2582 | 39822-39824 | 0.23 | 往年真题整理 / 2013级工科数学分析下 B卷 | `\sum_{n=1}^{\infty}a_n(x-1)^n` |
| 2616 | 40658-40660 | 0.36 | 往年真题整理 / 2015级工科数学分析下 A卷 | `f(x,y,z)=\ln(x^2+y^2+z^2).` |
| 2626 | 40964-40966 | 0.26 | 往年真题整理 / 2015级工科数学分析下 B卷 | `f(x,y,z)=\cos(xyz).` |
| 2639 | 41266-41268 | 0.23 | 往年真题整理 / 2016级工科数学分析下 A卷 | `f(x,y)=2x^2+y^2.` |
| 2669 | 41835-41837 | 0.19 | 往年真题整理 / 2016级工科数学分析下 B卷 | `\frac{x^2}{9}+\frac{y^2}{4}=1,` |
| 2859 | 46162-46164 | 0.33 | 往年真题整理 / 2022级工科数学分析下 B卷 | `\int_\Gamma (x+y)^2\,\mathrm{d}s=\underline{\hspace{4cm}}.` |
| 2902 | 47217-47219 | 0.31 | 往年真题整理 / 2024级工科数学分析（二）期末考试 A 卷 | `\sum_{n=1}^{\infty}n a_n(x-1)^{n-1}` |

## Low-Width But Structural Or Non-Bracket

| # | kind | lines | ratio | context | preview |
|---:|---|---:|---:|---|---|
| 115 | align* | 1590-1594 | 0.34 | 不定积分 / 习题 / 第一节习题：模法与多项式逆元 | `\frac{x^2}{AB^2} &=\frac{B-1}{AB^2}\\ &=\frac{1}{AB}-\frac{1}{AB^2}.` |
| 117 | bracket | 1608-1613 | 0.40 | 不定积分 / 习题 / 第一节习题：模法与多项式逆元 | `\frac{1}{AB^2} =\frac{(x+1)^2}{A} -\frac{x^2+x}{B} -\frac{x}{B^2}.` |
| 176 | align* | 2293-2297 | 0.47 | 不定积分 / 习题 / 第六节习题：\texorpdfstring{含有 $ax^2+bx+c\ (a>0)$ 的积分}{二次三项式积分} | `\int \frac{\mathrm{d}x}{ax^2+bx+c} &= \frac{1}{a}\int \frac{\mathrm{d}u}{u^2-\dfrac{\Delta}{4a^2}}.` |
| 190 | align* | 2448-2451 | 0.39 | 不定积分 / 习题 / 第七节习题：\texorpdfstring{含有 $\sqrt{x^2+a^2}\ (a>0)$ 的积分}{根式积分（加号）} | `2K&=xy-a^2L,\\ K&=\frac{1}{2}xy-\frac{a^2}{2}L.` |
| 473 | bracket | 5791-5793 | 0.19 | 微分方程 / 知识讲解 / 不要因为不能套公式就以为自己不会做，看看是否可分离、齐次与可化齐次 | `\begin{vmatrix}a_1&b_1\\a_2&b_2\end{vmatrix}=0.` |
| 475 | bracket | 5805-5807 | 0.19 | 微分方程 / 知识讲解 / 不要因为不能套公式就以为自己不会做，看看是否可分离、齐次与可化齐次 | `\begin{vmatrix}a_1&b_1\\a_2&b_2\end{vmatrix}\neq0.` |
| 523 | bracket | 6481-6486 | 0.49 | 微分方程 / 知识讲解 / 恰当方程与积分因子 | `\frac{\mathrm{d}y}{\mathrm{d}x} =\frac{r-x}{y} =\frac{y}{r+x} =\frac{y}{x+\sqrt{x^2+y^2}}.` |
| 541 | bracket | 6838-6840 | 0.30 | 微分方程 / 知识讲解 / 线性理论，特征根，比对系数 | `W(x) = \begin{vmatrix} 1 & x \\ 0 & 1 \end{vmatrix} = 1 \neq 0.` |
| 556 | bracket | 7159-7161 | 0.43 | 微分方程 / 知识讲解 / 常数变易法和几个刘维尔公式 | `W(x)=\begin{vmatrix} y_1 & y_2 \\ y_1' & y_2' \end{vmatrix}=y_1y_2'-y_2y_1',` |
| 634 | bracket | 8223-8228 | 0.44 | 微分方程 / 习题 / 第二节习题：变量可分离方程及齐次方程 | `\boxed{ \arctan\frac{2y}{x-1} +\ln\big((x-1)^2+4y^2\big) =C }.` |
| 640 | bracket | 8337-8342 | 0.30 | 微分方程 / 习题 / 第二节习题：变量可分离方程及齐次方程 | `\frac{\mathrm{d}A}{\mathrm{d}t} =\alpha\frac{\mathrm{d}P}{\mathrm{d}t} =\alpha\lambda P =\lambda A.` |
| 652 | bracket | 8498-8503 | 0.49 | 微分方程 / 习题 / 第二节习题：变量可分离方程及齐次方程 | `y=\pm\left( 2\ln\left\|\frac{2-\sqrt{4-x^2}}{x}\right\| \sqrt{4-x^2} \right)+C.` |
| 679 | bracket | 8895-8901 | 0.47 | 微分方程 / 习题 / 第三节习题：一阶线性微分方程 | `\boxed{ y=\frac{1}{x} \quad\text{或}\quad y=\frac{2Cx^2+1}{2Cx^3-x} },` |
| 691 | bracket | 9178-9183 | 0.41 | 微分方程 / 习题 / 第三节习题：一阶线性微分方程 | `\boxed{ y=\arctan\!\left[ \frac{1}{3}\left(1+x^2-\frac{1}{\sqrt{1+x^2}}\right) \right]}.` |
| 701 | bracket | 9333-9339 | 0.46 | 微分方程 / 习题 / 第四节习题：可降阶的高阶方程 | `p\frac{\mathrm{d}p}{\mathrm{d}y} =\frac{p^3}{\sqrt y}, \qquad \frac{\mathrm{d}p}{p^2} =\frac{\mathrm{d}y}{\sqrt y}.` |
| 713 | bracket | 9478-9484 | 0.44 | 微分方程 / 习题 / 第四节习题：可降阶的高阶方程 | `\boxed{ y=\frac{1}{8}\mathrm{e}^{2x} -\frac{1}{4}\mathrm{e}^2x^2 +\frac{1}{4}\mathrm{e}^2x -\frac{1}{8}\mathrm{e}^2 }.` |
| 753 | bracket | 9956-9963 | 0.37 | 微分方程 / 习题 / 第五节习题：二阶微分方程 | `W(x) = \begin{vmatrix} \mathrm{e}^x & \mathrm{e}^{2x} \\ \mathrm{e}^x & 2\mathrm{e}^{2x} \end{vmatrix} = \mathrm{e}^{3x}.` |
| 758 | bracket | 10005-10007 | 0.29 | 微分方程 / 习题 / 第五节习题：二阶微分方程 | `W(x)=\begin{vmatrix}1&x^2\\0&2x\end{vmatrix}=2x.` |
| 786 | bracket | 10384-10389 | 0.44 | 微分方程 / 习题 / 第五节习题：二阶微分方程 | `\boxed{\frac{\mathrm{d}^2V_C}{\mathrm{d}t^2} + \frac{R}{L}\frac{\mathrm{d}V_C}{\mathrm{d}t} + \frac{1}{LC}V_C = \frac{E_m}{LC}\sin\omega t}.` |
| 811 | bracket | 10765-10771 | 0.49 | 微分方程 / 习题 / 第六节习题：二阶常系数微分方程 | `\lambda^2-6\lambda+9=0 \implies (\lambda-3)^2=0 \implies \lambda_{1,2}=3.` |
| 824 | bracket | 10926-10932 | 0.47 | 微分方程 / 习题 / 第六节习题：二阶常系数微分方程 | `\lambda^2+4\lambda+4=0 \implies (\lambda+2)^2=0 \implies \lambda=-2.` |
| 862 | bracket | 11479-11486 | 0.39 | 微分方程 / 习题 / 第七节习题：微分方程组的基本理论 | `\begin{pmatrix} x' \\ y' \end{pmatrix} = \begin{pmatrix} 1 & 0 \\ 0 & 1 \end{pmatrix} \begin{pmatrix} x \\ y \end{pmatrix} + \begin{pmatrix} \sin t \\ \cos t \end{pmatrix}` |
| 863 | bracket | 11495-11500 | 0.31 | 微分方程 / 习题 / 第七节习题：微分方程组的基本理论 | `\begin{cases} x'=x+2y,\\ y'=4x+3y. \end{cases}` |
| 881 | bracket | 11663-11668 | 0.24 | 微分方程 / 习题 / 第七节习题：微分方程组的基本理论 | `\begin{cases} \dfrac{\mathrm{d}x}{\mathrm{d}t}=y,\\ \dfrac{\mathrm{d}y}{\mathrm{d}t}=x. \end{cases}` |
| 883 | bracket | 11677-11682 | 0.37 | 微分方程 / 习题 / 第七节习题：微分方程组的基本理论 | `\begin{cases} \dfrac{\mathrm{d}x}{\mathrm{d}t}=x+2y,\\ \dfrac{\mathrm{d}y}{\mathrm{d}t}=4x+3y. \end{cases}` |
| 884 | bracket | 11684-11689 | 0.36 | 微分方程 / 习题 / 第七节习题：微分方程组的基本理论 | `\begin{cases} \dfrac{\mathrm{d}x}{\mathrm{d}t}=x-5y,\\ \dfrac{\mathrm{d}y}{\mathrm{d}t}=2x-y. \end{cases}` |
| 1018 | bracket | 14317-14322 | 0.41 | 多元函数微分学 / 知识讲解 / 向量值函数，雅可比矩阵 | `f(x,y,z)=\begin{pmatrix} 3x+e^y z\\ x^3+y^2\sin z \end{pmatrix}` |
| 1021 | bracket | 14347-14353 | 0.49 | 多元函数微分学 / 知识讲解 / 向量值函数，雅可比矩阵 | `\boxed{Jf\!\left(\frac12,1,\pi\right) =\begin{pmatrix} 3 & e\pi & e\\[6pt] \dfrac34 & 0 & -1 \end{pmatrix}_{2\times 3}}.` |
| 1079 | bracket | 15274-15280 | 0.27 | 多元函数微分学 / 知识讲解 / 链式法则、高阶偏导与二阶全微分 | `H_{(x,y)}(u)= \begin{pmatrix} 0&0\\ 0&0 \end{pmatrix},` |
| 1080 | bracket | 15281-15287 | 0.39 | 多元函数微分学 / 知识讲解 / 链式法则、高阶偏导与二阶全微分 | `H_{(x,y)}(v)= \begin{pmatrix} -y\sin x&\cos x\\ \cos x&0 \end{pmatrix}.` |
| 1083 | bracket | 15353-15358 | 0.49 | 多元函数微分学 / 知识讲解 / 链式法则、高阶偏导与二阶全微分 | `\mathrm{d}^2z =z_{xx}\,\mathrm{d}x^2 +2z_{xy}\,\mathrm{d}x\,\mathrm{d}y +z_{yy}\,\mathrm{d}y^2.` |
| 1108 | align* | 15844-15848 | 0.43 | 多元函数微分学 / 知识讲解 / 隐函数专题：单方程、方程组与雅可比行列式 | `\mathrm{d}z &=\mathrm{d}y+ \frac{1+(x-1)\mathrm{e}^{z-y-x}}{1+x\mathrm{e}^{z-y-x}}\,\mathrm{d}x.` |
| 1110 | bracket | 15873-15879 | 0.40 | 多元函数微分学 / 知识讲解 / 隐函数专题：单方程、方程组与雅可比行列式 | `\frac{\partial(F,G)}{\partial(u,v)} :=\begin{vmatrix} \dfrac{\partial F}{\partial u} & \dfrac{\partial F}{\partial v}\\[8pt] \dfrac{\partial G}{\partial u} & \dfrac{\partial G}{\partial v} \end{vmatrix}` |
| 1114 | bracket | 15942-15947 | 0.33 | 多元函数微分学 / 知识讲解 / 隐函数专题：单方程、方程组与雅可比行列式 | `\begin{cases} xu-yv=0,\\ yu+xv=1. \end{cases}` |
| 1120 | bracket | 16029-16034 | 0.37 | 多元函数微分学 / 知识讲解 / 隐函数专题：单方程、方程组与雅可比行列式 | `\begin{cases} x=-u^2+v+z,\\ y=u+vz. \end{cases}` |
| 1169 | bracket | 16886-16891 | 0.49 | 多元函数微分学 / 知识讲解 / 约束极值与拉格朗日乘数法 | `\frac{\partial L}{\partial x_k} =\frac{x_1x_2\cdots x_n}{x_k}+\lambda=0 \implies \frac{P}{x_k}=-\lambda.` |
| 1181 | bracket | 17109-17114 | 0.43 | 多元函数微分学 / 知识讲解 / 偏微分方程专题：验证、变量替换与坐标变换 | `\left(\frac{\partial u}{\partial x}\right)^{\!2} +\left(\frac{\partial u}{\partial y}\right)^{\!2} =\left(\frac{\partial u}{\partial r}\right)^{\!2} +\frac{1}{r^2}\left(\frac{\partial u}{\partial\theta}\right)^{\!2}.` |
| 1212 | bracket | 17736-17738 | 0.34 | 多元函数微分学 / 习题 / 第二节习题：多元函数的基本概念 | `\lim_{\substack{x\to0\\ y\to1}}\frac{1-xy}{x^2+y^2}=1.` |
| 1213 | bracket | 17741-17743 | 0.39 | 多元函数微分学 / 习题 / 第二节习题：多元函数的基本概念 | `\lim_{\substack{x\to2\\ y\to0}}\frac1{x^2+y^2}=\frac14.` |
| 1260 | bracket | 18539-18541 | 0.27 | 多元函数微分学 / 习题 / 第四节习题：向量值函数及其微分 | `\lim_{t\to 1}f(t) = \begin{pmatrix} 1 \\ 0 \end{pmatrix}.` |
| 1262 | bracket | 18573-18575 | 0.23 | 多元函数微分学 / 习题 / 第四节习题：向量值函数及其微分 | `Jf(t)=\begin{pmatrix}1\\2t\\3t^2\end{pmatrix}.` |
| 1263 | bracket | 18586-18592 | 0.43 | 多元函数微分学 / 习题 / 第四节习题：向量值函数及其微分 | `Jf(u,v) = \begin{pmatrix} \cos v & -u\sin v \\ \sin v & u\cos v \\ 1 & 0 \end{pmatrix}.` |
| 1271 | bracket | 18752-18754 | 0.41 | 多元函数微分学 / 习题 / 第四节习题：向量值函数及其微分 | `f'(x,y) = Jf(x,y) = \begin{bmatrix} 2x & 2y \\ 3y & 3x \end{bmatrix}.` |
| 1337 | bracket | 19894-19899 | 0.49 | 多元函数微分学 / 习题 / 第六节习题：梯度与方向导数 | `\nabla T = \nabla(k r^{-1}) = -k r^{-2}\nabla r = -k\frac{\boldsymbol r}{r^3},` |
| 1343 | bracket | 20018-20023 | 0.39 | 多元函数微分学 / 习题 / 第七节习题：隐函数微分法 | `y'' = \frac{\dfrac{2y'}{y} - \dfrac{2y'}{x} + \dfrac{y}{x^2} - x\left(\dfrac{y'}{y}\right)^2} {\ln x - \dfrac{x}{y}},` |
| 1356 | bracket | 20222-20227 | 0.47 | 多元函数微分学 / 习题 / 第七节习题：隐函数微分法 | `\begin{cases} u = f(xu, v+y), \\ v = g(u-x, v^2y), \end{cases}` |
| 1408 | bracket | 21560-21562 | 0.23 | 多元函数微分学 / 习题 / 第十节习题：无约束的最优化问题 | `2\begin{pmatrix}1&1/2\\[2pt]1/2&1/3\end{pmatrix},` |
| 1428 | bracket | 22252-22257 | 0.47 | 多元函数微分学 / 习题 / 第十二节习题：偏导数在偏微分方程中的应用 | `\Delta f = f_{xx}+f_{yy} =\frac{1}{\sigma^2+\tau^2} \left(f_{\sigma\sigma}+f_{\tau\tau}\right),` |
| 1472 | bracket | 23205-23210 | 0.36 | 多元函数微分学 / 习题 / 本章总习题 | `\begin{cases} z=x^2+y^2,\\[4pt] y=\dfrac{1}{x}, \end{cases}` |
| 1487 | bracket | 23530-23536 | 0.31 | 重积分 / 知识讲解 / 二重积分基础专题：概念、性质与区域语言 | `f(x, y) = \begin{cases} 1, & (x, y) \text{ 两个坐标均为有理数时} \\ 0, & \text{其它情况} \end{cases}` |
| 1545 | bracket | 24338-24343 | 0.40 | 重积分 / 知识讲解 / 三重积分专题：直角坐标、柱坐标与球坐标 | `\begin{cases} x^{2}+y^{2}+z^{2}=4,\\ x^{2}+y^{2}=3z \end{cases}` |
| 1715 | bracket | 26812-26816 | 0.46 | 重积分 / 习题 / 本章总习题 | `J=\frac{\partial(x,y)}{\partial(u,v)} =\det\begin{pmatrix}2au&0\\0&2bv\end{pmatrix} =4abuv,` |
| 1725 | bracket | 26945-26955 | 0.11 | 曲线积分与曲面积分 / 知识讲解 / 总路线：先识别对象，再看结构，再选工具 | `\boxed{ \text{定义层语言} \longrightarrow \text{结构主工具} \longrightarrow \text{修正手段} \longrightarrow \text{最终计算} }.` |
| 1728 | bracket | 27032-27038 | 0.27 | 曲线积分与曲面积分 / 知识讲解 / 总路线：先识别对象，再看结构，再选工具 | `\begin{gathered} \boxed{\text{Green：平面闭曲线的环量 = 平面区域内的旋度总和}},\\ \boxed{\text{Stokes：空间闭曲线的环量 = 张成曲面上的旋度通量}},\\ \boxed{\text{Gauss：闭曲面的通量 = 所围体内的散度总和}}. \end{gathered}` |
| 1794 | equation | 27855-27857 | 0.40 | 曲线积分与曲面积分 / 知识讲解 / 第二类曲线积分：保守场、Green、Stokes | `S(D)=\frac12\oint_C (x\,\mathrm{d}y-y\,\mathrm{d}x).` |
| 1878 | bracket | 28718-28724 | 0.44 | 曲线积分与曲面积分 / 知识讲解 / 第二类曲面积分与通量 | `\begin{aligned} \frac{\partial(y,z)}{\partial(x,y)}&=1,& \frac{\partial(z,x)}{\partial(x,y)}&=1,& \frac{\partial(x,y)}{\partial(x,y)}&=1. \end{aligned}` |
| 1906 | bracket | 29023-29028 | 0.46 | 曲线积分与曲面积分 / 知识讲解 / 第二类曲面积分：投影、封口、Gauss | `\frac{\partial x^3}{\partial x} +\frac{\partial y^3}{\partial y} +\frac{\partial z^3}{\partial z} =3x^2+3y^2+3z^2.` |
| 2038 | bracket | 30338-30344 | 0.49 | 曲线积分与曲面积分 / 习题 / 第四节习题：第二类曲面积分 | `\operatorname{div}\vec F =\frac{\partial(y-z)}{\partial x} +\frac{\partial(z-x)}{\partial y} +\frac{\partial(x-y)}{\partial z} =0` |
| 2052 | bracket | 30536-30542 | 0.33 | 曲线积分与曲面积分 / 习题 / 第五节习题：格林公式及其应用 | `\boxed{ I=\begin{cases} 0,&0<R<1,\\ \pi,&R>1. \end{cases}}` |
| 2057 | bracket | 30578-30584 | 0.27 | 曲线积分与曲面积分 / 习题 / 第五节习题：格林公式及其应用 | `\boxed{ I=\begin{cases} 0,&0\notin D,\\ 2\pi,&0\in D. \end{cases}}` |
| 2058 | bracket | 30597-30602 | 0.34 | 曲线积分与曲面积分 / 习题 / 第五节习题：格林公式及其应用 | `Q_x-P_y =\frac{\partial^2 f}{\partial x^2} +\frac{\partial^2 f}{\partial y^2} =\Delta f.` |
| 2075 | bracket | 30908-30914 | 0.36 | 曲线积分与曲面积分 / 习题 / 第七节习题：散度和Gauss公式 | `\operatorname{div}\vec{r} =\frac{\partial x}{\partial x} +\frac{\partial y}{\partial y} +\frac{\partial z}{\partial z} =3,` |
| 2095 | bracket | 31220-31226 | 0.47 | 曲线积分与曲面积分 / 习题 / 第九节习题：梯度算子 | `\nabla\cdot(u\vec{C}) =a\frac{\partial u}{\partial x} +b\frac{\partial u}{\partial y} +c\frac{\partial u}{\partial z} =\nabla u\cdot \vec{C}.` |
| 2100 | bracket | 31284-31289 | 0.49 | 曲线积分与曲面积分 / 习题 / 第九节习题：梯度算子 | `\operatorname{div}(\vec{F}\times\vec{G}) =\frac{\partial(QN-RM)}{\partial x} +\frac{\partial(RL-PN)}{\partial y} +\frac{\partial(PM-QL)}{\partial z}.` |
| 2201 | bracket | 33072-33078 | 0.43 | 级数 / 知识讲解 / 傅里叶展开专题一：周期函数的三角级数 | `f(x)= \begin{cases} 0, & x\in(-\pi,0],\\ x, & x\in(0,\pi]. \end{cases}` |
| 2406 | bracket | 35830-35836 | 0.49 | 级数 / 习题 / 本章总习题 | `f(x)= \begin{cases} x, & 0\le x<1,\\ 2-x, & 1\le x\le2 \end{cases}` |
| 2486 | bracket | 37144-37150 | 0.44 | 往年真题整理 / 2006--2007 第二学期 B 卷 | `V\left(\frac p3\right) = \pi\left(\frac{2p}{3}\right)^2\frac p3 = \frac{4\pi p^3}{27},` |
| 2522 | bracket | 38354-38359 | 0.27 | 往年真题整理 / 2009级工科数学分析下 B卷 | `\cos\theta = \frac{\|\boldsymbol r'(t)\cdot\boldsymbol k\|} {\|\boldsymbol r'(t)\|\,\|\boldsymbol k\|}.` |
| 2563 | bracket | 39392-39400 | 0.47 | 往年真题整理 / 2013级工科数学分析下 A卷 | `D_{\nabla z/\|\nabla z\|}z = \nabla z\cdot\frac{\nabla z}{\|\nabla z\|} = \|\nabla z\| = 2\sqrt5.` |
| 2580 | bracket | 39739-39745 | 0.49 | 往年真题整理 / 2013级工科数学分析下 B卷 | `f(x)= \begin{cases} 2, & -1<x\le 0,\\ x^3, & 0<x\le 1, \end{cases}` |
| 2600 | bracket | 40196-40201 | 0.46 | 往年真题整理 / 2014级工科数学分析下 A卷 | `L:\begin{cases} x=a(t-\sin t),\\ y=a(1-\cos t), \end{cases}` |
| 2606 | bracket | 40390-40396 | 0.49 | 往年真题整理 / 2014级工科数学分析下 B卷 | `f(x)= \begin{cases} 3,&-1<x\le0,\\ x^3,&0<x\le1, \end{cases}` |
| 2644 | bracket | 41333-41338 | 0.43 | 往年真题整理 / 2016级工科数学分析下 A卷 | `\begin{cases} y'+y\cos x=\mathrm{e}^{-\sin x},\\ y\|_{x=0}=1 \end{cases}` |
| 2647 | bracket | 41404-41409 | 0.40 | 往年真题整理 / 2016级工科数学分析下 A卷 | `\begin{cases} x^2+y^2+z^2=9,\\ x-y+z=1 \end{cases}` |
| 2653 | bracket | 41598-41603 | 0.41 | 往年真题整理 / 2016级工科数学分析下 A卷 | `\begin{cases} 1+\alpha+\beta=0,\\ 3+2\alpha+\beta=-1, \end{cases}` |
| 2665 | bracket | 41731-41741 | 0.47 | 往年真题整理 / 2016级工科数学分析下 A卷 | `z_{xx} = 2f_\xi + 4x^2f_{\xi\xi} + 8xyf_{\xi\eta} + 4y^2f_{\eta\eta}.` |
| 2667 | bracket | 41784-41789 | 0.29 | 往年真题整理 / 2016级工科数学分析下 A卷 | `\begin{cases} z=x^2+y^2,\\ y=\dfrac1x \end{cases}` |
| 2670 | bracket | 41865-41870 | 0.37 | 往年真题整理 / 2016级工科数学分析下 B卷 | `\begin{cases} y'+\dfrac{3}{x}y=\dfrac{2}{x^3},\\ y\|_{x=1}=1 \end{cases}` |
| 2674 | bracket | 42257-42263 | 0.43 | 往年真题整理 / 2017级工科数学分析下 A卷 | `\begin{cases} x=t-\cos t,\\ y=1-\sin t,\\ z=t, \end{cases}` |
| 2675 | bracket | 42278-42284 | 0.49 | 往年真题整理 / 2017级工科数学分析下 A卷 | `f(x)= \begin{cases} -1, & -\pi<x\le 0,\\ 1, & 0<x\le \pi, \end{cases}` |
| 2676 | bracket | 42322-42328 | 0.44 | 往年真题整理 / 2017级工科数学分析下 A卷 | `f(x,y)= \begin{cases} x\sin\dfrac{1}{y}, & xy\ne 0,\\ 0, & xy=0, \end{cases}` |
| 2717 | bracket | 43261-43266 | 0.37 | 往年真题整理 / 2018级工科数学分析下 A卷 | `\mathrm{d}\omega = \frac{\mathbf T\cdot(\mathbf T_u\times\mathbf T_v)} {\|\mathbf T\|^3}\,\mathrm{d}u\,\mathrm{d}v.` |
| 2740 | bracket | 43624-43629 | 0.26 | 往年真题整理 / 2018级工科数学分析下 B卷 | `I=\begin{cases} 0, & 0\notin\Omega,\\ 4\pi, & 0\in\Omega. \end{cases}` |
| 2745 | bracket | 43756-43758 | 0.23 | 往年真题整理 / 2019级工科数学分析下 A卷 | `H=\begin{pmatrix}6x&-3\\-3&6y\end{pmatrix}.` |
| 2759 | bracket | 44191-44196 | 0.33 | 往年真题整理 / 2019级工科数学分析下 B卷补考 | `\begin{cases} y=f(x,t),\\ x=g(y,t) \end{cases}` |
| 2764 | bracket | 44291-44297 | 0.31 | 往年真题整理 / 2019级工科数学分析下 B卷补考 | `I= \begin{cases} 0, & P\text{ 在 }\Sigma\text{ 所围区域外},\\ -4\pi, & P\text{ 在 }\Sigma\text{ 所围区域内}. \end{cases}` |
| 2777 | bracket | 44551-44557 | 0.49 | 往年真题整理 / 2020级工科数学分析（二）期末考试 A 卷 | `\Gamma: \begin{cases} x^2+y^2+z^2-3x=0,\\ x+y-z=0 \end{cases}` |
| 2792 | bracket | 44858-44864 | 0.43 | 往年真题整理 / 2020级工科数学分析（二）期末考试 B 卷 | `\Gamma: \begin{cases} x^2+y^2+z^2=6,\\ x+y+z=0 \end{cases}` |
| 2834 | bracket | 45567-45572 | 0.36 | 往年真题整理 / 2021级工科数学分析（二）期末考试 B 卷 | `\begin{cases} x^2+y^2=1,\\ x-y+z=2, \end{cases}` |
| 2844 | bracket | 45768-45774 | 0.39 | 往年真题整理 / 2022级工科数学分析下 A卷 | `\begin{cases} x=t-\cos t,\\ y=\sin t,\\ z=2t \end{cases}` |
| 2862 | bracket | 46199-46205 | 0.47 | 往年真题整理 / 2022级工科数学分析下 B卷 | `f(x)= \begin{cases} x^2, & -\pi<x\le 0,\\ 0, & 0<x\le \pi, \end{cases}` |
| 2872 | bracket | 46443-46448 | 0.33 | 往年真题整理 / 2022级工科数学分析下 B卷 | `\begin{cases} x^2+y^2=2y,\\ y-z=1, \end{cases}` |
| 2884 | bracket | 46746-46751 | 0.29 | 往年真题整理 / 2023级工科数学分析（二）期末考试 A 卷 | `\begin{cases} z=x^2+y^2,\\ y=\dfrac1x \end{cases}` |
| 2885 | bracket | 46768-46773 | 0.40 | 往年真题整理 / 2023级工科数学分析（二）期末考试 A 卷 | `\begin{cases} x^2+y^2+z^2=6,\\ x+y+z=0 \end{cases}` |
| 2890 | bracket | 46952-46960 | 0.37 | 往年真题整理 / 2023级工科数学分析（二）期末考试 B 卷 | `\frac{\partial(u,v)}{\partial(x,y)} = \begin{vmatrix} 2x&2y\\ -2x&2y \end{vmatrix} =8xy.` |
| 2903 | bracket | 47233-47239 | 0.49 | 往年真题整理 / 2024级工科数学分析（二）期末考试 A 卷 | `f(x)= \begin{cases} 2, & -1<x\le 0,\\ x^3, & 0<x\le 1, \end{cases}` |
| 2919 | bracket | 47683-47690 | 0.21 | 往年真题整理 / 2024级工科数学分析（二）期末考试 B 卷 | `M= \begin{bmatrix} A&F&E\\ F&B&D\\ E&D&C \end{bmatrix}` |
