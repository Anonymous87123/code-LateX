from pathlib import Path
import re


path = Path(r"d:\code LateX\elegantbook\elegantbook2.tex")
text = path.read_text(encoding="utf-8")


def replace_overview(text: str, label: str, title: str, new_block: str) -> str:
    pattern = re.compile(
        rf"\\begin\{{skill\}}\[{re.escape(title)}\]\\label\{{{re.escape(label)}\}}.*?\\end\{{skill\}}",
        re.S,
    )
    text, count = pattern.subn(lambda _m: new_block, text, count=1)
    if count != 1:
        raise RuntimeError(f"Failed to replace overview {label}")
    return text


ch3 = r"""\begin{skill}[第3章冲刺总手册]\label{sk:ch3-overview}
第3章最怕的不是公式不会背，而是题目刚拿到手时不知道自己到底在做“定义域题”“极限题”“求导题”“几何题”“极值题”还是“PDE 验证/变换题”。所以你先别算，先把对象认出来。只要题面在问定义域、等高线、内点边界点、开闭性，就走点集链；只要在问趋于某点时的函数值，就走极限与连续链；只要在问偏导、全微分、可微、复合求导、隐函数求导，就走微分链；只要出现方向、法向、切线、切平面、最大变化率，就把梯度当主角；只要问极大极小、最值、约束条件，就切极值链；只要题面出现 $\Delta u$、波动方程、极坐标 Laplace 算子，就切 PDE 链。整章的题全都先经过这一层分流。

如果题目先考定义域与点集，不要凭图形感觉。先把函数能写出来的条件机械列全：分母不为零，根号内非负，对数真数大于零，反三角的自变量落在定义区间。定义域最后一定是这些条件的交集。若题目问等高线或等位面，就直接写
\[
f(x,y)=c,\qquad f(x,y,z)=c
\]
再化成熟悉曲线或曲面。若题目问边界、聚点、内点、外点、开集、闭集，必须回到定义：
\[
\partial A=\overline{A}\setminus A^\circ,\qquad
\overline{A}=A\cup A',\qquad
\text{区域}=\text{连通开集}.
\]
判断边界点要看任意邻域是否同时碰到集合内外两侧；判断聚点一定要用去心邻域；判断闭集最稳的是证明“补集是开集”或“它包含全部聚点”。这类题最短的答题句永远是“由……得限制条件……，故定义域为……；由定义知该点是/不是内点、边界点、聚点”。

如果题目在问极限或连续，先直接代入。代得出来且没有分母、根号奇性，就先记下候选值；代不出来，再按“代数化简 $\to$ 夹逼 $\to$ 极坐标 $\to$ 两路径反证”的顺序扫。只要题目在原点附近反复出现
\[
x^2+y^2,\qquad \sqrt{x^2+y^2},
\]
或者分子分母都是关于 $(x,y)$ 的齐次量，就优先切极坐标
\[
x=r\cos\theta,\qquad y=r\sin\theta.
\]
极坐标里最常用的判零模板是
\[
|f(x,y)|\le C r^\alpha,\qquad \alpha>0
\quad\Longrightarrow\quad
\lim_{(x,y)\to(0,0)}f(x,y)=0.
\]
如果你要证明极限不存在，不要硬证“所有路径都不一样”，只要找两条路径使极限值不同就够了。连续题则多补一句：先要求函数在该点有定义，再要求极限存在且等于函数值。别忘了孤立点自动连续，因为它的去心邻域里根本没有定义域内的别的点可供逼近。

一旦题目进入偏导、全微分、可微，就把“偏导存在”和“可微”严格分开。偏导只表示沿坐标方向的变化率：
\[
f_x(x_0,y_0)=\lim_{h\to0}\frac{f(x_0+h,y_0)-f(x_0,y_0)}{h},\qquad
f_y(x_0,y_0)=\lim_{k\to0}\frac{f(x_0,y_0+k)-f(x_0,y_0)}{k}.
\]
可微则要求函数在该点能被一个统一的线性函数逼近：
\[
\Delta f=f_x\,\Delta x+f_y\,\Delta y+o(\rho),\qquad
\rho=\sqrt{(\Delta x)^2+(\Delta y)^2}.
\]
于是全微分就是
\[
\mathrm{d}f=f_x\,\mathrm{d}x+f_y\,\mathrm{d}y.
\]
考试最稳的结论是：若偏导在邻域内连续，则函数可微；可微一定连续，也一定有偏导；但“偏导存在”本身既不保证连续，也不保证可微。题目若真让你按定义判可微，写法固定为“先求偏导并写出线性主部，再证余项除以 $\rho$ 趋于 $0$”。只要求偏导时，不要多谈可微；只要求可微时，也不要只算偏导就停。

如果题目是复合函数求导，不要凭感觉乱链，直接画依赖关系。对标量复合函数 $z=f(u,v)$，其中 $u=u(x,y),v=v(x,y)$，必须写
\[
z_x=f_u u_x+f_v v_x,\qquad
z_y=f_u u_y+f_v v_y.
\]
若自变量是参数 $t$，再写
\[
\frac{\mathrm{d}z}{\mathrm{d}t}=z_x\frac{\mathrm{d}x}{\mathrm{d}t}+z_y\frac{\mathrm{d}y}{\mathrm{d}t}.
\]
若是向量值函数，就改成矩阵语言
\[
J_{F\circ G}(x)=J_F(G(x))\,J_G(x).
\]
这条 Jacobian 链既服务本章复合求导，也服务下一章换元。只要题目里出现“从 $(u,v)$ 到 $(x,y)$ 的变换”“向量值函数”“多层嵌套”，你都可以把所有一阶导数塞进 Jacobian 矩阵统一处理。

如果题目由方程定义了未知函数，马上切到隐函数链，不要再按显函数公式硬算。单方程最常用的是
\[
F(x,y)=0\quad\Longrightarrow\quad
y'=-\frac{F_x}{F_y}\qquad(F_y\neq 0),
\]
以及曲面形式
\[
F(x,y,z)=0\quad\Longrightarrow\quad
z_x=-\frac{F_x}{F_z},\qquad
z_y=-\frac{F_y}{F_z}\qquad(F_z\neq 0).
\]
如果是方程组
\[
F(x,y,u,v)=0,\qquad G(x,y,u,v)=0,
\]
先记
\[
\Delta=\frac{\partial(F,G)}{\partial(u,v)}
=
\begin{vmatrix}
F_u & F_v\\
G_u & G_v
\end{vmatrix},
\qquad
\Delta\neq 0,
\]
再对 $x$ 或 $y$ 求导，列线性方程组
\[
\begin{cases}
F_u u_x+F_v v_x=-F_x,\\
G_u u_x+G_v v_x=-G_x,
\end{cases}
\qquad
\begin{cases}
F_u u_y+F_v v_y=-F_y,\\
G_u u_y+G_v v_y=-G_y.
\end{cases}
\]
用 Cramer 法则解就行。想背成比值也可以：
\[
u_x=-\frac{\partial(F,G)/\partial(x,v)}{\partial(F,G)/\partial(u,v)},\qquad
v_x=-\frac{\partial(F,G)/\partial(u,x)}{\partial(F,G)/\partial(u,v)},
\]
对 $y$ 同理。这里真正要防的是分母对应的 Jacobian 为零，那时局部未必能解出隐函数。

如果题目问方向导数、法向、最速上升、最速下降、等位面法线、切平面法向，你就把梯度拿出来。定义先背：
\[
\nabla f=(f_x,f_y)\quad\text{或}\quad (f_x,f_y,f_z),\qquad
D_{\boldsymbol l}f=\nabla f\cdot \boldsymbol l,
\]
其中 $\boldsymbol l$ 必须是单位向量。最大方向导数取在梯度方向，数值为
\[
\max D_{\boldsymbol l}f=\|\nabla f\|,\qquad
\min D_{\boldsymbol l}f=-\|\nabla f\|.
\]
若题目给的是隐式曲面 $F(x,y,z)=C$，则 $\nabla F$ 就是法向量；若给的是显式曲面 $z=f(x,y)$，其切平面写成
\[
z-z_0=f_x(x_0,y_0)(x-x_0)+f_y(x_0,y_0)(y-y_0),
\]
等价地也可写成
\[
f_x(x_0,y_0)(x-x_0)+f_y(x_0,y_0)(y-y_0)-(z-z_0)=0.
\]
参数曲线 $\boldsymbol r(t)=(x(t),y(t),z(t))$ 在 $t_0$ 处的切向量是 $\boldsymbol r'(t_0)$，切线式可写为
\[
\frac{x-x_0}{x'(t_0)}=\frac{y-y_0}{y'(t_0)}=\frac{z-z_0}{z'(t_0)}.
\]
若空间曲线是两个曲面 $F_1=0,F_2=0$ 的交线，则切向量直接取
\[
\nabla F_1\times \nabla F_2.
\]
整类题最容易错的是方向向量没单位化、法向量方向写反、把切平面和法平面混掉。

如果题目进入 Taylor 展开、局部极值、最值判别，就先写驻点，再看二阶信息。二元函数在 $(x_0,y_0)$ 的二阶 Taylor 展开写成
\[
f(x_0+h,y_0+k)
=f_0+f_x h+f_y k
+\frac12\left(f_{xx}h^2+2f_{xy}hk+f_{yy}k^2\right)+o(\rho^2),\qquad
\rho=\sqrt{h^2+k^2}.
\]
无约束极值的第一步永远是求驻点
\[
f_x=0,\qquad f_y=0.
\]
然后记
\[
\Delta=f_{xx}f_{yy}-f_{xy}^2.
\]
判别表机械背：
\[
\Delta>0,\ f_{xx}>0\Rightarrow \text{极小值},\qquad
\Delta>0,\ f_{xx}<0\Rightarrow \text{极大值},
\]
\[
\Delta<0\Rightarrow \text{鞍点},\qquad
\Delta=0\Rightarrow \text{二阶判别失效，需另想办法}.
\]
如果题目问的是闭区域上的最大最小值，就不能只看内部驻点，必须再扫边界；边界若能参数化或消元，就把它化成一元函数再做一元极值。考试里“驻点算完就停”是这类题最大的失分点。

有约束极值要先判能不能消元。约束简单、显式、代回后不炸时，消元法通常最短；约束复杂、变量对称、或根本不想解出某一变量时，立刻用 Lagrange 乘子。单个约束 $g=0$ 的模板是
\[
\nabla f=\lambda \nabla g,\qquad g=0.
\]
两个约束 $g=0,h=0$ 的模板是
\[
\nabla f=\lambda \nabla g+\mu \nabla h,\qquad g=0,\qquad h=0.
\]
最后把候选点全部代回原目标函数比较大小。若题目是“在等位面上求极值”，梯度正交关系尤其要牢记，因为约束面的法向就是 $\nabla g$。凡是极值题，最后都要补一句“比较各候选点函数值，故最大值/最小值为……”。

如果题目进入 PDE，整章其实只干两件事：验证一个给定函数是否满足 PDE，或者把 PDE 换到更合适的坐标系。验证题不要多想，原则只有一句：只求方程真正用到的偏导，然后代回去看等式是否成立。若
\[
u=\phi(\xi),\qquad \xi=\xi(x,y),
\]
则
\[
u_x=\phi'(\xi)\xi_x,\qquad
u_{xx}=\phi''(\xi)\xi_x^2+\phi'(\xi)\xi_{xx}.
\]
若
\[
u=u(\xi,\eta),\qquad \xi=\xi(x,y),\ \eta=\eta(x,y),
\]
则
\[
u_x=u_\xi \xi_x+u_\eta \eta_x,\qquad
u_y=u_\xi \xi_y+u_\eta \eta_y.
\]
所有二阶 PDE 都遵循“一阶结果再求一遍，不能跳步”这条铁律。若题目给出波动方程型通解 $u=\phi(x+at)+\psi(x-at)$，就分别对 $x,t$ 求二阶导代回即可。

如果 PDE 与边界都顺着极坐标长出来，就切极坐标。母式必须直接会写：
\[
x=r\cos\theta,\qquad y=r\sin\theta,
\]
\[
u_x=u_r\cos\theta-\frac{\sin\theta}{r}u_\theta,\qquad
u_y=u_r\sin\theta+\frac{\cos\theta}{r}u_\theta.
\]
二维 Laplace 算子极坐标形式是
\[
u_{xx}+u_{yy}=u_{rr}+\frac1r u_r+\frac1{r^2}u_{\theta\theta}.
\]
若题目有径向对称 $u=u(r)$，就进一步化成
\[
u_{xx}+u_{yy}=u_{rr}+\frac1r u_r.
\]
所以 PDE 变换题的固定流程就是“先写新旧变量关系，再写一阶导，再写需要的二阶导，最后整体代回”。最容易漏的是 $1/r$、$1/r^2$ 系数，以及径向对称时忘记把 $u_\theta,u_{\theta\theta}$ 消掉。

整章最后统一收尾时，你要强迫自己检查六件事。第一，定义域题有没有把所有限制取交集。第二，极限题若判不存在，是否真的给出了两条导致不同极限的路径。第三，可微题是否真的证了余项是 $o(\rho)$，而不是只算了偏导。第四，隐函数题的分母 Jacobian 是否非零。第五，极值题是否把边界候选点也算进去了。第六，PDE 题是否把所有需要的偏导都算齐了。只要这六项不漏，第3章的题就都能从“对象识别”顺着一条主线落到底。
\end{skill}"""


