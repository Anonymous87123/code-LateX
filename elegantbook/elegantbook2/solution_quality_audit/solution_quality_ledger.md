# 全书 solution 质量整改台账
## 说明
- 本台账由当前 `elegantbook2.tex` 自动全域遍历生成，覆盖每一个 `solution` 环境。
- `AUTO_FLAGGED_NEEDS_MANUAL` 不是最终定罪，只是优先人工复核队列；后续需要逐题审校并交 GPT-5.5 子代理复核。
- 硬性整改口径：补齐跳步、统一前文方法、修正数学错误、长行内公式回退为规范行间公式，禁止过度压缩。

## 汇总
- `total_solutions`: 1322
- `auto_flagged`: 1044
- `long_inline_flagged`: 319
- `jump_keyword_flagged`: 577
- `short_display_flagged`: 573
- `by_chapter`: 不定积分=155, 微分方程=160, 多元函数微分学=240, 重积分=88, 曲线积分与曲面积分=120, 级数=55, 往年真题整理=504
- `by_risk_tag`: 微分方程=201, 极值/拉格朗日=114, 隐函数/偏导=289, 重积分/换元=215, 曲面积分/通量=170, 级数/幂级数=191, 曲线积分=115, Green/Gauss/Stokes=77, Fourier=41
- `by_defect_flag`: 跳步关键词=577, 短display待判定=573, 长行内公式/排版风险=319, 高风险题解过短=125

