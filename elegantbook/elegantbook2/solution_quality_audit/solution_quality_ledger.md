# 全书 solution 质量整改台账
## 说明
- 本台账由当前 `elegantbook2.tex` 自动全域遍历生成，覆盖每一个 `solution` 环境。
- `AUTO_FLAGGED_NEEDS_MANUAL` 不是最终定罪，只是优先人工复核队列；后续需要逐题审校并交 GPT-5.5 子代理复核。
- 硬性整改口径：补齐跳步、统一前文方法、修正数学错误、长行内公式回退为规范行间公式，禁止过度压缩。

## 汇总
- `total_solutions`: 1322
- `auto_flagged`: 1086
- `long_inline_flagged`: 141
- `jump_keyword_flagged`: 584
- `short_display_flagged`: 795
- `by_chapter`: 不定积分=155, 微分方程=160, 多元函数微分学=240, 重积分=88, 曲线积分与曲面积分=120, 级数=55, 往年真题整理=504
- `by_risk_tag`: 微分方程=199, 极值/拉格朗日=114, 隐函数/偏导=289, 重积分/换元=215, 曲面积分/通量=168, 级数/幂级数=193, 曲线积分=115, Green/Gauss/Stokes=83, Fourier=41
- `by_defect_flag`: 跳步关键词=584, 短display待判定=795, 长行内公式/排版风险=141, 高风险题解过短=99, display密度偏高=1