ch4 = r"""\begin{skill}[第4章冲刺总手册]\label{sk:ch4-overview}
第4章的总原则不是“见积分就列二重积分”，而是先认对象，再先画图，再决定到底是直接列限、换序、换元，还是先写应用公式。你拿到题后先做四个判断：它是二重积分、三重积分、广义重积分还是应用题；区域是在平面上还是空间里；边界是直线/曲线拼成的普通区域，还是圆、环、球、锥、旋转对称区域；被积函数与边界里是否反复出现 $x^2+y^2$、$x^2+y^2+z^2$、线性斜带、椭圆等明显适合换元的结构。整章所有题都从这四步识别开始。

如果题目是二重积分，第一步永远先看区域 $D$，而不是先盯被积函数。你要先把边界求交点、画草图、确认是竖切更顺还是横切更顺。最基本的两类模板是
\[
D=\{(x,y):a\le x\le b,\ \varphi_1(x)\le y\le \varphi_2(x)\},
\]
和
\[
D=\{(x,y):c\le y\le d,\ \psi_1(y)\le x\le \psi_2(y)\}.
\]
一旦某个方向能一刀切到底，就直接按这个方向列限；若一刀切不完，就分块。二重积分的主公式只是
\[
\iint_D f(x,y)\,\mathrm{d}A
\]
而真正会丢分的是区域漏块、界限顺序写反、上下边界认错。考试里“先交点，后画图，再列限”一定要机械执行。

二重积分的性质也要会用，不只是会算。线性与区域可加性告诉你能拆就拆；面积公式
\[
\iint_D 1\,\mathrm{d}A=S(D)
\]
告诉你常函数积分就是面积；比较与估值告诉你
\[
mS(D)\le \iint_D f\,\mathrm{d}A\le MS(D),\qquad
\left|\iint_D f\,\mathrm{d}A\right|\le \iint_D |f|\,\mathrm{d}A;
\]
中值定理告诉你连续函数满足
\[
\iint_D f(x,y)\,\mathrm{d}A=f(\xi,\eta)S(D).
\]
所以如果题目问大小比较、符号、平均值、是否可能为零，不要急着真算，先看这些性质能不能秒掉。

一旦你已经列出了一个二重积分，但发现内层原函数难算、根本没法下手，就立刻回到区域图考虑换序。换序不是机械交换积分号，而是重新描述同一个区域。固定做法是：先画原区域，再沿新方向重新切片，再写出新的外层范围和新切片的左右或上下边界。若区域需要分块，换序后也常常需要分块，所以“换序前先看整体形状，换序后再决定是否分段”比死背模板更重要。

如果区域或被积函数围着圆和半径打转，就优先考虑极坐标。最基本的变换是
\[
x=r\cos\theta,\qquad y=r\sin\theta,\qquad
\mathrm{d}A=r\,\mathrm{d}r\,\mathrm{d}\theta.
\]
只要题面反复出现
\[
x^2+y^2,\qquad
x^2+y^2\le a^2,\qquad
x^2+y^2\ge a^2,
\]
或者区域是圆盘、圆环、扇形、花瓣形、由圆和射线围成的区域，极坐标通常是主路。别忘了换元时被积函数也要一起变，$x^2+y^2$ 直接换成 $r^2$，而 Jacobian 的 $r$ 一定要补上。若题目不是圆形而是椭圆、平行四边形、线性斜带，往往更该用一般换元而不是硬切极坐标。

一般换元只背一条公式：若
\[
x=x(u,v),\qquad y=y(u,v),\qquad
J=\frac{\partial(x,y)}{\partial(u,v)}\neq 0,
\]
则
\[
\iint_D f(x,y)\,\mathrm{d}x\mathrm{d}y
=\iint_{D'} f(x(u,v),y(u,v))\,|J|\,\mathrm{d}u\mathrm{d}v.
\]
这里的 $|J|$ 不是装饰，而是局部面积放缩倍数。考试中最常见的信号是：边界是两组平行线、线性组合 $ax+by$、椭圆或双曲线能被配方拉直、被积函数里恰好有一组线性因子适合拿来当新变量。若换过去区域还是很碎，说明换元选错了，及时撤回。

如果题目已经升级成三重积分，还是先看区域而不是先算。最常见的两类写法是“先一后二”和“先二后一”。前者长成
\[
\iiint_\Omega f(x,y,z)\,\mathrm{d}V
=\iint_D\left(\int_{z_-(x,y)}^{z_+(x,y)} f(x,y,z)\,\mathrm{d}z\right)\mathrm{d}A,
\]
也就是先在 $xy$ 平面投影，再用上下曲面定 $z$；后者则是在固定某个变量后，横截面更容易描述。真正的经验规则是：哪一个变量的上下界最明显，就把它放内层。若区域由两个曲面夹成，先求交线；若区域有对称性，先利用对称性减半或判零。

一旦三维边界反复出现 $x^2+y^2$，或区域绕 $z$ 轴旋转对称，就切柱坐标：
\[
x=r\cos\theta,\qquad y=r\sin\theta,\qquad z=z,\qquad
\mathrm{d}V=r\,\mathrm{d}r\,\mathrm{d}\theta\,\mathrm{d}z.
\]
用柱坐标时，固定流程是“先看俯视图定 $\theta,r$，再用上下曲面定 $z$”。常见翻译关系要直接会写：
\[
x^2+y^2=r^2,\qquad
z=x^2+y^2\Longleftrightarrow z=r^2,\qquad
x^2+y^2=az\Longleftrightarrow r^2=az.
\]
如果边界是球面、圆锥面、球冠、球扇形，或不等式核心是“到原点的距离”，就切球坐标：
\[
x=\rho\sin\varphi\cos\theta,\qquad
y=\rho\sin\varphi\sin\theta,\qquad
z=\rho\cos\varphi,
\]
\[
\mathrm{d}V=\rho^2\sin\varphi\,\mathrm{d}\rho\,\mathrm{d}\varphi\,\mathrm{d}\theta,\qquad
x^2+y^2+z^2=\rho^2.
\]
这里 $\varphi$ 是从 $z$ 轴正向量下来的天顶角，不是从水平面往上的仰角。常见翻译还包括
\[
z=kr\Longleftrightarrow \tan\varphi=\frac1k,\qquad
z=h\Longleftrightarrow \rho\cos\varphi=h,\qquad
x^2+y^2+z^2=2az\Longleftrightarrow \rho=2a\cos\varphi.
\]
用球坐标时，固定流程就是“先定方位角 $\theta$，再由锥面或半空间定 $\varphi$，最后沿射线定 $\rho$”。

如果题目是广义重积分，不要把“无穷区域”或“奇点”直接硬塞进普通积分。原则只有一句：先截断，再取极限。无界区域就先用大圆、大球或大盒子截断；内部有奇点，就挖去半径 $\varepsilon$ 的小圆或小球。写法固定成
\[
\lim_{R\to\infty}\iint_{D_R} f\,\mathrm{d}A,\qquad
\lim_{\varepsilon\to0^+}\iint_{D\setminus B_\varepsilon} f\,\mathrm{d}A,
\]
三重积分同理。这里最容易漏的是：极限没有写，或者只截断了区域没截断奇点附近。若题目只问收敛性，也可以先看被积函数在远处或奇点附近与哪个幂次函数同阶，再用比较法快速判断。

如果题目是应用题，就更不能先算积分，必须先写目标量公式。对平面薄片密度 $\rho(x,y)$，质量是
\[
M=\iint_D \rho\,\mathrm{d}A,
\]
质心是
\[
\bar x=\frac1M\iint_D x\rho\,\mathrm{d}A,\qquad
\bar y=\frac1M\iint_D y\rho\,\mathrm{d}A.
\]
对空间物体密度 $\rho(x,y,z)$，质量是
\[
M=\iiint_\Omega \rho\,\mathrm{d}V,
\]
质心是
\[
\bar x=\frac1M\iiint_\Omega x\rho\,\mathrm{d}V,\qquad
\bar y=\frac1M\iiint_\Omega y\rho\,\mathrm{d}V,\qquad
\bar z=\frac1M\iiint_\Omega z\rho\,\mathrm{d}V.
\]
常见静力矩、转动惯量也只是往 integrand 里多乘一个距离平方，例如绕 $x$ 轴的转动惯量写成
\[
I_x=\iiint_\Omega (y^2+z^2)\rho\,\mathrm{d}V.
\]
若区域关于某坐标面对称，而 integrand 对那一坐标是奇函数，很多矩量会直接为零，这比硬算快得多。

整章最后统一封口时，你要检查七件事。第一，区域是否真的被你完整描述了，没有重叠也没有漏块。第二，外层内层变量顺序与积分限是否匹配。第三，换序后描述的是否还是同一个区域。第四，换元后被积函数和 Jacobian 是否都换干净了，而且 Jacobian 取了绝对值。第五，柱坐标和球坐标里的角度范围是否写全。第六，应用题是不是先写了物理量公式再积分。第七，若题目有对称性，你有没有先利用对称性省掉一半计算。只要这七项不漏，第4章所有题都能沿着“先看区域，后选工具，最后封口”的总流程做下去。
\end{skill}"""