## 自动标记缺陷队列
| 全局序号 | 行号 | 章节 | 小节 | 题目预览 | 标签 | 标记 | 证据 | 建议 |
|---:|---:|---|---|---|---|---|---|---|
| 1 | 1413 | 不定积分 | 习题 | 混合分解 $\frac{x^3+2}{(x-1)^2(x^2+1)}$ |  | 跳步关键词,短display待判定 | 可得; 1415:F(x)=\frac{A}{x-1}+\frac{B}{(x-1)^2}+\frac{Cx+D}{x^2+1}. \| 1419:G(x)=(x-1)^2F(x)=\frac{x^3+2}{x^2+1}. \| 1423:B=G(1)=\frac{1^3+2}{1^2+1}=\frac32. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 2 | 1468 | 不定积分 | 习题 | 分解$\frac{x+2}{(x^2+2x+2)(x^2+1)}$ |  | 跳步关键词,短display待判定 | 可得; 1493:\frac{x+2}{(x^2+2x+2)(x^2+1)} =\frac{3x+2}{5(x^2+2x+2)} +\frac{4-3x}{5(x^2+1)}. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 4 | 1517 | 不定积分 | 习题 | 分解$\frac{1}{(x-1)^2(x^2+1)^2}$ |  | 短display待判定 | 1529:\frac{1}{A^2B^2} =\frac{B-3(x+1)A}{8A^2} +\frac{3(x+1)^2B-(x+1)^3A}{8B^2}. \| 1546:\frac{1}{(x-1)^2(x^2+1)^2} =-\frac{1}{2(x-1)} +\frac{1}{4(x-1)^2} +\frac{2x+1}{4(x^2+1)} +\fr | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 5 | 1558 | 不定积分 | 习题 | 分解 $\frac{2x^2 + 3}{(x-1)(x^2+x+1)}$ |  | 跳步关键词,短display待判定 | 于是; 1582:F(x)=\frac{5}{3(x-1)} +\frac{x-4}{3(x^2+x+1)}. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 6 | 1591 | 不定积分 | 习题 | 分解 $\frac{x^5}{(x^2+1)^3}$ |  | 短display待判定 | 1593:x^5=x(x^2)^2=x(t-1)^2=x(t^2-2t+1). | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 7 | 1610 | 不定积分 | 习题 | 分解 $\frac{x}{(x-1)^2(x+1)^2}$ |  | 跳步关键词,短display待判定 | 于是; 1632:F(x)=\frac{1}{4(x-1)^2} -\frac{1}{4(x+1)^2}. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 8 | 1641 | 不定积分 | 习题 | 分解 $\frac{x^2}{(x^2+1)^2(x^2+x+1)}$ |  | 跳步关键词,短display待判定 | 于是; 1651:\frac{1}{AB} =\frac{(x+1)B-xA}{AB} =\frac{x+1}{A}-\frac{x}{B}. \| 1657:\frac{1}{AB^2}=\frac{x+1}{AB}-\frac{x}{B^2}. \| 1668:\frac{1}{AB^2} =\frac{(x+1)^2}{A} -\frac{x^2+x}{B | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 9 | 1696 | 不定积分 | 习题 | 分解 $F(x) = \frac{1}{x(x-1)(x^2+1)}$ |  | 跳步关键词,短display待判定 | 可得,于是; 1726:\frac{P(x)}{BC} =\frac{1}{2(x-1)} +\frac{x-1}{2(x^2+1)}. \| 1732:F(x) =-\frac1x +\frac{1}{2(x-1)} +\frac{x-1}{2(x^2+1)}. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 10 | 1743 | 不定积分 | 习题 | 分解 $\frac{x^3}{(x-1)(x+1)(x^2+x+1)}$ |  | 短display待判定 | 1745:F(x)=\frac{A}{x-1} +\frac{B}{x+1} +\frac{Cx+D}{x^2+x+1}. \| 1751:A=\frac{1^3}{(1+1)(1+1+1)}=\frac16, \qquad B=\frac{(-1)^3}{(-1-1)(1-1+1)}=\frac12. \| 1771:3x^3-(2x-1)(x^2+x+1)  | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 13 | 1815 | 不定积分 | 习题 | 含有 $ax+b$ 的积分 - 3 |  | 跳步关键词 | 于是 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 14 | 1829 | 不定积分 | 习题 | 含有 $ax+b$ 的积分 - 4 |  | 跳步关键词 | 于是 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 15 | 1843 | 不定积分 | 习题 | 含有 $ax+b$ 的积分 - 5 |  | 短display待判定 | 1845:\frac{1}{x(ax+b)} =\frac{1}{b}\left(\frac{1}{x}-\frac{a}{ax+b}\right). \| 1857:\int \frac{\mathrm{d}x}{a x^2} =-\frac{1}{a x}+C. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 16 | 1866 | 不定积分 | 习题 | 含有 $ax+b$ 的积分 - 6 |  | 短display待判定 | 1868:\frac{1}{x^2(ax+b)} =\frac{1}{b}\left(\frac{1}{x^2}-\frac{a}{x(ax+b)}\right), \| 1880:\int \frac{\mathrm{d}x}{a x^3} =-\frac{1}{2a x^2}+C. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 17 | 1889 | 不定积分 | 习题 | 含有 $ax+b$ 的积分 - 7 |  | 跳步关键词 | 于是 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 18 | 1903 | 不定积分 | 习题 | 含有 $ax+b$ 的积分 - 8 |  | 跳步关键词 | 于是 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 19 | 1917 | 不定积分 | 习题 | 含有 $ax+b$ 的积分 - 9 |  | 跳步关键词,短display待判定 | 于是; 1919:\frac{1}{x(ax+b)^2} =\frac{1}{b}\left(\frac{1}{x(ax+b)}-\frac{a}{(ax+b)^2}\right). \| 1931:\int \frac{\mathrm{d}x}{a^2x^3} =-\frac{1}{2a^2x^2}+C. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 20 | 1941 | 不定积分 | 习题 | 含有 $\sqrt{ax+b}$ 的积分 - 10 |  | 跳步关键词,短display待判定 | 直接; 1943:y^2=ax+b,\qquad x=\frac{y^2-b}{a},\qquad \mathrm{d}x=\frac{2y}{a}\,\mathrm{d}y. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 21 | 1960 | 不定积分 | 习题 | 含有 $\sqrt{ax+b}$ 的积分 - 11 |  | 短display待判定 | 1962:y^2=ax+b,\qquad x=\frac{y^2-b}{a},\qquad \mathrm{d}x=\frac{2y}{a}\,\mathrm{d}y. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 22 | 1980 | 不定积分 | 习题 | 含有 $\sqrt{ax+b}$ 的积分 - 12 |  | 短display待判定 | 1982:y^2=ax+b,\qquad x=\frac{y^2-b}{a},\qquad \mathrm{d}x=\frac{2y}{a}\,\mathrm{d}y. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 23 | 2000 | 不定积分 | 习题 | 含有 $\sqrt{ax+b}$ 的积分 - 13 |  | 短display待判定 | 2002:y^2=ax+b,\qquad x=\frac{y^2-b}{a},\qquad \mathrm{d}x=\frac{2y}{a}\,\mathrm{d}y. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 24 | 2020 | 不定积分 | 习题 | 含有 $\sqrt{ax+b}$ 的积分 - 14 |  | 短display待判定 | 2022:y^2=ax+b,\qquad x=\frac{y^2-b}{a},\qquad \mathrm{d}x=\frac{2y}{a}\,\mathrm{d}y. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 25 | 2040 | 不定积分 | 习题 | 含有 $\sqrt{ax+b}$ 的积分 - 15 |  | 跳步关键词,短display待判定 | 于是; 2042:y^2=ax+b,\qquad x=\frac{y^2-b}{a},\qquad \mathrm{d}x=\frac{2y}{a}\,\mathrm{d}y. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 26 | 2072 | 不定积分 | 习题 | 含有 $\sqrt{ax+b}$ 的积分 - 16 |  | 短display待判定 | 2074:y^2=ax+b,\qquad x=\frac{y^2-b}{a},\qquad \mathrm{d}x=\frac{2y}{a}\,\mathrm{d}y. \| 2079:\int \frac{\mathrm{d}x}{x^2\sqrt{ax+b}} =\int \frac{2a}{(y^2-b)^2}\,\mathrm{d}y. \| 2084: | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 27 | 2111 | 不定积分 | 习题 | 含有 $\sqrt{ax+b}$ 的积分 - 17 |  | 跳步关键词,短display待判定 | 直接; 2113:y^2=ax+b,\qquad x=\frac{y^2-b}{a},\qquad \mathrm{d}x=\frac{2y}{a}\,\mathrm{d}y. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 28 | 2133 | 不定积分 | 习题 | 含有 $\sqrt{ax+b}$ 的积分 - 18 |  | 跳步关键词,短display待判定 | 直接; 2135:y^2=ax+b,\qquad x=\frac{y^2-b}{a},\qquad \mathrm{d}x=\frac{2y}{a}\,\mathrm{d}y. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 29 | 2156 | 不定积分 | 习题 | 含有 $x^2\pm a^2$ 的积分 - 19 |  | 短display待判定 | 2158:u=\frac{x}{a},\qquad \mathrm{d}u=\frac{1}{a}\,\mathrm{d}x. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 30 | 2173 | 不定积分 | 习题 | 含有 $x^2\pm a^2$ 的积分 - 20 |  | 短display待判定 | 2175:I_n=\int \frac{\mathrm{d}x}{(x^2+a^2)^n}. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 31 | 2206 | 不定积分 | 习题 | 含有 $x^2\pm a^2$ 的积分 - 21 |  | 跳步关键词,短display待判定 | 于是; 2208:\frac{1}{x^2-a^2}=\frac{A}{x-a}+\frac{B}{x+a}. \| 2212:A=\frac{1}{2a},\qquad B=-\frac{1}{2a}. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 32 | 2228 | 不定积分 | 习题 | 含有 $ax^2+b$ 的积分 - 22 |  | 跳步关键词,短display待判定 | 直接; 2249:\int \frac{\mathrm{d}x}{a x^2} =-\frac{1}{a x}+C. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 34 | 2273 | 不定积分 | 习题 | 含有 $ax^2+b$ 的积分 - 24 |  | 跳步关键词 | 直接 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 35 | 2289 | 不定积分 | 习题 | 含有 $ax^2+b$ 的积分 - 25 |  | 跳步关键词,短display待判定 | 直接; 2303:\int \frac{\mathrm{d}x}{a x^3} =-\frac{1}{2a x^2}+C. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 36 | 2312 | 不定积分 | 习题 | 含有 $ax^2+b$ 的积分 - 26 |  | 短display待判定 | 2323:\int \frac{\mathrm{d}x}{a x^4} =-\frac{1}{3a x^3}+C. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 37 | 2332 | 不定积分 | 习题 | 含有 $ax^2+b$ 的积分 - 27 |  | 短display待判定 | 2350:\int \frac{\mathrm{d}x}{a x^5} =-\frac{1}{4a x^4}+C. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 38 | 2359 | 不定积分 | 习题 | 含有 $ax^2+b$ 的积分 - 28 |  | 短display待判定 | 2379:\int \frac{\mathrm{d}x}{(a x^2)^2} =\int \frac{\mathrm{d}x}{a^2x^4} =-\frac{1}{3a^2x^3}+C. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 39 | 2390 | 不定积分 | 习题 | 含有 $ax^2+bx+c$ 的积分 - 29 |  | 短display待判定 | 2427:ax^2+bx+c=\frac{(2ax+b)^2}{4a}, | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 40 | 2442 | 不定积分 | 习题 | 含有 $ax^2+bx+c$ 的积分 - 30 |  | 跳步关键词 | 于是 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 41 | 2461 | 不定积分 | 习题 | 含有 $\sqrt{x^2+a^2}$ 的积分 - 31 |  | 跳步关键词,短display待判定 | 可得; 2463:y=\sqrt{x^2+a^2},\qquad y^2-x^2=a^2,\qquad x\,\mathrm{d}x=y\,\mathrm{d}y. \| 2477:\int \frac{\mathrm{d}x}{\sqrt{x^2+a^2}} =\int \frac{\mathrm{d}x}{y} =\ln(x+y)+C =\ln\!\lef | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 42 | 2488 | 不定积分 | 习题 | 含有 $\sqrt{x^2+a^2}$ 的积分 - 32 |  | 短display待判定 | 2499:\int \frac{\mathrm{d}x}{\sqrt{(x^2+a^2)^3}} =\int \frac{\mathrm{d}x}{y^3} =\frac{1}{a^2}\frac{x}{y}+C =\frac{x}{a^2\sqrt{x^2+a^2}}+C. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 43 | 2510 | 不定积分 | 习题 | 含有 $\sqrt{x^2+a^2}$ 的积分 - 33 |  | 跳步关键词 | 于是 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 44 | 2525 | 不定积分 | 习题 | 含有 $\sqrt{x^2+a^2}$ 的积分 - 34 |  | 跳步关键词 | 于是 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 45 | 2540 | 不定积分 | 习题 | 含有 $\sqrt{x^2+a^2}$ 的积分 - 35 |  | 短display待判定 | 2542:K=\int \frac{x^2}{y}\,\mathrm{d}x,\qquad L=\int \frac{\mathrm{d}x}{y}. \| 2560:\int \frac{x^2}{\sqrt{x^2+a^2}}\,\mathrm{d}x =\frac{x}{2}\sqrt{x^2+a^2} -\frac{a^2}{2}\ln\!\left( | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 47 | 2587 | 不定积分 | 习题 | 含有 $\sqrt{x^2+a^2}$ 的积分 - 37 |  | 跳步关键词,短display待判定 | 可得; 2589:\frac{\mathrm{d}x}{y}=\frac{\mathrm{d}y}{x},\qquad x^2=y^2-a^2, \| 2601:\frac{1}{2a}\ln\left\|\frac{y-a}{y+a}\right\| =\frac{1}{a}\ln\left\|\frac{y-a}{x}\right\|. \| 2606:\int \ | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 48 | 2615 | 不定积分 | 习题 | 含有 $\sqrt{x^2+a^2}$ 的积分 - 38 |  | 短display待判定 | 2625:\int \frac{\mathrm{d}x}{x^2\sqrt{x^2+a^2}} =-\frac{1}{a^2}\frac{y}{x}+C =-\frac{\sqrt{x^2+a^2}}{a^2x}+C. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 49 | 2635 | 不定积分 | 习题 | 含有 $\sqrt{x^2+a^2}$ 的积分 - 39 |  | 短display待判定 | 2653:\int \sqrt{x^2+a^2}\,\mathrm{d}x =\frac{x}{2}\sqrt{x^2+a^2} +\frac{a^2}{2}\ln\!\left(x+\sqrt{x^2+a^2}\right)+C. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 50 | 2663 | 不定积分 | 习题 | 含有 $\sqrt{x^2+a^2}$ 的积分 - 40 |  | 跳步关键词,短display待判定 | 于是; 2665:I_1=\int y\,\mathrm{d}x,\qquad I_2=\int y^3\,\mathrm{d}x. \| 2685:I_2=xy^3-3(I_2-a^2I_1), \qquad 4I_2=xy^3+3a^2I_1. \| 2691:I_1=\frac{1}{2}xy+\frac{a^2}{2}\ln(x+y) | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 51 | 2707 | 不定积分 | 习题 | 含有 $\sqrt{x^2+a^2}$ 的积分 - 41 |  | 跳步关键词 | 于是 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 52 | 2721 | 不定积分 | 习题 | 含有 $\sqrt{x^2+a^2}$ 的积分 - 42 |  | 短display待判定 | 2723:I_1=\int y\,\mathrm{d}x,\qquad I_2=\int y^3\,\mathrm{d}x. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 53 | 2749 | 不定积分 | 习题 | 含有 $\sqrt{x^2+a^2}$ 的积分 - 43 |  | 短display待判定 | 2761:\int \frac{\sqrt{x^2+a^2}}{x}\,\mathrm{d}x =\sqrt{x^2+a^2} +a\ln\left\|\frac{\sqrt{x^2+a^2}-a}{x}\right\|+C. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 55 | 2788 | 不定积分 | 习题 | 含有 $\sqrt{x^2-a^2}$ 的积分 - 45 |  | 跳步关键词,短display待判定 | 可得; 2790:y=\sqrt{x^2-a^2},\qquad x^2-y^2=a^2,\qquad x\,\mathrm{d}x=y\,\mathrm{d}y. \| 2802:\int \frac{\mathrm{d}x}{\sqrt{x^2-a^2}} =\int \frac{\mathrm{d}x}{y} =\ln\|x+y\|+C =\ln\!\lef | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 56 | 2813 | 不定积分 | 习题 | 含有 $\sqrt{x^2-a^2}$ 的积分 - 46 |  | 短display待判定 | 2823:\int \frac{\mathrm{d}x}{\sqrt{(x^2-a^2)^3}} =\int \frac{\mathrm{d}x}{y^3} =-\frac{x}{a^2y}+C =-\frac{x}{a^2\sqrt{x^2-a^2}}+C. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 57 | 2834 | 不定积分 | 习题 | 含有 $\sqrt{x^2-a^2}$ 的积分 - 47 |  | 跳步关键词 | 于是 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 58 | 2849 | 不定积分 | 习题 | 含有 $\sqrt{x^2-a^2}$ 的积分 - 48 |  | 跳步关键词 | 于是 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 59 | 2864 | 不定积分 | 习题 | 含有 $\sqrt{x^2-a^2}$ 的积分 - 49 |  | 短display待判定 | 2866:y=\sqrt{x^2-a^2},\qquad L=\int \frac{\mathrm{d}x}{y},\qquad K=\int \frac{x^2}{y}\,\mathrm{d}x. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 61 | 2909 | 不定积分 | 习题 | 含有 $\sqrt{x^2-a^2}$ 的积分 - 51 |  | 跳步关键词,短display待判定 | 可得; 2911:\frac{\mathrm{d}x}{y}=\frac{\mathrm{d}y}{x},\qquad x^2=y^2+a^2, | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 62 | 2928 | 不定积分 | 习题 | 含有 $\sqrt{x^2-a^2}$ 的积分 - 52 |  | 短display待判定 | 2938:\int \frac{\mathrm{d}x}{x^2\sqrt{x^2-a^2}} =\frac{1}{a^2}\frac{y}{x}+C =\frac{\sqrt{x^2-a^2}}{a^2x}+C. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 63 | 2948 | 不定积分 | 习题 | 含有 $\sqrt{x^2-a^2}$ 的积分 - 53 |  | 短display待判定 | 2950:I_1=\int y\,\mathrm{d}x,\qquad L=\int \frac{\mathrm{d}x}{y}. \| 2968:\int \sqrt{x^2-a^2}\,\mathrm{d}x =\frac{x}{2}\sqrt{x^2-a^2} -\frac{a^2}{2}\ln\!\left\|x+\sqrt{x^2-a^2}\right | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 64 | 2978 | 不定积分 | 习题 | 含有 $\sqrt{x^2-a^2}$ 的积分 - 54 |  | 跳步关键词,短display待判定 | 于是; 2980:I_1=\int y\,\mathrm{d}x,\qquad I_2=\int y^3\,\mathrm{d}x. \| 3001:I_2=xy^3-3(I_2+a^2I_1), \qquad 4I_2=xy^3-3a^2I_1. \| 3007:I_1=\frac{1}{2}xy-\frac{a^2}{2}\ln\|x+y\| | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 65 | 3023 | 不定积分 | 习题 | 含有 $\sqrt{x^2-a^2}$ 的积分 - 55 |  | 跳步关键词 | 于是 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 66 | 3037 | 不定积分 | 习题 | 含有 $\sqrt{x^2-a^2}$ 的积分 - 56 |  | 短display待判定 | 3039:I_1=\int y\,\mathrm{d}x,\qquad I_2=\int y^3\,\mathrm{d}x. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 67 | 3065 | 不定积分 | 习题 | 含有 $\sqrt{x^2-a^2}$ 的积分 - 57 |  | 短display待判定 | 3076:\int \frac{\sqrt{x^2-a^2}}{x}\,\mathrm{d}x =\sqrt{x^2-a^2}-a\arccos\frac{a}{\|x\|}+C. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 69 | 3103 | 不定积分 | 习题 | 含有 $\sqrt{a^2-x^2}$ 的积分 - 59 |  | 短display待判定 | 3105:y=\sqrt{a^2-x^2},\qquad x^2+y^2=a^2,\qquad x\,\mathrm{d}x=-y\,\mathrm{d}y. \| 3110:\mathrm{d}\arcsin\frac{x}{a} =\frac{\mathrm{d}x}{\sqrt{a^2-x^2}} =\frac{\mathrm{d}x}{y}. \| 31 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 70 | 3125 | 不定积分 | 习题 | 含有 $\sqrt{a^2-x^2}$ 的积分 - 60 |  | 跳步关键词,短display待判定 | 于是; 3136:\int \frac{\mathrm{d}x}{\sqrt{(a^2-x^2)^3}} =\int \frac{\mathrm{d}x}{y^3} =\frac{x}{a^2y}+C =\frac{x}{a^2\sqrt{a^2-x^2}}+C. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 71 | 3147 | 不定积分 | 习题 | 含有 $\sqrt{a^2-x^2}$ 的积分 - 61 |  | 跳步关键词 | 于是 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 72 | 3162 | 不定积分 | 习题 | 含有 $\sqrt{a^2-x^2}$ 的积分 - 62 |  | 跳步关键词 | 于是 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 73 | 3177 | 不定积分 | 习题 | 含有 $\sqrt{a^2-x^2}$ 的积分 - 63 |  | 短display待判定 | 3179:y=\sqrt{a^2-x^2},\qquad L=\int \frac{\mathrm{d}x}{y},\qquad K=\int \frac{x^2}{y}\,\mathrm{d}x. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 75 | 3221 | 不定积分 | 习题 | 含有 $\sqrt{a^2-x^2}$ 的积分 - 65 |  | 跳步关键词,短display待判定 | 可得; 3223:\frac{\mathrm{d}x}{y}=-\frac{\mathrm{d}y}{x},\qquad x^2=a^2-y^2, \| 3235:-\frac{1}{2a}\ln\left\|\frac{a+y}{a-y}\right\| =\frac{1}{a}\ln\left\|\frac{a-y}{x}\right\|. \| 3240:\int | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 76 | 3249 | 不定积分 | 习题 | 含有 $\sqrt{a^2-x^2}$ 的积分 - 66 |  | 短display待判定 | 3259:\int \frac{\mathrm{d}x}{x^2\sqrt{a^2-x^2}} =-\frac{1}{a^2}\frac{y}{x}+C =-\frac{\sqrt{a^2-x^2}}{a^2x}+C. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 77 | 3269 | 不定积分 | 习题 | 含有 $\sqrt{a^2-x^2}$ 的积分 - 67 |  | 短display待判定 | 3271:I_1=\int y\,\mathrm{d}x,\qquad L=\int \frac{\mathrm{d}x}{y}. \| 3285:I_1=\frac{1}{2}xy+\frac{a^2}{2}\arcsin\frac{x}{a}+C. \| 3289:\int \sqrt{a^2-x^2}\,\mathrm{d}x =\frac{x}{2}\s | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 78 | 3299 | 不定积分 | 习题 | 含有 $\sqrt{a^2-x^2}$ 的积分 - 68 |  | 跳步关键词,短display待判定 | 于是; 3301:I_1=\int y\,\mathrm{d}x,\qquad I_2=\int y^3\,\mathrm{d}x. \| 3322:I_2=xy^3-3(I_2-a^2I_1), \qquad 4I_2=xy^3+3a^2I_1. \| 3328:I_1=\frac{1}{2}xy+\frac{a^2}{2}\arcsin\frac{x}{a} | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 79 | 3344 | 不定积分 | 习题 | 含有 $\sqrt{a^2-x^2}$ 的积分 - 69 |  | 跳步关键词 | 于是 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 80 | 3358 | 不定积分 | 习题 | 含有 $\sqrt{a^2-x^2}$ 的积分 - 70 |  | 短display待判定 | 3360:I_1=\int y\,\mathrm{d}x,\qquad I_2=\int y^3\,\mathrm{d}x. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 81 | 3386 | 不定积分 | 习题 | 含有 $\sqrt{a^2-x^2}$ 的积分 - 71 |  | 短display待判定 | 3397:\int \frac{\sqrt{a^2-x^2}}{x}\,\mathrm{d}x =\sqrt{a^2-x^2} +a\ln\left\|\frac{a-\sqrt{a^2-x^2}}{x}\right\|+C. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 83 | 3424 | 不定积分 | 习题 | 含有 $\sqrt{ax^2+bx+c}$ 的积分 - 73 |  | 短display待判定 | 3426:y=\sqrt{ax^2+bx+c},\qquad u=2ax+b,\qquad v=2\sqrt a\,y. \| 3432:v^2-u^2=4ac-b^2,\qquad \mathrm{d}x=\frac{\mathrm{d}u}{2a},\qquad y=\frac{v}{2\sqrt a}. \| 3438:\mathrm{d}\ln\|u+v\| | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 84 | 3456 | 不定积分 | 习题 | 含有 $\sqrt{ax^2+bx+c}$ 的积分 - 74 |  | 跳步关键词,短display待判定 | 可得,于是; 3458:y=\sqrt{ax^2+bx+c},\qquad u=2ax+b,\qquad v=2\sqrt a\,y,\qquad \Delta=4ac-b^2. \| 3465:\mathrm{d}x=\frac{\mathrm{d}u}{2a},\qquad y=\frac{v}{2\sqrt a}. \| 3469:\int v\,\mat | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 86 | 3509 | 不定积分 | 习题 | 含有 $\sqrt{ax^2+bx+c}$ 的积分 - 76 |  | 短display待判定 | 3511:y=\sqrt{c+bx-ax^2},\qquad u=2ax-b,\qquad v=2\sqrt a\,y,\qquad \Delta=b^2+4ac. \| 3518:\mathrm{d}x=\frac{\mathrm{d}u}{2a},\qquad y=\frac{v}{2\sqrt a}. \| 3522:\int\frac{\mathrm{d | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 87 | 3540 | 不定积分 | 习题 | 含有 $\sqrt{ax^2+bx+c}$ 的积分 - 77 |  | 跳步关键词,短display待判定 | 于是; 3542:y=\sqrt{c+bx-ax^2},\qquad u=2ax-b,\qquad v=2\sqrt a\,y,\qquad \Delta=b^2+4ac. \| 3549:\int v\,\mathrm{d}u =\frac12uv+\frac{\Delta}{2}\int\frac{\mathrm{d}u}{v}. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 89 | 3590 | 不定积分 | 习题 | 含有 $\sqrt{\frac{x-a}{x-b}}$ 的积分 - 79 |  | 跳步关键词,短display待判定 | 于是; 3592:p=\sqrt{x-a},\qquad q=\sqrt{x-b}, \| 3596:p^2-q^2=b-a,\qquad \mathrm{d}x=2p\,\mathrm{d}p=2q\,\mathrm{d}q. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 90 | 3618 | 不定积分 | 习题 | 含有 $\sqrt{\frac{x-a}{b-x}}$ 的积分 - 80 |  | 短display待判定 | 3620:p^2+q^2=b-a,\qquad \mathrm{d}x=2p\,\mathrm{d}p=-2q\,\mathrm{d}q. \| 3634:\int\sqrt{\frac{x-a}{b-x}}\,\mathrm{d}x =-\sqrt{x-a}\sqrt{b-x} +(b-a)\arcsin\sqrt{\frac{x-a}{b-a}}+C. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 91 | 3644 | 不定积分 | 习题 | 含有 $\sqrt{(x-a)(b-x)}$ 的积分 - 81 |  | 跳步关键词 | 于是 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 92 | 3658 | 不定积分 | 习题 | 含有 $\sqrt{(x-a)(b-x)}$ 的积分 - 82 |  | 跳步关键词,短display待判定 | 于是; 3660:u=p^2-q^2=2x-a-b,\qquad v=2pq=2\sqrt{(x-a)(b-x)}. \| 3665:u^2+v^2=(b-a)^2,\qquad \mathrm{d}u=2\,\mathrm{d}x. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 93 | 3686 | 不定积分 | 习题 | 含有三角函数的积分 - 83 |  | 跳步关键词,短display待判定 | 直接; 3689:\int \sin x\,\mathrm{d}x =-\int \mathrm{d}(\cos x) =-\cos x+C. \| 3697:\int \sin x\,\mathrm{d}x =\int p\,\mathrm{d}x =-\int \mathrm{d}q =-q+C =-\cos x+C. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 94 | 3710 | 不定积分 | 习题 | 含有三角函数的积分 - 84 |  | 跳步关键词,短display待判定 | 可得,直接; 3713:\int \cos x\,\mathrm{d}x =\int \mathrm{d}(\sin x) =\sin x+C. \| 3719:\int \cos x\,\mathrm{d}x =\int q\,\mathrm{d}x =\int \mathrm{d}p =p+C =\sin x+C. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 95 | 3732 | 不定积分 | 习题 | 含有三角函数的积分 - 85 |  | 跳步关键词,短display待判定 | 于是; 3735:\int \tan x\,\mathrm{d}x =\int \frac{\sin x}{\cos x}\,\mathrm{d}x =\int \frac{1}{\cos x}\bigl(-\mathrm{d}(\cos x)\bigr), \| 3741:\int \tan x\,\mathrm{d}x =-\int \frac{\math | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 96 | 3764 | 不定积分 | 习题 | 含有三角函数的积分 - 86 |  | 短display待判定 | 3767:\int \cot x\,\mathrm{d}x =\int \frac{\cos x}{\sin x}\,\mathrm{d}x =\int \frac{1}{\sin x}\mathrm{d}(\sin x). \| 3774:\int \cot x\,\mathrm{d}x =\int \frac{q}{p}\frac{\mathrm{d}p} | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 97 | 3787 | 不定积分 | 习题 | 含有三角函数的积分 - 87 |  | 跳步关键词,短display待判定 | 可得; 3790:\int \sec x\,\mathrm{d}x =\int\frac{\sec x(\sec x+\tan x)} {\sec x+\tan x}\,\mathrm{d}x. \| 3796:\mathrm{d}(\sec x+\tan x) =(\sec x\tan x+\sec^2x)\,\mathrm{d}x, \| 3801:\int | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 98 | 3822 | 不定积分 | 习题 | 含有三角函数的积分 - 88 |  | 跳步关键词,短display待判定 | 可得,于是; 3825:\int \csc x\,\mathrm{d}x =\int\frac{\csc x(\csc x-\cot x)} {\csc x-\cot x}\,\mathrm{d}x. \| 3831:\mathrm{d}(\csc x-\cot x) =(-\csc x\cot x+\csc^2x)\,\mathrm{d}x, \| 3836: | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 99 | 3857 | 不定积分 | 习题 | 含有三角函数的积分 - 89 |  | 短display待判定 | 3863:\int \sec^2 x\,\mathrm{d}x =\int p^2\,\mathrm{d}x =\int \mathrm{d}q =q+C =\tan x+C. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 100 | 3876 | 不定积分 | 习题 | 含有三角函数的积分 - 90 |  | 短display待判定 | 3882:\int \csc^2 x\,\mathrm{d}x =\int p^2\,\mathrm{d}x =-\int \mathrm{d}q =-q+C =-\cot x+C. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 101 | 3895 | 不定积分 | 习题 | 含有三角函数的积分 - 91 |  | 跳步关键词,短display待判定 | 可得; 3901:\int \sec x\tan x\,\mathrm{d}x =\int pq\,\mathrm{d}x =\int \mathrm{d}p =p+C =\sec x+C. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 102 | 3914 | 不定积分 | 习题 | 含有三角函数的积分 - 92 |  | 跳步关键词,短display待判定 | 可得; 3920:\int \csc x\cot x\,\mathrm{d}x =\int pq\,\mathrm{d}x =-\int \mathrm{d}p =-p+C =-\csc x+C. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 103 | 3933 | 不定积分 | 习题 | 含有三角函数的积分 - 93 |  | 跳步关键词,短display待判定 | 可得,于是; 3936:\int \sin^2x\,\mathrm{d}x =\int\frac{1-\cos2x}{2}\,\mathrm{d}x =\frac{x}{2}-\frac{\sin2x}{4}+C. \| 3949:2\int p^2\,\mathrm{d}x =-pq+\int(p^2+q^2)\,\mathrm{d}x =-pq+x. \|  | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 104 | 3966 | 不定积分 | 习题 | 含有三角函数的积分 - 94 |  | 跳步关键词,短display待判定 | 可得,于是; 3969:\int \cos^2x\,\mathrm{d}x =\int\frac{1+\cos2x}{2}\,\mathrm{d}x =\frac{x}{2}+\frac{\sin2x}{4}+C. \| 3982:2\int q^2\,\mathrm{d}x =pq+\int(p^2+q^2)\,\mathrm{d}x =pq+x. \| 39 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 105 | 3999 | 不定积分 | 习题 | 含有三角函数的积分 - 95 |  | 短display待判定 | 4014:I_n =-\frac{\sin^{n-1}x\cos x}{n} +\frac{n-1}{n}I_{n-2}. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 106 | 4035 | 不定积分 | 习题 | 含有三角函数的积分 - 96 |  | 短display待判定 | 4050:I_n =\frac{\cos^{n-1}x\sin x}{n} +\frac{n-1}{n}I_{n-2}. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 107 | 4071 | 不定积分 | 习题 | 含有三角函数的积分 - 97 |  | 跳步关键词,短display待判定 | 整理得; 4086:\int\frac{\mathrm{d}x}{\sin^n x} =-\frac{\cos x}{(n-1)\sin^{n-1}x} +\frac{n-2}{n-1} \int\frac{\mathrm{d}x}{\sin^{n-2}x}. \| 4093:I_{-n} =-\frac{q}{(n-1)p^{n-1}} +\frac{n-2 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 108 | 4105 | 不定积分 | 习题 | 含有三角函数的积分 - 98 |  | 跳步关键词,短display待判定 | 整理得; 4120:\int\frac{\mathrm{d}x}{\cos^n x} =\frac{\sin x}{(n-1)\cos^{n-1}x} +\frac{n-2}{n-1} \int\frac{\mathrm{d}x}{\cos^{n-2}x}. \| 4127:I_{-n} =\frac{p}{(n-1)q^{n-1}} +\frac{n-2}{ | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 109 | 4139 | 不定积分 | 习题 | 含有三角函数的积分 - 99 |  | 短display待判定 | 4141:I_{m,n}=\int \cos^m x\sin^n x\,\mathrm{d}x, \| 4159:I_{m,n} =\frac{\cos^{m-1}x\sin^{n+1}x}{m+n} +\frac{m-1}{m+n}I_{m-2,n}. \| 4177:I_{m,n} =-\frac{\sin^{n-1}x\cos^{m+1}x}{m+n} + | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 110 | 4193 | 不定积分 | 习题 | 含有三角函数的积分 - 100 |  | 短display待判定 | 4196:\sin ax\cos bx =\frac12\bigl[\sin(a+b)x+\sin(a-b)x\bigr], \| 4201:\int \sin ax\cos bx\,\mathrm{d}x =-\frac{\cos(a+b)x}{2(a+b)} -\frac{\cos(a-b)x}{2(a-b)}+C. \| 4207:\int \sin ax | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 111 | 4228 | 不定积分 | 习题 | 含有三角函数的积分 - 101 |  | 短display待判定 | 4231:\sin ax\sin bx =\frac12\bigl[\cos(a-b)x-\cos(a+b)x\bigr], \| 4236:\int \sin ax\sin bx\,\mathrm{d}x =\frac{\sin(a-b)x}{2(a-b)} -\frac{\sin(a+b)x}{2(a+b)}+C. \| 4242:\int\sin^2 ax | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 112 | 4267 | 不定积分 | 习题 | 含有三角函数的积分 - 102 |  | 短display待判定 | 4270:\cos ax\cos bx =\frac12\bigl[\cos(a+b)x+\cos(a-b)x\bigr], \| 4275:\int \cos ax\cos bx\,\mathrm{d}x =\frac{\sin(a+b)x}{2(a+b)} +\frac{\sin(a-b)x}{2(a-b)}+C. \| 4281:\int\cos ax\c | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 113 | 4303 | 不定积分 | 习题 | 含有三角函数的积分 - 103 |  | 跳步关键词,短display待判定 | 直接,于是; 4306:\int\frac{\mathrm{d}x}{a+b\sin x}=\frac{x}{a}+C. \| 4310:\int\frac{\mathrm{d}x}{b\sin x} =\frac1b\ln\|\csc x-\cot x\|+C. \| 4315:t=\tan\frac{x}{2},\qquad \mathrm{d}x=\frac{ | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 114 | 4369 | 不定积分 | 习题 | 含有三角函数的积分 - 104 |  | 跳步关键词,短display待判定 | 于是; 4372:\int\frac{\mathrm{d}x}{a+b\cos x}=\frac{x}{a}+C. \| 4376:\int\frac{\mathrm{d}x}{b\cos x} =\frac1b\ln\|\sec x+\tan x\|+C. \| 4381:t=\tan\frac{x}{2},\qquad \mathrm{d}x=\frac{2\, | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 115 | 4436 | 不定积分 | 习题 | 含有三角函数的积分 - 105 |  | 跳步关键词,短display待判定 | 于是; 4439:\int \frac{\mathrm{d}x}{a^2\cos^2 x+b^2\sin^2 x} =\frac{1}{a^2}\tan x+C. \| 4444:\int \frac{\mathrm{d}x}{b^2\sin^2 x} =-\frac{1}{b^2}\cot x+C. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 116 | 4472 | 不定积分 | 习题 | 含有三角函数的积分 - 106 |  | 短display待判定 | 4475:\int \frac{\mathrm{d}x}{a^2\cos^2 x-b^2\sin^2 x} =\frac{1}{a^2}\tan x+C. \| 4480:\int \frac{\mathrm{d}x}{-b^2\sin^2 x} =\frac{1}{b^2}\cot x+C. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 117 | 4513 | 不定积分 | 习题 | 含有三角函数的积分 - 110 |  | 跳步关键词,短display待判定 | 直接,于是; 4516:u=x,\qquad \mathrm{d}v=\sin ax\,\mathrm{d}x =\mathrm{d}\left(-\frac{1}{a}\cos ax\right), | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 118 | 4542 | 不定积分 | 习题 | 含有三角函数的积分 - 111 |  | 跳步关键词,短display待判定 | 可得; 4545:\int x\cos ax\,\mathrm{d}x=\int x\,\mathrm{d}x=\frac{x^2}{2}+C. \| 4549:u=x,\qquad \mathrm{d}v=\cos ax\,\mathrm{d}x =\mathrm{d}\left(\frac1a\sin ax\right). | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 119 | 4573 | 不定积分 | 习题 | 含有三角函数的积分 - 112 |  | 跳步关键词,短display待判定 | 可得; 4576:\int \sin ax\,\mathrm{d}x=-\frac{1}{a}\cos ax+C. \| 4580:u=x^n,\qquad \mathrm{d}v=\sin ax\,\mathrm{d}x =\mathrm{d}\left(-\frac{1}{a}\cos ax\right), | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 120 | 4609 | 不定积分 | 习题 | 含有三角函数的积分 - 113 |  | 跳步关键词,短display待判定 | 可得; 4612:\int x^n\cos ax\,\mathrm{d}x =\int x^n\,\mathrm{d}x =\frac{x^{n+1}}{n+1}+C. \| 4618:\int \cos ax\,\mathrm{d}x=\frac{1}{a}\sin ax+C. \| 4622:u=x^n,\qquad \mathrm{d}v=\cos ax\ | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 121 | 4654 | 不定积分 | 习题 | 含有反三角函数的积分 - 114 |  | 跳步关键词,短display待判定 | 直接; 4666:\mathrm{d}\left(\arcsin\frac{x}{a}\right) = \frac{\mathrm{d}x}{\sqrt{a^2-x^2}} = \frac{\mathrm{d}x}{y}. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 123 | 4714 | 不定积分 | 习题 | 含有反三角函数的积分 - 116 |  | 跳步关键词 | 直接 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 125 | 4776 | 不定积分 | 习题 | 含有反三角函数的积分 - 118 |  | 短display待判定 | 4791:\int \frac{\mathrm{d}x}{\sqrt{a^2-x^2}}=-\arccos\frac{x}{a} \| 4796:\int \frac{\mathrm{d}x}{y}=-\arccos\frac{x}{a},\qquad \int y\mathrm{d}x=\frac{1}{2}xy+\frac{a^2}{2}\int\frac | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 128 | 4887 | 不定积分 | 习题 | 含有反三角函数的积分 - 121 |  | 短display待判定 | 4903:\mathrm{d}\left(\arctan\frac{x}{a}\right)=\frac{a}{y^2}\mathrm{d}x. \| 4907:\int \frac{\mathrm{d}x}{y^2}=\frac{1}{a}\arctan\frac{x}{a} | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 130 | 4967 | 不定积分 | 习题 | 含有指数函数的积分 - 123 |  | 跳步关键词,短display待判定 | 于是; 4972:\int a^x\,\mathrm{d}x =\int e^{x\ln a}\,\mathrm{d}x =\frac{1}{\ln a}e^{x\ln a}+C =\frac{a^x}{\ln a}+C. \| 4979:\left(\frac{a^x}{\ln a}\right)' =\frac{a^x\ln a}{\ln a} =a^x, | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 131 | 4994 | 不定积分 | 习题 | 含有指数函数的积分 - 124 |  | 短display待判定 | 4997:\int e^{ax}\,\mathrm{d}x =\frac1a\int e^{ax}\,\mathrm{d}(ax) =\frac1a e^{ax}+C. \| 5003:\left(\frac1a e^{ax}\right)'=e^{ax}\qquad(a\ne0). | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 132 | 5013 | 不定积分 | 习题 | 含有指数函数的积分 - 125 |  | 短display待判定 | 5016:u=x,\qquad \mathrm{d}v=e^{ax}\,\mathrm{d}x =\mathrm{d}\left(\frac1a e^{ax}\right). | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 133 | 5038 | 不定积分 | 习题 | 含有指数函数的积分 - 126 |  | 跳步关键词,短display待判定 | 可得; 5052:I_n =e^{ax}\sum_{k=0}^{n} (-1)^k\frac{n!}{(n-k)!}\frac{x^{n-k}}{a^{k+1}}+C, \qquad a\ne0. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 134 | 5065 | 不定积分 | 习题 | 含有指数函数的积分 - 127 |  | 长行内公式/排版风险,短display待判定 | 5067:199; 5069:\int x a^x\mathrm{d}x =\frac{x a^x}{\ln a} -\frac{a^x}{(\ln a)^2}+C. \| 5075:\int xa^x\,\mathrm{d}x =a^x\left(\frac{x}{L}-\frac{1}{L^2}\right)+C, | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 135 | 5086 | 不定积分 | 习题 | 含有指数函数的积分 - 128 |  | 短display待判定 | 5100:J_n =a^x\sum_{k=0}^{n} (-1)^k\frac{n!}{(n-k)!}\frac{x^{n-k}}{L^{k+1}}+C, \qquad L=\ln a\ne0. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 136 | 5112 | 不定积分 | 习题 | 含有指数函数的积分 - 129 |  | 跳步关键词,短display待判定 | 直接; 5123:\int e^{ax}\sin bx\,\mathrm{d}x =\frac{e^{ax}}{a^2+b^2} (a\sin bx-b\cos bx)+C. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 137 | 5137 | 不定积分 | 习题 | 含有指数函数的积分 - 130 |  | 短display待判定 | 5141:F' =e^{ax}\bigl[(aA+bB)\cos bx +(aB-bA)\sin bx\bigr]. \| 5148:\int e^{ax}\cos bx\,\mathrm{d}x =\frac{e^{ax}}{a^2+b^2} (a\cos bx+b\sin bx)+C. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 138 | 5160 | 不定积分 | 习题 | 含有指数函数的积分 - 131 |  | 短display待判定 | 5163:U=e^{ax}\sin^n bx,\qquad V=e^{ax}\sin^{n-1}bx\cos bx. \| 5175:aU'-nbV' =(a^2+n^2b^2)U -n(n-1)b^2e^{ax}\sin^{n-2}bx. \| 5181:aU-nbV =(a^2+n^2b^2)I_n -n(n-1)b^2I_{n-2}. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 139 | 5205 | 不定积分 | 习题 | 含有指数函数的积分 - 132 |  | 跳步关键词,短display待判定 | 于是; 5208:U=e^{ax}\cos^n bx,\qquad V=e^{ax}\cos^{n-1}bx\sin bx. \| 5220:aU'+nbV' =(a^2+n^2b^2)U -n(n-1)b^2e^{ax}\cos^{n-2}bx. \| 5226:aU+nbV =(a^2+n^2b^2)I_n -n(n-1)b^2I_{n-2}. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 140 | 5251 | 不定积分 | 习题 | 含有对数函数的积分 - 132(b) |  | 跳步关键词 | 于是 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 141 | 5270 | 不定积分 | 习题 | 含有对数函数的积分 - 133 |  | 跳步关键词,短display待判定 | 于是; 5273:\int \frac{\mathrm{d}x}{x\ln x} =\int \frac{\mathrm{d}(\ln x)}{\ln x} =\ln\|\ln x\|+C. \| 5280:\int \frac{\mathrm{d}x}{x\ln x} =\int \frac{e^t\,\mathrm{d}t}{e^t t} =\int\frac | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 142 | 5293 | 不定积分 | 习题 | 含有对数函数的积分 - 134 |  | 短display待判定 | 5307:\int \frac{\ln x}{x}\,\mathrm{d}x =\frac12(\ln x)^2+C. \| 5313:\int x^n\ln x\,\mathrm{d}x =\int t e^{(n+1)t}\,\mathrm{d}t. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 143 | 5335 | 不定积分 | 习题 | 含有对数函数的积分 - 135 |  | 短display待判定 | 5347:\int t^ne^t\,\mathrm{d}t =t^ne^t-n\int t^{n-1}e^t\,\mathrm{d}t. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 144 | 5358 | 不定积分 | 习题 | 含有对数函数的积分 - 136 |  | 短display待判定 | 5382:\int t^n e^{(m+1)t}\,\mathrm{d}t =\frac{t^ne^{(m+1)t}}{m+1} -\frac{n}{m+1} \int t^{n-1}e^{(m+1)t}\,\mathrm{d}t. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 145 | 5396 | 不定积分 | 习题 | 含有双曲函数的积分 - 137 |  | 跳步关键词,短display待判定 | 于是; 5400:\int \sinh x\,\mathrm{d}x =\frac12\int(e^x-e^{-x})\,\mathrm{d}x =\frac12(e^x+e^{-x})+C =\cosh x+C. \| 5409:\int \sinh x\,\mathrm{d}x =\int q\,\mathrm{d}x =\int \mathrm{d}p  | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 146 | 5422 | 不定积分 | 习题 | 含有双曲函数的积分 - 138 |  | 跳步关键词,短display待判定 | 可得; 5426:\int \cosh x\,\mathrm{d}x =\frac12\int(e^x+e^{-x})\,\mathrm{d}x =\frac12(e^x-e^{-x})+C =\sinh x+C. \| 5435:\int \cosh x\,\mathrm{d}x =\int p\,\mathrm{d}x =\int\mathrm{d}q = | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 147 | 5448 | 不定积分 | 习题 | 含有双曲函数的积分 - 139 |  | 短display待判定 | 5451:\int \tanh x\,\mathrm{d}x =\int \frac{\sinh x}{\cosh x}\,\mathrm{d}x =\int \frac{\mathrm{d}(\cosh x)}{\cosh x} =\ln(\cosh x)+C. \| 5458:\int \tanh x\,\mathrm{d}x =\int \frac{q} | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 148 | 5472 | 不定积分 | 习题 | 含有双曲函数的积分 - 140 |  | 跳步关键词,短display待判定 | 于是; 5476:\int\sinh^2x\,\mathrm{d}x =\frac12\int(\cosh2x-1)\,\mathrm{d}x =\frac14\sinh2x-\frac{x}{2}+C. \| 5491:\int\sinh^2x\,\mathrm{d}x =\frac12(pq-x)+C =\frac14\sinh2x-\frac{x}{2} | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 149 | 5502 | 不定积分 | 习题 | 含有双曲函数的积分 - 141 |  | 跳步关键词,短display待判定 | 于是; 5506:\int\cosh^2x\,\mathrm{d}x =\frac12\int(\cosh2x+1)\,\mathrm{d}x =\frac14\sinh2x+\frac{x}{2}+C. \| 5513:\int\cosh^2x\,\mathrm{d}x =\frac12(pq+x)+C =\frac14\sinh2x+\frac{x}{2} | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 150 | 5525 | 不定积分 | 习题 | 定积分 - 142 |  | 短display待判定 | 5538:\int_{-\pi}^{\pi}e^{inx}\,\mathrm{d}x =\left[\frac{e^{inx}}{in}\right]_{-\pi}^{\pi} =\frac{e^{in\pi}-e^{-in\pi}}{in}=0. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 151 | 5550 | 不定积分 | 习题 | 定积分 - 143 |  | 跳步关键词 | 直接,于是 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 154 | 5618 | 不定积分 | 习题 | 定积分 - 146 |  | 短display待判定 | 5622:\int_0^\pi\sin^2 mx\,\mathrm{d}x =\frac12\int_0^\pi(1-\cos2mx)\,\mathrm{d}x =\frac{\pi}{2}. \| 5629:\int_0^\pi\cos^2 mx\,\mathrm{d}x =\frac12\int_0^\pi(1+\cos2mx)\,\mathrm{d}x  | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 155 | 5655 | 不定积分 | 习题 | 定积分 - 147 |  | 跳步关键词,短display待判定 | 整理得; 5661:p^2+q^2=1,\qquad \mathrm{d}p=q\,\mathrm{d}x,\qquad \mathrm{d}q=-p\,\mathrm{d}x. \| 5667:x=0:\ (p,q)=(0,1),\qquad x=\frac{\pi}{2}:\ (p,q)=(1,0), \| 5685:I_n=\frac{n-1}{n}I_{ | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 156 | 5719 | 微分方程 | 知识讲解 | 已知通解 $y=c_1\mathrm{e}^{-x}+c_2\mathrm{e}^{2x}$，求其所满足的微分方程。 | 微分方程 | 跳步关键词,短display待判定 | 整理得; 5721:y'=-c_1\mathrm{e}^{-x}+2c_2\mathrm{e}^{2x},\qquad y''=c_1\mathrm{e}^{-x}+4c_2\mathrm{e}^{2x}. \| 5726:y+y''=5c_2\mathrm{e}^{2x},\qquad y'-y=-3c_2\mathrm{e}^{2x} | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 157 | 5748 | 微分方程 | 知识讲解 | 求 $\displaystyle\frac{\mathrm{d}y}{\mathrm{d}x}=-\frac{x}{y}$ 的通解。 | 微分方程 | 短display待判定 | 5751:\int y\,\mathrm{d}y=-\int x\,\mathrm{d}x,\qquad \frac{1}{2}y^{2}=-\frac{1}{2}x^{2}+C. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 158 | 5762 | 微分方程 | 知识讲解 | 求方程 $x^{2}y\,\mathrm{d}y+\sqrt{1-y^{2}}\,\mathrm{d}x=0$ 的全部解。 | 微分方程 | 短display待判定 | 5764:-\frac{y\,\mathrm{d}y}{\sqrt{1-y^{2}}} =\frac{\mathrm{d}x}{x^{2}}. \| 5769:\sqrt{1-y^{2}}=-\frac{1}{x}+C, | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 160 | 5795 | 微分方程 | 知识讲解 | 求 $\displaystyle\frac{\mathrm{d}y}{\mathrm{d}x}=p(x)\,y$ 的通解，其中 $p(x)$ 是连续函数。 | 微分方程 | 短display待判定 | 5797:\int\frac{\mathrm{d}y}{y} =\int p(x)\,\mathrm{d}x, \qquad \ln\|y\|=\int p(x)\,\mathrm{d}x+\bar{C}. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 161 | 5837 | 微分方程 | 知识讲解 | 求 $\displaystyle\frac{\mathrm{d}y}{\mathrm{d}x}=\frac{y}{x}+\tan\frac{y}{x}$ 的通解 | 微分方程 | 跳步关键词,短display待判定 | 于是; 5847:\frac{\mathrm{d}u}{\tan u} =\frac{\mathrm{d}x}{x}, \qquad \frac{\cos u}{\sin u}\mathrm{d}u =\frac{\mathrm{d}x}{x}. \| 5855:\int \frac{\mathrm{d}(\sin u)}{\sin u} =\int \fra | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 162 | 5873 | 微分方程 | 知识讲解 | 求解 $(x+y)\,\mathrm{d}x-(y-x)\,\mathrm{d}y=0$。 | 微分方程 | 短display待判定 | 5880:(x+ux)\,\mathrm{d}x -(ux-x)(u\,\mathrm{d}x+x\,\mathrm{d}u)=0. \| 5902:2\ln\|x\|+\ln\|1+2u-u^2\|=2C_1, \qquad \ln\left\|x^2(1+2u-u^2)\right\|=2C_1. \| 5908:x^2(1+2u-u^2)=C. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 163 | 5922 | 微分方程 | 知识讲解 | 求解 $x\,\mathrm{d}y-y\,\mathrm{d}x=\sqrt{x^{2}+y^{2}}\,\mathrm{d}x$。 | 微分方程 | 跳步关键词,短display待判定 | 同理,直接; 5928:\frac{\mathrm{d}y}{\mathrm{d}x} =\frac{y}{x}+\frac{\sqrt{x^2+y^2}}{x} =\frac{y}{x}+\sqrt{1+\left(\frac{y}{x}\right)^2}. \| 5936:u+x\frac{\mathrm{d}u}{\mathrm{d}x} =u+\sq | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 164 | 5978 | 微分方程 | 知识讲解 | 求解方程 $\displaystyle\frac{\mathrm{d}y}{\mathrm{d}x}=\frac{a_1x+b_1y+c_1}{a_2x+b_2 |  | 跳步关键词,短display待判定 | 代入得,直接; 5984:\frac{\mathrm{d}y}{\mathrm{d}x} =\frac{a_1x+b_1y}{a_2x+b_2y}. \| 5989:u+x\frac{\mathrm{d}u}{\mathrm{d}x} =\frac{a_1+b_1u}{a_2+b_2u}. \| 5998:a_1x+b_1y=\lambda L,\qquad a | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 165 | 6039 | 微分方程 | 知识讲解 | 求解 $\displaystyle\frac{\mathrm{d}y}{\mathrm{d}x}=\frac{x-y+1}{x+y-3}$。 |  | 跳步关键词,短display待判定 | 化简得; 6062:\ln\|1-2u-u^2\|=-2\ln\|X\|-2C_1=\ln(X^{-2})+C_2. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 166 | 6078 | 微分方程 | 知识讲解 | 求解初值问题 $\begin{cases}(x^2+2xy-y^2)\mathrm{d}x+(y^2+2xy-x^2)\mathrm{d}y=0,\\ y(1) | 微分方程 | 跳步关键词,短display待判定 | 显然,整理得,于是; 6114:\ln(u^2+1)-\ln\|u+1\| =-\ln\|x\|+\ln\|C\|, \qquad \ln\frac{u^2+1}{\|u+1\|} =\ln\frac{\|C\|}{\|x\|}. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 167 | 6146 | 微分方程 | 知识讲解 | 求解：(1) $f(xy)y\,\mathrm{d}x+g(xy)x\,\mathrm{d}y=0$； \quad (2) $\displaystyle\fra | 微分方程 | 短display待判定 | 6152:f(u)\frac{u}{x}\,\mathrm{d}x +g(u)\left(\mathrm{d}u-\frac{u}{x}\,\mathrm{d}x\right)=0. \| 6157:u\bigl[f(u)-g(u)\bigr]\frac{\mathrm{d}x}{x} +g(u)\mathrm{d}u=0. \| 6162:\frac{\mat | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 168 | 6242 | 微分方程 | 知识讲解 | 求方程 $\displaystyle\frac{\mathrm{d}y}{\mathrm{d}x}-\frac{y}{x}=x^{2}$ 的通解。 | 微分方程 | 跳步关键词,短display待判定 | 直接,略,于是; 6259:\frac{y}{x}=\int x\,\mathrm{d}x =\frac{x^{2}}{2}+C_0. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 169 | 6271 | 微分方程 | 知识讲解 | 解初值问题 $\begin{cases}(x^{2}-1)y'+2xy=\cos x,\\ y(0)=1.\end{cases}$ | 微分方程,极值/拉格朗日 | 跳步关键词,短display待判定 | 直接; 6279:(x^2-1)y=\int \cos x\,\mathrm{d}x=\sin x+C_0,\qquad y=\frac{\sin x+C_0}{x^2-1}. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 170 | 6291 | 微分方程 | 知识讲解 | 解方程 $y\ln y\,\mathrm{d}x+(x-\ln y)\,\mathrm{d}y=0$。 | 微分方程 | 短display待判定 | 6297:y\ln y\frac{\mathrm{d}x}{\mathrm{d}y}+(x-\ln y)=0 \implies \frac{\mathrm{d}x}{\mathrm{d}y}+\frac{1}{y\ln y}x=\frac{1}{y}. \| 6320:x\ln y=\int \frac{\ln y}{y}\,\mathrm{d}y =\int | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 171 | 6338 | 微分方程 | 知识讲解 | 质点在驱动力与阻力下的运动 | 微分方程 | 短display待判定 | 6348:\frac{\mathrm{d}v}{v}=-\frac{k_2}{m}\,\mathrm{d}t \implies \ln\|v\|=-\frac{k_2}{m}t+C_1 \implies v_h=C\mathrm{e}^{-\frac{k_2}{m}t}. \| 6365:v(t)=\frac{k_1}{2m}t^2. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 172 | 6392 | 微分方程 | 知识讲解 | 解方程 $\displaystyle\frac{\mathrm{d}y}{\mathrm{d}x}=\frac{4}{x}y+x\sqrt{y}\;(y>0,x | 微分方程 | 短display待判定 | 6397:y^{-\frac{1}{2}}\frac{\mathrm{d}y}{\mathrm{d}x} -\frac{4}{x}y^{\frac{1}{2}}=x,\qquad z=y^{\frac{1}{2}},\qquad \frac{\mathrm{d}z}{\mathrm{d}x} =\frac{1}{2}y^{-\f \| 6419:\sqrt{y | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 173 | 6531 | 微分方程 | 知识讲解 | 用 $X(x)Y(y)$ 积分因子看换元题 | 微分方程 | 跳步关键词,短display待判定 | 于是; 6534:\left(-\frac1x-\mathrm e^y\right)\mathrm{d}x+\mathrm{d}y=0, \| 6538:M=-\frac1x-\mathrm e^y,\qquad N=1,\qquad M_y-N_x=-\mathrm e^y. \| 6542:N\frac{X'}{X}-M\frac{Y'}{Y}=M_y-N_ | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 174 | 6664 | 微分方程 | 知识讲解 | 换元一例 | 微分方程,隐函数/偏导 | 跳步关键词,短display待判定 | 代入得; 6667:\sec^2 y\cdot\frac{X'}{X}-\left(\frac{x}{1+x^2}\tan y-x\right)\dfrac{Y'}{Y}=\frac{x}{1+x^2}\sec^2 y. \| 6671:\sec^2 y\cdot\frac{X'}{X}=\frac{x}{1+x^2}\sec^2 y\implies (\ln | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 175 | 6711 | 微分方程 | 知识讲解 | 如图所示的 $R$--$C$ 电路，电容 $C$ 初始无电荷。 合上开关 K 后电池 $E$ 对电容充电，求电压 $u_C$ 随时间的变化规律。 | 微分方程 | 短display待判定 | 6720:-\ln\|E-u_C\|=\frac{t}{RC}+C_1. \| 6724:E-u_C=K\mathrm{e}^{-\frac{t}{RC}}, \qquad u_C(t)=E-K\mathrm{e}^{-\frac{t}{RC}}. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 176 | 6742 | 微分方程 | 知识讲解 | 制造探照灯反射镜时要求点光源发出的光经镜面反射后平行射出， 试求反射镜面的几何形状。 | 微分方程 | 长行内公式/排版风险,短display待判定 | 6746:215; 6749:\frac{\mathrm{d}y}{\mathrm{d}x} =\frac{r-x}{y} =\frac{y}{r+x} =\frac{y}{x+\sqrt{x^2+y^2}}. \| 6758:\frac{\mathrm{d}x}{\mathrm{d}y} =\frac{x+\sqrt{x^2+y^2}}{y} =\frac{ | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 177 | 6818 | 微分方程 | 知识讲解 | 逐次积分 | 微分方程 | 短display待判定,高风险题解过短 | 6821:\boxed{y=\frac{1}{27}\mathrm{e}^{3x}+\sin x+\frac{C_1}{2}x^{2}+C_2x+C_3}. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 178 | 6829 | 微分方程 | 知识讲解 | 解初值问题 \(\displaystyle y''=\dfrac{3x^{2}}{1+x^{3}}\,y',\quad y\|_{x=0}=1,\quad y'\| | 微分方程 | 跳步关键词,短display待判定 | 代入得; 6831:p'=\frac{3x^{2}}{1+x^{3}}\,p. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 179 | 6845 | 微分方程 | 知识讲解 | 求 $y^{(5)}-\dfrac{1}{x}y^{(4)}=0$ 的通解。 | 微分方程 | 跳步关键词 | 于是 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 180 | 6866 | 微分方程 | 知识讲解 | 求 $y''=\dfrac{1+y'^{2}}{2y}$ 的通解。 | 微分方程 | 短display待判定 | 6869:\frac{2p\,\mathrm{d}p}{1+p^{2}}=\frac{\mathrm{d}y}{y}, \qquad \ln(1+p^{2})=\ln\|y\|+\ln\|C\|. \| 6875:p=\pm\sqrt{Cy-1}, \qquad \frac{\mathrm{d}y}{\mathrm{d}x}=\pm\sqrt{Cy-1}. \| 688 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 181 | 6897 | 微分方程 | 知识讲解 | 求 $yy''-y'^{2}=0$ 的通解。 | 微分方程 | 跳步关键词 | 代入得 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 182 | 6915 | 微分方程 | 知识讲解 | 导弹追击舰船 | 极值/拉格朗日 | 跳步关键词 | 于是 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 183 | 6948 | 微分方程 | 知识讲解 | 悬链线的形状 |  | 短display待判定 | 6955:H\tan\theta=\rho g\int_{0}^{x}\sqrt{1+y'^{2}}\;\mathrm{d}x. \| 6959:y'=\frac{\rho g}{H}\int_{0}^{x}\sqrt{1+y'^{2}}\;\mathrm{d}x. \| 6965:\frac{\mathrm{d}p}{\mathrm{d}x}=a\sqrt{1 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 186 | 7196 | 微分方程 | 知识讲解 | 非齐次通解的构造 | 微分方程 | 短display待判定 | 7202:(y^*)''-y^*=0-(Ax+B)=x. \| 7206:-A=1,\qquad -B=0, | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 188 | 7272 | 微分方程 | 知识讲解 | 求解 $y''+y=0$。 | 微分方程 | 高风险题解过短 |  | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 189 | 7281 | 微分方程 | 知识讲解 | 求解 $y''-y=0$。 | 微分方程 | 跳步关键词,高风险题解过短 | 可得 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 192 | 7342 | 微分方程 | 知识讲解 | 求微分方程 $y''-2y'+2y=x\mathrm{e}^x\cos x$ 的一个特解。 | 微分方程 | 跳步关键词,短display待判定 | 整理得; 7347:y^* = x\mathrm{e}^x\bigl[(Ax+B)\cos x + (Cx+D)\sin x\bigr] = \mathrm{e}^x\bigl[(Ax^2+Bx)\cos x + (Cx^2+Dx)\sin x\bigr] \| 7351:(y^*)'' - 2(y^*)' + 2y^* = \mathrm{e}^x\bigl | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 193 | 7374 | 微分方程 | 知识讲解 | 求 $y''-y=2x\,\mathrm{e}^{x}$ 的通解。 | 微分方程 | 跳步关键词,短display待判定 | 于是; 7379:L[\mathrm e^xz]=\mathrm e^x(z''+2z'). \| 7383:z'=2b_0x+b_1,\qquad z''=2b_0. \| 7387:L[y^*] =\mathrm e^x\bigl(4b_0x+2(b_0+b_1)\bigr). | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 194 | 7404 | 微分方程 | 知识讲解 | 求 $y''+4y'+4y=\cos 2x$ 的一个特解。 | 微分方程 | 短display待判定 | 7408:(y^*)'=-2A\sin2x+2B\cos2x, \qquad (y^*)''=-4A\cos2x-4B\sin2x. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 195 | 7481 | 微分方程 | 知识讲解 | 常数变易法的实际应用 | 微分方程 | 跳步关键词,短display待判定 | 直接; 7506:c_1'(x)(\sin^2x+\cos^2x)=1, \qquad c_1'(x)=1. \| 7512:\sin x+c_2'(x)\cos x=0, \qquad c_2'(x)=-\frac{\sin x}{\cos x}=-\tan x. \| 7520:c_1(x)=\int1\,\mathrm{d}x=x, | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 196 | 7650 | 微分方程 | 知识讲解 | 降阶法的应用 | 微分方程 | 短display待判定 | 7672:u(x)=\int \frac{1}{x^2}\cdot\frac{1}{1-x^2}\,\mathrm{d}x. \| 7676:\frac{1}{x^2(1-x^2)} =\frac{1}{x^2}+\frac{1}{1-x^2}. \| 7681:u(x)=\int\left(\frac{1}{x^2}+\frac{1}{1-x^2}\right | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 197 | 7774 | 微分方程 | 知识讲解 | 求解 $x^2y''-2y=x\;(x>0)$。 | 微分方程 | 跳步关键词,短display待判定 | 代入得; 7778:xy'=\frac{\mathrm{d}y}{\mathrm{d}t},\qquad x^2y''=\frac{\mathrm{d}^2y}{\mathrm{d}t^2} -\frac{\mathrm{d}y}{\mathrm{d}t}. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 199 | 7898 | 微分方程 | 知识讲解 | 消元法 I：重根情形 | 微分方程 | 短display待判定 | 7909:x'(t) =C_2\mathrm{e}^{-2t}-2(C_1+C_2t)\mathrm{e}^{-2t} =\mathrm{e}^{-2t}(C_2-2C_1-2C_2t). \| 7924:\boxed{ x(t)=(C_1+C_2t)\,\mathrm{e}^{-2t},\qquad y(t)=-(C_1+C_2+C_2t)\,\mathrm | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 200 | 7940 | 微分方程 | 知识讲解 | 消元法 II：带初值条件的非齐次型转化 | 微分方程 | 短display待判定 | 7946:\frac12(y''+y')=\frac32(y'+y)-2y=\frac32y'-\frac12y, \| 7954:y'(t)=C_2\mathrm{e}^t+(C_1+C_2t)\mathrm{e}^t =\mathrm{e}^t(C_1+C_2+C_2t). \| 7969:y(0)=C_1=0,\qquad x(0)=C_1+\frac{1 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 202 | 8000 | 微分方程 | 习题 | 验证解 | 微分方程 | 高风险题解过短 |  | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 203 | 8008 | 微分方程 | 习题 | 求参数 | 微分方程 | 高风险题解过短 |  | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 204 | 8016 | 微分方程 | 习题 | 求参数 |  | 跳步关键词,短display待判定 | 可得; 8021:9-\omega^2=0, \qquad \omega=\pm3. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 206 | 8082 | 微分方程 | 习题 | 函数对应微分方程 | 微分方程 | 短display待判定 | 8085:y'=2\cos x,\qquad y''=-2\sin x=-y, \| 8090:y'=2\cos 2x,\qquad y''=-4\sin 2x=-4y, \| 8095:y'=2\mathrm{e}^{2x}=2y, | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 207 | 8122 | 微分方程 | 习题 | 函数对应微分方程 | 微分方程 | 短display待判定 | 8130:x^2y''+2xy'-2y =x^2(6x^{-4})+2x(-2x^{-3})-2x^{-2} =0, | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 208 | 8154 | 微分方程 | 习题 | 曲线族对应微分方程 | 微分方程 | 短display待判定 | 8160:\mathrm{e}^{kx}=\frac{y}{x}, \qquad kx=\ln\frac{y}{x}. \| 8166:\frac{\mathrm{d}y}{\mathrm{d}x} =\frac{y}{x}+\left(\ln\frac{y}{x}\right)\frac{y}{x} =\frac{y}{x}\left(1+\ln\frac{ | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 209 | 8210 | 微分方程 | 习题 | 曲线族对应微分方程 | 微分方程 | 跳步关键词,短display待判定 | 可得,于是; 8215:(y')^2 =4C_1^2(x-C_2)^2 =4C_1\bigl[C_1(x-C_2)^2\bigr] =4C_1y =2yy''. \| 8223:\boxed{2yy''-(y')^2=0}. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 210 | 8240 | 微分方程 | 习题 | 相关概念 | 微分方程 | 跳步关键词,短display待判定 | 于是; 8248:u+x\frac{\mathrm{d}u}{\mathrm{d}x}=\varphi(u), \qquad \frac{\mathrm{d}u}{\mathrm{d}x}=\frac{\varphi(u)-u}{x}, | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 211 | 8260 | 微分方程 | 习题 | 求解方程 | 微分方程 | 短display待判定 | 8262:\frac{\mathrm{d}H}{H-20}=-k\,\mathrm{d}t, \qquad \ln\|H-20\|=-kt+C_1. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 212 | 8273 | 微分方程 | 习题 | 求解方程 | 极值/拉格朗日 | 跳步关键词,短display待判定 | 于是; 8275:\frac{\mathrm{d}P}{\mathrm{d}t}=2P(1-t). \| 8279:\frac{\mathrm{d}P}{P}=2(1-t)\,\mathrm{d}t, \qquad \ln P=2t-t^2+C_1. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 213 | 8301 | 微分方程 | 习题 | 求解方程 | 微分方程 | 跳步关键词,短display待判定 | 于是; 8304:\frac{\mathrm{d}P}{P}=0.02\,\mathrm{d}t, \qquad P=C\mathrm{e}^{0.02t}. \| 8312:\frac{\mathrm{d}y}{y}=-\frac{1}{3}\,\mathrm{d}x, \qquad y=C\mathrm{e}^{-x/3}. \| 8320:\frac{\m | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 214 | 8384 | 微分方程 | 习题 | 求解方程 | 微分方程 | 短display待判定 | 8386:\frac{\mathrm{d}y}{1-y}=\mathrm{d}t, \qquad -\ln\|1-y\|=t+C. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 215 | 8401 | 微分方程 | 习题 | 求解齐次方程 | 微分方程 | 跳步关键词,短display待判定 | 代入得,于是; 8405:u + x\frac{\mathrm{d}u}{\mathrm{d}x} = u\ln u \implies x\frac{\mathrm{d}u}{\mathrm{d}x} = u(\ln u - 1), \qquad \frac{\mathrm{d}u}{u(\ln u - 1)} = \frac{\mathrm{ \| 8413 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 216 | 8492 | 微分方程 | 习题 | 求解齐次方程 |  | 短display待判定 | 8495:y^2=2x^2(\ln x+C). \| 8499:y^2=2x^2(\ln x+2). \| 8503:\boxed{y=x\sqrt{2\ln x+4}}. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 217 | 8541 | 微分方程 | 习题 | 求解方程 | 微分方程 | 短display待判定 | 8544:y-x-2=0,\qquad x+y+4=0 \| 8548:\frac{\mathrm{d}Y}{\mathrm{d}X}=\frac{Y-X}{X+Y}. \| 8552:u+X\frac{\mathrm{d}u}{\mathrm{d}X} =\frac{u-1}{1+u}, \qquad \frac{1+u}{1+u^2}\mathrm{d}u= | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 218 | 8606 | 微分方程 | 习题 | 求解方程 | 微分方程 | 短display待判定 | 8609:\frac{y}{\sqrt{1-y^2}}\mathrm{d}y =\frac{1}{3x^2}\mathrm{d}x. \| 8614:-\sqrt{1-y^2}=-\frac{1}{3x}+C, \| 8622:\frac{\mathrm{d}u}{\sqrt{1+u^2}}=\frac{\mathrm{d}x}{x}. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 219 | 8643 | 微分方程 | 习题 | 求解方程 | 微分方程 | 跳步关键词,短display待判定 | 直接; 8650:y+x\frac{\mathrm{d}x}{\mathrm{d}y} =\pm\sqrt{x^2+y^2}. \| 8657:\frac{\mathrm{d}(x^2+y^2)}{2\sqrt{x^2+y^2}} =\pm\mathrm{d}y, \qquad \mathrm{d}\left(\sqrt{x^2+y^2}\right)=\pm | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 220 | 8682 | 微分方程 | 习题 | 实际应用题 |  | 跳步关键词,短display待判定 | 于是; 8685:4=k\frac{10}{5}, \qquad k=2. \| 8691:\frac{\mathrm{d}v}{\mathrm{d}t}=\frac{2t}{v}, \qquad v\,\mathrm{d}v=2t\,\mathrm{d}t. \| 8697:\frac{1}{2}v^2=t^2+C, \qquad v^2=2t^2+C_1. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 221 | 8729 | 微分方程 | 习题 | 实际应用题 | 微分方程 | 跳步关键词,短display待判定 | 于是; 8732:\frac{\mathrm{d}P}{\mathrm{d}t}=\lambda P. \| 8736:\frac{\mathrm{d}A}{\mathrm{d}t} =\alpha\frac{\mathrm{d}P}{\mathrm{d}t} =\alpha\lambda P =\lambda A. \| 8745:A(t)=10^9\math | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 224 | 8806 | 微分方程 | 习题 | 实际应用题 |  | 短display待判定 | 8808:\frac{\mathrm{d}x}{\mathrm{d}t}=k(a-x)(b-x), \qquad x(0)=0. \| 8814:\frac{\mathrm{d}x}{(a-x)(b-x)}=k\,\mathrm{d}t. \| 8820:\frac{1}{(a-x)(b-x)} =\frac{1}{b-a}\left(\frac{1}{a-x} | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 225 | 8865 | 微分方程 | 习题 | 实际应用题 |  | 跳步关键词,短display待判定 | 于是; 8867:m\frac{\mathrm{d}v}{\mathrm{d}t}=mg-\mu v^2. \| 8871:v_T=\sqrt{\frac{mg}{\mu}}, \| 8875:\frac{\mathrm{d}v}{v_T^2-v^2} =\frac{g}{v_T^2}\,\mathrm{d}t. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 226 | 8899 | 微分方程 | 习题 | 求解曲线 |  | 跳步关键词,短display待判定 | 于是; 8903:d=\sqrt{x^2+(y-Y_0)^2} =\|x\|\sqrt{1+(y')^2}. \| 8908:x\sqrt{1+(y')^2}=2, \qquad y'=\pm\frac{\sqrt{4-x^2}}{x}. \| 8914:y=\pm\int \frac{\sqrt{4-x^2}}{x}\,\mathrm{d}x. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 227 | 8952 | 微分方程 | 习题 | 求解曲线 |  | 跳步关键词,短display待判定 | 整理得; 8957:x=\frac{X_A}{2} =\frac{x-y/y'}{2}. \| 8962:xy'=-y, \qquad \frac{\mathrm{d}y}{y}=-\frac{\mathrm{d}x}{x}. \| 8968:\ln\|y\|=-\ln\|x\|+C_1, \qquad xy=C. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 228 | 8982 | 微分方程 | 习题 | 求解曲线 |  | 短display待判定 | 8984:(x-a)^2+y^2=a^2, \qquad x^2+y^2=2ax. \| 8990:2x+2yy'=2a =\frac{x^2+y^2}{x}, \qquad y'=\frac{y^2-x^2}{2xy}. \| 8997:\frac{\mathrm{d}y}{\mathrm{d}x}=\frac{2xy}{x^2-y^2}. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 229 | 9026 | 微分方程 | 习题 | 落体问题 |  | 短display待判定 | 9029:m\frac{\mathrm{d}v}{\mathrm{d}t}=mg-kv. \| 9033:\frac{\mathrm{d}v}{\mathrm{d}t} =-\frac{k}{m}\left(v-\frac{mg}{k}\right). \| 9038:\frac{\mathrm{d}v}{v-\frac{mg}{k}} =-\frac{k}{m | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 230 | 9056 | 微分方程 | 习题 | 实际应用题 | 微分方程 | 跳步关键词,短display待判定 | 于是; 9063:\boxed{\theta(t)=15-\frac{10}{k}\bigl(1-\mathrm{e}^{kt}\bigr)}. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 231 | 9079 | 微分方程 | 习题 | 基础：直接套用公式或常数变易法 | 微分方程 | 跳步关键词,短display待判定 | 整理得; 9086:\mathrm{e}^{x}y'+\mathrm{e}^{x}y=1, \qquad (y\mathrm{e}^{x})'=1. \| 9092:y\mathrm{e}^{x}=x+C, \qquad y=(x+C)\mathrm{e}^{-x}. \| 9099:\boxed{y=(x+1)\mathrm{e}^{-x}}. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 232 | 9168 | 微分方程 | 习题 | 基础：伯努利方程 |  | 跳步关键词,短display待判定 | 可得,化简得,代入得,整理得; 9174:y^{-3}y'-\frac{1}{x}y^{-2}=x^2. \| 9178:z'=-2y^{-3}y', \qquad y^{-3}y'=-\frac{1}{2}z'. \| 9184:-\frac{1}{2}z'-\frac{1}{x}z=x^2, \qquad z'+\frac{2}{x}z=-2x^2. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 233 | 9292 | 微分方程 | 习题 | 提高：角色互换与全微分 | 微分方程 | 跳步关键词,短display待判定 | 直接; 9297:\frac{\mathrm{d}y}{\mathrm{d}x}(x\ln y-1)=y\ln y. \| 9301:x\ln y\,\mathrm{d}y-\mathrm{d}y =y\ln y\,\mathrm{d}x. \| 9308:x\ln y\,\mathrm{d}y-y\ln y\,\mathrm{d}x=\mathrm{d}y,  | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 234 | 9351 | 微分方程 | 习题 | 提高：三角变形与全微分 | 微分方程 | 跳步关键词,短display待判定 | 直接; 9371:\boxed{y=C\sec x-1}. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 235 | 9380 | 微分方程 | 习题 | 黎卡提方程 | 微分方程 | 跳步关键词,短display待判定 | 可得,整理得; 9385:-\left(\frac{1}{x}\right)^2-\frac{1}{x}\left(\frac{1}{x}\right)+\frac{1}{x^2} =-\frac{1}{x^2}. \| 9392:y=\frac{1}{x}+u(x), \qquad y'=-\frac{1}{x^2}+u'. \| 9398:-\frac{1} | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 236 | 9461 | 微分方程 | 习题 | 基本概念 | 微分方程 | 跳步关键词,短display待判定 | 可得; 9464:\frac{\mathrm{d}y}{\mathrm{d}x}+P(x)y=Q(x). \| 9469:y'+P(x)y=0 \| 9473:y_h=C\mathrm{e}^{-\int P(x)\mathrm{d}x}. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 237 | 9508 | 微分方程 | 习题 | 一阶线性微分方程求通解 | 微分方程 | 跳步关键词,短display待判定 | 略; 9516:\boxed{y=(x+C)\cos x}. \| 9527:\boxed{y=(x^2+C)\sin x}. \| 9541:\boxed{x=Cy^3+\frac{1}{2}y^2}. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 238 | 9569 | 微分方程 | 习题 | 一阶线性微分方程初值问题 |  | 短display待判定 | 9574:((x+1)y)'=2\mathrm{e}^{-x}. \| 9578:(x+1)y=-2\mathrm{e}^{-x}+C. \| 9582:\boxed{y=\frac{2\mathrm{e}^{-1}-2\mathrm{e}^{-x}}{x+1}}. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 239 | 9641 | 微分方程 | 习题 | 求曲线方程 | 微分方程 | 跳步关键词,短display待判定 | 代入得,于是; 9644:y'=2x+y, \qquad y'-y=2x. \| 9650:(y\mathrm{e}^{-x})'=2x\mathrm{e}^{-x}. \| 9654:y\mathrm{e}^{-x} =-2x\mathrm{e}^{-x}-2\mathrm{e}^{-x}+C, \qquad y=-2(x+1)+C\mathrm{e}^{x} | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 240 | 9670 | 微分方程 | 习题 | 应用题: 电路模型 | 微分方程 | 跳步关键词,短display待判定 | 可得; 9678:\mu(t)=\exp\!\left(\int5\,\mathrm{d}t\right)=\mathrm{e}^{5t}. \| 9682:(I\mathrm{e}^{5t})'=10\mathrm{e}^{5t}\sin5t. \| 9686:\int \mathrm{e}^{at}\sin(bt)\,\mathrm{d}t =\frac{\ | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 241 | 9717 | 微分方程 | 习题 | 溶液混合问题 | 微分方程 | 跳步关键词,短display待判定 | 代入得; 9725:\frac{\mathrm{d}y}{\mathrm{d}t}=10-\frac{3y}{50+2t}, \qquad y'+\frac{3}{50+2t}y=10. \| 9736:\boxed{ y(t)=100+4t-90\left(\frac{50}{50+2t}\right)^{3/2} }. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 242 | 9749 | 微分方程 | 习题 | 一阶线性微分方程初值问题 | 微分方程 | 跳步关键词,短display待判定 | 于是; 9752:z'+\frac{x}{1+x^2}z=x. \| 9759:z\sqrt{1+x^2} =\int x\sqrt{1+x^2}\,\mathrm{d}x =\frac{1}{3}(1+x^2)^{3/2}+C. \| 9767:\boxed{ y=\arctan\!\left[ \frac{1}{3}\left(1+x^2-\frac{1}{ | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 243 | 9779 | 微分方程 | 习题 | 求通解 | 微分方程,重积分/换元 | 短display待判定 | 9785:y' + \frac{1}{x}y = \frac{2\ln x}{x}y^2. \| 9791:z'-\frac{1}{x}z=-\frac{2\ln x}{x}. \| 9798:zx^{-1} =\int-\frac{2\ln x}{x^2}\,\mathrm{d}x =\frac{2\ln x}{x}+\frac{2}{x}+C. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 244 | 9838 | 微分方程 | 习题 | 积分方程求未知函数 | 微分方程,重积分/换元 | 跳步关键词,短display待判定 | 可得,于是; 9844:f'(x)=3f(x)+2\mathrm{e}^{2x}, \qquad f'(x)-3f(x)=2\mathrm{e}^{2x}. \| 9854:\boxed{f(x)=3\mathrm{e}^{3x}-2\mathrm{e}^{2x}}. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 245 | 9863 | 微分方程 | 习题 | 积分与变量无关 | 微分方程 | 跳步关键词,短display待判定 | 可得; 9866:I(x)=\int_0^1 f(x)\,\mathrm{d}t+\int_0^1 xf(xt)\,\mathrm{d}t =f(x)+\int_0^x f(u)\,\mathrm{d}u. \| 9876:I(x)=C\mathrm{e}^{-x}+\int_0^x C\mathrm{e}^{-u}\,\mathrm{d}u =C. \| 98 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 246 | 9898 | 微分方程 | 习题 | 缺 $y$ 型与缺 $x$ 型 | 微分方程 | 跳步关键词,短display待判定 | 于是; 9902:(1+x^2)p'+xp=1, \qquad p'+\frac{x}{1+x^2}p=\frac{1}{1+x^2}. \| 9908:\mu(x)=\exp\!\left(\int\frac{x}{1+x^2}\,\mathrm{d}x\right)=\sqrt{1+x^2}. \| 9912:(p\sqrt{1+x^2})'=\frac{1 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 247 | 9979 | 微分方程 | 习题 | 求通解 | 微分方程 | 跳步关键词,短display待判定 | 直接,于是; 9990:(\mathrm{e}^{-x}p)' = x\mathrm{e}^{-x}, \qquad \mathrm{e}^{-x}p = -x\mathrm{e}^{-x} - \mathrm{e}^{-x} + C_1. \| 9999:p'=1-p^2. \| 10003:\frac{\mathrm{d}p}{1-p^2}=\mathrm{ | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 248 | 10060 | 微分方程 | 习题 | 求初值问题 | 微分方程 | 跳步关键词,短display待判定 | 代入得,直接,于是; 10063:y^3p\frac{\mathrm{d}p}{\mathrm{d}y}=-1, \qquad p\,\mathrm{d}p=-y^{-3}\mathrm{d}y. \| 10069:\frac{1}{2}p^2=\frac{1}{2}y^{-2}+C_1. \| 10074:p^2=y^{-2}-1=\frac{1-y^2}{y | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 249 | 10196 | 微分方程 | 习题 | 二阶方程的初值问题 |  | 跳步关键词,短display待判定 | 于是; 10201:yy'=x-1 \implies y\,\mathrm{d}y=(x-1)\mathrm{d}x,\qquad \frac12y^2=\frac12x^2-x+C_2. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 250 | 10215 | 微分方程 | 习题 | 可降阶的一阶齐次型综合应用 | 微分方程 | 跳步关键词,短display待判定 | 代入得,于是; 10218:xu'+u=u\ln u, \qquad x\frac{\mathrm{d}u}{\mathrm{d}x}=u(\ln u-1). \| 10225:\boxed{y=\frac{\mathrm e}{2}x^2+C_2}. \| 10229:\frac{\mathrm{d}u}{u(\ln u-1)}=\frac{\mathrm{d | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 251 | 10253 | 微分方程 | 习题 | 缺 $x$ 型二阶方程求解 | 微分方程 | 短display待判定 | 10255:p\frac{\mathrm{d}p}{\mathrm{d}y}(1+y^2)=2yp^2. \| 10259:\frac{\mathrm{d}p}{p}=\frac{2y}{1+y^2}\mathrm{d}y. \| 10263:\ln\|p\|=\ln(1+y^2)+\ln\|C_1\|, \qquad p=C_1(1+y^2). | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 252 | 10285 | 微分方程 | 习题 | 建立运动微分方程：追击问题 | 微分方程,隐函数/偏导 | 跳步关键词,短display待判定 | 可得; 10291:y'=\frac{(1+vt)-y}{0-x} =\frac{y-1-vt}{x}. \| 10301:\frac{\mathrm{d}t}{\mathrm{d}x} =\frac{\mathrm{d}t}{\mathrm{d}s}\frac{\mathrm{d}s}{\mathrm{d}x} =\frac{1}{2v}\sqrt{1+(y | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 253 | 10328 | 微分方程 | 习题 | 积分方程求导转化法 |  | 跳步关键词,短display待判定 | 于是; 10332:\int_0^x \sqrt{1+(y')^2}\,\mathrm{d}t =\int_0^x y(t)\,\mathrm{d}t, \qquad \sqrt{1+(y')^2}=y. \| 10339:(y')^2=y^2-1, \qquad y'=\sqrt{y^2-1}, \qquad \frac{\mathrm{d}y}{\sqrt | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 254 | 10361 | 微分方程 | 习题 | 物理建模与微分方程的推导 | 微分方程 | 短display待判定 | 10365:T\cos\theta=H, \qquad T\sin\theta=\rho g s. \| 10373:y''=\frac{\rho g}{H}\sqrt{1+(y')^2}. \| 10377:\frac{\mathrm{d}p}{\mathrm{d}x}=a\sqrt{1+p^2}, \qquad \frac{\mathrm{d}p}{\sqr | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 255 | 10391 | 微分方程 | 习题 | 基于牛顿第二定律降阶求解 |  | 跳步关键词,短display待判定 | 代入得; 10397:\int v\,\mathrm{d}v=-GM\int r^{-2}\,\mathrm{d}r \implies \frac12v^2=\frac{GM}{r}+C. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 256 | 10411 | 微分方程 | 习题 | 变加速直线运动的积分 |  | 跳步关键词,短display待判定 | 于是; 10415:m\frac{\mathrm{d}v}{\mathrm{d}t}=-kv, \qquad 300\frac{\mathrm{d}v}{\mathrm{d}t}=-10gv. \| 10421:\frac{\mathrm{d}v}{v}=-\frac{g}{30}\mathrm{d}t, \qquad \ln v=-\frac{g}{30}t | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 257 | 10452 | 微分方程 | 习题 | 基础：验证与判定 | 微分方程 | 短display待判定 | 10458:y_1'' - 4y_1' + 4y_1 =4\mathrm{e}^{2x} - 8\mathrm{e}^{2x} + 4\mathrm{e}^{2x}=0. \| 10504:y'' - 2xy' + 4y=-4-2x(-4x)+4(1-2x^2)=0, \| 10511:y_2(x)=(1-2x^2)\int_{x_0}^x \frac{\mat | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 258 | 10541 | 微分方程 | 习题 | 基础：常数变易法 | 微分方程 | 跳步关键词,短display待判定 | 于是; 10563:y^{*}(x) =-y_{1}\int \frac{y_{2}f(x)}{W(x)}\,\mathrm{d}x +y_{2}\int \frac{y_{1}f(x)}{W(x)}\,\mathrm{d}x, \| 10569:y^* =\sin x\int \cos x\cot x\,\mathrm{d}x -\cos x\int \si | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 259 | 10680 | 微分方程 | 习题 | 提高：叠加原理的应用 | 微分方程 | 跳步关键词 | 直接 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 260 | 10704 | 微分方程 | 习题 | 刘维尔公式的推广 | 微分方程 | 跳步关键词,短display待判定 | 可得,同理,直接,于是; 10707:L[y]=y'''+p(x)y''+q(x)y'+r(x)y=0 \| 10720:y_1u'''+(3y_1'+py_1)u'' +(3y_1''+2py_1'+qy_1)u' +uL[y_1]=0. \| 10727:w''+\left(3\frac{y_1'}{y_1}+p(x)\right)w' +\left(3\f | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 262 | 10824 | 微分方程 | 习题 | 解的验证 | 微分方程 | 短display待判定 | 10827:y'=-2\sin x+3\cos x,\qquad y''=-2\cos x-3\sin x. \| 10831:y''+y=(-2\cos x-3\sin x)+(2\cos x+3\sin x)=0. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 263 | 10840 | 微分方程 | 习题 | 含参方程的求解 | 微分方程 | 短display待判定 | 10843:y'=-A\alpha\sin\alpha x, \qquad y''=-A\alpha^2\cos\alpha x. \| 10849:A(5-\alpha^2)\cos\alpha x=0. \| 10859:\boxed{\alpha=\pm\sqrt5,\qquad A=-\frac{3}{\sqrt5\sin\sqrt5}}. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 264 | 10871 | 微分方程 | 习题 | 边值问题求解 | 微分方程 | 跳步关键词,短display待判定 | 可得,同理; 10874:y''=-\omega^2(A\cos\omega x+B\sin\omega x)=-\omega^2y, \| 10882:A\cos\left(4\cdot\frac{\pi}{8}\right) +B\sin\left(4\cdot\frac{\pi}{8}\right)=3, \| 10890:\boxed{(\omega,A | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 265 | 10898 | 微分方程 | 习题 | 线性算子的计算 |  | 短display待判定 | 10903:L[\cos\sqrt{3}x] =-3\cos\sqrt{3}x-3x(-\sqrt{3}\sin\sqrt{3}x)+3\cos\sqrt{3}x =3\sqrt{3}x\sin\sqrt{3}x. \| 10909:L[x^2+3x]=2-3x(2x+3)+3(x^2+3x)=2-3x^2. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 267 | 10932 | 微分方程 | 习题 | 非齐次叠加原理与猜测法 | 微分方程 | 短display待判定 | 10951:\boxed{y=y_h+y^*=C_1\sin x+C_2\cos x+\frac32\mathrm{e}^{-x}+2x}. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 268 | 10960 | 微分方程 | 习题 | 解的验证与通解构造 | 微分方程 | 短display待判定 | 10962:y_1'=2x\mathrm{e}^{x^2}, \qquad y_1''=(2+4x^2)\mathrm{e}^{x^2}. \| 10968:(2+4x^2)\mathrm{e}^{x^2} -4x(2x\mathrm{e}^{x^2}) +(4x^2-2)\mathrm{e}^{x^2}=0. \| 10976:y_2'=(1+2x^2)\ma | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 269 | 11002 | 微分方程 | 习题 | 积分算子的线性性证明 |  | 短display待判定 | 11004:T[Cy]=\int_a^x t^2(Cy(t))\,\mathrm{d}t =C\int_a^x t^2y(t)\,\mathrm{d}t =CT[y]. \| 11010:T[y_1+y_2] =\int_a^x t^2\bigl(y_1(t)+y_2(t)\bigr)\,\mathrm{d}t \| 11014:=\int_a^x t^2y_1 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 270 | 11030 | 微分方程 | 习题 | 物理建模：LRC电路微分方程 |  | 短display待判定 | 11043:\boxed{\frac{\mathrm{d}^2V_C}{\mathrm{d}t^2} + \frac{R}{L}\frac{\mathrm{d}V_C}{\mathrm{d}t} + \frac{1}{LC}V_C = \frac{E_m}{LC}\sin\omega t}. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 271 | 11055 | 微分方程 | 习题 | 物理建模：弹簧振子动力学 | 微分方程 | 跳步关键词,短display待判定 | 于是; 11063:my''+ky=0, \qquad y''+\frac{k}{m}y=0. \| 11071:y(t)=C_1\cos\left(\sqrt{\frac{k}{m}}t\right) +C_2\sin\left(\sqrt{\frac{k}{m}}t\right). \| 11080:y'(t)=-C_1\sqrt{\frac{k}{m}}\ | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 272 | 11096 | 微分方程 | 习题 | 根据基础解系反求微分方程 | 微分方程 | 跳步关键词 | 可得,容易,于是 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 273 | 11115 | 微分方程 | 习题 | 刘维尔公式应用 | 微分方程 | 跳步关键词,短display待判定 | 计算得,直接,略,于是; 11117:y''+P(x)y'+Q(x)y=0, \qquad P(x)=-\frac{2x+1}{2x-1}. \| 11123:\exp\left(-\int P(x)\,\mathrm{d}x\right) =\mathrm{e}^x(2x-1) \| 11128:y_2=y_1\int \frac{\exp\left(-\in | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 274 | 11146 | 微分方程 | 习题 | 常数变易法的综合应用 | 微分方程 | 短display待判定 | 11151:y''-\frac{2}{x}y'+\frac{2}{x^2}y=0, \qquad P(x)=-\frac{2}{x}. \| 11157:\exp\left(-\int P(x)\mathrm{d}x\right) =\exp\left(\int\frac{2}{x}\mathrm{d}x\right)=x^2, \| 11165:y''-\fr | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 275 | 11191 | 微分方程 | 习题 | 基本概念 | 微分方程 | 短display待判定 | 11195:(\lambda^2+p\lambda+q)\mathrm{e}^{\lambda x}=0. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 276 | 11217 | 微分方程 | 习题 | 齐次方程通解 | 微分方程 | 短display待判定 | 11234:\boxed{y = C_1\mathrm{e}^x + C_2\mathrm{e}^{-x} + C_3\cos x + C_4\sin x}. \| 11240:(-1)^3 - 6(-1)^2 + 3(-1) + 10 = -1 - 6 - 3 + 10 = 0, \| 11245:(\lambda^3 - 6\lambda^2 + 3\lam | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 277 | 11262 | 微分方程 | 习题 | 齐次方程初值问题 | 微分方程 | 短display待判定 | 11267:\lambda^2+4\lambda+29=0 \implies \lambda=\frac{-4\pm\sqrt{16-116}}{2}=-2\pm5i. \| 11275:y'(0)=15\implies C_2(0+5\cos0)=5C_2=15 \implies C_2=3. \| 11285:4\lambda^2+4\lambda+1=0  | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 278 | 11346 | 微分方程 | 习题 | 非齐次方程通解 | 微分方程 | 跳步关键词,短display待判定 | 代入得,于是; 11349:\lambda^2+\lambda-2=0 \implies(\lambda-1)(\lambda+2)=0 \implies \lambda_1=1,\ \lambda_2=-2. \| 11377:[-2A\sin x + 2B\cos x - x(A\cos x + B\sin x)] + x(A\cos x + B\sin  | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 279 | 11494 | 微分方程 | 习题 | 非齐次方程初值问题 | 微分方程 | 跳步关键词,短display待判定 | 代入得; 11499:(y^*)''+y^*=-4A\sin2x+A\sin2x=-3A\sin2x=-\sin2x, \| 11506:y(\pi)=C_1\cos\pi+C_2\sin\pi+\frac13\sin2\pi=-C_1=1, \| 11513:y'(\pi)=-C_1\sin\pi+C_2\cos\pi+\frac23\cos2\pi =-C_ | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 280 | 11574 | 微分方程 | 习题 | 含参方程的通解 | 微分方程 | 跳步关键词,短display待判定 | 代入得; 11580:A\alpha^2\mathrm{e}^{\alpha x}+4A\alpha\mathrm{e}^{\alpha x} +4A\mathrm{e}^{\alpha x} =\mathrm{e}^{\alpha x} \implies A(\alpha+2)^2=1. \| 11606:(y^*)''+a^2y^*=-A\sin x+a^ | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 281 | 11640 | 微分方程 | 习题 | Euler方程求解 | 微分方程,隐函数/偏导 | 跳步关键词,短display待判定 | 代入得,于是; 11643:x y' = D_t y,\qquad x^2 y'' = D_t(D_t-1)y = D_t^2 y - D_t y,\qquad x^3 y''' = D_t(D_t-1)(D_t-2)y. \| 11651:(D_t^2-D_t)y-D_t y+y=0 \implies y_{tt}''-2y_t'+y=0. \| 11668: | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 282 | 11736 | 微分方程 | 习题 | Euler方程初值问题 | 微分方程 | 跳步关键词,短display待判定 | 于是; 11741:(y_{tt}''-y_t')-y_t'+y=2\mathrm{e}^t \implies y_{tt}''-2y_t'+y=2\mathrm{e}^t. \| 11749:(y^*)''-2(y^*)'+y^* =A(t^2+4t+2-2t^2-4t+t^2)\mathrm{e}^t =2A\mathrm{e}^t=2\mathrm{e} | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 283 | 11777 | 微分方程 | 习题 | 无阻尼自由振动物理建模 | 微分方程 | 跳步关键词,短display待判定 | 整理得; 11795:y'(t) =-C_1\sqrt{\frac{g}{a}}\sin\left(\sqrt{\frac{g}{a}}t\right) +C_2\sqrt{\frac{g}{a}}\cos\left(\sqrt{\frac{g}{a}}t\right). | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 284 | 11810 | 微分方程 | 习题 | 阻尼自由振动物理建模 | 微分方程 | 短display待判定 | 11816:mx''=-kx-\mu x' \implies mx''+\mu x'+kx=0. \| 11835:\boxed{x(t) = \mathrm{e}^{-\frac{\mu}{2m}t} (C_1\cos\omega_d t + C_2\sin\omega_d t)}. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 285 | 11849 | 微分方程 | 习题 | 利用切线条件的非齐次方程初值问题 | 微分方程 | 短display待判定 | 11862:A(x+2)\mathrm{e}^x - 3A(x+1)\mathrm{e}^x + 2Ax\mathrm{e}^x = -A\mathrm{e}^x = 2\mathrm{e}^x. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 286 | 11882 | 微分方程 | 习题 | 变加速力学建模：链条滑落 | 微分方程 | 跳步关键词,短display待判定 | 化简得,代入得,直接; 11890:Mx''=F_{net}\implies 18\rho x''=\rho g(2x-18) \implies x''-\frac{g}{9}x=-g. \| 11904:x(0)=C_1\cosh0+C_2\sinh0+9=C_1+9=10 \implies C_1=1. \| 11915:\omega t=\operator | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 287 | 11926 | 微分方程 | 习题 | 平衡位置的改变及振动建模 | 微分方程 | 跳步关键词,短display待判定 | 直接; 11935:4mx''=-kx \implies 4mx''+\frac{mg}{a}x=0 \implies x''+\frac{g}{4a}x=0. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 288 | 11959 | 微分方程 | 习题 | 一阶速度模型的降阶求解 | 微分方程 | 跳步关键词,短display待判定 | 于是; 11976:x(t)=\int_0^t v(\tau)\mathrm{d}\tau =\int_0^t \left[ \frac{mg'}{k} - \frac{mg'}{k}\mathrm{e}^{-\frac{k}{m}\tau} \right] \mathrm{d}\tau, \| 11981:\boxed{x(t)=\frac{mg'}{k}t | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 289 | 11990 | 微分方程 | 习题 | 频率计算（保留重力加速度符号 $g$） |  | 跳步关键词,短display待判定 | 可得; 11998:mx''+kx=0\implies 2x''+gx=0 \implies x''+\frac{g}{2}x=0. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 290 | 12011 | 微分方程 | 习题 | 共振与受迫振动建模（保留符号 $g$） | 微分方程 | 跳步关键词,短display待判定 | 代入得; 12018:my''=-k(y-y_0)\implies 4y''=-4g(y-2\sin30t) \implies y''+gy=2g\sin30t. \| 12029:\boxed{y(t)=\frac{1}{g-900}\left(2g\sin30t-60\sqrt g\,\sin(\sqrt g\,t)\right)} \quad(g\neq | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 291 | 12049 | 微分方程 | 习题 | 积分微分方程转化为常系数方程 | 微分方程 | 跳步关键词,短display待判定 | 代入得,直接; 12054:f''(x)=6\sin^2 x-f(x),\qquad f''(x)+f(x)=6\sin^2 x=3(1-\cos 2x)=3-3\cos 2x. \| 12065:-4B\cos2x+B\cos2x=-3B\cos2x=-3\cos2x \implies B=1. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 293 | 12119 | 微分方程 | 习题 | 基础：消元法练习 | 微分方程 | 跳步关键词,短display待判定 | 整理得; 12125:\frac12x''-\frac12x' =4x+3\left(\frac12x'-\frac12x\right) =\frac52x+\frac32x'. \| 12133:y=\frac{1}{2}(5C_1\mathrm{e}^{5t}-C_2\mathrm{e}^{-t}) -\frac{1}{2}(C_1\mathrm{e}^{ | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 294 | 12215 | 微分方程 | 习题 | 提高：非齐次方程组 | 微分方程 | 跳步关键词,短display待判定 | 整理得; 12221:(2\mathrm{e}^{2t}-x''+2x')+x-2(\mathrm{e}^{2t}-x'+2x) =\mathrm{e}^{3t} \implies x''-4x'+3x=-\mathrm{e}^{3t}. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 295 | 12251 | 微分方程 | 习题 | 解微分方程组综合 | 微分方程 | 跳步关键词,短display待判定 | 可得,整理得; 12277:\frac15(x'-x'')=2x-\frac15(x-x') \implies -x''=9x \implies x''+9x=0. \| 12284:y=\frac15\left[ C_1\cos3t+C_2\sin3t-(-3C_1\sin3t+3C_2\cos3t) \right]. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 296 | 12298 | 微分方程 | 习题 | 微分方程组物理建模：炮弹受阻运动 | 微分方程 | 短display待判定 | 12321:y'(0)=v_0\sin\alpha \implies C_3-\frac{mg}{k}=v_0\sin\alpha \implies C_3=v_0\sin\alpha+\frac{mg}{k}. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 297 | 12346 | 微分方程 | 习题 | 有心力场中的粒子轨迹 | 微分方程 | 短display待判定 | 12353:mx''=-kx,\qquad my''=-ky \Longrightarrow x''+\omega^2x=0,\quad y''+\omega^2y=0. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 298 | 12387 | 微分方程 | 习题 | 基本概念与方程求解 | 微分方程 | 跳步关键词,短display待判定 | 代入得,显然,直接; 12401:(\lambda-1)^2=0 \implies \lambda^2-2\lambda+1=0 \implies y''-2y'+y=0. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 299 | 12470 | 微分方程 | 习题 | 微分方程概念辨析 | 微分方程 | 跳步关键词,短display待判定 | 直接; 12481:\frac{y-\ln x}{x}+\frac{\mathrm{d}y}{\mathrm{d}x}=0 \implies \frac{\mathrm{d}y}{\mathrm{d}x}+\frac{1}{x}y=\frac{\ln x}{x}. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 300 | 12513 | 微分方程 | 习题 | 人口增长模型 | 微分方程 | 短display待判定 | 12519:\frac{\mathrm{d}P}{P}=0.02\,\mathrm{d}t \implies \ln P=0.02t+C \implies P(t)=C_1e^{0.02t}; | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 301 | 12537 | 微分方程 | 习题 | 一阶线性微分方程解的结构 | 微分方程 | 短display待判定 | 12546:u(x) = C_1 e^{-\int P(x)\mathrm{d}x},\qquad v(x) = C_2 e^{-\int P(x)\mathrm{d}x}. \| 12554:\frac{y_3 - y_1}{y_2 - y_1} = \frac{v(x)}{u(x)} = \frac{C_2 e^{-\int P(x)\mathrm{d}x | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 302 | 12567 | 微分方程 | 习题 | Logistic 模型应用 | 微分方程 | 跳步关键词 | 化简得,直接 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 303 | 12602 | 微分方程 | 习题 | 微分方程的几何应用 | 微分方程,重积分/换元 | 短display待判定 | 12606:S = \frac{1}{2} \int_0^\theta r^2(\phi)\,\mathrm{d}\phi,\qquad s = \int_0^\theta \sqrt{r^2(\phi) + [r'(\phi)]^2}\,\mathrm{d}\phi. \| 12613:\frac{1}{2} \int_0^\theta r^2(\phi)\ | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 304 | 12655 | 微分方程 | 习题 | 微分方程在物理化学中的应用 | 微分方程 | 短display待判定 | 12660:-\frac{\mathrm{d}r}{\mathrm{d}t} =\alpha S=\alpha(4\pi r^2)=Kr^2 \qquad(\text{令 } K=4\pi\alpha>0). \| 12674:\frac{1}{0.19}=2K+4 \implies \frac{100}{19}=2K+4 \implies K=\frac{1 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 305 | 12695 | 微分方程 | 习题 | 动力学与微分方程 | 微分方程 | 短display待判定 | 12705:\frac{\mathrm{d}v}{\mathrm{d}t} =g-\frac{k}{m}v^2 =\frac{k}{m}\left(\frac{mg}{k}-v^2\right) =\frac{k}{m}(a^2-v^2). \| 12730:x(t)=\int_0^t \sqrt{\frac{mg}{k}} \tanh\left(\sqrt{ | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 306 | 12742 | 微分方程 | 习题 | 常系数线性非齐次方程的特解与通解 | 微分方程 | 跳步关键词,短display待判定 | 可得; 12758:y'=2e^{2x}+e^x+(1+x)e^x=2e^{2x}+(2+x)e^x, \| 12761:y''=4e^{2x}+e^x+(2+x)e^x=4e^{2x}+(3+x)e^x. \| 12765:y''-3y'+2y =[4e^{2x}+(3+x)e^x]-3[2e^{2x}+(2+x)e^x] +2[e^{2x}+(1+x)e^x | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 308 | 12808 | 微分方程 | 习题 | 自变量与因变量互换求解 | 微分方程 | 跳步关键词,短display待判定 | 直接; 12815:y''=\frac{\mathrm{d}}{\mathrm{d}x}(y') =\frac{\mathrm{d}}{\mathrm{d}y}\left(\frac{1}{x'}\right) \cdot\frac{\mathrm{d}y}{\mathrm{d}x} =-\frac{x''}{(x')^2}\cdot\f \| 12836:A | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 309 | 12858 | 微分方程 | 习题 | 一阶线性方程与积分不等式 | 微分方程 | 短display待判定 | 12863:y'e^{ax}+aye^{ax}=f(x)e^{ax} \implies \frac{\mathrm{d}}{\mathrm{d}x}(ye^{ax})=f(x)e^{ax}. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 310 | 12892 | 微分方程 | 习题 | 微分不等式比较定理 |  | 跳步关键词,短display待判定 | 于是; 12898:w'(x)=u_1'(x)-u_2'(x) \ge [a(x)u_1(x)+v(x)]-[a(x)u_2(x)+v(x)] =a(x)[u_1(x)-u_2(x)], \| 12912:H(x)\ge H(0)=w(0)e^0=0 \implies w(x)e^{-\int_0^x a(t)\mathrm{d}t}\ge0. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 311 | 12924 | 微分方程 | 习题 | 二阶微分方程解的单调性分析 |  | 跳步关键词,短display待判定 | 于是; 12929:E'(x)=\frac{\mathrm{d}}{\mathrm{d}x}[y(x)y'(x)] =[y'(x)]^2+y(x)y''(x) =[y'(x)]^2+a(x)[y(x)]^2. \| 12938:E(0)=y(0)y'(0)=y_0y_0'>0 \qquad(\text{因 } y_0>0,\ y_0'>0). | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 312 | 12962 | 微分方程 | 习题 | 由函数方程导出微分方程 | 微分方程 | 跳步关键词,短display待判定 | 直接,于是; 12970:f(x+h)-f(x) =\frac{f(h)\,[1+f^2(x)]}{1-f(x)f(h)}. \| 12975:f'(x)=\lim_{h\to0}\frac{f(x+h)-f(x)}{h} =[1+f^2(x)]\lim_{h\to0}\frac{f(h)}{h}. \| 12980:\boxed{f'(x)=k[1+f^2(x | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 313 | 12999 | 微分方程 | 习题 | 积微分方程求解 | 微分方程 | 跳步关键词,短display待判定 | 同理; 13014:r=\frac{1\pm\sqrt{(-1)^2-4(1)(-1)}}{2} =\frac{1\pm\sqrt5}{2}. \| 13025:C_1r_1+(1-C_1)r_2=1 \implies C_1(r_1-r_2)=1-r_2 \implies C_1=\frac{1-r_2}{r_1-r_2}. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 314 | 13043 | 微分方程 | 习题 | 变上限积分方程求解 | 微分方程 | 跳步关键词,短display待判定 | 直接,整理得; 13051:\left(f(x)\mathrm{e}^{-\frac{x^2}{2n}}\right)'=0, \| 13062:\boxed{f(x)=\frac{1}{n}\mathrm{e}^{\frac{x^2}{2n}}}. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 315 | 13073 | 微分方程 | 习题 | 含卷积的积分方程求解 | 微分方程 | 跳步关键词,短display待判定 | 化简得; 13083:f'(x)=\cos x-\left(\int_0^x f(t)\mathrm{d}t+xf(x)\right)+xf(x) =\cos x-\int_0^x f(t)\mathrm{d}t. \| 13103:(f^*)''=-x(A\cos x+B\sin x)-2A\sin x+2B\cos x, \| 13107:-2A\sin x | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 316 | 13283 | 多元函数微分学 | 知识讲解 | 开球是区域 |  | 短display待判定 | 13286:\\|x-a\\|\leqslant \\|x-p\\|+\\|p-a\\|<\varepsilon+\\|p-a\\|=r. \| 13293:\\|\Phi(t)-a\\| =\\|(1-t)(p-a)+t(q-a)\\| \leqslant (1-t)\\|p-a\\|+t\\|q-a\\|<r. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 317 | 13313 | 多元函数微分学 | 知识讲解 | 开但不连通的集合 |  | 跳步关键词 | 于是 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 318 | 13341 | 多元函数微分学 | 知识讲解 | 求二元函数的定义域 | 曲面积分/通量 | 跳步关键词,短display待判定 | 可得; 13344:D_1=\{(x,y)\mid x\geqslant 0,\;y\geqslant 0\} \cup\{(x,y)\mid x\leqslant 0,\;y\leqslant 0\}. \| 13353:x^2-2x+y^2\leqslant0 \Longleftrightarrow (x-1)^2+y^2\leqslant1. \| 133 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 319 | 13431 | 多元函数微分学 | 知识讲解 | 极坐标下的判零 |  | 跳步关键词,短display待判定 | 于是; 13433:f(r\cos\theta,r\sin\theta) =\frac{r^2\cos\theta\sin\theta}{r} =r\cos\theta\sin\theta. \| 13439:\|f(r\cos\theta,r\sin\theta)\|\leqslant \frac12r\to0. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 320 | 13474 | 多元函数微分学 | 知识讲解 | 角度不同导致极限不同 | 重积分/换元 | 短display待判定 | 13479:f(r\cos\theta,r\sin\theta) =\frac{r^2\cos\theta\sin\theta} {r^2(\cos^2\theta+\sin^2\theta)} =\frac12\sin(2\theta). \| 13496:\boxed{\displaystyle\lim_{(x,y)\to(0,0)}\frac{xy}{x | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 321 | 13505 | 多元函数微分学 | 知识讲解 | 角度随半径变化的情形 | 重积分/换元 | 跳步关键词,短display待判定 | 可得,直接; 13507:f(x,kx^2) =\frac{2x^2\cdot kx^2}{x^4+k^2x^4} =\frac{2k}{1+k^2}\qquad(x\neq0). \| 13513:\boxed{\displaystyle\lim_{(x,y)\to(0,0)}\frac{2x^2y}{x^4+y^2}\text{ 不存在}}. \| 1351 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 322 | 13560 | 多元函数微分学 | 知识讲解 | 二重极限存在但累次极限不全存在 |  | 短display待判定 | 13563:f(r\cos\theta,r\sin\theta) =r\sin\theta\sin\frac{1}{r\cos\theta}. \| 13568:\|f(r\cos\theta,r\sin\theta)\|\leqslant r\|\sin\theta\|\leqslant r\to0. \| 13576:\lim_{y\to0}\lim_{x\to0} | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 323 | 13594 | 多元函数微分学 | 知识讲解 | 含三角函数的极限 |  | 短display待判定 | 13596:\left\|\frac{\sin(x^3+y^3)}{x^2+y^2}\right\| =\left\|\frac{\sin\bigl(r^3(\cos^3\theta+\sin^3\theta)\bigr)}{r^2}\right\|. \| 13601:\left\|\frac{\sin\bigl(r^3(\cos^3\theta+\sin^3\the | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 324 | 13623 | 多元函数微分学 | 知识讲解 | 含分段定义的极限 |  | 短display待判定 | 13625:\|f(x,y)\|=\left\|\frac{\sin(xy)}{x}\right\| \leqslant \frac{\|xy\|}{\|x\|} =\|y\|=r\|\sin\theta\|\leqslant r. \| 13631:\boxed{\displaystyle\lim_{(x,y)\to(0,0)}f(x,y)=0}. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 325 | 13641 | 多元函数微分学 | 知识讲解 | 幂指型极限 | 重积分/换元 | 短display待判定 | 13644:(x^2+y^2)^{xy}=e^{\,xy\ln(x^2+y^2)}. \| 13650:xy\ln(x^2+y^2) =r^2\cos\theta\sin\theta\ln r^2. \| 13655:\bigl\|r^2\cos\theta\sin\theta\ln r^2\bigr\| \leqslant \frac12 r^2\|\ln r^2\| | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 326 | 13670 | 多元函数微分学 | 知识讲解 | 含小角三角函数的极限 |  | 短display待判定 | 13672:\left\|\frac{\sin(x^2y)}{x^2+y^2}\right\| =\left\|\frac{\sin\bigl(r^3\cos^2\theta\sin\theta\bigr)}{r^2}\right\| \leqslant r\|\cos^2\theta\sin\theta\| \leqslant r\to0. \| 13679:\boxe | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 327 | 13727 | 多元函数微分学 | 知识讲解 | 可去间断点 |  | 短display待判定 | 13731:f(r\cos\theta,r\sin\theta) =\frac{r^4\cos^2\theta\sin^2\theta}{r^2} =r^2\cos^2\theta\sin^2\theta. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 329 | 13768 | 多元函数微分学 | 知识讲解 | 边缘连续但不整体连续 |  | 跳步关键词,短display待判定 | 同理; 13771:\frac{xy}{x^2+y^2}=\cos\theta\sin\theta=\frac12\sin2\theta, | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 330 | 13886 | 多元函数微分学 | 知识讲解 | 方向导数的直接计算 | 隐函数/偏导 | 短display待判定 | 13890:u(t)=f\!\left(1+\frac{\sqrt2}{2}t,\;1+\frac{\sqrt2}{2}t\right) =\left(1+\frac{\sqrt2}{2}t\right)^{2}. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 331 | 13917 | 多元函数微分学 | 知识讲解 | 在某点处求偏导数值 | 隐函数/偏导 | 跳步关键词,短display待判定 | 于是; 13921:\varphi'(x)=-\frac{4}{(1+x)^2} \Longrightarrow f_x(3,2)=\varphi'(3)=-\frac14, \| 13926:\psi'(y)=\frac{2y}{4}=\frac{y}{2} \Longrightarrow f_y(3,2)=\psi'(2)=1. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 332 | 13936 | 多元函数微分学 | 知识讲解 | 求偏导函数（解析表达式） | 隐函数/偏导 | 跳步关键词,短display待判定 | 同理; 13941:\frac{\partial z}{\partial x} =\frac{1}{1+(y/x)^2}\cdot\left(\frac{y}{x}\right)'_{\!x} =\frac{x^2}{x^2+y^2}\cdot\left(-\frac{y}{x^2}\right) =\boxed{-\frac{y}{x^ \| 13949:\ | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 333 | 13965 | 多元函数微分学 | 知识讲解 | 复合函数的偏导数 | 隐函数/偏导 | 短display待判定 | 13974:f_x=5u^4u_x=5(3xy+2x)^4(3y+2), \qquad f_y=5u^4u_y=15x(3xy+2x)^4. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 334 | 14003 | 多元函数微分学 | 知识讲解 | 仅在某些方向存在方向导数 | 隐函数/偏导 | 短display待判定 | 14007:u(t)=f(t\cos\theta,t\sin\theta)=\sin 2\theta\quad(t\neq0), \qquad u(0)=f(0,0)=1. \| 14014:u'(0)=\lim_{t\to0}\frac{u(t)-u(0)}{t} =\lim_{t\to0}\frac{\sin2\theta-1}{t}. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 335 | 14120 | 多元函数微分学 | 知识讲解 | 范数函数的梯度 | 曲面积分/通量,隐函数/偏导 | 跳步关键词,短display待判定 | 同理; 14128:\frac{\partial f}{\partial x} =\frac{1}{2}(x^2+y^2+z^2)^{-1/2}\cdot 2x =\frac{x}{\sqrt{x^2+y^2+z^2}} =\frac{x}{\\|p\\|}. \| 14138:\boxed{\nabla f(p)=\frac{1}{\\|p\\|}(x,y,z)=\ | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 336 | 14173 | 多元函数微分学 | 知识讲解 | 沿特定方向的方向导数 | 隐函数/偏导 | 跳步关键词,短display待判定 | 可得; 14176:\frac{\partial z}{\partial x} =e^{xy}+xy\cdot e^{xy} =e^{xy}(1+xy),\qquad \frac{\partial z}{\partial y} =x\cdot e^{xy}\cdot x =x^2e^{xy}. \| 14195:\frac{\partial z}{\parti | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 337 | 14208 | 多元函数微分学 | 知识讲解 | 给定角度 | 隐函数/偏导 | 跳步关键词,短display待判定 | 于是; 14213:\left.\nabla u\right\|_{(1,1)} =\left(\frac{2}{2},\,\frac{2}{2}\right) =(1,\,1),\qquad \vec l=(\cos 60^\circ,\;\sin 60^\circ) =\left(\frac12,\;\frac{\sqrt3}{2}\r \| 14221:\ | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 338 | 14257 | 多元函数微分学 | 知识讲解 | 梯度为零的方向导数 | 隐函数/偏导 | 短display待判定 | 14268:\dfrac{\partial f}{\partial\vec l}(1,1) =(e,e)\cdot\left(\dfrac{\sqrt2}{2},-\dfrac{\sqrt2}{2}\right) =\dfrac{\sqrt2}{2}e-\dfrac{\sqrt2}{2}e=\boxed{0}. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 339 | 14302 | 多元函数微分学 | 知识讲解 | 证明某函数在原点可微 | 隐函数/偏导 | 短display待判定 | 14320:\lim_{(h_1,h_2)\to(0,0)} \frac{f(h_1,h_2) - f(0,0) - (f_x(0,0)h_1 + f_y(0,0)h_2)}{\sqrt{h_1^2+h_2^2}} = 0. \| 14335:\|R(h_1,h_2)\| =\left\|\rho\sin\frac{1}{\rho^2}\right\| \leqsla | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 340 | 14389 | 多元函数微分学 | 知识讲解 | 偏导存在但不可微 | 隐函数/偏导 | 跳步关键词,短display待判定 | 直接,略; 14393:f_x(0,0)=\lim_{x\to 0}\frac{f(x,0)-f(0,0)}{x}=0,\qquad f_y(0,0)=\lim_{y\to 0}\frac{f(0,y)-f(0,0)}{y}=0. \| 14407:\lim_{h_1\to 0^+} \frac{h_1^2}{(2h_1^2)^{\frac32}} =\lim | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 341 | 14433 | 多元函数微分学 | 知识讲解 | 可微但偏导数不连续 | 隐函数/偏导 | 跳步关键词,短display待判定 | 同理; 14437:f_x(0,0)=\lim_{t\to 0}\frac{f(t,0)-0}{t} =\lim_{t\to 0}t\sin\frac{1}{t^2}=0,\qquad f_y(0,0)=\lim_{t\to 0}\frac{f(0,t)-0}{t}=0. \| 14452:f_x(x,0) =2x\sin\frac{1}{x^2}-\frac | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 342 | 14484 | 多元函数微分学 | 知识讲解 | 多项式的全微分 | 隐函数/偏导 | 高风险题解过短 |  | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 343 | 14494 | 多元函数微分学 | 知识讲解 | 混合型函数的全微分 | 隐函数/偏导 | 高风险题解过短 |  | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 344 | 14504 | 多元函数微分学 | 知识讲解 | 利用全微分做近似计算 | 隐函数/偏导 | 跳步关键词,短display待判定 | 可得,容易; 14517:f(x_0+h_1,\,y_0+h_2) \approx f(x_0,y_0)+f_x(x_0,y_0)\,h_1+f_y(x_0,y_0)\,h_2 \| 14522:(1.03)^{1.98} \approx 1+2\times 0.03+0\times(-0.02) =1+0.06=\boxed{1.06}. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 345 | 14862 | 多元函数微分学 | 知识讲解 | 螺旋线的速度向量 |  | 短display待判定 | 14866:f'(t)=(-\sin t,\;\cos t,\;1)^{\mathsf T} =-\vec i\sin t+\vec j\cos t+\vec k. \| 14876:\\|f'(t)\\|=\sqrt{(-\sin t)^2+(\cos t)^2+1^2} =\sqrt{2}. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 346 | 14894 | 多元函数微分学 | 知识讲解 | Jacobian 矩阵的完整计算 | 隐函数/偏导 | 跳步关键词,短display待判定 | 直接; 14922:f\!\left(\tfrac12+h_1,\,1+h_2,\,\pi+h_3\right) \approx f\!\left(\tfrac12,1,\pi\right) +Jf\!\left(\tfrac12,1,\pi\right)\boldsymbol h. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 347 | 15077 | 多元函数微分学 | 知识讲解 | 一元复合：中间变量含 $t$ |  | 跳步关键词,短display待判定 | 直接; 15101:\frac{\mathrm{d}z}{\mathrm{d}t} =z_xx_t+z_yy_t =y\cos x\cdot 3t^2+\sin x\cdot 5. \| 15107:\frac{\mathrm{d}z}{\mathrm{d}t} =\boxed{3t^2(5t+2)\cos(t^3)+5\sin(t^3)}. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 348 | 15116 | 多元函数微分学 | 知识讲解 | 二元复合：中间变量含 $u,v$ | 隐函数/偏导 | 跳步关键词 | 直接 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 349 | 15185 | 多元函数微分学 | 知识讲解 | 抽象复合函数的偏导数 | 隐函数/偏导 | 跳步关键词 | 直接 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 350 | 15266 | 多元函数微分学 | 知识讲解 | 利用全微分形式不变性求偏导 | 隐函数/偏导 | 跳步关键词,短display待判定 | 可得; 15271:\mathrm{d}u=2\,\mathrm{d}x+\mathrm{d}y, \qquad \mathrm{d}z=\cos u\,\mathrm{d}u. \| 15277:\mathrm{d}z =2\cos(2x+y)\,\mathrm{d}x +\cos(2x+y)\,\mathrm{d}y. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 351 | 15293 | 多元函数微分学 | 知识讲解 | 三元函数的全微分求偏导 |  | 跳步关键词 | 直接 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 352 | 15503 | 多元函数微分学 | 知识讲解 | 混合偏导数不相等 | 隐函数/偏导 | 跳步关键词,短display待判定 | 同理,直接; 15507:f_x(0,0)=0,\qquad f_y(0,0)=0. \| 15514:f_x(0,y)=\lim_{h\to 0}\frac{f(h,y)-f(0,y)}{h} =\lim_{h\to 0}y\cdot\frac{h^2-y^2}{h^2+y^2} =-y. \| 15523:f_y(x,0)=\lim_{k\to 0}\fra | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 353 | 15559 | 多元函数微分学 | 知识讲解 | 二阶偏导数的完整计算 | 隐函数/偏导 | 短display待判定 | 15561:z=F(u,v),\qquad u=x,\qquad v=y,\qquad F(u,v)=v\cos u+3u^2e^v. \| 15620:\boxed{ f_{xx}=-y\cos x+6e^y,\quad f_{xy}=f_{yx}=-\sin x+6xe^y,\quad f_{yy}=3x^2e^y }. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 354 | 15632 | 多元函数微分学 | 知识讲解 | arctan 的二阶偏导数 | 隐函数/偏导 | 跳步关键词,短display待判定 | 可得; 15634:z=F(u,v),\qquad u=x,\qquad v=y,\qquad F(u,v)=\arctan\frac{v}{u}. \| 15656:F_u=-\frac{v}{u^2+v^2},\qquad F_v=\frac{u}{u^2+v^2}. \| 15691:\boxed{ f_{xx}=\frac{2xy}{(x^2+y^2)^ | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 356 | 15796 | 多元函数微分学 | 知识讲解 | 另一个抽象复合函数 | 隐函数/偏导 | 跳步关键词,短display待判定 | 直接; 15821:\boxed{z_x=2f_u+y\cos x\,f_v}. \| 15901:\boxed{ z_{xy} =-2f_{uu}+(2\sin x-y\cos x)f_{uv} +y\sin x\cos x\,f_{vv} +\cos x\,f_v }. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 357 | 15924 | 多元函数微分学 | 知识讲解 | 二阶全微分的计算 | 隐函数/偏导 | 短display待判定 | 15936:\mathrm{d}^2z =z_{xx}\,\mathrm{d}x^2 +2z_{xy}\,\mathrm{d}x\,\mathrm{d}y +z_{yy}\,\mathrm{d}y^2. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 359 | 16028 | 多元函数微分学 | 知识讲解 | 参数曲线的基本计算 |  | 跳步关键词 | 整理得 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 360 | 16065 | 多元函数微分学 | 知识讲解 | 显式曲线的切线与法平面 |  | 跳步关键词 | 整理得 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 361 | 16110 | 多元函数微分学 | 知识讲解 | 两柱面交线的切线与法平面 | 曲面积分/通量 | 短display待判定 | 16145:\boxed{\frac{x-a/\sqrt2}{1}=\frac{y-a/\sqrt2}{-1}=\frac{z-a/\sqrt2}{-1}}. \| 16149:1\cdot\left(x-\dfrac{a}{\sqrt2}\right) -1\cdot\left(y-\dfrac{a}{\sqrt2}\right) -1\cdot\left( | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 362 | 16246 | 多元函数微分学 | 知识讲解 | 显式曲面：反正切曲面 | 曲面积分/通量,隐函数/偏导 | 跳步关键词,短display待判定 | 整理得; 16253:z_x=-\frac{y}{x^2+y^2},\qquad z_y=\frac{x}{x^2+y^2}. \| 16260:z_x(1,1)=-\dfrac{1}{1+1}=-\dfrac{1}{2},\qquad z_y(1,1)=\dfrac{1}{1+1}=\dfrac{1}{2}. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 363 | 16279 | 多元函数微分学 | 知识讲解 | 隐式曲面：椭球面 | 曲面积分/通量,隐函数/偏导 | 短display待判定 | 16283:F(x,y,z)=\frac{x^2}{a^2}+\frac{y^2}{b^2}+\frac{z^2}{c^2}-1=0. \| 16290:\nabla F(p_0)= \left(\frac{2x_0}{a^2},\,\frac{2y_0}{b^2},\,\frac{2z_0}{c^2}\right). \| 16298:\frac{2x_0}{ | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 364 | 16392 | 多元函数微分学 | 知识讲解 | 隐函数的全微分 | 隐函数/偏导 | 跳步关键词 | 直接,整理得 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 365 | 16533 | 多元函数微分学 | 知识讲解 | 线性方程组的隐函数 | 隐函数/偏导 | 跳步关键词 | 可得,略 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 366 | 16620 | 多元函数微分学 | 知识讲解 | 非线性方程组的隐函数 | 隐函数/偏导 | 短display待判定 | 16666:\boxed{ \frac{\partial u}{\partial x} = -\frac{z}{2uz+1},\qquad \frac{\partial v}{\partial x} = \frac{1}{2uz+1},\qquad \frac{\partial u}{\partial z} = \frac{z-v | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 367 | 16682 | 多元函数微分学 | 知识讲解 | 线性近似计算 | 隐函数/偏导 | 跳步关键词,短display待判定 | 可得; 16693:\frac{f_x}{f}=\frac{2}{x},\qquad \frac{f_y}{f}=-\frac{1}{2y},\qquad \frac{f_z}{f}=-\frac{1}{3z}. \| 16699:\nabla f(x,y,z) =f(x,y,z)\left(\frac{2}{x},\;-\frac{1}{2y},\;-\fr | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 370 | 17001 | 多元函数微分学 | 知识讲解 | 退化的 Hesse 判别：$\Delta=0$ 的三种可能性 | 极值/拉格朗日,隐函数/偏导 | 跳步关键词 | 显然,直接 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 371 | 17031 | 多元函数微分学 | 知识讲解 | 含三次项的多项式函数 | 极值/拉格朗日,隐函数/偏导 | 短display待判定 | 17035:x-3y-9=0,\qquad 9y^2+18y-3x+9=0. \| 17039:9y^2+9y-18=0 \quad\Longleftrightarrow\quad (y+2)(y-1)=0. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 372 | 17058 | 多元函数微分学 | 知识讲解 | 超越函数的无穷多极值点 | 极值/拉格朗日,隐函数/偏导 | 短display待判定 | 17063:z_x=-(1+\mathrm{e}^{y})\sin x=0,\qquad z_y=\mathrm{e}^{y}(\cos x-1-y)=0. \| 17074:z_{xx}=-(1+\mathrm{e}^{y})\cos x,\qquad z_{xy}=-\mathrm{e}^{y}\sin x,\qquad z_{yy}=\mathrm{e} | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 373 | 17094 | 多元函数微分学 | 知识讲解 | 退化鞍点 | 极值/拉格朗日,隐函数/偏导 | 跳步关键词,短display待判定 | 直接; 17099:z_x=-6xy+8x^3=2x(4x^2-3y),\qquad z_y=2y-3x^2. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 374 | 17128 | 多元函数微分学 | 知识讲解 | 提高：Hesse 矩阵与极值判定 | 级数/幂级数,极值/拉格朗日,隐函数/偏导 | 跳步关键词,短display待判定 | 直接; 17162:3(h_1^2+h_2^2+h_3^2)-3(h_1h_2+h_2h_3+h_3h_1) =\frac{3}{2}\left[(h_1-h_2)^2+(h_2-h_3)^2+(h_3-h_1)^2\right]\geqslant 0. \| 17168:f(x,y,z)-(-6)=x^3+y^3+z^3-3xyz =\frac{1}{2}( | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 376 | 17214 | 多元函数微分学 | 知识讲解 | 思考题：三角函数在多边形域上的最值 | 极值/拉格朗日,隐函数/偏导 | 短display待判定 | 17244:f\left(\frac{\pi}{3},\frac{\pi}{3}\right) =\sin\frac{\pi}{3}\sin\frac{\pi}{3}\sin\frac{2\pi}{3} =\frac{3\sqrt{3}}{8}. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 377 | 17260 | 多元函数微分学 | 知识讲解 | 长方体的表面积最小化 | 极值/拉格朗日,隐函数/偏导 | 跳步关键词,短display待判定 | 直接,容易; 17269:\frac{S}{2} =xy+\frac{2}{x}+\frac{2}{y} \geqslant 3\sqrt[3]{xy\cdot\frac{2}{x}\cdot\frac{2}{y}} =3\sqrt[3]{4}. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 378 | 17305 | 多元函数微分学 | 知识讲解 | 圆周上的乘积极值 | 曲面积分/通量,极值/拉格朗日 | 跳步关键词,短display待判定 | 直接,于是; 17324:x+2\lambda(-2\lambda x)=x(1-4\lambda^2)=0. \| 17329:1-4\lambda^2=0,\qquad \lambda=\pm\frac12. \| 17333:(\sqrt2,\sqrt2),\quad (-\sqrt2,-\sqrt2),\quad (\sqrt2,-\sqrt2),\qu | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 379 | 17396 | 多元函数微分学 | 知识讲解 | 长方体表面积的 Lagrange 解法 | 极值/拉格朗日,隐函数/偏导 | 跳步关键词,短display待判定 | 同理; 17401:L(x,y,z;\lambda)=2(xy+yz+zx)+\lambda(xyz-2). \| 17421:\frac{S}{2}=xy+yz+zx \geqslant 3\sqrt[3]{(xy)(yz)(zx)} =3\sqrt[3]{(xyz)^2} =3\sqrt[3]{4}. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 380 | 17447 | 多元函数微分学 | 知识讲解 | 算术--几何平均不等式的最优化证明 | 极值/拉格朗日,隐函数/偏导 | 跳步关键词,短display待判定 | 可得,于是; 17452:L(x_1,\dots,x_n;\lambda) =x_1x_2\cdots x_n +\lambda(x_1+x_2+\cdots+x_n-a). \| 17466:\overline D=\{x_i\geqslant0,\ x_1+\cdots+x_n=a\}. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 381 | 17830 | 多元函数微分学 | 知识讲解 | 一般变量替换下的 PDE 变换 | 隐函数/偏导 | 跳步关键词,短display待判定 | 代入得; 17852:z_x=\frac{1}{v}+\frac{1}{v}\!\left(w_u\!\left(-\frac{v}{x^2}\right)+w_v\cdot 0\right)-0 =\frac{1}{v}-\frac{vw_u}{x^2v}=\frac{1}{v}-\frac{w_u}{x^2}. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 382 | 17903 | 多元函数微分学 | 习题 | 基本概念问答 | 极值/拉格朗日 | 长行内公式/排版风险 | 17906:225; 17909:177 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 384 | 17971 | 多元函数微分学 | 习题 | 闭集的判定 |  | 跳步关键词,短display待判定 | 可得,同理; 17976:B^c=\{(x,y) \mid x^2+y^2 \neq 1\} =\{(x,y) \mid x^2+y^2 < 1\}\cup \{(x,y) \mid x^2+y^2 > 1\}. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 385 | 18002 | 多元函数微分学 | 习题 | 点集拓扑基本概念的计算 |  | 跳步关键词,短display待判定 | 可得; 18017:\partial B = \left\{(x,y) \mid \frac{x^2}{3} + \frac{y^2}{4} = 1\right\} \cup \left\{(x,y) \mid \frac{x^2}{3} + \frac{y^2}{4} = 5\right\}. \| 18024:(B^c)^\circ= \left\{(x, | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 389 | 18133 | 多元函数微分学 | 习题 | 基础：极坐标下的极限计算 |  | 跳步关键词,短display待判定 | 代入得; 18137:\frac{x^3+y^3}{x^2+y^2} =r(\cos^3\theta+\sin^3\theta). \| 18144:\left\|\frac{x^2\sin^2y}{x^2+2y^2}\right\| \leqslant \frac{r^2\cos^2\theta\cdot r^2\sin^2\theta} {r^2(\cos^2 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 390 | 18170 | 多元函数微分学 | 习题 | 基础：极限存在性判定 | 重积分/换元 | 跳步关键词,长行内公式/排版风险,短display待判定 | 代入得; 18199:184; 18201:178; 18174:f(r\cos\theta,r\sin\theta) =\frac{r^2\cos^2\theta-r^2\sin^2\theta}{r^2\cos^2\theta+r^2\sin^2\theta} =\cos^2\theta-\sin^2\theta=\cos2\theta. \| 18181 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 391 | 18213 | 多元函数微分学 | 习题 | 提高：累次极限与二重极限 |  | 跳步关键词,长行内公式/排版风险,短display待判定 | 于是; 18228:210; 18223:f(r\cos\theta,r\sin\theta)=\cos2\theta, | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 392 | 18239 | 多元函数微分学 | 习题 | 提高：连续性综合 | 隐函数/偏导 | 跳步关键词,短display待判定 | 可得,同理; 18244:f(r\cos\theta,r\sin\theta)=r(\cos^3\theta+\sin^3\theta), | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 393 | 18283 | 多元函数微分学 | 习题 | 基本概念问答 | 曲面积分/通量 | 长行内公式/排版风险 | 18289:235; 18290:237 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 397 | 18364 | 多元函数微分学 | 习题 | 构造函数表达式 |  | 跳步关键词 | 直接 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 398 | 18375 | 多元函数微分学 | 习题 | 多元函数极限计算 |  | 跳步关键词,短display待判定 | 于是; 18378:\frac{1-xy}{x^2+y^2} =\frac{1-r\cos\theta(1+r\sin\theta)} {r^2\cos^2\theta+(1+r\sin\theta)^2} \to1. \| 18386:\frac{1}{x^2+y^2} =\frac{1}{(2+r\cos\theta)^2+r^2\sin^2\theta} | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 399 | 18418 | 多元函数微分学 | 习题 | 连续性判定 | 重积分/换元 | 短display待判定 | 18423:f(r\cos\theta,r\sin\theta) =\frac{r\cos^2\theta\sin\theta}{r^2\cos^4\theta+\sin^2\theta}. \| 18428:f(r\cos\theta,r\sin\theta)=\frac12. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 400 | 18439 | 多元函数微分学 | 习题 | 求间断点集 | 重积分/换元 | 短display待判定 | 18453:\frac{1}{x^2-xy+y^2} =\frac{1}{r^2(\cos^2\theta-\cos\theta\sin\theta+\sin^2\theta)}. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 401 | 18466 | 多元函数微分学 | 习题 | 实际问题中的极限 | 重积分/换元 | 短display待判定 | 18470:Q(r\cos\theta,r\sin\theta) =\frac{17.86r^2\cos\theta\sin\theta} {r(1.798\cos\theta+\sin\theta)} =r\frac{17.86\cos\theta\sin\theta} {1.798\cos\theta+\sin\theta}. \| 18479:\boxe | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 407 | 18623 | 多元函数微分学 | 习题 | 可微性判定 | 隐函数/偏导 | 跳步关键词,长行内公式/排版风险,短display待判定 | 同理; 18627:192; 18628:183; 18634:\frac{r\cos^3\theta\sin\theta}{r^4\cos^6\theta+\sin^2\theta}. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 408 | 18654 | 多元函数微分学 | 习题 | 偏导数连续性的分析 | 隐函数/偏导 | 长行内公式/排版风险,短display待判定 | 18667:275; 18670:\lim_{(x,y) \to (0,0)} \frac{f(x,y) - f(0,0) - (1 \cdot x + 0 \cdot y)}{\sqrt{x^2+y^2}} = \lim_{(x,y) \to (0,0)} \frac{\frac{x^3}{x^2+y^2} - x}{\sqrt{x^2+y^2}}  | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 409 | 18686 | 多元函数微分学 | 习题 | 方向导数与梯度的关系预告 | 极值/拉格朗日,隐函数/偏导 | 短display待判定 | 18690:f(p_0 + t\vec l) - f(p_0) = f_x(p_0)(tl_1) + f_y(p_0)(tl_2) + o(\\|t\vec l\\|) = t\bigl(f_x(p_0)l_1 + f_y(p_0)l_2\bigr) + o(\|t\|). | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 410 | 18719 | 多元函数微分学 | 习题 | 基本概念问答 | 曲面积分/通量,隐函数/偏导 | 长行内公式/排版风险,短display待判定 | 18728:215; 18723:\lim_{\Delta x\to0}\frac{f(x+\Delta x,y,z)-f(x,y,z)}{\Delta x} | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 411 | 18745 | 多元函数微分学 | 习题 | 偏导数的计算 | 隐函数/偏导 | 跳步关键词,长行内公式/排版风险,短display待判定 | 显然; 18758:198; 18764:u_x = \dfrac{-2x}{(x^2+y^2+z^2)^2},\quad u_y = \dfrac{-2y}{(x^2+y^2+z^2)^2},\quad u_z = \dfrac{-2z}{(x^2+y^2+z^2)^2}. \| 18770:u_x = z^{xy}\ln z \cdot y = yz^{x | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 413 | 18828 | 多元函数微分学 | 习题 | 分段函数的偏导数 | 隐函数/偏导 | 长行内公式/排版风险 | 18835:218 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 414 | 18849 | 多元函数微分学 | 习题 | 多元复合函数的偏导数 | 隐函数/偏导 | 跳步关键词,长行内公式/排版风险,高风险题解过短 | 可得,直接; 18852:187 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 417 | 18923 | 多元函数微分学 | 习题 | 可微性判定与偏导数有界性 | 隐函数/偏导,重积分/换元 | 跳步关键词,短display待判定 | 计算得,显然,同理; 18927:f(r\cos\theta,r\sin\theta)=r\cos\theta\sin\theta. \| 18940:\lim_{(x,y)\to(0,0)} \frac{f(x,y) - f(0,0)}{\sqrt{x^2+y^2}} = \lim_{(x,y)\to(0,0)} \frac{xy}{x^2+y^2}. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 418 | 18959 | 多元函数微分学 | 习题 | 偏导数的计算与求导法则 |  | 跳步关键词,长行内公式/排版风险,短display待判定 | 直接,略; 18982:173; 18966:\frac{(21x^2y^6-2y)(15xy-8) - (3x^2y^7-y^2)(15x)}{(15xy-8)^2}, | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 419 | 18993 | 多元函数微分学 | 习题 | 分段函数在指定点的偏导数 | 隐函数/偏导 | 跳步关键词 | 同理 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 420 | 19006 | 多元函数微分学 | 习题 | 全微分近似值计算 | 隐函数/偏导 | 跳步关键词,长行内公式/排版风险 | 计算得; 19020:177 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 421 | 19033 | 多元函数微分学 | 习题 | 偏导数不连续但可微的证明 | 隐函数/偏导,重积分/换元 | 跳步关键词,长行内公式/排版风险 | 可得,同理,于是; 19044:208; 19046:181 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 422 | 19060 | 多元函数微分学 | 习题 | 绝对值与函数可微性 | 隐函数/偏导 | 长行内公式/排版风险 | 19063:239 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 423 | 19082 | 多元函数微分学 | 习题 | 基础：向量值函数的极限与连续 |  | 跳步关键词 | 同理 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 424 | 19112 | 多元函数微分学 | 习题 | 基础：Jacobian 矩阵计算 | 隐函数/偏导 | 跳步关键词 | 可得,直接 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 426 | 19205 | 多元函数微分学 | 习题 | Jacobian 行列式与坐标变换 | 隐函数/偏导,重积分/换元 | 跳步关键词,长行内公式/排版风险 | 计算得,可得,显然; 19208:301; 19213:261 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 427 | 19244 | 多元函数微分学 | 习题 | 概念与基本性质问答 | 隐函数/偏导 | 长行内公式/排版风险 | 19247:268; 19251:338; 19252:174; 19257:363; 19258:205 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 428 | 19266 | 多元函数微分学 | 习题 | Jacobian 矩阵计算（二维） | 隐函数/偏导 | 长行内公式/排版风险 | 19269:216 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 430 | 19325 | 多元函数微分学 | 习题 | 复杂函数的点处 Jacobian 矩阵计算 | 隐函数/偏导 | 跳步关键词,长行内公式/排版风险 | 代入得,显然; 19348:181; 19349:174 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 431 | 19382 | 多元函数微分学 | 习题 | 基本概念问答 | 隐函数/偏导 | 跳步关键词,长行内公式/排版风险 | 可得; 19392:203; 19401:187 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 432 | 19414 | 多元函数微分学 | 习题 | 链式法则求一阶导数 | 隐函数/偏导 | 跳步关键词 | 直接 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 433 | 19475 | 多元函数微分学 | 习题 | 链式法则求偏导数 | 隐函数/偏导 | 长行内公式/排版风险 | 19493:187; 19494:183 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 435 | 19540 | 多元函数微分学 | 习题 | 点处偏导数与全导数计算 | 隐函数/偏导 | 短display待判定 | 19571:\left.\frac{\mathrm{d}u}{\mathrm{d}w}\right\|_{w=1} =\frac{\partial u}{\partial s}\frac{\mathrm{d}s}{\mathrm{d}w} +\frac{\partial u}{\partial t}\frac{\mathrm{d}t | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 436 | 19584 | 多元函数微分学 | 习题 | 抽象复合函数求导 | 隐函数/偏导 | 跳步关键词,长行内公式/排版风险 | 于是; 19587:256; 19592:271 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 437 | 19606 | 多元函数微分学 | 习题 | 求具体函数的二阶偏导数 | 隐函数/偏导 | 长行内公式/排版风险,短display待判定 | 19640:221; 19642:224; 19631:z_{xx}=\frac{-2y e^y}{(x+y)^3},\qquad z_{xy}=\frac{e^y(x-y)}{(x+y)^3},\qquad z_{yy}=\frac{x(x^2+xy-2)e^y}{(x+y)^3}. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 438 | 19649 | 多元函数微分学 | 习题 | 二阶偏导数在原点的值 | 级数/幂级数,隐函数/偏导 | 跳步关键词 | 直接 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 439 | 19670 | 多元函数微分学 | 习题 | 偏微分方程待定常数 | 微分方程,隐函数/偏导 | 长行内公式/排版风险 | 19680:184 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 441 | 19781 | 多元函数微分学 | 习题 | 抽象函数的二阶偏导数 | 隐函数/偏导 | 跳步关键词,长行内公式/排版风险 | 直接,于是; 19798:239 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 442 | 19843 | 多元函数微分学 | 习题 | 混合偏导数不相等 | 隐函数/偏导 | 跳步关键词 | 同理,直接 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 443 | 19868 | 多元函数微分学 | 习题 | 欧拉齐次函数定理 | 微分方程,隐函数/偏导 | 长行内公式/排版风险 | 19885:205; 19888:235 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 445 | 19937 | 多元函数微分学 | 习题 | 基本概念问答 | 极值/拉格朗日,隐函数/偏导 | 长行内公式/排版风险 | 19940:289 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 446 | 19965 | 多元函数微分学 | 习题 | 利用方向角计算方向导数 | 隐函数/偏导 | 长行内公式/排版风险 | 19979:196; 19982:201 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 447 | 19994 | 多元函数微分学 | 习题 | 计算具体点的梯度 | 隐函数/偏导 | 长行内公式/排版风险 | 20004:185 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 452 | 20119 | 多元函数微分学 | 习题 | 梯度的几何与物理综合应用 | 曲面积分/通量,极值/拉格朗日,隐函数/偏导 | 跳步关键词 | 显然 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 454 | 20201 | 多元函数微分学 | 习题 | 最速下降方向求解 | 隐函数/偏导 | 跳步关键词,长行内公式/排版风险 | 同理; 20205:179; 20206:220 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 456 | 20249 | 多元函数微分学 | 习题 | 向径表示法计算梯度 | 隐函数/偏导 | 跳步关键词 | 于是 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 459 | 20322 | 多元函数微分学 | 习题 | 隐函数的基本概念 | 隐函数/偏导 | 跳步关键词 | 直接 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 460 | 20344 | 多元函数微分学 | 习题 | 单方程隐函数求导 | 隐函数/偏导 | 跳步关键词,长行内公式/排版风险 | 代入得,直接; 20360:172 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 461 | 20392 | 多元函数微分学 | 习题 | 三元单方程隐函数的二阶偏导数 | 隐函数/偏导 | 跳步关键词 | 同理,直接 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 463 | 20440 | 多元函数微分学 | 习题 | 抽象隐函数求导 | 隐函数/偏导 | 长行内公式/排版风险 | 20450:196; 20456:258 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 469 | 20638 | 多元函数微分学 | 习题 | 提高：三元函数的高阶展开 | 级数/幂级数,极值/拉格朗日,隐函数/偏导 | 跳步关键词 | 直接 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 470 | 20667 | 多元函数微分学 | 习题 | Taylor 级数的收敛性与解析延拓 | 级数/幂级数 | 跳步关键词,长行内公式/排版风险 | 显然,于是; 20679:173 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 474 | 20768 | 多元函数微分学 | 习题 | 一阶 Taylor 近似应用二 | 级数/幂级数,隐函数/偏导 | 跳步关键词,长行内公式/排版风险 | 同理; 20782:250 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 477 | 20845 | 多元函数微分学 | 习题 | 曲线切向量的基本计算 | 曲面积分/通量 | 跳步关键词,长行内公式/排版风险 | 代入得,直接; 20850:184; 20852:291 | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 478 | 20870 | 多元函数微分学 | 习题 | 切线与法平面的几何计算 |  | 跳步关键词,长行内公式/排版风险,短display待判定 | 于是; 20872:227; 20874:361; 20881:179; 20885:245; 20876:1(x-\pi/2+1) + 1(y-1) + \sqrt{2}(z-2\sqrt{2}) = 0 \implies x+y+\sqrt{2}z - \dfrac{\pi}{2} - 4 = 0. | 人工逐题复核；若确认则补推导/改排版/统一方法 |
| 479 | 20892 | 多元函数微分学 | 习题 | 寻找满足特定切线条件的点 | 曲面积分/通量 | 长行内公式/排版风险 | 20902:205 | 人工逐题复核；若确认则补推导/改排版/统一方法 |

> 自动标记项共 1044 条，Markdown 仅列前 400 条；完整逐题台账见 `solution_quality_audit/solution_index.csv`。

## 全量逐题索引
| 全局序号 | 行号 | 章节 | 小节 | 状态 | 标记 |
|---:|---:|---|---|---|---|
| 1 | 1413 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 2 | 1468 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 3 | 1503 | 不定积分 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 4 | 1517 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 5 | 1558 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 6 | 1591 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 7 | 1610 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 8 | 1641 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 9 | 1696 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 10 | 1743 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 11 | 1788 | 不定积分 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 12 | 1801 | 不定积分 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 13 | 1815 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 14 | 1829 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 15 | 1843 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 16 | 1866 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 17 | 1889 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 18 | 1903 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 19 | 1917 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 20 | 1941 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 21 | 1960 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 22 | 1980 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 23 | 2000 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 24 | 2020 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 25 | 2040 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 26 | 2072 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 27 | 2111 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 28 | 2133 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 29 | 2156 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 30 | 2173 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 31 | 2206 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 32 | 2228 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 33 | 2258 | 不定积分 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 34 | 2273 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 35 | 2289 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 36 | 2312 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 37 | 2332 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 38 | 2359 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 39 | 2390 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 40 | 2442 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 41 | 2461 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 42 | 2488 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 43 | 2510 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 44 | 2525 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 45 | 2540 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 46 | 2570 | 不定积分 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 47 | 2587 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 48 | 2615 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 49 | 2635 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 50 | 2663 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 51 | 2707 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 52 | 2721 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 53 | 2749 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 54 | 2771 | 不定积分 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 55 | 2788 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 56 | 2813 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 57 | 2834 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 58 | 2849 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 59 | 2864 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 60 | 2892 | 不定积分 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 61 | 2909 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 62 | 2928 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 63 | 2948 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 64 | 2978 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 65 | 3023 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 66 | 3037 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 67 | 3065 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 68 | 3085 | 不定积分 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 69 | 3103 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 70 | 3125 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 71 | 3147 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 72 | 3162 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 73 | 3177 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 74 | 3205 | 不定积分 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 75 | 3221 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 76 | 3249 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 77 | 3269 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 78 | 3299 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 79 | 3344 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 80 | 3358 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 81 | 3386 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 82 | 3407 | 不定积分 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 83 | 3424 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 84 | 3456 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 85 | 3488 | 不定积分 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 86 | 3509 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 87 | 3540 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 88 | 3568 | 不定积分 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 89 | 3590 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 90 | 3618 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 91 | 3644 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 92 | 3658 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 93 | 3686 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 94 | 3710 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 95 | 3732 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 96 | 3764 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 97 | 3787 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 98 | 3822 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 99 | 3857 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 100 | 3876 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 101 | 3895 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 102 | 3914 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 103 | 3933 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 104 | 3966 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 105 | 3999 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 106 | 4035 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 107 | 4071 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 108 | 4105 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 109 | 4139 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 110 | 4193 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 111 | 4228 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 112 | 4267 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 113 | 4303 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 114 | 4369 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 115 | 4436 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 116 | 4472 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 117 | 4513 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 118 | 4542 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 119 | 4573 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 120 | 4609 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 121 | 4654 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 122 | 4683 | 不定积分 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 123 | 4714 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 124 | 4754 | 不定积分 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 125 | 4776 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 126 | 4822 | 不定积分 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 127 | 4863 | 不定积分 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 128 | 4887 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 129 | 4929 | 不定积分 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 130 | 4967 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 131 | 4994 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 132 | 5013 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 133 | 5038 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 134 | 5065 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险,短display待判定 |
| 135 | 5086 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 136 | 5112 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 137 | 5137 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 138 | 5160 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 139 | 5205 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 140 | 5251 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 141 | 5270 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 142 | 5293 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 143 | 5335 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 144 | 5358 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 145 | 5396 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 146 | 5422 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 147 | 5448 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 148 | 5472 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 149 | 5502 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 150 | 5525 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 151 | 5550 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 152 | 5570 | 不定积分 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 153 | 5594 | 不定积分 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 154 | 5618 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 155 | 5655 | 不定积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 156 | 5719 | 微分方程 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 157 | 5748 | 微分方程 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 158 | 5762 | 微分方程 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 159 | 5782 | 微分方程 | 知识讲解 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 160 | 5795 | 微分方程 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 161 | 5837 | 微分方程 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 162 | 5873 | 微分方程 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 163 | 5922 | 微分方程 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 164 | 5978 | 微分方程 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 165 | 6039 | 微分方程 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 166 | 6078 | 微分方程 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 167 | 6146 | 微分方程 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 168 | 6242 | 微分方程 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 169 | 6271 | 微分方程 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 170 | 6291 | 微分方程 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 171 | 6338 | 微分方程 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 172 | 6392 | 微分方程 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 173 | 6531 | 微分方程 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 174 | 6664 | 微分方程 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 175 | 6711 | 微分方程 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 176 | 6742 | 微分方程 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险,短display待判定 |
| 177 | 6818 | 微分方程 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定,高风险题解过短 |
| 178 | 6829 | 微分方程 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 179 | 6845 | 微分方程 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 180 | 6866 | 微分方程 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 181 | 6897 | 微分方程 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 182 | 6915 | 微分方程 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 183 | 6948 | 微分方程 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 184 | 7022 | 微分方程 | 知识讲解 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 185 | 7100 | 微分方程 | 知识讲解 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 186 | 7196 | 微分方程 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 187 | 7229 | 微分方程 | 知识讲解 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 188 | 7272 | 微分方程 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 189 | 7281 | 微分方程 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,高风险题解过短 |
| 190 | 7294 | 微分方程 | 知识讲解 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 191 | 7306 | 微分方程 | 知识讲解 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 192 | 7342 | 微分方程 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 193 | 7374 | 微分方程 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 194 | 7404 | 微分方程 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 195 | 7481 | 微分方程 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 196 | 7650 | 微分方程 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 197 | 7774 | 微分方程 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 198 | 7797 | 微分方程 | 知识讲解 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 199 | 7898 | 微分方程 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 200 | 7940 | 微分方程 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 201 | 7988 | 微分方程 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 202 | 8000 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 203 | 8008 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 204 | 8016 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 205 | 8039 | 微分方程 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 206 | 8082 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 207 | 8122 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 208 | 8154 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 209 | 8210 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 210 | 8240 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 211 | 8260 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 212 | 8273 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 213 | 8301 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 214 | 8384 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 215 | 8401 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 216 | 8492 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 217 | 8541 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 218 | 8606 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 219 | 8643 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 220 | 8682 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 221 | 8729 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 222 | 8772 | 微分方程 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 223 | 8793 | 微分方程 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 224 | 8806 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 225 | 8865 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 226 | 8899 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 227 | 8952 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 228 | 8982 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 229 | 9026 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 230 | 9056 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 231 | 9079 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 232 | 9168 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 233 | 9292 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 234 | 9351 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 235 | 9380 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 236 | 9461 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 237 | 9508 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 238 | 9569 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 239 | 9641 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 240 | 9670 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 241 | 9717 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 242 | 9749 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 243 | 9779 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 244 | 9838 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 245 | 9863 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 246 | 9898 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 247 | 9979 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 248 | 10060 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 249 | 10196 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 250 | 10215 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 251 | 10253 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 252 | 10285 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 253 | 10328 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 254 | 10361 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 255 | 10391 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 256 | 10411 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 257 | 10452 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 258 | 10541 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 259 | 10680 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 260 | 10704 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 261 | 10801 | 微分方程 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 262 | 10824 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 263 | 10840 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 264 | 10871 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 265 | 10898 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 266 | 10918 | 微分方程 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 267 | 10932 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 268 | 10960 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 269 | 11002 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 270 | 11030 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 271 | 11055 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 272 | 11096 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 273 | 11115 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 274 | 11146 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 275 | 11191 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 276 | 11217 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 277 | 11262 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 278 | 11346 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 279 | 11494 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 280 | 11574 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 281 | 11640 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 282 | 11736 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 283 | 11777 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 284 | 11810 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 285 | 11849 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 286 | 11882 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 287 | 11926 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 288 | 11959 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 289 | 11990 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 290 | 12011 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 291 | 12049 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 292 | 12094 | 微分方程 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 293 | 12119 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 294 | 12215 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 295 | 12251 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 296 | 12298 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 297 | 12346 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 298 | 12387 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 299 | 12470 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 300 | 12513 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 301 | 12537 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 302 | 12567 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 303 | 12602 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 304 | 12655 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 305 | 12695 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 306 | 12742 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 307 | 12783 | 微分方程 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 308 | 12808 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 309 | 12858 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 310 | 12892 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 311 | 12924 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 312 | 12962 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 313 | 12999 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 314 | 13043 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 315 | 13073 | 微分方程 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 316 | 13283 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 317 | 13313 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 318 | 13341 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 319 | 13431 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 320 | 13474 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 321 | 13505 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 322 | 13560 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 323 | 13594 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 324 | 13623 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 325 | 13641 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 326 | 13670 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 327 | 13727 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 328 | 13744 | 多元函数微分学 | 知识讲解 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 329 | 13768 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 330 | 13886 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 331 | 13917 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 332 | 13936 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 333 | 13965 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 334 | 14003 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 335 | 14120 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 336 | 14173 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 337 | 14208 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 338 | 14257 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 339 | 14302 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 340 | 14389 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 341 | 14433 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 342 | 14484 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 343 | 14494 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 344 | 14504 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 345 | 14862 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 346 | 14894 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 347 | 15077 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 348 | 15116 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 349 | 15185 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 350 | 15266 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 351 | 15293 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 352 | 15503 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 353 | 15559 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 354 | 15632 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 355 | 15704 | 多元函数微分学 | 知识讲解 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 356 | 15796 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 357 | 15924 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 358 | 16006 | 多元函数微分学 | 知识讲解 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 359 | 16028 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 360 | 16065 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 361 | 16110 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 362 | 16246 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 363 | 16279 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 364 | 16392 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 365 | 16533 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 366 | 16620 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 367 | 16682 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 368 | 16900 | 多元函数微分学 | 知识讲解 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 369 | 16920 | 多元函数微分学 | 知识讲解 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 370 | 17001 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 371 | 17031 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 372 | 17058 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 373 | 17094 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 374 | 17128 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 375 | 17189 | 多元函数微分学 | 知识讲解 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 376 | 17214 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 377 | 17260 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 378 | 17305 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 379 | 17396 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 380 | 17447 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 381 | 17830 | 多元函数微分学 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 382 | 17903 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 383 | 17951 | 多元函数微分学 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 384 | 17971 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 385 | 18002 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 386 | 18060 | 多元函数微分学 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 387 | 18080 | 多元函数微分学 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 388 | 18102 | 多元函数微分学 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 389 | 18133 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 390 | 18170 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险,短display待判定 |
| 391 | 18213 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险,短display待判定 |
| 392 | 18239 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 393 | 18283 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 394 | 18305 | 多元函数微分学 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 395 | 18327 | 多元函数微分学 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 396 | 18345 | 多元函数微分学 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 397 | 18364 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 398 | 18375 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 399 | 18418 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 400 | 18439 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 401 | 18466 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 402 | 18491 | 多元函数微分学 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 403 | 18514 | 多元函数微分学 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 404 | 18534 | 多元函数微分学 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 405 | 18550 | 多元函数微分学 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 406 | 18589 | 多元函数微分学 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 407 | 18623 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险,短display待判定 |
| 408 | 18654 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险,短display待判定 |
| 409 | 18686 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 410 | 18719 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险,短display待判定 |
| 411 | 18745 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险,短display待判定 |
| 412 | 18798 | 多元函数微分学 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 413 | 18828 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 414 | 18849 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险,高风险题解过短 |
| 415 | 18864 | 多元函数微分学 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 416 | 18893 | 多元函数微分学 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 417 | 18923 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 418 | 18959 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险,短display待判定 |
| 419 | 18993 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 420 | 19006 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险 |
| 421 | 19033 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险 |
| 422 | 19060 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 423 | 19082 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 424 | 19112 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 425 | 19150 | 多元函数微分学 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 426 | 19205 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险 |
| 427 | 19244 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 428 | 19266 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 429 | 19282 | 多元函数微分学 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 430 | 19325 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险 |
| 431 | 19382 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险 |
| 432 | 19414 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 433 | 19475 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 434 | 19519 | 多元函数微分学 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 435 | 19540 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 436 | 19584 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险 |
| 437 | 19606 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险,短display待判定 |
| 438 | 19649 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 439 | 19670 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 440 | 19691 | 多元函数微分学 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 441 | 19781 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险 |
| 442 | 19843 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 443 | 19868 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 444 | 19897 | 多元函数微分学 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 445 | 19937 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 446 | 19965 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 447 | 19994 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 448 | 20018 | 多元函数微分学 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 449 | 20041 | 多元函数微分学 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 450 | 20064 | 多元函数微分学 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 451 | 20087 | 多元函数微分学 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 452 | 20119 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 453 | 20166 | 多元函数微分学 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 454 | 20201 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险 |
| 455 | 20226 | 多元函数微分学 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 456 | 20249 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 457 | 20268 | 多元函数微分学 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 458 | 20294 | 多元函数微分学 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 459 | 20322 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 460 | 20344 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险 |
| 461 | 20392 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 462 | 20414 | 多元函数微分学 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 463 | 20440 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 464 | 20463 | 多元函数微分学 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 465 | 20489 | 多元函数微分学 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 466 | 20509 | 多元函数微分学 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 467 | 20545 | 多元函数微分学 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 468 | 20584 | 多元函数微分学 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 469 | 20638 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 470 | 20667 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险 |
| 471 | 20692 | 多元函数微分学 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 472 | 20716 | 多元函数微分学 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 473 | 20747 | 多元函数微分学 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 474 | 20768 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险 |
| 475 | 20790 | 多元函数微分学 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 476 | 20803 | 多元函数微分学 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 477 | 20845 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险 |
| 478 | 20870 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险,短display待判定 |
| 479 | 20892 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 480 | 20909 | 多元函数微分学 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 481 | 20925 | 多元函数微分学 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 482 | 20947 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险 |
| 483 | 20975 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 484 | 20998 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险 |
| 485 | 21020 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险,短display待判定 |
| 486 | 21059 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 487 | 21077 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 488 | 21101 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 489 | 21143 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险 |
| 490 | 21172 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险 |
| 491 | 21210 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 492 | 21250 | 多元函数微分学 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 493 | 21294 | 多元函数微分学 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 494 | 21315 | 多元函数微分学 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 495 | 21384 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险 |
| 496 | 21485 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 497 | 21533 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险,短display待判定 |
| 498 | 21561 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险,短display待判定 |
| 499 | 21606 | 多元函数微分学 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 500 | 21631 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 501 | 21657 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险 |
| 502 | 21673 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险,短display待判定 |
| 503 | 21699 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险,短display待判定 |
| 504 | 21734 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 505 | 21762 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 506 | 21812 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 507 | 21864 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 508 | 21919 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 509 | 21950 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 510 | 21971 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险 |
| 511 | 22042 | 多元函数微分学 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 512 | 22062 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 513 | 22074 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险 |
| 514 | 22119 | 多元函数微分学 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 515 | 22178 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 516 | 22208 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险,高风险题解过短 |
| 517 | 22219 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 518 | 22254 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 519 | 22317 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险 |
| 520 | 22383 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 521 | 22464 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 522 | 22488 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险,短display待判定 |
| 523 | 22522 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险 |
| 524 | 22564 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险 |
| 525 | 22661 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 526 | 22766 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 527 | 22794 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险,短display待判定 |
| 528 | 22830 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 529 | 22871 | 多元函数微分学 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 530 | 22891 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险,高风险题解过短 |
| 531 | 22906 | 多元函数微分学 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 532 | 22926 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险,短display待判定 |
| 533 | 22943 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 534 | 22965 | 多元函数微分学 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 535 | 22981 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险,短display待判定 |
| 536 | 23018 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 537 | 23047 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 538 | 23067 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 539 | 23096 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 540 | 23114 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 541 | 23138 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险 |
| 542 | 23159 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 543 | 23193 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险 |
| 544 | 23216 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,高风险题解过短 |
| 545 | 23231 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 546 | 23254 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 547 | 23271 | 多元函数微分学 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 548 | 23286 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险 |
| 549 | 23303 | 多元函数微分学 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 550 | 23319 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 551 | 23342 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 552 | 23357 | 多元函数微分学 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 553 | 23371 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 554 | 23394 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 555 | 23411 | 多元函数微分学 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险,短display待判定 |
| 556 | 23502 | 重积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险 |
| 557 | 23517 | 重积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险 |
| 558 | 23530 | 重积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险 |
| 559 | 23550 | 重积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险,短display待判定 |
| 560 | 23628 | 重积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 561 | 23640 | 重积分 | 知识讲解 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 562 | 23676 | 重积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险,短display待判定 |
| 563 | 23707 | 重积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 564 | 23727 | 重积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 565 | 23760 | 重积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险,短display待判定 |
| 566 | 23841 | 重积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 567 | 23867 | 重积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险,短display待判定 |
| 568 | 23910 | 重积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 569 | 23968 | 重积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险,高风险题解过短 |
| 570 | 23980 | 重积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 571 | 24010 | 重积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险,短display待判定 |
| 572 | 24119 | 重积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 573 | 24170 | 重积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 574 | 24207 | 重积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险 |
| 575 | 24248 | 重积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险 |
| 576 | 24267 | 重积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险 |
| 577 | 24292 | 重积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险 |
| 578 | 24325 | 重积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 579 | 24363 | 重积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 580 | 24394 | 重积分 | 知识讲解 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 581 | 24431 | 重积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 582 | 24469 | 重积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 583 | 24506 | 重积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险 |
| 584 | 24531 | 重积分 | 知识讲解 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 585 | 24560 | 重积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 586 | 24592 | 重积分 | 知识讲解 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 587 | 24626 | 重积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险,高风险题解过短 |
| 588 | 24637 | 重积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险,高风险题解过短 |
| 589 | 24653 | 重积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 590 | 24674 | 重积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 591 | 24690 | 重积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险 |
| 592 | 24709 | 重积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 593 | 24741 | 重积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险 |
| 594 | 24772 | 重积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险,短display待判定 |
| 595 | 24824 | 重积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险,短display待判定 |
| 596 | 24877 | 重积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险,短display待判定 |
| 597 | 24946 | 重积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 598 | 25002 | 重积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 599 | 25032 | 重积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 600 | 25049 | 重积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 601 | 25075 | 重积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 602 | 25106 | 重积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险 |
| 603 | 25127 | 重积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险 |
| 604 | 25148 | 重积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险 |
| 605 | 25177 | 重积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险,短display待判定 |
| 606 | 25198 | 重积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险,短display待判定 |
| 607 | 25219 | 重积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险 |
| 608 | 25232 | 重积分 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 609 | 25248 | 重积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险,短display待判定 |
| 610 | 25275 | 重积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险,短display待判定 |
| 611 | 25291 | 重积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险,短display待判定 |
| 612 | 25315 | 重积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 613 | 25350 | 重积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 614 | 25410 | 重积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 615 | 25458 | 重积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险 |
| 616 | 25506 | 重积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险,短display待判定 |
| 617 | 25574 | 重积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 618 | 25639 | 重积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险 |
| 619 | 25674 | 重积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险 |
| 620 | 25711 | 重积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 621 | 25751 | 重积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险,短display待判定 |
| 622 | 25805 | 重积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险 |
| 623 | 25831 | 重积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 624 | 25867 | 重积分 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 625 | 25903 | 重积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 626 | 25927 | 重积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 627 | 25961 | 重积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 628 | 25987 | 重积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险 |
| 629 | 25999 | 重积分 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 630 | 26015 | 重积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险 |
| 631 | 26037 | 重积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险 |
| 632 | 26068 | 重积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险,短display待判定 |
| 633 | 26115 | 重积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 634 | 26173 | 重积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险 |
| 635 | 26190 | 重积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 636 | 26204 | 重积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 637 | 26223 | 重积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 638 | 26243 | 重积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 639 | 26264 | 重积分 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 640 | 26277 | 重积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 641 | 26295 | 重积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险,短display待判定 |
| 642 | 26318 | 重积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险,高风险题解过短 |
| 643 | 26329 | 重积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 644 | 26550 | 曲线积分与曲面积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险,短display待判定 |
| 645 | 26565 | 曲线积分与曲面积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险,高风险题解过短 |
| 646 | 26576 | 曲线积分与曲面积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 647 | 26587 | 曲线积分与曲面积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险,短display待判定 |
| 648 | 26621 | 曲线积分与曲面积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 649 | 26634 | 曲线积分与曲面积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险 |
| 650 | 26688 | 曲线积分与曲面积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 651 | 26717 | 曲线积分与曲面积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 652 | 26730 | 曲线积分与曲面积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险,高风险题解过短 |
| 653 | 26740 | 曲线积分与曲面积分 | 知识讲解 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 654 | 26750 | 曲线积分与曲面积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险,短display待判定 |
| 655 | 26788 | 曲线积分与曲面积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 656 | 26807 | 曲线积分与曲面积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险,短display待判定 |
| 657 | 26835 | 曲线积分与曲面积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 658 | 26905 | 曲线积分与曲面积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险 |
| 659 | 26923 | 曲线积分与曲面积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 660 | 26948 | 曲线积分与曲面积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 661 | 26957 | 曲线积分与曲面积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 662 | 26973 | 曲线积分与曲面积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 663 | 27002 | 曲线积分与曲面积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 664 | 27012 | 曲线积分与曲面积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 665 | 27022 | 曲线积分与曲面积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 666 | 27122 | 曲线积分与曲面积分 | 知识讲解 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 667 | 27150 | 曲线积分与曲面积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,高风险题解过短 |
| 668 | 27162 | 曲线积分与曲面积分 | 知识讲解 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 669 | 27182 | 曲线积分与曲面积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 670 | 27250 | 曲线积分与曲面积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 671 | 27273 | 曲线积分与曲面积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 672 | 27320 | 曲线积分与曲面积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 673 | 27364 | 曲线积分与曲面积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 674 | 27404 | 曲线积分与曲面积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 675 | 27521 | 曲线积分与曲面积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 676 | 27543 | 曲线积分与曲面积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 677 | 27559 | 曲线积分与曲面积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 678 | 27582 | 曲线积分与曲面积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险,短display待判定 |
| 679 | 27607 | 曲线积分与曲面积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 680 | 27713 | 曲线积分与曲面积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 681 | 27735 | 曲线积分与曲面积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险,短display待判定 |
| 682 | 27755 | 曲线积分与曲面积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 683 | 27909 | 曲线积分与曲面积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 684 | 28020 | 曲线积分与曲面积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险,短display待判定 |
| 685 | 28045 | 曲线积分与曲面积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险,短display待判定 |
| 686 | 28070 | 曲线积分与曲面积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 687 | 28125 | 曲线积分与曲面积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 688 | 28175 | 曲线积分与曲面积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 689 | 28294 | 曲线积分与曲面积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 690 | 28323 | 曲线积分与曲面积分 | 知识讲解 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 691 | 28356 | 曲线积分与曲面积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 692 | 28385 | 曲线积分与曲面积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 693 | 28422 | 曲线积分与曲面积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 694 | 28456 | 曲线积分与曲面积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 695 | 28517 | 曲线积分与曲面积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险 |
| 696 | 28540 | 曲线积分与曲面积分 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险,短display待判定 |
| 697 | 28636 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 698 | 28654 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 699 | 28686 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险,高风险题解过短 |
| 700 | 28694 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 701 | 28706 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险,短display待判定 |
| 702 | 28721 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 703 | 28747 | 曲线积分与曲面积分 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 704 | 28759 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 705 | 28783 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 706 | 28819 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 707 | 28853 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 708 | 28885 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险 |
| 709 | 28906 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 710 | 28937 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 711 | 28967 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险,短display待判定 |
| 712 | 28997 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 713 | 29062 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 714 | 29080 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 715 | 29098 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险 |
| 716 | 29117 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险,高风险题解过短 |
| 717 | 29134 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 718 | 29158 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 719 | 29338 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 720 | 29392 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险,短display待判定 |
| 721 | 29450 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 722 | 29493 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 723 | 29556 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 724 | 29575 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 725 | 29593 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险 |
| 726 | 29613 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 727 | 29631 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险 |
| 728 | 29649 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 729 | 29668 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 730 | 29688 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险,高风险题解过短 |
| 731 | 29707 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险 |
| 732 | 29727 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险 |
| 733 | 29745 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险 |
| 734 | 29763 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 735 | 29775 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险 |
| 736 | 29793 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险,短display待判定 |
| 737 | 29813 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险,短display待判定 |
| 738 | 29829 | 曲线积分与曲面积分 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 739 | 29841 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 740 | 29862 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 741 | 29885 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 742 | 29914 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险,短display待判定 |
| 743 | 29936 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险 |
| 744 | 29955 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 745 | 29981 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 746 | 29992 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 747 | 30008 | 曲线积分与曲面积分 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 748 | 30030 | 曲线积分与曲面积分 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 749 | 30048 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险,短display待判定 |
| 750 | 30094 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 751 | 30112 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险,短display待判定 |
| 752 | 30134 | 曲线积分与曲面积分 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 753 | 30161 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 754 | 30188 | 曲线积分与曲面积分 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 755 | 30205 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 756 | 30217 | 曲线积分与曲面积分 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 757 | 30237 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险 |
| 758 | 30274 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险,短display待判定 |
| 759 | 30346 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险 |
| 760 | 30401 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险 |
| 761 | 30469 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 762 | 30549 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险 |
| 763 | 30601 | 曲线积分与曲面积分 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险,短display待判定 |
| 764 | 30976 | 级数 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 765 | 31033 | 级数 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险,短display待判定 |
| 766 | 31074 | 级数 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 767 | 31160 | 级数 | 知识讲解 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 768 | 32420 | 级数 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 769 | 32439 | 级数 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 770 | 32467 | 级数 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险 |
| 771 | 32486 | 级数 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 772 | 32507 | 级数 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 773 | 32536 | 级数 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 774 | 32566 | 级数 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 775 | 32608 | 级数 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 776 | 32646 | 级数 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险 |
| 777 | 32670 | 级数 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 778 | 32696 | 级数 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险 |
| 779 | 32716 | 级数 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险,高风险题解过短 |
| 780 | 32737 | 级数 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险 |
| 781 | 32761 | 级数 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 782 | 32781 | 级数 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 783 | 32802 | 级数 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 784 | 32815 | 级数 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 785 | 32837 | 级数 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 786 | 32856 | 级数 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 787 | 32872 | 级数 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险 |
| 788 | 32887 | 级数 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 789 | 32896 | 级数 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 790 | 32921 | 级数 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 791 | 32948 | 级数 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险,短display待判定 |
| 792 | 32981 | 级数 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 793 | 33024 | 级数 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 794 | 33059 | 级数 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 795 | 33091 | 级数 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 796 | 33109 | 级数 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 797 | 33130 | 级数 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险,短display待判定 |
| 798 | 33168 | 级数 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 799 | 33179 | 级数 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险,短display待判定 |
| 800 | 33198 | 级数 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险,短display待判定 |
| 801 | 33228 | 级数 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 802 | 33257 | 级数 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险,短display待判定 |
| 803 | 33374 | 级数 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险,高风险题解过短 |
| 804 | 33387 | 级数 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 805 | 33411 | 级数 | 习题 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 806 | 33463 | 级数 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险,短display待判定 |
| 807 | 33595 | 级数 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 808 | 33634 | 级数 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险,短display待判定 |
| 809 | 33680 | 级数 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险,短display待判定 |
| 810 | 33718 | 级数 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 811 | 33747 | 级数 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 812 | 33781 | 级数 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 813 | 33858 | 级数 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险 |
| 814 | 33897 | 级数 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险 |
| 815 | 33947 | 级数 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险,短display待判定 |
| 816 | 33979 | 级数 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险 |
| 817 | 34022 | 级数 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险,短display待判定 |
| 818 | 34117 | 级数 | 习题 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险,短display待判定 |
| 819 | 34266 | 往年真题整理 | 2006--2007 第二学期 A 卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 820 | 34294 | 往年真题整理 | 2006--2007 第二学期 A 卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 821 | 34321 | 往年真题整理 | 2006--2007 第二学期 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 822 | 34360 | 往年真题整理 | 2006--2007 第二学期 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 823 | 34397 | 往年真题整理 | 2006--2007 第二学期 A 卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 824 | 34413 | 往年真题整理 | 2006--2007 第二学期 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险,高风险题解过短 |
| 825 | 34427 | 往年真题整理 | 2006--2007 第二学期 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 826 | 34447 | 往年真题整理 | 2006--2007 第二学期 A 卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 827 | 34466 | 往年真题整理 | 2006--2007 第二学期 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 828 | 34482 | 往年真题整理 | 2006--2007 第二学期 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 829 | 34508 | 往年真题整理 | 2006--2007 第二学期 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险,短display待判定 |
| 830 | 34524 | 往年真题整理 | 2006--2007 第二学期 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 831 | 34551 | 往年真题整理 | 2006--2007 第二学期 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险,高风险题解过短 |
| 832 | 34564 | 往年真题整理 | 2006--2007 第二学期 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险,短display待判定 |
| 833 | 34582 | 往年真题整理 | 2006--2007 第二学期 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 834 | 34609 | 往年真题整理 | 2006--2007 第二学期 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 835 | 34625 | 往年真题整理 | 2006--2007 第二学期 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险 |
| 836 | 34644 | 往年真题整理 | 2006--2007 第二学期 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险 |
| 837 | 34661 | 往年真题整理 | 2006--2007 第二学期 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 838 | 34687 | 往年真题整理 | 2006--2007 第二学期 B 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险,高风险题解过短 |
| 839 | 34703 | 往年真题整理 | 2006--2007 第二学期 B 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 840 | 34723 | 往年真题整理 | 2006--2007 第二学期 B 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 841 | 34748 | 往年真题整理 | 2006--2007 第二学期 B 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 842 | 34773 | 往年真题整理 | 2006--2007 第二学期 B 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险,高风险题解过短 |
| 843 | 34787 | 往年真题整理 | 2006--2007 第二学期 B 卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 844 | 34801 | 往年真题整理 | 2006--2007 第二学期 B 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险,高风险题解过短 |
| 845 | 34813 | 往年真题整理 | 2006--2007 第二学期 B 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 846 | 34834 | 往年真题整理 | 2006--2007 第二学期 B 卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 847 | 34858 | 往年真题整理 | 2006--2007 第二学期 B 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 848 | 34887 | 往年真题整理 | 2006--2007 第二学期 B 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险,短display待判定 |
| 849 | 34907 | 往年真题整理 | 2006--2007 第二学期 B 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 850 | 34940 | 往年真题整理 | 2006--2007 第二学期 B 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 851 | 34960 | 往年真题整理 | 2006--2007 第二学期 B 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险,短display待判定 |
| 852 | 35004 | 往年真题整理 | 2006--2007 第二学期 B 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险,短display待判定 |
| 853 | 35026 | 往年真题整理 | 2006--2007 第二学期 B 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 854 | 35044 | 往年真题整理 | 2006--2007 第二学期 B 卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 855 | 35068 | 往年真题整理 | 2006--2007 第二学期 B 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 856 | 35091 | 往年真题整理 | 2006--2007 第二学期 B 卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 857 | 35120 | 往年真题整理 | 2007--2008 第二学期 A 卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 858 | 35135 | 往年真题整理 | 2007--2008 第二学期 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 859 | 35159 | 往年真题整理 | 2007--2008 第二学期 A 卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 860 | 35176 | 往年真题整理 | 2007--2008 第二学期 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险,高风险题解过短 |
| 861 | 35187 | 往年真题整理 | 2007--2008 第二学期 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 862 | 35205 | 往年真题整理 | 2007--2008 第二学期 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 863 | 35224 | 往年真题整理 | 2007--2008 第二学期 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 864 | 35250 | 往年真题整理 | 2007--2008 第二学期 A 卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 865 | 35268 | 往年真题整理 | 2007--2008 第二学期 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,高风险题解过短 |
| 866 | 35284 | 往年真题整理 | 2007--2008 第二学期 A 卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 867 | 35305 | 往年真题整理 | 2007--2008 第二学期 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险,高风险题解过短 |
| 868 | 35315 | 往年真题整理 | 2007--2008 第二学期 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 869 | 35335 | 往年真题整理 | 2007--2008 第二学期 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 870 | 35358 | 往年真题整理 | 2007--2008 第二学期 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 871 | 35383 | 往年真题整理 | 2007--2008 第二学期 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险,短display待判定 |
| 872 | 35411 | 往年真题整理 | 2007--2008 第二学期 A 卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 873 | 35438 | 往年真题整理 | 2007--2008 第二学期 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 874 | 35467 | 往年真题整理 | 2007--2008 第二学期 A 卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 875 | 35486 | 往年真题整理 | 2007--2008 第二学期 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 876 | 35509 | 往年真题整理 | 2009级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 877 | 35521 | 往年真题整理 | 2009级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 878 | 35546 | 往年真题整理 | 2009级工科数学分析下 A卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 879 | 35568 | 往年真题整理 | 2009级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 880 | 35595 | 往年真题整理 | 2009级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险,高风险题解过短 |
| 881 | 35607 | 往年真题整理 | 2009级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 882 | 35624 | 往年真题整理 | 2009级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 883 | 35641 | 往年真题整理 | 2009级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 884 | 35656 | 往年真题整理 | 2009级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 885 | 35684 | 往年真题整理 | 2009级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 886 | 35698 | 往年真题整理 | 2009级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险 |
| 887 | 35711 | 往年真题整理 | 2009级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 888 | 35740 | 往年真题整理 | 2009级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 889 | 35760 | 往年真题整理 | 2009级工科数学分析下 A卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 890 | 35785 | 往年真题整理 | 2009级工科数学分析下 A卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 891 | 35802 | 往年真题整理 | 2009级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 892 | 35833 | 往年真题整理 | 2009级工科数学分析下 A卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 893 | 35854 | 往年真题整理 | 2009级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 894 | 35879 | 往年真题整理 | 2009级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 895 | 35901 | 往年真题整理 | 2009级工科数学分析下 B卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 896 | 35918 | 往年真题整理 | 2009级工科数学分析下 B卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 897 | 35939 | 往年真题整理 | 2009级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 898 | 35972 | 往年真题整理 | 2009级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,高风险题解过短 |
| 899 | 35984 | 往年真题整理 | 2009级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 900 | 35997 | 往年真题整理 | 2009级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 901 | 36026 | 往年真题整理 | 2009级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 902 | 36045 | 往年真题整理 | 2009级工科数学分析下 B卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 903 | 36061 | 往年真题整理 | 2009级工科数学分析下 B卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 904 | 36087 | 往年真题整理 | 2009级工科数学分析下 B卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 905 | 36102 | 往年真题整理 | 2009级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 906 | 36126 | 往年真题整理 | 2009级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 907 | 36143 | 往年真题整理 | 2009级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 908 | 36167 | 往年真题整理 | 2009级工科数学分析下 B卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 909 | 36184 | 往年真题整理 | 2009级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 910 | 36201 | 往年真题整理 | 2009级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 911 | 36226 | 往年真题整理 | 2009级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 912 | 36250 | 往年真题整理 | 2012级工科数学分析下 A卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 913 | 36267 | 往年真题整理 | 2012级工科数学分析下 A卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 914 | 36300 | 往年真题整理 | 2012级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 915 | 36332 | 往年真题整理 | 2012级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 916 | 36357 | 往年真题整理 | 2012级工科数学分析下 A卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 917 | 36374 | 往年真题整理 | 2012级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 918 | 36398 | 往年真题整理 | 2012级工科数学分析下 A卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 919 | 36419 | 往年真题整理 | 2012级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 920 | 36439 | 往年真题整理 | 2012级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 921 | 36465 | 往年真题整理 | 2012级工科数学分析下 A卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 922 | 36483 | 往年真题整理 | 2012级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 923 | 36513 | 往年真题整理 | 2012级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 924 | 36549 | 往年真题整理 | 2012级工科数学分析下 A卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 925 | 36567 | 往年真题整理 | 2012级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险 |
| 926 | 36583 | 往年真题整理 | 2012级工科数学分析下 A卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 927 | 36603 | 往年真题整理 | 2012级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 928 | 36630 | 往年真题整理 | 2012级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 929 | 36653 | 往年真题整理 | 2012级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险,高风险题解过短 |
| 930 | 36666 | 往年真题整理 | 2012级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 931 | 36682 | 往年真题整理 | 2012级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 932 | 36698 | 往年真题整理 | 2012级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险,高风险题解过短 |
| 933 | 36715 | 往年真题整理 | 2012级工科数学分析下 B卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 934 | 36733 | 往年真题整理 | 2012级工科数学分析下 B卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 935 | 36749 | 往年真题整理 | 2012级工科数学分析下 B卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 936 | 36764 | 往年真题整理 | 2012级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险,短display待判定 |
| 937 | 36785 | 往年真题整理 | 2012级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 938 | 36799 | 往年真题整理 | 2012级工科数学分析下 B卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 939 | 36817 | 往年真题整理 | 2012级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险 |
| 940 | 36835 | 往年真题整理 | 2012级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 941 | 36857 | 往年真题整理 | 2012级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 942 | 36880 | 往年真题整理 | 2012级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,高风险题解过短 |
| 943 | 36893 | 往年真题整理 | 2012级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 944 | 36929 | 往年真题整理 | 2012级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 945 | 36956 | 往年真题整理 | 2012级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 946 | 36982 | 往年真题整理 | 2013级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 947 | 36996 | 往年真题整理 | 2013级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 948 | 37011 | 往年真题整理 | 2013级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 949 | 37036 | 往年真题整理 | 2013级工科数学分析下 A卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 950 | 37058 | 往年真题整理 | 2013级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,高风险题解过短 |
| 951 | 37072 | 往年真题整理 | 2013级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 952 | 37084 | 往年真题整理 | 2013级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 953 | 37096 | 往年真题整理 | 2013级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 954 | 37106 | 往年真题整理 | 2013级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 955 | 37122 | 往年真题整理 | 2013级工科数学分析下 A卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 956 | 37138 | 往年真题整理 | 2013级工科数学分析下 A卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 957 | 37157 | 往年真题整理 | 2013级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 958 | 37183 | 往年真题整理 | 2013级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 959 | 37201 | 往年真题整理 | 2013级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 960 | 37240 | 往年真题整理 | 2013级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 961 | 37256 | 往年真题整理 | 2013级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 962 | 37279 | 往年真题整理 | 2013级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 963 | 37307 | 往年真题整理 | 2013级工科数学分析下 B卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 964 | 37322 | 往年真题整理 | 2013级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险,高风险题解过短 |
| 965 | 37336 | 往年真题整理 | 2013级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 966 | 37362 | 往年真题整理 | 2013级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险,高风险题解过短 |
| 967 | 37383 | 往年真题整理 | 2013级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 968 | 37398 | 往年真题整理 | 2013级工科数学分析下 B卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 969 | 37411 | 往年真题整理 | 2013级工科数学分析下 B卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 970 | 37429 | 往年真题整理 | 2013级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 971 | 37443 | 往年真题整理 | 2013级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 972 | 37460 | 往年真题整理 | 2013级工科数学分析下 B卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 973 | 37480 | 往年真题整理 | 2013级工科数学分析下 B卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 974 | 37509 | 往年真题整理 | 2013级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 975 | 37547 | 往年真题整理 | 2013级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险 |
| 976 | 37564 | 往年真题整理 | 2013级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 977 | 37606 | 往年真题整理 | 2013级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 978 | 37636 | 往年真题整理 | 2013级工科数学分析下 B卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 979 | 37653 | 往年真题整理 | 2013级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 980 | 37674 | 往年真题整理 | 2014级工科数学分析下 A卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 981 | 37687 | 往年真题整理 | 2014级工科数学分析下 A卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 982 | 37705 | 往年真题整理 | 2014级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 983 | 37725 | 往年真题整理 | 2014级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 984 | 37737 | 往年真题整理 | 2014级工科数学分析下 A卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 985 | 37754 | 往年真题整理 | 2014级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 986 | 37772 | 往年真题整理 | 2014级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 987 | 37799 | 往年真题整理 | 2014级工科数学分析下 A卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 988 | 37815 | 往年真题整理 | 2014级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 989 | 37846 | 往年真题整理 | 2014级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 990 | 37870 | 往年真题整理 | 2014级工科数学分析下 A卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 991 | 37890 | 往年真题整理 | 2014级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 992 | 37906 | 往年真题整理 | 2014级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险 |
| 993 | 37923 | 往年真题整理 | 2014级工科数学分析下 B卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 994 | 37937 | 往年真题整理 | 2014级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 995 | 37954 | 往年真题整理 | 2014级工科数学分析下 B卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 996 | 37974 | 往年真题整理 | 2014级工科数学分析下 B卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 997 | 37989 | 往年真题整理 | 2014级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 998 | 38005 | 往年真题整理 | 2014级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 999 | 38025 | 往年真题整理 | 2014级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 1000 | 38057 | 往年真题整理 | 2014级工科数学分析下 B卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1001 | 38077 | 往年真题整理 | 2014级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险,短display待判定 |
| 1002 | 38115 | 往年真题整理 | 2014级工科数学分析下 B卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1003 | 38128 | 往年真题整理 | 2014级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险 |
| 1004 | 38146 | 往年真题整理 | 2014级工科数学分析下 B卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1005 | 38161 | 往年真题整理 | 2014级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1006 | 38191 | 往年真题整理 | 2015级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1007 | 38204 | 往年真题整理 | 2015级工科数学分析下 A卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1008 | 38225 | 往年真题整理 | 2015级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 1009 | 38246 | 往年真题整理 | 2015级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险,高风险题解过短 |
| 1010 | 38263 | 往年真题整理 | 2015级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 1011 | 38278 | 往年真题整理 | 2015级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1012 | 38293 | 往年真题整理 | 2015级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1013 | 38313 | 往年真题整理 | 2015级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1014 | 38332 | 往年真题整理 | 2015级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1015 | 38345 | 往年真题整理 | 2015级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 1016 | 38370 | 往年真题整理 | 2015级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 1017 | 38382 | 往年真题整理 | 2015级工科数学分析下 A卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1018 | 38400 | 往年真题整理 | 2015级工科数学分析下 A卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1019 | 38420 | 往年真题整理 | 2015级工科数学分析下 A卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1020 | 38435 | 往年真题整理 | 2015级工科数学分析下 A卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1021 | 38455 | 往年真题整理 | 2015级工科数学分析下 B卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1022 | 38471 | 往年真题整理 | 2015级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1023 | 38490 | 往年真题整理 | 2015级工科数学分析下 B卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1024 | 38507 | 往年真题整理 | 2015级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,高风险题解过短 |
| 1025 | 38520 | 往年真题整理 | 2015级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 1026 | 38533 | 往年真题整理 | 2015级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 1027 | 38559 | 往年真题整理 | 2015级工科数学分析下 B卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1028 | 38577 | 往年真题整理 | 2015级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 1029 | 38602 | 往年真题整理 | 2015级工科数学分析下 B卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1030 | 38620 | 往年真题整理 | 2015级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 1031 | 38647 | 往年真题整理 | 2015级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 1032 | 38664 | 往年真题整理 | 2015级工科数学分析下 B卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1033 | 38684 | 往年真题整理 | 2015级工科数学分析下 B卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1034 | 38701 | 往年真题整理 | 2015级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 1035 | 38723 | 往年真题整理 | 2015级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1036 | 38750 | 往年真题整理 | 2016级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 1037 | 38761 | 往年真题整理 | 2016级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1038 | 38776 | 往年真题整理 | 2016级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 1039 | 38800 | 往年真题整理 | 2016级工科数学分析下 A卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1040 | 38823 | 往年真题整理 | 2016级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1041 | 38850 | 往年真题整理 | 2016级工科数学分析下 A卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1042 | 38874 | 往年真题整理 | 2016级工科数学分析下 A卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1043 | 38893 | 往年真题整理 | 2016级工科数学分析下 A卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1044 | 38911 | 往年真题整理 | 2016级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 1045 | 38926 | 往年真题整理 | 2016级工科数学分析下 A卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1046 | 38944 | 往年真题整理 | 2016级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险,高风险题解过短 |
| 1047 | 38960 | 往年真题整理 | 2016级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险 |
| 1048 | 38983 | 往年真题整理 | 2016级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 1049 | 39010 | 往年真题整理 | 2016级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 1050 | 39033 | 往年真题整理 | 2016级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险,短display待判定 |
| 1051 | 39051 | 往年真题整理 | 2016级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 1052 | 39085 | 往年真题整理 | 2016级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 1053 | 39114 | 往年真题整理 | 2016级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 1054 | 39139 | 往年真题整理 | 2016级工科数学分析下 A卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1055 | 39154 | 往年真题整理 | 2016级工科数学分析下 A卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1056 | 39183 | 往年真题整理 | 2016级工科数学分析下 A卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1057 | 39209 | 往年真题整理 | 2016级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 1058 | 39233 | 往年真题整理 | 2016级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 1059 | 39245 | 往年真题整理 | 2016级工科数学分析下 B卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1060 | 39266 | 往年真题整理 | 2016级工科数学分析下 B卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1061 | 39279 | 往年真题整理 | 2016级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1062 | 39300 | 往年真题整理 | 2016级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1063 | 39317 | 往年真题整理 | 2016级工科数学分析下 B卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1064 | 39333 | 往年真题整理 | 2016级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 1065 | 39366 | 往年真题整理 | 2016级工科数学分析下 B卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1066 | 39383 | 往年真题整理 | 2016级工科数学分析下 B卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1067 | 39403 | 往年真题整理 | 2016级工科数学分析下 B卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1068 | 39416 | 往年真题整理 | 2016级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 1069 | 39437 | 往年真题整理 | 2016级工科数学分析下 B卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1070 | 39451 | 往年真题整理 | 2016级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1071 | 39469 | 往年真题整理 | 2016级工科数学分析下 B卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1072 | 39485 | 往年真题整理 | 2016级工科数学分析下 B卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1073 | 39501 | 往年真题整理 | 2016级工科数学分析下 B卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1074 | 39520 | 往年真题整理 | 2016级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1075 | 39545 | 往年真题整理 | 2016级工科数学分析下 B卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1076 | 39565 | 往年真题整理 | 2016级工科数学分析下 B卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1077 | 39588 | 往年真题整理 | 2016级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1078 | 39611 | 往年真题整理 | 2017级工科数学分析下 A卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1079 | 39626 | 往年真题整理 | 2017级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1080 | 39639 | 往年真题整理 | 2017级工科数学分析下 A卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1081 | 39660 | 往年真题整理 | 2017级工科数学分析下 A卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1082 | 39681 | 往年真题整理 | 2017级工科数学分析下 A卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1083 | 39704 | 往年真题整理 | 2017级工科数学分析下 A卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1084 | 39729 | 往年真题整理 | 2017级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1085 | 39751 | 往年真题整理 | 2017级工科数学分析下 A卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1086 | 39773 | 往年真题整理 | 2017级工科数学分析下 A卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1087 | 39794 | 往年真题整理 | 2017级工科数学分析下 A卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1088 | 39814 | 往年真题整理 | 2017级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险,短display待判定 |
| 1089 | 39841 | 往年真题整理 | 2017级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1090 | 39873 | 往年真题整理 | 2017级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 1091 | 39908 | 往年真题整理 | 2017级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 1092 | 39933 | 往年真题整理 | 2017级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1093 | 39953 | 往年真题整理 | 2017级工科数学分析下 A卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1094 | 39973 | 往年真题整理 | 2017级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险,短display待判定 |
| 1095 | 40010 | 往年真题整理 | 2017级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 1096 | 40048 | 往年真题整理 | 2017级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1097 | 40062 | 往年真题整理 | 2017级工科数学分析下 B卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1098 | 40079 | 往年真题整理 | 2017级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 1099 | 40091 | 往年真题整理 | 2017级工科数学分析下 B卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1100 | 40105 | 往年真题整理 | 2017级工科数学分析下 B卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1101 | 40125 | 往年真题整理 | 2017级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 1102 | 40141 | 往年真题整理 | 2017级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 1103 | 40155 | 往年真题整理 | 2017级工科数学分析下 B卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1104 | 40171 | 往年真题整理 | 2017级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险,高风险题解过短 |
| 1105 | 40186 | 往年真题整理 | 2017级工科数学分析下 B卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1106 | 40202 | 往年真题整理 | 2017级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 1107 | 40227 | 往年真题整理 | 2017级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1108 | 40254 | 往年真题整理 | 2017级工科数学分析下 B卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1109 | 40289 | 往年真题整理 | 2017级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1110 | 40329 | 往年真题整理 | 2017级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1111 | 40361 | 往年真题整理 | 2017级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 1112 | 40380 | 往年真题整理 | 2017级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1113 | 40403 | 往年真题整理 | 2017级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1114 | 40437 | 往年真题整理 | 2018级工科数学分析下 A卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1115 | 40450 | 往年真题整理 | 2018级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险 |
| 1116 | 40466 | 往年真题整理 | 2018级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 1117 | 40477 | 往年真题整理 | 2018级工科数学分析下 A卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1118 | 40493 | 往年真题整理 | 2018级工科数学分析下 A卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1119 | 40510 | 往年真题整理 | 2018级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 1120 | 40530 | 往年真题整理 | 2018级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 1121 | 40554 | 往年真题整理 | 2018级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 1122 | 40574 | 往年真题整理 | 2018级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1123 | 40597 | 往年真题整理 | 2018级工科数学分析下 A卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1124 | 40618 | 往年真题整理 | 2018级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 1125 | 40657 | 往年真题整理 | 2018级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1126 | 40677 | 往年真题整理 | 2018级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 1127 | 40695 | 往年真题整理 | 2018级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 1128 | 40722 | 往年真题整理 | 2018级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 1129 | 40750 | 往年真题整理 | 2018级工科数学分析下 B卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1130 | 40773 | 往年真题整理 | 2018级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 1131 | 40788 | 往年真题整理 | 2018级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,高风险题解过短 |
| 1132 | 40800 | 往年真题整理 | 2018级工科数学分析下 B卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1133 | 40823 | 往年真题整理 | 2018级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1134 | 40841 | 往年真题整理 | 2018级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 1135 | 40856 | 往年真题整理 | 2018级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 1136 | 40881 | 往年真题整理 | 2018级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 1137 | 40905 | 往年真题整理 | 2018级工科数学分析下 B卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1138 | 40933 | 往年真题整理 | 2018级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险 |
| 1139 | 40954 | 往年真题整理 | 2018级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险,短display待判定 |
| 1140 | 40977 | 往年真题整理 | 2018级工科数学分析下 B卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1141 | 40997 | 往年真题整理 | 2018级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1142 | 41019 | 往年真题整理 | 2018级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 1143 | 41054 | 往年真题整理 | 2019级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 1144 | 41066 | 往年真题整理 | 2019级工科数学分析下 A卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1145 | 41079 | 往年真题整理 | 2019级工科数学分析下 A卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1146 | 41096 | 往年真题整理 | 2019级工科数学分析下 A卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1147 | 41111 | 往年真题整理 | 2019级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1148 | 41130 | 往年真题整理 | 2019级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1149 | 41146 | 往年真题整理 | 2019级工科数学分析下 A卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1150 | 41191 | 往年真题整理 | 2019级工科数学分析下 A卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1151 | 41225 | 往年真题整理 | 2019级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 1152 | 41249 | 往年真题整理 | 2019级工科数学分析下 A卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1153 | 41282 | 往年真题整理 | 2019级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1154 | 41306 | 往年真题整理 | 2019级工科数学分析下 A卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1155 | 41325 | 往年真题整理 | 2019级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 1156 | 41359 | 往年真题整理 | 2019级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1157 | 41381 | 往年真题整理 | 2019级工科数学分析下 A卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1158 | 41408 | 往年真题整理 | 2019级工科数学分析下 B卷补考 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1159 | 41421 | 往年真题整理 | 2019级工科数学分析下 B卷补考 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1160 | 41436 | 往年真题整理 | 2019级工科数学分析下 B卷补考 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1161 | 41449 | 往年真题整理 | 2019级工科数学分析下 B卷补考 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1162 | 41469 | 往年真题整理 | 2019级工科数学分析下 B卷补考 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 1163 | 41486 | 往年真题整理 | 2019级工科数学分析下 B卷补考 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1164 | 41516 | 往年真题整理 | 2019级工科数学分析下 B卷补考 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1165 | 41536 | 往年真题整理 | 2019级工科数学分析下 B卷补考 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1166 | 41556 | 往年真题整理 | 2019级工科数学分析下 B卷补考 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 1167 | 41578 | 往年真题整理 | 2019级工科数学分析下 B卷补考 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 1168 | 41625 | 往年真题整理 | 2019级工科数学分析下 B卷补考 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1169 | 41650 | 往年真题整理 | 2019级工科数学分析下 B卷补考 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1170 | 41672 | 往年真题整理 | 2019级工科数学分析下 B卷补考 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1171 | 41689 | 往年真题整理 | 2019级工科数学分析下 B卷补考 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1172 | 41705 | 往年真题整理 | 2019级工科数学分析下 B卷补考 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1173 | 41733 | 往年真题整理 | 2020级工科数学分析（二）期末考试 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1174 | 41764 | 往年真题整理 | 2020级工科数学分析（二）期末考试 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1175 | 41787 | 往年真题整理 | 2020级工科数学分析（二）期末考试 A 卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1176 | 41811 | 往年真题整理 | 2020级工科数学分析（二）期末考试 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1177 | 41825 | 往年真题整理 | 2020级工科数学分析（二）期末考试 A 卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1178 | 41855 | 往年真题整理 | 2020级工科数学分析（二）期末考试 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 1179 | 41869 | 往年真题整理 | 2020级工科数学分析（二）期末考试 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 1180 | 41897 | 往年真题整理 | 2020级工科数学分析（二）期末考试 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险,高风险题解过短 |
| 1181 | 41906 | 往年真题整理 | 2020级工科数学分析（二）期末考试 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险,高风险题解过短 |
| 1182 | 41919 | 往年真题整理 | 2020级工科数学分析（二）期末考试 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 1183 | 41943 | 往年真题整理 | 2020级工科数学分析（二）期末考试 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1184 | 41959 | 往年真题整理 | 2020级工科数学分析（二）期末考试 A 卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1185 | 41977 | 往年真题整理 | 2020级工科数学分析（二）期末考试 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险 |
| 1186 | 42004 | 往年真题整理 | 2020级工科数学分析（二）期末考试 B 卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1187 | 42029 | 往年真题整理 | 2020级工科数学分析（二）期末考试 B 卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1188 | 42049 | 往年真题整理 | 2020级工科数学分析（二）期末考试 B 卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1189 | 42070 | 往年真题整理 | 2020级工科数学分析（二）期末考试 B 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 1190 | 42088 | 往年真题整理 | 2020级工科数学分析（二）期末考试 B 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 1191 | 42122 | 往年真题整理 | 2020级工科数学分析（二）期末考试 B 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 1192 | 42135 | 往年真题整理 | 2020级工科数学分析（二）期末考试 B 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1193 | 42163 | 往年真题整理 | 2020级工科数学分析（二）期末考试 B 卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1194 | 42180 | 往年真题整理 | 2020级工科数学分析（二）期末考试 B 卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1195 | 42196 | 往年真题整理 | 2020级工科数学分析（二）期末考试 B 卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1196 | 42230 | 往年真题整理 | 2020级工科数学分析（二）期末考试 B 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 1197 | 42254 | 往年真题整理 | 2020级工科数学分析（二）期末考试 B 卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1198 | 42272 | 往年真题整理 | 2020级工科数学分析（二）期末考试 B 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1199 | 42302 | 往年真题整理 | 2021级工科数学分析（二）期末考试 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 1200 | 42312 | 往年真题整理 | 2021级工科数学分析（二）期末考试 A 卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1201 | 42326 | 往年真题整理 | 2021级工科数学分析（二）期末考试 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 1202 | 42338 | 往年真题整理 | 2021级工科数学分析（二）期末考试 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 1203 | 42350 | 往年真题整理 | 2021级工科数学分析（二）期末考试 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 1204 | 42365 | 往年真题整理 | 2021级工科数学分析（二）期末考试 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 1205 | 42392 | 往年真题整理 | 2021级工科数学分析（二）期末考试 A 卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1206 | 42408 | 往年真题整理 | 2021级工科数学分析（二）期末考试 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 1207 | 42421 | 往年真题整理 | 2021级工科数学分析（二）期末考试 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险 |
| 1208 | 42442 | 往年真题整理 | 2021级工科数学分析（二）期末考试 A 卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1209 | 42456 | 往年真题整理 | 2021级工科数学分析（二）期末考试 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1210 | 42469 | 往年真题整理 | 2021级工科数学分析（二）期末考试 A 卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1211 | 42485 | 往年真题整理 | 2021级工科数学分析（二）期末考试 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1212 | 42506 | 往年真题整理 | 2021级工科数学分析（二）期末考试 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 1213 | 42540 | 往年真题整理 | 2021级工科数学分析（二）期末考试 B 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 1214 | 42551 | 往年真题整理 | 2021级工科数学分析（二）期末考试 B 卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1215 | 42571 | 往年真题整理 | 2021级工科数学分析（二）期末考试 B 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 1216 | 42581 | 往年真题整理 | 2021级工科数学分析（二）期末考试 B 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 1217 | 42593 | 往年真题整理 | 2021级工科数学分析（二）期末考试 B 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 1218 | 42607 | 往年真题整理 | 2021级工科数学分析（二）期末考试 B 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 1219 | 42626 | 往年真题整理 | 2021级工科数学分析（二）期末考试 B 卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1220 | 42641 | 往年真题整理 | 2021级工科数学分析（二）期末考试 B 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险,短display待判定 |
| 1221 | 42687 | 往年真题整理 | 2021级工科数学分析（二）期末考试 B 卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1222 | 42705 | 往年真题整理 | 2021级工科数学分析（二）期末考试 B 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1223 | 42723 | 往年真题整理 | 2021级工科数学分析（二）期末考试 B 卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1224 | 42749 | 往年真题整理 | 2021级工科数学分析（二）期末考试 B 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险,高风险题解过短 |
| 1225 | 42762 | 往年真题整理 | 2021级工科数学分析（二）期末考试 B 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1226 | 42782 | 往年真题整理 | 2021级工科数学分析（二）期末考试 B 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1227 | 42803 | 往年真题整理 | 2022级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 1228 | 42813 | 往年真题整理 | 2022级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 1229 | 42824 | 往年真题整理 | 2022级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 1230 | 42845 | 往年真题整理 | 2022级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1231 | 42865 | 往年真题整理 | 2022级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 1232 | 42886 | 往年真题整理 | 2022级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 1233 | 42903 | 往年真题整理 | 2022级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 1234 | 42921 | 往年真题整理 | 2022级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 1235 | 42940 | 往年真题整理 | 2022级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 1236 | 42958 | 往年真题整理 | 2022级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 1237 | 42976 | 往年真题整理 | 2022级工科数学分析下 A卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1238 | 42995 | 往年真题整理 | 2022级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险,短display待判定 |
| 1239 | 43009 | 往年真题整理 | 2022级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 1240 | 43027 | 往年真题整理 | 2022级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险,短display待判定 |
| 1241 | 43060 | 往年真题整理 | 2022级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 1242 | 43076 | 往年真题整理 | 2022级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险,高风险题解过短 |
| 1243 | 43090 | 往年真题整理 | 2022级工科数学分析下 A卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1244 | 43120 | 往年真题整理 | 2022级工科数学分析下 A卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1245 | 43142 | 往年真题整理 | 2022级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,高风险题解过短 |
| 1246 | 43153 | 往年真题整理 | 2022级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 1247 | 43167 | 往年真题整理 | 2022级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1248 | 43181 | 往年真题整理 | 2022级工科数学分析下 B卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1249 | 43203 | 往年真题整理 | 2022级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险,高风险题解过短 |
| 1250 | 43220 | 往年真题整理 | 2022级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 1251 | 43236 | 往年真题整理 | 2022级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 1252 | 43251 | 往年真题整理 | 2022级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 1253 | 43271 | 往年真题整理 | 2022级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,高风险题解过短 |
| 1254 | 43287 | 往年真题整理 | 2022级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险,高风险题解过短 |
| 1255 | 43304 | 往年真题整理 | 2022级工科数学分析下 B卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1256 | 43336 | 往年真题整理 | 2022级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 1257 | 43363 | 往年真题整理 | 2022级工科数学分析下 B卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1258 | 43396 | 往年真题整理 | 2022级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 1259 | 43428 | 往年真题整理 | 2022级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 1260 | 43446 | 往年真题整理 | 2022级工科数学分析下 B卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1261 | 43466 | 往年真题整理 | 2022级工科数学分析下 B卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1262 | 43485 | 往年真题整理 | 2022级工科数学分析下 B卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1263 | 43508 | 往年真题整理 | 2023级工科数学分析（二）期末考试 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险,高风险题解过短 |
| 1264 | 43518 | 往年真题整理 | 2023级工科数学分析（二）期末考试 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 1265 | 43530 | 往年真题整理 | 2023级工科数学分析（二）期末考试 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 1266 | 43549 | 往年真题整理 | 2023级工科数学分析（二）期末考试 A 卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1267 | 43570 | 往年真题整理 | 2023级工科数学分析（二）期末考试 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险,高风险题解过短 |
| 1268 | 43584 | 往年真题整理 | 2023级工科数学分析（二）期末考试 A 卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1269 | 43597 | 往年真题整理 | 2023级工科数学分析（二）期末考试 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 1270 | 43611 | 往年真题整理 | 2023级工科数学分析（二）期末考试 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1271 | 43625 | 往年真题整理 | 2023级工科数学分析（二）期末考试 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 1272 | 43646 | 往年真题整理 | 2023级工科数学分析（二）期末考试 A 卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1273 | 43668 | 往年真题整理 | 2023级工科数学分析（二）期末考试 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 1274 | 43685 | 往年真题整理 | 2023级工科数学分析（二）期末考试 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1275 | 43708 | 往年真题整理 | 2023级工科数学分析（二）期末考试 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 1276 | 43729 | 往年真题整理 | 2023级工科数学分析（二）期末考试 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1277 | 43751 | 往年真题整理 | 2023级工科数学分析（二）期末考试 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险,短display待判定 |
| 1278 | 43773 | 往年真题整理 | 2023级工科数学分析（二）期末考试 B 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 1279 | 43783 | 往年真题整理 | 2023级工科数学分析（二）期末考试 B 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 1280 | 43795 | 往年真题整理 | 2023级工科数学分析（二）期末考试 B 卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1281 | 43809 | 往年真题整理 | 2023级工科数学分析（二）期末考试 B 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 1282 | 43848 | 往年真题整理 | 2023级工科数学分析（二）期末考试 B 卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1283 | 43865 | 往年真题整理 | 2023级工科数学分析（二）期末考试 B 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 1284 | 43876 | 往年真题整理 | 2023级工科数学分析（二）期末考试 B 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 1285 | 43895 | 往年真题整理 | 2023级工科数学分析（二）期末考试 B 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1286 | 43920 | 往年真题整理 | 2023级工科数学分析（二）期末考试 B 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险,短display待判定 |
| 1287 | 43943 | 往年真题整理 | 2023级工科数学分析（二）期末考试 B 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险 |
| 1288 | 43967 | 往年真题整理 | 2023级工科数学分析（二）期末考试 B 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险,短display待判定 |
| 1289 | 43995 | 往年真题整理 | 2023级工科数学分析（二）期末考试 B 卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1290 | 44013 | 往年真题整理 | 2023级工科数学分析（二）期末考试 B 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险 |
| 1291 | 44055 | 往年真题整理 | 2023级工科数学分析（二）期末考试 B 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1292 | 44077 | 往年真题整理 | 2023级工科数学分析（二）期末考试 B 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险 |
| 1293 | 44097 | 往年真题整理 | 2024级工科数学分析（二）期末考试 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 1294 | 44107 | 往年真题整理 | 2024级工科数学分析（二）期末考试 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 1295 | 44120 | 往年真题整理 | 2024级工科数学分析（二）期末考试 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 1296 | 44138 | 往年真题整理 | 2024级工科数学分析（二）期末考试 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 1297 | 44156 | 往年真题整理 | 2024级工科数学分析（二）期末考试 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 1298 | 44173 | 往年真题整理 | 2024级工科数学分析（二）期末考试 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险,高风险题解过短 |
| 1299 | 44185 | 往年真题整理 | 2024级工科数学分析（二）期末考试 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险,短display待判定 |
| 1300 | 44204 | 往年真题整理 | 2024级工科数学分析（二）期末考试 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1301 | 44225 | 往年真题整理 | 2024级工科数学分析（二）期末考试 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 1302 | 44255 | 往年真题整理 | 2024级工科数学分析（二）期末考试 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险,高风险题解过短 |
| 1303 | 44273 | 往年真题整理 | 2024级工科数学分析（二）期末考试 A 卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1304 | 44291 | 往年真题整理 | 2024级工科数学分析（二）期末考试 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险,高风险题解过短 |
| 1305 | 44307 | 往年真题整理 | 2024级工科数学分析（二）期末考试 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 1306 | 44354 | 往年真题整理 | 2024级工科数学分析（二）期末考试 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,高风险题解过短 |
| 1307 | 44370 | 往年真题整理 | 2024级工科数学分析（二）期末考试 A 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 1308 | 44387 | 往年真题整理 | 2024级工科数学分析（二）期末考试 B 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 1309 | 44398 | 往年真题整理 | 2024级工科数学分析（二）期末考试 B 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 1310 | 44413 | 往年真题整理 | 2024级工科数学分析（二）期末考试 B 卷 | AUTO_INDEXED_NO_HEURISTIC_FLAG |  |
| 1311 | 44425 | 往年真题整理 | 2024级工科数学分析（二）期末考试 B 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 1312 | 44445 | 往年真题整理 | 2024级工科数学分析（二）期末考试 B 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 1313 | 44462 | 往年真题整理 | 2024级工科数学分析（二）期末考试 B 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 高风险题解过短 |
| 1314 | 44475 | 往年真题整理 | 2024级工科数学分析（二）期末考试 B 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,短display待判定 |
| 1315 | 44500 | 往年真题整理 | 2024级工科数学分析（二）期末考试 B 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
| 1316 | 44532 | 往年真题整理 | 2024级工科数学分析（二）期末考试 B 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 1317 | 44561 | 往年真题整理 | 2024级工科数学分析（二）期末考试 B 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词,长行内公式/排版风险 |
| 1318 | 44578 | 往年真题整理 | 2024级工科数学分析（二）期末考试 B 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 1319 | 44600 | 往年真题整理 | 2024级工科数学分析（二）期末考试 B 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 短display待判定 |
| 1320 | 44636 | 往年真题整理 | 2024级工科数学分析（二）期末考试 B 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险 |
| 1321 | 44661 | 往年真题整理 | 2024级工科数学分析（二）期末考试 B 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 长行内公式/排版风险,高风险题解过短 |
| 1322 | 44684 | 往年真题整理 | 2024级工科数学分析（二）期末考试 B 卷 | AUTO_FLAGGED_NEEDS_MANUAL | 跳步关键词 |
