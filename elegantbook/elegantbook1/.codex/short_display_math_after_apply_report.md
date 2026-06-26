# Short Display Math Audit

- total display blocks: 3571
- ratio < 0.5: 2364
- inline-safe candidates: 1579

## Low-Width Blocks

| index | lines | ratio | status | kind | preview |
|---:|---:|---:|---|---|---|
| 2 | 170-172 | 0.31 | inline_safe | bracket | `\Omega=\{\omega:\omega \text{ 是该随机试验的一个可能结果}\}.` |
| 4 | 236-238 | 0.31 | inline_safe | bracket | `A \cap (B - C) = (A \cap B) - (A \cap C).` |
| 6 | 260-262 | 0.20 | inline_safe | bracket | `\text{A、B、C 都发生} \Longleftrightarrow ABC.` |
| 7 | 265-267 | 0.07 | inline_safe | bracket | `\overline{ABC}.` |
| 8 | 288-290 | 0.20 | inline_safe | bracket | `A=\bigcap_{i=1}^{n}A_i` |
| 10 | 301-303 | 0.18 | inline_safe | bracket | `\bigcup_{i=1}^{n}\overline{A_i}.` |
| 11 | 320-322 | 0.16 | inline_safe | bracket | `\overline{A}\,\overline{B}=\overline{A\cup B}.` |
| 12 | 324-326 | 0.35 | inline_safe | bracket | `\overline{A\cup B}=\varnothing \quad\Longrightarrow\quad A\cup B=\Omega.` |
| 14 | 342-344 | 0.13 | inline_safe | bracket | `AC=BC=\varnothing` |
| 15 | 365-367 | 0.23 | inline_safe | bracket | `\overline{A}\,\overline{B}\,\overline{C}=\overline{A\cup B\cup C}.` |
| 16 | 370-372 | 0.21 | inline_safe | bracket | `\overline{ABC}=\overline{A}\cup\overline{B}\cup\overline{C}.` |
| 17 | 375-377 | 0.17 | inline_safe | bracket | `\overline{AB}\cap\overline{AC}\cap\overline{BC},` |
| 18 | 379-381 | 0.40 | inline_safe | bracket | `\overline{A}\,\overline{B}\,\overline{C}\cup A\overline{B}\,\overline{C}\cup\overline{A}\,B\,\overline{C}\cup\overline{A}\,\overline{B}\,C.` |
| 19 | 416-418 | 0.49 | inline_safe | bracket | `A=\{\text{点落入 }[0,1]\},\qquad B=\{\text{点落入 }[1,2]\}.` |
| 21 | 446-448 | 0.20 | inline_safe | bracket | `P(AB)=P(\overline{A}\,\overline{B})` |
| 22 | 452-454 | 0.16 | inline_safe | bracket | `\overline{A}\,\overline{B}=\overline{A\cup B},` |
| 23 | 456-458 | 0.39 | inline_safe | bracket | `P(\overline{A}\,\overline{B})=P(\overline{A\cup B})=1-P(A\cup B).` |
| 24 | 461-463 | 0.35 | inline_safe | bracket | `P(A\cup B)=P(A)+P(B)-P(AB),` |
| 25 | 465-467 | 0.41 | inline_safe | bracket | `P(\overline{A}\,\overline{B})=1-P(A)-P(B)+P(AB),` |
| 26 | 469-471 | 0.37 | inline_safe | bracket | `P(AB)=1-P(A)-P(B)+P(AB).` |
| 27 | 485-487 | 0.28 | inline_safe | bracket | `P(A-B)=P(A)-P(AB).` |
| 28 | 489-491 | 0.41 | inline_safe | bracket | `P(\overline{AB})=1-P(AB)=1-0.4=0.6.` |
| 29 | 504-506 | 0.35 | inline_safe | bracket | `P(A\cup B)=P(A)+P(B)-P(AB).` |
| 31 | 523-525 | 0.28 | inline_safe | bracket | `P(AB)=0.5-0.3=0.2.` |
| 32 | 527-530 | 0.33 | normalized_width_not_low | bracket | `P(A\cup B)=P(A)+P(B)-P(AB) =0.5+0.4-0.2=0.7.` |
| 33 | 559-561 | 0.46 | inline_safe | bracket | `P\!\left(\bigcup_{i=1}^{\infty} A_i\right) = \sum_{i=1}^{\infty} P(A_i),` |
| 34 | 579-581 | 0.46 | inline_safe | bracket | `P\!\left(\bigcup_{i=1}^{n} A_i\right) = \sum_{i=1}^{n} P(A_i);` |
| 35 | 583-585 | 0.28 | inline_safe | bracket | `P(A - B) = P(A) - P(AB);` |
| 38 | 602-604 | 0.40 | inline_safe | bracket | `P\!\left(\bigcup_{i=1}^{\infty} \varnothing\right) = \sum_{i=1}^{\infty} P(\varnothing).` |
| 40 | 626-628 | 0.25 | inline_safe | bracket | `P(A \cup B) = P(A) + P(B),` |
| 41 | 645-647 | 0.36 | inline_safe | bracket | `P(A-B)=P(A)-P(AB)=P(A).` |
| 42 | 656-658 | 0.22 | inline_safe | bracket | `P(AB)\neq P(A)P(B),` |
| 43 | 675-686 | 0.11 | inline_unsafe_marker | bracket | `\begin{array}{c\|cccccc} B\setminus C & 1 & 2 & 3 & 4 & 5 & 6 \\ \midrule 1 & - & - & - & - & - & - \\ 2 & 0 & - & - & - & - & - \\ 3 & + & + & - & - & - & - \\ 4 & + & + & + & +...` |
| 47 | 748-750 | 0.28 | inline_safe | bracket | `P(A-B)=P(A)-P(AB),` |
| 49 | 760-762 | 0.36 | inline_safe | bracket | `P(A\overline{B}) = P(A) - P(B) + P(\overline{A}B).` |
| 50 | 798-800 | 0.31 | inline_safe | bracket | `P(A-B)=P(A)-0=P(A),` |
| 53 | 861-863 | 0.38 | inline_safe | bracket | `P(A) = \frac{k}{n} = \frac{\text{事件} \ A \ \text{所含基本事件的个数}}{\text{基本事件总数}}.` |
| 56 | 909-911 | 0.32 | inline_safe | bracket | `n_A = n!, \quad P(A) = \frac{n!}{N^n}.` |
| 59 | 959-961 | 0.27 | inline_safe | bracket | `P = \frac{5^2 - 2^2}{5^2} = \frac{21}{25}.` |
| 60 | 964-966 | 0.39 | inline_safe | bracket | `P = \frac{5 \cdot 4 - 2 \cdot 1}{5 \cdot 4} = \frac{18}{20} = \frac{9}{10}.` |
| 61 | 969-971 | 0.33 | inline_safe | bracket | `P = \frac{\mathrm{C}_5^2 - \mathrm{C}_2^2}{\mathrm{C}_5^2} = \frac{9}{10}.` |
| 62 | 988-993 | 0.18 | normalized_width_not_low | bracket | `P(\text{至少一个黑球}) =1-\frac{\mathrm C_4^3}{\mathrm C_6^3} =1-\frac4{20} =\frac45.` |
| 63 | 1007-1009 | 0.29 | inline_safe | bracket | `p_2 = \frac{\mathrm{C}_{40}^{15} \mathrm{C}_{60}^{5}}{\mathrm{C}_{100}^{20}}.` |
| 64 | 1011-1013 | 0.21 | inline_safe | bracket | `p_3 = \frac{40}{100} = \frac{2}{5}.` |
| 65 | 1015-1017 | 0.43 | inline_safe | bracket | `p_4 = \frac{\mathrm{C}_{40}^1 \cdot 99!}{100!} = \frac{40}{100} = \frac{2}{5}.` |
| 66 | 1046-1051 | 0.23 | normalized_width_not_low | bracket | `P(\text{花色各不相同}) =\frac{\mathrm C_4^3\cdot 13^3}{\mathrm C_{52}^{3}} =\frac{4\cdot 2197}{22100} =\frac{8788}{22100}.` |
| 67 | 1054-1059 | 0.17 | normalized_width_not_low | bracket | `P(\text{至少 2 张同花色}) =1-\frac{8788}{22100} =\frac{13312}{22100} =\frac{256}{425}.` |
| 70 | 1094-1096 | 0.23 | inline_safe | bracket | `P(A) = \frac{S_A \text{ 的几何度量}}{\Omega \text{ 的几何度量}}.` |
| 71 | 1110-1112 | 0.35 | inline_safe | bracket | `D=\{(x,y)\mid 0<x<1,\ 0<y<1\}` |
| 72 | 1116-1118 | 0.38 | inline_safe | bracket | `y=x+0.5,\qquad y=x-0.5` |
| 73 | 1122-1124 | 0.36 | inline_safe | bracket | `\frac12\cdot 0.5\cdot 0.5=\frac18.` |
| 74 | 1143-1148 | 0.16 | structural | bracket | `P\!\left(\angle AEB\ge \frac{\pi}{2}\right) =\frac{S_{\text{半圆}}}{S_{\text{矩形}}} =\frac{25\pi/2}{50} =\frac{\pi}{4}.` |
| 75 | 1158-1158 | 0.40 | inline_safe | bracket | `A = \left\{(x,y)\,\middle\|\, x+y<\frac{5}{4},\ xy>\frac{1}{4}\right\}.` |
| 77 | 1176-1176 | 0.39 | inline_safe | bracket | `P = \frac{a^2/2+\pi a^2/4}{\pi a^2/2} = \frac{1}{2}+\frac{1}{\pi}.` |
| 78 | 1186-1188 | 0.19 | inline_safe | bracket | `P(B\|A) = \frac{P(AB)}{P(A)}` |
| 81 | 1221-1223 | 0.33 | inline_safe | bracket | `P(B) = P(B\|\Omega) \xrightarrow{\Omega \to A} P(B\|A).` |
| 82 | 1225-1227 | 0.28 | inline_safe | bracket | `P(A\|B)=\frac{P(A)}{P(B)}\ge P(A),` |
| 83 | 1229-1231 | 0.38 | inline_safe | bracket | `P[(B-C)\|A] = P(B\|A) - P(BC\|A).` |
| 84 | 1243-1246 | 0.39 | normalized_width_not_low | bracket | `P(\overline A B)=P(B\mid \overline A)P(\overline A) =\frac56\left(1-\frac25\right)=\frac12.` |
| 85 | 1248-1253 | 0.14 | normalized_width_not_low | bracket | `P(\overline A\mid B) =\frac{P(\overline A B)}{P(B)} =\frac{\frac12}{\frac45} =\frac58.` |
| 86 | 1258-1260 | 0.30 | inline_safe | bracket | `P(A\mid B)+P(\overline A\mid \overline B)=1,` |
| 88 | 1273-1275 | 0.28 | inline_safe | bracket | `\frac{x}{b}+\frac{1-a-b+x}{1-b}=1.` |
| 89 | 1277-1279 | 0.44 | inline_safe | bracket | `x(1-b)+b(1-a-b+x)=b(1-b).` |
| 90 | 1281-1283 | 0.08 | inline_safe | bracket | `x=ab,` |
| 91 | 1291-1293 | 0.24 | inline_safe | bracket | `P(AB) = P(B\|A)\,P(A).` |
| 93 | 1302-1305 | 0.49 | display_environment | env:align* | `P(A_1 A_2 \cdots A_n) &= P\!\bigl[(A_1 \cdots A_{n-1}) \cdot A_n\bigr] \\ &= P(A_n \| A_1 \cdots A_{n-1}) \cdot P(A_1 \cdots A_{n-1}),` |
| 94 | 1321-1323 | 0.43 | inline_safe | bracket | `P(A) = \sum_{i=1}^{n} P(B_i)\,P(A\|B_i).` |
| 103 | 1410-1412 | 0.45 | inline_safe | bracket | `P(A-B) = P(A) - P(AB) \ge P(A) - P(B),` |
| 104 | 1428-1430 | 0.33 | inline_safe | bracket | `P(A\cup B)=P(A)+P(B)-P(AB)` |
| 107 | 1449-1451 | 0.49 | inline_safe | bracket | `P(\overline{A}\cup\overline{B})=P(\overline{AB})=1-P(AB)=1-0=1.` |
| 108 | 1464-1466 | 0.29 | inline_safe | bracket | `P(AB\mid \overline C)=\frac{P(AB\overline C)}{P(\overline C)}.` |
| 110 | 1478-1480 | 0.34 | inline_safe | bracket | `P(AB\mid \overline C)=\frac{1/2}{2/3}=\frac34.` |
| 119 | 1569-1571 | 0.47 | inline_safe | bracket | `P(A_1)=\frac{2}{12},\qquad P(\overline{A_1})=\frac{10}{12}.` |
| 120 | 1573-1575 | 0.23 | inline_safe | bracket | `P(A_2\mid A_1)=\frac{1}{11}.` |
| 121 | 1577-1579 | 0.24 | inline_safe | bracket | `P(A_2\mid \overline{A_1})=\frac{2}{11}.` |
| 122 | 1582-1587 | 0.41 | normalized_width_not_low | bracket | `P(A_2)=\frac{2}{12}\cdot\frac{1}{11}+\frac{10}{12}\cdot\frac{2}{11} =\frac{2+20}{132} =\frac{22}{132} =\frac16.` |
| 127 | 1634-1634 | 0.47 | inline_safe | bracket | `P(AB) = P(A) - P(A\overline{B}) = 0.7 - 0.5 = 0.2.` |
| 129 | 1638-1638 | 0.37 | inline_safe | bracket | `B \cap (A\cup\overline{B}) = (B\cap A)\cup(B\cap\overline{B}) = AB,` |
| 130 | 1640-1640 | 0.45 | inline_safe | bracket | `P(B\|A\cup\overline{B}) = \frac{P(AB)}{P(A\cup\overline{B})} = \frac{0.2}{0.8} = 0.25.` |
| 131 | 1655-1657 | 0.40 | inline_safe | bracket | `P(A\mid B)=\frac{P(AB)}{P(B)}=\frac{P(A)}{P(B)}\ge P(A).` |
| 132 | 1674-1676 | 0.44 | inline_safe | bracket | `A=\{\text{传送信号 }0\},\qquad B=\{\text{接收到信号 }0\}.` |
| 134 | 1682-1684 | 0.21 | inline_safe | bracket | `P(\overline B\|\overline A)=0.9,` |
| 135 | 1686-1688 | 0.30 | inline_safe | bracket | `P(B\|\overline A)=1-0.9=0.1.` |
| 136 | 1691-1699 | 0.37 | inline_unsafe_marker | bracket | `\begin{aligned} P(B) &=P(A)P(B\|A)+P(\overline A)P(B\|\overline A)\\ &=0.7\times 0.8+0.3\times 0.1\\ &=0.56+0.03\\ &=0.59. \end{aligned}` |
| 137 | 1702-1704 | 0.27 | inline_safe | bracket | `P(A\|B)=\frac{P(A)P(B\|A)}{P(B)}.` |
| 138 | 1706-1708 | 0.44 | inline_safe | bracket | `P(A\|B)=\frac{0.7\times 0.8}{0.59}=\frac{0.56}{0.59}=\frac{56}{59}.` |
| 141 | 1734-1736 | 0.44 | inline_safe | bracket | `P(AB)=P(A)P(B)=0.6\times 0.7=0.42.` |
| 142 | 1738-1746 | 0.25 | inline_unsafe_marker | bracket | `\begin{aligned} P(C) &=P(A\cup B)\\ &=P(A)+P(B)-P(AB)\\ &=0.6+0.7-0.42\\ &=0.88. \end{aligned}` |
| 143 | 1749-1751 | 0.49 | inline_safe | bracket | `P(A\|C)=\frac{P(AC)}{P(C)}=\frac{P(A)}{P(C)}=\frac{0.6}{0.88}=\frac{15}{22}.` |
| 144 | 1764-1766 | 0.49 | inline_safe | bracket | `A=\{\text{取出的球是白球}\},\qquad B=\{\text{原来那个球是白球}\}.` |
| 145 | 1768-1770 | 0.29 | inline_safe | bracket | `P(B)=P(\overline B)=\frac12.` |
| 146 | 1781-1783 | 0.48 | inline_safe | bracket | `P(B\|A)=\frac{P(B)P(A\|B)}{P(B)P(A\|B)+P(\overline B)P(A\|\overline B)}.` |
| 147 | 1785-1793 | 0.42 | inline_unsafe_marker | bracket | `\begin{aligned} P(B\|A) &=\frac{\frac12\times 1}{\frac12\times 1+\frac12\times\frac12}\\ &=\frac{\frac12}{\frac12+\frac14} =\frac{\frac12}{\frac34} =\frac23. \end{aligned}` |
| 155 | 1900-1902 | 0.38 | inline_safe | bracket | `P(B\mid \overline{A})=\frac{P(B)}{P(\overline{A})}=\frac{0.4}{0.7}=\frac{4}{7}.` |
| 156 | 1912-1916 | 0.11 | inline_safe | bracket | `A\cap\overline{A\cup B\cup C} \subset A\cap\overline A =\varnothing,` |
| 157 | 1931-1933 | 0.38 | inline_safe | bracket | `P(\overline B-\overline A)=P(\overline B)-P(\overline A).` |
| 159 | 1948-1950 | 0.35 | inline_safe | bracket | `P(B\|A_1)=\frac{\mathrm{C}_4^2}{\mathrm{C}_9^2}=\frac16.` |
| 160 | 1952-1954 | 0.45 | inline_safe | bracket | `P(B\|A_2)=P(B\|A_3)=\frac{\mathrm{C}_5^2}{\mathrm{C}_9^2}=\frac{5}{18}.` |
| 162 | 1962-1966 | 0.34 | normalized_width_not_low | bracket | `P(A_1\|B)=\frac{P(A_1)P(B\|A_1)}{P(B)} =\frac{\frac12\cdot\frac16}{\frac29} =\frac38.` |
| 163 | 1978-1980 | 0.49 | inline_safe | bracket | `P(Y=k\mid X=n) = \mathrm{C}_n^k\,p^k\,(1-p)^{n-k}.` |
| 165 | 2006-2006 | 0.33 | inline_safe | bracket | `E(X\|A) = \frac{1+5+10}{3} = \frac{16}{3}.` |
| 166 | 2008-2008 | 0.28 | inline_safe | bracket | `E(X\|B) = \frac{2+5+8}{3} = 5.` |
| 168 | 2017-2017 | 0.24 | inline_safe | bracket | `P(E_1) = \frac{m+2}{3(n+2)}.` |
| 169 | 2019-2019 | 0.24 | inline_safe | bracket | `P(E_2) = \frac{m+2}{3(n+2)}.` |
| 170 | 2026-2026 | 0.18 | inline_safe | bracket | `P(E_1\|E) = \frac{1}{3}.` |
| 171 | 2028-2028 | 0.48 | inline_safe | bracket | `\frac{m+2}{3(n+2)} = \frac{1}{3} \implies m+2 = n+2 \implies m = n,` |
| 173 | 2041-2043 | 0.44 | inline_safe | bracket | `P(E_1 E_2) = \frac{(n+2)^2 - \sum s_i^2}{9(n+1)(n+2)}.` |
| 174 | 2045-2047 | 0.33 | inline_safe | bracket | `\frac{(n+2)^2 - \sum s_i^2}{(n+1)(n+2)} = 1,` |
| 175 | 2051-2056 | 0.22 | inline_unsafe_marker | bracket | `\begin{cases} \displaystyle\sum s_i = n+2, \\[6pt] \displaystyle\sum s_i^2 = n+2. \end{cases}` |
| 176 | 2069-2071 | 0.22 | inline_safe | bracket | `P(AB) = P(A)\,P(B),` |
| 178 | 2084-2091 | 0.29 | inline_unsafe_marker | bracket | `\begin{cases} P(AB) = P(A)\,P(B), \\ P(AC) = P(A)\,P(C), \\ P(BC) = P(B)\,P(C), \\ P(ABC) = P(A)\,P(B)\,P(C). \end{cases}` |
| 181 | 2150-2152 | 0.27 | inline_safe | bracket | `P(ABC)=P(A)P(B)P(C).` |
| 182 | 2154-2156 | 0.27 | inline_safe | bracket | `P(A\cdot BC)=P(A)P(BC).` |
| 183 | 2158-2160 | 0.27 | inline_safe | bracket | `P(ABC)=P(A)P(B)P(C).` |
| 188 | 2221-2228 | 0.44 | inline_unsafe_marker | bracket | `\begin{aligned} P[(A\cup B)C] &= P(AC\cup BC) = P(AC)+P(BC)-P(ABC) \\ &= P(A)\,P(C)+P(B)\,P(C)-P(ABC), \\ P(A\cup B)\,P(C) &= [P(A)+P(B)-P(AB)]\,P(C) \\ &= P(A)\,P(C)+P(B)\,P(C)...` |
| 190 | 2243-2245 | 0.34 | inline_safe | bracket | `C\cap(A\cup B) = (\overline{A}\cup B)\cap(A\cup B) = B,` |
| 191 | 2247-2249 | 0.43 | inline_safe | bracket | `P(C\mid(A\cup B)) = \frac{P(B)}{P(A\cup B)} = \frac{0.4}{0.7} = \frac{4}{7}.` |
| 197 | 2350-2352 | 0.39 | inline_safe | bracket | `3p(1-p)^2 \cdot p = 3p^2(1-p)^2.` |
| 198 | 2357-2359 | 0.38 | inline_safe | bracket | `\mathrm{C}_{n-1}^{k-1}\, p^k\, (1-p)^{n-k},` |
| 202 | 2402-2404 | 0.21 | inline_safe | bracket | `B=A_1\cup A_2\cup A_3,` |
| 203 | 2405-2407 | 0.25 | inline_safe | bracket | `\overline{B}=\overline{A_1}\,\overline{A_2}\,\overline{A_3},` |
| 204 | 2411-2416 | 0.36 | normalized_width_not_low | bracket | `P(\overline{B}) =P(\overline{A_1})P(\overline{A_2})P(\overline{A_3}) =\frac45\times\frac23\times\frac34 =\frac25.` |
| 205 | 2419-2421 | 0.47 | inline_safe | bracket | `P(B)=1-P(\overline{B})=1-\frac25=\frac35.` |
| 206 | 2435-2438 | 0.21 | inline_safe | bracket | `P(A\cup B) =1-P(\overline A\,\overline B).` |
| 207 | 2440-2445 | 0.33 | normalized_width_not_low | bracket | `P(\overline A\,\overline B) =P(\overline A)P(\overline B) =\left(1-\frac12\right)\left(1-\frac13\right) =\frac13.` |
| 208 | 2447-2449 | 0.36 | inline_safe | bracket | `P(A\cup B)=1-\frac13=\frac23.` |
| 211 | 2498-2500 | 0.20 | inline_safe | bracket | `P(B\|A)=\frac{P(AB)}{P(A)}.` |
| 212 | 2502-2504 | 0.23 | inline_safe | bracket | `P(B\|A)=\frac{P(A)}{P(A)}=1.` |
| 213 | 2519-2523 | 0.25 | normalized_width_not_low | bracket | `(A\cup B)-B=(A\cup B)\overline B =A\overline B\cup B\overline B =A\overline B=A-B.` |
| 214 | 2527-2529 | 0.31 | inline_safe | bracket | `(A-B)\cup B=A\overline B\cup B=A\cup B,` |
| 215 | 2540-2542 | 0.13 | inline_safe | bracket | `\binom{10}{3}=120.` |
| 216 | 2545-2549 | 0.24 | inline_safe | bracket | `P=\frac{\binom42\binom61}{\binom{10}{3}} =\frac{6\times 6}{120} =\frac{3}{10}.` |
| 217 | 2552-2556 | 0.19 | inline_safe | bracket | `P=1-\frac{\binom63}{\binom{10}{3}} =1-\frac{20}{120} =\frac56.` |
| 218 | 2564-2567 | 0.35 | normalized_width_not_low | bracket | `A=\{\text{两颗骰子的点数之和为 }7\},\qquad B=\{\text{其中一颗为 }1\text{ 点}\}.` |
| 219 | 2569-2571 | 0.45 | inline_safe | bracket | `(1,6),(2,5),(3,4),(4,3),(5,2),(6,1),` |
| 220 | 2575-2577 | 0.15 | inline_safe | bracket | `(1,6),(6,1),` |
| 221 | 2579-2581 | 0.27 | inline_safe | bracket | `P(B\|A)=\frac{2}{6}=\frac13.` |
| 222 | 2588-2590 | 0.47 | inline_safe | bracket | `P(A)=\frac12,\qquad P(B)=\frac23,` |
| 224 | 2602-2607 | 0.38 | normalized_width_not_low | bracket | `\max\left\{0,\frac12+\frac23-1\right\} =\frac16, \qquad \min\left\{\frac12,\frac23\right\}=\frac12.` |
| 225 | 2609-2611 | 0.32 | inline_safe | bracket | `\frac16\le P(AB)\le \frac12.` |
| 226 | 2626-2628 | 0.11 | inline_safe | bracket | `5^2=25.` |
| 227 | 2630-2632 | 0.37 | inline_safe | bracket | `(1,1),(2,2),(3,3),(4,4),(5,5),` |
| 228 | 2634-2636 | 0.35 | inline_safe | bracket | `1-\frac5{25}=\frac{20}{25}=\frac45.` |
| 229 | 2651-2653 | 0.47 | inline_safe | bracket | `A=\{\text{点数之和为偶数}\},\qquad B=\{\text{点数之和为 }6\}.` |
| 230 | 2655-2657 | 0.29 | inline_safe | bracket | `\|A\|=3\times3+3\times3=18.` |
| 231 | 2659-2661 | 0.37 | inline_safe | bracket | `(1,5),(2,4),(3,3),(4,2),(5,1),` |
| 232 | 2663-2665 | 0.30 | inline_safe | bracket | `P(B\|A)=\frac{\|B\|}{\|A\|}=\frac5{18}.` |
| 233 | 2673-2676 | 0.33 | normalized_width_not_low | bracket | `P(A\cup B)=P(A)+P(B)-P(AB) =P(A)+P(B)-P(A)P(B).` |
| 235 | 2688-2692 | 0.29 | normalized_width_not_low | bracket | `P=0.7+(1-0.7)\times0.8 =0.7+0.24 =0.94.` |
| 236 | 2703-2705 | 0.13 | inline_safe | bracket | `5^4=625.` |
| 237 | 2708-2710 | 0.31 | inline_safe | bracket | `P=\frac5{625}=\frac1{125}.` |
| 238 | 2713-2715 | 0.48 | inline_safe | bracket | `\binom51\binom42A_4^2=5\times6\times12=360.` |
| 239 | 2717-2719 | 0.21 | inline_safe | bracket | `P=\frac{360}{625}=\frac{72}{125}.` |
| 241 | 2732-2734 | 0.46 | inline_safe | bracket | `P(G\|H)=0.9,\qquad P(G\|\overline H)=0.2.` |
| 242 | 2737-2740 | 0.42 | normalized_width_not_low | bracket | `P(G)=P(H)P(G\|H)+P(\overline H)P(G\|\overline H) =0.1\times0.9+0.9\times0.2=0.27.` |
| 243 | 2743-2747 | 0.26 | normalized_width_not_low | bracket | `P(H\|G)=\frac{P(H)P(G\|H)}{P(G)} =\frac{0.1\times0.9}{0.27} =\frac13.` |
| 246 | 2762-2770 | 0.45 | inline_unsafe_marker | bracket | `\begin{aligned} P((A\cup B)C) &=P(AC\cup BC)\\ &=P(AC)+P(BC)-P(ABC)\\ &=P(A)P(C)+P(B)P(C)-P(A)P(B)P(C)\\ &=\bigl[P(A)+P(B)-P(A)P(B)\bigr]P(C). \end{aligned}` |
| 248 | 2776-2778 | 0.29 | inline_safe | bracket | `P((A\cup B)C)=P(A\cup B)P(C),` |
| 249 | 2789-2791 | 0.32 | inline_safe | bracket | `AB=\varnothing,\qquad P(AB)=0.` |
| 250 | 2793-2795 | 0.40 | inline_safe | bracket | `P(B\|A)=\frac{P(AB)}{P(A)}=\frac0{P(A)}=0.` |
| 251 | 2804-2806 | 0.11 | inline_safe | bracket | `6^2=36.` |
| 252 | 2808-2810 | 0.25 | inline_safe | bracket | `(1,1),(2,2),\dots,(6,6),` |
| 253 | 2812-2814 | 0.35 | inline_safe | bracket | `1-\frac6{36}=\frac{30}{36}=\frac56.` |
| 254 | 2822-2825 | 0.33 | normalized_width_not_low | bracket | `P(A\cup B)=P(A)+P(B)-P(AB) =P(A)+P(B)-P(A)P(B).` |
| 255 | 2827-2829 | 0.46 | inline_safe | bracket | `P(A\cup B)=0.3+0.5-0.3\times0.5=0.65.` |
| 256 | 2839-2841 | 0.13 | inline_safe | bracket | `\binom{12}{3}=220.` |
| 257 | 2844-2846 | 0.33 | inline_safe | bracket | `\binom51\binom41\binom31=60,` |
| 258 | 2848-2850 | 0.25 | inline_safe | bracket | `P=\frac{60}{220}=\frac3{11}.` |
| 259 | 2853-2857 | 0.19 | inline_safe | bracket | `P=1-\frac{\binom73}{\binom{12}{3}} =1-\frac{35}{220} =\frac{37}{44}.` |
| 262 | 2875-2882 | 0.48 | inline_unsafe_marker | bracket | `\begin{aligned} P(D) &=P(A)P(D\|A)+P(B)P(D\|B)+P(C)P(D\|C)\\ &=0.5\times0.03+0.3\times0.04+0.2\times0.01\\ &=0.029. \end{aligned}` |
| 263 | 2886-2890 | 0.26 | normalized_width_not_low | bracket | `P(A\|D)=\frac{P(A)P(D\|A)}{P(D)} =\frac{0.5\times0.03}{0.029} =\frac{15}{29}.` |
| 265 | 2910-2912 | 0.31 | inline_safe | bracket | `P(A\|B)=\frac{P(AB)}{P(B)}=\frac{P(A)}{P(B)}.` |
| 266 | 2927-2929 | 0.09 | inline_safe | bracket | `2^3=8` |
| 267 | 2931-2933 | 0.13 | inline_safe | bracket | `\binom32=3` |
| 268 | 2935-2937 | 0.31 | inline_safe | bracket | `P(A)=\frac{\binom32}{2^3}=\frac38.` |
| 269 | 2945-2947 | 0.22 | inline_safe | bracket | `P=\frac{20}{50}=\frac25.` |
| 271 | 2968-2970 | 0.13 | inline_safe | bracket | `\binom{10}{3}=120.` |
| 272 | 2973-2975 | 0.47 | inline_safe | bracket | `P(A)=\frac{\binom42}{\binom{10}{3}}=\frac6{120}=\frac1{20}.` |
| 273 | 2978-2982 | 0.24 | normalized_width_not_low | bracket | `P(B)=1-\frac8{\binom{10}{3}} =1-\frac8{120} =\frac{14}{15}.` |
| 274 | 2990-2992 | 0.38 | inline_safe | bracket | `P(G)=0.96,\quad P(\overline G)=0.04,` |
| 275 | 2993-2995 | 0.43 | inline_safe | bracket | `P(T\|G)=0.98,\quad P(T\|\overline G)=0.05.` |
| 277 | 3001-3005 | 0.26 | normalized_width_not_low | bracket | `P(G\|T)=\frac{P(G)P(T\|G)}{P(T)} =\frac{0.96\times0.98}{0.9428} \approx0.9979.` |
| 278 | 3015-3017 | 0.24 | inline_safe | bracket | `1-(1-p)^3=\frac{37}{64}.` |
| 279 | 3019-3021 | 0.36 | inline_safe | bracket | `(1-p)^3=\frac{27}{64}=\left(\frac34\right)^3,` |
| 280 | 3023-3025 | 0.14 | inline_safe | bracket | `p=\frac14.` |
| 284 | 3045-3049 | 0.34 | normalized_width_not_low | bracket | `P(B_1\|A)=\frac{P(B_1)P(A\|B_1)}{P(A)} =\frac{0.5\times0.9}{0.83} =\frac{45}{83}\approx0.542.` |
| 285 | 3063-3065 | 0.15 | inline_safe | bracket | `A-B=A\overline B.` |
| 286 | 3067-3069 | 0.15 | inline_safe | bracket | `A=AB\cup A\overline B.` |
| 287 | 3071-3073 | 0.28 | inline_safe | bracket | `P(A)=P(AB)+P(A\overline B),` |
| 288 | 3075-3077 | 0.40 | inline_safe | bracket | `P(A-B)=P(A\overline B)=P(A)-P(AB).` |
| 289 | 3084-3087 | 0.42 | normalized_width_not_low | bracket | `P\{X\ge0,Y\ge0\}=\frac37,\qquad P\{X\ge0\}=P\{Y\ge0\}=\frac47.` |
| 290 | 3092-3094 | 0.21 | inline_safe | bracket | `\{X\ge0\}\cup\{Y\ge0\}.` |
| 291 | 3096-3103 | 0.48 | inline_unsafe_marker | bracket | `\begin{aligned} P\{\max(X,Y)\ge0\} &=P\{X\ge0\}+P\{Y\ge0\}-P\{X\ge0,Y\ge0\}\\ &=\frac47+\frac47-\frac37 =\frac57. \end{aligned}` |
| 292 | 3111-3113 | 0.07 | inline_safe | bracket | `A=B.` |
| 293 | 3123-3125 | 0.05 | inline_safe | bracket | `\binom{52}{13}` |
| 294 | 3127-3129 | 0.21 | inline_safe | bracket | `\binom{13}{5}\binom{13}{5}\binom{13}{2}\binom{13}{1}.` |
| 295 | 3131-3133 | 0.23 | inline_safe | bracket | `\frac{\binom{13}{5}\binom{13}{5}\binom{13}{2}\binom{13}{1}}{\binom{52}{13}}.` |
| 296 | 3136-3138 | 0.10 | inline_safe | bracket | `\frac14.` |
| 297 | 3143-3145 | 0.35 | inline_safe | bracket | `P(A)+P(B)+P(C)\le 2+P(D).` |
| 298 | 3149-3151 | 0.08 | inline_safe | bracket | `ABC\subset D,` |
| 299 | 3155-3157 | 0.29 | inline_safe | bracket | `P(A)+P(B)-P(AB)\le1,` |
| 300 | 3159-3161 | 0.29 | inline_safe | bracket | `P(A)+P(B)\le1+P(AB).` |
| 301 | 3163-3171 | 0.27 | inline_unsafe_marker | bracket | `\begin{aligned} P(A)+P(B)+P(C) &\le 1+P(AB)+P(C)\\ &=1+P(AB\cup C)+P(ABC)\\ &\le 2+P(ABC)\\ &\le 2+P(D). \end{aligned}` |
| 302 | 3179-3181 | 0.36 | inline_safe | bracket | `\overline X=\frac1n\sum_{i=1}^{n}X_i.` |
| 303 | 3188-3190 | 0.37 | inline_safe | bracket | `f(x)=\lambda e^{-\lambda x},\qquad x>0,` |
| 305 | 3196-3198 | 0.28 | inline_safe | bracket | `\overline X\xrightarrow{P}E(X_1)=\frac1\lambda,` |
| 307 | 3213-3216 | 0.43 | normalized_width_not_low | bracket | `\sum_{n=1}^{\infty}P\!\left\{X=(-1)^{n+1}\frac{2^n}{n}\right\} =\sum_{n=1}^{\infty}\frac1{2^n}=1,` |
| 308 | 3218-3222 | 0.34 | normalized_width_not_low | bracket | `\sum_{n=1}^{\infty} \left\|(-1)^{n+1}\frac{2^n}{n}\right\|\frac1{2^n} =\sum_{n=1}^{\infty}\frac1n=\infty.` |
| 309 | 3224-3226 | 0.38 | inline_safe | bracket | `\sum_{n=1}^{\infty}(-1)^{n+1}\frac1n,` |
| 310 | 3243-3245 | 0.29 | inline_safe | bracket | `P(\text{拒绝 }H_0\mid H_0\text{ 为假})=1-\alpha.` |
| 311 | 3252-3254 | 0.25 | inline_safe | bracket | `\alpha=P(\text{拒绝 }H_0\mid H_0\text{ 为真}).` |
| 312 | 3256-3258 | 0.19 | inline_safe | bracket | `P(\text{拒绝 }H_0\mid H_0\text{ 为假})` |
| 313 | 3264-3266 | 0.18 | inline_safe | bracket | `P(\|X-\mu\|\ge2\sigma)` |
| 314 | 3271-3273 | 0.44 | inline_safe | bracket | `P(\|X-\mu\|\ge2\sigma)\le \frac{\sigma^2}{(2\sigma)^2}=\frac14.` |
| 315 | 3275-3277 | 0.36 | inline_safe | bracket | `0\le P(\|X-\mu\|\ge2\sigma)\le \frac14.` |
| 318 | 3300-3302 | 0.47 | inline_safe | bracket | `P(\text{能击沉})=1-\frac{13}{1296}=\frac{1283}{1296}\approx0.9900.` |
| 319 | 3314-3316 | 0.06 | inline_safe | bracket | `\binom{52}{5}.` |
| 320 | 3319-3321 | 0.31 | inline_safe | bracket | `P_1=\frac{4(13-4)}{\binom{52}{5}}=\frac{36}{\binom{52}{5}}.` |
| 321 | 3324-3326 | 0.38 | inline_safe | bracket | `P_2=\frac{\binom{13}{1}\binom43\binom{12}{1}\binom42}{\binom{52}{5}}.` |
| 322 | 3329-3331 | 0.46 | inline_safe | bracket | `P_3=\frac{\binom{13}{1}\binom43\binom{12}{2}\binom41\binom41}{\binom{52}{5}}.` |
| 323 | 3341-3343 | 0.38 | inline_safe | bracket | `P(B)=0.96,\quad P(\overline B)=0.04,` |
| 324 | 3344-3346 | 0.49 | inline_safe | bracket | `P(A\|B)=0.98,\qquad P(A\|\overline B)=0.05.` |
| 326 | 3353-3357 | 0.26 | normalized_width_not_low | bracket | `P(B\|A)=\frac{P(B)P(A\|B)}{P(A)} =\frac{0.96\times0.98}{0.9428} \approx0.9979.` |
| 327 | 3360-3362 | 0.14 | inline_safe | bracket | `1-0.05^n.` |
| 328 | 3364-3366 | 0.23 | inline_safe | bracket | `1-0.05^n>0.999,` |
| 329 | 3368-3370 | 0.18 | inline_safe | bracket | `0.05^n<0.001.` |
| 331 | 3376-3378 | 0.06 | inline_safe | bracket | `n=3` |
| 333 | 3400-3402 | 0.47 | inline_safe | bracket | `P(\text{能击沉})=1-\frac{41}{1280}=\frac{1239}{1280}\approx0.9680.` |
| 334 | 3413-3415 | 0.06 | inline_safe | bracket | `\binom{52}{5}.` |
| 335 | 3418-3420 | 0.20 | inline_safe | bracket | `P_1=\frac{9\cdot4^5}{\binom{52}{5}}.` |
| 336 | 3423-3425 | 0.38 | inline_safe | bracket | `P_2=\frac{\binom{13}{2}\binom42^2\cdot 11\cdot4}{\binom{52}{5}}.` |
| 337 | 3428-3430 | 0.25 | inline_safe | bracket | `P_3=\frac{13\cdot12\cdot4}{\binom{52}{5}}.` |
| 338 | 3440-3442 | 0.43 | inline_safe | bracket | `P(B)=0.96,\qquad P(\overline B)=0.04,` |
| 339 | 3443-3445 | 0.49 | inline_safe | bracket | `P(A\|B)=0.97,\qquad P(A\|\overline B)=0.06.` |
| 341 | 3452-3456 | 0.26 | normalized_width_not_low | bracket | `P(B\|A)=\frac{P(B)P(A\|B)}{P(A)} =\frac{0.96\times0.97}{0.9336} =\frac{388}{389}\approx0.9974.` |
| 342 | 3459-3461 | 0.14 | inline_safe | bracket | `1-0.06^n.` |
| 343 | 3463-3465 | 0.23 | inline_safe | bracket | `1-0.06^n>0.999,` |
| 344 | 3467-3469 | 0.18 | inline_safe | bracket | `0.06^n<0.001.` |
| 346 | 3475-3477 | 0.06 | inline_safe | bracket | `n=3` |
| 349 | 3498-3502 | 0.42 | normalized_width_not_low | bracket | `\frac8{20}\cdot\frac12+\frac{12}{20}\cdot\frac13 =\frac15+\frac15 =\frac25.` |
| 350 | 3518-3520 | 0.11 | inline_safe | bracket | `\overline B\subset \overline A.` |
| 351 | 3523-3525 | 0.25 | inline_safe | bracket | `\overline A B=B\cap\overline A=B-A.` |
| 352 | 3527-3529 | 0.38 | inline_safe | bracket | `P(A\cup B)=P(A)+P(B)-P(A)P(B),` |
| 353 | 3531-3533 | 0.26 | inline_safe | bracket | `AB(A\overline B)=A B\overline B=\varnothing,` |
| 354 | 3539-3541 | 0.35 | inline_safe | bracket | `\max\{P(\overline A),P(\overline B)\}=\underline{\hspace{2cm}}.` |
| 355 | 3547-3549 | 0.32 | inline_safe | bracket | `AB=\varnothing,\qquad P(AB)=0.` |
| 356 | 3551-3553 | 0.21 | inline_safe | bracket | `P(AB)=P(A)P(B).` |
| 357 | 3555-3557 | 0.16 | inline_safe | bracket | `P(A)P(B)=0,` |
| 358 | 3559-3561 | 0.30 | inline_safe | bracket | `\max\{P(\overline A),P(\overline B)\}=1.` |
| 359 | 3571-3573 | 0.47 | inline_safe | bracket | `P(B_j)=\frac16,\qquad j=1,2,\dots,6.` |
| 360 | 3575-3577 | 0.27 | inline_safe | bracket | `P(A\|B_j)=\frac{\binom4j}{\binom{10}j};` |
| 362 | 3597-3603 | 0.29 | normalized_width_not_low | bracket | `P(B_3\|A) =\frac{P(B_3)P(A\|B_3)}{P(A)} =\frac{\frac16\cdot\frac{\binom43}{\binom{10}3}}{\frac2{21}} =\frac{\frac16\cdot\frac1{30}}{\frac2{21}} =\frac7{120}.` |
| 363 | 3613-3615 | 0.09 | inline_safe | bracket | `\binom92` |
| 364 | 3617-3619 | 0.21 | inline_safe | bracket | `\binom11\binom81=8` |
| 365 | 3621-3625 | 0.24 | inline_safe | bracket | `P=\frac{\binom11\binom81}{\binom92} =\frac8{36} =\frac29.` |
| 366 | 3635-3637 | 0.43 | inline_safe | bracket | `P(A)=0.45,\qquad P(\overline A)=0.55,` |
| 367 | 3638-3640 | 0.49 | inline_safe | bracket | `P(B\|A)=0.90,\qquad P(B\|\overline A)=0.05.` |
| 368 | 3643-3650 | 0.37 | inline_unsafe_marker | bracket | `\begin{aligned} P(B) &=P(A)P(B\|A)+P(\overline A)P(B\|\overline A)\\ &=0.45\times0.90+0.55\times0.05\\ &=0.4325. \end{aligned}` |
| 369 | 3653-3657 | 0.26 | normalized_width_not_low | bracket | `P(A\|B)=\frac{P(A)P(B\|A)}{P(B)} =\frac{0.45\times0.90}{0.4325} \approx0.9364.` |
| 370 | 3665-3667 | 0.37 | inline_safe | bracket | `0.95\times0.90\times0.75=0.64125.` |
| 371 | 3669-3671 | 0.32 | inline_safe | bracket | `0.64125\times0.9=0.577125.` |
| 372 | 3674-3676 | 0.21 | inline_safe | bracket | `0.9\times0.9=0.81.` |
| 373 | 3678-3680 | 0.24 | inline_safe | bracket | `0.81\times0.8=0.648.` |
| 374 | 3682-3684 | 0.21 | inline_safe | bracket | `0.648>0.577125,` |
| 378 | 3707-3709 | 0.28 | inline_safe | bracket | `2P(X>Y)+P(X=Y)=1.` |
| 379 | 3711-3715 | 0.37 | normalized_width_not_low | bracket | `P(X+U>Y) =\frac12\{2P(X>Y)+P(X=Y)\} =\frac12.` |
| 382 | 3732-3736 | 0.46 | normalized_width_not_low | bracket | `P(B)=\frac59\cdot0.95+\frac49\cdot0.98 =\frac{4.75+3.92}{9} =\frac{867}{900}.` |
| 383 | 3738-3741 | 0.34 | inline_safe | bracket | `P(A_1\|B)=\frac{P(A_1)P(B\|A_1)}{P(B)} =\frac{475}{867},` |
| 384 | 3742-3745 | 0.34 | inline_safe | bracket | `P(A_2\|B)=\frac{P(A_2)P(B\|A_2)}{P(B)} =\frac{392}{867}.` |
| 385 | 3763-3765 | 0.27 | inline_safe | bracket | `P=\frac{2\cdot4!}{5!}=\frac25.` |
| 386 | 3768-3770 | 0.27 | inline_safe | bracket | `P=\frac{2!\,3!}{5!}=\frac1{10}.` |
| 388 | 3779-3781 | 0.33 | inline_safe | bracket | `P=1-\frac7{10}=\frac3{10}.` |
| 389 | 3784-3786 | 0.22 | inline_safe | bracket | `P=\frac{4!}{5!}=\frac15.` |
| 392 | 3802-3806 | 0.26 | normalized_width_not_low | bracket | `P(A\|C)=\frac{P(A)P(C\|A)}{P(C)} =\frac{0.5\times0.05}{0.02625} =\frac{20}{21}.` |
| 393 | 3815-3817 | 0.15 | inline_safe | bracket | `T=a+b+c.` |
| 395 | 3825-3827 | 0.45 | inline_safe | bracket | `P(\text{第 }k\text{ 次取到红球})=E(M_{k-1})=\frac{a}{a+b+c}.` |
| 398 | 3849-3852 | 0.31 | inline_safe | bracket | `P(\overline A\,\overline B\,\overline C) =1-P(A\cup B\cup C)=\frac38.` |
| 401 | 3873-3875 | 0.46 | inline_safe | bracket | `P(\overline A\,\overline B\,\overline C)=1-\frac25=\frac35.` |
| 408 | 3917-3921 | 0.47 | normalized_width_not_low | bracket | `P(D\|B_1)=\frac4{12}=\frac13,\qquad P(D\|B_2)=\frac6{16}=\frac38,\qquad P(D\|B_3)=\frac8{24}=\frac13.` |
| 411 | 3933-3935 | 0.45 | inline_safe | bracket | `P(B_3\|D)=\frac{\frac12\cdot\frac13}{11/32}=\frac{16}{33}.` |
| 416 | 3961-3963 | 0.49 | inline_safe | bracket | `P(B_3\|D)=\frac{\frac13\cdot\frac14}{1/3}=\frac14.` |
| 417 | 3976-3978 | 0.13 | inline_safe | bracket | `P=\frac{\binom{51}{5}}{\binom{52}{6}}.` |
| 418 | 3981-3983 | 0.20 | inline_safe | bracket | `P=\frac{\binom{51}{5}-\binom{47}{5}}{\binom{52}{6}}.` |
| 419 | 3986-3988 | 0.09 | inline_safe | bracket | `\binom{13}{n}4^n` |
| 420 | 3990-3992 | 0.17 | inline_safe | bracket | `1-\frac{\binom{13}{n}4^n}{\binom{52}{n}}.` |
| 421 | 3994-3996 | 0.28 | inline_safe | bracket | `1-\frac{\binom{13}{n}4^n}{\binom{52}{n}}>\frac12.` |
| 423 | 4011-4019 | 0.37 | inline_unsafe_marker | bracket | `\begin{aligned} P(B) &=P(A)P(B\|A)+P(\overline A)P(B\|\overline A)\\ &=\frac{13}{25}\cdot\frac{\binom{12}{2}}{\binom{24}{2}} +\frac{12}{25}\cdot\frac{\binom{13}{2}}{\binom{24}{2}}...` |
| 424 | 4022-4027 | 0.21 | normalized_width_not_low | bracket | `P(A\|B) =\frac{P(A)P(B\|A)}{P(B)} =\frac{\frac{13}{25}\cdot\frac{\binom{12}{2}}{\binom{24}{2}}}{13/50} =\frac{11}{23}.` |
| 425 | 4033-4039 | 0.13 | inline_unsafe_marker | bracket | `f(x)= \begin{cases} ax^2, & 0\le x\le1,\\ 0, & \text{其他}, \end{cases}` |
| 426 | 4046-4048 | 0.27 | inline_safe | bracket | `\int_0^1 ax^2\,\mathrm dx=1,` |
| 427 | 4052-4055 | 0.32 | normalized_width_not_low | bracket | `P(A)=\int_{1/2}^{1}3x^2\,\mathrm dx =1-\frac18=\frac78.` |
| 428 | 4057-4059 | 0.21 | inline_safe | bracket | `P(\overline B)=\frac18.` |
| 429 | 4061-4066 | 0.36 | normalized_width_not_low | bracket | `P(A\cup\overline B) =P(A)+P(\overline B)-P(A)P(\overline B) =\frac78+\frac18-\frac7{64} =\frac{57}{64}.` |
| 430 | 4079-4081 | 0.13 | inline_safe | bracket | `P=\frac{\binom{51}{4}}{\binom{52}{5}}.` |
| 431 | 4084-4088 | 0.24 | normalized_width_not_low | bracket | `P(A)=P(B)=\frac{\binom{51}{4}}{\binom{52}{5}}, \qquad P(AB)=\frac{\binom{50}{3}}{\binom{52}{5}}.` |
| 432 | 4090-4093 | 0.20 | inline_safe | bracket | `P(A\cup B) =\frac{2\binom{51}{4}-\binom{50}{3}}{\binom{52}{5}}.` |
| 433 | 4096-4099 | 0.20 | inline_safe | bracket | `P(\text{至少有一个对子}) =1-\frac{\binom{13}{5}4^5}{\binom{52}{5}}.` |
| 435 | 4113-4115 | 0.43 | inline_safe | bracket | `P(A)=\frac{16}{33},\qquad P(\overline A)=\frac{17}{33}.` |
| 436 | 4118-4126 | 0.37 | inline_unsafe_marker | bracket | `\begin{aligned} P(B) &=P(A)P(B\|A)+P(\overline A)P(B\|\overline A)\\ &=\frac{16}{33}\cdot\frac{\binom{15}{2}}{\binom{32}{2}} +\frac{17}{33}\cdot\frac{\binom{16}{2}}{\binom{32}{2}}...` |
| 437 | 4129-4134 | 0.21 | normalized_width_not_low | bracket | `P(A\|B) =\frac{P(A)P(B\|A)}{P(B)} =\frac{\frac{16}{33}\cdot\frac{\binom{15}{2}}{\binom{32}{2}}}{5/22} =\frac{14}{31}.` |
| 438 | 4142-4144 | 0.10 | inline_safe | bracket | `n-r-1` |
| 440 | 4152-4157 | 0.29 | normalized_width_not_low | bracket | `P_2 =\frac{\binom{n-2}{r}r!(n-r-2)!}{(n-1)!} =\frac{(n-2)!}{(n-1)!} =\frac1{n-1}.` |
| 444 | 4180-4185 | 0.24 | normalized_width_not_low | bracket | `P(A_2\|B) =\frac{P(A_2)P(B\|A_2)}{P(B)} =\frac{0.35\cdot0.02}{0.0185} =\frac{14}{37}\approx0.378.` |
| 445 | 4195-4198 | 0.35 | normalized_width_not_low | bracket | `A_1=\{\text{乙第一次投中}\},\qquad B_i=\{\text{甲第 }i\text{ 次投中}\},\quad i=1,2.` |
| 446 | 4200-4202 | 0.46 | inline_safe | bracket | `P(B_1)=0.7,\qquad P(\overline B_1)=0.3.` |
| 449 | 4231-4233 | 0.45 | inline_safe | bracket | `A_1=\{\text{笔试及格}\},\qquad A_2=\{\text{口试及格}\}.` |
| 451 | 4240-4248 | 0.35 | inline_unsafe_marker | bracket | `\begin{aligned} P(A_1\cup A_2) &=P(A_1)+P(\overline A_1A_2)\\ &=p+P(A_2\mid \overline A_1)P(\overline A_1)\\ &=p+\frac p2(1-p) =\frac32p-\frac12p^2. \end{aligned}` |
| 452 | 4250-4253 | 0.18 | inline_safe | bracket | `P(A_1\mid A_2) =\frac{P(A_1A_2)}{P(A_2)}.` |
| 453 | 4255-4257 | 0.45 | inline_safe | bracket | `P(A_1A_2)=P(A_2\mid A_1)P(A_1)=p^2,` |
| 455 | 4262-4266 | 0.17 | inline_safe | bracket | `P(A_1\mid A_2) =\frac{p^2}{p(1+p)/2} =\frac{2p}{1+p}.` |
| 456 | 4278-4280 | 0.26 | inline_safe | bracket | `P_1=\frac{8\cdot7}{10\cdot9}=\frac{28}{45}.` |
| 457 | 4283-4285 | 0.30 | inline_safe | bracket | `P_2=\frac{8\cdot2\cdot2}{10\cdot9}=\frac{16}{45}.` |
| 458 | 4295-4298 | 0.48 | normalized_width_not_low | bracket | `A_i=\{\text{第 }i\text{ 次取到红球}\},\quad i=1,2,\qquad B_j=\{\text{取到第 }j\text{ 箱}\},\quad j=1,2.` |
| 462 | 4314-4318 | 0.31 | normalized_width_not_low | bracket | `P(A_2\mid A_1)=\frac{P(A_1A_2)}{P(A_1)} =\frac{19/60}{19/30} =\frac12.` |
| 465 | 4342-4347 | 0.24 | normalized_width_not_low | bracket | `P(A_1\mid B) =\frac{P(A_1)P(B\mid A_1)}{P(B)} =\frac{0.25\cdot0.05}{0.0345} =\frac{25}{69}\approx0.36.` |
| 466 | 4360-4362 | 0.31 | inline_safe | bracket | `P_1=\frac{\binom54 2^4}{\binom{10}{4}}=\frac{8}{21}.` |
| 467 | 4365-4367 | 0.43 | inline_safe | bracket | `P_2=\frac{\binom51\binom42 2^2}{\binom{10}{4}}=\frac47.` |
| 468 | 4370-4372 | 0.32 | inline_safe | bracket | `P_3=\frac{\binom52}{\binom{10}{4}}=\frac1{21}.` |
| 471 | 4390-4394 | 0.45 | normalized_width_not_low | bracket | `P(A\|B_0)=1,\qquad P(A\|B_1)=\frac{\binom{19}{4}}{\binom{20}{4}}=\frac45,\qquad P(A\|B_2)=\frac{\binom{18}{4}}{\binom{20}{4}}=\frac{12}{19}.` |
| 473 | 4401-4406 | 0.24 | normalized_width_not_low | bracket | `P(B_0\|A) =\frac{P(B_0)P(A\|B_0)}{P(A)} =\frac{0.8}{448/475} =\frac{95}{112}\approx0.848.` |
| 474 | 4411-4420 | 0.09 | inline_unsafe_marker | bracket | `\begin{array}{c\|cccc} & Y=-1 & Y=0 & Y=1 & Y=2\\ \hline X=-2 & a & 0 & 0 & 0\\ X=-1 & 0.14 & b & 0 & 0\\ X=0 & 0.01 & 0.02 & 0.03 & 0\\ X=1 & 0.12 & 0.13 & 0.14 & 0.15 \end{array}` |
| 476 | 4432-4434 | 0.15 | inline_safe | bracket | `a+b=0.26.` |
| 478 | 4446-4448 | 0.17 | inline_safe | bracket | `4a+b=0.80.` |
| 479 | 4450-4452 | 0.43 | inline_safe | bracket | `a+b=0.26,\qquad 4a+b=0.80,` |
| 480 | 4454-4456 | 0.33 | inline_safe | bracket | `a=0.18,\qquad b=0.08.` |
| 482 | 4463-4472 | 0.17 | inline_unsafe_marker | bracket | `F_X(x)= \begin{cases} 0, & x<-2,\\ 0.18, & -2\le x<-1,\\ 0.40, & -1\le x<0,\\ 0.46, & 0\le x<1,\\ 1, & x\ge1. \end{cases}` |
| 484 | 4490-4492 | 0.30 | inline_safe | bracket | `\frac{\hat p-p}{\sqrt{p(1-p)/n}}\approx N(0,1).` |
| 485 | 4494-4496 | 0.29 | inline_safe | bracket | `P(\|\hat p-p\|<0.1)>0.99.` |
| 486 | 4498-4500 | 0.35 | inline_safe | bracket | `2\Phi\!\left(\frac{0.1}{\sqrt{p(1-p)/n}}\right)-1>0.99.` |
| 487 | 4502-4504 | 0.29 | inline_safe | bracket | `\frac{0.1}{\sqrt{p(1-p)/n}}\ge 2.575.` |
| 488 | 4506-4508 | 0.30 | inline_safe | bracket | `n\ge \frac{(2.575)^2}{0.1^2}p(1-p).` |
| 489 | 4510-4512 | 0.32 | inline_safe | bracket | `n\ge \frac{(2.575)^2}{0.04}\approx165.77.` |
| 490 | 4514-4516 | 0.10 | inline_safe | bracket | `n=166.` |
| 491 | 4521-4523 | 0.21 | inline_safe | bracket | `\frac{x^2}{a^2}+\frac{y^2}{b^2}\le1` |
| 492 | 4531-4537 | 0.22 | inline_unsafe_marker | bracket | `f(x,y)= \begin{cases} \dfrac1{\pi ab}, & \dfrac{x^2}{a^2}+\dfrac{y^2}{b^2}\le1,\\[6pt] 0, & \text{其他}. \end{cases}` |
| 494 | 4544-4550 | 0.25 | inline_unsafe_marker | bracket | `f_X(x)= \begin{cases} \dfrac2{\pi a}\sqrt{1-\dfrac{x^2}{a^2}}, & \|x\|\le a,\\[6pt] 0, & \text{其他}. \end{cases}` |
| 495 | 4552-4558 | 0.25 | inline_unsafe_marker | bracket | `f_Y(y)= \begin{cases} \dfrac2{\pi b}\sqrt{1-\dfrac{y^2}{b^2}}, & \|y\|\le b,\\[6pt] 0, & \text{其他}. \end{cases}` |
| 496 | 4561-4563 | 0.38 | inline_safe | bracket | `DX=\frac{a^2}{4},\qquad DY=\frac{b^2}{4}.` |
| 497 | 4565-4567 | 0.27 | inline_safe | bracket | `a=12,\qquad b=8.` |
| 499 | 4578-4584 | 0.11 | inline_unsafe_marker | bracket | `f(x,y)= \begin{cases} 2, & (x,y)\in G,\\ 0, & \text{其他}. \end{cases}` |
| 501 | 4596-4602 | 0.11 | inline_unsafe_marker | bracket | `f_X(x)= \begin{cases} 2x, & 0<x<1,\\ 0, & \text{其他}. \end{cases}` |
| 502 | 4605-4607 | 0.45 | inline_safe | bracket | `EX=EY=\int_0^1 2x^2\,\mathrm dx=\frac23,` |
| 503 | 4609-4613 | 0.49 | normalized_width_not_low | bracket | `E(XY)=\int_0^1\int_{1-x}^{1}2xy\,\mathrm dy\,\mathrm dx =\int_0^1 x\bigl[1-(1-x)^2\bigr]\,\mathrm dx =\int_0^1(2x^2-x^3)\,\mathrm dx=\frac5{12}.` |
| 504 | 4615-4618 | 0.41 | normalized_width_not_low | bracket | `\operatorname{Cov}(X,Y)=E(XY)-EX\,EY =\frac5{12}-\frac49=-\frac1{36}.` |
| 506 | 4627-4631 | 0.41 | normalized_width_not_low | bracket | `DU=D(X+Y)=DX+DY+2\operatorname{Cov}(X,Y) =\frac1{18}+\frac1{18}-\frac1{18} =\frac1{18}.` |
| 507 | 4636-4642 | 0.21 | inline_unsafe_marker | bracket | `f(x,y)= \begin{cases} Axy, & 0<x<2,\ 0<y<2,\\ 0, & \text{其他}. \end{cases}` |
| 508 | 4651-4655 | 0.43 | normalized_width_not_low | bracket | `1=\int_0^2\int_0^2 Axy\,\mathrm dy\,\mathrm dx =A\left(\int_0^2 x\,\mathrm dx\right)\left(\int_0^2 y\,\mathrm dy\right) =4A.` |
| 512 | 4679-4681 | 0.38 | inline_safe | bracket | `E(e^{tX+sY})=E(e^{tX})E(e^{sY}).` |
| 513 | 4683-4686 | 0.37 | normalized_width_not_low | bracket | `E(e^{tX})=\int_0^2 \frac{x}{2}e^{tx}\,\mathrm dx =\frac{e^{2t}(2t-1)+1}{2t^2},` |
| 514 | 4688-4690 | 0.35 | inline_safe | bracket | `E(e^{sY})=\frac{e^{2s}(2s-1)+1}{2s^2}.` |
| 517 | 4704-4706 | 0.36 | inline_safe | bracket | `DX=2-\left(\frac43\right)^2=\frac29.` |
| 518 | 4708-4710 | 0.16 | inline_safe | bracket | `\operatorname{Cov}(X,Y)=0.` |
| 521 | 4730-4732 | 0.19 | inline_safe | bracket | `EN=\frac{p}{1-p}=1.` |
| 523 | 4739-4741 | 0.23 | inline_safe | bracket | `E=475+\frac12E.` |
| 524 | 4743-4745 | 0.10 | inline_safe | bracket | `E=950.` |
| 525 | 4757-4759 | 0.18 | inline_safe | bracket | `P(A)=\frac mn.` |
| 528 | 4798-4801 | 0.15 | inline_safe | bracket | `\frac{5}{100}\cdot\frac{95}{99} =\frac{19}{396}.` |
| 529 | 4804-4808 | 0.37 | normalized_width_not_low | bracket | `P(D_1G_2)=P(D_1)P(G_2\|D_1) =0.05\cdot\frac{95}{99} =\frac{19}{396}.` |
| 530 | 4820-4822 | 0.26 | inline_safe | bracket | `0\le P(AB)\le P(A)=0,` |
| 531 | 4824-4826 | 0.29 | inline_safe | bracket | `P(A)P(B)=0\cdot P(B)=0,` |
| 532 | 4828-4830 | 0.21 | inline_safe | bracket | `P(AB)=P(A)P(B),` |
| 534 | 4840-4842 | 0.15 | inline_safe | bracket | `P(A\mid \overline A\cup B).` |
| 535 | 4846-4848 | 0.27 | inline_safe | bracket | `P(B)=0.7-0.3=0.4.` |
| 537 | 4854-4856 | 0.43 | inline_safe | bracket | `P(\overline A\cup B)=P(\overline A)+P(B)-P(\overline A B).` |
| 539 | 4862-4864 | 0.39 | inline_safe | bracket | `P(\overline A\cup B)=0.3+0.4-0.1=0.6.` |
| 540 | 4866-4868 | 0.18 | inline_safe | bracket | `A(\overline A\cup B)=AB,` |
| 541 | 4870-4874 | 0.30 | inline_safe | bracket | `P(A\mid \overline A\cup B)=\frac{P(AB)}{P(\overline A\cup B)} =\frac{0.3}{0.6} =0.5.` |
| 542 | 4884-4888 | 0.23 | normalized_width_not_low | bracket | `A_1=\{\text{甲不及格}\},\quad A_2=\{\text{乙不及格}\},\quad A_3=\{\text{丙不及格}\}.` |
| 545 | 4899-4908 | 0.25 | inline_unsafe_marker | bracket | `\begin{aligned} P(E) &=0.4\cdot0.3\cdot0.5 +0.4\cdot0.7\cdot0.5 +0.6\cdot0.3\cdot0.5\\ &=0.06+0.14+0.09 =0.29. \end{aligned}` |
| 546 | 4911-4913 | 0.34 | inline_safe | bracket | `A_1A_2\overline A_3\cup \overline A_1A_2A_3.` |
| 547 | 4915-4919 | 0.43 | normalized_width_not_low | bracket | `\frac{0.4\cdot0.3\cdot0.5+0.6\cdot0.3\cdot0.5}{0.29} =\frac{0.15}{0.29} =\frac{15}{29}.` |
| 548 | 4924-4926 | 0.15 | inline_safe | bracket | `P(A\mid A\cup \overline B).` |
| 549 | 4930-4932 | 0.26 | inline_safe | bracket | `P(AB)=1-0.8=0.2.` |
| 550 | 4934-4936 | 0.49 | inline_safe | bracket | `P(A\overline B)=P(A)-P(AB)=0.7-0.2=0.5.` |
| 551 | 4938-4941 | 0.42 | normalized_width_not_low | bracket | `P(A\cup\overline B)=P(A)+P(\overline B)-P(A\overline B) =0.7+0.6-0.5=0.8.` |
| 552 | 4943-4948 | 0.16 | normalized_width_not_low | bracket | `P(A\mid A\cup\overline B) =\frac{P(A)}{P(A\cup\overline B)} =\frac{0.7}{0.8} =\frac78.` |
| 553 | 4958-4960 | 0.40 | inline_safe | bracket | `P=\frac4{10}\cdot\frac69=\frac4{15}.` |
| 554 | 4963-4965 | 0.41 | inline_safe | bracket | `P(B)=\frac{\binom62}{\binom{10}2}=\frac{15}{45}=\frac13.` |
| 555 | 4967-4972 | 0.25 | normalized_width_not_low | bracket | `P(A)=1-P(\text{两次都是旧球}) =1-\frac{\binom42}{\binom{10}2} =1-\frac6{45} =\frac{13}{15}.` |
| 556 | 4974-4978 | 0.18 | inline_safe | bracket | `P(B\|A)=\frac{P(B)}{P(A)} =\frac{1/3}{13/15} =\frac5{13}.` |
| 557 | 4988-4990 | 0.14 | inline_safe | bracket | `\binom72=21` |
| 558 | 4994-4996 | 0.22 | inline_safe | bracket | `7-(k+1)=6-k.` |
| 560 | 5002-5007 | 0.11 | inline_unsafe_marker | bracket | `\begin{array}{c\|cccccc} k&0&1&2&3&4&5\\ \hline P(K=k)&\dfrac6{21}&\dfrac5{21}&\dfrac4{21}&\dfrac3{21}&\dfrac2{21}&\dfrac1{21} \end{array}` |
| 562 | 5015-5017 | 0.38 | inline_safe | bracket | `P(K\ge2)=\frac{4+3+2+1}{21}=\frac{10}{21}.` |
| 563 | 5023-5025 | 0.27 | inline_safe | bracket | `P(A)=P(B)=P(C)=\rho.` |
| 564 | 5030-5033 | 0.39 | normalized_width_not_low | bracket | `P(AB)=P(A)P(B)=\rho^2,\qquad P(AC)=P(A)P(C)=\rho^2.` |
| 565 | 5035-5037 | 0.11 | inline_safe | bracket | `AB\cup AC\subset A.` |
| 566 | 5039-5041 | 0.40 | inline_safe | bracket | `P(AB)+P(AC)=P(AB\cup AC)\le P(A),` |
| 567 | 5043-5045 | 0.12 | inline_safe | bracket | `2\rho^2\le \rho.` |
| 568 | 5047-5049 | 0.15 | inline_safe | bracket | `\rho\le \frac12.` |
| 569 | 5053-5055 | 0.17 | inline_safe | bracket | `\Omega=\{1,2,3,4\},` |
| 571 | 5061-5063 | 0.43 | inline_safe | bracket | `P(AB)=P(\{1\})=\frac14=P(A)P(B),` |
| 572 | 5064-5066 | 0.43 | inline_safe | bracket | `P(AC)=P(\{2\})=\frac14=P(A)P(C),` |
| 573 | 5067-5069 | 0.43 | inline_safe | bracket | `P(BC)=P(\{3\})=\frac14=P(B)P(C),` |
| 574 | 5071-5073 | 0.20 | inline_safe | bracket | `\rho_{\max}=\frac12.` |
| 576 | 5155-5157 | 0.23 | inline_safe | bracket | `\{\omega \mid X(\omega) \le x,\ \omega \in \Omega\}` |
| 577 | 5181-5183 | 0.41 | inline_safe | bracket | `F(x) = P\{X \le x\} \quad (-\infty < x < +\infty)` |
| 579 | 5246-5252 | 0.13 | inline_unsafe_marker | bracket | `F(x) = \begin{cases} 0, & x < 0, \\ \dfrac{1}{2}, & 0 \le x < 1, \\ 1 - e^{-x}, & x \ge 1. \end{cases}` |
| 580 | 5297-5302 | 0.14 | inline_unsafe_marker | bracket | `F(x) = \begin{cases} a + b e^{-x}, & x > 0, \\ 0, & x \le 0. \end{cases}` |
| 582 | 5314-5316 | 0.44 | inline_safe | bracket | `F(0) = \lim_{x \to 0^+} F(x) = a + b = 0,` |
| 583 | 5318-5323 | 0.13 | inline_unsafe_marker | bracket | `F(x) = \begin{cases} 1 - e^{-x}, & x > 0, \\ 0, & x \le 0. \end{cases}` |
| 585 | 5334-5336 | 0.38 | inline_safe | bracket | `P\{X = x_i\} = p_i, \quad i = 1, 2, \dots` |
| 586 | 5341-5347 | 0.08 | inline_unsafe_marker | bracket | `\begin{array}{c\|cccc} X & x_1 & x_2 & \cdots \\ \hline P & p_1 & p_2 & \cdots \end{array}` |
| 587 | 5378-5380 | 0.44 | inline_safe | bracket | `F(x) = \int_{-\infty}^{x} f(t)\,\mathrm{d}t \quad (x \in \mathbf{R}),` |
| 589 | 5402-5407 | 0.16 | inline_unsafe_marker | bracket | `f(x) = \begin{cases} 0, & x \text{ 为 } F(x) \text{ 的不可导点}, \\ F'(x), & x \text{ 为 } F(x) \text{ 的可导点}. \end{cases}` |
| 590 | 5420-5426 | 0.11 | inline_unsafe_marker | bracket | `F(x) = \begin{cases} 0, & x < 0, \\ \dfrac{x^3}{2}, & 0 \le x < 1, \\ 1, & x \ge 1, \end{cases}` |
| 591 | 5452-5458 | 0.15 | inline_unsafe_marker | bracket | `F(x) = \begin{cases} 0, & x < 0, \\ Ax^2 + \dfrac{2}{3}x, & 0 \le x < 1, \\ 1, & x \ge 1. \end{cases}` |
| 593 | 5468-5470 | 0.46 | inline_safe | bracket | `f(x) = F'(x) = \frac{2x}{3} + \frac{2}{3}, \quad x \in [0,1),` |
| 594 | 5472-5477 | 0.13 | inline_unsafe_marker | bracket | `f(x) = \begin{cases} \dfrac{2x}{3} + \dfrac{2}{3}, & 0 \le x < 1, \\ 0, & \text{其他}. \end{cases}` |
| 596 | 5485-5491 | 0.11 | inline_unsafe_marker | bracket | `\begin{array}{c\|ccc} X & 1 & 2 & 3 \\ \hline P\{X=k\} & \theta^2 & 2\theta(1-\theta) & (1-\theta)^2 \end{array}` |
| 597 | 5499-5505 | 0.10 | inline_unsafe_marker | bracket | `\begin{array}{c\|ccc} X & 1 & 2 & 3 \\ \hline P\{X=k\} & \dfrac{1}{4} & \dfrac{1}{2} & \dfrac{1}{4} \end{array}` |
| 599 | 5525-5527 | 0.30 | inline_safe | bracket | `\sum_{k=1}^{\infty}P\{X=k\}=1.` |
| 600 | 5534-5541 | 0.14 | inline_unsafe_marker | bracket | `F(x) = \begin{cases} 0, & x<-1, \\ 0.4, & -1 \le x<1, \\ 0.8, & 1 \le x<3, \\ 1, & x \ge 3. \end{cases}` |
| 601 | 5547-5551 | 0.45 | display_environment | env:align* | `P\{X=-1\} &= F(-1) - F(-1^-) = 0.4 - 0 = 0.4, \\ P\{X=1\} &= F(1) - F(1^-) = 0.8 - 0.4 = 0.4, \\ P\{X=3\} &= F(3) - F(3^-) = 1 - 0.8 = 0.2.` |
| 602 | 5553-5559 | 0.07 | inline_unsafe_marker | bracket | `\begin{array}{c\|ccc} X & -1 & 1 & 3 \\ \hline P & 0.4 & 0.4 & 0.2 \end{array}` |
| 604 | 5595-5597 | 0.38 | inline_safe | bracket | `F'(x)=F(x),\qquad F(0)=1.` |
| 606 | 5604-5606 | 0.27 | inline_unsafe_marker | bracket | `F(x) = \begin{cases} e^x, & x < 0, \\ 1, & x \ge 0, \end{cases} \quad f(x) = \begin{cases} e^x, & x \le 0, \\ 0, & x > 0. \end{cases}` |
| 607 | 5609-5615 | 0.08 | inline_unsafe_marker | bracket | `f(x)= \begin{cases} e^x,&x\le 0,\\ 0,&x>0. \end{cases}` |
| 608 | 5624-5629 | 0.16 | inline_unsafe_marker | bracket | `f(x) = \begin{cases} 2\left(1 - \dfrac{1}{x^2}\right), & 1 \le x \le 2, \\ 0, & \text{其他}. \end{cases}` |
| 610 | 5644-5650 | 0.17 | inline_unsafe_marker | bracket | `F(x) = \begin{cases} 0, & x < 1, \\ 2\left(x + \dfrac{1}{x} - 2\right), & 1 \le x < 2, \\ 1, & x \ge 2. \end{cases}` |
| 611 | 5655-5660 | 0.40 | display_environment | env:align* | `&\text{A. } f(x) = \begin{cases} 2(1-\|x\|), & \|x\| \le 1 \\ 0, & \|x\|>1 \end{cases} &&\text{B. } f(x) = \begin{cases} \frac{1}{\sqrt{2\pi}\sigma} e^{-\frac{(x-\mu)^2}{2\sigma^2}}, ...` |
| 612 | 5677-5679 | 0.15 | inline_unsafe_marker | bracket | `f(x) = \begin{cases} A\sin x, & 0 \le x \le \pi \\ 0, & \text{其他} \end{cases}` |
| 615 | 5692-5698 | 0.16 | inline_unsafe_marker | bracket | `F(x) = \begin{cases} 0, & x<0, \\[6pt] \dfrac{1}{2}(1-\cos x), & 0 \le x < \pi, \\[6pt] 1, & x \ge \pi. \end{cases}` |
| 617 | 5736-5738 | 0.48 | inline_safe | bracket | `\int_{-\infty}^{+\infty}\bigl(f_1(x)+f_2(x)\bigr)\,\mathrm dx=2,` |
| 618 | 5742-5744 | 0.45 | inline_safe | bracket | `\lim_{x\to+\infty}\bigl(F_1(x)+F_2(x)\bigr)=2\ne1.` |
| 619 | 5746-5748 | 0.24 | inline_safe | bracket | `F(x)=F_1(x)F_2(x)` |
| 622 | 5792-5799 | 0.11 | inline_unsafe_marker | bracket | `F(x)= \begin{cases} 0, & x<0, \\[6pt] 1-p, & 0\leqslant x<1, \\[6pt] 1, & x\geqslant1. \end{cases}` |
| 624 | 5836-5838 | 0.28 | inline_safe | bracket | `P(X\geqslant1)=1-P(X=0),` |
| 626 | 5846-5854 | 0.46 | inline_unsafe_marker | bracket | `\begin{aligned} P(Y\geqslant1) &=1-P(Y=0)=1-\mathrm{C}_4^0p^0(1-p)^4\\ &=1-\left(\frac{2}{3}\right)^4\\ &=1-\frac{16}{81} =\frac{65}{81}. \end{aligned}` |
| 627 | 5865-5867 | 0.19 | inline_safe | bracket | `DX=10p(1-p).` |
| 628 | 5869-5871 | 0.25 | inline_safe | bracket | `10p(1-p)=\frac52,` |
| 629 | 5873-5875 | 0.22 | inline_safe | bracket | `p(1-p)=\frac14.` |
| 630 | 5877-5879 | 0.23 | inline_safe | bracket | `\left(p-\frac12\right)^2=0,` |
| 631 | 5881-5883 | 0.14 | inline_safe | bracket | `p=\frac12.` |
| 632 | 5888-5890 | 0.31 | inline_safe | bracket | `EX=15,\qquad DX=10,` |
| 633 | 5895-5897 | 0.39 | inline_safe | bracket | `EX=np,\qquad DX=np(1-p).` |
| 634 | 5899-5901 | 0.26 | inline_safe | bracket | `1-p=\frac{10}{15}=\frac23,` |
| 635 | 5903-5905 | 0.18 | inline_safe | bracket | `n=\frac{15}{1/3}=45.` |
| 638 | 5925-5931 | 0.17 | inline_unsafe_marker | bracket | `f(x)= \begin{cases} ax^2+bx+c, & 0<x<1,\\ 0, & \text{其他}, \end{cases}` |
| 639 | 5936-5938 | 0.39 | inline_safe | bracket | `\int_0^1(ax^2+bx+c)\,\mathrm dx=1,` |
| 640 | 5940-5942 | 0.35 | inline_unsafe_marker | bracket | `\frac13a+\frac12b+c=1. \tag{1}` |
| 641 | 5944-5946 | 0.48 | inline_safe | bracket | `\int_0^1x(ax^2+bx+c)\,\mathrm dx=\frac12,` |
| 643 | 5952-5954 | 0.43 | inline_safe | bracket | `EX^2=\frac3{20}+\frac14=\frac25.` |
| 646 | 5964-5966 | 0.49 | inline_safe | bracket | `a=12,\qquad b=-12,\qquad c=3.` |
| 650 | 6002-6004 | 0.45 | inline_safe | bracket | `\mathrm{C}_n^k p^k (1-p)^{n-k} \approx \frac{\lambda^k}{k!} e^{-\lambda}.` |
| 651 | 6020-6022 | 0.28 | inline_safe | bracket | `P\{X=k\}=\frac{\lambda^k}{k!}e^{-\lambda},` |
| 652 | 6024-6026 | 0.31 | inline_safe | bracket | `\frac{\lambda^1}{1!}e^{-\lambda}=\frac{\lambda^2}{2!}e^{-\lambda}.` |
| 653 | 6028-6030 | 0.34 | inline_safe | bracket | `\lambda=\frac{\lambda^2}{2}\implies 1=\frac{\lambda}{2}\implies \lambda=2.` |
| 654 | 6033-6040 | 0.16 | inline_unsafe_marker | bracket | `\begin{aligned} P\{X=4\} &=\frac{2^4}{4!}e^{-2}\\ &=\frac{16}{24}e^{-2} =\frac{2}{3}e^{-2}. \end{aligned}` |
| 659 | 6074-6076 | 0.25 | inline_safe | bracket | `E[(X-1)(X-2)]=1.` |
| 661 | 6085-6089 | 0.21 | normalized_width_not_low | bracket | `E[(X-1)(X-2)] =E(X^2-3X+2) =\lambda^2-2\lambda+2.` |
| 662 | 6091-6093 | 0.20 | inline_safe | bracket | `\lambda^2-2\lambda+2=1,` |
| 663 | 6095-6097 | 0.16 | inline_safe | bracket | `(\lambda-1)^2=0.` |
| 664 | 6099-6101 | 0.07 | inline_safe | bracket | `\lambda=1.` |
| 666 | 6114-6124 | 0.18 | inline_unsafe_marker | bracket | `\begin{array}{c\|cccccc} \hline X & 0 & 1 & 2 & 3 & 4 & 5 \\ \hline P & \dfrac{\mathrm{C}_5^0\mathrm{C}_{15}^8}{\mathrm{C}_{20}^8} & \dfrac{\mathrm{C}_5^1\mathrm{C}_{15}^7}{\math...` |
| 667 | 6137-6140 | 0.37 | normalized_width_not_low | bracket | `P(X=k)=\frac{\binom3k\binom3{3-k}}{\binom63}, \qquad k=0,1,2,3.` |
| 668 | 6142-6148 | 0.10 | inline_unsafe_marker | bracket | `\begin{array}{c\|cccc} X & 0 & 1 & 2 & 3\\ \hline P & \dfrac1{20} & \dfrac9{20} & \dfrac9{20} & \dfrac1{20} \end{array}` |
| 670 | 6156-6158 | 0.20 | inline_safe | bracket | `P(A\|X=k)=\frac{k}{6}.` |
| 671 | 6160-6164 | 0.44 | normalized_width_not_low | bracket | `P(A)=\sum_{k=0}^3P(X=k)P(A\|X=k) =\frac{EX}{6} =\frac{1}{4}.` |
| 672 | 6175-6177 | 0.22 | inline_safe | bracket | `P=\frac{10}{15}=\frac23.` |
| 673 | 6180-6185 | 0.39 | normalized_width_not_low | bracket | `P(AB) =\frac{\binom{10}{3}\binom52\binom74\binom32} {\binom{15}{5}\binom{10}{6}} =\frac{200}{1001}.` |
| 674 | 6188-6192 | 0.36 | normalized_width_not_low | bracket | `P(C)=\frac{\binom{10}{3}\binom52}{\binom{15}{5}}=\frac{400}{1001}, \qquad P(D)=\frac{\binom52\binom{10}{4}}{\binom{15}{6}}=\frac{420}{1001}.` |
| 675 | 6194-6198 | 0.33 | normalized_width_not_low | bracket | `P(C\cup D)=P(C)+P(D)-P(CD) =\frac{400+420-200}{1001} =\frac{620}{1001}.` |
| 676 | 6209-6211 | 0.27 | inline_safe | bracket | `P=\frac9{15}=\frac35.` |
| 677 | 6214-6218 | 0.44 | normalized_width_not_low | bracket | `P=\frac{\binom93\binom61\binom64\binom51} {\binom{15}{4}\binom{11}{5}} =\frac{60}{1001}.` |
| 678 | 6221-6225 | 0.39 | normalized_width_not_low | bracket | `P(C)=\frac{\binom92\binom62}{\binom{15}{4}}=\frac{396}{1001}, \qquad P(D)=\frac{\binom63\binom92}{\binom{15}{5}}=\frac{240}{1001}.` |
| 679 | 6227-6231 | 0.49 | normalized_width_not_low | bracket | `P(CD)=\frac{\binom92\binom62\binom72\binom43} {\binom{15}{4}\binom{11}{5}} =\frac{72}{1001}.` |
| 680 | 6233-6236 | 0.30 | inline_safe | bracket | `P(C\cup D)=\frac{396+240-72}{1001} =\frac{564}{1001}.` |
| 681 | 6247-6249 | 0.27 | inline_safe | bracket | `P=\frac9{15}=\frac35.` |
| 682 | 6252-6256 | 0.44 | normalized_width_not_low | bracket | `P=\frac{\binom93\binom62\binom64\binom42} {\binom{15}{5}\binom{10}{6}} =\frac{180}{1001}.` |
| 683 | 6259-6263 | 0.39 | normalized_width_not_low | bracket | `P(C)=\frac{\binom93\binom62}{\binom{15}{5}}=\frac{420}{1001}, \qquad P(D)=\frac{\binom62\binom94}{\binom{15}{6}}=\frac{378}{1001}.` |
| 684 | 6265-6269 | 0.49 | normalized_width_not_low | bracket | `P(CD)=\frac{\binom93\binom62\binom64\binom42} {\binom{15}{5}\binom{10}{6}} =\frac{180}{1001}.` |
| 685 | 6271-6274 | 0.32 | inline_safe | bracket | `P(C\cup D)=\frac{420+378-180}{1001} =\frac{618}{1001}.` |
| 686 | 6279-6288 | 0.11 | inline_unsafe_marker | bracket | `F(x)= \begin{cases} 0, & x\le0,\\ \dfrac{x}{2}, & 0<x<1,\\ \dfrac23, & 1\le x<2,\\ \dfrac{11}{12}, & 2\le x<3,\\ 1, & x\ge3. \end{cases}` |
| 689 | 6305-6308 | 0.41 | normalized_width_not_low | bracket | `P\{2\le X\le4\}=P\{X=2\}+P\{X=3\} =\frac14+\frac1{12}=\frac13.` |
| 691 | 6319-6328 | 0.11 | inline_unsafe_marker | bracket | `F(x)= \begin{cases} 0, & x\le0,\\ \dfrac{x}{3}, & 0<x<1,\\ \dfrac12, & 1\le x<2,\\ \dfrac34, & 2\le x<3,\\ 1, & x\ge3. \end{cases}` |
| 693 | 6342-6346 | 0.43 | normalized_width_not_low | bracket | `P\left\{X<\frac12\right\}=F\!\left(\frac12\right)=\frac16, \qquad P\{2<X\le3\}=P\{X=3\}=\frac14.` |
| 694 | 6348-6352 | 0.49 | normalized_width_not_low | bracket | `EX=\int_0^1 x\cdot\frac13\,\mathrm dx +1\cdot\frac16+2\cdot\frac14+3\cdot\frac14 =\frac{19}{12}.` |
| 696 | 6371-6373 | 0.41 | inline_safe | bracket | `P(X=k)=A\lambda^k,\qquad k=1,2,\dots` |
| 697 | 6384-6387 | 0.21 | inline_safe | bracket | `\sum_{k=1}^{\infty}A\lambda^k =A\frac{\lambda}{1-\lambda}=1,` |
| 698 | 6389-6391 | 0.13 | inline_safe | bracket | `A=\frac{1-\lambda}{\lambda}.` |
| 699 | 6393-6395 | 0.44 | inline_safe | bracket | `1+A=\frac{1}{\lambda},\qquad \lambda=(1+A)^{-1},` |
| 703 | 6432-6434 | 0.36 | inline_safe | bracket | `P\{\text{继续}\}=P\{8,9,10\}=\frac3{10},` |
| 707 | 6451-6456 | 0.44 | normalized_width_not_low | bracket | `P\{X=i\}P\{Y=j\} =\frac7{10}\left(\frac3{10}\right)^{i-1}\cdot\frac17 =\left(\frac3{10}\right)^{i-1}\frac1{10} =P\{X=i,Y=j\},` |
| 708 | 6460-6462 | 0.44 | inline_safe | bracket | `E(X-1)=EX-1=\frac{10}{7}-1=\frac37.` |
| 709 | 6464-6466 | 0.28 | inline_safe | bracket | `EY=\frac{1+2+\cdots+7}{7}=4.` |
| 711 | 6480-6483 | 0.49 | normalized_width_not_low | bracket | `P\{X=2m-1\}=0.8(0.2)^{m-1}(0.5)^{m-1} =0.8(0.1)^{m-1},\qquad m=1,2,\dots.` |
| 712 | 6485-6488 | 0.37 | normalized_width_not_low | bracket | `P\{X=2m\}=(0.2)^m(0.5)^{m} =(0.1)^m,\qquad m=1,2,\dots.` |
| 713 | 6490-6496 | 0.26 | inline_unsafe_marker | bracket | `P\{X=k\}= \begin{cases} 0.8(0.1)^{m-1}, & k=2m-1,\ m=1,2,\dots,\\ (0.1)^m, & k=2m,\ m=1,2,\dots. \end{cases}` |
| 714 | 6499-6501 | 0.46 | inline_safe | bracket | `Y=1+2+\cdots+(X-1)=\frac{X(X-1)}2.` |
| 716 | 6511-6514 | 0.49 | normalized_width_not_low | bracket | `\sum_{m=1}^{\infty}m r^m=\frac{r}{(1-r)^2},\qquad \sum_{m=1}^{\infty}m^2 r^m=\frac{r(1+r)}{(1-r)^3},` |
| 717 | 6516-6518 | 0.12 | inline_safe | bracket | `EY=\frac{14}{27}.` |
| 721 | 6560-6562 | 0.33 | inline_safe | bracket | `T = \min\{X_1,X_2,X_3,X_4\}.` |
| 722 | 6565-6567 | 0.41 | inline_safe | bracket | `F_X(x) = 1-e^{-0.2x},\quad x\geqslant0.` |
| 724 | 6577-6583 | 0.17 | inline_unsafe_marker | bracket | `F_T(t)= \begin{cases} 0, & t<0, \\[4pt] 1-e^{-0.8t}, & t\geqslant0. \end{cases}` |
| 725 | 6604-6606 | 0.37 | inline_safe | bracket | `F(-a)=\int_{-\infty}^{-a}f(x)\,\mathrm{d}x.` |
| 726 | 6608-6617 | 0.33 | inline_unsafe_marker | bracket | `\begin{aligned} F(-a) &=\int_{+\infty}^{a}f(-t)(-\,\mathrm{d}t) =\int_{a}^{+\infty}f(-t)\,\mathrm{d}t \\ &=\int_{a}^{+\infty}f(t)\,\mathrm{d}t =1-\int_{-\infty}^{a}f(t)\,\mathrm...` |
| 727 | 6621-6623 | 0.49 | inline_safe | bracket | `P(\|X\|<a)=P(-a<X<a)=F(a)-F(-a).` |
| 728 | 6625-6627 | 0.48 | inline_safe | bracket | `P(\|X\|<a)=F(a)-[1-F(a)]=2F(a)-1.` |
| 731 | 6644-6649 | 0.10 | inline_unsafe_marker | bracket | `f(x) = \begin{cases} \frac{1}{b-a}, & a < x < b, \\ 0, & \text{其他}, \end{cases}` |
| 732 | 6651-6657 | 0.11 | inline_unsafe_marker | bracket | `F(x) = \begin{cases} 0, & x < a, \\ \frac{x-a}{b-a}, & a \le x < b, \\ 1, & x \ge b. \end{cases}` |
| 734 | 6681-6687 | 0.11 | inline_unsafe_marker | bracket | `F(x) = \begin{cases} 0, & x < 1, \\ \frac{5 + 2x}{12}, & 1 \le x < 4, \\ 1, & x \ge 4. \end{cases}` |
| 735 | 6697-6699 | 0.33 | inline_safe | bracket | `P\{X>4\}=\frac{b-4}{b-a}=\frac12.` |
| 736 | 6701-6703 | 0.45 | inline_safe | bracket | `2(b-4)=b-a \quad \Longrightarrow \quad a+b=8.` |
| 738 | 6710-6712 | 0.48 | inline_safe | bracket | `4(3-a)=b-a \quad \Longrightarrow \quad b=12-3a.` |
| 739 | 6715-6720 | 0.14 | inline_unsafe_marker | bracket | `\begin{cases} a+b=8,\\ b=12-3a, \end{cases}` |
| 741 | 6739-6741 | 0.43 | inline_safe | bracket | `P\{\text{方程有实根}\}=P(X\le 1)=\frac{1-0}{8}=\frac{1}{8}.` |
| 742 | 6749-6751 | 0.20 | inline_safe | bracket | `Y\sim B\!\left(4,\frac18\right).` |
| 744 | 6766-6768 | 0.28 | inline_safe | bracket | `P\{X>3\} = \frac{5-3}{5-2} = \frac{2}{3}.` |
| 746 | 6779-6784 | 0.11 | inline_unsafe_marker | bracket | `f(x) = \begin{cases} \lambda e^{-\lambda x}, & x > 0, \\ 0, & x \le 0, \end{cases}` |
| 747 | 6786-6791 | 0.14 | inline_unsafe_marker | bracket | `F(x) = \begin{cases} 1 - e^{-\lambda x}, & x \ge 0, \\ 0, & x < 0. \end{cases}` |
| 748 | 6796-6798 | 0.33 | inline_safe | bracket | `P\{X > s + t \mid X > s\} = P\{X > t\}.` |
| 749 | 6803-6806 | 0.45 | display_environment | env:align* | `P\{X > s + t \mid X > s\} &= \frac{P\{X > s + t\}}{P\{X > s\}} \\ &= \frac{e^{-\lambda(s+t)}}{e^{-\lambda s}} = e^{-\lambda t} = P\{X > t\}.` |
| 752 | 6838-6844 | 0.15 | inline_unsafe_marker | bracket | `f(x)= \begin{cases} Ae^{-x/100}, & x>0,\\ 0, & \text{其他}. \end{cases}` |
| 753 | 6851-6853 | 0.44 | inline_safe | bracket | `1=\int_0^\infty Ae^{-x/100}\,\mathrm dx=100A,` |
| 754 | 6855-6857 | 0.25 | inline_safe | bracket | `A=\frac1{100}=0.01.` |
| 755 | 6859-6863 | 0.49 | normalized_width_not_low | bracket | `P(200<X<300) =\int_{200}^{300}\frac1{100}e^{-x/100}\,\mathrm dx =e^{-2}-e^{-3}.` |
| 757 | 6870-6872 | 0.20 | inline_safe | bracket | `Y\sim B(5,e^{-3}).` |
| 762 | 6914-6920 | 0.31 | inline_unsafe_marker | bracket | `\begin{aligned} P\{\max\{X_1,X_2\}>5\} &= 1-P\{X_1\leqslant5, X_2\leqslant5\} \\ &= 1-\left(1-e^{-\lambda\cdot5}\right)^2 \\ &= 1-\left(1-e^{-\frac{5}{4}}\right)^2. \end{aligned}` |
| 763 | 6926-6932 | 0.08 | inline_unsafe_marker | bracket | `f(x)= \begin{cases} e^{-x}, & x\geqslant0, \\[4pt] 0, & x<0, \end{cases}` |
| 764 | 6937-6939 | 0.29 | inline_safe | bracket | `\{X_1 < T,\ X_1+X_2 > T\}.` |
| 766 | 6953-6955 | 0.17 | inline_safe | bracket | `X+Y\sim E(2\lambda).` |
| 767 | 6962-6964 | 0.48 | inline_safe | bracket | `f_{X+Y}(z)=\lambda^2 z e^{-\lambda z},\qquad z>0.` |
| 772 | 7026-7028 | 0.20 | inline_safe | bracket | `F(-x)\ne 1-F(x).` |
| 773 | 7035-7037 | 0.21 | inline_safe | bracket | `F(x)=\Phi\left(\frac{x-\mu}{\sigma}\right).` |
| 774 | 7039-7041 | 0.21 | inline_safe | bracket | `F(-x)=1-F(x).` |
| 775 | 7050-7052 | 0.28 | inline_safe | bracket | `P(X<\mu)=P(X>\mu)=\frac{1}{2}.` |
| 776 | 7054-7056 | 0.11 | inline_safe | bracket | `C=\mu=3.` |
| 779 | 7075-7077 | 0.16 | inline_safe | bracket | `Z=X-2Y+1` |
| 780 | 7082-7084 | 0.41 | inline_safe | bracket | `EZ=EX-2EY+1=2-4+1=-1,` |
| 781 | 7086-7088 | 0.40 | inline_safe | bracket | `DZ=DX+4DY=0.2+4\times0.2=1,` |
| 782 | 7090-7092 | 0.17 | inline_safe | bracket | `Z\sim N(-1,1).` |
| 783 | 7094-7097 | 0.46 | normalized_width_not_low | bracket | `f_Z(z)=\frac1{\sqrt{2\pi}}\exp\!\left\{-\frac{(z+1)^2}{2}\right\}, \qquad -\infty<z<+\infty.` |
| 784 | 7108-7110 | 0.25 | inline_safe | bracket | `Z=\frac{X-\mu}{\sigma}\sim N(0,1),` |
| 785 | 7112-7120 | 0.29 | inline_unsafe_marker | bracket | `\begin{aligned} P\{\|X-\mu\|<1\} &=P\left\{-1<X-\mu<1\right\}\\ &=P\left\{-\frac{1}{\sigma}<\frac{X-\mu}{\sigma}<\frac{1}{\sigma}\right\}\\ &=P\left\{-\frac{1}{\sigma}<Z<\frac{1}{...` |
| 786 | 7123-7125 | 0.04 | inline_safe | bracket | `\frac{1}{\sigma}` |
| 787 | 7127-7129 | 0.07 | inline_safe | bracket | `\Phi\left(\frac{1}{\sigma}\right)` |
| 788 | 7131-7133 | 0.13 | inline_safe | bracket | `2\Phi\left(\frac{1}{\sigma}\right)-1` |
| 789 | 7148-7150 | 0.36 | inline_safe | bracket | `P\{\|X\|<x\}=P\{-x<X<x\}=\alpha.` |
| 790 | 7154-7156 | 0.21 | inline_safe | bracket | `\Phi(x)-\Phi(-x)=\alpha,` |
| 791 | 7158-7160 | 0.16 | inline_safe | bracket | `2\Phi(x)-1=\alpha,` |
| 792 | 7162-7164 | 0.17 | inline_safe | bracket | `\Phi(x)=\frac{1+\alpha}{2}.` |
| 793 | 7166-7168 | 0.33 | inline_safe | bracket | `P\{X>x\}=1-\Phi(x)=\frac{1-\alpha}{2}.` |
| 795 | 7186-7189 | 0.31 | normalized_width_not_low | bracket | `\Rightarrow \Phi\left(\frac{1}{\sigma_1}\right)>\Phi\left(\frac{1}{\sigma_2}\right)\implies \frac{1}{\sigma_1}>\frac{1}{\sigma_2} \Rightarrow \sigma_1<\sigma_2.` |
| 824 | 7392-7394 | 0.33 | inline_safe | bracket | `D(X) = \frac{\sigma^2}{\sqrt{2\pi}} \cdot \sqrt{2\pi} = \sigma^2.` |
| 829 | 7433-7439 | 0.15 | inline_unsafe_marker | bracket | `f_Z(z) = \begin{cases} \dfrac{1}{\lambda}z^{\frac{1}{\lambda}-1}, & 0<z<1, \\[6pt] 0, & \text{其他}. \end{cases}` |
| 832 | 7463-7470 | 0.13 | inline_unsafe_marker | bracket | `F(x)= \begin{cases} 0, & x<0, \\ \dfrac{1}{2}, & 0\leqslant x<1, \\ 1-e^{-x}, & x\geqslant1, \end{cases}` |
| 833 | 7475-7480 | 0.39 | inline_unsafe_marker | bracket | `\begin{aligned} P\{0\leqslant X\leqslant1\}&=F(1)-F(0^-)=1-e^{-1}; \\ P\{0<X<1\}&=F(1^-)-F(0)=\frac{1}{2}-\frac{1}{2}=0. \end{aligned}` |
| 834 | 7485-7493 | 0.14 | inline_unsafe_marker | bracket | `F(x)= \begin{cases} 0, & x<-1, \\ 0.4, & -1\leqslant x<2, \\ 0.8, & 2\leqslant x<3, \\ 1, & x\geqslant3, \end{cases}` |
| 837 | 7505-7507 | 0.49 | inline_safe | bracket | `P\{X=3\}=F(3)-F(3^-)=1-0.8=0.2.` |
| 839 | 7521-7527 | 0.10 | inline_unsafe_marker | bracket | `f(x)= \begin{cases} \dfrac{A}{x^2}, & x>100, \\[6pt] 0, & x\leqslant100, \end{cases}` |
| 840 | 7533-7535 | 0.49 | inline_safe | bracket | `A\left[-\frac{1}{x}\right]_{100}^{+\infty} = \frac{A}{100} = 1 \Rightarrow A=100.` |
| 843 | 7543-7545 | 0.46 | inline_safe | bracket | `P\{X=1000\}=0 \quad (\text{连续型随机变量单点概率为0}).` |
| 845 | 7551-7557 | 0.12 | inline_unsafe_marker | bracket | `F(x)= \begin{cases} 0, & x<100, \\[6pt] 1-\dfrac{100}{x}, & x\geqslant100. \end{cases}` |
| 846 | 7563-7570 | 0.15 | inline_unsafe_marker | bracket | `F(x)= \begin{cases} 0, & x<-a, \\[6pt] A+B\arcsin\dfrac{x}{a}, & -a\leqslant x\leqslant a, \\[6pt] 1, & x\geqslant a, \end{cases}` |
| 848 | 7583-7589 | 0.19 | inline_unsafe_marker | bracket | `f(x) = F'(x) = \begin{cases} \dfrac{1}{\pi\sqrt{a^2-x^2}}, & -a<x<a, \\[6pt] 0, & \text{其他}. \end{cases}` |
| 850 | 7599-7605 | 0.10 | inline_unsafe_marker | bracket | `f(x)= \begin{cases} \dfrac{3}{8}x^2, & 0<x<2, \\[6pt] 0, & \text{其他}. \end{cases}` |
| 854 | 7627-7634 | 0.11 | inline_unsafe_marker | bracket | `f(x)= \begin{cases} x, & 0\leqslant x<1, \\[6pt] 2-x, & 1\leqslant x<2, \\[6pt] 0, & \text{其他}. \end{cases}` |
| 855 | 7642-7644 | 0.34 | inline_safe | bracket | `F(x) = \int_0^x t\,dt = \frac{x^2}{2};` |
| 857 | 7652-7660 | 0.20 | inline_unsafe_marker | bracket | `F(x)= \begin{cases} 0, & x<0, \\[6pt] \dfrac{x^2}{2}, & 0\leqslant x<1, \\[6pt] -\dfrac{x^2}{2}+2x-1, & 1\leqslant x<2, \\[6pt] 1, & x\geqslant2. \end{cases}` |
| 858 | 7665-7687 | 0.29 | inline_unsafe_marker | bracket | `\begin{aligned} &\text{A. } F(x)= \begin{cases} 0, & x<-1, \\[4pt] \dfrac{1}{3}, & -1\leqslant x\leqslant2, \\[4pt] 1, & x>2, \end{cases} &&\text{B. } F(x)= \begin{cases} 0, & x...` |
| 859 | 7702-7709 | 0.20 | inline_unsafe_marker | bracket | `F(x)= \begin{cases} A_1, & x<-a, \\[4pt] A_2+A_3\arctan\dfrac{x}{a}, & x\in[-a,a], \\[6pt] A_4, & x>a, \end{cases}` |
| 862 | 7731-7737 | 0.18 | inline_unsafe_marker | bracket | `f(x)=F'(x)= \begin{cases} \dfrac{2a}{\pi(x^2+a^2)}, & -a\leqslant x\leqslant a, \\[6pt] 0, & \text{其他}. \end{cases}` |
| 863 | 7739-7744 | 0.38 | inline_unsafe_marker | bracket | `\begin{cases} \Delta=X^2-\dfrac{a^2}{4}\geqslant0, \\[4pt] X<0 \quad (\text{由韦达定理，根的和}=-X>0). \end{cases}` |
| 867 | 7790-7792 | 0.38 | inline_safe | bracket | `P\{X = x_i\} = p_i,\quad i=1,2,\dots` |
| 868 | 7794-7796 | 0.41 | inline_safe | bracket | `P\{Y = g(x_i)\} = p_i,\quad i=1,2,\dots` |
| 869 | 7798-7800 | 0.13 | inline_unsafe_marker | bracket | `Y \sim \begin{pmatrix} g(x_1) & g(x_2) & \cdots \\ p_1 & p_2 & \cdots \end{pmatrix}.` |
| 873 | 7846-7848 | 0.21 | inline_safe | bracket | `f_Y(y) = F_Y'(y).` |
| 874 | 7862-7867 | 0.25 | inline_unsafe_marker | bracket | `f_Y(y) = \begin{cases} f_X[h(y)] \cdot \|h'(y)\|, & \alpha < y < \beta, \\ 0, & \text{其他}, \end{cases}` |
| 877 | 7880-7882 | 0.46 | inline_safe | bracket | `f_Y(y) = F_Y'(y) = f_X[h(y)] \cdot h'(y).` |
| 879 | 7902-7904 | 0.40 | inline_safe | bracket | `F_Y(y) = P\{Y \le y\} = P\{g(X) \le y\}.` |
| 880 | 7912-7917 | 0.17 | inline_unsafe_marker | bracket | `f_X(x) = \begin{cases} 1, & -\dfrac{1}{2} < x < \dfrac{1}{2}, \\[6pt] 0, & \text{其他}, \end{cases}` |
| 882 | 7935-7937 | 0.22 | inline_safe | bracket | `\left(a-\dfrac{b}{2},\ a+\dfrac{b}{2}\right).` |
| 884 | 7946-7948 | 0.36 | inline_safe | bracket | `f_Y(y) = f_X\left(\frac{y-a}{b}\right) \cdot \frac{1}{\|b\|}.` |
| 885 | 7950-7955 | 0.27 | inline_unsafe_marker | bracket | `f_Y(y) = \begin{cases} \dfrac{1}{\|b\|}, & a - \dfrac{\|b\|}{2} < y < a + \dfrac{\|b\|}{2}, \\[8pt] 0, & \text{其他}. \end{cases}` |
| 887 | 7962-7967 | 0.12 | inline_unsafe_marker | bracket | `f_Y(y) = \begin{cases} \dfrac{1}{\sqrt{y}}, & 0 < y < \dfrac{1}{4}, \\[6pt] 0, & \text{其他}. \end{cases}` |
| 889 | 7973-7978 | 0.13 | inline_unsafe_marker | bracket | `f_Y(y) = \begin{cases} 2, & 0 \le y < \dfrac{1}{2}, \\[6pt] 0, & \text{其他}. \end{cases}` |
| 890 | 7986-7992 | 0.13 | inline_unsafe_marker | bracket | `f_X(x)= \begin{cases} \dfrac14, & -2<x<2,\\ 0, & \text{其他}. \end{cases}` |
| 891 | 7994-7998 | 0.43 | normalized_width_not_low | bracket | `f_Y(y)=\frac{f_X(-\sqrt y)}{2\sqrt y}+\frac{f_X(\sqrt y)}{2\sqrt y} =\frac{1/4}{2\sqrt y}+\frac{1/4}{2\sqrt y} =\frac{1}{4\sqrt y}.` |
| 892 | 8000-8006 | 0.11 | inline_unsafe_marker | bracket | `f_Y(y)= \begin{cases} \dfrac{1}{4\sqrt y}, & 0<y<4,\\[6pt] 0, & \text{其他}. \end{cases}` |
| 894 | 8021-8023 | 0.46 | inline_safe | bracket | `P\{Y=0\} = P\{X^2=0\} = P\{X=0\} = \frac{1}{2}.` |
| 896 | 8031-8033 | 0.10 | inline_unsafe_marker | bracket | `Y \sim \begin{pmatrix} 0 & 1 \\[4pt] \dfrac{1}{2} & \dfrac{1}{2} \end{pmatrix}.` |
| 898 | 8056-8062 | 0.11 | inline_unsafe_marker | bracket | `F_Y(y) = \begin{cases} 0, & y < 0, \\ y, & 0 \le y < 1, \\ 1, & y \ge 1, \end{cases}` |
| 901 | 8092-8097 | 0.23 | inline_unsafe_marker | bracket | `f_X(x) = F'_X(x) = \begin{cases} 1, & 0 < x < 1, \\[4pt] 0, & \text{其他}. \end{cases}` |
| 905 | 8119-8124 | 0.14 | inline_unsafe_marker | bracket | `f_Z(z) = \begin{cases} \dfrac{2}{(1+z)^2}, & z > 1, \\[6pt] 0, & \text{其他}. \end{cases}` |
| 906 | 8129-8135 | 0.13 | inline_unsafe_marker | bracket | `f_X(x) = \begin{cases} \dfrac{1}{2}, & -1 < x < 0, \\[6pt] \dfrac{1}{4}, & 0 \le x < 2, \\[6pt] 0, & \text{其他}, \end{cases}` |
| 907 | 8143-8149 | 0.44 | inline_unsafe_marker | bracket | `\begin{aligned} F_Y(y) &= P\{-\sqrt{y} \le X \le \sqrt{y}\} \\ &= P\{-\sqrt{y} \le X < 0\} + P\{0 \le X \le \sqrt{y}\} \\ &= \frac{1}{2}\sqrt{y} + \frac{1}{4}\sqrt{y} = \frac{3}...` |
| 909 | 8159-8165 | 0.11 | inline_unsafe_marker | bracket | `f_Y(y) = \begin{cases} \dfrac{3}{8\sqrt{y}}, & 0 < y < 1, \\[6pt] \dfrac{1}{8\sqrt{y}}, & 1 \le y < 4, \\[6pt] 0, & \text{其他}. \end{cases}` |
| 911 | 8185-8192 | 0.11 | inline_unsafe_marker | bracket | `F_Y(y)= \begin{cases} 0, & y<1, \\[6pt] \dfrac{1}{3}, & 1\leqslant y<2, \\[6pt] 1, & y\geqslant2. \end{cases}` |
| 912 | 8203-8205 | 0.21 | inline_safe | bracket | `\frac{\mathrm{d}x}{\mathrm{d}y} = \frac{1}{2(1-y)}.` |
| 914 | 8213-8218 | 0.11 | inline_unsafe_marker | bracket | `f_Y(y) = \begin{cases} 1, & 0 < y < 1, \\[4pt] 0, & \text{其他}. \end{cases}` |
| 917 | 8243-8248 | 0.21 | inline_unsafe_marker | bracket | `f_Y(y) = \begin{cases} \dfrac{1}{\sqrt{8\pi}} e^{-\frac{y^2}{32}}, & y > 0, \\[6pt] 0, & y \le 0. \end{cases}` |
| 919 | 8263-8267 | 0.21 | display_environment | env:align* | `F_Y(y) &= P\{Y \le y\} \\ &= P\{1-\sqrt[3]{X} \le y\} \\ &= P\{\sqrt[3]{X} \ge 1-y\}` |
| 924 | 8302-8304 | 0.40 | inline_safe | bracket | `f_Y(y) = F_Y'(y) = f_X\left(\frac{y}{2}\right) \cdot \frac{1}{2}` |
| 927 | 8327-8329 | 0.21 | inline_safe | bracket | `\left\|\frac{\mathrm dx}{\mathrm dy}\right\|=\frac12.` |
| 928 | 8331-8335 | 0.38 | normalized_width_not_low | bracket | `f_Y(y)=f_X\left(\frac y2\right)\cdot\frac12 =\frac{1}{\pi\left(1+\frac{y^2}{4}\right)}\cdot\frac12 =\frac{2}{\pi(4+y^2)}.` |
| 931 | 8355-8361 | 0.33 | inline_unsafe_marker | bracket | `f_Y(y) = \begin{cases} \dfrac{1}{2\sqrt{\pi(y-1)}}\exp\left\{-\dfrac{y-1}{4}\right\}, & y>1, \\[8pt] 0, & y\leqslant1. \end{cases}` |
| 932 | 8369-8374 | 0.44 | display_environment | env:align* | `F_X(x) &= \int_{-\infty}^{x} \frac{e^t}{(1+e^t)^2}\,\mathrm{d}t \\ &= \left[-\frac{1}{1+e^t}\right]_{-\infty}^{x} \\ &= \left(-\frac{1}{1+e^x}\right) - \left(-\frac{1}{1+0}\righ...` |
| 934 | 8385-8387 | 0.36 | inline_safe | bracket | `F_Y(y) = \frac{e^{\ln y}}{1+e^{\ln y}} = \frac{y}{1+y}.` |
| 936 | 8395-8401 | 0.14 | inline_unsafe_marker | bracket | `f_Y(y)= \begin{cases} \dfrac{1}{(1+y)^2}, & y>0, \\[8pt] 0, & y\leqslant0. \end{cases}` |
| 937 | 8411-8417 | 0.13 | inline_unsafe_marker | bracket | `f_X(x)= \begin{cases} \dfrac{1}{3}, & -1<x<2, \\[6pt] 0, & \text{其他}. \end{cases}` |
| 940 | 8433-8440 | 0.11 | inline_unsafe_marker | bracket | `f_Y(y)= \begin{cases} \dfrac{2}{3}, & 0<y<1, \\[6pt] \dfrac{1}{3}, & 1\leqslant y<2, \\[6pt] 0, & \text{其他}. \end{cases}` |
| 941 | 8501-8504 | 0.49 | normalized_width_not_low | bracket | `P(X=1)=P(X=-1)=\frac12,\qquad P(Y=1)=P(Y=-1)=\frac12.` |
| 942 | 8515-8523 | 0.49 | inline_unsafe_marker | bracket | `\begin{aligned} P(X=Y) &=P(X=1,Y=1)+P(X=-1,Y=-1)\\ &=P(X=1)P(Y=1)+P(X=-1)P(Y=-1)\\ &=\frac12\cdot\frac12+\frac12\cdot\frac12 =\frac12. \end{aligned}` |
| 943 | 8529-8532 | 0.49 | normalized_width_not_low | bracket | `P(X=1)=P(X=-1)=\frac12,\qquad P(Y=1)=P(Y=-1)=\frac12.` |
| 944 | 8543-8551 | 0.49 | inline_unsafe_marker | bracket | `\begin{aligned} P(X=Y) &=P(X=1,Y=1)+P(X=-1,Y=-1)\\ &=P(X=1)P(Y=1)+P(X=-1)P(Y=-1)\\ &=\frac12\cdot\frac12+\frac12\cdot\frac12 =\frac12. \end{aligned}` |
| 945 | 8566-8568 | 0.43 | inline_safe | bracket | `E(X)=np,\qquad D(X)=np(1-p).` |
| 946 | 8570-8572 | 0.20 | inline_safe | bracket | `np(1-p)=1.44.` |
| 947 | 8574-8576 | 0.24 | inline_safe | bracket | `1-p=\frac{1.44}{2.4}=0.6,` |
| 948 | 8578-8580 | 0.37 | inline_safe | bracket | `p=0.4,\qquad n=\frac{2.4}{0.4}=6.` |
| 949 | 8589-8591 | 0.15 | inline_safe | bracket | `\binom53=10.` |
| 950 | 8595-8597 | 0.43 | inline_safe | bracket | `P(X=1)=\frac{\binom42}{\binom53}=\frac{6}{10}=\frac35.` |
| 951 | 8600-8602 | 0.32 | inline_safe | bracket | `P(X=2)=\frac{\binom32}{\binom53}=\frac{3}{10}.` |
| 952 | 8605-8607 | 0.32 | inline_safe | bracket | `P(X=3)=\frac{1}{\binom53}=\frac{1}{10}.` |
| 953 | 8610-8616 | 0.10 | inline_unsafe_marker | bracket | `\begin{array}{c\|ccc} X & 1 & 2 & 3\\ \hline P & \dfrac35 & \dfrac3{10} & \dfrac1{10} \end{array}.` |
| 954 | 8621-8627 | 0.13 | inline_unsafe_marker | bracket | `f(x)= \begin{cases} 1-\|x\|, & -1<x<1,\\ 0, & \text{其他}. \end{cases}` |
| 955 | 8632-8634 | 0.10 | inline_safe | bracket | `1<Y<2.` |
| 956 | 8637-8646 | 0.45 | inline_unsafe_marker | bracket | `\begin{aligned} F_Y(y) &=P(X^2+1\le y) =P(\|X\|\le \sqrt{y-1})\\ &=\int_{-\sqrt{y-1}}^{\sqrt{y-1}}(1-\|x\|)\,\mathrm{d}x\\ &=2\int_0^{\sqrt{y-1}}(1-x)\,\mathrm{d}x\\ &=2\sqrt{y-1}-(...` |
| 957 | 8648-8655 | 0.22 | inline_unsafe_marker | bracket | `F_Y(y)= \begin{cases} 0, & y\le 1,\\ 2\sqrt{y-1}-(y-1), & 1<y<2,\\ 1, & y\ge 2. \end{cases}` |
| 958 | 8658-8660 | 0.27 | inline_safe | bracket | `f_Y(y)=\frac{1}{\sqrt{y-1}}-1.` |
| 959 | 8662-8668 | 0.16 | inline_unsafe_marker | bracket | `f_Y(y)= \begin{cases} \dfrac{1}{\sqrt{y-1}}-1, & 1<y<2,\\ 0, & \text{其他}. \end{cases}` |
| 960 | 8676-8678 | 0.21 | inline_safe | bracket | `F(x)=\frac{a+be^x}{3+e^x}.` |
| 962 | 8693-8695 | 0.33 | inline_safe | bracket | `\lim_{x\to-\infty}F(x)=\frac{a}{3}=0,` |
| 963 | 8699-8701 | 0.31 | inline_safe | bracket | `\lim_{x\to+\infty}F(x)=b=1,` |
| 964 | 8703-8705 | 0.37 | inline_safe | bracket | `F(0)=\frac{0+1}{3+1}=\frac14=0.25.` |
| 966 | 8723-8727 | 0.38 | normalized_width_not_low | bracket | `E(X)=5\cdot\frac35+2\cdot\frac25 =3+\frac45 =3.8.` |
| 967 | 8735-8737 | 0.43 | inline_safe | bracket | `E(\zeta)=np,\qquad D(\zeta)=np(1-p).` |
| 968 | 8739-8741 | 0.19 | inline_safe | bracket | `np(1-p)=1.2.` |
| 969 | 8743-8745 | 0.23 | inline_safe | bracket | `1-p=\frac{1.2}{3}=0.4,` |
| 970 | 8747-8749 | 0.16 | inline_safe | bracket | `n=\frac{3}{0.6}=5.` |
| 971 | 8757-8759 | 0.21 | inline_safe | bracket | `D(\zeta)=\sigma^2(\zeta)=4.` |
| 972 | 8761-8763 | 0.30 | inline_safe | bracket | `D(\zeta)=E(\zeta^2)-[E(\zeta)]^2,` |
| 973 | 8765-8767 | 0.46 | inline_safe | bracket | `E(\zeta^2)=D(\zeta)+[E(\zeta)]^2=4+25=29.` |
| 975 | 8779-8781 | 0.33 | inline_safe | bracket | `x^2+2x+2=(x+1)^2+1.` |
| 976 | 8783-8787 | 0.42 | normalized_width_not_low | bracket | `1=\int_{-\infty}^{+\infty}\frac{a}{(x+1)^2+1}\,\mathrm{d}x =a\left[\arctan(x+1)\right]_{-\infty}^{+\infty} =a\pi,` |
| 977 | 8789-8791 | 0.14 | inline_safe | bracket | `a=\frac1\pi.` |
| 978 | 8794-8802 | 0.37 | inline_unsafe_marker | bracket | `\begin{aligned} P(\zeta\ge0) &=\int_0^{+\infty}\frac{1/\pi}{(x+1)^2+1}\,\mathrm{d}x\\ &=\frac1\pi\left[\arctan(x+1)\right]_{0}^{+\infty}\\ &=\frac1\pi\left(\frac\pi2-\frac\pi4\r...` |
| 979 | 8807-8813 | 0.15 | inline_unsafe_marker | bracket | `f(x)= \begin{cases} \dfrac{A}{1+x}, & 0\le x\le 3,\\ 0, & x<0\ \text{或}\ x>3. \end{cases}` |
| 980 | 8821-8824 | 0.26 | inline_safe | bracket | `1=\int_0^3\frac{A}{1+x}\,\mathrm{d}x =A\ln4,` |
| 981 | 8826-8828 | 0.17 | inline_safe | bracket | `A=\frac1{\ln4}.` |
| 982 | 8831-8836 | 0.34 | normalized_width_not_low | bracket | `P(\zeta<1)=\int_0^1\frac{A}{1+x}\,\mathrm{d}x =A\ln2 =\frac{\ln2}{\ln4} =\frac12.` |
| 983 | 8839-8848 | 0.38 | inline_unsafe_marker | bracket | `\begin{aligned} E(\zeta) &=\int_0^3 x\frac{A}{1+x}\,\mathrm{d}x\\ &=A\int_0^3\left(1-\frac1{1+x}\right)\,\mathrm{d}x\\ &=A[x-\ln(1+x)]_0^3 =\frac{3-\ln4}{\ln4} =\frac3{\ln4}-1. ...` |
| 984 | 8856-8858 | 0.47 | inline_safe | bracket | `f(x)=\frac{a}{x^2+1},\qquad -\infty<x<+\infty.` |
| 985 | 8863-8865 | 0.36 | inline_safe | bracket | `\int_{-\infty}^{+\infty}\frac{1}{x^2+1}\,\mathrm{d}x=\pi,` |
| 986 | 8867-8869 | 0.42 | inline_safe | bracket | `1=\int_{-\infty}^{+\infty}\frac{a}{x^2+1}\,\mathrm{d}x=a\pi,` |
| 987 | 8871-8873 | 0.14 | inline_safe | bracket | `a=\frac1\pi.` |
| 988 | 8876-8878 | 0.13 | inline_safe | bracket | `\xi=\frac{Y-1}{2},` |
| 989 | 8880-8882 | 0.28 | inline_safe | bracket | `\left\|\frac{\mathrm{d}}{\mathrm{d}y}\frac{y-1}{2}\right\|=\frac12.` |
| 990 | 8884-8892 | 0.38 | inline_unsafe_marker | bracket | `\begin{aligned} f_\eta(y) &=f_\xi\!\left(\frac{y-1}{2}\right)\cdot\frac12\\ &=\frac{1}{\pi\left[\left(\dfrac{y-1}{2}\right)^2+1\right]}\cdot\frac12\\ &=\frac{2}{\pi\bigl[(y-1)^2...` |
| 992 | 8904-8906 | 0.43 | inline_safe | bracket | `E(\xi)=np,\qquad D(\xi)=np(1-p).` |
| 993 | 8908-8910 | 0.19 | inline_safe | bracket | `np(1-p)=2.1.` |
| 994 | 8912-8914 | 0.23 | inline_safe | bracket | `1-p=\frac{2.1}{3}=0.7,` |
| 995 | 8916-8918 | 0.17 | inline_safe | bracket | `n=\frac{3}{0.3}=10.` |
| 996 | 8927-8929 | 0.17 | inline_safe | bracket | `\xi=1,2,3,4,5.` |
| 997 | 8932-8937 | 0.18 | normalized_width_not_low | bracket | `P(\xi=k) =\frac{4}{6}\cdot\frac{3}{5}\cdots \frac{4-(k-2)}{6-(k-2)}\cdot \frac{2}{6-(k-1)},` |
| 998 | 8941-8947 | 0.10 | inline_unsafe_marker | bracket | `\begin{array}{c\|ccccc} \xi & 1 & 2 & 3 & 4 & 5\\ \hline P & \dfrac13 & \dfrac4{15} & \dfrac15 & \dfrac2{15} & \dfrac1{15} \end{array}.` |
| 1000 | 8959-8965 | 0.14 | inline_unsafe_marker | bracket | `f(x)= \begin{cases} 2\sin x, & 0\le x\le A\pi,\\ 0, & \text{其他}. \end{cases}` |
| 1001 | 8976-8978 | 0.27 | inline_safe | bracket | `\int_0^{A\pi}2\sin x\,\mathrm{d}x=1.` |
| 1002 | 8980-8982 | 0.40 | inline_safe | bracket | `2[-\cos x]_0^{A\pi}=2(1-\cos A\pi)=1,` |
| 1003 | 8984-8986 | 0.18 | inline_safe | bracket | `\cos A\pi=\frac12.` |
| 1004 | 8988-8990 | 0.36 | inline_safe | bracket | `A\pi=\frac{\pi}{3},\qquad A=\frac13.` |
| 1005 | 8995-8997 | 0.29 | inline_safe | bracket | `P(X=3)=\frac43 e^{-2},` |
| 1006 | 9002-9004 | 0.27 | inline_safe | bracket | `P(X=3)=e^{-\lambda}\frac{\lambda^3}{3!}.` |
| 1007 | 9006-9008 | 0.33 | inline_safe | bracket | `\frac43 e^{-2}=e^{-2}\frac{2^3}{3!},` |
| 1008 | 9010-9012 | 0.13 | inline_safe | bracket | `EX=\lambda=2.` |
| 1010 | 9024-9026 | 0.37 | inline_safe | bracket | `\sum_{k=1}^{\infty}5A\left(\frac12\right)^k=1.` |
| 1011 | 9028-9030 | 0.34 | inline_safe | bracket | `\sum_{k=1}^{\infty}\left(\frac12\right)^k=1,` |
| 1012 | 9032-9034 | 0.34 | inline_safe | bracket | `5A=1,\qquad A=\frac15.` |
| 1013 | 9039-9046 | 0.18 | inline_unsafe_marker | bracket | `F(x)= \begin{cases} 1-e^{-\lambda x}, & x>0,\\ 0, & x\le0, \end{cases} \qquad \lambda>0.` |
| 1014 | 9051-9053 | 0.29 | inline_safe | bracket | `p(x)=F'(x)=\lambda e^{-\lambda x};` |
| 1015 | 9055-9061 | 0.11 | inline_unsafe_marker | bracket | `p(x)= \begin{cases} \lambda e^{-\lambda x}, & x>0,\\ 0, & x\le0. \end{cases}` |
| 1016 | 9063-9065 | 0.45 | inline_safe | bracket | `E\xi=\frac1\lambda,\qquad D\xi=\frac1{\lambda^2}.` |
| 1017 | 9073-9075 | 0.25 | inline_safe | bracket | `Z=\frac{X-2}{\sigma}\sim N(0,1).` |
| 1018 | 9077-9079 | 0.14 | inline_safe | bracket | `a=\frac2\sigma.` |
| 1020 | 9085-9087 | 0.13 | inline_safe | bracket | `\Phi(a)=0.8.` |
| 1022 | 9098-9100 | 0.14 | inline_safe | bracket | `P(X\le1+\mu)` |
| 1023 | 9111-9115 | 0.29 | normalized_width_not_low | bracket | `P(X\le1+\mu) =P\!\left(\frac{X-\mu}{\sigma}\le\frac{1+\mu-\mu}{\sigma}\right) =\Phi\!\left(\frac1\sigma\right).` |
| 1024 | 9130-9132 | 0.15 | inline_safe | bracket | `P(\xi=x)=0.` |
| 1025 | 9140-9142 | 0.39 | inline_safe | bracket | `X\sim N(0,1),\qquad Y\sim N(1,1).` |
| 1026 | 9153-9155 | 0.18 | inline_safe | bracket | `X+Y\sim N(1,2).` |
| 1027 | 9157-9159 | 0.27 | inline_safe | bracket | `P(X+Y\le1)=\frac12.` |
| 1028 | 9165-9167 | 0.21 | inline_safe | bracket | `P(X<Y)=\,\underline{\hspace{2cm}}.` |
| 1029 | 9178-9180 | 0.48 | inline_safe | bracket | `P(X<Y)=P(Y<X),\qquad P(X=Y)=0.` |
| 1030 | 9182-9184 | 0.38 | inline_safe | bracket | `P(X<Y)+P(Y<X)+P(X=Y)=1,` |
| 1031 | 9186-9188 | 0.21 | inline_safe | bracket | `P(X<Y)=\frac12.` |
| 1032 | 9193-9199 | 0.10 | inline_unsafe_marker | bracket | `\begin{array}{c\|ccccc} X&-2&-1&0&1&2\\ \hline P&a&\dfrac14&\dfrac18&b&\dfrac18 \end{array}` |
| 1033 | 9210-9212 | 0.45 | inline_safe | bracket | `a+b+\frac14+\frac18+\frac18=1,` |
| 1034 | 9214-9216 | 0.18 | inline_safe | bracket | `a+b=\frac12.` |
| 1036 | 9222-9224 | 0.21 | inline_safe | bracket | `EX=\frac12-3a.` |
| 1037 | 9226-9228 | 0.32 | inline_safe | bracket | `EX=\frac12-3a<\frac14,` |
| 1038 | 9234-9240 | 0.21 | inline_unsafe_marker | bracket | `F(x)= \begin{cases} \dfrac12e^x,& x\le0,\\[4pt] 1-\dfrac12e^{-x},& x>0. \end{cases}` |
| 1039 | 9245-9247 | 0.13 | inline_safe | bracket | `\|5\xi-2\|<3` |
| 1040 | 9249-9251 | 0.18 | inline_safe | bracket | `-3<5\xi-2<3,` |
| 1041 | 9253-9255 | 0.20 | inline_safe | bracket | `-\frac15<\xi<1.` |
| 1042 | 9257-9264 | 0.47 | inline_unsafe_marker | bracket | `\begin{aligned} P\{\|5\xi-2\|<3\} &=F(1)-F\!\left(-\frac15\right)\\ &=\left(1-\frac12e^{-1}\right)-\frac12e^{-1/5}\\ &=1-\frac12e^{-1}-\frac12e^{-0.2}. \end{aligned}` |
| 1044 | 9284-9286 | 0.32 | inline_safe | bracket | `\sum_{i=1}^n X_i\sim B(n,p).` |
| 1045 | 9288-9292 | 0.25 | inline_safe | bracket | `\overline X=\frac{k}{n} \quad\Longleftrightarrow\quad \sum_{i=1}^{n}X_i=k.` |
| 1046 | 9294-9298 | 0.32 | normalized_width_not_low | bracket | `P\left\{\overline X=\frac{k}{n}\right\} =P\left\{\sum_{i=1}^{n}X_i=k\right\} =\binom nk p^k(1-p)^{n-k}.` |
| 1047 | 9310-9313 | 0.45 | normalized_width_not_low | bracket | `P(X\le1+\mu)=P\left(\frac{X-\mu}{\sigma}\le \frac{1+\mu-\mu}{\sigma}\right) =\Phi\left(\frac1\sigma\right).` |
| 1048 | 9319-9325 | 0.07 | inline_unsafe_marker | bracket | `\begin{array}{c\|ccc} \xi & 0 & 1 & 2\\ \hline P & 0.25 & 0.35 & 0.40 \end{array}` |
| 1049 | 9337-9339 | 0.18 | inline_safe | bracket | `F(x)=P\{\xi<x\},` |
| 1050 | 9341-9343 | 0.16 | inline_safe | bracket | `0<1<\sqrt2<2,` |
| 1052 | 9357-9359 | 0.17 | inline_safe | bracket | `E(3X+5)=11` |
| 1053 | 9361-9363 | 0.08 | inline_safe | bracket | `EX=2.` |
| 1054 | 9365-9367 | 0.37 | inline_safe | bracket | `P(0<X<2)=P(2<X<4)=0.15.` |
| 1056 | 9376-9384 | 0.14 | inline_unsafe_marker | bracket | `F(x)= \begin{cases} 0, & x\le -1,\\ 0.3, & -1<x\le 1,\\ 0.8, & 1<x\le 3,\\ 1, & x>3. \end{cases}` |
| 1058 | 9393-9399 | 0.07 | inline_unsafe_marker | bracket | `\begin{array}{c\|ccc} X & -1 & 1 & 3\\ \hline P & 0.3 & 0.5 & 0.2 \end{array}` |
| 1062 | 9422-9425 | 0.49 | normalized_width_not_low | bracket | `F(x)=\frac12+\int_0^x\frac12e^{-t}\,\mathrm{d}t =1-\frac12e^{-x}.` |
| 1063 | 9427-9433 | 0.21 | inline_unsafe_marker | bracket | `F(x)= \begin{cases} \dfrac12e^x, & x\le0,\\[4pt] 1-\dfrac12e^{-x}, & x>0. \end{cases}` |
| 1064 | 9436-9443 | 0.45 | inline_unsafe_marker | bracket | `\begin{aligned} P(-5<X<10) &=F(10)-F(-5)\\ &=\left(1-\frac12e^{-10}\right)-\frac12e^{-5}\\ &=1-\frac12(e^{-5}+e^{-10}). \end{aligned}` |
| 1065 | 9446-9448 | 0.08 | inline_safe | bracket | `EX=0.` |
| 1066 | 9450-9453 | 0.48 | normalized_width_not_low | bracket | `EX^2=2\int_0^\infty x^2\cdot\frac12e^{-x}\,\mathrm{d}x =\int_0^\infty x^2e^{-x}\,\mathrm{d}x=2.` |
| 1067 | 9455-9457 | 0.28 | inline_safe | bracket | `DX=EX^2-(EX)^2=2.` |
| 1068 | 9464-9466 | 0.27 | inline_safe | bracket | `Y=a^X\qquad (a>0)` |
| 1069 | 9473-9479 | 0.11 | inline_unsafe_marker | bracket | `F_Y(y)= \begin{cases} 0, & y<1,\\ 1, & y\ge1. \end{cases}` |
| 1070 | 9482-9484 | 0.29 | inline_safe | bracket | `x=\frac{\ln y}{\ln a},\qquad y>0.` |
| 1071 | 9486-9488 | 0.21 | inline_safe | bracket | `\left\|\frac{\mathrm{d}x}{\mathrm{d}y}\right\|=\frac{1}{y\|\ln a\|}.` |
| 1073 | 9494-9503 | 0.26 | inline_unsafe_marker | bracket | `f_Y(y)= \begin{cases} \displaystyle \frac{1}{y\|\ln a\|\,\sigma\sqrt{2\pi}} \exp\!\left[-\frac{\left(\dfrac{\ln y}{\ln a}-\mu\right)^2}{2\sigma^2}\right], & y>0,\\[12pt] 0, & y\le...` |
| 1074 | 9511-9513 | 0.15 | inline_safe | bracket | `\lambda\Delta t+o(\Delta t).` |
| 1075 | 9518-9520 | 0.45 | inline_safe | bracket | `P(t<\xi\le t+\Delta t\,\|\,\xi>t)=\lambda\Delta t+o(\Delta t).` |
| 1076 | 9522-9525 | 0.21 | inline_safe | bracket | `\frac{F(t+\Delta t)-F(t)}{1-F(t)} =\lambda\Delta t+o(\Delta t).` |
| 1077 | 9527-9529 | 0.24 | inline_safe | bracket | `F'(t)=\lambda[1-F(t)].` |
| 1078 | 9531-9533 | 0.42 | inline_safe | bracket | `S'(t)=-\lambda S(t),\qquad S(0)=1.` |
| 1079 | 9535-9537 | 0.18 | inline_safe | bracket | `S(t)=e^{-\lambda t}.` |
| 1080 | 9539-9541 | 0.40 | inline_safe | bracket | `P(\xi>t)=e^{-\lambda t},\qquad t\ge0.` |
| 1081 | 9551-9553 | 0.23 | inline_safe | bracket | `\xi=m,m+1,m+2,\dots.` |
| 1082 | 9555-9558 | 0.41 | normalized_width_not_low | bracket | `P(\xi=k)=\binom{k-1}{m-1}p^m(1-p)^{k-m}, \qquad k=m,m+1,\dots.` |
| 1083 | 9561-9563 | 0.28 | inline_safe | bracket | `\xi=\xi_1+\xi_2+\cdots+\xi_m,` |
| 1084 | 9565-9567 | 0.39 | inline_safe | bracket | `E\xi=\sum_{i=1}^m E\xi_i=\frac mp.` |
| 1085 | 9572-9574 | 0.08 | inline_safe | bracket | `\eta=\|\xi\|` |
| 1086 | 9579-9581 | 0.29 | inline_safe | bracket | `F_\eta(y)=P(\|\xi\|\le y)=0.` |
| 1087 | 9583-9586 | 0.29 | normalized_width_not_low | bracket | `F_\eta(y)=P(-y\le \xi\le y) =F_\xi(y)-F_\xi(-y).` |
| 1088 | 9588-9590 | 0.34 | inline_safe | bracket | `f_\eta(y)=f_\xi(y)+f_\xi(-y).` |
| 1089 | 9592-9601 | 0.23 | normalized_width_not_low | bracket | `f_\eta(y)= \frac{1}{\sigma\sqrt{2\pi}} \left[ \exp\!\left(-\frac{(y-\mu)^2}{2\sigma^2}\right) + \exp\!\left(-\frac{(-y-\mu)^2}{2\sigma^2}\right) \right], \qquad y>0.` |
| 1090 | 9603-9615 | 0.20 | inline_unsafe_marker | bracket | `f_\eta(y)= \begin{cases} \displaystyle \frac{1}{\sigma\sqrt{2\pi}} \left[ \exp\!\left(-\frac{(y-\mu)^2}{2\sigma^2}\right) + \exp\!\left(-\frac{(y+\mu)^2}{2\sigma^2}\right) \righ...` |
| 1091 | 9628-9630 | 0.25 | inline_safe | bracket | `Y=a^{5X}=\exp(5X\ln a)` |
| 1092 | 9632-9634 | 0.31 | inline_safe | bracket | `x=\frac{\ln y}{5\ln a},\qquad y>0,` |
| 1093 | 9636-9638 | 0.25 | inline_safe | bracket | `\left\|\frac{\mathrm dx}{\mathrm dy}\right\|=\frac{1}{5\|\ln a\|\,y}.` |
| 1094 | 9640-9643 | 0.25 | inline_safe | bracket | `f_X(x)=\frac1{\sigma\sqrt{2\pi}} \exp\!\left[-\frac{(x-\mu)^2}{2\sigma^2}\right],` |
| 1095 | 9645-9655 | 0.22 | inline_unsafe_marker | bracket | `f_Y(y)= \begin{cases} \displaystyle \frac{1}{5\|\ln a\|\,y\,\sigma\sqrt{2\pi}} \exp\!\left[ -\frac{\left(\dfrac{\ln y}{5\ln a}-\mu\right)^2}{2\sigma^2} \right], & y>0,\\[14pt] 0,&...` |
| 1096 | 9667-9669 | 0.31 | inline_safe | bracket | `F(x)=\int_{-\infty}^{x}f(t)\,\mathrm{d}t.` |
| 1097 | 9677-9679 | 0.27 | inline_safe | bracket | `x_{k-1}<x_k<x_{k+1}.` |
| 1098 | 9690-9692 | 0.39 | inline_safe | bracket | `P(X=x_k)=F(x_k)-F(x_k-0).` |
| 1099 | 9694-9696 | 0.29 | inline_safe | bracket | `F(x_k-0)=F(x_{k-1}),` |
| 1100 | 9698-9700 | 0.39 | inline_safe | bracket | `P(X=x_k)=F(x_k)-F(x_{k-1}).` |
| 1101 | 9705-9707 | 0.19 | inline_safe | bracket | `Y=\max(X,2003)` |
| 1102 | 9718-9720 | 0.26 | inline_safe | bracket | `F_Y(y)=P(Y\le y)=0.` |
| 1104 | 9726-9728 | 0.34 | inline_safe | bracket | `F_Y(2003)=P(X\le2003)>0,` |
| 1105 | 9730-9732 | 0.22 | inline_safe | bracket | `F_Y(2003-0)=0.` |
| 1106 | 9738-9740 | 0.10 | inline_safe | bracket | `Y=3e^X` |
| 1107 | 9745-9747 | 0.34 | inline_safe | bracket | `x=\ln\frac y3,\qquad y>0.` |
| 1108 | 9749-9751 | 0.20 | inline_safe | bracket | `\left\|\frac{\mathrm{d}x}{\mathrm{d}y}\right\|=\frac1y.` |
| 1109 | 9753-9759 | 0.24 | inline_unsafe_marker | bracket | `f_Y(y)= \begin{cases} \displaystyle \frac1y f\!\left(\ln\frac y3\right), & y>0,\\[8pt] 0, & y\le0. \end{cases}` |
| 1110 | 9764-9766 | 0.23 | inline_safe | bracket | `(X_1,X_2,X_3,X_4)` |
| 1111 | 9768-9770 | 0.19 | inline_safe | bracket | `P(-1<\overline X<5).` |
| 1112 | 9774-9776 | 0.34 | inline_safe | bracket | `\overline X\sim N\left(3,\frac44\right)=N(3,1).` |
| 1113 | 9778-9782 | 0.27 | normalized_width_not_low | bracket | `P(-1<\overline X<5) =P\left(-4<\frac{\overline X-3}{1}<2\right) =\Phi(2)-\Phi(-4).` |
| 1114 | 9784-9786 | 0.39 | inline_safe | bracket | `P(-1<\overline X<5)\approx \Phi(2)=0.9772.` |
| 1115 | 9798-9800 | 0.31 | inline_safe | bracket | `F(x)=\int_{-\infty}^{x}f(t)\,\mathrm{d}t,` |
| 1116 | 9802-9804 | 0.16 | inline_safe | bracket | `f(x)=F'(x).` |
| 1117 | 9822-9824 | 0.33 | inline_safe | bracket | `P(X<-2004)=P(X>2004).` |
| 1118 | 9826-9831 | 0.35 | normalized_width_not_low | bracket | `P(\|X\|>2004) =P(X<-2004)+P(X>2004) =2P(X>2004) =2[1-F(2004)].` |
| 1119 | 9836-9838 | 0.13 | inline_safe | bracket | `Z=\|X-Y\|.` |
| 1120 | 9845-9847 | 0.13 | inline_safe | bracket | `F_Z(z)=0.` |
| 1121 | 9849-9851 | 0.33 | inline_safe | bracket | `2\cdot\frac{(1-z)^2}{2}=(1-z)^2.` |
| 1123 | 9857-9859 | 0.13 | inline_safe | bracket | `F_Z(z)=1.` |
| 1124 | 9861-9868 | 0.13 | inline_unsafe_marker | bracket | `F_Z(z)= \begin{cases} 0, & z<0,\\ 2z-z^2, & 0\le z\le1,\\ 1, & z>1. \end{cases}` |
| 1125 | 9883-9885 | 0.32 | inline_safe | bracket | `\sum_{i=1}^{n}X_i\sim B(n,p).` |
| 1126 | 9887-9889 | 0.36 | inline_safe | bracket | `\overline X=\frac1n\sum_{i=1}^{n}X_i.` |
| 1127 | 9891-9895 | 0.32 | normalized_width_not_low | bracket | `P\!\left(\overline X=\frac{k}{n}\right) =P\!\left(\sum_{i=1}^{n}X_i=k\right) =\binom nk p^k(1-p)^{n-k}.` |
| 1129 | 10015-10017 | 0.29 | inline_safe | bracket | `F(x,y) = P\{X \leqslant x, Y \leqslant y\}` |
| 1130 | 10023-10025 | 0.32 | inline_safe | bracket | `\{(x,y)\mid x\le x_0,\ y\le y_0\}` |
| 1134 | 10050-10052 | 0.13 | inline_unsafe_marker | bracket | `F(x,y) = \begin{cases} 1, & x+y \geqslant 0, \\ 0, & x+y < 0, \end{cases}` |
| 1139 | 10133-10137 | 0.44 | normalized_width_not_low | bracket | `P\{\min(X,Y)\ge 0\}=P\{X\ge 0\}P\{Y\ge 0\} =\frac12\cdot\frac12 =\frac14.` |
| 1141 | 10165-10167 | 0.32 | inline_safe | bracket | `P\{\max(X,Y)\le 1\}=\,\underline{\hspace{2cm}}.` |
| 1142 | 10171-10174 | 0.25 | inline_safe | bracket | `P\{\max(X,Y)\le1\} =P\{X\le1\}P\{Y\le1\}.` |
| 1143 | 10176-10178 | 0.37 | inline_safe | bracket | `P\{X\le1\}=P\{Y\le1\}=\frac13.` |
| 1156 | 10302-10304 | 0.47 | inline_safe | bracket | `P\{X \leqslant x, Y \leqslant y\} = P\{X \leqslant x\} \cdot P\{Y \leqslant y\},` |
| 1157 | 10306-10308 | 0.31 | inline_safe | bracket | `F(x,y) = F_X(x) \cdot F_Y(y),` |
| 1162 | 10372-10374 | 0.29 | inline_safe | bracket | `p_{ij} = p_{i\cdot} \cdot p_{\cdot j}.` |
| 1165 | 10392-10394 | 0.30 | inline_safe | bracket | `f(x,y) = f_X(x) \cdot f_Y(y)` |
| 1171 | 10446-10448 | 0.43 | inline_safe | bracket | `F(x_0, y_0) \neq F_X(x_0) \cdot F_Y(y_0).` |
| 1173 | 10473-10475 | 0.44 | inline_safe | bracket | `f(x) = \frac{1}{2}e^{-\|x\|}, \quad x \in (-\infty, +\infty),` |
| 1174 | 10480-10482 | 0.35 | inline_safe | bracket | `\{X\le 1\},\qquad \{\|X\|\le 1\}.` |
| 1176 | 10494-10501 | 0.33 | inline_unsafe_marker | bracket | `\begin{aligned} P\{\|X\|\le 1\} &=\frac{1}{2}\int_{-1}^{1}e^{-\|x\|}\,\mathrm{d}x =\int_{0}^{1}e^{-x}\,\mathrm{d}x =1-e^{-1}. \end{aligned}` |
| 1179 | 10513-10517 | 0.31 | normalized_width_not_low | bracket | `\left(1-\frac{1}{2}e^{-1}\right)(1-e^{-1}) =1-\frac{3}{2}e^{-1}+\frac{1}{2}e^{-2} \neq 1-e^{-1}.` |
| 1182 | 10583-10585 | 0.49 | inline_safe | bracket | `F(x,y) = \sum_{x_i \leqslant x}\sum_{y_j \leqslant y}p_{ij}.` |
| 1183 | 10588-10590 | 0.44 | inline_safe | bracket | `P\{(X,Y) \in G\} = \sum_{(x_i,y_j) \in G}p_{ij},` |
| 1188 | 10654-10661 | 0.33 | inline_unsafe_marker | bracket | `\begin{aligned} p_{00} &= P\{X_1=0, X_2=0\} = \frac{1}{9}, &\quad p_{01} &= P\{X_1=0, X_2=1\} = \frac{2}{9}, \\ p_{02} &= P\{X_1=0, X_2=2\} = \frac{1}{9}, &\quad p_{10} &= P\{X_...` |
| 1189 | 10680-10684 | 0.29 | display_environment | env:align* | `P\{X_1=0 \mid X_2=1\} &= \frac{p_{01}}{p_{\cdot 1}} = \frac{2/9}{4/9} = \frac{1}{2}\\ P\{X_1=1 \mid X_2=1\} &= \frac{p_{11}}{p_{\cdot 1}} = \frac{2/9}{4/9} = \frac{1}{2}\\ P\{X_...` |
| 1190 | 10706-10708 | 0.42 | inline_safe | bracket | `0.4 + a + b + 0.1 = 1 \implies a + b = 0.5.` |
| 1198 | 10780-10782 | 0.34 | inline_safe | bracket | `P\{X_2=0,\ X_1=-1\}=\frac{1}{4},` |
| 1199 | 10784-10788 | 0.29 | normalized_width_not_low | bracket | `P\{X_2=0\}\,P\{X_1=-1\} =\frac{1}{2}\times\frac{1}{4} =\frac{1}{8}.` |
| 1200 | 10792-10794 | 0.22 | inline_safe | bracket | `Z\in\{-2,-1,0,1\}.` |
| 1202 | 10802-10804 | 0.09 | inline_unsafe_marker | bracket | `Z \sim \begin{pmatrix} -2 & -1 & 0 & 1 \\ 0 & 3/4 & 0 & 1/4 \end{pmatrix}.` |
| 1203 | 10811-10818 | 0.23 | inline_unsafe_marker | bracket | `\begin{array}{c\|ccc} X_i&-1&0&1\\ \hline P&\dfrac14&\dfrac12&\dfrac14 \end{array} \qquad (i=1,2),` |
| 1204 | 10829-10831 | 0.23 | inline_safe | bracket | `P\{X_1X_2=0\}=1,` |
| 1207 | 10842-10844 | 0.49 | inline_safe | bracket | `P\{X_2=0,\ X_1\ne0\}=P\{X_1\ne0\}=\frac12.` |
| 1208 | 10846-10848 | 0.28 | inline_safe | bracket | `P\{X_1=0,X_2=0\}=0.` |
| 1209 | 10851-10853 | 0.47 | inline_safe | bracket | `P\{X_1=X_2\}=P\{X_1=0,X_2=0\}=0.` |
| 1212 | 10869-10877 | 0.47 | inline_unsafe_marker | bracket | `\begin{aligned} P(X=Y) &=P(X=0,Y=0)+P(X=1,Y=1)\\ &=\frac13\cdot\frac13+\frac23\cdot\frac23 =\frac19+\frac49 =\frac59. \end{aligned}` |
| 1213 | 10885-10893 | 0.07 | inline_unsafe_marker | bracket | `\begin{array}{c\|ccc} Y \backslash X & -1 & 0 & 1\\ \hline 0 & a & 0 & 0.1\\ 1 & 0.1 & 0.2 & 0\\ 2 & 0.2 & 0.1 & 0.2 \end{array}` |
| 1214 | 10901-10903 | 0.48 | inline_safe | bracket | `a+0.1+0.1+0.2+0.2+0.1+0.2=1,` |
| 1215 | 10905-10907 | 0.09 | inline_safe | bracket | `a=0.1.` |
| 1216 | 10910-10912 | 0.32 | inline_safe | bracket | `(-1,0),\qquad (-1,1).` |
| 1218 | 10919-10926 | 0.44 | inline_unsafe_marker | bracket | `\begin{aligned} E(XY) &=(-1)\cdot1\cdot0.1+(-1)\cdot2\cdot0.2 +1\cdot2\cdot0.2\\ &=-0.1-0.4+0.4=-0.1. \end{aligned}` |
| 1219 | 10933-10940 | 0.07 | inline_unsafe_marker | bracket | `\begin{array}{c\|ccc} X\backslash Y & -1 & 0 & 1\\ \hline 0 & 0.1 & 0.3 & 0.1\\ 1 & 0.2 & 0.2 & 0.1 \end{array}` |
| 1221 | 10949-10955 | 0.08 | inline_unsafe_marker | bracket | `Z_1\sim \begin{pmatrix} 0 & 1\\ 0.7 & 0.3 \end{pmatrix}.` |
| 1223 | 10961-10967 | 0.08 | inline_unsafe_marker | bracket | `Z_2\sim \begin{pmatrix} 0 & 1\\ 0.5 & 0.5 \end{pmatrix}.` |
| 1224 | 10969-10972 | 0.44 | normalized_width_not_low | bracket | `EX=P(X=1)=0.2+0.2+0.1=0.5, \qquad E(Y^2)=P(Y^2=1)=0.5,` |
| 1225 | 10973-10975 | 0.34 | inline_safe | bracket | `E(XY^2)=P(XY^2=1)=0.3.` |
| 1226 | 10977-10981 | 0.31 | normalized_width_not_low | bracket | `\operatorname{Cov}(X,Y^2) =E(XY^2)-EX\,E(Y^2) =0.3-0.5\cdot0.5=0.05.` |
| 1227 | 10988-11000 | 0.21 | inline_unsafe_marker | bracket | `X= \begin{cases} 1, & \text{若取出的产品是一等品},\\ 0, & \text{否则}, \end{cases} \qquad Y= \begin{cases} 1, & \text{若取出的产品是一等品或二等品},\\ 0, & \text{否则}. \end{cases}` |
| 1228 | 11005-11007 | 0.38 | inline_safe | bracket | `P(X^2=0,Y=0)=P(\text{三等品})=0.1,` |
| 1229 | 11008-11010 | 0.38 | inline_safe | bracket | `P(X^2=0,Y=1)=P(\text{二等品})=0.2,` |
| 1230 | 11011-11014 | 0.38 | normalized_width_not_low | bracket | `P(X^2=1,Y=0)=0,\qquad P(X^2=1,Y=1)=P(\text{一等品})=0.7.` |
| 1231 | 11016-11023 | 0.07 | inline_unsafe_marker | bracket | `\begin{array}{c\|cc} X^2\backslash Y & 0 & 1\\ \hline 0 & 0.1 & 0.2\\ 1 & 0 & 0.7 \end{array}` |
| 1233 | 11030-11033 | 0.39 | normalized_width_not_low | bracket | `\operatorname{Cov}(X^2,Y)=E(X^2Y)-E(X^2)EY =0.7-0.7\cdot0.9=0.07.` |
| 1234 | 11040-11048 | 0.07 | inline_unsafe_marker | bracket | `\begin{array}{c\|ccc} X\backslash Y & -1 & 0 & 1\\ \hline -1 & a & 0 & 0.2\\ 0 & 0.1 & b & 0.2\\ 1 & 0 & 0.1 & c \end{array}` |
| 1235 | 11050-11052 | 0.27 | inline_safe | bracket | `P\{Y\le0\mid X\le0\}=0.5.` |
| 1238 | 11068-11070 | 0.19 | inline_safe | bracket | `-a+c=-0.1.` |
| 1239 | 11072-11076 | 0.22 | inline_safe | bracket | `\frac{P\{Y\le0,\ X\le0\}}{P\{X\le0\}} =\frac{a+b+0.1}{a+b+0.5} =0.5,` |
| 1240 | 11078-11080 | 0.14 | inline_safe | bracket | `a+b=0.3.` |
| 1242 | 11087-11093 | 0.10 | inline_unsafe_marker | bracket | `\begin{array}{c\|ccccc} Z & -2 & -1 & 0 & 1 & 2\\ \hline P & 0.2 & 0.1 & 0.3 & 0.3 & 0.1 \end{array}` |
| 1243 | 11096-11098 | 0.46 | inline_safe | bracket | `P\{X=Z\}=P\{Y=0\}=0+b+0.1=0.2.` |
| 1246 | 11150-11152 | 0.09 | inline_unsafe_marker | bracket | `Z \sim \begin{pmatrix} -1 & 0 & 1 \\ 0.1344 & 0.7312 & 0.1344 \end{pmatrix}.` |
| 1247 | 11172-11174 | 0.25 | inline_safe | bracket | `p_{ij}=p_{i\cdot}p_{\cdot j}.` |
| 1248 | 11178-11182 | 0.32 | normalized_width_not_low | bracket | `p_{21}=p_{2\cdot}p_{\cdot 1}=\frac{1}{8}, \qquad p_{\cdot 1}=\frac{1}{6},` |
| 1249 | 11184-11186 | 0.25 | inline_safe | bracket | `p_{2\cdot}=\frac{1/8}{1/6}=\frac{3}{4}.` |
| 1250 | 11188-11190 | 0.41 | inline_safe | bracket | `p_{1\cdot}=1-p_{2\cdot}=1-\frac{3}{4}=\frac{1}{4}.` |
| 1251 | 11193-11195 | 0.32 | inline_safe | bracket | `p_{12}=p_{1\cdot}p_{\cdot 2}=\frac{1}{8},` |
| 1252 | 11197-11199 | 0.25 | inline_safe | bracket | `p_{\cdot 2}=\frac{1/8}{1/4}=\frac{1}{2}.` |
| 1254 | 11219-11222 | 0.38 | normalized_width_not_low | bracket | `\frac{1}{24}+\frac{1}{8}+\frac{1}{12}=\frac{1}{4},\qquad \frac{1}{8}+\frac{3}{8}+\frac{1}{4}=\frac{3}{4},` |
| 1255 | 11224-11228 | 0.30 | normalized_width_not_low | bracket | `\frac{1}{24}+\frac{1}{8}=\frac{1}{6},\qquad \frac{1}{8}+\frac{3}{8}=\frac{1}{2},\qquad \frac{1}{12}+\frac{1}{4}=\frac{1}{3}.` |
| 1256 | 11259-11263 | 0.28 | display_environment | env:align* | `P\{X_1=1 \mid X_2=2\} =& \frac{p_{12}}{p_{\cdot 2}} = \frac{1/6}{1/4} = \frac{2}{3}\\ P\{X_1=2 \mid X_2=2\} = &\frac{p_{22}}{p_{\cdot 2}} = \frac{0}{1/4} = 0\\ P\{X_1=3 \mid X_2...` |
| 1258 | 11271-11273 | 0.06 | inline_unsafe_marker | bracket | `Y \sim \begin{pmatrix} 1 & 2 & 3 & 6 \\ 1/6 & 1/3 & 1/3 & 1/6 \end{pmatrix}.` |
| 1260 | 11295-11297 | 0.09 | inline_unsafe_marker | bracket | `Z \sim \begin{pmatrix} -2 & -1 & 0 & 1 \\ 1/6 & 1/6 & 1/3 & 1/3 \end{pmatrix}.` |
| 1261 | 11299-11304 | 0.37 | display_environment | env:align* | `(X,Y)=(-1,-1) &: U=-1,\ V=-1, \quad P = 1/3. \\ (X,Y)=(-1,1) &: U=1,\ V=-1, \quad P = 1/6. \\ (X,Y)=(0,-1) &: U=0,\ V=-1, \quad P = 1/3. \\ (X,Y)=(0,1) &: U=1,\ V=0, \quad P = 1/6.` |
| 1262 | 11317-11319 | 0.11 | inline_unsafe_marker | bracket | `UV \sim \begin{pmatrix} -1 & 0 & 1 \\ 1/6 & 1/2 & 1/3 \end{pmatrix}.` |
| 1263 | 11325-11327 | 0.19 | inline_unsafe_marker | bracket | `X = \begin{cases} 1, & A \text{发生}, \\ 0, & A \text{不发生}, \end{cases} \quad Y = \begin{cases} 1, & B \text{发生}, \\ 0, & B \text{不发生}. \end{cases}` |
| 1266 | 11354-11356 | 0.07 | inline_unsafe_marker | bracket | `Z \sim \begin{pmatrix} 0 & 1 & 2 \\ 2/3 & 1/4 & 1/12 \end{pmatrix}.` |
| 1268 | 11367-11369 | 0.11 | inline_unsafe_marker | bracket | `Z = \begin{cases} 1, & X+Y \text{为偶数}, \\ 0, & X+Y \text{为奇数}. \end{cases}` |
| 1270 | 11378-11380 | 0.30 | inline_safe | bracket | `p^2 = p\left[(1-p)^2+p^2\right].` |
| 1276 | 11449-11452 | 0.46 | normalized_width_not_low | bracket | `P(X=0)=P(Y=0)=\frac13,\qquad P(X=1)=P(Y=1)=\frac23.` |
| 1277 | 11454-11461 | 0.47 | inline_unsafe_marker | bracket | `\begin{aligned} P(X=Y) &=P(X=0,Y=0)+P(X=1,Y=1)\\ &=\frac13\cdot\frac13+\frac23\cdot\frac23\\ &=\frac59. \end{aligned}` |
| 1279 | 11470-11472 | 0.43 | inline_safe | bracket | `U=\max(X,Y),\qquad V=\min(X,Y).` |
| 1281 | 11487-11498 | 0.09 | inline_unsafe_marker | bracket | `\begin{array}{c\|cc\|c} \toprule U\backslash V & 1 & 2 & p_{i\cdot}\\ \midrule 1 & \dfrac49 & 0 & \dfrac49\\[4pt] 2 & \dfrac49 & \dfrac19 & \dfrac59\\ \midrule p_{\cdot j} & \dfra...` |
| 1284 | 11508-11513 | 0.24 | normalized_width_not_low | bracket | `\operatorname{Cov}(U,V) =E(UV)-EU\,EV =\frac{16}{9}-\frac{14}{9}\cdot\frac{10}{9} =\frac4{81}.` |
| 1285 | 11524-11527 | 0.42 | normalized_width_not_low | bracket | `P(X=i,Y=j)=\frac{2!}{i!\,j!\,(2-i-j)!} \left(\frac13\right)^2.` |
| 1286 | 11529-11539 | 0.09 | inline_unsafe_marker | bracket | `\begin{array}{c\|ccc} \toprule X\backslash Y & 0 & 1 & 2\\ \midrule 0 & \dfrac19 & \dfrac29 & \dfrac19\\[4pt] 1 & \dfrac29 & \dfrac29 & 0\\[4pt] 2 & \dfrac19 & 0 & 0\\ \bottomrul...` |
| 1287 | 11541-11543 | 0.34 | inline_safe | bracket | `P(X=0)=P(Y=0)=\frac49.` |
| 1289 | 11551-11567 | 0.11 | inline_unsafe_marker | bracket | `\begin{array}{c\|ccc} \toprule u & 0 & 1 & 2\\ \midrule P(U=u) & \dfrac19 & \dfrac69 & \dfrac29\\ \bottomrule \end{array} \qquad \begin{array}{c\|ccc} \toprule v & 0 & 1 & 2\\ \mi...` |
| 1290 | 11574-11576 | 0.30 | inline_unsafe_marker | bracket | `X = \begin{cases} 1, & X_1+X_2=1, \\ 0, & X_1+X_2\neq 1, \end{cases} \quad Y = \begin{cases} 1, & X_2+X_3=1, \\ 0, & X_2+X_3\neq 1. \end{cases}` |
| 1291 | 11584-11586 | 0.29 | inline_safe | bracket | `P(X=1,Y=1) = 2e^{-3}.` |
| 1296 | 11666-11668 | 0.42 | inline_safe | bracket | `P\{(X,Y) \in G\} = \iint_G f(x,y)\,\mathrm{d}x\,\mathrm{d}y;` |
| 1297 | 11670-11672 | 0.26 | inline_safe | bracket | `f(x,y) = \frac{\partial^2 F(x,y)}{\partial x\,\partial y}.` |
| 1298 | 11686-11688 | 0.33 | inline_safe | bracket | `\iint\limits_{\mathbb{R}^2} f(x,y) \,\mathrm{d}x\,\mathrm{d}y = 1` |
| 1299 | 11690-11692 | 0.46 | inline_safe | bracket | `\int_{0}^{+\infty} \left( \int_{0}^{y} A e^{-y} \,\mathrm{d}x \right) \mathrm{d}y = 1` |
| 1301 | 11698-11700 | 0.21 | inline_safe | bracket | `A \times 1 = 1 \implies A = 1` |
| 1302 | 11702-11704 | 0.36 | inline_safe | bracket | `P\{X+Y \geqslant 1\} = 1 - P\{X+Y < 1\}` |
| 1303 | 11706-11711 | 0.19 | inline_unsafe_marker | bracket | `\begin{cases} 0 < x < y & \text{(密度函数非零的固有条件)} \\ x + y < 1 & \text{(题目要求的事件条件)} \end{cases}` |
| 1307 | 11733-11735 | 0.34 | inline_safe | bracket | `P\{X/Y \leqslant 1/2\} = \frac{1}{2} \times 1 = \frac{1}{2}` |
| 1308 | 11743-11747 | 0.38 | inline_unsafe_marker | bracket | `f_X(x) = \begin{cases} 4e^{-4x}, & x > 0 \\ 0, & x \leqslant 0 \end{cases} \quad \text{与} \quad F_X(x) = P\{X \leqslant x\} = \begin{cases} 1 - e^{-4x}, & x > 0 \\ 0, & x \leqsl...` |
| 1309 | 11750-11752 | 0.28 | inline_safe | bracket | `P\{X\in A\mid Y=y\}=P\{X\in A\},` |
| 1310 | 11754-11756 | 0.47 | inline_safe | bracket | `P(\{X\in A\}\cap\{Y=y\})=P\{X\in A\}\cdot P\{Y=y\}.` |
| 1316 | 11786-11788 | 0.18 | inline_safe | bracket | `P\{X \geqslant -2\} = 1` |
| 1324 | 11834-11836 | 0.18 | inline_unsafe_marker | bracket | `f_X(x) = \begin{cases} 3x^2, & 0 < x < 1, \\ 0, & \text{其他}, \end{cases}` |
| 1325 | 11838-11840 | 0.25 | inline_unsafe_marker | bracket | `f_{Y\|X}(y\|x) = \begin{cases} \dfrac{3y^2}{x^3}, & 0 < y < x, \\ 0, & \text{其他}. \end{cases}` |
| 1328 | 11863-11865 | 0.26 | inline_safe | bracket | `f_{Y\|X}(y\|x) = \frac{f(x,y)}{f_X(x)}` |
| 1329 | 11869-11871 | 0.26 | inline_safe | bracket | `f_{X\|Y}(x\|y) = \frac{f(x,y)}{f_Y(y)}` |
| 1332 | 11904-11910 | 0.20 | inline_unsafe_marker | bracket | `f(x,y)= \begin{cases} A, & 0<x<2,\ \|y\|<x,\\ 0, & \text{其他}. \end{cases}` |
| 1333 | 11918-11922 | 0.40 | normalized_width_not_low | bracket | `1=\int_0^2\int_{-x}^{x}A\,\mathrm dy\,\mathrm dx =\int_0^2 2Ax\,\mathrm dx =4A,` |
| 1334 | 11926-11928 | 0.46 | inline_safe | bracket | `f_X(x)=\int_{-x}^{x}\frac14\,\mathrm dy=\frac{x}{2}.` |
| 1335 | 11930-11937 | 0.26 | inline_unsafe_marker | bracket | `f_{Y\|X}(y\|x)=\frac{f(x,y)}{f_X(x)} = \begin{cases} \dfrac1{2x}, & -x<y<x,\ 0<x<2,\\[4pt] 0, & \text{其他}. \end{cases}` |
| 1337 | 11944-11946 | 0.35 | inline_safe | bracket | `\operatorname{Cov}(X,Y)=E(XY)-EX\,EY=0.` |
| 1338 | 11952-11954 | 0.19 | inline_unsafe_marker | bracket | `f(x,y) = \begin{cases} e^{-y}, & x > 0,\ y > x, \\ 0, & \text{其他}, \end{cases}` |
| 1343 | 11980-11982 | 0.27 | inline_unsafe_marker | bracket | `f(x,y) = \begin{cases} A(6-x-y), & 0 \leqslant x \leqslant 2,\ 2 \leqslant y \leqslant 4, \\ 0, & \text{其他}. \end{cases}` |
| 1353 | 12057-12061 | 0.16 | inline_unsafe_marker | bracket | `F_Y(y) = \begin{cases} 0, & y \leqslant 0, \\ \dfrac{3y}{4}, & 0 < y \leqslant 1, \\ \dfrac{1}{2} + \dfrac{y}{4}, & 1 < y \leqslant 2, \\ 1, & y \geqslant 2. \end{cases} \qquad ...` |
| 1354 | 12071-12073 | 0.18 | inline_unsafe_marker | bracket | `f(x,y) = \begin{cases} \dfrac{1}{S_D}, & (x,y) \in D, \\ 0, & \text{其他}, \end{cases}` |
| 1355 | 12078-12080 | 0.24 | inline_safe | bracket | `P\{(X,Y) \in G\} = \frac{S_G}{S_D}.` |
| 1358 | 12108-12114 | 0.11 | inline_unsafe_marker | bracket | `f(x,y)= \begin{cases} \dfrac12, & (x,y)\in D,\\[4pt] 0, & \text{其他}. \end{cases}` |
| 1359 | 12117-12120 | 0.41 | normalized_width_not_low | bracket | `f_X(x)=\int_0^{1/x}\frac12\,\mathrm dy =\frac1{2x},\qquad 1\le x\le e^2.` |
| 1360 | 12122-12129 | 0.23 | inline_unsafe_marker | bracket | `f_Y(y)= \begin{cases} \dfrac12(e^2-1), & 0\le y\le e^{-2},\\[6pt] \dfrac1{2y}-\dfrac12, & e^{-2}<y\le1,\\[6pt] 0, & \text{其他}. \end{cases}` |
| 1361 | 12133-12135 | 0.36 | inline_safe | bracket | `P(X+Y\ge2)=1-P(X+Y<2).` |
| 1363 | 12150-12156 | 0.20 | inline_unsafe_marker | bracket | `f(x,y)= \begin{cases} e^{-y}, & 0\le x\le1,\ y>0,\\ 0, & \text{其他}. \end{cases}` |
| 1364 | 12163-12165 | 0.42 | inline_safe | bracket | `f_\xi(x)=\int_0^{+\infty}e^{-y}\,\mathrm dy=1;` |
| 1365 | 12167-12173 | 0.13 | inline_unsafe_marker | bracket | `f_\xi(x)= \begin{cases} 1, & 0\le x\le1,\\ 0, & \text{其他}. \end{cases}` |
| 1366 | 12175-12177 | 0.45 | inline_safe | bracket | `f_\eta(y)=\int_0^1 e^{-y}\,\mathrm dx=e^{-y};` |
| 1367 | 12179-12185 | 0.11 | inline_unsafe_marker | bracket | `f_\eta(y)= \begin{cases} e^{-y}, & y>0,\\ 0, & \text{其他}. \end{cases}` |
| 1368 | 12188-12190 | 0.28 | inline_safe | bracket | `f(x,y)=f_\xi(x)f_\eta(y),` |
| 1372 | 12206-12213 | 0.16 | inline_unsafe_marker | bracket | `f_\zeta(z)= \begin{cases} 1-e^{-z}, & 0<z<1,\\ (e-1)e^{-z}, & z\ge1,\\ 0, & \text{其他}. \end{cases}` |
| 1374 | 12227-12231 | 0.47 | normalized_width_not_low | bracket | `1=\int_0^1\int_0^x Ay(1-x)\,\mathrm dy\,\mathrm dx =\frac A2\int_0^1 x^2(1-x)\,\mathrm dx =\frac A{24},` |
| 1375 | 12233-12235 | 0.08 | inline_safe | bracket | `A=24.` |
| 1376 | 12238-12245 | 0.47 | inline_unsafe_marker | bracket | `\begin{aligned} F(x,y) &=\int_0^y\int_0^u 24v(1-u)\,\mathrm dv\,\mathrm du +\int_y^x\int_0^y 24v(1-u)\,\mathrm dv\,\mathrm du\\ &=3y^4-8y^3+12\left(x-\frac{x^2}{2}\right)y^2. \e...` |
| 1378 | 12252-12254 | 0.35 | inline_safe | bracket | `F(x,y)=3y^4-8y^3+6y^2.` |
| 1379 | 12256-12265 | 0.38 | inline_unsafe_marker | bracket | `F(x,y)= \begin{cases} 0, & x<0\ \text{或}\ y<0,\\[3pt] 3y^4-8y^3+12\left(x-\dfrac{x^2}{2}\right)y^2, & 0\le x<1,\ 0\le y<x,\\[6pt] 3y^4-8y^3+6y^2, & x\ge1,\ 0\le y<1,\\[6pt] 4x^3...` |
| 1380 | 12272-12274 | 0.31 | inline_safe | bracket | `D=\{(x,y)\mid x^2+y^2\le1\}` |
| 1381 | 12282-12288 | 0.18 | inline_unsafe_marker | bracket | `\varphi(x,y)= \begin{cases} \dfrac1\pi, & x^2+y^2\le1,\\[6pt] 0, & \text{其他}. \end{cases}` |
| 1382 | 12291-12293 | 0.33 | inline_safe | bracket | `-\sqrt{1-x^2}<y<\sqrt{1-x^2}.` |
| 1384 | 12301-12307 | 0.16 | inline_unsafe_marker | bracket | `\varphi_\xi(x)= \begin{cases} \dfrac{2}{\pi}\sqrt{1-x^2}, & \|x\|<1,\\[6pt] 0, & \text{其他}. \end{cases}` |
| 1385 | 12309-12315 | 0.16 | inline_unsafe_marker | bracket | `\varphi_\eta(y)= \begin{cases} \dfrac{2}{\pi}\sqrt{1-y^2}, & \|y\|<1,\\[6pt] 0, & \text{其他}. \end{cases}` |
| 1387 | 12322-12324 | 0.35 | inline_safe | bracket | `\operatorname{Cov}(\xi,\eta)=E(\xi\eta)-E\xi\,E\eta=0,` |
| 1388 | 12328-12330 | 0.26 | inline_safe | bracket | `\varphi(x,y)\ne \varphi_\xi(x)\varphi_\eta(y),` |
| 1390 | 12348-12350 | 0.34 | inline_unsafe_marker | bracket | `f(x,y) = \begin{cases} 3/4, & -1 < x < 1,\ 0 \leqslant y \leqslant 1-x^2, \\ 0, & \text{其他}. \end{cases}` |
| 1393 | 12359-12361 | 0.41 | inline_unsafe_marker | bracket | `f_{Y\|X}(y\|x) = \frac{f(x,y)}{f_X(x)} = \begin{cases} \dfrac{1}{1-x^2}, & 0 \leqslant y \leqslant 1-x^2, \\ 0, & \text{其他}. \end{cases}` |
| 1396 | 12397-12397 | 0.24 | inline_unsafe_marker | bracket | `f(x,y) = \begin{cases} kx^2, & 0 < x < 1,\ x^2 < y < 1, \\ 0, & \text{其他}. \end{cases}` |
| 1402 | 12423-12423 | 0.22 | inline_unsafe_marker | bracket | `f(x,y) = \begin{cases} 2-x-y, & 0 < x < 1,\ 0 < y < 1, \\ 0, & \text{其他}. \end{cases}` |
| 1405 | 12436-12438 | 0.47 | inline_safe | bracket | `f_Z(z) = \int_0^z(2-z)\,\mathrm{d}x = z(2-z).` |
| 1407 | 12444-12446 | 0.21 | inline_unsafe_marker | bracket | `f_Z(z) = \begin{cases} z(2-z), & 0 < z < 1, \\ (2-z)^2, & 1 \leqslant z < 2, \\ 0, & \text{其他}. \end{cases}` |
| 1408 | 12457-12459 | 0.31 | inline_unsafe_marker | bracket | `f(x,y) = \begin{cases} 1, & 0 \leqslant y \leqslant 1,\ y \leqslant x \leqslant 2-y, \\ 0, & \text{其他}. \end{cases}` |
| 1409 | 12465-12467 | 0.13 | inline_unsafe_marker | bracket | `f_X(x) = \begin{cases} x, & 0 < x < 1, \\ 2-x, & 1 < x < 2, \\ 0, & \text{其他}. \end{cases}` |
| 1410 | 12472-12474 | 0.19 | inline_unsafe_marker | bracket | `f_Y(y) = \begin{cases} 2-2y, & 0 < y < 1, \\ 0, & \text{其他}. \end{cases}` |
| 1412 | 12480-12482 | 0.26 | inline_unsafe_marker | bracket | `f_{X\|Y}(x\|y) = \begin{cases} \dfrac{1}{2-2y}, & y \leqslant x \leqslant 2-y, \\ 0, & \text{其他}. \end{cases}` |
| 1413 | 12494-12496 | 0.13 | inline_unsafe_marker | bracket | `f_X(x) = \begin{cases} 1, & 0 < x < 1, \\ 0, & \text{其他}. \end{cases}` |
| 1414 | 12498-12500 | 0.21 | inline_unsafe_marker | bracket | `f_{Y\|X}(y\|x) = \begin{cases} \dfrac{1}{x}, & 0 < y < x, \\ 0, & \text{其他}. \end{cases}` |
| 1415 | 12502-12504 | 0.15 | inline_unsafe_marker | bracket | `f(x,y) = \begin{cases} \dfrac{1}{x}, & 0 < y < x < 1, \\ 0, & \text{其他}. \end{cases}` |
| 1417 | 12510-12512 | 0.19 | inline_unsafe_marker | bracket | `f_Y(y) = \begin{cases} -\ln y, & 0 < y < 1, \\ 0, & \text{其他}. \end{cases}` |
| 1422 | 12545-12547 | 0.44 | inline_safe | bracket | `(X,Y) \sim N(\mu_1, \mu_2, \sigma_1^2, \sigma_2^2; 0).` |
| 1425 | 12581-12583 | 0.25 | inline_unsafe_marker | bracket | `f(x,y) = \begin{cases} 2, & 0 < x < 1,\ 0 < y < 1-x, \\ 0, & \text{其他}, \end{cases}` |
| 1426 | 12593-12595 | 0.45 | inline_unsafe_marker | bracket | `f(x,y) = f_X(x)\,f_Y(y) = \begin{cases} e^{-(x+y)}, & x > 0,\ y > 0, \\ 0, & \text{其他}. \end{cases}` |
| 1432 | 12656-12658 | 0.37 | inline_safe | bracket | `Z = X + Y \sim B(2+4, p) = B(6, p).` |
| 1436 | 12685-12687 | 0.29 | inline_unsafe_marker | bracket | `Y_1 \sim \begin{pmatrix} 0 & 1 & 2 \\ 1/9 & 4/9 & 4/9 \end{pmatrix}, \qquad Y_2 \sim \begin{pmatrix} -2 & -1 & 0 & 1 & 2 \\ 1/9 & 2/9 & 1/3 & 2/9 & 1/9 \end{pmatrix}.` |
| 1438 | 12725-12727 | 0.33 | inline_safe | bracket | `\max\{X, Y\} \leqslant z \iff X \leqslant z \text{ 且 } Y \leqslant z,` |
| 1440 | 12740-12742 | 0.16 | inline_unsafe_marker | bracket | `F_Z(z) = \begin{cases} 0, & z \leqslant 0, \\ z(1 - e^{-z}), & 0 < z < 1, \\ 1 - e^{-z}, & z \geqslant 1. \end{cases}` |
| 1441 | 12747-12759 | 0.13 | inline_unsafe_marker | bracket | `f_X(x)= \begin{cases} 1, & 0\le x\le1,\\ 0, & \text{其他}, \end{cases} \qquad f_Y(y)= \begin{cases} e^{-y}, & y>0,\\ 0, & \text{其他}. \end{cases}` |
| 1442 | 12761-12767 | 0.15 | inline_unsafe_marker | bracket | `Z=g(X,Y)= \begin{cases} 1, & X\le Y,\\ 0, & X>Y. \end{cases}` |
| 1443 | 12772-12774 | 0.29 | inline_safe | bracket | `EZ=P(Z=1)=P(X\le Y).` |
| 1445 | 12780-12784 | 0.47 | normalized_width_not_low | bracket | `P(X\le Y)=\int_0^1 P(Y\ge x)f_X(x)\,\mathrm dx =\int_0^1 e^{-x}\,\mathrm dx =1-e^{-1}.` |
| 1446 | 12786-12788 | 0.18 | inline_safe | bracket | `EZ=1-e^{-1}.` |
| 1447 | 12790-12792 | 0.28 | inline_safe | bracket | `DZ=(1-e^{-1})e^{-1}.` |
| 1448 | 12797-12803 | 0.11 | inline_unsafe_marker | bracket | `f_X(x)= \begin{cases} \lambda e^{-\lambda x}, & x>0,\\ 0, & x\le0. \end{cases}` |
| 1449 | 12805-12807 | 0.19 | inline_safe | bracket | `Y=\max\{X^2,4\}.` |
| 1450 | 12812-12814 | 0.27 | inline_safe | bracket | `F_Y(y)=P\{Y\le y\}=0.` |
| 1452 | 12820-12824 | 0.31 | normalized_width_not_low | bracket | `F_Y(y)=P\{0<X\le\sqrt y\} =\int_0^{\sqrt y}\lambda e^{-\lambda x}\,\mathrm dx =1-e^{-\lambda\sqrt y}.` |
| 1453 | 12826-12832 | 0.17 | inline_unsafe_marker | bracket | `F_Y(y)= \begin{cases} 0, & y<4,\\ 1-e^{-\lambda\sqrt y}, & y\ge4. \end{cases}` |
| 1455 | 12841-12847 | 0.11 | inline_unsafe_marker | bracket | `f_X(x)= \begin{cases} \lambda e^{-\lambda x}, & x>0,\\ 0, & x\le0. \end{cases}` |
| 1456 | 12849-12855 | 0.12 | inline_unsafe_marker | bracket | `Y=g(X)= \begin{cases} X, & X>1,\\ 2X, & X\le1. \end{cases}` |
| 1457 | 12860-12862 | 0.44 | inline_safe | bracket | `F_Y(y)=P\{X\le y/2\}=1-e^{-\lambda y/2}.` |
| 1458 | 12865-12872 | 0.46 | inline_unsafe_marker | bracket | `\begin{aligned} F_Y(y) &=P\{2X\le y,\ X\le1\}+P\{X\le y,\ X>1\}\\ &=P\{X\le y/2\}+P\{1<X\le y\}\\ &=(1-e^{-\lambda y/2})+(e^{-\lambda}-e^{-\lambda y}). \end{aligned}` |
| 1459 | 12874-12880 | 0.38 | inline_unsafe_marker | bracket | `F_Y(y)= \begin{cases} 1-e^{-\lambda y/2}, & 0<y\le1,\\ 1+e^{-\lambda}-e^{-\lambda y/2}-e^{-\lambda y}, & 1<y\le2. \end{cases}` |
| 1460 | 12885-12891 | 0.05 | inline_unsafe_marker | bracket | `X\sim \begin{pmatrix} 1 & 2\\ 0.3 & 0.7 \end{pmatrix},` |
| 1462 | 12904-12906 | 0.39 | inline_safe | bracket | `G(u)=0.3F(u-1)+0.7F(u-2).` |
| 1463 | 12908-12910 | 0.39 | inline_safe | bracket | `g(u)=0.3f(u-1)+0.7f(u-2).` |
| 1464 | 12915-12921 | 0.19 | inline_unsafe_marker | bracket | `\varphi(x,y)= \begin{cases} A e^{-(2x+3y)}, & x>0,\ y>0,\\ 0, & \text{其他}. \end{cases}` |
| 1467 | 12939-12941 | 0.42 | inline_safe | bracket | `0\le x\le1,\quad 0\le y\le x+\frac13,` |
| 1468 | 12943-12945 | 0.39 | inline_safe | bracket | `1\le x\le3,\quad 0\le y\le \frac{6-2x}{3}.` |
| 1470 | 12959-12965 | 0.19 | inline_unsafe_marker | bracket | `f(x,y)= \begin{cases} k e^{-(2x+3y)}, & x>0,\ y>0,\\ 0, & \text{其他}. \end{cases}` |
| 1473 | 12990-12996 | 0.31 | inline_unsafe_marker | bracket | `F(x,y)= \begin{cases} (1-e^{-2x})(1-e^{-3y}), & x>0,\ y>0,\\ 0, & x\le0\ \text{或}\ y\le0. \end{cases}` |
| 1478 | 13025-13031 | 0.19 | inline_unsafe_marker | bracket | `\varphi(x,y)= \begin{cases} A e^{-(3x+2y)}, & x>0,\ y>0,\\ 0, & \text{其他}. \end{cases}` |
| 1481 | 13049-13051 | 0.42 | inline_safe | bracket | `0\le x\le\frac35,\quad 0\le y\le x+1,` |
| 1482 | 13053-13055 | 0.46 | inline_safe | bracket | `\frac35\le x\le3,\quad 0\le y\le\frac{6-2x}{3}.` |
| 1484 | 13069-13075 | 0.20 | inline_unsafe_marker | bracket | `f(x,y)= \begin{cases} 1, & \|y\|<x,\ 0<x<1,\\ 0, & \text{其他}. \end{cases}` |
| 1486 | 13087-13093 | 0.11 | inline_unsafe_marker | bracket | `f_X(x)= \begin{cases} 2x, & 0<x<1,\\ 0, & \text{其他}. \end{cases}` |
| 1488 | 13099-13105 | 0.13 | inline_unsafe_marker | bracket | `f_Y(y)= \begin{cases} 1-\|y\|, & -1<y<1,\\ 0, & \text{其他}. \end{cases}` |
| 1489 | 13108-13112 | 0.48 | normalized_width_not_low | bracket | `EX=\int_0^1 x\cdot2x\,\mathrm dx=\frac23, \qquad EX^2=\int_0^1 x^2\cdot2x\,\mathrm dx=\frac12,` |
| 1491 | 13118-13120 | 0.41 | inline_safe | bracket | `EY=\int_{-1}^{1}y(1-\|y\|)\,\mathrm dy=0.` |
| 1493 | 13126-13128 | 0.35 | inline_safe | bracket | `\operatorname{Cov}(X,Y)=E(XY)-EX\,EY=0.` |
| 1494 | 13131-13133 | 0.13 | inline_safe | bracket | `f(x,y)=0,` |
| 1495 | 13135-13137 | 0.43 | inline_safe | bracket | `f_X(1/2)f_Y(3/4)=1\cdot\frac14>0.` |
| 1496 | 13143-13149 | 0.13 | inline_unsafe_marker | bracket | `f(x,y)= \begin{cases} \dfrac{21}{4}x^2y, & x^2<y<1,\\ 0, & \text{其他}. \end{cases}` |
| 1497 | 13156-13159 | 0.48 | normalized_width_not_low | bracket | `f_X(x)=\int_{x^2}^{1}\frac{21}{4}x^2y\,\mathrm dy =\frac{21}{8}x^2(1-x^4),\qquad -1<x<1.` |
| 1498 | 13161-13167 | 0.21 | inline_unsafe_marker | bracket | `f_X(x)= \begin{cases} \dfrac{21}{8}x^2(1-x^4), & -1<x<1,\\ 0, & \text{其他}. \end{cases}` |
| 1499 | 13169-13172 | 0.46 | normalized_width_not_low | bracket | `f_Y(y)=\int_{-\sqrt y}^{\sqrt y}\frac{21}{4}x^2y\,\mathrm dx =\frac72 y^{5/2},\qquad 0<y<1.` |
| 1500 | 13174-13180 | 0.17 | inline_unsafe_marker | bracket | `f_Y(y)= \begin{cases} \dfrac72 y^{5/2}, & 0<y<1,\\ 0, & \text{其他}. \end{cases}` |
| 1501 | 13183-13185 | 0.08 | inline_safe | bracket | `EX=0.` |
| 1502 | 13187-13190 | 0.42 | normalized_width_not_low | bracket | `EY=\int_0^1 y\cdot\frac72 y^{5/2}\,\mathrm dy =\frac72\cdot\frac{2}{9}=\frac79.` |
| 1505 | 13201-13203 | 0.35 | inline_safe | bracket | `\operatorname{Cov}(X,Y)=E(XY)-EX\,EY=0.` |
| 1506 | 13211-13213 | 0.25 | inline_unsafe_marker | bracket | `f(x,y) = \begin{cases} e^{-(x+y)}, & x > 0,\ y > 0, \\ 0, & \text{其他}, \end{cases}` |
| 1510 | 13234-13236 | 0.21 | inline_unsafe_marker | bracket | `f_Z(z) = \begin{cases} ze^{-z}, & z > 0, \\ 0, & z \leqslant 0. \end{cases}` |
| 1511 | 13243-13243 | 0.30 | inline_unsafe_marker | bracket | `f_X(x)=\begin{cases}2\mathrm{e}^{-2x},&x\geqslant0\\0,&x<0\end{cases},~f_Y(y)=\begin{cases}2\mathrm{e}^{-2y},&y\geqslant0\\0,&y<0\end{cases}` |
| 1512 | 13244-13244 | 0.25 | inline_unsafe_marker | bracket | `F_T(t) =\begin{cases}1 - e^{-2t}, & t>0 \\0, & t\le 0\end{cases}\quad (T=X,Y)` |
| 1515 | 13269-13269 | 0.36 | inline_unsafe_marker | bracket | `f_Z(z) =\begin{cases}2\left( e^{-\frac{2z}{3}} - e^{-z} \right), & z > 0 \\0, & z \le 0\end{cases}` |
| 1516 | 13276-13278 | 0.37 | inline_unsafe_marker | bracket | `f(x,y) = \begin{cases} \dfrac{1}{2}(x+y)e^{-(x+y)}, & x>0,\ y>0, \\ 0, & \text{其他}. \end{cases}` |
| 1520 | 13310-13312 | 0.26 | inline_unsafe_marker | bracket | `f_Z(z) = \begin{cases} \dfrac{z^2}{2}e^{-z}, & z > 0 \\ 0, & z \leqslant 0 \end{cases}` |
| 1521 | 13334-13336 | 0.27 | inline_unsafe_marker | bracket | `f_X(x) = \begin{cases} 2e^{-2x}, & x > 0, \\ 0, & \text{其他}, \end{cases} \quad f_Y(y) = \begin{cases} 3y^2, & 0 < y < 1, \\ 0, & \text{其他}. \end{cases}` |
| 1522 | 13342-13344 | 0.46 | inline_unsafe_marker | bracket | `f(x,y) = f_X(x)\,f_Y(y) = \begin{cases} 6y^2 e^{-2x}, & x > 0,\ 0 < y < 1 \\ 0, & \text{其他} \end{cases}` |
| 1526 | 13372-13374 | 0.42 | display_environment | env:align* | `f_Z(z) &= \frac{\mathrm{d}}{\mathrm{d}z} F_Z(z) = \frac{3(e^2-1)}{2}e^{-2z}` |
| 1527 | 13377-13379 | 0.45 | inline_unsafe_marker | bracket | `f_Z(z) = \begin{cases} 3z^2 - 3z + \dfrac{3}{2} - \dfrac{3}{2}e^{-2z}, & 0 < z < 1 \\ \dfrac{3(e^2-1)}{2}e^{-2z}, & z \geqslant 1 \\ 0, & \text{其他} \end{cases}` |
| 1528 | 13384-13386 | 0.11 | inline_safe | bracket | `Z=2X-Y` |
| 1529 | 13391-13393 | 0.34 | inline_safe | bracket | `0<x<1,\qquad 2x-z\ge0.` |
| 1530 | 13395-13398 | 0.43 | normalized_width_not_low | bracket | `f_Z(z)=\int f_X(x)f_Y(2x-z)\,\mathrm dx =\int e^{-(2x-z)}\,\mathrm dx,` |
| 1531 | 13402-13405 | 0.42 | normalized_width_not_low | bracket | `f_Z(z)=\int_0^1 e^{-(2x-z)}\,\mathrm dx =\frac{e^z(1-e^{-2})}{2}.` |
| 1532 | 13407-13410 | 0.45 | normalized_width_not_low | bracket | `f_Z(z)=\int_{z/2}^{1} e^{-(2x-z)}\,\mathrm dx =\frac{1-e^{z-2}}{2}.` |
| 1533 | 13412-13419 | 0.21 | inline_unsafe_marker | bracket | `f_Z(z)= \begin{cases} \dfrac{e^z(1-e^{-2})}{2}, & z\le0,\\[6pt] \dfrac{1-e^{z-2}}{2}, & 0<z<2,\\[6pt] 0, & z\ge2. \end{cases}` |
| 1534 | 13428-13430 | 0.25 | inline_unsafe_marker | bracket | `f(x,y) = \begin{cases} \dfrac{1}{2}, & 0 \leqslant x \leqslant 2,\ 0 \leqslant y \leqslant 1 \\ 0, & \text{其他} \end{cases}` |
| 1537 | 13450-13452 | 0.29 | inline_unsafe_marker | bracket | `f_Z(z) = \begin{cases} \dfrac{1}{2}(\ln 2 - \ln z), & 0 < z < 2 \\ 0, & \text{其他} \end{cases}` |
| 1546 | 13529-13531 | 0.46 | inline_safe | bracket | `f_Z(z) = \int_{-\infty}^{+\infty}\|y\|\,f(yz, y)\,\mathrm{d}y.` |
| 1559 | 13654-13656 | 0.49 | inline_safe | bracket | `P(X+Y=k) = \binom{n+m}{k} p^k (1-p)^{n+m-k},` |
| 1563 | 13685-13688 | 0.38 | normalized_width_not_low | bracket | `P(X=k)=\frac{3^k}{k!}e^{-3},\qquad P(Y=i-k)=\frac{3^{i-k}}{(i-k)!}e^{-3}.` |
| 1564 | 13690-13699 | 0.46 | inline_unsafe_marker | bracket | `\begin{aligned} P(X+Y=i) &=\sum_{k=0}^{i}\frac{3^k}{k!}e^{-3}\cdot \frac{3^{i-k}}{(i-k)!}e^{-3}\\ &=e^{-6}\frac{1}{i!}\sum_{k=0}^{i}\binom{i}{k}3^k3^{i-k}\\ &=e^{-6}\frac{(3+3)^...` |
| 1565 | 13705-13707 | 0.36 | inline_safe | bracket | `\varphi_X(t) = \exp\left(i\mu t - \frac{1}{2}\sigma^2 t^2\right).` |
| 1569 | 13748-13750 | 0.44 | inline_safe | bracket | `F_{\max}(z) = P\{X \leqslant z, Y \leqslant z\} = F(z, z).` |
| 1577 | 13828-13830 | 0.27 | inline_unsafe_marker | bracket | `f(x,y) = \begin{cases} \dfrac{1}{(b-a)^2}, & a \leqslant x \leqslant b,\ a \leqslant y \leqslant b, \\ 0, & \text{其他}. \end{cases}` |
| 1579 | 13838-13840 | 0.37 | inline_unsafe_marker | bracket | `f_Z(z) = F_Z'(z) = \begin{cases} \dfrac{2(z-a)}{(b-a)^2}, & a \leqslant z \leqslant b, \\ 0, & \text{其他}. \end{cases}` |
| 1581 | 13862-13864 | 0.45 | inline_safe | bracket | `f_X(x)=\frac{1}{\pi(1+x^2)},\qquad x\in\mathbb R,` |
| 1582 | 13873-13875 | 0.47 | inline_safe | bracket | `x=\frac y3,\qquad \left\|\frac{\mathrm dx}{\mathrm dy}\right\|=\frac13.` |
| 1583 | 13877-13881 | 0.37 | normalized_width_not_low | bracket | `f_Y(y)=f_X\!\left(\frac y3\right)\cdot\frac13 =\frac{1}{\pi\left(1+\frac{y^2}{9}\right)}\cdot\frac13 =\frac{3}{\pi(9+y^2)},\qquad y\in\mathbb R.` |
| 1586 | 13898-13900 | 0.44 | inline_unsafe_marker | bracket | `f_Y(y) = \begin{cases} \dfrac{1}{2\sqrt{\pi(y-1)}}\,\exp\!\left\{-\dfrac{y-1}{4}\right\}, & y > 1, \\ 0, & y \leqslant 1. \end{cases}` |
| 1587 | 13907-13909 | 0.22 | inline_unsafe_marker | bracket | `f(x,y) = \begin{cases} \lambda e^{-\lambda y}, & 0 < x < y, \\ 0, & \text{其他}, \end{cases}` |
| 1592 | 13935-13937 | 0.35 | inline_unsafe_marker | bracket | `f_Z(z) = \begin{cases} e^{-\lambda z/2} - e^{-\lambda z}, & z > 0, \\ 0, & z \leqslant 0. \end{cases}` |
| 1593 | 13939-13941 | 0.31 | inline_unsafe_marker | bracket | `f_N(n) = f_X(n) = \begin{cases} e^{-\lambda n}, & n > 0, \\ 0, & n \leqslant 0. \end{cases}` |
| 1594 | 13948-13950 | 0.39 | inline_unsafe_marker | bracket | `f_X(x) = \begin{cases} e^{-x}, & x > 0, \\ 0, & x \leqslant 0, \end{cases} \quad f_Y(y) = \begin{cases} \dfrac{1}{2}e^{-y/2}, & y > 0, \\ 0, & y \leqslant 0. \end{cases}` |
| 1597 | 13965-13967 | 0.32 | inline_unsafe_marker | bracket | `f_Z(z) = \begin{cases} e^{-z/2} - e^{-z}, & z > 0, \\ 0, & z \leqslant 0. \end{cases}` |
| 1598 | 13975-13977 | 0.22 | inline_unsafe_marker | bracket | `f(x,y) = \begin{cases} cxe^{-y}, & 0 < x < y < +\infty, \\ 0, & \text{其他}. \end{cases}` |
| 1606 | 14017-14019 | 0.42 | inline_unsafe_marker | bracket | `f_Z(z) = \begin{cases} \left(\dfrac{z}{2}-1\right)e^{-z/2} + e^{-z}, & z \geqslant 0, \\ 0, & z < 0. \end{cases}` |
| 1612 | 14052-14054 | 0.25 | inline_unsafe_marker | bracket | `f_Z(z) = \begin{cases} \dfrac{1}{(z+1)^2}, & z > 0, \\ 0, & z \leqslant 0. \end{cases}` |
| 1615 | 14075-14077 | 0.25 | inline_unsafe_marker | bracket | `f_Z(z) = \begin{cases} \dfrac{2(b-z)}{(b-a)^2}, & a \leqslant z \leqslant b, \\ 0, & \text{其他}. \end{cases}` |
| 1616 | 14091-14093 | 0.40 | inline_safe | bracket | `X\sim P(\lambda_1),\qquad Y\sim P(\lambda_2),` |
| 1617 | 14095-14097 | 0.26 | inline_safe | bracket | `X+Y\sim P(\lambda_1+\lambda_2).` |
| 1619 | 14124-14126 | 0.43 | inline_safe | bracket | `Z=\min(X,Y),\qquad W=\max(X,Y),` |
| 1620 | 14128-14130 | 0.15 | inline_safe | bracket | `Z+W=X+Y.` |
| 1621 | 14132-14134 | 0.33 | inline_safe | bracket | `P(Z+W\geqslant 1)=P(X+Y\geqslant 1).` |
| 1622 | 14137-14139 | 0.40 | inline_safe | bracket | `G=\{(x,y):0\le x\le 1,\ 0\le y\le 2\}` |
| 1623 | 14141-14143 | 0.43 | inline_safe | bracket | `f(x,y)=\frac12\qquad ((x,y)\in G).` |
| 1625 | 14153-14155 | 0.27 | inline_safe | bracket | `P(Z+W\geqslant 1)=\frac34.` |
| 1626 | 14161-14163 | 0.35 | inline_unsafe_marker | bracket | `f(x,y) = \begin{cases} \dfrac{2}{\pi}\,e^{-\frac{x^2+y^2}{2}}, & x>0,\ y>0, \\ 0, & \text{其他}. \end{cases}` |
| 1633 | 14216-14218 | 0.45 | inline_safe | bracket | `P(\xi=k)=\frac13,\qquad k=1,2,3.` |
| 1634 | 14220-14222 | 0.43 | inline_safe | bracket | `X=\max(\xi,\eta),\qquad Y=\min(\xi,\eta).` |
| 1635 | 14231-14233 | 0.29 | inline_safe | bracket | `P(X=x,Y=x)=\frac19.` |
| 1636 | 14235-14237 | 0.29 | inline_safe | bracket | `P(X=x,Y=y)=\frac29.` |
| 1637 | 14239-14247 | 0.09 | inline_unsafe_marker | bracket | `\begin{array}{c\|ccc} & X=1 & X=2 & X=3\\ \hline Y=1 & \dfrac19 & \dfrac29 & \dfrac29\\[4pt] Y=2 & 0 & \dfrac19 & \dfrac29\\[4pt] Y=3 & 0 & 0 & \dfrac19 \end{array}.` |
| 1640 | 14265-14271 | 0.27 | inline_unsafe_marker | bracket | `f(x,y)= \begin{cases} \dfrac32xy^2, & 0\le x\le 2,\ 0\le y\le 1,\\ 0, & \text{其他}. \end{cases}` |
| 1641 | 14276-14280 | 0.39 | normalized_width_not_low | bracket | `f_X(x)=\int_0^1 \frac32xy^2\,\mathrm{d}y =\frac32x\cdot\frac13 =\frac{x}{2}.` |
| 1642 | 14282-14286 | 0.39 | normalized_width_not_low | bracket | `f_Y(y)=\int_0^2 \frac32xy^2\,\mathrm{d}x =\frac32y^2\cdot\frac{2^2}{2} =3y^2.` |
| 1644 | 14302-14304 | 0.21 | inline_safe | bracket | `Y\|X=n\sim B(n,p).` |
| 1645 | 14306-14312 | 0.46 | inline_unsafe_marker | bracket | `\begin{aligned} P(X=n,Y=k) &=P(X=n)P(Y=k\|X=n)\\ &=e^{-\lambda}\frac{\lambda^n}{n!}\binom nkp^k(1-p)^{n-k}. \end{aligned}` |
| 1647 | 14328-14330 | 0.13 | inline_safe | bracket | `Y\sim P(\lambda p).` |
| 1648 | 14339-14347 | 0.08 | inline_unsafe_marker | bracket | `\begin{array}{c\|cccc} & \eta=1 & \eta=2 & \eta=4 & \eta=5\\ \hline \zeta=0 & 0.05 & 0.12 & 0.15 & 0.07\\ \zeta=1 & 0.03 & 0.10 & 0.08 & 0.11\\ \zeta=2 & 0.07 & 0.01 & 0.11 & 0.1...` |
| 1651 | 14363-14365 | 0.26 | inline_safe | bracket | `P(\zeta=0,\eta=1)=0.05,` |
| 1652 | 14367-14369 | 0.48 | inline_safe | bracket | `P(\zeta=0)P(\eta=1)=0.39\times0.15=0.0585.` |
| 1653 | 14373-14379 | 0.13 | inline_unsafe_marker | bracket | `\begin{array}{c\|ccccccc} Z & 0 & 1 & 2 & 4 & 5 & 8 & 10\\ \hline P & 0.39 & 0.03 & 0.17 & 0.09 & 0.11 & 0.11 & 0.10 \end{array}.` |
| 1655 | 14392-14394 | 0.16 | inline_safe | bracket | `E(\zeta\eta)=3.16.` |
| 1656 | 14402-14414 | 0.11 | inline_unsafe_marker | bracket | `X\sim \begin{pmatrix} 1&2&3\\ 0.5&0.1&0.4 \end{pmatrix}, \qquad Y\sim \begin{pmatrix} 1&2&3\\ 0.3&0.3&0.4 \end{pmatrix}.` |
| 1659 | 14432-14434 | 0.27 | inline_safe | bracket | `P(X=Y)=0.34=\frac{17}{50}.` |
| 1660 | 14445-14447 | 0.14 | inline_safe | bracket | `\binom42=6.` |
| 1661 | 14449-14451 | 0.45 | inline_safe | bracket | `(1,2),(1,3),(1,4),(2,3),(2,4),(3,4),` |
| 1662 | 14453-14461 | 0.09 | inline_unsafe_marker | bracket | `\begin{array}{c\|ccc} & \xi=2 & \xi=3 & \xi=4\\ \hline \eta=1 & \dfrac16 & \dfrac16 & \dfrac16\\[4pt] \eta=2 & 0 & \dfrac16 & \dfrac16\\[4pt] \eta=3 & 0 & 0 & \dfrac16 \end{array}.` |
| 1665 | 14471-14473 | 0.29 | inline_safe | bracket | `P(\xi=2,\eta=1)=\frac16,` |
| 1668 | 14490-14502 | 0.11 | inline_unsafe_marker | bracket | `\xi= \begin{cases} 1, & A\text{ 发生},\\ 0, & A\text{ 不发生}, \end{cases} \qquad \eta= \begin{cases} 1, & B\text{ 发生},\\ 0, & B\text{ 不发生}. \end{cases}` |
| 1669 | 14509-14511 | 0.49 | inline_safe | bracket | `P(\xi=1)=P(A),\qquad P(\eta=1)=P(B).` |
| 1671 | 14517-14520 | 0.38 | normalized_width_not_low | bracket | `P(A\overline B)=P(A)P(\overline B),\qquad P(\overline A B)=P(\overline A)P(B),` |
| 1672 | 14521-14523 | 0.33 | inline_safe | bracket | `P(\overline A\,\overline B)=P(\overline A)P(\overline B).` |
| 1674 | 14535-14541 | 0.18 | inline_unsafe_marker | bracket | `p(x,y)= \begin{cases} Ce^{-2(x+y)}, & x>0,\ y>0,\\ 0, & \text{其他}. \end{cases}` |
| 1675 | 14550-14554 | 0.49 | normalized_width_not_low | bracket | `1=\int_0^\infty\int_0^\infty Ce^{-2(x+y)}\,\mathrm{d}y\,\mathrm{d}x =C\left(\int_0^\infty e^{-2x}\,\mathrm{d}x\right)^2 =C\left(\frac12\right)^2.` |
| 1676 | 14556-14558 | 0.07 | inline_safe | bracket | `C=4.` |
| 1677 | 14561-14563 | 0.28 | inline_safe | bracket | `p(x,y)=4e^{-2(x+y)}.` |
| 1683 | 14593-14595 | 0.16 | inline_safe | bracket | `\operatorname{Cov}(\xi,\eta)=0.` |
| 1684 | 14617-14619 | 0.21 | inline_safe | bracket | `\frac{x^2}{a^2}+\frac{y^2}{b^2}\le1` |
| 1685 | 14627-14633 | 0.22 | inline_unsafe_marker | bracket | `f(x,y)= \begin{cases} \dfrac1{\pi ab}, & \dfrac{x^2}{a^2}+\dfrac{y^2}{b^2}\le1,\\[6pt] 0, & \text{其他}. \end{cases}` |
| 1686 | 14635-14637 | 0.43 | inline_safe | bracket | `-b\sqrt{1-\frac{x^2}{a^2}}\le y\le b\sqrt{1-\frac{x^2}{a^2}}.` |
| 1688 | 14644-14650 | 0.25 | inline_unsafe_marker | bracket | `f_X(x)= \begin{cases} \dfrac2{\pi a}\sqrt{1-\dfrac{x^2}{a^2}}, & \|x\|\le a,\\[6pt] 0, & \text{其他}. \end{cases}` |
| 1689 | 14652-14658 | 0.25 | inline_unsafe_marker | bracket | `f_Y(y)= \begin{cases} \dfrac2{\pi b}\sqrt{1-\dfrac{y^2}{b^2}}, & \|y\|\le b,\\[6pt] 0, & \text{其他}. \end{cases}` |
| 1690 | 14661-14663 | 0.44 | inline_safe | bracket | `EX^2=\frac{a^2}{4},\qquad EY^2=\frac{b^2}{4}.` |
| 1691 | 14665-14667 | 0.48 | inline_safe | bracket | `DX=\frac{a^2}{4}=25,\qquad DY=\frac{b^2}{4}=4.` |
| 1692 | 14669-14671 | 0.27 | inline_safe | bracket | `a=10,\qquad b=4.` |
| 1693 | 14678-14680 | 0.15 | inline_safe | bracket | `Z=\min\{X,Y\}` |
| 1694 | 14685-14687 | 0.26 | inline_safe | bracket | `F_Z(z)=P(Z\le z)=0.` |
| 1695 | 14689-14697 | 0.25 | inline_unsafe_marker | bracket | `\begin{aligned} F_Z(z) &=1-P(Z>z)\\ &=1-P(X>z,Y>z)\\ &=1-P(X>z)P(Y>z)\\ &=1-(1-z)e^{-5z}. \end{aligned}` |
| 1696 | 14699-14701 | 0.13 | inline_safe | bracket | `F_Z(z)=1.` |
| 1697 | 14703-14710 | 0.22 | inline_unsafe_marker | bracket | `F_Z(z)= \begin{cases} 0, & z\le0,\\ 1-(1-z)e^{-5z}, & 0<z\le1,\\ 1, & z>1. \end{cases}` |
| 1698 | 14713-14716 | 0.39 | normalized_width_not_low | bracket | `f_Z(z)=\frac{\mathrm{d}}{\mathrm{d}z}\left[1-(1-z)e^{-5z}\right] =(6-5z)e^{-5z}.` |
| 1699 | 14718-14724 | 0.19 | inline_unsafe_marker | bracket | `f_Z(z)= \begin{cases} (6-5z)e^{-5z}, & 0<z<1,\\ 0, & \text{其他}. \end{cases}` |
| 1700 | 14731-14737 | 0.13 | inline_unsafe_marker | bracket | `f(x,y)= \begin{cases} 6x, & 0<x<y<1,\\ 0, & \text{其他}. \end{cases}` |
| 1701 | 14745-14747 | 0.43 | inline_safe | bracket | `f_X(x)=\int_x^1 6x\,\mathrm{d}y=6x(1-x),` |
| 1702 | 14749-14751 | 0.38 | inline_safe | bracket | `f_Y(y)=\int_0^y 6x\,\mathrm{d}x=3y^2,` |
| 1703 | 14753-14765 | 0.12 | inline_unsafe_marker | bracket | `f_X(x)= \begin{cases} 6x(1-x),&0<x<1,\\ 0,&\text{其他}, \end{cases} \qquad f_Y(y)= \begin{cases} 3y^2,&0<y<1,\\ 0,&\text{其他}. \end{cases}` |
| 1704 | 14768-14770 | 0.42 | inline_safe | bracket | `0<x<\frac12,\qquad x<y<1-x.` |
| 1706 | 14779-14781 | 0.48 | inline_safe | bracket | `EX=\int_0^1 x\cdot6x(1-x)\,\mathrm{d}x=\frac12,` |
| 1707 | 14782-14784 | 0.43 | inline_safe | bracket | `EY=\int_0^1 y\cdot3y^2\,\mathrm{d}y=\frac34,` |
| 1708 | 14785-14788 | 0.47 | normalized_width_not_low | bracket | `E(XY)=\int_0^1\int_0^y xy\cdot6x\,\mathrm{d}x\,\mathrm{d}y =\int_0^1 2y^4\,\mathrm{d}y=\frac25.` |
| 1709 | 14790-14794 | 0.35 | normalized_width_not_low | bracket | `\operatorname{Cov}(X,Y)=E(XY)-EX\,EY =\frac25-\frac12\cdot\frac34 =\frac1{40}.` |
| 1710 | 14799-14805 | 0.13 | inline_unsafe_marker | bracket | `f(x,y)= \begin{cases} 6x, & 0<x<y<1,\\ 0, & \text{其他}. \end{cases}` |
| 1711 | 14813-14815 | 0.43 | inline_safe | bracket | `f_X(x)=\int_x^1 6x\,\mathrm{d}y=6x(1-x).` |
| 1712 | 14817-14819 | 0.38 | inline_safe | bracket | `f_Y(y)=\int_0^y 6x\,\mathrm{d}x=3y^2.` |
| 1713 | 14821-14833 | 0.12 | inline_unsafe_marker | bracket | `f_X(x)= \begin{cases} 6x(1-x),&0<x<1,\\ 0,&\text{其他}, \end{cases} \qquad f_Y(y)= \begin{cases} 3y^2,&0<y<1,\\ 0,&\text{其他}. \end{cases}` |
| 1714 | 14836-14840 | 0.29 | normalized_width_not_low | bracket | `f_X\left(\frac13\right) =6\cdot\frac13\cdot\frac23 =\frac43.` |
| 1715 | 14842-14844 | 0.37 | inline_safe | bracket | `f\left(\frac13,y\right)=6\cdot\frac13=2.` |
| 1716 | 14846-14851 | 0.41 | normalized_width_not_low | bracket | `f_{Y\|X}\left(y\mid \frac13\right) =\frac{f(1/3,y)}{f_X(1/3)} =\frac{2}{4/3} =\frac32,\qquad \frac13<y<1.` |
| 1717 | 14853-14859 | 0.23 | inline_unsafe_marker | bracket | `f_{Y\|X}\left(y\mid \frac13\right)= \begin{cases} \dfrac32, & \dfrac13<y<1,\\[6pt] 0, & \text{其他}. \end{cases}` |
| 1718 | 14862-14864 | 0.42 | inline_safe | bracket | `0<x<\frac12,\qquad x<y<1-x.` |
| 1719 | 14866-14871 | 0.41 | normalized_width_not_low | bracket | `P(X+Y\le1) =\int_0^{1/2}\int_x^{1-x}6x\,\mathrm{d}y\,\mathrm{d}x =\int_0^{1/2}6x(1-2x)\,\mathrm{d}x =\frac14.` |
| 1720 | 14876-14882 | 0.15 | inline_unsafe_marker | bracket | `f(x,y)= \begin{cases} 2e^{-2x-y},&x>0,\ y>0,\\ 0,&\text{其他}. \end{cases}` |
| 1723 | 14896-14904 | 0.33 | inline_unsafe_marker | bracket | `\begin{aligned} F_Z(z) &=P\{\max(X,Y)\le z\}\\ &=P(X\le z,Y\le z)\\ &=F_X(z)F_Y(z) =(1-e^{-2z})(1-e^{-z}). \end{aligned}` |
| 1725 | 14911-14917 | 0.34 | inline_unsafe_marker | bracket | `f_Z(z)= \begin{cases} e^{-z}+2e^{-2z}-3e^{-3z},&z>0,\\ 0,&\text{其他}. \end{cases}` |
| 1726 | 14922-14924 | 0.30 | inline_safe | bracket | `\{(x,y):0<x<2,\ 0<y<1\}` |
| 1727 | 14931-14937 | 0.21 | inline_unsafe_marker | bracket | `f(x,y)= \begin{cases} \dfrac12,&0<x<2,\ 0<y<1,\\ 0,&\text{其他}. \end{cases}` |
| 1728 | 14939-14951 | 0.11 | inline_unsafe_marker | bracket | `f_X(x)= \begin{cases} \dfrac12,&0<x<2,\\ 0,&\text{其他}, \end{cases} \qquad f_Y(y)= \begin{cases} 1,&0<y<1,\\ 0,&\text{其他}. \end{cases}` |
| 1729 | 14953-14955 | 0.28 | inline_safe | bracket | `F(x,y)=F_X(x)F_Y(y),` |
| 1730 | 14957-14971 | 0.11 | inline_unsafe_marker | bracket | `F_X(x)= \begin{cases} 0,&x\le0,\\ \dfrac{x}{2},&0<x\le2,\\ 1,&x>2, \end{cases} \qquad F_Y(y)= \begin{cases} 0,&y\le0,\\ y,&0<y\le1,\\ 1,&y>1. \end{cases}` |
| 1732 | 14979-14984 | 0.25 | normalized_width_not_low | bracket | `\operatorname{Cov}(\xi,\eta) =\operatorname{Cov}(X+Y,aX+bY) =aDX+bDY =\frac a3+\frac b{12}.` |
| 1735 | 14994-14998 | 0.23 | normalized_width_not_low | bracket | `\frac{a^2}{3}+\frac{16a^2}{12}=1 \quad\Longrightarrow\quad \frac{5a^2}{3}=1.` |
| 1736 | 15000-15002 | 0.49 | inline_safe | bracket | `a=\pm\sqrt{\frac35},\qquad b=\mp4\sqrt{\frac35}.` |
| 1737 | 15009-15015 | 0.08 | inline_unsafe_marker | bracket | `\begin{array}{c\|cccc} (X,Y)&(1,0)&(1,1)&(2,0)&(2,1)\\ \hline P&0.4&0.2&a&b \end{array}` |
| 1738 | 15020-15022 | 0.25 | inline_safe | bracket | `0.4+0.2+a+b=1,` |
| 1739 | 15024-15026 | 0.14 | inline_safe | bracket | `a+b=0.4.` |
| 1741 | 15034-15036 | 0.18 | inline_safe | bracket | `0.2+2b=0.8,` |
| 1742 | 15038-15040 | 0.09 | inline_safe | bracket | `b=0.3.` |
| 1743 | 15042-15044 | 0.21 | inline_safe | bracket | `a=0.4-b=0.1.` |
| 1744 | 15049-15055 | 0.23 | inline_unsafe_marker | bracket | `f(x,y)= \begin{cases} A\left(x^2+\dfrac12xy\right),&0<x<1,\ 0<y<2,\\[6pt] 0,&\text{其他}. \end{cases}` |
| 1746 | 15073-15075 | 0.14 | inline_safe | bracket | `A=\frac67.` |
| 1747 | 15078-15085 | 0.48 | inline_unsafe_marker | bracket | `\begin{aligned} f_X(x) &=\int_0^2 \frac67\left(x^2+\frac12xy\right)\,\mathrm dy\\ &=\frac67(2x^2+x) =\frac{12}{7}x^2+\frac67x. \end{aligned}` |
| 1748 | 15087-15093 | 0.23 | inline_unsafe_marker | bracket | `f_X(x)= \begin{cases} \dfrac{12}{7}x^2+\dfrac67x,&0<x<1,\\[6pt] 0,&\text{其他}. \end{cases}` |
| 1749 | 15095-15099 | 0.47 | normalized_width_not_low | bracket | `EX=\int_0^1 x\left(\frac{12}{7}x^2+\frac67x\right)\,\mathrm dx =\frac{12}{7}\cdot\frac14+\frac67\cdot\frac13 =\frac57.` |
| 1750 | 15102-15104 | 0.31 | inline_safe | bracket | `0<x<1,\qquad 0<y<x.` |
| 1752 | 15121-15130 | 0.09 | inline_unsafe_marker | bracket | `\begin{array}{c\|cccc} & Y=-1 & Y=0 & Y=1 & Y=2\\ \hline X=-2 & a & 0 & 0 & 0\\ X=-1 & 0.14 & b & 0 & 0\\ X=0 & 0.01 & 0.02 & 0.03 & 0\\ X=1 & 0.12 & 0.13 & 0.14 & 0.15 \end{array}` |
| 1754 | 15142-15144 | 0.15 | inline_safe | bracket | `a+b=0.26.` |
| 1756 | 15155-15157 | 0.17 | inline_safe | bracket | `3a+b=0.60.` |
| 1757 | 15159-15161 | 0.43 | inline_safe | bracket | `a+b=0.26,\qquad 3a+b=0.60,` |
| 1758 | 15163-15165 | 0.33 | inline_safe | bracket | `a=0.17,\qquad b=0.09.` |
| 1759 | 15168-15170 | 0.26 | inline_safe | bracket | `P(X=-2)=a=0.17,` |
| 1760 | 15171-15173 | 0.34 | inline_safe | bracket | `P(X=-1)=0.14+b=0.23,` |
| 1761 | 15174-15176 | 0.44 | inline_safe | bracket | `P(X=0)=0.01+0.02+0.03=0.06,` |
| 1763 | 15181-15190 | 0.17 | inline_unsafe_marker | bracket | `F_X(x)= \begin{cases} 0, & x<-2,\\ 0.17, & -2\le x<-1,\\ 0.40, & -1\le x<0,\\ 0.46, & 0\le x<1,\\ 1, & x\ge1. \end{cases}` |
| 1765 | 15206-15208 | 0.23 | inline_safe | bracket | `\{0<x<a,\ 0<y<b\}` |
| 1766 | 15216-15222 | 0.21 | inline_unsafe_marker | bracket | `f(x,y)= \begin{cases} \dfrac1{ab}, & 0<x<a,\ 0<y<b,\\ 0, & \text{其他}. \end{cases}` |
| 1767 | 15224-15236 | 0.11 | inline_unsafe_marker | bracket | `f_X(x)= \begin{cases} \dfrac1a, & 0<x<a,\\ 0, & \text{其他}, \end{cases} \qquad f_Y(y)= \begin{cases} \dfrac1b, & 0<y<b,\\ 0, & \text{其他}. \end{cases}` |
| 1768 | 15239-15241 | 0.38 | inline_safe | bracket | `DX=\frac{a^2}{12},\qquad DY=\frac{b^2}{12}.` |
| 1769 | 15243-15245 | 0.38 | inline_safe | bracket | `\frac{a^2}{12}=12,\qquad \frac{b^2}{12}=36.` |
| 1770 | 15247-15249 | 0.32 | inline_safe | bracket | `a=12,\qquad b=12\sqrt3.` |
| 1772 | 15260-15266 | 0.21 | inline_unsafe_marker | bracket | `f(x,y)= \begin{cases} Axy, & 0<x<1,\ 0<y<1,\\ 0, & \text{其他}. \end{cases}` |
| 1773 | 15275-15279 | 0.40 | normalized_width_not_low | bracket | `1=\int_0^1\int_0^1 Axy\,\mathrm{d}y\,\mathrm{d}x =A\left(\int_0^1 x\,\mathrm{d}x\right)\left(\int_0^1 y\,\mathrm{d}y\right) =\frac{A}{4}.` |
| 1774 | 15281-15283 | 0.07 | inline_safe | bracket | `A=4.` |
| 1776 | 15292-15299 | 0.47 | inline_unsafe_marker | bracket | `\begin{aligned} E(e^{tX+sY}) &=\int_0^1\int_0^1 e^{tx+sy}4xy\,\mathrm{d}y\,\mathrm{d}x\\ &=4\left(\int_0^1 xe^{tx}\,\mathrm{d}x\right) \left(\int_0^1 ye^{sy}\,\mathrm{d}y\right)...` |
| 1779 | 15308-15312 | 0.37 | normalized_width_not_low | bracket | `E(e^{tX+sY}) =4\left(\frac{e^t}{t}-\frac{e^t}{t^2}+\frac1{t^2}\right) \left(\frac{e^s}{s}-\frac{e^s}{s^2}+\frac1{s^2}\right),` |
| 1781 | 15320-15322 | 0.38 | inline_safe | bracket | `EX=\int_0^1 2x^2\,\mathrm{d}x=\frac23,` |
| 1782 | 15323-15325 | 0.41 | inline_safe | bracket | `EX^2=\int_0^1 2x^3\,\mathrm{d}x=\frac12,` |
| 1784 | 15330-15332 | 0.16 | inline_safe | bracket | `\operatorname{Cov}(X,Y)=0.` |
| 1785 | 15339-15341 | 0.35 | inline_safe | bracket | `1\le x\le2,\qquad 1\le y\le3` |
| 1786 | 15349-15351 | 0.21 | inline_safe | bracket | `(2-1)(3-1)=2,` |
| 1787 | 15353-15359 | 0.21 | inline_unsafe_marker | bracket | `f(x,y)= \begin{cases} \dfrac12, & 1<x<2,\ 1<y<3,\\ 0, & \text{其他}. \end{cases}` |
| 1788 | 15361-15364 | 0.34 | normalized_width_not_low | bracket | `f_\xi(x)=\int_1^3\frac12\,\mathrm{d}y =1,\qquad 1<x<2,` |
| 1789 | 15365-15368 | 0.34 | normalized_width_not_low | bracket | `f_\eta(y)=\int_1^2\frac12\,\mathrm{d}x =\frac12,\qquad 1<y<3.` |
| 1790 | 15370-15382 | 0.11 | inline_unsafe_marker | bracket | `f_\xi(x)= \begin{cases} 1, & 1<x<2,\\ 0, & \text{其他}, \end{cases} \qquad f_\eta(y)= \begin{cases} \dfrac12, & 1<y<3,\\ 0, & \text{其他}. \end{cases}` |
| 1791 | 15385-15392 | 0.43 | inline_unsafe_marker | bracket | `\begin{aligned} P(\xi<1.5,\eta<4) &=\int_1^{1.5}\int_1^3 \frac12\,\mathrm{d}y\,\mathrm{d}x\\ &=\int_1^{1.5}1\,\mathrm{d}x =0.5. \end{aligned}` |
| 1793 | 15405-15411 | 0.20 | inline_unsafe_marker | bracket | `f(x,y)= \begin{cases} 1, & \|y\|<x,\ 0<x<1,\\ 0, & \text{其他}. \end{cases}` |
| 1794 | 15416-15418 | 0.36 | inline_safe | bracket | `f_X(x)=\int_{-x}^{x}1\,\mathrm{d}y=2x.` |
| 1795 | 15420-15422 | 0.40 | inline_safe | bracket | `f_{Y\|X}(y\|x)=\frac{f(x,y)}{f_X(x)}=\frac1{2x}.` |
| 1796 | 15424-15430 | 0.24 | inline_unsafe_marker | bracket | `f_{Y\|X}(y\|x)= \begin{cases} \dfrac1{2x}, & 0<x<1,\ -x<y<x,\\[6pt] 0, & \text{其他}. \end{cases}` |
| 1797 | 15435-15437 | 0.13 | inline_safe | bracket | `Z=3X+2Y` |
| 1798 | 15442-15444 | 0.28 | inline_safe | bracket | `U=3X,\qquad V=2Y.` |
| 1799 | 15446-15448 | 0.45 | inline_safe | bracket | `f_U(u)=\frac{\lambda}{3}e^{-\lambda u/3},\qquad u>0,` |
| 1800 | 15449-15451 | 0.45 | inline_safe | bracket | `f_V(v)=\frac{\mu}{2}e^{-\mu v/2},\qquad v>0.` |
| 1801 | 15453-15463 | 0.37 | inline_unsafe_marker | bracket | `\begin{aligned} f_Z(z) &=\int_0^z f_U(u)f_V(z-u)\,\mathrm{d}u\\ &=\int_0^z \frac{\lambda}{3}e^{-\lambda u/3} \frac{\mu}{2}e^{-\mu(z-u)/2}\,\mathrm{d}u\\ &=\frac{\lambda\mu}{6}e^...` |
| 1802 | 15465-15470 | 0.29 | normalized_width_not_low | bracket | `f_Z(z)= \frac{\lambda\mu}{6} \frac{e^{-\mu z/2}-e^{-\lambda z/3}}{\lambda/3-\mu/2}, \qquad z>0.` |
| 1803 | 15472-15477 | 0.29 | normalized_width_not_low | bracket | `f_Z(z)= \frac{\lambda\mu}{2\lambda-3\mu} \left(e^{-\mu z/2}-e^{-\lambda z/3}\right), \qquad z>0.` |
| 1804 | 15479-15481 | 0.47 | inline_safe | bracket | `f_Z(z)=\frac{\lambda\mu}{6}z e^{-\lambda z/3},\qquad z>0.` |
| 1805 | 15483-15495 | 0.29 | inline_unsafe_marker | bracket | `f_Z(z)= \begin{cases} \displaystyle \frac{\lambda\mu}{2\lambda-3\mu} \left(e^{-\mu z/2}-e^{-\lambda z/3}\right), & z>0,\ 2\lambda\ne3\mu,\\[10pt] \displaystyle \frac{\lambda\mu}...` |
| 1806 | 15503-15505 | 0.11 | inline_safe | bracket | `W=X+Y.` |
| 1807 | 15509-15513 | 0.36 | normalized_width_not_low | bracket | `P(W=0)=(1-p)^2,\qquad P(W=1)=2p(1-p),\qquad P(W=2)=p^2.` |
| 1808 | 15515-15517 | 0.45 | inline_safe | bracket | `P(Z=1)=p,\qquad P(Z=0)=1-p.` |
| 1809 | 15519-15522 | 0.27 | inline_safe | bracket | `P(W=w,Z=z) =P(X+Y=w)P(Z=z),` |
| 1810 | 15524-15526 | 0.39 | inline_safe | bracket | `P(W=w,Z=z)=P(W=w)P(Z=z).` |
| 1811 | 15534-15536 | 0.27 | inline_safe | bracket | `y=x^2,\qquad y=x` |
| 1812 | 15538-15548 | 0.19 | inline_unsafe_marker | bracket | `\begin{array}{ll} \text{A. } f(x,y)=\begin{cases}6, & (x,y)\in G,\\0, & \text{其他},\end{cases} & \text{B. } f(x,y)=\begin{cases}1/6, & (x,y)\in G,\\0, & \text{其他},\end{cases} \\[...` |
| 1813 | 15554-15559 | 0.32 | normalized_width_not_low | bracket | `S_G=\int_0^1(x-x^2)\,\mathrm{d}x =\left[\frac{x^2}{2}-\frac{x^3}{3}\right]_0^1 =\frac12-\frac13 =\frac16.` |
| 1814 | 15561-15567 | 0.24 | inline_unsafe_marker | bracket | `f(x,y)= \begin{cases} 6, & 0<x<1,\ x^2<y<x,\\ 0, & \text{其他}. \end{cases}` |
| 1815 | 15572-15574 | 0.34 | inline_safe | bracket | `(X,Y)\sim N(0,0.5;\ 0,0.5;\ 0),` |
| 1816 | 15585-15587 | 0.37 | inline_safe | bracket | `D(X-Y)=DX+DY-2\operatorname{Cov}(X,Y).` |
| 1817 | 15589-15591 | 0.32 | inline_safe | bracket | `\operatorname{Cov}(X,Y)=\rho\sqrt{DX}\sqrt{DY}=0,` |
| 1818 | 15593-15595 | 0.22 | inline_safe | bracket | `Z=X-Y\sim N(0,1).` |
| 1820 | 15601-15604 | 0.34 | normalized_width_not_low | bracket | `D(\|Z\|)=E(\|Z\|^2)-[E\|Z\|]^2 =1-\frac2\pi.` |
| 1821 | 15614-15616 | 0.42 | inline_safe | bracket | `f_X(x)=\frac1a,\qquad 0<x<a.` |
| 1823 | 15622-15625 | 0.45 | normalized_width_not_low | bracket | `f(x,y)=f_X(x)f_{Y\|X}(y\|x) =\frac1{a(a-x)},\qquad 0<x<y<a,` |
| 1824 | 15627-15633 | 0.18 | inline_unsafe_marker | bracket | `f(x,y)= \begin{cases} \dfrac1{a(a-x)}, & 0<x<y<a,\\[8pt] 0, & \text{其他}. \end{cases}` |
| 1825 | 15636-15640 | 0.42 | normalized_width_not_low | bracket | `f_Y(y)=\int_0^y \frac1{a(a-x)}\,\mathrm{d}x =\frac1a\left[-\ln(a-x)\right]_0^y =\frac1a\ln\frac{a}{a-y}.` |
| 1826 | 15642-15648 | 0.20 | inline_unsafe_marker | bracket | `f_Y(y)= \begin{cases} \dfrac1a\ln\dfrac{a}{a-y}, & 0<y<a,\\[10pt] 0, & \text{其他}. \end{cases}` |
| 1828 | 15776-15778 | 0.30 | inline_safe | bracket | `EX = \sum_{i=1}^{\infty} x_i p_i.` |
| 1829 | 15781-15783 | 0.33 | inline_safe | bracket | `EX = \int_{-\infty}^{+\infty} x f(x)\,\mathrm{d}x.` |
| 1830 | 15789-15791 | 0.45 | inline_safe | bracket | `f(x) = \frac{1}{\pi(1+x^2)}, \quad -\infty < x < +\infty,` |
| 1832 | 15810-15813 | 0.28 | inline_unsafe_marker | bracket | `X \sim f(x) = \begin{cases} 2x\theta^2, & 0 < x < \dfrac{1}{\theta}\ (\theta > 0), \\[4pt] 0, & \text{其他}, \end{cases} \quad E[a(X+2Y)] = \frac{1}{\theta},` |
| 1834 | 15827-15829 | 0.44 | inline_safe | bracket | `E[a(X+2Y)] = 3a\cdot\frac{2}{3\theta} = \frac{2a}{\theta} = \frac{1}{\theta},` |
| 1836 | 15847-15849 | 0.39 | inline_safe | bracket | `\lambda^2 - 2\lambda + 2 = 1 \implies (\lambda - 1)^2 = 0,` |
| 1841 | 15898-15900 | 0.46 | inline_unsafe_marker | bracket | `Y = \begin{cases} 500n + 300(X-n) = 300X + 200n, & X \geqslant n, \\[4pt] 500X - 200(n-X) = 700X - 200n, & X < n. \end{cases}` |
| 1844 | 15920-15922 | 0.31 | inline_unsafe_marker | bracket | `L(y,X) = \begin{cases} 3y, & X \geqslant y, \\[4pt] 3X - (y - X) = 4X - y, & X < y. \end{cases}` |
| 1850 | 15953-15955 | 0.25 | inline_safe | bracket | `120+250=370\text{（万元）}.` |
| 1851 | 15962-15964 | 0.40 | inline_safe | bracket | `E[g(X)] = \sum_{i=1}^{\infty} g(x_i) p_i.` |
| 1852 | 15966-15968 | 0.43 | inline_safe | bracket | `E[g(X)] = \int_{-\infty}^{+\infty} g(x) f(x)\,\mathrm{d}x.` |
| 1853 | 15976-15978 | 0.43 | inline_safe | bracket | `\int_{-\infty}^{+\infty}\frac{\|x\|}{\pi(1+x^2)}\,\mathrm{d}x = +\infty,` |
| 1854 | 15990-15994 | 0.47 | normalized_width_not_low | bracket | `P(X=0)=0.9^2,\qquad P(X=1)=\mathrm{C}_2^1\cdot 0.1\cdot 0.9,\qquad P(X=2)=0.1^2.` |
| 1856 | 16004-16006 | 0.42 | inline_safe | bracket | `E(2^X)=0.81+0.36+0.04=1.21.` |
| 1857 | 16013-16015 | 0.14 | inline_safe | bracket | `Y=2^X-1.` |
| 1858 | 16020-16022 | 0.29 | inline_safe | bracket | `E(t^X)=(1-p+pt)^n.` |
| 1860 | 16028-16030 | 0.43 | inline_safe | bracket | `EY=E(2^X-1)=1.331-1=0.331.` |
| 1862 | 16050-16052 | 0.30 | inline_unsafe_marker | bracket | `f(y) = \begin{cases} \dfrac{y}{a^2}\,e^{-\frac{y^2}{2a^2}}, & y > 0,\ a > 0, \\[4pt] 0, & y \leqslant 0, \end{cases}` |
| 1864 | 16063-16065 | 0.49 | inline_safe | bracket | `\int_0^{+\infty}\frac{1}{\sqrt{2\pi}\,a}\,e^{-\frac{y^2}{2a^2}}\,\mathrm{d}y = \frac{1}{2},` |
| 1865 | 16067-16069 | 0.38 | inline_safe | bracket | `EZ = \frac{1}{a^2}\cdot\frac{\sqrt{2\pi}\,a}{2} = \frac{\sqrt{2\pi}}{2a}.` |
| 1866 | 16074-16076 | 0.36 | inline_safe | bracket | `D=\{(x,y)\mid 1\le x^2+y^2\le2\}` |
| 1867 | 16081-16083 | 0.43 | inline_safe | bracket | `f(x,y)=\frac1{8\pi}\exp\!\left\{-\frac{x^2+y^2}{8}\right\}.` |
| 1868 | 16085-16093 | 0.44 | inline_unsafe_marker | bracket | `\begin{aligned} P\{(X,Y)\in D\} &=\int_0^{2\pi}\int_1^{\sqrt2} \frac1{8\pi}e^{-r^2/8}\,r\,\mathrm dr\,\mathrm d\theta\\ &=\frac14\int_1^{\sqrt2}r e^{-r^2/8}\,\mathrm dr =e^{-1/8...` |
| 1869 | 16095-16097 | 0.46 | inline_safe | bracket | `f_R(r)=\frac{r}{4}e^{-r^2/8},\qquad r>0.` |
| 1870 | 16099-16102 | 0.46 | normalized_width_not_low | bracket | `EZ=\int_0^{+\infty}r\cdot\frac{r}{4}e^{-r^2/8}\,\mathrm dr =2\sqrt{\frac\pi2}=\sqrt{2\pi}.` |
| 1871 | 16111-16113 | 0.07 | inline_unsafe_marker | bracket | `Y = \begin{cases} 1, & X > 0, \\ 0, & X = 0, \\ -1, & X < 0, \end{cases}` |
| 1873 | 16141-16143 | 0.38 | inline_safe | bracket | `U + V = X + Y, \quad U \cdot V = X \cdot Y.` |
| 1877 | 16168-16168 | 0.46 | display_environment | dollar | `P(X = k) = \frac{\lambda^k e^{-\lambda}}{k!}, \quad k = 0, 1, 2, \dots` |
| 1882 | 16183-16183 | 0.26 | display_environment | dollar | `E[Y] = 1 - \frac{1 - e^{-\lambda}}{\lambda}` |
| 1884 | 16200-16200 | 0.23 | display_environment | dollar | `X = X_1 + X_2 + X_3` |
| 1886 | 16206-16206 | 0.23 | display_environment | dollar | `P(X_1 = 1) = \frac{a}{a+b}` |
| 1888 | 16216-16216 | 0.23 | display_environment | dollar | `P(X_3 = 1) = \frac{a}{a+b}` |
| 1895 | 16282-16284 | 0.40 | inline_safe | bracket | `f(x)=\frac12x,\qquad 0<x<2,` |
| 1896 | 16286-16291 | 0.36 | normalized_width_not_low | bracket | `EX=\int_0^2 x\cdot \frac12x\,\mathrm dx =\frac12\int_0^2 x^2\,\mathrm dx =\frac12\cdot\frac{8}{3} =\frac43.` |
| 1897 | 16297-16299 | 0.39 | inline_safe | bracket | `P\{F(X)>EX-1\}=P\left(Y>\frac13\right).` |
| 1898 | 16301-16303 | 0.44 | inline_safe | bracket | `P\left(Y>\frac13\right)=1-\frac13=\frac23.` |
| 1899 | 16309-16311 | 0.11 | inline_unsafe_marker | bracket | `F(x) = \begin{cases} 0, & x \leqslant 0, \\ \dfrac{x^2}{4}, & 0 < x < 2, \\ 1, & x \geqslant 2. \end{cases}` |
| 1900 | 16323-16325 | 0.38 | inline_safe | bracket | `E(XY) = EX \cdot EY = 1 \times \frac{1}{3} = \frac{1}{3}.` |
| 1901 | 16333-16336 | 0.18 | inline_unsafe_marker | bracket | `f_X(x) = \begin{cases} 3x^2, & 0 < x < 1, \\ 0, & \text{其他}, \end{cases}\quad f_Y(y) = \begin{cases} 2y, & 0 < y < 1, \\ 0, & \text{其他}, \end{cases}` |
| 1903 | 16357-16357 | 0.21 | inline_unsafe_marker | bracket | `f_{X_i}(x_i) =\begin{cases}\displaystyle \frac{1}{3}, & 0 < x_i < 3 \\0, & \text{其他}\end{cases}\quad (i=1,2)` |
| 1908 | 16377-16379 | 0.41 | inline_safe | bracket | `DD = ED^2 - (ED)^2 = \frac{3}{2} - 1 = \frac{1}{2}.` |
| 1909 | 16384-16386 | 0.22 | inline_safe | bracket | `\boldsymbol{E(X_{(k)}) = \frac{k}{n+1}}` |
| 1912 | 16400-16402 | 0.43 | inline_safe | bracket | `E(X_{(k)}) = \frac{k}{k + (n-k+1)} = \frac{k}{n+1}` |
| 1913 | 16407-16410 | 0.36 | normalized_width_not_low | bracket | `M = \max\{X_1, \dots, X_n\},\qquad N = \min\{X_1, \dots, X_n\}` |
| 1919 | 16458-16458 | 0.30 | display_environment | dollar | `P(Y \le 1) = \left(\frac{1}{3}\right)^3 = \frac{1}{27}` |
| 1920 | 16459-16459 | 0.30 | display_environment | dollar | `P(Y \le 2) = \left(\frac{2}{3}\right)^3 = \frac{8}{27}` |
| 1921 | 16460-16460 | 0.22 | display_environment | dollar | `P(Y \le 3) = 1^3 = 1` |
| 1922 | 16462-16462 | 0.30 | display_environment | dollar | `P(Y = 1) = P(Y \le 1) = \frac{1}{27}` |
| 1926 | 16483-16485 | 0.45 | inline_safe | bracket | `DX = E[(X - EX)^2] = E(X^2) - (EX)^2.` |
| 1927 | 16497-16499 | 0.36 | inline_safe | bracket | `Y=\frac1{10}\sum_{i=1}^{10}X_i,` |
| 1928 | 16507-16512 | 0.42 | normalized_width_not_low | bracket | `D(Y)=D\!\left(\frac1{10}\sum_{i=1}^{10}X_i\right) =\frac1{100}\sum_{i=1}^{10}D(X_i) =\frac1{100}\cdot10A =0.1A.` |
| 1929 | 16519-16521 | 0.14 | inline_unsafe_marker | bracket | `F(x) = \begin{cases} 0, & x < -1, \\ 0.2, & -1 \leqslant x < 0, \\ 0.8, & 0 \leqslant x < 1, \\ 1, & x \geqslant 1, \end{cases}` |
| 1930 | 16527-16529 | 0.09 | inline_unsafe_marker | bracket | `X \sim \begin{pmatrix} -1 & 0 & 1 \\ 0.2 & 0.6 & 0.2 \end{pmatrix}.` |
| 1934 | 16544-16544 | 0.12 | display_environment | dollar | `f(x) = \begin{cases} 2x, & 0 < x < 1, \\ 0, & \text{其他.} \end{cases}` |
| 1941 | 16596-16598 | 0.15 | inline_safe | bracket | `10\sqrt{\frac{1}{4}} = 5.` |
| 1942 | 16603-16605 | 0.17 | inline_unsafe_marker | bracket | `f(x) = \begin{cases} \dfrac{1}{2}\sin x, & 0 \leqslant x \leqslant \pi, \\[4pt] 0, & \text{其他}, \end{cases}` |
| 1943 | 16610-16615 | 0.37 | normalized_width_not_low | bracket | `P\!\left(X > \frac{\pi}{3}\right) = \int_{\frac{\pi}{3}}^{\pi} \frac{1}{2}\sin x\,\mathrm{d}x = \frac12\bigl[-\cos x\bigr]_{\pi/3}^{\pi} = \frac12\left(1+\frac12\right) = \frac34.` |
| 1944 | 16618-16620 | 0.20 | inline_safe | bracket | `Y\sim B\!\left(4,\frac34\right).` |
| 1947 | 16645-16647 | 0.35 | inline_safe | bracket | `D(X \pm Y) = DX + DY \pm 2\,\mathrm{Cov}(X,Y).` |
| 1953 | 16696-16698 | 0.31 | inline_safe | bracket | `g'(c) = -2EX + 2c \stackrel{\text{令}}{=} 0,` |
| 1954 | 16713-16715 | 0.27 | inline_safe | bracket | `E(X+Y)=E(X)+E(Y).` |
| 1955 | 16717-16719 | 0.48 | inline_safe | bracket | `E(XY)=E(X)E(Y),\qquad \operatorname{Cov}(X,Y)=0,` |
| 1956 | 16721-16723 | 0.25 | inline_safe | bracket | `D(X\pm Y)=D(X)+D(Y).` |
| 1958 | 16732-16732 | 0.36 | display_environment | dollar | `\boldsymbol{E(\overline{X}) = \mu}, \quad \boldsymbol{D(\overline{X}) = \frac{\sigma^2}{n}}` |
| 1961 | 16750-16752 | 0.19 | inline_safe | bracket | `E(XY)=EX\cdot EY` |
| 1962 | 16754-16756 | 0.38 | inline_safe | bracket | `\mathrm{Cov}(X,Y)=E(XY)-EX\cdot EY=0.` |
| 1963 | 16766-16768 | 0.47 | inline_safe | bracket | `D(XY)=DX\cdot DY+DX(EY)^2+DY(EX)^2,` |
| 1964 | 16772-16774 | 0.36 | inline_safe | bracket | `D(X+Y)=DX+DY+2\mathrm{Cov}(X,Y)` |
| 1965 | 16786-16788 | 0.37 | inline_safe | bracket | `D(X+Y)=DX+DY+2\mathrm{Cov}(X,Y),` |
| 1967 | 16795-16797 | 0.37 | inline_safe | bracket | `D(X-Y)=DX+DY-2\mathrm{Cov}(X,Y),` |
| 1969 | 16815-16817 | 0.37 | inline_safe | bracket | `D(X+Y)=DX+DY+2\mathrm{Cov}(X,Y).` |
| 1970 | 16820-16822 | 0.37 | inline_safe | bracket | `2\mathrm{Cov}(X,Y)=0 \implies \mathrm{Cov}(X,Y)=0.` |
| 1974 | 16864-16866 | 0.35 | inline_safe | bracket | `-x^2+2x-1=-(x-1)^2.` |
| 1975 | 16868-16872 | 0.36 | normalized_width_not_low | bracket | `f(x)=\frac1{\sqrt{\pi}}e^{-(x-1)^2} =\frac{1}{\sqrt{2\pi}\cdot(1/\sqrt2)} \exp\!\left\{-\frac{(x-1)^2}{2(1/2)}\right\}.` |
| 1976 | 16874-16876 | 0.21 | inline_safe | bracket | `X\sim N\left(1,\frac12\right),` |
| 1977 | 16878-16880 | 0.11 | inline_safe | bracket | `E(X)=1.` |
| 1981 | 16914-16916 | 0.39 | inline_safe | bracket | `F_U(u) = \frac{4u - u^2}{4} = \frac{(4-u)u}{4}.` |
| 1982 | 16918-16920 | 0.32 | inline_unsafe_marker | bracket | `f_U(u) = F_U'(u) = \begin{cases} \dfrac{2-u}{2}, & 0 < u < 2, \\[4pt] 0, & \text{其他}. \end{cases}` |
| 1983 | 16953-16953 | 0.33 | inline_safe | bracket | `EX = 1\cdot p + 0\cdot(1-p) = p.` |
| 1984 | 16954-16954 | 0.42 | inline_safe | bracket | `EX^2 = 1^2\cdot p + 0^2\cdot(1-p) = p.` |
| 1985 | 16955-16955 | 0.47 | inline_safe | bracket | `DX = EX^2 - (EX)^2 = p - p^2 = p(1-p).` |
| 1990 | 16967-16967 | 0.46 | inline_safe | bracket | `DX = EX^2 - (EX)^2 = \lambda^2 + \lambda - \lambda^2 = \lambda.` |
| 2003 | 17018-17020 | 0.38 | inline_safe | bracket | `D(\chi^2) = \sum_{i=1}^{n}D(X_i^2).` |
| 2005 | 17025-17027 | 0.15 | inline_safe | bracket | `D(\chi^2) = 2n.` |
| 2012 | 17125-17127 | 0.48 | inline_safe | bracket | `P(X_{(5)} < 3) = [P(X_1 < 3)]^5 = [\Phi(1)]^5.` |
| 2014 | 17133-17137 | 0.44 | normalized_width_not_low | bracket | `\mathrm{Cov}(X_1,\bar X) =\mathrm{Cov}\!\left(X_1,\frac15\sum_{i=1}^{5}X_i\right) =\frac15\sum_{i=1}^{5}\mathrm{Cov}(X_1,X_i).` |
| 2015 | 17140-17142 | 0.49 | inline_safe | bracket | `\mathrm{Cov}(X_1,X_i)=0\qquad (i=2,3,4,5),` |
| 2016 | 17144-17146 | 0.26 | inline_safe | bracket | `\mathrm{Cov}(X_1,X_1)=DX_1.` |
| 2017 | 17148-17150 | 0.35 | inline_safe | bracket | `\mathrm{Cov}(X_1,\bar X)=\frac15\,DX_1.` |
| 2018 | 17153-17155 | 0.29 | inline_safe | bracket | `\mathrm{Cov}(X_1,\bar X)=\frac45.` |
| 2019 | 17161-17163 | 0.19 | inline_safe | bracket | `P\!\left(\|2X-Y\|\ge1\right).` |
| 2021 | 17173-17175 | 0.25 | inline_safe | bracket | `W=\frac{Z+1}{5}\sim N(0,1).` |
| 2022 | 17177-17179 | 0.48 | inline_safe | bracket | `P(\|2X-Y\|\ge1)=P(Z\le-1)+P(Z\ge1).` |
| 2024 | 17186-17188 | 0.48 | inline_safe | bracket | `P(\|2X-Y\|\ge1)=0.5+0.3446=0.8446.` |
| 2025 | 17193-17199 | 0.08 | inline_unsafe_marker | bracket | `\begin{array}{c\|cccc} (X,Y) & (1,0) & (1,1) & (2,0) & (2,1) \\ \hline P & 0.4 & 0.2 & a & b \end{array}` |
| 2026 | 17204-17206 | 0.42 | inline_safe | bracket | `0.4+0.2+a+b=1 \implies a+b=0.4.` |
| 2027 | 17208-17210 | 0.46 | inline_safe | bracket | `E(XY)=1\cdot1\cdot0.2+2\cdot1\cdot b=0.8,` |
| 2030 | 17226-17228 | 0.20 | inline_unsafe_marker | bracket | `f(x,y) = \begin{cases} xe^{-y}, & 0 < x < y, \\ 0, & \text{其他}, \end{cases}` |
| 2033 | 17248-17255 | 0.07 | inline_unsafe_marker | bracket | `\begin{array}{c\|ccc} X \backslash Y & 0 & 1 & 2 \\ \hline -1 & 0.1 & 0.1 & b \\ 1 & a & 0.1 & 0.1 \end{array}` |
| 2034 | 17261-17264 | 0.47 | display_environment | env:align* | `P\{\max(X,Y)=2\} &= P\{Y=2\} = b + 0.1,\\ P\{\min(X,Y)=1\} &= P\{X=1,Y=1\} + P\{X=1,Y=2\} = 0.2.` |
| 2038 | 17283-17286 | 0.10 | inline_unsafe_marker | bracket | `X \sim \begin{pmatrix} 0 & 1 \\ \frac{1}{4} & \frac{3}{4} \end{pmatrix},\quad Y \sim \begin{pmatrix} 0 & 1 \\ \frac{1}{2} & \frac{1}{2} \end{pmatrix},` |
| 2040 | 17297-17301 | 0.40 | display_environment | env:align* | `P\{X=1,Y=0\} &= P\{X=1\} - P\{X=1,Y=1\} = \frac{1}{4},\\ P\{X=0,Y=1\} &= P\{Y=1\} - P\{X=1,Y=1\} = 0,\\ P\{X=0,Y=0\} &= P\{X=0\} = \frac{1}{4}.` |
| 2041 | 17303-17312 | 0.08 | inline_unsafe_marker | bracket | `\begin{array}{c\|cc\|c} X \backslash Y & 0 & 1 & P_i \\ \hline 0 & \frac{1}{4} & 0 & \frac{1}{4} \\[4pt] 1 & \frac{1}{4} & \frac{1}{2} & \frac{3}{4} \\ \hline P_j & \frac{1}{2} & ...` |
| 2042 | 17320-17322 | 0.23 | inline_safe | bracket | `\rho_{XY} = \frac{\mathrm{Cov}(X,Y)}{\sqrt{DX \cdot DY}}` |
| 2044 | 17352-17354 | 0.49 | inline_safe | bracket | `DY - 2t\,\mathrm{Cov}(X,Y) + t^2 DX \geqslant 0, \quad \forall\, t \in \mathbb{R}.` |
| 2046 | 17419-17421 | 0.38 | inline_safe | bracket | `X \sim B(n, p_1), \quad Y \sim B(n, p_2)` |
| 2048 | 17429-17439 | 0.11 | inline_unsafe_marker | bracket | `X_i = \begin{cases} 1, & \text{第 } i \text{ 次摸出红球}, \\ 0, & \text{其他}, \end{cases} \qquad Y_i = \begin{cases} 1, & \text{第 } i \text{ 次摸出白球}, \\ 0, & \text{其他}, \end{cases}` |
| 2052 | 17463-17468 | 0.44 | display_environment | env:align* | `r(X,Y) &= \frac{\text{Cov}(X,Y)}{\sqrt{D(X)} \sqrt{D(Y)}} \\[6pt] &= \frac{-n p_1 p_2}{\sqrt{np_1(1-p_1)} \sqrt{np_2(1-p_2)}} \\[6pt] &= \frac{-n p_1 p_2}{n \sqrt{p_1 p_2 (1-p_1...` |
| 2054 | 17483-17485 | 0.27 | inline_unsafe_marker | bracket | `f(x,y) = \begin{cases} 24y(1-x), & 0 \leqslant x \leqslant 1,\ 0 \leqslant y \leqslant x, \\ 0, & \text{其他}, \end{cases}` |
| 2057 | 17512-17518 | 0.27 | inline_unsafe_marker | bracket | `f(x,y)= \begin{cases} A(x+y), & 0\le x\le1,\ 0\le y\le2,\\ 0, & \text{其他}. \end{cases}` |
| 2058 | 17523-17525 | 0.30 | inline_safe | bracket | `D=\{0\le x\le1,\ y\ge x^2\}` |
| 2059 | 17530-17533 | 0.45 | normalized_width_not_low | bracket | `1=A\int_0^1\int_0^2(x+y)\,\mathrm dy\,\mathrm dx =A\int_0^1(2x+2)\,\mathrm dx=3A,` |
| 2060 | 17535-17537 | 0.14 | inline_safe | bracket | `A=\frac13.` |
| 2064 | 17555-17559 | 0.33 | normalized_width_not_low | bracket | `\operatorname{Cov}(X,Y)=E(XY)-E(X)E(Y) =\frac23-\frac59\cdot\frac{11}{9} =-\frac1{81}.` |
| 2069 | 17578-17583 | 0.28 | normalized_width_not_low | bracket | `\rho_{XY} =\frac{\operatorname{Cov}(X,Y)}{\sqrt{D(X)}\sqrt{D(Y)}} =\frac{-1/81}{\sqrt{(13/162)(23/81)}} =-\sqrt{\frac{2}{299}}.` |
| 2071 | 17596-17598 | 0.40 | inline_safe | bracket | `P\{(X,Y)\in D\}=1-\frac7{60}=\frac{53}{60}.` |
| 2072 | 17605-17612 | 0.13 | inline_unsafe_marker | bracket | `f_X(x)= \begin{cases} \dfrac12, & -1<x<0,\\[4pt] \dfrac14, & 0\le x<2,\\[4pt] 0, & \text{其他}. \end{cases}` |
| 2073 | 17620-17624 | 0.43 | normalized_width_not_low | bracket | `f_Y(y)=\frac{f_X(-\sqrt y)}{2\sqrt y}+\frac{f_X(\sqrt y)}{2\sqrt y} =\frac{1/2+1/4}{2\sqrt y} =\frac{3}{8\sqrt y}.` |
| 2074 | 17626-17629 | 0.24 | inline_safe | bracket | `f_Y(y)=\frac{f_X(\sqrt y)}{2\sqrt y} =\frac{1}{8\sqrt y}.` |
| 2075 | 17631-17638 | 0.11 | inline_unsafe_marker | bracket | `f_Y(y)= \begin{cases} \dfrac{3}{8\sqrt y}, & 0<y<1,\\[6pt] \dfrac{1}{8\sqrt y}, & 1<y<4,\\[6pt] 0, & \text{其他}. \end{cases}` |
| 2079 | 17654-17658 | 0.35 | normalized_width_not_low | bracket | `\operatorname{Cov}(X,Y)=EXY-EX\,EY =\frac78-\frac14\cdot\frac56 =\frac23.` |
| 2080 | 17661-17664 | 0.37 | normalized_width_not_low | bracket | `F\!\left(-\frac12,4\right) =P\left\{X\le-\frac12,\ X^2\le4\right\}.` |
| 2081 | 17666-17671 | 0.36 | normalized_width_not_low | bracket | `F\!\left(-\frac12,4\right) =P\left\{-1<X\le-\frac12\right\} =\int_{-1}^{-1/2}\frac12\,\mathrm dx =\frac14.` |
| 2082 | 17682-17685 | 0.24 | inline_safe | bracket | `F_\eta(y)=P(2^\xi\le y) =P\left(\xi\le\frac{\ln y}{\ln2}\right).` |
| 2083 | 17687-17692 | 0.21 | normalized_width_not_low | bracket | `f_\eta(y) =\frac{1}{2\sqrt{2\pi}\,y\ln2} \exp\left\{-\frac{(\ln y)^2}{8\ln^2 2}\right\}, \qquad y>0,` |
| 2084 | 17696-17700 | 0.29 | normalized_width_not_low | bracket | `E\eta=E e^{(\ln2)\xi} =\exp\left\{\frac12\cdot4\ln^2 2\right\} =e^{2\ln^2 2}=2^{2\ln2}.` |
| 2085 | 17703-17707 | 0.37 | normalized_width_not_low | bracket | `E\eta^2=E e^{2(\ln2)\xi} =\exp\left\{\frac12\cdot4\cdot(2\ln2)^2\right\} =e^{8\ln^2 2}.` |
| 2086 | 17709-17712 | 0.31 | normalized_width_not_low | bracket | `D\eta=e^{8\ln^2 2}-e^{4\ln^2 2} =2^{4\ln2}\left(2^{4\ln2}-1\right).` |
| 2087 | 17723-17725 | 0.27 | inline_safe | bracket | `F_\eta(y)=P\left(\xi\le\frac{\ln y}{\ln3}\right),` |
| 2088 | 17727-17732 | 0.21 | normalized_width_not_low | bracket | `f_\eta(y) =\frac{1}{2\sqrt{2\pi}\,y\ln3} \exp\left\{-\frac{(\ln y)^2}{8\ln^2 3}\right\}, \qquad y>0.` |
| 2089 | 17736-17739 | 0.27 | inline_safe | bracket | `E\eta=E e^{(\ln3)\xi} =e^{2\ln^2 3}=3^{2\ln3},` |
| 2090 | 17740-17743 | 0.22 | inline_safe | bracket | `E\eta^2=E e^{2(\ln3)\xi} =e^{8\ln^2 3}.` |
| 2091 | 17745-17748 | 0.31 | normalized_width_not_low | bracket | `D\eta=e^{8\ln^2 3}-e^{4\ln^2 3} =3^{4\ln3}\left(3^{4\ln3}-1\right).` |
| 2093 | 17795-17797 | 0.28 | inline_safe | bracket | `DY=D(aX+b)=a^2DX.` |
| 2094 | 17800-17805 | 0.21 | normalized_width_not_low | bracket | `\rho_{XY} =\frac{\mathrm{Cov}(X,Y)}{\sqrt{DX}\sqrt{DY}} =\frac{aDX}{\sqrt{DX}\sqrt{a^2DX}} =\frac{a}{\|a\|}.` |
| 2095 | 17808-17810 | 0.11 | inline_unsafe_marker | bracket | `\rho_{XY} = \begin{cases} 1, & a > 0, \\ -1, & a < 0. \end{cases}` |
| 2096 | 17819-17821 | 0.27 | inline_safe | bracket | `Y=X_1-2X_2+3X_3.` |
| 2099 | 17834-17836 | 0.35 | inline_safe | bracket | `D(Y)=3+4\cdot4+9\cdot3=46.` |
| 2100 | 17841-17843 | 0.22 | inline_safe | bracket | `D(X-3Y-4)=\text{（\quad）}.` |
| 2101 | 17851-17854 | 0.43 | normalized_width_not_low | bracket | `DX=3,\qquad DY=8\cdot\frac13\left(1-\frac13\right)=\frac{16}{9}.` |
| 2103 | 17863-17866 | 0.13 | inline_unsafe_marker | bracket | `X = \begin{cases} 1, & A \text{ 发生}, \\ 0, & A \text{ 不发生}, \end{cases}\quad Y = \begin{cases} 1, & B \text{ 发生}, \\ 0, & B \text{ 不发生}. \end{cases}` |
| 2109 | 17898-17905 | 0.09 | inline_unsafe_marker | bracket | `\begin{array}{c\|ccc} \xi\backslash \eta & -1 & 0 & 1\\ \hline 0 & \dfrac16 & \dfrac13 & \dfrac16\\[4pt] 1 & \dfrac16 & 0 & \dfrac16 \end{array}` |
| 2115 | 17934-17936 | 0.35 | inline_safe | bracket | `\operatorname{Cov}(\xi,\eta)=E(\xi\eta)-E\xi\,E\eta=0,` |
| 2116 | 17938-17940 | 0.11 | inline_safe | bracket | `\rho_{\xi\eta}=0.` |
| 2117 | 17942-17945 | 0.36 | normalized_width_not_low | bracket | `D(\xi-\eta)=D\xi+D\eta-2\operatorname{Cov}(\xi,\eta) =\frac29+\frac23=\frac89.` |
| 2118 | 17950-17961 | 0.07 | inline_unsafe_marker | bracket | `\begin{array}{c\|ccc} X & 0 & 1 & 2 \\ \hline P & \frac{1}{3} & \frac{1}{3} & \frac{1}{3} \end{array},\quad \begin{array}{c\|ccc} Y & -1 & 0 & 1 \\ \hline P & \frac{1}{3} & \frac{...` |
| 2120 | 17974-17978 | 0.30 | normalized_width_not_low | bracket | `P\{X=0,Y=0\} = \frac{1}{3},\quad P\{X=1,Y=1\} = \frac{1}{3},\quad P\{X=1,Y=-1\} = \frac{1}{3}.` |
| 2121 | 17980-17989 | 0.09 | inline_unsafe_marker | bracket | `\begin{array}{c\|ccc\|c} X \backslash Y & -1 & 0 & 1 & P_i \\ \hline 0 & 0 & \frac{1}{3} & 0 & \frac{1}{3} \\[4pt] 1 & \frac{1}{3} & 0 & \frac{1}{3} & \frac{2}{3} \\ \hline P_j & ...` |
| 2122 | 17991-17995 | 0.30 | display_environment | env:align* | `P\{Z=-1\} &= P\{X=1,Y=-1\} = \frac{1}{3},\\ P\{Z=0\} &= P\{X=0,Y=0\} = \frac{1}{3},\\ P\{Z=1\} &= P\{X=1,Y=1\} = \frac{1}{3}.` |
| 2123 | 18010-18017 | 0.10 | inline_unsafe_marker | bracket | `\begin{array}{c\|cc} X_1 \backslash X_2 & -1 & 1 \\ \hline -1 & \frac{1}{6} & \frac{1}{3} \\[4pt] 1 & \frac{1}{3} & \frac{1}{6} \end{array}` |
| 2124 | 18031-18039 | 0.41 | inline_unsafe_marker | bracket | `\begin{aligned} EY &=\int_{-\infty}^{+\infty} y\,f(-y)\,\mathrm{d}y\\ &=\int_{+\infty}^{-\infty} (-t)\,f(t)\,(-\,\mathrm{d}t)\\ &=-\int_{-\infty}^{+\infty} t\,f(t)\,\mathrm{d}t\...` |
| 2125 | 18041-18043 | 0.31 | inline_safe | bracket | `EZ=EX+EY=EX-EX=0.` |
| 2126 | 18046-18053 | 0.35 | inline_unsafe_marker | bracket | `\begin{aligned} EY^2 &=\int_{-\infty}^{+\infty} y^2 f(-y)\,\mathrm{d}y\\ &=\int_{-\infty}^{+\infty} t^2 f(t)\,\mathrm{d}t\\ &=EX^2. \end{aligned}` |
| 2129 | 18075-18077 | 0.27 | inline_unsafe_marker | bracket | `f_Z(z) = \begin{cases} \lambda^2 z\,e^{-\lambda z}, & z > 0, \\[4pt] 0, & z \leqslant 0. \end{cases}` |
| 2134 | 18131-18133 | 0.35 | inline_safe | bracket | `\int_{-\infty}^{+\infty} x^3 f(x)\,\mathrm{d}x = 0.` |
| 2136 | 18146-18149 | 0.40 | normalized_width_not_low | bracket | `EX = \int_{-\pi}^{\pi} \frac{\sin\theta}{2\pi}\,\mathrm{d}\theta = 0,\quad EY = \int_{-\pi}^{\pi} \frac{\cos\theta}{2\pi}\,\mathrm{d}\theta = 0,` |
| 2138 | 18169-18171 | 0.35 | inline_safe | bracket | `\rho_{UV} = \frac{E(UV) - EU \cdot EV}{\sqrt{DU}\sqrt{DV}} = 0.` |
| 2140 | 18197-18203 | 0.37 | inline_unsafe_marker | bracket | `f_Y(y) = \begin{cases} \displaystyle\int_y^1 \frac{1}{x}\,\mathrm{d}x = -\ln y, & 0.5 \leqslant y < 1, \\[8pt] \displaystyle\int_{0.5}^1 \frac{1}{x}\,\mathrm{d}x = \ln 2, & -0.5...` |
| 2144 | 18229-18231 | 0.41 | inline_safe | bracket | `\rho_{Z_1Z_2} = \frac{3\sigma^2}{\sqrt{5\sigma^2}\sqrt{5\sigma^2}} = \frac{3}{5}.` |
| 2146 | 18248-18251 | 0.47 | normalized_width_not_low | bracket | `E\|Z\|=\frac{2}{\sqrt{2\pi}}\int_0^{+\infty} z\,e^{-\frac{z^2}{2}}\,\mathrm{d}z =\sqrt{\frac{2}{\pi}}.` |
| 2147 | 18254-18256 | 0.15 | inline_safe | bracket | `\|Z\|^2=Z^2,` |
| 2151 | 18274-18276 | 0.27 | inline_safe | bracket | `E\max\{\xi,\eta\}=a+\frac{\sigma}{\sqrt{\pi}}.` |
| 2152 | 18280-18282 | 0.38 | inline_safe | bracket | `X=\frac{\xi-a}{\sigma},\qquad Y=\frac{\eta-a}{\sigma}.` |
| 2153 | 18284-18286 | 0.32 | inline_safe | bracket | `\max\{\xi,\eta\}=a+\sigma\max\{X,Y\}.` |
| 2154 | 18290-18292 | 0.34 | inline_safe | bracket | `\max\{X,Y\}=\frac{X+Y+\|X-Y\|}{2},` |
| 2155 | 18294-18298 | 0.42 | normalized_width_not_low | bracket | `E\max\{X,Y\} =\frac12E(X+Y)+\frac12E\|X-Y\| =\frac12E\|X-Y\|.` |
| 2156 | 18300-18302 | 0.18 | inline_safe | bracket | `X-Y\sim N(0,2),` |
| 2157 | 18304-18306 | 0.24 | inline_safe | bracket | `E\|X-Y\|=\sqrt2\,E\|Z\|.` |
| 2159 | 18313-18315 | 0.43 | inline_safe | bracket | `E\|X-Y\|=\sqrt2\sqrt{\frac2\pi}=\frac2{\sqrt{\pi}},` |
| 2160 | 18317-18319 | 0.28 | inline_safe | bracket | `E\max\{X,Y\}=\frac1{\sqrt{\pi}}.` |
| 2161 | 18321-18323 | 0.27 | inline_safe | bracket | `E\max\{\xi,\eta\}=a+\frac{\sigma}{\sqrt{\pi}}.` |
| 2166 | 18354-18356 | 0.48 | inline_safe | bracket | `\rho_{XZ} = \frac{\mathrm{Cov}(X,Z)}{\sqrt{DX}\sqrt{DZ}} = \frac{6}{\sqrt{9 \times 7}} = \frac{2\sqrt{7}}{7}.` |
| 2167 | 18369-18371 | 0.34 | inline_safe | bracket | `(X,Y)\sim N(1,3^2;\,0,4^2,\,0),` |
| 2168 | 18373-18375 | 0.11 | inline_safe | bracket | `\rho_{XY}=0.` |
| 2169 | 18377-18379 | 0.36 | inline_safe | bracket | `\mathrm{Cov}(X,Y)=\rho_{XY}\sqrt{DX}\sqrt{DY}=0.` |
| 2170 | 18382-18384 | 0.15 | inline_safe | bracket | `X\ \text{与}\ Y\ \text{相互独立}.` |
| 2171 | 18387-18389 | 0.33 | inline_safe | bracket | `E(XY) = EX \cdot EY = 1 \times 0 = 0.` |
| 2173 | 18408-18410 | 0.25 | inline_safe | bracket | `D\xi=E(\xi^2)-(E\xi)^2` |
| 2174 | 18412-18414 | 0.48 | inline_safe | bracket | `E(\xi^2)=D\xi+(E\xi)^2=2.4+6^2=38.4.` |
| 2175 | 18424-18426 | 0.23 | inline_safe | bracket | `\rho_{XY}=\frac{\operatorname{Cov}(X,Y)}{\sqrt{DX}\sqrt{DY}},` |
| 2176 | 18428-18431 | 0.31 | normalized_width_not_low | bracket | `\operatorname{Cov}(X,Y)=\rho_{XY}\sqrt{DX}\sqrt{DY} =0.4\times5\times6=12.` |
| 2178 | 18447-18449 | 0.18 | inline_safe | bracket | `P(\xi=5)=q^4.` |
| 2180 | 18469-18471 | 0.23 | inline_safe | bracket | `\rho_{XY}=\frac{\operatorname{Cov}(X,Y)}{\sqrt{DX}\sqrt{DY}},` |
| 2181 | 18473-18475 | 0.21 | inline_safe | bracket | `0.4=\frac{12}{\sqrt{DX}\cdot6}.` |
| 2182 | 18477-18479 | 0.25 | inline_safe | bracket | `\sqrt{DX}=\frac{12}{0.4\times6}=5,` |
| 2183 | 18481-18483 | 0.10 | inline_safe | bracket | `DX=25.` |
| 2184 | 18488-18490 | 0.21 | inline_safe | bracket | `E(XY)=E(X)E(Y),` |
| 2185 | 18501-18503 | 0.20 | inline_safe | bracket | `E(XY)=E(X)E(Y)` |
| 2186 | 18505-18507 | 0.39 | inline_safe | bracket | `\operatorname{Cov}(X,Y)=E(XY)-E(X)E(Y)=0.` |
| 2188 | 18517-18519 | 0.20 | inline_safe | bracket | `E(XY)=E(X)E(Y)` |
| 2189 | 18526-18528 | 0.21 | inline_safe | bracket | `E(XY)=E(X)E(Y),` |
| 2190 | 18532-18534 | 0.43 | inline_safe | bracket | `EX=0,\qquad E(XY)=E(X^3)=0,` |
| 2191 | 18536-18538 | 0.25 | inline_safe | bracket | `E(XY)=E(X)E(Y)=0.` |
| 2192 | 18553-18555 | 0.16 | inline_safe | bracket | `\operatorname{Cov}(X,Y)=0.` |
| 2193 | 18557-18563 | 0.28 | inline_unsafe_marker | bracket | `\begin{aligned} D(X+2Y) &=DX+4DY+4\operatorname{Cov}(X,Y)\\ &=DX+4DY. \end{aligned}` |
| 2196 | 18581-18583 | 0.49 | inline_safe | bracket | `EA=2-1-1=0,\qquad EB=1-1=0.` |
| 2199 | 18602-18604 | 0.33 | inline_safe | bracket | `Y=\frac1n\sum_{i=1}^n X_i.` |
| 2200 | 18615-18620 | 0.42 | normalized_width_not_low | bracket | `\operatorname{Cov}(X_1,Y) =\operatorname{Cov}\!\left(X_1,\frac1n\sum_{i=1}^nX_i\right) =\frac1n\operatorname{Cov}(X_1,X_1) =\frac{\sigma^2}{n}.` |
| 2201 | 18624-18626 | 0.13 | inline_safe | bracket | `DY=\frac{\sigma^2}{n}.` |
| 2202 | 18628-18632 | 0.44 | normalized_width_not_low | bracket | `D(X_1+Y)=DX_1+DY+2\operatorname{Cov}(X_1,Y) =\sigma^2+\frac{\sigma^2}{n}+\frac{2\sigma^2}{n} =\frac{(n+3)\sigma^2}{n},` |
| 2203 | 18633-18637 | 0.44 | normalized_width_not_low | bracket | `D(X_1-Y)=DX_1+DY-2\operatorname{Cov}(X_1,Y) =\sigma^2+\frac{\sigma^2}{n}-\frac{2\sigma^2}{n} =\frac{(n-1)\sigma^2}{n}.` |
| 2204 | 18643-18645 | 0.13 | inline_safe | bracket | `Z=3X-2.` |
| 2205 | 18650-18652 | 0.08 | inline_safe | bracket | `EX=2.` |
| 2206 | 18654-18656 | 0.49 | inline_safe | bracket | `E(Z)=E(3X-2)=3EX-2=3\times2-2=4.` |
| 2207 | 18661-18663 | 0.28 | inline_safe | bracket | `(X,Y)\sim N(0,1;\,0,4;\,\rho),` |
| 2208 | 18668-18670 | 0.33 | inline_safe | bracket | `\operatorname{Cov}(X,Y)=\rho\sqrt{DX}\sqrt{DY}=2\rho.` |
| 2209 | 18672-18679 | 0.28 | inline_unsafe_marker | bracket | `\begin{aligned} D(2X-Y) &=4DX+DY-4\operatorname{Cov}(X,Y)\\ &=4+4-4\cdot2\rho\\ &=8-8\rho. \end{aligned}` |
| 2210 | 18681-18683 | 0.13 | inline_safe | bracket | `8-8\rho=1,` |
| 2211 | 18685-18687 | 0.14 | inline_safe | bracket | `\rho=\frac78.` |
| 2212 | 18695-18697 | 0.18 | inline_safe | bracket | `X+Y\sim B(7,p).` |
| 2213 | 18700-18702 | 0.33 | inline_safe | bracket | `X+Y\sim B(3+4,p)=B(7,p).` |
| 2214 | 18707-18709 | 0.26 | inline_safe | bracket | `x^2+2Xx+5X-4=0` |
| 2215 | 18716-18718 | 0.32 | inline_safe | bracket | `\Delta=(2X)^2-4(5X-4)\ge0.` |
| 2216 | 18720-18724 | 0.23 | normalized_width_not_low | bracket | `4(X^2-5X+4)\ge0 \quad\Longleftrightarrow\quad (X-1)(X-4)\ge0.` |
| 2217 | 18726-18728 | 0.27 | inline_safe | bracket | `X\le1\quad\text{或}\quad X\ge4.` |
| 2218 | 18730-18734 | 0.35 | normalized_width_not_low | bracket | `P\{\text{方程有实根}\} =P(0<X\le1)+P(4\le X<5) =\frac15+\frac15=\frac25.` |
| 2219 | 18750-18752 | 0.22 | inline_safe | bracket | `P(\|\xi\|>t)\le \frac{c}{t^3}.` |
| 2220 | 18756-18758 | 0.14 | inline_safe | bracket | `\|\xi\|^3>t^3.` |
| 2221 | 18760-18762 | 0.28 | inline_safe | bracket | `\mathbf 1_{\{\|\xi\|>t\}}\le \frac{\|\xi\|^3}{t^3}.` |
| 2222 | 18764-18769 | 0.30 | normalized_width_not_low | bracket | `P(\|\xi\|>t)=E\mathbf 1_{\{\|\xi\|>t\}} \le E\left(\frac{\|\xi\|^3}{t^3}\right) =\frac{E\|\xi\|^3}{t^3} =\frac{c}{t^3}.` |
| 2223 | 18780-18782 | 0.47 | inline_safe | bracket | `p=\frac12\cdot0.4+\frac12\cdot0.6=0.5,` |
| 2224 | 18784-18786 | 0.35 | inline_safe | bracket | `P(N=k)=p^kq=(0.5)^{k+1}.` |
| 2225 | 18788-18791 | 0.36 | inline_safe | bracket | `EN=\sum_{k=0}^{\infty}k(0.5)^{k+1} =\frac{p}{q}=1.` |
| 2227 | 18798-18801 | 0.38 | normalized_width_not_low | bracket | `ES=\sum_{k=1}^{\infty}350(0.5)^{k-1} =350\cdot\frac1{1-0.5}=700.` |
| 2228 | 18813-18816 | 0.32 | normalized_width_not_low | bracket | `P(A_1)=0.3,\qquad P(A_2)=0.7\times0.3=0.21,` |
| 2229 | 18817-18820 | 0.48 | normalized_width_not_low | bracket | `P(A_3)=0.7^2\times0.3=0.147,\qquad P(A_4)=0.7^3\times0.3=0.1029,` |
| 2230 | 18821-18823 | 0.30 | inline_safe | bracket | `P(A_0)=0.7^4=0.2401.` |
| 2231 | 18826-18828 | 0.39 | inline_safe | bracket | `100-10k,\qquad k=1,2,3,4.` |
| 2232 | 18830-18832 | 0.24 | inline_safe | bracket | `-40-100=-140.` |
| 2234 | 18851-18853 | 0.23 | inline_safe | bracket | `D(X+Y)=D(X-Y),` |
| 2235 | 18864-18866 | 0.37 | inline_safe | bracket | `D(X+Y)=DX+DY+2\operatorname{Cov}(X,Y),` |
| 2236 | 18867-18869 | 0.37 | inline_safe | bracket | `D(X-Y)=DX+DY-2\operatorname{Cov}(X,Y).` |
| 2237 | 18871-18874 | 0.27 | normalized_width_not_low | bracket | `DX+DY+2\operatorname{Cov}(X,Y) =DX+DY-2\operatorname{Cov}(X,Y),` |
| 2238 | 18876-18878 | 0.17 | inline_safe | bracket | `4\operatorname{Cov}(X,Y)=0.` |
| 2239 | 18880-18882 | 0.16 | inline_safe | bracket | `\operatorname{Cov}(X,Y)=0,` |
| 2241 | 18892-18894 | 0.21 | inline_safe | bracket | `P\{X+Y\ge 6\}\le c?` |
| 2242 | 18898-18900 | 0.42 | inline_safe | bracket | `E(X+Y)=E(X)+E(Y)=-2+2=0.` |
| 2243 | 18902-18905 | 0.36 | normalized_width_not_low | bracket | `\operatorname{Cov}(X,Y)=\rho_{X,Y}\sqrt{D(X)}\sqrt{D(Y)} =-0.5\times 1\times 2=-1.` |
| 2244 | 18907-18910 | 0.40 | normalized_width_not_low | bracket | `D(X+Y)=D(X)+D(Y)+2\operatorname{Cov}(X,Y) =1+4+2(-1)=3.` |
| 2245 | 18913-18915 | 0.32 | inline_safe | bracket | `\{X+Y\ge 6\}\subset \{\|X+Y\|\ge 6\},` |
| 2246 | 18917-18922 | 0.36 | normalized_width_not_low | bracket | `P\{X+Y\ge 6\}\le P\{\|X+Y\|\ge 6\} \le \frac{D(X+Y)}{6^2} =\frac{3}{36} =\frac1{12}.` |
| 2247 | 18924-18926 | 0.15 | inline_safe | bracket | `c=\frac1{12}.` |
| 2248 | 18934-18940 | 0.13 | inline_unsafe_marker | bracket | `f(x)= \begin{cases} a\sin x, & 0\le x\le \pi,\\ 0, & \text{其他}. \end{cases}` |
| 2249 | 18948-18952 | 0.24 | normalized_width_not_low | bracket | `1=\int_0^\pi a\sin x\,\mathrm{d}x =a[-\cos x]_0^\pi =2a,` |
| 2250 | 18954-18956 | 0.14 | inline_safe | bracket | `a=\frac12.` |
| 2251 | 18959-18963 | 0.40 | normalized_width_not_low | bracket | `E(X)=\int_0^\pi x\cdot\frac12\sin x\,\mathrm{d}x =\frac12[-x\cos x+\sin x]_0^\pi =\frac{\pi}{2}.` |
| 2252 | 18965-18972 | 0.49 | inline_unsafe_marker | bracket | `\begin{aligned} E(X^2) &=\int_0^\pi x^2\cdot\frac12\sin x\,\mathrm{d}x\\ &=\frac12[-x^2\cos x+2x\sin x+2\cos x]_0^\pi\\ &=\frac{\pi^2-4}{2}. \end{aligned}` |
| 2253 | 18974-18978 | 0.29 | normalized_width_not_low | bracket | `D(X)=E(X^2)-[E(X)]^2 =\frac{\pi^2-4}{2}-\frac{\pi^2}{4} =\frac{\pi^2}{4}-2.` |
| 2254 | 18981-18983 | 0.22 | inline_safe | bracket | `P(A\|B)=\frac{P(A\cap B)}{P(B)}.` |
| 2255 | 18985-18989 | 0.45 | normalized_width_not_low | bracket | `P(A\cap B)=\int_{\pi/4}^{2\pi/3}\frac12\sin x\,\mathrm{d}x =\frac12\left(\cos\frac{\pi}{4}-\cos\frac{2\pi}{3}\right) =\frac{\sqrt2+1}{4},` |
| 2256 | 18990-18994 | 0.38 | normalized_width_not_low | bracket | `P(B)=\int_{\pi/4}^{\pi}\frac12\sin x\,\mathrm{d}x =\frac12\left(\cos\frac{\pi}{4}-\cos\pi\right) =\frac{2+\sqrt2}{4}.` |
| 2257 | 18996-18998 | 0.22 | inline_safe | bracket | `P(A\|B)=\frac{\sqrt2+1}{\sqrt2+2}.` |
| 2258 | 19005-19007 | 0.16 | inline_safe | bracket | `P(\|X\|>k)=0.` |
| 2259 | 19014-19016 | 0.26 | inline_safe | bracket | `\|E X\|\le E\|X\|\le k<+\infty.` |
| 2260 | 19022-19024 | 0.33 | inline_safe | bracket | `D(X)=4,\qquad D(Y)=1,` |
| 2261 | 19026-19028 | 0.13 | inline_safe | bracket | `D(3X-2Y).` |
| 2262 | 19039-19042 | 0.35 | normalized_width_not_low | bracket | `\operatorname{Cov}(X,Y)=\rho_{XY}\sqrt{D(X)}\sqrt{D(Y)} =0.6\times2\times1=1.2.` |
| 2263 | 19044-19052 | 0.49 | inline_unsafe_marker | bracket | `\begin{aligned} D(3X-2Y) &=9D(X)+4D(Y)+2\cdot3\cdot(-2)\operatorname{Cov}(X,Y)\\ &=9\times4+4\times1-12\times1.2\\ &=36+4-14.4\\ &=25.6. \end{aligned}` |
| 2264 | 19064-19066 | 0.18 | inline_safe | bracket | `X+Y\sim N(0,2).` |
| 2265 | 19068-19070 | 0.11 | inline_safe | bracket | `X+Y=0,` |
| 2267 | 19080-19082 | 0.22 | inline_safe | bracket | `Z=(2X-Y+1)^2.` |
| 2268 | 19087-19089 | 0.17 | inline_safe | bracket | `W=2X-Y+1.` |
| 2270 | 19095-19098 | 0.35 | normalized_width_not_low | bracket | `\operatorname{Cov}(X,Y)=\rho_{XY}\sqrt{D(X)}\sqrt{D(Y)} =0.6\times1\times2=1.2.` |
| 2271 | 19100-19104 | 0.32 | normalized_width_not_low | bracket | `D(W)=D(2X-Y+1) =4D(X)+D(Y)-4\operatorname{Cov}(X,Y) =4+4-4.8=3.2.` |
| 2275 | 19174-19190 | 0.41 | inline_unsafe_marker | bracket | `\begin{cases} \text{马尔可夫不等式：} \displaystyle P\{X \geqslant a\} \leqslant \frac{EX}{a}\ (X\ge 0) \\[6pt] \text{切比雪夫不等式：} \displaystyle P\left\{\|X - EX\| \geqslant \varepsilon\righ...` |
| 2276 | 19241-19245 | 0.37 | normalized_width_not_low | bracket | `\lim_{n\to\infty} P\{\|X_n - X\| \geqslant \varepsilon\} = 0 \quad \text{或等价地} \quad \lim_{n\to\infty} P\{\|X_n - X\| < \varepsilon\} = 1,` |
| 2277 | 19247-19249 | 0.22 | inline_safe | bracket | `X_n \stackrel{P}{\longrightarrow} X\ (n\to\infty).` |
| 2278 | 19255-19257 | 0.27 | inline_safe | bracket | `g(X_n, Y_n) \stackrel{P}{\longrightarrow} g(a, b).` |
| 2280 | 19291-19293 | 0.20 | inline_safe | bracket | `P\{X\ge a\}\le \frac{EX}{a}.` |
| 2281 | 19297-19302 | 0.28 | display_environment | env:align* | `EX &= \int_0^{+\infty}x\,f(x)\,\mathrm{d}x \\ &\ge \int_a^{+\infty}x\,f(x)\,\mathrm{d}x \\ &\ge a\int_a^{+\infty}f(x)\,\mathrm{d}x \\ &= a\,P\{X\ge a\}.` |
| 2282 | 19304-19306 | 0.20 | inline_safe | bracket | `P\{X\ge a\}\le \frac{EX}{a}.` |
| 2283 | 19313-19315 | 0.24 | inline_safe | bracket | `\{(X-EX)^2\ge \varepsilon^2\},` |
| 2285 | 19325-19327 | 0.23 | inline_safe | bracket | `P(X\ge 12)\le \underline{\hspace{2cm}}.` |
| 2286 | 19331-19333 | 0.33 | inline_safe | bracket | `P(X\ge 12)\le \frac{3}{12}=\frac14.` |
| 2287 | 19351-19353 | 0.30 | inline_safe | bracket | `P\{\|X - EX\| \geqslant \varepsilon\} \leqslant \frac{DX}{\varepsilon^2},` |
| 2288 | 19355-19357 | 0.33 | inline_safe | bracket | `P\{\|X - EX\| < \varepsilon\} \geqslant 1 - \frac{DX}{\varepsilon^2}.` |
| 2290 | 19381-19383 | 0.35 | inline_safe | bracket | `P(\|X-EX\|<\varepsilon)\ge 1-\frac{0.009}{\varepsilon^2}.` |
| 2292 | 19400-19402 | 0.25 | inline_safe | bracket | `S=\sum_{i=1}^9X_i.` |
| 2293 | 19404-19407 | 0.43 | normalized_width_not_low | bracket | `ES=\sum_{i=1}^9EX_i=9,\qquad DS=\sum_{i=1}^9DX_i=9.` |
| 2294 | 19409-19411 | 0.33 | inline_safe | bracket | `P\{\|S-ES\|<\varepsilon\}\ge1-\frac{DS}{\varepsilon^2},` |
| 2295 | 19413-19416 | 0.34 | normalized_width_not_low | bracket | `P\left\{\left\|\sum_{i=1}^9X_i-9\right\|<\varepsilon\right\} \ge1-\frac9{\varepsilon^2}.` |
| 2296 | 19425-19427 | 0.30 | inline_safe | bracket | `P\{\|X - EX\| \geq \varepsilon\} \leq \frac{DX}{\varepsilon^2},` |
| 2297 | 19429-19431 | 0.33 | inline_safe | bracket | `P\{\|X - EX\| < \varepsilon\} \geq 1 - \frac{DX}{\varepsilon^2}.` |
| 2298 | 19441-19443 | 0.17 | inline_safe | bracket | `P(\|X-EX\|<\varepsilon)` |
| 2300 | 19452-19454 | 0.32 | inline_safe | bracket | `P(\|X-EX\|<\varepsilon)\ge 1-\frac{DX}{\varepsilon^2},` |
| 2302 | 19471-19473 | 0.29 | inline_safe | bracket | `P(\|X-EX\|\ge \varepsilon)\le \frac{DX}{\varepsilon^2}.` |
| 2303 | 19475-19477 | 0.07 | inline_safe | bracket | `\varepsilon=2.` |
| 2304 | 19479-19481 | 0.42 | inline_safe | bracket | `P(\|X - EX\| \geq 2) \leq \frac{DX}{\varepsilon^2} = \frac{2}{4} = \frac{1}{2}.` |
| 2305 | 19491-19493 | 0.25 | inline_safe | bracket | `\rho(X,Y)=\frac{\mathrm{Cov}(X,Y)}{\sqrt{DX}\sqrt{DY}},` |
| 2306 | 19495-19498 | 0.33 | normalized_width_not_low | bracket | `\mathrm{Cov}(X,Y)=\rho(X,Y)\sqrt{DX}\sqrt{DY} =0.5\times \sqrt{1}\times \sqrt{4}=1.` |
| 2308 | 19506-19508 | 0.38 | inline_safe | bracket | `E(X+Y)=EX+EY=-2+2=0.` |
| 2309 | 19510-19512 | 0.41 | inline_safe | bracket | `P\{\|X+Y\| \geq 6\} \leq \frac{D(X+Y)}{36} = \frac{7}{36}.` |
| 2311 | 19524-19526 | 0.28 | inline_safe | bracket | `P\{X+Y\ge 6\}\le\,\underline{\hspace{2cm}}.` |
| 2312 | 19530-19532 | 0.26 | inline_safe | bracket | `E(X+Y)=EX+EY=0.` |
| 2313 | 19534-19537 | 0.33 | normalized_width_not_low | bracket | `\mathrm{Cov}(X,Y)=\rho(X,Y)\sqrt{DX}\sqrt{DY} =-0.5\cdot1\cdot2=-1,` |
| 2315 | 19543-19545 | 0.32 | inline_safe | bracket | `\{X+Y\ge6\}\subset \{\|X+Y\|\ge6\},` |
| 2316 | 19547-19552 | 0.21 | normalized_width_not_low | bracket | `P\{X+Y\ge6\} \le P\{\|X+Y\|\ge6\} \le \frac{D(X+Y)}{6^2} =\frac{1}{12}.` |
| 2317 | 19557-19559 | 0.26 | inline_unsafe_marker | bracket | `f(x) = \begin{cases} \dfrac{1}{2}\,x^2\,e^{-x}, & x > 0, \\[4pt] 0, & x \leq 0, \end{cases}` |
| 2319 | 19568-19570 | 0.38 | inline_safe | bracket | `DX = EX^2 - (EX)^2 = 12 - 9 = 3.` |
| 2320 | 19572-19574 | 0.48 | inline_safe | bracket | `P(\|X - 3\| < 2) \geq 1 - \frac{DX}{2^2} = 1 - \frac{3}{4} = \frac{1}{4}.` |
| 2321 | 19585-19587 | 0.12 | inline_unsafe_marker | bracket | `f(x) = \begin{cases} 2x, & 0 < x < 1, \\ 0, & \text{其他}, \end{cases}` |
| 2322 | 19596-19600 | 0.42 | normalized_width_not_low | bracket | `EX = \int_0^1 2x^2\,\mathrm{d}x = \frac{2}{3},\quad EX^2 = \int_0^1 2x^3\,\mathrm{d}x = \frac{1}{2},\quad DX = \frac{1}{2} - \frac{4}{9} = \frac{1}{18}.` |
| 2324 | 19618-19620 | 0.36 | inline_safe | bracket | `\overline{X}_n=\frac1n\sum_{i=1}^n X_i` |
| 2325 | 19624-19626 | 0.43 | inline_safe | bracket | `D\overline{X}_n=\frac1{n^2}\sum_{i=1}^n DX_i.` |
| 2326 | 19632-19634 | 0.31 | inline_safe | bracket | `DX_i \leq C \quad (\text{对一切 } i \geq 1),` |
| 2330 | 19655-19657 | 0.29 | inline_safe | bracket | `\frac1n\sum_{i=1}^n EX_i` |
| 2331 | 19659-19661 | 0.30 | inline_safe | bracket | `\frac{1}{n}\sum_{i=1}^{n} X_i \stackrel{P}{\longrightarrow} \mu.` |
| 2332 | 19693-19695 | 0.38 | inline_safe | bracket | `\lim_{n\to\infty} P\!\left\{\left\|\frac{\mu_n}{n} - p\right\| < \varepsilon\right\} = 1,` |
| 2333 | 19701-19703 | 0.29 | inline_safe | bracket | `\frac1n\sum_{i=1}^n p_i,` |
| 2334 | 19710-19712 | 0.20 | inline_safe | bracket | `\overline{X}_n = \frac{\mu_n}{n} \xrightarrow{P} p.` |
| 2335 | 19719-19721 | 0.43 | inline_safe | bracket | `\frac{\mu_n}{n}=\frac{1}{n}\sum_{i=1}^{n}X_i=\bar X_n,` |
| 2336 | 19725-19727 | 0.28 | inline_safe | bracket | `F_n(x) = \frac{\text{样本值中} \leq x \text{的个数}}{n}` |
| 2337 | 19738-19746 | 0.11 | inline_unsafe_marker | bracket | `F_7(x) = \begin{cases} 0, & x < 1, \\ \dfrac{3}{7}, & 1 \leq x < 2, \\[6pt] \dfrac{5}{7}, & 2 \leq x < 3, \\[6pt] \dfrac{6}{7}, & 3 \leq x < 5, \\[6pt] 1, & x \geq 5. \end{cases}` |
| 2338 | 19755-19757 | 0.30 | inline_safe | bracket | `\frac1n\sum_{i=1}^n EX_i;` |
| 2342 | 19783-19786 | 0.38 | normalized_width_not_low | bracket | `P\!\left\{\left\|\frac{1}{n}\sum_{k=1}^{n} X_k - \mu\right\| \geq \varepsilon\right\} \leq \frac{\sigma^2/n}{\varepsilon^2} \xrightarrow{n\to\infty} 0.` |
| 2343 | 19795-19797 | 0.22 | inline_safe | bracket | `\frac1n\sum h(X_i)` |
| 2344 | 19801-19803 | 0.42 | inline_safe | bracket | `\frac{1}{n}\sum_{i=1}^{n} X_i^k \stackrel{P}{\longrightarrow} E(X_1^k).` |
| 2345 | 19812-19814 | 0.17 | inline_unsafe_marker | bracket | `f(x) = \begin{cases} 1 - \|x\|, & \|x\| < 1, \\ 0, & \text{其他}, \end{cases}` |
| 2346 | 19823-19825 | 0.42 | inline_safe | bracket | `\frac{1}{n}\sum_{i=1}^{n} X_i^2 \stackrel{P}{\longrightarrow} E(X_1^2).` |
| 2348 | 19843-19845 | 0.18 | inline_safe | bracket | `X_1, X_2, \dots, X_n` |
| 2349 | 19849-19851 | 0.38 | inline_safe | bracket | `\overline{X}_n=\frac1n\sum_{i=1}^n X_i,` |
| 2351 | 19857-19859 | 0.41 | inline_safe | bracket | `EX_i = \frac{1 + 2 + 3 + 4 + 5 + 6}{6} = \frac{7}{2}.` |
| 2352 | 19862-19864 | 0.49 | inline_safe | bracket | `\overline{X}_n = \frac{1}{n}\sum_{i=1}^{n} X_i \stackrel{P}{\longrightarrow} EX_i = \frac{7}{2}.` |
| 2353 | 19879-19881 | 0.17 | inline_safe | bracket | `\overline{X}_n-\mu \stackrel{P}{\longrightarrow} 0,` |
| 2356 | 19907-19910 | 0.31 | inline_safe | bracket | `\frac{\overline{X}_n-\mu}{\sigma/\sqrt{n}} =\frac{\sum_{i=1}^n X_i-n\mu}{\sqrt{n}\,\sigma}.` |
| 2357 | 19962-19964 | 0.24 | inline_safe | bracket | `\text{独立}+\text{同分布}+\text{期望、方差存在}.` |
| 2358 | 19979-19981 | 0.20 | inline_safe | bracket | `P\{80\le X\le 100\}` |
| 2359 | 19986-19988 | 0.39 | inline_safe | bracket | `EX=np,\qquad DX=np(1-p).` |
| 2360 | 19990-19992 | 0.31 | inline_safe | bracket | `n=100,\qquad p=0.8,` |
| 2362 | 19999-20001 | 0.22 | inline_safe | bracket | `\frac{X-80}{4}\approx N(0,1).` |
| 2363 | 20003-20009 | 0.31 | normalized_width_not_low | bracket | `P(80\le X\le 100) \approx \Phi\!\left(\frac{100.5-80}{4}\right) -\Phi\!\left(\frac{79.5-80}{4}\right) =\Phi(5.125)-\Phi(-0.125).` |
| 2365 | 20016-20020 | 0.29 | normalized_width_not_low | bracket | `\Phi\!\left(\frac{100-80}{4}\right) -\Phi\!\left(\frac{80-80}{4}\right) =\Phi(5)-\Phi(0)=\frac12,` |
| 2366 | 20026-20028 | 0.43 | inline_safe | bracket | `P\!\left(\sum_{i=1}^{100} X_i < 240\right) =\,\underline{\hspace{2cm}}.` |
| 2367 | 20035-20037 | 0.45 | inline_safe | bracket | `\mu=EX_i=2,\qquad \sigma^2=DX_i=4.` |
| 2368 | 20040-20042 | 0.28 | inline_safe | bracket | `S=\sum_{i=1}^{100} X_i.` |
| 2370 | 20049-20051 | 0.23 | inline_safe | bracket | `\frac{S-200}{20}\approx N(0,1),` |
| 2372 | 20065-20067 | 0.39 | inline_safe | bracket | `p=0.0005\times0.01=5\times10^{-6}.` |
| 2373 | 20069-20071 | 0.37 | inline_safe | bracket | `Y\sim B(2\times10^5,\ 5\times10^{-6}).` |
| 2375 | 20077-20079 | 0.32 | inline_safe | bracket | `Y\approx N(1,\ 1-5\times10^{-6}).` |
| 2376 | 20081-20086 | 0.30 | normalized_width_not_low | bracket | `P(Y>3)\approx 1-\Phi\!\left(\frac{3-1}{\sqrt{1-5\times10^{-6}}}\right) \approx 1-\Phi(2) =0.0228.` |
| 2377 | 20091-20093 | 0.29 | inline_unsafe_marker | bracket | `f(x) = \begin{cases} \dfrac{1}{100}\,e^{-x/100}, & x > 0, \\[4pt] 0, & x \leq 0, \end{cases}` |
| 2382 | 20147-20149 | 0.28 | inline_safe | bracket | `S_n=\sum_{i=1}^{n} X_i.` |
| 2383 | 20151-20153 | 0.41 | inline_safe | bracket | `ES_n=\frac{n}{\lambda},\qquad DS_n=\frac{n}{\lambda^2}.` |
| 2384 | 20156-20159 | 0.31 | normalized_width_not_low | bracket | `\frac{S_n - ES_n}{\sqrt{DS_n}} = \frac{S_n - n/\lambda}{\sqrt{n}/\lambda} = \frac{\lambda S_n - n}{\sqrt{n}} \to N(0,1),` |
| 2386 | 20180-20182 | 0.34 | inline_safe | bracket | `\frac{\sum X_i - n \cdot 2}{\sqrt{n \cdot 2}} \to N(0,1).` |
| 2387 | 20184-20188 | 0.32 | normalized_width_not_low | bracket | `P\!\left(\frac{\sum X_i - 2n}{\sqrt{n}} < 2\right) = P\!\left(\frac{\sum X_i - 2n}{\sqrt{2n}} < \frac{2}{\sqrt{2}}\right) = P(Z < \sqrt{2}) = \Phi(\sqrt{2}).` |
| 2388 | 20195-20197 | 0.33 | inline_safe | bracket | `Z_n = \frac{1}{n}\sum_{i=1}^{n} X_i^2` |
| 2390 | 20206-20208 | 0.46 | inline_safe | bracket | `\frac{\sum_{i=1}^{n} X_i^2 - n\alpha_2}{\sqrt{n(\alpha_4 - \alpha_2^2)}} \to N(0,1),` |
| 2391 | 20210-20212 | 0.38 | inline_safe | bracket | `\frac{Z_n - \alpha_2}{\sqrt{(\alpha_4 - \alpha_2^2)/n}} \to N(0,1),` |
| 2392 | 20214-20216 | 0.40 | inline_safe | bracket | `\mu = \alpha_2,\quad \sigma^2 = \frac{\alpha_4 - \alpha_2^2}{n}.` |
| 2393 | 20232-20234 | 0.46 | inline_safe | bracket | `\lim_{n\to\infty} P\!\left\{\frac{Y_n - np}{\sqrt{np(1-p)}} \leq x\right\} = \Phi(x).` |
| 2395 | 20259-20261 | 0.28 | inline_safe | bracket | `P\{a-0.5 < X < b+0.5\},` |
| 2396 | 20270-20272 | 0.22 | inline_safe | bracket | `X\sim B(1000,0.03).` |
| 2400 | 20314-20316 | 0.21 | inline_safe | bracket | `X\sim B(1000,0.8).` |
| 2401 | 20318-20321 | 0.49 | normalized_width_not_low | bracket | `EX=np=1000\times0.8=800,\qquad DX=np(1-p)=1000\times0.8\times0.2=160.` |
| 2402 | 20323-20325 | 0.20 | inline_safe | bracket | `P(X\le M)\ge0.99.` |
| 2403 | 20327-20330 | 0.16 | inline_safe | bracket | `P(X\le M)\approx \Phi\left(\frac{M-800}{\sqrt{160}}\right).` |
| 2404 | 20332-20334 | 0.21 | inline_safe | bracket | `\frac{M-800}{\sqrt{160}}\ge2.33.` |
| 2405 | 20336-20338 | 0.38 | inline_safe | bracket | `M\ge800+2.33\sqrt{160}\approx829.47.` |
| 2406 | 20340-20342 | 0.09 | inline_safe | bracket | `M=830` |
| 2407 | 20351-20353 | 0.35 | inline_safe | bracket | `P\!\left(0.76 \leq \frac{X}{n} \leq 0.84\right) \geq 0.90.` |
| 2409 | 20371-20373 | 0.45 | inline_safe | bracket | `X\sim B(n,0.8),\qquad \hat p=\frac Xn.` |
| 2411 | 20379-20382 | 0.39 | normalized_width_not_low | bracket | `P(0.76\le \hat p\le0.84) =P(\|\hat p-0.8\|\le0.04)\ge0.90.` |
| 2412 | 20385-20390 | 0.25 | normalized_width_not_low | bracket | `P(\|\hat p-0.8\|<0.04) \ge1-\frac{D\hat p}{0.04^2} =1-\frac{0.16/n}{0.0016} =1-\frac{100}{n}.` |
| 2413 | 20392-20394 | 0.21 | inline_safe | bracket | `1-\frac{100}{n}\ge0.90,` |
| 2414 | 20396-20398 | 0.12 | inline_safe | bracket | `n\ge1000.` |
| 2415 | 20402-20404 | 0.26 | inline_safe | bracket | `\frac{\hat p-0.8}{\sqrt{0.16/n}}\approx N(0,1).` |
| 2416 | 20406-20411 | 0.26 | normalized_width_not_low | bracket | `P(\|\hat p-0.8\|\le0.04) \approx P\left(\|Z\|\le\frac{0.04}{\sqrt{0.16/n}}\right) =P(\|Z\|\le0.1\sqrt n).` |
| 2417 | 20413-20415 | 0.28 | inline_safe | bracket | `2\Phi(0.1\sqrt n)-1\ge0.90,` |
| 2418 | 20417-20419 | 0.22 | inline_safe | bracket | `\Phi(0.1\sqrt n)\ge0.95.` |
| 2419 | 20421-20423 | 0.20 | inline_safe | bracket | `0.1\sqrt n\ge1.645,` |
| 2420 | 20425-20427 | 0.32 | inline_safe | bracket | `n\ge(16.45)^2=270.6025.` |
| 2421 | 20429-20431 | 0.09 | inline_safe | bracket | `n=271` |
| 2422 | 20448-20450 | 0.23 | inline_safe | bracket | `X_n\sim B\!\left(n,\frac12\right).` |
| 2425 | 20462-20464 | 0.43 | inline_safe | bracket | `\lim_{n\to\infty} P\!\left\{\frac{2X_n-n}{\sqrt n}\le x\right\}=\Phi(x),` |
| 2426 | 20476-20478 | 0.18 | inline_safe | bracket | `\zeta\sim B(n,0.95).` |
| 2427 | 20480-20482 | 0.25 | inline_safe | bracket | `P(\zeta\ge 2000)\ge 0.95.` |
| 2429 | 20489-20493 | 0.26 | inline_safe | bracket | `P(\zeta\ge 2000) \approx 1-\Phi\!\left(\frac{2000-0.95n}{\sqrt{0.0475n}}\right).` |
| 2430 | 20495-20497 | 0.34 | inline_safe | bracket | `1-\Phi\!\left(\frac{2000-0.95n}{\sqrt{0.0475n}}\right)=0.95.` |
| 2431 | 20499-20501 | 0.30 | inline_safe | bracket | `\frac{2000-0.95n}{\sqrt{0.0475n}}=-1.65.` |
| 2432 | 20503-20505 | 0.11 | inline_safe | bracket | `n=2123.` |
| 2433 | 20519-20521 | 0.25 | inline_safe | bracket | `X\sim B(25000,0.001).` |
| 2435 | 20527-20529 | 0.38 | inline_safe | bracket | `25000\times240=6000000\quad(\text{元}),` |
| 2436 | 20531-20533 | 0.28 | inline_safe | bracket | `L=6000000-200000X.` |
| 2437 | 20536-20538 | 0.47 | inline_safe | bracket | `6000000-200000X<0 \quad\Longleftrightarrow\quad X>30.` |
| 2438 | 20540-20545 | 0.22 | normalized_width_not_low | bracket | `P(L<0)=P(X>30) \approx 1-\Phi\left(\frac{30-25}{5}\right) =1-\Phi(1) =0.1587.` |
| 2439 | 20548-20552 | 0.36 | normalized_width_not_low | bracket | `6000000-200000X\ge1000000 \quad\Longleftrightarrow\quad X\le25.` |
| 2440 | 20554-20558 | 0.33 | normalized_width_not_low | bracket | `P(L\ge1000000)=P(X\le25) \approx \Phi\left(\frac{25-25}{5}\right) =\Phi(0)=0.5.` |
| 2441 | 20567-20569 | 0.21 | inline_safe | bracket | `X\sim B(n,0.0006).` |
| 2442 | 20571-20573 | 0.21 | inline_safe | bracket | `L=50n-10000X.` |
| 2443 | 20575-20577 | 0.26 | inline_safe | bracket | `P(L\ge10000)\ge0.95.` |
| 2444 | 20579-20582 | 0.34 | normalized_width_not_low | bracket | `P\left(X\le \frac{50n-10000}{10000}\right) =P(X\le0.005n-1)\ge0.95.` |
| 2445 | 20585-20587 | 0.47 | inline_safe | bracket | `X\approx N\bigl(0.0006n,\ 0.0006(1-0.0006)n\bigr).` |
| 2446 | 20589-20593 | 0.31 | inline_safe | bracket | `\frac{0.005n-1-0.0006n} {\sqrt{0.0006(1-0.0006)n}} \ge z_{0.05}.` |
| 2447 | 20595-20597 | 0.33 | inline_safe | bracket | `\frac{0.0044n-1}{\sqrt{0.00059964\,n}}\ge1.645.` |
| 2448 | 20599-20601 | 0.11 | inline_safe | bracket | `n\gtrsim 413.3.` |
| 2449 | 20603-20605 | 0.09 | inline_safe | bracket | `n=414` |
| 2450 | 20618-20620 | 0.21 | inline_safe | bracket | `X\sim B(n,0.0003).` |
| 2451 | 20622-20624 | 0.21 | inline_safe | bracket | `L=20n-10000X.` |
| 2452 | 20626-20628 | 0.26 | inline_safe | bracket | `P(L\ge10000)\ge0.95,` |
| 2453 | 20630-20633 | 0.34 | normalized_width_not_low | bracket | `P\left(X\le \frac{20n-10000}{10000}\right) =P(X\le0.002n-1)\ge0.95.` |
| 2454 | 20636-20638 | 0.47 | inline_safe | bracket | `X\approx N\bigl(0.0003n,\ 0.0003(1-0.0003)n\bigr).` |
| 2455 | 20640-20644 | 0.31 | inline_safe | bracket | `\frac{0.002n-1-0.0003n} {\sqrt{0.0003(1-0.0003)n}} \ge z_{0.05}.` |
| 2456 | 20646-20648 | 0.33 | inline_safe | bracket | `\frac{0.0017n-1}{\sqrt{0.00029991\,n}}\ge1.645.` |
| 2457 | 20650-20652 | 0.12 | inline_safe | bracket | `n\gtrsim1158.7.` |
| 2458 | 20654-20656 | 0.10 | inline_safe | bracket | `n=1159` |
| 2459 | 20673-20675 | 0.24 | inline_safe | bracket | `X\sim B(9000,0.001).` |
| 2460 | 20677-20680 | 0.39 | normalized_width_not_low | bracket | `EX=9000\times0.001=9,\qquad DX=9000\times0.001\times0.999\approx9.` |
| 2462 | 20687-20691 | 0.21 | normalized_width_not_low | bracket | `P(X>22.5)\approx 1-\Phi\!\left(\frac{22.5-9}{3}\right) =1-\Phi(4.5)\approx0.` |
| 2464 | 20699-20703 | 0.24 | normalized_width_not_low | bracket | `P(X\le17.5)\approx \Phi\!\left(\frac{17.5-9}{3}\right) =\Phi(2.83)\approx0.995.` |
| 2465 | 20715-20717 | 0.26 | inline_safe | bracket | `S=\sum_{i=1}^{50}X_i.` |
| 2467 | 20723-20731 | 0.31 | inline_unsafe_marker | bracket | `\begin{aligned} P(400\le S\le500) &\approx P\left\{\frac{400-450}{3\sqrt{50}}\le Z\le \frac{500-450}{3\sqrt{50}}\right\}\\ &=2\Phi\left(\frac{\sqrt{50}}3\right)-1 \approx2\Phi(2...` |
| 2468 | 20734-20736 | 0.24 | inline_safe | bracket | `P\{10S\ge m\}\ge0.95.` |
| 2469 | 20738-20740 | 0.28 | inline_safe | bracket | `\Phi\left(\frac{450-m/10}{3\sqrt{50}}\right)=0.95,` |
| 2470 | 20742-20744 | 0.45 | inline_safe | bracket | `m=10\left(450-1.645\cdot3\sqrt{50}\right)\approx4151.` |
| 2471 | 20748-20750 | 0.24 | inline_safe | bracket | `P\{10S\le M\}\ge0.95.` |
| 2472 | 20752-20754 | 0.28 | inline_safe | bracket | `\Phi\left(\frac{M/10-450}{3\sqrt{50}}\right)=0.95,` |
| 2473 | 20756-20758 | 0.45 | inline_safe | bracket | `M=10\left(450+1.645\cdot3\sqrt{50}\right)\approx4849.` |
| 2474 | 20770-20772 | 0.26 | inline_safe | bracket | `S=\sum_{i=1}^{50}X_i.` |
| 2475 | 20774-20776 | 0.34 | inline_safe | bracket | `ES=450,\qquad DS=450.` |
| 2476 | 20778-20783 | 0.25 | normalized_width_not_low | bracket | `P(400\le S\le500) \approx2\Phi\left(\frac{50}{3\sqrt{50}}\right)-1 =2\Phi\left(\frac{\sqrt{50}}3\right)-1 \approx0.9818.` |
| 2477 | 20786-20788 | 0.24 | inline_safe | bracket | `P\{10S\ge m\}\ge0.90.` |
| 2478 | 20790-20792 | 0.28 | inline_safe | bracket | `\Phi\left(\frac{450-m/10}{3\sqrt{50}}\right)=0.90.` |
| 2479 | 20794-20796 | 0.43 | inline_safe | bracket | `m=10\left(450-1.28\cdot3\sqrt{50}\right)\approx4228.` |
| 2480 | 20800-20802 | 0.23 | inline_safe | bracket | `P\{10S\le M\}\ge0.90` |
| 2481 | 20804-20806 | 0.43 | inline_safe | bracket | `M=10\left(450+1.28\cdot3\sqrt{50}\right)\approx4772.` |
| 2483 | 20822-20824 | 0.34 | inline_safe | bracket | `ES=750,\qquad DS=750.` |
| 2484 | 20826-20830 | 0.30 | normalized_width_not_low | bracket | `P(700\le S\le800) \approx2\Phi\left(\frac{50}{\sqrt{750}}\right)-1 \approx2\Phi(1.83)-1\approx0.932.` |
| 2485 | 20833-20835 | 0.21 | inline_safe | bracket | `P\{9S\ge m\}\ge0.95` |
| 2486 | 20837-20839 | 0.40 | inline_safe | bracket | `m=9\left(750-1.645\sqrt{750}\right)\approx6345.` |
| 2487 | 20843-20845 | 0.40 | inline_safe | bracket | `M=9\left(750+1.645\sqrt{750}\right)\approx7155.` |
| 2488 | 20853-20855 | 0.33 | inline_safe | bracket | `S_{900}=\sum_{i=1}^{900}X_i.` |
| 2489 | 20860-20863 | 0.34 | normalized_width_not_low | bracket | `EX_i=\frac{1+5}{2}=3,\qquad DX_i=\frac{(5-1)^2}{12}=\frac43.` |
| 2490 | 20865-20868 | 0.42 | normalized_width_not_low | bracket | `ES_{900}=900\cdot3=2700,\qquad DS_{900}=900\cdot\frac43=1200.` |
| 2491 | 20870-20872 | 0.30 | inline_safe | bracket | `\frac{S_{900}-2700}{\sqrt{1200}}\approx N(0,1).` |
| 2492 | 20874-20882 | 0.24 | inline_unsafe_marker | bracket | `\begin{aligned} P\{S_{900}>2632\} &\approx P\left\{Z>\frac{2632-2700}{\sqrt{1200}}\right\}\\ &=P\left\{Z>-\frac{68}{20\sqrt3}\right\} =P\left\{Z>-\frac{17\sqrt3}{15}\right\}. \e...` |
| 2493 | 20884-20886 | 0.44 | inline_safe | bracket | `P\{S_{900}>2632\}\approx \Phi(1.96)\approx0.975.` |
| 2494 | 20894-20901 | 0.29 | inline_unsafe_marker | bracket | `X_i= \begin{cases} 1, & \text{第 }i\text{ 个患者用药有效},\\ 0, & \text{否则}, \end{cases} \qquad i=1,2,\dots,100,` |
| 2495 | 20903-20905 | 0.33 | inline_safe | bracket | `S_{100}=\sum_{i=1}^{100}X_i.` |
| 2496 | 20907-20910 | 0.42 | normalized_width_not_low | bracket | `ES_{100}=100\times0.8=80,\qquad DS_{100}=100\times0.8\times0.2=16.` |
| 2497 | 20912-20914 | 0.27 | inline_safe | bracket | `\frac{S_{100}-80}{4}\approx N(0,1).` |
| 2498 | 20916-20922 | 0.37 | inline_unsafe_marker | bracket | `\begin{aligned} P\{S_{100}\ge76\} &\approx P\left\{Z\ge\frac{76-80}{4}\right\}\\ &=P\{Z\ge -1\}=\Phi(1)=0.8413. \end{aligned}` |
| 2500 | 20935-20937 | 0.29 | inline_safe | bracket | `S=\sum_{k=1}^{1000}X_k.` |
| 2501 | 20939-20942 | 0.40 | normalized_width_not_low | bracket | `ES=1000\cdot10=10000,\qquad DS=1000\cdot\frac{100}{3}=\frac{100000}{3}.` |
| 2502 | 20944-20946 | 0.29 | inline_safe | bracket | `\frac{S-10000}{\sqrt{100000/3}}\approx N(0,1).` |
| 2503 | 20948-20951 | 0.29 | inline_safe | bracket | `P\{S\le L\}\approx \Phi\!\left(\frac{L-10000}{\sqrt{100000/3}}\right)=0.99.` |
| 2504 | 20953-20955 | 0.27 | inline_safe | bracket | `\frac{L-10000}{\sqrt{100000/3}}\approx2.33.` |
| 2505 | 20957-20959 | 0.46 | inline_safe | bracket | `L\approx10000+2.33\sqrt{\frac{100000}{3}}\approx10425.` |
| 2506 | 20965-20967 | 0.29 | inline_safe | bracket | `P\{\|\overline X-\mu\|<1\}\ge0.95,` |
| 2507 | 20972-20976 | 0.14 | inline_safe | bracket | `\frac{\overline X-\mu}{\sigma/\sqrt n} =\frac{\overline X-\mu}{20/\sqrt n} \approx N(0,1).` |
| 2508 | 20978-20982 | 0.19 | inline_safe | bracket | `P\{\|\overline X-\mu\|<1\} \approx 2\Phi\!\left(\frac{\sqrt n}{20}\right)-1.` |
| 2509 | 20984-20986 | 0.29 | inline_safe | bracket | `\frac{\sqrt n}{20}\ge z_{0.025}=1.96.` |
| 2510 | 20988-20990 | 0.36 | inline_safe | bracket | `n\ge (20\times1.96)^2=1536.64.` |
| 2511 | 20992-20994 | 0.11 | inline_safe | bracket | `n=1537.` |
| 2512 | 21002-21004 | 0.36 | inline_safe | bracket | `P(B_k)=0.84\times0.90=0.756.` |
| 2513 | 21006-21013 | 0.32 | inline_unsafe_marker | bracket | `X_k= \begin{cases} 1, & B_k\text{ 发生},\\ 0, & B_k\text{ 不发生}, \end{cases} \qquad k=1,2,\dots,10000,` |
| 2514 | 21015-21017 | 0.30 | inline_safe | bracket | `X=\sum_{k=1}^{10000}X_k.` |
| 2515 | 21019-21021 | 0.25 | inline_safe | bracket | `X\sim B(10000,0.756),` |
| 2517 | 21027-21029 | 0.27 | inline_safe | bracket | `\frac{X-7560}{\sqrt{1844.64}}\approx N(0,1).` |
| 2518 | 21031-21040 | 0.26 | inline_unsafe_marker | bracket | `\begin{aligned} P\{X\ge7500\} &\approx P\left\{Z\ge\frac{7500-7560}{\sqrt{1844.64}}\right\}\\ &=1-\Phi(-1.40) =\Phi(1.40) =0.92. \end{aligned}` |
| 2519 | 21051-21053 | 0.20 | inline_safe | bracket | `P(X>96)=0.023` |
| 2520 | 21055-21057 | 0.39 | inline_safe | bracket | `\frac{96-72}{\sigma}\approx2,\qquad \frac{12}{\sigma}\approx1.` |
| 2521 | 21059-21063 | 0.47 | normalized_width_not_low | bracket | `p=P(60<X\le84) =\Phi\!\left(\frac{12}{\sigma}\right)-\Phi\!\left(-\frac{12}{\sigma}\right) \approx2\Phi(1)-1=2\times0.8413-1=0.6826.` |
| 2522 | 21065-21067 | 0.24 | inline_safe | bracket | `Y\sim B(100,0.6826),` |
| 2524 | 21074-21077 | 0.48 | normalized_width_not_low | bracket | `EY=100\times0.6826=68.26,\qquad DY=100\times0.6826\times0.3174\approx21.6657.` |
| 2528 | 21096-21098 | 0.35 | inline_safe | bracket | `DX_i=21.35-4.6^2=0.19.` |
| 2529 | 21100-21102 | 0.28 | inline_safe | bracket | `S=\sum_{i=1}^{200}X_i.` |
| 2531 | 21108-21110 | 0.23 | inline_safe | bracket | `\frac{S-920}{\sqrt{38}}\approx N(0,1).` |
| 2532 | 21112-21120 | 0.34 | inline_unsafe_marker | bracket | `\begin{aligned} P(910\le S\le930) &\approx P\left(-\frac{10}{\sqrt{38}}\le Z\le \frac{10}{\sqrt{38}}\right)\\ &=2\Phi(1.622)-1 =2\times0.9474-1 =0.8948. \end{aligned}` |
| 2534 | 21131-21138 | 0.29 | inline_unsafe_marker | bracket | `X_i= \begin{cases} 1, & \text{第 }i\text{ 粒为良种},\\ 0, & \text{第 }i\text{ 粒不是良种}, \end{cases} \qquad i=1,2,\dots,180.` |
| 2536 | 21144-21146 | 0.42 | inline_safe | bracket | `\hat p=\frac1{180}\sum_{i=1}^{180}X_i.` |
| 2537 | 21148-21150 | 0.26 | inline_safe | bracket | `\frac{\hat p-p}{\sqrt{pq/180}}\approx N(0,1).` |
| 2538 | 21152-21156 | 0.21 | inline_safe | bracket | `\sqrt{\frac{pq}{180}} =\sqrt{\frac{(1/6)(5/6)}{180}} =\frac1{36},` |
| 2539 | 21158-21161 | 0.26 | inline_safe | bracket | `P\left\{\left\|\hat p-\frac16\right\|<C\right\} \approx 2\Phi(36C)-1.` |
| 2540 | 21163-21165 | 0.23 | inline_safe | bracket | `2\Phi(36C)-1=0.99,` |
| 2541 | 21167-21169 | 0.19 | inline_safe | bracket | `\Phi(36C)=0.995.` |
| 2543 | 21182-21184 | 0.17 | inline_safe | bracket | `\|X-100\|\ge3.` |
| 2544 | 21186-21190 | 0.30 | normalized_width_not_low | bracket | `p=P\{\|X-100\|\ge3\} =2\left[1-\Phi\left(\frac3{\sqrt{2.34}}\right)\right] \approx2(1-\Phi(1.96))=0.05.` |
| 2545 | 21192-21194 | 0.17 | inline_safe | bracket | `Y\sim B(100,p).` |
| 2546 | 21196-21201 | 0.32 | normalized_width_not_low | bracket | `P(Y\ge3) \approx1-e^{-5}\left(1+5+\frac{5^2}{2!}\right) =1-\frac{37}{2}e^{-5} \approx0.8753.` |
| 2547 | 21209-21213 | 0.30 | normalized_width_not_low | bracket | `p=P\{\|X-100\|\ge3\} =2\left[1-\Phi\left(\frac3{\sqrt{2.25}}\right)\right] =2(1-\Phi(2)).` |
| 2548 | 21215-21217 | 0.24 | inline_safe | bracket | `Y\sim B(100,0.0456).` |
| 2549 | 21219-21224 | 0.43 | normalized_width_not_low | bracket | `P(Y\ge5) \approx1-e^{-4.56}\left(1+4.56+\frac{4.56^2}{2!} +\frac{4.56^3}{3!}+\frac{4.56^4}{4!}\right) \approx0.479.` |
| 2550 | 21234-21236 | 0.19 | inline_safe | bracket | `X\sim B(100,0.9).` |
| 2552 | 21242-21248 | 0.44 | inline_unsafe_marker | bracket | `\begin{aligned} P(X\ge85) &\approx 1-\Phi\!\left(\frac{85-90}{\sqrt9}\right)\\ &=1-\Phi(-1.67)=\Phi(1.67)\approx0.9525. \end{aligned}` |
| 2553 | 21257-21259 | 0.29 | inline_safe | bracket | `X\sim B(5000000,0.0003).` |
| 2554 | 21261-21263 | 0.37 | inline_safe | bracket | `EX=5000000\times0.0003=1500,` |
| 2557 | 21272-21274 | 0.28 | inline_safe | bracket | `P\{X\le10M-2\}\ge0.99.` |
| 2558 | 21276-21278 | 0.29 | inline_safe | bracket | `\frac{10M-2-1500}{\sqrt{1500}}\ge2.33.` |
| 2559 | 21280-21282 | 0.43 | inline_safe | bracket | `M\ge \frac{1502+2.33\sqrt{1500}}{10}\approx159.23.` |
| 2560 | 21284-21286 | 0.10 | inline_safe | bracket | `M=160.` |
| 2561 | 21291-21298 | 0.25 | inline_unsafe_marker | bracket | `\xi_n\sim \begin{pmatrix} -\sqrt n & 0 & \sqrt n\\ \dfrac1n & 1-\dfrac2n & \dfrac1n \end{pmatrix}, \qquad n=2,3,4,\dots` |
| 2565 | 21316-21318 | 0.42 | inline_safe | bracket | `\overline{\xi}_n=\frac1n\sum_{k=2}^{n+1}\xi_k.` |
| 2567 | 21325-21329 | 0.18 | inline_safe | bracket | `P\{\|\overline{\xi}_n\| \ge \varepsilon\} \le \frac{D\overline{\xi}_n}{\varepsilon^2} =\frac{2}{n\varepsilon^2}\to0.` |
| 2568 | 21331-21333 | 0.34 | inline_safe | bracket | `\lim_{n\to\infty}P\{\|\overline{\xi}_n\|<\varepsilon\}=1,` |
| 2570 | 21348-21350 | 0.37 | inline_safe | bracket | `EX_i=\frac{0.005+0.035}{2}=0.02,` |
| 2571 | 21351-21353 | 0.48 | inline_safe | bracket | `DX_i=\frac{(0.035-0.005)^2}{12}=0.000075.` |
| 2572 | 21355-21357 | 0.45 | inline_safe | bracket | `\overline X=\frac1{2000}\sum_{i=1}^{2000}X_i.` |
| 2573 | 21359-21361 | 0.33 | inline_safe | bracket | `\overline X\approx N\left(0.02,\frac{0.000075}{2000}\right).` |
| 2574 | 21363-21369 | 0.30 | inline_unsafe_marker | bracket | `\begin{aligned} P(\overline X<0.025) &\approx \Phi\!\left(\frac{0.025-0.02}{\sqrt{0.000075/2000}}\right)\\ &=\Phi(25.82)\approx1. \end{aligned}` |
| 2575 | 21375-21381 | 0.46 | inline_unsafe_marker | bracket | `f(x)= \begin{cases} \dfrac1{20000}e^{-\frac1{20000}(x-365)},&x\ge365,\\[6pt] 0,&x<365. \end{cases}` |
| 2576 | 21389-21395 | 0.36 | inline_unsafe_marker | bracket | `F(x)= \begin{cases} 0,&x<365,\\[4pt] 1-e^{-\frac1{20000}(x-365)},&x\ge365. \end{cases}` |
| 2578 | 21403-21405 | 0.22 | inline_safe | bracket | `N\sim B(1000,0.04).` |
| 2580 | 21412-21414 | 0.42 | inline_safe | bracket | `2000N\ge100000,\qquad\text{即 }N\ge50.` |
| 2581 | 21416-21425 | 0.30 | inline_unsafe_marker | bracket | `\begin{aligned} P(\text{亏本}) &\approx P(N\ge50)\\ &=P\left(\frac{N-40}{6.2}\ge\frac{50-40}{6.2}\right)\\ &\approx1-\Phi(1.61) =1-0.946 =0.054. \end{aligned}` |
| 2582 | 21428-21430 | 0.21 | inline_safe | bracket | `1000P_0-2000N.` |
| 2583 | 21432-21434 | 0.37 | inline_safe | bracket | `P(1000P_0-2000N<0)\le0.01,` |
| 2584 | 21436-21438 | 0.25 | inline_safe | bracket | `P\left(N\ge\frac{P_0}{2}\right)\le0.01.` |
| 2585 | 21440-21442 | 0.25 | inline_safe | bracket | `\frac{P_0/2-40}{6.2}\ge2.33.` |
| 2586 | 21444-21446 | 0.44 | inline_safe | bracket | `P_0\ge2(40+6.2\times2.33)=108.892.` |
| 2587 | 21448-21450 | 0.20 | inline_safe | bracket | `P_0\approx108.9\text{ 元/件},` |
| 2589 | 21465-21467 | 0.30 | inline_safe | bracket | `\frac{m/n-p}{\sqrt{p(1-p)/n}}\approx N(0,1).` |
| 2590 | 21469-21471 | 0.34 | inline_safe | bracket | `P\left(\left\|\frac mn-p\right\|<0.1\right)>0.95.` |
| 2591 | 21473-21475 | 0.35 | inline_safe | bracket | `2\Phi\left(\frac{0.1}{\sqrt{p(1-p)/n}}\right)-1>0.95.` |
| 2592 | 21477-21479 | 0.27 | inline_safe | bracket | `\frac{0.1}{\sqrt{p(1-p)/n}}\ge1.96.` |
| 2593 | 21481-21483 | 0.26 | inline_safe | bracket | `n\ge (19.6)^2p(1-p).` |
| 2594 | 21485-21487 | 0.23 | inline_safe | bracket | `p(1-p)\le\frac14,` |
| 2595 | 21489-21491 | 0.39 | inline_safe | bracket | `n\ge (19.6)^2\cdot\frac14=96.04.` |
| 2596 | 21493-21495 | 0.08 | inline_safe | bracket | `n=97.` |
| 2597 | 21505-21507 | 0.19 | inline_safe | bracket | `\xi_1,\xi_2,\dots,\xi_n,` |
| 2599 | 21513-21515 | 0.28 | inline_safe | bracket | `S_n=\sum_{i=1}^n \xi_i,` |
| 2600 | 21517-21519 | 0.41 | inline_safe | bracket | `ES_n=0,\qquad DS_n=\frac n3.` |
| 2601 | 21521-21523 | 0.22 | inline_safe | bracket | `\frac{S_n}{\sqrt{n/3}}\approx N(0,1).` |
| 2602 | 21525-21527 | 0.27 | inline_safe | bracket | `P(\|S_n\|\le10)\ge0.99.` |
| 2603 | 21529-21533 | 0.29 | normalized_width_not_low | bracket | `P\left(\left\|\frac{S_n}{\sqrt{n/3}}\right\|\le \frac{10}{\sqrt{n/3}}\right) \approx 2\Phi\left(\frac{10}{\sqrt{n/3}}\right)-1\ge0.99.` |
| 2604 | 21535-21537 | 0.25 | inline_safe | bracket | `\Phi\left(\frac{10}{\sqrt{n/3}}\right)\ge0.995.` |
| 2605 | 21539-21541 | 0.19 | inline_safe | bracket | `\frac{10}{\sqrt{n/3}}\ge2.58.` |
| 2606 | 21543-21545 | 0.31 | inline_safe | bracket | `n\le 3\left(\frac{10}{2.58}\right)^2\approx45.06.` |
| 2607 | 21547-21549 | 0.07 | inline_safe | bracket | `n=45` |
| 2609 | 21559-21568 | 0.32 | normalized_width_not_low | bracket | `\lim_{n\to\infty} P\left( \left\| \frac1n\sum_{i=1}^n \xi_i - \frac1n\sum_{i=1}^n E(\xi_i) \right\|<\varepsilon \right)=1.` |
| 2610 | 21572-21574 | 0.28 | inline_safe | bracket | `S_n=\sum_{i=1}^n \xi_i.` |
| 2611 | 21576-21578 | 0.46 | inline_safe | bracket | `E\left(\frac{S_n}{n}\right)=\frac1n\sum_{i=1}^n E(\xi_i),` |
| 2612 | 21580-21584 | 0.38 | normalized_width_not_low | bracket | `D\left(\frac{S_n}{n}\right) =\frac1{n^2}D(S_n) =\frac1{n^2}D\!\left(\sum_{i=1}^n \xi_i\right).` |
| 2613 | 21586-21601 | 0.35 | inline_unsafe_marker | bracket | `\begin{aligned} P\left( \left\| \frac{S_n}{n} - E\left(\frac{S_n}{n}\right) \right\|\ge\varepsilon \right) &\le \frac{D(S_n/n)}{\varepsilon^2}\\ &= \frac1{\varepsilon^2} \frac1{n^...` |
| 2614 | 21603-21612 | 0.32 | normalized_width_not_low | bracket | `\lim_{n\to\infty} P\left( \left\| \frac1n\sum_{i=1}^n \xi_i - \frac1n\sum_{i=1}^n E(\xi_i) \right\|\ge\varepsilon \right)=0.` |
| 2615 | 21614-21623 | 0.32 | normalized_width_not_low | bracket | `\lim_{n\to\infty} P\left( \left\| \frac1n\sum_{i=1}^n \xi_i - \frac1n\sum_{i=1}^n E(\xi_i) \right\|<\varepsilon \right)=1.` |
| 2616 | 21633-21635 | 0.42 | inline_safe | bracket | `X_i\sim P(1),\qquad i=1,2,\dots,52,` |
| 2617 | 21637-21639 | 0.26 | inline_safe | bracket | `S=\sum_{i=1}^{52}X_i.` |
| 2618 | 21641-21643 | 0.31 | inline_safe | bracket | `ES=52,\qquad DS=52.` |
| 2619 | 21645-21647 | 0.22 | inline_safe | bracket | `\frac{S-52}{\sqrt{52}}\approx N(0,1).` |
| 2620 | 21649-21660 | 0.29 | inline_unsafe_marker | bracket | `\begin{aligned} P(50\le S\le70) &\approx \Phi\left(\frac{70-52}{\sqrt{52}}\right) - \Phi\left(\frac{50-52}{\sqrt{52}}\right)\\ &= \Phi(2.50)-\Phi(-0.28)\\ &=\Phi(2.50)+\Phi(0.28...` |
| 2622 | 21672-21679 | 0.48 | inline_unsafe_marker | bracket | `\begin{aligned} P\{5 \leq X \leq 10\} &= P\!\left\{\frac{5 - 5}{\sqrt{4.75}} \leq \frac{X - 5}{\sqrt{4.75}} \leq \frac{10 - 5}{\sqrt{4.75}}\right\} \\ &= P\!\left\{0 \leq \frac{...` |
| 2623 | 21695-21697 | 0.23 | inline_safe | bracket | `X_i\sim B\!\left(1,\frac12\right),` |
| 2624 | 21701-21703 | 0.28 | inline_safe | bracket | `S=\sum_{i=1}^{100} X_i.` |
| 2627 | 21725-21727 | 0.49 | inline_safe | bracket | `n\ln 0.99 > \ln 0.9 \implies n < \frac{\ln 0.9}{\ln 0.99} \approx 10.48,` |
| 2634 | 21780-21782 | 0.42 | inline_safe | bracket | `E(T_2) = \frac{10000}{4} \times 2.3756 = 5939.` |
| 2636 | 21929-21931 | 0.48 | inline_safe | bracket | `F(x_1, x_2, \dots, x_n) = \prod_{i=1}^{n} F(x_i).` |
| 2637 | 21971-21973 | 0.31 | inline_safe | bracket | `\sum_{i=1}^{n}\left(\frac{X_i-\mu}{\sigma}\right)^2` |
| 2639 | 22059-22061 | 0.46 | inline_safe | bracket | `S^2=\frac{1}{n-1}\sum_{i=1}^{n}(X_i-\overline{X})^2,` |
| 2644 | 22104-22107 | 0.49 | normalized_width_not_low | bracket | `\overline{x} =\frac{17\times5+18\times15+19\times22+20\times8}{50}.` |
| 2645 | 22109-22112 | 0.43 | normalized_width_not_low | bracket | `17\times5+18\times15+19\times22+20\times8 =85+270+418+160=933.` |
| 2646 | 22114-22116 | 0.23 | inline_safe | bracket | `\overline{x}=\frac{933}{50}=18.66.` |
| 2647 | 22128-22132 | 0.40 | normalized_width_not_low | bracket | `Y_i=X_i-\overline{X} =X_i-\frac{1}{n}\sum_{k=1}^{n}X_k =\left(1-\frac{1}{n}\right)X_i-\frac{1}{n}\sum_{k\ne i}X_k.` |
| 2648 | 22135-22139 | 0.24 | normalized_width_not_low | bracket | `DY_i =\left(1-\frac{1}{n}\right)^2 DX_i \frac{1}{n^2}\sum_{k\ne i}DX_k.` |
| 2649 | 22141-22146 | 0.32 | normalized_width_not_low | bracket | `DY_i=\left(1-\frac{1}{n}\right)^2+\frac{n-1}{n^2} =1-\frac{2}{n}+\frac{1}{n^2}+\frac{n-1}{n^2} =1-\frac{1}{n} =\frac{n-1}{n}.` |
| 2652 | 22168-22170 | 0.21 | inline_safe | bracket | `E(Y_1+Y_n)=0.` |
| 2653 | 22172-22174 | 0.33 | inline_safe | bracket | `P\{Y_1+Y_n\le0\}=\frac12.` |
| 2654 | 22179-22182 | 0.32 | normalized_width_not_low | bracket | `Y=\left(\sum_{i=1}^{3}X_i\right)^2+ \left(\sum_{i=4}^{6}X_i\right)^2.` |
| 2656 | 22193-22195 | 0.39 | inline_safe | bracket | `U\sim N(0,3),\qquad V\sim N(0,3),` |
| 2657 | 22197-22199 | 0.49 | inline_safe | bracket | `\frac{U}{\sqrt3}\sim N(0,1),\qquad \frac{V}{\sqrt3}\sim N(0,1),` |
| 2658 | 22201-22206 | 0.17 | normalized_width_not_low | bracket | `\frac13Y =\left(\frac{U}{\sqrt3}\right)^2+ \left(\frac{V}{\sqrt3}\right)^2 \sim\chi^2(2).` |
| 2659 | 22212-22214 | 0.46 | inline_safe | bracket | `Y_i=X_i-\overline X,\qquad i=1,2,\cdots,n.` |
| 2662 | 22234-22237 | 0.36 | normalized_width_not_low | bracket | `\operatorname{Cov}(Y_1,Y_n) =\operatorname{Cov}(X_1-\overline X,\ X_n-\overline X).` |
| 2663 | 22239-22244 | 0.46 | normalized_width_not_low | bracket | `\operatorname{Cov}(X_1,X_n)=0,\qquad \operatorname{Cov}(X_1,\overline X)=\operatorname{Cov}(X_n,\overline X)=\frac{\sigma^2}{n}, \qquad D\overline X=\frac{\sigma^2}{n},` |
| 2664 | 22246-22250 | 0.32 | normalized_width_not_low | bracket | `\operatorname{Cov}(Y_1,Y_n) =0-\frac{\sigma^2}{n}-\frac{\sigma^2}{n}+\frac{\sigma^2}{n} =-\frac{\sigma^2}{n}.` |
| 2665 | 22253-22256 | 0.21 | inline_safe | bracket | `E\!\left[c(Y_1+Y_n)^2\right] =cD(Y_1+Y_n).` |
| 2666 | 22258-22263 | 0.39 | normalized_width_not_low | bracket | `D(Y_1+Y_n) =DY_1+DY_n+2\operatorname{Cov}(Y_1,Y_n) =\left(\frac{n-1}{n}+\frac{n-1}{n}-\frac2n\right)\sigma^2 =\frac{2(n-2)}{n}\sigma^2.` |
| 2667 | 22265-22269 | 0.24 | normalized_width_not_low | bracket | `c\cdot\frac{2(n-2)}{n}=1, \qquad\text{即}\qquad c=\frac{n}{2(n-2)}.` |
| 2668 | 22272-22274 | 0.45 | inline_safe | bracket | `D\hat\theta_1=V_1,\qquad D\hat\theta_2=V_2.` |
| 2670 | 22280-22285 | 0.26 | normalized_width_not_low | bracket | `D\hat\theta_3 =\left(\frac{V_2}{V_1+V_2}\right)^2V_1 +\left(\frac{V_1}{V_1+V_2}\right)^2V_2 =\frac{V_1V_2}{V_1+V_2},` |
| 2672 | 22335-22337 | 0.40 | inline_safe | bracket | `\chi^2 = X_1^2 + X_2^2 + \cdots + X_n^2,` |
| 2674 | 22363-22365 | 0.44 | inline_safe | bracket | `\sum_{i=1}^{10}(Y_i-\overline{Y})^2\sim \chi^2(9).` |
| 2676 | 22375-22377 | 0.10 | inline_safe | bracket | `EZ=18.` |
| 2680 | 22403-22405 | 0.23 | inline_safe | bracket | `\text{即}\quad \frac{Y}{8}\sim \chi^2(2),` |
| 2681 | 22411-22413 | 0.49 | inline_safe | bracket | `X = a(X_1 - 2X_2)^2 + b(3X_3 - 4X_4)^2,` |
| 2686 | 22440-22442 | 0.47 | inline_safe | bracket | `X = a(X_1 - 2X_2)^2 + b(3X_3 - 4X_4)^2` |
| 2687 | 22450-22452 | 0.46 | inline_safe | bracket | `Z=\frac1{\sigma^2}\sum_{i=1}^6(\xi_i-\mu)^2,` |
| 2688 | 22471-22473 | 0.23 | inline_safe | bracket | `\frac{\xi_i-\mu}{\sigma}\sim N(0,1),` |
| 2689 | 22475-22477 | 0.48 | inline_safe | bracket | `Z=\sum_{i=1}^6\left(\frac{\xi_i-\mu}{\sigma}\right)^2\sim\chi^2(6).` |
| 2691 | 22483-22487 | 0.46 | normalized_width_not_low | bracket | `f_Z(z)=\frac{1}{2^3\Gamma(3)}z^2e^{-z/2} =\frac{1}{8\cdot2}z^2e^{-z/2} =\frac1{16}z^2e^{-z/2},\qquad z>0.` |
| 2692 | 22496-22498 | 0.15 | inline_safe | bracket | `t = \frac{X}{\sqrt{Y/n}},` |
| 2693 | 22523-22525 | 0.26 | inline_safe | bracket | `Y=\frac{X_1-X_2}{\sqrt{X_3^2+X_4^2}}` |
| 2696 | 22544-22546 | 0.27 | inline_safe | bracket | `\frac{X_{n+1} - \overline{X}}{S}\sqrt{\frac{n}{n+1}}` |
| 2699 | 22572-22574 | 0.17 | inline_safe | bracket | `X^2 \sim F(1,n).` |
| 2700 | 22576-22578 | 0.31 | inline_safe | bracket | `P\{Y > c^2\} = P\{X^2 > c^2\}.` |
| 2701 | 22579-22581 | 0.29 | inline_safe | bracket | `\text{而 } X^2>c^2 \Longleftrightarrow X>c \text{ 或 } X<-c.` |
| 2702 | 22583-22585 | 0.18 | inline_safe | bracket | `P\{X<-c\}=\alpha.` |
| 2704 | 22599-22601 | 0.15 | inline_safe | bracket | `F = \frac{X/n_1}{Y/n_2},` |
| 2705 | 22620-22622 | 0.39 | inline_safe | bracket | `\sum_{i=2}^{n}X_i^2\sim\chi^2(n-1),` |
| 2706 | 22624-22628 | 0.36 | normalized_width_not_low | bracket | `\frac{X_1^2/1}{\left(\sum_{i=2}^{n}X_i^2\right)/(n-1)} =\frac{(n-1)X_1^2}{\sum_{i=2}^{n}X_i^2} \sim F(1,n-1).` |
| 2707 | 22642-22644 | 0.24 | inline_safe | bracket | `\frac{(n-1)X_1^2}{\displaystyle\sum_{i=2}^{n}X_i^2}` |
| 2708 | 22649-22651 | 0.20 | inline_safe | bracket | `X_1^2\sim\chi^2(1).` |
| 2709 | 22653-22655 | 0.39 | inline_safe | bracket | `\sum_{i=2}^{n}X_i^2\sim\chi^2(n-1),` |
| 2710 | 22657-22661 | 0.39 | normalized_width_not_low | bracket | `\frac{(n-1)X_1^2}{\sum_{i=2}^{n}X_i^2} =\frac{X_1^2/1}{\left(\sum_{i=2}^{n}X_i^2\right)/(n-1)} \sim F(1,n-1).` |
| 2711 | 22673-22677 | 0.40 | normalized_width_not_low | bracket | `X_1^2 \sim \chi^2(1), \qquad X_2^2+X_3^2+X_4^2 \sim \chi^2(3),` |
| 2712 | 22681-22683 | 0.37 | inline_safe | bracket | `\frac{\chi^2(n_1)/n_1}{\chi^2(n_2)/n_2}\sim F(n_1,n_2).` |
| 2714 | 22690-22692 | 0.07 | inline_safe | bracket | `c=3.` |
| 2715 | 22702-22704 | 0.15 | inline_safe | bracket | `T = \frac{U}{\sqrt{V/n}},` |
| 2716 | 22708-22710 | 0.29 | inline_safe | bracket | `T^2 = \frac{U^2/1}{V/n} \sim F(1,n),` |
| 2717 | 22714-22716 | 0.18 | inline_safe | bracket | `T^2 \sim F(1,15).` |
| 2718 | 22727-22729 | 0.15 | inline_safe | bracket | `X = \frac{U}{\sqrt{V/n}},` |
| 2719 | 22733-22735 | 0.29 | inline_safe | bracket | `X^2 = \frac{U^2/1}{V/n} \sim F(1,n).` |
| 2720 | 22737-22739 | 0.35 | inline_safe | bracket | `Y = \frac{1}{X^2} = \frac{V/n}{U^2/1} \sim F(n, 1).` |
| 2721 | 22740-22742 | 0.07 | inline_safe | bracket | `\text{故应选 } C.` |
| 2724 | 22763-22765 | 0.39 | inline_safe | bracket | `\frac{S_1^2/S_2^2}{\sigma_1^2/\sigma_2^2}\sim F(m{-}1,n{-}1).` |
| 2725 | 22823-22827 | 0.39 | normalized_width_not_low | bracket | `\frac{(n-1)S^2}{\sigma^2} =\frac{1}{\sigma^2}\sum_{i=1}^{n}(X_i-\overline{X})^2 \sim \chi^2(n-1).` |
| 2727 | 22848-22852 | 0.49 | normalized_width_not_low | bracket | `EX^2=\int_{-\infty}^{+\infty}x^2\cdot\frac{1}{2}e^{-\|x\|}\,\mathrm{d}x =2\int_0^{+\infty}x^2\cdot\frac{1}{2}e^{-x}\,\mathrm{d}x =\int_0^{+\infty}x^2\,e^{-x}\,\mathrm{d}x=\Gamma(3...` |
| 2729 | 22863-22865 | 0.30 | inline_safe | bracket | `E(\overline X),\qquad D(\overline X).` |
| 2730 | 22869-22871 | 0.40 | inline_safe | bracket | `E(X_i)=n,\qquad D(X_i)=2n.` |
| 2731 | 22873-22875 | 0.24 | inline_safe | bracket | `E(\overline X)=E(X_1)=n,` |
| 2732 | 22877-22880 | 0.21 | inline_safe | bracket | `D(\overline X)=\frac{D(X_1)}{n} =\frac{2n}{n}=2.` |
| 2733 | 22882-22884 | 0.38 | inline_safe | bracket | `E(\overline X)=n,\qquad D(\overline X)=2.` |
| 2734 | 22897-22901 | 0.43 | normalized_width_not_low | bracket | `\overline{X}\sim N\!\left(\mu,\frac{\sigma^2}{n}\right),\qquad \frac{(n-1)S^2}{\sigma^2}\sim\chi^2(n-1),\qquad \frac{\sqrt{n}(\overline{X}-\mu)}{S}\sim t(n-1).` |
| 2735 | 22905-22907 | 0.32 | inline_safe | bracket | `E(2X_2-X_1)=2\mu-\mu=\mu,` |
| 2737 | 22914-22916 | 0.30 | inline_safe | bracket | `\frac{\sqrt{n}(\overline{X}-\mu)}{S}\sim t(n-1),` |
| 2738 | 22918-22920 | 0.33 | inline_safe | bracket | `\frac{n(\overline{X}-\mu)^2}{S^2}\sim F(1,n-1),` |
| 2739 | 22924-22926 | 0.31 | inline_safe | bracket | `\frac{(n-1)S^2}{\sigma^2}\sim\chi^2(n-1),` |
| 2740 | 22930-22932 | 0.30 | inline_safe | bracket | `\frac{\sqrt{n}(\overline{X}-\mu)}{S}\sim t(n-1),` |
| 2741 | 22942-22944 | 0.44 | inline_safe | bracket | `E\!\left(\sum_{i=1}^{n}(X_i-\overline{X})^2\right)=\underline{\hspace{2cm}}.` |
| 2742 | 22952-22954 | 0.34 | inline_safe | bracket | `E\!\left(\sum_{i=1}^{n}(X_i-\overline{X})^2\right),` |
| 2744 | 22961-22963 | 0.46 | inline_safe | bracket | `E\!\left[\frac{1}{4}\sum_{i=1}^{n}(X_i-\overline{X})^2\right]=n-1.` |
| 2745 | 22965-22967 | 0.47 | inline_safe | bracket | `E\!\left(\sum_{i=1}^{n}(X_i-\overline{X})^2\right)=4(n-1).` |
| 2746 | 22974-22976 | 0.46 | inline_safe | bracket | `Y = \frac{X_1 + X_2 + X_3 + X_4}{\sqrt{X_5^2 + X_6^2 + X_7^2 + X_8^2}}` |
| 2747 | 22985-22987 | 0.09 | inline_safe | bracket | `\frac{U}{\sqrt{V/\nu}}` |
| 2754 | 23034-23036 | 0.18 | inline_safe | bracket | `\overline{X}\sim N\!\left(0,\frac{4}{10}\right).` |
| 2755 | 23038-23040 | 0.24 | inline_safe | bracket | `\frac{\sqrt{10}\,\overline{X}}{2}\sim N(0,1),` |
| 2756 | 23042-23044 | 0.23 | inline_safe | bracket | `\frac{10\overline{X}^2}{4}\sim\chi^2(1).` |
| 2757 | 23047-23049 | 0.38 | inline_safe | bracket | `\frac{(n-1)S^2}{\sigma^2}=\frac{9S^2}{4}\sim\chi^2(9),` |
| 2759 | 23058-23060 | 0.08 | inline_safe | bracket | `c=10.` |
| 2760 | 23070-23072 | 0.39 | inline_safe | bracket | `X_1-X_2\sim N(0,4+4)=N(0,8),` |
| 2761 | 23074-23076 | 0.26 | inline_safe | bracket | `\frac{X_1-X_2}{\sqrt{8}}\sim N(0,1).` |
| 2762 | 23079-23083 | 0.31 | normalized_width_not_low | bracket | `\sum_{i=3}^{8}X_i^2 =4\sum_{i=3}^{8}\left(\frac{X_i}{2}\right)^2 \sim 4\chi^2(6).` |
| 2764 | 23091-23093 | 0.32 | inline_safe | bracket | `c=\sqrt{3},\qquad Y\sim t(6).` |
| 2765 | 23096-23098 | 0.34 | inline_safe | bracket | `\overline{X}\sim N\!\left(0,\frac{4}{8}\right)=N\!\left(0,\frac12\right),` |
| 2766 | 23100-23102 | 0.20 | inline_safe | bracket | `\sqrt{2}\,\overline{X}\sim N(0,1).` |
| 2768 | 23112-23114 | 0.20 | inline_safe | bracket | `\overline{X}\sim N\!\left(1,\frac{\sigma^2}{6}\right).` |
| 2770 | 23124-23126 | 0.21 | inline_safe | bracket | `\frac{5S^2}{\sigma^2}\sim\chi^2(5),` |
| 2774 | 23166-23168 | 0.27 | inline_safe | bracket | `\overline{X}-\overline{Y}\sim N\!\left(0,\frac{2\sigma^2}{n}\right).` |
| 2775 | 23170-23174 | 0.28 | normalized_width_not_low | bracket | `P\{\|\overline{X}-\overline{Y}\|>\sigma\} = P\!\left\{\left\|\frac{\overline{X}-\overline{Y}}{\sigma\sqrt{2/n}}\right\|>\sqrt{\frac{n}{2}}\right\} = 2\!\left[1-\Phi\!\left(\sqrt{\fr...` |
| 2777 | 23188-23191 | 0.36 | normalized_width_not_low | bracket | `\overline X\sim N\!\left(0,\frac4{10}\right),\qquad \overline Y\sim N\!\left(0,\frac9{15}\right).` |
| 2780 | 23202-23204 | 0.31 | inline_safe | bracket | `E\|\overline X-\overline Y\|=\sqrt{\frac2\pi}.` |
| 2781 | 23210-23212 | 0.42 | inline_safe | bracket | `Y = \frac{2X_1^2 + X_2^2 + \cdots + X_{10}^2}{X_{11}^2 + X_{12}^2 + \cdots + X_{15}^2}` |
| 2782 | 23219-23221 | 0.46 | inline_safe | bracket | `\chi_1^2 = \frac{2X_1^2+X_2^2+\cdots+X_{10}^2}{9}` |
| 2784 | 23227-23230 | 0.43 | normalized_width_not_low | bracket | `U = \dfrac{2X_1^2+\cdots+X_{10}^2}{9},\qquad V = \dfrac{X_{11}^2+\cdots+X_{15}^2}{9}.` |
| 2785 | 23242-23245 | 0.43 | inline_safe | bracket | `Y=\frac{X_1^2+X_2^2+\cdots+X_{10}^2} {2\left(X_{11}^2+X_{12}^2+\cdots+X_{15}^2\right)}` |
| 2786 | 23250-23253 | 0.45 | normalized_width_not_low | bracket | `U=\sum_{i=1}^{10}\left(\frac{X_i}{2}\right)^2,\qquad V=\sum_{i=11}^{15}\left(\frac{X_i}{2}\right)^2.` |
| 2787 | 23255-23259 | 0.14 | inline_safe | bracket | `Y=\frac{4U}{2\cdot4V} =\frac{U}{2V} =\frac{U/10}{V/5}.` |
| 2788 | 23261-23263 | 0.15 | inline_safe | bracket | `Y\sim F(10,5).` |
| 2789 | 23268-23270 | 0.14 | inline_safe | bracket | `\frac{2Y_1}{Y_2+Y_3}` |
| 2790 | 23275-23277 | 0.26 | inline_safe | bracket | `Y_2+Y_3\sim\chi^2(2n).` |
| 2791 | 23279-23282 | 0.26 | inline_safe | bracket | `\frac{2Y_1}{Y_2+Y_3} =\frac{Y_1/n}{(Y_2+Y_3)/(2n)}.` |
| 2792 | 23284-23286 | 0.27 | inline_safe | bracket | `\frac{2Y_1}{Y_2+Y_3}\sim F(n,2n).` |
| 2793 | 23302-23304 | 0.23 | inline_safe | bracket | `\frac{X_i-1}{2}\sim N(0,1).` |
| 2794 | 23306-23310 | 0.37 | normalized_width_not_low | bracket | `\frac14\sum_{i=1}^n(X_i-1)^2 =\sum_{i=1}^n\left(\frac{X_i-1}{2}\right)^2 \sim\chi^2(n),` |
| 2795 | 23314-23316 | 0.24 | inline_safe | bracket | `\overline X\sim N\left(1,\frac4n\right),` |
| 2796 | 23318-23320 | 0.23 | inline_safe | bracket | `\frac{\overline X-1}{2/\sqrt n}\sim N(0,1),` |
| 2797 | 23335-23337 | 0.49 | inline_safe | bracket | `\frac{X_i-\mu}{\sigma}\sim N(0,1),\qquad i=1,2,\dots,n,` |
| 2798 | 23339-23343 | 0.40 | normalized_width_not_low | bracket | `\frac1{\sigma^2}\sum_{i=1}^{n}(X_i-\mu)^2 =\sum_{i=1}^{n}\left(\frac{X_i-\mu}{\sigma}\right)^2 \sim\chi^2(n).` |
| 2799 | 23347-23349 | 0.22 | inline_safe | bracket | `\overline X\sim N\left(\mu,\frac{\sigma^2}{n}\right).` |
| 2801 | 23355-23357 | 0.31 | inline_safe | bracket | `\frac{\sqrt n(\overline X-\mu)}{S}\sim t(n-1),` |
| 2802 | 23363-23365 | 0.09 | inline_safe | bracket | `Y=X^2` |
| 2803 | 23370-23372 | 0.15 | inline_safe | bracket | `X=\frac{U}{\sqrt{V/m}},` |
| 2804 | 23374-23376 | 0.18 | inline_safe | bracket | `X^2=\frac{U^2/1}{V/m}.` |
| 2805 | 23378-23380 | 0.21 | inline_safe | bracket | `Y=X^2\sim F(1,m).` |
| 2806 | 23386-23388 | 0.17 | inline_safe | bracket | `P(X>z_\alpha)=\alpha.` |
| 2807 | 23390-23392 | 0.16 | inline_safe | bracket | `P(\|X\|<c)=\alpha,` |
| 2808 | 23397-23399 | 0.15 | inline_safe | bracket | `P(\|X\|<c)=\alpha` |
| 2809 | 23401-23403 | 0.09 | inline_safe | bracket | `\frac{1-\alpha}{2}.` |
| 2810 | 23405-23407 | 0.21 | inline_safe | bracket | `P(X>c)=\frac{1-\alpha}{2}.` |
| 2811 | 23409-23411 | 0.16 | inline_safe | bracket | `c=z_{\frac{1-\alpha}{2}}.` |
| 2812 | 23425-23429 | 0.38 | normalized_width_not_low | bracket | `\sum_{i=1}^n (X_i-\overline X)^2 =\frac{1}{1}\sum_{i=1}^n (X_i-\overline X)^2 \sim\chi^2(n-1).` |
| 2813 | 23432-23434 | 0.41 | inline_safe | bracket | `\sum_{i=1}^n (X_i-\mu)^2\sim\chi^2(n),` |
| 2814 | 23436-23438 | 0.25 | inline_safe | bracket | `\frac{\overline X-\mu}{S/\sqrt n}\sim t(n-1),` |
| 2815 | 23444-23446 | 0.31 | inline_safe | bracket | `\xi=\frac{(X_2+X_3+X_4)^2}{3X_1^2}.` |
| 2816 | 23451-23453 | 0.32 | inline_safe | bracket | `X_2+X_3+X_4\sim N(0,27).` |
| 2817 | 23455-23457 | 0.33 | inline_safe | bracket | `\frac{X_2+X_3+X_4}{3\sqrt3}\sim N(0,1),` |
| 2818 | 23459-23461 | 0.39 | inline_safe | bracket | `\frac{(X_2+X_3+X_4)^2}{27}\sim\chi^2(1).` |
| 2819 | 23463-23465 | 0.22 | inline_safe | bracket | `\frac{X_1^2}{9}\sim\chi^2(1).` |
| 2820 | 23467-23472 | 0.31 | normalized_width_not_low | bracket | `\xi =\frac{(X_2+X_3+X_4)^2}{3X_1^2} =\frac{\dfrac{(X_2+X_3+X_4)^2}{27}}{\dfrac{X_1^2}{9}} \sim F(1,1).` |
| 2821 | 23514-23516 | 0.27 | inline_safe | bracket | `P(\|X\|>x_\alpha)=（\quad）。` |
| 2822 | 23524-23526 | 0.17 | inline_safe | bracket | `P(X>x_\alpha)=\alpha.` |
| 2823 | 23528-23530 | 0.20 | inline_safe | bracket | `P(X<-x_\alpha)=\alpha.` |
| 2825 | 23539-23541 | 0.28 | inline_safe | bracket | `P(\|X\|\le x_\alpha)=（\quad）。` |
| 2826 | 23548-23550 | 0.18 | inline_safe | bracket | `P(X\le x_\alpha)=\alpha.` |
| 2827 | 23552-23554 | 0.39 | inline_safe | bracket | `P(X<-x_\alpha)=P(X>x_\alpha)=1-\alpha.` |
| 2828 | 23556-23561 | 0.27 | normalized_width_not_low | bracket | `P(\|X\|\le x_\alpha) =P(-x_\alpha\le X\le x_\alpha) =1-2(1-\alpha) =2\alpha-1.` |
| 2829 | 23573-23575 | 0.38 | inline_safe | bracket | `\frac{(n-1)S^2}{\sigma^2}=\frac{9S^2}{16}\sim\chi^2(9).` |
| 2830 | 23577-23579 | 0.21 | inline_safe | bracket | `P(S^2 \geq a)=0.1,` |
| 2831 | 23581-23583 | 0.30 | inline_safe | bracket | `P\!\left(\frac{9}{16}S^2 \geq \frac{9}{16}a\right)=0.1.` |
| 2833 | 23600-23602 | 0.40 | inline_safe | bracket | `P(X\le x)=1-0.95-0.02=0.03.` |
| 2835 | 23630-23632 | 0.17 | inline_safe | bracket | `n\overline{X}\sim N(0,n),` |
| 2836 | 23636-23638 | 0.35 | inline_safe | bracket | `\sum_{i=1}^n X_i^2\sim \chi^2(n),` |
| 2837 | 23642-23644 | 0.23 | inline_safe | bracket | `\frac{\overline{X}-\mu}{S/\sqrt{n}}\sim t(n-1).` |
| 2838 | 23660-23662 | 0.35 | inline_safe | bracket | `\sum_{i=1}^{n}X_i^2 \sim \chi^2(n),` |
| 2839 | 23666-23668 | 0.43 | inline_safe | bracket | `\sum_{i=1}^{n-1}X_i^2 \sim \chi^2(n-1).` |
| 2843 | 23698-23700 | 0.39 | inline_safe | bracket | `X_1-X_2\sim N(0,1+1)=N(0,2).` |
| 2844 | 23702-23704 | 0.26 | inline_safe | bracket | `\frac{X_1-X_2}{\sqrt2}\sim N(0,1).` |
| 2847 | 23715-23717 | 0.26 | inline_safe | bracket | `\frac{X_1-X_2}{\sqrt2}\sim N(0,1).` |
| 2848 | 23719-23721 | 0.22 | inline_safe | bracket | `\sum_{i=3}^{n}X_i^2` |
| 2849 | 23723-23725 | 0.39 | inline_safe | bracket | `\sum_{i=3}^{n}X_i^2\sim\chi^2(n-2).` |
| 2851 | 23731-23734 | 0.45 | normalized_width_not_low | bracket | `\frac{(X_1-X_2)/\sqrt2}{\sqrt{\sum_{i=3}^{n}X_i^2/(n-2)}} =\sqrt{\frac{n-2}{2}}\cdot\frac{X_1-X_2}{\sqrt{\sum_{i=3}^{n}X_i^2}}.` |
| 2858 | 23893-23899 | 0.16 | inline_unsafe_marker | bracket | `f(x)= \begin{cases} \dfrac{6x}{\theta^3}(\theta-x), & 0<x<\theta,\\ 0, & \text{其他}, \end{cases}` |
| 2864 | 23957-23963 | 0.13 | inline_unsafe_marker | bracket | `f(x)= \begin{cases} \dfrac{2x}{\alpha^2}, & 0\leq x\leq\alpha,\\ 0, & \text{其他}, \end{cases}` |
| 2867 | 23978-23980 | 0.32 | inline_safe | bracket | `\hat{\alpha}=\max\{X_1,X_2,\dots,X_n\}.` |
| 2868 | 23982-23984 | 0.42 | inline_safe | bracket | `\hat{p}=\frac{1}{\hat{\alpha}}=\frac{1}{\max\{X_1,X_2,\dots,X_n\}}.` |
| 2869 | 24002-24004 | 0.35 | inline_safe | bracket | `L(\theta)=\frac{1}{\theta^n}\cdot\mathbf{1}\{\theta\geq X_{(n)}\}.` |
| 2871 | 24027-24030 | 0.36 | normalized_width_not_low | bracket | `L(N)=\prod_{i=1}^n P\{X=x_i\} =\left(\frac1N\right)^n,` |
| 2872 | 24032-24034 | 0.35 | inline_safe | bracket | `N\ge \max\{x_1,\dots,x_n\}=x_{(n)}.` |
| 2873 | 24036-24038 | 0.36 | inline_safe | bracket | `\widehat N=X_{(n)}=\max\{X_1,\dots,X_n\}.` |
| 2875 | 24045-24047 | 0.11 | inline_safe | bracket | `\widehat N=239.` |
| 2877 | 24060-24062 | 0.34 | inline_safe | bracket | `L(\theta)=\left(\frac{1-\theta}{2}\right)^{\!3}\left(\frac{1+\theta}{4}\right)^{\!5}.` |
| 2879 | 24068-24072 | 0.42 | normalized_width_not_low | bracket | `\frac{\mathrm{d}}{\mathrm{d}\theta}\ln L(\theta)=-\frac{3}{1-\theta}+\frac{5}{1+\theta}=0 \implies -3(1+\theta)+5(1-\theta)=0 \implies \theta=\frac{1}{4}.` |
| 2880 | 24077-24083 | 0.13 | inline_unsafe_marker | bracket | `f(x)= \begin{cases} (1+\theta)x^\theta, & 0<x<1,\\ 0, & \text{其他}, \end{cases}` |
| 2886 | 24111-24113 | 0.17 | inline_safe | bracket | `E(X)=\frac{\theta+1}{\theta+2},` |
| 2887 | 24115-24119 | 0.39 | normalized_width_not_low | bracket | `\overline L=\frac1n\sum_{i=1}^n\ln X_i, \qquad \hat\theta_{\text{MLE}}=-1-\frac1{\overline L}.` |
| 2888 | 24121-24126 | 0.41 | normalized_width_not_low | bracket | `\widehat{E(X)}_{\text{MLE}} =\frac{\hat\theta_{\text{MLE}}+1}{\hat\theta_{\text{MLE}}+2} =\frac{1}{1-\overline L} =\frac{1}{1-\frac1n\sum_{i=1}^n\ln X_i}.` |
| 2890 | 24149-24151 | 0.08 | inline_safe | bracket | `\hat{\lambda}=1.` |
| 2892 | 24168-24170 | 0.35 | inline_safe | bracket | `\hat{\sigma}^2 = \frac{1}{n}\sum_{i=1}^{n}X_i^2.` |
| 2893 | 24177-24179 | 0.42 | inline_safe | bracket | `P(X=x; \theta)=h(x)c(\theta)\exp\{w(\theta)t(x)\},` |
| 2896 | 24188-24188 | 0.48 | display_environment | dollar | `-\frac{c'(\theta)}{c(\theta)w'(\theta)} = \frac{1}{n}\sum_{i=1}^n X_i = \overline{X}` |
| 2898 | 24190-24190 | 0.11 | display_environment | dollar | `E(X)=\overline{X}` |
| 2902 | 24220-24222 | 0.43 | inline_safe | bracket | `EX = 2\theta(1-\theta) + 2(1-\theta)^2 = 2-2\theta.` |
| 2910 | 24287-24289 | 0.25 | inline_safe | bracket | `\hat{\theta}_{\text{MLE}} = \frac{7-\sqrt{13}}{12}.` |
| 2911 | 24307-24309 | 0.46 | inline_safe | bracket | `EX = \theta^2 + \theta(1-\theta) + 3(1-\theta) = 3-2\theta.` |
| 2916 | 24336-24338 | 0.43 | inline_safe | bracket | `\ell'(p)=\frac{n}{p}-\frac{\sum_{i=1}^n x_i-n}{1-p}.` |
| 2917 | 24340-24342 | 0.41 | inline_safe | bracket | `n(1-p)=p\left(\sum_{i=1}^n x_i-n\right),` |
| 2918 | 24344-24346 | 0.26 | inline_safe | bracket | `n=p\sum_{i=1}^n x_i.` |
| 2919 | 24348-24350 | 0.39 | inline_safe | bracket | `\hat p=\frac{n}{\sum_{i=1}^n x_i}=\frac{1}{\overline X}.` |
| 2921 | 24356-24358 | 0.23 | inline_safe | bracket | `\boxed{\hat p=\dfrac1{\overline X}}.` |
| 2926 | 24390-24392 | 0.20 | inline_unsafe_marker | bracket | `f(x;\theta) = \begin{cases} \dfrac{1}{1-\theta}, & \theta \leq x \leq 1, \\[4pt] 0, & \text{其他}, \end{cases}` |
| 2928 | 24404-24406 | 0.37 | inline_safe | bracket | `\hat{\theta}_{\text{MLE}} = \min\{X_1, X_2, \dots, X_n\}.` |
| 2929 | 24411-24417 | 0.16 | inline_unsafe_marker | bracket | `f(x;\theta)= \begin{cases} \dfrac1{\|\theta\|}, & \theta<x<\theta+\|\theta\|,\\[6pt] 0, & \text{其他}. \end{cases}` |
| 2930 | 24424-24427 | 0.43 | normalized_width_not_low | bracket | `X_{(1)}=\min_{1\le i\le n}X_i,\qquad X_{(n)}=\max_{1\le i\le n}X_i.` |
| 2931 | 24430-24432 | 0.10 | inline_safe | bracket | `\theta<x<0.` |
| 2932 | 24434-24437 | 0.46 | normalized_width_not_low | bracket | `L(\theta)=\left(-\frac1\theta\right)^n \mathbf{1}\{\theta<X_{(1)},\ X_{(n)}<0\},\qquad \theta<0.` |
| 2933 | 24439-24441 | 0.37 | inline_safe | bracket | `\hat\theta=X_{(1)}=\min\{X_1,\dots,X_n\}.` |
| 2934 | 24444-24446 | 0.11 | inline_safe | bracket | `\theta<x<2\theta.` |
| 2935 | 24448-24450 | 0.35 | inline_safe | bracket | `\theta<X_{(1)},\qquad X_{(n)}<2\theta,` |
| 2936 | 24452-24454 | 0.27 | inline_safe | bracket | `\frac{X_{(n)}}2<\theta<X_{(1)}.` |
| 2937 | 24456-24459 | 0.31 | inline_safe | bracket | `L(\theta)=\theta^{-n} \mathbf{1}\left\{\frac{X_{(n)}}2<\theta<X_{(1)}\right\}.` |
| 2939 | 24468-24474 | 0.07 | inline_unsafe_marker | bracket | `\begin{array}{c\|ccc} X & -1 & 0 & 3\\ \hline P & \theta & 3\theta & 1-4\theta \end{array}` |
| 2941 | 24486-24488 | 0.22 | inline_safe | bracket | `\hat\theta_1=\frac{3-\overline X}{13}.` |
| 2942 | 24491-24494 | 0.41 | normalized_width_not_low | bracket | `L(\theta)=\theta^{r_1}(3\theta)^{r_2}(1-4\theta)^{r_3} =3^{r_2}\theta^{r_1+r_2}(1-4\theta)^{r_3}.` |
| 2944 | 24500-24502 | 0.41 | inline_safe | bracket | `\ell'(\theta)=\frac{r_1+r_2}{\theta}-\frac{4r_3}{1-4\theta}=0.` |
| 2945 | 24504-24507 | 0.24 | inline_safe | bracket | `\hat\theta_2=\frac{r_1+r_2}{4n} =\frac{1-r_3/n}{4}.` |
| 2946 | 24511-24514 | 0.26 | inline_safe | bracket | `E\hat\theta_1=\frac{3-E\overline X}{13} =\frac{3-(3-13\theta)}{13}=\theta,` |
| 2947 | 24518-24520 | 0.21 | inline_safe | bracket | `E\left(\frac{r_3}{n}\right)=1-4\theta.` |
| 2948 | 24522-24526 | 0.29 | normalized_width_not_low | bracket | `E\hat\theta_2 =E\left(\frac{1-r_3/n}{4}\right) =\frac{1-(1-4\theta)}4=\theta.` |
| 2949 | 24532-24538 | 0.07 | inline_unsafe_marker | bracket | `\begin{array}{c\|ccc} X & -1 & 1 & 2\\ \hline P & \theta & 2\theta & 1-3\theta \end{array}` |
| 2950 | 24546-24548 | 0.49 | inline_safe | bracket | `EX=(-1)\theta+1\cdot2\theta+2(1-3\theta)=2-5\theta.` |
| 2951 | 24550-24552 | 0.22 | inline_safe | bracket | `\hat\theta_1=\frac{2-\overline X}{5}.` |
| 2952 | 24555-24558 | 0.41 | normalized_width_not_low | bracket | `L(\theta)=\theta^{r_1}(2\theta)^{r_2}(1-3\theta)^{r_3} =2^{r_2}\theta^{r_1+r_2}(1-3\theta)^{r_3}.` |
| 2954 | 24564-24566 | 0.41 | inline_safe | bracket | `\ell'(\theta)=\frac{r_1+r_2}{\theta}-\frac{3r_3}{1-3\theta}=0.` |
| 2955 | 24568-24570 | 0.33 | inline_safe | bracket | `\hat\theta_2=\frac13\left(1-\frac{r_3}{n}\right).` |
| 2956 | 24574-24577 | 0.24 | inline_safe | bracket | `E\hat\theta_1=\frac{2-E\overline X}{5} =\frac{2-(2-5\theta)}{5}=\theta,` |
| 2957 | 24581-24583 | 0.21 | inline_safe | bracket | `E\left(\frac{r_3}{n}\right)=1-3\theta.` |
| 2958 | 24585-24589 | 0.33 | normalized_width_not_low | bracket | `E\hat\theta_2 =\frac13\left(1-E\frac{r_3}{n}\right) =\frac13\{1-(1-3\theta)\}=\theta.` |
| 2959 | 24595-24601 | 0.18 | inline_unsafe_marker | bracket | `f(x;\theta)= \begin{cases} 2e^{-2(x-\theta)}, & x>\theta,\\ 0, & x\le\theta, \end{cases}` |
| 2960 | 24609-24611 | 0.30 | inline_safe | bracket | `EX=\theta+EY=\theta+\frac12.` |
| 2961 | 24613-24615 | 0.24 | inline_safe | bracket | `\hat\theta=\overline X-\frac12.` |
| 2962 | 24618-24622 | 0.29 | normalized_width_not_low | bracket | `E\hat\theta=E\overline X-\frac12 =\left(\theta+\frac12\right)-\frac12 =\theta,` |
| 2963 | 24628-24634 | 0.14 | inline_unsafe_marker | bracket | `f(x;\theta)= \begin{cases} 2\theta e^{-2\theta x}, & x>0,\\ 0, & x\le0, \end{cases}` |
| 2964 | 24642-24645 | 0.42 | normalized_width_not_low | bracket | `L(\theta)=\prod_{i=1}^n 2\theta e^{-2\theta X_i} =(2\theta)^n\exp\left(-2\theta\sum_{i=1}^n X_i\right).` |
| 2965 | 24647-24649 | 0.44 | inline_safe | bracket | `\ell(\theta)=n\ln(2\theta)-2\theta\sum_{i=1}^n X_i.` |
| 2966 | 24651-24653 | 0.42 | inline_safe | bracket | `\ell'(\theta)=\frac{n}{\theta}-2\sum_{i=1}^n X_i=0,` |
| 2967 | 24655-24658 | 0.33 | normalized_width_not_low | bracket | `\hat\theta_1=\frac{n}{2\sum_{i=1}^n X_i} =\frac1{2\overline X}.` |
| 2968 | 24660-24662 | 0.17 | inline_safe | bracket | `EX=\frac1{2\theta}.` |
| 2969 | 24664-24666 | 0.24 | inline_safe | bracket | `\hat\theta_2=\frac1{2\overline X}.` |
| 2970 | 24669-24671 | 0.14 | inline_safe | bracket | `S\sim \Gamma(n,2\theta)` |
| 2971 | 24673-24675 | 0.24 | inline_safe | bracket | `E\left(\frac1S\right)=\frac{2\theta}{n-1}.` |
| 2972 | 24677-24682 | 0.23 | normalized_width_not_low | bracket | `E\hat\theta_1 =E\left(\frac{n}{2S}\right) =\frac n2\cdot\frac{2\theta}{n-1} =\frac{n}{n-1}\theta.` |
| 2973 | 24684-24686 | 0.16 | inline_safe | bracket | `\frac{n-1}{n}\hat\theta_1.` |
| 2976 | 24709-24711 | 0.44 | inline_safe | bracket | `F(t) = 1 - e^{-t^2/\theta^2}\quad(t \geq 0).` |
| 2979 | 24723-24725 | 0.48 | inline_safe | bracket | `\hat{Q} = Q(\hat{\theta}) = \frac{\hat{\theta}^2}{2}\ln\hat{\theta} - \frac{3}{4}\hat{\theta}^2 + \hat{\theta}.` |
| 2980 | 24737-24739 | 0.39 | inline_safe | bracket | `E\overline X=\mu,\qquad D\overline X=\frac{\sigma^2}{n}.` |
| 2981 | 24741-24744 | 0.33 | normalized_width_not_low | bracket | `E(\overline X^2)=D\overline X+(E\overline X)^2 =\frac{\sigma^2}{n}+\mu^2.` |
| 2982 | 24746-24748 | 0.18 | inline_safe | bracket | `E(\overline X^2)\ne \mu^2.` |
| 2983 | 24754-24761 | 0.20 | inline_unsafe_marker | bracket | `f(x)= \begin{cases} (\theta+1)(x-5)^\theta, & 5<x<6,\\ 0, & \text{其他}, \end{cases} \qquad \theta>0.` |
| 2984 | 24766-24771 | 0.35 | normalized_width_not_low | bracket | `E(X)=5+E(U) =5+\int_0^1 u(\theta+1)u^\theta\,\mathrm{d}u =5+\frac{\theta+1}{\theta+2} =6-\frac1{\theta+2}.` |
| 2985 | 24773-24775 | 0.25 | inline_safe | bracket | `\overline X=6-\frac1{\theta+2},` |
| 2986 | 24777-24779 | 0.31 | inline_safe | bracket | `\hat\theta_M=\frac1{6-\overline X}-2.` |
| 2987 | 24782-24784 | 0.49 | inline_safe | bracket | `L(\theta)=(\theta+1)^n\prod_{i=1}^n (X_i-5)^\theta.` |
| 2990 | 24794-24797 | 0.42 | inline_safe | bracket | `\hat\theta_L =-\frac{n}{\sum_{i=1}^n\ln(X_i-5)}-1.` |
| 2991 | 24799-24801 | 0.31 | inline_safe | bracket | `\ell''(\theta)=-\frac{n}{(\theta+1)^2}<0,` |
| 2992 | 24826-24830 | 0.33 | normalized_width_not_low | bracket | `E\sum_{i=1}^{n}(X_i-\mu)^2 =\sum_{i=1}^{n}E(X_i-\mu)^2 =n\sigma^2.` |
| 2993 | 24832-24836 | 0.44 | normalized_width_not_low | bracket | `E\hat\sigma_3^2 =E\left[\frac1n\sum_{i=1}^{n}(X_i-\mu)^2\right] =\sigma^2,` |
| 2995 | 24853-24856 | 0.28 | normalized_width_not_low | bracket | `ET=E\!\left(\overline{X}^2-\frac{1}{n}S^2\right) =E(\overline{X}^2)-\frac{1}{n}E(S^2).` |
| 2997 | 24863-24866 | 0.33 | normalized_width_not_low | bracket | `E(\overline{X}^2)=D(\overline{X})+[E(\overline{X})]^2 =\frac{\sigma^2}{n}+\mu^2.` |
| 2998 | 24868-24870 | 0.41 | inline_safe | bracket | `ET=\left(\frac{\sigma^2}{n}+\mu^2\right)-\frac{1}{n}\sigma^2=\mu^2.` |
| 2999 | 24883-24885 | 0.43 | inline_safe | bracket | `\hat \mu = a_1 X_1 + a_2 X_2 + \dots + a_n X_n` |
| 3000 | 24887-24889 | 0.43 | inline_safe | bracket | `\hat\mu \text{ 是 } \mu \text{ 的无偏估计} \iff a_1+a_2+\dots+a_n=1` |
| 3002 | 24907-24909 | 0.39 | inline_safe | bracket | `\hat\mu=a_1X_1+a_2X_2+a_3X_3` |
| 3003 | 24927-24929 | 0.43 | inline_safe | bracket | `\widehat\mu=\frac14X_1+aX_2+\frac12X_3` |
| 3004 | 24934-24937 | 0.32 | inline_safe | bracket | `E\widehat\mu =\left(\frac14+a+\frac12\right)\mu.` |
| 3005 | 24939-24941 | 0.30 | inline_safe | bracket | `\frac14+a+\frac12=1.` |
| 3006 | 24943-24945 | 0.14 | inline_safe | bracket | `a=\frac14.` |
| 3007 | 24955-24957 | 0.13 | inline_safe | bracket | `E(c\overline{X})=\theta.` |
| 3008 | 24961-24963 | 0.44 | inline_safe | bracket | `f(x;\theta)=\frac{3x^2}{\theta^3},\qquad 0\le x\le \theta,` |
| 3009 | 24965-24970 | 0.34 | normalized_width_not_low | bracket | `EX=\int_0^\theta x\cdot \frac{3x^2}{\theta^3}\,\mathrm dx =\frac{3}{\theta^3}\int_0^\theta x^3\,\mathrm dx =\frac{3}{\theta^3}\cdot\frac{\theta^4}{4} =\frac{3\theta}{4}.` |
| 3010 | 24973-24975 | 0.33 | inline_safe | bracket | `E(c\overline{X})=cE(\overline{X})=c\cdot\frac{3\theta}{4}.` |
| 3011 | 24977-24979 | 0.28 | inline_safe | bracket | `c\cdot\frac{3\theta}{4}=\theta\implies c=\frac{4}{3}.` |
| 3012 | 24986-24988 | 0.26 | inline_unsafe_marker | bracket | `f(x,\theta) = \begin{cases} \dfrac{1}{\theta}\,e^{-x/\theta}, & x > 0\ (\theta > 0), \\ 0, & x \leq 0, \end{cases}` |
| 3014 | 25001-25003 | 0.46 | inline_safe | bracket | `\ln L(\theta)=-n\ln\theta-\frac{1}{\theta}\sum_{i=1}^n X_i.` |
| 3015 | 25006-25009 | 0.39 | inline_safe | bracket | `\frac{\mathrm{d}\ln L}{\mathrm{d}\theta} =-\frac{n}{\theta}+\frac{1}{\theta^2}\sum_{i=1}^n X_i.` |
| 3016 | 25011-25015 | 0.39 | normalized_width_not_low | bracket | `-\frac{n}{\theta}+\frac{1}{\theta^2}\sum_{i=1}^n X_i=0 \quad\Longrightarrow\quad \hat{\theta}=\frac{1}{n}\sum_{i=1}^n X_i=\overline{X}.` |
| 3017 | 25018-25021 | 0.39 | normalized_width_not_low | bracket | `\frac{\mathrm{d}^2\ln L}{\mathrm{d}\theta^2} =\frac{n}{\theta^2}-\frac{2}{\theta^3}\sum_{i=1}^n X_i.` |
| 3018 | 25023-25027 | 0.22 | normalized_width_not_low | bracket | `\left.\frac{\mathrm{d}^2\ln L}{\mathrm{d}\theta^2}\right\|_{\theta=\overline{X}} =\frac{n}{\overline{X}^2}-\frac{2n\overline{X}}{\overline{X}^3} =-\frac{n}{\overline{X}^2}<0,` |
| 3019 | 25031-25033 | 0.08 | inline_safe | bracket | `EX=\theta,` |
| 3021 | 25045-25047 | 0.46 | inline_safe | bracket | `D = k\sum_{i=1}^{n-1}(X_{i+1}-X_i)^2` |
| 3022 | 25054-25056 | 0.33 | inline_safe | bracket | `E(X_{i+1}-X_i)=\mu-\mu=0,` |
| 3025 | 25068-25073 | 0.48 | normalized_width_not_low | bracket | `ED =k\sum_{i=1}^{n-1}E\bigl[(X_{i+1}-X_i)^2\bigr] =k(n-1)\cdot 2\sigma^2 =2k(n-1)\sigma^2.` |
| 3027 | 25094-25096 | 0.46 | inline_safe | bracket | `f = (2\pi\sigma^2)^{-(m+n)/2}\,\exp\!\left\{-\frac{T}{2\sigma^2}\right\}.` |
| 3029 | 25102-25104 | 0.35 | inline_safe | bracket | `E(\hat{\sigma}^2) = \frac{(m+n)\sigma^2}{m+n} = \sigma^2.` |
| 3030 | 25110-25112 | 0.27 | inline_unsafe_marker | bracket | `F(x,\alpha,\beta) = \begin{cases} 1-\left(\dfrac{\alpha}{x}\right)^{\!\beta}, & x > \alpha, \\ 0, & x \leq \alpha, \end{cases}` |
| 3033 | 25139-25141 | 0.35 | inline_safe | bracket | `\hat{\theta}_2 = \max\{X_1, X_2, \dots, X_n\}.` |
| 3035 | 25148-25153 | 0.32 | display_environment | dollar | `F_X(x) = \begin{cases} 0, & x<0 \\ \displaystyle \int_{0}^{x} \frac{3t^2}{\theta^3} dt = \frac{x^3}{\theta^3}, & 0\leq x\leq\theta \\ 1, & x>\theta \end{cases}` |
| 3037 | 25157-25157 | 0.48 | display_environment | dollar | `f_{\hat{\theta}_2}(x) = F'_{\hat{\theta}_2}(x) =\begin{cases}\displaystyle \frac{3n x^{3n-1}}{\theta^{3n}}, & 0\leq x\leq\theta \\0, & \text{其他}\end{cases}` |
| 3039 | 25172-25174 | 0.32 | inline_unsafe_marker | bracket | `f_X(x,\theta) = \begin{cases} 4\,e^{-4(x-\theta)}, & x \geq \theta, \\ 0, & \text{其他}, \end{cases}` |
| 3041 | 25183-25183 | 0.40 | display_environment | dollar | `\hat{\theta} = X_{(1)} = \min\{X_1,X_2,\dots,X_n\}` |
| 3043 | 25188-25188 | 0.39 | display_environment | dollar | `X_{(1)} - \theta = \min\{Y_1,Y_2,\dots,Y_n\}` |
| 3045 | 25192-25192 | 0.20 | display_environment | dollar | `E\left(\min Y_i\right) = \frac{1}{4n}` |
| 3047 | 25198-25200 | 0.33 | display_environment | dollar | `\hat{\theta}_{\text{unbiased}} = X_{(1)} - \frac{1}{4n}` |
| 3049 | 25219-25221 | 0.46 | inline_safe | bracket | `S^2=\frac{1}{n-1}\sum_{i=1}^n (X_i-\overline{X})^2.` |
| 3050 | 25223-25226 | 0.49 | normalized_width_not_low | bracket | `\sum_{i=1}^n (X_i-\overline{X})^2 =\sum_{i=1}^n (X_i-\mu)^2-n(\overline{X}-\mu)^2.` |
| 3052 | 25233-25235 | 0.34 | inline_safe | bracket | `E(\overline{X}-\mu)^2=D(\overline{X})=\frac{\sigma^2}{n},` |
| 3053 | 25237-25240 | 0.39 | normalized_width_not_low | bracket | `E\!\left[\sum_{i=1}^n (X_i-\overline{X})^2\right] =n\sigma^2-n\cdot\frac{\sigma^2}{n}=(n-1)\sigma^2.` |
| 3056 | 25262-25264 | 0.31 | inline_safe | bracket | `E(S_X^2+S_Y^2)=2\sigma^2,` |
| 3058 | 25268-25270 | 0.38 | inline_safe | bracket | `E\!\left(\frac{S_X^2+S_Y^2}{m+n-2}\right)=\frac{2\sigma^2}{m+n-2},` |
| 3059 | 25271-25274 | 0.38 | normalized_width_not_low | bracket | `E\!\left(\frac{(m-1)S_X^2+(n-1)S_Y^2}{m+n-2}\right) =\frac{(m-1)\sigma^2+(n-1)\sigma^2}{m+n-2}.` |
| 3061 | 25295-25297 | 0.33 | inline_safe | bracket | `E(X)=\lambda,\qquad D(X)=\lambda.` |
| 3062 | 25299-25301 | 0.41 | inline_safe | bracket | `E(\overline{X})=\frac{1}{n}\sum_{i=1}^n E(X_i)=\lambda,` |
| 3063 | 25305-25307 | 0.21 | inline_safe | bracket | `E(S^2)=D(X)=\lambda.` |
| 3064 | 25323-25325 | 0.28 | inline_safe | bracket | `EX=\lambda,\qquad DX=\lambda.` |
| 3065 | 25327-25329 | 0.38 | inline_safe | bracket | `E(\overline{X})=\lambda,\qquad D(\overline{X})=\frac{\lambda}{n}.` |
| 3066 | 25332-25335 | 0.33 | inline_safe | bracket | `E(\overline{X}^2)=D(\overline{X})+[E(\overline{X})]^2 =\frac{\lambda}{n}+\lambda^2.` |
| 3067 | 25338-25340 | 0.30 | inline_safe | bracket | `E\!\left(\frac{1}{n}\overline{X}\right)=\frac{1}{n}E(\overline{X})=\frac{\lambda}{n},` |
| 3068 | 25342-25346 | 0.22 | inline_safe | bracket | `E\!\left(\overline{X}^2-\frac{1}{n}\overline{X}\right) =\left(\frac{\lambda}{n}+\lambda^2\right)-\frac{\lambda}{n} =\lambda^2.` |
| 3069 | 25349-25351 | 0.15 | inline_safe | bracket | `\overline{X}^2-\frac{1}{n}\overline{X}` |
| 3070 | 25356-25356 | 0.28 | inline_safe | bracket | `X_{(n)} = \max(X_1, \dots, X_n)` |
| 3072 | 25362-25362 | 0.48 | display_environment | dollar | `f_{X_{(n)}}(x) = \frac{n}{\theta^n}x^{n-1} \quad (0 < x < \theta)` |
| 3074 | 25363-25363 | 0.46 | display_environment | dollar | `E\left(\frac{n+1}{n}X_{(n)}\right) = \frac{n+1}{n} \cdot \frac{n}{n+1}\theta = \theta` |
| 3075 | 25381-25385 | 0.46 | normalized_width_not_low | bracket | `\hat{\mu}_1 = \frac{1}{5}X_1 + \frac{3}{10}X_2 + \frac{1}{2}X_3,\quad \hat{\mu}_2 = \frac{1}{3}X_1 + \frac{1}{4}X_2 + \frac{5}{12}X_3,\quad \hat{\mu}_3 = \frac{1}{3}X_1 + \frac{...` |
| 3076 | 25393-25397 | 0.34 | inline_safe | bracket | `E\hat{\mu}_1 =\left(\frac15+\frac{3}{10}+\frac12\right)\mu =\mu.` |
| 3077 | 25400-25404 | 0.34 | inline_safe | bracket | `E\hat{\mu}_2 =\left(\frac13+\frac14+\frac{5}{12}\right)\mu =\mu.` |
| 3078 | 25407-25411 | 0.38 | normalized_width_not_low | bracket | `E\hat{\mu}_3 =\left(\frac13+\frac16+\frac12\right)\mu =\mu.` |
| 3082 | 25437-25441 | 0.29 | normalized_width_not_low | bracket | `\frac{38}{100}=0.380,\qquad \frac{50}{144}\approx 0.347,\qquad \frac{14}{36}\approx 0.389.` |
| 3083 | 25443-25445 | 0.23 | inline_safe | bracket | `\frac{50}{144}<\frac{38}{100}<\frac{14}{36}.` |
| 3084 | 25465-25469 | 0.40 | normalized_width_not_low | bracket | `D\mu_2=D\!\left(\frac23X_1+\frac13X_2\right) =\left(\frac23\right)^2+\left(\frac13\right)^2 =\frac59.` |
| 3085 | 25472-25476 | 0.39 | normalized_width_not_low | bracket | `D\mu_3=\left(\frac14\right)^2+\left(\frac34\right)^2 =\frac{1}{16}+\frac{9}{16} =\frac58.` |
| 3087 | 25484-25486 | 0.35 | inline_safe | bracket | `\frac12<\frac59<\frac58<1.` |
| 3088 | 25498-25500 | 0.35 | inline_safe | bracket | `EX=\frac{\theta}{2},\qquad DX=\frac{\theta^2}{12}.` |
| 3089 | 25505-25507 | 0.33 | inline_safe | bracket | `E(\hat{\theta}_1)=E(2\overline{X})=2EX=\theta,` |
| 3090 | 25508-25510 | 0.40 | inline_safe | bracket | `E(\hat{\theta}_2)=E(X_1+X_2)=2EX=\theta,` |
| 3092 | 25515-25519 | 0.41 | normalized_width_not_low | bracket | `D\hat{\theta}_1 = 4D(\overline{X}) = \frac{4\theta^2}{12\cdot3} = \frac{\theta^2}{9}, \quad D\hat{\theta}_2 = 2\cdot\frac{\theta^2}{12} = \frac{\theta^2}{6},` |
| 3094 | 25523-25525 | 0.26 | inline_safe | bracket | `\frac{\theta^2}{9}<\frac{3\theta^2}{25}<\frac{\theta^2}{6}.` |
| 3095 | 25532-25538 | 0.11 | inline_unsafe_marker | bracket | `f(x;\theta)= \begin{cases} \dfrac1\theta, & 0<x<\theta,\\ 0, & \text{其它}. \end{cases}` |
| 3096 | 25543-25546 | 0.49 | normalized_width_not_low | bracket | `L(\theta)=\prod_{i=1}^n \frac1\theta \mathbf 1_{(0,\theta)}(X_i) =\theta^{-n}\mathbf 1_{\{\theta\ge X_{(n)}\}},` |
| 3097 | 25548-25550 | 0.18 | inline_safe | bracket | `\hat\theta_1=X_{(n)}.` |
| 3098 | 25552-25554 | 0.17 | inline_safe | bracket | `\hat\theta_2=2\overline X.` |
| 3099 | 25556-25558 | 0.36 | inline_safe | bracket | `E(\hat\theta_2)=2E(\overline X)=2EX=\theta,` |
| 3100 | 25562-25564 | 0.37 | inline_safe | bracket | `E(\hat\theta_1)=E(X_{(n)})=\frac{n}{n+1}\theta,` |
| 3101 | 25591-25595 | 0.44 | normalized_width_not_low | bracket | `EX^2 =\frac{1}{2\theta}\int_{-\infty}^{+\infty}x^2e^{-\|x\|/\theta}\,\mathrm{d}x =\frac1\theta\int_0^\infty x^2e^{-x/\theta}\,\mathrm{d}x.` |
| 3102 | 25597-25601 | 0.33 | inline_safe | bracket | `EX^2 =\theta^2\int_0^\infty t^2e^{-t}\,\mathrm{d}t =2\theta^2.` |
| 3103 | 25603-25605 | 0.40 | inline_safe | bracket | `2\theta^2=\frac1n\sum_{i=1}^{n}X_i^2,` |
| 3104 | 25607-25609 | 0.40 | inline_safe | bracket | `\hat{\theta}_M=\sqrt{\frac{1}{2n}\sum_{i=1}^{n}X_i^2}.` |
| 3105 | 25612-25615 | 0.43 | normalized_width_not_low | bracket | `L(\theta)=\prod_{i=1}^{n}\frac{1}{2\theta}e^{-\|X_i\|/\theta} =(2\theta)^{-n}e^{-\sum\|X_i\|/\theta}.` |
| 3107 | 25621-25624 | 0.46 | normalized_width_not_low | bracket | `\frac{\mathrm d}{\mathrm d\theta}\ln L(\theta) =-\frac{n}{\theta}+\frac{1}{\theta^2}\sum_{i=1}^{n}\|X_i\|=0,` |
| 3108 | 25626-25628 | 0.35 | inline_safe | bracket | `\hat{\theta}_L=\frac{1}{n}\sum_{i=1}^{n}\|X_i\|.` |
| 3109 | 25631-25635 | 0.44 | normalized_width_not_low | bracket | `E\|X\| =\frac{1}{2\theta}\int_{-\infty}^{+\infty}\|x\|e^{-\|x\|/\theta}\,\mathrm{d}x =\frac{1}{\theta}\int_0^\infty xe^{-x/\theta}\,\mathrm{d}x.` |
| 3110 | 25637-25639 | 0.48 | inline_safe | bracket | `E\|X\|=\theta\int_0^\infty te^{-t}\,\mathrm{d}t=\theta\,\Gamma(2)=\theta.` |
| 3112 | 25647-25649 | 0.37 | inline_safe | bracket | `\hat{\theta}_L = \frac{1}{n}\sum\|X_i\| \xrightarrow{P} E\|X\| = \theta.` |
| 3114 | 25663-25665 | 0.08 | inline_safe | bracket | `EX=0,` |
| 3115 | 25667-25671 | 0.44 | normalized_width_not_low | bracket | `EX^2 =\frac{1}{2\theta}\int_{-\infty}^{+\infty}x^2e^{-\|x\|/\theta}\,\mathrm{d}x =\frac{1}{\theta}\int_0^\infty x^2e^{-x/\theta}\,\mathrm{d}x.` |
| 3116 | 25673-25677 | 0.38 | normalized_width_not_low | bracket | `EX^2 =\frac{1}{\theta}\int_0^\infty \theta^2t^2e^{-t}\theta\,\mathrm{d}t =\theta^2\Gamma(3)=2\theta^2.` |
| 3117 | 25679-25681 | 0.40 | inline_safe | bracket | `2\theta^2=\frac1n\sum_{i=1}^n X_i^2,` |
| 3118 | 25683-25685 | 0.41 | inline_safe | bracket | `\hat\theta_M=\sqrt{\frac{1}{2n}\sum_{i=1}^n X_i^2}.` |
| 3119 | 25690-25692 | 0.37 | inline_safe | bracket | `Y = \frac{2}{n(n+1)}\sum_{i=1}^{n}iX_i` |
| 3123 | 25715-25717 | 0.26 | inline_safe | bracket | `\mathrm{MSE}(\hat{\theta}) = E(\hat{\theta} - \theta)^2` |
| 3126 | 25754-25756 | 0.18 | inline_unsafe_marker | bracket | `f(x) = \begin{cases} e^{\theta-x}, & x > \theta, \\ 0, & x \leq \theta, \end{cases}` |
| 3127 | 25766-25768 | 0.38 | inline_safe | bracket | `\mathrm{MSE}_L = \left(\frac{1}{n}\right)^{\!2} + \frac{1}{n^2} = \frac{2}{n^2}.` |
| 3128 | 25774-25781 | 0.18 | inline_unsafe_marker | bracket | `f(x;\theta)= \begin{cases} 2e^{-2(x-\theta)}, & x>\theta,\\ 0, & x\le\theta, \end{cases} \qquad \theta>0.` |
| 3129 | 25790-25793 | 0.40 | normalized_width_not_low | bracket | `F(x)=\int_{\theta}^{x}2e^{-2(t-\theta)}\,\mathrm dt =1-e^{-2(x-\theta)}.` |
| 3130 | 25795-25801 | 0.21 | inline_unsafe_marker | bracket | `F(x)= \begin{cases} 0, & x\le\theta,\\ 1-e^{-2(x-\theta)}, & x>\theta. \end{cases}` |
| 3131 | 25804-25812 | 0.31 | inline_unsafe_marker | bracket | `\begin{aligned} F_{X_{(1)}}(x) &=P\{X_{(1)}\le x\}\\ &=1-P\{X_1>x,\dots,X_n>x\}\\ &=1-[1-F(x)]^n =1-e^{-2n(x-\theta)}. \end{aligned}` |
| 3132 | 25814-25820 | 0.22 | inline_unsafe_marker | bracket | `F_{\hat\theta}(x)= \begin{cases} 0, & x\le\theta,\\ 1-e^{-2n(x-\theta)}, & x>\theta. \end{cases}` |
| 3133 | 25823-25825 | 0.24 | inline_safe | bracket | `E\hat\theta=\theta+\frac1{2n}.` |
| 3135 | 25865-25871 | 0.11 | inline_unsafe_marker | bracket | `\begin{array}{c\|ccc} X & 1 & 2 & 3\\ \hline P & \theta^2 & 2\theta(1-\theta) & (1-\theta)^2 \end{array}` |
| 3136 | 25873-25875 | 0.30 | inline_safe | bracket | `(x_1,x_2,x_3)=(1,2,1),` |
| 3137 | 25880-25883 | 0.39 | normalized_width_not_low | bracket | `L(\theta)=(\theta^2)^2\cdot[2\theta(1-\theta)] =2\theta^5(1-\theta),\qquad 0<\theta<1.` |
| 3138 | 25885-25887 | 0.39 | inline_safe | bracket | `\ln L(\theta)=\ln2+5\ln\theta+\ln(1-\theta).` |
| 3139 | 25889-25891 | 0.20 | inline_safe | bracket | `\frac{5}{\theta}-\frac{1}{1-\theta}=0.` |
| 3140 | 25893-25895 | 0.15 | inline_safe | bracket | `5(1-\theta)=\theta,` |
| 3141 | 25897-25899 | 0.17 | inline_safe | bracket | `\hat\theta=\frac56.` |
| 3145 | 25922-25924 | 0.40 | inline_safe | bracket | `\frac1n\sum_{i=1}^{n}X_i^2=2\theta^2,` |
| 3146 | 25926-25928 | 0.46 | inline_safe | bracket | `\hat\theta_M=\sqrt{\frac1{2n}\sum_{i=1}^{n}X_i^2}.` |
| 3149 | 25941-25943 | 0.49 | inline_safe | bracket | `\ell'(\theta)=-\frac n\theta+\frac{\sum_{i=1}^{n}\|X_i\|}{\theta^2}.` |
| 3150 | 25945-25947 | 0.41 | inline_safe | bracket | `\hat\theta_L=\frac1n\sum_{i=1}^{n}\|X_i\|.` |
| 3151 | 25953-25955 | 0.30 | inline_safe | bracket | `k\sum_{i=1}^{n}\|X_i-\overline X\|` |
| 3152 | 25960-25962 | 0.20 | inline_safe | bracket | `Y_i=X_i-\overline X.` |
| 3153 | 25964-25966 | 0.11 | inline_safe | bracket | `EY_i=0.` |
| 3154 | 25968-25971 | 0.39 | normalized_width_not_low | bracket | `D(Y_i)=D(X_i-\overline X) =DX_i+D\overline X-2\operatorname{Cov}(X_i,\overline X).` |
| 3155 | 25973-25975 | 0.42 | inline_safe | bracket | `DX_i=\sigma^2,\qquad D\overline X=\frac{\sigma^2}{n},` |
| 3156 | 25976-25980 | 0.43 | normalized_width_not_low | bracket | `\operatorname{Cov}(X_i,\overline X) =\operatorname{Cov}\left(X_i,\frac1n\sum_{j=1}^n X_j\right) =\frac{\sigma^2}{n}.` |
| 3157 | 25982-25985 | 0.35 | normalized_width_not_low | bracket | `D(Y_i)=\sigma^2+\frac{\sigma^2}{n}-2\frac{\sigma^2}{n} =\frac{n-1}{n}\sigma^2.` |
| 3158 | 25987-25989 | 0.27 | inline_safe | bracket | `Y_i\sim N\left(0,\frac{n-1}{n}\sigma^2\right).` |
| 3159 | 25991-25993 | 0.22 | inline_safe | bracket | `E\|Z\|=\tau\sqrt{\frac2\pi}.` |
| 3160 | 25995-25998 | 0.28 | inline_safe | bracket | `E\|X_i-\overline X\| =\sigma\sqrt{\frac{n-1}{n}}\sqrt{\frac2\pi}.` |
| 3161 | 26000-26003 | 0.34 | normalized_width_not_low | bracket | `E\left[k\sum_{i=1}^{n}\|X_i-\overline X\|\right] =kn\sigma\sqrt{\frac{n-1}{n}}\sqrt{\frac2\pi}.` |
| 3162 | 26005-26008 | 0.30 | normalized_width_not_low | bracket | `k=\frac1{n}\sqrt{\frac{n}{n-1}}\sqrt{\frac{\pi}{2}} =\sqrt{\frac{\pi}{2n(n-1)}}.` |
| 3165 | 26108-26110 | 0.25 | display_environment | env:equation | `P\{\underline{\theta}<\theta<\overline{\theta}\} \ge 1-\alpha` |
| 3166 | 26214-26216 | 0.20 | inline_safe | bracket | `\overline{X}\sim N\!\left(\mu,\frac{\sigma^2}{n}\right).` |
| 3167 | 26218-26220 | 0.26 | inline_safe | bracket | `W=\frac{\overline{X}-\mu}{\sigma/\sqrt{n}}\sim N(0,1).` |
| 3168 | 26224-26226 | 0.45 | inline_safe | bracket | `P\left\{-z_{\alpha/2}<\frac{\overline{X}-\mu}{\sigma/\sqrt{n}}<z_{\alpha/2}\right\}=1-\alpha.` |
| 3170 | 26234-26236 | 0.45 | inline_safe | bracket | `\left(\overline{X}-\frac{\sigma}{\sqrt{n}}z_{\alpha/2},\ \overline{X}+\frac{\sigma}{\sqrt{n}}z_{\alpha/2}\right).` |
| 3171 | 26250-26252 | 0.37 | inline_safe | bracket | `T=\frac{\overline X-\mu}{S/\sqrt n}\sim t(n-1)=t(8).` |
| 3172 | 26254-26256 | 0.34 | inline_safe | bracket | `P\left\{T\ge -t_{0.05}(8)\right\}=0.95,` |
| 3173 | 26258-26260 | 0.44 | inline_safe | bracket | `P\left\{\mu\le \overline X+t_{0.05}(8)\frac{S}{\sqrt n}\right\}=0.95.` |
| 3174 | 26262-26265 | 0.31 | inline_safe | bracket | `U=6+1.8595\cdot\frac{\sqrt{0.33}}{3} \approx 6.356.` |
| 3175 | 26278-26280 | 0.38 | inline_safe | bracket | `b=EX=E(e^Y)=e^{\mu+\frac12}.` |
| 3176 | 26283-26285 | 0.24 | inline_safe | bracket | `\overline Y\sim N\left(\mu,\frac14\right).` |
| 3178 | 26293-26296 | 0.34 | normalized_width_not_low | bracket | `\left(\overline y-\frac{1.96}{2},\ \overline y+\frac{1.96}{2}\right) =(-0.98,\ 0.98).` |
| 3179 | 26299-26303 | 0.32 | normalized_width_not_low | bracket | `-0.98<\mu<0.98 \quad\Longrightarrow\quad -0.48<\mu+\frac12<1.48.` |
| 3180 | 26305-26307 | 0.25 | inline_safe | bracket | `\left(e^{-0.48},\ e^{1.48}\right).` |
| 3181 | 26315-26317 | 0.32 | inline_safe | bracket | `P\{\|\overline X-\mu\|\le20\}\ge0.95.` |
| 3182 | 26319-26321 | 0.23 | inline_safe | bracket | `\frac{\overline X-\mu}{\sigma/\sqrt n}\sim N(0,1),` |
| 3183 | 26323-26326 | 0.23 | inline_safe | bracket | `P\{\|\overline X-\mu\|\le20\} =2\Phi\left(\frac{20\sqrt n}{100}\right)-1.` |
| 3184 | 26328-26330 | 0.32 | inline_safe | bracket | `\frac{20\sqrt n}{100}\ge z_{0.025}=1.96.` |
| 3185 | 26332-26334 | 0.36 | inline_safe | bracket | `n\ge\left(\frac{1.96\times100}{20}\right)^2=96.04.` |
| 3186 | 26343-26346 | 0.23 | inline_safe | bracket | `P\{\|\overline X-\mu\|\le80\} =2\Phi\left(\frac{80\sqrt n}{200}\right)-1.` |
| 3187 | 26348-26350 | 0.19 | inline_safe | bracket | `\frac{80\sqrt n}{200}\ge1.96.` |
| 3188 | 26352-26354 | 0.36 | inline_safe | bracket | `n\ge\left(\frac{1.96\times200}{80}\right)^2=24.01.` |
| 3189 | 26366-26368 | 0.10 | inline_safe | bracket | `\frac{\overline{X}-\mu}{\sigma/\sqrt{n}}.` |
| 3190 | 26372-26374 | 0.28 | inline_safe | bracket | `W=\frac{\overline{X}-\mu}{S/\sqrt{n}}\sim t(n-1).` |
| 3194 | 26405-26407 | 0.36 | inline_safe | bracket | `W=\frac{(n-1)S^2}{\sigma^2}\sim\chi^2(n-1).` |
| 3198 | 26438-26440 | 0.10 | inline_safe | bracket | `\overline{X}-\overline{Y}.` |
| 3203 | 26474-26478 | 0.27 | normalized_width_not_low | bracket | `\frac{S_1^2/\sigma_1^2}{S_2^2/\sigma_2^2} =\frac{S_1^2}{S_2^2}\cdot\frac{\sigma_2^2}{\sigma_1^2} \sim F(n_1-1,n_2-1).` |
| 3207 | 26498-26501 | 0.46 | normalized_width_not_low | bracket | `\left(\frac{S_1^2}{S_2^2}\cdot\frac{1}{F_{\alpha/2}(n_1-1,n_2-1)},\ \frac{S_1^2}{S_2^2}\cdot F_{\alpha/2}(n_2-1,n_1-1)\right).` |
| 3208 | 26516-26518 | 0.42 | display_environment | env:equation* | `\frac{X_i-\mu}{\sigma} \sim N(0,1), \quad i=1,2,\dots,n` |
| 3215 | 26562-26565 | 0.43 | display_environment | env:align* | `E(\overline{X}-\overline{Y}) &= E(\overline{X}) - E(\overline{Y}) = \mu_1 - \mu_2 \\ D(\overline{X}-\overline{Y}) &= D(\overline{X}) + D(\overline{Y}) = \frac{\sigma_1^2}{n_1} +...` |
| 3217 | 26572-26574 | 0.45 | display_environment | env:equation* | `W = \frac{(\overline{X}-\overline{Y}) - (\mu_1-\mu_2)}{\sqrt{\frac{\sigma_1^2}{n_1} + \frac{\sigma_2^2}{n_2}}} \sim N(0,1)` |
| 3229 | 26657-26659 | 0.43 | display_environment | env:equation* | `\left( \overline{X} - \frac{\sigma}{\sqrt{n}} z_{\alpha/2},\ \overline{X} + \frac{\sigma}{\sqrt{n}} z_{\alpha/2} \right)` |
| 3230 | 26661-26663 | 0.20 | inline_safe | bracket | `L = 2\frac{\sigma}{\sqrt{n}} z_{\alpha/2}.` |
| 3231 | 26675-26677 | 0.44 | display_environment | env:equation* | `Z = \frac{\overline{X}-\mu}{\sigma/\sqrt{n}} = \frac{\overline{X}-\mu}{1/\sqrt{100}} \stackrel{\text{近似}}{\sim} N(0,1)` |
| 3232 | 26681-26683 | 0.44 | display_environment | env:equation* | `\left( \overline{X} - \frac{1}{10} \times 1.96,\ \overline{X} + \frac{1}{10} \times 1.96 \right)` |
| 3233 | 26696-26698 | 0.25 | display_environment | env:equation* | `L = 2 \cdot \frac{\sigma}{\sqrt{n}} z_{0.025}` |
| 3236 | 26717-26719 | 0.31 | display_environment | env:equation* | `\frac{1.73}{5} \times 2.0639 \approx 0.7141` |
| 3237 | 26730-26732 | 0.42 | display_environment | env:equation* | `\left( \frac{(n-1)S^2}{\chi^2_{0.025}(9)},\ \frac{(n-1)S^2}{\chi^2_{0.975}(9)} \right)` |
| 3238 | 26734-26736 | 0.49 | display_environment | env:equation* | `\frac{18}{19.023} \approx 0.9462,\quad \frac{18}{2.70} \approx 6.6667` |
| 3239 | 26748-26750 | 0.22 | inline_safe | bracket | `P\{\mu \ge \underline{\mu}\}=0.95.` |
| 3240 | 26752-26754 | 0.33 | display_environment | env:equation* | `P\left( \frac{\overline{X}-\mu}{\sigma/\sqrt{n}} \le z_{0.05} \right) = 0.95` |
| 3241 | 26756-26758 | 0.38 | display_environment | env:equation* | `\underline{\mu} = 6 - 1.645 \frac{\sigma}{3} \approx 6 - 0.5483\sigma` |
| 3242 | 26766-26768 | 0.21 | inline_safe | bracket | `P\{\theta>\underline{\theta}\}\ge 1-\alpha.` |
| 3243 | 26773-26775 | 0.21 | inline_safe | bracket | `P\{\theta>\underline{\theta}\}\ge 1-\alpha.` |
| 3244 | 26777-26779 | 0.20 | inline_safe | bracket | `P\{\theta>\underline{\theta}\}=1-\alpha,` |
| 3246 | 26797-26799 | 0.26 | inline_safe | bracket | `Z=\frac{\overline{X}-\mu}{\sigma/\sqrt{n}}\sim N(0,1).` |
| 3247 | 26801-26805 | 0.45 | normalized_width_not_low | bracket | `\overline{x} =\frac{1820+1834+1831+1816+1824}{5} =\frac{9125}{5}=1825.` |
| 3248 | 26807-26812 | 0.19 | structural | bracket | `\left( \overline{x}-1.96\frac{\sigma}{\sqrt n}, \overline{x}+1.96\frac{\sigma}{\sqrt n} \right).` |
| 3249 | 26814-26816 | 0.22 | inline_safe | bracket | `1.96\frac{10}{\sqrt5}\approx 8.77.` |
| 3251 | 26822-26824 | 0.25 | inline_safe | bracket | `[1816.23,\ 1833.77].` |
| 3252 | 26833-26835 | 0.44 | display_environment | env:equation* | `\overline{X} = \frac{1}{n}\sum_{i=1}^9 X_i = \frac{198}{9} = 22` |
| 3256 | 26863-26865 | 0.26 | inline_safe | bracket | `\hat p=\frac{175}{400}=0.4375.` |
| 3258 | 26871-26873 | 0.38 | inline_safe | bracket | `\sqrt{\frac{0.4375\times0.5625}{400}}\approx0.0248,` |
| 3260 | 26886-26888 | 0.27 | inline_safe | bracket | `\hat p=\frac{275}{600}\approx0.4583.` |
| 3262 | 26894-26896 | 0.33 | inline_safe | bracket | `\sqrt{\frac{\hat p(1-\hat p)}{600}}\approx0.0203,` |
| 3264 | 26909-26911 | 0.30 | inline_safe | bracket | `\frac{\hat p-p}{\sqrt{p(1-p)/n}}\approx N(0,1).` |
| 3265 | 26913-26915 | 0.30 | inline_safe | bracket | `P\{\|\hat p-p\|<0.1\}>0.95.` |
| 3266 | 26917-26919 | 0.31 | inline_safe | bracket | `P\left\{\left\|Z\right\|<\frac{0.1\sqrt n}{1/2}\right\}\ge0.95.` |
| 3267 | 26921-26923 | 0.21 | inline_safe | bracket | `\frac{0.1\sqrt n}{1/2}\ge1.96,` |
| 3268 | 26925-26927 | 0.29 | inline_safe | bracket | `n\ge\left(\frac{1.96}{0.2}\right)^2=96.04.` |
| 3269 | 26958-26960 | 0.16 | inline_safe | bracket | `X\sim N(\mu,\sigma^2)` |
| 3270 | 26962-26964 | 0.36 | inline_safe | bracket | `\overline X=15,\qquad S^2=0.36.` |
| 3271 | 26969-26971 | 0.29 | inline_safe | bracket | `T=\frac{\overline X-\mu}{S/\sqrt n}\sim t(n-1).` |
| 3272 | 26973-26975 | 0.21 | inline_safe | bracket | `P(\mu<\overline\mu)=0.95.` |
| 3273 | 26977-26979 | 0.42 | inline_safe | bracket | `P\left\{\frac{\overline X-\mu}{S/\sqrt n}>-t_{0.05}(15)\right\}=0.95` |
| 3274 | 26981-26983 | 0.32 | inline_safe | bracket | `\mu<\overline X+t_{0.05}(15)\frac{S}{\sqrt n}.` |
| 3275 | 26985-26987 | 0.40 | inline_safe | bracket | `S=\sqrt{0.36}=0.6,\qquad n=16.` |
| 3276 | 26989-26994 | 0.27 | normalized_width_not_low | bracket | `\overline\mu =15+1.7531\cdot\frac{0.6}{4} =15+0.2630 =15.2630.` |
| 3277 | 26996-26998 | 0.19 | inline_safe | bracket | `(-\infty,\,15.2630).` |
| 3279 | 27094-27096 | 0.26 | inline_safe | bracket | `\alpha = P\{\text{拒绝}\, H_0 \mid H_0\text{ 为真}\}.` |
| 3280 | 27098-27100 | 0.28 | inline_safe | bracket | `\beta = P\{\text{未拒绝}\, H_0 \mid H_1\text{ 为真}\}.` |
| 3281 | 27223-27225 | 0.14 | inline_safe | bracket | `H_1\colon \theta>\theta_0` |
| 3282 | 27227-27229 | 0.14 | inline_safe | bracket | `H_1\colon \theta<\theta_0` |
| 3283 | 27231-27233 | 0.13 | inline_safe | bracket | `H_1\colon \theta\ne\theta_0` |
| 3284 | 27248-27250 | 0.25 | inline_safe | bracket | `\alpha=P(\text{拒绝 }H_0\mid H_0\text{ 成立}).` |
| 3285 | 27252-27254 | 0.25 | inline_safe | bracket | `P(\text{接受 }H_1\mid H_0\text{ 成立})=\alpha.` |
| 3286 | 27267-27269 | 0.18 | inline_safe | bracket | `T=\frac{\overline{X}-\mu_0}{S/\sqrt{n}}.` |
| 3287 | 27271-27273 | 0.44 | inline_safe | bracket | `S^2=\frac{Q^2}{n-1},\qquad S=\frac{Q}{\sqrt{n-1}},` |
| 3289 | 27279-27281 | 0.44 | inline_safe | bracket | `\text{故应选取的检验统计量为}\quad T=\frac{\overline{X}\sqrt{n(n-1)}}{Q}.` |
| 3292 | 27389-27391 | 0.35 | inline_safe | bracket | `H_0:\mu=5,\qquad H_1:\mu\ne 5,` |
| 3293 | 27396-27398 | 0.29 | inline_safe | bracket | `Z=\frac{\overline{X}-5}{1/\sqrt{100}}\sim N(0,1).` |
| 3294 | 27401-27403 | 0.28 | inline_safe | bracket | `\|Z\|\ge z_{\alpha/2}=z_{0.005}.` |
| 3295 | 27405-27407 | 0.19 | inline_safe | bracket | `z_{0.005}=2.57.` |
| 3296 | 27410-27414 | 0.16 | inline_safe | bracket | `z=\frac{5.32-5}{1/\sqrt{100}} =\frac{0.32}{0.1} =3.2.` |
| 3297 | 27416-27418 | 0.19 | inline_safe | bracket | `\|z\|=3.2>2.57,` |
| 3298 | 27428-27430 | 0.43 | inline_safe | bracket | `H_0\colon \mu=570,\qquad H_1\colon \mu\neq570.` |
| 3299 | 27432-27434 | 0.29 | inline_safe | bracket | `Z=\frac{\overline{X}-570}{8/\sqrt{10}}\sim N(0,1).` |
| 3300 | 27436-27438 | 0.26 | inline_safe | bracket | `\|z\|\ge z_{0.025}=1.96.` |
| 3301 | 27440-27444 | 0.20 | inline_safe | bracket | `z=\frac{575.2-570}{8/\sqrt{10}} =\frac{5.2\sqrt{10}}{8} \approx 2.055.` |
| 3302 | 27453-27455 | 0.39 | inline_safe | bracket | `H_0\colon \mu \leq 1500,\quad H_1\colon \mu > 1500.` |
| 3303 | 27457-27459 | 0.45 | inline_safe | bracket | `Z = \frac{\overline{X}-\mu_0}{\sigma/\sqrt{n}} = \frac{\overline{X}-1500}{200/\sqrt{25}} \sim N(0,1).` |
| 3304 | 27462-27464 | 0.41 | inline_safe | bracket | `z = \frac{1675-1500}{200/5} = \frac{175}{40} = 4.375.` |
| 3305 | 27491-27493 | 0.40 | inline_safe | bracket | `H_0\colon \mu = 2000,\quad H_1\colon \mu \neq 2000.` |
| 3306 | 27495-27497 | 0.40 | inline_safe | bracket | `t = \frac{\overline{X}-\mu_0}{S/\sqrt{n}} \sim t(n-1) = t(24).` |
| 3308 | 27512-27514 | 0.34 | inline_safe | bracket | `H_0\colon \mu \leq 70,\quad H_1\colon \mu > 70.` |
| 3309 | 27516-27518 | 0.28 | inline_safe | bracket | `t = \frac{\overline{X}-\mu_0}{S/\sqrt{n}} \sim t(24).` |
| 3310 | 27521-27523 | 0.43 | inline_safe | bracket | `t = \frac{69.5-70}{15/\sqrt{25}} = \frac{-0.5}{3} = -0.167.` |
| 3311 | 27538-27540 | 0.29 | inline_safe | bracket | `T=\frac{\overline X-\mu}{S/\sqrt n}\sim t(n-1).` |
| 3312 | 27542-27544 | 0.28 | inline_safe | bracket | `\overline x\pm t_{0.025}(35)\frac{s}{\sqrt n}.` |
| 3313 | 27546-27550 | 0.20 | normalized_width_not_low | bracket | `2.0301\cdot\frac{15}{\sqrt{36}} =2.0301\cdot2.5 =5.07525.` |
| 3314 | 27552-27555 | 0.44 | normalized_width_not_low | bracket | `\mu\in(66.5-5.07525,\ 66.5+5.07525) \approx(61.42,\ 71.58).` |
| 3315 | 27558-27560 | 0.39 | inline_safe | bracket | `H_0\colon\mu=70,\qquad H_1\colon\mu\neq70` |
| 3318 | 27577-27579 | 0.46 | inline_safe | bracket | `\chi^2=\frac{(n-1)s^2}{\sigma_0^2}=\frac{25\times7200}{5000}=36.` |
| 3322 | 27602-27604 | 0.43 | inline_safe | bracket | `\chi^2=\frac{(n-1)s^2}{\sigma_0^2}=\frac{0.82}{0.16}=5.125.` |
| 3325 | 27625-27630 | 0.47 | normalized_width_not_low | bracket | `S^2=\frac1{3}\sum_{i=1}^{4}(x_i-\overline x)^2 =\frac{40}{3}, \qquad S=\sqrt{\frac{40}{3}}\approx3.65.` |
| 3326 | 27633-27635 | 0.43 | inline_safe | bracket | `H_0:\mu=1260,\qquad H_1:\mu\ne1260.` |
| 3327 | 27637-27639 | 0.29 | inline_safe | bracket | `T=\frac{\overline X-1260}{S/\sqrt4}\sim t(3).` |
| 3328 | 27641-27643 | 0.37 | inline_safe | bracket | `\|T_0\|=\frac{1267-1260}{3.65/2}\approx3.836.` |
| 3329 | 27645-27647 | 0.35 | inline_safe | bracket | `3.836>t_{0.025}(3)=3.1824,` |
| 3330 | 27651-27653 | 0.36 | inline_safe | bracket | `H_0:\sigma\le2,\qquad H_1:\sigma>2.` |
| 3331 | 27655-27657 | 0.34 | inline_safe | bracket | `\chi^2=\frac{(n-1)S^2}{\sigma_0^2}\sim\chi^2(3).` |
| 3332 | 27659-27661 | 0.32 | inline_safe | bracket | `\chi_0^2=\frac{3\cdot(40/3)}{4}=10.` |
| 3333 | 27663-27665 | 0.32 | inline_safe | bracket | `\chi^2>\chi^2_{0.05}(3)=7.815.` |
| 3336 | 27690-27692 | 0.39 | inline_safe | bracket | `\chi^2 = \frac{(n-1)S^2}{\sigma_0^2} \sim \chi^2(n-1).` |
| 3338 | 27716-27718 | 0.40 | inline_safe | bracket | `H_0\colon \sigma^2 = 64,\quad H_1\colon \sigma^2 \neq 64.` |
| 3341 | 27729-27731 | 0.45 | inline_safe | bracket | `\chi^2 = \frac{9 \times 68.16}{64} = \frac{613.44}{64} = 9.585.` |
| 3342 | 27737-27739 | 0.39 | inline_safe | bracket | `1.31,\ 1.55,\ 1.34,\ 1.40,\ 1.45.` |
| 3344 | 27749-27753 | 0.35 | normalized_width_not_low | bracket | `\chi^2=\frac{(n-1)S^2}{\sigma_0^2} =\frac{\sum_{i=1}^{n}(X_i-\overline{X})^2}{0.048^2} \sim \chi^2(4).` |
| 3347 | 27765-27767 | 0.33 | inline_safe | bracket | `\chi^2=\frac{0.0362}{0.048^2}\approx15.7118.` |
| 3348 | 27769-27773 | 0.34 | normalized_width_not_low | bracket | `\chi^2\le \chi^2_{0.95}(4)=0.711 \quad\text{或}\quad \chi^2\ge \chi^2_{0.05}(4)=9.488.` |
| 3349 | 27780-27782 | 0.37 | inline_safe | bracket | `H_0\colon \sigma\ge2,\qquad H_1\colon \sigma<2,` |
| 3350 | 27793-27796 | 0.33 | normalized_width_not_low | bracket | `\chi^2=\frac{(n-1)S^2}{\sigma_0^2} =\frac{(n-1)S^2}{4}\sim\chi^2(n-1)` |
| 3351 | 27800-27802 | 0.28 | inline_safe | bracket | `\chi^2\le \chi^2_{1-\alpha}(n-1),` |
| 3355 | 27830-27832 | 0.13 | inline_safe | bracket | `H_0\colon \mu=50` |
| 3356 | 27839-27841 | 0.30 | inline_safe | bracket | `u=\frac{\overline X-\mu_0}{\sigma/\sqrt n}\sim N(0,1).` |
| 3357 | 27843-27845 | 0.30 | inline_safe | bracket | `u=\frac{48.5-50}{2/\sqrt9}=-2.25.` |
| 3358 | 27847-27849 | 0.26 | inline_safe | bracket | `\|u\|\ge u_{0.025}=1.96.` |
| 3359 | 27853-27855 | 0.32 | inline_safe | bracket | `t=\frac{\overline X-\mu_0}{S/\sqrt n}\sim t(n-1).` |
| 3360 | 27857-27859 | 0.28 | inline_safe | bracket | `t=\frac{48.5-50}{2.5/\sqrt9}=-1.8.` |
| 3361 | 27861-27863 | 0.30 | inline_safe | bracket | `\|t\|\ge t_{0.025}(8)=2.31.` |
| 3363 | 27878-27880 | 0.37 | inline_safe | bracket | `\overline x=\frac{6.0+5.7+\cdots+5.0}{9}=6.` |
| 3364 | 27883-27885 | 0.21 | inline_safe | bracket | `\overline X\sim N\!\left(\mu,\frac{\sigma^2}{n}\right),` |
| 3365 | 27887-27889 | 0.23 | inline_safe | bracket | `\overline x\pm u_{0.025}\frac{\sigma}{\sqrt n}.` |
| 3366 | 27891-27894 | 0.18 | inline_safe | bracket | `6\pm1.96\cdot\frac{0.6}{3} =6\pm0.392,` |
| 3367 | 27896-27898 | 0.20 | inline_safe | bracket | `(5.608,\ 6.392).` |
| 3369 | 27906-27908 | 0.21 | inline_safe | bracket | `\frac{\overline X-\mu}{S/\sqrt n}\sim t(8).` |
| 3370 | 27910-27913 | 0.26 | normalized_width_not_low | bracket | `\overline x\pm t_{0.025}(8)\frac{S}{\sqrt n} \approx6\pm2.306\frac{\sqrt{0.33}}{3}.` |
| 3371 | 27915-27917 | 0.23 | inline_safe | bracket | `\mu\in(5.558,\ 6.442).` |
| 3372 | 27926-27928 | 0.40 | inline_safe | bracket | `F = \frac{S_1^2}{S_2^2} \sim F(n_1-1, n_2-1).` |
| 3376 | 27971-27973 | 0.25 | inline_safe | bracket | `F = \frac{0.844}{0.767} \approx 1.100.` |
| 3379 | 27991-27993 | 0.39 | inline_safe | bracket | `1.23,\ 1.22,\ 1.20,\ 1.26,\ 1.23.` |
| 3382 | 28020-28022 | 0.43 | inline_safe | bracket | `H_0\colon \mu=100,\qquad H_1\colon \mu\neq100.` |
| 3383 | 28024-28026 | 0.28 | inline_safe | bracket | `t=\frac{\overline X-100}{S/\sqrt n}\sim t(5).` |
| 3384 | 28028-28030 | 0.33 | inline_safe | bracket | `t=\frac{99.3-100}{6.24/\sqrt6}\approx -0.275.` |
| 3385 | 28034-28036 | 0.37 | inline_safe | bracket | `H_0\colon \sigma\le5,\qquad H_1\colon \sigma>5.` |
| 3387 | 28055-28057 | 0.41 | inline_safe | bracket | `H_0\colon \mu=100,\qquad H_1\colon \mu\ne100.` |
| 3388 | 28059-28061 | 0.40 | inline_safe | bracket | `t=\frac{\overline X-100}{S/\sqrt n}\sim t(n-1)=t(9).` |
| 3389 | 28063-28065 | 0.32 | inline_safe | bracket | `t=\frac{98.2-100}{2.25/\sqrt{10}}\approx -2.53.` |
| 3390 | 28067-28069 | 0.30 | inline_safe | bracket | `\|t\|\ge t_{0.025}(9)=2.26.` |
| 3391 | 28073-28075 | 0.42 | inline_safe | bracket | `H_0\colon \sigma^2\le4,\qquad H_1\colon \sigma^2>4.` |
| 3392 | 28077-28079 | 0.34 | inline_safe | bracket | `\chi^2=\frac{(n-1)S^2}{\sigma_0^2}\sim\chi^2(9).` |
| 3393 | 28081-28083 | 0.34 | inline_safe | bracket | `\chi^2=\frac{9\times2.25^2}{4}\approx11.39.` |
| 3394 | 28085-28087 | 0.24 | inline_safe | bracket | `\chi^2\ge \chi^2_{0.05}(9).` |
| 3397 | 28110-28112 | 0.47 | inline_safe | bracket | `H_0\colon \mu=52.00,\qquad H_1\colon \mu>52.00.` |
| 3398 | 28114-28116 | 0.30 | inline_safe | bracket | `t=\frac{\overline X-52.00}{S/\sqrt n}\sim t(6).` |
| 3399 | 28118-28120 | 0.37 | inline_safe | bracket | `t=\frac{52.1357-52.00}{2.6954/\sqrt7}\approx0.133.` |
| 3400 | 28122-28124 | 0.29 | inline_safe | bracket | `t\ge t_{0.05}(6)\approx1.943.` |
| 3401 | 28128-28131 | 0.31 | normalized_width_not_low | bracket | `\mu\in\left(\overline{x}-t_{0.025}(6)\frac{s}{\sqrt n}, \overline{x}+t_{0.025}(6)\frac{s}{\sqrt n}\right).` |
| 3402 | 28133-28138 | 0.32 | normalized_width_not_low | bracket | `\mu\in \left(52.1357-2.447\frac{2.6954}{\sqrt7}, 52.1357+2.447\frac{2.6954}{\sqrt7}\right) \approx(49.64,\ 54.63).` |
| 3403 | 28148-28150 | 0.46 | inline_safe | bracket | `H_0\colon \mu=235.5,\qquad H_1\colon \mu\ne235.5.` |
| 3404 | 28152-28154 | 0.39 | inline_safe | bracket | `t=\frac{\sqrt n(\overline X-\mu_0)}{S}\sim t(n-1).` |
| 3405 | 28156-28160 | 0.32 | inline_safe | bracket | `\|t\| =\left\|\frac{\sqrt{49}(236.5-235.5)}{3.5}\right\| =2.` |
| 3406 | 28162-28164 | 0.26 | inline_safe | bracket | `\|t\|\ge u_{0.005}=2.58.` |
| 3407 | 28166-28168 | 0.10 | inline_safe | bracket | `2<2.58,` |
| 3408 | 28174-28176 | 0.17 | inline_safe | bracket | `\overline{x}=495.3\ \text{克},` |
| 3409 | 28178-28180 | 0.15 | inline_safe | bracket | `s=13.74\ \text{克}.` |
| 3410 | 28188-28190 | 0.43 | inline_safe | bracket | `H_0\colon \mu=500,\qquad H_1\colon \mu\neq500.` |
| 3411 | 28192-28194 | 0.28 | inline_safe | bracket | `t=\frac{\overline X-500}{S/\sqrt n}\sim t(5).` |
| 3412 | 28196-28200 | 0.20 | inline_safe | bracket | `t=\frac{495.3-500}{13.74/\sqrt6} \approx \frac{-4.7}{5.609} \approx -0.838.` |
| 3413 | 28202-28204 | 0.33 | inline_safe | bracket | `\|t\|\ge t_{0.025}(5)=2.5706.` |
| 3414 | 28208-28210 | 0.39 | inline_safe | bracket | `H_0\colon \sigma\le10,\qquad H_1\colon \sigma>10.` |
| 3415 | 28212-28214 | 0.33 | inline_safe | bracket | `\chi^2=\frac{(n-1)S^2}{100}\sim\chi^2(5)` |
| 3416 | 28216-28220 | 0.24 | normalized_width_not_low | bracket | `\chi^2=\frac{5\times 13.74^2}{100} =\frac{5\times188.7876}{100} \approx9.439.` |
| 3417 | 28222-28224 | 0.35 | inline_safe | bracket | `\chi^2\ge\chi^2_{0.05}(5)=11.071.` |
| 3418 | 28232-28234 | 0.36 | inline_safe | bracket | `\overline X=499,\qquad S=16.03.` |
| 3419 | 28242-28244 | 0.28 | inline_safe | bracket | `T=\frac{\overline X-500}{S/\sqrt n}\sim t(8).` |
| 3420 | 28246-28248 | 0.30 | inline_safe | bracket | `\|T\|>t_{0.025}(8)=2.306.` |
| 3421 | 28250-28254 | 0.21 | normalized_width_not_low | bracket | `T_0=\frac{499-500}{16.03/3} =-\frac3{16.03} \approx -0.187.` |
| 3422 | 28258-28261 | 0.22 | inline_safe | bracket | `\chi^2=\frac{(n-1)S^2}{100} =\frac{8S^2}{100},` |
| 3423 | 28263-28265 | 0.37 | inline_safe | bracket | `\frac{8S^2}{100}>\chi^2_{0.05}(8)=15.507.` |
| 3424 | 28267-28270 | 0.17 | inline_safe | bracket | `\frac{8\times16.03^2}{100} \approx20.56.` |
| 3427 | 28302-28304 | 0.37 | inline_safe | bracket | `F=\frac{S_1^2}{S_2^2}=\frac{3.762}{4.019}\approx0.936.` |
| 3430 | 28322-28327 | 0.38 | normalized_width_not_low | bracket | `\left( \overline X-t_{1-\alpha/2}(n-1)\frac{S}{\sqrt{n-1}}, \overline X+t_{1-\alpha/2}(n-1)\frac{S}{\sqrt{n-1}} \right).` |
| 3432 | 28333-28335 | 0.28 | inline_safe | bracket | `1.943\cdot\frac{2.71}{\sqrt6}\approx2.15.` |
| 3434 | 28341-28343 | 0.20 | inline_safe | bracket | `(122.9,\ 127.1).` |
| 3435 | 28346-28348 | 0.47 | inline_safe | bracket | `H_0\colon\mu_1=\mu_2,\qquad H_1\colon\mu_1\ne\mu_2.` |
| 3436 | 28350-28355 | 0.26 | structural | bracket | `u= \frac{(\overline X-\overline Y)-0} {\sqrt{\sigma_1^2/n+\sigma_2^2/m}} \sim N(0,1).` |
| 3437 | 28357-28362 | 0.26 | structural | bracket | `u= \frac{1295-1230} {\sqrt{84^2/60+96^2/60}} \approx3.95.` |
| 3438 | 28364-28366 | 0.26 | inline_safe | bracket | `\|u\|\ge u_{0.975}=1.96.` |
| 3439 | 28378-28380 | 0.31 | inline_safe | bracket | `T=\frac{\overline X-\mu}{S^*/\sqrt n}\sim t(n-1).` |
| 3440 | 28382-28384 | 0.25 | inline_safe | bracket | `\overline x\pm t_{0.95}(6)\frac{S^*}{\sqrt7}.` |
| 3441 | 28386-28388 | 0.28 | inline_safe | bracket | `1.943\cdot\frac{2.71}{\sqrt7}\approx1.99.` |
| 3443 | 28394-28396 | 0.15 | inline_safe | bracket | `(123,\ 127).` |
| 3444 | 28399-28401 | 0.41 | inline_safe | bracket | `H_0\colon \mu=124,\qquad H_1\colon \mu\ne124.` |
| 3445 | 28403-28407 | 0.18 | inline_safe | bracket | `T=\frac{\overline X-\mu_0}{S^*/\sqrt n} =\frac{125-124}{2.71/\sqrt7} \approx0.976.` |
| 3446 | 28409-28411 | 0.30 | inline_safe | bracket | `\|T\|\ge t_{0.95}(6)=1.943.` |
| 3447 | 28413-28415 | 0.17 | inline_safe | bracket | `0.976<1.943,` |
| 3448 | 28424-28426 | 0.37 | inline_safe | bracket | `H_0\colon \theta=\theta_0,\quad H_1\colon \theta\neq\theta_0,` |
| 3452 | 28454-28456 | 0.42 | inline_safe | bracket | `t = \frac{10-9.7}{0.4/4} = \frac{0.3}{0.1} = 3.0 > 2.132.` |
| 3454 | 28471-28477 | 0.30 | normalized_width_not_low | bracket | `\mu\in \left( \overline x-t_{0.025}(15)\frac{s}{\sqrt n}, \overline x+t_{0.025}(15)\frac{s}{\sqrt n} \right).` |
| 3455 | 28479-28482 | 0.32 | normalized_width_not_low | bracket | `t_{0.025}(15)\frac{s}{\sqrt n} =2.132\cdot\frac{0.4}{4}=0.2132.` |
| 3456 | 28484-28486 | 0.27 | inline_safe | bracket | `\mu\in(9.7868,\ 10.2132).` |
| 3457 | 28489-28492 | 0.35 | normalized_width_not_low | bracket | `H_0\colon \sigma^2=0.048^2,\qquad H_1\colon \sigma^2\ne0.048^2.` |
| 3460 | 28506-28508 | 0.33 | inline_safe | bracket | `\chi^2=\frac{0.031525}{0.048^2}\approx13.683.` |
| 3461 | 28510-28514 | 0.34 | normalized_width_not_low | bracket | `\chi^2>\chi^2_{0.025}(5)=12.833 \quad\text{或}\quad \chi^2<\chi^2_{0.975}(5)=0.831.` |
| 3463 | 28533-28535 | 0.27 | inline_safe | bracket | `\overline{x}=\frac{799.8}{8}=99.975,` |
| 3464 | 28537-28539 | 0.41 | inline_safe | bracket | `\sum_{i=1}^8(x_i-\overline{x})^2=8.815.` |
| 3466 | 28546-28548 | 0.41 | inline_safe | bracket | `H_0\colon \mu=100,\qquad H_1\colon \mu\ne100.` |
| 3467 | 28550-28552 | 0.26 | inline_safe | bracket | `t=\frac{\overline{X}-100}{S/\sqrt n}\sim t(7).` |
| 3468 | 28554-28556 | 0.36 | inline_safe | bracket | `t=\frac{99.975-100}{1.1222/\sqrt8}\approx -0.063.` |
| 3469 | 28558-28560 | 0.32 | inline_safe | bracket | `\|t\|\ge t_{0.025}(7)\approx2.365.` |
| 3470 | 28562-28564 | 0.22 | inline_safe | bracket | `\|-0.063\|<2.365,` |
| 3471 | 28568-28570 | 0.42 | inline_safe | bracket | `\frac{(n-1)S^2}{\sigma^2}\sim\chi^2(n-1)=\chi^2(7).` |
| 3472 | 28572-28577 | 0.18 | structural | bracket | `\left( \frac{(n-1)S^2}{\chi^2_{0.05}(7)}, \frac{(n-1)S^2}{\chi^2_{0.95}(7)} \right).` |
| 3473 | 28579-28585 | 0.25 | structural | bracket | `\left( \frac{8.815}{14.067}, \frac{8.815}{2.167} \right) \approx(0.6268,\ 4.068).` |
| 3474 | 28587-28589 | 0.20 | inline_safe | bracket | `(0.627,\ 4.068).` |
| 3475 | 28594-28596 | 0.46 | inline_safe | bracket | `0.530,\ 0.542,\ 0.510,\ 0.495,\ 0.515.` |
| 3480 | 28618-28620 | 0.48 | inline_safe | bracket | `t=\frac{0.5184-0.5}{0.0182/\sqrt{5}}=\frac{0.0184}{0.00813}\approx 2.264.` |
| 3481 | 28637-28639 | 0.35 | inline_safe | bracket | `H_0\colon\theta=0.1,\quad H_1\colon\theta>0.1,` |
| 3484 | 28658-28660 | 0.12 | inline_safe | bracket | `\alpha=0.009.` |
| 3485 | 28666-28668 | 0.38 | inline_safe | bracket | `H_0\colon\mu=2\quad\text{vs}\quad H_1\colon\mu=3,` |
| 3488 | 28688-28692 | 0.19 | inline_unsafe_marker | bracket | `H_0\colon f(x)=\begin{cases}1/2, & 0\leq x\leq2,\\0, & \text{其他},\end{cases} \quad H_1\colon f(x)=\begin{cases}x/2, & 0\leq x\leq2,\\0, & \text{其他}.\end{cases}` |
| 3491 | 28736-28738 | 0.26 | inline_safe | bracket | `\alpha = P\{\text{拒绝}\,H_0 \mid H_0\text{ 为真}\}.` |
| 3492 | 28808-28810 | 0.49 | inline_safe | bracket | `A_k=\{\text{第 }k\text{ 个人抽中红球}\},\qquad k=1,2,\dots,n.` |
| 3493 | 28815-28817 | 0.42 | inline_safe | bracket | `P(A_k)=\frac{M}{N},\qquad k=1,2,\dots,n.` |
| 3494 | 28822-28824 | 0.16 | inline_safe | bracket | `P(A_1)=\frac{M}{N}.` |
| 3497 | 28835-28840 | 0.40 | display_environment | env:align* | `P(A_2) &=\frac{M-1}{N-1}\cdot\frac{M}{N}+\frac{M}{N-1}\cdot\frac{N-M}{N} \\ &=\frac{M(M-1)+M(N-M)}{N(N-1)} \\ &=\frac{M(N-1)}{N(N-1)}=\frac{M}{N}.` |
| 3498 | 28860-28862 | 0.42 | inline_safe | bracket | `A=\{\text{甲取到红球}\},\qquad B=\{\text{乙取到红球}\}.` |
| 3499 | 28865-28867 | 0.14 | inline_safe | bracket | `P(B)=\frac{5}{12}.` |
| 3500 | 28870-28872 | 0.20 | inline_safe | bracket | `P(B\|\overline A)=\frac{5}{11}.` |
| 3501 | 28875-28877 | 0.37 | inline_safe | bracket | `A\overline B\qquad\text{和}\qquad \overline A B.` |
| 3502 | 28879-28881 | 0.41 | inline_safe | bracket | `P(\text{恰有一人取到红球})=P(A\overline B)+P(\overline A B).` |
| 3503 | 28883-28886 | 0.38 | normalized_width_not_low | bracket | `P(A\overline B)=\frac{5}{12}\cdot\frac{7}{11},\qquad P(\overline A B)=\frac{7}{12}\cdot\frac{5}{11}.` |
| 3504 | 28888-28892 | 0.33 | normalized_width_not_low | bracket | `P(A\overline B)+P(\overline A B) =\frac{5}{12}\cdot\frac{7}{11}+\frac{7}{12}\cdot\frac{5}{11} =\frac{35}{66}.` |
| 3505 | 28895-28897 | 0.41 | inline_safe | bracket | `\frac{5}{12},\qquad \frac{5}{11},\qquad \frac{35}{66}.` |
| 3506 | 28906-28908 | 0.25 | inline_safe | bracket | `C_n=\{\text{至少有两个人生日相同}\}.` |
| 3507 | 28913-28915 | 0.44 | inline_safe | bracket | `P(\overline{C_n})=\frac{365\cdot364\cdots(365-n+1)}{365^n},` |
| 3508 | 28917-28919 | 0.47 | inline_safe | bracket | `P(C_n)=1-\frac{365\cdot364\cdots(365-n+1)}{365^n}.` |
| 3509 | 28929-28933 | 0.41 | normalized_width_not_low | bracket | `P(\overline{C_n}) =1\cdot\frac{364}{365}\cdot\frac{363}{365}\cdots\frac{365-n+1}{365} =\frac{365\cdot364\cdots(365-n+1)}{365^n}.` |
| 3510 | 28935-28938 | 0.39 | normalized_width_not_low | bracket | `P(C_n)=1-P(\overline{C_n}) =1-\frac{365\cdot364\cdots(365-n+1)}{365^n}.` |
| 3511 | 28945-28948 | 0.32 | normalized_width_not_low | bracket | `\prod_{k=0}^{n-1}\left(1-\frac{k}{365}\right) \approx \exp\!\left(-\frac{n(n-1)}{2\cdot365}\right)` |
| 3512 | 28950-28952 | 0.36 | inline_safe | bracket | `P(C_n)\approx 1-\exp\!\left(-\frac{n(n-1)}{730}\right).` |
| 3513 | 28964-28966 | 0.30 | inline_safe | bracket | `C=\{\text{30 名同学中至少有两人同生日}\}.` |
| 3514 | 28968-28970 | 0.30 | inline_safe | bracket | `\overline C=\{\text{30 名同学的生日两两不同}\}.` |
| 3515 | 28973-28977 | 0.37 | normalized_width_not_low | bracket | `P(\overline C) =\frac{365}{365}\cdot\frac{364}{365}\cdot\frac{363}{365}\cdots\frac{336}{365} =\frac{365\cdot364\cdots336}{365^{30}}.` |
| 3516 | 28980-28983 | 0.28 | inline_safe | bracket | `P(C)=1-P(\overline C) =1-\frac{365\cdot364\cdots336}{365^{30}}.` |
| 3517 | 28986-28988 | 0.25 | inline_safe | bracket | `1-\frac{365\cdot364\cdots336}{365^{30}}.` |
| 3518 | 29004-29008 | 0.25 | normalized_width_not_low | bracket | `p_1+p_2+0.25=1, \qquad\text{即}\qquad p_1+p_2=0.75.` |
| 3519 | 29011-29013 | 0.46 | inline_safe | bracket | `m=p_2(1+m)+p_1(2+m)+0.25\cdot3.` |
| 3520 | 29015-29017 | 0.36 | inline_safe | bracket | `7=p_2(8)+p_1(9)+\frac34.` |
| 3521 | 29019-29022 | 0.47 | normalized_width_not_low | bracket | `m=(p_1+p_2)m+p_2+2p_1+\frac34 =0.75m+p_2+2p_1+\frac34.` |
| 3522 | 29024-29026 | 0.43 | inline_safe | bracket | `7=0.75\cdot7+p_2+2p_1+\frac34,` |
| 3523 | 29028-29030 | 0.18 | inline_safe | bracket | `p_2+2p_1=1.` |
| 3524 | 29032-29037 | 0.21 | inline_unsafe_marker | bracket | `\begin{cases} p_1+p_2=0.75,\\ 2p_1+p_2=1, \end{cases}` |
| 3525 | 29039-29041 | 0.37 | inline_safe | bracket | `p_1=0.5,\qquad p_2=0.25.` |
| 3526 | 29049-29051 | 0.08 | inline_safe | bracket | `m=EX.` |
| 3528 | 29057-29059 | 0.20 | inline_safe | bracket | `m=2+\frac23m,` |
| 3529 | 29061-29063 | 0.34 | inline_safe | bracket | `\frac13m=2,\qquad m=6.` |
| 3530 | 29073-29075 | 0.43 | inline_safe | bracket | `P_i=\{\text{从本金 }i\text{ 出发，最终先达到 }N\text{ 而不是先破产的概率}\}.` |
| 3531 | 29080-29082 | 0.38 | inline_safe | bracket | `P_i=\frac{i}{N},\qquad i=0,1,\dots,N.` |
| 3535 | 29114-29116 | 0.31 | inline_safe | bracket | `P_0=0,\qquad P_N=1.` |
| 3536 | 29119-29121 | 0.43 | inline_safe | bracket | `p(P_{i+1}-P_i)=q(P_i-P_{i-1}),` |
| 3537 | 29123-29125 | 0.41 | inline_safe | bracket | `P_{i+1}-P_i=\frac{q}{p}(P_i-P_{i-1}).` |
| 3538 | 29127-29129 | 0.32 | inline_safe | bracket | `P_i=\frac{1-(q/p)^i}{1-q/p}\cdot P_1.` |
| 3540 | 29135-29137 | 0.24 | inline_safe | bracket | `P_i=\frac{1-(q/p)^i}{1-(q/p)^N}.` |
| 3541 | 29142-29144 | 0.31 | inline_safe | bracket | `P_0=0,\qquad P_N=1.` |
| 3543 | 29173-29175 | 0.25 | inline_safe | bracket | `\frac{q}{p}=\frac{3/5}{2/5}=\frac32.` |
| 3544 | 29178-29180 | 0.24 | inline_safe | bracket | `P_i=\frac{1-(q/p)^i}{1-(q/p)^N},` |
| 3545 | 29182-29184 | 0.24 | inline_safe | bracket | `P_2=\frac{1-(3/2)^2}{1-(3/2)^5}.` |
| 3546 | 29187-29189 | 0.49 | inline_safe | bracket | `1-\left(\frac32\right)^2=1-\frac94=-\frac54,` |
| 3547 | 29190-29192 | 0.45 | inline_safe | bracket | `1-\left(\frac32\right)^5=1-\frac{243}{32}=-\frac{211}{32}.` |
| 3548 | 29194-29198 | 0.21 | inline_safe | bracket | `P_2=\frac{-5/4}{-211/32} =\frac{5}{4}\cdot\frac{32}{211} =\frac{40}{211}.` |
| 3549 | 29201-29203 | 0.19 | inline_safe | bracket | `\frac{40}{211}\approx0.1896.` |
| 3551 | 29226-29228 | 0.16 | inline_safe | bracket | `M=\{\text{两人能够见面}\}` |
| 3552 | 29234-29236 | 0.26 | inline_safe | bracket | `P(M)=1-\left(1-\frac{\tau}{T}\right)^2.` |
| 3553 | 29241-29243 | 0.39 | inline_safe | bracket | `2\cdot\frac12(T-\tau)^2=(T-\tau)^2.` |
| 3554 | 29246-29249 | 0.25 | inline_safe | bracket | `P(M)=1-\frac{(T-\tau)^2}{T^2} =1-\left(1-\frac{\tau}{T}\right)^2.` |
| 3555 | 29256-29258 | 0.23 | inline_safe | bracket | `P(\text{针与平行线相交})=\frac{2l}{\pi d}.` |
| 3556 | 29270-29272 | 0.39 | inline_safe | bracket | `X=\text{甲的到达时刻},\qquad Y=\text{乙的到达时刻}.` |
| 3558 | 29279-29284 | 0.28 | normalized_width_not_low | bracket | `P(\text{见面})=1-\left(1-\frac{5}{30}\right)^2 =1-\left(\frac56\right)^2 =1-\frac{25}{36} =\frac{11}{36}.` |
| 3559 | 29289-29291 | 0.06 | inline_safe | bracket | `\frac{11}{36}.` |
| 3561 | 29319-29321 | 0.47 | inline_safe | bracket | `T_k=\text{从已经收集到 }k-1\text{ 种，到第一次收集到第 }k\text{ 种所需的次数},` |
| 3562 | 29332-29334 | 0.33 | inline_safe | bracket | `E(T_k)=\frac{1}{p_k}=\frac{n}{n-k+1}.` |
| 3563 | 29336-29341 | 0.48 | display_environment | env:align* | `E(T) &=E(T_1)+E(T_2)+\cdots+E(T_n) \\ &=\frac{n}{n}+\frac{n}{n-1}+\cdots+\frac{n}{1} \\ &=n\left(1+\frac12+\frac13+\cdots+\frac1n\right).` |
| 3564 | 29358-29360 | 0.40 | inline_safe | bracket | `T=\text{从已有 2 种开始，到集齐 5 种还需的购买次数}.` |
| 3565 | 29362-29366 | 0.34 | normalized_width_not_low | bracket | `T_3=\text{从 2 种到 3 种所需次数},\quad T_4=\text{从 3 种到 4 种所需次数},\quad T_5=\text{从 4 种到 5 种所需次数}.` |
| 3566 | 29373-29375 | 0.30 | inline_safe | bracket | `E(T_3)=\frac{1}{p_3}=\frac53.` |
| 3570 | 29392-29394 | 0.38 | inline_safe | bracket | `E(T)=\frac{10}{6}+\frac{15}{6}+\frac{30}{6}=\frac{55}{6}.` |
| 3571 | 29397-29399 | 0.14 | inline_safe | bracket | `\frac{55}{6}\approx 9.17` |