ch5 = r"""\begin{skill}[第5章冲刺总手册]\label{sk:ch5-overview}
第5章的全部题目先只看积分记号，不看别的。看到 $\mathrm{d}s$ 就认作第一类曲线积分；看到 $P\,\mathrm{d}x+Q\,\mathrm{d}y(+R\,\mathrm{d}z)$ 就认作第二类曲线积分；看到 $\mathrm{d}S$ 就认作第一类曲面积分；看到 $\mathrm{d}y\mathrm{d}z,\mathrm{d}z\mathrm{d}x,\mathrm{d}x\mathrm{d}y$ 或 $\vec F\cdot\mathrm{d}\vec S$ 就认作第二类曲面积分。认完对象以后，再只查三件事：它闭不闭，方向怎么记，区域里有没有奇点。Green、Gauss、Stokes、保守场全都只在这三件事过关以后才能上。

如果题目是第一类曲线积分，它积的是“标量 $\times$ 弧长”，因此方向不影响值。主公式只有
\[
\int_\Gamma f\,\mathrm{d}s=\int_a^b f(\boldsymbol r(t))\,\|\boldsymbol r'(t)\|\,\mathrm{d}t.
\]
若曲线已经参数化，就直接代；若是平面显式曲线 $y=y(x)$，就写
\[
\mathrm{d}s=\sqrt{1+y'^2(x)}\,\mathrm{d}x;
\]
若是 $x=x(y)$，就写
\[
\mathrm{d}s=\sqrt{1+x'^2(y)}\,\mathrm{d}y.
\]
若是空间曲线，则
\[
\mathrm{d}s=\sqrt{x'^2+y'^2+z'^2}\,\mathrm{d}t.
\]
遇到弧长、线密度、细线质量、沿曲线分布的电荷总量，本质都是这条公式。这里最容易错的是把它当成第二类曲线积分去追方向，或忘了 $\mathrm{d}s$ 永远非负。

如果题目是第二类曲线积分，你先不要急着参数化。先看它是不是端点题、路径无关题、全微分题或闭路题。只要出现这些信号，就先判保守场。平面场 $\vec F=(P,Q)$ 在单连通区域内的常用判据是
\[
P_y=Q_x;
\]
空间场 $\vec F=(P,Q,R)$ 在单连通区域内的常用判据是
\[
\nabla\times\vec F=\vec 0.
\]
一旦判成保守场，先求势函数 $u$，使
\[
\nabla u=\vec F,
\]
然后直接写
\[
\int_A^B \vec F\cdot\mathrm{d}\boldsymbol r=u(B)-u(A),\qquad
\oint \vec F\cdot\mathrm{d}\boldsymbol r=0.
\]
求势函数的最稳做法是先从一个分量积分出主干，再用其余分量回填待定函数。若题目还要求“显式求势函数”，就必须把这个待定函数真正算出来。这里最大的陷阱是：$P_y=Q_x$ 或 $\nabla\times\vec F=0$ 只是局部条件，若定义域不是单连通，闭路积分未必为零。

如果第二类曲线积分是在平面闭曲线上，而且区域内没有奇点，优先考虑 Green 公式而不是硬参数化。环量式是
\[
\oint_\Gamma P\,\mathrm{d}x+Q\,\mathrm{d}y=\iint_D(Q_x-P_y)\,\mathrm{d}A,
\]
通量式是
\[
\oint_\Gamma P\,\mathrm{d}y-Q\,\mathrm{d}x=\iint_D(P_x+Q_y)\,\mathrm{d}A.
\]
所以只要题目出现面积、环量、流量、沿闭曲线的二类线积分、外法向导数，Green 就要第一时间浮出来。面积公式也要直接会用：
\[
S(D)=\oint_\Gamma x\,\mathrm{d}y=-\oint_\Gamma y\,\mathrm{d}x=\frac12\oint_\Gamma (x\,\mathrm{d}y-y\,\mathrm{d}x).
\]
若题目是多连通区域，记账原则永远是“外逆内顺”，也就是外边界按正向，内边界按反向。若区域里有奇点，不能直接上 Green，先挖洞再说。

挖洞类题一定要记住一个基准积分：
\[
\oint_C \frac{-y\,\mathrm{d}x+x\,\mathrm{d}y}{x^2+y^2}=2k\pi,
\]
其中 $k$ 是曲线绕原点的绕数。凡是看到分母里有 $x^2+y^2$、题面又是闭路、而区域包着原点或别的奇点，你就要先想“这是 Green 禁用题，应该挖洞或直接用绕数”。若题目只差一小段边就能闭合，也可以先补边再用 Green，最后减掉补边贡献。

如果题目是第一类曲面积分，它积的是“标量 $\times$ 面积”，方向同样不影响值。主公式有两种。若曲面参数化为 $\boldsymbol r(u,v)$，就写
\[
\iint_\Sigma f\,\mathrm{d}S=\iint f(\boldsymbol r(u,v))\,\|\boldsymbol r_u\times\boldsymbol r_v\|\,\mathrm{d}u\mathrm{d}v.
\]
若曲面是图形曲面 $z=z(x,y)$，就写
\[
\mathrm{d}S=\sqrt{1+z_x^2+z_y^2}\,\mathrm{d}x\mathrm{d}y,\qquad
\iint_\Sigma f\,\mathrm{d}S=\iint_D f(x,y,z(x,y))\sqrt{1+z_x^2+z_y^2}\,\mathrm{d}x\mathrm{d}y.
\]
若题目是面积，只需令 $f\equiv1$。整类题最常见的坑是参数区间没覆盖整个曲面，或把第一类曲面积分误当成第二类去记方向符号。

如果题目是第二类曲面积分，你第一眼就要想法向和闭合，而不是马上参数化。定义上
\[
\iint_\Sigma \vec F\cdot\mathrm{d}\vec S
=\iint_\Sigma P\,\mathrm{d}y\mathrm{d}z+Q\,\mathrm{d}z\mathrm{d}x+R\,\mathrm{d}x\mathrm{d}y.
\]
参数化时可以统一写成
\[
\iint_\Sigma \vec F\cdot\mathrm{d}\vec S
=\pm\iint_D \vec F(\boldsymbol r(u,v))\cdot(\boldsymbol r_u\times \boldsymbol r_v)\,\mathrm{d}u\mathrm{d}v,
\]
符号由定向决定。若曲面是图形曲面 $z=z(x,y)$，向上取法向时有
\[
\iint_\Sigma P\,\mathrm{d}y\mathrm{d}z+Q\,\mathrm{d}z\mathrm{d}x+R\,\mathrm{d}x\mathrm{d}y
=\iint_D(-Pz_x-Qz_y+R)\,\mathrm{d}x\mathrm{d}y,
\]
向下则整体变号。若曲面能对 $xOy$、$yOz$、$zOx$ 某个坐标平面单值投影，优先选投影最简单的那个平面；若分片更省，就分片；若只差一张盖子就能闭合，就优先封口后上 Gauss。

Gauss 公式只管闭曲面的总通量。对闭曲面 $\partial\Omega$ 取外法向时，
\[
\oiint_{\partial\Omega}\vec F\cdot\vec n\,\mathrm{d}S
=\iiint_\Omega \operatorname{div}\vec F\,\mathrm{d}V,\qquad
\operatorname{div}\vec F=P_x+Q_y+R_z.
\]
所以只要题目是闭曲面的第二类曲面积分，或原曲面不闭但补一张面就能闭，Gauss 就是主路。封口法的模板固定写成
\[
I_{\text{原}}+I_{\text{补面}}=\iiint_\Omega \operatorname{div}\vec F\,\mathrm{d}V,\qquad
I_{\text{原}}=\text{总体}-I_{\text{补面}}.
\]
若 $\operatorname{div}\vec F=0$，总通量立刻为零；若被积向量场和区域高度对称，也要先看奇偶性和对称性再决定算不算。封口题里最容易错的是补面法向取反，导致最后加减号全错。

Stokes 公式只管空间闭曲线与其张成曲面的边界关系。对有向曲面 $\Sigma$ 及其正向边界 $\partial\Sigma$，
\[
\oint_{\partial\Sigma}\vec F\cdot\mathrm{d}\boldsymbol r
=\iint_\Sigma (\nabla\times\vec F)\cdot\vec n\,\mathrm{d}S,
\]
其中
\[
\nabla\times\vec F=(R_y-Q_z,\ P_z-R_x,\ Q_x-P_y).
\]
所以只要题目是空间闭曲线上的二类线积分，而那条曲线又是某个曲面的边界，就要优先想 Stokes。真正的优势不在于“多写一个公式”，而在于你可以换成同边界的更简单曲面。因此只要边界是圆、椭圆、平面截线、球面和平面的交线，而原曲面很难，你就把它换成平面圆盘、平面片等最简单同边界曲面，再用 Stokes。这里的方向账只能靠右手法则：四指沿边界正向卷曲时，大拇指指向法向正向。

Green、Gauss、Stokes 本质上都在做“边界积分 = 内部导数积分”，所以综合题的总路由只有一句：先认对象，再判闭合，再判奇点，再决定是保守场、Green、Gauss、Stokes，还是直接参数化。你可以把它机械写成：端点差优先保守场；平面闭曲线优先 Green；空间闭曲线优先 Stokes；闭曲面优先 Gauss；对象差一点才匹配定理时，做最小改造：补边、挖洞、封口、换面。改造模板也必须直接会写：
\[
I_{\text{原}}=I_{\text{闭}}-I_{\text{补边}},\qquad
I_{\text{原}}+I_{\text{补面}}=I_{\text{总体}},\qquad
I_{\text{外}}-\sum I_{\text{内}}=\iint_{D_\varepsilon}(Q_x-P_y)\,\mathrm{d}A.
\]
改造只做最小必要量，改完立刻送进标准定理，不要过度施工。

若题目出现 $u,v,\Delta,\partial/\partial n$ 这类符号，说明它不是普通流量题，而是 Green 第一、第二公式链。平面版常用为
\[
\iint_D (u\Delta v+u_xv_x+u_yv_y)\,\mathrm{d}A=\oint_\Gamma u\frac{\partial v}{\partial n}\,\mathrm{d}s,
\]
\[
\iint_D (u\Delta v-v\Delta u)\,\mathrm{d}A=\oint_\Gamma\left(u\frac{\partial v}{\partial n}-v\frac{\partial u}{\partial n}\right)\,\mathrm{d}s.
\]
三维版对应为
\[
\iiint_\Omega (u\Delta v+\nabla u\cdot\nabla v)\,\mathrm{d}V=\oiint_{\partial\Omega} u\frac{\partial v}{\partial n}\,\mathrm{d}S,
\]
\[
\iiint_\Omega (u\Delta v-v\Delta u)\,\mathrm{d}V=\oiint_{\partial\Omega}\left(u\frac{\partial v}{\partial n}-v\frac{\partial u}{\partial n}\right)\,\mathrm{d}S.
\]
若 $u$ 调和而 $v=\ln r$ 或 $v=1/r$，这些公式还能直接导出调和函数的边界表示式。遇到这类题时，不要再回到普通 Green/Gauss 环量模板，而要沿“法向导数 + 调和函数 + Green 第二公式”这条专用链走。

最后把本章常用向量算子速背掉，因为很多定理题、判保守场题、综合题都要用：
\[
\nabla u=(u_x,u_y,u_z),\qquad
\operatorname{div}\vec F=P_x+Q_y+R_z,\qquad
\operatorname{rot}\vec F=\nabla\times\vec F.
\]
还要会用
\[
\nabla\cdot(\nabla u)=\Delta u,\qquad
\nabla\times(\nabla u)=\vec 0,\qquad
\nabla\cdot(\nabla\times\vec F)=0.
\]
若 $r=\sqrt{x^2+y^2+z^2}$，还常用
\[
\nabla r=\frac{\vec r}{r},\qquad
\nabla f(r)=f'(r)\frac{\vec r}{r}.
\]
这些结论既能帮你快速判保守场，也能帮你在 Gauss、Stokes、Green 第二公式题里缩短推导。

整章最后统一封口时，你要检查八件事。第一，是否把积分对象认对了。第二，第一类积分是不是本来与方向无关。第三，Green、Gauss、Stokes 的对象是否真的匹配。第四，方向账是否和题设一致。第五，定义域内是否有奇点或洞，单连通条件是否满足。第六，补边、挖洞、封口、换面后有没有把补上的量正确减回。第七，若用了投影公式，投影平面与符号是否一致。第八，若用了保守场，最终是否真的写成端点差或闭路为零。只要这八项没漏，第5章所有题都能沿着“认对象 $\to$ 判闭合 $\to$ 判奇点 $\to$ 选主定理 $\to$ 封口检查”的主线机械做完。
\end{skill}"""