## 自动标记缺陷队列
| 全局序号 | 行号 | 章节 | 小节 | 题目预览 | 标签 | 标记 | 证据 | 建议 |
|---:|---:|---|---|---|---|---|---|---|
| 1 | 1413 | 不定积分 | 习题 | 混合分解 $\frac{x^3+2}{(x-1)^2(x^2+1)}$ |  | 跳步关键词,短display待判定 | 可得; 1415:F(x)=\frac{A}{x-1}+\frac{B}{(x-1)^2}+\frac{Cx+D}{x^2+1}. \| 1419:G(x)=(x-1)^2F(x)=\frac{x^3+2}{x^2+1}. \| 1423:B=G(1)=\frac{1^3+2}{1^2+1}=\frac32. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 2 | 1468 | 不定积分 | 习题 | 分解$\frac{x+2}{(x^2+2x+2)(x^2+1)}$ |  | 跳步关键词,短display待判定 | 可得; 1493:\frac{x+2}{(x^2+2x+2)(x^2+1)} =\frac{3x+2}{5(x^2+2x+2)} +\frac{4-3x}{5(x^2+1)}. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 4 | 1517 | 不定积分 | 习题 | 分解$\frac{1}{(x-1)^2(x^2+1)^2}$ |  | 短display待判定 | 1529:\frac{1}{A^2B^2} =\frac{B-3(x+1)A}{8A^2} +\frac{3(x+1)^2B-(x+1)^3A}{8B^2}. \| 1546:\frac{1}{(x-1)^2(x^2+1)^2} =-\frac{1}{2(x-1)} +\frac{1}{4(x-1)^2} +\frac{2x+1}{4(x^2+1)} +\fr | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 5 | 1558 | 不定积分 | 习题 | 分解 $\frac{2x^2 + 3}{(x-1)(x^2+x+1)}$ |  | 跳步关键词,短display待判定 | 于是; 1560:A=x^2+x+1,\qquad B=x-1,\qquad P(x)=2x^2+3. \| 1586:F(x)=\frac{5}{3(x-1)} +\frac{x-4}{3(x^2+x+1)}. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 6 | 1595 | 不定积分 | 习题 | 分解 $\frac{x^5}{(x^2+1)^3}$ |  | 短display待判定 | 1597:x^5=x(x^2)^2=x(t-1)^2=x(t^2-2t+1). | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 7 | 1614 | 不定积分 | 习题 | 分解 $\frac{x}{(x-1)^2(x+1)^2}$ |  | 跳步关键词,短display待判定 | 于是; 1636:F(x)=\frac{1}{4(x-1)^2} -\frac{1}{4(x+1)^2}. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 8 | 1645 | 不定积分 | 习题 | 分解 $\frac{x^2}{(x^2+1)^2(x^2+x+1)}$ |  | 跳步关键词,短display待判定 | 于是; 1655:\frac{1}{AB} =\frac{(x+1)B-xA}{AB} =\frac{x+1}{A}-\frac{x}{B}. \| 1661:\frac{1}{AB^2}=\frac{x+1}{AB}-\frac{x}{B^2}. \| 1672:\frac{1}{AB^2} =\frac{(x+1)^2}{A} -\frac{x^2+x}{B | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 9 | 1700 | 不定积分 | 习题 | 分解 $F(x) = \frac{1}{x(x-1)(x^2+1)}$ |  | 跳步关键词,短display待判定 | 可得,于是; 1712:B=x^2+1,\qquad C=x-1,\qquad P(x)=x^2-x+1. \| 1734:\frac{P(x)}{BC} =\frac{1}{2(x-1)} +\frac{x-1}{2(x^2+1)}. \| 1740:F(x) =-\frac1x +\frac{1}{2(x-1)} +\frac{x-1}{2(x^2+1)}. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 10 | 1751 | 不定积分 | 习题 | 分解 $\frac{x^3}{(x-1)(x+1)(x^2+x+1)}$ |  | 短display待判定 | 1753:F(x)=\frac{A}{x-1} +\frac{B}{x+1} +\frac{Cx+D}{x^2+x+1}. \| 1759:A=\frac{1^3}{(1+1)(1+1+1)}=\frac16, \qquad B=\frac{(-1)^3}{(-1-1)(1-1+1)}=\frac12. \| 1779:3x^3-(2x-1)(x^2+x+1)  | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 13 | 1823 | 不定积分 | 习题 | 含有 $ax+b$ 的积分 - 3 |  | 跳步关键词 | 于是 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 14 | 1837 | 不定积分 | 习题 | 含有 $ax+b$ 的积分 - 4 |  | 跳步关键词 | 于是 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 15 | 1851 | 不定积分 | 习题 | 含有 $ax+b$ 的积分 - 5 |  | 短display待判定 | 1853:\frac{1}{x(ax+b)} =\frac{1}{b}\left(\frac{1}{x}-\frac{a}{ax+b}\right). \| 1865:\int \frac{\mathrm{d}x}{a x^2} =-\frac{1}{a x}+C. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 16 | 1874 | 不定积分 | 习题 | 含有 $ax+b$ 的积分 - 6 |  | 短display待判定 | 1876:\frac{1}{x^2(ax+b)} =\frac{1}{b}\left(\frac{1}{x^2}-\frac{a}{x(ax+b)}\right), \| 1888:\int \frac{\mathrm{d}x}{a x^3} =-\frac{1}{2a x^2}+C. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 17 | 1897 | 不定积分 | 习题 | 含有 $ax+b$ 的积分 - 7 |  | 跳步关键词 | 于是 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 18 | 1911 | 不定积分 | 习题 | 含有 $ax+b$ 的积分 - 8 |  | 跳步关键词 | 于是 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 19 | 1925 | 不定积分 | 习题 | 含有 $ax+b$ 的积分 - 9 |  | 跳步关键词,短display待判定 | 于是; 1927:\frac{1}{x(ax+b)^2} =\frac{1}{b}\left(\frac{1}{x(ax+b)}-\frac{a}{(ax+b)^2}\right). \| 1939:\int \frac{\mathrm{d}x}{a^2x^3} =-\frac{1}{2a^2x^2}+C. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 20 | 1949 | 不定积分 | 习题 | 含有 $\sqrt{ax+b}$ 的积分 - 10 |  | 跳步关键词,短display待判定 | 直接; 1951:y^2=ax+b,\qquad x=\frac{y^2-b}{a},\qquad \mathrm{d}x=\frac{2y}{a}\,\mathrm{d}y. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 21 | 1968 | 不定积分 | 习题 | 含有 $\sqrt{ax+b}$ 的积分 - 11 |  | 短display待判定 | 1970:y^2=ax+b,\qquad x=\frac{y^2-b}{a},\qquad \mathrm{d}x=\frac{2y}{a}\,\mathrm{d}y. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 22 | 1988 | 不定积分 | 习题 | 含有 $\sqrt{ax+b}$ 的积分 - 12 |  | 短display待判定 | 1990:y^2=ax+b,\qquad x=\frac{y^2-b}{a},\qquad \mathrm{d}x=\frac{2y}{a}\,\mathrm{d}y. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 23 | 2008 | 不定积分 | 习题 | 含有 $\sqrt{ax+b}$ 的积分 - 13 |  | 短display待判定 | 2010:y^2=ax+b,\qquad x=\frac{y^2-b}{a},\qquad \mathrm{d}x=\frac{2y}{a}\,\mathrm{d}y. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 24 | 2028 | 不定积分 | 习题 | 含有 $\sqrt{ax+b}$ 的积分 - 14 |  | 短display待判定 | 2030:y^2=ax+b,\qquad x=\frac{y^2-b}{a},\qquad \mathrm{d}x=\frac{2y}{a}\,\mathrm{d}y. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 25 | 2048 | 不定积分 | 习题 | 含有 $\sqrt{ax+b}$ 的积分 - 15 |  | 跳步关键词,短display待判定 | 于是; 2050:y^2=ax+b,\qquad x=\frac{y^2-b}{a},\qquad \mathrm{d}x=\frac{2y}{a}\,\mathrm{d}y. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 26 | 2080 | 不定积分 | 习题 | 含有 $\sqrt{ax+b}$ 的积分 - 16 |  | 短display待判定 | 2082:y^2=ax+b,\qquad x=\frac{y^2-b}{a},\qquad \mathrm{d}x=\frac{2y}{a}\,\mathrm{d}y. \| 2087:\int \frac{\mathrm{d}x}{x^2\sqrt{ax+b}} =\int \frac{2a}{(y^2-b)^2}\,\mathrm{d}y. \| 2092: | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 27 | 2119 | 不定积分 | 习题 | 含有 $\sqrt{ax+b}$ 的积分 - 17 |  | 跳步关键词,短display待判定 | 直接; 2121:y^2=ax+b,\qquad x=\frac{y^2-b}{a},\qquad \mathrm{d}x=\frac{2y}{a}\,\mathrm{d}y. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 28 | 2141 | 不定积分 | 习题 | 含有 $\sqrt{ax+b}$ 的积分 - 18 |  | 跳步关键词,短display待判定 | 直接; 2143:y^2=ax+b,\qquad x=\frac{y^2-b}{a},\qquad \mathrm{d}x=\frac{2y}{a}\,\mathrm{d}y. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 29 | 2164 | 不定积分 | 习题 | 含有 $x^2\pm a^2$ 的积分 - 19 |  | 短display待判定 | 2166:u=\frac{x}{a},\qquad \mathrm{d}u=\frac{1}{a}\,\mathrm{d}x. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 30 | 2181 | 不定积分 | 习题 | 含有 $x^2\pm a^2$ 的积分 - 20 |  | 短display待判定 | 2183:I_n=\int \frac{\mathrm{d}x}{(x^2+a^2)^n}. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 31 | 2214 | 不定积分 | 习题 | 含有 $x^2\pm a^2$ 的积分 - 21 |  | 跳步关键词,短display待判定 | 于是; 2216:\frac{1}{x^2-a^2}=\frac{A}{x-a}+\frac{B}{x+a}. \| 2220:A=\frac{1}{2a},\qquad B=-\frac{1}{2a}. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 32 | 2236 | 不定积分 | 习题 | 含有 $ax^2+b$ 的积分 - 22 |  | 跳步关键词,短display待判定 | 直接; 2257:\int \frac{\mathrm{d}x}{a x^2} =-\frac{1}{a x}+C. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 34 | 2281 | 不定积分 | 习题 | 含有 $ax^2+b$ 的积分 - 24 |  | 跳步关键词 | 直接 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 35 | 2297 | 不定积分 | 习题 | 含有 $ax^2+b$ 的积分 - 25 |  | 跳步关键词,短display待判定 | 直接; 2311:\int \frac{\mathrm{d}x}{a x^3} =-\frac{1}{2a x^2}+C. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 36 | 2320 | 不定积分 | 习题 | 含有 $ax^2+b$ 的积分 - 26 |  | 短display待判定 | 2331:\int \frac{\mathrm{d}x}{a x^4} =-\frac{1}{3a x^3}+C. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 37 | 2340 | 不定积分 | 习题 | 含有 $ax^2+b$ 的积分 - 27 |  | 短display待判定 | 2358:\int \frac{\mathrm{d}x}{a x^5} =-\frac{1}{4a x^4}+C. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 38 | 2367 | 不定积分 | 习题 | 含有 $ax^2+b$ 的积分 - 28 |  | 短display待判定 | 2387:\int \frac{\mathrm{d}x}{(a x^2)^2} =\int \frac{\mathrm{d}x}{a^2x^4} =-\frac{1}{3a^2x^3}+C. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 39 | 2398 | 不定积分 | 习题 | 含有 $ax^2+bx+c$ 的积分 - 29 |  | 短display待判定 | 2435:ax^2+bx+c=\frac{(2ax+b)^2}{4a}, | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 40 | 2450 | 不定积分 | 习题 | 含有 $ax^2+bx+c$ 的积分 - 30 |  | 跳步关键词 | 于是 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 41 | 2469 | 不定积分 | 习题 | 含有 $\sqrt{x^2+a^2}$ 的积分 - 31 |  | 跳步关键词,短display待判定 | 可得; 2471:y=\sqrt{x^2+a^2},\qquad y^2-x^2=a^2,\qquad x\,\mathrm{d}x=y\,\mathrm{d}y. \| 2485:\int \frac{\mathrm{d}x}{\sqrt{x^2+a^2}} =\int \frac{\mathrm{d}x}{y} =\ln(x+y)+C =\ln\!\lef | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 42 | 2496 | 不定积分 | 习题 | 含有 $\sqrt{x^2+a^2}$ 的积分 - 32 |  | 短display待判定 | 2507:\int \frac{\mathrm{d}x}{\sqrt{(x^2+a^2)^3}} =\int \frac{\mathrm{d}x}{y^3} =\frac{1}{a^2}\frac{x}{y}+C =\frac{x}{a^2\sqrt{x^2+a^2}}+C. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 43 | 2518 | 不定积分 | 习题 | 含有 $\sqrt{x^2+a^2}$ 的积分 - 33 |  | 跳步关键词 | 于是 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 44 | 2533 | 不定积分 | 习题 | 含有 $\sqrt{x^2+a^2}$ 的积分 - 34 |  | 跳步关键词 | 于是 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 45 | 2548 | 不定积分 | 习题 | 含有 $\sqrt{x^2+a^2}$ 的积分 - 35 |  | 短display待判定 | 2550:K=\int \frac{x^2}{y}\,\mathrm{d}x,\qquad L=\int \frac{\mathrm{d}x}{y}. \| 2568:\int \frac{x^2}{\sqrt{x^2+a^2}}\,\mathrm{d}x =\frac{x}{2}\sqrt{x^2+a^2} -\frac{a^2}{2}\ln\!\left( | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 47 | 2595 | 不定积分 | 习题 | 含有 $\sqrt{x^2+a^2}$ 的积分 - 37 |  | 跳步关键词,短display待判定 | 可得; 2597:\frac{\mathrm{d}x}{y}=\frac{\mathrm{d}y}{x},\qquad x^2=y^2-a^2, \| 2609:\frac{1}{2a}\ln\left\|\frac{y-a}{y+a}\right\| =\frac{1}{a}\ln\left\|\frac{y-a}{x}\right\|. \| 2614:\int \ | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 48 | 2623 | 不定积分 | 习题 | 含有 $\sqrt{x^2+a^2}$ 的积分 - 38 |  | 短display待判定 | 2633:\int \frac{\mathrm{d}x}{x^2\sqrt{x^2+a^2}} =-\frac{1}{a^2}\frac{y}{x}+C =-\frac{\sqrt{x^2+a^2}}{a^2x}+C. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 49 | 2643 | 不定积分 | 习题 | 含有 $\sqrt{x^2+a^2}$ 的积分 - 39 |  | 短display待判定 | 2661:\int \sqrt{x^2+a^2}\,\mathrm{d}x =\frac{x}{2}\sqrt{x^2+a^2} +\frac{a^2}{2}\ln\!\left(x+\sqrt{x^2+a^2}\right)+C. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 50 | 2671 | 不定积分 | 习题 | 含有 $\sqrt{x^2+a^2}$ 的积分 - 40 |  | 跳步关键词,短display待判定 | 于是; 2673:I_1=\int y\,\mathrm{d}x,\qquad I_2=\int y^3\,\mathrm{d}x. \| 2693:I_2=xy^3-3(I_2-a^2I_1), \qquad 4I_2=xy^3+3a^2I_1. \| 2699:I_1=\frac{1}{2}xy+\frac{a^2}{2}\ln(x+y) | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 51 | 2715 | 不定积分 | 习题 | 含有 $\sqrt{x^2+a^2}$ 的积分 - 41 |  | 跳步关键词 | 于是 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 52 | 2729 | 不定积分 | 习题 | 含有 $\sqrt{x^2+a^2}$ 的积分 - 42 |  | 短display待判定 | 2731:I_1=\int y\,\mathrm{d}x,\qquad I_2=\int y^3\,\mathrm{d}x. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 53 | 2757 | 不定积分 | 习题 | 含有 $\sqrt{x^2+a^2}$ 的积分 - 43 |  | 短display待判定 | 2769:\int \frac{\sqrt{x^2+a^2}}{x}\,\mathrm{d}x =\sqrt{x^2+a^2} +a\ln\left\|\frac{\sqrt{x^2+a^2}-a}{x}\right\|+C. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 55 | 2796 | 不定积分 | 习题 | 含有 $\sqrt{x^2-a^2}$ 的积分 - 45 |  | 跳步关键词,短display待判定 | 可得; 2798:y=\sqrt{x^2-a^2},\qquad x^2-y^2=a^2,\qquad x\,\mathrm{d}x=y\,\mathrm{d}y. \| 2810:\int \frac{\mathrm{d}x}{\sqrt{x^2-a^2}} =\int \frac{\mathrm{d}x}{y} =\ln\|x+y\|+C =\ln\!\lef | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 56 | 2821 | 不定积分 | 习题 | 含有 $\sqrt{x^2-a^2}$ 的积分 - 46 |  | 短display待判定 | 2831:\int \frac{\mathrm{d}x}{\sqrt{(x^2-a^2)^3}} =\int \frac{\mathrm{d}x}{y^3} =-\frac{x}{a^2y}+C =-\frac{x}{a^2\sqrt{x^2-a^2}}+C. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 57 | 2842 | 不定积分 | 习题 | 含有 $\sqrt{x^2-a^2}$ 的积分 - 47 |  | 跳步关键词 | 于是 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 58 | 2857 | 不定积分 | 习题 | 含有 $\sqrt{x^2-a^2}$ 的积分 - 48 |  | 跳步关键词 | 于是 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 59 | 2872 | 不定积分 | 习题 | 含有 $\sqrt{x^2-a^2}$ 的积分 - 49 |  | 短display待判定 | 2874:y=\sqrt{x^2-a^2},\qquad L=\int \frac{\mathrm{d}x}{y},\qquad K=\int \frac{x^2}{y}\,\mathrm{d}x. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 61 | 2917 | 不定积分 | 习题 | 含有 $\sqrt{x^2-a^2}$ 的积分 - 51 |  | 跳步关键词,短display待判定 | 可得; 2919:\frac{\mathrm{d}x}{y}=\frac{\mathrm{d}y}{x},\qquad x^2=y^2+a^2, | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 62 | 2936 | 不定积分 | 习题 | 含有 $\sqrt{x^2-a^2}$ 的积分 - 52 |  | 短display待判定 | 2946:\int \frac{\mathrm{d}x}{x^2\sqrt{x^2-a^2}} =\frac{1}{a^2}\frac{y}{x}+C =\frac{\sqrt{x^2-a^2}}{a^2x}+C. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 63 | 2956 | 不定积分 | 习题 | 含有 $\sqrt{x^2-a^2}$ 的积分 - 53 |  | 短display待判定 | 2958:I_1=\int y\,\mathrm{d}x,\qquad L=\int \frac{\mathrm{d}x}{y}. \| 2976:\int \sqrt{x^2-a^2}\,\mathrm{d}x =\frac{x}{2}\sqrt{x^2-a^2} -\frac{a^2}{2}\ln\!\left\|x+\sqrt{x^2-a^2}\right | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 64 | 2986 | 不定积分 | 习题 | 含有 $\sqrt{x^2-a^2}$ 的积分 - 54 |  | 跳步关键词,短display待判定 | 于是; 2988:I_1=\int y\,\mathrm{d}x,\qquad I_2=\int y^3\,\mathrm{d}x. \| 3009:I_2=xy^3-3(I_2+a^2I_1), \qquad 4I_2=xy^3-3a^2I_1. \| 3015:I_1=\frac{1}{2}xy-\frac{a^2}{2}\ln\|x+y\| | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 65 | 3031 | 不定积分 | 习题 | 含有 $\sqrt{x^2-a^2}$ 的积分 - 55 |  | 跳步关键词 | 于是 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 66 | 3045 | 不定积分 | 习题 | 含有 $\sqrt{x^2-a^2}$ 的积分 - 56 |  | 短display待判定 | 3047:I_1=\int y\,\mathrm{d}x,\qquad I_2=\int y^3\,\mathrm{d}x. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 67 | 3073 | 不定积分 | 习题 | 含有 $\sqrt{x^2-a^2}$ 的积分 - 57 |  | 短display待判定 | 3084:\int \frac{\sqrt{x^2-a^2}}{x}\,\mathrm{d}x =\sqrt{x^2-a^2}-a\arccos\frac{a}{\|x\|}+C. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 69 | 3111 | 不定积分 | 习题 | 含有 $\sqrt{a^2-x^2}$ 的积分 - 59 |  | 短display待判定 | 3113:y=\sqrt{a^2-x^2},\qquad x^2+y^2=a^2,\qquad x\,\mathrm{d}x=-y\,\mathrm{d}y. \| 3118:\mathrm{d}\arcsin\frac{x}{a} =\frac{\mathrm{d}x}{\sqrt{a^2-x^2}} =\frac{\mathrm{d}x}{y}. \| 31 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 70 | 3133 | 不定积分 | 习题 | 含有 $\sqrt{a^2-x^2}$ 的积分 - 60 |  | 跳步关键词,短display待判定 | 于是; 3144:\int \frac{\mathrm{d}x}{\sqrt{(a^2-x^2)^3}} =\int \frac{\mathrm{d}x}{y^3} =\frac{x}{a^2y}+C =\frac{x}{a^2\sqrt{a^2-x^2}}+C. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 71 | 3155 | 不定积分 | 习题 | 含有 $\sqrt{a^2-x^2}$ 的积分 - 61 |  | 跳步关键词 | 于是 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 72 | 3170 | 不定积分 | 习题 | 含有 $\sqrt{a^2-x^2}$ 的积分 - 62 |  | 跳步关键词 | 于是 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 73 | 3185 | 不定积分 | 习题 | 含有 $\sqrt{a^2-x^2}$ 的积分 - 63 |  | 短display待判定 | 3187:y=\sqrt{a^2-x^2},\qquad L=\int \frac{\mathrm{d}x}{y},\qquad K=\int \frac{x^2}{y}\,\mathrm{d}x. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 75 | 3229 | 不定积分 | 习题 | 含有 $\sqrt{a^2-x^2}$ 的积分 - 65 |  | 跳步关键词,短display待判定 | 可得; 3231:\frac{\mathrm{d}x}{y}=-\frac{\mathrm{d}y}{x},\qquad x^2=a^2-y^2, \| 3243:-\frac{1}{2a}\ln\left\|\frac{a+y}{a-y}\right\| =\frac{1}{a}\ln\left\|\frac{a-y}{x}\right\|. \| 3248:\int | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 76 | 3257 | 不定积分 | 习题 | 含有 $\sqrt{a^2-x^2}$ 的积分 - 66 |  | 短display待判定 | 3267:\int \frac{\mathrm{d}x}{x^2\sqrt{a^2-x^2}} =-\frac{1}{a^2}\frac{y}{x}+C =-\frac{\sqrt{a^2-x^2}}{a^2x}+C. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 77 | 3277 | 不定积分 | 习题 | 含有 $\sqrt{a^2-x^2}$ 的积分 - 67 |  | 短display待判定 | 3279:I_1=\int y\,\mathrm{d}x,\qquad L=\int \frac{\mathrm{d}x}{y}. \| 3293:I_1=\frac{1}{2}xy+\frac{a^2}{2}\arcsin\frac{x}{a}+C. \| 3297:\int \sqrt{a^2-x^2}\,\mathrm{d}x =\frac{x}{2}\s | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 78 | 3307 | 不定积分 | 习题 | 含有 $\sqrt{a^2-x^2}$ 的积分 - 68 |  | 跳步关键词,短display待判定 | 于是; 3309:I_1=\int y\,\mathrm{d}x,\qquad I_2=\int y^3\,\mathrm{d}x. \| 3330:I_2=xy^3-3(I_2-a^2I_1), \qquad 4I_2=xy^3+3a^2I_1. \| 3336:I_1=\frac{1}{2}xy+\frac{a^2}{2}\arcsin\frac{x}{a} | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 79 | 3352 | 不定积分 | 习题 | 含有 $\sqrt{a^2-x^2}$ 的积分 - 69 |  | 跳步关键词 | 于是 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 80 | 3366 | 不定积分 | 习题 | 含有 $\sqrt{a^2-x^2}$ 的积分 - 70 |  | 短display待判定 | 3368:I_1=\int y\,\mathrm{d}x,\qquad I_2=\int y^3\,\mathrm{d}x. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 81 | 3394 | 不定积分 | 习题 | 含有 $\sqrt{a^2-x^2}$ 的积分 - 71 |  | 短display待判定 | 3405:\int \frac{\sqrt{a^2-x^2}}{x}\,\mathrm{d}x =\sqrt{a^2-x^2} +a\ln\left\|\frac{a-\sqrt{a^2-x^2}}{x}\right\|+C. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 83 | 3432 | 不定积分 | 习题 | 含有 $\sqrt{ax^2+bx+c}$ 的积分 - 73 |  | 短display待判定 | 3434:y=\sqrt{ax^2+bx+c},\qquad u=2ax+b,\qquad v=2\sqrt a\,y. \| 3440:v^2-u^2=4ac-b^2,\qquad \mathrm{d}x=\frac{\mathrm{d}u}{2a},\qquad y=\frac{v}{2\sqrt a}. \| 3446:\mathrm{d}\ln\|u+v\| | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 84 | 3464 | 不定积分 | 习题 | 含有 $\sqrt{ax^2+bx+c}$ 的积分 - 74 |  | 跳步关键词,短display待判定 | 可得,于是; 3466:y=\sqrt{ax^2+bx+c},\qquad u=2ax+b,\qquad v=2\sqrt a\,y,\qquad \Delta=4ac-b^2. \| 3473:\mathrm{d}x=\frac{\mathrm{d}u}{2a},\qquad y=\frac{v}{2\sqrt a}. \| 3477:\int v\,\mat | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 86 | 3517 | 不定积分 | 习题 | 含有 $\sqrt{ax^2+bx+c}$ 的积分 - 76 |  | 短display待判定 | 3519:y=\sqrt{c+bx-ax^2},\qquad u=2ax-b,\qquad v=2\sqrt a\,y,\qquad \Delta=b^2+4ac. \| 3526:\mathrm{d}x=\frac{\mathrm{d}u}{2a},\qquad y=\frac{v}{2\sqrt a}. \| 3530:\int\frac{\mathrm{d | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 87 | 3548 | 不定积分 | 习题 | 含有 $\sqrt{ax^2+bx+c}$ 的积分 - 77 |  | 跳步关键词,短display待判定 | 于是; 3550:y=\sqrt{c+bx-ax^2},\qquad u=2ax-b,\qquad v=2\sqrt a\,y,\qquad \Delta=b^2+4ac. \| 3557:\int v\,\mathrm{d}u =\frac12uv+\frac{\Delta}{2}\int\frac{\mathrm{d}u}{v}. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 89 | 3598 | 不定积分 | 习题 | 含有 $\sqrt{\frac{x-a}{x-b}}$ 的积分 - 79 |  | 跳步关键词,短display待判定 | 于是; 3600:p=\sqrt{x-a},\qquad q=\sqrt{x-b}, \| 3604:p^2-q^2=b-a,\qquad \mathrm{d}x=2p\,\mathrm{d}p=2q\,\mathrm{d}q. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 90 | 3626 | 不定积分 | 习题 | 含有 $\sqrt{\frac{x-a}{b-x}}$ 的积分 - 80 |  | 短display待判定 | 3628:p^2+q^2=b-a,\qquad \mathrm{d}x=2p\,\mathrm{d}p=-2q\,\mathrm{d}q. \| 3642:\int q\,\mathrm{d}p =\frac12pq+\frac{b-a}{2}\arcsin\frac{p}{\sqrt{b-a}}, \| 3647:\int\sqrt{\frac{x-a}{b- | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 91 | 3657 | 不定积分 | 习题 | 含有 $\sqrt{(x-a)(b-x)}$ 的积分 - 81 |  | 跳步关键词 | 于是 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 92 | 3671 | 不定积分 | 习题 | 含有 $\sqrt{(x-a)(b-x)}$ 的积分 - 82 |  | 跳步关键词,短display待判定 | 于是; 3673:u=p^2-q^2=2x-a-b,\qquad v=2pq=2\sqrt{(x-a)(b-x)}. \| 3678:u^2+v^2=(b-a)^2,\qquad \mathrm{d}u=2\,\mathrm{d}x. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 93 | 3699 | 不定积分 | 习题 | 含有三角函数的积分 - 83 |  | 跳步关键词,短display待判定 | 直接; 3702:\int \sin x\,\mathrm{d}x =-\int \mathrm{d}(\cos x) =-\cos x+C. \| 3710:\int \sin x\,\mathrm{d}x =\int p\,\mathrm{d}x =-\int \mathrm{d}q =-q+C =-\cos x+C. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 94 | 3723 | 不定积分 | 习题 | 含有三角函数的积分 - 84 |  | 跳步关键词,短display待判定 | 可得,直接; 3726:\int \cos x\,\mathrm{d}x =\int \mathrm{d}(\sin x) =\sin x+C. \| 3732:\int \cos x\,\mathrm{d}x =\int q\,\mathrm{d}x =\int \mathrm{d}p =p+C =\sin x+C. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 95 | 3745 | 不定积分 | 习题 | 含有三角函数的积分 - 85 |  | 跳步关键词,短display待判定 | 于是; 3748:\int \tan x\,\mathrm{d}x =\int \frac{\sin x}{\cos x}\,\mathrm{d}x =\int \frac{1}{\cos x}\bigl(-\mathrm{d}(\cos x)\bigr), \| 3754:\int \tan x\,\mathrm{d}x =-\int \frac{\math | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 96 | 3777 | 不定积分 | 习题 | 含有三角函数的积分 - 86 |  | 短display待判定 | 3780:\int \cot x\,\mathrm{d}x =\int \frac{\cos x}{\sin x}\,\mathrm{d}x =\int \frac{1}{\sin x}\mathrm{d}(\sin x). \| 3787:\int \cot x\,\mathrm{d}x =\int \frac{q}{p}\frac{\mathrm{d}p} | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 97 | 3800 | 不定积分 | 习题 | 含有三角函数的积分 - 87 |  | 跳步关键词,短display待判定 | 可得; 3803:\int \sec x\,\mathrm{d}x =\int\frac{\sec x(\sec x+\tan x)} {\sec x+\tan x}\,\mathrm{d}x. \| 3809:\mathrm{d}(\sec x+\tan x) =(\sec x\tan x+\sec^2x)\,\mathrm{d}x, \| 3814:\int | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 98 | 3835 | 不定积分 | 习题 | 含有三角函数的积分 - 88 |  | 跳步关键词,短display待判定 | 可得,于是; 3838:\int \csc x\,\mathrm{d}x =\int\frac{\csc x(\csc x-\cot x)} {\csc x-\cot x}\,\mathrm{d}x. \| 3844:\mathrm{d}(\csc x-\cot x) =(-\csc x\cot x+\csc^2x)\,\mathrm{d}x, \| 3849: | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 99 | 3870 | 不定积分 | 习题 | 含有三角函数的积分 - 89 |  | 短display待判定 | 3876:\int \sec^2 x\,\mathrm{d}x =\int p^2\,\mathrm{d}x =\int \mathrm{d}q =q+C =\tan x+C. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 100 | 3889 | 不定积分 | 习题 | 含有三角函数的积分 - 90 |  | 短display待判定 | 3895:\int \csc^2 x\,\mathrm{d}x =\int p^2\,\mathrm{d}x =-\int \mathrm{d}q =-q+C =-\cot x+C. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 101 | 3908 | 不定积分 | 习题 | 含有三角函数的积分 - 91 |  | 跳步关键词,短display待判定 | 可得; 3914:\int \sec x\tan x\,\mathrm{d}x =\int pq\,\mathrm{d}x =\int \mathrm{d}p =p+C =\sec x+C. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 102 | 3927 | 不定积分 | 习题 | 含有三角函数的积分 - 92 |  | 跳步关键词,短display待判定 | 可得; 3933:\int \csc x\cot x\,\mathrm{d}x =\int pq\,\mathrm{d}x =-\int \mathrm{d}p =-p+C =-\csc x+C. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 103 | 3946 | 不定积分 | 习题 | 含有三角函数的积分 - 93 |  | 跳步关键词,短display待判定 | 可得,于是; 3950:\int \sin^2x\,\mathrm{d}x =\int\frac{1-\cos2x}{2}\,\mathrm{d}x =\frac{x}{2}-\frac{\sin2x}{4}+C. \| 3963:2\int p^2\,\mathrm{d}x =-pq+\int(p^2+q^2)\,\mathrm{d}x =-pq+x. \|  | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 104 | 3980 | 不定积分 | 习题 | 含有三角函数的积分 - 94 |  | 跳步关键词,短display待判定 | 可得,于是; 3983:\int \cos^2x\,\mathrm{d}x =\int\frac{1+\cos2x}{2}\,\mathrm{d}x =\frac{x}{2}+\frac{\sin2x}{4}+C. \| 3996:2\int q^2\,\mathrm{d}x =pq+\int(p^2+q^2)\,\mathrm{d}x =pq+x. \| 40 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 105 | 4013 | 不定积分 | 习题 | 含有三角函数的积分 - 95 |  | 短display待判定 | 4028:I_n =-\frac{\sin^{n-1}x\cos x}{n} +\frac{n-1}{n}I_{n-2}. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 106 | 4049 | 不定积分 | 习题 | 含有三角函数的积分 - 96 |  | 短display待判定 | 4064:I_n =\frac{\cos^{n-1}x\sin x}{n} +\frac{n-1}{n}I_{n-2}. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 107 | 4085 | 不定积分 | 习题 | 含有三角函数的积分 - 97 |  | 跳步关键词,短display待判定 | 整理得; 4100:\int\frac{\mathrm{d}x}{\sin^n x} =-\frac{\cos x}{(n-1)\sin^{n-1}x} +\frac{n-2}{n-1} \int\frac{\mathrm{d}x}{\sin^{n-2}x}. \| 4107:(2-n)I_{2-n}=-p^{1-n}q+(1-n)I_{-n}. \| 4111 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 108 | 4123 | 不定积分 | 习题 | 含有三角函数的积分 - 98 |  | 跳步关键词,短display待判定 | 整理得; 4138:\int\frac{\mathrm{d}x}{\cos^n x} =\frac{\sin x}{(n-1)\cos^{n-1}x} +\frac{n-2}{n-1} \int\frac{\mathrm{d}x}{\cos^{n-2}x}. \| 4145:I_{-n} =\frac{p}{(n-1)q^{n-1}} +\frac{n-2}{ | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 109 | 4157 | 不定积分 | 习题 | 含有三角函数的积分 - 99 |  | 短display待判定 | 4159:I_{m,n}=\int \cos^m x\sin^n x\,\mathrm{d}x, \| 4177:I_{m,n} =\frac{\cos^{m-1}x\sin^{n+1}x}{m+n} +\frac{m-1}{m+n}I_{m-2,n}. \| 4195:I_{m,n} =-\frac{\sin^{n-1}x\cos^{m+1}x}{m+n} + | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 110 | 4211 | 不定积分 | 习题 | 含有三角函数的积分 - 100 |  | 短display待判定 | 4214:\sin ax\cos bx =\frac12\bigl[\sin(a+b)x+\sin(a-b)x\bigr], \| 4219:\int \sin ax\cos bx\,\mathrm{d}x =-\frac{\cos(a+b)x}{2(a+b)} -\frac{\cos(a-b)x}{2(a-b)}+C. \| 4225:\int \sin ax | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 111 | 4246 | 不定积分 | 习题 | 含有三角函数的积分 - 101 |  | 短display待判定 | 4249:\sin ax\sin bx =\frac12\bigl[\cos(a-b)x-\cos(a+b)x\bigr], \| 4254:\int \sin ax\sin bx\,\mathrm{d}x =\frac{\sin(a-b)x}{2(a-b)} -\frac{\sin(a+b)x}{2(a+b)}+C. \| 4260:\int\sin^2 ax | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 112 | 4285 | 不定积分 | 习题 | 含有三角函数的积分 - 102 |  | 短display待判定 | 4288:\cos ax\cos bx =\frac12\bigl[\cos(a+b)x+\cos(a-b)x\bigr], \| 4293:\int \cos ax\cos bx\,\mathrm{d}x =\frac{\sin(a+b)x}{2(a+b)} +\frac{\sin(a-b)x}{2(a-b)}+C. \| 4299:\int\cos ax\c | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 113 | 4321 | 不定积分 | 习题 | 含有三角函数的积分 - 103 |  | 跳步关键词,短display待判定 | 直接,于是; 4324:\int\frac{\mathrm{d}x}{a+b\sin x}=\frac{x}{a}+C. \| 4328:\int\frac{\mathrm{d}x}{b\sin x} =\frac1b\ln\|\csc x-\cot x\|+C. \| 4333:t=\tan\frac{x}{2},\qquad \mathrm{d}x=\frac{ | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 114 | 4387 | 不定积分 | 习题 | 含有三角函数的积分 - 104 |  | 跳步关键词,短display待判定 | 于是; 4390:\int\frac{\mathrm{d}x}{a+b\cos x}=\frac{x}{a}+C. \| 4394:\int\frac{\mathrm{d}x}{b\cos x} =\frac1b\ln\|\sec x+\tan x\|+C. \| 4399:t=\tan\frac{x}{2},\qquad \mathrm{d}x=\frac{2\, | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 115 | 4454 | 不定积分 | 习题 | 含有三角函数的积分 - 105 |  | 跳步关键词,短display待判定 | 于是; 4457:\int \frac{\mathrm{d}x}{a^2\cos^2 x+b^2\sin^2 x} =\frac{1}{a^2}\tan x+C. \| 4462:\int \frac{\mathrm{d}x}{b^2\sin^2 x} =-\frac{1}{b^2}\cot x+C. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 116 | 4490 | 不定积分 | 习题 | 含有三角函数的积分 - 106 |  | 短display待判定 | 4493:\int \frac{\mathrm{d}x}{a^2\cos^2 x-b^2\sin^2 x} =\frac{1}{a^2}\tan x+C. \| 4498:\int \frac{\mathrm{d}x}{-b^2\sin^2 x} =\frac{1}{b^2}\cot x+C. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 117 | 4531 | 不定积分 | 习题 | 含有三角函数的积分 - 110 |  | 跳步关键词,短display待判定 | 直接,于是; 4534:u=x,\qquad \mathrm{d}v=\sin ax\,\mathrm{d}x =\mathrm{d}\left(-\frac{1}{a}\cos ax\right), | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 118 | 4560 | 不定积分 | 习题 | 含有三角函数的积分 - 111 |  | 跳步关键词,短display待判定 | 可得; 4563:\int x\cos ax\,\mathrm{d}x=\int x\,\mathrm{d}x=\frac{x^2}{2}+C. \| 4567:u=x,\qquad \mathrm{d}v=\cos ax\,\mathrm{d}x =\mathrm{d}\left(\frac1a\sin ax\right). | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 119 | 4591 | 不定积分 | 习题 | 含有三角函数的积分 - 112 |  | 跳步关键词,短display待判定 | 可得; 4594:\int \sin ax\,\mathrm{d}x=-\frac{1}{a}\cos ax+C. \| 4598:u=x^n,\qquad \mathrm{d}v=\sin ax\,\mathrm{d}x =\mathrm{d}\left(-\frac{1}{a}\cos ax\right), | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 120 | 4627 | 不定积分 | 习题 | 含有三角函数的积分 - 113 |  | 跳步关键词,短display待判定 | 可得; 4630:\int x^n\cos ax\,\mathrm{d}x =\int x^n\,\mathrm{d}x =\frac{x^{n+1}}{n+1}+C. \| 4636:\int \cos ax\,\mathrm{d}x=\frac{1}{a}\sin ax+C. \| 4640:u=x^n,\qquad \mathrm{d}v=\cos ax\ | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 121 | 4672 | 不定积分 | 习题 | 含有反三角函数的积分 - 114 |  | 跳步关键词,短display待判定 | 直接; 4684:\mathrm{d}\left(\arcsin\frac{x}{a}\right) = \frac{\mathrm{d}x}{\sqrt{a^2-x^2}} = \frac{\mathrm{d}x}{y}. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 123 | 4732 | 不定积分 | 习题 | 含有反三角函数的积分 - 116 |  | 跳步关键词 | 直接 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 124 | 4772 | 不定积分 | 习题 | 含有反三角函数的积分 - 117 |  | 短display待判定 | 4775:\mathrm{d}\left(\arccos\frac{x}{a}\right) =-\frac{1}{\sqrt{a^2-x^2}}\mathrm{d}x. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 125 | 4798 | 不定积分 | 习题 | 含有反三角函数的积分 - 118 |  | 短display待判定 | 4813:\int \frac{\mathrm{d}x}{\sqrt{a^2-x^2}}=-\arccos\frac{x}{a} \| 4818:\int \frac{\mathrm{d}x}{y}=-\arccos\frac{x}{a},\qquad \int y\mathrm{d}x=\frac{1}{2}xy+\frac{a^2}{2}\int\frac | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 127 | 4885 | 不定积分 | 习题 | 含有反三角函数的积分 - 120 |  | 短display待判定 | 4897:\mathrm{d}\left(\arctan\frac{x}{a}\right) =\frac{a}{x^2+a^2}\mathrm{d}x =\frac{a}{y^2}\mathrm{d}x. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 128 | 4915 | 不定积分 | 习题 | 含有反三角函数的积分 - 121 |  | 短display待判定 | 4931:\mathrm{d}\left(\arctan\frac{x}{a}\right)=\frac{a}{y^2}\mathrm{d}x. \| 4935:\int \frac{\mathrm{d}x}{y^2}=\frac{1}{a}\arctan\frac{x}{a} | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 130 | 4995 | 不定积分 | 习题 | 含有指数函数的积分 - 123 |  | 跳步关键词,短display待判定 | 于是; 5000:\int a^x\,\mathrm{d}x =\int e^{x\ln a}\,\mathrm{d}x =\frac{1}{\ln a}e^{x\ln a}+C =\frac{a^x}{\ln a}+C. \| 5007:\left(\frac{a^x}{\ln a}\right)' =\frac{a^x\ln a}{\ln a} =a^x, | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 131 | 5022 | 不定积分 | 习题 | 含有指数函数的积分 - 124 |  | 短display待判定 | 5025:\int e^{ax}\,\mathrm{d}x =\frac1a\int e^{ax}\,\mathrm{d}(ax) =\frac1a e^{ax}+C. \| 5031:\left(\frac1a e^{ax}\right)'=e^{ax}\qquad(a\ne0). | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 132 | 5041 | 不定积分 | 习题 | 含有指数函数的积分 - 125 |  | 短display待判定 | 5044:\int xe^{ax}\,\mathrm{d}x=\int x\,\mathrm{d}x=\frac{x^2}{2}+C. \| 5048:u=x,\qquad \mathrm{d}v=e^{ax}\,\mathrm{d}x =\mathrm{d}\left(\frac1a e^{ax}\right). \| 5064:I_1=\int xe^{ax | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 133 | 5075 | 不定积分 | 习题 | 含有指数函数的积分 - 126 |  | 跳步关键词,短display待判定 | 可得; 5078:\int x^n e^{ax}\,\mathrm{d}x =\int x^n\,\mathrm{d}x =\frac{x^{n+1}}{n+1}+C. \| 5084:I_0=\int e^{ax}\,\mathrm{d}x=\frac1a e^{ax}+C. \| 5097:I_n =e^{ax}\sum_{k=0}^{n} (-1)^k\f | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 134 | 5110 | 不定积分 | 习题 | 含有指数函数的积分 - 127 |  | 短display待判定 | 5113:\int xa^x\,\mathrm{d}x=\int x\,\mathrm{d}x=\frac{x^2}{2}+C. \| 5118:\int x a^x\mathrm{d}x =\frac{x a^x}{\ln a} -\frac{a^x}{(\ln a)^2}+C. \| 5124:\int xa^x\,\mathrm{d}x =a^x\left | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 135 | 5135 | 不定积分 | 习题 | 含有指数函数的积分 - 128 |  | 短display待判定 | 5138:\int x^n a^x\,\mathrm{d}x=\frac{x^{n+1}}{n+1}+C. \| 5142:J_0=\int a^x\,\mathrm{d}x=\frac{a^x}{L}+C. \| 5155:J_n =a^x\sum_{k=0}^{n} (-1)^k\frac{n!}{(n-k)!}\frac{x^{n-k}}{L^{k+1}} | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 136 | 5167 | 不定积分 | 习题 | 含有指数函数的积分 - 129 |  | 跳步关键词,短display待判定 | 直接; 5178:\int e^{ax}\sin bx\,\mathrm{d}x =\frac{e^{ax}}{a^2+b^2} (a\sin bx-b\cos bx)+C. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 137 | 5192 | 不定积分 | 习题 | 含有指数函数的积分 - 130 |  | 短display待判定 | 5196:F' =e^{ax}\bigl[(aA+bB)\cos bx +(aB-bA)\sin bx\bigr]. \| 5203:\int e^{ax}\cos bx\,\mathrm{d}x =\frac{e^{ax}}{a^2+b^2} (a\cos bx+b\sin bx)+C. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 138 | 5215 | 不定积分 | 习题 | 含有指数函数的积分 - 131 |  | 短display待判定 | 5218:U=e^{ax}\sin^n bx,\qquad V=e^{ax}\sin^{n-1}bx\cos bx. \| 5230:aU'-nbV' =(a^2+n^2b^2)U -n(n-1)b^2e^{ax}\sin^{n-2}bx. \| 5236:aU-nbV =(a^2+n^2b^2)I_n -n(n-1)b^2I_{n-2}. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 139 | 5260 | 不定积分 | 习题 | 含有指数函数的积分 - 132 |  | 跳步关键词,短display待判定 | 于是; 5263:U=e^{ax}\cos^n bx,\qquad V=e^{ax}\cos^{n-1}bx\sin bx. \| 5275:aU'+nbV' =(a^2+n^2b^2)U -n(n-1)b^2e^{ax}\cos^{n-2}bx. \| 5281:aU+nbV =(a^2+n^2b^2)I_n -n(n-1)b^2I_{n-2}. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 140 | 5306 | 不定积分 | 习题 | 含有对数函数的积分 - 132(b) |  | 跳步关键词,短display待判定 | 于是; 5318:\int te^t\,\mathrm{d}t =te^t-\int e^t\,\mathrm{d}t =e^t(t-1)+C. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 141 | 5330 | 不定积分 | 习题 | 含有对数函数的积分 - 133 |  | 跳步关键词,短display待判定 | 于是; 5333:\int \frac{\mathrm{d}x}{x\ln x} =\int \frac{\mathrm{d}(\ln x)}{\ln x} =\ln\|\ln x\|+C. \| 5340:\int \frac{\mathrm{d}x}{x\ln x} =\int \frac{e^t\,\mathrm{d}t}{e^t t} =\int\frac | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 142 | 5353 | 不定积分 | 习题 | 含有对数函数的积分 - 134 |  | 短display待判定 | 5367:\int \frac{\ln x}{x}\,\mathrm{d}x =\frac12(\ln x)^2+C. \| 5373:\int x^n\ln x\,\mathrm{d}x =\int t e^{(n+1)t}\,\mathrm{d}t. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 143 | 5395 | 不定积分 | 习题 | 含有对数函数的积分 - 135 |  | 短display待判定 | 5407:\int t^ne^t\,\mathrm{d}t =t^ne^t-n\int t^{n-1}e^t\,\mathrm{d}t. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 144 | 5418 | 不定积分 | 习题 | 含有对数函数的积分 - 136 |  | 短display待判定 | 5442:\int t^n e^{(m+1)t}\,\mathrm{d}t =\frac{t^ne^{(m+1)t}}{m+1} -\frac{n}{m+1} \int t^{n-1}e^{(m+1)t}\,\mathrm{d}t. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 145 | 5456 | 不定积分 | 习题 | 含有双曲函数的积分 - 137 |  | 跳步关键词,短display待判定 | 于是; 5460:\int \sinh x\,\mathrm{d}x =\frac12\int(e^x-e^{-x})\,\mathrm{d}x =\frac12(e^x+e^{-x})+C =\cosh x+C. \| 5469:\int \sinh x\,\mathrm{d}x =\int q\,\mathrm{d}x =\int \mathrm{d}p  | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 146 | 5482 | 不定积分 | 习题 | 含有双曲函数的积分 - 138 |  | 跳步关键词,短display待判定 | 可得; 5486:\int \cosh x\,\mathrm{d}x =\frac12\int(e^x+e^{-x})\,\mathrm{d}x =\frac12(e^x-e^{-x})+C =\sinh x+C. \| 5495:\int \cosh x\,\mathrm{d}x =\int p\,\mathrm{d}x =\int\mathrm{d}q = | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 147 | 5508 | 不定积分 | 习题 | 含有双曲函数的积分 - 139 |  | 短display待判定 | 5511:\int \tanh x\,\mathrm{d}x =\int \frac{\sinh x}{\cosh x}\,\mathrm{d}x =\int \frac{\mathrm{d}(\cosh x)}{\cosh x} =\ln(\cosh x)+C. \| 5518:\int \tanh x\,\mathrm{d}x =\int \frac{q} | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 148 | 5532 | 不定积分 | 习题 | 含有双曲函数的积分 - 140 |  | 跳步关键词,短display待判定 | 于是; 5536:\int\sinh^2x\,\mathrm{d}x =\frac12\int(\cosh2x-1)\,\mathrm{d}x =\frac14\sinh2x-\frac{x}{2}+C. \| 5551:\int\sinh^2x\,\mathrm{d}x =\frac12(pq-x)+C =\frac14\sinh2x-\frac{x}{2} | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 149 | 5562 | 不定积分 | 习题 | 含有双曲函数的积分 - 141 |  | 跳步关键词,短display待判定 | 于是; 5566:\int\cosh^2x\,\mathrm{d}x =\frac12\int(\cosh2x+1)\,\mathrm{d}x =\frac14\sinh2x+\frac{x}{2}+C. \| 5573:\int\cosh^2x\,\mathrm{d}x =\frac12(pq+x)+C =\frac14\sinh2x+\frac{x}{2} | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 150 | 5585 | 不定积分 | 习题 | 定积分 - 142 |  | 短display待判定 | 5598:\int_{-\pi}^{\pi}e^{inx}\,\mathrm{d}x =\left[\frac{e^{inx}}{in}\right]_{-\pi}^{\pi} =\frac{e^{in\pi}-e^{-in\pi}}{in}=0. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 151 | 5610 | 不定积分 | 习题 | 定积分 - 143 |  | 跳步关键词,短display待判定 | 直接,于是; 5614:\cos mx\sin nx =\frac12\bigl[\sin(n+m)x+\sin(n-m)x\bigr]. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 152 | 5634 | 不定积分 | 习题 | 定积分 - 144 |  | 短display待判定 | 5637:\cos mx\cos nx =\frac12\bigl[\cos(m+n)x+\cos(m-n)x\bigr]. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 153 | 5662 | 不定积分 | 习题 | 定积分 - 145 |  | 短display待判定 | 5665:\sin mx\sin nx =\frac12\bigl[\cos(m-n)x-\cos(m+n)x\bigr]. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 154 | 5690 | 不定积分 | 习题 | 定积分 - 146 |  | 短display待判定 | 5693:\sin mx\sin nx =\frac12\bigl[\cos(m-n)x-\cos(m+n)x\bigr]. \| 5698:\int_0^\pi\sin^2 mx\,\mathrm{d}x =\frac12\int_0^\pi(1-\cos2mx)\,\mathrm{d}x =\frac{\pi}{2}. \| 5704:\cos mx\cos | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 155 | 5735 | 不定积分 | 习题 | 定积分 - 147 |  | 跳步关键词,短display待判定 | 整理得; 5738:\int_0^{\pi/2}\cos^n x\,\mathrm{d}x =\int_0^{\pi/2}\sin^n t\,\mathrm{d}t. \| 5745:p^2+q^2=1,\qquad \mathrm{d}p=q\,\mathrm{d}x,\qquad \mathrm{d}q=-p\,\mathrm{d}x. \| 5751:x= | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 156 | 5803 | 微分方程 | 知识讲解 | 已知通解 $y=c_1\mathrm{e}^{-x}+c_2\mathrm{e}^{2x}$，求其所满足的微分方程。 | 微分方程 | 跳步关键词,短display待判定 | 整理得; 5805:y'=-c_1\mathrm{e}^{-x}+2c_2\mathrm{e}^{2x},\qquad y''=c_1\mathrm{e}^{-x}+4c_2\mathrm{e}^{2x}. \| 5810:y+y''=5c_2\mathrm{e}^{2x},\qquad y'-y=-3c_2\mathrm{e}^{2x} | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 157 | 5832 | 微分方程 | 知识讲解 | 求 $\displaystyle\frac{\mathrm{d}y}{\mathrm{d}x}=-\frac{x}{y}$ 的通解。 | 微分方程 | 短display待判定 | 5835:\int y\,\mathrm{d}y=-\int x\,\mathrm{d}x,\qquad \frac{1}{2}y^{2}=-\frac{1}{2}x^{2}+C. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 158 | 5846 | 微分方程 | 知识讲解 | 求方程 $x^{2}y\,\mathrm{d}y+\sqrt{1-y^{2}}\,\mathrm{d}x=0$ 的全部解。 | 微分方程 | 短display待判定 | 5848:-\frac{y\,\mathrm{d}y}{\sqrt{1-y^{2}}} =\frac{\mathrm{d}x}{x^{2}}. \| 5853:\sqrt{1-y^{2}}=-\frac{1}{x}+C, \| 5860:\boxed{\sqrt{1-y^{2}}+\frac{1}{x}=C \quad (x\neq0,\ \|y\|<1)}, \q | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 159 | 5870 | 微分方程 | 知识讲解 | 求 $\displaystyle\frac{\mathrm{d}y}{\mathrm{d}x}=y^{2}\cos x$ 满足初始条件 $y(0)=1$ 的特解 | 微分方程 | 短display待判定 | 5877:\boxed{y=\frac{1}{1-\sin x}},\qquad x\neq\frac{\pi}{2}+2k\pi. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 160 | 5885 | 微分方程 | 知识讲解 | 求 $\displaystyle\frac{\mathrm{d}y}{\mathrm{d}x}=p(x)\,y$ 的通解，其中 $p(x)$ 是连续函数。 | 微分方程 | 短display待判定 | 5887:\int\frac{\mathrm{d}y}{y} =\int p(x)\,\mathrm{d}x, \qquad \ln\|y\|=\int p(x)\,\mathrm{d}x+\bar{C}. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 161 | 5927 | 微分方程 | 知识讲解 | 求 $\displaystyle\frac{\mathrm{d}y}{\mathrm{d}x}=\frac{y}{x}+\tan\frac{y}{x}$ 的通解 | 微分方程 | 跳步关键词,短display待判定 | 于是; 5937:\frac{\mathrm{d}u}{\tan u} =\frac{\mathrm{d}x}{x}, \qquad \frac{\cos u}{\sin u}\mathrm{d}u =\frac{\mathrm{d}x}{x}. \| 5945:\int \frac{\mathrm{d}(\sin u)}{\sin u} =\int \fra | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 162 | 5967 | 微分方程 | 知识讲解 | 求解 $(x+y)\,\mathrm{d}x-(y-x)\,\mathrm{d}y=0$。 | 微分方程 | 短display待判定 | 5971:\frac{\mathrm{d}y}{\mathrm{d}x} = \frac{x+y}{y-x} = \frac{1 + \frac{y}{x}}{\frac{y}{x} - 1}. \| 5979:(x+ux)\,\mathrm{d}x -(ux-x)(u\,\mathrm{d}x+x\,\mathrm{d}u)=0. \| 5996:\frac{ | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 163 | 6027 | 微分方程 | 知识讲解 | 求解 $x\,\mathrm{d}y-y\,\mathrm{d}x=\sqrt{x^{2}+y^{2}}\,\mathrm{d}x$。 | 微分方程 | 跳步关键词,短display待判定 | 同理,直接; 6033:\frac{\mathrm{d}y}{\mathrm{d}x} =\frac{y}{x}+\frac{\sqrt{x^2+y^2}}{x} =\frac{y}{x}+\sqrt{1+\left(\frac{y}{x}\right)^2}. \| 6041:u+x\frac{\mathrm{d}u}{\mathrm{d}x} =u+\sq | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 164 | 6085 | 微分方程 | 知识讲解 | 求解方程 $\displaystyle\frac{\mathrm{d}y}{\mathrm{d}x}=\frac{a_1x+b_1y+c_1}{a_2x+b_2 |  | 跳步关键词,短display待判定 | 代入得,直接; 6091:\frac{\mathrm{d}y}{\mathrm{d}x} =\frac{a_1x+b_1y}{a_2x+b_2y}. \| 6096:u+x\frac{\mathrm{d}u}{\mathrm{d}x} =\frac{a_1+b_1u}{a_2+b_2u}. \| 6108:a_1x+b_1y=\lambda L,\qquad a | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 165 | 6152 | 微分方程 | 知识讲解 | 求解 $\displaystyle\frac{\mathrm{d}y}{\mathrm{d}x}=\frac{x-y+1}{x+y-3}$。 |  | 跳步关键词,短display待判定 | 化简得; 6166:u+X\frac{\mathrm{d}u}{\mathrm{d}X} = \frac{X-uX}{X+uX} = \frac{1-u}{1+u}. \| 6174:-\frac{1}{2} \int \frac{\mathrm{d}(1-2u-u^2)}{1-2u-u^2} = \int \frac{\mathrm{d}X}{X}. \| 6 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 166 | 6210 | 微分方程 | 知识讲解 | 求解初值问题 \[ \begin{cases} | 微分方程 | 跳步关键词,短display待判定 | 显然,整理得,于是; 6214:\frac{\mathrm{d}y}{\mathrm{d}x} =-\frac{x^2+2xy-y^2}{y^2+2xy-x^2}. \| 6219:\frac{\mathrm{d}y}{\mathrm{d}x} =\frac{(y/x)^2 - 2(y/x) - 1}{(y/x)^2 + 2(y/x) - 1}. \| 6225 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 167 | 6307 | 微分方程 | 知识讲解 | 求解：(1) $f(xy)y\,\mathrm{d}x+g(xy)x\,\mathrm{d}y=0$； \quad (2) $\displaystyle\fra | 微分方程 | 短display待判定 | 6312:x\,\mathrm{d}y = \mathrm{d}u - y\,\mathrm{d}x = \mathrm{d}u - \frac{u}{x}\,\mathrm{d}x. \| 6317:f(u)\frac{u}{x}\,\mathrm{d}x +g(u)\left(\mathrm{d}u-\frac{u}{x}\,\mathrm{d}x\rig | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 168 | 6407 | 微分方程 | 知识讲解 | 求方程 $\displaystyle\frac{\mathrm{d}y}{\mathrm{d}x}-\frac{y}{x}=x^{2}$ 的通解。 | 微分方程 | 跳步关键词,短display待判定 | 直接,略,于是; 6424:\frac{y}{x}=\int x\,\mathrm{d}x =\frac{x^{2}}{2}+C_0. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 169 | 6436 | 微分方程 | 知识讲解 | 解初值问题 $\begin{cases}(x^{2}-1)y'+2xy=\cos x,\\ y(0)=1.\end{cases}$ | 微分方程,极值/拉格朗日 | 跳步关键词,短display待判定 | 直接; 6444:(x^2-1)y=\int \cos x\,\mathrm{d}x=\sin x+C_0,\qquad y=\frac{\sin x+C_0}{x^2-1}. \| 6449:\boxed{y=\frac{\sin x - 1}{x^{2}-1} = \frac{1-\sin x}{1-x^{2}}}. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 170 | 6459 | 微分方程 | 知识讲解 | 解方程 $y\ln y\,\mathrm{d}x+(x-\ln y)\,\mathrm{d}y=0$。 | 微分方程 | 短display待判定 | 6465:y\ln y\frac{\mathrm{d}x}{\mathrm{d}y}+(x-\ln y)=0 \implies \frac{\mathrm{d}x}{\mathrm{d}y}+\frac{1}{y\ln y}x=\frac{1}{y}. \| 6488:x\ln y=\int \frac{\ln y}{y}\,\mathrm{d}y =\int | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 171 | 6506 | 微分方程 | 知识讲解 | 质点在驱动力与阻力下的运动 | 微分方程 | 短display待判定 | 6511:m\frac{\mathrm{d}v}{\mathrm{d}t}=k_1t-k_2v,\qquad v(0)=0,\qquad \frac{\mathrm{d}v}{\mathrm{d}t}+\frac{k_2}{m}v=\frac{k_1}{m}t. \| 6519:\frac{\mathrm{d}v}{v}=-\frac{k_2}{m}\,\ma | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 172 | 6573 | 微分方程 | 知识讲解 | 解方程 $\displaystyle\frac{\mathrm{d}y}{\mathrm{d}x}=\frac{4}{x}y+x\sqrt{y}\;(y>0,x | 微分方程 | 短display待判定 | 6576:\frac{\mathrm{d}y}{\mathrm{d}x}-\frac{4}{x}y=xy^{\frac{1}{2}}. \| 6582:y^{-\frac{1}{2}}\frac{\mathrm{d}y}{\mathrm{d}x} -\frac{4}{x}y^{\frac{1}{2}}=x,\qquad z=y^{\frac{1}{2}},\q | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 173 | 6717 | 微分方程 | 知识讲解 | 用 $X(x)Y(y)$ 积分因子看换元题 | 微分方程 | 跳步关键词,短display待判定 | 于是; 6720:\left(-\frac1x-\mathrm e^y\right)\mathrm{d}x+\mathrm{d}y=0, \| 6724:M=-\frac1x-\mathrm e^y,\qquad N=1,\qquad M_y-N_x=-\mathrm e^y. \| 6728:N\frac{X'}{X}-M\frac{Y'}{Y}=M_y-N_ | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 174 | 6832 | 微分方程 | 知识讲解 | 换元一例 | 微分方程,隐函数/偏导 | 跳步关键词,短display待判定 | 代入得; 6834:\left(\frac{x}{1+x^2}\tan y-x\right)\mathrm{d}x+\sec^2 y\,\mathrm{d}y=0, \| 6838:\sec^2 y\cdot\frac{X'}{X}-\left(\frac{x}{1+x^2}\tan y-x\right)\dfrac{Y'}{Y}=\frac{x}{1+x^2 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 175 | 6886 | 微分方程 | 知识讲解 | 如图所示的 $R$--$C$ 电路，电容 $C$ 初始无电荷。 合上开关 K 后电池 $E$ 对电容充电，求电压 $u_C$ 随时间的变化规律。 | 微分方程 | 短display待判定 | 6891:I = \frac{\mathrm{d}Q}{\mathrm{d}t} = C\frac{\mathrm{d}u_C}{\mathrm{d}t}. \| 6899:-\ln\|E-u_C\|=\frac{t}{RC}+C_1. \| 6903:E-u_C=K\mathrm{e}^{-\frac{t}{RC}}, \qquad u_C(t)=E-K\math | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 176 | 6921 | 微分方程 | 知识讲解 | 制造探照灯反射镜时要求点光源发出的光经镜面反射后平行射出， 试求反射镜面的几何形状。 | 微分方程 | 长行内公式/排版风险,短display待判定 | 6925:215; 6928:\frac{\mathrm{d}y}{\mathrm{d}x} =\frac{r-x}{y} =\frac{y}{r+x} =\frac{y}{x+\sqrt{x^2+y^2}}. \| 6937:\frac{\mathrm{d}x}{\mathrm{d}y} =\frac{x+\sqrt{x^2+y^2}}{y} =\frac{ | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 177 | 6997 | 微分方程 | 知识讲解 | 逐次积分 | 微分方程 | 短display待判定,高风险题解过短 | 7000:\boxed{y=\frac{1}{27}\mathrm{e}^{3x}+\sin x+\frac{C_1}{2}x^{2}+C_2x+C_3}. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 178 | 7008 | 微分方程 | 知识讲解 | 解初值问题 \(\displaystyle y''=\dfrac{3x^{2}}{1+x^{3}}\,y',\quad y\|_{x=0}=1,\quad y'\| | 微分方程 | 跳步关键词,短display待判定 | 代入得; 7010:p'=\frac{3x^{2}}{1+x^{3}}\,p. \| 7015:\frac{\mathrm{d}p}{p}=\frac{3x^{2}\,\mathrm{d}x}{1+x^{3}}, \| 7019:\ln\|p\|=\ln(1+x^{3})+\ln C_1 \implies p=C_{1}(1+x^{3}). | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 179 | 7035 | 微分方程 | 知识讲解 | 求 $y^{(5)}-\dfrac{1}{x}y^{(4)}=0$ 的通解。 | 微分方程 | 跳步关键词 | 于是 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 180 | 7056 | 微分方程 | 知识讲解 | 求 $y''=\dfrac{1+y'^{2}}{2y}$ 的通解。 | 微分方程 | 短display待判定 | 7059:\frac{2p\,\mathrm{d}p}{1+p^{2}}=\frac{\mathrm{d}y}{y}, \qquad \ln(1+p^{2})=\ln\|y\|+\ln\|C\|. \| 7065:p=\pm\sqrt{Cy-1}, \qquad \frac{\mathrm{d}y}{\mathrm{d}x}=\pm\sqrt{Cy-1}. \| 707 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 181 | 7087 | 微分方程 | 知识讲解 | 求 $yy''-y'^{2}=0$ 的通解。 | 微分方程 | 跳步关键词,短display待判定 | 代入得; 7093:\frac{\mathrm{d}p}{p}=\frac{\mathrm{d}y}{y},\qquad p=C_{1}y. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 182 | 7108 | 微分方程 | 知识讲解 | 导弹追击舰船 | 极值/拉格朗日 | 跳步关键词,短display待判定 | 于是; 7116:\int_{0}^{x}\sqrt{1+y'^{2}}\;\mathrm{d}x=5v_{0}t. \| 7122:(1-x)y'+y=\frac15\int_{0}^{x}\sqrt{1+y'^{2}}\;\mathrm{d}x. \| 7128:-y'+(1-x)y''+y'=\frac15\sqrt{1+y'^{2}}, \qquad ( | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 183 | 7160 | 微分方程 | 知识讲解 | 悬链线的形状 |  | 短display待判定 | 7167:H\tan\theta=\rho g\int_{0}^{x}\sqrt{1+y'^{2}}\;\mathrm{d}x. \| 7171:y'=\frac{\rho g}{H}\int_{0}^{x}\sqrt{1+y'^{2}}\;\mathrm{d}x. \| 7177:\frac{\mathrm{d}p}{\mathrm{d}x}=a\sqrt{1 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 184 | 7236 | 微分方程 | 知识讲解 | 算子的计算 |  | 短display待判定 | 7239:L[\cos x] = -\cos x + x \cos x = (x-1) \cos x. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 186 | 7416 | 微分方程 | 知识讲解 | 非齐次通解的构造 | 微分方程 | 短display待判定 | 7422:(y^*)''-y^*=0-(Ax+B)=x. \| 7426:-A=1,\qquad -B=0, | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 187 | 7449 | 微分方程 | 知识讲解 | 非齐次叠加原理应用 | 微分方程 | 短display待判定 | 7456:y = c_{1} \sin x + c_{2} \cos x + x + \frac{1}{2} e^{x}. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 188 | 7495 | 微分方程 | 知识讲解 | 求解 $y''+y=0$。 | 微分方程 | 高风险题解过短 |  | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 189 | 7504 | 微分方程 | 知识讲解 | 求解 $y''-y=0$。 | 微分方程 | 跳步关键词,高风险题解过短 | 可得 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 190 | 7517 | 微分方程 | 知识讲解 | 解初值问题 $\begin{cases} 16y''-24y'+9y=0,\\ | 微分方程 | 短display待判定 | 7522:y'=c_2\,\mathrm{e}^{3x/4}+\frac34(c_1+c_2x)\,\mathrm{e}^{3x/4}. \| 7526:y(0)=c_1=4,\qquad y'(0)=c_2+\tfrac34 c_1=2, | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 191 | 7536 | 微分方程 | 知识讲解 | 求解 $y^{(5)}+2y'''+y'=0$。 | 微分方程 | 短display待判定 | 7546:\boxed{y=c_1+(c_2+c_3x)\cos x+(c_4+c_5x)\sin x}. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 192 | 7574 | 微分方程 | 知识讲解 | 求微分方程 $y''-2y'+2y=x\mathrm{e}^x\cos x$ 的一个特解。 | 微分方程 | 跳步关键词,短display待判定 | 整理得; 7579:y^* = x\mathrm{e}^x\bigl[(Ax+B)\cos x + (Cx+D)\sin x\bigr] = \mathrm{e}^x\bigl[(Ax^2+Bx)\cos x + (Cx^2+Dx)\sin x\bigr] \| 7583:(y^*)'' - 2(y^*)' + 2y^* = \mathrm{e}^x\bigl | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 193 | 7606 | 微分方程 | 知识讲解 | 求 $y''-y=2x\,\mathrm{e}^{x}$ 的通解。 | 微分方程 | 跳步关键词,短display待判定 | 于是; 7609:y^*=x\,\mathrm{e}^x(b_0x+b_1)=\mathrm{e}^x(b_0 x^2+b_1 x). \| 7613:L[\mathrm e^xz]=\mathrm e^x(z''+2z'). \| 7617:z'=2b_0x+b_1,\qquad z''=2b_0. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 194 | 7640 | 微分方程 | 知识讲解 | 求 $y''+4y'+4y=\cos 2x$ 的一个特解。 | 微分方程 | 短display待判定 | 7644:(y^*)'=-2A\sin2x+2B\cos2x, \qquad (y^*)''=-4A\cos2x-4B\sin2x. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 195 | 7717 | 微分方程 | 知识讲解 | 常数变易法的实际应用 | 微分方程 | 跳步关键词,短display待判定 | 直接; 7742:c_1'(x)(\sin^2x+\cos^2x)=1, \qquad c_1'(x)=1. \| 7748:\sin x+c_2'(x)\cos x=0, \qquad c_2'(x)=-\frac{\sin x}{\cos x}=-\tan x. \| 7757:c_2(x)=\int(-\tan x)\,\mathrm{d}x =\int\ | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 196 | 7884 | 微分方程 | 知识讲解 | 降阶法的应用 | 微分方程 | 短display待判定 | 7888:y'' - \frac{2 x}{1-x^{2}} y' + \frac{2}{1-x^{2}} y = 0. \| 7904:e^{-\int P(x) \mathrm{d}x}=e^{-\ln\|1-x^2\|}\sim \frac{1}{1-x^2}. \| 7910:u(x)=\int \frac{1}{x^2}\cdot\frac{1}{1-x^ | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 197 | 8012 | 微分方程 | 知识讲解 | 求解 $x^2y''-2y=x\;(x>0)$。 | 微分方程 | 跳步关键词,短display待判定 | 代入得; 8014:\frac{\mathrm{d}^2 y}{\mathrm{d}t^2}-\frac{\mathrm{d}y}{\mathrm{d}t}-2y=\mathrm{e}^t. \| 8018:xy'=\frac{\mathrm{d}y}{\mathrm{d}t},\qquad x^2y''=\frac{\mathrm{d}^2y}{\mathr | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 199 | 8148 | 微分方程 | 知识讲解 | 消元法 I：重根情形 | 微分方程 | 短display待判定 | 8152:\frac{\mathrm{d}y}{\mathrm{d}t} =-\frac{\mathrm{d}^{2}x}{\mathrm{d}t^{2}}-3\frac{\mathrm{d}x}{\mathrm{d}t}. \| 8157:-\frac{\mathrm{d}^{2}x}{\mathrm{d}t^{2}}-3\frac{\mathrm{d}x} | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 200 | 8199 | 微分方程 | 知识讲解 | 消元法 II：带初值条件的非齐次型转化 | 微分方程 | 短display待判定 | 8203:\frac{\mathrm{d}x}{\mathrm{d}t} =\frac12\left(\frac{\mathrm{d}^{2}y}{\mathrm{d}t^{2}}+\frac{\mathrm{d}y}{\mathrm{d}t}\right). \| 8208:\frac12(y''+y')=\frac32(y'+y)-2y=\frac32y' | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 202 | 8265 | 微分方程 | 习题 | 验证解 | 微分方程 | 高风险题解过短 |  | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 203 | 8273 | 微分方程 | 习题 | 求参数 | 微分方程 | 高风险题解过短 |  | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 204 | 8281 | 微分方程 | 习题 | 求参数 |  | 跳步关键词,短display待判定 | 可得; 8286:9-\omega^2=0, \qquad \omega=\pm3. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 205 | 8304 | 微分方程 | 习题 | 求参数 | 微分方程 | 短display待判定 | 8318:y(\pi)=C_1\sin(\pi-C_2)=C_1\sin C_2=1 \qquad\text{（式1）}, \| 8322:y'(\pi)=C_1\cos(\pi-C_2)=-C_1\cos C_2=0 \qquad\text{（式2）}. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 206 | 8354 | 微分方程 | 习题 | 函数对应微分方程 | 微分方程 | 短display待判定 | 8357:y'=2\cos x,\qquad y''=-2\sin x=-y, \| 8362:y'=2\cos 2x,\qquad y''=-4\sin 2x=-4y, | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 207 | 8386 | 微分方程 | 习题 | 函数对应微分方程 | 微分方程 | 短display待判定 | 8394:x^2y''+2xy'-2y =x^2(6x^{-4})+2x(-2x^{-3})-2x^{-2} =0, | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 208 | 8418 | 微分方程 | 习题 | 曲线族对应微分方程 | 微分方程 | 短display待判定 | 8424:\mathrm{e}^{kx}=\frac{y}{x}, \qquad kx=\ln\frac{y}{x}. \| 8430:\frac{\mathrm{d}y}{\mathrm{d}x} =\frac{y}{x}+\left(\ln\frac{y}{x}\right)\frac{y}{x} =\frac{y}{x}\left(1+\ln\frac{ | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 209 | 8476 | 微分方程 | 习题 | 曲线族对应微分方程 | 微分方程 | 跳步关键词,短display待判定 | 可得,于是; 8481:(y')^2 =4C_1^2(x-C_2)^2 =4C_1\bigl[C_1(x-C_2)^2\bigr] =4C_1y =2yy''. \| 8489:\boxed{2yy''-(y')^2=0}. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 210 | 8506 | 微分方程 | 习题 | 相关概念 | 微分方程 | 跳步关键词,短display待判定 | 于是; 8514:u+x\frac{\mathrm{d}u}{\mathrm{d}x}=\varphi(u), \qquad \frac{\mathrm{d}u}{\mathrm{d}x}=\frac{\varphi(u)-u}{x}, | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 211 | 8526 | 微分方程 | 习题 | 求解方程 | 微分方程 | 短display待判定 | 8528:\frac{\mathrm{d}H}{H-20}=-k\,\mathrm{d}t, \qquad \ln\|H-20\|=-kt+C_1. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 212 | 8539 | 微分方程 | 习题 | 求解方程 | 极值/拉格朗日 | 跳步关键词,短display待判定 | 于是; 8541:\frac{\mathrm{d}P}{\mathrm{d}t}=2P(1-t). \| 8545:\frac{\mathrm{d}P}{P}=2(1-t)\,\mathrm{d}t, \qquad \ln P=2t-t^2+C_1. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 213 | 8567 | 微分方程 | 习题 | 求解方程 | 微分方程 | 跳步关键词,短display待判定 | 于是; 8570:\frac{\mathrm{d}P}{P}=0.02\,\mathrm{d}t, \qquad P=C\mathrm{e}^{0.02t}. \| 8578:\frac{\mathrm{d}y}{y}=-\frac{1}{3}\,\mathrm{d}x, \qquad y=C\mathrm{e}^{-x/3}. \| 8586:\frac{\m | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 214 | 8650 | 微分方程 | 习题 | 求解方程 | 微分方程 | 短display待判定 | 8652:\frac{\mathrm{d}y}{1-y}=\mathrm{d}t, \qquad -\ln\|1-y\|=t+C. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 215 | 8667 | 微分方程 | 习题 | 求解齐次方程 | 微分方程 | 跳步关键词,短display待判定 | 代入得,于是; 8671:u + x\frac{\mathrm{d}u}{\mathrm{d}x} = u\ln u \implies x\frac{\mathrm{d}u}{\mathrm{d}x} = u(\ln u - 1), \qquad \frac{\mathrm{d}u}{u(\ln u - 1)} = \frac{\mathrm{ \| 8679 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 216 | 8755 | 微分方程 | 习题 | 求解齐次方程 |  | 短display待判定 | 8760:\boxed{y=x\sqrt{2\ln x+4}}. \| 8765:\frac{\mathrm{d}y}{\mathrm{d}x} = \frac{y^2-2xy-x^2}{y^2+2xy-x^2}. \| 8770:u+xu'=\frac{u^2-2u-1}{u^2+2u-1}, \qquad xu'=-\frac{(u+1)(u^2+1)}{u | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 217 | 8803 | 微分方程 | 习题 | 求解方程 | 微分方程 | 短display待判定 | 8806:y-x-2=0,\qquad x+y+4=0 \| 8810:\frac{\mathrm{d}Y}{\mathrm{d}X}=\frac{Y-X}{X+Y}. \| 8814:u+X\frac{\mathrm{d}u}{\mathrm{d}X} =\frac{u-1}{1+u}, \qquad \frac{1+u}{1+u^2}\mathrm{d}u= | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 218 | 8868 | 微分方程 | 习题 | 求解方程 | 微分方程 | 短display待判定 | 8871:\frac{y}{\sqrt{1-y^2}}\mathrm{d}y =\frac{1}{3x^2}\mathrm{d}x. \| 8876:-\sqrt{1-y^2}=-\frac{1}{3x}+C, \| 8883:\mathrm{d}\left(\frac{y}{x}\right)=\frac{x\,\mathrm{d}y-y\,\mathrm{d | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 219 | 8908 | 微分方程 | 习题 | 求解方程 | 微分方程 | 跳步关键词,短display待判定 | 直接; 8913:Y_0=y+\frac{x}{y'}=y+x\frac{\mathrm{d}x}{\mathrm{d}y}. \| 8918:y+x\frac{\mathrm{d}x}{\mathrm{d}y} =\pm\sqrt{x^2+y^2}. \| 8925:\frac{\mathrm{d}(x^2+y^2)}{2\sqrt{x^2+y^2}} =\p | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 220 | 8950 | 微分方程 | 习题 | 实际应用题 |  | 跳步关键词,短display待判定 | 于是; 8953:4=k\frac{10}{5}, \qquad k=2. \| 8959:\frac{\mathrm{d}v}{\mathrm{d}t}=\frac{2t}{v}, \qquad v\,\mathrm{d}v=2t\,\mathrm{d}t. \| 8965:\frac{1}{2}v^2=t^2+C, \qquad v^2=2t^2+C_1. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 221 | 8997 | 微分方程 | 习题 | 实际应用题 | 微分方程 | 跳步关键词,短display待判定 | 于是; 9000:\frac{\mathrm{d}P}{\mathrm{d}t}=\lambda P. \| 9004:\frac{\mathrm{d}A}{\mathrm{d}t} =\alpha\frac{\mathrm{d}P}{\mathrm{d}t} =\alpha\lambda P =\lambda A. \| 9014:2\times10^9=10 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 223 | 9058 | 微分方程 | 习题 | 实际应用题 | 微分方程 | 短display待判定 | 9060:\frac{\mathrm{d}R}{\mathrm{d}t}=-kR,\qquad R(t)=C\mathrm{e}^{-kt}. \| 9065:\frac{1}{2}R_0=R_0\mathrm{e}^{-1600k}, \qquad \mathrm{e}^{-1600k}=\frac{1}{2}. \| 9071:k=\frac{\ln 2}{ | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 224 | 9079 | 微分方程 | 习题 | 实际应用题 |  | 短display待判定 | 9081:\frac{\mathrm{d}x}{\mathrm{d}t}=k(a-x)(b-x), \qquad x(0)=0. \| 9087:\frac{\mathrm{d}x}{(a-x)(b-x)}=k\,\mathrm{d}t. \| 9093:\frac{1}{(a-x)(b-x)} =\frac{1}{b-a}\left(\frac{1}{a-x} | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 225 | 9134 | 微分方程 | 习题 | 实际应用题 |  | 跳步关键词,短display待判定 | 于是; 9136:m\frac{\mathrm{d}v}{\mathrm{d}t}=mg-\mu v^2. \| 9140:\frac{\mathrm{d}v}{v_T^2-v^2} =\frac{g}{v_T^2}\,\mathrm{d}t. \| 9145:\frac{1}{2v_T}\ln\left\|\frac{v_T+v}{v_T-v}\right\| = | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 226 | 9164 | 微分方程 | 习题 | 求解曲线 |  | 跳步关键词,短display待判定 | 于是; 9168:d=\sqrt{x^2+(y-Y_0)^2} =\|x\|\sqrt{1+(y')^2}. \| 9173:x\sqrt{1+(y')^2}=2, \qquad y'=\pm\frac{\sqrt{4-x^2}}{x}. \| 9179:y=\pm\int \frac{\sqrt{4-x^2}}{x}\,\mathrm{d}x. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 227 | 9217 | 微分方程 | 习题 | 求解曲线 |  | 跳步关键词,短display待判定 | 整理得; 9222:x=\frac{X_A}{2} =\frac{x-y/y'}{2}. \| 9227:xy'=-y, \qquad \frac{\mathrm{d}y}{y}=-\frac{\mathrm{d}x}{x}. \| 9233:\ln\|y\|=-\ln\|x\|+C_1, \qquad xy=C. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 228 | 9247 | 微分方程 | 习题 | 求解曲线 |  | 短display待判定 | 9249:(x-a)^2+y^2=a^2, \qquad x^2+y^2=2ax. \| 9255:2x+2yy'=2a =\frac{x^2+y^2}{x}, \qquad y'=\frac{y^2-x^2}{2xy}. \| 9262:\frac{\mathrm{d}y}{\mathrm{d}x}=\frac{2xy}{x^2-y^2}. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 229 | 9287 | 微分方程 | 习题 | 落体问题 |  | 短display待判定 | 9290:m\frac{\mathrm{d}v}{\mathrm{d}t}=mg-kv. \| 9294:\frac{\mathrm{d}v}{\mathrm{d}t} =-\frac{k}{m}\left(v-\frac{mg}{k}\right). \| 9299:\frac{\mathrm{d}v}{v-\frac{mg}{k}} =-\frac{k}{m | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 230 | 9317 | 微分方程 | 习题 | 实际应用题 | 微分方程 | 跳步关键词,短display待判定 | 于是; 9324:\boxed{\theta(t)=15-\frac{10}{k}\bigl(1-\mathrm{e}^{kt}\bigr)}. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 231 | 9340 | 微分方程 | 习题 | 基础：直接套用公式或常数变易法 | 微分方程 | 跳步关键词,短display待判定 | 整理得; 9347:\mathrm{e}^{x}y'+\mathrm{e}^{x}y=1, \qquad (y\mathrm{e}^{x})'=1. \| 9353:y\mathrm{e}^{x}=x+C, \qquad y=(x+C)\mathrm{e}^{-x}. \| 9360:\boxed{y=(x+1)\mathrm{e}^{-x}}. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 232 | 9428 | 微分方程 | 习题 | 基础：伯努利方程 |  | 跳步关键词,短display待判定 | 可得,化简得,代入得,整理得; 9434:y^{-3}y'-\frac{1}{x}y^{-2}=x^2. \| 9438:z'=-2y^{-3}y', \qquad y^{-3}y'=-\frac{1}{2}z'. \| 9444:-\frac{1}{2}z'-\frac{1}{x}z=x^2, \qquad z'+\frac{2}{x}z=-2x^2. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 233 | 9552 | 微分方程 | 习题 | 提高：角色互换与全微分 | 微分方程 | 跳步关键词,短display待判定 | 直接; 9557:\frac{\mathrm{d}y}{\mathrm{d}x}(x\ln y-1)=y\ln y. \| 9561:x\ln y\,\mathrm{d}y-\mathrm{d}y =y\ln y\,\mathrm{d}x. \| 9568:x\ln y\,\mathrm{d}y-y\ln y\,\mathrm{d}x=\mathrm{d}y,  | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 234 | 9611 | 微分方程 | 习题 | 提高：三角变形与全微分 | 微分方程 | 跳步关键词,短display待判定 | 直接; 9631:\boxed{y=C\sec x-1}. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 235 | 9640 | 微分方程 | 习题 | 黎卡提方程 | 微分方程 | 跳步关键词,短display待判定 | 可得,整理得; 9645:-\left(\frac{1}{x}\right)^2-\frac{1}{x}\left(\frac{1}{x}\right)+\frac{1}{x^2} =-\frac{1}{x^2}. \| 9652:y=\frac{1}{x}+u(x), \qquad y'=-\frac{1}{x^2}+u'. \| 9658:-\frac{1} | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 236 | 9717 | 微分方程 | 习题 | 基本概念 | 微分方程 | 跳步关键词,短display待判定 | 可得; 9720:\frac{\mathrm{d}y}{\mathrm{d}x}+P(x)y=Q(x). \| 9726:y=C(x)\mathrm{e}^{-\int P(x)\mathrm{d}x}. \| 9733:y^{-n}y'+P(x)y^{1-n}=Q(x). | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 237 | 9754 | 微分方程 | 习题 | 一阶线性微分方程求通解 | 微分方程 | 跳步关键词,短display待判定 | 略; 9759:\mu(x) = \exp\!\left(\int \tan x\,\mathrm{d}x\right) = \mathrm{e}^{-\ln\|\cos x\|} = \sec x. \| 9768:\boxed{y=(x+C)\cos x}. \| 9776:\mu(x) = \exp\!\left(\int -\cot x\,\mathrm{d | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 238 | 9835 | 微分方程 | 习题 | 一阶线性微分方程初值问题 |  | 短display待判定 | 9840:((x+1)y)'=2\mathrm{e}^{-x}. \| 9844:(x+1)y=-2\mathrm{e}^{-x}+C. \| 9848:\boxed{y=\frac{2\mathrm{e}^{-1}-2\mathrm{e}^{-x}}{x+1}}. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 239 | 9907 | 微分方程 | 习题 | 求曲线方程 | 微分方程 | 跳步关键词,短display待判定 | 代入得,于是; 9910:y'=2x+y, \qquad y'-y=2x. \| 9916:(y\mathrm{e}^{-x})'=2x\mathrm{e}^{-x}. \| 9920:y\mathrm{e}^{-x} =-2x\mathrm{e}^{-x}-2\mathrm{e}^{-x}+C, \qquad y=-2(x+1)+C\mathrm{e}^{x} | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 240 | 9936 | 微分方程 | 习题 | 应用题: 电路模型 | 微分方程 | 跳步关键词,短display待判定 | 可得; 9944:\mu(t)=\exp\!\left(\int5\,\mathrm{d}t\right)=\mathrm{e}^{5t}. \| 9948:(I\mathrm{e}^{5t})'=10\mathrm{e}^{5t}\sin5t. \| 9952:\int \mathrm{e}^{at}\sin(bt)\,\mathrm{d}t =\frac{\ | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 241 | 9983 | 微分方程 | 习题 | 溶液混合问题 | 微分方程 | 跳步关键词,短display待判定 | 代入得; 9990:\frac{y(t)}{V(t)} \times 3\ \mathrm{L/min} = \frac{3y}{50+2t}\ \mathrm{g/min}. \| 9995:\frac{\mathrm{d}y}{\mathrm{d}t}=10-\frac{3y}{50+2t}, \qquad y'+\frac{3}{50+2t}y=10.  | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 242 | 10023 | 微分方程 | 习题 | 一阶线性微分方程初值问题 | 微分方程 | 跳步关键词,短display待判定 | 于是; 10027:\mu(x) =\exp\!\left(\int\frac{x}{1+x^2}\,\mathrm{d}x\right) =\sqrt{1+x^2}. \| 10034:z\sqrt{1+x^2} =\int x\sqrt{1+x^2}\,\mathrm{d}x =\frac{1}{3}(1+x^2)^{3/2}+C. \| 10042:\bo | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 243 | 10054 | 微分方程 | 习题 | 求通解 | 微分方程,重积分/换元 | 短display待判定 | 10060:y' + \frac{1}{x}y = \frac{2\ln x}{x}y^2. \| 10066:z'-\frac{1}{x}z=-\frac{2\ln x}{x}. \| 10073:zx^{-1} =\int-\frac{2\ln x}{x^2}\,\mathrm{d}x =\frac{2\ln x}{x}+\frac{2}{x}+C. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 244 | 10110 | 微分方程 | 习题 | 积分方程求未知函数 | 微分方程,重积分/换元 | 跳步关键词,短display待判定 | 可得,于是; 10116:f'(x)=3f(x)+2\mathrm{e}^{2x}, \qquad f'(x)-3f(x)=2\mathrm{e}^{2x}. \| 10126:\boxed{f(x)=3\mathrm{e}^{3x}-2\mathrm{e}^{2x}}. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 245 | 10135 | 微分方程 | 习题 | 积分与变量无关 | 微分方程 | 跳步关键词,短display待判定 | 可得; 10138:I(x)=\int_0^1 f(x)\,\mathrm{d}t+\int_0^1 xf(xt)\,\mathrm{d}t =f(x)+\int_0^x f(u)\,\mathrm{d}u. \| 10148:I(x)=C\mathrm{e}^{-x}+\int_0^x C\mathrm{e}^{-u}\,\mathrm{d}u =C. \|  | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 246 | 10170 | 微分方程 | 习题 | 缺 $y$ 型与缺 $x$ 型 | 微分方程 | 跳步关键词,短display待判定 | 于是; 10174:(1+x^2)p'+xp=1, \qquad p'+\frac{x}{1+x^2}p=\frac{1}{1+x^2}. \| 10180:\mu(x)=\exp\!\left(\int\frac{x}{1+x^2}\,\mathrm{d}x\right)=\sqrt{1+x^2}. \| 10184:(p\sqrt{1+x^2})'=\fra | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 247 | 10251 | 微分方程 | 习题 | 求通解 | 微分方程 | 跳步关键词,短display待判定 | 直接,于是; 10259:\int \arctan x \,\mathrm{d}x = x\arctan x - \int \frac{x}{1+x^2}\,\mathrm{d}x, \| 10264:y = x\arctan x - \frac{1}{2}\ln(1+x^2) + C_1 x + C_2. \| 10269:(\mathrm{e}^{-x}p) | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 248 | 10336 | 微分方程 | 习题 | 求初值问题 | 微分方程 | 跳步关键词,短display待判定 | 代入得,直接,于是; 10339:y^3p\frac{\mathrm{d}p}{\mathrm{d}y}=-1, \qquad p\,\mathrm{d}p=-y^{-3}\mathrm{d}y. \| 10345:\frac{1}{2}p^2=\frac{1}{2}y^{-2}+C_1. \| 10350:p^2=y^{-2}-1=\frac{1-y^2}{y | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 249 | 10480 | 微分方程 | 习题 | 二阶方程的初值问题 |  | 跳步关键词,短display待判定 | 于是; 10485:yy'=x-1 \implies y\,\mathrm{d}y=(x-1)\mathrm{d}x,\qquad \frac12y^2=\frac12x^2-x+C_2. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 250 | 10499 | 微分方程 | 习题 | 可降阶的一阶齐次型综合应用 | 微分方程 | 跳步关键词,短display待判定 | 代入得,于是; 10502:xu'+u=u\ln u, \qquad x\frac{\mathrm{d}u}{\mathrm{d}x}=u(\ln u-1). \| 10509:\boxed{y=\frac{\mathrm e}{2}x^2+C_2}. \| 10513:\frac{\mathrm{d}u}{u(\ln u-1)}=\frac{\mathrm{d | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 251 | 10537 | 微分方程 | 习题 | 缺 $x$ 型二阶方程求解 | 微分方程 | 短display待判定 | 10539:p\frac{\mathrm{d}p}{\mathrm{d}y}(1+y^2)=2yp^2. \| 10543:\frac{\mathrm{d}p}{p}=\frac{2y}{1+y^2}\mathrm{d}y. \| 10547:\ln\|p\|=\ln(1+y^2)+\ln\|C_1\|, \qquad p=C_1(1+y^2). | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 252 | 10569 | 微分方程 | 习题 | 建立运动微分方程：追击问题 | 微分方程,隐函数/偏导 | 跳步关键词,短display待判定 | 可得; 10575:y'=\frac{(1+vt)-y}{0-x} =\frac{y-1-vt}{x}. \| 10585:\frac{\mathrm{d}t}{\mathrm{d}x} =\frac{\mathrm{d}t}{\mathrm{d}s}\frac{\mathrm{d}s}{\mathrm{d}x} =\frac{1}{2v}\sqrt{1+(y | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 253 | 10612 | 微分方程 | 习题 | 积分方程求导转化法 |  | 跳步关键词,短display待判定 | 于是; 10616:\int_0^x \sqrt{1+(y')^2}\,\mathrm{d}t =\int_0^x y(t)\,\mathrm{d}t, \qquad \sqrt{1+(y')^2}=y. \| 10623:(y')^2=y^2-1, \qquad y'=\sqrt{y^2-1}, \qquad \frac{\mathrm{d}y}{\sqrt | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 254 | 10645 | 微分方程 | 习题 | 物理建模与微分方程的推导 | 微分方程 | 短display待判定 | 10649:T\cos\theta=H, \qquad T\sin\theta=\rho g s. \| 10657:y''=\frac{\rho g}{H}\sqrt{1+(y')^2}. \| 10661:\frac{\mathrm{d}p}{\mathrm{d}x}=a\sqrt{1+p^2}, \qquad \frac{\mathrm{d}p}{\sqr | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 255 | 10675 | 微分方程 | 习题 | 基于牛顿第二定律降阶求解 |  | 跳步关键词,短display待判定 | 代入得; 10679:m\frac{\mathrm{d}^2r}{\mathrm{d}t^2} = -G\frac{Mm}{r^2}, \qquad v\frac{\mathrm{d}v}{\mathrm{d}r} = -\frac{GM}{r^2}. \| 10686:\int v\,\mathrm{d}v=-GM\int r^{-2}\,\mathrm{d | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 256 | 10700 | 微分方程 | 习题 | 变加速直线运动的积分 |  | 跳步关键词,短display待判定 | 于是; 10704:m\frac{\mathrm{d}v}{\mathrm{d}t}=-kv, \qquad 300\frac{\mathrm{d}v}{\mathrm{d}t}=-10gv. \| 10710:\frac{\mathrm{d}v}{v}=-\frac{g}{30}\mathrm{d}t, \qquad \ln v=-\frac{g}{30}t | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 257 | 10746 | 微分方程 | 习题 | 基础：验证与判定 | 微分方程 | 短display待判定 | 10752:y_1'' - 4y_1' + 4y_1 =4\mathrm{e}^{2x} - 8\mathrm{e}^{2x} + 4\mathrm{e}^{2x}=0. \| 10760:y_2'' = 2\mathrm{e}^{2x} + 2(1+2x)\mathrm{e}^{2x} = (4+4x)\mathrm{e}^{2x}. \| 10802:y'' | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 258 | 10844 | 微分方程 | 习题 | 基础：常数变易法 | 微分方程 | 跳步关键词,短display待判定 | 于是; 10866:y^{*}(x) =-y_{1}\int \frac{y_{2}f(x)}{W(x)}\,\mathrm{d}x +y_{2}\int \frac{y_{1}f(x)}{W(x)}\,\mathrm{d}x, \| 10872:y^* =\sin x\int \cos x\cot x\,\mathrm{d}x -\cos x\int \si | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 259 | 10987 | 微分方程 | 习题 | 提高：叠加原理的应用 | 微分方程 | 跳步关键词 | 直接 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 260 | 11011 | 微分方程 | 习题 | 刘维尔公式的推广 | 微分方程 | 跳步关键词,短display待判定 | 可得,同理,直接,于是; 11014:L[y]=y'''+p(x)y''+q(x)y'+r(x)y=0 \| 11027:y_1u'''+(3y_1'+py_1)u'' +(3y_1''+2py_1'+qy_1)u' +uL[y_1]=0. \| 11034:w''+\left(3\frac{y_1'}{y_1}+p(x)\right)w' +\left(3\f | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 262 | 11135 | 微分方程 | 习题 | 解的验证 | 微分方程 | 短display待判定 | 11138:y'=-2\sin x+3\cos x,\qquad y''=-2\cos x-3\sin x. \| 11142:y''+y=(-2\cos x-3\sin x)+(2\cos x+3\sin x)=0. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 263 | 11151 | 微分方程 | 习题 | 含参方程的求解 | 微分方程 | 短display待判定 | 11154:y'=-A\alpha\sin\alpha x, \qquad y''=-A\alpha^2\cos\alpha x. \| 11160:A(5-\alpha^2)\cos\alpha x=0. \| 11166:-A\alpha\sin\alpha = 3 \implies -A(\pm\sqrt{5})\sin(\pm\sqrt{5}) = 3. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 264 | 11191 | 微分方程 | 习题 | 边值问题求解 | 微分方程 | 跳步关键词,短display待判定 | 可得,同理; 11194:y''=-\omega^2(A\cos\omega x+B\sin\omega x)=-\omega^2y, \| 11202:A\cos\left(4\cdot\frac{\pi}{8}\right) +B\sin\left(4\cdot\frac{\pi}{8}\right)=3, \| 11210:\boxed{(\omega,A | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 265 | 11218 | 微分方程 | 习题 | 线性算子的计算 |  | 短display待判定 | 11221:L[\mathrm{e}^x] = \mathrm{e}^x - 3x\mathrm{e}^x + 3\mathrm{e}^x = (4 - 3x)\mathrm{e}^x. \| 11227:L[\cos\sqrt{3}x] =-3\cos\sqrt{3}x-3x(-\sqrt{3}\sin\sqrt{3}x)+3\cos\sqrt{3}x =3 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 267 | 11256 | 微分方程 | 习题 | 非齐次叠加原理与猜测法 | 微分方程 | 短display待判定 | 11265:A\mathrm{e}^{-x} + A\mathrm{e}^{-x} = 3\mathrm{e}^{-x} \implies 2A = 3 \implies A = \frac{3}{2}. \| 11279:\boxed{y=y_h+y^*=C_1\sin x+C_2\cos x+\frac32\mathrm{e}^{-x}+2x}. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 268 | 11288 | 微分方程 | 习题 | 解的验证与通解构造 | 微分方程 | 短display待判定 | 11290:y_1'=2x\mathrm{e}^{x^2}, \qquad y_1''=(2+4x^2)\mathrm{e}^{x^2}. \| 11296:(2+4x^2)\mathrm{e}^{x^2} -4x(2x\mathrm{e}^{x^2}) +(4x^2-2)\mathrm{e}^{x^2}=0. \| 11304:y_2'=(1+2x^2)\ma | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 269 | 11330 | 微分方程 | 习题 | 积分算子的线性性证明 |  | 短display待判定 | 11332:T[Cy]=\int_a^x t^2(Cy(t))\,\mathrm{d}t =C\int_a^x t^2y(t)\,\mathrm{d}t =CT[y]. \| 11338:T[y_1+y_2] =\int_a^x t^2\bigl(y_1(t)+y_2(t)\bigr)\,\mathrm{d}t \| 11342:=\int_a^x t^2y_1 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 270 | 11358 | 微分方程 | 习题 | 物理建模：LRC电路微分方程 |  | 短display待判定 | 11371:\boxed{\frac{\mathrm{d}^2V_C}{\mathrm{d}t^2} + \frac{R}{L}\frac{\mathrm{d}V_C}{\mathrm{d}t} + \frac{1}{LC}V_C = \frac{E_m}{LC}\sin\omega t}. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 271 | 11383 | 微分方程 | 习题 | 物理建模：弹簧振子动力学 | 微分方程 | 跳步关键词,短display待判定 | 于是; 11391:my''+ky=0, \qquad y''+\frac{k}{m}y=0. \| 11399:y(t)=C_1\cos\left(\sqrt{\frac{k}{m}}t\right) +C_2\sin\left(\sqrt{\frac{k}{m}}t\right). \| 11408:y'(t)=-C_1\sqrt{\frac{k}{m}}\ | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 272 | 11424 | 微分方程 | 习题 | 根据基础解系反求微分方程 | 微分方程 | 跳步关键词 | 可得,容易,于是 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 273 | 11443 | 微分方程 | 习题 | 刘维尔公式应用 | 微分方程 | 跳步关键词,短display待判定 | 计算得,直接,略,于是; 11445:y''+P(x)y'+Q(x)y=0, \qquad P(x)=-\frac{2x+1}{2x-1}. \| 11451:\exp\left(-\int P(x)\,\mathrm{d}x\right) =\mathrm{e}^x(2x-1) \| 11456:y_2=y_1\int \frac{\exp\left(-\in | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 274 | 11474 | 微分方程 | 习题 | 常数变易法的综合应用 | 微分方程 | 短display待判定 | 11479:y''-\frac{2}{x}y'+\frac{2}{x^2}y=0, \qquad P(x)=-\frac{2}{x}. \| 11485:\exp\left(-\int P(x)\mathrm{d}x\right) =\exp\left(\int\frac{2}{x}\mathrm{d}x\right)=x^2, \| 11493:y''-\fr | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 275 | 11519 | 微分方程 | 习题 | 基本概念 | 微分方程 | 短display待判定 | 11523:(\lambda^2+p\lambda+q)\mathrm{e}^{\lambda x}=0. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 276 | 11545 | 微分方程 | 习题 | 齐次方程通解 | 微分方程 | 短display待判定 | 11561:(\lambda^2 - 1)(\lambda^2 + 1) = (\lambda-1)(\lambda+1)(\lambda^2+1) = 0. \| 11567:\boxed{y = C_1\mathrm{e}^x + C_2\mathrm{e}^{-x} + C_3\cos x + C_4\sin x}. \| 11573:(-1)^3 - 6 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 277 | 11595 | 微分方程 | 习题 | 齐次方程初值问题 | 微分方程 | 短display待判定 | 11600:\lambda^2+4\lambda+29=0 \implies \lambda=\frac{-4\pm\sqrt{16-116}}{2}=-2\pm5i. \| 11606:y(0) = 0 \implies \mathrm{e}^0(C_1\cos 0 + C_2\sin 0) = C_1 = 0. \| 11613:y' = C_2(-2\ma | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 278 | 11701 | 微分方程 | 习题 | 非齐次方程通解 | 微分方程 | 跳步关键词,短display待判定 | 代入得,于是; 11704:\lambda^2+\lambda-2=0 \implies(\lambda-1)(\lambda+2)=0 \implies \lambda_1=1,\ \lambda_2=-2. \| 11720:-A - 9A = -10A = -2 \implies A = \frac{1}{5}, \| 11726:\boxed{y = C | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 279 | 11878 | 微分方程 | 习题 | 非齐次方程初值问题 | 微分方程 | 跳步关键词,短display待判定 | 代入得; 11883:(y^*)''+y^*=-4A\sin2x+A\sin2x=-3A\sin2x=-\sin2x, \| 11890:y(\pi)=C_1\cos\pi+C_2\sin\pi+\frac13\sin2\pi=-C_1=1, \| 11895:y' = -C_1\sin x + C_2\cos x + \frac{2}{3}\cos 2x. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 280 | 11978 | 微分方程 | 习题 | 含参方程的通解 | 微分方程 | 跳步关键词,短display待判定 | 代入得; 11981:\lambda^2+4\lambda+4=0 \implies (\lambda+2)^2=0 \implies \lambda=-2. \| 11992:A\alpha^2\mathrm{e}^{\alpha x}+4A\alpha\mathrm{e}^{\alpha x} +4A\mathrm{e}^{\alpha x} =\math | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 281 | 12061 | 微分方程 | 习题 | Euler方程求解 | 微分方程,隐函数/偏导 | 跳步关键词,短display待判定 | 代入得,于是; 12064:x y' = D_t y,\qquad x^2 y'' = D_t(D_t-1)y = D_t^2 y - D_t y,\qquad x^3 y''' = D_t(D_t-1)(D_t-2)y. \| 12072:(D_t^2-D_t)y-D_t y+y=0 \implies y_{tt}''-2y_t'+y=0. \| 12081: | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 282 | 12172 | 微分方程 | 习题 | Euler方程初值问题 | 微分方程 | 跳步关键词,短display待判定 | 于是; 12177:(y_{tt}''-y_t')-y_t'+y=2\mathrm{e}^t \implies y_{tt}''-2y_t'+y=2\mathrm{e}^t. \| 12185:(y^*)''-2(y^*)'+y^* =A(t^2+4t+2-2t^2-4t+t^2)\mathrm{e}^t =2A\mathrm{e}^t=2\mathrm{e} | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 283 | 12219 | 微分方程 | 习题 | 无阻尼自由振动物理建模 | 微分方程 | 跳步关键词,短display待判定 | 整理得; 12230:y(t)=C_1\cos\left(\sqrt{\frac{g}{a}}t\right) +C_2\sin\left(\sqrt{\frac{g}{a}}t\right). \| 12241:y'(t) =-C_1\sqrt{\frac{g}{a}}\sin\left(\sqrt{\frac{g}{a}}t\right) +C_2\sqr | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 284 | 12256 | 微分方程 | 习题 | 阻尼自由振动物理建模 | 微分方程 | 短display待判定 | 12262:mx''=-kx-\mu x' \implies mx''+\mu x'+kx=0. \| 12281:\boxed{x(t) = \mathrm{e}^{-\frac{\mu}{2m}t} (C_1\cos\omega_d t + C_2\sin\omega_d t)}. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 285 | 12295 | 微分方程 | 习题 | 利用切线条件的非齐次方程初值问题 | 微分方程 | 短display待判定 | 12308:A(x+2)\mathrm{e}^x - 3A(x+1)\mathrm{e}^x + 2Ax\mathrm{e}^x = -A\mathrm{e}^x = 2\mathrm{e}^x. \| 12318:y(0) = C_1 + C_2 - 0 = 1 \implies C_1 + C_2 = 1. \| 12324:y'(0) = C_1 + 2C | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 286 | 12336 | 微分方程 | 习题 | 变加速力学建模：链条滑落 | 微分方程 | 跳步关键词,短display待判定 | 化简得,代入得,直接; 12342:F_{net} = \rho g x - \rho g (18-x) = \rho g(2x - 18), \| 12346:Mx''=F_{net}\implies 18\rho x''=\rho g(2x-18) \implies x''-\frac{g}{9}x=-g. \| 12360:x(0)=C_1\cosh0+C | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 287 | 12382 | 微分方程 | 习题 | 平衡位置的改变及振动建模 | 微分方程 | 跳步关键词,短display待判定 | 直接; 12391:4mx''=-kx \implies 4mx''+\frac{mg}{a}x=0 \implies x''+\frac{g}{4a}x=0. \| 12397:x(t) = C_1\cos\left(\sqrt{\frac{g}{4a}} t\right) + C_2\sin\left(\sqrt{\frac{g}{4a}} t\right | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 288 | 12418 | 微分方程 | 习题 | 一阶速度模型的降阶求解 | 微分方程 | 跳步关键词,短display待判定 | 于是; 12424:m x'' = mg - F_b - kx' \implies x'' + \frac{k}{m} x' = g'. \| 12432:v' + \frac{k}{m}v = g', \qquad v(t) = \frac{mg'}{k} + C_1\mathrm{e}^{-\frac{k}{m}t}. \| 12443:x(t)=\int_ | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 289 | 12457 | 微分方程 | 习题 | 频率计算（保留重力加速度符号 $g$） |  | 跳步关键词,短display待判定 | 可得; 12465:mx''+kx=0\implies 2x''+gx=0 \implies x''+\frac{g}{2}x=0. \| 12470:\omega^2 = \frac{g}{2} \implies \omega = \sqrt{\frac{g}{2}}, \qquad \boxed{T = \frac{2\pi}{\omega} = 2\pi | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 290 | 12482 | 微分方程 | 习题 | 共振与受迫振动建模（保留符号 $g$） | 微分方程 | 跳步关键词,短display待判定 | 代入得; 12489:my''=-k(y-y_0)\implies 4y''=-4g(y-2\sin30t) \implies y''+gy=2g\sin30t. \| 12500:\boxed{y(t)=\frac{1}{g-900}\left(2g\sin30t-60\sqrt g\,\sin(\sqrt g\,t)\right)} \quad(g\neq | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 291 | 12520 | 微分方程 | 习题 | 积分微分方程转化为常系数方程 | 微分方程 | 跳步关键词,短display待判定 | 代入得,直接; 12525:f''(x)=6\sin^2 x-f(x),\qquad f''(x)+f(x)=6\sin^2 x=3(1-\cos 2x)=3-3\cos 2x. \| 12536:-4B\cos2x+B\cos2x=-3B\cos2x=-3\cos2x \implies B=1. \| 12541:f(x) = C_1\cos x + C_2\ | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 293 | 12620 | 微分方程 | 习题 | 基础：消元法练习 | 微分方程 | 跳步关键词,短display待判定 | 整理得; 12626:\frac12x''-\frac12x' =4x+3\left(\frac12x'-\frac12x\right) =\frac52x+\frac32x'. \| 12634:y=\frac{1}{2}(5C_1\mathrm{e}^{5t}-C_2\mathrm{e}^{-t}) -\frac{1}{2}(C_1\mathrm{e}^{ | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 294 | 12721 | 微分方程 | 习题 | 提高：非齐次方程组 | 微分方程 | 跳步关键词,短display待判定 | 整理得; 12727:(2\mathrm{e}^{2t}-x''+2x')+x-2(\mathrm{e}^{2t}-x'+2x) =\mathrm{e}^{3t} \implies x''-4x'+3x=-\mathrm{e}^{3t}. \| 12738:(D-1)(D-3)[At\mathrm{e}^{3t}] = -\mathrm{e}^{3t} \im | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 295 | 12800 | 微分方程 | 习题 | 解微分方程组综合 | 微分方程 | 跳步关键词,短display待判定 | 可得,整理得; 12807:x(t) = C_1\mathrm{e}^t + C_2\mathrm{e}^{-t}, \qquad y(t) = C_1\mathrm{e}^t - C_2\mathrm{e}^{-t}. \| 12831:\frac15(x'-x'')=2x-\frac15(x-x') \implies -x''=9x \implies x' | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 296 | 12855 | 微分方程 | 习题 | 微分方程组物理建模：炮弹受阻运动 | 微分方程 | 短display待判定 | 12878:y'(0)=v_0\sin\alpha \implies C_3-\frac{mg}{k}=v_0\sin\alpha \implies C_3=v_0\sin\alpha+\frac{mg}{k}. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 297 | 12903 | 微分方程 | 习题 | 有心力场中的粒子轨迹 | 微分方程 | 短display待判定 | 12910:mx''=-kx,\qquad my''=-ky \Longrightarrow x''+\omega^2x=0,\quad y''+\omega^2y=0. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 298 | 12944 | 微分方程 | 习题 | 基本概念与方程求解 | 微分方程 | 跳步关键词,短display待判定 | 代入得,显然,直接; 12958:(\lambda-1)^2=0 \implies \lambda^2-2\lambda+1=0 \implies y''-2y'+y=0. \| 12971:y_2 = u(x) \int \frac{1}{u^2(x)} e^{-\int a(x)\mathrm{d}x} \mathrm{d}x. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 299 | 13030 | 微分方程 | 习题 | 微分方程概念辨析 | 微分方程 | 跳步关键词,短display待判定 | 直接; 13035:L[y_1-y_2] = L[y_1] - L[y_2] = f(x) - f(x) = 0. \| 13044:\frac{y-\ln x}{x}+\frac{\mathrm{d}y}{\mathrm{d}x}=0 \implies \frac{\mathrm{d}y}{\mathrm{d}x}+\frac{1}{x}y=\frac{\l | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 300 | 13076 | 微分方程 | 习题 | 人口增长模型 | 微分方程 | 短display待判定 | 13082:\frac{\mathrm{d}P}{P}=0.02\,\mathrm{d}t \implies \ln P=0.02t+C \implies P(t)=C_1e^{0.02t}; | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 301 | 13100 | 微分方程 | 习题 | 一阶线性微分方程解的结构 | 微分方程 | 短display待判定 | 13109:u(x) = C_1 e^{-\int P(x)\mathrm{d}x},\qquad v(x) = C_2 e^{-\int P(x)\mathrm{d}x}. \| 13117:\frac{y_3 - y_1}{y_2 - y_1} = \frac{v(x)}{u(x)} = \frac{C_2 e^{-\int P(x)\mathrm{d}x | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 302 | 13130 | 微分方程 | 习题 | Logistic 模型应用 | 微分方程 | 跳步关键词 | 化简得,直接 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 303 | 13165 | 微分方程 | 习题 | 微分方程的几何应用 | 微分方程,重积分/换元 | 短display待判定 | 13169:S = \frac{1}{2} \int_0^\theta r^2(\phi)\,\mathrm{d}\phi,\qquad s = \int_0^\theta \sqrt{r^2(\phi) + [r'(\phi)]^2}\,\mathrm{d}\phi. \| 13176:\frac{1}{2} \int_0^\theta r^2(\phi)\ | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 304 | 13218 | 微分方程 | 习题 | 微分方程在物理化学中的应用 | 微分方程 | 短display待判定 | 13223:-\frac{\mathrm{d}r}{\mathrm{d}t} =\alpha S=\alpha(4\pi r^2)=Kr^2 \qquad(\text{令 } K=4\pi\alpha>0). \| 13237:\frac{1}{0.19}=2K+4 \implies \frac{100}{19}=2K+4 \implies K=\frac{1 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 305 | 13258 | 微分方程 | 习题 | 动力学与微分方程 | 微分方程 | 短display待判定 | 13268:\frac{\mathrm{d}v}{\mathrm{d}t} =g-\frac{k}{m}v^2 =\frac{k}{m}\left(\frac{mg}{k}-v^2\right) =\frac{k}{m}(a^2-v^2). \| 13293:x(t)=\int_0^t \sqrt{\frac{mg}{k}} \tanh\left(\sqrt{ | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 306 | 13305 | 微分方程 | 习题 | 常系数线性非齐次方程的特解与通解 | 微分方程 | 跳步关键词,短display待判定 | 可得; 13321:y'=2e^{2x}+e^x+(1+x)e^x=2e^{2x}+(2+x)e^x, \| 13324:y''=4e^{2x}+e^x+(2+x)e^x=4e^{2x}+(3+x)e^x. \| 13328:y''-3y'+2y =[4e^{2x}+(3+x)e^x]-3[2e^{2x}+(2+x)e^x] +2[e^{2x}+(1+x)e^x | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 307 | 13346 | 微分方程 | 习题 | 二阶齐次方程的初值问题 | 微分方程 | 短display待判定 | 13355:\lambda^2 - 4\lambda + 3 = 0 \implies (\lambda-1)(\lambda-3) = 0. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 308 | 13376 | 微分方程 | 习题 | 自变量与因变量互换求解 | 微分方程 | 跳步关键词,短display待判定 | 直接; 13381:y' = \frac{\mathrm{d}y}{\mathrm{d}x} = \frac{1}{\frac{\mathrm{d}x}{\mathrm{d}y}} = \frac{1}{x'}. \| 13387:y''=\frac{\mathrm{d}}{\mathrm{d}x}(y') =\frac{\mathrm{d}}{\mathrm | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 309 | 13442 | 微分方程 | 习题 | 一阶线性方程与积分不等式 | 微分方程 | 短display待判定 | 13447:y'e^{ax}+aye^{ax}=f(x)e^{ax} \implies \frac{\mathrm{d}}{\mathrm{d}x}(ye^{ax})=f(x)e^{ax}. \| 13452:y(x)e^{ax} - y(0)e^0 = \int_0^x f(t)e^{at} \mathrm{d}t. \| 13456:y(x) = e^{-a | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 310 | 13482 | 微分方程 | 习题 | 微分不等式比较定理 |  | 跳步关键词,短display待判定 | 于是; 13488:w'(x)=u_1'(x)-u_2'(x) \ge [a(x)u_1(x)+v(x)]-[a(x)u_2(x)+v(x)] =a(x)[u_1(x)-u_2(x)], \| 13497:[w'(x) - a(x)w(x)] e^{-\int_0^x a(t)\mathrm{d}t} \ge 0 \implies \frac{\mathrm{ | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 311 | 13518 | 微分方程 | 习题 | 二阶微分方程解的单调性分析 |  | 跳步关键词,短display待判定 | 于是; 13523:E'(x)=\frac{\mathrm{d}}{\mathrm{d}x}[y(x)y'(x)] =[y'(x)]^2+y(x)y''(x) =[y'(x)]^2+a(x)[y(x)]^2. \| 13532:E(0)=y(0)y'(0)=y_0y_0'>0 \qquad(\text{因 } y_0>0,\ y_0'>0). \| 13543: | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 312 | 13559 | 微分方程 | 习题 | 由函数方程导出微分方程 | 微分方程 | 跳步关键词,短display待判定 | 直接,于是; 13567:f(x+h)-f(x) =\frac{f(h)\,[1+f^2(x)]}{1-f(x)f(h)}. \| 13572:f'(x)=\lim_{h\to0}\frac{f(x+h)-f(x)}{h} =[1+f^2(x)]\lim_{h\to0}\frac{f(h)}{h}. \| 13577:\boxed{f'(x)=k[1+f^2(x | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 313 | 13596 | 微分方程 | 习题 | 积微分方程求解 | 微分方程 | 跳步关键词,短display待判定 | 同理; 13600:u''(t) = u'(t) + u(t) \implies u'' - u' - u = 0. \| 13610:u'(0) = u(0) + \int_0^0 u(s)\mathrm{d}s = 1 + 0 = 1. \| 13617:r=\frac{1\pm\sqrt{(-1)^2-4(1)(-1)}}{2} =\frac{1\pm\s | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 314 | 13658 | 微分方程 | 习题 | 变上限积分方程求解 | 微分方程 | 跳步关键词,短display待判定 | 直接,整理得; 13662:x f(x) = n f'(x) \implies f'(x) - \frac{x}{n} f(x) = 0. \| 13670:\left(f(x)\mathrm{e}^{-\frac{x^2}{2n}}\right)'=0, \| 13681:\boxed{f(x)=\frac{1}{n}\mathrm{e}^{\frac{x^2 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 315 | 13692 | 微分方程 | 习题 | 含卷积的积分方程求解 | 微分方程 | 跳步关键词,短display待判定 | 化简得; 13697:f(x) = \sin x - \left( x\int_0^x f(t)\mathrm{d}t - \int_0^x tf(t)\mathrm{d}t \right) = \sin x - x\int_0^x f(t)\mathrm{d}t + \int_0^x tf(t)\mathrm{d}t. \| 13705:f'(x)=\cos | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 316 | 13914 | 多元函数微分学 | 知识讲解 | 开球是区域 |  | 短display待判定 | 13917:\\|x-a\\|\leqslant \\|x-p\\|+\\|p-a\\|<\varepsilon+\\|p-a\\|=r. \| 13924:\\|\Phi(t)-a\\| =\\|(1-t)(p-a)+t(q-a)\\| \leqslant (1-t)\\|p-a\\|+t\\|q-a\\|<r. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 317 | 13944 | 多元函数微分学 | 知识讲解 | 开但不连通的集合 |  | 跳步关键词 | 于是 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 318 | 13972 | 多元函数微分学 | 知识讲解 | 求二元函数的定义域 | 曲面积分/通量 | 跳步关键词,短display待判定 | 可得; 13975:D_1=\{(x,y)\mid x\geqslant 0,\;y\geqslant 0\} \cup\{(x,y)\mid x\leqslant 0,\;y\leqslant 0\}. \| 13984:x^2-2x+y^2\leqslant0 \Longleftrightarrow (x-1)^2+y^2\leqslant1. \| 139 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 319 | 14062 | 多元函数微分学 | 知识讲解 | 极坐标下的判零 |  | 跳步关键词,短display待判定 | 于是; 14064:f(r\cos\theta,r\sin\theta) =\frac{r^2\cos\theta\sin\theta}{r} =r\cos\theta\sin\theta. \| 14070:\|f(r\cos\theta,r\sin\theta)\|\leqslant \frac12r\to0. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 320 | 14105 | 多元函数微分学 | 知识讲解 | 角度不同导致极限不同 | 重积分/换元 | 短display待判定 | 14110:f(r\cos\theta,r\sin\theta) =\frac{r^2\cos\theta\sin\theta} {r^2(\cos^2\theta+\sin^2\theta)} =\frac12\sin(2\theta). \| 14123:\lim_{r\to 0^+} f = \frac{1}{2}\sin\left(2 \cdot \f | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 321 | 14141 | 多元函数微分学 | 知识讲解 | 角度随半径变化的情形 | 重积分/换元 | 跳步关键词,短display待判定 | 可得,直接; 14143:f(x,kx^2) =\frac{2x^2\cdot kx^2}{x^4+k^2x^4} =\frac{2k}{1+k^2}\qquad(x\neq0). \| 14149:\boxed{\displaystyle\lim_{(x,y)\to(0,0)}\frac{2x^2y}{x^4+y^2}\text{ 不存在}}. \| 1415 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 322 | 14196 | 多元函数微分学 | 知识讲解 | 二重极限存在但累次极限不全存在 |  | 短display待判定 | 14199:f(r\cos\theta,r\sin\theta) =r\sin\theta\sin\frac{1}{r\cos\theta}. \| 14204:\|f(r\cos\theta,r\sin\theta)\|\leqslant r\|\sin\theta\|\leqslant r\to0. \| 14212:\lim_{y\to0}\lim_{x\to0} | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 323 | 14230 | 多元函数微分学 | 知识讲解 | 含三角函数的极限 |  | 短display待判定 | 14232:\left\|\frac{\sin(x^3+y^3)}{x^2+y^2}\right\| =\left\|\frac{\sin\bigl(r^3(\cos^3\theta+\sin^3\theta)\bigr)}{r^2}\right\|. \| 14237:\left\|\frac{\sin\bigl(r^3(\cos^3\theta+\sin^3\the | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 324 | 14259 | 多元函数微分学 | 知识讲解 | 含分段定义的极限 |  | 短display待判定 | 14261:\|f(x,y)\|=\left\|\frac{\sin(xy)}{x}\right\| \leqslant \frac{\|xy\|}{\|x\|} =\|y\|=r\|\sin\theta\|\leqslant r. \| 14267:\boxed{\displaystyle\lim_{(x,y)\to(0,0)}f(x,y)=0}. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 325 | 14277 | 多元函数微分学 | 知识讲解 | 幂指型极限 | 重积分/换元 | 短display待判定 | 14280:(x^2+y^2)^{xy}=e^{\,xy\ln(x^2+y^2)}. \| 14286:xy\ln(x^2+y^2) =r^2\cos\theta\sin\theta\ln r^2. \| 14291:\bigl\|r^2\cos\theta\sin\theta\ln r^2\bigr\| \leqslant \frac12 r^2\|\ln r^2\| | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 326 | 14306 | 多元函数微分学 | 知识讲解 | 含小角三角函数的极限 |  | 短display待判定 | 14308:\left\|\frac{\sin(x^2y)}{x^2+y^2}\right\| =\left\|\frac{\sin\bigl(r^3\cos^2\theta\sin\theta\bigr)}{r^2}\right\| \leqslant r\|\cos^2\theta\sin\theta\| \leqslant r\to0. \| 14315:\boxe | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 327 | 14363 | 多元函数微分学 | 知识讲解 | 可去间断点 |  | 短display待判定 | 14367:f(r\cos\theta,r\sin\theta) =\frac{r^4\cos^2\theta\sin^2\theta}{r^2} =r^2\cos^2\theta\sin^2\theta. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 328 | 14380 | 多元函数微分学 | 知识讲解 | 复合函数的连续性 | 隐函数/偏导 | 短display待判定 | 14383:(x,y,z)\;\xmapsto{\;g\;}\; xy+z\;\xmapsto{\;\sin\;}\; \sin(xy+z)=f(x,y,z). | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 329 | 14406 | 多元函数微分学 | 知识讲解 | 边缘连续但不整体连续 |  | 跳步关键词,短display待判定 | 同理; 14409:\frac{xy}{x^2+y^2}=\cos\theta\sin\theta=\frac12\sin2\theta, | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 330 | 14524 | 多元函数微分学 | 知识讲解 | 方向导数的直接计算 | 隐函数/偏导 | 短display待判定 | 14528:u(t)=f\!\left(1+\frac{\sqrt2}{2}t,\;1+\frac{\sqrt2}{2}t\right) =\left(1+\frac{\sqrt2}{2}t\right)^{2}. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 331 | 14555 | 多元函数微分学 | 知识讲解 | 在某点处求偏导数值 | 隐函数/偏导 | 跳步关键词,短display待判定 | 于是; 14559:\varphi'(x)=-\frac{4}{(1+x)^2} \Longrightarrow f_x(3,2)=\varphi'(3)=-\frac14, \| 14564:\psi'(y)=\frac{2y}{4}=\frac{y}{2} \Longrightarrow f_y(3,2)=\psi'(2)=1. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 332 | 14574 | 多元函数微分学 | 知识讲解 | 求偏导函数（解析表达式） | 隐函数/偏导 | 跳步关键词,短display待判定 | 同理; 14579:\frac{\partial z}{\partial x} =\frac{1}{1+(y/x)^2}\cdot\left(\frac{y}{x}\right)'_{\!x} =\frac{x^2}{x^2+y^2}\cdot\left(-\frac{y}{x^2}\right) =\boxed{-\frac{y}{x^ \| 14587:\ | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 333 | 14603 | 多元函数微分学 | 知识讲解 | 复合函数的偏导数 | 隐函数/偏导 | 短display待判定 | 14612:f_x=5u^4u_x=5(3xy+2x)^4(3y+2), \qquad f_y=5u^4u_y=15x(3xy+2x)^4. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 334 | 14641 | 多元函数微分学 | 知识讲解 | 仅在某些方向存在方向导数 | 隐函数/偏导 | 短display待判定 | 14645:u(t)=f(t\cos\theta,t\sin\theta)=\sin 2\theta\quad(t\neq0), \qquad u(0)=f(0,0)=1. \| 14652:u'(0)=\lim_{t\to0}\frac{u(t)-u(0)}{t} =\lim_{t\to0}\frac{\sin2\theta-1}{t}. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 335 | 14758 | 多元函数微分学 | 知识讲解 | 范数函数的梯度 | 曲面积分/通量,隐函数/偏导 | 跳步关键词,短display待判定 | 同理; 14761:f(p)=\sqrt{x^2+y^2+z^2}=(x^2+y^2+z^2)^{1/2}. \| 14768:\frac{\partial f}{\partial x} =\frac{1}{2}(x^2+y^2+z^2)^{-1/2}\cdot 2x =\frac{x}{\sqrt{x^2+y^2+z^2}} =\frac{x}{\\|p\\|} | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 336 | 14815 | 多元函数微分学 | 知识讲解 | 沿特定方向的方向导数 | 隐函数/偏导 | 跳步关键词,短display待判定 | 可得; 14818:\frac{\partial z}{\partial x} =e^{xy}+xy\cdot e^{xy} =e^{xy}(1+xy),\qquad \frac{\partial z}{\partial y} =x\cdot e^{xy}\cdot x =x^2e^{xy}. \| 14834:\vec l=\dfrac{1}{\sqrt2} | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 337 | 14854 | 多元函数微分学 | 知识讲解 | 给定角度 | 隐函数/偏导 | 跳步关键词,短display待判定 | 于是; 14859:\left.\nabla u\right\|_{(1,1)} =\left(\frac{2}{2},\,\frac{2}{2}\right) =(1,\,1),\qquad \vec l=(\cos 60^\circ,\;\sin 60^\circ) =\left(\frac12,\;\frac{\sqrt3}{2}\r \| 14867:\ | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 338 | 14903 | 多元函数微分学 | 知识讲解 | 梯度为零的方向导数 | 隐函数/偏导 | 短display待判定 | 14912:\vec l=\dfrac{(1,-1)}{\sqrt{1^2+(-1)^2}} =\left(\dfrac{\sqrt2}{2},\,-\dfrac{\sqrt2}{2}\right). \| 14917:\dfrac{\partial f}{\partial\vec l}(1,1) =(e,e)\cdot\left(\dfrac{\sqrt2} | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 339 | 14951 | 多元函数微分学 | 知识讲解 | 证明某函数在原点可微 | 隐函数/偏导 | 短display待判定 | 14968:A h_1 + B h_2 = 1\cdot h_1 + 1\cdot h_2 = h_1 + h_2. \| 14972:\lim_{(h_1,h_2)\to(0,0)} \frac{f(h_1,h_2) - f(0,0) - (f_x(0,0)h_1 + f_y(0,0)h_2)}{\sqrt{h_1^2+h_2^2}} = 0. \| 1498 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 340 | 15059 | 多元函数微分学 | 知识讲解 | 偏导存在但不可微 | 隐函数/偏导 | 跳步关键词,短display待判定 | 直接,略; 15063:f_x(0,0)=\lim_{x\to 0}\frac{f(x,0)-f(0,0)}{x}=0,\qquad f_y(0,0)=\lim_{y\to 0}\frac{f(0,y)-f(0,0)}{y}=0. \| 15077:\lim_{h_1\to 0^+} \frac{h_1^2}{(2h_1^2)^{\frac32}} =\lim | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 341 | 15103 | 多元函数微分学 | 知识讲解 | 可微但偏导数不连续 | 隐函数/偏导 | 跳步关键词,短display待判定 | 同理; 15107:f_x(0,0)=\lim_{t\to 0}\frac{f(t,0)-0}{t} =\lim_{t\to 0}t\sin\frac{1}{t^2}=0,\qquad f_y(0,0)=\lim_{t\to 0}\frac{f(0,t)-0}{t}=0. \| 15122:f_x(x,0) =2x\sin\frac{1}{x^2}-\frac | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 342 | 15154 | 多元函数微分学 | 知识讲解 | 多项式的全微分 | 隐函数/偏导 | 短display待判定 | 15157:\frac{\partial z}{\partial x}=2x+4y^2, \qquad \frac{\partial z}{\partial y}=8xy+4y^3. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 343 | 15169 | 多元函数微分学 | 知识讲解 | 混合型函数的全微分 | 隐函数/偏导 | 短display待判定 | 15172:\frac{\partial u}{\partial x}=2,\qquad \frac{\partial u}{\partial y}=-\sin y+z e^{yz},\qquad \frac{\partial u}{\partial z}=ye^{yz}. \| 15178:\boxed{\mathrm{d}u=2\,\mathrm{d}x+ | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 344 | 15187 | 多元函数微分学 | 知识讲解 | 利用全微分做近似计算 | 隐函数/偏导 | 跳步关键词,短display待判定 | 可得,容易; 15200:f(x_0+h_1,\,y_0+h_2) \approx f(x_0,y_0)+f_x(x_0,y_0)\,h_1+f_y(x_0,y_0)\,h_2 \| 15205:(1.03)^{1.98} \approx 1+2\times 0.03+0\times(-0.02) =1+0.06=\boxed{1.06}. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 345 | 15545 | 多元函数微分学 | 知识讲解 | 螺旋线的速度向量 |  | 短display待判定 | 15549:f'(t)=(-\sin t,\;\cos t,\;1)^{\mathsf T} =-\vec i\sin t+\vec j\cos t+\vec k. \| 15559:\\|f'(t)\\|=\sqrt{(-\sin t)^2+(\cos t)^2+1^2} =\sqrt{2}. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 346 | 15577 | 多元函数微分学 | 知识讲解 | Jacobian 矩阵的完整计算 | 隐函数/偏导 | 跳步关键词,短display待判定 | 直接; 15579:f_1(x,y,z)=3x+e^yz,\qquad f_2(x,y,z)=x^3+y^2\sin z. \| 15609:f\!\left(\tfrac12+h_1,\,1+h_2,\,\pi+h_3\right) \approx f\!\left(\tfrac12,1,\pi\right) +Jf\!\left(\tfrac12,1,\p | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 347 | 15764 | 多元函数微分学 | 知识讲解 | 一元复合：中间变量含 $t$ |  | 跳步关键词,短display待判定 | 直接; 15788:\frac{\mathrm{d}z}{\mathrm{d}t} =z_xx_t+z_yy_t =y\cos x\cdot 3t^2+\sin x\cdot 5. \| 15794:\frac{\mathrm{d}z}{\mathrm{d}t} =\boxed{3t^2(5t+2)\cos(t^3)+5\sin(t^3)}. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 348 | 15803 | 多元函数微分学 | 知识讲解 | 二元复合：中间变量含 $u,v$ | 隐函数/偏导 | 跳步关键词 | 直接 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 349 | 15872 | 多元函数微分学 | 知识讲解 | 抽象复合函数的偏导数 | 隐函数/偏导 | 跳步关键词 | 直接 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 350 | 15953 | 多元函数微分学 | 知识讲解 | 利用全微分形式不变性求偏导 | 隐函数/偏导 | 跳步关键词,短display待判定 | 可得; 15958:\mathrm{d}u=2\,\mathrm{d}x+\mathrm{d}y, \qquad \mathrm{d}z=\cos u\,\mathrm{d}u. \| 15964:\mathrm{d}z =2\cos(2x+y)\,\mathrm{d}x +\cos(2x+y)\,\mathrm{d}y. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 351 | 15980 | 多元函数微分学 | 知识讲解 | 三元函数的全微分求偏导 |  | 跳步关键词 | 直接 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 352 | 16190 | 多元函数微分学 | 知识讲解 | 混合偏导数不相等 | 隐函数/偏导 | 跳步关键词,短display待判定 | 同理,直接; 16194:f_x(0,0)=0,\qquad f_y(0,0)=0. \| 16201:f_x(0,y)=\lim_{h\to 0}\frac{f(h,y)-f(0,y)}{h} =\lim_{h\to 0}y\cdot\frac{h^2-y^2}{h^2+y^2} =-y. \| 16210:f_y(x,0)=\lim_{k\to 0}\fra | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 353 | 16246 | 多元函数微分学 | 知识讲解 | 二阶偏导数的完整计算 | 隐函数/偏导 | 短display待判定 | 16248:z=F(u,v),\qquad u=x,\qquad v=y,\qquad F(u,v)=v\cos u+3u^2e^v. \| 16307:\boxed{ f_{xx}=-y\cos x+6e^y,\quad f_{xy}=f_{yx}=-\sin x+6xe^y,\quad f_{yy}=3x^2e^y }. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 354 | 16319 | 多元函数微分学 | 知识讲解 | arctan 的二阶偏导数 | 隐函数/偏导 | 跳步关键词,短display待判定 | 可得; 16321:z=F(u,v),\qquad u=x,\qquad v=y,\qquad F(u,v)=\arctan\frac{v}{u}. \| 16343:F_u=-\frac{v}{u^2+v^2},\qquad F_v=\frac{u}{u^2+v^2}. \| 16378:\boxed{ f_{xx}=\frac{2xy}{(x^2+y^2)^ | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 356 | 16483 | 多元函数微分学 | 知识讲解 | 另一个抽象复合函数 | 隐函数/偏导 | 跳步关键词,短display待判定 | 直接; 16508:\boxed{z_x=2f_u+y\cos x\,f_v}. \| 16588:\boxed{ z_{xy} =-2f_{uu}+(2\sin x-y\cos x)f_{uv} +y\sin x\cos x\,f_{vv} +\cos x\,f_v }. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 357 | 16611 | 多元函数微分学 | 知识讲解 | 二阶全微分的计算 | 隐函数/偏导 | 短display待判定 | 16623:\mathrm{d}^2z =z_{xx}\,\mathrm{d}x^2 +2z_{xy}\,\mathrm{d}x\,\mathrm{d}y +z_{yy}\,\mathrm{d}y^2. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 359 | 16715 | 多元函数微分学 | 知识讲解 | 参数曲线的基本计算 |  | 跳步关键词,短display待判定 | 整理得; 16725:x'(t)=2t+1,\qquad y'(t)=2t-1,\qquad z'(t)=2t. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 360 | 16755 | 多元函数微分学 | 知识讲解 | 显式曲线的切线与法平面 |  | 跳步关键词 | 整理得 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 361 | 16800 | 多元函数微分学 | 知识讲解 | 两柱面交线的切线与法平面 | 曲面积分/通量 | 短display待判定 | 16835:\boxed{\frac{x-a/\sqrt2}{1}=\frac{y-a/\sqrt2}{-1}=\frac{z-a/\sqrt2}{-1}}. \| 16839:1\cdot\left(x-\dfrac{a}{\sqrt2}\right) -1\cdot\left(y-\dfrac{a}{\sqrt2}\right) -1\cdot\left( | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 362 | 16939 | 多元函数微分学 | 知识讲解 | 显式曲面：反正切曲面 | 曲面积分/通量,隐函数/偏导 | 跳步关键词,短display待判定 | 整理得; 16946:z_x=-\frac{y}{x^2+y^2},\qquad z_y=\frac{x}{x^2+y^2}. \| 16953:z_x(1,1)=-\dfrac{1}{1+1}=-\dfrac{1}{2},\qquad z_y(1,1)=\dfrac{1}{1+1}=\dfrac{1}{2}. \| 16960:\vec{n}=(-z_x,-z | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 363 | 16981 | 多元函数微分学 | 知识讲解 | 隐式曲面：椭球面 | 曲面积分/通量,隐函数/偏导 | 短display待判定 | 16985:F(x,y,z)=\frac{x^2}{a^2}+\frac{y^2}{b^2}+\frac{z^2}{c^2}-1=0. \| 16991:F_x=\dfrac{2x}{a^2},\qquad F_y=\dfrac{2y}{b^2},\qquad F_z=\dfrac{2z}{c^2}. \| 16997:\nabla F(p_0)= \left( | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 364 | 17099 | 多元函数微分学 | 知识讲解 | 隐函数的全微分 | 隐函数/偏导 | 跳步关键词 | 直接,整理得 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 365 | 17240 | 多元函数微分学 | 知识讲解 | 线性方程组的隐函数 | 隐函数/偏导 | 跳步关键词 | 可得,略 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 366 | 17327 | 多元函数微分学 | 知识讲解 | 非线性方程组的隐函数 | 隐函数/偏导 | 短display待判定 | 17373:\boxed{ \frac{\partial u}{\partial x} = -\frac{z}{2uz+1},\qquad \frac{\partial v}{\partial x} = \frac{1}{2uz+1},\qquad \frac{\partial u}{\partial z} = \frac{z-v | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 367 | 17389 | 多元函数微分学 | 知识讲解 | 线性近似计算 | 隐函数/偏导 | 跳步关键词,短display待判定 | 可得; 17400:\frac{f_x}{f}=\frac{2}{x},\qquad \frac{f_y}{f}=-\frac{1}{2y},\qquad \frac{f_z}{f}=-\frac{1}{3z}. \| 17406:\nabla f(x,y,z) =f(x,y,z)\left(\frac{2}{x},\;-\frac{1}{2y},\;-\fr | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 370 | 17708 | 多元函数微分学 | 知识讲解 | 退化的 Hesse 判别：$\Delta=0$ 的三种可能性 | 极值/拉格朗日,隐函数/偏导 | 跳步关键词 | 显然,直接 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 371 | 17738 | 多元函数微分学 | 知识讲解 | 含三次项的多项式函数 | 极值/拉格朗日,隐函数/偏导 | 短display待判定 | 17742:f_x = x-3y-9,\qquad f_y = 9y^2+18y-3x+9. \| 17747:x-3y-9=0,\qquad 9y^2+18y-3x+9=0. \| 17751:9y^2+9y-18=0 \quad\Longleftrightarrow\quad (y+2)(y-1)=0. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 372 | 17770 | 多元函数微分学 | 知识讲解 | 超越函数的无穷多极值点 | 极值/拉格朗日,隐函数/偏导 | 短display待判定 | 17775:z_x=-(1+\mathrm{e}^{y})\sin x=0,\qquad z_y=\mathrm{e}^{y}(\cos x-1-y)=0. \| 17786:z_{xx}=-(1+\mathrm{e}^{y})\cos x,\qquad z_{xy}=-\mathrm{e}^{y}\sin x,\qquad z_{yy}=\mathrm{e} | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 373 | 17806 | 多元函数微分学 | 知识讲解 | 退化鞍点 | 极值/拉格朗日,隐函数/偏导 | 跳步关键词,短display待判定 | 直接; 17811:z_x=-6xy+8x^3=2x(4x^2-3y),\qquad z_y=2y-3x^2. \| 17820:z_{xx}=-6y+24x^2,\qquad z_{xy}=-6x,\qquad z_{yy}=2. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 374 | 17843 | 多元函数微分学 | 知识讲解 | 提高：Hesse 矩阵与极值判定 | 级数/幂级数,极值/拉格朗日,隐函数/偏导 | 跳步关键词,短display待判定 | 直接; 17847:f_x = 3x^2 - 3yz,\qquad f_y = 3y^2 - 3xz,\qquad f_z = 3z^2 - 3xy. \| 17855:f_{xx}=f_{yy}=f_{zz}=6,\qquad f_{xy}=f_{xz}=f_{yz}=-3. \| 17886:3(h_1^2+h_2^2+h_3^2)-3(h_1h_2+h_2 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 376 | 17938 | 多元函数微分学 | 知识讲解 | 思考题：三角函数在多边形域上的最值 | 极值/拉格朗日,隐函数/偏导 | 短display待判定 | 17968:f\left(\frac{\pi}{3},\frac{\pi}{3}\right) =\sin\frac{\pi}{3}\sin\frac{\pi}{3}\sin\frac{2\pi}{3} =\frac{3\sqrt{3}}{8}. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 377 | 17984 | 多元函数微分学 | 知识讲解 | 长方体的表面积最小化 | 极值/拉格朗日,隐函数/偏导 | 跳步关键词,短display待判定 | 直接,容易; 17993:\frac{S}{2} =xy+\frac{2}{x}+\frac{2}{y} \geqslant 3\sqrt[3]{xy\cdot\frac{2}{x}\cdot\frac{2}{y}} =3\sqrt[3]{4}. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 378 | 18029 | 多元函数微分学 | 知识讲解 | 圆周上的乘积极值 | 曲面积分/通量,极值/拉格朗日 | 跳步关键词,短display待判定 | 直接,于是; 18048:x+2\lambda(-2\lambda x)=x(1-4\lambda^2)=0. \| 18053:1-4\lambda^2=0,\qquad \lambda=\pm\frac12. \| 18057:(\sqrt2,\sqrt2),\quad (-\sqrt2,-\sqrt2),\quad (\sqrt2,-\sqrt2),\qu | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 379 | 18123 | 多元函数微分学 | 知识讲解 | 长方体表面积的 Lagrange 解法 | 极值/拉格朗日,隐函数/偏导 | 跳步关键词,短display待判定 | 同理; 18128:L(x,y,z;\lambda)=2(xy+yz+zx)+\lambda(xyz-2). \| 18144:\dfrac{1}{z}+\dfrac{1}{y} =\dfrac{1}{z}+\dfrac{1}{x} \implies x=y. \| 18153:\frac{S}{2}=xy+yz+zx \geqslant 3\sqrt[3]{( | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 380 | 18179 | 多元函数微分学 | 知识讲解 | 算术--几何平均不等式的最优化证明 | 极值/拉格朗日,隐函数/偏导 | 跳步关键词,短display待判定 | 可得,于是; 18184:L(x_1,\dots,x_n;\lambda) =x_1x_2\cdots x_n +\lambda(x_1+x_2+\cdots+x_n-a). \| 18191:\frac{\partial L}{\partial x_k} =\frac{x_1x_2\cdots x_n}{x_k}+\lambda=0 \implies \fr | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 381 | 18567 | 多元函数微分学 | 知识讲解 | 一般变量替换下的 PDE 变换 | 隐函数/偏导 | 跳步关键词,短display待判定 | 代入得; 18589:z_x=\frac{1}{v}+\frac{1}{v}\!\left(w_u\!\left(-\frac{v}{x^2}\right)+w_v\cdot 0\right)-0 =\frac{1}{v}-\frac{vw_u}{x^2v}=\frac{1}{v}-\frac{w_u}{x^2}. \| 18612:\frac{vw_{uu} | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 382 | 18645 | 多元函数微分学 | 习题 | 基本概念问答 | 极值/拉格朗日 | 短display待判定 | 18651:B_r(P_0)= \{(x,y)\in\mathbb R^2:\sqrt{(x-x_0)^2+(y-y_0)^2}<r\}. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 383 | 18689 | 多元函数微分学 | 习题 | 范数不等式的证明与几何意义 |  | 短display待判定 | 18692:\\|x-z\\|=\\|u+v\\|\leqslant \\|u\\|+\\|v\\| =\\|x-y\\|+\\|y-z\\|. \| 18699:\\|x\\|=\\|(x-y)+y\\|\leqslant \\|x-y\\|+\\|y\\|, \| 18704:-\\|x-y\\|\leqslant \\|x\\|-\\|y\\|\leqslant \\|x-y\\|, | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 385 | 18732 | 多元函数微分学 | 习题 | 点集拓扑基本概念的计算 |  | 短display待判定 | 18745:\partial B= \left\{(x,y)\mid \frac{x^2}{3}+\frac{y^2}{4}=1\right\} \cup \left\{(x,y)\mid \frac{x^2}{3}+\frac{y^2}{4}=5\right\}; \| 18752:(B^c)^\circ= \left\{(x,y)\mid \frac{x^ | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 386 | 18782 | 多元函数微分学 | 习题 | 开集性质的证明 |  | 短display待判定 | 18786:\\|z-p_0\\| =\\|(z-q)+(q-p_0)\\| \leqslant \\|z-q\\|+\\|q-p_0\\| <\delta+d=r. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 387 | 18801 | 多元函数微分学 | 习题 | 邻域概念的高维推广 |  | 跳步关键词,短display待判定 | 于是; 18803:\\|P-P_0\\|=\sqrt{\sum_{i=1}^n (x_i-a_i)^2}. \| 18807:B_r(P_0)=\{P\in\mathbb R^n\mid \\|P-P_0\\|<r\}. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 388 | 18827 | 多元函数微分学 | 习题 | 基础：定义域与图像 |  | 短display待判定 | 18833:D=\{(x,y)\mid \|x\|\leqslant1,\ \|y\|\geqslant1\}. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 389 | 18852 | 多元函数微分学 | 习题 | 基础：极坐标下的极限计算 |  | 跳步关键词,短display待判定 | 代入得; 18856:\frac{x^3+y^3}{x^2+y^2} =r(\cos^3\theta+\sin^3\theta). \| 18863:\left\|\frac{x^2\sin^2y}{x^2+2y^2}\right\| \leqslant \frac{r^2\cos^2\theta\cdot r^2\sin^2\theta} {r^2(\cos^2 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 390 | 18889 | 多元函数微分学 | 习题 | 基础：极限存在性判定 |  | 短display待判定 | 18894:f(x,x^3)=\frac{x^3\cdot x^3}{x^6+x^6}=\frac12. \| 18900:\left\|\frac{xy}{\|x\|+\|y\|}\right\| \leqslant \min\{\|x\|,\|y\|\} \leqslant \sqrt{x^2+y^2}\to0. \| 18908:\|(x^2+y^2)\cos \frac1{x | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 391 | 18923 | 多元函数微分学 | 习题 | 提高：累次极限与二重极限 |  | 跳步关键词,短display待判定 | 直接; 18926:\lim_{y\to0}\lim_{x\to0}\frac{x^2-y^2}{x^2+y^2} =\lim_{y\to0}(-1)=-1. \| 18931:\lim_{x\to0}\lim_{y\to0}\frac{x^2-y^2}{x^2+y^2} =\lim_{x\to0}1=1. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 392 | 18949 | 多元函数微分学 | 习题 | 提高：连续性综合 | 隐函数/偏导 | 短display待判定 | 18952:f(r\cos\theta,r\sin\theta)=r(\cos^3\theta+\sin^3\theta), \| 18958:f_x(0,0)=\lim_{h\to0}\frac{f(h,0)-f(0,0)}{h}=0,\qquad f_y(0,0)=0. \| 18963:\frac{f(x,y)-f(0,0)-0}{\sqrt{x^2+y^ | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 393 | 18988 | 多元函数微分学 | 习题 | 基本概念问答 |  | 短display待判定 | 18996:0<\sqrt{(x-x_0)^2+(y-y_0)^2}<\delta \quad\Longrightarrow\quad \|f(x,y)-A\|<\varepsilon, | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 394 | 19017 | 多元函数微分学 | 习题 | 求定义域 |  | 短display待判定 | 19025:D=\{(x,y)\mid \|y\|\leqslant \|x\|,\ x\neq0\}. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 395 | 19035 | 多元函数微分学 | 习题 | 齐次函数性质 |  | 跳步关键词 | 于是 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 397 | 19071 | 多元函数微分学 | 习题 | 构造函数表达式 |  | 跳步关键词 | 直接 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 398 | 19082 | 多元函数微分学 | 习题 | 多元函数极限计算 |  | 跳步关键词,短display待判定 | 直接; 19085:\lim_{\substack{x\to0\\ y\to1}}\frac{1-xy}{x^2+y^2}=1. \| 19090:\lim_{\substack{x\to2\\ y\to0}}\frac1{x^2+y^2}=\frac14. \| 19095:\left\|\frac{\sin(xy)}{x}\right\| \leqslant\f | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 399 | 19115 | 多元函数微分学 | 习题 | 连续性判定 |  | 短display待判定 | 19117:f(x,x^2)=\frac{x^2\cdot x^2}{x^4+x^4}=\frac12\qquad (x\neq0). | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 400 | 19127 | 多元函数微分学 | 习题 | 求间断点集 |  | 短display待判定 | 19134:x^3+y^3=(x+y)(x^2-xy+y^2). \| 19138:f(x,y)=\frac1{x^2-xy+y^2}. \| 19142:\frac1{x_0^2-x_0(-x_0)+(-x_0)^2}=\frac1{3x_0^2}. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 401 | 19163 | 多元函数微分学 | 习题 | 实际问题中的极限 | 重积分/换元 | 短display待判定 | 19167:Q(r\cos\theta,r\sin\theta) =\frac{17.86r^2\cos\theta\sin\theta} {r(1.798\cos\theta+\sin\theta)} =r\frac{17.86\cos\theta\sin\theta} {1.798\cos\theta+\sin\theta}. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 406 | 19271 | 多元函数微分学 | 习题 | 方向导数与偏导数的计算 | 隐函数/偏导 | 跳步关键词,短display待判定 | 于是; 19283:f_x(x,y,z)= \frac{1}{y} - \frac{z}{x^2},\qquad f_y(x,y,z)= -\frac{x}{y^2} + \frac{1}{z},\qquad f_z(x,y,z)= -\frac{y}{z^2} + \frac{1}{x}. \| 19290:f_x = \frac{y}{1+(xy)^2}, | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 407 | 19313 | 多元函数微分学 | 习题 | 可微性判定 | 隐函数/偏导 | 跳步关键词,短display待判定 | 同理; 19318:\frac{f(x,y)-f(0,0)}{\sqrt{x^2+y^2}} =\frac{\sqrt{\|xy\|}}{\sqrt{x^2+y^2}}. \| 19327:\frac{f(x,y)-f(0,0)}{\sqrt{x^2+y^2}} =\frac{x^3y}{(x^6+y^2)\sqrt{x^2+y^2}}. \| 19332:\fra | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 408 | 19353 | 多元函数微分学 | 习题 | 偏导数连续性的分析 | 隐函数/偏导 | 短display待判定 | 19363:f_x(0,0)=\lim_{x\to0}\frac{f(x,0)-0}{x}=1,\qquad f_y(0,0)=\lim_{y\to0}\frac{f(0,y)-0}{y}=0. \| 19368:f_x(r\cos\theta, r\sin\theta) =\cos^4\theta + 3\cos^2\theta\sin^2\theta,\q | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 409 | 19396 | 多元函数微分学 | 习题 | 方向导数与梯度的关系预告 | 极值/拉格朗日,隐函数/偏导 | 短display待判定 | 19400:f(p_0 + t\vec l) - f(p_0) = f_x(p_0)(tl_1) + f_y(p_0)(tl_2) + o(\\|t\vec l\\|) = t\bigl(f_x(p_0)l_1 + f_y(p_0)l_2\bigr) + o(\|t\|). \| 19410:D_{\vec l} f \leqslant \\|\nabla f(p_0) | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 410 | 19433 | 多元函数微分学 | 习题 | 基本概念问答 | 曲面积分/通量,隐函数/偏导 | 短display待判定 | 19437:\lim_{\Delta x\to0}\frac{f(x+\Delta x,y,z)-f(x,y,z)}{\Delta x} \| 19443:f(a+\Delta x,b+\Delta y)-f(a,b) =A\Delta x+B\Delta y+o(\rho), | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 411 | 19464 | 多元函数微分学 | 习题 | 偏导数的计算 | 隐函数/偏导 | 跳步关键词,短display待判定 | 显然; 19478:\frac{\partial z}{\partial x} =\sec^2\left(\frac{x^2}{y}\right)\frac{2x}{y},\qquad \frac{\partial z}{\partial y} =-\sec^2\left(\frac{x^2}{y}\right)\frac{x^2}{y^ \| 19489:u | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 412 | 19523 | 多元函数微分学 | 习题 | 指定点的偏导数计算 | 隐函数/偏导 | 跳步关键词,短display待判定 | 于是; 19532:z_x = -e^{-x}\sin(x+2y) + e^{-x}\cos(x+2y),\qquad z_y = 2e^{-x}\cos(x+2y). \| 19537:z_x(0,\pi/4)=-e^0\sin(\pi/2)+e^0\cos(\pi/2)=-1,\qquad z_y(0,\pi/4)=2e^0\cos(\pi/2)=0. \| | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 413 | 19569 | 多元函数微分学 | 习题 | 分段函数的偏导数 | 隐函数/偏导 | 短display待判定 | 19577:f_x(0,0)=\lim_{x\to0}\frac{f(x,0)-f(0,0)}{x}=0,\qquad f_y(0,0)=\lim_{y\to0}\frac{f(0,y)-f(0,0)}{y}=0. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 414 | 19594 | 多元函数微分学 | 习题 | 多元复合函数的偏导数 | 隐函数/偏导 | 跳步关键词,短display待判定 | 可得; 19597:\frac{\partial u}{\partial x_k}=\frac{1}{\sum_{i=1}^n x_i}. \| 19601:\frac{\partial u}{\partial x_k} =\frac{2x_k}{\sqrt{1-\left(\sum_{i=1}^n x_i^2\right)^2}}. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 415 | 19616 | 多元函数微分学 | 习题 | 全微分的计算 |  | 短display待判定 | 19633:z_x = -\frac{xy}{(x^2+y^2)^{3/2}},\qquad z_y = \frac{x^2}{(x^2+y^2)^{3/2}}. \| 19637:\mathrm{d}z = -\dfrac{xy}{(x^2+y^2)^{3/2}}\,\mathrm{d}x +\dfrac{x^2}{(x^2+y^2)^{3/2}}\,\ma | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 417 | 19685 | 多元函数微分学 | 习题 | 可微性判定与偏导数有界性 | 隐函数/偏导,重积分/换元 | 跳步关键词,短display待判定 | 可得,显然,同理,直接; 19689:f(r\cos\theta,r\sin\theta)=r\cos\theta\sin\theta. \| 19696:f_x(x,y)=\frac{y^3}{(x^2+y^2)^{3/2}},\qquad f_y(x,y)=\frac{x^3}{(x^2+y^2)^{3/2}}, \| 19702:\|y^3\|=\|y\|^3\l | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 418 | 19729 | 多元函数微分学 | 习题 | 偏导数的计算与求导法则 |  | 跳步关键词,短display待判定 | 化简得,直接; 19736:\frac{(21x^2y^6-2y)(15xy-8) - (3x^2y^7-y^2)(15x)}{(15xy-8)^2}, \| 19740:\frac{270x^3y^7-168x^2y^6-15xy^2+16y}{(15xy-8)^2}. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 419 | 19765 | 多元函数微分学 | 习题 | 分段函数在指定点的偏导数 | 隐函数/偏导 | 跳步关键词,短display待判定 | 同理; 19768:f_x(0,0) =\lim_{x\to0}\frac{f(x,0)-f(0,0)}{x} =\lim_{x\to0}\frac{x^3/x^2-0}{x} =1. \| 19777:f_x(0,0)=\lim_{x\to0}\frac{f(x,0)-0}{x}=0,\qquad f_y(0,0)=\lim_{y\to0}\frac{f(0 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 420 | 19787 | 多元函数微分学 | 习题 | 全微分近似值计算 | 隐函数/偏导 | 短display待判定 | 19794:f(1-0.03,1+0.05) \approx 1+1(-0.03)+0(0.05) =\boxed{0.97}. \| 19807:f(29^\circ,46^\circ) \approx 0.5+\frac{\sqrt3}{2}\left(-\frac{\pi}{180}\right) +\frac{\pi}{180} =0.5+\frac{ | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 421 | 19825 | 多元函数微分学 | 习题 | 偏导数不连续但可微的证明 | 隐函数/偏导,重积分/换元 | 跳步关键词,短display待判定 | 可得,同理,于是; 19837:f_x(r\cos\theta,r\sin\theta) =r\sin\theta\sin\frac{1}{r} -\cos^2\theta\sin\theta\cos\frac{1}{r}. \| 19848:f_y(x,y) =x\sin\frac{1}{\sqrt{x^2+y^2}} -\frac{xy^2}{(x^2+y | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 422 | 19876 | 多元函数微分学 | 习题 | 绝对值与函数可微性 | 隐函数/偏导 | 短display待判定 | 19880:f_x(0,0) = \lim_{\Delta x \to 0} \frac{f(\Delta x,0)-f(0,0)}{\Delta x} = \lim_{\Delta x \to 0}\frac{\|\Delta x\|}{\Delta x}. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 423 | 19904 | 多元函数微分学 | 习题 | 基础：向量值函数的极限与连续 |  | 跳步关键词 | 同理 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 424 | 19937 | 多元函数微分学 | 习题 | 基础：Jacobian 矩阵计算 | 隐函数/偏导 | 跳步关键词 | 可得,直接 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 426 | 20034 | 多元函数微分学 | 习题 | Jacobian 行列式与坐标变换 | 隐函数/偏导,重积分/换元 | 跳步关键词,短display待判定 | 计算得,显然; 20038:J(g \circ f)(\boldsymbol x) =Jg(f(\boldsymbol x))\cdot Jf(\boldsymbol x). \| 20043:\det J(g \circ f)(\boldsymbol x) =\det Jg(f(\boldsymbol x))\cdot \det Jf(\boldsymbol | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 427 | 20089 | 多元函数微分学 | 习题 | 概念与基本性质问答 | 隐函数/偏导 | 短display待判定 | 20097:0 < \\|\boldsymbol x-\boldsymbol a\\|_n < \delta,\quad \boldsymbol x\in D \quad\Longrightarrow\quad \\|f(\boldsymbol x)-\boldsymbol A\\|_m<\varepsilon, \| 20111:f(\boldsymbol x^\c | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 428 | 20125 | 多元函数微分学 | 习题 | Jacobian 矩阵计算（二维） | 隐函数/偏导 | 短display待判定 | 20129:\frac{\partial f_1}{\partial x}=2x,\quad \frac{\partial f_1}{\partial y}=2y,\quad \frac{\partial f_2}{\partial x}=3y,\quad \frac{\partial f_2}{\partial y}=3x. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 431 | 20220 | 多元函数微分学 | 习题 | 基本概念问答 | 隐函数/偏导 | 跳步关键词 | 可得 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 432 | 20254 | 多元函数微分学 | 习题 | 链式法则求一阶导数 | 隐函数/偏导 | 跳步关键词,短display待判定 | 直接; 20277:\frac{\mathrm{d}z}{\mathrm{d}t} = \frac{3t^2}{t^3+1} - \frac{2}{t} = \frac{t^3-2}{t(t^3+1)}. \| 20295:\frac{\mathrm{d}z}{\mathrm{d}t} =e^y(2)+(x+y+1)e^y(-2t) =2e^{1-t^2}(1 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 433 | 20323 | 多元函数微分学 | 习题 | 链式法则求偏导数 | 隐函数/偏导 | 短display待判定 | 20355:\frac{\partial z}{\partial u} =\frac{2}{1+(x+y)^2}+\frac{2uv}{1+(x+y)^2} =\frac{2(1+uv)}{1+(x+y)^2}, \| 20360:\frac{\partial z}{\partial v} =\frac{-2v}{1+(x+y)^2}+\frac{u^2}{1 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 435 | 20415 | 多元函数微分学 | 习题 | 点处偏导数与全导数计算 | 隐函数/偏导 | 短display待判定 | 20446:\left.\frac{\mathrm{d}u}{\mathrm{d}w}\right\|_{w=1} =\frac{\partial u}{\partial s}\frac{\mathrm{d}s}{\mathrm{d}w} +\frac{\partial u}{\partial t}\frac{\mathrm{d}t | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 436 | 20459 | 多元函数微分学 | 习题 | 抽象复合函数求导 | 隐函数/偏导 | 短display待判定 | 20463:z_x=f'(v)\frac{x}{v},\qquad z_y=f'(v)\frac{y}{v}. \| 20472:z_x=f_1'+\frac{1}{y}f_2',\qquad z_y=-\frac{x}{y^2}f_2'. \| 20478:u_x=f_1'+yf_2'+yzf_3',\qquad u_y=xf_2'+xzf_3',\qquad | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 437 | 20494 | 多元函数微分学 | 习题 | 求具体函数的二阶偏导数 | 隐函数/偏导 | 短display待判定 | 20519:z_x = \frac{y e^y}{(x+y)^2},\qquad z_y = \frac{x(x+y-1)e^y}{(x+y)^2}. \| 20524:z_{xx}=\frac{-2y e^y}{(x+y)^3},\qquad z_{xy}=\frac{e^y(xy+y^2+x-y)}{(x+y)^3}, \| 20528:z_{yy}=\fr | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 438 | 20556 | 多元函数微分学 | 习题 | 二阶偏导数在原点的值 | 级数/幂级数,隐函数/偏导 | 跳步关键词,短display待判定 | 直接; 20567:f_{xx}=\frac{\partial}{\partial x}(b+2d x+ey)=2d \quad\Longrightarrow\quad d=\frac12 f_{xx}(0,0). \| 20574:f_{yy}=\frac{\partial}{\partial y}(c+ex+2ky)=2k \quad\Longrighta | 人工逐题复核；若确认则补推导/改排版/统一方法 |

> 自动标记项共 1086 条，Markdown 仅列前 400 条；完整逐题台账见 `solution_quality_audit/solution_index.csv`。

## 全量逐题索引
| 全局序号 | 行号 | 章节 | 小节 | 状态 | 标记 |
|---:|---:|---|---|---|---|
| 1 | 1413 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 2 | 1468 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 3 | 1503 | 不定积分 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 4 | 1517 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 5 | 1558 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 6 | 1595 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 7 | 1614 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 8 | 1645 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 9 | 1700 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 10 | 1751 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 11 | 1796 | 不定积分 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 12 | 1809 | 不定积分 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 13 | 1823 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 14 | 1837 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 15 | 1851 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 16 | 1874 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 17 | 1897 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 18 | 1911 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 19 | 1925 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 20 | 1949 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 21 | 1968 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 22 | 1988 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 23 | 2008 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 24 | 2028 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 25 | 2048 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 26 | 2080 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 27 | 2119 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 28 | 2141 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 29 | 2164 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 30 | 2181 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 31 | 2214 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 32 | 2236 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 33 | 2266 | 不定积分 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 34 | 2281 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 35 | 2297 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 36 | 2320 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 37 | 2340 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 38 | 2367 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 39 | 2398 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 40 | 2450 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 41 | 2469 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 42 | 2496 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 43 | 2518 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 44 | 2533 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 45 | 2548 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 46 | 2578 | 不定积分 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 47 | 2595 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 48 | 2623 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 49 | 2643 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 50 | 2671 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 51 | 2715 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 52 | 2729 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 53 | 2757 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 54 | 2779 | 不定积分 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 55 | 2796 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 56 | 2821 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 57 | 2842 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 58 | 2857 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 59 | 2872 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 60 | 2900 | 不定积分 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 61 | 2917 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 62 | 2936 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 63 | 2956 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 64 | 2986 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 65 | 3031 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 66 | 3045 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 67 | 3073 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 68 | 3093 | 不定积分 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 69 | 3111 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 70 | 3133 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 71 | 3155 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 72 | 3170 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 73 | 3185 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 74 | 3213 | 不定积分 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 75 | 3229 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 76 | 3257 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 77 | 3277 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 78 | 3307 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 79 | 3352 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 80 | 3366 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 81 | 3394 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 82 | 3415 | 不定积分 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 83 | 3432 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 84 | 3464 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 85 | 3496 | 不定积分 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 86 | 3517 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 87 | 3548 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 88 | 3576 | 不定积分 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 89 | 3598 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 90 | 3626 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 91 | 3657 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 92 | 3671 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 93 | 3699 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 94 | 3723 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 95 | 3745 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 96 | 3777 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 97 | 3800 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 98 | 3835 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 99 | 3870 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 100 | 3889 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 101 | 3908 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 102 | 3927 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 103 | 3946 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 104 | 3980 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 105 | 4013 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 106 | 4049 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 107 | 4085 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 108 | 4123 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 109 | 4157 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 110 | 4211 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 111 | 4246 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 112 | 4285 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 113 | 4321 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 114 | 4387 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 115 | 4454 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 116 | 4490 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 117 | 4531 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 118 | 4560 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 119 | 4591 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 120 | 4627 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 121 | 4672 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 122 | 4701 | 不定积分 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 123 | 4732 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 124 | 4772 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 125 | 4798 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 126 | 4844 | 不定积分 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 127 | 4885 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 128 | 4915 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 129 | 4957 | 不定积分 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 130 | 4995 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 131 | 5022 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 132 | 5041 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 133 | 5075 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 134 | 5110 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 135 | 5135 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 136 | 5167 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 137 | 5192 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 138 | 5215 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 139 | 5260 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 140 | 5306 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 141 | 5330 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 142 | 5353 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 143 | 5395 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 144 | 5418 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 145 | 5456 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 146 | 5482 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 147 | 5508 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 148 | 5532 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 149 | 5562 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 150 | 5585 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 151 | 5610 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 152 | 5634 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 153 | 5662 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 154 | 5690 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 155 | 5735 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 156 | 5803 | 微分方程 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 157 | 5832 | 微分方程 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 158 | 5846 | 微分方程 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 159 | 5870 | 微分方程 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 160 | 5885 | 微分方程 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 161 | 5927 | 微分方程 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 162 | 5967 | 微分方程 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 163 | 6027 | 微分方程 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 164 | 6085 | 微分方程 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 165 | 6152 | 微分方程 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 166 | 6210 | 微分方程 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 167 | 6307 | 微分方程 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 168 | 6407 | 微分方程 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 169 | 6436 | 微分方程 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 170 | 6459 | 微分方程 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 171 | 6506 | 微分方程 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 172 | 6573 | 微分方程 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 173 | 6717 | 微分方程 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 174 | 6832 | 微分方程 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 175 | 6886 | 微分方程 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 176 | 6921 | 微分方程 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险,短display待判定 |
| 177 | 6997 | 微分方程 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定,高风险题解过短 |
| 178 | 7008 | 微分方程 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 179 | 7035 | 微分方程 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 180 | 7056 | 微分方程 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 181 | 7087 | 微分方程 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 182 | 7108 | 微分方程 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 183 | 7160 | 微分方程 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 184 | 7236 | 微分方程 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 185 | 7317 | 微分方程 | 知识讲解 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 186 | 7416 | 微分方程 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 187 | 7449 | 微分方程 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 188 | 7495 | 微分方程 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 189 | 7504 | 微分方程 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,高风险题解过短 |
| 190 | 7517 | 微分方程 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 191 | 7536 | 微分方程 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 192 | 7574 | 微分方程 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 193 | 7606 | 微分方程 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 194 | 7640 | 微分方程 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 195 | 7717 | 微分方程 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 196 | 7884 | 微分方程 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 197 | 8012 | 微分方程 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 198 | 8047 | 微分方程 | 知识讲解 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 199 | 8148 | 微分方程 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 200 | 8199 | 微分方程 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 201 | 8253 | 微分方程 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 202 | 8265 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 203 | 8273 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 204 | 8281 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 205 | 8304 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 206 | 8354 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 207 | 8386 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 208 | 8418 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 209 | 8476 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 210 | 8506 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 211 | 8526 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 212 | 8539 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 213 | 8567 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 214 | 8650 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 215 | 8667 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 216 | 8755 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 217 | 8803 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 218 | 8868 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 219 | 8908 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 220 | 8950 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 221 | 8997 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 222 | 9037 | 微分方程 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 223 | 9058 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 224 | 9079 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 225 | 9134 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 226 | 9164 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 227 | 9217 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 228 | 9247 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 229 | 9287 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 230 | 9317 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 231 | 9340 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 232 | 9428 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 233 | 9552 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 234 | 9611 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 235 | 9640 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 236 | 9717 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 237 | 9754 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 238 | 9835 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 239 | 9907 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 240 | 9936 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 241 | 9983 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 242 | 10023 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 243 | 10054 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 244 | 10110 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 245 | 10135 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 246 | 10170 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 247 | 10251 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 248 | 10336 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 249 | 10480 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 250 | 10499 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 251 | 10537 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 252 | 10569 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 253 | 10612 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 254 | 10645 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 255 | 10675 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 256 | 10700 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 257 | 10746 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 258 | 10844 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 259 | 10987 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 260 | 11011 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 261 | 11112 | 微分方程 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 262 | 11135 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 263 | 11151 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 264 | 11191 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 265 | 11218 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 266 | 11242 | 微分方程 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 267 | 11256 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 268 | 11288 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 269 | 11330 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 270 | 11358 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 271 | 11383 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 272 | 11424 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 273 | 11443 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 274 | 11474 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 275 | 11519 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 276 | 11545 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 277 | 11595 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 278 | 11701 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 279 | 11878 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 280 | 11978 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 281 | 12061 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 282 | 12172 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 283 | 12219 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 284 | 12256 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 285 | 12295 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 286 | 12336 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 287 | 12382 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 288 | 12418 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 289 | 12457 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 290 | 12482 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 291 | 12520 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 292 | 12575 | 微分方程 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 293 | 12620 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 294 | 12721 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 295 | 12800 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 296 | 12855 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 297 | 12903 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 298 | 12944 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 299 | 13030 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 300 | 13076 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 301 | 13100 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 302 | 13130 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 303 | 13165 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 304 | 13218 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 305 | 13258 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 306 | 13305 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 307 | 13346 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 308 | 13376 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 309 | 13442 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 310 | 13482 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 311 | 13518 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 312 | 13559 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 313 | 13596 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 314 | 13658 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 315 | 13692 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 316 | 13914 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 317 | 13944 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 318 | 13972 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 319 | 14062 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 320 | 14105 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 321 | 14141 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 322 | 14196 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 323 | 14230 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 324 | 14259 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 325 | 14277 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 326 | 14306 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 327 | 14363 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 328 | 14380 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 329 | 14406 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 330 | 14524 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 331 | 14555 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 332 | 14574 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 333 | 14603 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 334 | 14641 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 335 | 14758 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 336 | 14815 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 337 | 14854 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 338 | 14903 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 339 | 14951 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 340 | 15059 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 341 | 15103 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 342 | 15154 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 343 | 15169 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 344 | 15187 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 345 | 15545 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 346 | 15577 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 347 | 15764 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 348 | 15803 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 349 | 15872 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 350 | 15953 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 351 | 15980 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 352 | 16190 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 353 | 16246 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 354 | 16319 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 355 | 16391 | 多元函数微分学 | 知识讲解 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 356 | 16483 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 357 | 16611 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 358 | 16693 | 多元函数微分学 | 知识讲解 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 359 | 16715 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 360 | 16755 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 361 | 16800 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 362 | 16939 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 363 | 16981 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 364 | 17099 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 365 | 17240 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 366 | 17327 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 367 | 17389 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 368 | 17607 | 多元函数微分学 | 知识讲解 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 369 | 17627 | 多元函数微分学 | 知识讲解 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 370 | 17708 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 371 | 17738 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 372 | 17770 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 373 | 17806 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 374 | 17843 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 375 | 17913 | 多元函数微分学 | 知识讲解 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 376 | 17938 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 377 | 17984 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 378 | 18029 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 379 | 18123 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 380 | 18179 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 381 | 18567 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 382 | 18645 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 383 | 18689 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 384 | 18717 | 多元函数微分学 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 385 | 18732 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 386 | 18782 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 387 | 18801 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 388 | 18827 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 389 | 18852 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 390 | 18889 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 391 | 18923 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 392 | 18949 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 393 | 18988 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 394 | 19017 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 395 | 19035 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 396 | 19052 | 多元函数微分学 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 397 | 19071 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 398 | 19082 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 399 | 19115 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 400 | 19127 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 401 | 19163 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 402 | 19186 | 多元函数微分学 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 403 | 19209 | 多元函数微分学 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 404 | 19229 | 多元函数微分学 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 405 | 19247 | 多元函数微分学 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 406 | 19271 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 407 | 19313 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 408 | 19353 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 409 | 19396 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 410 | 19433 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 411 | 19464 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 412 | 19523 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 413 | 19569 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 414 | 19594 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 415 | 19616 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 416 | 19655 | 多元函数微分学 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 417 | 19685 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 418 | 19729 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 419 | 19765 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 420 | 19787 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 421 | 19825 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 422 | 19876 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 423 | 19904 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 424 | 19937 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 425 | 19978 | 多元函数微分学 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 426 | 20034 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 427 | 20089 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 428 | 20125 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 429 | 20147 | 多元函数微分学 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 430 | 20177 | 多元函数微分学 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 431 | 20220 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 432 | 20254 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 433 | 20323 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 434 | 20393 | 多元函数微分学 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 435 | 20415 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 436 | 20459 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 437 | 20494 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 438 | 20556 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 439 | 20587 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 440 | 20618 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 441 | 20714 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 442 | 20787 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 443 | 20827 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 444 | 20868 | 多元函数微分学 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 445 | 20908 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 446 | 20942 | 多元函数微分学 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 447 | 20970 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 448 | 20998 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 449 | 21025 | 多元函数微分学 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 450 | 21048 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 451 | 21076 | 多元函数微分学 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 452 | 21110 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 453 | 21169 | 多元函数微分学 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 454 | 21215 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 455 | 21243 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 456 | 21262 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 457 | 21281 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 458 | 21312 | 多元函数微分学 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 459 | 21341 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 460 | 21363 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 461 | 21432 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 462 | 21467 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 463 | 21501 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 464 | 21533 | 多元函数微分学 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 465 | 21560 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 466 | 21586 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 467 | 21649 | 多元函数微分学 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 468 | 21689 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 469 | 21759 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 470 | 21793 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 471 | 21823 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 472 | 21851 | 多元函数微分学 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 473 | 21882 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 474 | 21907 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 475 | 21936 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 476 | 21955 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 477 | 22003 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 478 | 22043 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险,短display待判定 |
| 479 | 22076 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 480 | 22093 | 多元函数微分学 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 481 | 22109 | 多元函数微分学 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 482 | 22131 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险,短display待判定 |
| 483 | 22169 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险,短display待判定 |
| 484 | 22198 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险 |
| 485 | 22220 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险,短display待判定 |
| 486 | 22260 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 487 | 22278 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险,短display待判定 |
| 488 | 22302 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 489 | 22344 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 490 | 22380 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险,短display待判定 |
| 491 | 22421 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 492 | 22467 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 493 | 22521 | 多元函数微分学 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 494 | 22542 | 多元函数微分学 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 495 | 22611 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险,短display待判定 |
| 496 | 22716 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 497 | 22764 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险,短display待判定 |
| 498 | 22792 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险,短display待判定 |
| 499 | 22847 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 500 | 22882 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 501 | 22908 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险 |
| 502 | 22924 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 503 | 22955 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险,短display待判定 |
| 504 | 22990 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 505 | 23023 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 506 | 23073 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险,短display待判定 |
| 507 | 23129 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险,短display待判定 |
| 508 | 23189 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 509 | 23220 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 510 | 23241 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险,短display待判定 |
| 511 | 23316 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 512 | 23339 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 513 | 23351 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 514 | 23409 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 515 | 23472 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 516 | 23506 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 517 | 23523 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 518 | 23564 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 519 | 23635 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险,短display待判定 |
| 520 | 23735 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 521 | 23816 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 522 | 23840 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险,短display待判定 |
| 523 | 23874 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险,短display待判定 |
| 524 | 23931 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险,短display待判定 |
| 525 | 24044 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 526 | 24149 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险,短display待判定 |
| 527 | 24184 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险,短display待判定 |
| 528 | 24238 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 529 | 24279 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 530 | 24299 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 531 | 24319 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 532 | 24342 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 533 | 24365 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 534 | 24387 | 多元函数微分学 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 535 | 24404 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 536 | 24453 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险,短display待判定 |
| 537 | 24495 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 538 | 24517 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 539 | 24551 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 540 | 24569 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 541 | 24598 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险,短display待判定 |
| 542 | 24627 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 543 | 24674 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险 |
| 544 | 24697 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,高风险题解过短 |
| 545 | 24712 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 546 | 24742 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 547 | 24768 | 多元函数微分学 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 548 | 24783 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险,短display待判定 |
| 549 | 24805 | 多元函数微分学 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 550 | 24821 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 551 | 24853 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 552 | 24868 | 多元函数微分学 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 553 | 24882 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 554 | 24914 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 555 | 24941 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险,短display待判定 |
| 556 | 25032 | 重积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 557 | 25056 | 重积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险 |
| 558 | 25069 | 重积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险 |
| 559 | 25089 | 重积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险,短display待判定 |
| 560 | 25168 | 重积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 561 | 25185 | 重积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 562 | 25233 | 重积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 563 | 25285 | 重积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 564 | 25305 | 重积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 565 | 25343 | 重积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险,短display待判定 |
| 566 | 25424 | 重积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 567 | 25450 | 重积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 568 | 25508 | 重积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 569 | 25577 | 重积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险,高风险题解过短 |
| 570 | 25589 | 重积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险,短display待判定 |
| 571 | 25619 | 重积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险,短display待判定 |
| 572 | 25744 | 重积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 573 | 25795 | 重积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险,短display待判定 |
| 574 | 25843 | 重积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险 |
| 575 | 25884 | 重积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险 |
| 576 | 25903 | 重积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 577 | 25933 | 重积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险,短display待判定 |
| 578 | 25970 | 重积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 579 | 26008 | 重积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 580 | 26050 | 重积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 581 | 26090 | 重积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 582 | 26144 | 重积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 583 | 26181 | 重积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险,短display待判定 |
| 584 | 26213 | 重积分 | 知识讲解 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 585 | 26242 | 重积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 586 | 26274 | 重积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 587 | 26312 | 重积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 588 | 26330 | 重积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 589 | 26354 | 重积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 590 | 26375 | 重积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 591 | 26391 | 重积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 592 | 26430 | 重积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 593 | 26462 | 重积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险,短display待判定 |
| 594 | 26497 | 重积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险,短display待判定 |
| 595 | 26549 | 重积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 596 | 26639 | 重积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 597 | 26748 | 重积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 598 | 26821 | 重积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 599 | 26857 | 重积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 600 | 26877 | 重积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 601 | 26907 | 重积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 602 | 26938 | 重积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 603 | 26981 | 重积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险 |
| 604 | 27002 | 重积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 605 | 27051 | 重积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险,短display待判定 |
| 606 | 27072 | 重积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险,短display待判定 |
| 607 | 27093 | 重积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 608 | 27125 | 重积分 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 609 | 27141 | 重积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 610 | 27185 | 重积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险,短display待判定 |
| 611 | 27207 | 重积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险,短display待判定 |
| 612 | 27231 | 重积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 613 | 27286 | 重积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 614 | 27346 | 重积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 615 | 27394 | 重积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险,短display待判定 |
| 616 | 27475 | 重积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 617 | 27585 | 重积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 618 | 27663 | 重积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险,短display待判定 |
| 619 | 27710 | 重积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险,短display待判定 |
| 620 | 27753 | 重积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险,短display待判定 |
| 621 | 27797 | 重积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险,短display待判定 |
| 622 | 27862 | 重积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险,短display待判定 |
| 623 | 27896 | 重积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 624 | 27932 | 重积分 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 625 | 27968 | 重积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 626 | 27992 | 重积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 627 | 28026 | 重积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 628 | 28056 | 重积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险 |
| 629 | 28068 | 重积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 630 | 28086 | 重积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 631 | 28114 | 重积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 632 | 28158 | 重积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险,短display待判定 |
| 633 | 28205 | 重积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 634 | 28265 | 重积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险,短display待判定 |
| 635 | 28287 | 重积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 636 | 28311 | 重积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 637 | 28344 | 重积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 638 | 28364 | 重积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 639 | 28394 | 重积分 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 640 | 28407 | 重积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险,短display待判定 |
| 641 | 28429 | 重积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险,短display待判定 |
| 642 | 28451 | 重积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 643 | 28471 | 重积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 644 | 28692 | 曲线积分与曲面积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定,display密度偏高 |
| 645 | 28716 | 曲线积分与曲面积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 646 | 28743 | 曲线积分与曲面积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 647 | 28766 | 曲线积分与曲面积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 648 | 28793 | 曲线积分与曲面积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 649 | 28806 | 曲线积分与曲面积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险 |
| 650 | 28860 | 曲线积分与曲面积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 651 | 28889 | 曲线积分与曲面积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 652 | 28902 | 曲线积分与曲面积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 653 | 28927 | 曲线积分与曲面积分 | 知识讲解 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 654 | 28937 | 曲线积分与曲面积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 655 | 28981 | 曲线积分与曲面积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 656 | 29020 | 曲线积分与曲面积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 657 | 29058 | 曲线积分与曲面积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 658 | 29130 | 曲线积分与曲面积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 659 | 29156 | 曲线积分与曲面积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 660 | 29181 | 曲线积分与曲面积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 661 | 29201 | 曲线积分与曲面积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 662 | 29217 | 曲线积分与曲面积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 663 | 29246 | 曲线积分与曲面积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 664 | 29273 | 曲线积分与曲面积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 665 | 29293 | 曲线积分与曲面积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 666 | 29376 | 曲线积分与曲面积分 | 知识讲解 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 667 | 29404 | 曲线积分与曲面积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 668 | 29422 | 曲线积分与曲面积分 | 知识讲解 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 669 | 29442 | 曲线积分与曲面积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 670 | 29524 | 曲线积分与曲面积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 671 | 29563 | 曲线积分与曲面积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 672 | 29612 | 曲线积分与曲面积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 673 | 29665 | 曲线积分与曲面积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 674 | 29729 | 曲线积分与曲面积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 675 | 29850 | 曲线积分与曲面积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 676 | 29872 | 曲线积分与曲面积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 677 | 29900 | 曲线积分与曲面积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 678 | 29923 | 曲线积分与曲面积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 679 | 29970 | 曲线积分与曲面积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 680 | 30093 | 曲线积分与曲面积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 681 | 30121 | 曲线积分与曲面积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 682 | 30148 | 曲线积分与曲面积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 683 | 30298 | 曲线积分与曲面积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 684 | 30424 | 曲线积分与曲面积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 685 | 30461 | 曲线积分与曲面积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 686 | 30488 | 曲线积分与曲面积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 687 | 30543 | 曲线积分与曲面积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 688 | 30593 | 曲线积分与曲面积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 689 | 30729 | 曲线积分与曲面积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 690 | 30759 | 曲线积分与曲面积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 691 | 30814 | 曲线积分与曲面积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 692 | 30843 | 曲线积分与曲面积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 693 | 30880 | 曲线积分与曲面积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 694 | 30914 | 曲线积分与曲面积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 695 | 30975 | 曲线积分与曲面积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 696 | 31020 | 曲线积分与曲面积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 697 | 31135 | 曲线积分与曲面积分 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 698 | 31153 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 699 | 31214 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 700 | 31237 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 701 | 31263 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 702 | 31293 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 703 | 31327 | 曲线积分与曲面积分 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 704 | 31339 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 705 | 31376 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 706 | 31428 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 707 | 31496 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 708 | 31561 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 709 | 31588 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 710 | 31640 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 711 | 31684 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 712 | 31723 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 713 | 31828 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 714 | 31856 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 715 | 31888 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 716 | 31916 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 717 | 31947 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 718 | 31981 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 719 | 32116 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 720 | 32144 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 721 | 32177 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 722 | 32206 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 723 | 32242 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 724 | 32263 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 725 | 32288 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 726 | 32318 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 727 | 32340 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 728 | 32380 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 729 | 32427 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 730 | 32474 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 731 | 32516 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 732 | 32539 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 733 | 32583 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 734 | 32609 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 735 | 32648 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 736 | 32677 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 737 | 32703 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 738 | 32723 | 曲线积分与曲面积分 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 739 | 32737 | 曲线积分与曲面积分 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 740 | 32759 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 741 | 32782 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 742 | 32811 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 743 | 32841 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 744 | 32871 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 745 | 32899 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 746 | 32919 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 747 | 32935 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 748 | 32960 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 749 | 32985 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 750 | 33037 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 751 | 33063 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 752 | 33106 | 曲线积分与曲面积分 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 753 | 33133 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 754 | 33160 | 曲线积分与曲面积分 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 755 | 33177 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 756 | 33189 | 曲线积分与曲面积分 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 757 | 33209 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 758 | 33250 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 759 | 33362 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 760 | 33436 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 761 | 33516 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 762 | 33596 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 763 | 33677 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 764 | 34069 | 级数 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 765 | 34128 | 级数 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 766 | 34187 | 级数 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 767 | 34273 | 级数 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 768 | 35533 | 级数 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 769 | 35552 | 级数 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 770 | 35580 | 级数 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 771 | 35604 | 级数 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 772 | 35636 | 级数 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 773 | 35672 | 级数 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 774 | 35702 | 级数 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 775 | 35784 | 级数 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 776 | 35861 | 级数 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 777 | 35919 | 级数 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 778 | 35957 | 级数 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 779 | 36000 | 级数 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 780 | 36026 | 级数 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 781 | 36055 | 级数 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 782 | 36080 | 级数 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 783 | 36110 | 级数 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 784 | 36123 | 级数 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 785 | 36145 | 级数 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 786 | 36164 | 级数 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 787 | 36184 | 级数 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 788 | 36213 | 级数 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,高风险题解过短 |
| 789 | 36222 | 级数 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 790 | 36246 | 级数 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 791 | 36273 | 级数 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 792 | 36319 | 级数 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 793 | 36397 | 级数 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 794 | 36462 | 级数 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 795 | 36497 | 级数 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 796 | 36515 | 级数 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 797 | 36559 | 级数 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 798 | 36625 | 级数 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 799 | 36645 | 级数 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 800 | 36676 | 级数 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 801 | 36744 | 级数 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 802 | 36779 | 级数 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 803 | 36946 | 级数 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 804 | 36971 | 级数 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 805 | 36999 | 级数 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 806 | 37051 | 级数 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 807 | 37264 | 级数 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 808 | 37303 | 级数 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 809 | 37394 | 级数 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 810 | 37469 | 级数 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 811 | 37498 | 级数 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 812 | 37532 | 级数 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 813 | 37615 | 级数 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 814 | 37660 | 级数 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 815 | 37755 | 级数 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 816 | 37809 | 级数 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 817 | 37886 | 级数 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 818 | 38058 | 级数 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 819 | 38410 | 往年真题整理 | 2006--2007 第二学期 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 820 | 38441 | 往年真题整理 | 2006--2007 第二学期 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 821 | 38477 | 往年真题整理 | 2006--2007 第二学期 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 822 | 38516 | 往年真题整理 | 2006--2007 第二学期 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 823 | 38553 | 往年真题整理 | 2006--2007 第二学期 A 卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 824 | 38569 | 往年真题整理 | 2006--2007 第二学期 A 卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 825 | 38586 | 往年真题整理 | 2006--2007 第二学期 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 826 | 38606 | 往年真题整理 | 2006--2007 第二学期 A 卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 827 | 38625 | 往年真题整理 | 2006--2007 第二学期 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 828 | 38641 | 往年真题整理 | 2006--2007 第二学期 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 829 | 38667 | 往年真题整理 | 2006--2007 第二学期 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 830 | 38691 | 往年真题整理 | 2006--2007 第二学期 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 831 | 38718 | 往年真题整理 | 2006--2007 第二学期 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 832 | 38742 | 往年真题整理 | 2006--2007 第二学期 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 833 | 38769 | 往年真题整理 | 2006--2007 第二学期 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 834 | 38796 | 往年真题整理 | 2006--2007 第二学期 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 835 | 38824 | 往年真题整理 | 2006--2007 第二学期 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 836 | 38849 | 往年真题整理 | 2006--2007 第二学期 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 837 | 38878 | 往年真题整理 | 2006--2007 第二学期 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 838 | 38910 | 往年真题整理 | 2006--2007 第二学期 B 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 839 | 38930 | 往年真题整理 | 2006--2007 第二学期 B 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 840 | 38950 | 往年真题整理 | 2006--2007 第二学期 B 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 841 | 38975 | 往年真题整理 | 2006--2007 第二学期 B 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 842 | 39000 | 往年真题整理 | 2006--2007 第二学期 B 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 843 | 39023 | 往年真题整理 | 2006--2007 第二学期 B 卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 844 | 39037 | 往年真题整理 | 2006--2007 第二学期 B 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 845 | 39067 | 往年真题整理 | 2006--2007 第二学期 B 卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 846 | 39090 | 往年真题整理 | 2006--2007 第二学期 B 卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 847 | 39114 | 往年真题整理 | 2006--2007 第二学期 B 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 848 | 39143 | 往年真题整理 | 2006--2007 第二学期 B 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 849 | 39174 | 往年真题整理 | 2006--2007 第二学期 B 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 850 | 39207 | 往年真题整理 | 2006--2007 第二学期 B 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 851 | 39227 | 往年真题整理 | 2006--2007 第二学期 B 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 852 | 39289 | 往年真题整理 | 2006--2007 第二学期 B 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 853 | 39315 | 往年真题整理 | 2006--2007 第二学期 B 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 854 | 39333 | 往年真题整理 | 2006--2007 第二学期 B 卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 855 | 39357 | 往年真题整理 | 2006--2007 第二学期 B 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 856 | 39380 | 往年真题整理 | 2006--2007 第二学期 B 卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 857 | 39409 | 往年真题整理 | 2007--2008 第二学期 A 卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 858 | 39424 | 往年真题整理 | 2007--2008 第二学期 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 859 | 39448 | 往年真题整理 | 2007--2008 第二学期 A 卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 860 | 39465 | 往年真题整理 | 2007--2008 第二学期 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险,高风险题解过短 |
| 861 | 39476 | 往年真题整理 | 2007--2008 第二学期 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 862 | 39494 | 往年真题整理 | 2007--2008 第二学期 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 863 | 39513 | 往年真题整理 | 2007--2008 第二学期 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 864 | 39539 | 往年真题整理 | 2007--2008 第二学期 A 卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 865 | 39557 | 往年真题整理 | 2007--2008 第二学期 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,高风险题解过短 |
| 866 | 39573 | 往年真题整理 | 2007--2008 第二学期 A 卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 867 | 39594 | 往年真题整理 | 2007--2008 第二学期 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险,高风险题解过短 |
| 868 | 39604 | 往年真题整理 | 2007--2008 第二学期 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 869 | 39624 | 往年真题整理 | 2007--2008 第二学期 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 870 | 39647 | 往年真题整理 | 2007--2008 第二学期 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 871 | 39672 | 往年真题整理 | 2007--2008 第二学期 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险,短display待判定 |
| 872 | 39700 | 往年真题整理 | 2007--2008 第二学期 A 卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 873 | 39727 | 往年真题整理 | 2007--2008 第二学期 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 874 | 39756 | 往年真题整理 | 2007--2008 第二学期 A 卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 875 | 39775 | 往年真题整理 | 2007--2008 第二学期 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 876 | 39798 | 往年真题整理 | 2009级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 877 | 39810 | 往年真题整理 | 2009级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 878 | 39835 | 往年真题整理 | 2009级工科数学分析下 A卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 879 | 39857 | 往年真题整理 | 2009级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 880 | 39884 | 往年真题整理 | 2009级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险,高风险题解过短 |
| 881 | 39896 | 往年真题整理 | 2009级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 882 | 39913 | 往年真题整理 | 2009级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 883 | 39930 | 往年真题整理 | 2009级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 884 | 39945 | 往年真题整理 | 2009级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 885 | 39973 | 往年真题整理 | 2009级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 886 | 39987 | 往年真题整理 | 2009级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险 |
| 887 | 40000 | 往年真题整理 | 2009级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 888 | 40029 | 往年真题整理 | 2009级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 889 | 40049 | 往年真题整理 | 2009级工科数学分析下 A卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 890 | 40074 | 往年真题整理 | 2009级工科数学分析下 A卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 891 | 40091 | 往年真题整理 | 2009级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 892 | 40122 | 往年真题整理 | 2009级工科数学分析下 A卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 893 | 40143 | 往年真题整理 | 2009级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 894 | 40168 | 往年真题整理 | 2009级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 895 | 40190 | 往年真题整理 | 2009级工科数学分析下 B卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 896 | 40207 | 往年真题整理 | 2009级工科数学分析下 B卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 897 | 40228 | 往年真题整理 | 2009级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 898 | 40261 | 往年真题整理 | 2009级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,高风险题解过短 |
| 899 | 40273 | 往年真题整理 | 2009级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 900 | 40286 | 往年真题整理 | 2009级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 901 | 40315 | 往年真题整理 | 2009级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 902 | 40334 | 往年真题整理 | 2009级工科数学分析下 B卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 903 | 40350 | 往年真题整理 | 2009级工科数学分析下 B卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 904 | 40376 | 往年真题整理 | 2009级工科数学分析下 B卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 905 | 40391 | 往年真题整理 | 2009级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 906 | 40415 | 往年真题整理 | 2009级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 907 | 40432 | 往年真题整理 | 2009级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 908 | 40456 | 往年真题整理 | 2009级工科数学分析下 B卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 909 | 40473 | 往年真题整理 | 2009级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 910 | 40490 | 往年真题整理 | 2009级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 911 | 40515 | 往年真题整理 | 2009级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 912 | 40539 | 往年真题整理 | 2012级工科数学分析下 A卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 913 | 40556 | 往年真题整理 | 2012级工科数学分析下 A卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 914 | 40589 | 往年真题整理 | 2012级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 915 | 40621 | 往年真题整理 | 2012级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 916 | 40646 | 往年真题整理 | 2012级工科数学分析下 A卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 917 | 40663 | 往年真题整理 | 2012级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 918 | 40687 | 往年真题整理 | 2012级工科数学分析下 A卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 919 | 40708 | 往年真题整理 | 2012级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 920 | 40728 | 往年真题整理 | 2012级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 921 | 40754 | 往年真题整理 | 2012级工科数学分析下 A卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 922 | 40772 | 往年真题整理 | 2012级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 923 | 40802 | 往年真题整理 | 2012级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 924 | 40838 | 往年真题整理 | 2012级工科数学分析下 A卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 925 | 40856 | 往年真题整理 | 2012级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险 |
| 926 | 40872 | 往年真题整理 | 2012级工科数学分析下 A卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 927 | 40892 | 往年真题整理 | 2012级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 928 | 40919 | 往年真题整理 | 2012级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 929 | 40942 | 往年真题整理 | 2012级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险,高风险题解过短 |
| 930 | 40955 | 往年真题整理 | 2012级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 931 | 40971 | 往年真题整理 | 2012级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 932 | 40987 | 往年真题整理 | 2012级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险,高风险题解过短 |
| 933 | 41004 | 往年真题整理 | 2012级工科数学分析下 B卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 934 | 41022 | 往年真题整理 | 2012级工科数学分析下 B卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 935 | 41038 | 往年真题整理 | 2012级工科数学分析下 B卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 936 | 41053 | 往年真题整理 | 2012级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险,短display待判定 |
| 937 | 41074 | 往年真题整理 | 2012级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 938 | 41088 | 往年真题整理 | 2012级工科数学分析下 B卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 939 | 41106 | 往年真题整理 | 2012级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险 |
| 940 | 41124 | 往年真题整理 | 2012级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 941 | 41146 | 往年真题整理 | 2012级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 942 | 41169 | 往年真题整理 | 2012级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,高风险题解过短 |
| 943 | 41182 | 往年真题整理 | 2012级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 944 | 41218 | 往年真题整理 | 2012级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 945 | 41245 | 往年真题整理 | 2012级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 946 | 41271 | 往年真题整理 | 2013级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 947 | 41285 | 往年真题整理 | 2013级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 948 | 41300 | 往年真题整理 | 2013级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 949 | 41325 | 往年真题整理 | 2013级工科数学分析下 A卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 950 | 41347 | 往年真题整理 | 2013级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,高风险题解过短 |
| 951 | 41361 | 往年真题整理 | 2013级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 952 | 41373 | 往年真题整理 | 2013级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 953 | 41385 | 往年真题整理 | 2013级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 954 | 41395 | 往年真题整理 | 2013级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 955 | 41411 | 往年真题整理 | 2013级工科数学分析下 A卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 956 | 41427 | 往年真题整理 | 2013级工科数学分析下 A卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 957 | 41446 | 往年真题整理 | 2013级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 958 | 41472 | 往年真题整理 | 2013级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 959 | 41490 | 往年真题整理 | 2013级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 960 | 41529 | 往年真题整理 | 2013级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 961 | 41545 | 往年真题整理 | 2013级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 962 | 41568 | 往年真题整理 | 2013级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 963 | 41596 | 往年真题整理 | 2013级工科数学分析下 B卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 964 | 41611 | 往年真题整理 | 2013级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险,高风险题解过短 |
| 965 | 41625 | 往年真题整理 | 2013级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 966 | 41651 | 往年真题整理 | 2013级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险,高风险题解过短 |
| 967 | 41672 | 往年真题整理 | 2013级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 968 | 41687 | 往年真题整理 | 2013级工科数学分析下 B卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 969 | 41700 | 往年真题整理 | 2013级工科数学分析下 B卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 970 | 41718 | 往年真题整理 | 2013级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 971 | 41732 | 往年真题整理 | 2013级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 972 | 41749 | 往年真题整理 | 2013级工科数学分析下 B卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 973 | 41769 | 往年真题整理 | 2013级工科数学分析下 B卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 974 | 41798 | 往年真题整理 | 2013级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 975 | 41836 | 往年真题整理 | 2013级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险 |
| 976 | 41853 | 往年真题整理 | 2013级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 977 | 41895 | 往年真题整理 | 2013级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 978 | 41925 | 往年真题整理 | 2013级工科数学分析下 B卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 979 | 41942 | 往年真题整理 | 2013级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 980 | 41963 | 往年真题整理 | 2014级工科数学分析下 A卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 981 | 41976 | 往年真题整理 | 2014级工科数学分析下 A卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 982 | 41994 | 往年真题整理 | 2014级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 983 | 42014 | 往年真题整理 | 2014级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 984 | 42026 | 往年真题整理 | 2014级工科数学分析下 A卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 985 | 42043 | 往年真题整理 | 2014级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 986 | 42061 | 往年真题整理 | 2014级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 987 | 42088 | 往年真题整理 | 2014级工科数学分析下 A卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 988 | 42104 | 往年真题整理 | 2014级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 989 | 42135 | 往年真题整理 | 2014级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 990 | 42159 | 往年真题整理 | 2014级工科数学分析下 A卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 991 | 42179 | 往年真题整理 | 2014级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 992 | 42195 | 往年真题整理 | 2014级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险 |
| 993 | 42212 | 往年真题整理 | 2014级工科数学分析下 B卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 994 | 42226 | 往年真题整理 | 2014级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 995 | 42243 | 往年真题整理 | 2014级工科数学分析下 B卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 996 | 42263 | 往年真题整理 | 2014级工科数学分析下 B卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 997 | 42278 | 往年真题整理 | 2014级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 998 | 42294 | 往年真题整理 | 2014级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 999 | 42314 | 往年真题整理 | 2014级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 1000 | 42346 | 往年真题整理 | 2014级工科数学分析下 B卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1001 | 42366 | 往年真题整理 | 2014级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险,短display待判定 |
| 1002 | 42404 | 往年真题整理 | 2014级工科数学分析下 B卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1003 | 42417 | 往年真题整理 | 2014级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险 |
| 1004 | 42435 | 往年真题整理 | 2014级工科数学分析下 B卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1005 | 42450 | 往年真题整理 | 2014级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1006 | 42480 | 往年真题整理 | 2015级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1007 | 42493 | 往年真题整理 | 2015级工科数学分析下 A卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1008 | 42514 | 往年真题整理 | 2015级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 1009 | 42535 | 往年真题整理 | 2015级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险,高风险题解过短 |
| 1010 | 42552 | 往年真题整理 | 2015级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 1011 | 42567 | 往年真题整理 | 2015级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1012 | 42582 | 往年真题整理 | 2015级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1013 | 42602 | 往年真题整理 | 2015级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1014 | 42621 | 往年真题整理 | 2015级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1015 | 42634 | 往年真题整理 | 2015级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 1016 | 42659 | 往年真题整理 | 2015级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 1017 | 42671 | 往年真题整理 | 2015级工科数学分析下 A卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1018 | 42689 | 往年真题整理 | 2015级工科数学分析下 A卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1019 | 42709 | 往年真题整理 | 2015级工科数学分析下 A卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1020 | 42724 | 往年真题整理 | 2015级工科数学分析下 A卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1021 | 42744 | 往年真题整理 | 2015级工科数学分析下 B卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1022 | 42760 | 往年真题整理 | 2015级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1023 | 42779 | 往年真题整理 | 2015级工科数学分析下 B卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1024 | 42796 | 往年真题整理 | 2015级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,高风险题解过短 |
| 1025 | 42809 | 往年真题整理 | 2015级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 1026 | 42822 | 往年真题整理 | 2015级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 1027 | 42848 | 往年真题整理 | 2015级工科数学分析下 B卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1028 | 42866 | 往年真题整理 | 2015级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 1029 | 42891 | 往年真题整理 | 2015级工科数学分析下 B卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1030 | 42909 | 往年真题整理 | 2015级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 1031 | 42936 | 往年真题整理 | 2015级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 1032 | 42953 | 往年真题整理 | 2015级工科数学分析下 B卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1033 | 42973 | 往年真题整理 | 2015级工科数学分析下 B卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1034 | 42990 | 往年真题整理 | 2015级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 1035 | 43012 | 往年真题整理 | 2015级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1036 | 43039 | 往年真题整理 | 2016级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 1037 | 43050 | 往年真题整理 | 2016级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1038 | 43065 | 往年真题整理 | 2016级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 1039 | 43089 | 往年真题整理 | 2016级工科数学分析下 A卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1040 | 43112 | 往年真题整理 | 2016级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1041 | 43139 | 往年真题整理 | 2016级工科数学分析下 A卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1042 | 43163 | 往年真题整理 | 2016级工科数学分析下 A卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1043 | 43182 | 往年真题整理 | 2016级工科数学分析下 A卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1044 | 43200 | 往年真题整理 | 2016级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 1045 | 43215 | 往年真题整理 | 2016级工科数学分析下 A卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1046 | 43233 | 往年真题整理 | 2016级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险,高风险题解过短 |
| 1047 | 43249 | 往年真题整理 | 2016级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险 |
| 1048 | 43272 | 往年真题整理 | 2016级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 1049 | 43299 | 往年真题整理 | 2016级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 1050 | 43322 | 往年真题整理 | 2016级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险,短display待判定 |
| 1051 | 43340 | 往年真题整理 | 2016级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 1052 | 43374 | 往年真题整理 | 2016级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 1053 | 43403 | 往年真题整理 | 2016级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 1054 | 43428 | 往年真题整理 | 2016级工科数学分析下 A卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1055 | 43443 | 往年真题整理 | 2016级工科数学分析下 A卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1056 | 43472 | 往年真题整理 | 2016级工科数学分析下 A卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1057 | 43498 | 往年真题整理 | 2016级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 1058 | 43522 | 往年真题整理 | 2016级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 1059 | 43534 | 往年真题整理 | 2016级工科数学分析下 B卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1060 | 43555 | 往年真题整理 | 2016级工科数学分析下 B卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1061 | 43568 | 往年真题整理 | 2016级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1062 | 43589 | 往年真题整理 | 2016级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1063 | 43606 | 往年真题整理 | 2016级工科数学分析下 B卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1064 | 43622 | 往年真题整理 | 2016级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 1065 | 43655 | 往年真题整理 | 2016级工科数学分析下 B卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1066 | 43672 | 往年真题整理 | 2016级工科数学分析下 B卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1067 | 43692 | 往年真题整理 | 2016级工科数学分析下 B卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1068 | 43705 | 往年真题整理 | 2016级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 1069 | 43726 | 往年真题整理 | 2016级工科数学分析下 B卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1070 | 43740 | 往年真题整理 | 2016级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1071 | 43758 | 往年真题整理 | 2016级工科数学分析下 B卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1072 | 43774 | 往年真题整理 | 2016级工科数学分析下 B卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1073 | 43790 | 往年真题整理 | 2016级工科数学分析下 B卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1074 | 43809 | 往年真题整理 | 2016级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1075 | 43834 | 往年真题整理 | 2016级工科数学分析下 B卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1076 | 43854 | 往年真题整理 | 2016级工科数学分析下 B卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1077 | 43877 | 往年真题整理 | 2016级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1078 | 43900 | 往年真题整理 | 2017级工科数学分析下 A卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1079 | 43915 | 往年真题整理 | 2017级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1080 | 43928 | 往年真题整理 | 2017级工科数学分析下 A卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1081 | 43949 | 往年真题整理 | 2017级工科数学分析下 A卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1082 | 43970 | 往年真题整理 | 2017级工科数学分析下 A卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1083 | 43993 | 往年真题整理 | 2017级工科数学分析下 A卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1084 | 44018 | 往年真题整理 | 2017级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1085 | 44040 | 往年真题整理 | 2017级工科数学分析下 A卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1086 | 44062 | 往年真题整理 | 2017级工科数学分析下 A卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1087 | 44083 | 往年真题整理 | 2017级工科数学分析下 A卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1088 | 44103 | 往年真题整理 | 2017级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险,短display待判定 |
| 1089 | 44130 | 往年真题整理 | 2017级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1090 | 44162 | 往年真题整理 | 2017级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 1091 | 44197 | 往年真题整理 | 2017级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 1092 | 44222 | 往年真题整理 | 2017级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1093 | 44242 | 往年真题整理 | 2017级工科数学分析下 A卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1094 | 44262 | 往年真题整理 | 2017级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险,短display待判定 |
| 1095 | 44299 | 往年真题整理 | 2017级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 1096 | 44337 | 往年真题整理 | 2017级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1097 | 44351 | 往年真题整理 | 2017级工科数学分析下 B卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1098 | 44368 | 往年真题整理 | 2017级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 1099 | 44380 | 往年真题整理 | 2017级工科数学分析下 B卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1100 | 44394 | 往年真题整理 | 2017级工科数学分析下 B卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1101 | 44414 | 往年真题整理 | 2017级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 1102 | 44430 | 往年真题整理 | 2017级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 1103 | 44444 | 往年真题整理 | 2017级工科数学分析下 B卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1104 | 44460 | 往年真题整理 | 2017级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险,高风险题解过短 |
| 1105 | 44475 | 往年真题整理 | 2017级工科数学分析下 B卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1106 | 44491 | 往年真题整理 | 2017级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 1107 | 44516 | 往年真题整理 | 2017级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1108 | 44543 | 往年真题整理 | 2017级工科数学分析下 B卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1109 | 44578 | 往年真题整理 | 2017级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1110 | 44618 | 往年真题整理 | 2017级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1111 | 44650 | 往年真题整理 | 2017级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 1112 | 44669 | 往年真题整理 | 2017级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1113 | 44692 | 往年真题整理 | 2017级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1114 | 44726 | 往年真题整理 | 2018级工科数学分析下 A卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1115 | 44739 | 往年真题整理 | 2018级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险 |
| 1116 | 44755 | 往年真题整理 | 2018级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 1117 | 44766 | 往年真题整理 | 2018级工科数学分析下 A卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1118 | 44782 | 往年真题整理 | 2018级工科数学分析下 A卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1119 | 44799 | 往年真题整理 | 2018级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 1120 | 44819 | 往年真题整理 | 2018级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 1121 | 44843 | 往年真题整理 | 2018级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 1122 | 44863 | 往年真题整理 | 2018级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1123 | 44886 | 往年真题整理 | 2018级工科数学分析下 A卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1124 | 44907 | 往年真题整理 | 2018级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 1125 | 44946 | 往年真题整理 | 2018级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1126 | 44966 | 往年真题整理 | 2018级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 1127 | 44984 | 往年真题整理 | 2018级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 1128 | 45011 | 往年真题整理 | 2018级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 1129 | 45039 | 往年真题整理 | 2018级工科数学分析下 B卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1130 | 45062 | 往年真题整理 | 2018级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 1131 | 45077 | 往年真题整理 | 2018级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,高风险题解过短 |
| 1132 | 45089 | 往年真题整理 | 2018级工科数学分析下 B卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1133 | 45112 | 往年真题整理 | 2018级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1134 | 45130 | 往年真题整理 | 2018级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 1135 | 45145 | 往年真题整理 | 2018级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 1136 | 45170 | 往年真题整理 | 2018级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 1137 | 45194 | 往年真题整理 | 2018级工科数学分析下 B卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1138 | 45222 | 往年真题整理 | 2018级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险 |
| 1139 | 45243 | 往年真题整理 | 2018级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险,短display待判定 |
| 1140 | 45266 | 往年真题整理 | 2018级工科数学分析下 B卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1141 | 45286 | 往年真题整理 | 2018级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1142 | 45308 | 往年真题整理 | 2018级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 1143 | 45343 | 往年真题整理 | 2019级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 1144 | 45355 | 往年真题整理 | 2019级工科数学分析下 A卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1145 | 45368 | 往年真题整理 | 2019级工科数学分析下 A卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1146 | 45385 | 往年真题整理 | 2019级工科数学分析下 A卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1147 | 45400 | 往年真题整理 | 2019级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1148 | 45419 | 往年真题整理 | 2019级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1149 | 45435 | 往年真题整理 | 2019级工科数学分析下 A卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1150 | 45480 | 往年真题整理 | 2019级工科数学分析下 A卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1151 | 45514 | 往年真题整理 | 2019级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 1152 | 45538 | 往年真题整理 | 2019级工科数学分析下 A卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1153 | 45571 | 往年真题整理 | 2019级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1154 | 45595 | 往年真题整理 | 2019级工科数学分析下 A卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1155 | 45614 | 往年真题整理 | 2019级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 1156 | 45648 | 往年真题整理 | 2019级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1157 | 45670 | 往年真题整理 | 2019级工科数学分析下 A卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1158 | 45697 | 往年真题整理 | 2019级工科数学分析下 B卷补考 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1159 | 45710 | 往年真题整理 | 2019级工科数学分析下 B卷补考 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1160 | 45725 | 往年真题整理 | 2019级工科数学分析下 B卷补考 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1161 | 45738 | 往年真题整理 | 2019级工科数学分析下 B卷补考 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1162 | 45758 | 往年真题整理 | 2019级工科数学分析下 B卷补考 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 1163 | 45775 | 往年真题整理 | 2019级工科数学分析下 B卷补考 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1164 | 45805 | 往年真题整理 | 2019级工科数学分析下 B卷补考 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1165 | 45825 | 往年真题整理 | 2019级工科数学分析下 B卷补考 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1166 | 45845 | 往年真题整理 | 2019级工科数学分析下 B卷补考 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 1167 | 45867 | 往年真题整理 | 2019级工科数学分析下 B卷补考 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 1168 | 45914 | 往年真题整理 | 2019级工科数学分析下 B卷补考 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1169 | 45939 | 往年真题整理 | 2019级工科数学分析下 B卷补考 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1170 | 45961 | 往年真题整理 | 2019级工科数学分析下 B卷补考 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1171 | 45978 | 往年真题整理 | 2019级工科数学分析下 B卷补考 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1172 | 45994 | 往年真题整理 | 2019级工科数学分析下 B卷补考 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1173 | 46022 | 往年真题整理 | 2020级工科数学分析（二）期末考试 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1174 | 46053 | 往年真题整理 | 2020级工科数学分析（二）期末考试 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1175 | 46076 | 往年真题整理 | 2020级工科数学分析（二）期末考试 A 卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1176 | 46100 | 往年真题整理 | 2020级工科数学分析（二）期末考试 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1177 | 46114 | 往年真题整理 | 2020级工科数学分析（二）期末考试 A 卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1178 | 46144 | 往年真题整理 | 2020级工科数学分析（二）期末考试 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 1179 | 46158 | 往年真题整理 | 2020级工科数学分析（二）期末考试 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 1180 | 46186 | 往年真题整理 | 2020级工科数学分析（二）期末考试 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险,高风险题解过短 |
| 1181 | 46195 | 往年真题整理 | 2020级工科数学分析（二）期末考试 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险,高风险题解过短 |
| 1182 | 46208 | 往年真题整理 | 2020级工科数学分析（二）期末考试 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 1183 | 46232 | 往年真题整理 | 2020级工科数学分析（二）期末考试 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1184 | 46248 | 往年真题整理 | 2020级工科数学分析（二）期末考试 A 卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1185 | 46266 | 往年真题整理 | 2020级工科数学分析（二）期末考试 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险 |
| 1186 | 46293 | 往年真题整理 | 2020级工科数学分析（二）期末考试 B 卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1187 | 46318 | 往年真题整理 | 2020级工科数学分析（二）期末考试 B 卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1188 | 46338 | 往年真题整理 | 2020级工科数学分析（二）期末考试 B 卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1189 | 46359 | 往年真题整理 | 2020级工科数学分析（二）期末考试 B 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 1190 | 46377 | 往年真题整理 | 2020级工科数学分析（二）期末考试 B 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 1191 | 46411 | 往年真题整理 | 2020级工科数学分析（二）期末考试 B 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 1192 | 46424 | 往年真题整理 | 2020级工科数学分析（二）期末考试 B 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1193 | 46452 | 往年真题整理 | 2020级工科数学分析（二）期末考试 B 卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1194 | 46469 | 往年真题整理 | 2020级工科数学分析（二）期末考试 B 卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1195 | 46485 | 往年真题整理 | 2020级工科数学分析（二）期末考试 B 卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1196 | 46519 | 往年真题整理 | 2020级工科数学分析（二）期末考试 B 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 1197 | 46543 | 往年真题整理 | 2020级工科数学分析（二）期末考试 B 卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1198 | 46561 | 往年真题整理 | 2020级工科数学分析（二）期末考试 B 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1199 | 46591 | 往年真题整理 | 2021级工科数学分析（二）期末考试 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 1200 | 46601 | 往年真题整理 | 2021级工科数学分析（二）期末考试 A 卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1201 | 46615 | 往年真题整理 | 2021级工科数学分析（二）期末考试 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 1202 | 46627 | 往年真题整理 | 2021级工科数学分析（二）期末考试 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 1203 | 46639 | 往年真题整理 | 2021级工科数学分析（二）期末考试 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 1204 | 46654 | 往年真题整理 | 2021级工科数学分析（二）期末考试 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 1205 | 46681 | 往年真题整理 | 2021级工科数学分析（二）期末考试 A 卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1206 | 46697 | 往年真题整理 | 2021级工科数学分析（二）期末考试 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 1207 | 46710 | 往年真题整理 | 2021级工科数学分析（二）期末考试 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险 |
| 1208 | 46731 | 往年真题整理 | 2021级工科数学分析（二）期末考试 A 卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1209 | 46745 | 往年真题整理 | 2021级工科数学分析（二）期末考试 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1210 | 46758 | 往年真题整理 | 2021级工科数学分析（二）期末考试 A 卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1211 | 46774 | 往年真题整理 | 2021级工科数学分析（二）期末考试 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1212 | 46795 | 往年真题整理 | 2021级工科数学分析（二）期末考试 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 1213 | 46829 | 往年真题整理 | 2021级工科数学分析（二）期末考试 B 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 1214 | 46840 | 往年真题整理 | 2021级工科数学分析（二）期末考试 B 卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1215 | 46860 | 往年真题整理 | 2021级工科数学分析（二）期末考试 B 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 1216 | 46870 | 往年真题整理 | 2021级工科数学分析（二）期末考试 B 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 1217 | 46882 | 往年真题整理 | 2021级工科数学分析（二）期末考试 B 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 1218 | 46896 | 往年真题整理 | 2021级工科数学分析（二）期末考试 B 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 1219 | 46915 | 往年真题整理 | 2021级工科数学分析（二）期末考试 B 卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1220 | 46930 | 往年真题整理 | 2021级工科数学分析（二）期末考试 B 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险,短display待判定 |
| 1221 | 46976 | 往年真题整理 | 2021级工科数学分析（二）期末考试 B 卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1222 | 46994 | 往年真题整理 | 2021级工科数学分析（二）期末考试 B 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1223 | 47012 | 往年真题整理 | 2021级工科数学分析（二）期末考试 B 卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1224 | 47038 | 往年真题整理 | 2021级工科数学分析（二）期末考试 B 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险,高风险题解过短 |
| 1225 | 47051 | 往年真题整理 | 2021级工科数学分析（二）期末考试 B 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1226 | 47071 | 往年真题整理 | 2021级工科数学分析（二）期末考试 B 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1227 | 47092 | 往年真题整理 | 2022级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 1228 | 47102 | 往年真题整理 | 2022级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 1229 | 47113 | 往年真题整理 | 2022级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 1230 | 47134 | 往年真题整理 | 2022级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1231 | 47154 | 往年真题整理 | 2022级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 1232 | 47175 | 往年真题整理 | 2022级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 1233 | 47192 | 往年真题整理 | 2022级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 1234 | 47210 | 往年真题整理 | 2022级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 1235 | 47229 | 往年真题整理 | 2022级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 1236 | 47247 | 往年真题整理 | 2022级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 1237 | 47265 | 往年真题整理 | 2022级工科数学分析下 A卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1238 | 47284 | 往年真题整理 | 2022级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险,短display待判定 |
| 1239 | 47298 | 往年真题整理 | 2022级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 1240 | 47316 | 往年真题整理 | 2022级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险,短display待判定 |
| 1241 | 47349 | 往年真题整理 | 2022级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 1242 | 47365 | 往年真题整理 | 2022级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险,高风险题解过短 |
| 1243 | 47379 | 往年真题整理 | 2022级工科数学分析下 A卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1244 | 47409 | 往年真题整理 | 2022级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1245 | 47431 | 往年真题整理 | 2022级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,高风险题解过短 |
| 1246 | 47442 | 往年真题整理 | 2022级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 1247 | 47456 | 往年真题整理 | 2022级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1248 | 47470 | 往年真题整理 | 2022级工科数学分析下 B卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1249 | 47492 | 往年真题整理 | 2022级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险,高风险题解过短 |
| 1250 | 47509 | 往年真题整理 | 2022级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 1251 | 47525 | 往年真题整理 | 2022级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 1252 | 47540 | 往年真题整理 | 2022级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 1253 | 47560 | 往年真题整理 | 2022级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,高风险题解过短 |
| 1254 | 47576 | 往年真题整理 | 2022级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险,高风险题解过短 |
| 1255 | 47593 | 往年真题整理 | 2022级工科数学分析下 B卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1256 | 47625 | 往年真题整理 | 2022级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 1257 | 47652 | 往年真题整理 | 2022级工科数学分析下 B卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1258 | 47685 | 往年真题整理 | 2022级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 1259 | 47717 | 往年真题整理 | 2022级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 1260 | 47735 | 往年真题整理 | 2022级工科数学分析下 B卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1261 | 47755 | 往年真题整理 | 2022级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1262 | 47774 | 往年真题整理 | 2022级工科数学分析下 B卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1263 | 47797 | 往年真题整理 | 2023级工科数学分析（二）期末考试 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险,高风险题解过短 |
| 1264 | 47807 | 往年真题整理 | 2023级工科数学分析（二）期末考试 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 1265 | 47819 | 往年真题整理 | 2023级工科数学分析（二）期末考试 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 1266 | 47838 | 往年真题整理 | 2023级工科数学分析（二）期末考试 A 卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1267 | 47859 | 往年真题整理 | 2023级工科数学分析（二）期末考试 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险,高风险题解过短 |
| 1268 | 47873 | 往年真题整理 | 2023级工科数学分析（二）期末考试 A 卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1269 | 47886 | 往年真题整理 | 2023级工科数学分析（二）期末考试 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 1270 | 47900 | 往年真题整理 | 2023级工科数学分析（二）期末考试 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1271 | 47914 | 往年真题整理 | 2023级工科数学分析（二）期末考试 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 1272 | 47935 | 往年真题整理 | 2023级工科数学分析（二）期末考试 A 卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1273 | 47957 | 往年真题整理 | 2023级工科数学分析（二）期末考试 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 1274 | 47974 | 往年真题整理 | 2023级工科数学分析（二）期末考试 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1275 | 47997 | 往年真题整理 | 2023级工科数学分析（二）期末考试 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 1276 | 48018 | 往年真题整理 | 2023级工科数学分析（二）期末考试 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1277 | 48040 | 往年真题整理 | 2023级工科数学分析（二）期末考试 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险,短display待判定 |
| 1278 | 48062 | 往年真题整理 | 2023级工科数学分析（二）期末考试 B 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 1279 | 48072 | 往年真题整理 | 2023级工科数学分析（二）期末考试 B 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 1280 | 48084 | 往年真题整理 | 2023级工科数学分析（二）期末考试 B 卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1281 | 48098 | 往年真题整理 | 2023级工科数学分析（二）期末考试 B 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 1282 | 48137 | 往年真题整理 | 2023级工科数学分析（二）期末考试 B 卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1283 | 48154 | 往年真题整理 | 2023级工科数学分析（二）期末考试 B 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 1284 | 48165 | 往年真题整理 | 2023级工科数学分析（二）期末考试 B 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 1285 | 48184 | 往年真题整理 | 2023级工科数学分析（二）期末考试 B 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1286 | 48209 | 往年真题整理 | 2023级工科数学分析（二）期末考试 B 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险,短display待判定 |
| 1287 | 48232 | 往年真题整理 | 2023级工科数学分析（二）期末考试 B 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险 |
| 1288 | 48256 | 往年真题整理 | 2023级工科数学分析（二）期末考试 B 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险,短display待判定 |
| 1289 | 48284 | 往年真题整理 | 2023级工科数学分析（二）期末考试 B 卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1290 | 48302 | 往年真题整理 | 2023级工科数学分析（二）期末考试 B 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险 |
| 1291 | 48344 | 往年真题整理 | 2023级工科数学分析（二）期末考试 B 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1292 | 48366 | 往年真题整理 | 2023级工科数学分析（二）期末考试 B 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险 |
| 1293 | 48386 | 往年真题整理 | 2024级工科数学分析（二）期末考试 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 1294 | 48396 | 往年真题整理 | 2024级工科数学分析（二）期末考试 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 1295 | 48409 | 往年真题整理 | 2024级工科数学分析（二）期末考试 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 1296 | 48427 | 往年真题整理 | 2024级工科数学分析（二）期末考试 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 1297 | 48445 | 往年真题整理 | 2024级工科数学分析（二）期末考试 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 1298 | 48462 | 往年真题整理 | 2024级工科数学分析（二）期末考试 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险,高风险题解过短 |
| 1299 | 48474 | 往年真题整理 | 2024级工科数学分析（二）期末考试 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险,短display待判定 |
| 1300 | 48493 | 往年真题整理 | 2024级工科数学分析（二）期末考试 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1301 | 48514 | 往年真题整理 | 2024级工科数学分析（二）期末考试 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 1302 | 48544 | 往年真题整理 | 2024级工科数学分析（二）期末考试 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险,高风险题解过短 |
| 1303 | 48562 | 往年真题整理 | 2024级工科数学分析（二）期末考试 A 卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1304 | 48580 | 往年真题整理 | 2024级工科数学分析（二）期末考试 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险,高风险题解过短 |
| 1305 | 48596 | 往年真题整理 | 2024级工科数学分析（二）期末考试 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 1306 | 48643 | 往年真题整理 | 2024级工科数学分析（二）期末考试 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,高风险题解过短 |
| 1307 | 48659 | 往年真题整理 | 2024级工科数学分析（二）期末考试 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 1308 | 48676 | 往年真题整理 | 2024级工科数学分析（二）期末考试 B 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 1309 | 48687 | 往年真题整理 | 2024级工科数学分析（二）期末考试 B 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 1310 | 48702 | 往年真题整理 | 2024级工科数学分析（二）期末考试 B 卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1311 | 48714 | 往年真题整理 | 2024级工科数学分析（二）期末考试 B 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 1312 | 48734 | 往年真题整理 | 2024级工科数学分析（二）期末考试 B 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 1313 | 48751 | 往年真题整理 | 2024级工科数学分析（二）期末考试 B 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 1314 | 48764 | 往年真题整理 | 2024级工科数学分析（二）期末考试 B 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 1315 | 48789 | 往年真题整理 | 2024级工科数学分析（二）期末考试 B 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1316 | 48821 | 往年真题整理 | 2024级工科数学分析（二）期末考试 B 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 1317 | 48850 | 往年真题整理 | 2024级工科数学分析（二）期末考试 B 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险 |
| 1318 | 48867 | 往年真题整理 | 2024级工科数学分析（二）期末考试 B 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 1319 | 48889 | 往年真题整理 | 2024级工科数学分析（二）期末考试 B 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 1320 | 48925 | 往年真题整理 | 2024级工科数学分析（二）期末考试 B 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 1321 | 48950 | 往年真题整理 | 2024级工科数学分析（二）期末考试 B 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险,高风险题解过短 |
| 1322 | 48973 | 往年真题整理 | 2024级工科数学分析（二）期末考试 B 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