text = replace_overview(text, "sk:ch3-overview", "第3章冲刺总手册", ch3)
text = replace_overview(text, "sk:ch4-overview", "第4章冲刺总手册", ch4)
text = replace_overview(text, "sk:ch5-overview", "第5章冲刺总手册", ch5)

chapter_local = {
    "sk:ch2-overview": [
        "sk:ode-concepts",
        "sk:ode-separable-homogeneous",
        "sk:ode-linear-first-order",
        "sk:ode-exact-factor",
        "sk:ode-reduction-order",
        "sk:ode-missing-x",
        "sk:wronskian",
        "sk:ode-second-linear",
        "sk:ode-second-solution",
        "sk:ode-third-solution",
        "sk:ode-constant-coeff",
        "sk:ode-system",
        "sk:ode-first-order-tree",
        "sk:ode-higher-order-tree",
    ],
    "sk:ch3-overview": [
        "sk:multivar-basics",
        "sk:multivar-limit",
        "sk:differential-differentiability",
        "sk:jacobian",
        "sk:chain-rule",
        "sk:gradient-directional",
        "sk:implicit-function",
        "sk:implicit-system",
        "sk:taylor-extrema",
        "sk:tangent-plane",
        "sk:unconstrained-extrema",
        "sk:constrained-extrema-entry",
        "sk:lagrange",
        "sk:pde-verify-transform",
        "sk:pde-transform",
    ],
    "sk:ch4-overview": [
        "sk:double-integral-concepts",
        "sk:double-integral-setup",
        "sk:change-order",
        "sk:polar-jacobian",
        "sk:double-integral-tree",
        "sk:improper-multiple",
        "sk:triple-integral",
        "sk:coordinate-choice",
        "sk:polar-cylinder-sphere",
        "sk:multiple-apps",
    ],
    "sk:ch5-overview": [
        "sk:curve1",
        "sk:curve2",
        "sk:surface1",
        "sk:surface2",
        "sk:surface2-orientation",
        "sk:surface2-projection",
        "sk:surface2-method",
        "sk:green",
        "sk:green-hole",
        "sk:conservative",
        "sk:potential-undetermined",
        "sk:gauss",
        "sk:gauss-cap",
        "sk:stokes",
        "sk:theorem-directions",
        "sk:boundary-transform",
        "sk:stokes-change",
        "sk:nabla-operators",
        "sk:gst-tree",
        "sk:gst-transform",
    ],
}

for labels in chapter_local.values():
    for lbl in labels:
        pattern = re.compile(
            rf"\n\\begin\{{skill\}}\[[^\n]*\]\\label\{{{re.escape(lbl)}\}}.*?\\end\{{skill\}}\n",
            re.S,
        )
        text, count = pattern.subn("\n", text)
        if count == 0:
            raise RuntimeError(f"Failed to remove skill block {lbl}")

lines = text.splitlines()
for i, line in enumerate(lines):
    if r"\useskills{" in line:
        for chapter_label, labels in chapter_local.items():
            if any(lbl in line for lbl in labels):
                lines[i] = rf"\useskills{{\skillref{{{chapter_label}}}}}"
                break
text = "\n".join(lines)

for chapter_label, labels in chapter_local.items():
    for lbl in labels:
        text = text.replace(rf"\skillref{{{lbl}}}", rf"\skillref{{{chapter_label}}}")

text = re.sub(r"\n{3,}", "\n\n", text)
path.write_text(text, encoding="utf-8")
print("rewrite complete")
