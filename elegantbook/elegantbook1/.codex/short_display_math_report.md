# Short Display Math Audit

- total display blocks: 3578
- ratio < 0.5: 2371
- inline-safe candidates: 1586

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
| 63 | 1005-1007 | 0.40 | inline_safe | bracket | `p_1 = \frac{\mathrm{C}_{20}^{15} \cdot 40^{15} \cdot 60^{5}}{100^{20}}.` |
| 64 | 1009-1011 | 0.29 | inline_safe | bracket | `p_2 = \frac{\mathrm{C}_{40}^{15} \mathrm{C}_{60}^{5}}{\mathrm{C}_{100}^{20}}.` |
| 65 | 1013-1015 | 0.21 | inline_safe | bracket | `p_3 = \frac{40}{100} = \frac{2}{5}.` |
| 66 | 1017-1019 | 0.43 | inline_safe | bracket | `p_4 = \frac{\mathrm{C}_{40}^1 \cdot 99!}{100!} = \frac{40}{100} = \frac{2}{5}.` |
| 67 | 1048-1053 | 0.23 | normalized_width_not_low | bracket | `P(\text{花色各不相同}) =\frac{\mathrm C_4^3\cdot 13^3}{\mathrm C_{52}^{3}} =\frac{4\cdot 2197}{22100} =\frac{8788}{22100}.` |
| 68 | 1056-1061 | 0.17 | normalized_width_not_low | bracket | `P(\text{至少 2 张同花色}) =1-\frac{8788}{22100} =\frac{13312}{22100} =\frac{256}{425}.` |
| 71 | 1096-1098 | 0.23 | inline_safe | bracket | `P(A) = \frac{S_A \text{ 的几何度量}}{\Omega \text{ 的几何度量}}.` |
| 72 | 1112-1114 | 0.35 | inline_safe | bracket | `D=\{(x,y)\mid 0<x<1,\ 0<y<1\}` |
| 73 | 1118-1120 | 0.38 | inline_safe | bracket | `y=x+0.5,\qquad y=x-0.5` |
| 74 | 1124-1126 | 0.36 | inline_safe | bracket | `\frac12\cdot 0.5\cdot 0.5=\frac18.` |
| 75 | 1145-1150 | 0.16 | structural | bracket | `P\!\left(\angle AEB\ge \frac{\pi}{2}\right) =\frac{S_{\text{半圆}}}{S_{\text{矩形}}} =\frac{25\pi/2}{50} =\frac{\pi}{4}.` |
| 76 | 1160-1160 | 0.40 | inline_safe | bracket | `A = \left\{(x,y)\,\middle\|\, x+y<\frac{5}{4},\ xy>\frac{1}{4}\right\}.` |
| 78 | 1178-1178 | 0.39 | inline_safe | bracket | `P = \frac{a^2/2+\pi a^2/4}{\pi a^2/2} = \frac{1}{2}+\frac{1}{\pi}.` |
| 79 | 1188-1190 | 0.19 | inline_safe | bracket | `P(B\|A) = \frac{P(AB)}{P(A)}` |
| 82 | 1223-1225 | 0.33 | inline_safe | bracket | `P(B) = P(B\|\Omega) \xrightarrow{\Omega \to A} P(B\|A).` |
| 83 | 1227-1229 | 0.28 | inline_safe | bracket | `P(A\|B)=\frac{P(A)}{P(B)}\ge P(A),` |
| 84 | 1231-1233 | 0.38 | inline_safe | bracket | `P[(B-C)\|A] = P(B\|A) - P(BC\|A).` |
| 85 | 1245-1248 | 0.39 | normalized_width_not_low | bracket | `P(\overline A B)=P(B\mid \overline A)P(\overline A) =\frac56\left(1-\frac25\right)=\frac12.` |
| 86 | 1250-1255 | 0.14 | normalized_width_not_low | bracket | `P(\overline A\mid B) =\frac{P(\overline A B)}{P(B)} =\frac{\frac12}{\frac45} =\frac58.` |
| 87 | 1260-1262 | 0.30 | inline_safe | bracket | `P(A\mid B)+P(\overline A\mid \overline B)=1,` |
| 89 | 1275-1277 | 0.28 | inline_safe | bracket | `\frac{x}{b}+\frac{1-a-b+x}{1-b}=1.` |
| 90 | 1279-1281 | 0.44 | inline_safe | bracket | `x(1-b)+b(1-a-b+x)=b(1-b).` |
| 91 | 1283-1285 | 0.08 | inline_safe | bracket | `x=ab,` |
| 92 | 1293-1295 | 0.24 | inline_safe | bracket | `P(AB) = P(B\|A)\,P(A).` |
| 94 | 1304-1307 | 0.49 | display_environment | env:align* | `P(A_1 A_2 \cdots A_n) &= P\!\bigl[(A_1 \cdots A_{n-1}) \cdot A_n\bigr] \\ &= P(A_n \| A_1 \cdots A_{n-1}) \cdot P(A_1 \cdots A_{n-1}),` |
| 95 | 1323-1325 | 0.43 | inline_safe | bracket | `P(A) = \sum_{i=1}^{n} P(B_i)\,P(A\|B_i).` |
| 104 | 1412-1414 | 0.45 | inline_safe | bracket | `P(A-B) = P(A) - P(AB) \ge P(A) - P(B),` |
| 105 | 1430-1432 | 0.33 | inline_safe | bracket | `P(A\cup B)=P(A)+P(B)-P(AB)` |
| 108 | 1451-1453 | 0.49 | inline_safe | bracket | `P(\overline{A}\cup\overline{B})=P(\overline{AB})=1-P(AB)=1-0=1.` |
| 109 | 1466-1468 | 0.29 | inline_safe | bracket | `P(AB\mid \overline C)=\frac{P(AB\overline C)}{P(\overline C)}.` |
| 111 | 1480-1482 | 0.34 | inline_safe | bracket | `P(AB\mid \overline C)=\frac{1/2}{2/3}=\frac34.` |
| 120 | 1571-1573 | 0.47 | inline_safe | bracket | `P(A_1)=\frac{2}{12},\qquad P(\overline{A_1})=\frac{10}{12}.` |
| 121 | 1575-1577 | 0.23 | inline_safe | bracket | `P(A_2\mid A_1)=\frac{1}{11}.` |
| 122 | 1579-1581 | 0.24 | inline_safe | bracket | `P(A_2\mid \overline{A_1})=\frac{2}{11}.` |
| 123 | 1584-1589 | 0.41 | normalized_width_not_low | bracket | `P(A_2)=\frac{2}{12}\cdot\frac{1}{11}+\frac{10}{12}\cdot\frac{2}{11} =\frac{2+20}{132} =\frac{22}{132} =\frac16.` |
| 128 | 1636-1636 | 0.47 | inline_safe | bracket | `P(AB) = P(A) - P(A\overline{B}) = 0.7 - 0.5 = 0.2.` |
| 130 | 1640-1640 | 0.37 | inline_safe | bracket | `B \cap (A\cup\overline{B}) = (B\cap A)\cup(B\cap\overline{B}) = AB,` |
| 131 | 1642-1642 | 0.45 | inline_safe | bracket | `P(B\|A\cup\overline{B}) = \frac{P(AB)}{P(A\cup\overline{B})} = \frac{0.2}{0.8} = 0.25.` |
| 132 | 1657-1659 | 0.40 | inline_safe | bracket | `P(A\mid B)=\frac{P(AB)}{P(B)}=\frac{P(A)}{P(B)}\ge P(A).` |
| 133 | 1676-1678 | 0.44 | inline_safe | bracket | `A=\{\text{传送信号 }0\},\qquad B=\{\text{接收到信号 }0\}.` |
| 135 | 1684-1686 | 0.21 | inline_safe | bracket | `P(\overline B\|\overline A)=0.9,` |
| 136 | 1688-1690 | 0.30 | inline_safe | bracket | `P(B\|\overline A)=1-0.9=0.1.` |
| 137 | 1693-1701 | 0.37 | inline_unsafe_marker | bracket | `\begin{aligned} P(B) &=P(A)P(B\|A)+P(\overline A)P(B\|\overline A)\\ &=0.7\times 0.8+0.3\times 0.1\\ &=0.56+0.03\\ &=0.59. \end{aligned}` |
| 138 | 1704-1706 | 0.27 | inline_safe | bracket | `P(A\|B)=\frac{P(A)P(B\|A)}{P(B)}.` |
| 139 | 1708-1710 | 0.44 | inline_safe | bracket | `P(A\|B)=\frac{0.7\times 0.8}{0.59}=\frac{0.56}{0.59}=\frac{56}{59}.` |
| 142 | 1736-1738 | 0.44 | inline_safe | bracket | `P(AB)=P(A)P(B)=0.6\times 0.7=0.42.` |
| 143 | 1740-1748 | 0.25 | inline_unsafe_marker | bracket | `\begin{aligned} P(C) &=P(A\cup B)\\ &=P(A)+P(B)-P(AB)\\ &=0.6+0.7-0.42\\ &=0.88. \end{aligned}` |
| 144 | 1751-1753 | 0.49 | inline_safe | bracket | `P(A\|C)=\frac{P(AC)}{P(C)}=\frac{P(A)}{P(C)}=\frac{0.6}{0.88}=\frac{15}{22}.` |
| 145 | 1766-1768 | 0.49 | inline_safe | bracket | `A=\{\text{取出的球是白球}\},\qquad B=\{\text{原来那个球是白球}\}.` |
| 146 | 1770-1772 | 0.29 | inline_safe | bracket | `P(B)=P(\overline B)=\frac12.` |
| 147 | 1783-1785 | 0.48 | inline_safe | bracket | `P(B\|A)=\frac{P(B)P(A\|B)}{P(B)P(A\|B)+P(\overline B)P(A\|\overline B)}.` |
| 148 | 1787-1795 | 0.42 | inline_unsafe_marker | bracket | `\begin{aligned} P(B\|A) &=\frac{\frac12\times 1}{\frac12\times 1+\frac12\times\frac12}\\ &=\frac{\frac12}{\frac12+\frac14} =\frac{\frac12}{\frac34} =\frac23. \end{aligned}` |
| 156 | 1902-1904 | 0.38 | inline_safe | bracket | `P(B\mid \overline{A})=\frac{P(B)}{P(\overline{A})}=\frac{0.4}{0.7}=\frac{4}{7}.` |
| 157 | 1914-1918 | 0.11 | inline_safe | bracket | `A\cap\overline{A\cup B\cup C} \subset A\cap\overline A =\varnothing,` |
| 158 | 1933-1935 | 0.38 | inline_safe | bracket | `P(\overline B-\overline A)=P(\overline B)-P(\overline A).` |
| 160 | 1950-1952 | 0.35 | inline_safe | bracket | `P(B\|A_1)=\frac{\mathrm{C}_4^2}{\mathrm{C}_9^2}=\frac16.` |
| 161 | 1954-1956 | 0.45 | inline_safe | bracket | `P(B\|A_2)=P(B\|A_3)=\frac{\mathrm{C}_5^2}{\mathrm{C}_9^2}=\frac{5}{18}.` |
| 163 | 1964-1968 | 0.34 | normalized_width_not_low | bracket | `P(A_1\|B)=\frac{P(A_1)P(B\|A_1)}{P(B)} =\frac{\frac12\cdot\frac16}{\frac29} =\frac38.` |
| 164 | 1980-1982 | 0.49 | inline_safe | bracket | `P(Y=k\mid X=n) = \mathrm{C}_n^k\,p^k\,(1-p)^{n-k}.` |
| 166 | 2008-2008 | 0.33 | inline_safe | bracket | `E(X\|A) = \frac{1+5+10}{3} = \frac{16}{3}.` |
| 167 | 2010-2010 | 0.28 | inline_safe | bracket | `E(X\|B) = \frac{2+5+8}{3} = 5.` |
| 169 | 2019-2019 | 0.24 | inline_safe | bracket | `P(E_1) = \frac{m+2}{3(n+2)}.` |
| 170 | 2021-2021 | 0.24 | inline_safe | bracket | `P(E_2) = \frac{m+2}{3(n+2)}.` |
| 171 | 2028-2028 | 0.18 | inline_safe | bracket | `P(E_1\|E) = \frac{1}{3}.` |
| 172 | 2030-2030 | 0.48 | inline_safe | bracket | `\frac{m+2}{3(n+2)} = \frac{1}{3} \implies m+2 = n+2 \implies m = n,` |
| 174 | 2043-2045 | 0.44 | inline_safe | bracket | `P(E_1 E_2) = \frac{(n+2)^2 - \sum s_i^2}{9(n+1)(n+2)}.` |
| 175 | 2047-2049 | 0.33 | inline_safe | bracket | `\frac{(n+2)^2 - \sum s_i^2}{(n+1)(n+2)} = 1,` |
| 176 | 2053-2058 | 0.22 | inline_unsafe_marker | bracket | `\begin{cases} \displaystyle\sum s_i = n+2, \\[6pt] \displaystyle\sum s_i^2 = n+2. \end{cases}` |
| 177 | 2071-2073 | 0.22 | inline_safe | bracket | `P(AB) = P(A)\,P(B),` |
| 179 | 2086-2093 | 0.29 | inline_unsafe_marker | bracket | `\begin{cases} P(AB) = P(A)\,P(B), \\ P(AC) = P(A)\,P(C), \\ P(BC) = P(B)\,P(C), \\ P(ABC) = P(A)\,P(B)\,P(C). \end{cases}` |
| 182 | 2152-2154 | 0.27 | inline_safe | bracket | `P(ABC)=P(A)P(B)P(C).` |
| 183 | 2156-2158 | 0.27 | inline_safe | bracket | `P(A\cdot BC)=P(A)P(BC).` |
| 184 | 2160-2162 | 0.27 | inline_safe | bracket | `P(ABC)=P(A)P(B)P(C).` |
| 189 | 2223-2230 | 0.44 | inline_unsafe_marker | bracket | `\begin{aligned} P[(A\cup B)C] &= P(AC\cup BC) = P(AC)+P(BC)-P(ABC) \\ &= P(A)\,P(C)+P(B)\,P(C)-P(ABC), \\ P(A\cup B)\,P(C) &= [P(A)+P(B)-P(AB)]\,P(C) \\ &= P(A)\,P(C)+P(B)\,P(C)...` |
| 191 | 2245-2247 | 0.34 | inline_safe | bracket | `C\cap(A\cup B) = (\overline{A}\cup B)\cap(A\cup B) = B,` |
| 192 | 2249-2251 | 0.43 | inline_safe | bracket | `P(C\mid(A\cup B)) = \frac{P(B)}{P(A\cup B)} = \frac{0.4}{0.7} = \frac{4}{7}.` |
| 198 | 2352-2354 | 0.39 | inline_safe | bracket | `3p(1-p)^2 \cdot p = 3p^2(1-p)^2.` |
| 199 | 2359-2361 | 0.38 | inline_safe | bracket | `\mathrm{C}_{n-1}^{k-1}\, p^k\, (1-p)^{n-k},` |
| 203 | 2404-2406 | 0.21 | inline_safe | bracket | `B=A_1\cup A_2\cup A_3,` |
| 204 | 2407-2409 | 0.25 | inline_safe | bracket | `\overline{B}=\overline{A_1}\,\overline{A_2}\,\overline{A_3},` |
| 205 | 2413-2418 | 0.36 | normalized_width_not_low | bracket | `P(\overline{B}) =P(\overline{A_1})P(\overline{A_2})P(\overline{A_3}) =\frac45\times\frac23\times\frac34 =\frac25.` |
| 206 | 2421-2423 | 0.47 | inline_safe | bracket | `P(B)=1-P(\overline{B})=1-\frac25=\frac35.` |
| 207 | 2437-2440 | 0.21 | inline_safe | bracket | `P(A\cup B) =1-P(\overline A\,\overline B).` |
| 208 | 2442-2447 | 0.33 | normalized_width_not_low | bracket | `P(\overline A\,\overline B) =P(\overline A)P(\overline B) =\left(1-\frac12\right)\left(1-\frac13\right) =\frac13.` |
| 209 | 2449-2451 | 0.36 | inline_safe | bracket | `P(A\cup B)=1-\frac13=\frac23.` |
| 212 | 2500-2502 | 0.20 | inline_safe | bracket | `P(B\|A)=\frac{P(AB)}{P(A)}.` |
| 213 | 2504-2506 | 0.23 | inline_safe | bracket | `P(B\|A)=\frac{P(A)}{P(A)}=1.` |
| 214 | 2521-2525 | 0.25 | normalized_width_not_low | bracket | `(A\cup B)-B=(A\cup B)\overline B =A\overline B\cup B\overline B =A\overline B=A-B.` |
| 215 | 2529-2531 | 0.31 | inline_safe | bracket | `(A-B)\cup B=A\overline B\cup B=A\cup B,` |
| 216 | 2542-2544 | 0.13 | inline_safe | bracket | `\binom{10}{3}=120.` |
| 217 | 2547-2551 | 0.24 | inline_safe | bracket | `P=\frac{\binom42\binom61}{\binom{10}{3}} =\frac{6\times 6}{120} =\frac{3}{10}.` |
| 218 | 2554-2558 | 0.19 | inline_safe | bracket | `P=1-\frac{\binom63}{\binom{10}{3}} =1-\frac{20}{120} =\frac56.` |
| 219 | 2566-2569 | 0.35 | normalized_width_not_low | bracket | `A=\{\text{两颗骰子的点数之和为 }7\},\qquad B=\{\text{其中一颗为 }1\text{ 点}\}.` |
| 220 | 2571-2573 | 0.45 | inline_safe | bracket | `(1,6),(2,5),(3,4),(4,3),(5,2),(6,1),` |
| 221 | 2577-2579 | 0.15 | inline_safe | bracket | `(1,6),(6,1),` |
| 222 | 2581-2583 | 0.27 | inline_safe | bracket | `P(B\|A)=\frac{2}{6}=\frac13.` |
| 223 | 2590-2592 | 0.47 | inline_safe | bracket | `P(A)=\frac12,\qquad P(B)=\frac23,` |
| 225 | 2604-2609 | 0.38 | normalized_width_not_low | bracket | `\max\left\{0,\frac12+\frac23-1\right\} =\frac16, \qquad \min\left\{\frac12,\frac23\right\}=\frac12.` |
| 226 | 2611-2613 | 0.32 | inline_safe | bracket | `\frac16\le P(AB)\le \frac12.` |
| 227 | 2628-2630 | 0.11 | inline_safe | bracket | `5^2=25.` |
| 228 | 2632-2634 | 0.37 | inline_safe | bracket | `(1,1),(2,2),(3,3),(4,4),(5,5),` |
| 229 | 2636-2638 | 0.35 | inline_safe | bracket | `1-\frac5{25}=\frac{20}{25}=\frac45.` |
| 230 | 2653-2655 | 0.47 | inline_safe | bracket | `A=\{\text{点数之和为偶数}\},\qquad B=\{\text{点数之和为 }6\}.` |
| 231 | 2657-2659 | 0.29 | inline_safe | bracket | `\|A\|=3\times3+3\times3=18.` |
| 232 | 2661-2663 | 0.37 | inline_safe | bracket | `(1,5),(2,4),(3,3),(4,2),(5,1),` |
| 233 | 2665-2667 | 0.30 | inline_safe | bracket | `P(B\|A)=\frac{\|B\|}{\|A\|}=\frac5{18}.` |
| 234 | 2675-2678 | 0.33 | normalized_width_not_low | bracket | `P(A\cup B)=P(A)+P(B)-P(AB) =P(A)+P(B)-P(A)P(B).` |
| 236 | 2690-2694 | 0.29 | normalized_width_not_low | bracket | `P=0.7+(1-0.7)\times0.8 =0.7+0.24 =0.94.` |
| 237 | 2705-2707 | 0.13 | inline_safe | bracket | `5^4=625.` |
| 238 | 2710-2712 | 0.31 | inline_safe | bracket | `P=\frac5{625}=\frac1{125}.` |
| 239 | 2715-2717 | 0.48 | inline_safe | bracket | `\binom51\binom42A_4^2=5\times6\times12=360.` |
| 240 | 2719-2721 | 0.21 | inline_safe | bracket | `P=\frac{360}{625}=\frac{72}{125}.` |
| 242 | 2734-2736 | 0.46 | inline_safe | bracket | `P(G\|H)=0.9,\qquad P(G\|\overline H)=0.2.` |
| 243 | 2739-2742 | 0.42 | normalized_width_not_low | bracket | `P(G)=P(H)P(G\|H)+P(\overline H)P(G\|\overline H) =0.1\times0.9+0.9\times0.2=0.27.` |
| 244 | 2745-2749 | 0.26 | normalized_width_not_low | bracket | `P(H\|G)=\frac{P(H)P(G\|H)}{P(G)} =\frac{0.1\times0.9}{0.27} =\frac13.` |
| 247 | 2764-2772 | 0.45 | inline_unsafe_marker | bracket | `\begin{aligned} P((A\cup B)C) &=P(AC\cup BC)\\ &=P(AC)+P(BC)-P(ABC)\\ &=P(A)P(C)+P(B)P(C)-P(A)P(B)P(C)\\ &=\bigl[P(A)+P(B)-P(A)P(B)\bigr]P(C). \end{aligned}` |
| 249 | 2778-2780 | 0.29 | inline_safe | bracket | `P((A\cup B)C)=P(A\cup B)P(C),` |
| 250 | 2791-2793 | 0.32 | inline_safe | bracket | `AB=\varnothing,\qquad P(AB)=0.` |
| 251 | 2795-2797 | 0.40 | inline_safe | bracket | `P(B\|A)=\frac{P(AB)}{P(A)}=\frac0{P(A)}=0.` |
| 252 | 2806-2808 | 0.11 | inline_safe | bracket | `6^2=36.` |
| 253 | 2810-2812 | 0.25 | inline_safe | bracket | `(1,1),(2,2),\dots,(6,6),` |
| 254 | 2814-2816 | 0.35 | inline_safe | bracket | `1-\frac6{36}=\frac{30}{36}=\frac56.` |
| 255 | 2824-2827 | 0.33 | normalized_width_not_low | bracket | `P(A\cup B)=P(A)+P(B)-P(AB) =P(A)+P(B)-P(A)P(B).` |
| 256 | 2829-2831 | 0.46 | inline_safe | bracket | `P(A\cup B)=0.3+0.5-0.3\times0.5=0.65.` |
| 257 | 2841-2843 | 0.13 | inline_safe | bracket | `\binom{12}{3}=220.` |
| 258 | 2846-2848 | 0.33 | inline_safe | bracket | `\binom51\binom41\binom31=60,` |
| 259 | 2850-2852 | 0.25 | inline_safe | bracket | `P=\frac{60}{220}=\frac3{11}.` |
| 260 | 2855-2859 | 0.19 | inline_safe | bracket | `P=1-\frac{\binom73}{\binom{12}{3}} =1-\frac{35}{220} =\frac{37}{44}.` |
| 263 | 2877-2884 | 0.48 | inline_unsafe_marker | bracket | `\begin{aligned} P(D) &=P(A)P(D\|A)+P(B)P(D\|B)+P(C)P(D\|C)\\ &=0.5\times0.03+0.3\times0.04+0.2\times0.01\\ &=0.029. \end{aligned}` |
| 264 | 2888-2892 | 0.26 | normalized_width_not_low | bracket | `P(A\|D)=\frac{P(A)P(D\|A)}{P(D)} =\frac{0.5\times0.03}{0.029} =\frac{15}{29}.` |
| 266 | 2912-2914 | 0.31 | inline_safe | bracket | `P(A\|B)=\frac{P(AB)}{P(B)}=\frac{P(A)}{P(B)}.` |
| 267 | 2929-2931 | 0.09 | inline_safe | bracket | `2^3=8` |
| 268 | 2933-2935 | 0.13 | inline_safe | bracket | `\binom32=3` |
| 269 | 2937-2939 | 0.31 | inline_safe | bracket | `P(A)=\frac{\binom32}{2^3}=\frac38.` |
| 270 | 2947-2949 | 0.22 | inline_safe | bracket | `P=\frac{20}{50}=\frac25.` |
| 272 | 2970-2972 | 0.13 | inline_safe | bracket | `\binom{10}{3}=120.` |
| 273 | 2975-2977 | 0.47 | inline_safe | bracket | `P(A)=\frac{\binom42}{\binom{10}{3}}=\frac6{120}=\frac1{20}.` |
| 274 | 2980-2984 | 0.24 | normalized_width_not_low | bracket | `P(B)=1-\frac8{\binom{10}{3}} =1-\frac8{120} =\frac{14}{15}.` |
| 275 | 2992-2994 | 0.38 | inline_safe | bracket | `P(G)=0.96,\quad P(\overline G)=0.04,` |
| 276 | 2995-2997 | 0.43 | inline_safe | bracket | `P(T\|G)=0.98,\quad P(T\|\overline G)=0.05.` |
| 278 | 3003-3007 | 0.26 | normalized_width_not_low | bracket | `P(G\|T)=\frac{P(G)P(T\|G)}{P(T)} =\frac{0.96\times0.98}{0.9428} \approx0.9979.` |
| 279 | 3017-3019 | 0.24 | inline_safe | bracket | `1-(1-p)^3=\frac{37}{64}.` |
| 280 | 3021-3023 | 0.36 | inline_safe | bracket | `(1-p)^3=\frac{27}{64}=\left(\frac34\right)^3,` |
| 281 | 3025-3027 | 0.14 | inline_safe | bracket | `p=\frac14.` |
| 285 | 3047-3051 | 0.34 | normalized_width_not_low | bracket | `P(B_1\|A)=\frac{P(B_1)P(A\|B_1)}{P(A)} =\frac{0.5\times0.9}{0.83} =\frac{45}{83}\approx0.542.` |
| 286 | 3065-3067 | 0.15 | inline_safe | bracket | `A-B=A\overline B.` |
| 287 | 3069-3071 | 0.15 | inline_safe | bracket | `A=AB\cup A\overline B.` |
| 288 | 3073-3075 | 0.28 | inline_safe | bracket | `P(A)=P(AB)+P(A\overline B),` |
| 289 | 3077-3079 | 0.40 | inline_safe | bracket | `P(A-B)=P(A\overline B)=P(A)-P(AB).` |
| 290 | 3086-3089 | 0.42 | normalized_width_not_low | bracket | `P\{X\ge0,Y\ge0\}=\frac37,\qquad P\{X\ge0\}=P\{Y\ge0\}=\frac47.` |
| 291 | 3094-3096 | 0.21 | inline_safe | bracket | `\{X\ge0\}\cup\{Y\ge0\}.` |
| 292 | 3098-3105 | 0.48 | inline_unsafe_marker | bracket | `\begin{aligned} P\{\max(X,Y)\ge0\} &=P\{X\ge0\}+P\{Y\ge0\}-P\{X\ge0,Y\ge0\}\\ &=\frac47+\frac47-\frac37 =\frac57. \end{aligned}` |
| 293 | 3113-3115 | 0.07 | inline_safe | bracket | `A=B.` |
| 294 | 3125-3127 | 0.05 | inline_safe | bracket | `\binom{52}{13}` |
| 295 | 3129-3131 | 0.21 | inline_safe | bracket | `\binom{13}{5}\binom{13}{5}\binom{13}{2}\binom{13}{1}.` |
| 296 | 3133-3135 | 0.23 | inline_safe | bracket | `\frac{\binom{13}{5}\binom{13}{5}\binom{13}{2}\binom{13}{1}}{\binom{52}{13}}.` |
| 297 | 3138-3140 | 0.10 | inline_safe | bracket | `\frac14.` |
| 298 | 3145-3147 | 0.35 | inline_safe | bracket | `P(A)+P(B)+P(C)\le 2+P(D).` |
| 299 | 3151-3153 | 0.08 | inline_safe | bracket | `ABC\subset D,` |
| 300 | 3157-3159 | 0.29 | inline_safe | bracket | `P(A)+P(B)-P(AB)\le1,` |
| 301 | 3161-3163 | 0.29 | inline_safe | bracket | `P(A)+P(B)\le1+P(AB).` |
| 302 | 3165-3173 | 0.27 | inline_unsafe_marker | bracket | `\begin{aligned} P(A)+P(B)+P(C) &\le 1+P(AB)+P(C)\\ &=1+P(AB\cup C)+P(ABC)\\ &\le 2+P(ABC)\\ &\le 2+P(D). \end{aligned}` |
| 303 | 3181-3183 | 0.36 | inline_safe | bracket | `\overline X=\frac1n\sum_{i=1}^{n}X_i.` |
| 304 | 3190-3192 | 0.37 | inline_safe | bracket | `f(x)=\lambda e^{-\lambda x},\qquad x>0,` |
| 306 | 3198-3200 | 0.28 | inline_safe | bracket | `\overline X\xrightarrow{P}E(X_1)=\frac1\lambda,` |
| 308 | 3215-3218 | 0.43 | normalized_width_not_low | bracket | `\sum_{n=1}^{\infty}P\!\left\{X=(-1)^{n+1}\frac{2^n}{n}\right\} =\sum_{n=1}^{\infty}\frac1{2^n}=1,` |
| 309 | 3220-3224 | 0.34 | normalized_width_not_low | bracket | `\sum_{n=1}^{\infty} \left\|(-1)^{n+1}\frac{2^n}{n}\right\|\frac1{2^n} =\sum_{n=1}^{\infty}\frac1n=\infty.` |
| 310 | 3226-3228 | 0.38 | inline_safe | bracket | `\sum_{n=1}^{\infty}(-1)^{n+1}\frac1n,` |
| 311 | 3245-3247 | 0.29 | inline_safe | bracket | `P(\text{拒绝 }H_0\mid H_0\text{ 为假})=1-\alpha.` |
| 312 | 3254-3256 | 0.25 | inline_safe | bracket | `\alpha=P(\text{拒绝 }H_0\mid H_0\text{ 为真}).` |
| 313 | 3258-3260 | 0.19 | inline_safe | bracket | `P(\text{拒绝 }H_0\mid H_0\text{ 为假})` |
| 314 | 3266-3268 | 0.18 | inline_safe | bracket | `P(\|X-\mu\|\ge2\sigma)` |
| 315 | 3273-3275 | 0.44 | inline_safe | bracket | `P(\|X-\mu\|\ge2\sigma)\le \frac{\sigma^2}{(2\sigma)^2}=\frac14.` |
| 316 | 3277-3279 | 0.36 | inline_safe | bracket | `0\le P(\|X-\mu\|\ge2\sigma)\le \frac14.` |
| 319 | 3302-3304 | 0.47 | inline_safe | bracket | `P(\text{能击沉})=1-\frac{13}{1296}=\frac{1283}{1296}\approx0.9900.` |
| 320 | 3316-3318 | 0.06 | inline_safe | bracket | `\binom{52}{5}.` |
| 321 | 3321-3323 | 0.31 | inline_safe | bracket | `P_1=\frac{4(13-4)}{\binom{52}{5}}=\frac{36}{\binom{52}{5}}.` |
| 322 | 3326-3328 | 0.38 | inline_safe | bracket | `P_2=\frac{\binom{13}{1}\binom43\binom{12}{1}\binom42}{\binom{52}{5}}.` |
| 323 | 3331-3333 | 0.46 | inline_safe | bracket | `P_3=\frac{\binom{13}{1}\binom43\binom{12}{2}\binom41\binom41}{\binom{52}{5}}.` |
| 324 | 3343-3345 | 0.38 | inline_safe | bracket | `P(B)=0.96,\quad P(\overline B)=0.04,` |
| 325 | 3346-3348 | 0.49 | inline_safe | bracket | `P(A\|B)=0.98,\qquad P(A\|\overline B)=0.05.` |
| 327 | 3355-3359 | 0.26 | normalized_width_not_low | bracket | `P(B\|A)=\frac{P(B)P(A\|B)}{P(A)} =\frac{0.96\times0.98}{0.9428} \approx0.9979.` |
| 328 | 3362-3364 | 0.14 | inline_safe | bracket | `1-0.05^n.` |
| 329 | 3366-3368 | 0.23 | inline_safe | bracket | `1-0.05^n>0.999,` |
| 330 | 3370-3372 | 0.18 | inline_safe | bracket | `0.05^n<0.001.` |
| 332 | 3378-3380 | 0.06 | inline_safe | bracket | `n=3` |
| 334 | 3402-3404 | 0.47 | inline_safe | bracket | `P(\text{能击沉})=1-\frac{41}{1280}=\frac{1239}{1280}\approx0.9680.` |
| 335 | 3415-3417 | 0.06 | inline_safe | bracket | `\binom{52}{5}.` |
| 336 | 3420-3422 | 0.20 | inline_safe | bracket | `P_1=\frac{9\cdot4^5}{\binom{52}{5}}.` |
| 337 | 3425-3427 | 0.38 | inline_safe | bracket | `P_2=\frac{\binom{13}{2}\binom42^2\cdot 11\cdot4}{\binom{52}{5}}.` |
| 338 | 3430-3432 | 0.25 | inline_safe | bracket | `P_3=\frac{13\cdot12\cdot4}{\binom{52}{5}}.` |
| 339 | 3442-3444 | 0.43 | inline_safe | bracket | `P(B)=0.96,\qquad P(\overline B)=0.04,` |
| 340 | 3445-3447 | 0.49 | inline_safe | bracket | `P(A\|B)=0.97,\qquad P(A\|\overline B)=0.06.` |
| 342 | 3454-3458 | 0.26 | normalized_width_not_low | bracket | `P(B\|A)=\frac{P(B)P(A\|B)}{P(A)} =\frac{0.96\times0.97}{0.9336} =\frac{388}{389}\approx0.9974.` |
| 343 | 3461-3463 | 0.14 | inline_safe | bracket | `1-0.06^n.` |
| 344 | 3465-3467 | 0.23 | inline_safe | bracket | `1-0.06^n>0.999,` |
| 345 | 3469-3471 | 0.18 | inline_safe | bracket | `0.06^n<0.001.` |
| 347 | 3477-3479 | 0.06 | inline_safe | bracket | `n=3` |
| 350 | 3500-3504 | 0.42 | normalized_width_not_low | bracket | `\frac8{20}\cdot\frac12+\frac{12}{20}\cdot\frac13 =\frac15+\frac15 =\frac25.` |
| 351 | 3520-3522 | 0.11 | inline_safe | bracket | `\overline B\subset \overline A.` |
| 352 | 3525-3527 | 0.25 | inline_safe | bracket | `\overline A B=B\cap\overline A=B-A.` |
| 353 | 3529-3531 | 0.38 | inline_safe | bracket | `P(A\cup B)=P(A)+P(B)-P(A)P(B),` |
| 354 | 3533-3535 | 0.26 | inline_safe | bracket | `AB(A\overline B)=A B\overline B=\varnothing,` |
| 355 | 3541-3543 | 0.35 | inline_safe | bracket | `\max\{P(\overline A),P(\overline B)\}=\underline{\hspace{2cm}}.` |
| 356 | 3549-3551 | 0.32 | inline_safe | bracket | `AB=\varnothing,\qquad P(AB)=0.` |
| 357 | 3553-3555 | 0.21 | inline_safe | bracket | `P(AB)=P(A)P(B).` |
| 358 | 3557-3559 | 0.16 | inline_safe | bracket | `P(A)P(B)=0,` |
| 359 | 3561-3563 | 0.30 | inline_safe | bracket | `\max\{P(\overline A),P(\overline B)\}=1.` |
| 360 | 3573-3575 | 0.47 | inline_safe | bracket | `P(B_j)=\frac16,\qquad j=1,2,\dots,6.` |
| 361 | 3577-3579 | 0.27 | inline_safe | bracket | `P(A\|B_j)=\frac{\binom4j}{\binom{10}j};` |
| 363 | 3599-3605 | 0.29 | normalized_width_not_low | bracket | `P(B_3\|A) =\frac{P(B_3)P(A\|B_3)}{P(A)} =\frac{\frac16\cdot\frac{\binom43}{\binom{10}3}}{\frac2{21}} =\frac{\frac16\cdot\frac1{30}}{\frac2{21}} =\frac7{120}.` |
| 364 | 3615-3617 | 0.09 | inline_safe | bracket | `\binom92` |
| 365 | 3619-3621 | 0.21 | inline_safe | bracket | `\binom11\binom81=8` |
| 366 | 3623-3627 | 0.24 | inline_safe | bracket | `P=\frac{\binom11\binom81}{\binom92} =\frac8{36} =\frac29.` |
| 367 | 3637-3639 | 0.43 | inline_safe | bracket | `P(A)=0.45,\qquad P(\overline A)=0.55,` |
| 368 | 3640-3642 | 0.49 | inline_safe | bracket | `P(B\|A)=0.90,\qquad P(B\|\overline A)=0.05.` |
| 369 | 3645-3652 | 0.37 | inline_unsafe_marker | bracket | `\begin{aligned} P(B) &=P(A)P(B\|A)+P(\overline A)P(B\|\overline A)\\ &=0.45\times0.90+0.55\times0.05\\ &=0.4325. \end{aligned}` |
| 370 | 3655-3659 | 0.26 | normalized_width_not_low | bracket | `P(A\|B)=\frac{P(A)P(B\|A)}{P(B)} =\frac{0.45\times0.90}{0.4325} \approx0.9364.` |
| 371 | 3667-3669 | 0.37 | inline_safe | bracket | `0.95\times0.90\times0.75=0.64125.` |
| 372 | 3671-3673 | 0.32 | inline_safe | bracket | `0.64125\times0.9=0.577125.` |
| 373 | 3676-3678 | 0.21 | inline_safe | bracket | `0.9\times0.9=0.81.` |
| 374 | 3680-3682 | 0.24 | inline_safe | bracket | `0.81\times0.8=0.648.` |
| 375 | 3684-3686 | 0.21 | inline_safe | bracket | `0.648>0.577125,` |
| 379 | 3709-3711 | 0.28 | inline_safe | bracket | `2P(X>Y)+P(X=Y)=1.` |
| 380 | 3713-3717 | 0.37 | normalized_width_not_low | bracket | `P(X+U>Y) =\frac12\{2P(X>Y)+P(X=Y)\} =\frac12.` |
| 383 | 3734-3738 | 0.46 | normalized_width_not_low | bracket | `P(B)=\frac59\cdot0.95+\frac49\cdot0.98 =\frac{4.75+3.92}{9} =\frac{867}{900}.` |
| 384 | 3740-3743 | 0.34 | inline_safe | bracket | `P(A_1\|B)=\frac{P(A_1)P(B\|A_1)}{P(B)} =\frac{475}{867},` |
| 385 | 3744-3747 | 0.34 | inline_safe | bracket | `P(A_2\|B)=\frac{P(A_2)P(B\|A_2)}{P(B)} =\frac{392}{867}.` |
| 386 | 3765-3767 | 0.27 | inline_safe | bracket | `P=\frac{2\cdot4!}{5!}=\frac25.` |
| 387 | 3770-3772 | 0.27 | inline_safe | bracket | `P=\frac{2!\,3!}{5!}=\frac1{10}.` |
| 389 | 3781-3783 | 0.33 | inline_safe | bracket | `P=1-\frac7{10}=\frac3{10}.` |
| 390 | 3786-3788 | 0.22 | inline_safe | bracket | `P=\frac{4!}{5!}=\frac15.` |
| 393 | 3804-3808 | 0.26 | normalized_width_not_low | bracket | `P(A\|C)=\frac{P(A)P(C\|A)}{P(C)} =\frac{0.5\times0.05}{0.02625} =\frac{20}{21}.` |
| 394 | 3817-3819 | 0.15 | inline_safe | bracket | `T=a+b+c.` |
| 396 | 3827-3829 | 0.45 | inline_safe | bracket | `P(\text{第 }k\text{ 次取到红球})=E(M_{k-1})=\frac{a}{a+b+c}.` |
| 399 | 3851-3854 | 0.31 | inline_safe | bracket | `P(\overline A\,\overline B\,\overline C) =1-P(A\cup B\cup C)=\frac38.` |
| 402 | 3875-3877 | 0.46 | inline_safe | bracket | `P(\overline A\,\overline B\,\overline C)=1-\frac25=\frac35.` |
| 409 | 3919-3923 | 0.47 | normalized_width_not_low | bracket | `P(D\|B_1)=\frac4{12}=\frac13,\qquad P(D\|B_2)=\frac6{16}=\frac38,\qquad P(D\|B_3)=\frac8{24}=\frac13.` |
| 412 | 3935-3937 | 0.45 | inline_safe | bracket | `P(B_3\|D)=\frac{\frac12\cdot\frac13}{11/32}=\frac{16}{33}.` |
| 417 | 3963-3965 | 0.49 | inline_safe | bracket | `P(B_3\|D)=\frac{\frac13\cdot\frac14}{1/3}=\frac14.` |
| 418 | 3978-3980 | 0.13 | inline_safe | bracket | `P=\frac{\binom{51}{5}}{\binom{52}{6}}.` |
| 419 | 3983-3985 | 0.20 | inline_safe | bracket | `P=\frac{\binom{51}{5}-\binom{47}{5}}{\binom{52}{6}}.` |
| 420 | 3988-3990 | 0.09 | inline_safe | bracket | `\binom{13}{n}4^n` |
| 421 | 3992-3994 | 0.17 | inline_safe | bracket | `1-\frac{\binom{13}{n}4^n}{\binom{52}{n}}.` |
| 422 | 3996-3998 | 0.28 | inline_safe | bracket | `1-\frac{\binom{13}{n}4^n}{\binom{52}{n}}>\frac12.` |
| 424 | 4013-4021 | 0.37 | inline_unsafe_marker | bracket | `\begin{aligned} P(B) &=P(A)P(B\|A)+P(\overline A)P(B\|\overline A)\\ &=\frac{13}{25}\cdot\frac{\binom{12}{2}}{\binom{24}{2}} +\frac{12}{25}\cdot\frac{\binom{13}{2}}{\binom{24}{2}}...` |
| 425 | 4024-4029 | 0.21 | normalized_width_not_low | bracket | `P(A\|B) =\frac{P(A)P(B\|A)}{P(B)} =\frac{\frac{13}{25}\cdot\frac{\binom{12}{2}}{\binom{24}{2}}}{13/50} =\frac{11}{23}.` |
| 426 | 4035-4041 | 0.13 | inline_unsafe_marker | bracket | `f(x)= \begin{cases} ax^2, & 0\le x\le1,\\ 0, & \text{其他}, \end{cases}` |
| 427 | 4048-4050 | 0.27 | inline_safe | bracket | `\int_0^1 ax^2\,\mathrm dx=1,` |
| 428 | 4054-4057 | 0.32 | normalized_width_not_low | bracket | `P(A)=\int_{1/2}^{1}3x^2\,\mathrm dx =1-\frac18=\frac78.` |
| 429 | 4059-4061 | 0.21 | inline_safe | bracket | `P(\overline B)=\frac18.` |
| 430 | 4063-4068 | 0.36 | normalized_width_not_low | bracket | `P(A\cup\overline B) =P(A)+P(\overline B)-P(A)P(\overline B) =\frac78+\frac18-\frac7{64} =\frac{57}{64}.` |
| 431 | 4081-4083 | 0.13 | inline_safe | bracket | `P=\frac{\binom{51}{4}}{\binom{52}{5}}.` |
| 432 | 4086-4090 | 0.24 | normalized_width_not_low | bracket | `P(A)=P(B)=\frac{\binom{51}{4}}{\binom{52}{5}}, \qquad P(AB)=\frac{\binom{50}{3}}{\binom{52}{5}}.` |
| 433 | 4092-4095 | 0.20 | inline_safe | bracket | `P(A\cup B) =\frac{2\binom{51}{4}-\binom{50}{3}}{\binom{52}{5}}.` |
| 434 | 4098-4101 | 0.20 | inline_safe | bracket | `P(\text{至少有一个对子}) =1-\frac{\binom{13}{5}4^5}{\binom{52}{5}}.` |
| 436 | 4115-4117 | 0.43 | inline_safe | bracket | `P(A)=\frac{16}{33},\qquad P(\overline A)=\frac{17}{33}.` |
| 437 | 4120-4128 | 0.37 | inline_unsafe_marker | bracket | `\begin{aligned} P(B) &=P(A)P(B\|A)+P(\overline A)P(B\|\overline A)\\ &=\frac{16}{33}\cdot\frac{\binom{15}{2}}{\binom{32}{2}} +\frac{17}{33}\cdot\frac{\binom{16}{2}}{\binom{32}{2}}...` |
| 438 | 4131-4136 | 0.21 | normalized_width_not_low | bracket | `P(A\|B) =\frac{P(A)P(B\|A)}{P(B)} =\frac{\frac{16}{33}\cdot\frac{\binom{15}{2}}{\binom{32}{2}}}{5/22} =\frac{14}{31}.` |
| 439 | 4144-4146 | 0.10 | inline_safe | bracket | `n-r-1` |
| 441 | 4154-4159 | 0.29 | normalized_width_not_low | bracket | `P_2 =\frac{\binom{n-2}{r}r!(n-r-2)!}{(n-1)!} =\frac{(n-2)!}{(n-1)!} =\frac1{n-1}.` |
| 445 | 4182-4187 | 0.24 | normalized_width_not_low | bracket | `P(A_2\|B) =\frac{P(A_2)P(B\|A_2)}{P(B)} =\frac{0.35\cdot0.02}{0.0185} =\frac{14}{37}\approx0.378.` |
| 446 | 4197-4200 | 0.35 | normalized_width_not_low | bracket | `A_1=\{\text{乙第一次投中}\},\qquad B_i=\{\text{甲第 }i\text{ 次投中}\},\quad i=1,2.` |
| 447 | 4202-4204 | 0.46 | inline_safe | bracket | `P(B_1)=0.7,\qquad P(\overline B_1)=0.3.` |
| 450 | 4233-4235 | 0.45 | inline_safe | bracket | `A_1=\{\text{笔试及格}\},\qquad A_2=\{\text{口试及格}\}.` |
| 452 | 4242-4250 | 0.35 | inline_unsafe_marker | bracket | `\begin{aligned} P(A_1\cup A_2) &=P(A_1)+P(\overline A_1A_2)\\ &=p+P(A_2\mid \overline A_1)P(\overline A_1)\\ &=p+\frac p2(1-p) =\frac32p-\frac12p^2. \end{aligned}` |
| 453 | 4252-4255 | 0.18 | inline_safe | bracket | `P(A_1\mid A_2) =\frac{P(A_1A_2)}{P(A_2)}.` |
| 454 | 4257-4259 | 0.45 | inline_safe | bracket | `P(A_1A_2)=P(A_2\mid A_1)P(A_1)=p^2,` |
| 456 | 4264-4268 | 0.17 | inline_safe | bracket | `P(A_1\mid A_2) =\frac{p^2}{p(1+p)/2} =\frac{2p}{1+p}.` |
| 457 | 4280-4282 | 0.26 | inline_safe | bracket | `P_1=\frac{8\cdot7}{10\cdot9}=\frac{28}{45}.` |
| 458 | 4285-4287 | 0.30 | inline_safe | bracket | `P_2=\frac{8\cdot2\cdot2}{10\cdot9}=\frac{16}{45}.` |
| 459 | 4297-4300 | 0.48 | normalized_width_not_low | bracket | `A_i=\{\text{第 }i\text{ 次取到红球}\},\quad i=1,2,\qquad B_j=\{\text{取到第 }j\text{ 箱}\},\quad j=1,2.` |
| 463 | 4316-4320 | 0.31 | normalized_width_not_low | bracket | `P(A_2\mid A_1)=\frac{P(A_1A_2)}{P(A_1)} =\frac{19/60}{19/30} =\frac12.` |
| 466 | 4344-4349 | 0.24 | normalized_width_not_low | bracket | `P(A_1\mid B) =\frac{P(A_1)P(B\mid A_1)}{P(B)} =\frac{0.25\cdot0.05}{0.0345} =\frac{25}{69}\approx0.36.` |
| 467 | 4362-4364 | 0.31 | inline_safe | bracket | `P_1=\frac{\binom54 2^4}{\binom{10}{4}}=\frac{8}{21}.` |
| 468 | 4367-4369 | 0.43 | inline_safe | bracket | `P_2=\frac{\binom51\binom42 2^2}{\binom{10}{4}}=\frac47.` |
| 469 | 4372-4374 | 0.32 | inline_safe | bracket | `P_3=\frac{\binom52}{\binom{10}{4}}=\frac1{21}.` |
| 472 | 4392-4396 | 0.45 | normalized_width_not_low | bracket | `P(A\|B_0)=1,\qquad P(A\|B_1)=\frac{\binom{19}{4}}{\binom{20}{4}}=\frac45,\qquad P(A\|B_2)=\frac{\binom{18}{4}}{\binom{20}{4}}=\frac{12}{19}.` |
| 474 | 4403-4408 | 0.24 | normalized_width_not_low | bracket | `P(B_0\|A) =\frac{P(B_0)P(A\|B_0)}{P(A)} =\frac{0.8}{448/475} =\frac{95}{112}\approx0.848.` |
| 475 | 4413-4422 | 0.09 | inline_unsafe_marker | bracket | `\begin{array}{c\|cccc} & Y=-1 & Y=0 & Y=1 & Y=2\\ \hline X=-2 & a & 0 & 0 & 0\\ X=-1 & 0.14 & b & 0 & 0\\ X=0 & 0.01 & 0.02 & 0.03 & 0\\ X=1 & 0.12 & 0.13 & 0.14 & 0.15 \end{array}` |
| 477 | 4434-4436 | 0.15 | inline_safe | bracket | `a+b=0.26.` |
| 479 | 4448-4450 | 0.17 | inline_safe | bracket | `4a+b=0.80.` |
| 480 | 4452-4454 | 0.43 | inline_safe | bracket | `a+b=0.26,\qquad 4a+b=0.80,` |
| 481 | 4456-4458 | 0.33 | inline_safe | bracket | `a=0.18,\qquad b=0.08.` |
| 483 | 4465-4474 | 0.17 | inline_unsafe_marker | bracket | `F_X(x)= \begin{cases} 0, & x<-2,\\ 0.18, & -2\le x<-1,\\ 0.40, & -1\le x<0,\\ 0.46, & 0\le x<1,\\ 1, & x\ge1. \end{cases}` |
| 485 | 4492-4494 | 0.30 | inline_safe | bracket | `\frac{\hat p-p}{\sqrt{p(1-p)/n}}\approx N(0,1).` |
| 486 | 4496-4498 | 0.29 | inline_safe | bracket | `P(\|\hat p-p\|<0.1)>0.99.` |
| 487 | 4500-4502 | 0.35 | inline_safe | bracket | `2\Phi\!\left(\frac{0.1}{\sqrt{p(1-p)/n}}\right)-1>0.99.` |
| 488 | 4504-4506 | 0.29 | inline_safe | bracket | `\frac{0.1}{\sqrt{p(1-p)/n}}\ge 2.575.` |
| 489 | 4508-4510 | 0.30 | inline_safe | bracket | `n\ge \frac{(2.575)^2}{0.1^2}p(1-p).` |
| 490 | 4512-4514 | 0.32 | inline_safe | bracket | `n\ge \frac{(2.575)^2}{0.04}\approx165.77.` |
| 491 | 4516-4518 | 0.10 | inline_safe | bracket | `n=166.` |
| 492 | 4523-4525 | 0.21 | inline_safe | bracket | `\frac{x^2}{a^2}+\frac{y^2}{b^2}\le1` |
| 493 | 4533-4539 | 0.22 | inline_unsafe_marker | bracket | `f(x,y)= \begin{cases} \dfrac1{\pi ab}, & \dfrac{x^2}{a^2}+\dfrac{y^2}{b^2}\le1,\\[6pt] 0, & \text{其他}. \end{cases}` |
| 495 | 4546-4552 | 0.25 | inline_unsafe_marker | bracket | `f_X(x)= \begin{cases} \dfrac2{\pi a}\sqrt{1-\dfrac{x^2}{a^2}}, & \|x\|\le a,\\[6pt] 0, & \text{其他}. \end{cases}` |
| 496 | 4554-4560 | 0.25 | inline_unsafe_marker | bracket | `f_Y(y)= \begin{cases} \dfrac2{\pi b}\sqrt{1-\dfrac{y^2}{b^2}}, & \|y\|\le b,\\[6pt] 0, & \text{其他}. \end{cases}` |
| 497 | 4563-4565 | 0.38 | inline_safe | bracket | `DX=\frac{a^2}{4},\qquad DY=\frac{b^2}{4}.` |
| 498 | 4567-4569 | 0.27 | inline_safe | bracket | `a=12,\qquad b=8.` |
| 500 | 4580-4586 | 0.11 | inline_unsafe_marker | bracket | `f(x,y)= \begin{cases} 2, & (x,y)\in G,\\ 0, & \text{其他}. \end{cases}` |
| 502 | 4598-4604 | 0.11 | inline_unsafe_marker | bracket | `f_X(x)= \begin{cases} 2x, & 0<x<1,\\ 0, & \text{其他}. \end{cases}` |
| 503 | 4607-4609 | 0.45 | inline_safe | bracket | `EX=EY=\int_0^1 2x^2\,\mathrm dx=\frac23,` |
| 504 | 4611-4615 | 0.49 | normalized_width_not_low | bracket | `E(XY)=\int_0^1\int_{1-x}^{1}2xy\,\mathrm dy\,\mathrm dx =\int_0^1 x\bigl[1-(1-x)^2\bigr]\,\mathrm dx =\int_0^1(2x^2-x^3)\,\mathrm dx=\frac5{12}.` |
| 505 | 4617-4620 | 0.41 | normalized_width_not_low | bracket | `\operatorname{Cov}(X,Y)=E(XY)-EX\,EY =\frac5{12}-\frac49=-\frac1{36}.` |
| 507 | 4629-4633 | 0.41 | normalized_width_not_low | bracket | `DU=D(X+Y)=DX+DY+2\operatorname{Cov}(X,Y) =\frac1{18}+\frac1{18}-\frac1{18} =\frac1{18}.` |
| 508 | 4638-4644 | 0.21 | inline_unsafe_marker | bracket | `f(x,y)= \begin{cases} Axy, & 0<x<2,\ 0<y<2,\\ 0, & \text{其他}. \end{cases}` |
| 509 | 4653-4657 | 0.43 | normalized_width_not_low | bracket | `1=\int_0^2\int_0^2 Axy\,\mathrm dy\,\mathrm dx =A\left(\int_0^2 x\,\mathrm dx\right)\left(\int_0^2 y\,\mathrm dy\right) =4A.` |
| 513 | 4681-4683 | 0.38 | inline_safe | bracket | `E(e^{tX+sY})=E(e^{tX})E(e^{sY}).` |
| 514 | 4685-4688 | 0.37 | normalized_width_not_low | bracket | `E(e^{tX})=\int_0^2 \frac{x}{2}e^{tx}\,\mathrm dx =\frac{e^{2t}(2t-1)+1}{2t^2},` |
| 515 | 4690-4692 | 0.35 | inline_safe | bracket | `E(e^{sY})=\frac{e^{2s}(2s-1)+1}{2s^2}.` |
| 518 | 4706-4708 | 0.36 | inline_safe | bracket | `DX=2-\left(\frac43\right)^2=\frac29.` |
| 519 | 4710-4712 | 0.16 | inline_safe | bracket | `\operatorname{Cov}(X,Y)=0.` |
| 522 | 4732-4734 | 0.19 | inline_safe | bracket | `EN=\frac{p}{1-p}=1.` |
| 524 | 4741-4743 | 0.23 | inline_safe | bracket | `E=475+\frac12E.` |
| 525 | 4745-4747 | 0.10 | inline_safe | bracket | `E=950.` |
| 526 | 4759-4761 | 0.18 | inline_safe | bracket | `P(A)=\frac mn.` |
| 529 | 4800-4803 | 0.15 | inline_safe | bracket | `\frac{5}{100}\cdot\frac{95}{99} =\frac{19}{396}.` |
| 530 | 4806-4810 | 0.37 | normalized_width_not_low | bracket | `P(D_1G_2)=P(D_1)P(G_2\|D_1) =0.05\cdot\frac{95}{99} =\frac{19}{396}.` |
| 531 | 4822-4824 | 0.26 | inline_safe | bracket | `0\le P(AB)\le P(A)=0,` |
| 532 | 4826-4828 | 0.29 | inline_safe | bracket | `P(A)P(B)=0\cdot P(B)=0,` |
| 533 | 4830-4832 | 0.21 | inline_safe | bracket | `P(AB)=P(A)P(B),` |
| 535 | 4842-4844 | 0.15 | inline_safe | bracket | `P(A\mid \overline A\cup B).` |
| 536 | 4848-4850 | 0.27 | inline_safe | bracket | `P(B)=0.7-0.3=0.4.` |
| 538 | 4856-4858 | 0.43 | inline_safe | bracket | `P(\overline A\cup B)=P(\overline A)+P(B)-P(\overline A B).` |
| 540 | 4864-4866 | 0.39 | inline_safe | bracket | `P(\overline A\cup B)=0.3+0.4-0.1=0.6.` |
| 541 | 4868-4870 | 0.18 | inline_safe | bracket | `A(\overline A\cup B)=AB,` |
| 542 | 4872-4876 | 0.30 | inline_safe | bracket | `P(A\mid \overline A\cup B)=\frac{P(AB)}{P(\overline A\cup B)} =\frac{0.3}{0.6} =0.5.` |
| 543 | 4886-4890 | 0.23 | normalized_width_not_low | bracket | `A_1=\{\text{甲不及格}\},\quad A_2=\{\text{乙不及格}\},\quad A_3=\{\text{丙不及格}\}.` |
| 546 | 4901-4910 | 0.25 | inline_unsafe_marker | bracket | `\begin{aligned} P(E) &=0.4\cdot0.3\cdot0.5 +0.4\cdot0.7\cdot0.5 +0.6\cdot0.3\cdot0.5\\ &=0.06+0.14+0.09 =0.29. \end{aligned}` |
| 547 | 4913-4915 | 0.34 | inline_safe | bracket | `A_1A_2\overline A_3\cup \overline A_1A_2A_3.` |
| 548 | 4917-4921 | 0.43 | normalized_width_not_low | bracket | `\frac{0.4\cdot0.3\cdot0.5+0.6\cdot0.3\cdot0.5}{0.29} =\frac{0.15}{0.29} =\frac{15}{29}.` |
| 549 | 4926-4928 | 0.15 | inline_safe | bracket | `P(A\mid A\cup \overline B).` |
| 550 | 4932-4934 | 0.26 | inline_safe | bracket | `P(AB)=1-0.8=0.2.` |
| 551 | 4936-4938 | 0.49 | inline_safe | bracket | `P(A\overline B)=P(A)-P(AB)=0.7-0.2=0.5.` |
| 552 | 4940-4943 | 0.42 | normalized_width_not_low | bracket | `P(A\cup\overline B)=P(A)+P(\overline B)-P(A\overline B) =0.7+0.6-0.5=0.8.` |
| 553 | 4945-4950 | 0.16 | normalized_width_not_low | bracket | `P(A\mid A\cup\overline B) =\frac{P(A)}{P(A\cup\overline B)} =\frac{0.7}{0.8} =\frac78.` |
| 554 | 4960-4962 | 0.40 | inline_safe | bracket | `P=\frac4{10}\cdot\frac69=\frac4{15}.` |
| 555 | 4965-4967 | 0.41 | inline_safe | bracket | `P(B)=\frac{\binom62}{\binom{10}2}=\frac{15}{45}=\frac13.` |
| 556 | 4969-4974 | 0.25 | normalized_width_not_low | bracket | `P(A)=1-P(\text{两次都是旧球}) =1-\frac{\binom42}{\binom{10}2} =1-\frac6{45} =\frac{13}{15}.` |
| 557 | 4976-4980 | 0.18 | inline_safe | bracket | `P(B\|A)=\frac{P(B)}{P(A)} =\frac{1/3}{13/15} =\frac5{13}.` |
| 558 | 4990-4992 | 0.14 | inline_safe | bracket | `\binom72=21` |
| 559 | 4996-4998 | 0.22 | inline_safe | bracket | `7-(k+1)=6-k.` |
| 561 | 5004-5009 | 0.11 | inline_unsafe_marker | bracket | `\begin{array}{c\|cccccc} k&0&1&2&3&4&5\\ \hline P(K=k)&\dfrac6{21}&\dfrac5{21}&\dfrac4{21}&\dfrac3{21}&\dfrac2{21}&\dfrac1{21} \end{array}` |
| 563 | 5017-5019 | 0.38 | inline_safe | bracket | `P(K\ge2)=\frac{4+3+2+1}{21}=\frac{10}{21}.` |
| 564 | 5025-5027 | 0.27 | inline_safe | bracket | `P(A)=P(B)=P(C)=\rho.` |
| 565 | 5032-5035 | 0.39 | normalized_width_not_low | bracket | `P(AB)=P(A)P(B)=\rho^2,\qquad P(AC)=P(A)P(C)=\rho^2.` |
| 566 | 5037-5039 | 0.11 | inline_safe | bracket | `AB\cup AC\subset A.` |
| 567 | 5041-5043 | 0.40 | inline_safe | bracket | `P(AB)+P(AC)=P(AB\cup AC)\le P(A),` |
| 568 | 5045-5047 | 0.12 | inline_safe | bracket | `2\rho^2\le \rho.` |
| 569 | 5049-5051 | 0.15 | inline_safe | bracket | `\rho\le \frac12.` |
| 570 | 5055-5057 | 0.17 | inline_safe | bracket | `\Omega=\{1,2,3,4\},` |
| 572 | 5063-5065 | 0.43 | inline_safe | bracket | `P(AB)=P(\{1\})=\frac14=P(A)P(B),` |
| 573 | 5066-5068 | 0.43 | inline_safe | bracket | `P(AC)=P(\{2\})=\frac14=P(A)P(C),` |
| 574 | 5069-5071 | 0.43 | inline_safe | bracket | `P(BC)=P(\{3\})=\frac14=P(B)P(C),` |
| 575 | 5073-5075 | 0.20 | inline_safe | bracket | `\rho_{\max}=\frac12.` |
| 577 | 5157-5159 | 0.23 | inline_safe | bracket | `\{\omega \mid X(\omega) \le x,\ \omega \in \Omega\}` |
| 578 | 5183-5185 | 0.41 | inline_safe | bracket | `F(x) = P\{X \le x\} \quad (-\infty < x < +\infty)` |
| 580 | 5248-5254 | 0.13 | inline_unsafe_marker | bracket | `F(x) = \begin{cases} 0, & x < 0, \\ \dfrac{1}{2}, & 0 \le x < 1, \\ 1 - e^{-x}, & x \ge 1. \end{cases}` |
| 581 | 5299-5304 | 0.14 | inline_unsafe_marker | bracket | `F(x) = \begin{cases} a + b e^{-x}, & x > 0, \\ 0, & x \le 0. \end{cases}` |
| 583 | 5316-5318 | 0.44 | inline_safe | bracket | `F(0) = \lim_{x \to 0^+} F(x) = a + b = 0,` |
| 584 | 5320-5325 | 0.13 | inline_unsafe_marker | bracket | `F(x) = \begin{cases} 1 - e^{-x}, & x > 0, \\ 0, & x \le 0. \end{cases}` |
| 586 | 5336-5338 | 0.38 | inline_safe | bracket | `P\{X = x_i\} = p_i, \quad i = 1, 2, \dots` |
| 587 | 5343-5349 | 0.08 | inline_unsafe_marker | bracket | `\begin{array}{c\|cccc} X & x_1 & x_2 & \cdots \\ \hline P & p_1 & p_2 & \cdots \end{array}` |
| 588 | 5380-5382 | 0.44 | inline_safe | bracket | `F(x) = \int_{-\infty}^{x} f(t)\,\mathrm{d}t \quad (x \in \mathbf{R}),` |
| 590 | 5404-5409 | 0.16 | inline_unsafe_marker | bracket | `f(x) = \begin{cases} 0, & x \text{ 为 } F(x) \text{ 的不可导点}, \\ F'(x), & x \text{ 为 } F(x) \text{ 的可导点}. \end{cases}` |
| 591 | 5422-5428 | 0.11 | inline_unsafe_marker | bracket | `F(x) = \begin{cases} 0, & x < 0, \\ \dfrac{x^3}{2}, & 0 \le x < 1, \\ 1, & x \ge 1, \end{cases}` |
| 592 | 5454-5460 | 0.15 | inline_unsafe_marker | bracket | `F(x) = \begin{cases} 0, & x < 0, \\ Ax^2 + \dfrac{2}{3}x, & 0 \le x < 1, \\ 1, & x \ge 1. \end{cases}` |
| 594 | 5470-5472 | 0.46 | inline_safe | bracket | `f(x) = F'(x) = \frac{2x}{3} + \frac{2}{3}, \quad x \in [0,1),` |
| 595 | 5474-5479 | 0.13 | inline_unsafe_marker | bracket | `f(x) = \begin{cases} \dfrac{2x}{3} + \dfrac{2}{3}, & 0 \le x < 1, \\ 0, & \text{其他}. \end{cases}` |
| 597 | 5487-5493 | 0.11 | inline_unsafe_marker | bracket | `\begin{array}{c\|ccc} X & 1 & 2 & 3 \\ \hline P\{X=k\} & \theta^2 & 2\theta(1-\theta) & (1-\theta)^2 \end{array}` |
| 598 | 5501-5507 | 0.10 | inline_unsafe_marker | bracket | `\begin{array}{c\|ccc} X & 1 & 2 & 3 \\ \hline P\{X=k\} & \dfrac{1}{4} & \dfrac{1}{2} & \dfrac{1}{4} \end{array}` |
| 600 | 5527-5529 | 0.30 | inline_safe | bracket | `\sum_{k=1}^{\infty}P\{X=k\}=1.` |
| 601 | 5536-5543 | 0.14 | inline_unsafe_marker | bracket | `F(x) = \begin{cases} 0, & x<-1, \\ 0.4, & -1 \le x<1, \\ 0.8, & 1 \le x<3, \\ 1, & x \ge 3. \end{cases}` |
| 602 | 5549-5553 | 0.45 | display_environment | env:align* | `P\{X=-1\} &= F(-1) - F(-1^-) = 0.4 - 0 = 0.4, \\ P\{X=1\} &= F(1) - F(1^-) = 0.8 - 0.4 = 0.4, \\ P\{X=3\} &= F(3) - F(3^-) = 1 - 0.8 = 0.2.` |
| 603 | 5555-5561 | 0.07 | inline_unsafe_marker | bracket | `\begin{array}{c\|ccc} X & -1 & 1 & 3 \\ \hline P & 0.4 & 0.4 & 0.2 \end{array}` |
| 605 | 5597-5599 | 0.38 | inline_safe | bracket | `F'(x)=F(x),\qquad F(0)=1.` |
| 607 | 5606-5608 | 0.27 | inline_unsafe_marker | bracket | `F(x) = \begin{cases} e^x, & x < 0, \\ 1, & x \ge 0, \end{cases} \quad f(x) = \begin{cases} e^x, & x \le 0, \\ 0, & x > 0. \end{cases}` |
| 608 | 5611-5617 | 0.08 | inline_unsafe_marker | bracket | `f(x)= \begin{cases} e^x,&x\le 0,\\ 0,&x>0. \end{cases}` |
| 609 | 5626-5631 | 0.16 | inline_unsafe_marker | bracket | `f(x) = \begin{cases} 2\left(1 - \dfrac{1}{x^2}\right), & 1 \le x \le 2, \\ 0, & \text{其他}. \end{cases}` |
| 611 | 5646-5652 | 0.17 | inline_unsafe_marker | bracket | `F(x) = \begin{cases} 0, & x < 1, \\ 2\left(x + \dfrac{1}{x} - 2\right), & 1 \le x < 2, \\ 1, & x \ge 2. \end{cases}` |
| 612 | 5657-5662 | 0.40 | display_environment | env:align* | `&\text{A. } f(x) = \begin{cases} 2(1-\|x\|), & \|x\| \le 1 \\ 0, & \|x\|>1 \end{cases} &&\text{B. } f(x) = \begin{cases} \frac{1}{\sqrt{2\pi}\sigma} e^{-\frac{(x-\mu)^2}{2\sigma^2}}, ...` |
| 613 | 5679-5681 | 0.15 | inline_unsafe_marker | bracket | `f(x) = \begin{cases} A\sin x, & 0 \le x \le \pi \\ 0, & \text{其他} \end{cases}` |
| 616 | 5694-5700 | 0.16 | inline_unsafe_marker | bracket | `F(x) = \begin{cases} 0, & x<0, \\[6pt] \dfrac{1}{2}(1-\cos x), & 0 \le x < \pi, \\[6pt] 1, & x \ge \pi. \end{cases}` |
| 618 | 5738-5740 | 0.48 | inline_safe | bracket | `\int_{-\infty}^{+\infty}\bigl(f_1(x)+f_2(x)\bigr)\,\mathrm dx=2,` |
| 619 | 5744-5746 | 0.45 | inline_safe | bracket | `\lim_{x\to+\infty}\bigl(F_1(x)+F_2(x)\bigr)=2\ne1.` |
| 620 | 5748-5750 | 0.24 | inline_safe | bracket | `F(x)=F_1(x)F_2(x)` |
| 623 | 5794-5801 | 0.11 | inline_unsafe_marker | bracket | `F(x)= \begin{cases} 0, & x<0, \\[6pt] 1-p, & 0\leqslant x<1, \\[6pt] 1, & x\geqslant1. \end{cases}` |
| 625 | 5838-5840 | 0.28 | inline_safe | bracket | `P(X\geqslant1)=1-P(X=0),` |
| 627 | 5848-5856 | 0.46 | inline_unsafe_marker | bracket | `\begin{aligned} P(Y\geqslant1) &=1-P(Y=0)=1-\mathrm{C}_4^0p^0(1-p)^4\\ &=1-\left(\frac{2}{3}\right)^4\\ &=1-\frac{16}{81} =\frac{65}{81}. \end{aligned}` |
| 628 | 5867-5869 | 0.19 | inline_safe | bracket | `DX=10p(1-p).` |
| 629 | 5871-5873 | 0.25 | inline_safe | bracket | `10p(1-p)=\frac52,` |
| 630 | 5875-5877 | 0.22 | inline_safe | bracket | `p(1-p)=\frac14.` |
| 631 | 5879-5881 | 0.23 | inline_safe | bracket | `\left(p-\frac12\right)^2=0,` |
| 632 | 5883-5885 | 0.14 | inline_safe | bracket | `p=\frac12.` |
| 633 | 5890-5892 | 0.31 | inline_safe | bracket | `EX=15,\qquad DX=10,` |
| 634 | 5897-5899 | 0.39 | inline_safe | bracket | `EX=np,\qquad DX=np(1-p).` |
| 635 | 5901-5903 | 0.26 | inline_safe | bracket | `1-p=\frac{10}{15}=\frac23,` |
| 636 | 5905-5907 | 0.18 | inline_safe | bracket | `n=\frac{15}{1/3}=45.` |
| 639 | 5927-5933 | 0.17 | inline_unsafe_marker | bracket | `f(x)= \begin{cases} ax^2+bx+c, & 0<x<1,\\ 0, & \text{其他}, \end{cases}` |
| 640 | 5938-5940 | 0.39 | inline_safe | bracket | `\int_0^1(ax^2+bx+c)\,\mathrm dx=1,` |
| 641 | 5942-5944 | 0.35 | inline_unsafe_marker | bracket | `\frac13a+\frac12b+c=1. \tag{1}` |
| 642 | 5946-5948 | 0.48 | inline_safe | bracket | `\int_0^1x(ax^2+bx+c)\,\mathrm dx=\frac12,` |
| 644 | 5954-5956 | 0.43 | inline_safe | bracket | `EX^2=\frac3{20}+\frac14=\frac25.` |
| 647 | 5966-5968 | 0.49 | inline_safe | bracket | `a=12,\qquad b=-12,\qquad c=3.` |
| 651 | 6004-6006 | 0.45 | inline_safe | bracket | `\mathrm{C}_n^k p^k (1-p)^{n-k} \approx \frac{\lambda^k}{k!} e^{-\lambda}.` |
| 652 | 6022-6024 | 0.28 | inline_safe | bracket | `P\{X=k\}=\frac{\lambda^k}{k!}e^{-\lambda},` |
| 653 | 6026-6028 | 0.31 | inline_safe | bracket | `\frac{\lambda^1}{1!}e^{-\lambda}=\frac{\lambda^2}{2!}e^{-\lambda}.` |
| 654 | 6030-6032 | 0.34 | inline_safe | bracket | `\lambda=\frac{\lambda^2}{2}\implies 1=\frac{\lambda}{2}\implies \lambda=2.` |
| 655 | 6035-6042 | 0.16 | inline_unsafe_marker | bracket | `\begin{aligned} P\{X=4\} &=\frac{2^4}{4!}e^{-2}\\ &=\frac{16}{24}e^{-2} =\frac{2}{3}e^{-2}. \end{aligned}` |
| 660 | 6076-6078 | 0.25 | inline_safe | bracket | `E[(X-1)(X-2)]=1.` |
| 662 | 6087-6091 | 0.21 | normalized_width_not_low | bracket | `E[(X-1)(X-2)] =E(X^2-3X+2) =\lambda^2-2\lambda+2.` |
| 663 | 6093-6095 | 0.20 | inline_safe | bracket | `\lambda^2-2\lambda+2=1,` |
| 664 | 6097-6099 | 0.16 | inline_safe | bracket | `(\lambda-1)^2=0.` |
| 665 | 6101-6103 | 0.07 | inline_safe | bracket | `\lambda=1.` |
| 667 | 6116-6126 | 0.18 | inline_unsafe_marker | bracket | `\begin{array}{c\|cccccc} \hline X & 0 & 1 & 2 & 3 & 4 & 5 \\ \hline P & \dfrac{\mathrm{C}_5^0\mathrm{C}_{15}^8}{\mathrm{C}_{20}^8} & \dfrac{\mathrm{C}_5^1\mathrm{C}_{15}^7}{\math...` |
| 668 | 6139-6142 | 0.37 | normalized_width_not_low | bracket | `P(X=k)=\frac{\binom3k\binom3{3-k}}{\binom63}, \qquad k=0,1,2,3.` |
| 669 | 6144-6150 | 0.10 | inline_unsafe_marker | bracket | `\begin{array}{c\|cccc} X & 0 & 1 & 2 & 3\\ \hline P & \dfrac1{20} & \dfrac9{20} & \dfrac9{20} & \dfrac1{20} \end{array}` |
| 671 | 6158-6160 | 0.20 | inline_safe | bracket | `P(A\|X=k)=\frac{k}{6}.` |
| 672 | 6162-6166 | 0.44 | normalized_width_not_low | bracket | `P(A)=\sum_{k=0}^3P(X=k)P(A\|X=k) =\frac{EX}{6} =\frac{1}{4}.` |
| 673 | 6177-6179 | 0.22 | inline_safe | bracket | `P=\frac{10}{15}=\frac23.` |
| 674 | 6182-6187 | 0.39 | normalized_width_not_low | bracket | `P(AB) =\frac{\binom{10}{3}\binom52\binom74\binom32} {\binom{15}{5}\binom{10}{6}} =\frac{200}{1001}.` |
| 675 | 6190-6194 | 0.36 | normalized_width_not_low | bracket | `P(C)=\frac{\binom{10}{3}\binom52}{\binom{15}{5}}=\frac{400}{1001}, \qquad P(D)=\frac{\binom52\binom{10}{4}}{\binom{15}{6}}=\frac{420}{1001}.` |
| 676 | 6196-6200 | 0.33 | normalized_width_not_low | bracket | `P(C\cup D)=P(C)+P(D)-P(CD) =\frac{400+420-200}{1001} =\frac{620}{1001}.` |
| 677 | 6211-6213 | 0.27 | inline_safe | bracket | `P=\frac9{15}=\frac35.` |
| 678 | 6216-6220 | 0.44 | normalized_width_not_low | bracket | `P=\frac{\binom93\binom61\binom64\binom51} {\binom{15}{4}\binom{11}{5}} =\frac{60}{1001}.` |
| 679 | 6223-6227 | 0.39 | normalized_width_not_low | bracket | `P(C)=\frac{\binom92\binom62}{\binom{15}{4}}=\frac{396}{1001}, \qquad P(D)=\frac{\binom63\binom92}{\binom{15}{5}}=\frac{240}{1001}.` |
| 680 | 6229-6233 | 0.49 | normalized_width_not_low | bracket | `P(CD)=\frac{\binom92\binom62\binom72\binom43} {\binom{15}{4}\binom{11}{5}} =\frac{72}{1001}.` |
| 681 | 6235-6238 | 0.30 | inline_safe | bracket | `P(C\cup D)=\frac{396+240-72}{1001} =\frac{564}{1001}.` |
| 682 | 6249-6251 | 0.27 | inline_safe | bracket | `P=\frac9{15}=\frac35.` |
| 683 | 6254-6258 | 0.44 | normalized_width_not_low | bracket | `P=\frac{\binom93\binom62\binom64\binom42} {\binom{15}{5}\binom{10}{6}} =\frac{180}{1001}.` |
| 684 | 6261-6265 | 0.39 | normalized_width_not_low | bracket | `P(C)=\frac{\binom93\binom62}{\binom{15}{5}}=\frac{420}{1001}, \qquad P(D)=\frac{\binom62\binom94}{\binom{15}{6}}=\frac{378}{1001}.` |
| 685 | 6267-6271 | 0.49 | normalized_width_not_low | bracket | `P(CD)=\frac{\binom93\binom62\binom64\binom42} {\binom{15}{5}\binom{10}{6}} =\frac{180}{1001}.` |
| 686 | 6273-6276 | 0.32 | inline_safe | bracket | `P(C\cup D)=\frac{420+378-180}{1001} =\frac{618}{1001}.` |
| 687 | 6281-6290 | 0.11 | inline_unsafe_marker | bracket | `F(x)= \begin{cases} 0, & x\le0,\\ \dfrac{x}{2}, & 0<x<1,\\ \dfrac23, & 1\le x<2,\\ \dfrac{11}{12}, & 2\le x<3,\\ 1, & x\ge3. \end{cases}` |
| 690 | 6307-6310 | 0.41 | normalized_width_not_low | bracket | `P\{2\le X\le4\}=P\{X=2\}+P\{X=3\} =\frac14+\frac1{12}=\frac13.` |
| 692 | 6321-6330 | 0.11 | inline_unsafe_marker | bracket | `F(x)= \begin{cases} 0, & x\le0,\\ \dfrac{x}{3}, & 0<x<1,\\ \dfrac12, & 1\le x<2,\\ \dfrac34, & 2\le x<3,\\ 1, & x\ge3. \end{cases}` |
| 694 | 6344-6348 | 0.43 | normalized_width_not_low | bracket | `P\left\{X<\frac12\right\}=F\!\left(\frac12\right)=\frac16, \qquad P\{2<X\le3\}=P\{X=3\}=\frac14.` |
| 695 | 6350-6354 | 0.49 | normalized_width_not_low | bracket | `EX=\int_0^1 x\cdot\frac13\,\mathrm dx +1\cdot\frac16+2\cdot\frac14+3\cdot\frac14 =\frac{19}{12}.` |
| 697 | 6373-6375 | 0.41 | inline_safe | bracket | `P(X=k)=A\lambda^k,\qquad k=1,2,\dots` |
| 698 | 6386-6389 | 0.21 | inline_safe | bracket | `\sum_{k=1}^{\infty}A\lambda^k =A\frac{\lambda}{1-\lambda}=1,` |
| 699 | 6391-6393 | 0.13 | inline_safe | bracket | `A=\frac{1-\lambda}{\lambda}.` |
| 700 | 6395-6397 | 0.44 | inline_safe | bracket | `1+A=\frac{1}{\lambda},\qquad \lambda=(1+A)^{-1},` |
| 704 | 6434-6436 | 0.36 | inline_safe | bracket | `P\{\text{继续}\}=P\{8,9,10\}=\frac3{10},` |
| 708 | 6453-6458 | 0.44 | normalized_width_not_low | bracket | `P\{X=i\}P\{Y=j\} =\frac7{10}\left(\frac3{10}\right)^{i-1}\cdot\frac17 =\left(\frac3{10}\right)^{i-1}\frac1{10} =P\{X=i,Y=j\},` |
| 709 | 6462-6464 | 0.44 | inline_safe | bracket | `E(X-1)=EX-1=\frac{10}{7}-1=\frac37.` |
| 710 | 6466-6468 | 0.28 | inline_safe | bracket | `EY=\frac{1+2+\cdots+7}{7}=4.` |
| 712 | 6482-6485 | 0.49 | normalized_width_not_low | bracket | `P\{X=2m-1\}=0.8(0.2)^{m-1}(0.5)^{m-1} =0.8(0.1)^{m-1},\qquad m=1,2,\dots.` |
| 713 | 6487-6490 | 0.37 | normalized_width_not_low | bracket | `P\{X=2m\}=(0.2)^m(0.5)^{m} =(0.1)^m,\qquad m=1,2,\dots.` |
| 714 | 6492-6498 | 0.26 | inline_unsafe_marker | bracket | `P\{X=k\}= \begin{cases} 0.8(0.1)^{m-1}, & k=2m-1,\ m=1,2,\dots,\\ (0.1)^m, & k=2m,\ m=1,2,\dots. \end{cases}` |
| 715 | 6501-6503 | 0.46 | inline_safe | bracket | `Y=1+2+\cdots+(X-1)=\frac{X(X-1)}2.` |
| 717 | 6513-6516 | 0.49 | normalized_width_not_low | bracket | `\sum_{m=1}^{\infty}m r^m=\frac{r}{(1-r)^2},\qquad \sum_{m=1}^{\infty}m^2 r^m=\frac{r(1+r)}{(1-r)^3},` |
| 718 | 6518-6520 | 0.12 | inline_safe | bracket | `EY=\frac{14}{27}.` |
| 722 | 6562-6564 | 0.33 | inline_safe | bracket | `T = \min\{X_1,X_2,X_3,X_4\}.` |
| 723 | 6567-6569 | 0.41 | inline_safe | bracket | `F_X(x) = 1-e^{-0.2x},\quad x\geqslant0.` |
| 725 | 6579-6585 | 0.17 | inline_unsafe_marker | bracket | `F_T(t)= \begin{cases} 0, & t<0, \\[4pt] 1-e^{-0.8t}, & t\geqslant0. \end{cases}` |
| 726 | 6606-6608 | 0.37 | inline_safe | bracket | `F(-a)=\int_{-\infty}^{-a}f(x)\,\mathrm{d}x.` |
| 727 | 6610-6619 | 0.33 | inline_unsafe_marker | bracket | `\begin{aligned} F(-a) &=\int_{+\infty}^{a}f(-t)(-\,\mathrm{d}t) =\int_{a}^{+\infty}f(-t)\,\mathrm{d}t \\ &=\int_{a}^{+\infty}f(t)\,\mathrm{d}t =1-\int_{-\infty}^{a}f(t)\,\mathrm...` |
| 728 | 6623-6625 | 0.49 | inline_safe | bracket | `P(\|X\|<a)=P(-a<X<a)=F(a)-F(-a).` |
| 729 | 6627-6629 | 0.48 | inline_safe | bracket | `P(\|X\|<a)=F(a)-[1-F(a)]=2F(a)-1.` |
| 732 | 6646-6651 | 0.10 | inline_unsafe_marker | bracket | `f(x) = \begin{cases} \frac{1}{b-a}, & a < x < b, \\ 0, & \text{其他}, \end{cases}` |
| 733 | 6653-6659 | 0.11 | inline_unsafe_marker | bracket | `F(x) = \begin{cases} 0, & x < a, \\ \frac{x-a}{b-a}, & a \le x < b, \\ 1, & x \ge b. \end{cases}` |
| 735 | 6683-6689 | 0.11 | inline_unsafe_marker | bracket | `F(x) = \begin{cases} 0, & x < 1, \\ \frac{5 + 2x}{12}, & 1 \le x < 4, \\ 1, & x \ge 4. \end{cases}` |
| 736 | 6699-6701 | 0.33 | inline_safe | bracket | `P\{X>4\}=\frac{b-4}{b-a}=\frac12.` |
| 737 | 6703-6705 | 0.45 | inline_safe | bracket | `2(b-4)=b-a \quad \Longrightarrow \quad a+b=8.` |
| 739 | 6712-6714 | 0.48 | inline_safe | bracket | `4(3-a)=b-a \quad \Longrightarrow \quad b=12-3a.` |
| 740 | 6717-6722 | 0.14 | inline_unsafe_marker | bracket | `\begin{cases} a+b=8,\\ b=12-3a, \end{cases}` |
| 742 | 6741-6743 | 0.43 | inline_safe | bracket | `P\{\text{方程有实根}\}=P(X\le 1)=\frac{1-0}{8}=\frac{1}{8}.` |
| 743 | 6751-6753 | 0.20 | inline_safe | bracket | `Y\sim B\!\left(4,\frac18\right).` |
| 745 | 6768-6770 | 0.28 | inline_safe | bracket | `P\{X>3\} = \frac{5-3}{5-2} = \frac{2}{3}.` |
| 747 | 6781-6786 | 0.11 | inline_unsafe_marker | bracket | `f(x) = \begin{cases} \lambda e^{-\lambda x}, & x > 0, \\ 0, & x \le 0, \end{cases}` |
| 748 | 6788-6793 | 0.14 | inline_unsafe_marker | bracket | `F(x) = \begin{cases} 1 - e^{-\lambda x}, & x \ge 0, \\ 0, & x < 0. \end{cases}` |
| 749 | 6798-6800 | 0.33 | inline_safe | bracket | `P\{X > s + t \mid X > s\} = P\{X > t\}.` |
| 750 | 6805-6808 | 0.45 | display_environment | env:align* | `P\{X > s + t \mid X > s\} &= \frac{P\{X > s + t\}}{P\{X > s\}} \\ &= \frac{e^{-\lambda(s+t)}}{e^{-\lambda s}} = e^{-\lambda t} = P\{X > t\}.` |
| 753 | 6840-6846 | 0.15 | inline_unsafe_marker | bracket | `f(x)= \begin{cases} Ae^{-x/100}, & x>0,\\ 0, & \text{其他}. \end{cases}` |
| 754 | 6853-6855 | 0.44 | inline_safe | bracket | `1=\int_0^\infty Ae^{-x/100}\,\mathrm dx=100A,` |
| 755 | 6857-6859 | 0.25 | inline_safe | bracket | `A=\frac1{100}=0.01.` |
| 756 | 6861-6865 | 0.49 | normalized_width_not_low | bracket | `P(200<X<300) =\int_{200}^{300}\frac1{100}e^{-x/100}\,\mathrm dx =e^{-2}-e^{-3}.` |
| 758 | 6872-6874 | 0.20 | inline_safe | bracket | `Y\sim B(5,e^{-3}).` |
| 763 | 6916-6922 | 0.31 | inline_unsafe_marker | bracket | `\begin{aligned} P\{\max\{X_1,X_2\}>5\} &= 1-P\{X_1\leqslant5, X_2\leqslant5\} \\ &= 1-\left(1-e^{-\lambda\cdot5}\right)^2 \\ &= 1-\left(1-e^{-\frac{5}{4}}\right)^2. \end{aligned}` |
| 764 | 6928-6934 | 0.08 | inline_unsafe_marker | bracket | `f(x)= \begin{cases} e^{-x}, & x\geqslant0, \\[4pt] 0, & x<0, \end{cases}` |
| 765 | 6939-6941 | 0.29 | inline_safe | bracket | `\{X_1 < T,\ X_1+X_2 > T\}.` |
| 767 | 6955-6957 | 0.17 | inline_safe | bracket | `X+Y\sim E(2\lambda).` |
| 768 | 6964-6966 | 0.48 | inline_safe | bracket | `f_{X+Y}(z)=\lambda^2 z e^{-\lambda z},\qquad z>0.` |
| 773 | 7028-7030 | 0.20 | inline_safe | bracket | `F(-x)\ne 1-F(x).` |
| 774 | 7037-7039 | 0.21 | inline_safe | bracket | `F(x)=\Phi\left(\frac{x-\mu}{\sigma}\right).` |
| 775 | 7041-7043 | 0.21 | inline_safe | bracket | `F(-x)=1-F(x).` |
| 776 | 7052-7054 | 0.28 | inline_safe | bracket | `P(X<\mu)=P(X>\mu)=\frac{1}{2}.` |
| 777 | 7056-7058 | 0.11 | inline_safe | bracket | `C=\mu=3.` |
| 780 | 7077-7079 | 0.16 | inline_safe | bracket | `Z=X-2Y+1` |
| 781 | 7084-7086 | 0.41 | inline_safe | bracket | `EZ=EX-2EY+1=2-4+1=-1,` |
| 782 | 7088-7090 | 0.40 | inline_safe | bracket | `DZ=DX+4DY=0.2+4\times0.2=1,` |
| 783 | 7092-7094 | 0.17 | inline_safe | bracket | `Z\sim N(-1,1).` |
| 784 | 7096-7099 | 0.46 | normalized_width_not_low | bracket | `f_Z(z)=\frac1{\sqrt{2\pi}}\exp\!\left\{-\frac{(z+1)^2}{2}\right\}, \qquad -\infty<z<+\infty.` |
| 785 | 7110-7112 | 0.25 | inline_safe | bracket | `Z=\frac{X-\mu}{\sigma}\sim N(0,1),` |
| 786 | 7114-7122 | 0.29 | inline_unsafe_marker | bracket | `\begin{aligned} P\{\|X-\mu\|<1\} &=P\left\{-1<X-\mu<1\right\}\\ &=P\left\{-\frac{1}{\sigma}<\frac{X-\mu}{\sigma}<\frac{1}{\sigma}\right\}\\ &=P\left\{-\frac{1}{\sigma}<Z<\frac{1}{...` |
| 787 | 7125-7127 | 0.04 | inline_safe | bracket | `\frac{1}{\sigma}` |
| 788 | 7129-7131 | 0.07 | inline_safe | bracket | `\Phi\left(\frac{1}{\sigma}\right)` |
| 789 | 7133-7135 | 0.13 | inline_safe | bracket | `2\Phi\left(\frac{1}{\sigma}\right)-1` |
| 790 | 7150-7152 | 0.36 | inline_safe | bracket | `P\{\|X\|<x\}=P\{-x<X<x\}=\alpha.` |
| 791 | 7156-7158 | 0.21 | inline_safe | bracket | `\Phi(x)-\Phi(-x)=\alpha,` |
| 792 | 7160-7162 | 0.16 | inline_safe | bracket | `2\Phi(x)-1=\alpha,` |
| 793 | 7164-7166 | 0.17 | inline_safe | bracket | `\Phi(x)=\frac{1+\alpha}{2}.` |
| 794 | 7168-7170 | 0.33 | inline_safe | bracket | `P\{X>x\}=1-\Phi(x)=\frac{1-\alpha}{2}.` |
| 796 | 7188-7191 | 0.31 | normalized_width_not_low | bracket | `\Rightarrow \Phi\left(\frac{1}{\sigma_1}\right)>\Phi\left(\frac{1}{\sigma_2}\right)\implies \frac{1}{\sigma_1}>\frac{1}{\sigma_2} \Rightarrow \sigma_1<\sigma_2.` |
| 825 | 7394-7396 | 0.33 | inline_safe | bracket | `D(X) = \frac{\sigma^2}{\sqrt{2\pi}} \cdot \sqrt{2\pi} = \sigma^2.` |
| 830 | 7435-7441 | 0.15 | inline_unsafe_marker | bracket | `f_Z(z) = \begin{cases} \dfrac{1}{\lambda}z^{\frac{1}{\lambda}-1}, & 0<z<1, \\[6pt] 0, & \text{其他}. \end{cases}` |
| 833 | 7465-7472 | 0.13 | inline_unsafe_marker | bracket | `F(x)= \begin{cases} 0, & x<0, \\ \dfrac{1}{2}, & 0\leqslant x<1, \\ 1-e^{-x}, & x\geqslant1, \end{cases}` |
| 834 | 7477-7482 | 0.39 | inline_unsafe_marker | bracket | `\begin{aligned} P\{0\leqslant X\leqslant1\}&=F(1)-F(0^-)=1-e^{-1}; \\ P\{0<X<1\}&=F(1^-)-F(0)=\frac{1}{2}-\frac{1}{2}=0. \end{aligned}` |
| 835 | 7487-7495 | 0.14 | inline_unsafe_marker | bracket | `F(x)= \begin{cases} 0, & x<-1, \\ 0.4, & -1\leqslant x<2, \\ 0.8, & 2\leqslant x<3, \\ 1, & x\geqslant3, \end{cases}` |
| 838 | 7507-7509 | 0.49 | inline_safe | bracket | `P\{X=3\}=F(3)-F(3^-)=1-0.8=0.2.` |
| 840 | 7523-7529 | 0.10 | inline_unsafe_marker | bracket | `f(x)= \begin{cases} \dfrac{A}{x^2}, & x>100, \\[6pt] 0, & x\leqslant100, \end{cases}` |
| 841 | 7535-7537 | 0.49 | inline_safe | bracket | `A\left[-\frac{1}{x}\right]_{100}^{+\infty} = \frac{A}{100} = 1 \Rightarrow A=100.` |
| 844 | 7545-7547 | 0.46 | inline_safe | bracket | `P\{X=1000\}=0 \quad (\text{连续型随机变量单点概率为0}).` |
| 846 | 7553-7559 | 0.12 | inline_unsafe_marker | bracket | `F(x)= \begin{cases} 0, & x<100, \\[6pt] 1-\dfrac{100}{x}, & x\geqslant100. \end{cases}` |
| 847 | 7565-7572 | 0.15 | inline_unsafe_marker | bracket | `F(x)= \begin{cases} 0, & x<-a, \\[6pt] A+B\arcsin\dfrac{x}{a}, & -a\leqslant x\leqslant a, \\[6pt] 1, & x\geqslant a, \end{cases}` |
| 849 | 7585-7591 | 0.19 | inline_unsafe_marker | bracket | `f(x) = F'(x) = \begin{cases} \dfrac{1}{\pi\sqrt{a^2-x^2}}, & -a<x<a, \\[6pt] 0, & \text{其他}. \end{cases}` |
| 851 | 7601-7607 | 0.10 | inline_unsafe_marker | bracket | `f(x)= \begin{cases} \dfrac{3}{8}x^2, & 0<x<2, \\[6pt] 0, & \text{其他}. \end{cases}` |
| 855 | 7629-7636 | 0.11 | inline_unsafe_marker | bracket | `f(x)= \begin{cases} x, & 0\leqslant x<1, \\[6pt] 2-x, & 1\leqslant x<2, \\[6pt] 0, & \text{其他}. \end{cases}` |
| 856 | 7644-7646 | 0.34 | inline_safe | bracket | `F(x) = \int_0^x t\,dt = \frac{x^2}{2};` |
| 858 | 7654-7662 | 0.20 | inline_unsafe_marker | bracket | `F(x)= \begin{cases} 0, & x<0, \\[6pt] \dfrac{x^2}{2}, & 0\leqslant x<1, \\[6pt] -\dfrac{x^2}{2}+2x-1, & 1\leqslant x<2, \\[6pt] 1, & x\geqslant2. \end{cases}` |
| 859 | 7667-7689 | 0.29 | inline_unsafe_marker | bracket | `\begin{aligned} &\text{A. } F(x)= \begin{cases} 0, & x<-1, \\[4pt] \dfrac{1}{3}, & -1\leqslant x\leqslant2, \\[4pt] 1, & x>2, \end{cases} &&\text{B. } F(x)= \begin{cases} 0, & x...` |
| 860 | 7704-7711 | 0.20 | inline_unsafe_marker | bracket | `F(x)= \begin{cases} A_1, & x<-a, \\[4pt] A_2+A_3\arctan\dfrac{x}{a}, & x\in[-a,a], \\[6pt] A_4, & x>a, \end{cases}` |
| 863 | 7733-7739 | 0.18 | inline_unsafe_marker | bracket | `f(x)=F'(x)= \begin{cases} \dfrac{2a}{\pi(x^2+a^2)}, & -a\leqslant x\leqslant a, \\[6pt] 0, & \text{其他}. \end{cases}` |
| 864 | 7741-7746 | 0.38 | inline_unsafe_marker | bracket | `\begin{cases} \Delta=X^2-\dfrac{a^2}{4}\geqslant0, \\[4pt] X<0 \quad (\text{由韦达定理，根的和}=-X>0). \end{cases}` |
| 868 | 7792-7794 | 0.38 | inline_safe | bracket | `P\{X = x_i\} = p_i,\quad i=1,2,\dots` |
| 869 | 7796-7798 | 0.41 | inline_safe | bracket | `P\{Y = g(x_i)\} = p_i,\quad i=1,2,\dots` |
| 870 | 7800-7802 | 0.13 | inline_unsafe_marker | bracket | `Y \sim \begin{pmatrix} g(x_1) & g(x_2) & \cdots \\ p_1 & p_2 & \cdots \end{pmatrix}.` |
| 874 | 7848-7850 | 0.21 | inline_safe | bracket | `f_Y(y) = F_Y'(y).` |
| 875 | 7864-7869 | 0.25 | inline_unsafe_marker | bracket | `f_Y(y) = \begin{cases} f_X[h(y)] \cdot \|h'(y)\|, & \alpha < y < \beta, \\ 0, & \text{其他}, \end{cases}` |
| 878 | 7882-7884 | 0.46 | inline_safe | bracket | `f_Y(y) = F_Y'(y) = f_X[h(y)] \cdot h'(y).` |
| 880 | 7904-7906 | 0.40 | inline_safe | bracket | `F_Y(y) = P\{Y \le y\} = P\{g(X) \le y\}.` |
| 881 | 7914-7919 | 0.17 | inline_unsafe_marker | bracket | `f_X(x) = \begin{cases} 1, & -\dfrac{1}{2} < x < \dfrac{1}{2}, \\[6pt] 0, & \text{其他}, \end{cases}` |
| 883 | 7937-7939 | 0.22 | inline_safe | bracket | `\left(a-\dfrac{b}{2},\ a+\dfrac{b}{2}\right).` |
| 885 | 7948-7950 | 0.36 | inline_safe | bracket | `f_Y(y) = f_X\left(\frac{y-a}{b}\right) \cdot \frac{1}{\|b\|}.` |
| 886 | 7952-7957 | 0.27 | inline_unsafe_marker | bracket | `f_Y(y) = \begin{cases} \dfrac{1}{\|b\|}, & a - \dfrac{\|b\|}{2} < y < a + \dfrac{\|b\|}{2}, \\[8pt] 0, & \text{其他}. \end{cases}` |
| 888 | 7964-7969 | 0.12 | inline_unsafe_marker | bracket | `f_Y(y) = \begin{cases} \dfrac{1}{\sqrt{y}}, & 0 < y < \dfrac{1}{4}, \\[6pt] 0, & \text{其他}. \end{cases}` |
| 890 | 7975-7980 | 0.13 | inline_unsafe_marker | bracket | `f_Y(y) = \begin{cases} 2, & 0 \le y < \dfrac{1}{2}, \\[6pt] 0, & \text{其他}. \end{cases}` |
| 891 | 7988-7994 | 0.13 | inline_unsafe_marker | bracket | `f_X(x)= \begin{cases} \dfrac14, & -2<x<2,\\ 0, & \text{其他}. \end{cases}` |
| 892 | 7996-8000 | 0.43 | normalized_width_not_low | bracket | `f_Y(y)=\frac{f_X(-\sqrt y)}{2\sqrt y}+\frac{f_X(\sqrt y)}{2\sqrt y} =\frac{1/4}{2\sqrt y}+\frac{1/4}{2\sqrt y} =\frac{1}{4\sqrt y}.` |
| 893 | 8002-8008 | 0.11 | inline_unsafe_marker | bracket | `f_Y(y)= \begin{cases} \dfrac{1}{4\sqrt y}, & 0<y<4,\\[6pt] 0, & \text{其他}. \end{cases}` |
| 895 | 8023-8025 | 0.46 | inline_safe | bracket | `P\{Y=0\} = P\{X^2=0\} = P\{X=0\} = \frac{1}{2}.` |
| 897 | 8033-8035 | 0.10 | inline_unsafe_marker | bracket | `Y \sim \begin{pmatrix} 0 & 1 \\[4pt] \dfrac{1}{2} & \dfrac{1}{2} \end{pmatrix}.` |
| 899 | 8058-8064 | 0.11 | inline_unsafe_marker | bracket | `F_Y(y) = \begin{cases} 0, & y < 0, \\ y, & 0 \le y < 1, \\ 1, & y \ge 1, \end{cases}` |
| 902 | 8094-8099 | 0.23 | inline_unsafe_marker | bracket | `f_X(x) = F'_X(x) = \begin{cases} 1, & 0 < x < 1, \\[4pt] 0, & \text{其他}. \end{cases}` |
| 906 | 8121-8126 | 0.14 | inline_unsafe_marker | bracket | `f_Z(z) = \begin{cases} \dfrac{2}{(1+z)^2}, & z > 1, \\[6pt] 0, & \text{其他}. \end{cases}` |
| 907 | 8131-8137 | 0.13 | inline_unsafe_marker | bracket | `f_X(x) = \begin{cases} \dfrac{1}{2}, & -1 < x < 0, \\[6pt] \dfrac{1}{4}, & 0 \le x < 2, \\[6pt] 0, & \text{其他}, \end{cases}` |
| 908 | 8145-8151 | 0.44 | inline_unsafe_marker | bracket | `\begin{aligned} F_Y(y) &= P\{-\sqrt{y} \le X \le \sqrt{y}\} \\ &= P\{-\sqrt{y} \le X < 0\} + P\{0 \le X \le \sqrt{y}\} \\ &= \frac{1}{2}\sqrt{y} + \frac{1}{4}\sqrt{y} = \frac{3}...` |
| 910 | 8161-8167 | 0.11 | inline_unsafe_marker | bracket | `f_Y(y) = \begin{cases} \dfrac{3}{8\sqrt{y}}, & 0 < y < 1, \\[6pt] \dfrac{1}{8\sqrt{y}}, & 1 \le y < 4, \\[6pt] 0, & \text{其他}. \end{cases}` |
| 912 | 8187-8194 | 0.11 | inline_unsafe_marker | bracket | `F_Y(y)= \begin{cases} 0, & y<1, \\[6pt] \dfrac{1}{3}, & 1\leqslant y<2, \\[6pt] 1, & y\geqslant2. \end{cases}` |
| 913 | 8205-8207 | 0.21 | inline_safe | bracket | `\frac{\mathrm{d}x}{\mathrm{d}y} = \frac{1}{2(1-y)}.` |
| 915 | 8215-8220 | 0.11 | inline_unsafe_marker | bracket | `f_Y(y) = \begin{cases} 1, & 0 < y < 1, \\[4pt] 0, & \text{其他}. \end{cases}` |
| 918 | 8245-8250 | 0.21 | inline_unsafe_marker | bracket | `f_Y(y) = \begin{cases} \dfrac{1}{\sqrt{8\pi}} e^{-\frac{y^2}{32}}, & y > 0, \\[6pt] 0, & y \le 0. \end{cases}` |
| 920 | 8265-8269 | 0.21 | display_environment | env:align* | `F_Y(y) &= P\{Y \le y\} \\ &= P\{1-\sqrt[3]{X} \le y\} \\ &= P\{\sqrt[3]{X} \ge 1-y\}` |
| 925 | 8304-8306 | 0.40 | inline_safe | bracket | `f_Y(y) = F_Y'(y) = f_X\left(\frac{y}{2}\right) \cdot \frac{1}{2}` |
| 928 | 8329-8331 | 0.21 | inline_safe | bracket | `\left\|\frac{\mathrm dx}{\mathrm dy}\right\|=\frac12.` |
| 929 | 8333-8337 | 0.38 | normalized_width_not_low | bracket | `f_Y(y)=f_X\left(\frac y2\right)\cdot\frac12 =\frac{1}{\pi\left(1+\frac{y^2}{4}\right)}\cdot\frac12 =\frac{2}{\pi(4+y^2)}.` |
| 932 | 8357-8363 | 0.33 | inline_unsafe_marker | bracket | `f_Y(y) = \begin{cases} \dfrac{1}{2\sqrt{\pi(y-1)}}\exp\left\{-\dfrac{y-1}{4}\right\}, & y>1, \\[8pt] 0, & y\leqslant1. \end{cases}` |
| 933 | 8371-8376 | 0.44 | display_environment | env:align* | `F_X(x) &= \int_{-\infty}^{x} \frac{e^t}{(1+e^t)^2}\,\mathrm{d}t \\ &= \left[-\frac{1}{1+e^t}\right]_{-\infty}^{x} \\ &= \left(-\frac{1}{1+e^x}\right) - \left(-\frac{1}{1+0}\righ...` |
| 935 | 8387-8389 | 0.36 | inline_safe | bracket | `F_Y(y) = \frac{e^{\ln y}}{1+e^{\ln y}} = \frac{y}{1+y}.` |
| 937 | 8397-8403 | 0.14 | inline_unsafe_marker | bracket | `f_Y(y)= \begin{cases} \dfrac{1}{(1+y)^2}, & y>0, \\[8pt] 0, & y\leqslant0. \end{cases}` |
| 938 | 8413-8419 | 0.13 | inline_unsafe_marker | bracket | `f_X(x)= \begin{cases} \dfrac{1}{3}, & -1<x<2, \\[6pt] 0, & \text{其他}. \end{cases}` |
| 941 | 8435-8442 | 0.11 | inline_unsafe_marker | bracket | `f_Y(y)= \begin{cases} \dfrac{2}{3}, & 0<y<1, \\[6pt] \dfrac{1}{3}, & 1\leqslant y<2, \\[6pt] 0, & \text{其他}. \end{cases}` |
| 942 | 8503-8506 | 0.49 | normalized_width_not_low | bracket | `P(X=1)=P(X=-1)=\frac12,\qquad P(Y=1)=P(Y=-1)=\frac12.` |
| 943 | 8517-8525 | 0.49 | inline_unsafe_marker | bracket | `\begin{aligned} P(X=Y) &=P(X=1,Y=1)+P(X=-1,Y=-1)\\ &=P(X=1)P(Y=1)+P(X=-1)P(Y=-1)\\ &=\frac12\cdot\frac12+\frac12\cdot\frac12 =\frac12. \end{aligned}` |
| 944 | 8531-8534 | 0.49 | normalized_width_not_low | bracket | `P(X=1)=P(X=-1)=\frac12,\qquad P(Y=1)=P(Y=-1)=\frac12.` |
| 945 | 8545-8553 | 0.49 | inline_unsafe_marker | bracket | `\begin{aligned} P(X=Y) &=P(X=1,Y=1)+P(X=-1,Y=-1)\\ &=P(X=1)P(Y=1)+P(X=-1)P(Y=-1)\\ &=\frac12\cdot\frac12+\frac12\cdot\frac12 =\frac12. \end{aligned}` |
| 946 | 8568-8570 | 0.43 | inline_safe | bracket | `E(X)=np,\qquad D(X)=np(1-p).` |
| 947 | 8572-8574 | 0.20 | inline_safe | bracket | `np(1-p)=1.44.` |
| 948 | 8576-8578 | 0.24 | inline_safe | bracket | `1-p=\frac{1.44}{2.4}=0.6,` |
| 949 | 8580-8582 | 0.37 | inline_safe | bracket | `p=0.4,\qquad n=\frac{2.4}{0.4}=6.` |
| 950 | 8591-8593 | 0.15 | inline_safe | bracket | `\binom53=10.` |
| 951 | 8597-8599 | 0.43 | inline_safe | bracket | `P(X=1)=\frac{\binom42}{\binom53}=\frac{6}{10}=\frac35.` |
| 952 | 8602-8604 | 0.32 | inline_safe | bracket | `P(X=2)=\frac{\binom32}{\binom53}=\frac{3}{10}.` |
| 953 | 8607-8609 | 0.32 | inline_safe | bracket | `P(X=3)=\frac{1}{\binom53}=\frac{1}{10}.` |
| 954 | 8612-8618 | 0.10 | inline_unsafe_marker | bracket | `\begin{array}{c\|ccc} X & 1 & 2 & 3\\ \hline P & \dfrac35 & \dfrac3{10} & \dfrac1{10} \end{array}.` |
| 955 | 8623-8629 | 0.13 | inline_unsafe_marker | bracket | `f(x)= \begin{cases} 1-\|x\|, & -1<x<1,\\ 0, & \text{其他}. \end{cases}` |
| 956 | 8634-8636 | 0.10 | inline_safe | bracket | `1<Y<2.` |
| 957 | 8639-8648 | 0.45 | inline_unsafe_marker | bracket | `\begin{aligned} F_Y(y) &=P(X^2+1\le y) =P(\|X\|\le \sqrt{y-1})\\ &=\int_{-\sqrt{y-1}}^{\sqrt{y-1}}(1-\|x\|)\,\mathrm{d}x\\ &=2\int_0^{\sqrt{y-1}}(1-x)\,\mathrm{d}x\\ &=2\sqrt{y-1}-(...` |
| 958 | 8650-8657 | 0.22 | inline_unsafe_marker | bracket | `F_Y(y)= \begin{cases} 0, & y\le 1,\\ 2\sqrt{y-1}-(y-1), & 1<y<2,\\ 1, & y\ge 2. \end{cases}` |
| 959 | 8660-8662 | 0.27 | inline_safe | bracket | `f_Y(y)=\frac{1}{\sqrt{y-1}}-1.` |
| 960 | 8664-8670 | 0.16 | inline_unsafe_marker | bracket | `f_Y(y)= \begin{cases} \dfrac{1}{\sqrt{y-1}}-1, & 1<y<2,\\ 0, & \text{其他}. \end{cases}` |
| 961 | 8678-8680 | 0.21 | inline_safe | bracket | `F(x)=\frac{a+be^x}{3+e^x}.` |
| 963 | 8695-8697 | 0.33 | inline_safe | bracket | `\lim_{x\to-\infty}F(x)=\frac{a}{3}=0,` |
| 964 | 8701-8703 | 0.31 | inline_safe | bracket | `\lim_{x\to+\infty}F(x)=b=1,` |
| 965 | 8705-8707 | 0.37 | inline_safe | bracket | `F(0)=\frac{0+1}{3+1}=\frac14=0.25.` |
| 967 | 8725-8729 | 0.38 | normalized_width_not_low | bracket | `E(X)=5\cdot\frac35+2\cdot\frac25 =3+\frac45 =3.8.` |
| 968 | 8737-8739 | 0.43 | inline_safe | bracket | `E(\zeta)=np,\qquad D(\zeta)=np(1-p).` |
| 969 | 8741-8743 | 0.19 | inline_safe | bracket | `np(1-p)=1.2.` |
| 970 | 8745-8747 | 0.23 | inline_safe | bracket | `1-p=\frac{1.2}{3}=0.4,` |
| 971 | 8749-8751 | 0.16 | inline_safe | bracket | `n=\frac{3}{0.6}=5.` |
| 972 | 8759-8761 | 0.21 | inline_safe | bracket | `D(\zeta)=\sigma^2(\zeta)=4.` |
| 973 | 8763-8765 | 0.30 | inline_safe | bracket | `D(\zeta)=E(\zeta^2)-[E(\zeta)]^2,` |
| 974 | 8767-8769 | 0.46 | inline_safe | bracket | `E(\zeta^2)=D(\zeta)+[E(\zeta)]^2=4+25=29.` |
| 976 | 8781-8783 | 0.33 | inline_safe | bracket | `x^2+2x+2=(x+1)^2+1.` |
| 977 | 8785-8789 | 0.42 | normalized_width_not_low | bracket | `1=\int_{-\infty}^{+\infty}\frac{a}{(x+1)^2+1}\,\mathrm{d}x =a\left[\arctan(x+1)\right]_{-\infty}^{+\infty} =a\pi,` |
| 978 | 8791-8793 | 0.14 | inline_safe | bracket | `a=\frac1\pi.` |
| 979 | 8796-8804 | 0.37 | inline_unsafe_marker | bracket | `\begin{aligned} P(\zeta\ge0) &=\int_0^{+\infty}\frac{1/\pi}{(x+1)^2+1}\,\mathrm{d}x\\ &=\frac1\pi\left[\arctan(x+1)\right]_{0}^{+\infty}\\ &=\frac1\pi\left(\frac\pi2-\frac\pi4\r...` |
| 980 | 8809-8815 | 0.15 | inline_unsafe_marker | bracket | `f(x)= \begin{cases} \dfrac{A}{1+x}, & 0\le x\le 3,\\ 0, & x<0\ \text{或}\ x>3. \end{cases}` |
| 981 | 8823-8826 | 0.26 | inline_safe | bracket | `1=\int_0^3\frac{A}{1+x}\,\mathrm{d}x =A\ln4,` |
| 982 | 8828-8830 | 0.17 | inline_safe | bracket | `A=\frac1{\ln4}.` |
| 983 | 8833-8838 | 0.34 | normalized_width_not_low | bracket | `P(\zeta<1)=\int_0^1\frac{A}{1+x}\,\mathrm{d}x =A\ln2 =\frac{\ln2}{\ln4} =\frac12.` |
| 984 | 8841-8850 | 0.38 | inline_unsafe_marker | bracket | `\begin{aligned} E(\zeta) &=\int_0^3 x\frac{A}{1+x}\,\mathrm{d}x\\ &=A\int_0^3\left(1-\frac1{1+x}\right)\,\mathrm{d}x\\ &=A[x-\ln(1+x)]_0^3 =\frac{3-\ln4}{\ln4} =\frac3{\ln4}-1. ...` |
| 985 | 8858-8860 | 0.47 | inline_safe | bracket | `f(x)=\frac{a}{x^2+1},\qquad -\infty<x<+\infty.` |
| 986 | 8865-8867 | 0.36 | inline_safe | bracket | `\int_{-\infty}^{+\infty}\frac{1}{x^2+1}\,\mathrm{d}x=\pi,` |
| 987 | 8869-8871 | 0.42 | inline_safe | bracket | `1=\int_{-\infty}^{+\infty}\frac{a}{x^2+1}\,\mathrm{d}x=a\pi,` |
| 988 | 8873-8875 | 0.14 | inline_safe | bracket | `a=\frac1\pi.` |
| 989 | 8878-8880 | 0.13 | inline_safe | bracket | `\xi=\frac{Y-1}{2},` |
| 990 | 8882-8884 | 0.28 | inline_safe | bracket | `\left\|\frac{\mathrm{d}}{\mathrm{d}y}\frac{y-1}{2}\right\|=\frac12.` |
| 991 | 8886-8894 | 0.38 | inline_unsafe_marker | bracket | `\begin{aligned} f_\eta(y) &=f_\xi\!\left(\frac{y-1}{2}\right)\cdot\frac12\\ &=\frac{1}{\pi\left[\left(\dfrac{y-1}{2}\right)^2+1\right]}\cdot\frac12\\ &=\frac{2}{\pi\bigl[(y-1)^2...` |
| 993 | 8906-8908 | 0.43 | inline_safe | bracket | `E(\xi)=np,\qquad D(\xi)=np(1-p).` |
| 994 | 8910-8912 | 0.19 | inline_safe | bracket | `np(1-p)=2.1.` |
| 995 | 8914-8916 | 0.23 | inline_safe | bracket | `1-p=\frac{2.1}{3}=0.7,` |
| 996 | 8918-8920 | 0.17 | inline_safe | bracket | `n=\frac{3}{0.3}=10.` |
| 997 | 8929-8931 | 0.17 | inline_safe | bracket | `\xi=1,2,3,4,5.` |
| 998 | 8934-8939 | 0.18 | normalized_width_not_low | bracket | `P(\xi=k) =\frac{4}{6}\cdot\frac{3}{5}\cdots \frac{4-(k-2)}{6-(k-2)}\cdot \frac{2}{6-(k-1)},` |
| 999 | 8943-8949 | 0.10 | inline_unsafe_marker | bracket | `\begin{array}{c\|ccccc} \xi & 1 & 2 & 3 & 4 & 5\\ \hline P & \dfrac13 & \dfrac4{15} & \dfrac15 & \dfrac2{15} & \dfrac1{15} \end{array}.` |
| 1001 | 8961-8967 | 0.14 | inline_unsafe_marker | bracket | `f(x)= \begin{cases} 2\sin x, & 0\le x\le A\pi,\\ 0, & \text{其他}. \end{cases}` |
| 1002 | 8978-8980 | 0.27 | inline_safe | bracket | `\int_0^{A\pi}2\sin x\,\mathrm{d}x=1.` |
| 1003 | 8982-8984 | 0.40 | inline_safe | bracket | `2[-\cos x]_0^{A\pi}=2(1-\cos A\pi)=1,` |
| 1004 | 8986-8988 | 0.18 | inline_safe | bracket | `\cos A\pi=\frac12.` |
| 1005 | 8990-8992 | 0.36 | inline_safe | bracket | `A\pi=\frac{\pi}{3},\qquad A=\frac13.` |
| 1006 | 8997-8999 | 0.29 | inline_safe | bracket | `P(X=3)=\frac43 e^{-2},` |
| 1007 | 9004-9006 | 0.27 | inline_safe | bracket | `P(X=3)=e^{-\lambda}\frac{\lambda^3}{3!}.` |
| 1008 | 9008-9010 | 0.33 | inline_safe | bracket | `\frac43 e^{-2}=e^{-2}\frac{2^3}{3!},` |
| 1009 | 9012-9014 | 0.13 | inline_safe | bracket | `EX=\lambda=2.` |
| 1011 | 9026-9028 | 0.37 | inline_safe | bracket | `\sum_{k=1}^{\infty}5A\left(\frac12\right)^k=1.` |
| 1012 | 9030-9032 | 0.34 | inline_safe | bracket | `\sum_{k=1}^{\infty}\left(\frac12\right)^k=1,` |
| 1013 | 9034-9036 | 0.34 | inline_safe | bracket | `5A=1,\qquad A=\frac15.` |
| 1014 | 9041-9048 | 0.18 | inline_unsafe_marker | bracket | `F(x)= \begin{cases} 1-e^{-\lambda x}, & x>0,\\ 0, & x\le0, \end{cases} \qquad \lambda>0.` |
| 1015 | 9053-9055 | 0.29 | inline_safe | bracket | `p(x)=F'(x)=\lambda e^{-\lambda x};` |
| 1016 | 9057-9063 | 0.11 | inline_unsafe_marker | bracket | `p(x)= \begin{cases} \lambda e^{-\lambda x}, & x>0,\\ 0, & x\le0. \end{cases}` |
| 1017 | 9065-9067 | 0.45 | inline_safe | bracket | `E\xi=\frac1\lambda,\qquad D\xi=\frac1{\lambda^2}.` |
| 1018 | 9075-9077 | 0.25 | inline_safe | bracket | `Z=\frac{X-2}{\sigma}\sim N(0,1).` |
| 1019 | 9079-9081 | 0.14 | inline_safe | bracket | `a=\frac2\sigma.` |
| 1021 | 9087-9089 | 0.13 | inline_safe | bracket | `\Phi(a)=0.8.` |
| 1023 | 9100-9102 | 0.14 | inline_safe | bracket | `P(X\le1+\mu)` |
| 1024 | 9113-9117 | 0.29 | normalized_width_not_low | bracket | `P(X\le1+\mu) =P\!\left(\frac{X-\mu}{\sigma}\le\frac{1+\mu-\mu}{\sigma}\right) =\Phi\!\left(\frac1\sigma\right).` |
| 1025 | 9132-9134 | 0.15 | inline_safe | bracket | `P(\xi=x)=0.` |
| 1026 | 9142-9144 | 0.39 | inline_safe | bracket | `X\sim N(0,1),\qquad Y\sim N(1,1).` |
| 1027 | 9155-9157 | 0.18 | inline_safe | bracket | `X+Y\sim N(1,2).` |
| 1028 | 9159-9161 | 0.27 | inline_safe | bracket | `P(X+Y\le1)=\frac12.` |
| 1029 | 9167-9169 | 0.21 | inline_safe | bracket | `P(X<Y)=\,\underline{\hspace{2cm}}.` |
| 1030 | 9180-9182 | 0.48 | inline_safe | bracket | `P(X<Y)=P(Y<X),\qquad P(X=Y)=0.` |
| 1031 | 9184-9186 | 0.38 | inline_safe | bracket | `P(X<Y)+P(Y<X)+P(X=Y)=1,` |
| 1032 | 9188-9190 | 0.21 | inline_safe | bracket | `P(X<Y)=\frac12.` |
| 1033 | 9195-9201 | 0.10 | inline_unsafe_marker | bracket | `\begin{array}{c\|ccccc} X&-2&-1&0&1&2\\ \hline P&a&\dfrac14&\dfrac18&b&\dfrac18 \end{array}` |
| 1034 | 9212-9214 | 0.45 | inline_safe | bracket | `a+b+\frac14+\frac18+\frac18=1,` |
| 1035 | 9216-9218 | 0.18 | inline_safe | bracket | `a+b=\frac12.` |
| 1037 | 9224-9226 | 0.21 | inline_safe | bracket | `EX=\frac12-3a.` |
| 1038 | 9228-9230 | 0.32 | inline_safe | bracket | `EX=\frac12-3a<\frac14,` |
| 1039 | 9236-9242 | 0.21 | inline_unsafe_marker | bracket | `F(x)= \begin{cases} \dfrac12e^x,& x\le0,\\[4pt] 1-\dfrac12e^{-x},& x>0. \end{cases}` |
| 1040 | 9247-9249 | 0.13 | inline_safe | bracket | `\|5\xi-2\|<3` |
| 1041 | 9251-9253 | 0.18 | inline_safe | bracket | `-3<5\xi-2<3,` |
| 1042 | 9255-9257 | 0.20 | inline_safe | bracket | `-\frac15<\xi<1.` |
| 1043 | 9259-9266 | 0.47 | inline_unsafe_marker | bracket | `\begin{aligned} P\{\|5\xi-2\|<3\} &=F(1)-F\!\left(-\frac15\right)\\ &=\left(1-\frac12e^{-1}\right)-\frac12e^{-1/5}\\ &=1-\frac12e^{-1}-\frac12e^{-0.2}. \end{aligned}` |
| 1045 | 9286-9288 | 0.32 | inline_safe | bracket | `\sum_{i=1}^n X_i\sim B(n,p).` |
| 1046 | 9290-9294 | 0.25 | inline_safe | bracket | `\overline X=\frac{k}{n} \quad\Longleftrightarrow\quad \sum_{i=1}^{n}X_i=k.` |
| 1047 | 9296-9300 | 0.32 | normalized_width_not_low | bracket | `P\left\{\overline X=\frac{k}{n}\right\} =P\left\{\sum_{i=1}^{n}X_i=k\right\} =\binom nk p^k(1-p)^{n-k}.` |
| 1048 | 9312-9315 | 0.45 | normalized_width_not_low | bracket | `P(X\le1+\mu)=P\left(\frac{X-\mu}{\sigma}\le \frac{1+\mu-\mu}{\sigma}\right) =\Phi\left(\frac1\sigma\right).` |
| 1049 | 9321-9327 | 0.07 | inline_unsafe_marker | bracket | `\begin{array}{c\|ccc} \xi & 0 & 1 & 2\\ \hline P & 0.25 & 0.35 & 0.40 \end{array}` |
| 1050 | 9339-9341 | 0.18 | inline_safe | bracket | `F(x)=P\{\xi<x\},` |
| 1051 | 9343-9345 | 0.16 | inline_safe | bracket | `0<1<\sqrt2<2,` |
| 1053 | 9359-9361 | 0.17 | inline_safe | bracket | `E(3X+5)=11` |
| 1054 | 9363-9365 | 0.08 | inline_safe | bracket | `EX=2.` |
| 1055 | 9367-9369 | 0.37 | inline_safe | bracket | `P(0<X<2)=P(2<X<4)=0.15.` |
| 1057 | 9378-9386 | 0.14 | inline_unsafe_marker | bracket | `F(x)= \begin{cases} 0, & x\le -1,\\ 0.3, & -1<x\le 1,\\ 0.8, & 1<x\le 3,\\ 1, & x>3. \end{cases}` |
| 1059 | 9395-9401 | 0.07 | inline_unsafe_marker | bracket | `\begin{array}{c\|ccc} X & -1 & 1 & 3\\ \hline P & 0.3 & 0.5 & 0.2 \end{array}` |
| 1063 | 9424-9427 | 0.49 | normalized_width_not_low | bracket | `F(x)=\frac12+\int_0^x\frac12e^{-t}\,\mathrm{d}t =1-\frac12e^{-x}.` |
| 1064 | 9429-9435 | 0.21 | inline_unsafe_marker | bracket | `F(x)= \begin{cases} \dfrac12e^x, & x\le0,\\[4pt] 1-\dfrac12e^{-x}, & x>0. \end{cases}` |
| 1065 | 9438-9445 | 0.45 | inline_unsafe_marker | bracket | `\begin{aligned} P(-5<X<10) &=F(10)-F(-5)\\ &=\left(1-\frac12e^{-10}\right)-\frac12e^{-5}\\ &=1-\frac12(e^{-5}+e^{-10}). \end{aligned}` |
| 1066 | 9448-9450 | 0.08 | inline_safe | bracket | `EX=0.` |
| 1067 | 9452-9455 | 0.48 | normalized_width_not_low | bracket | `EX^2=2\int_0^\infty x^2\cdot\frac12e^{-x}\,\mathrm{d}x =\int_0^\infty x^2e^{-x}\,\mathrm{d}x=2.` |
| 1068 | 9457-9459 | 0.28 | inline_safe | bracket | `DX=EX^2-(EX)^2=2.` |
| 1069 | 9466-9468 | 0.27 | inline_safe | bracket | `Y=a^X\qquad (a>0)` |
| 1070 | 9475-9481 | 0.11 | inline_unsafe_marker | bracket | `F_Y(y)= \begin{cases} 0, & y<1,\\ 1, & y\ge1. \end{cases}` |
| 1071 | 9484-9486 | 0.29 | inline_safe | bracket | `x=\frac{\ln y}{\ln a},\qquad y>0.` |
| 1072 | 9488-9490 | 0.21 | inline_safe | bracket | `\left\|\frac{\mathrm{d}x}{\mathrm{d}y}\right\|=\frac{1}{y\|\ln a\|}.` |
| 1074 | 9496-9505 | 0.26 | inline_unsafe_marker | bracket | `f_Y(y)= \begin{cases} \displaystyle \frac{1}{y\|\ln a\|\,\sigma\sqrt{2\pi}} \exp\!\left[-\frac{\left(\dfrac{\ln y}{\ln a}-\mu\right)^2}{2\sigma^2}\right], & y>0,\\[12pt] 0, & y\le...` |
| 1075 | 9513-9515 | 0.15 | inline_safe | bracket | `\lambda\Delta t+o(\Delta t).` |
| 1076 | 9520-9522 | 0.45 | inline_safe | bracket | `P(t<\xi\le t+\Delta t\,\|\,\xi>t)=\lambda\Delta t+o(\Delta t).` |
| 1077 | 9524-9527 | 0.21 | inline_safe | bracket | `\frac{F(t+\Delta t)-F(t)}{1-F(t)} =\lambda\Delta t+o(\Delta t).` |
| 1078 | 9529-9531 | 0.24 | inline_safe | bracket | `F'(t)=\lambda[1-F(t)].` |
| 1079 | 9533-9535 | 0.42 | inline_safe | bracket | `S'(t)=-\lambda S(t),\qquad S(0)=1.` |
| 1080 | 9537-9539 | 0.18 | inline_safe | bracket | `S(t)=e^{-\lambda t}.` |
| 1081 | 9541-9543 | 0.40 | inline_safe | bracket | `P(\xi>t)=e^{-\lambda t},\qquad t\ge0.` |
| 1082 | 9553-9555 | 0.23 | inline_safe | bracket | `\xi=m,m+1,m+2,\dots.` |
| 1083 | 9557-9560 | 0.41 | normalized_width_not_low | bracket | `P(\xi=k)=\binom{k-1}{m-1}p^m(1-p)^{k-m}, \qquad k=m,m+1,\dots.` |
| 1084 | 9563-9565 | 0.28 | inline_safe | bracket | `\xi=\xi_1+\xi_2+\cdots+\xi_m,` |
| 1085 | 9567-9569 | 0.39 | inline_safe | bracket | `E\xi=\sum_{i=1}^m E\xi_i=\frac mp.` |
| 1086 | 9574-9576 | 0.08 | inline_safe | bracket | `\eta=\|\xi\|` |
| 1087 | 9581-9583 | 0.29 | inline_safe | bracket | `F_\eta(y)=P(\|\xi\|\le y)=0.` |
| 1088 | 9585-9588 | 0.29 | normalized_width_not_low | bracket | `F_\eta(y)=P(-y\le \xi\le y) =F_\xi(y)-F_\xi(-y).` |
| 1089 | 9590-9592 | 0.34 | inline_safe | bracket | `f_\eta(y)=f_\xi(y)+f_\xi(-y).` |
| 1090 | 9594-9603 | 0.23 | normalized_width_not_low | bracket | `f_\eta(y)= \frac{1}{\sigma\sqrt{2\pi}} \left[ \exp\!\left(-\frac{(y-\mu)^2}{2\sigma^2}\right) + \exp\!\left(-\frac{(-y-\mu)^2}{2\sigma^2}\right) \right], \qquad y>0.` |
| 1091 | 9605-9617 | 0.20 | inline_unsafe_marker | bracket | `f_\eta(y)= \begin{cases} \displaystyle \frac{1}{\sigma\sqrt{2\pi}} \left[ \exp\!\left(-\frac{(y-\mu)^2}{2\sigma^2}\right) + \exp\!\left(-\frac{(y+\mu)^2}{2\sigma^2}\right) \righ...` |
| 1092 | 9630-9632 | 0.25 | inline_safe | bracket | `Y=a^{5X}=\exp(5X\ln a)` |
| 1093 | 9634-9636 | 0.31 | inline_safe | bracket | `x=\frac{\ln y}{5\ln a},\qquad y>0,` |
| 1094 | 9638-9640 | 0.25 | inline_safe | bracket | `\left\|\frac{\mathrm dx}{\mathrm dy}\right\|=\frac{1}{5\|\ln a\|\,y}.` |
| 1095 | 9642-9645 | 0.25 | inline_safe | bracket | `f_X(x)=\frac1{\sigma\sqrt{2\pi}} \exp\!\left[-\frac{(x-\mu)^2}{2\sigma^2}\right],` |
| 1096 | 9647-9657 | 0.22 | inline_unsafe_marker | bracket | `f_Y(y)= \begin{cases} \displaystyle \frac{1}{5\|\ln a\|\,y\,\sigma\sqrt{2\pi}} \exp\!\left[ -\frac{\left(\dfrac{\ln y}{5\ln a}-\mu\right)^2}{2\sigma^2} \right], & y>0,\\[14pt] 0,&...` |
| 1097 | 9669-9671 | 0.31 | inline_safe | bracket | `F(x)=\int_{-\infty}^{x}f(t)\,\mathrm{d}t.` |
| 1098 | 9679-9681 | 0.27 | inline_safe | bracket | `x_{k-1}<x_k<x_{k+1}.` |
| 1099 | 9692-9694 | 0.39 | inline_safe | bracket | `P(X=x_k)=F(x_k)-F(x_k-0).` |
| 1100 | 9696-9698 | 0.29 | inline_safe | bracket | `F(x_k-0)=F(x_{k-1}),` |
| 1101 | 9700-9702 | 0.39 | inline_safe | bracket | `P(X=x_k)=F(x_k)-F(x_{k-1}).` |
| 1102 | 9707-9709 | 0.19 | inline_safe | bracket | `Y=\max(X,2003)` |
| 1103 | 9720-9722 | 0.26 | inline_safe | bracket | `F_Y(y)=P(Y\le y)=0.` |
| 1105 | 9728-9730 | 0.34 | inline_safe | bracket | `F_Y(2003)=P(X\le2003)>0,` |
| 1106 | 9732-9734 | 0.22 | inline_safe | bracket | `F_Y(2003-0)=0.` |
| 1107 | 9740-9742 | 0.10 | inline_safe | bracket | `Y=3e^X` |
| 1108 | 9747-9749 | 0.34 | inline_safe | bracket | `x=\ln\frac y3,\qquad y>0.` |
| 1109 | 9751-9753 | 0.20 | inline_safe | bracket | `\left\|\frac{\mathrm{d}x}{\mathrm{d}y}\right\|=\frac1y.` |
| 1110 | 9755-9761 | 0.24 | inline_unsafe_marker | bracket | `f_Y(y)= \begin{cases} \displaystyle \frac1y f\!\left(\ln\frac y3\right), & y>0,\\[8pt] 0, & y\le0. \end{cases}` |
| 1111 | 9766-9768 | 0.23 | inline_safe | bracket | `(X_1,X_2,X_3,X_4)` |
| 1112 | 9770-9772 | 0.19 | inline_safe | bracket | `P(-1<\overline X<5).` |
| 1113 | 9776-9778 | 0.34 | inline_safe | bracket | `\overline X\sim N\left(3,\frac44\right)=N(3,1).` |
| 1114 | 9780-9784 | 0.27 | normalized_width_not_low | bracket | `P(-1<\overline X<5) =P\left(-4<\frac{\overline X-3}{1}<2\right) =\Phi(2)-\Phi(-4).` |
| 1115 | 9786-9788 | 0.39 | inline_safe | bracket | `P(-1<\overline X<5)\approx \Phi(2)=0.9772.` |
| 1116 | 9800-9802 | 0.31 | inline_safe | bracket | `F(x)=\int_{-\infty}^{x}f(t)\,\mathrm{d}t,` |
| 1117 | 9804-9806 | 0.16 | inline_safe | bracket | `f(x)=F'(x).` |
| 1118 | 9814-9816 | 0.16 | inline_safe | bracket | `P(\|X\|>2004).` |
| 1119 | 9826-9828 | 0.33 | inline_safe | bracket | `P(X<-2004)=P(X>2004).` |
| 1120 | 9830-9835 | 0.35 | normalized_width_not_low | bracket | `P(\|X\|>2004) =P(X<-2004)+P(X>2004) =2P(X>2004) =2[1-F(2004)].` |
| 1121 | 9840-9842 | 0.13 | inline_safe | bracket | `Z=\|X-Y\|.` |
| 1122 | 9849-9851 | 0.13 | inline_safe | bracket | `F_Z(z)=0.` |
| 1123 | 9853-9855 | 0.33 | inline_safe | bracket | `2\cdot\frac{(1-z)^2}{2}=(1-z)^2.` |
| 1125 | 9861-9863 | 0.13 | inline_safe | bracket | `F_Z(z)=1.` |
| 1126 | 9865-9872 | 0.13 | inline_unsafe_marker | bracket | `F_Z(z)= \begin{cases} 0, & z<0,\\ 2z-z^2, & 0\le z\le1,\\ 1, & z>1. \end{cases}` |
| 1127 | 9877-9879 | 0.15 | inline_safe | bracket | `P\!\left(\overline X=\frac{k}{n}\right).` |
| 1128 | 9889-9891 | 0.32 | inline_safe | bracket | `\sum_{i=1}^{n}X_i\sim B(n,p).` |
| 1129 | 9893-9895 | 0.36 | inline_safe | bracket | `\overline X=\frac1n\sum_{i=1}^{n}X_i.` |
| 1130 | 9897-9901 | 0.32 | normalized_width_not_low | bracket | `P\!\left(\overline X=\frac{k}{n}\right) =P\!\left(\sum_{i=1}^{n}X_i=k\right) =\binom nk p^k(1-p)^{n-k}.` |
| 1132 | 10021-10023 | 0.29 | inline_safe | bracket | `F(x,y) = P\{X \leqslant x, Y \leqslant y\}` |
| 1133 | 10029-10031 | 0.32 | inline_safe | bracket | `\{(x,y)\mid x\le x_0,\ y\le y_0\}` |
| 1137 | 10056-10058 | 0.13 | inline_unsafe_marker | bracket | `F(x,y) = \begin{cases} 1, & x+y \geqslant 0, \\ 0, & x+y < 0, \end{cases}` |
| 1142 | 10139-10143 | 0.44 | normalized_width_not_low | bracket | `P\{\min(X,Y)\ge 0\}=P\{X\ge 0\}P\{Y\ge 0\} =\frac12\cdot\frac12 =\frac14.` |
| 1144 | 10171-10173 | 0.32 | inline_safe | bracket | `P\{\max(X,Y)\le 1\}=\,\underline{\hspace{2cm}}.` |
| 1145 | 10177-10180 | 0.25 | inline_safe | bracket | `P\{\max(X,Y)\le1\} =P\{X\le1\}P\{Y\le1\}.` |
| 1146 | 10182-10184 | 0.37 | inline_safe | bracket | `P\{X\le1\}=P\{Y\le1\}=\frac13.` |
| 1159 | 10308-10310 | 0.47 | inline_safe | bracket | `P\{X \leqslant x, Y \leqslant y\} = P\{X \leqslant x\} \cdot P\{Y \leqslant y\},` |
| 1160 | 10312-10314 | 0.31 | inline_safe | bracket | `F(x,y) = F_X(x) \cdot F_Y(y),` |
| 1165 | 10378-10380 | 0.29 | inline_safe | bracket | `p_{ij} = p_{i\cdot} \cdot p_{\cdot j}.` |
| 1168 | 10398-10400 | 0.30 | inline_safe | bracket | `f(x,y) = f_X(x) \cdot f_Y(y)` |
| 1174 | 10452-10454 | 0.43 | inline_safe | bracket | `F(x_0, y_0) \neq F_X(x_0) \cdot F_Y(y_0).` |
| 1176 | 10479-10481 | 0.44 | inline_safe | bracket | `f(x) = \frac{1}{2}e^{-\|x\|}, \quad x \in (-\infty, +\infty),` |
| 1177 | 10486-10488 | 0.35 | inline_safe | bracket | `\{X\le 1\},\qquad \{\|X\|\le 1\}.` |
| 1179 | 10500-10507 | 0.33 | inline_unsafe_marker | bracket | `\begin{aligned} P\{\|X\|\le 1\} &=\frac{1}{2}\int_{-1}^{1}e^{-\|x\|}\,\mathrm{d}x =\int_{0}^{1}e^{-x}\,\mathrm{d}x =1-e^{-1}. \end{aligned}` |
| 1182 | 10519-10523 | 0.31 | normalized_width_not_low | bracket | `\left(1-\frac{1}{2}e^{-1}\right)(1-e^{-1}) =1-\frac{3}{2}e^{-1}+\frac{1}{2}e^{-2} \neq 1-e^{-1}.` |
| 1185 | 10589-10591 | 0.49 | inline_safe | bracket | `F(x,y) = \sum_{x_i \leqslant x}\sum_{y_j \leqslant y}p_{ij}.` |
| 1186 | 10594-10596 | 0.44 | inline_safe | bracket | `P\{(X,Y) \in G\} = \sum_{(x_i,y_j) \in G}p_{ij},` |
| 1191 | 10660-10667 | 0.33 | inline_unsafe_marker | bracket | `\begin{aligned} p_{00} &= P\{X_1=0, X_2=0\} = \frac{1}{9}, &\quad p_{01} &= P\{X_1=0, X_2=1\} = \frac{2}{9}, \\ p_{02} &= P\{X_1=0, X_2=2\} = \frac{1}{9}, &\quad p_{10} &= P\{X_...` |
| 1192 | 10686-10690 | 0.29 | display_environment | env:align* | `P\{X_1=0 \mid X_2=1\} &= \frac{p_{01}}{p_{\cdot 1}} = \frac{2/9}{4/9} = \frac{1}{2}\\ P\{X_1=1 \mid X_2=1\} &= \frac{p_{11}}{p_{\cdot 1}} = \frac{2/9}{4/9} = \frac{1}{2}\\ P\{X_...` |
| 1193 | 10712-10714 | 0.42 | inline_safe | bracket | `0.4 + a + b + 0.1 = 1 \implies a + b = 0.5.` |
| 1201 | 10786-10788 | 0.34 | inline_safe | bracket | `P\{X_2=0,\ X_1=-1\}=\frac{1}{4},` |
| 1202 | 10790-10794 | 0.29 | normalized_width_not_low | bracket | `P\{X_2=0\}\,P\{X_1=-1\} =\frac{1}{2}\times\frac{1}{4} =\frac{1}{8}.` |
| 1203 | 10798-10800 | 0.22 | inline_safe | bracket | `Z\in\{-2,-1,0,1\}.` |
| 1205 | 10808-10810 | 0.09 | inline_unsafe_marker | bracket | `Z \sim \begin{pmatrix} -2 & -1 & 0 & 1 \\ 0 & 3/4 & 0 & 1/4 \end{pmatrix}.` |
| 1206 | 10817-10824 | 0.23 | inline_unsafe_marker | bracket | `\begin{array}{c\|ccc} X_i&-1&0&1\\ \hline P&\dfrac14&\dfrac12&\dfrac14 \end{array} \qquad (i=1,2),` |
| 1207 | 10835-10837 | 0.23 | inline_safe | bracket | `P\{X_1X_2=0\}=1,` |
| 1210 | 10848-10850 | 0.49 | inline_safe | bracket | `P\{X_2=0,\ X_1\ne0\}=P\{X_1\ne0\}=\frac12.` |
| 1211 | 10852-10854 | 0.28 | inline_safe | bracket | `P\{X_1=0,X_2=0\}=0.` |
| 1212 | 10857-10859 | 0.47 | inline_safe | bracket | `P\{X_1=X_2\}=P\{X_1=0,X_2=0\}=0.` |
| 1215 | 10875-10883 | 0.47 | inline_unsafe_marker | bracket | `\begin{aligned} P(X=Y) &=P(X=0,Y=0)+P(X=1,Y=1)\\ &=\frac13\cdot\frac13+\frac23\cdot\frac23 =\frac19+\frac49 =\frac59. \end{aligned}` |
| 1216 | 10891-10899 | 0.07 | inline_unsafe_marker | bracket | `\begin{array}{c\|ccc} Y \backslash X & -1 & 0 & 1\\ \hline 0 & a & 0 & 0.1\\ 1 & 0.1 & 0.2 & 0\\ 2 & 0.2 & 0.1 & 0.2 \end{array}` |
| 1217 | 10907-10909 | 0.48 | inline_safe | bracket | `a+0.1+0.1+0.2+0.2+0.1+0.2=1,` |
| 1218 | 10911-10913 | 0.09 | inline_safe | bracket | `a=0.1.` |
| 1219 | 10916-10918 | 0.32 | inline_safe | bracket | `(-1,0),\qquad (-1,1).` |
| 1221 | 10925-10932 | 0.44 | inline_unsafe_marker | bracket | `\begin{aligned} E(XY) &=(-1)\cdot1\cdot0.1+(-1)\cdot2\cdot0.2 +1\cdot2\cdot0.2\\ &=-0.1-0.4+0.4=-0.1. \end{aligned}` |
| 1222 | 10939-10946 | 0.07 | inline_unsafe_marker | bracket | `\begin{array}{c\|ccc} X\backslash Y & -1 & 0 & 1\\ \hline 0 & 0.1 & 0.3 & 0.1\\ 1 & 0.2 & 0.2 & 0.1 \end{array}` |
| 1224 | 10955-10961 | 0.08 | inline_unsafe_marker | bracket | `Z_1\sim \begin{pmatrix} 0 & 1\\ 0.7 & 0.3 \end{pmatrix}.` |
| 1226 | 10967-10973 | 0.08 | inline_unsafe_marker | bracket | `Z_2\sim \begin{pmatrix} 0 & 1\\ 0.5 & 0.5 \end{pmatrix}.` |
| 1227 | 10975-10978 | 0.44 | normalized_width_not_low | bracket | `EX=P(X=1)=0.2+0.2+0.1=0.5, \qquad E(Y^2)=P(Y^2=1)=0.5,` |
| 1228 | 10979-10981 | 0.34 | inline_safe | bracket | `E(XY^2)=P(XY^2=1)=0.3.` |
| 1229 | 10983-10987 | 0.31 | normalized_width_not_low | bracket | `\operatorname{Cov}(X,Y^2) =E(XY^2)-EX\,E(Y^2) =0.3-0.5\cdot0.5=0.05.` |
| 1230 | 10994-11006 | 0.21 | inline_unsafe_marker | bracket | `X= \begin{cases} 1, & \text{若取出的产品是一等品},\\ 0, & \text{否则}, \end{cases} \qquad Y= \begin{cases} 1, & \text{若取出的产品是一等品或二等品},\\ 0, & \text{否则}. \end{cases}` |
| 1231 | 11011-11013 | 0.38 | inline_safe | bracket | `P(X^2=0,Y=0)=P(\text{三等品})=0.1,` |
| 1232 | 11014-11016 | 0.38 | inline_safe | bracket | `P(X^2=0,Y=1)=P(\text{二等品})=0.2,` |
| 1233 | 11017-11020 | 0.38 | normalized_width_not_low | bracket | `P(X^2=1,Y=0)=0,\qquad P(X^2=1,Y=1)=P(\text{一等品})=0.7.` |
| 1234 | 11022-11029 | 0.07 | inline_unsafe_marker | bracket | `\begin{array}{c\|cc} X^2\backslash Y & 0 & 1\\ \hline 0 & 0.1 & 0.2\\ 1 & 0 & 0.7 \end{array}` |
| 1236 | 11036-11039 | 0.39 | normalized_width_not_low | bracket | `\operatorname{Cov}(X^2,Y)=E(X^2Y)-E(X^2)EY =0.7-0.7\cdot0.9=0.07.` |
| 1237 | 11046-11054 | 0.07 | inline_unsafe_marker | bracket | `\begin{array}{c\|ccc} X\backslash Y & -1 & 0 & 1\\ \hline -1 & a & 0 & 0.2\\ 0 & 0.1 & b & 0.2\\ 1 & 0 & 0.1 & c \end{array}` |
| 1238 | 11056-11058 | 0.27 | inline_safe | bracket | `P\{Y\le0\mid X\le0\}=0.5.` |
| 1241 | 11074-11076 | 0.19 | inline_safe | bracket | `-a+c=-0.1.` |
| 1242 | 11078-11082 | 0.22 | inline_safe | bracket | `\frac{P\{Y\le0,\ X\le0\}}{P\{X\le0\}} =\frac{a+b+0.1}{a+b+0.5} =0.5,` |
| 1243 | 11084-11086 | 0.14 | inline_safe | bracket | `a+b=0.3.` |
| 1245 | 11093-11099 | 0.10 | inline_unsafe_marker | bracket | `\begin{array}{c\|ccccc} Z & -2 & -1 & 0 & 1 & 2\\ \hline P & 0.2 & 0.1 & 0.3 & 0.3 & 0.1 \end{array}` |
| 1246 | 11102-11104 | 0.46 | inline_safe | bracket | `P\{X=Z\}=P\{Y=0\}=0+b+0.1=0.2.` |
| 1249 | 11156-11158 | 0.09 | inline_unsafe_marker | bracket | `Z \sim \begin{pmatrix} -1 & 0 & 1 \\ 0.1344 & 0.7312 & 0.1344 \end{pmatrix}.` |
| 1250 | 11178-11180 | 0.25 | inline_safe | bracket | `p_{ij}=p_{i\cdot}p_{\cdot j}.` |
| 1251 | 11184-11188 | 0.32 | normalized_width_not_low | bracket | `p_{21}=p_{2\cdot}p_{\cdot 1}=\frac{1}{8}, \qquad p_{\cdot 1}=\frac{1}{6},` |
| 1252 | 11190-11192 | 0.25 | inline_safe | bracket | `p_{2\cdot}=\frac{1/8}{1/6}=\frac{3}{4}.` |
| 1253 | 11194-11196 | 0.41 | inline_safe | bracket | `p_{1\cdot}=1-p_{2\cdot}=1-\frac{3}{4}=\frac{1}{4}.` |
| 1254 | 11199-11201 | 0.32 | inline_safe | bracket | `p_{12}=p_{1\cdot}p_{\cdot 2}=\frac{1}{8},` |
| 1255 | 11203-11205 | 0.25 | inline_safe | bracket | `p_{\cdot 2}=\frac{1/8}{1/4}=\frac{1}{2}.` |
| 1257 | 11225-11228 | 0.38 | normalized_width_not_low | bracket | `\frac{1}{24}+\frac{1}{8}+\frac{1}{12}=\frac{1}{4},\qquad \frac{1}{8}+\frac{3}{8}+\frac{1}{4}=\frac{3}{4},` |
| 1258 | 11230-11234 | 0.30 | normalized_width_not_low | bracket | `\frac{1}{24}+\frac{1}{8}=\frac{1}{6},\qquad \frac{1}{8}+\frac{3}{8}=\frac{1}{2},\qquad \frac{1}{12}+\frac{1}{4}=\frac{1}{3}.` |
| 1259 | 11265-11269 | 0.28 | display_environment | env:align* | `P\{X_1=1 \mid X_2=2\} =& \frac{p_{12}}{p_{\cdot 2}} = \frac{1/6}{1/4} = \frac{2}{3}\\ P\{X_1=2 \mid X_2=2\} = &\frac{p_{22}}{p_{\cdot 2}} = \frac{0}{1/4} = 0\\ P\{X_1=3 \mid X_2...` |
| 1261 | 11277-11279 | 0.06 | inline_unsafe_marker | bracket | `Y \sim \begin{pmatrix} 1 & 2 & 3 & 6 \\ 1/6 & 1/3 & 1/3 & 1/6 \end{pmatrix}.` |
| 1263 | 11301-11303 | 0.09 | inline_unsafe_marker | bracket | `Z \sim \begin{pmatrix} -2 & -1 & 0 & 1 \\ 1/6 & 1/6 & 1/3 & 1/3 \end{pmatrix}.` |
| 1264 | 11305-11310 | 0.37 | display_environment | env:align* | `(X,Y)=(-1,-1) &: U=-1,\ V=-1, \quad P = 1/3. \\ (X,Y)=(-1,1) &: U=1,\ V=-1, \quad P = 1/6. \\ (X,Y)=(0,-1) &: U=0,\ V=-1, \quad P = 1/3. \\ (X,Y)=(0,1) &: U=1,\ V=0, \quad P = 1/6.` |
| 1265 | 11323-11325 | 0.11 | inline_unsafe_marker | bracket | `UV \sim \begin{pmatrix} -1 & 0 & 1 \\ 1/6 & 1/2 & 1/3 \end{pmatrix}.` |
| 1266 | 11331-11333 | 0.19 | inline_unsafe_marker | bracket | `X = \begin{cases} 1, & A \text{发生}, \\ 0, & A \text{不发生}, \end{cases} \quad Y = \begin{cases} 1, & B \text{发生}, \\ 0, & B \text{不发生}. \end{cases}` |
| 1269 | 11360-11362 | 0.07 | inline_unsafe_marker | bracket | `Z \sim \begin{pmatrix} 0 & 1 & 2 \\ 2/3 & 1/4 & 1/12 \end{pmatrix}.` |
| 1271 | 11373-11375 | 0.11 | inline_unsafe_marker | bracket | `Z = \begin{cases} 1, & X+Y \text{为偶数}, \\ 0, & X+Y \text{为奇数}. \end{cases}` |
| 1273 | 11384-11386 | 0.30 | inline_safe | bracket | `p^2 = p\left[(1-p)^2+p^2\right].` |
| 1279 | 11455-11458 | 0.46 | normalized_width_not_low | bracket | `P(X=0)=P(Y=0)=\frac13,\qquad P(X=1)=P(Y=1)=\frac23.` |
| 1280 | 11460-11467 | 0.47 | inline_unsafe_marker | bracket | `\begin{aligned} P(X=Y) &=P(X=0,Y=0)+P(X=1,Y=1)\\ &=\frac13\cdot\frac13+\frac23\cdot\frac23\\ &=\frac59. \end{aligned}` |
| 1282 | 11476-11478 | 0.43 | inline_safe | bracket | `U=\max(X,Y),\qquad V=\min(X,Y).` |
| 1284 | 11493-11504 | 0.09 | inline_unsafe_marker | bracket | `\begin{array}{c\|cc\|c} \toprule U\backslash V & 1 & 2 & p_{i\cdot}\\ \midrule 1 & \dfrac49 & 0 & \dfrac49\\[4pt] 2 & \dfrac49 & \dfrac19 & \dfrac59\\ \midrule p_{\cdot j} & \dfra...` |
| 1287 | 11514-11519 | 0.24 | normalized_width_not_low | bracket | `\operatorname{Cov}(U,V) =E(UV)-EU\,EV =\frac{16}{9}-\frac{14}{9}\cdot\frac{10}{9} =\frac4{81}.` |
| 1288 | 11530-11533 | 0.42 | normalized_width_not_low | bracket | `P(X=i,Y=j)=\frac{2!}{i!\,j!\,(2-i-j)!} \left(\frac13\right)^2.` |
| 1289 | 11535-11545 | 0.09 | inline_unsafe_marker | bracket | `\begin{array}{c\|ccc} \toprule X\backslash Y & 0 & 1 & 2\\ \midrule 0 & \dfrac19 & \dfrac29 & \dfrac19\\[4pt] 1 & \dfrac29 & \dfrac29 & 0\\[4pt] 2 & \dfrac19 & 0 & 0\\ \bottomrul...` |
| 1290 | 11547-11549 | 0.34 | inline_safe | bracket | `P(X=0)=P(Y=0)=\frac49.` |
| 1292 | 11557-11573 | 0.11 | inline_unsafe_marker | bracket | `\begin{array}{c\|ccc} \toprule u & 0 & 1 & 2\\ \midrule P(U=u) & \dfrac19 & \dfrac69 & \dfrac29\\ \bottomrule \end{array} \qquad \begin{array}{c\|ccc} \toprule v & 0 & 1 & 2\\ \mi...` |
| 1293 | 11580-11582 | 0.30 | inline_unsafe_marker | bracket | `X = \begin{cases} 1, & X_1+X_2=1, \\ 0, & X_1+X_2\neq 1, \end{cases} \quad Y = \begin{cases} 1, & X_2+X_3=1, \\ 0, & X_2+X_3\neq 1. \end{cases}` |
| 1294 | 11590-11592 | 0.29 | inline_safe | bracket | `P(X=1,Y=1) = 2e^{-3}.` |
| 1299 | 11672-11674 | 0.42 | inline_safe | bracket | `P\{(X,Y) \in G\} = \iint_G f(x,y)\,\mathrm{d}x\,\mathrm{d}y;` |
| 1300 | 11676-11678 | 0.26 | inline_safe | bracket | `f(x,y) = \frac{\partial^2 F(x,y)}{\partial x\,\partial y}.` |
| 1301 | 11692-11694 | 0.33 | inline_safe | bracket | `\iint\limits_{\mathbb{R}^2} f(x,y) \,\mathrm{d}x\,\mathrm{d}y = 1` |
| 1302 | 11696-11698 | 0.46 | inline_safe | bracket | `\int_{0}^{+\infty} \left( \int_{0}^{y} A e^{-y} \,\mathrm{d}x \right) \mathrm{d}y = 1` |
| 1304 | 11704-11706 | 0.21 | inline_safe | bracket | `A \times 1 = 1 \implies A = 1` |
| 1305 | 11708-11710 | 0.36 | inline_safe | bracket | `P\{X+Y \geqslant 1\} = 1 - P\{X+Y < 1\}` |
| 1306 | 11712-11717 | 0.19 | inline_unsafe_marker | bracket | `\begin{cases} 0 < x < y & \text{(密度函数非零的固有条件)} \\ x + y < 1 & \text{(题目要求的事件条件)} \end{cases}` |
| 1310 | 11739-11741 | 0.34 | inline_safe | bracket | `P\{X/Y \leqslant 1/2\} = \frac{1}{2} \times 1 = \frac{1}{2}` |
| 1311 | 11749-11753 | 0.38 | inline_unsafe_marker | bracket | `f_X(x) = \begin{cases} 4e^{-4x}, & x > 0 \\ 0, & x \leqslant 0 \end{cases} \quad \text{与} \quad F_X(x) = P\{X \leqslant x\} = \begin{cases} 1 - e^{-4x}, & x > 0 \\ 0, & x \leqsl...` |
| 1312 | 11756-11758 | 0.28 | inline_safe | bracket | `P\{X\in A\mid Y=y\}=P\{X\in A\},` |
| 1313 | 11760-11762 | 0.47 | inline_safe | bracket | `P(\{X\in A\}\cap\{Y=y\})=P\{X\in A\}\cdot P\{Y=y\}.` |
| 1319 | 11792-11794 | 0.18 | inline_safe | bracket | `P\{X \geqslant -2\} = 1` |
| 1327 | 11840-11842 | 0.18 | inline_unsafe_marker | bracket | `f_X(x) = \begin{cases} 3x^2, & 0 < x < 1, \\ 0, & \text{其他}, \end{cases}` |
| 1328 | 11844-11846 | 0.25 | inline_unsafe_marker | bracket | `f_{Y\|X}(y\|x) = \begin{cases} \dfrac{3y^2}{x^3}, & 0 < y < x, \\ 0, & \text{其他}. \end{cases}` |
| 1331 | 11869-11871 | 0.26 | inline_safe | bracket | `f_{Y\|X}(y\|x) = \frac{f(x,y)}{f_X(x)}` |
| 1332 | 11875-11877 | 0.26 | inline_safe | bracket | `f_{X\|Y}(x\|y) = \frac{f(x,y)}{f_Y(y)}` |
| 1335 | 11910-11916 | 0.20 | inline_unsafe_marker | bracket | `f(x,y)= \begin{cases} A, & 0<x<2,\ \|y\|<x,\\ 0, & \text{其他}. \end{cases}` |
| 1336 | 11924-11928 | 0.40 | normalized_width_not_low | bracket | `1=\int_0^2\int_{-x}^{x}A\,\mathrm dy\,\mathrm dx =\int_0^2 2Ax\,\mathrm dx =4A,` |
| 1337 | 11932-11934 | 0.46 | inline_safe | bracket | `f_X(x)=\int_{-x}^{x}\frac14\,\mathrm dy=\frac{x}{2}.` |
| 1338 | 11936-11943 | 0.26 | inline_unsafe_marker | bracket | `f_{Y\|X}(y\|x)=\frac{f(x,y)}{f_X(x)} = \begin{cases} \dfrac1{2x}, & -x<y<x,\ 0<x<2,\\[4pt] 0, & \text{其他}. \end{cases}` |
| 1340 | 11950-11952 | 0.35 | inline_safe | bracket | `\operatorname{Cov}(X,Y)=E(XY)-EX\,EY=0.` |
| 1341 | 11958-11960 | 0.19 | inline_unsafe_marker | bracket | `f(x,y) = \begin{cases} e^{-y}, & x > 0,\ y > x, \\ 0, & \text{其他}, \end{cases}` |
| 1346 | 11986-11988 | 0.27 | inline_unsafe_marker | bracket | `f(x,y) = \begin{cases} A(6-x-y), & 0 \leqslant x \leqslant 2,\ 2 \leqslant y \leqslant 4, \\ 0, & \text{其他}. \end{cases}` |
| 1356 | 12063-12067 | 0.16 | inline_unsafe_marker | bracket | `F_Y(y) = \begin{cases} 0, & y \leqslant 0, \\ \dfrac{3y}{4}, & 0 < y \leqslant 1, \\ \dfrac{1}{2} + \dfrac{y}{4}, & 1 < y \leqslant 2, \\ 1, & y \geqslant 2. \end{cases} \qquad ...` |
| 1357 | 12077-12079 | 0.18 | inline_unsafe_marker | bracket | `f(x,y) = \begin{cases} \dfrac{1}{S_D}, & (x,y) \in D, \\ 0, & \text{其他}, \end{cases}` |
| 1358 | 12084-12086 | 0.24 | inline_safe | bracket | `P\{(X,Y) \in G\} = \frac{S_G}{S_D}.` |
| 1361 | 12114-12120 | 0.11 | inline_unsafe_marker | bracket | `f(x,y)= \begin{cases} \dfrac12, & (x,y)\in D,\\[4pt] 0, & \text{其他}. \end{cases}` |
| 1362 | 12123-12126 | 0.41 | normalized_width_not_low | bracket | `f_X(x)=\int_0^{1/x}\frac12\,\mathrm dy =\frac1{2x},\qquad 1\le x\le e^2.` |
| 1363 | 12128-12135 | 0.23 | inline_unsafe_marker | bracket | `f_Y(y)= \begin{cases} \dfrac12(e^2-1), & 0\le y\le e^{-2},\\[6pt] \dfrac1{2y}-\dfrac12, & e^{-2}<y\le1,\\[6pt] 0, & \text{其他}. \end{cases}` |
| 1364 | 12139-12141 | 0.36 | inline_safe | bracket | `P(X+Y\ge2)=1-P(X+Y<2).` |
| 1366 | 12156-12162 | 0.20 | inline_unsafe_marker | bracket | `f(x,y)= \begin{cases} e^{-y}, & 0\le x\le1,\ y>0,\\ 0, & \text{其他}. \end{cases}` |
| 1367 | 12169-12171 | 0.42 | inline_safe | bracket | `f_\xi(x)=\int_0^{+\infty}e^{-y}\,\mathrm dy=1;` |
| 1368 | 12173-12179 | 0.13 | inline_unsafe_marker | bracket | `f_\xi(x)= \begin{cases} 1, & 0\le x\le1,\\ 0, & \text{其他}. \end{cases}` |
| 1369 | 12181-12183 | 0.45 | inline_safe | bracket | `f_\eta(y)=\int_0^1 e^{-y}\,\mathrm dx=e^{-y};` |
| 1370 | 12185-12191 | 0.11 | inline_unsafe_marker | bracket | `f_\eta(y)= \begin{cases} e^{-y}, & y>0,\\ 0, & \text{其他}. \end{cases}` |
| 1371 | 12194-12196 | 0.28 | inline_safe | bracket | `f(x,y)=f_\xi(x)f_\eta(y),` |
| 1375 | 12212-12219 | 0.16 | inline_unsafe_marker | bracket | `f_\zeta(z)= \begin{cases} 1-e^{-z}, & 0<z<1,\\ (e-1)e^{-z}, & z\ge1,\\ 0, & \text{其他}. \end{cases}` |
| 1377 | 12233-12237 | 0.47 | normalized_width_not_low | bracket | `1=\int_0^1\int_0^x Ay(1-x)\,\mathrm dy\,\mathrm dx =\frac A2\int_0^1 x^2(1-x)\,\mathrm dx =\frac A{24},` |
| 1378 | 12239-12241 | 0.08 | inline_safe | bracket | `A=24.` |
| 1379 | 12244-12251 | 0.47 | inline_unsafe_marker | bracket | `\begin{aligned} F(x,y) &=\int_0^y\int_0^u 24v(1-u)\,\mathrm dv\,\mathrm du +\int_y^x\int_0^y 24v(1-u)\,\mathrm dv\,\mathrm du\\ &=3y^4-8y^3+12\left(x-\frac{x^2}{2}\right)y^2. \e...` |
| 1381 | 12258-12260 | 0.35 | inline_safe | bracket | `F(x,y)=3y^4-8y^3+6y^2.` |
| 1382 | 12262-12271 | 0.38 | inline_unsafe_marker | bracket | `F(x,y)= \begin{cases} 0, & x<0\ \text{或}\ y<0,\\[3pt] 3y^4-8y^3+12\left(x-\dfrac{x^2}{2}\right)y^2, & 0\le x<1,\ 0\le y<x,\\[6pt] 3y^4-8y^3+6y^2, & x\ge1,\ 0\le y<1,\\[6pt] 4x^3...` |
| 1383 | 12278-12280 | 0.31 | inline_safe | bracket | `D=\{(x,y)\mid x^2+y^2\le1\}` |
| 1384 | 12288-12294 | 0.18 | inline_unsafe_marker | bracket | `\varphi(x,y)= \begin{cases} \dfrac1\pi, & x^2+y^2\le1,\\[6pt] 0, & \text{其他}. \end{cases}` |
| 1385 | 12297-12299 | 0.33 | inline_safe | bracket | `-\sqrt{1-x^2}<y<\sqrt{1-x^2}.` |
| 1387 | 12307-12313 | 0.16 | inline_unsafe_marker | bracket | `\varphi_\xi(x)= \begin{cases} \dfrac{2}{\pi}\sqrt{1-x^2}, & \|x\|<1,\\[6pt] 0, & \text{其他}. \end{cases}` |
| 1388 | 12315-12321 | 0.16 | inline_unsafe_marker | bracket | `\varphi_\eta(y)= \begin{cases} \dfrac{2}{\pi}\sqrt{1-y^2}, & \|y\|<1,\\[6pt] 0, & \text{其他}. \end{cases}` |
| 1390 | 12328-12330 | 0.35 | inline_safe | bracket | `\operatorname{Cov}(\xi,\eta)=E(\xi\eta)-E\xi\,E\eta=0,` |
| 1391 | 12334-12336 | 0.26 | inline_safe | bracket | `\varphi(x,y)\ne \varphi_\xi(x)\varphi_\eta(y),` |
| 1393 | 12354-12356 | 0.34 | inline_unsafe_marker | bracket | `f(x,y) = \begin{cases} 3/4, & -1 < x < 1,\ 0 \leqslant y \leqslant 1-x^2, \\ 0, & \text{其他}. \end{cases}` |
| 1396 | 12365-12367 | 0.41 | inline_unsafe_marker | bracket | `f_{Y\|X}(y\|x) = \frac{f(x,y)}{f_X(x)} = \begin{cases} \dfrac{1}{1-x^2}, & 0 \leqslant y \leqslant 1-x^2, \\ 0, & \text{其他}. \end{cases}` |
| 1399 | 12403-12403 | 0.24 | inline_unsafe_marker | bracket | `f(x,y) = \begin{cases} kx^2, & 0 < x < 1,\ x^2 < y < 1, \\ 0, & \text{其他}. \end{cases}` |
| 1405 | 12429-12429 | 0.22 | inline_unsafe_marker | bracket | `f(x,y) = \begin{cases} 2-x-y, & 0 < x < 1,\ 0 < y < 1, \\ 0, & \text{其他}. \end{cases}` |
| 1408 | 12442-12444 | 0.47 | inline_safe | bracket | `f_Z(z) = \int_0^z(2-z)\,\mathrm{d}x = z(2-z).` |
| 1410 | 12450-12452 | 0.21 | inline_unsafe_marker | bracket | `f_Z(z) = \begin{cases} z(2-z), & 0 < z < 1, \\ (2-z)^2, & 1 \leqslant z < 2, \\ 0, & \text{其他}. \end{cases}` |
| 1411 | 12463-12465 | 0.31 | inline_unsafe_marker | bracket | `f(x,y) = \begin{cases} 1, & 0 \leqslant y \leqslant 1,\ y \leqslant x \leqslant 2-y, \\ 0, & \text{其他}. \end{cases}` |
| 1412 | 12471-12473 | 0.13 | inline_unsafe_marker | bracket | `f_X(x) = \begin{cases} x, & 0 < x < 1, \\ 2-x, & 1 < x < 2, \\ 0, & \text{其他}. \end{cases}` |
| 1413 | 12478-12480 | 0.19 | inline_unsafe_marker | bracket | `f_Y(y) = \begin{cases} 2-2y, & 0 < y < 1, \\ 0, & \text{其他}. \end{cases}` |
| 1415 | 12486-12488 | 0.26 | inline_unsafe_marker | bracket | `f_{X\|Y}(x\|y) = \begin{cases} \dfrac{1}{2-2y}, & y \leqslant x \leqslant 2-y, \\ 0, & \text{其他}. \end{cases}` |
| 1416 | 12500-12502 | 0.13 | inline_unsafe_marker | bracket | `f_X(x) = \begin{cases} 1, & 0 < x < 1, \\ 0, & \text{其他}. \end{cases}` |
| 1417 | 12504-12506 | 0.21 | inline_unsafe_marker | bracket | `f_{Y\|X}(y\|x) = \begin{cases} \dfrac{1}{x}, & 0 < y < x, \\ 0, & \text{其他}. \end{cases}` |
| 1418 | 12508-12510 | 0.15 | inline_unsafe_marker | bracket | `f(x,y) = \begin{cases} \dfrac{1}{x}, & 0 < y < x < 1, \\ 0, & \text{其他}. \end{cases}` |
| 1420 | 12516-12518 | 0.19 | inline_unsafe_marker | bracket | `f_Y(y) = \begin{cases} -\ln y, & 0 < y < 1, \\ 0, & \text{其他}. \end{cases}` |
| 1425 | 12551-12553 | 0.44 | inline_safe | bracket | `(X,Y) \sim N(\mu_1, \mu_2, \sigma_1^2, \sigma_2^2; 0).` |
| 1428 | 12587-12589 | 0.25 | inline_unsafe_marker | bracket | `f(x,y) = \begin{cases} 2, & 0 < x < 1,\ 0 < y < 1-x, \\ 0, & \text{其他}, \end{cases}` |
| 1429 | 12599-12601 | 0.45 | inline_unsafe_marker | bracket | `f(x,y) = f_X(x)\,f_Y(y) = \begin{cases} e^{-(x+y)}, & x > 0,\ y > 0, \\ 0, & \text{其他}. \end{cases}` |
| 1435 | 12662-12664 | 0.37 | inline_safe | bracket | `Z = X + Y \sim B(2+4, p) = B(6, p).` |
| 1439 | 12691-12693 | 0.29 | inline_unsafe_marker | bracket | `Y_1 \sim \begin{pmatrix} 0 & 1 & 2 \\ 1/9 & 4/9 & 4/9 \end{pmatrix}, \qquad Y_2 \sim \begin{pmatrix} -2 & -1 & 0 & 1 & 2 \\ 1/9 & 2/9 & 1/3 & 2/9 & 1/9 \end{pmatrix}.` |
| 1441 | 12731-12733 | 0.33 | inline_safe | bracket | `\max\{X, Y\} \leqslant z \iff X \leqslant z \text{ 且 } Y \leqslant z,` |
| 1443 | 12746-12748 | 0.16 | inline_unsafe_marker | bracket | `F_Z(z) = \begin{cases} 0, & z \leqslant 0, \\ z(1 - e^{-z}), & 0 < z < 1, \\ 1 - e^{-z}, & z \geqslant 1. \end{cases}` |
| 1444 | 12753-12765 | 0.13 | inline_unsafe_marker | bracket | `f_X(x)= \begin{cases} 1, & 0\le x\le1,\\ 0, & \text{其他}, \end{cases} \qquad f_Y(y)= \begin{cases} e^{-y}, & y>0,\\ 0, & \text{其他}. \end{cases}` |
| 1445 | 12767-12773 | 0.15 | inline_unsafe_marker | bracket | `Z=g(X,Y)= \begin{cases} 1, & X\le Y,\\ 0, & X>Y. \end{cases}` |
| 1446 | 12778-12780 | 0.29 | inline_safe | bracket | `EZ=P(Z=1)=P(X\le Y).` |
| 1448 | 12786-12790 | 0.47 | normalized_width_not_low | bracket | `P(X\le Y)=\int_0^1 P(Y\ge x)f_X(x)\,\mathrm dx =\int_0^1 e^{-x}\,\mathrm dx =1-e^{-1}.` |
| 1449 | 12792-12794 | 0.18 | inline_safe | bracket | `EZ=1-e^{-1}.` |
| 1450 | 12796-12798 | 0.28 | inline_safe | bracket | `DZ=(1-e^{-1})e^{-1}.` |
| 1451 | 12803-12809 | 0.11 | inline_unsafe_marker | bracket | `f_X(x)= \begin{cases} \lambda e^{-\lambda x}, & x>0,\\ 0, & x\le0. \end{cases}` |
| 1452 | 12811-12813 | 0.19 | inline_safe | bracket | `Y=\max\{X^2,4\}.` |
| 1453 | 12818-12820 | 0.27 | inline_safe | bracket | `F_Y(y)=P\{Y\le y\}=0.` |
| 1455 | 12826-12830 | 0.31 | normalized_width_not_low | bracket | `F_Y(y)=P\{0<X\le\sqrt y\} =\int_0^{\sqrt y}\lambda e^{-\lambda x}\,\mathrm dx =1-e^{-\lambda\sqrt y}.` |
| 1456 | 12832-12838 | 0.17 | inline_unsafe_marker | bracket | `F_Y(y)= \begin{cases} 0, & y<4,\\ 1-e^{-\lambda\sqrt y}, & y\ge4. \end{cases}` |
| 1458 | 12847-12853 | 0.11 | inline_unsafe_marker | bracket | `f_X(x)= \begin{cases} \lambda e^{-\lambda x}, & x>0,\\ 0, & x\le0. \end{cases}` |
| 1459 | 12855-12861 | 0.12 | inline_unsafe_marker | bracket | `Y=g(X)= \begin{cases} X, & X>1,\\ 2X, & X\le1. \end{cases}` |
| 1460 | 12866-12868 | 0.44 | inline_safe | bracket | `F_Y(y)=P\{X\le y/2\}=1-e^{-\lambda y/2}.` |
| 1461 | 12871-12878 | 0.46 | inline_unsafe_marker | bracket | `\begin{aligned} F_Y(y) &=P\{2X\le y,\ X\le1\}+P\{X\le y,\ X>1\}\\ &=P\{X\le y/2\}+P\{1<X\le y\}\\ &=(1-e^{-\lambda y/2})+(e^{-\lambda}-e^{-\lambda y}). \end{aligned}` |
| 1462 | 12880-12886 | 0.38 | inline_unsafe_marker | bracket | `F_Y(y)= \begin{cases} 1-e^{-\lambda y/2}, & 0<y\le1,\\ 1+e^{-\lambda}-e^{-\lambda y/2}-e^{-\lambda y}, & 1<y\le2. \end{cases}` |
| 1463 | 12891-12897 | 0.05 | inline_unsafe_marker | bracket | `X\sim \begin{pmatrix} 1 & 2\\ 0.3 & 0.7 \end{pmatrix},` |
| 1465 | 12910-12912 | 0.39 | inline_safe | bracket | `G(u)=0.3F(u-1)+0.7F(u-2).` |
| 1466 | 12914-12916 | 0.39 | inline_safe | bracket | `g(u)=0.3f(u-1)+0.7f(u-2).` |
| 1467 | 12921-12927 | 0.19 | inline_unsafe_marker | bracket | `\varphi(x,y)= \begin{cases} A e^{-(2x+3y)}, & x>0,\ y>0,\\ 0, & \text{其他}. \end{cases}` |
| 1470 | 12945-12947 | 0.42 | inline_safe | bracket | `0\le x\le1,\quad 0\le y\le x+\frac13,` |
| 1471 | 12949-12951 | 0.39 | inline_safe | bracket | `1\le x\le3,\quad 0\le y\le \frac{6-2x}{3}.` |
| 1473 | 12965-12971 | 0.19 | inline_unsafe_marker | bracket | `f(x,y)= \begin{cases} k e^{-(2x+3y)}, & x>0,\ y>0,\\ 0, & \text{其他}. \end{cases}` |
| 1476 | 12996-13002 | 0.31 | inline_unsafe_marker | bracket | `F(x,y)= \begin{cases} (1-e^{-2x})(1-e^{-3y}), & x>0,\ y>0,\\ 0, & x\le0\ \text{或}\ y\le0. \end{cases}` |
| 1481 | 13031-13037 | 0.19 | inline_unsafe_marker | bracket | `\varphi(x,y)= \begin{cases} A e^{-(3x+2y)}, & x>0,\ y>0,\\ 0, & \text{其他}. \end{cases}` |
| 1484 | 13055-13057 | 0.42 | inline_safe | bracket | `0\le x\le\frac35,\quad 0\le y\le x+1,` |
| 1485 | 13059-13061 | 0.46 | inline_safe | bracket | `\frac35\le x\le3,\quad 0\le y\le\frac{6-2x}{3}.` |
| 1487 | 13075-13081 | 0.20 | inline_unsafe_marker | bracket | `f(x,y)= \begin{cases} 1, & \|y\|<x,\ 0<x<1,\\ 0, & \text{其他}. \end{cases}` |
| 1489 | 13093-13099 | 0.11 | inline_unsafe_marker | bracket | `f_X(x)= \begin{cases} 2x, & 0<x<1,\\ 0, & \text{其他}. \end{cases}` |
| 1491 | 13105-13111 | 0.13 | inline_unsafe_marker | bracket | `f_Y(y)= \begin{cases} 1-\|y\|, & -1<y<1,\\ 0, & \text{其他}. \end{cases}` |
| 1492 | 13114-13118 | 0.48 | normalized_width_not_low | bracket | `EX=\int_0^1 x\cdot2x\,\mathrm dx=\frac23, \qquad EX^2=\int_0^1 x^2\cdot2x\,\mathrm dx=\frac12,` |
| 1494 | 13124-13126 | 0.41 | inline_safe | bracket | `EY=\int_{-1}^{1}y(1-\|y\|)\,\mathrm dy=0.` |
| 1496 | 13132-13134 | 0.35 | inline_safe | bracket | `\operatorname{Cov}(X,Y)=E(XY)-EX\,EY=0.` |
| 1497 | 13137-13139 | 0.13 | inline_safe | bracket | `f(x,y)=0,` |
| 1498 | 13141-13143 | 0.43 | inline_safe | bracket | `f_X(1/2)f_Y(3/4)=1\cdot\frac14>0.` |
| 1499 | 13149-13155 | 0.13 | inline_unsafe_marker | bracket | `f(x,y)= \begin{cases} \dfrac{21}{4}x^2y, & x^2<y<1,\\ 0, & \text{其他}. \end{cases}` |
| 1500 | 13162-13165 | 0.48 | normalized_width_not_low | bracket | `f_X(x)=\int_{x^2}^{1}\frac{21}{4}x^2y\,\mathrm dy =\frac{21}{8}x^2(1-x^4),\qquad -1<x<1.` |
| 1501 | 13167-13173 | 0.21 | inline_unsafe_marker | bracket | `f_X(x)= \begin{cases} \dfrac{21}{8}x^2(1-x^4), & -1<x<1,\\ 0, & \text{其他}. \end{cases}` |
| 1502 | 13175-13178 | 0.46 | normalized_width_not_low | bracket | `f_Y(y)=\int_{-\sqrt y}^{\sqrt y}\frac{21}{4}x^2y\,\mathrm dx =\frac72 y^{5/2},\qquad 0<y<1.` |
| 1503 | 13180-13186 | 0.17 | inline_unsafe_marker | bracket | `f_Y(y)= \begin{cases} \dfrac72 y^{5/2}, & 0<y<1,\\ 0, & \text{其他}. \end{cases}` |
| 1504 | 13189-13191 | 0.08 | inline_safe | bracket | `EX=0.` |
| 1505 | 13193-13196 | 0.42 | normalized_width_not_low | bracket | `EY=\int_0^1 y\cdot\frac72 y^{5/2}\,\mathrm dy =\frac72\cdot\frac{2}{9}=\frac79.` |
| 1508 | 13207-13209 | 0.35 | inline_safe | bracket | `\operatorname{Cov}(X,Y)=E(XY)-EX\,EY=0.` |
| 1509 | 13217-13219 | 0.25 | inline_unsafe_marker | bracket | `f(x,y) = \begin{cases} e^{-(x+y)}, & x > 0,\ y > 0, \\ 0, & \text{其他}, \end{cases}` |
| 1513 | 13240-13242 | 0.21 | inline_unsafe_marker | bracket | `f_Z(z) = \begin{cases} ze^{-z}, & z > 0, \\ 0, & z \leqslant 0. \end{cases}` |
| 1514 | 13249-13249 | 0.30 | inline_unsafe_marker | bracket | `f_X(x)=\begin{cases}2\mathrm{e}^{-2x},&x\geqslant0\\0,&x<0\end{cases},~f_Y(y)=\begin{cases}2\mathrm{e}^{-2y},&y\geqslant0\\0,&y<0\end{cases}` |
| 1515 | 13250-13250 | 0.25 | inline_unsafe_marker | bracket | `F_T(t) =\begin{cases}1 - e^{-2t}, & t>0 \\0, & t\le 0\end{cases}\quad (T=X,Y)` |
| 1518 | 13275-13275 | 0.36 | inline_unsafe_marker | bracket | `f_Z(z) =\begin{cases}2\left( e^{-\frac{2z}{3}} - e^{-z} \right), & z > 0 \\0, & z \le 0\end{cases}` |
| 1519 | 13282-13284 | 0.37 | inline_unsafe_marker | bracket | `f(x,y) = \begin{cases} \dfrac{1}{2}(x+y)e^{-(x+y)}, & x>0,\ y>0, \\ 0, & \text{其他}. \end{cases}` |
| 1521 | 13292-13292 | 0.39 | inline_safe | bracket | `f_Y(y) = \frac{y+1}{2}e^{-y},\quad y>0.` |
| 1524 | 13316-13318 | 0.26 | inline_unsafe_marker | bracket | `f_Z(z) = \begin{cases} \dfrac{z^2}{2}e^{-z}, & z > 0 \\ 0, & z \leqslant 0 \end{cases}` |
| 1525 | 13340-13342 | 0.27 | inline_unsafe_marker | bracket | `f_X(x) = \begin{cases} 2e^{-2x}, & x > 0, \\ 0, & \text{其他}, \end{cases} \quad f_Y(y) = \begin{cases} 3y^2, & 0 < y < 1, \\ 0, & \text{其他}. \end{cases}` |
| 1526 | 13348-13350 | 0.46 | inline_unsafe_marker | bracket | `f(x,y) = f_X(x)\,f_Y(y) = \begin{cases} 6y^2 e^{-2x}, & x > 0,\ 0 < y < 1 \\ 0, & \text{其他} \end{cases}` |
| 1530 | 13378-13380 | 0.42 | display_environment | env:align* | `f_Z(z) &= \frac{\mathrm{d}}{\mathrm{d}z} F_Z(z) = \frac{3(e^2-1)}{2}e^{-2z}` |
| 1531 | 13383-13385 | 0.45 | inline_unsafe_marker | bracket | `f_Z(z) = \begin{cases} 3z^2 - 3z + \dfrac{3}{2} - \dfrac{3}{2}e^{-2z}, & 0 < z < 1 \\ \dfrac{3(e^2-1)}{2}e^{-2z}, & z \geqslant 1 \\ 0, & \text{其他} \end{cases}` |
| 1532 | 13390-13392 | 0.11 | inline_safe | bracket | `Z=2X-Y` |
| 1533 | 13397-13399 | 0.34 | inline_safe | bracket | `0<x<1,\qquad 2x-z\ge0.` |
| 1534 | 13401-13404 | 0.43 | normalized_width_not_low | bracket | `f_Z(z)=\int f_X(x)f_Y(2x-z)\,\mathrm dx =\int e^{-(2x-z)}\,\mathrm dx,` |
| 1535 | 13408-13411 | 0.42 | normalized_width_not_low | bracket | `f_Z(z)=\int_0^1 e^{-(2x-z)}\,\mathrm dx =\frac{e^z(1-e^{-2})}{2}.` |
| 1536 | 13413-13416 | 0.45 | normalized_width_not_low | bracket | `f_Z(z)=\int_{z/2}^{1} e^{-(2x-z)}\,\mathrm dx =\frac{1-e^{z-2}}{2}.` |
| 1537 | 13418-13425 | 0.21 | inline_unsafe_marker | bracket | `f_Z(z)= \begin{cases} \dfrac{e^z(1-e^{-2})}{2}, & z\le0,\\[6pt] \dfrac{1-e^{z-2}}{2}, & 0<z<2,\\[6pt] 0, & z\ge2. \end{cases}` |
| 1538 | 13434-13436 | 0.25 | inline_unsafe_marker | bracket | `f(x,y) = \begin{cases} \dfrac{1}{2}, & 0 \leqslant x \leqslant 2,\ 0 \leqslant y \leqslant 1 \\ 0, & \text{其他} \end{cases}` |
| 1541 | 13456-13458 | 0.29 | inline_unsafe_marker | bracket | `f_Z(z) = \begin{cases} \dfrac{1}{2}(\ln 2 - \ln z), & 0 < z < 2 \\ 0, & \text{其他} \end{cases}` |
| 1550 | 13535-13537 | 0.46 | inline_safe | bracket | `f_Z(z) = \int_{-\infty}^{+\infty}\|y\|\,f(yz, y)\,\mathrm{d}y.` |
| 1563 | 13660-13662 | 0.49 | inline_safe | bracket | `P(X+Y=k) = \binom{n+m}{k} p^k (1-p)^{n+m-k},` |
| 1567 | 13691-13694 | 0.38 | normalized_width_not_low | bracket | `P(X=k)=\frac{3^k}{k!}e^{-3},\qquad P(Y=i-k)=\frac{3^{i-k}}{(i-k)!}e^{-3}.` |
| 1568 | 13696-13705 | 0.46 | inline_unsafe_marker | bracket | `\begin{aligned} P(X+Y=i) &=\sum_{k=0}^{i}\frac{3^k}{k!}e^{-3}\cdot \frac{3^{i-k}}{(i-k)!}e^{-3}\\ &=e^{-6}\frac{1}{i!}\sum_{k=0}^{i}\binom{i}{k}3^k3^{i-k}\\ &=e^{-6}\frac{(3+3)^...` |
| 1569 | 13711-13713 | 0.36 | inline_safe | bracket | `\varphi_X(t) = \exp\left(i\mu t - \frac{1}{2}\sigma^2 t^2\right).` |
| 1573 | 13754-13756 | 0.44 | inline_safe | bracket | `F_{\max}(z) = P\{X \leqslant z, Y \leqslant z\} = F(z, z).` |
| 1581 | 13834-13836 | 0.27 | inline_unsafe_marker | bracket | `f(x,y) = \begin{cases} \dfrac{1}{(b-a)^2}, & a \leqslant x \leqslant b,\ a \leqslant y \leqslant b, \\ 0, & \text{其他}. \end{cases}` |
| 1583 | 13844-13846 | 0.37 | inline_unsafe_marker | bracket | `f_Z(z) = F_Z'(z) = \begin{cases} \dfrac{2(z-a)}{(b-a)^2}, & a \leqslant z \leqslant b, \\ 0, & \text{其他}. \end{cases}` |
| 1585 | 13868-13870 | 0.45 | inline_safe | bracket | `f_X(x)=\frac{1}{\pi(1+x^2)},\qquad x\in\mathbb R,` |
| 1586 | 13879-13881 | 0.47 | inline_safe | bracket | `x=\frac y3,\qquad \left\|\frac{\mathrm dx}{\mathrm dy}\right\|=\frac13.` |
| 1587 | 13883-13887 | 0.37 | normalized_width_not_low | bracket | `f_Y(y)=f_X\!\left(\frac y3\right)\cdot\frac13 =\frac{1}{\pi\left(1+\frac{y^2}{9}\right)}\cdot\frac13 =\frac{3}{\pi(9+y^2)},\qquad y\in\mathbb R.` |
| 1590 | 13904-13906 | 0.44 | inline_unsafe_marker | bracket | `f_Y(y) = \begin{cases} \dfrac{1}{2\sqrt{\pi(y-1)}}\,\exp\!\left\{-\dfrac{y-1}{4}\right\}, & y > 1, \\ 0, & y \leqslant 1. \end{cases}` |
| 1591 | 13913-13915 | 0.22 | inline_unsafe_marker | bracket | `f(x,y) = \begin{cases} \lambda e^{-\lambda y}, & 0 < x < y, \\ 0, & \text{其他}, \end{cases}` |
| 1596 | 13941-13943 | 0.35 | inline_unsafe_marker | bracket | `f_Z(z) = \begin{cases} e^{-\lambda z/2} - e^{-\lambda z}, & z > 0, \\ 0, & z \leqslant 0. \end{cases}` |
| 1597 | 13945-13947 | 0.31 | inline_unsafe_marker | bracket | `f_N(n) = f_X(n) = \begin{cases} e^{-\lambda n}, & n > 0, \\ 0, & n \leqslant 0. \end{cases}` |
| 1598 | 13954-13956 | 0.39 | inline_unsafe_marker | bracket | `f_X(x) = \begin{cases} e^{-x}, & x > 0, \\ 0, & x \leqslant 0, \end{cases} \quad f_Y(y) = \begin{cases} \dfrac{1}{2}e^{-y/2}, & y > 0, \\ 0, & y \leqslant 0. \end{cases}` |
| 1601 | 13971-13973 | 0.32 | inline_unsafe_marker | bracket | `f_Z(z) = \begin{cases} e^{-z/2} - e^{-z}, & z > 0, \\ 0, & z \leqslant 0. \end{cases}` |
| 1602 | 13981-13983 | 0.22 | inline_unsafe_marker | bracket | `f(x,y) = \begin{cases} cxe^{-y}, & 0 < x < y < +\infty, \\ 0, & \text{其他}. \end{cases}` |
| 1610 | 14023-14025 | 0.42 | inline_unsafe_marker | bracket | `f_Z(z) = \begin{cases} \left(\dfrac{z}{2}-1\right)e^{-z/2} + e^{-z}, & z \geqslant 0, \\ 0, & z < 0. \end{cases}` |
| 1616 | 14058-14060 | 0.25 | inline_unsafe_marker | bracket | `f_Z(z) = \begin{cases} \dfrac{1}{(z+1)^2}, & z > 0, \\ 0, & z \leqslant 0. \end{cases}` |
| 1619 | 14081-14083 | 0.25 | inline_unsafe_marker | bracket | `f_Z(z) = \begin{cases} \dfrac{2(b-z)}{(b-a)^2}, & a \leqslant z \leqslant b, \\ 0, & \text{其他}. \end{cases}` |
| 1620 | 14097-14099 | 0.40 | inline_safe | bracket | `X\sim P(\lambda_1),\qquad Y\sim P(\lambda_2),` |
| 1621 | 14101-14103 | 0.26 | inline_safe | bracket | `X+Y\sim P(\lambda_1+\lambda_2).` |
| 1623 | 14130-14132 | 0.43 | inline_safe | bracket | `Z=\min(X,Y),\qquad W=\max(X,Y),` |
| 1624 | 14134-14136 | 0.15 | inline_safe | bracket | `Z+W=X+Y.` |
| 1625 | 14138-14140 | 0.33 | inline_safe | bracket | `P(Z+W\geqslant 1)=P(X+Y\geqslant 1).` |
| 1626 | 14143-14145 | 0.40 | inline_safe | bracket | `G=\{(x,y):0\le x\le 1,\ 0\le y\le 2\}` |
| 1627 | 14147-14149 | 0.43 | inline_safe | bracket | `f(x,y)=\frac12\qquad ((x,y)\in G).` |
| 1629 | 14159-14161 | 0.27 | inline_safe | bracket | `P(Z+W\geqslant 1)=\frac34.` |
| 1630 | 14167-14169 | 0.35 | inline_unsafe_marker | bracket | `f(x,y) = \begin{cases} \dfrac{2}{\pi}\,e^{-\frac{x^2+y^2}{2}}, & x>0,\ y>0, \\ 0, & \text{其他}. \end{cases}` |
| 1637 | 14222-14224 | 0.45 | inline_safe | bracket | `P(\xi=k)=\frac13,\qquad k=1,2,3.` |
| 1638 | 14226-14228 | 0.43 | inline_safe | bracket | `X=\max(\xi,\eta),\qquad Y=\min(\xi,\eta).` |
| 1639 | 14237-14239 | 0.29 | inline_safe | bracket | `P(X=x,Y=x)=\frac19.` |
| 1640 | 14241-14243 | 0.29 | inline_safe | bracket | `P(X=x,Y=y)=\frac29.` |
| 1641 | 14245-14253 | 0.09 | inline_unsafe_marker | bracket | `\begin{array}{c\|ccc} & X=1 & X=2 & X=3\\ \hline Y=1 & \dfrac19 & \dfrac29 & \dfrac29\\[4pt] Y=2 & 0 & \dfrac19 & \dfrac29\\[4pt] Y=3 & 0 & 0 & \dfrac19 \end{array}.` |
| 1644 | 14271-14277 | 0.27 | inline_unsafe_marker | bracket | `f(x,y)= \begin{cases} \dfrac32xy^2, & 0\le x\le 2,\ 0\le y\le 1,\\ 0, & \text{其他}. \end{cases}` |
| 1645 | 14282-14286 | 0.39 | normalized_width_not_low | bracket | `f_X(x)=\int_0^1 \frac32xy^2\,\mathrm{d}y =\frac32x\cdot\frac13 =\frac{x}{2}.` |
| 1646 | 14288-14292 | 0.39 | normalized_width_not_low | bracket | `f_Y(y)=\int_0^2 \frac32xy^2\,\mathrm{d}x =\frac32y^2\cdot\frac{2^2}{2} =3y^2.` |
| 1648 | 14308-14310 | 0.21 | inline_safe | bracket | `Y\|X=n\sim B(n,p).` |
| 1649 | 14312-14318 | 0.46 | inline_unsafe_marker | bracket | `\begin{aligned} P(X=n,Y=k) &=P(X=n)P(Y=k\|X=n)\\ &=e^{-\lambda}\frac{\lambda^n}{n!}\binom nkp^k(1-p)^{n-k}. \end{aligned}` |
| 1651 | 14334-14336 | 0.13 | inline_safe | bracket | `Y\sim P(\lambda p).` |
| 1652 | 14345-14353 | 0.08 | inline_unsafe_marker | bracket | `\begin{array}{c\|cccc} & \eta=1 & \eta=2 & \eta=4 & \eta=5\\ \hline \zeta=0 & 0.05 & 0.12 & 0.15 & 0.07\\ \zeta=1 & 0.03 & 0.10 & 0.08 & 0.11\\ \zeta=2 & 0.07 & 0.01 & 0.11 & 0.1...` |
| 1655 | 14369-14371 | 0.26 | inline_safe | bracket | `P(\zeta=0,\eta=1)=0.05,` |
| 1656 | 14373-14375 | 0.48 | inline_safe | bracket | `P(\zeta=0)P(\eta=1)=0.39\times0.15=0.0585.` |
| 1657 | 14379-14385 | 0.13 | inline_unsafe_marker | bracket | `\begin{array}{c\|ccccccc} Z & 0 & 1 & 2 & 4 & 5 & 8 & 10\\ \hline P & 0.39 & 0.03 & 0.17 & 0.09 & 0.11 & 0.11 & 0.10 \end{array}.` |
| 1659 | 14398-14400 | 0.16 | inline_safe | bracket | `E(\zeta\eta)=3.16.` |
| 1660 | 14408-14420 | 0.11 | inline_unsafe_marker | bracket | `X\sim \begin{pmatrix} 1&2&3\\ 0.5&0.1&0.4 \end{pmatrix}, \qquad Y\sim \begin{pmatrix} 1&2&3\\ 0.3&0.3&0.4 \end{pmatrix}.` |
| 1663 | 14438-14440 | 0.27 | inline_safe | bracket | `P(X=Y)=0.34=\frac{17}{50}.` |
| 1664 | 14451-14453 | 0.14 | inline_safe | bracket | `\binom42=6.` |
| 1665 | 14455-14457 | 0.45 | inline_safe | bracket | `(1,2),(1,3),(1,4),(2,3),(2,4),(3,4),` |
| 1666 | 14459-14467 | 0.09 | inline_unsafe_marker | bracket | `\begin{array}{c\|ccc} & \xi=2 & \xi=3 & \xi=4\\ \hline \eta=1 & \dfrac16 & \dfrac16 & \dfrac16\\[4pt] \eta=2 & 0 & \dfrac16 & \dfrac16\\[4pt] \eta=3 & 0 & 0 & \dfrac16 \end{array}.` |
| 1669 | 14477-14479 | 0.29 | inline_safe | bracket | `P(\xi=2,\eta=1)=\frac16,` |
| 1672 | 14496-14508 | 0.11 | inline_unsafe_marker | bracket | `\xi= \begin{cases} 1, & A\text{ 发生},\\ 0, & A\text{ 不发生}, \end{cases} \qquad \eta= \begin{cases} 1, & B\text{ 发生},\\ 0, & B\text{ 不发生}. \end{cases}` |
| 1673 | 14515-14517 | 0.49 | inline_safe | bracket | `P(\xi=1)=P(A),\qquad P(\eta=1)=P(B).` |
| 1675 | 14523-14526 | 0.38 | normalized_width_not_low | bracket | `P(A\overline B)=P(A)P(\overline B),\qquad P(\overline A B)=P(\overline A)P(B),` |
| 1676 | 14527-14529 | 0.33 | inline_safe | bracket | `P(\overline A\,\overline B)=P(\overline A)P(\overline B).` |
| 1678 | 14541-14547 | 0.18 | inline_unsafe_marker | bracket | `p(x,y)= \begin{cases} Ce^{-2(x+y)}, & x>0,\ y>0,\\ 0, & \text{其他}. \end{cases}` |
| 1679 | 14556-14560 | 0.49 | normalized_width_not_low | bracket | `1=\int_0^\infty\int_0^\infty Ce^{-2(x+y)}\,\mathrm{d}y\,\mathrm{d}x =C\left(\int_0^\infty e^{-2x}\,\mathrm{d}x\right)^2 =C\left(\frac12\right)^2.` |
| 1680 | 14562-14564 | 0.07 | inline_safe | bracket | `C=4.` |
| 1681 | 14567-14569 | 0.28 | inline_safe | bracket | `p(x,y)=4e^{-2(x+y)}.` |
| 1687 | 14599-14601 | 0.16 | inline_safe | bracket | `\operatorname{Cov}(\xi,\eta)=0.` |
| 1688 | 14623-14625 | 0.21 | inline_safe | bracket | `\frac{x^2}{a^2}+\frac{y^2}{b^2}\le1` |
| 1689 | 14633-14639 | 0.22 | inline_unsafe_marker | bracket | `f(x,y)= \begin{cases} \dfrac1{\pi ab}, & \dfrac{x^2}{a^2}+\dfrac{y^2}{b^2}\le1,\\[6pt] 0, & \text{其他}. \end{cases}` |
| 1690 | 14641-14643 | 0.43 | inline_safe | bracket | `-b\sqrt{1-\frac{x^2}{a^2}}\le y\le b\sqrt{1-\frac{x^2}{a^2}}.` |
| 1692 | 14650-14656 | 0.25 | inline_unsafe_marker | bracket | `f_X(x)= \begin{cases} \dfrac2{\pi a}\sqrt{1-\dfrac{x^2}{a^2}}, & \|x\|\le a,\\[6pt] 0, & \text{其他}. \end{cases}` |
| 1693 | 14658-14664 | 0.25 | inline_unsafe_marker | bracket | `f_Y(y)= \begin{cases} \dfrac2{\pi b}\sqrt{1-\dfrac{y^2}{b^2}}, & \|y\|\le b,\\[6pt] 0, & \text{其他}. \end{cases}` |
| 1694 | 14667-14669 | 0.44 | inline_safe | bracket | `EX^2=\frac{a^2}{4},\qquad EY^2=\frac{b^2}{4}.` |
| 1695 | 14671-14673 | 0.48 | inline_safe | bracket | `DX=\frac{a^2}{4}=25,\qquad DY=\frac{b^2}{4}=4.` |
| 1696 | 14675-14677 | 0.27 | inline_safe | bracket | `a=10,\qquad b=4.` |
| 1697 | 14684-14686 | 0.15 | inline_safe | bracket | `Z=\min\{X,Y\}` |
| 1698 | 14691-14693 | 0.26 | inline_safe | bracket | `F_Z(z)=P(Z\le z)=0.` |
| 1699 | 14695-14703 | 0.25 | inline_unsafe_marker | bracket | `\begin{aligned} F_Z(z) &=1-P(Z>z)\\ &=1-P(X>z,Y>z)\\ &=1-P(X>z)P(Y>z)\\ &=1-(1-z)e^{-5z}. \end{aligned}` |
| 1700 | 14705-14707 | 0.13 | inline_safe | bracket | `F_Z(z)=1.` |
| 1701 | 14709-14716 | 0.22 | inline_unsafe_marker | bracket | `F_Z(z)= \begin{cases} 0, & z\le0,\\ 1-(1-z)e^{-5z}, & 0<z\le1,\\ 1, & z>1. \end{cases}` |
| 1702 | 14719-14722 | 0.39 | normalized_width_not_low | bracket | `f_Z(z)=\frac{\mathrm{d}}{\mathrm{d}z}\left[1-(1-z)e^{-5z}\right] =(6-5z)e^{-5z}.` |
| 1703 | 14724-14730 | 0.19 | inline_unsafe_marker | bracket | `f_Z(z)= \begin{cases} (6-5z)e^{-5z}, & 0<z<1,\\ 0, & \text{其他}. \end{cases}` |
| 1704 | 14737-14743 | 0.13 | inline_unsafe_marker | bracket | `f(x,y)= \begin{cases} 6x, & 0<x<y<1,\\ 0, & \text{其他}. \end{cases}` |
| 1705 | 14751-14753 | 0.43 | inline_safe | bracket | `f_X(x)=\int_x^1 6x\,\mathrm{d}y=6x(1-x),` |
| 1706 | 14755-14757 | 0.38 | inline_safe | bracket | `f_Y(y)=\int_0^y 6x\,\mathrm{d}x=3y^2,` |
| 1707 | 14759-14771 | 0.12 | inline_unsafe_marker | bracket | `f_X(x)= \begin{cases} 6x(1-x),&0<x<1,\\ 0,&\text{其他}, \end{cases} \qquad f_Y(y)= \begin{cases} 3y^2,&0<y<1,\\ 0,&\text{其他}. \end{cases}` |
| 1708 | 14774-14776 | 0.42 | inline_safe | bracket | `0<x<\frac12,\qquad x<y<1-x.` |
| 1710 | 14785-14787 | 0.48 | inline_safe | bracket | `EX=\int_0^1 x\cdot6x(1-x)\,\mathrm{d}x=\frac12,` |
| 1711 | 14788-14790 | 0.43 | inline_safe | bracket | `EY=\int_0^1 y\cdot3y^2\,\mathrm{d}y=\frac34,` |
| 1712 | 14791-14794 | 0.47 | normalized_width_not_low | bracket | `E(XY)=\int_0^1\int_0^y xy\cdot6x\,\mathrm{d}x\,\mathrm{d}y =\int_0^1 2y^4\,\mathrm{d}y=\frac25.` |
| 1713 | 14796-14800 | 0.35 | normalized_width_not_low | bracket | `\operatorname{Cov}(X,Y)=E(XY)-EX\,EY =\frac25-\frac12\cdot\frac34 =\frac1{40}.` |
| 1714 | 14805-14811 | 0.13 | inline_unsafe_marker | bracket | `f(x,y)= \begin{cases} 6x, & 0<x<y<1,\\ 0, & \text{其他}. \end{cases}` |
| 1715 | 14819-14821 | 0.43 | inline_safe | bracket | `f_X(x)=\int_x^1 6x\,\mathrm{d}y=6x(1-x).` |
| 1716 | 14823-14825 | 0.38 | inline_safe | bracket | `f_Y(y)=\int_0^y 6x\,\mathrm{d}x=3y^2.` |
| 1717 | 14827-14839 | 0.12 | inline_unsafe_marker | bracket | `f_X(x)= \begin{cases} 6x(1-x),&0<x<1,\\ 0,&\text{其他}, \end{cases} \qquad f_Y(y)= \begin{cases} 3y^2,&0<y<1,\\ 0,&\text{其他}. \end{cases}` |
| 1718 | 14842-14846 | 0.29 | normalized_width_not_low | bracket | `f_X\left(\frac13\right) =6\cdot\frac13\cdot\frac23 =\frac43.` |
| 1719 | 14848-14850 | 0.37 | inline_safe | bracket | `f\left(\frac13,y\right)=6\cdot\frac13=2.` |
| 1720 | 14852-14857 | 0.41 | normalized_width_not_low | bracket | `f_{Y\|X}\left(y\mid \frac13\right) =\frac{f(1/3,y)}{f_X(1/3)} =\frac{2}{4/3} =\frac32,\qquad \frac13<y<1.` |
| 1721 | 14859-14865 | 0.23 | inline_unsafe_marker | bracket | `f_{Y\|X}\left(y\mid \frac13\right)= \begin{cases} \dfrac32, & \dfrac13<y<1,\\[6pt] 0, & \text{其他}. \end{cases}` |
| 1722 | 14868-14870 | 0.42 | inline_safe | bracket | `0<x<\frac12,\qquad x<y<1-x.` |
| 1723 | 14872-14877 | 0.41 | normalized_width_not_low | bracket | `P(X+Y\le1) =\int_0^{1/2}\int_x^{1-x}6x\,\mathrm{d}y\,\mathrm{d}x =\int_0^{1/2}6x(1-2x)\,\mathrm{d}x =\frac14.` |
| 1724 | 14882-14888 | 0.15 | inline_unsafe_marker | bracket | `f(x,y)= \begin{cases} 2e^{-2x-y},&x>0,\ y>0,\\ 0,&\text{其他}. \end{cases}` |
| 1727 | 14902-14910 | 0.33 | inline_unsafe_marker | bracket | `\begin{aligned} F_Z(z) &=P\{\max(X,Y)\le z\}\\ &=P(X\le z,Y\le z)\\ &=F_X(z)F_Y(z) =(1-e^{-2z})(1-e^{-z}). \end{aligned}` |
| 1729 | 14917-14923 | 0.34 | inline_unsafe_marker | bracket | `f_Z(z)= \begin{cases} e^{-z}+2e^{-2z}-3e^{-3z},&z>0,\\ 0,&\text{其他}. \end{cases}` |
| 1730 | 14928-14930 | 0.30 | inline_safe | bracket | `\{(x,y):0<x<2,\ 0<y<1\}` |
| 1731 | 14937-14943 | 0.21 | inline_unsafe_marker | bracket | `f(x,y)= \begin{cases} \dfrac12,&0<x<2,\ 0<y<1,\\ 0,&\text{其他}. \end{cases}` |
| 1732 | 14945-14957 | 0.11 | inline_unsafe_marker | bracket | `f_X(x)= \begin{cases} \dfrac12,&0<x<2,\\ 0,&\text{其他}, \end{cases} \qquad f_Y(y)= \begin{cases} 1,&0<y<1,\\ 0,&\text{其他}. \end{cases}` |
| 1733 | 14959-14961 | 0.28 | inline_safe | bracket | `F(x,y)=F_X(x)F_Y(y),` |
| 1734 | 14963-14977 | 0.11 | inline_unsafe_marker | bracket | `F_X(x)= \begin{cases} 0,&x\le0,\\ \dfrac{x}{2},&0<x\le2,\\ 1,&x>2, \end{cases} \qquad F_Y(y)= \begin{cases} 0,&y\le0,\\ y,&0<y\le1,\\ 1,&y>1. \end{cases}` |
| 1736 | 14985-14990 | 0.25 | normalized_width_not_low | bracket | `\operatorname{Cov}(\xi,\eta) =\operatorname{Cov}(X+Y,aX+bY) =aDX+bDY =\frac a3+\frac b{12}.` |
| 1739 | 15000-15004 | 0.23 | normalized_width_not_low | bracket | `\frac{a^2}{3}+\frac{16a^2}{12}=1 \quad\Longrightarrow\quad \frac{5a^2}{3}=1.` |
| 1740 | 15006-15008 | 0.49 | inline_safe | bracket | `a=\pm\sqrt{\frac35},\qquad b=\mp4\sqrt{\frac35}.` |
| 1741 | 15015-15021 | 0.08 | inline_unsafe_marker | bracket | `\begin{array}{c\|cccc} (X,Y)&(1,0)&(1,1)&(2,0)&(2,1)\\ \hline P&0.4&0.2&a&b \end{array}` |
| 1742 | 15026-15028 | 0.25 | inline_safe | bracket | `0.4+0.2+a+b=1,` |
| 1743 | 15030-15032 | 0.14 | inline_safe | bracket | `a+b=0.4.` |
| 1745 | 15040-15042 | 0.18 | inline_safe | bracket | `0.2+2b=0.8,` |
| 1746 | 15044-15046 | 0.09 | inline_safe | bracket | `b=0.3.` |
| 1747 | 15048-15050 | 0.21 | inline_safe | bracket | `a=0.4-b=0.1.` |
| 1748 | 15055-15061 | 0.23 | inline_unsafe_marker | bracket | `f(x,y)= \begin{cases} A\left(x^2+\dfrac12xy\right),&0<x<1,\ 0<y<2,\\[6pt] 0,&\text{其他}. \end{cases}` |
| 1750 | 15079-15081 | 0.14 | inline_safe | bracket | `A=\frac67.` |
| 1751 | 15084-15091 | 0.48 | inline_unsafe_marker | bracket | `\begin{aligned} f_X(x) &=\int_0^2 \frac67\left(x^2+\frac12xy\right)\,\mathrm dy\\ &=\frac67(2x^2+x) =\frac{12}{7}x^2+\frac67x. \end{aligned}` |
| 1752 | 15093-15099 | 0.23 | inline_unsafe_marker | bracket | `f_X(x)= \begin{cases} \dfrac{12}{7}x^2+\dfrac67x,&0<x<1,\\[6pt] 0,&\text{其他}. \end{cases}` |
| 1753 | 15101-15105 | 0.47 | normalized_width_not_low | bracket | `EX=\int_0^1 x\left(\frac{12}{7}x^2+\frac67x\right)\,\mathrm dx =\frac{12}{7}\cdot\frac14+\frac67\cdot\frac13 =\frac57.` |
| 1754 | 15108-15110 | 0.31 | inline_safe | bracket | `0<x<1,\qquad 0<y<x.` |
| 1756 | 15127-15136 | 0.09 | inline_unsafe_marker | bracket | `\begin{array}{c\|cccc} & Y=-1 & Y=0 & Y=1 & Y=2\\ \hline X=-2 & a & 0 & 0 & 0\\ X=-1 & 0.14 & b & 0 & 0\\ X=0 & 0.01 & 0.02 & 0.03 & 0\\ X=1 & 0.12 & 0.13 & 0.14 & 0.15 \end{array}` |
| 1758 | 15148-15150 | 0.15 | inline_safe | bracket | `a+b=0.26.` |
| 1760 | 15161-15163 | 0.17 | inline_safe | bracket | `3a+b=0.60.` |
| 1761 | 15165-15167 | 0.43 | inline_safe | bracket | `a+b=0.26,\qquad 3a+b=0.60,` |
| 1762 | 15169-15171 | 0.33 | inline_safe | bracket | `a=0.17,\qquad b=0.09.` |
| 1763 | 15174-15176 | 0.26 | inline_safe | bracket | `P(X=-2)=a=0.17,` |
| 1764 | 15177-15179 | 0.34 | inline_safe | bracket | `P(X=-1)=0.14+b=0.23,` |
| 1765 | 15180-15182 | 0.44 | inline_safe | bracket | `P(X=0)=0.01+0.02+0.03=0.06,` |
| 1767 | 15187-15196 | 0.17 | inline_unsafe_marker | bracket | `F_X(x)= \begin{cases} 0, & x<-2,\\ 0.17, & -2\le x<-1,\\ 0.40, & -1\le x<0,\\ 0.46, & 0\le x<1,\\ 1, & x\ge1. \end{cases}` |
| 1769 | 15212-15214 | 0.23 | inline_safe | bracket | `\{0<x<a,\ 0<y<b\}` |
| 1770 | 15222-15228 | 0.21 | inline_unsafe_marker | bracket | `f(x,y)= \begin{cases} \dfrac1{ab}, & 0<x<a,\ 0<y<b,\\ 0, & \text{其他}. \end{cases}` |
| 1771 | 15230-15242 | 0.11 | inline_unsafe_marker | bracket | `f_X(x)= \begin{cases} \dfrac1a, & 0<x<a,\\ 0, & \text{其他}, \end{cases} \qquad f_Y(y)= \begin{cases} \dfrac1b, & 0<y<b,\\ 0, & \text{其他}. \end{cases}` |
| 1772 | 15245-15247 | 0.38 | inline_safe | bracket | `DX=\frac{a^2}{12},\qquad DY=\frac{b^2}{12}.` |
| 1773 | 15249-15251 | 0.38 | inline_safe | bracket | `\frac{a^2}{12}=12,\qquad \frac{b^2}{12}=36.` |
| 1774 | 15253-15255 | 0.32 | inline_safe | bracket | `a=12,\qquad b=12\sqrt3.` |
| 1776 | 15266-15272 | 0.21 | inline_unsafe_marker | bracket | `f(x,y)= \begin{cases} Axy, & 0<x<1,\ 0<y<1,\\ 0, & \text{其他}. \end{cases}` |
| 1777 | 15281-15285 | 0.40 | normalized_width_not_low | bracket | `1=\int_0^1\int_0^1 Axy\,\mathrm{d}y\,\mathrm{d}x =A\left(\int_0^1 x\,\mathrm{d}x\right)\left(\int_0^1 y\,\mathrm{d}y\right) =\frac{A}{4}.` |
| 1778 | 15287-15289 | 0.07 | inline_safe | bracket | `A=4.` |
| 1780 | 15298-15305 | 0.47 | inline_unsafe_marker | bracket | `\begin{aligned} E(e^{tX+sY}) &=\int_0^1\int_0^1 e^{tx+sy}4xy\,\mathrm{d}y\,\mathrm{d}x\\ &=4\left(\int_0^1 xe^{tx}\,\mathrm{d}x\right) \left(\int_0^1 ye^{sy}\,\mathrm{d}y\right)...` |
| 1783 | 15314-15318 | 0.37 | normalized_width_not_low | bracket | `E(e^{tX+sY}) =4\left(\frac{e^t}{t}-\frac{e^t}{t^2}+\frac1{t^2}\right) \left(\frac{e^s}{s}-\frac{e^s}{s^2}+\frac1{s^2}\right),` |
| 1785 | 15326-15328 | 0.38 | inline_safe | bracket | `EX=\int_0^1 2x^2\,\mathrm{d}x=\frac23,` |
| 1786 | 15329-15331 | 0.41 | inline_safe | bracket | `EX^2=\int_0^1 2x^3\,\mathrm{d}x=\frac12,` |
| 1788 | 15336-15338 | 0.16 | inline_safe | bracket | `\operatorname{Cov}(X,Y)=0.` |
| 1789 | 15345-15347 | 0.35 | inline_safe | bracket | `1\le x\le2,\qquad 1\le y\le3` |
| 1790 | 15355-15357 | 0.21 | inline_safe | bracket | `(2-1)(3-1)=2,` |
| 1791 | 15359-15365 | 0.21 | inline_unsafe_marker | bracket | `f(x,y)= \begin{cases} \dfrac12, & 1<x<2,\ 1<y<3,\\ 0, & \text{其他}. \end{cases}` |
| 1792 | 15367-15370 | 0.34 | normalized_width_not_low | bracket | `f_\xi(x)=\int_1^3\frac12\,\mathrm{d}y =1,\qquad 1<x<2,` |
| 1793 | 15371-15374 | 0.34 | normalized_width_not_low | bracket | `f_\eta(y)=\int_1^2\frac12\,\mathrm{d}x =\frac12,\qquad 1<y<3.` |
| 1794 | 15376-15388 | 0.11 | inline_unsafe_marker | bracket | `f_\xi(x)= \begin{cases} 1, & 1<x<2,\\ 0, & \text{其他}, \end{cases} \qquad f_\eta(y)= \begin{cases} \dfrac12, & 1<y<3,\\ 0, & \text{其他}. \end{cases}` |
| 1795 | 15391-15398 | 0.43 | inline_unsafe_marker | bracket | `\begin{aligned} P(\xi<1.5,\eta<4) &=\int_1^{1.5}\int_1^3 \frac12\,\mathrm{d}y\,\mathrm{d}x\\ &=\int_1^{1.5}1\,\mathrm{d}x =0.5. \end{aligned}` |
| 1797 | 15411-15417 | 0.20 | inline_unsafe_marker | bracket | `f(x,y)= \begin{cases} 1, & \|y\|<x,\ 0<x<1,\\ 0, & \text{其他}. \end{cases}` |
| 1798 | 15422-15424 | 0.36 | inline_safe | bracket | `f_X(x)=\int_{-x}^{x}1\,\mathrm{d}y=2x.` |
| 1799 | 15426-15428 | 0.40 | inline_safe | bracket | `f_{Y\|X}(y\|x)=\frac{f(x,y)}{f_X(x)}=\frac1{2x}.` |
| 1800 | 15430-15436 | 0.24 | inline_unsafe_marker | bracket | `f_{Y\|X}(y\|x)= \begin{cases} \dfrac1{2x}, & 0<x<1,\ -x<y<x,\\[6pt] 0, & \text{其他}. \end{cases}` |
| 1801 | 15441-15443 | 0.13 | inline_safe | bracket | `Z=3X+2Y` |
| 1802 | 15448-15450 | 0.28 | inline_safe | bracket | `U=3X,\qquad V=2Y.` |
| 1803 | 15452-15454 | 0.45 | inline_safe | bracket | `f_U(u)=\frac{\lambda}{3}e^{-\lambda u/3},\qquad u>0,` |
| 1804 | 15455-15457 | 0.45 | inline_safe | bracket | `f_V(v)=\frac{\mu}{2}e^{-\mu v/2},\qquad v>0.` |
| 1805 | 15459-15469 | 0.37 | inline_unsafe_marker | bracket | `\begin{aligned} f_Z(z) &=\int_0^z f_U(u)f_V(z-u)\,\mathrm{d}u\\ &=\int_0^z \frac{\lambda}{3}e^{-\lambda u/3} \frac{\mu}{2}e^{-\mu(z-u)/2}\,\mathrm{d}u\\ &=\frac{\lambda\mu}{6}e^...` |
| 1806 | 15471-15476 | 0.29 | normalized_width_not_low | bracket | `f_Z(z)= \frac{\lambda\mu}{6} \frac{e^{-\mu z/2}-e^{-\lambda z/3}}{\lambda/3-\mu/2}, \qquad z>0.` |
| 1807 | 15478-15483 | 0.29 | normalized_width_not_low | bracket | `f_Z(z)= \frac{\lambda\mu}{2\lambda-3\mu} \left(e^{-\mu z/2}-e^{-\lambda z/3}\right), \qquad z>0.` |
| 1808 | 15485-15487 | 0.47 | inline_safe | bracket | `f_Z(z)=\frac{\lambda\mu}{6}z e^{-\lambda z/3},\qquad z>0.` |
| 1809 | 15489-15501 | 0.29 | inline_unsafe_marker | bracket | `f_Z(z)= \begin{cases} \displaystyle \frac{\lambda\mu}{2\lambda-3\mu} \left(e^{-\mu z/2}-e^{-\lambda z/3}\right), & z>0,\ 2\lambda\ne3\mu,\\[10pt] \displaystyle \frac{\lambda\mu}...` |
| 1810 | 15509-15511 | 0.11 | inline_safe | bracket | `W=X+Y.` |
| 1811 | 15515-15519 | 0.36 | normalized_width_not_low | bracket | `P(W=0)=(1-p)^2,\qquad P(W=1)=2p(1-p),\qquad P(W=2)=p^2.` |
| 1812 | 15521-15523 | 0.45 | inline_safe | bracket | `P(Z=1)=p,\qquad P(Z=0)=1-p.` |
| 1813 | 15525-15528 | 0.27 | inline_safe | bracket | `P(W=w,Z=z) =P(X+Y=w)P(Z=z),` |
| 1814 | 15530-15532 | 0.39 | inline_safe | bracket | `P(W=w,Z=z)=P(W=w)P(Z=z).` |
| 1815 | 15540-15542 | 0.27 | inline_safe | bracket | `y=x^2,\qquad y=x` |
| 1816 | 15544-15554 | 0.19 | inline_unsafe_marker | bracket | `\begin{array}{ll} \text{A. } f(x,y)=\begin{cases}6, & (x,y)\in G,\\0, & \text{其他},\end{cases} & \text{B. } f(x,y)=\begin{cases}1/6, & (x,y)\in G,\\0, & \text{其他},\end{cases} \\[...` |
| 1817 | 15560-15565 | 0.32 | normalized_width_not_low | bracket | `S_G=\int_0^1(x-x^2)\,\mathrm{d}x =\left[\frac{x^2}{2}-\frac{x^3}{3}\right]_0^1 =\frac12-\frac13 =\frac16.` |
| 1818 | 15567-15573 | 0.24 | inline_unsafe_marker | bracket | `f(x,y)= \begin{cases} 6, & 0<x<1,\ x^2<y<x,\\ 0, & \text{其他}. \end{cases}` |
| 1819 | 15578-15580 | 0.34 | inline_safe | bracket | `(X,Y)\sim N(0,0.5;\ 0,0.5;\ 0),` |
| 1820 | 15591-15593 | 0.37 | inline_safe | bracket | `D(X-Y)=DX+DY-2\operatorname{Cov}(X,Y).` |
| 1821 | 15595-15597 | 0.32 | inline_safe | bracket | `\operatorname{Cov}(X,Y)=\rho\sqrt{DX}\sqrt{DY}=0,` |
| 1822 | 15599-15601 | 0.22 | inline_safe | bracket | `Z=X-Y\sim N(0,1).` |
| 1824 | 15607-15610 | 0.34 | normalized_width_not_low | bracket | `D(\|Z\|)=E(\|Z\|^2)-[E\|Z\|]^2 =1-\frac2\pi.` |
| 1825 | 15620-15622 | 0.42 | inline_safe | bracket | `f_X(x)=\frac1a,\qquad 0<x<a.` |
| 1827 | 15628-15631 | 0.45 | normalized_width_not_low | bracket | `f(x,y)=f_X(x)f_{Y\|X}(y\|x) =\frac1{a(a-x)},\qquad 0<x<y<a,` |
| 1828 | 15633-15639 | 0.18 | inline_unsafe_marker | bracket | `f(x,y)= \begin{cases} \dfrac1{a(a-x)}, & 0<x<y<a,\\[8pt] 0, & \text{其他}. \end{cases}` |
| 1829 | 15642-15646 | 0.42 | normalized_width_not_low | bracket | `f_Y(y)=\int_0^y \frac1{a(a-x)}\,\mathrm{d}x =\frac1a\left[-\ln(a-x)\right]_0^y =\frac1a\ln\frac{a}{a-y}.` |
| 1830 | 15648-15654 | 0.20 | inline_unsafe_marker | bracket | `f_Y(y)= \begin{cases} \dfrac1a\ln\dfrac{a}{a-y}, & 0<y<a,\\[10pt] 0, & \text{其他}. \end{cases}` |
| 1832 | 15782-15784 | 0.30 | inline_safe | bracket | `EX = \sum_{i=1}^{\infty} x_i p_i.` |
| 1833 | 15787-15789 | 0.33 | inline_safe | bracket | `EX = \int_{-\infty}^{+\infty} x f(x)\,\mathrm{d}x.` |
| 1834 | 15795-15797 | 0.45 | inline_safe | bracket | `f(x) = \frac{1}{\pi(1+x^2)}, \quad -\infty < x < +\infty,` |
| 1836 | 15816-15819 | 0.28 | inline_unsafe_marker | bracket | `X \sim f(x) = \begin{cases} 2x\theta^2, & 0 < x < \dfrac{1}{\theta}\ (\theta > 0), \\[4pt] 0, & \text{其他}, \end{cases} \quad E[a(X+2Y)] = \frac{1}{\theta},` |
| 1838 | 15833-15835 | 0.44 | inline_safe | bracket | `E[a(X+2Y)] = 3a\cdot\frac{2}{3\theta} = \frac{2a}{\theta} = \frac{1}{\theta},` |
| 1840 | 15853-15855 | 0.39 | inline_safe | bracket | `\lambda^2 - 2\lambda + 2 = 1 \implies (\lambda - 1)^2 = 0,` |
| 1845 | 15904-15906 | 0.46 | inline_unsafe_marker | bracket | `Y = \begin{cases} 500n + 300(X-n) = 300X + 200n, & X \geqslant n, \\[4pt] 500X - 200(n-X) = 700X - 200n, & X < n. \end{cases}` |
| 1848 | 15926-15928 | 0.31 | inline_unsafe_marker | bracket | `L(y,X) = \begin{cases} 3y, & X \geqslant y, \\[4pt] 3X - (y - X) = 4X - y, & X < y. \end{cases}` |
| 1854 | 15959-15961 | 0.25 | inline_safe | bracket | `120+250=370\text{（万元）}.` |
| 1855 | 15968-15970 | 0.40 | inline_safe | bracket | `E[g(X)] = \sum_{i=1}^{\infty} g(x_i) p_i.` |
| 1856 | 15972-15974 | 0.43 | inline_safe | bracket | `E[g(X)] = \int_{-\infty}^{+\infty} g(x) f(x)\,\mathrm{d}x.` |
| 1857 | 15982-15984 | 0.43 | inline_safe | bracket | `\int_{-\infty}^{+\infty}\frac{\|x\|}{\pi(1+x^2)}\,\mathrm{d}x = +\infty,` |
| 1858 | 15996-16000 | 0.47 | normalized_width_not_low | bracket | `P(X=0)=0.9^2,\qquad P(X=1)=\mathrm{C}_2^1\cdot 0.1\cdot 0.9,\qquad P(X=2)=0.1^2.` |
| 1860 | 16010-16012 | 0.42 | inline_safe | bracket | `E(2^X)=0.81+0.36+0.04=1.21.` |
| 1861 | 16019-16021 | 0.14 | inline_safe | bracket | `Y=2^X-1.` |
| 1862 | 16026-16028 | 0.29 | inline_safe | bracket | `E(t^X)=(1-p+pt)^n.` |
| 1864 | 16034-16036 | 0.43 | inline_safe | bracket | `EY=E(2^X-1)=1.331-1=0.331.` |
| 1866 | 16056-16058 | 0.30 | inline_unsafe_marker | bracket | `f(y) = \begin{cases} \dfrac{y}{a^2}\,e^{-\frac{y^2}{2a^2}}, & y > 0,\ a > 0, \\[4pt] 0, & y \leqslant 0, \end{cases}` |
| 1868 | 16069-16071 | 0.49 | inline_safe | bracket | `\int_0^{+\infty}\frac{1}{\sqrt{2\pi}\,a}\,e^{-\frac{y^2}{2a^2}}\,\mathrm{d}y = \frac{1}{2},` |
| 1869 | 16073-16075 | 0.38 | inline_safe | bracket | `EZ = \frac{1}{a^2}\cdot\frac{\sqrt{2\pi}\,a}{2} = \frac{\sqrt{2\pi}}{2a}.` |
| 1870 | 16080-16082 | 0.36 | inline_safe | bracket | `D=\{(x,y)\mid 1\le x^2+y^2\le2\}` |
| 1871 | 16087-16089 | 0.43 | inline_safe | bracket | `f(x,y)=\frac1{8\pi}\exp\!\left\{-\frac{x^2+y^2}{8}\right\}.` |
| 1872 | 16091-16099 | 0.44 | inline_unsafe_marker | bracket | `\begin{aligned} P\{(X,Y)\in D\} &=\int_0^{2\pi}\int_1^{\sqrt2} \frac1{8\pi}e^{-r^2/8}\,r\,\mathrm dr\,\mathrm d\theta\\ &=\frac14\int_1^{\sqrt2}r e^{-r^2/8}\,\mathrm dr =e^{-1/8...` |
| 1873 | 16101-16103 | 0.46 | inline_safe | bracket | `f_R(r)=\frac{r}{4}e^{-r^2/8},\qquad r>0.` |
| 1874 | 16105-16108 | 0.46 | normalized_width_not_low | bracket | `EZ=\int_0^{+\infty}r\cdot\frac{r}{4}e^{-r^2/8}\,\mathrm dr =2\sqrt{\frac\pi2}=\sqrt{2\pi}.` |
| 1875 | 16117-16119 | 0.07 | inline_unsafe_marker | bracket | `Y = \begin{cases} 1, & X > 0, \\ 0, & X = 0, \\ -1, & X < 0, \end{cases}` |
| 1877 | 16147-16149 | 0.38 | inline_safe | bracket | `U + V = X + Y, \quad U \cdot V = X \cdot Y.` |
| 1881 | 16174-16174 | 0.46 | display_environment | dollar | `P(X = k) = \frac{\lambda^k e^{-\lambda}}{k!}, \quad k = 0, 1, 2, \dots` |
| 1886 | 16189-16189 | 0.26 | display_environment | dollar | `E[Y] = 1 - \frac{1 - e^{-\lambda}}{\lambda}` |
| 1888 | 16206-16206 | 0.23 | display_environment | dollar | `X = X_1 + X_2 + X_3` |
| 1890 | 16212-16212 | 0.23 | display_environment | dollar | `P(X_1 = 1) = \frac{a}{a+b}` |
| 1892 | 16222-16222 | 0.23 | display_environment | dollar | `P(X_3 = 1) = \frac{a}{a+b}` |
| 1899 | 16288-16290 | 0.40 | inline_safe | bracket | `f(x)=\frac12x,\qquad 0<x<2,` |
| 1900 | 16292-16297 | 0.36 | normalized_width_not_low | bracket | `EX=\int_0^2 x\cdot \frac12x\,\mathrm dx =\frac12\int_0^2 x^2\,\mathrm dx =\frac12\cdot\frac{8}{3} =\frac43.` |
| 1901 | 16303-16305 | 0.39 | inline_safe | bracket | `P\{F(X)>EX-1\}=P\left(Y>\frac13\right).` |
| 1902 | 16307-16309 | 0.44 | inline_safe | bracket | `P\left(Y>\frac13\right)=1-\frac13=\frac23.` |
| 1903 | 16315-16317 | 0.11 | inline_unsafe_marker | bracket | `F(x) = \begin{cases} 0, & x \leqslant 0, \\ \dfrac{x^2}{4}, & 0 < x < 2, \\ 1, & x \geqslant 2. \end{cases}` |
| 1904 | 16329-16331 | 0.38 | inline_safe | bracket | `E(XY) = EX \cdot EY = 1 \times \frac{1}{3} = \frac{1}{3}.` |
| 1905 | 16339-16342 | 0.18 | inline_unsafe_marker | bracket | `f_X(x) = \begin{cases} 3x^2, & 0 < x < 1, \\ 0, & \text{其他}, \end{cases}\quad f_Y(y) = \begin{cases} 2y, & 0 < y < 1, \\ 0, & \text{其他}, \end{cases}` |
| 1907 | 16363-16363 | 0.21 | inline_unsafe_marker | bracket | `f_{X_i}(x_i) =\begin{cases}\displaystyle \frac{1}{3}, & 0 < x_i < 3 \\0, & \text{其他}\end{cases}\quad (i=1,2)` |
| 1912 | 16383-16385 | 0.41 | inline_safe | bracket | `DD = ED^2 - (ED)^2 = \frac{3}{2} - 1 = \frac{1}{2}.` |
| 1913 | 16390-16392 | 0.22 | inline_safe | bracket | `\boldsymbol{E(X_{(k)}) = \frac{k}{n+1}}` |
| 1916 | 16406-16408 | 0.43 | inline_safe | bracket | `E(X_{(k)}) = \frac{k}{k + (n-k+1)} = \frac{k}{n+1}` |
| 1917 | 16413-16416 | 0.36 | normalized_width_not_low | bracket | `M = \max\{X_1, \dots, X_n\},\qquad N = \min\{X_1, \dots, X_n\}` |
| 1923 | 16464-16464 | 0.30 | display_environment | dollar | `P(Y \le 1) = \left(\frac{1}{3}\right)^3 = \frac{1}{27}` |
| 1924 | 16465-16465 | 0.30 | display_environment | dollar | `P(Y \le 2) = \left(\frac{2}{3}\right)^3 = \frac{8}{27}` |
| 1925 | 16466-16466 | 0.22 | display_environment | dollar | `P(Y \le 3) = 1^3 = 1` |
| 1926 | 16468-16468 | 0.30 | display_environment | dollar | `P(Y = 1) = P(Y \le 1) = \frac{1}{27}` |
| 1930 | 16489-16491 | 0.45 | inline_safe | bracket | `DX = E[(X - EX)^2] = E(X^2) - (EX)^2.` |
| 1931 | 16503-16505 | 0.36 | inline_safe | bracket | `Y=\frac1{10}\sum_{i=1}^{10}X_i,` |
| 1932 | 16513-16518 | 0.42 | normalized_width_not_low | bracket | `D(Y)=D\!\left(\frac1{10}\sum_{i=1}^{10}X_i\right) =\frac1{100}\sum_{i=1}^{10}D(X_i) =\frac1{100}\cdot10A =0.1A.` |
| 1933 | 16525-16527 | 0.14 | inline_unsafe_marker | bracket | `F(x) = \begin{cases} 0, & x < -1, \\ 0.2, & -1 \leqslant x < 0, \\ 0.8, & 0 \leqslant x < 1, \\ 1, & x \geqslant 1, \end{cases}` |
| 1934 | 16533-16535 | 0.09 | inline_unsafe_marker | bracket | `X \sim \begin{pmatrix} -1 & 0 & 1 \\ 0.2 & 0.6 & 0.2 \end{pmatrix}.` |
| 1938 | 16550-16550 | 0.12 | display_environment | dollar | `f(x) = \begin{cases} 2x, & 0 < x < 1, \\ 0, & \text{其他.} \end{cases}` |
| 1945 | 16602-16604 | 0.15 | inline_safe | bracket | `10\sqrt{\frac{1}{4}} = 5.` |
| 1946 | 16609-16611 | 0.17 | inline_unsafe_marker | bracket | `f(x) = \begin{cases} \dfrac{1}{2}\sin x, & 0 \leqslant x \leqslant \pi, \\[4pt] 0, & \text{其他}, \end{cases}` |
| 1947 | 16616-16621 | 0.37 | normalized_width_not_low | bracket | `P\!\left(X > \frac{\pi}{3}\right) = \int_{\frac{\pi}{3}}^{\pi} \frac{1}{2}\sin x\,\mathrm{d}x = \frac12\bigl[-\cos x\bigr]_{\pi/3}^{\pi} = \frac12\left(1+\frac12\right) = \frac34.` |
| 1948 | 16624-16626 | 0.20 | inline_safe | bracket | `Y\sim B\!\left(4,\frac34\right).` |
| 1951 | 16651-16653 | 0.35 | inline_safe | bracket | `D(X \pm Y) = DX + DY \pm 2\,\mathrm{Cov}(X,Y).` |
| 1957 | 16702-16704 | 0.31 | inline_safe | bracket | `g'(c) = -2EX + 2c \stackrel{\text{令}}{=} 0,` |
| 1958 | 16719-16721 | 0.27 | inline_safe | bracket | `E(X+Y)=E(X)+E(Y).` |
| 1959 | 16723-16725 | 0.48 | inline_safe | bracket | `E(XY)=E(X)E(Y),\qquad \operatorname{Cov}(X,Y)=0,` |
| 1960 | 16727-16729 | 0.25 | inline_safe | bracket | `D(X\pm Y)=D(X)+D(Y).` |
| 1962 | 16738-16738 | 0.36 | display_environment | dollar | `\boldsymbol{E(\overline{X}) = \mu}, \quad \boldsymbol{D(\overline{X}) = \frac{\sigma^2}{n}}` |
| 1965 | 16756-16758 | 0.19 | inline_safe | bracket | `E(XY)=EX\cdot EY` |
| 1966 | 16760-16762 | 0.38 | inline_safe | bracket | `\mathrm{Cov}(X,Y)=E(XY)-EX\cdot EY=0.` |
| 1967 | 16772-16774 | 0.47 | inline_safe | bracket | `D(XY)=DX\cdot DY+DX(EY)^2+DY(EX)^2,` |
| 1968 | 16778-16780 | 0.36 | inline_safe | bracket | `D(X+Y)=DX+DY+2\mathrm{Cov}(X,Y)` |
| 1969 | 16792-16794 | 0.37 | inline_safe | bracket | `D(X+Y)=DX+DY+2\mathrm{Cov}(X,Y),` |
| 1971 | 16801-16803 | 0.37 | inline_safe | bracket | `D(X-Y)=DX+DY-2\mathrm{Cov}(X,Y),` |
| 1973 | 16821-16823 | 0.37 | inline_safe | bracket | `D(X+Y)=DX+DY+2\mathrm{Cov}(X,Y).` |
| 1974 | 16826-16828 | 0.37 | inline_safe | bracket | `2\mathrm{Cov}(X,Y)=0 \implies \mathrm{Cov}(X,Y)=0.` |
| 1978 | 16870-16872 | 0.35 | inline_safe | bracket | `-x^2+2x-1=-(x-1)^2.` |
| 1979 | 16874-16878 | 0.36 | normalized_width_not_low | bracket | `f(x)=\frac1{\sqrt{\pi}}e^{-(x-1)^2} =\frac{1}{\sqrt{2\pi}\cdot(1/\sqrt2)} \exp\!\left\{-\frac{(x-1)^2}{2(1/2)}\right\}.` |
| 1980 | 16880-16882 | 0.21 | inline_safe | bracket | `X\sim N\left(1,\frac12\right),` |
| 1981 | 16884-16886 | 0.11 | inline_safe | bracket | `E(X)=1.` |
| 1985 | 16920-16922 | 0.39 | inline_safe | bracket | `F_U(u) = \frac{4u - u^2}{4} = \frac{(4-u)u}{4}.` |
| 1986 | 16924-16926 | 0.32 | inline_unsafe_marker | bracket | `f_U(u) = F_U'(u) = \begin{cases} \dfrac{2-u}{2}, & 0 < u < 2, \\[4pt] 0, & \text{其他}. \end{cases}` |
| 1987 | 16959-16959 | 0.33 | inline_safe | bracket | `EX = 1\cdot p + 0\cdot(1-p) = p.` |
| 1988 | 16960-16960 | 0.42 | inline_safe | bracket | `EX^2 = 1^2\cdot p + 0^2\cdot(1-p) = p.` |
| 1989 | 16961-16961 | 0.47 | inline_safe | bracket | `DX = EX^2 - (EX)^2 = p - p^2 = p(1-p).` |
| 1994 | 16973-16973 | 0.46 | inline_safe | bracket | `DX = EX^2 - (EX)^2 = \lambda^2 + \lambda - \lambda^2 = \lambda.` |
| 2007 | 17024-17026 | 0.38 | inline_safe | bracket | `D(\chi^2) = \sum_{i=1}^{n}D(X_i^2).` |
| 2009 | 17031-17033 | 0.15 | inline_safe | bracket | `D(\chi^2) = 2n.` |
| 2016 | 17131-17133 | 0.48 | inline_safe | bracket | `P(X_{(5)} < 3) = [P(X_1 < 3)]^5 = [\Phi(1)]^5.` |
| 2018 | 17139-17143 | 0.44 | normalized_width_not_low | bracket | `\mathrm{Cov}(X_1,\bar X) =\mathrm{Cov}\!\left(X_1,\frac15\sum_{i=1}^{5}X_i\right) =\frac15\sum_{i=1}^{5}\mathrm{Cov}(X_1,X_i).` |
| 2019 | 17146-17148 | 0.49 | inline_safe | bracket | `\mathrm{Cov}(X_1,X_i)=0\qquad (i=2,3,4,5),` |
| 2020 | 17150-17152 | 0.26 | inline_safe | bracket | `\mathrm{Cov}(X_1,X_1)=DX_1.` |
| 2021 | 17154-17156 | 0.35 | inline_safe | bracket | `\mathrm{Cov}(X_1,\bar X)=\frac15\,DX_1.` |
| 2022 | 17159-17161 | 0.29 | inline_safe | bracket | `\mathrm{Cov}(X_1,\bar X)=\frac45.` |
| 2023 | 17167-17169 | 0.19 | inline_safe | bracket | `P\!\left(\|2X-Y\|\ge1\right).` |
| 2025 | 17179-17181 | 0.25 | inline_safe | bracket | `W=\frac{Z+1}{5}\sim N(0,1).` |
| 2026 | 17183-17185 | 0.48 | inline_safe | bracket | `P(\|2X-Y\|\ge1)=P(Z\le-1)+P(Z\ge1).` |
| 2028 | 17192-17194 | 0.48 | inline_safe | bracket | `P(\|2X-Y\|\ge1)=0.5+0.3446=0.8446.` |
| 2029 | 17199-17205 | 0.08 | inline_unsafe_marker | bracket | `\begin{array}{c\|cccc} (X,Y) & (1,0) & (1,1) & (2,0) & (2,1) \\ \hline P & 0.4 & 0.2 & a & b \end{array}` |
| 2030 | 17210-17212 | 0.42 | inline_safe | bracket | `0.4+0.2+a+b=1 \implies a+b=0.4.` |
| 2031 | 17214-17216 | 0.46 | inline_safe | bracket | `E(XY)=1\cdot1\cdot0.2+2\cdot1\cdot b=0.8,` |
| 2034 | 17232-17234 | 0.20 | inline_unsafe_marker | bracket | `f(x,y) = \begin{cases} xe^{-y}, & 0 < x < y, \\ 0, & \text{其他}, \end{cases}` |
| 2037 | 17254-17261 | 0.07 | inline_unsafe_marker | bracket | `\begin{array}{c\|ccc} X \backslash Y & 0 & 1 & 2 \\ \hline -1 & 0.1 & 0.1 & b \\ 1 & a & 0.1 & 0.1 \end{array}` |
| 2038 | 17267-17270 | 0.47 | display_environment | env:align* | `P\{\max(X,Y)=2\} &= P\{Y=2\} = b + 0.1,\\ P\{\min(X,Y)=1\} &= P\{X=1,Y=1\} + P\{X=1,Y=2\} = 0.2.` |
| 2042 | 17289-17292 | 0.10 | inline_unsafe_marker | bracket | `X \sim \begin{pmatrix} 0 & 1 \\ \frac{1}{4} & \frac{3}{4} \end{pmatrix},\quad Y \sim \begin{pmatrix} 0 & 1 \\ \frac{1}{2} & \frac{1}{2} \end{pmatrix},` |
| 2044 | 17303-17307 | 0.40 | display_environment | env:align* | `P\{X=1,Y=0\} &= P\{X=1\} - P\{X=1,Y=1\} = \frac{1}{4},\\ P\{X=0,Y=1\} &= P\{Y=1\} - P\{X=1,Y=1\} = 0,\\ P\{X=0,Y=0\} &= P\{X=0\} = \frac{1}{4}.` |
| 2045 | 17309-17318 | 0.08 | inline_unsafe_marker | bracket | `\begin{array}{c\|cc\|c} X \backslash Y & 0 & 1 & P_i \\ \hline 0 & \frac{1}{4} & 0 & \frac{1}{4} \\[4pt] 1 & \frac{1}{4} & \frac{1}{2} & \frac{3}{4} \\ \hline P_j & \frac{1}{2} & ...` |
| 2046 | 17326-17328 | 0.23 | inline_safe | bracket | `\rho_{XY} = \frac{\mathrm{Cov}(X,Y)}{\sqrt{DX \cdot DY}}` |
| 2048 | 17358-17360 | 0.49 | inline_safe | bracket | `DY - 2t\,\mathrm{Cov}(X,Y) + t^2 DX \geqslant 0, \quad \forall\, t \in \mathbb{R}.` |
| 2050 | 17425-17427 | 0.38 | inline_safe | bracket | `X \sim B(n, p_1), \quad Y \sim B(n, p_2)` |
| 2052 | 17435-17445 | 0.11 | inline_unsafe_marker | bracket | `X_i = \begin{cases} 1, & \text{第 } i \text{ 次摸出红球}, \\ 0, & \text{其他}, \end{cases} \qquad Y_i = \begin{cases} 1, & \text{第 } i \text{ 次摸出白球}, \\ 0, & \text{其他}, \end{cases}` |
| 2056 | 17469-17474 | 0.44 | display_environment | env:align* | `r(X,Y) &= \frac{\text{Cov}(X,Y)}{\sqrt{D(X)} \sqrt{D(Y)}} \\[6pt] &= \frac{-n p_1 p_2}{\sqrt{np_1(1-p_1)} \sqrt{np_2(1-p_2)}} \\[6pt] &= \frac{-n p_1 p_2}{n \sqrt{p_1 p_2 (1-p_1...` |
| 2058 | 17489-17491 | 0.27 | inline_unsafe_marker | bracket | `f(x,y) = \begin{cases} 24y(1-x), & 0 \leqslant x \leqslant 1,\ 0 \leqslant y \leqslant x, \\ 0, & \text{其他}, \end{cases}` |
| 2061 | 17518-17524 | 0.27 | inline_unsafe_marker | bracket | `f(x,y)= \begin{cases} A(x+y), & 0\le x\le1,\ 0\le y\le2,\\ 0, & \text{其他}. \end{cases}` |
| 2062 | 17529-17531 | 0.30 | inline_safe | bracket | `D=\{0\le x\le1,\ y\ge x^2\}` |
| 2063 | 17536-17539 | 0.45 | normalized_width_not_low | bracket | `1=A\int_0^1\int_0^2(x+y)\,\mathrm dy\,\mathrm dx =A\int_0^1(2x+2)\,\mathrm dx=3A,` |
| 2064 | 17541-17543 | 0.14 | inline_safe | bracket | `A=\frac13.` |
| 2068 | 17561-17565 | 0.33 | normalized_width_not_low | bracket | `\operatorname{Cov}(X,Y)=E(XY)-E(X)E(Y) =\frac23-\frac59\cdot\frac{11}{9} =-\frac1{81}.` |
| 2073 | 17584-17589 | 0.28 | normalized_width_not_low | bracket | `\rho_{XY} =\frac{\operatorname{Cov}(X,Y)}{\sqrt{D(X)}\sqrt{D(Y)}} =\frac{-1/81}{\sqrt{(13/162)(23/81)}} =-\sqrt{\frac{2}{299}}.` |
| 2075 | 17602-17604 | 0.40 | inline_safe | bracket | `P\{(X,Y)\in D\}=1-\frac7{60}=\frac{53}{60}.` |
| 2076 | 17611-17618 | 0.13 | inline_unsafe_marker | bracket | `f_X(x)= \begin{cases} \dfrac12, & -1<x<0,\\[4pt] \dfrac14, & 0\le x<2,\\[4pt] 0, & \text{其他}. \end{cases}` |
| 2077 | 17626-17630 | 0.43 | normalized_width_not_low | bracket | `f_Y(y)=\frac{f_X(-\sqrt y)}{2\sqrt y}+\frac{f_X(\sqrt y)}{2\sqrt y} =\frac{1/2+1/4}{2\sqrt y} =\frac{3}{8\sqrt y}.` |
| 2078 | 17632-17635 | 0.24 | inline_safe | bracket | `f_Y(y)=\frac{f_X(\sqrt y)}{2\sqrt y} =\frac{1}{8\sqrt y}.` |
| 2079 | 17637-17644 | 0.11 | inline_unsafe_marker | bracket | `f_Y(y)= \begin{cases} \dfrac{3}{8\sqrt y}, & 0<y<1,\\[6pt] \dfrac{1}{8\sqrt y}, & 1<y<4,\\[6pt] 0, & \text{其他}. \end{cases}` |
| 2083 | 17660-17664 | 0.35 | normalized_width_not_low | bracket | `\operatorname{Cov}(X,Y)=EXY-EX\,EY =\frac78-\frac14\cdot\frac56 =\frac23.` |
| 2084 | 17667-17670 | 0.37 | normalized_width_not_low | bracket | `F\!\left(-\frac12,4\right) =P\left\{X\le-\frac12,\ X^2\le4\right\}.` |
| 2085 | 17672-17677 | 0.36 | normalized_width_not_low | bracket | `F\!\left(-\frac12,4\right) =P\left\{-1<X\le-\frac12\right\} =\int_{-1}^{-1/2}\frac12\,\mathrm dx =\frac14.` |
| 2086 | 17688-17691 | 0.24 | inline_safe | bracket | `F_\eta(y)=P(2^\xi\le y) =P\left(\xi\le\frac{\ln y}{\ln2}\right).` |
| 2087 | 17693-17698 | 0.21 | normalized_width_not_low | bracket | `f_\eta(y) =\frac{1}{2\sqrt{2\pi}\,y\ln2} \exp\left\{-\frac{(\ln y)^2}{8\ln^2 2}\right\}, \qquad y>0,` |
| 2088 | 17702-17706 | 0.29 | normalized_width_not_low | bracket | `E\eta=E e^{(\ln2)\xi} =\exp\left\{\frac12\cdot4\ln^2 2\right\} =e^{2\ln^2 2}=2^{2\ln2}.` |
| 2089 | 17709-17713 | 0.37 | normalized_width_not_low | bracket | `E\eta^2=E e^{2(\ln2)\xi} =\exp\left\{\frac12\cdot4\cdot(2\ln2)^2\right\} =e^{8\ln^2 2}.` |
| 2090 | 17715-17718 | 0.31 | normalized_width_not_low | bracket | `D\eta=e^{8\ln^2 2}-e^{4\ln^2 2} =2^{4\ln2}\left(2^{4\ln2}-1\right).` |
| 2091 | 17729-17731 | 0.27 | inline_safe | bracket | `F_\eta(y)=P\left(\xi\le\frac{\ln y}{\ln3}\right),` |
| 2092 | 17733-17738 | 0.21 | normalized_width_not_low | bracket | `f_\eta(y) =\frac{1}{2\sqrt{2\pi}\,y\ln3} \exp\left\{-\frac{(\ln y)^2}{8\ln^2 3}\right\}, \qquad y>0.` |
| 2093 | 17742-17745 | 0.27 | inline_safe | bracket | `E\eta=E e^{(\ln3)\xi} =e^{2\ln^2 3}=3^{2\ln3},` |
| 2094 | 17746-17749 | 0.22 | inline_safe | bracket | `E\eta^2=E e^{2(\ln3)\xi} =e^{8\ln^2 3}.` |
| 2095 | 17751-17754 | 0.31 | normalized_width_not_low | bracket | `D\eta=e^{8\ln^2 3}-e^{4\ln^2 3} =3^{4\ln3}\left(3^{4\ln3}-1\right).` |
| 2097 | 17801-17803 | 0.28 | inline_safe | bracket | `DY=D(aX+b)=a^2DX.` |
| 2098 | 17806-17811 | 0.21 | normalized_width_not_low | bracket | `\rho_{XY} =\frac{\mathrm{Cov}(X,Y)}{\sqrt{DX}\sqrt{DY}} =\frac{aDX}{\sqrt{DX}\sqrt{a^2DX}} =\frac{a}{\|a\|}.` |
| 2099 | 17814-17816 | 0.11 | inline_unsafe_marker | bracket | `\rho_{XY} = \begin{cases} 1, & a > 0, \\ -1, & a < 0. \end{cases}` |
| 2100 | 17825-17827 | 0.27 | inline_safe | bracket | `Y=X_1-2X_2+3X_3.` |
| 2103 | 17840-17842 | 0.35 | inline_safe | bracket | `D(Y)=3+4\cdot4+9\cdot3=46.` |
| 2104 | 17847-17849 | 0.22 | inline_safe | bracket | `D(X-3Y-4)=\text{（\quad）}.` |
| 2105 | 17857-17860 | 0.43 | normalized_width_not_low | bracket | `DX=3,\qquad DY=8\cdot\frac13\left(1-\frac13\right)=\frac{16}{9}.` |
| 2107 | 17869-17872 | 0.13 | inline_unsafe_marker | bracket | `X = \begin{cases} 1, & A \text{ 发生}, \\ 0, & A \text{ 不发生}, \end{cases}\quad Y = \begin{cases} 1, & B \text{ 发生}, \\ 0, & B \text{ 不发生}. \end{cases}` |
| 2113 | 17904-17911 | 0.09 | inline_unsafe_marker | bracket | `\begin{array}{c\|ccc} \xi\backslash \eta & -1 & 0 & 1\\ \hline 0 & \dfrac16 & \dfrac13 & \dfrac16\\[4pt] 1 & \dfrac16 & 0 & \dfrac16 \end{array}` |
| 2119 | 17940-17942 | 0.35 | inline_safe | bracket | `\operatorname{Cov}(\xi,\eta)=E(\xi\eta)-E\xi\,E\eta=0,` |
| 2120 | 17944-17946 | 0.11 | inline_safe | bracket | `\rho_{\xi\eta}=0.` |
| 2121 | 17948-17951 | 0.36 | normalized_width_not_low | bracket | `D(\xi-\eta)=D\xi+D\eta-2\operatorname{Cov}(\xi,\eta) =\frac29+\frac23=\frac89.` |
| 2122 | 17956-17967 | 0.07 | inline_unsafe_marker | bracket | `\begin{array}{c\|ccc} X & 0 & 1 & 2 \\ \hline P & \frac{1}{3} & \frac{1}{3} & \frac{1}{3} \end{array},\quad \begin{array}{c\|ccc} Y & -1 & 0 & 1 \\ \hline P & \frac{1}{3} & \frac{...` |
| 2124 | 17980-17984 | 0.30 | normalized_width_not_low | bracket | `P\{X=0,Y=0\} = \frac{1}{3},\quad P\{X=1,Y=1\} = \frac{1}{3},\quad P\{X=1,Y=-1\} = \frac{1}{3}.` |
| 2125 | 17986-17995 | 0.09 | inline_unsafe_marker | bracket | `\begin{array}{c\|ccc\|c} X \backslash Y & -1 & 0 & 1 & P_i \\ \hline 0 & 0 & \frac{1}{3} & 0 & \frac{1}{3} \\[4pt] 1 & \frac{1}{3} & 0 & \frac{1}{3} & \frac{2}{3} \\ \hline P_j & ...` |
| 2126 | 17997-18001 | 0.30 | display_environment | env:align* | `P\{Z=-1\} &= P\{X=1,Y=-1\} = \frac{1}{3},\\ P\{Z=0\} &= P\{X=0,Y=0\} = \frac{1}{3},\\ P\{Z=1\} &= P\{X=1,Y=1\} = \frac{1}{3}.` |
| 2127 | 18016-18023 | 0.10 | inline_unsafe_marker | bracket | `\begin{array}{c\|cc} X_1 \backslash X_2 & -1 & 1 \\ \hline -1 & \frac{1}{6} & \frac{1}{3} \\[4pt] 1 & \frac{1}{3} & \frac{1}{6} \end{array}` |
| 2128 | 18037-18045 | 0.41 | inline_unsafe_marker | bracket | `\begin{aligned} EY &=\int_{-\infty}^{+\infty} y\,f(-y)\,\mathrm{d}y\\ &=\int_{+\infty}^{-\infty} (-t)\,f(t)\,(-\,\mathrm{d}t)\\ &=-\int_{-\infty}^{+\infty} t\,f(t)\,\mathrm{d}t\...` |
| 2129 | 18047-18049 | 0.31 | inline_safe | bracket | `EZ=EX+EY=EX-EX=0.` |
| 2130 | 18052-18059 | 0.35 | inline_unsafe_marker | bracket | `\begin{aligned} EY^2 &=\int_{-\infty}^{+\infty} y^2 f(-y)\,\mathrm{d}y\\ &=\int_{-\infty}^{+\infty} t^2 f(t)\,\mathrm{d}t\\ &=EX^2. \end{aligned}` |
| 2133 | 18081-18083 | 0.27 | inline_unsafe_marker | bracket | `f_Z(z) = \begin{cases} \lambda^2 z\,e^{-\lambda z}, & z > 0, \\[4pt] 0, & z \leqslant 0. \end{cases}` |
| 2138 | 18137-18139 | 0.35 | inline_safe | bracket | `\int_{-\infty}^{+\infty} x^3 f(x)\,\mathrm{d}x = 0.` |
| 2140 | 18152-18155 | 0.40 | normalized_width_not_low | bracket | `EX = \int_{-\pi}^{\pi} \frac{\sin\theta}{2\pi}\,\mathrm{d}\theta = 0,\quad EY = \int_{-\pi}^{\pi} \frac{\cos\theta}{2\pi}\,\mathrm{d}\theta = 0,` |
| 2142 | 18175-18177 | 0.35 | inline_safe | bracket | `\rho_{UV} = \frac{E(UV) - EU \cdot EV}{\sqrt{DU}\sqrt{DV}} = 0.` |
| 2144 | 18203-18209 | 0.37 | inline_unsafe_marker | bracket | `f_Y(y) = \begin{cases} \displaystyle\int_y^1 \frac{1}{x}\,\mathrm{d}x = -\ln y, & 0.5 \leqslant y < 1, \\[8pt] \displaystyle\int_{0.5}^1 \frac{1}{x}\,\mathrm{d}x = \ln 2, & -0.5...` |
| 2148 | 18235-18237 | 0.41 | inline_safe | bracket | `\rho_{Z_1Z_2} = \frac{3\sigma^2}{\sqrt{5\sigma^2}\sqrt{5\sigma^2}} = \frac{3}{5}.` |
| 2150 | 18254-18257 | 0.47 | normalized_width_not_low | bracket | `E\|Z\|=\frac{2}{\sqrt{2\pi}}\int_0^{+\infty} z\,e^{-\frac{z^2}{2}}\,\mathrm{d}z =\sqrt{\frac{2}{\pi}}.` |
| 2151 | 18260-18262 | 0.15 | inline_safe | bracket | `\|Z\|^2=Z^2,` |
| 2155 | 18280-18282 | 0.27 | inline_safe | bracket | `E\max\{\xi,\eta\}=a+\frac{\sigma}{\sqrt{\pi}}.` |
| 2156 | 18286-18288 | 0.38 | inline_safe | bracket | `X=\frac{\xi-a}{\sigma},\qquad Y=\frac{\eta-a}{\sigma}.` |
| 2157 | 18290-18292 | 0.32 | inline_safe | bracket | `\max\{\xi,\eta\}=a+\sigma\max\{X,Y\}.` |
| 2158 | 18296-18298 | 0.34 | inline_safe | bracket | `\max\{X,Y\}=\frac{X+Y+\|X-Y\|}{2},` |
| 2159 | 18300-18304 | 0.42 | normalized_width_not_low | bracket | `E\max\{X,Y\} =\frac12E(X+Y)+\frac12E\|X-Y\| =\frac12E\|X-Y\|.` |
| 2160 | 18306-18308 | 0.18 | inline_safe | bracket | `X-Y\sim N(0,2),` |
| 2161 | 18310-18312 | 0.24 | inline_safe | bracket | `E\|X-Y\|=\sqrt2\,E\|Z\|.` |
| 2163 | 18319-18321 | 0.43 | inline_safe | bracket | `E\|X-Y\|=\sqrt2\sqrt{\frac2\pi}=\frac2{\sqrt{\pi}},` |
| 2164 | 18323-18325 | 0.28 | inline_safe | bracket | `E\max\{X,Y\}=\frac1{\sqrt{\pi}}.` |
| 2165 | 18327-18329 | 0.27 | inline_safe | bracket | `E\max\{\xi,\eta\}=a+\frac{\sigma}{\sqrt{\pi}}.` |
| 2170 | 18360-18362 | 0.48 | inline_safe | bracket | `\rho_{XZ} = \frac{\mathrm{Cov}(X,Z)}{\sqrt{DX}\sqrt{DZ}} = \frac{6}{\sqrt{9 \times 7}} = \frac{2\sqrt{7}}{7}.` |
| 2171 | 18375-18377 | 0.34 | inline_safe | bracket | `(X,Y)\sim N(1,3^2;\,0,4^2,\,0),` |
| 2172 | 18379-18381 | 0.11 | inline_safe | bracket | `\rho_{XY}=0.` |
| 2173 | 18383-18385 | 0.36 | inline_safe | bracket | `\mathrm{Cov}(X,Y)=\rho_{XY}\sqrt{DX}\sqrt{DY}=0.` |
| 2174 | 18388-18390 | 0.15 | inline_safe | bracket | `X\ \text{与}\ Y\ \text{相互独立}.` |
| 2175 | 18393-18395 | 0.33 | inline_safe | bracket | `E(XY) = EX \cdot EY = 1 \times 0 = 0.` |
| 2177 | 18414-18416 | 0.25 | inline_safe | bracket | `D\xi=E(\xi^2)-(E\xi)^2` |
| 2178 | 18418-18420 | 0.48 | inline_safe | bracket | `E(\xi^2)=D\xi+(E\xi)^2=2.4+6^2=38.4.` |
| 2179 | 18430-18432 | 0.23 | inline_safe | bracket | `\rho_{XY}=\frac{\operatorname{Cov}(X,Y)}{\sqrt{DX}\sqrt{DY}},` |
| 2180 | 18434-18437 | 0.31 | normalized_width_not_low | bracket | `\operatorname{Cov}(X,Y)=\rho_{XY}\sqrt{DX}\sqrt{DY} =0.4\times5\times6=12.` |
| 2182 | 18453-18455 | 0.18 | inline_safe | bracket | `P(\xi=5)=q^4.` |
| 2184 | 18475-18477 | 0.23 | inline_safe | bracket | `\rho_{XY}=\frac{\operatorname{Cov}(X,Y)}{\sqrt{DX}\sqrt{DY}},` |
| 2185 | 18479-18481 | 0.21 | inline_safe | bracket | `0.4=\frac{12}{\sqrt{DX}\cdot6}.` |
| 2186 | 18483-18485 | 0.25 | inline_safe | bracket | `\sqrt{DX}=\frac{12}{0.4\times6}=5,` |
| 2187 | 18487-18489 | 0.10 | inline_safe | bracket | `DX=25.` |
| 2188 | 18494-18496 | 0.21 | inline_safe | bracket | `E(XY)=E(X)E(Y),` |
| 2189 | 18507-18509 | 0.20 | inline_safe | bracket | `E(XY)=E(X)E(Y)` |
| 2190 | 18511-18513 | 0.39 | inline_safe | bracket | `\operatorname{Cov}(X,Y)=E(XY)-E(X)E(Y)=0.` |
| 2192 | 18523-18525 | 0.20 | inline_safe | bracket | `E(XY)=E(X)E(Y)` |
| 2193 | 18532-18534 | 0.21 | inline_safe | bracket | `E(XY)=E(X)E(Y),` |
| 2194 | 18538-18540 | 0.43 | inline_safe | bracket | `EX=0,\qquad E(XY)=E(X^3)=0,` |
| 2195 | 18542-18544 | 0.25 | inline_safe | bracket | `E(XY)=E(X)E(Y)=0.` |
| 2196 | 18559-18561 | 0.16 | inline_safe | bracket | `\operatorname{Cov}(X,Y)=0.` |
| 2197 | 18563-18569 | 0.28 | inline_unsafe_marker | bracket | `\begin{aligned} D(X+2Y) &=DX+4DY+4\operatorname{Cov}(X,Y)\\ &=DX+4DY. \end{aligned}` |
| 2200 | 18587-18589 | 0.49 | inline_safe | bracket | `EA=2-1-1=0,\qquad EB=1-1=0.` |
| 2203 | 18608-18610 | 0.33 | inline_safe | bracket | `Y=\frac1n\sum_{i=1}^n X_i.` |
| 2204 | 18621-18626 | 0.42 | normalized_width_not_low | bracket | `\operatorname{Cov}(X_1,Y) =\operatorname{Cov}\!\left(X_1,\frac1n\sum_{i=1}^nX_i\right) =\frac1n\operatorname{Cov}(X_1,X_1) =\frac{\sigma^2}{n}.` |
| 2205 | 18630-18632 | 0.13 | inline_safe | bracket | `DY=\frac{\sigma^2}{n}.` |
| 2206 | 18634-18638 | 0.44 | normalized_width_not_low | bracket | `D(X_1+Y)=DX_1+DY+2\operatorname{Cov}(X_1,Y) =\sigma^2+\frac{\sigma^2}{n}+\frac{2\sigma^2}{n} =\frac{(n+3)\sigma^2}{n},` |
| 2207 | 18639-18643 | 0.44 | normalized_width_not_low | bracket | `D(X_1-Y)=DX_1+DY-2\operatorname{Cov}(X_1,Y) =\sigma^2+\frac{\sigma^2}{n}-\frac{2\sigma^2}{n} =\frac{(n-1)\sigma^2}{n}.` |
| 2208 | 18649-18651 | 0.13 | inline_safe | bracket | `Z=3X-2.` |
| 2209 | 18656-18658 | 0.08 | inline_safe | bracket | `EX=2.` |
| 2210 | 18660-18662 | 0.49 | inline_safe | bracket | `E(Z)=E(3X-2)=3EX-2=3\times2-2=4.` |
| 2211 | 18667-18669 | 0.28 | inline_safe | bracket | `(X,Y)\sim N(0,1;\,0,4;\,\rho),` |
| 2212 | 18674-18676 | 0.33 | inline_safe | bracket | `\operatorname{Cov}(X,Y)=\rho\sqrt{DX}\sqrt{DY}=2\rho.` |
| 2213 | 18678-18685 | 0.28 | inline_unsafe_marker | bracket | `\begin{aligned} D(2X-Y) &=4DX+DY-4\operatorname{Cov}(X,Y)\\ &=4+4-4\cdot2\rho\\ &=8-8\rho. \end{aligned}` |
| 2214 | 18687-18689 | 0.13 | inline_safe | bracket | `8-8\rho=1,` |
| 2215 | 18691-18693 | 0.14 | inline_safe | bracket | `\rho=\frac78.` |
| 2216 | 18701-18703 | 0.18 | inline_safe | bracket | `X+Y\sim B(7,p).` |
| 2217 | 18706-18708 | 0.33 | inline_safe | bracket | `X+Y\sim B(3+4,p)=B(7,p).` |
| 2218 | 18713-18715 | 0.26 | inline_safe | bracket | `x^2+2Xx+5X-4=0` |
| 2219 | 18722-18724 | 0.32 | inline_safe | bracket | `\Delta=(2X)^2-4(5X-4)\ge0.` |
| 2220 | 18726-18730 | 0.23 | normalized_width_not_low | bracket | `4(X^2-5X+4)\ge0 \quad\Longleftrightarrow\quad (X-1)(X-4)\ge0.` |
| 2221 | 18732-18734 | 0.27 | inline_safe | bracket | `X\le1\quad\text{或}\quad X\ge4.` |
| 2222 | 18736-18740 | 0.35 | normalized_width_not_low | bracket | `P\{\text{方程有实根}\} =P(0<X\le1)+P(4\le X<5) =\frac15+\frac15=\frac25.` |
| 2223 | 18756-18758 | 0.22 | inline_safe | bracket | `P(\|\xi\|>t)\le \frac{c}{t^3}.` |
| 2224 | 18762-18764 | 0.14 | inline_safe | bracket | `\|\xi\|^3>t^3.` |
| 2225 | 18766-18768 | 0.28 | inline_safe | bracket | `\mathbf 1_{\{\|\xi\|>t\}}\le \frac{\|\xi\|^3}{t^3}.` |
| 2226 | 18770-18775 | 0.30 | normalized_width_not_low | bracket | `P(\|\xi\|>t)=E\mathbf 1_{\{\|\xi\|>t\}} \le E\left(\frac{\|\xi\|^3}{t^3}\right) =\frac{E\|\xi\|^3}{t^3} =\frac{c}{t^3}.` |
| 2227 | 18786-18788 | 0.47 | inline_safe | bracket | `p=\frac12\cdot0.4+\frac12\cdot0.6=0.5,` |
| 2228 | 18790-18792 | 0.35 | inline_safe | bracket | `P(N=k)=p^kq=(0.5)^{k+1}.` |
| 2229 | 18794-18797 | 0.36 | inline_safe | bracket | `EN=\sum_{k=0}^{\infty}k(0.5)^{k+1} =\frac{p}{q}=1.` |
| 2231 | 18804-18807 | 0.38 | normalized_width_not_low | bracket | `ES=\sum_{k=1}^{\infty}350(0.5)^{k-1} =350\cdot\frac1{1-0.5}=700.` |
| 2232 | 18819-18822 | 0.32 | normalized_width_not_low | bracket | `P(A_1)=0.3,\qquad P(A_2)=0.7\times0.3=0.21,` |
| 2233 | 18823-18826 | 0.48 | normalized_width_not_low | bracket | `P(A_3)=0.7^2\times0.3=0.147,\qquad P(A_4)=0.7^3\times0.3=0.1029,` |
| 2234 | 18827-18829 | 0.30 | inline_safe | bracket | `P(A_0)=0.7^4=0.2401.` |
| 2235 | 18832-18834 | 0.39 | inline_safe | bracket | `100-10k,\qquad k=1,2,3,4.` |
| 2236 | 18836-18838 | 0.24 | inline_safe | bracket | `-40-100=-140.` |
| 2238 | 18857-18859 | 0.23 | inline_safe | bracket | `D(X+Y)=D(X-Y),` |
| 2239 | 18870-18872 | 0.37 | inline_safe | bracket | `D(X+Y)=DX+DY+2\operatorname{Cov}(X,Y),` |
| 2240 | 18873-18875 | 0.37 | inline_safe | bracket | `D(X-Y)=DX+DY-2\operatorname{Cov}(X,Y).` |
| 2241 | 18877-18880 | 0.27 | normalized_width_not_low | bracket | `DX+DY+2\operatorname{Cov}(X,Y) =DX+DY-2\operatorname{Cov}(X,Y),` |
| 2242 | 18882-18884 | 0.17 | inline_safe | bracket | `4\operatorname{Cov}(X,Y)=0.` |
| 2243 | 18886-18888 | 0.16 | inline_safe | bracket | `\operatorname{Cov}(X,Y)=0,` |
| 2245 | 18898-18900 | 0.21 | inline_safe | bracket | `P\{X+Y\ge 6\}\le c?` |
| 2246 | 18904-18906 | 0.42 | inline_safe | bracket | `E(X+Y)=E(X)+E(Y)=-2+2=0.` |
| 2247 | 18908-18911 | 0.36 | normalized_width_not_low | bracket | `\operatorname{Cov}(X,Y)=\rho_{X,Y}\sqrt{D(X)}\sqrt{D(Y)} =-0.5\times 1\times 2=-1.` |
| 2248 | 18913-18916 | 0.40 | normalized_width_not_low | bracket | `D(X+Y)=D(X)+D(Y)+2\operatorname{Cov}(X,Y) =1+4+2(-1)=3.` |
| 2249 | 18919-18921 | 0.32 | inline_safe | bracket | `\{X+Y\ge 6\}\subset \{\|X+Y\|\ge 6\},` |
| 2250 | 18923-18928 | 0.36 | normalized_width_not_low | bracket | `P\{X+Y\ge 6\}\le P\{\|X+Y\|\ge 6\} \le \frac{D(X+Y)}{6^2} =\frac{3}{36} =\frac1{12}.` |
| 2251 | 18930-18932 | 0.15 | inline_safe | bracket | `c=\frac1{12}.` |
| 2252 | 18940-18946 | 0.13 | inline_unsafe_marker | bracket | `f(x)= \begin{cases} a\sin x, & 0\le x\le \pi,\\ 0, & \text{其他}. \end{cases}` |
| 2253 | 18954-18958 | 0.24 | normalized_width_not_low | bracket | `1=\int_0^\pi a\sin x\,\mathrm{d}x =a[-\cos x]_0^\pi =2a,` |
| 2254 | 18960-18962 | 0.14 | inline_safe | bracket | `a=\frac12.` |
| 2255 | 18965-18969 | 0.40 | normalized_width_not_low | bracket | `E(X)=\int_0^\pi x\cdot\frac12\sin x\,\mathrm{d}x =\frac12[-x\cos x+\sin x]_0^\pi =\frac{\pi}{2}.` |
| 2256 | 18971-18978 | 0.49 | inline_unsafe_marker | bracket | `\begin{aligned} E(X^2) &=\int_0^\pi x^2\cdot\frac12\sin x\,\mathrm{d}x\\ &=\frac12[-x^2\cos x+2x\sin x+2\cos x]_0^\pi\\ &=\frac{\pi^2-4}{2}. \end{aligned}` |
| 2257 | 18980-18984 | 0.29 | normalized_width_not_low | bracket | `D(X)=E(X^2)-[E(X)]^2 =\frac{\pi^2-4}{2}-\frac{\pi^2}{4} =\frac{\pi^2}{4}-2.` |
| 2258 | 18987-18989 | 0.22 | inline_safe | bracket | `P(A\|B)=\frac{P(A\cap B)}{P(B)}.` |
| 2259 | 18991-18995 | 0.45 | normalized_width_not_low | bracket | `P(A\cap B)=\int_{\pi/4}^{2\pi/3}\frac12\sin x\,\mathrm{d}x =\frac12\left(\cos\frac{\pi}{4}-\cos\frac{2\pi}{3}\right) =\frac{\sqrt2+1}{4},` |
| 2260 | 18996-19000 | 0.38 | normalized_width_not_low | bracket | `P(B)=\int_{\pi/4}^{\pi}\frac12\sin x\,\mathrm{d}x =\frac12\left(\cos\frac{\pi}{4}-\cos\pi\right) =\frac{2+\sqrt2}{4}.` |
| 2261 | 19002-19004 | 0.22 | inline_safe | bracket | `P(A\|B)=\frac{\sqrt2+1}{\sqrt2+2}.` |
| 2262 | 19011-19013 | 0.16 | inline_safe | bracket | `P(\|X\|>k)=0.` |
| 2263 | 19020-19022 | 0.26 | inline_safe | bracket | `\|E X\|\le E\|X\|\le k<+\infty.` |
| 2264 | 19028-19030 | 0.33 | inline_safe | bracket | `D(X)=4,\qquad D(Y)=1,` |
| 2265 | 19032-19034 | 0.13 | inline_safe | bracket | `D(3X-2Y).` |
| 2266 | 19045-19048 | 0.35 | normalized_width_not_low | bracket | `\operatorname{Cov}(X,Y)=\rho_{XY}\sqrt{D(X)}\sqrt{D(Y)} =0.6\times2\times1=1.2.` |
| 2267 | 19050-19058 | 0.49 | inline_unsafe_marker | bracket | `\begin{aligned} D(3X-2Y) &=9D(X)+4D(Y)+2\cdot3\cdot(-2)\operatorname{Cov}(X,Y)\\ &=9\times4+4\times1-12\times1.2\\ &=36+4-14.4\\ &=25.6. \end{aligned}` |
| 2268 | 19070-19072 | 0.18 | inline_safe | bracket | `X+Y\sim N(0,2).` |
| 2269 | 19074-19076 | 0.11 | inline_safe | bracket | `X+Y=0,` |
| 2271 | 19086-19088 | 0.22 | inline_safe | bracket | `Z=(2X-Y+1)^2.` |
| 2272 | 19093-19095 | 0.17 | inline_safe | bracket | `W=2X-Y+1.` |
| 2274 | 19101-19104 | 0.35 | normalized_width_not_low | bracket | `\operatorname{Cov}(X,Y)=\rho_{XY}\sqrt{D(X)}\sqrt{D(Y)} =0.6\times1\times2=1.2.` |
| 2275 | 19106-19110 | 0.32 | normalized_width_not_low | bracket | `D(W)=D(2X-Y+1) =4D(X)+D(Y)-4\operatorname{Cov}(X,Y) =4+4-4.8=3.2.` |
| 2279 | 19180-19196 | 0.41 | inline_unsafe_marker | bracket | `\begin{cases} \text{马尔可夫不等式：} \displaystyle P\{X \geqslant a\} \leqslant \frac{EX}{a}\ (X\ge 0) \\[6pt] \text{切比雪夫不等式：} \displaystyle P\left\{\|X - EX\| \geqslant \varepsilon\righ...` |
| 2280 | 19247-19251 | 0.37 | normalized_width_not_low | bracket | `\lim_{n\to\infty} P\{\|X_n - X\| \geqslant \varepsilon\} = 0 \quad \text{或等价地} \quad \lim_{n\to\infty} P\{\|X_n - X\| < \varepsilon\} = 1,` |
| 2281 | 19253-19255 | 0.22 | inline_safe | bracket | `X_n \stackrel{P}{\longrightarrow} X\ (n\to\infty).` |
| 2282 | 19261-19263 | 0.27 | inline_safe | bracket | `g(X_n, Y_n) \stackrel{P}{\longrightarrow} g(a, b).` |
| 2284 | 19297-19299 | 0.20 | inline_safe | bracket | `P\{X\ge a\}\le \frac{EX}{a}.` |
| 2285 | 19303-19308 | 0.28 | display_environment | env:align* | `EX &= \int_0^{+\infty}x\,f(x)\,\mathrm{d}x \\ &\ge \int_a^{+\infty}x\,f(x)\,\mathrm{d}x \\ &\ge a\int_a^{+\infty}f(x)\,\mathrm{d}x \\ &= a\,P\{X\ge a\}.` |
| 2286 | 19310-19312 | 0.20 | inline_safe | bracket | `P\{X\ge a\}\le \frac{EX}{a}.` |
| 2287 | 19319-19321 | 0.24 | inline_safe | bracket | `\{(X-EX)^2\ge \varepsilon^2\},` |
| 2289 | 19331-19333 | 0.23 | inline_safe | bracket | `P(X\ge 12)\le \underline{\hspace{2cm}}.` |
| 2290 | 19337-19339 | 0.33 | inline_safe | bracket | `P(X\ge 12)\le \frac{3}{12}=\frac14.` |
| 2291 | 19357-19359 | 0.30 | inline_safe | bracket | `P\{\|X - EX\| \geqslant \varepsilon\} \leqslant \frac{DX}{\varepsilon^2},` |
| 2292 | 19361-19363 | 0.33 | inline_safe | bracket | `P\{\|X - EX\| < \varepsilon\} \geqslant 1 - \frac{DX}{\varepsilon^2}.` |
| 2294 | 19387-19389 | 0.35 | inline_safe | bracket | `P(\|X-EX\|<\varepsilon)\ge 1-\frac{0.009}{\varepsilon^2}.` |
| 2296 | 19406-19408 | 0.25 | inline_safe | bracket | `S=\sum_{i=1}^9X_i.` |
| 2297 | 19410-19413 | 0.43 | normalized_width_not_low | bracket | `ES=\sum_{i=1}^9EX_i=9,\qquad DS=\sum_{i=1}^9DX_i=9.` |
| 2298 | 19415-19417 | 0.33 | inline_safe | bracket | `P\{\|S-ES\|<\varepsilon\}\ge1-\frac{DS}{\varepsilon^2},` |
| 2299 | 19419-19422 | 0.34 | normalized_width_not_low | bracket | `P\left\{\left\|\sum_{i=1}^9X_i-9\right\|<\varepsilon\right\} \ge1-\frac9{\varepsilon^2}.` |
| 2300 | 19431-19433 | 0.30 | inline_safe | bracket | `P\{\|X - EX\| \geq \varepsilon\} \leq \frac{DX}{\varepsilon^2},` |
| 2301 | 19435-19437 | 0.33 | inline_safe | bracket | `P\{\|X - EX\| < \varepsilon\} \geq 1 - \frac{DX}{\varepsilon^2}.` |
| 2302 | 19447-19449 | 0.17 | inline_safe | bracket | `P(\|X-EX\|<\varepsilon)` |
| 2304 | 19458-19460 | 0.32 | inline_safe | bracket | `P(\|X-EX\|<\varepsilon)\ge 1-\frac{DX}{\varepsilon^2},` |
| 2306 | 19477-19479 | 0.29 | inline_safe | bracket | `P(\|X-EX\|\ge \varepsilon)\le \frac{DX}{\varepsilon^2}.` |
| 2307 | 19481-19483 | 0.07 | inline_safe | bracket | `\varepsilon=2.` |
| 2308 | 19485-19487 | 0.42 | inline_safe | bracket | `P(\|X - EX\| \geq 2) \leq \frac{DX}{\varepsilon^2} = \frac{2}{4} = \frac{1}{2}.` |
| 2309 | 19497-19499 | 0.25 | inline_safe | bracket | `\rho(X,Y)=\frac{\mathrm{Cov}(X,Y)}{\sqrt{DX}\sqrt{DY}},` |
| 2310 | 19501-19504 | 0.33 | normalized_width_not_low | bracket | `\mathrm{Cov}(X,Y)=\rho(X,Y)\sqrt{DX}\sqrt{DY} =0.5\times \sqrt{1}\times \sqrt{4}=1.` |
| 2312 | 19512-19514 | 0.38 | inline_safe | bracket | `E(X+Y)=EX+EY=-2+2=0.` |
| 2313 | 19516-19518 | 0.41 | inline_safe | bracket | `P\{\|X+Y\| \geq 6\} \leq \frac{D(X+Y)}{36} = \frac{7}{36}.` |
| 2315 | 19530-19532 | 0.28 | inline_safe | bracket | `P\{X+Y\ge 6\}\le\,\underline{\hspace{2cm}}.` |
| 2316 | 19536-19538 | 0.26 | inline_safe | bracket | `E(X+Y)=EX+EY=0.` |
| 2317 | 19540-19543 | 0.33 | normalized_width_not_low | bracket | `\mathrm{Cov}(X,Y)=\rho(X,Y)\sqrt{DX}\sqrt{DY} =-0.5\cdot1\cdot2=-1,` |
| 2319 | 19549-19551 | 0.32 | inline_safe | bracket | `\{X+Y\ge6\}\subset \{\|X+Y\|\ge6\},` |
| 2320 | 19553-19558 | 0.21 | normalized_width_not_low | bracket | `P\{X+Y\ge6\} \le P\{\|X+Y\|\ge6\} \le \frac{D(X+Y)}{6^2} =\frac{1}{12}.` |
| 2321 | 19563-19565 | 0.26 | inline_unsafe_marker | bracket | `f(x) = \begin{cases} \dfrac{1}{2}\,x^2\,e^{-x}, & x > 0, \\[4pt] 0, & x \leq 0, \end{cases}` |
| 2323 | 19574-19576 | 0.38 | inline_safe | bracket | `DX = EX^2 - (EX)^2 = 12 - 9 = 3.` |
| 2324 | 19578-19580 | 0.48 | inline_safe | bracket | `P(\|X - 3\| < 2) \geq 1 - \frac{DX}{2^2} = 1 - \frac{3}{4} = \frac{1}{4}.` |
| 2325 | 19591-19593 | 0.12 | inline_unsafe_marker | bracket | `f(x) = \begin{cases} 2x, & 0 < x < 1, \\ 0, & \text{其他}, \end{cases}` |
| 2326 | 19602-19606 | 0.42 | normalized_width_not_low | bracket | `EX = \int_0^1 2x^2\,\mathrm{d}x = \frac{2}{3},\quad EX^2 = \int_0^1 2x^3\,\mathrm{d}x = \frac{1}{2},\quad DX = \frac{1}{2} - \frac{4}{9} = \frac{1}{18}.` |
| 2328 | 19624-19626 | 0.36 | inline_safe | bracket | `\overline{X}_n=\frac1n\sum_{i=1}^n X_i` |
| 2329 | 19630-19632 | 0.43 | inline_safe | bracket | `D\overline{X}_n=\frac1{n^2}\sum_{i=1}^n DX_i.` |
| 2330 | 19638-19640 | 0.31 | inline_safe | bracket | `DX_i \leq C \quad (\text{对一切 } i \geq 1),` |
| 2334 | 19661-19663 | 0.29 | inline_safe | bracket | `\frac1n\sum_{i=1}^n EX_i` |
| 2335 | 19665-19667 | 0.30 | inline_safe | bracket | `\frac{1}{n}\sum_{i=1}^{n} X_i \stackrel{P}{\longrightarrow} \mu.` |
| 2336 | 19699-19701 | 0.38 | inline_safe | bracket | `\lim_{n\to\infty} P\!\left\{\left\|\frac{\mu_n}{n} - p\right\| < \varepsilon\right\} = 1,` |
| 2337 | 19707-19709 | 0.29 | inline_safe | bracket | `\frac1n\sum_{i=1}^n p_i,` |
| 2338 | 19716-19718 | 0.20 | inline_safe | bracket | `\overline{X}_n = \frac{\mu_n}{n} \xrightarrow{P} p.` |
| 2339 | 19725-19727 | 0.43 | inline_safe | bracket | `\frac{\mu_n}{n}=\frac{1}{n}\sum_{i=1}^{n}X_i=\bar X_n,` |
| 2340 | 19731-19733 | 0.28 | inline_safe | bracket | `F_n(x) = \frac{\text{样本值中} \leq x \text{的个数}}{n}` |
| 2341 | 19744-19752 | 0.11 | inline_unsafe_marker | bracket | `F_7(x) = \begin{cases} 0, & x < 1, \\ \dfrac{3}{7}, & 1 \leq x < 2, \\[6pt] \dfrac{5}{7}, & 2 \leq x < 3, \\[6pt] \dfrac{6}{7}, & 3 \leq x < 5, \\[6pt] 1, & x \geq 5. \end{cases}` |
| 2342 | 19761-19763 | 0.30 | inline_safe | bracket | `\frac1n\sum_{i=1}^n EX_i;` |
| 2346 | 19789-19792 | 0.38 | normalized_width_not_low | bracket | `P\!\left\{\left\|\frac{1}{n}\sum_{k=1}^{n} X_k - \mu\right\| \geq \varepsilon\right\} \leq \frac{\sigma^2/n}{\varepsilon^2} \xrightarrow{n\to\infty} 0.` |
| 2347 | 19801-19803 | 0.22 | inline_safe | bracket | `\frac1n\sum h(X_i)` |
| 2348 | 19807-19809 | 0.42 | inline_safe | bracket | `\frac{1}{n}\sum_{i=1}^{n} X_i^k \stackrel{P}{\longrightarrow} E(X_1^k).` |
| 2349 | 19818-19820 | 0.17 | inline_unsafe_marker | bracket | `f(x) = \begin{cases} 1 - \|x\|, & \|x\| < 1, \\ 0, & \text{其他}, \end{cases}` |
| 2350 | 19829-19831 | 0.42 | inline_safe | bracket | `\frac{1}{n}\sum_{i=1}^{n} X_i^2 \stackrel{P}{\longrightarrow} E(X_1^2).` |
| 2352 | 19849-19851 | 0.18 | inline_safe | bracket | `X_1, X_2, \dots, X_n` |
| 2353 | 19855-19857 | 0.38 | inline_safe | bracket | `\overline{X}_n=\frac1n\sum_{i=1}^n X_i,` |
| 2355 | 19863-19865 | 0.41 | inline_safe | bracket | `EX_i = \frac{1 + 2 + 3 + 4 + 5 + 6}{6} = \frac{7}{2}.` |
| 2356 | 19868-19870 | 0.49 | inline_safe | bracket | `\overline{X}_n = \frac{1}{n}\sum_{i=1}^{n} X_i \stackrel{P}{\longrightarrow} EX_i = \frac{7}{2}.` |
| 2357 | 19885-19887 | 0.17 | inline_safe | bracket | `\overline{X}_n-\mu \stackrel{P}{\longrightarrow} 0,` |
| 2360 | 19913-19916 | 0.31 | inline_safe | bracket | `\frac{\overline{X}_n-\mu}{\sigma/\sqrt{n}} =\frac{\sum_{i=1}^n X_i-n\mu}{\sqrt{n}\,\sigma}.` |
| 2361 | 19968-19970 | 0.24 | inline_safe | bracket | `\text{独立}+\text{同分布}+\text{期望、方差存在}.` |
| 2362 | 19985-19987 | 0.20 | inline_safe | bracket | `P\{80\le X\le 100\}` |
| 2363 | 19992-19994 | 0.39 | inline_safe | bracket | `EX=np,\qquad DX=np(1-p).` |
| 2364 | 19996-19998 | 0.31 | inline_safe | bracket | `n=100,\qquad p=0.8,` |
| 2366 | 20005-20007 | 0.22 | inline_safe | bracket | `\frac{X-80}{4}\approx N(0,1).` |
| 2367 | 20009-20015 | 0.31 | normalized_width_not_low | bracket | `P(80\le X\le 100) \approx \Phi\!\left(\frac{100.5-80}{4}\right) -\Phi\!\left(\frac{79.5-80}{4}\right) =\Phi(5.125)-\Phi(-0.125).` |
| 2369 | 20022-20026 | 0.29 | normalized_width_not_low | bracket | `\Phi\!\left(\frac{100-80}{4}\right) -\Phi\!\left(\frac{80-80}{4}\right) =\Phi(5)-\Phi(0)=\frac12,` |
| 2370 | 20032-20034 | 0.43 | inline_safe | bracket | `P\!\left(\sum_{i=1}^{100} X_i < 240\right) =\,\underline{\hspace{2cm}}.` |
| 2371 | 20041-20043 | 0.45 | inline_safe | bracket | `\mu=EX_i=2,\qquad \sigma^2=DX_i=4.` |
| 2372 | 20046-20048 | 0.28 | inline_safe | bracket | `S=\sum_{i=1}^{100} X_i.` |
| 2374 | 20055-20057 | 0.23 | inline_safe | bracket | `\frac{S-200}{20}\approx N(0,1),` |
| 2376 | 20071-20073 | 0.39 | inline_safe | bracket | `p=0.0005\times0.01=5\times10^{-6}.` |
| 2377 | 20075-20077 | 0.37 | inline_safe | bracket | `Y\sim B(2\times10^5,\ 5\times10^{-6}).` |
| 2379 | 20083-20085 | 0.32 | inline_safe | bracket | `Y\approx N(1,\ 1-5\times10^{-6}).` |
| 2380 | 20087-20092 | 0.30 | normalized_width_not_low | bracket | `P(Y>3)\approx 1-\Phi\!\left(\frac{3-1}{\sqrt{1-5\times10^{-6}}}\right) \approx 1-\Phi(2) =0.0228.` |
| 2381 | 20097-20099 | 0.29 | inline_unsafe_marker | bracket | `f(x) = \begin{cases} \dfrac{1}{100}\,e^{-x/100}, & x > 0, \\[4pt] 0, & x \leq 0, \end{cases}` |
| 2386 | 20153-20155 | 0.28 | inline_safe | bracket | `S_n=\sum_{i=1}^{n} X_i.` |
| 2387 | 20157-20159 | 0.41 | inline_safe | bracket | `ES_n=\frac{n}{\lambda},\qquad DS_n=\frac{n}{\lambda^2}.` |
| 2388 | 20162-20165 | 0.31 | normalized_width_not_low | bracket | `\frac{S_n - ES_n}{\sqrt{DS_n}} = \frac{S_n - n/\lambda}{\sqrt{n}/\lambda} = \frac{\lambda S_n - n}{\sqrt{n}} \to N(0,1),` |
| 2390 | 20186-20188 | 0.34 | inline_safe | bracket | `\frac{\sum X_i - n \cdot 2}{\sqrt{n \cdot 2}} \to N(0,1).` |
| 2391 | 20190-20194 | 0.32 | normalized_width_not_low | bracket | `P\!\left(\frac{\sum X_i - 2n}{\sqrt{n}} < 2\right) = P\!\left(\frac{\sum X_i - 2n}{\sqrt{2n}} < \frac{2}{\sqrt{2}}\right) = P(Z < \sqrt{2}) = \Phi(\sqrt{2}).` |
| 2392 | 20201-20203 | 0.33 | inline_safe | bracket | `Z_n = \frac{1}{n}\sum_{i=1}^{n} X_i^2` |
| 2394 | 20212-20214 | 0.46 | inline_safe | bracket | `\frac{\sum_{i=1}^{n} X_i^2 - n\alpha_2}{\sqrt{n(\alpha_4 - \alpha_2^2)}} \to N(0,1),` |
| 2395 | 20216-20218 | 0.38 | inline_safe | bracket | `\frac{Z_n - \alpha_2}{\sqrt{(\alpha_4 - \alpha_2^2)/n}} \to N(0,1),` |
| 2396 | 20220-20222 | 0.40 | inline_safe | bracket | `\mu = \alpha_2,\quad \sigma^2 = \frac{\alpha_4 - \alpha_2^2}{n}.` |
| 2397 | 20238-20240 | 0.46 | inline_safe | bracket | `\lim_{n\to\infty} P\!\left\{\frac{Y_n - np}{\sqrt{np(1-p)}} \leq x\right\} = \Phi(x).` |
| 2399 | 20265-20267 | 0.28 | inline_safe | bracket | `P\{a-0.5 < X < b+0.5\},` |
| 2400 | 20276-20278 | 0.22 | inline_safe | bracket | `X\sim B(1000,0.03).` |
| 2404 | 20320-20322 | 0.21 | inline_safe | bracket | `X\sim B(1000,0.8).` |
| 2405 | 20324-20327 | 0.49 | normalized_width_not_low | bracket | `EX=np=1000\times0.8=800,\qquad DX=np(1-p)=1000\times0.8\times0.2=160.` |
| 2406 | 20329-20331 | 0.20 | inline_safe | bracket | `P(X\le M)\ge0.99.` |
| 2407 | 20333-20336 | 0.16 | inline_safe | bracket | `P(X\le M)\approx \Phi\left(\frac{M-800}{\sqrt{160}}\right).` |
| 2408 | 20338-20340 | 0.21 | inline_safe | bracket | `\frac{M-800}{\sqrt{160}}\ge2.33.` |
| 2409 | 20342-20344 | 0.38 | inline_safe | bracket | `M\ge800+2.33\sqrt{160}\approx829.47.` |
| 2410 | 20346-20348 | 0.09 | inline_safe | bracket | `M=830` |
| 2411 | 20357-20359 | 0.35 | inline_safe | bracket | `P\!\left(0.76 \leq \frac{X}{n} \leq 0.84\right) \geq 0.90.` |
| 2413 | 20377-20379 | 0.45 | inline_safe | bracket | `X\sim B(n,0.8),\qquad \hat p=\frac Xn.` |
| 2415 | 20385-20388 | 0.39 | normalized_width_not_low | bracket | `P(0.76\le \hat p\le0.84) =P(\|\hat p-0.8\|\le0.04)\ge0.90.` |
| 2416 | 20391-20396 | 0.25 | normalized_width_not_low | bracket | `P(\|\hat p-0.8\|<0.04) \ge1-\frac{D\hat p}{0.04^2} =1-\frac{0.16/n}{0.0016} =1-\frac{100}{n}.` |
| 2417 | 20398-20400 | 0.21 | inline_safe | bracket | `1-\frac{100}{n}\ge0.90,` |
| 2418 | 20402-20404 | 0.12 | inline_safe | bracket | `n\ge1000.` |
| 2419 | 20408-20410 | 0.26 | inline_safe | bracket | `\frac{\hat p-0.8}{\sqrt{0.16/n}}\approx N(0,1).` |
| 2420 | 20412-20417 | 0.26 | normalized_width_not_low | bracket | `P(\|\hat p-0.8\|\le0.04) \approx P\left(\|Z\|\le\frac{0.04}{\sqrt{0.16/n}}\right) =P(\|Z\|\le0.1\sqrt n).` |
| 2421 | 20419-20421 | 0.28 | inline_safe | bracket | `2\Phi(0.1\sqrt n)-1\ge0.90,` |
| 2422 | 20423-20425 | 0.22 | inline_safe | bracket | `\Phi(0.1\sqrt n)\ge0.95.` |
| 2423 | 20427-20429 | 0.20 | inline_safe | bracket | `0.1\sqrt n\ge1.645,` |
| 2424 | 20431-20433 | 0.32 | inline_safe | bracket | `n\ge(16.45)^2=270.6025.` |
| 2425 | 20435-20437 | 0.09 | inline_safe | bracket | `n=271` |
| 2426 | 20454-20456 | 0.23 | inline_safe | bracket | `X_n\sim B\!\left(n,\frac12\right).` |
| 2429 | 20468-20470 | 0.43 | inline_safe | bracket | `\lim_{n\to\infty} P\!\left\{\frac{2X_n-n}{\sqrt n}\le x\right\}=\Phi(x),` |
| 2430 | 20482-20484 | 0.18 | inline_safe | bracket | `\zeta\sim B(n,0.95).` |
| 2431 | 20486-20488 | 0.25 | inline_safe | bracket | `P(\zeta\ge 2000)\ge 0.95.` |
| 2433 | 20495-20499 | 0.26 | inline_safe | bracket | `P(\zeta\ge 2000) \approx 1-\Phi\!\left(\frac{2000-0.95n}{\sqrt{0.0475n}}\right).` |
| 2434 | 20501-20503 | 0.34 | inline_safe | bracket | `1-\Phi\!\left(\frac{2000-0.95n}{\sqrt{0.0475n}}\right)=0.95.` |
| 2435 | 20505-20507 | 0.30 | inline_safe | bracket | `\frac{2000-0.95n}{\sqrt{0.0475n}}=-1.65.` |
| 2436 | 20509-20511 | 0.11 | inline_safe | bracket | `n=2123.` |
| 2437 | 20525-20527 | 0.25 | inline_safe | bracket | `X\sim B(25000,0.001).` |
| 2439 | 20533-20535 | 0.38 | inline_safe | bracket | `25000\times240=6000000\quad(\text{元}),` |
| 2440 | 20537-20539 | 0.28 | inline_safe | bracket | `L=6000000-200000X.` |
| 2441 | 20542-20544 | 0.47 | inline_safe | bracket | `6000000-200000X<0 \quad\Longleftrightarrow\quad X>30.` |
| 2442 | 20546-20551 | 0.22 | normalized_width_not_low | bracket | `P(L<0)=P(X>30) \approx 1-\Phi\left(\frac{30-25}{5}\right) =1-\Phi(1) =0.1587.` |
| 2443 | 20554-20558 | 0.36 | normalized_width_not_low | bracket | `6000000-200000X\ge1000000 \quad\Longleftrightarrow\quad X\le25.` |
| 2444 | 20560-20564 | 0.33 | normalized_width_not_low | bracket | `P(L\ge1000000)=P(X\le25) \approx \Phi\left(\frac{25-25}{5}\right) =\Phi(0)=0.5.` |
| 2445 | 20573-20575 | 0.21 | inline_safe | bracket | `X\sim B(n,0.0006).` |
| 2446 | 20577-20579 | 0.21 | inline_safe | bracket | `L=50n-10000X.` |
| 2447 | 20581-20583 | 0.26 | inline_safe | bracket | `P(L\ge10000)\ge0.95.` |
| 2448 | 20585-20588 | 0.34 | normalized_width_not_low | bracket | `P\left(X\le \frac{50n-10000}{10000}\right) =P(X\le0.005n-1)\ge0.95.` |
| 2449 | 20591-20593 | 0.47 | inline_safe | bracket | `X\approx N\bigl(0.0006n,\ 0.0006(1-0.0006)n\bigr).` |
| 2450 | 20595-20599 | 0.31 | inline_safe | bracket | `\frac{0.005n-1-0.0006n} {\sqrt{0.0006(1-0.0006)n}} \ge z_{0.05}.` |
| 2451 | 20601-20603 | 0.33 | inline_safe | bracket | `\frac{0.0044n-1}{\sqrt{0.00059964\,n}}\ge1.645.` |
| 2452 | 20605-20607 | 0.11 | inline_safe | bracket | `n\gtrsim 413.3.` |
| 2453 | 20609-20611 | 0.09 | inline_safe | bracket | `n=414` |
| 2454 | 20624-20626 | 0.21 | inline_safe | bracket | `X\sim B(n,0.0003).` |
| 2455 | 20628-20630 | 0.21 | inline_safe | bracket | `L=20n-10000X.` |
| 2456 | 20632-20634 | 0.26 | inline_safe | bracket | `P(L\ge10000)\ge0.95,` |
| 2457 | 20636-20639 | 0.34 | normalized_width_not_low | bracket | `P\left(X\le \frac{20n-10000}{10000}\right) =P(X\le0.002n-1)\ge0.95.` |
| 2458 | 20642-20644 | 0.47 | inline_safe | bracket | `X\approx N\bigl(0.0003n,\ 0.0003(1-0.0003)n\bigr).` |
| 2459 | 20646-20650 | 0.31 | inline_safe | bracket | `\frac{0.002n-1-0.0003n} {\sqrt{0.0003(1-0.0003)n}} \ge z_{0.05}.` |
| 2460 | 20652-20654 | 0.33 | inline_safe | bracket | `\frac{0.0017n-1}{\sqrt{0.00029991\,n}}\ge1.645.` |
| 2461 | 20656-20658 | 0.12 | inline_safe | bracket | `n\gtrsim1158.7.` |
| 2462 | 20660-20662 | 0.10 | inline_safe | bracket | `n=1159` |
| 2463 | 20679-20681 | 0.24 | inline_safe | bracket | `X\sim B(9000,0.001).` |
| 2464 | 20683-20686 | 0.39 | normalized_width_not_low | bracket | `EX=9000\times0.001=9,\qquad DX=9000\times0.001\times0.999\approx9.` |
| 2466 | 20693-20697 | 0.21 | normalized_width_not_low | bracket | `P(X>22.5)\approx 1-\Phi\!\left(\frac{22.5-9}{3}\right) =1-\Phi(4.5)\approx0.` |
| 2468 | 20705-20709 | 0.24 | normalized_width_not_low | bracket | `P(X\le17.5)\approx \Phi\!\left(\frac{17.5-9}{3}\right) =\Phi(2.83)\approx0.995.` |
| 2469 | 20721-20723 | 0.26 | inline_safe | bracket | `S=\sum_{i=1}^{50}X_i.` |
| 2471 | 20729-20737 | 0.31 | inline_unsafe_marker | bracket | `\begin{aligned} P(400\le S\le500) &\approx P\left\{\frac{400-450}{3\sqrt{50}}\le Z\le \frac{500-450}{3\sqrt{50}}\right\}\\ &=2\Phi\left(\frac{\sqrt{50}}3\right)-1 \approx2\Phi(2...` |
| 2472 | 20740-20742 | 0.24 | inline_safe | bracket | `P\{10S\ge m\}\ge0.95.` |
| 2473 | 20744-20746 | 0.28 | inline_safe | bracket | `\Phi\left(\frac{450-m/10}{3\sqrt{50}}\right)=0.95,` |
| 2474 | 20748-20750 | 0.45 | inline_safe | bracket | `m=10\left(450-1.645\cdot3\sqrt{50}\right)\approx4151.` |
| 2475 | 20754-20756 | 0.24 | inline_safe | bracket | `P\{10S\le M\}\ge0.95.` |
| 2476 | 20758-20760 | 0.28 | inline_safe | bracket | `\Phi\left(\frac{M/10-450}{3\sqrt{50}}\right)=0.95,` |
| 2477 | 20762-20764 | 0.45 | inline_safe | bracket | `M=10\left(450+1.645\cdot3\sqrt{50}\right)\approx4849.` |
| 2478 | 20776-20778 | 0.26 | inline_safe | bracket | `S=\sum_{i=1}^{50}X_i.` |
| 2479 | 20780-20782 | 0.34 | inline_safe | bracket | `ES=450,\qquad DS=450.` |
| 2480 | 20784-20789 | 0.25 | normalized_width_not_low | bracket | `P(400\le S\le500) \approx2\Phi\left(\frac{50}{3\sqrt{50}}\right)-1 =2\Phi\left(\frac{\sqrt{50}}3\right)-1 \approx0.9818.` |
| 2481 | 20792-20794 | 0.24 | inline_safe | bracket | `P\{10S\ge m\}\ge0.90.` |
| 2482 | 20796-20798 | 0.28 | inline_safe | bracket | `\Phi\left(\frac{450-m/10}{3\sqrt{50}}\right)=0.90.` |
| 2483 | 20800-20802 | 0.43 | inline_safe | bracket | `m=10\left(450-1.28\cdot3\sqrt{50}\right)\approx4228.` |
| 2484 | 20806-20808 | 0.23 | inline_safe | bracket | `P\{10S\le M\}\ge0.90` |
| 2485 | 20810-20812 | 0.43 | inline_safe | bracket | `M=10\left(450+1.28\cdot3\sqrt{50}\right)\approx4772.` |
| 2487 | 20828-20830 | 0.34 | inline_safe | bracket | `ES=750,\qquad DS=750.` |
| 2488 | 20832-20836 | 0.30 | normalized_width_not_low | bracket | `P(700\le S\le800) \approx2\Phi\left(\frac{50}{\sqrt{750}}\right)-1 \approx2\Phi(1.83)-1\approx0.932.` |
| 2489 | 20839-20841 | 0.21 | inline_safe | bracket | `P\{9S\ge m\}\ge0.95` |
| 2490 | 20843-20845 | 0.40 | inline_safe | bracket | `m=9\left(750-1.645\sqrt{750}\right)\approx6345.` |
| 2491 | 20849-20851 | 0.40 | inline_safe | bracket | `M=9\left(750+1.645\sqrt{750}\right)\approx7155.` |
| 2492 | 20859-20861 | 0.33 | inline_safe | bracket | `S_{900}=\sum_{i=1}^{900}X_i.` |
| 2493 | 20866-20869 | 0.34 | normalized_width_not_low | bracket | `EX_i=\frac{1+5}{2}=3,\qquad DX_i=\frac{(5-1)^2}{12}=\frac43.` |
| 2494 | 20871-20874 | 0.42 | normalized_width_not_low | bracket | `ES_{900}=900\cdot3=2700,\qquad DS_{900}=900\cdot\frac43=1200.` |
| 2495 | 20876-20878 | 0.30 | inline_safe | bracket | `\frac{S_{900}-2700}{\sqrt{1200}}\approx N(0,1).` |
| 2496 | 20880-20888 | 0.24 | inline_unsafe_marker | bracket | `\begin{aligned} P\{S_{900}>2632\} &\approx P\left\{Z>\frac{2632-2700}{\sqrt{1200}}\right\}\\ &=P\left\{Z>-\frac{68}{20\sqrt3}\right\} =P\left\{Z>-\frac{17\sqrt3}{15}\right\}. \e...` |
| 2497 | 20890-20892 | 0.44 | inline_safe | bracket | `P\{S_{900}>2632\}\approx \Phi(1.96)\approx0.975.` |
| 2498 | 20900-20907 | 0.29 | inline_unsafe_marker | bracket | `X_i= \begin{cases} 1, & \text{第 }i\text{ 个患者用药有效},\\ 0, & \text{否则}, \end{cases} \qquad i=1,2,\dots,100,` |
| 2499 | 20909-20911 | 0.33 | inline_safe | bracket | `S_{100}=\sum_{i=1}^{100}X_i.` |
| 2500 | 20913-20916 | 0.42 | normalized_width_not_low | bracket | `ES_{100}=100\times0.8=80,\qquad DS_{100}=100\times0.8\times0.2=16.` |
| 2501 | 20918-20920 | 0.27 | inline_safe | bracket | `\frac{S_{100}-80}{4}\approx N(0,1).` |
| 2502 | 20922-20928 | 0.37 | inline_unsafe_marker | bracket | `\begin{aligned} P\{S_{100}\ge76\} &\approx P\left\{Z\ge\frac{76-80}{4}\right\}\\ &=P\{Z\ge -1\}=\Phi(1)=0.8413. \end{aligned}` |
| 2504 | 20941-20943 | 0.29 | inline_safe | bracket | `S=\sum_{k=1}^{1000}X_k.` |
| 2505 | 20945-20948 | 0.40 | normalized_width_not_low | bracket | `ES=1000\cdot10=10000,\qquad DS=1000\cdot\frac{100}{3}=\frac{100000}{3}.` |
| 2506 | 20950-20952 | 0.29 | inline_safe | bracket | `\frac{S-10000}{\sqrt{100000/3}}\approx N(0,1).` |
| 2507 | 20954-20957 | 0.29 | inline_safe | bracket | `P\{S\le L\}\approx \Phi\!\left(\frac{L-10000}{\sqrt{100000/3}}\right)=0.99.` |
| 2508 | 20959-20961 | 0.27 | inline_safe | bracket | `\frac{L-10000}{\sqrt{100000/3}}\approx2.33.` |
| 2509 | 20963-20965 | 0.46 | inline_safe | bracket | `L\approx10000+2.33\sqrt{\frac{100000}{3}}\approx10425.` |
| 2510 | 20971-20973 | 0.29 | inline_safe | bracket | `P\{\|\overline X-\mu\|<1\}\ge0.95,` |
| 2511 | 20978-20982 | 0.14 | inline_safe | bracket | `\frac{\overline X-\mu}{\sigma/\sqrt n} =\frac{\overline X-\mu}{20/\sqrt n} \approx N(0,1).` |
| 2512 | 20984-20988 | 0.19 | inline_safe | bracket | `P\{\|\overline X-\mu\|<1\} \approx 2\Phi\!\left(\frac{\sqrt n}{20}\right)-1.` |
| 2513 | 20990-20992 | 0.29 | inline_safe | bracket | `\frac{\sqrt n}{20}\ge z_{0.025}=1.96.` |
| 2514 | 20994-20996 | 0.36 | inline_safe | bracket | `n\ge (20\times1.96)^2=1536.64.` |
| 2515 | 20998-21000 | 0.11 | inline_safe | bracket | `n=1537.` |
| 2516 | 21008-21010 | 0.36 | inline_safe | bracket | `P(B_k)=0.84\times0.90=0.756.` |
| 2517 | 21012-21019 | 0.32 | inline_unsafe_marker | bracket | `X_k= \begin{cases} 1, & B_k\text{ 发生},\\ 0, & B_k\text{ 不发生}, \end{cases} \qquad k=1,2,\dots,10000,` |
| 2518 | 21021-21023 | 0.30 | inline_safe | bracket | `X=\sum_{k=1}^{10000}X_k.` |
| 2519 | 21025-21027 | 0.25 | inline_safe | bracket | `X\sim B(10000,0.756),` |
| 2521 | 21033-21035 | 0.27 | inline_safe | bracket | `\frac{X-7560}{\sqrt{1844.64}}\approx N(0,1).` |
| 2522 | 21037-21046 | 0.26 | inline_unsafe_marker | bracket | `\begin{aligned} P\{X\ge7500\} &\approx P\left\{Z\ge\frac{7500-7560}{\sqrt{1844.64}}\right\}\\ &=1-\Phi(-1.40) =\Phi(1.40) =0.92. \end{aligned}` |
| 2523 | 21057-21059 | 0.20 | inline_safe | bracket | `P(X>96)=0.023` |
| 2524 | 21061-21063 | 0.39 | inline_safe | bracket | `\frac{96-72}{\sigma}\approx2,\qquad \frac{12}{\sigma}\approx1.` |
| 2525 | 21065-21069 | 0.47 | normalized_width_not_low | bracket | `p=P(60<X\le84) =\Phi\!\left(\frac{12}{\sigma}\right)-\Phi\!\left(-\frac{12}{\sigma}\right) \approx2\Phi(1)-1=2\times0.8413-1=0.6826.` |
| 2526 | 21071-21073 | 0.24 | inline_safe | bracket | `Y\sim B(100,0.6826),` |
| 2528 | 21080-21083 | 0.48 | normalized_width_not_low | bracket | `EY=100\times0.6826=68.26,\qquad DY=100\times0.6826\times0.3174\approx21.6657.` |
| 2532 | 21102-21104 | 0.35 | inline_safe | bracket | `DX_i=21.35-4.6^2=0.19.` |
| 2533 | 21106-21108 | 0.28 | inline_safe | bracket | `S=\sum_{i=1}^{200}X_i.` |
| 2535 | 21114-21116 | 0.23 | inline_safe | bracket | `\frac{S-920}{\sqrt{38}}\approx N(0,1).` |
| 2536 | 21118-21126 | 0.34 | inline_unsafe_marker | bracket | `\begin{aligned} P(910\le S\le930) &\approx P\left(-\frac{10}{\sqrt{38}}\le Z\le \frac{10}{\sqrt{38}}\right)\\ &=2\Phi(1.622)-1 =2\times0.9474-1 =0.8948. \end{aligned}` |
| 2538 | 21137-21144 | 0.29 | inline_unsafe_marker | bracket | `X_i= \begin{cases} 1, & \text{第 }i\text{ 粒为良种},\\ 0, & \text{第 }i\text{ 粒不是良种}, \end{cases} \qquad i=1,2,\dots,180.` |
| 2540 | 21150-21152 | 0.42 | inline_safe | bracket | `\hat p=\frac1{180}\sum_{i=1}^{180}X_i.` |
| 2541 | 21154-21156 | 0.26 | inline_safe | bracket | `\frac{\hat p-p}{\sqrt{pq/180}}\approx N(0,1).` |
| 2542 | 21158-21162 | 0.21 | inline_safe | bracket | `\sqrt{\frac{pq}{180}} =\sqrt{\frac{(1/6)(5/6)}{180}} =\frac1{36},` |
| 2543 | 21164-21167 | 0.26 | inline_safe | bracket | `P\left\{\left\|\hat p-\frac16\right\|<C\right\} \approx 2\Phi(36C)-1.` |
| 2544 | 21169-21171 | 0.23 | inline_safe | bracket | `2\Phi(36C)-1=0.99,` |
| 2545 | 21173-21175 | 0.19 | inline_safe | bracket | `\Phi(36C)=0.995.` |
| 2547 | 21188-21190 | 0.17 | inline_safe | bracket | `\|X-100\|\ge3.` |
| 2548 | 21192-21196 | 0.30 | normalized_width_not_low | bracket | `p=P\{\|X-100\|\ge3\} =2\left[1-\Phi\left(\frac3{\sqrt{2.34}}\right)\right] \approx2(1-\Phi(1.96))=0.05.` |
| 2549 | 21198-21200 | 0.17 | inline_safe | bracket | `Y\sim B(100,p).` |
| 2550 | 21202-21207 | 0.32 | normalized_width_not_low | bracket | `P(Y\ge3) \approx1-e^{-5}\left(1+5+\frac{5^2}{2!}\right) =1-\frac{37}{2}e^{-5} \approx0.8753.` |
| 2551 | 21215-21219 | 0.30 | normalized_width_not_low | bracket | `p=P\{\|X-100\|\ge3\} =2\left[1-\Phi\left(\frac3{\sqrt{2.25}}\right)\right] =2(1-\Phi(2)).` |
| 2552 | 21221-21223 | 0.24 | inline_safe | bracket | `Y\sim B(100,0.0456).` |
| 2553 | 21225-21230 | 0.43 | normalized_width_not_low | bracket | `P(Y\ge5) \approx1-e^{-4.56}\left(1+4.56+\frac{4.56^2}{2!} +\frac{4.56^3}{3!}+\frac{4.56^4}{4!}\right) \approx0.479.` |
| 2554 | 21240-21242 | 0.19 | inline_safe | bracket | `X\sim B(100,0.9).` |
| 2556 | 21248-21254 | 0.44 | inline_unsafe_marker | bracket | `\begin{aligned} P(X\ge85) &\approx 1-\Phi\!\left(\frac{85-90}{\sqrt9}\right)\\ &=1-\Phi(-1.67)=\Phi(1.67)\approx0.9525. \end{aligned}` |
| 2557 | 21263-21265 | 0.29 | inline_safe | bracket | `X\sim B(5000000,0.0003).` |
| 2558 | 21267-21269 | 0.37 | inline_safe | bracket | `EX=5000000\times0.0003=1500,` |
| 2561 | 21278-21280 | 0.28 | inline_safe | bracket | `P\{X\le10M-2\}\ge0.99.` |
| 2562 | 21282-21284 | 0.29 | inline_safe | bracket | `\frac{10M-2-1500}{\sqrt{1500}}\ge2.33.` |
| 2563 | 21286-21288 | 0.43 | inline_safe | bracket | `M\ge \frac{1502+2.33\sqrt{1500}}{10}\approx159.23.` |
| 2564 | 21290-21292 | 0.10 | inline_safe | bracket | `M=160.` |
| 2565 | 21297-21304 | 0.25 | inline_unsafe_marker | bracket | `\xi_n\sim \begin{pmatrix} -\sqrt n & 0 & \sqrt n\\ \dfrac1n & 1-\dfrac2n & \dfrac1n \end{pmatrix}, \qquad n=2,3,4,\dots` |
| 2569 | 21322-21324 | 0.42 | inline_safe | bracket | `\overline{\xi}_n=\frac1n\sum_{k=2}^{n+1}\xi_k.` |
| 2571 | 21331-21335 | 0.18 | inline_safe | bracket | `P\{\|\overline{\xi}_n\| \ge \varepsilon\} \le \frac{D\overline{\xi}_n}{\varepsilon^2} =\frac{2}{n\varepsilon^2}\to0.` |
| 2572 | 21337-21339 | 0.34 | inline_safe | bracket | `\lim_{n\to\infty}P\{\|\overline{\xi}_n\|<\varepsilon\}=1,` |
| 2574 | 21354-21356 | 0.37 | inline_safe | bracket | `EX_i=\frac{0.005+0.035}{2}=0.02,` |
| 2575 | 21357-21359 | 0.48 | inline_safe | bracket | `DX_i=\frac{(0.035-0.005)^2}{12}=0.000075.` |
| 2576 | 21361-21363 | 0.45 | inline_safe | bracket | `\overline X=\frac1{2000}\sum_{i=1}^{2000}X_i.` |
| 2577 | 21365-21367 | 0.33 | inline_safe | bracket | `\overline X\approx N\left(0.02,\frac{0.000075}{2000}\right).` |
| 2578 | 21369-21375 | 0.30 | inline_unsafe_marker | bracket | `\begin{aligned} P(\overline X<0.025) &\approx \Phi\!\left(\frac{0.025-0.02}{\sqrt{0.000075/2000}}\right)\\ &=\Phi(25.82)\approx1. \end{aligned}` |
| 2579 | 21381-21387 | 0.46 | inline_unsafe_marker | bracket | `f(x)= \begin{cases} \dfrac1{20000}e^{-\frac1{20000}(x-365)},&x\ge365,\\[6pt] 0,&x<365. \end{cases}` |
| 2580 | 21395-21401 | 0.36 | inline_unsafe_marker | bracket | `F(x)= \begin{cases} 0,&x<365,\\[4pt] 1-e^{-\frac1{20000}(x-365)},&x\ge365. \end{cases}` |
| 2582 | 21409-21411 | 0.22 | inline_safe | bracket | `N\sim B(1000,0.04).` |
| 2584 | 21418-21420 | 0.42 | inline_safe | bracket | `2000N\ge100000,\qquad\text{即 }N\ge50.` |
| 2585 | 21422-21431 | 0.30 | inline_unsafe_marker | bracket | `\begin{aligned} P(\text{亏本}) &\approx P(N\ge50)\\ &=P\left(\frac{N-40}{6.2}\ge\frac{50-40}{6.2}\right)\\ &\approx1-\Phi(1.61) =1-0.946 =0.054. \end{aligned}` |
| 2586 | 21434-21436 | 0.21 | inline_safe | bracket | `1000P_0-2000N.` |
| 2587 | 21438-21440 | 0.37 | inline_safe | bracket | `P(1000P_0-2000N<0)\le0.01,` |
| 2588 | 21442-21444 | 0.25 | inline_safe | bracket | `P\left(N\ge\frac{P_0}{2}\right)\le0.01.` |
| 2589 | 21446-21448 | 0.25 | inline_safe | bracket | `\frac{P_0/2-40}{6.2}\ge2.33.` |
| 2590 | 21450-21452 | 0.44 | inline_safe | bracket | `P_0\ge2(40+6.2\times2.33)=108.892.` |
| 2591 | 21454-21456 | 0.20 | inline_safe | bracket | `P_0\approx108.9\text{ 元/件},` |
| 2593 | 21471-21473 | 0.30 | inline_safe | bracket | `\frac{m/n-p}{\sqrt{p(1-p)/n}}\approx N(0,1).` |
| 2594 | 21475-21477 | 0.34 | inline_safe | bracket | `P\left(\left\|\frac mn-p\right\|<0.1\right)>0.95.` |
| 2595 | 21479-21481 | 0.35 | inline_safe | bracket | `2\Phi\left(\frac{0.1}{\sqrt{p(1-p)/n}}\right)-1>0.95.` |
| 2596 | 21483-21485 | 0.27 | inline_safe | bracket | `\frac{0.1}{\sqrt{p(1-p)/n}}\ge1.96.` |
| 2597 | 21487-21489 | 0.26 | inline_safe | bracket | `n\ge (19.6)^2p(1-p).` |
| 2598 | 21491-21493 | 0.23 | inline_safe | bracket | `p(1-p)\le\frac14,` |
| 2599 | 21495-21497 | 0.39 | inline_safe | bracket | `n\ge (19.6)^2\cdot\frac14=96.04.` |
| 2600 | 21499-21501 | 0.08 | inline_safe | bracket | `n=97.` |
| 2601 | 21511-21513 | 0.19 | inline_safe | bracket | `\xi_1,\xi_2,\dots,\xi_n,` |
| 2603 | 21519-21521 | 0.28 | inline_safe | bracket | `S_n=\sum_{i=1}^n \xi_i,` |
| 2604 | 21523-21525 | 0.41 | inline_safe | bracket | `ES_n=0,\qquad DS_n=\frac n3.` |
| 2605 | 21527-21529 | 0.22 | inline_safe | bracket | `\frac{S_n}{\sqrt{n/3}}\approx N(0,1).` |
| 2606 | 21531-21533 | 0.27 | inline_safe | bracket | `P(\|S_n\|\le10)\ge0.99.` |
| 2607 | 21535-21539 | 0.29 | normalized_width_not_low | bracket | `P\left(\left\|\frac{S_n}{\sqrt{n/3}}\right\|\le \frac{10}{\sqrt{n/3}}\right) \approx 2\Phi\left(\frac{10}{\sqrt{n/3}}\right)-1\ge0.99.` |
| 2608 | 21541-21543 | 0.25 | inline_safe | bracket | `\Phi\left(\frac{10}{\sqrt{n/3}}\right)\ge0.995.` |
| 2609 | 21545-21547 | 0.19 | inline_safe | bracket | `\frac{10}{\sqrt{n/3}}\ge2.58.` |
| 2610 | 21549-21551 | 0.31 | inline_safe | bracket | `n\le 3\left(\frac{10}{2.58}\right)^2\approx45.06.` |
| 2611 | 21553-21555 | 0.07 | inline_safe | bracket | `n=45` |
| 2613 | 21565-21574 | 0.32 | normalized_width_not_low | bracket | `\lim_{n\to\infty} P\left( \left\| \frac1n\sum_{i=1}^n \xi_i - \frac1n\sum_{i=1}^n E(\xi_i) \right\|<\varepsilon \right)=1.` |
| 2614 | 21578-21580 | 0.28 | inline_safe | bracket | `S_n=\sum_{i=1}^n \xi_i.` |
| 2615 | 21582-21584 | 0.46 | inline_safe | bracket | `E\left(\frac{S_n}{n}\right)=\frac1n\sum_{i=1}^n E(\xi_i),` |
| 2616 | 21586-21590 | 0.38 | normalized_width_not_low | bracket | `D\left(\frac{S_n}{n}\right) =\frac1{n^2}D(S_n) =\frac1{n^2}D\!\left(\sum_{i=1}^n \xi_i\right).` |
| 2617 | 21592-21607 | 0.35 | inline_unsafe_marker | bracket | `\begin{aligned} P\left( \left\| \frac{S_n}{n} - E\left(\frac{S_n}{n}\right) \right\|\ge\varepsilon \right) &\le \frac{D(S_n/n)}{\varepsilon^2}\\ &= \frac1{\varepsilon^2} \frac1{n^...` |
| 2618 | 21609-21618 | 0.32 | normalized_width_not_low | bracket | `\lim_{n\to\infty} P\left( \left\| \frac1n\sum_{i=1}^n \xi_i - \frac1n\sum_{i=1}^n E(\xi_i) \right\|\ge\varepsilon \right)=0.` |
| 2619 | 21620-21629 | 0.32 | normalized_width_not_low | bracket | `\lim_{n\to\infty} P\left( \left\| \frac1n\sum_{i=1}^n \xi_i - \frac1n\sum_{i=1}^n E(\xi_i) \right\|<\varepsilon \right)=1.` |
| 2620 | 21639-21641 | 0.42 | inline_safe | bracket | `X_i\sim P(1),\qquad i=1,2,\dots,52,` |
| 2621 | 21643-21645 | 0.26 | inline_safe | bracket | `S=\sum_{i=1}^{52}X_i.` |
| 2622 | 21647-21649 | 0.31 | inline_safe | bracket | `ES=52,\qquad DS=52.` |
| 2623 | 21651-21653 | 0.22 | inline_safe | bracket | `\frac{S-52}{\sqrt{52}}\approx N(0,1).` |
| 2624 | 21655-21666 | 0.29 | inline_unsafe_marker | bracket | `\begin{aligned} P(50\le S\le70) &\approx \Phi\left(\frac{70-52}{\sqrt{52}}\right) - \Phi\left(\frac{50-52}{\sqrt{52}}\right)\\ &= \Phi(2.50)-\Phi(-0.28)\\ &=\Phi(2.50)+\Phi(0.28...` |
| 2626 | 21678-21685 | 0.48 | inline_unsafe_marker | bracket | `\begin{aligned} P\{5 \leq X \leq 10\} &= P\!\left\{\frac{5 - 5}{\sqrt{4.75}} \leq \frac{X - 5}{\sqrt{4.75}} \leq \frac{10 - 5}{\sqrt{4.75}}\right\} \\ &= P\!\left\{0 \leq \frac{...` |
| 2627 | 21701-21703 | 0.23 | inline_safe | bracket | `X_i\sim B\!\left(1,\frac12\right),` |
| 2628 | 21707-21709 | 0.28 | inline_safe | bracket | `S=\sum_{i=1}^{100} X_i.` |
| 2631 | 21731-21733 | 0.49 | inline_safe | bracket | `n\ln 0.99 > \ln 0.9 \implies n < \frac{\ln 0.9}{\ln 0.99} \approx 10.48,` |
| 2638 | 21786-21788 | 0.42 | inline_safe | bracket | `E(T_2) = \frac{10000}{4} \times 2.3756 = 5939.` |
| 2640 | 21935-21937 | 0.48 | inline_safe | bracket | `F(x_1, x_2, \dots, x_n) = \prod_{i=1}^{n} F(x_i).` |
| 2641 | 21977-21979 | 0.31 | inline_safe | bracket | `\sum_{i=1}^{n}\left(\frac{X_i-\mu}{\sigma}\right)^2` |
| 2643 | 22065-22067 | 0.46 | inline_safe | bracket | `S^2=\frac{1}{n-1}\sum_{i=1}^{n}(X_i-\overline{X})^2,` |
| 2648 | 22110-22113 | 0.49 | normalized_width_not_low | bracket | `\overline{x} =\frac{17\times5+18\times15+19\times22+20\times8}{50}.` |
| 2649 | 22115-22118 | 0.43 | normalized_width_not_low | bracket | `17\times5+18\times15+19\times22+20\times8 =85+270+418+160=933.` |
| 2650 | 22120-22122 | 0.23 | inline_safe | bracket | `\overline{x}=\frac{933}{50}=18.66.` |
| 2651 | 22134-22138 | 0.40 | normalized_width_not_low | bracket | `Y_i=X_i-\overline{X} =X_i-\frac{1}{n}\sum_{k=1}^{n}X_k =\left(1-\frac{1}{n}\right)X_i-\frac{1}{n}\sum_{k\ne i}X_k.` |
| 2652 | 22141-22145 | 0.24 | normalized_width_not_low | bracket | `DY_i =\left(1-\frac{1}{n}\right)^2 DX_i \frac{1}{n^2}\sum_{k\ne i}DX_k.` |
| 2653 | 22147-22152 | 0.32 | normalized_width_not_low | bracket | `DY_i=\left(1-\frac{1}{n}\right)^2+\frac{n-1}{n^2} =1-\frac{2}{n}+\frac{1}{n^2}+\frac{n-1}{n^2} =1-\frac{1}{n} =\frac{n-1}{n}.` |
| 2656 | 22174-22176 | 0.21 | inline_safe | bracket | `E(Y_1+Y_n)=0.` |
| 2657 | 22178-22180 | 0.33 | inline_safe | bracket | `P\{Y_1+Y_n\le0\}=\frac12.` |
| 2658 | 22185-22188 | 0.32 | normalized_width_not_low | bracket | `Y=\left(\sum_{i=1}^{3}X_i\right)^2+ \left(\sum_{i=4}^{6}X_i\right)^2.` |
| 2660 | 22199-22201 | 0.39 | inline_safe | bracket | `U\sim N(0,3),\qquad V\sim N(0,3),` |
| 2661 | 22203-22205 | 0.49 | inline_safe | bracket | `\frac{U}{\sqrt3}\sim N(0,1),\qquad \frac{V}{\sqrt3}\sim N(0,1),` |
| 2662 | 22207-22212 | 0.17 | normalized_width_not_low | bracket | `\frac13Y =\left(\frac{U}{\sqrt3}\right)^2+ \left(\frac{V}{\sqrt3}\right)^2 \sim\chi^2(2).` |
| 2663 | 22218-22220 | 0.46 | inline_safe | bracket | `Y_i=X_i-\overline X,\qquad i=1,2,\cdots,n.` |
| 2666 | 22240-22243 | 0.36 | normalized_width_not_low | bracket | `\operatorname{Cov}(Y_1,Y_n) =\operatorname{Cov}(X_1-\overline X,\ X_n-\overline X).` |
| 2667 | 22245-22250 | 0.46 | normalized_width_not_low | bracket | `\operatorname{Cov}(X_1,X_n)=0,\qquad \operatorname{Cov}(X_1,\overline X)=\operatorname{Cov}(X_n,\overline X)=\frac{\sigma^2}{n}, \qquad D\overline X=\frac{\sigma^2}{n},` |
| 2668 | 22252-22256 | 0.32 | normalized_width_not_low | bracket | `\operatorname{Cov}(Y_1,Y_n) =0-\frac{\sigma^2}{n}-\frac{\sigma^2}{n}+\frac{\sigma^2}{n} =-\frac{\sigma^2}{n}.` |
| 2669 | 22259-22262 | 0.21 | inline_safe | bracket | `E\!\left[c(Y_1+Y_n)^2\right] =cD(Y_1+Y_n).` |
| 2670 | 22264-22269 | 0.39 | normalized_width_not_low | bracket | `D(Y_1+Y_n) =DY_1+DY_n+2\operatorname{Cov}(Y_1,Y_n) =\left(\frac{n-1}{n}+\frac{n-1}{n}-\frac2n\right)\sigma^2 =\frac{2(n-2)}{n}\sigma^2.` |
| 2671 | 22271-22275 | 0.24 | normalized_width_not_low | bracket | `c\cdot\frac{2(n-2)}{n}=1, \qquad\text{即}\qquad c=\frac{n}{2(n-2)}.` |
| 2672 | 22278-22280 | 0.45 | inline_safe | bracket | `D\hat\theta_1=V_1,\qquad D\hat\theta_2=V_2.` |
| 2674 | 22286-22291 | 0.26 | normalized_width_not_low | bracket | `D\hat\theta_3 =\left(\frac{V_2}{V_1+V_2}\right)^2V_1 +\left(\frac{V_1}{V_1+V_2}\right)^2V_2 =\frac{V_1V_2}{V_1+V_2},` |
| 2676 | 22341-22343 | 0.40 | inline_safe | bracket | `\chi^2 = X_1^2 + X_2^2 + \cdots + X_n^2,` |
| 2678 | 22369-22371 | 0.44 | inline_safe | bracket | `\sum_{i=1}^{10}(Y_i-\overline{Y})^2\sim \chi^2(9).` |
| 2680 | 22381-22383 | 0.10 | inline_safe | bracket | `EZ=18.` |
| 2684 | 22409-22411 | 0.23 | inline_safe | bracket | `\text{即}\quad \frac{Y}{8}\sim \chi^2(2),` |
| 2685 | 22417-22419 | 0.49 | inline_safe | bracket | `X = a(X_1 - 2X_2)^2 + b(3X_3 - 4X_4)^2,` |
| 2690 | 22446-22448 | 0.47 | inline_safe | bracket | `X = a(X_1 - 2X_2)^2 + b(3X_3 - 4X_4)^2` |
| 2691 | 22456-22458 | 0.46 | inline_safe | bracket | `Z=\frac1{\sigma^2}\sum_{i=1}^6(\xi_i-\mu)^2,` |
| 2692 | 22477-22479 | 0.23 | inline_safe | bracket | `\frac{\xi_i-\mu}{\sigma}\sim N(0,1),` |
| 2693 | 22481-22483 | 0.48 | inline_safe | bracket | `Z=\sum_{i=1}^6\left(\frac{\xi_i-\mu}{\sigma}\right)^2\sim\chi^2(6).` |
| 2695 | 22489-22493 | 0.46 | normalized_width_not_low | bracket | `f_Z(z)=\frac{1}{2^3\Gamma(3)}z^2e^{-z/2} =\frac{1}{8\cdot2}z^2e^{-z/2} =\frac1{16}z^2e^{-z/2},\qquad z>0.` |
| 2696 | 22502-22504 | 0.15 | inline_safe | bracket | `t = \frac{X}{\sqrt{Y/n}},` |
| 2697 | 22529-22531 | 0.26 | inline_safe | bracket | `Y=\frac{X_1-X_2}{\sqrt{X_3^2+X_4^2}}` |
| 2700 | 22550-22552 | 0.27 | inline_safe | bracket | `\frac{X_{n+1} - \overline{X}}{S}\sqrt{\frac{n}{n+1}}` |
| 2703 | 22578-22580 | 0.17 | inline_safe | bracket | `X^2 \sim F(1,n).` |
| 2704 | 22582-22584 | 0.31 | inline_safe | bracket | `P\{Y > c^2\} = P\{X^2 > c^2\}.` |
| 2705 | 22585-22587 | 0.29 | inline_safe | bracket | `\text{而 } X^2>c^2 \Longleftrightarrow X>c \text{ 或 } X<-c.` |
| 2706 | 22589-22591 | 0.18 | inline_safe | bracket | `P\{X<-c\}=\alpha.` |
| 2708 | 22605-22607 | 0.15 | inline_safe | bracket | `F = \frac{X/n_1}{Y/n_2},` |
| 2709 | 22626-22628 | 0.39 | inline_safe | bracket | `\sum_{i=2}^{n}X_i^2\sim\chi^2(n-1),` |
| 2710 | 22630-22634 | 0.36 | normalized_width_not_low | bracket | `\frac{X_1^2/1}{\left(\sum_{i=2}^{n}X_i^2\right)/(n-1)} =\frac{(n-1)X_1^2}{\sum_{i=2}^{n}X_i^2} \sim F(1,n-1).` |
| 2711 | 22648-22650 | 0.24 | inline_safe | bracket | `\frac{(n-1)X_1^2}{\displaystyle\sum_{i=2}^{n}X_i^2}` |
| 2712 | 22655-22657 | 0.20 | inline_safe | bracket | `X_1^2\sim\chi^2(1).` |
| 2713 | 22659-22661 | 0.39 | inline_safe | bracket | `\sum_{i=2}^{n}X_i^2\sim\chi^2(n-1),` |
| 2714 | 22663-22667 | 0.39 | normalized_width_not_low | bracket | `\frac{(n-1)X_1^2}{\sum_{i=2}^{n}X_i^2} =\frac{X_1^2/1}{\left(\sum_{i=2}^{n}X_i^2\right)/(n-1)} \sim F(1,n-1).` |
| 2715 | 22679-22683 | 0.40 | normalized_width_not_low | bracket | `X_1^2 \sim \chi^2(1), \qquad X_2^2+X_3^2+X_4^2 \sim \chi^2(3),` |
| 2716 | 22687-22689 | 0.37 | inline_safe | bracket | `\frac{\chi^2(n_1)/n_1}{\chi^2(n_2)/n_2}\sim F(n_1,n_2).` |
| 2718 | 22696-22698 | 0.07 | inline_safe | bracket | `c=3.` |
| 2719 | 22708-22710 | 0.15 | inline_safe | bracket | `T = \frac{U}{\sqrt{V/n}},` |
| 2720 | 22714-22716 | 0.29 | inline_safe | bracket | `T^2 = \frac{U^2/1}{V/n} \sim F(1,n),` |
| 2721 | 22720-22722 | 0.18 | inline_safe | bracket | `T^2 \sim F(1,15).` |
| 2722 | 22733-22735 | 0.15 | inline_safe | bracket | `X = \frac{U}{\sqrt{V/n}},` |
| 2723 | 22739-22741 | 0.29 | inline_safe | bracket | `X^2 = \frac{U^2/1}{V/n} \sim F(1,n).` |
| 2724 | 22743-22745 | 0.35 | inline_safe | bracket | `Y = \frac{1}{X^2} = \frac{V/n}{U^2/1} \sim F(n, 1).` |
| 2725 | 22746-22748 | 0.07 | inline_safe | bracket | `\text{故应选 } C.` |
| 2728 | 22769-22771 | 0.39 | inline_safe | bracket | `\frac{S_1^2/S_2^2}{\sigma_1^2/\sigma_2^2}\sim F(m{-}1,n{-}1).` |
| 2729 | 22829-22833 | 0.39 | normalized_width_not_low | bracket | `\frac{(n-1)S^2}{\sigma^2} =\frac{1}{\sigma^2}\sum_{i=1}^{n}(X_i-\overline{X})^2 \sim \chi^2(n-1).` |
| 2731 | 22854-22858 | 0.49 | normalized_width_not_low | bracket | `EX^2=\int_{-\infty}^{+\infty}x^2\cdot\frac{1}{2}e^{-\|x\|}\,\mathrm{d}x =2\int_0^{+\infty}x^2\cdot\frac{1}{2}e^{-x}\,\mathrm{d}x =\int_0^{+\infty}x^2\,e^{-x}\,\mathrm{d}x=\Gamma(3...` |
| 2733 | 22869-22871 | 0.30 | inline_safe | bracket | `E(\overline X),\qquad D(\overline X).` |
| 2734 | 22875-22877 | 0.40 | inline_safe | bracket | `E(X_i)=n,\qquad D(X_i)=2n.` |
| 2735 | 22879-22881 | 0.24 | inline_safe | bracket | `E(\overline X)=E(X_1)=n,` |
| 2736 | 22883-22886 | 0.21 | inline_safe | bracket | `D(\overline X)=\frac{D(X_1)}{n} =\frac{2n}{n}=2.` |
| 2737 | 22888-22890 | 0.38 | inline_safe | bracket | `E(\overline X)=n,\qquad D(\overline X)=2.` |
| 2738 | 22903-22907 | 0.43 | normalized_width_not_low | bracket | `\overline{X}\sim N\!\left(\mu,\frac{\sigma^2}{n}\right),\qquad \frac{(n-1)S^2}{\sigma^2}\sim\chi^2(n-1),\qquad \frac{\sqrt{n}(\overline{X}-\mu)}{S}\sim t(n-1).` |
| 2739 | 22911-22913 | 0.32 | inline_safe | bracket | `E(2X_2-X_1)=2\mu-\mu=\mu,` |
| 2741 | 22920-22922 | 0.30 | inline_safe | bracket | `\frac{\sqrt{n}(\overline{X}-\mu)}{S}\sim t(n-1),` |
| 2742 | 22924-22926 | 0.33 | inline_safe | bracket | `\frac{n(\overline{X}-\mu)^2}{S^2}\sim F(1,n-1),` |
| 2743 | 22930-22932 | 0.31 | inline_safe | bracket | `\frac{(n-1)S^2}{\sigma^2}\sim\chi^2(n-1),` |
| 2744 | 22936-22938 | 0.30 | inline_safe | bracket | `\frac{\sqrt{n}(\overline{X}-\mu)}{S}\sim t(n-1),` |
| 2745 | 22948-22950 | 0.44 | inline_safe | bracket | `E\!\left(\sum_{i=1}^{n}(X_i-\overline{X})^2\right)=\underline{\hspace{2cm}}.` |
| 2746 | 22958-22960 | 0.34 | inline_safe | bracket | `E\!\left(\sum_{i=1}^{n}(X_i-\overline{X})^2\right),` |
| 2748 | 22967-22969 | 0.46 | inline_safe | bracket | `E\!\left[\frac{1}{4}\sum_{i=1}^{n}(X_i-\overline{X})^2\right]=n-1.` |
| 2749 | 22971-22973 | 0.47 | inline_safe | bracket | `E\!\left(\sum_{i=1}^{n}(X_i-\overline{X})^2\right)=4(n-1).` |
| 2750 | 22980-22982 | 0.46 | inline_safe | bracket | `Y = \frac{X_1 + X_2 + X_3 + X_4}{\sqrt{X_5^2 + X_6^2 + X_7^2 + X_8^2}}` |
| 2751 | 22991-22993 | 0.09 | inline_safe | bracket | `\frac{U}{\sqrt{V/\nu}}` |
| 2758 | 23040-23042 | 0.18 | inline_safe | bracket | `\overline{X}\sim N\!\left(0,\frac{4}{10}\right).` |
| 2759 | 23044-23046 | 0.24 | inline_safe | bracket | `\frac{\sqrt{10}\,\overline{X}}{2}\sim N(0,1),` |
| 2760 | 23048-23050 | 0.23 | inline_safe | bracket | `\frac{10\overline{X}^2}{4}\sim\chi^2(1).` |
| 2761 | 23053-23055 | 0.38 | inline_safe | bracket | `\frac{(n-1)S^2}{\sigma^2}=\frac{9S^2}{4}\sim\chi^2(9),` |
| 2763 | 23064-23066 | 0.08 | inline_safe | bracket | `c=10.` |
| 2764 | 23076-23078 | 0.39 | inline_safe | bracket | `X_1-X_2\sim N(0,4+4)=N(0,8),` |
| 2765 | 23080-23082 | 0.26 | inline_safe | bracket | `\frac{X_1-X_2}{\sqrt{8}}\sim N(0,1).` |
| 2766 | 23085-23089 | 0.31 | normalized_width_not_low | bracket | `\sum_{i=3}^{8}X_i^2 =4\sum_{i=3}^{8}\left(\frac{X_i}{2}\right)^2 \sim 4\chi^2(6).` |
| 2768 | 23097-23099 | 0.32 | inline_safe | bracket | `c=\sqrt{3},\qquad Y\sim t(6).` |
| 2769 | 23102-23104 | 0.34 | inline_safe | bracket | `\overline{X}\sim N\!\left(0,\frac{4}{8}\right)=N\!\left(0,\frac12\right),` |
| 2770 | 23106-23108 | 0.20 | inline_safe | bracket | `\sqrt{2}\,\overline{X}\sim N(0,1).` |
| 2772 | 23118-23120 | 0.20 | inline_safe | bracket | `\overline{X}\sim N\!\left(1,\frac{\sigma^2}{6}\right).` |
| 2774 | 23130-23132 | 0.21 | inline_safe | bracket | `\frac{5S^2}{\sigma^2}\sim\chi^2(5),` |
| 2778 | 23172-23174 | 0.27 | inline_safe | bracket | `\overline{X}-\overline{Y}\sim N\!\left(0,\frac{2\sigma^2}{n}\right).` |
| 2779 | 23176-23180 | 0.28 | normalized_width_not_low | bracket | `P\{\|\overline{X}-\overline{Y}\|>\sigma\} = P\!\left\{\left\|\frac{\overline{X}-\overline{Y}}{\sigma\sqrt{2/n}}\right\|>\sqrt{\frac{n}{2}}\right\} = 2\!\left[1-\Phi\!\left(\sqrt{\fr...` |
| 2781 | 23194-23197 | 0.36 | normalized_width_not_low | bracket | `\overline X\sim N\!\left(0,\frac4{10}\right),\qquad \overline Y\sim N\!\left(0,\frac9{15}\right).` |
| 2784 | 23208-23210 | 0.31 | inline_safe | bracket | `E\|\overline X-\overline Y\|=\sqrt{\frac2\pi}.` |
| 2785 | 23216-23218 | 0.42 | inline_safe | bracket | `Y = \frac{2X_1^2 + X_2^2 + \cdots + X_{10}^2}{X_{11}^2 + X_{12}^2 + \cdots + X_{15}^2}` |
| 2786 | 23225-23227 | 0.46 | inline_safe | bracket | `\chi_1^2 = \frac{2X_1^2+X_2^2+\cdots+X_{10}^2}{9}` |
| 2788 | 23233-23236 | 0.43 | normalized_width_not_low | bracket | `U = \dfrac{2X_1^2+\cdots+X_{10}^2}{9},\qquad V = \dfrac{X_{11}^2+\cdots+X_{15}^2}{9}.` |
| 2789 | 23248-23251 | 0.43 | inline_safe | bracket | `Y=\frac{X_1^2+X_2^2+\cdots+X_{10}^2} {2\left(X_{11}^2+X_{12}^2+\cdots+X_{15}^2\right)}` |
| 2790 | 23256-23259 | 0.45 | normalized_width_not_low | bracket | `U=\sum_{i=1}^{10}\left(\frac{X_i}{2}\right)^2,\qquad V=\sum_{i=11}^{15}\left(\frac{X_i}{2}\right)^2.` |
| 2791 | 23261-23265 | 0.14 | inline_safe | bracket | `Y=\frac{4U}{2\cdot4V} =\frac{U}{2V} =\frac{U/10}{V/5}.` |
| 2792 | 23267-23269 | 0.15 | inline_safe | bracket | `Y\sim F(10,5).` |
| 2793 | 23274-23276 | 0.14 | inline_safe | bracket | `\frac{2Y_1}{Y_2+Y_3}` |
| 2794 | 23281-23283 | 0.26 | inline_safe | bracket | `Y_2+Y_3\sim\chi^2(2n).` |
| 2795 | 23285-23288 | 0.26 | inline_safe | bracket | `\frac{2Y_1}{Y_2+Y_3} =\frac{Y_1/n}{(Y_2+Y_3)/(2n)}.` |
| 2796 | 23290-23292 | 0.27 | inline_safe | bracket | `\frac{2Y_1}{Y_2+Y_3}\sim F(n,2n).` |
| 2797 | 23308-23310 | 0.23 | inline_safe | bracket | `\frac{X_i-1}{2}\sim N(0,1).` |
| 2798 | 23312-23316 | 0.37 | normalized_width_not_low | bracket | `\frac14\sum_{i=1}^n(X_i-1)^2 =\sum_{i=1}^n\left(\frac{X_i-1}{2}\right)^2 \sim\chi^2(n),` |
| 2799 | 23320-23322 | 0.24 | inline_safe | bracket | `\overline X\sim N\left(1,\frac4n\right),` |
| 2800 | 23324-23326 | 0.23 | inline_safe | bracket | `\frac{\overline X-1}{2/\sqrt n}\sim N(0,1),` |
| 2801 | 23341-23343 | 0.49 | inline_safe | bracket | `\frac{X_i-\mu}{\sigma}\sim N(0,1),\qquad i=1,2,\dots,n,` |
| 2802 | 23345-23349 | 0.40 | normalized_width_not_low | bracket | `\frac1{\sigma^2}\sum_{i=1}^{n}(X_i-\mu)^2 =\sum_{i=1}^{n}\left(\frac{X_i-\mu}{\sigma}\right)^2 \sim\chi^2(n).` |
| 2803 | 23353-23355 | 0.22 | inline_safe | bracket | `\overline X\sim N\left(\mu,\frac{\sigma^2}{n}\right).` |
| 2805 | 23361-23363 | 0.31 | inline_safe | bracket | `\frac{\sqrt n(\overline X-\mu)}{S}\sim t(n-1),` |
| 2806 | 23369-23371 | 0.09 | inline_safe | bracket | `Y=X^2` |
| 2807 | 23376-23378 | 0.15 | inline_safe | bracket | `X=\frac{U}{\sqrt{V/m}},` |
| 2808 | 23380-23382 | 0.18 | inline_safe | bracket | `X^2=\frac{U^2/1}{V/m}.` |
| 2809 | 23384-23386 | 0.21 | inline_safe | bracket | `Y=X^2\sim F(1,m).` |
| 2810 | 23392-23394 | 0.17 | inline_safe | bracket | `P(X>z_\alpha)=\alpha.` |
| 2811 | 23396-23398 | 0.16 | inline_safe | bracket | `P(\|X\|<c)=\alpha,` |
| 2812 | 23403-23405 | 0.15 | inline_safe | bracket | `P(\|X\|<c)=\alpha` |
| 2813 | 23407-23409 | 0.09 | inline_safe | bracket | `\frac{1-\alpha}{2}.` |
| 2814 | 23411-23413 | 0.21 | inline_safe | bracket | `P(X>c)=\frac{1-\alpha}{2}.` |
| 2815 | 23415-23417 | 0.16 | inline_safe | bracket | `c=z_{\frac{1-\alpha}{2}}.` |
| 2816 | 23431-23435 | 0.38 | normalized_width_not_low | bracket | `\sum_{i=1}^n (X_i-\overline X)^2 =\frac{1}{1}\sum_{i=1}^n (X_i-\overline X)^2 \sim\chi^2(n-1).` |
| 2817 | 23438-23440 | 0.41 | inline_safe | bracket | `\sum_{i=1}^n (X_i-\mu)^2\sim\chi^2(n),` |
| 2818 | 23442-23444 | 0.25 | inline_safe | bracket | `\frac{\overline X-\mu}{S/\sqrt n}\sim t(n-1),` |
| 2819 | 23450-23452 | 0.31 | inline_safe | bracket | `\xi=\frac{(X_2+X_3+X_4)^2}{3X_1^2}.` |
| 2820 | 23457-23459 | 0.32 | inline_safe | bracket | `X_2+X_3+X_4\sim N(0,27).` |
| 2821 | 23461-23463 | 0.33 | inline_safe | bracket | `\frac{X_2+X_3+X_4}{3\sqrt3}\sim N(0,1),` |
| 2822 | 23465-23467 | 0.39 | inline_safe | bracket | `\frac{(X_2+X_3+X_4)^2}{27}\sim\chi^2(1).` |
| 2823 | 23469-23471 | 0.22 | inline_safe | bracket | `\frac{X_1^2}{9}\sim\chi^2(1).` |
| 2824 | 23473-23478 | 0.31 | normalized_width_not_low | bracket | `\xi =\frac{(X_2+X_3+X_4)^2}{3X_1^2} =\frac{\dfrac{(X_2+X_3+X_4)^2}{27}}{\dfrac{X_1^2}{9}} \sim F(1,1).` |
| 2825 | 23520-23522 | 0.27 | inline_safe | bracket | `P(\|X\|>x_\alpha)=（\quad）。` |
| 2826 | 23530-23532 | 0.17 | inline_safe | bracket | `P(X>x_\alpha)=\alpha.` |
| 2827 | 23534-23536 | 0.20 | inline_safe | bracket | `P(X<-x_\alpha)=\alpha.` |
| 2829 | 23545-23547 | 0.28 | inline_safe | bracket | `P(\|X\|\le x_\alpha)=（\quad）。` |
| 2830 | 23554-23556 | 0.18 | inline_safe | bracket | `P(X\le x_\alpha)=\alpha.` |
| 2831 | 23558-23560 | 0.39 | inline_safe | bracket | `P(X<-x_\alpha)=P(X>x_\alpha)=1-\alpha.` |
| 2832 | 23562-23567 | 0.27 | normalized_width_not_low | bracket | `P(\|X\|\le x_\alpha) =P(-x_\alpha\le X\le x_\alpha) =1-2(1-\alpha) =2\alpha-1.` |
| 2833 | 23579-23581 | 0.38 | inline_safe | bracket | `\frac{(n-1)S^2}{\sigma^2}=\frac{9S^2}{16}\sim\chi^2(9).` |
| 2834 | 23583-23585 | 0.21 | inline_safe | bracket | `P(S^2 \geq a)=0.1,` |
| 2835 | 23587-23589 | 0.30 | inline_safe | bracket | `P\!\left(\frac{9}{16}S^2 \geq \frac{9}{16}a\right)=0.1.` |
| 2837 | 23606-23608 | 0.40 | inline_safe | bracket | `P(X\le x)=1-0.95-0.02=0.03.` |
| 2839 | 23636-23638 | 0.17 | inline_safe | bracket | `n\overline{X}\sim N(0,n),` |
| 2840 | 23642-23644 | 0.35 | inline_safe | bracket | `\sum_{i=1}^n X_i^2\sim \chi^2(n),` |
| 2841 | 23648-23650 | 0.23 | inline_safe | bracket | `\frac{\overline{X}-\mu}{S/\sqrt{n}}\sim t(n-1).` |
| 2842 | 23666-23668 | 0.35 | inline_safe | bracket | `\sum_{i=1}^{n}X_i^2 \sim \chi^2(n),` |
| 2843 | 23672-23674 | 0.43 | inline_safe | bracket | `\sum_{i=1}^{n-1}X_i^2 \sim \chi^2(n-1).` |
| 2847 | 23704-23706 | 0.39 | inline_safe | bracket | `X_1-X_2\sim N(0,1+1)=N(0,2).` |
| 2848 | 23708-23710 | 0.26 | inline_safe | bracket | `\frac{X_1-X_2}{\sqrt2}\sim N(0,1).` |
| 2851 | 23721-23723 | 0.26 | inline_safe | bracket | `\frac{X_1-X_2}{\sqrt2}\sim N(0,1).` |
| 2852 | 23725-23727 | 0.22 | inline_safe | bracket | `\sum_{i=3}^{n}X_i^2` |
| 2853 | 23729-23731 | 0.39 | inline_safe | bracket | `\sum_{i=3}^{n}X_i^2\sim\chi^2(n-2).` |
| 2855 | 23737-23740 | 0.45 | normalized_width_not_low | bracket | `\frac{(X_1-X_2)/\sqrt2}{\sqrt{\sum_{i=3}^{n}X_i^2/(n-2)}} =\sqrt{\frac{n-2}{2}}\cdot\frac{X_1-X_2}{\sqrt{\sum_{i=3}^{n}X_i^2}}.` |
| 2862 | 23852-23852 | 0.18 | inline_safe | bracket | `X_1, X_2, \dots, X_n` |
| 2863 | 23853-23853 | 0.23 | inline_safe | bracket | `\hat{\theta}(X_1, X_2, \dots, X_n)` |
| 2864 | 23854-23854 | 0.23 | inline_safe | bracket | `\hat{\theta}(x_1, x_2, \dots, x_n)` |
| 2865 | 23899-23905 | 0.16 | inline_unsafe_marker | bracket | `f(x)= \begin{cases} \dfrac{6x}{\theta^3}(\theta-x), & 0<x<\theta,\\ 0, & \text{其他}, \end{cases}` |
| 2871 | 23963-23969 | 0.13 | inline_unsafe_marker | bracket | `f(x)= \begin{cases} \dfrac{2x}{\alpha^2}, & 0\leq x\leq\alpha,\\ 0, & \text{其他}, \end{cases}` |
| 2874 | 23984-23986 | 0.32 | inline_safe | bracket | `\hat{\alpha}=\max\{X_1,X_2,\dots,X_n\}.` |
| 2875 | 23988-23990 | 0.42 | inline_safe | bracket | `\hat{p}=\frac{1}{\hat{\alpha}}=\frac{1}{\max\{X_1,X_2,\dots,X_n\}}.` |
| 2876 | 24008-24010 | 0.35 | inline_safe | bracket | `L(\theta)=\frac{1}{\theta^n}\cdot\mathbf{1}\{\theta\geq X_{(n)}\}.` |
| 2878 | 24033-24036 | 0.36 | normalized_width_not_low | bracket | `L(N)=\prod_{i=1}^n P\{X=x_i\} =\left(\frac1N\right)^n,` |
| 2879 | 24038-24040 | 0.35 | inline_safe | bracket | `N\ge \max\{x_1,\dots,x_n\}=x_{(n)}.` |
| 2880 | 24042-24044 | 0.36 | inline_safe | bracket | `\widehat N=X_{(n)}=\max\{X_1,\dots,X_n\}.` |
| 2882 | 24051-24053 | 0.11 | inline_safe | bracket | `\widehat N=239.` |
| 2884 | 24066-24068 | 0.34 | inline_safe | bracket | `L(\theta)=\left(\frac{1-\theta}{2}\right)^{\!3}\left(\frac{1+\theta}{4}\right)^{\!5}.` |
| 2886 | 24074-24078 | 0.42 | normalized_width_not_low | bracket | `\frac{\mathrm{d}}{\mathrm{d}\theta}\ln L(\theta)=-\frac{3}{1-\theta}+\frac{5}{1+\theta}=0 \implies -3(1+\theta)+5(1-\theta)=0 \implies \theta=\frac{1}{4}.` |
| 2887 | 24083-24089 | 0.13 | inline_unsafe_marker | bracket | `f(x)= \begin{cases} (1+\theta)x^\theta, & 0<x<1,\\ 0, & \text{其他}, \end{cases}` |
| 2893 | 24117-24119 | 0.17 | inline_safe | bracket | `E(X)=\frac{\theta+1}{\theta+2},` |
| 2894 | 24121-24125 | 0.39 | normalized_width_not_low | bracket | `\overline L=\frac1n\sum_{i=1}^n\ln X_i, \qquad \hat\theta_{\text{MLE}}=-1-\frac1{\overline L}.` |
| 2895 | 24127-24132 | 0.41 | normalized_width_not_low | bracket | `\widehat{E(X)}_{\text{MLE}} =\frac{\hat\theta_{\text{MLE}}+1}{\hat\theta_{\text{MLE}}+2} =\frac{1}{1-\overline L} =\frac{1}{1-\frac1n\sum_{i=1}^n\ln X_i}.` |
| 2897 | 24155-24157 | 0.08 | inline_safe | bracket | `\hat{\lambda}=1.` |
| 2899 | 24174-24176 | 0.35 | inline_safe | bracket | `\hat{\sigma}^2 = \frac{1}{n}\sum_{i=1}^{n}X_i^2.` |
| 2900 | 24183-24185 | 0.42 | inline_safe | bracket | `P(X=x; \theta)=h(x)c(\theta)\exp\{w(\theta)t(x)\},` |
| 2903 | 24194-24194 | 0.48 | display_environment | dollar | `-\frac{c'(\theta)}{c(\theta)w'(\theta)} = \frac{1}{n}\sum_{i=1}^n X_i = \overline{X}` |
| 2905 | 24196-24196 | 0.11 | display_environment | dollar | `E(X)=\overline{X}` |
| 2909 | 24226-24228 | 0.43 | inline_safe | bracket | `EX = 2\theta(1-\theta) + 2(1-\theta)^2 = 2-2\theta.` |
| 2917 | 24293-24295 | 0.25 | inline_safe | bracket | `\hat{\theta}_{\text{MLE}} = \frac{7-\sqrt{13}}{12}.` |
| 2918 | 24313-24315 | 0.46 | inline_safe | bracket | `EX = \theta^2 + \theta(1-\theta) + 3(1-\theta) = 3-2\theta.` |
| 2923 | 24342-24344 | 0.43 | inline_safe | bracket | `\ell'(p)=\frac{n}{p}-\frac{\sum_{i=1}^n x_i-n}{1-p}.` |
| 2924 | 24346-24348 | 0.41 | inline_safe | bracket | `n(1-p)=p\left(\sum_{i=1}^n x_i-n\right),` |
| 2925 | 24350-24352 | 0.26 | inline_safe | bracket | `n=p\sum_{i=1}^n x_i.` |
| 2926 | 24354-24356 | 0.39 | inline_safe | bracket | `\hat p=\frac{n}{\sum_{i=1}^n x_i}=\frac{1}{\overline X}.` |
| 2928 | 24362-24364 | 0.23 | inline_safe | bracket | `\boxed{\hat p=\dfrac1{\overline X}}.` |
| 2933 | 24396-24398 | 0.20 | inline_unsafe_marker | bracket | `f(x;\theta) = \begin{cases} \dfrac{1}{1-\theta}, & \theta \leq x \leq 1, \\[4pt] 0, & \text{其他}, \end{cases}` |
| 2935 | 24410-24412 | 0.37 | inline_safe | bracket | `\hat{\theta}_{\text{MLE}} = \min\{X_1, X_2, \dots, X_n\}.` |
| 2936 | 24417-24423 | 0.16 | inline_unsafe_marker | bracket | `f(x;\theta)= \begin{cases} \dfrac1{\|\theta\|}, & \theta<x<\theta+\|\theta\|,\\[6pt] 0, & \text{其他}. \end{cases}` |
| 2937 | 24430-24433 | 0.43 | normalized_width_not_low | bracket | `X_{(1)}=\min_{1\le i\le n}X_i,\qquad X_{(n)}=\max_{1\le i\le n}X_i.` |
| 2938 | 24436-24438 | 0.10 | inline_safe | bracket | `\theta<x<0.` |
| 2939 | 24440-24443 | 0.46 | normalized_width_not_low | bracket | `L(\theta)=\left(-\frac1\theta\right)^n \mathbf{1}\{\theta<X_{(1)},\ X_{(n)}<0\},\qquad \theta<0.` |
| 2940 | 24445-24447 | 0.37 | inline_safe | bracket | `\hat\theta=X_{(1)}=\min\{X_1,\dots,X_n\}.` |
| 2941 | 24450-24452 | 0.11 | inline_safe | bracket | `\theta<x<2\theta.` |
| 2942 | 24454-24456 | 0.35 | inline_safe | bracket | `\theta<X_{(1)},\qquad X_{(n)}<2\theta,` |
| 2943 | 24458-24460 | 0.27 | inline_safe | bracket | `\frac{X_{(n)}}2<\theta<X_{(1)}.` |
| 2944 | 24462-24465 | 0.31 | inline_safe | bracket | `L(\theta)=\theta^{-n} \mathbf{1}\left\{\frac{X_{(n)}}2<\theta<X_{(1)}\right\}.` |
| 2946 | 24474-24480 | 0.07 | inline_unsafe_marker | bracket | `\begin{array}{c\|ccc} X & -1 & 0 & 3\\ \hline P & \theta & 3\theta & 1-4\theta \end{array}` |
| 2948 | 24492-24494 | 0.22 | inline_safe | bracket | `\hat\theta_1=\frac{3-\overline X}{13}.` |
| 2949 | 24497-24500 | 0.41 | normalized_width_not_low | bracket | `L(\theta)=\theta^{r_1}(3\theta)^{r_2}(1-4\theta)^{r_3} =3^{r_2}\theta^{r_1+r_2}(1-4\theta)^{r_3}.` |
| 2951 | 24506-24508 | 0.41 | inline_safe | bracket | `\ell'(\theta)=\frac{r_1+r_2}{\theta}-\frac{4r_3}{1-4\theta}=0.` |
| 2952 | 24510-24513 | 0.24 | inline_safe | bracket | `\hat\theta_2=\frac{r_1+r_2}{4n} =\frac{1-r_3/n}{4}.` |
| 2953 | 24517-24520 | 0.26 | inline_safe | bracket | `E\hat\theta_1=\frac{3-E\overline X}{13} =\frac{3-(3-13\theta)}{13}=\theta,` |
| 2954 | 24524-24526 | 0.21 | inline_safe | bracket | `E\left(\frac{r_3}{n}\right)=1-4\theta.` |
| 2955 | 24528-24532 | 0.29 | normalized_width_not_low | bracket | `E\hat\theta_2 =E\left(\frac{1-r_3/n}{4}\right) =\frac{1-(1-4\theta)}4=\theta.` |
| 2956 | 24538-24544 | 0.07 | inline_unsafe_marker | bracket | `\begin{array}{c\|ccc} X & -1 & 1 & 2\\ \hline P & \theta & 2\theta & 1-3\theta \end{array}` |
| 2957 | 24552-24554 | 0.49 | inline_safe | bracket | `EX=(-1)\theta+1\cdot2\theta+2(1-3\theta)=2-5\theta.` |
| 2958 | 24556-24558 | 0.22 | inline_safe | bracket | `\hat\theta_1=\frac{2-\overline X}{5}.` |
| 2959 | 24561-24564 | 0.41 | normalized_width_not_low | bracket | `L(\theta)=\theta^{r_1}(2\theta)^{r_2}(1-3\theta)^{r_3} =2^{r_2}\theta^{r_1+r_2}(1-3\theta)^{r_3}.` |
| 2961 | 24570-24572 | 0.41 | inline_safe | bracket | `\ell'(\theta)=\frac{r_1+r_2}{\theta}-\frac{3r_3}{1-3\theta}=0.` |
| 2962 | 24574-24576 | 0.33 | inline_safe | bracket | `\hat\theta_2=\frac13\left(1-\frac{r_3}{n}\right).` |
| 2963 | 24580-24583 | 0.24 | inline_safe | bracket | `E\hat\theta_1=\frac{2-E\overline X}{5} =\frac{2-(2-5\theta)}{5}=\theta,` |
| 2964 | 24587-24589 | 0.21 | inline_safe | bracket | `E\left(\frac{r_3}{n}\right)=1-3\theta.` |
| 2965 | 24591-24595 | 0.33 | normalized_width_not_low | bracket | `E\hat\theta_2 =\frac13\left(1-E\frac{r_3}{n}\right) =\frac13\{1-(1-3\theta)\}=\theta.` |
| 2966 | 24601-24607 | 0.18 | inline_unsafe_marker | bracket | `f(x;\theta)= \begin{cases} 2e^{-2(x-\theta)}, & x>\theta,\\ 0, & x\le\theta, \end{cases}` |
| 2967 | 24615-24617 | 0.30 | inline_safe | bracket | `EX=\theta+EY=\theta+\frac12.` |
| 2968 | 24619-24621 | 0.24 | inline_safe | bracket | `\hat\theta=\overline X-\frac12.` |
| 2969 | 24624-24628 | 0.29 | normalized_width_not_low | bracket | `E\hat\theta=E\overline X-\frac12 =\left(\theta+\frac12\right)-\frac12 =\theta,` |
| 2970 | 24634-24640 | 0.14 | inline_unsafe_marker | bracket | `f(x;\theta)= \begin{cases} 2\theta e^{-2\theta x}, & x>0,\\ 0, & x\le0, \end{cases}` |
| 2971 | 24648-24651 | 0.42 | normalized_width_not_low | bracket | `L(\theta)=\prod_{i=1}^n 2\theta e^{-2\theta X_i} =(2\theta)^n\exp\left(-2\theta\sum_{i=1}^n X_i\right).` |
| 2972 | 24653-24655 | 0.44 | inline_safe | bracket | `\ell(\theta)=n\ln(2\theta)-2\theta\sum_{i=1}^n X_i.` |
| 2973 | 24657-24659 | 0.42 | inline_safe | bracket | `\ell'(\theta)=\frac{n}{\theta}-2\sum_{i=1}^n X_i=0,` |
| 2974 | 24661-24664 | 0.33 | normalized_width_not_low | bracket | `\hat\theta_1=\frac{n}{2\sum_{i=1}^n X_i} =\frac1{2\overline X}.` |
| 2975 | 24666-24668 | 0.17 | inline_safe | bracket | `EX=\frac1{2\theta}.` |
| 2976 | 24670-24672 | 0.24 | inline_safe | bracket | `\hat\theta_2=\frac1{2\overline X}.` |
| 2977 | 24675-24677 | 0.14 | inline_safe | bracket | `S\sim \Gamma(n,2\theta)` |
| 2978 | 24679-24681 | 0.24 | inline_safe | bracket | `E\left(\frac1S\right)=\frac{2\theta}{n-1}.` |
| 2979 | 24683-24688 | 0.23 | normalized_width_not_low | bracket | `E\hat\theta_1 =E\left(\frac{n}{2S}\right) =\frac n2\cdot\frac{2\theta}{n-1} =\frac{n}{n-1}\theta.` |
| 2980 | 24690-24692 | 0.16 | inline_safe | bracket | `\frac{n-1}{n}\hat\theta_1.` |
| 2983 | 24715-24717 | 0.44 | inline_safe | bracket | `F(t) = 1 - e^{-t^2/\theta^2}\quad(t \geq 0).` |
| 2986 | 24729-24731 | 0.48 | inline_safe | bracket | `\hat{Q} = Q(\hat{\theta}) = \frac{\hat{\theta}^2}{2}\ln\hat{\theta} - \frac{3}{4}\hat{\theta}^2 + \hat{\theta}.` |
| 2987 | 24743-24745 | 0.39 | inline_safe | bracket | `E\overline X=\mu,\qquad D\overline X=\frac{\sigma^2}{n}.` |
| 2988 | 24747-24750 | 0.33 | normalized_width_not_low | bracket | `E(\overline X^2)=D\overline X+(E\overline X)^2 =\frac{\sigma^2}{n}+\mu^2.` |
| 2989 | 24752-24754 | 0.18 | inline_safe | bracket | `E(\overline X^2)\ne \mu^2.` |
| 2990 | 24760-24767 | 0.20 | inline_unsafe_marker | bracket | `f(x)= \begin{cases} (\theta+1)(x-5)^\theta, & 5<x<6,\\ 0, & \text{其他}, \end{cases} \qquad \theta>0.` |
| 2991 | 24772-24777 | 0.35 | normalized_width_not_low | bracket | `E(X)=5+E(U) =5+\int_0^1 u(\theta+1)u^\theta\,\mathrm{d}u =5+\frac{\theta+1}{\theta+2} =6-\frac1{\theta+2}.` |
| 2992 | 24779-24781 | 0.25 | inline_safe | bracket | `\overline X=6-\frac1{\theta+2},` |
| 2993 | 24783-24785 | 0.31 | inline_safe | bracket | `\hat\theta_M=\frac1{6-\overline X}-2.` |
| 2994 | 24788-24790 | 0.49 | inline_safe | bracket | `L(\theta)=(\theta+1)^n\prod_{i=1}^n (X_i-5)^\theta.` |
| 2997 | 24800-24803 | 0.42 | inline_safe | bracket | `\hat\theta_L =-\frac{n}{\sum_{i=1}^n\ln(X_i-5)}-1.` |
| 2998 | 24805-24807 | 0.31 | inline_safe | bracket | `\ell''(\theta)=-\frac{n}{(\theta+1)^2}<0,` |
| 2999 | 24832-24836 | 0.33 | normalized_width_not_low | bracket | `E\sum_{i=1}^{n}(X_i-\mu)^2 =\sum_{i=1}^{n}E(X_i-\mu)^2 =n\sigma^2.` |
| 3000 | 24838-24842 | 0.44 | normalized_width_not_low | bracket | `E\hat\sigma_3^2 =E\left[\frac1n\sum_{i=1}^{n}(X_i-\mu)^2\right] =\sigma^2,` |
| 3002 | 24859-24862 | 0.28 | normalized_width_not_low | bracket | `ET=E\!\left(\overline{X}^2-\frac{1}{n}S^2\right) =E(\overline{X}^2)-\frac{1}{n}E(S^2).` |
| 3004 | 24869-24872 | 0.33 | normalized_width_not_low | bracket | `E(\overline{X}^2)=D(\overline{X})+[E(\overline{X})]^2 =\frac{\sigma^2}{n}+\mu^2.` |
| 3005 | 24874-24876 | 0.41 | inline_safe | bracket | `ET=\left(\frac{\sigma^2}{n}+\mu^2\right)-\frac{1}{n}\sigma^2=\mu^2.` |
| 3006 | 24889-24891 | 0.43 | inline_safe | bracket | `\hat \mu = a_1 X_1 + a_2 X_2 + \dots + a_n X_n` |
| 3007 | 24893-24895 | 0.43 | inline_safe | bracket | `\hat\mu \text{ 是 } \mu \text{ 的无偏估计} \iff a_1+a_2+\dots+a_n=1` |
| 3009 | 24913-24915 | 0.39 | inline_safe | bracket | `\hat\mu=a_1X_1+a_2X_2+a_3X_3` |
| 3010 | 24933-24935 | 0.43 | inline_safe | bracket | `\widehat\mu=\frac14X_1+aX_2+\frac12X_3` |
| 3011 | 24940-24943 | 0.32 | inline_safe | bracket | `E\widehat\mu =\left(\frac14+a+\frac12\right)\mu.` |
| 3012 | 24945-24947 | 0.30 | inline_safe | bracket | `\frac14+a+\frac12=1.` |
| 3013 | 24949-24951 | 0.14 | inline_safe | bracket | `a=\frac14.` |
| 3014 | 24961-24963 | 0.13 | inline_safe | bracket | `E(c\overline{X})=\theta.` |
| 3015 | 24967-24969 | 0.44 | inline_safe | bracket | `f(x;\theta)=\frac{3x^2}{\theta^3},\qquad 0\le x\le \theta,` |
| 3016 | 24971-24976 | 0.34 | normalized_width_not_low | bracket | `EX=\int_0^\theta x\cdot \frac{3x^2}{\theta^3}\,\mathrm dx =\frac{3}{\theta^3}\int_0^\theta x^3\,\mathrm dx =\frac{3}{\theta^3}\cdot\frac{\theta^4}{4} =\frac{3\theta}{4}.` |
| 3017 | 24979-24981 | 0.33 | inline_safe | bracket | `E(c\overline{X})=cE(\overline{X})=c\cdot\frac{3\theta}{4}.` |
| 3018 | 24983-24985 | 0.28 | inline_safe | bracket | `c\cdot\frac{3\theta}{4}=\theta\implies c=\frac{4}{3}.` |
| 3019 | 24992-24994 | 0.26 | inline_unsafe_marker | bracket | `f(x,\theta) = \begin{cases} \dfrac{1}{\theta}\,e^{-x/\theta}, & x > 0\ (\theta > 0), \\ 0, & x \leq 0, \end{cases}` |
| 3021 | 25007-25009 | 0.46 | inline_safe | bracket | `\ln L(\theta)=-n\ln\theta-\frac{1}{\theta}\sum_{i=1}^n X_i.` |
| 3022 | 25012-25015 | 0.39 | inline_safe | bracket | `\frac{\mathrm{d}\ln L}{\mathrm{d}\theta} =-\frac{n}{\theta}+\frac{1}{\theta^2}\sum_{i=1}^n X_i.` |
| 3023 | 25017-25021 | 0.39 | normalized_width_not_low | bracket | `-\frac{n}{\theta}+\frac{1}{\theta^2}\sum_{i=1}^n X_i=0 \quad\Longrightarrow\quad \hat{\theta}=\frac{1}{n}\sum_{i=1}^n X_i=\overline{X}.` |
| 3024 | 25024-25027 | 0.39 | normalized_width_not_low | bracket | `\frac{\mathrm{d}^2\ln L}{\mathrm{d}\theta^2} =\frac{n}{\theta^2}-\frac{2}{\theta^3}\sum_{i=1}^n X_i.` |
| 3025 | 25029-25033 | 0.22 | normalized_width_not_low | bracket | `\left.\frac{\mathrm{d}^2\ln L}{\mathrm{d}\theta^2}\right\|_{\theta=\overline{X}} =\frac{n}{\overline{X}^2}-\frac{2n\overline{X}}{\overline{X}^3} =-\frac{n}{\overline{X}^2}<0,` |
| 3026 | 25037-25039 | 0.08 | inline_safe | bracket | `EX=\theta,` |
| 3028 | 25051-25053 | 0.46 | inline_safe | bracket | `D = k\sum_{i=1}^{n-1}(X_{i+1}-X_i)^2` |
| 3029 | 25060-25062 | 0.33 | inline_safe | bracket | `E(X_{i+1}-X_i)=\mu-\mu=0,` |
| 3032 | 25074-25079 | 0.48 | normalized_width_not_low | bracket | `ED =k\sum_{i=1}^{n-1}E\bigl[(X_{i+1}-X_i)^2\bigr] =k(n-1)\cdot 2\sigma^2 =2k(n-1)\sigma^2.` |
| 3034 | 25100-25102 | 0.46 | inline_safe | bracket | `f = (2\pi\sigma^2)^{-(m+n)/2}\,\exp\!\left\{-\frac{T}{2\sigma^2}\right\}.` |
| 3036 | 25108-25110 | 0.35 | inline_safe | bracket | `E(\hat{\sigma}^2) = \frac{(m+n)\sigma^2}{m+n} = \sigma^2.` |
| 3037 | 25116-25118 | 0.27 | inline_unsafe_marker | bracket | `F(x,\alpha,\beta) = \begin{cases} 1-\left(\dfrac{\alpha}{x}\right)^{\!\beta}, & x > \alpha, \\ 0, & x \leq \alpha, \end{cases}` |
| 3040 | 25145-25147 | 0.35 | inline_safe | bracket | `\hat{\theta}_2 = \max\{X_1, X_2, \dots, X_n\}.` |
| 3042 | 25154-25159 | 0.32 | display_environment | dollar | `F_X(x) = \begin{cases} 0, & x<0 \\ \displaystyle \int_{0}^{x} \frac{3t^2}{\theta^3} dt = \frac{x^3}{\theta^3}, & 0\leq x\leq\theta \\ 1, & x>\theta \end{cases}` |
| 3044 | 25163-25163 | 0.48 | display_environment | dollar | `f_{\hat{\theta}_2}(x) = F'_{\hat{\theta}_2}(x) =\begin{cases}\displaystyle \frac{3n x^{3n-1}}{\theta^{3n}}, & 0\leq x\leq\theta \\0, & \text{其他}\end{cases}` |
| 3046 | 25178-25180 | 0.32 | inline_unsafe_marker | bracket | `f_X(x,\theta) = \begin{cases} 4\,e^{-4(x-\theta)}, & x \geq \theta, \\ 0, & \text{其他}, \end{cases}` |
| 3048 | 25189-25189 | 0.40 | display_environment | dollar | `\hat{\theta} = X_{(1)} = \min\{X_1,X_2,\dots,X_n\}` |
| 3050 | 25194-25194 | 0.39 | display_environment | dollar | `X_{(1)} - \theta = \min\{Y_1,Y_2,\dots,Y_n\}` |
| 3052 | 25198-25198 | 0.20 | display_environment | dollar | `E\left(\min Y_i\right) = \frac{1}{4n}` |
| 3054 | 25204-25206 | 0.33 | display_environment | dollar | `\hat{\theta}_{\text{unbiased}} = X_{(1)} - \frac{1}{4n}` |
| 3056 | 25225-25227 | 0.46 | inline_safe | bracket | `S^2=\frac{1}{n-1}\sum_{i=1}^n (X_i-\overline{X})^2.` |
| 3057 | 25229-25232 | 0.49 | normalized_width_not_low | bracket | `\sum_{i=1}^n (X_i-\overline{X})^2 =\sum_{i=1}^n (X_i-\mu)^2-n(\overline{X}-\mu)^2.` |
| 3059 | 25239-25241 | 0.34 | inline_safe | bracket | `E(\overline{X}-\mu)^2=D(\overline{X})=\frac{\sigma^2}{n},` |
| 3060 | 25243-25246 | 0.39 | normalized_width_not_low | bracket | `E\!\left[\sum_{i=1}^n (X_i-\overline{X})^2\right] =n\sigma^2-n\cdot\frac{\sigma^2}{n}=(n-1)\sigma^2.` |
| 3063 | 25268-25270 | 0.31 | inline_safe | bracket | `E(S_X^2+S_Y^2)=2\sigma^2,` |
| 3065 | 25274-25276 | 0.38 | inline_safe | bracket | `E\!\left(\frac{S_X^2+S_Y^2}{m+n-2}\right)=\frac{2\sigma^2}{m+n-2},` |
| 3066 | 25277-25280 | 0.38 | normalized_width_not_low | bracket | `E\!\left(\frac{(m-1)S_X^2+(n-1)S_Y^2}{m+n-2}\right) =\frac{(m-1)\sigma^2+(n-1)\sigma^2}{m+n-2}.` |
| 3068 | 25301-25303 | 0.33 | inline_safe | bracket | `E(X)=\lambda,\qquad D(X)=\lambda.` |
| 3069 | 25305-25307 | 0.41 | inline_safe | bracket | `E(\overline{X})=\frac{1}{n}\sum_{i=1}^n E(X_i)=\lambda,` |
| 3070 | 25311-25313 | 0.21 | inline_safe | bracket | `E(S^2)=D(X)=\lambda.` |
| 3071 | 25329-25331 | 0.28 | inline_safe | bracket | `EX=\lambda,\qquad DX=\lambda.` |
| 3072 | 25333-25335 | 0.38 | inline_safe | bracket | `E(\overline{X})=\lambda,\qquad D(\overline{X})=\frac{\lambda}{n}.` |
| 3073 | 25338-25341 | 0.33 | inline_safe | bracket | `E(\overline{X}^2)=D(\overline{X})+[E(\overline{X})]^2 =\frac{\lambda}{n}+\lambda^2.` |
| 3074 | 25344-25346 | 0.30 | inline_safe | bracket | `E\!\left(\frac{1}{n}\overline{X}\right)=\frac{1}{n}E(\overline{X})=\frac{\lambda}{n},` |
| 3075 | 25348-25352 | 0.22 | inline_safe | bracket | `E\!\left(\overline{X}^2-\frac{1}{n}\overline{X}\right) =\left(\frac{\lambda}{n}+\lambda^2\right)-\frac{\lambda}{n} =\lambda^2.` |
| 3076 | 25355-25357 | 0.15 | inline_safe | bracket | `\overline{X}^2-\frac{1}{n}\overline{X}` |
| 3077 | 25362-25362 | 0.28 | inline_safe | bracket | `X_{(n)} = \max(X_1, \dots, X_n)` |
| 3079 | 25368-25368 | 0.48 | display_environment | dollar | `f_{X_{(n)}}(x) = \frac{n}{\theta^n}x^{n-1} \quad (0 < x < \theta)` |
| 3081 | 25369-25369 | 0.46 | display_environment | dollar | `E\left(\frac{n+1}{n}X_{(n)}\right) = \frac{n+1}{n} \cdot \frac{n}{n+1}\theta = \theta` |
| 3082 | 25387-25391 | 0.46 | normalized_width_not_low | bracket | `\hat{\mu}_1 = \frac{1}{5}X_1 + \frac{3}{10}X_2 + \frac{1}{2}X_3,\quad \hat{\mu}_2 = \frac{1}{3}X_1 + \frac{1}{4}X_2 + \frac{5}{12}X_3,\quad \hat{\mu}_3 = \frac{1}{3}X_1 + \frac{...` |
| 3083 | 25399-25403 | 0.34 | inline_safe | bracket | `E\hat{\mu}_1 =\left(\frac15+\frac{3}{10}+\frac12\right)\mu =\mu.` |
| 3084 | 25406-25410 | 0.34 | inline_safe | bracket | `E\hat{\mu}_2 =\left(\frac13+\frac14+\frac{5}{12}\right)\mu =\mu.` |
| 3085 | 25413-25417 | 0.38 | normalized_width_not_low | bracket | `E\hat{\mu}_3 =\left(\frac13+\frac16+\frac12\right)\mu =\mu.` |
| 3089 | 25443-25447 | 0.29 | normalized_width_not_low | bracket | `\frac{38}{100}=0.380,\qquad \frac{50}{144}\approx 0.347,\qquad \frac{14}{36}\approx 0.389.` |
| 3090 | 25449-25451 | 0.23 | inline_safe | bracket | `\frac{50}{144}<\frac{38}{100}<\frac{14}{36}.` |
| 3091 | 25471-25475 | 0.40 | normalized_width_not_low | bracket | `D\mu_2=D\!\left(\frac23X_1+\frac13X_2\right) =\left(\frac23\right)^2+\left(\frac13\right)^2 =\frac59.` |
| 3092 | 25478-25482 | 0.39 | normalized_width_not_low | bracket | `D\mu_3=\left(\frac14\right)^2+\left(\frac34\right)^2 =\frac{1}{16}+\frac{9}{16} =\frac58.` |
| 3094 | 25490-25492 | 0.35 | inline_safe | bracket | `\frac12<\frac59<\frac58<1.` |
| 3095 | 25504-25506 | 0.35 | inline_safe | bracket | `EX=\frac{\theta}{2},\qquad DX=\frac{\theta^2}{12}.` |
| 3096 | 25511-25513 | 0.33 | inline_safe | bracket | `E(\hat{\theta}_1)=E(2\overline{X})=2EX=\theta,` |
| 3097 | 25514-25516 | 0.40 | inline_safe | bracket | `E(\hat{\theta}_2)=E(X_1+X_2)=2EX=\theta,` |
| 3099 | 25521-25525 | 0.41 | normalized_width_not_low | bracket | `D\hat{\theta}_1 = 4D(\overline{X}) = \frac{4\theta^2}{12\cdot3} = \frac{\theta^2}{9}, \quad D\hat{\theta}_2 = 2\cdot\frac{\theta^2}{12} = \frac{\theta^2}{6},` |
| 3101 | 25529-25531 | 0.26 | inline_safe | bracket | `\frac{\theta^2}{9}<\frac{3\theta^2}{25}<\frac{\theta^2}{6}.` |
| 3102 | 25538-25544 | 0.11 | inline_unsafe_marker | bracket | `f(x;\theta)= \begin{cases} \dfrac1\theta, & 0<x<\theta,\\ 0, & \text{其它}. \end{cases}` |
| 3103 | 25549-25552 | 0.49 | normalized_width_not_low | bracket | `L(\theta)=\prod_{i=1}^n \frac1\theta \mathbf 1_{(0,\theta)}(X_i) =\theta^{-n}\mathbf 1_{\{\theta\ge X_{(n)}\}},` |
| 3104 | 25554-25556 | 0.18 | inline_safe | bracket | `\hat\theta_1=X_{(n)}.` |
| 3105 | 25558-25560 | 0.17 | inline_safe | bracket | `\hat\theta_2=2\overline X.` |
| 3106 | 25562-25564 | 0.36 | inline_safe | bracket | `E(\hat\theta_2)=2E(\overline X)=2EX=\theta,` |
| 3107 | 25568-25570 | 0.37 | inline_safe | bracket | `E(\hat\theta_1)=E(X_{(n)})=\frac{n}{n+1}\theta,` |
| 3108 | 25597-25601 | 0.44 | normalized_width_not_low | bracket | `EX^2 =\frac{1}{2\theta}\int_{-\infty}^{+\infty}x^2e^{-\|x\|/\theta}\,\mathrm{d}x =\frac1\theta\int_0^\infty x^2e^{-x/\theta}\,\mathrm{d}x.` |
| 3109 | 25603-25607 | 0.33 | inline_safe | bracket | `EX^2 =\theta^2\int_0^\infty t^2e^{-t}\,\mathrm{d}t =2\theta^2.` |
| 3110 | 25609-25611 | 0.40 | inline_safe | bracket | `2\theta^2=\frac1n\sum_{i=1}^{n}X_i^2,` |
| 3111 | 25613-25615 | 0.40 | inline_safe | bracket | `\hat{\theta}_M=\sqrt{\frac{1}{2n}\sum_{i=1}^{n}X_i^2}.` |
| 3112 | 25618-25621 | 0.43 | normalized_width_not_low | bracket | `L(\theta)=\prod_{i=1}^{n}\frac{1}{2\theta}e^{-\|X_i\|/\theta} =(2\theta)^{-n}e^{-\sum\|X_i\|/\theta}.` |
| 3114 | 25627-25630 | 0.46 | normalized_width_not_low | bracket | `\frac{\mathrm d}{\mathrm d\theta}\ln L(\theta) =-\frac{n}{\theta}+\frac{1}{\theta^2}\sum_{i=1}^{n}\|X_i\|=0,` |
| 3115 | 25632-25634 | 0.35 | inline_safe | bracket | `\hat{\theta}_L=\frac{1}{n}\sum_{i=1}^{n}\|X_i\|.` |
| 3116 | 25637-25641 | 0.44 | normalized_width_not_low | bracket | `E\|X\| =\frac{1}{2\theta}\int_{-\infty}^{+\infty}\|x\|e^{-\|x\|/\theta}\,\mathrm{d}x =\frac{1}{\theta}\int_0^\infty xe^{-x/\theta}\,\mathrm{d}x.` |
| 3117 | 25643-25645 | 0.48 | inline_safe | bracket | `E\|X\|=\theta\int_0^\infty te^{-t}\,\mathrm{d}t=\theta\,\Gamma(2)=\theta.` |
| 3119 | 25653-25655 | 0.37 | inline_safe | bracket | `\hat{\theta}_L = \frac{1}{n}\sum\|X_i\| \xrightarrow{P} E\|X\| = \theta.` |
| 3121 | 25669-25671 | 0.08 | inline_safe | bracket | `EX=0,` |
| 3122 | 25673-25677 | 0.44 | normalized_width_not_low | bracket | `EX^2 =\frac{1}{2\theta}\int_{-\infty}^{+\infty}x^2e^{-\|x\|/\theta}\,\mathrm{d}x =\frac{1}{\theta}\int_0^\infty x^2e^{-x/\theta}\,\mathrm{d}x.` |
| 3123 | 25679-25683 | 0.38 | normalized_width_not_low | bracket | `EX^2 =\frac{1}{\theta}\int_0^\infty \theta^2t^2e^{-t}\theta\,\mathrm{d}t =\theta^2\Gamma(3)=2\theta^2.` |
| 3124 | 25685-25687 | 0.40 | inline_safe | bracket | `2\theta^2=\frac1n\sum_{i=1}^n X_i^2,` |
| 3125 | 25689-25691 | 0.41 | inline_safe | bracket | `\hat\theta_M=\sqrt{\frac{1}{2n}\sum_{i=1}^n X_i^2}.` |
| 3126 | 25696-25698 | 0.37 | inline_safe | bracket | `Y = \frac{2}{n(n+1)}\sum_{i=1}^{n}iX_i` |
| 3130 | 25721-25723 | 0.26 | inline_safe | bracket | `\mathrm{MSE}(\hat{\theta}) = E(\hat{\theta} - \theta)^2` |
| 3133 | 25760-25762 | 0.18 | inline_unsafe_marker | bracket | `f(x) = \begin{cases} e^{\theta-x}, & x > \theta, \\ 0, & x \leq \theta, \end{cases}` |
| 3134 | 25772-25774 | 0.38 | inline_safe | bracket | `\mathrm{MSE}_L = \left(\frac{1}{n}\right)^{\!2} + \frac{1}{n^2} = \frac{2}{n^2}.` |
| 3135 | 25780-25787 | 0.18 | inline_unsafe_marker | bracket | `f(x;\theta)= \begin{cases} 2e^{-2(x-\theta)}, & x>\theta,\\ 0, & x\le\theta, \end{cases} \qquad \theta>0.` |
| 3136 | 25796-25799 | 0.40 | normalized_width_not_low | bracket | `F(x)=\int_{\theta}^{x}2e^{-2(t-\theta)}\,\mathrm dt =1-e^{-2(x-\theta)}.` |
| 3137 | 25801-25807 | 0.21 | inline_unsafe_marker | bracket | `F(x)= \begin{cases} 0, & x\le\theta,\\ 1-e^{-2(x-\theta)}, & x>\theta. \end{cases}` |
| 3138 | 25810-25818 | 0.31 | inline_unsafe_marker | bracket | `\begin{aligned} F_{X_{(1)}}(x) &=P\{X_{(1)}\le x\}\\ &=1-P\{X_1>x,\dots,X_n>x\}\\ &=1-[1-F(x)]^n =1-e^{-2n(x-\theta)}. \end{aligned}` |
| 3139 | 25820-25826 | 0.22 | inline_unsafe_marker | bracket | `F_{\hat\theta}(x)= \begin{cases} 0, & x\le\theta,\\ 1-e^{-2n(x-\theta)}, & x>\theta. \end{cases}` |
| 3140 | 25829-25831 | 0.24 | inline_safe | bracket | `E\hat\theta=\theta+\frac1{2n}.` |
| 3142 | 25871-25877 | 0.11 | inline_unsafe_marker | bracket | `\begin{array}{c\|ccc} X & 1 & 2 & 3\\ \hline P & \theta^2 & 2\theta(1-\theta) & (1-\theta)^2 \end{array}` |
| 3143 | 25879-25881 | 0.30 | inline_safe | bracket | `(x_1,x_2,x_3)=(1,2,1),` |
| 3144 | 25886-25889 | 0.39 | normalized_width_not_low | bracket | `L(\theta)=(\theta^2)^2\cdot[2\theta(1-\theta)] =2\theta^5(1-\theta),\qquad 0<\theta<1.` |
| 3145 | 25891-25893 | 0.39 | inline_safe | bracket | `\ln L(\theta)=\ln2+5\ln\theta+\ln(1-\theta).` |
| 3146 | 25895-25897 | 0.20 | inline_safe | bracket | `\frac{5}{\theta}-\frac{1}{1-\theta}=0.` |
| 3147 | 25899-25901 | 0.15 | inline_safe | bracket | `5(1-\theta)=\theta,` |
| 3148 | 25903-25905 | 0.17 | inline_safe | bracket | `\hat\theta=\frac56.` |
| 3152 | 25928-25930 | 0.40 | inline_safe | bracket | `\frac1n\sum_{i=1}^{n}X_i^2=2\theta^2,` |
| 3153 | 25932-25934 | 0.46 | inline_safe | bracket | `\hat\theta_M=\sqrt{\frac1{2n}\sum_{i=1}^{n}X_i^2}.` |
| 3156 | 25947-25949 | 0.49 | inline_safe | bracket | `\ell'(\theta)=-\frac n\theta+\frac{\sum_{i=1}^{n}\|X_i\|}{\theta^2}.` |
| 3157 | 25951-25953 | 0.41 | inline_safe | bracket | `\hat\theta_L=\frac1n\sum_{i=1}^{n}\|X_i\|.` |
| 3158 | 25959-25961 | 0.30 | inline_safe | bracket | `k\sum_{i=1}^{n}\|X_i-\overline X\|` |
| 3159 | 25966-25968 | 0.20 | inline_safe | bracket | `Y_i=X_i-\overline X.` |
| 3160 | 25970-25972 | 0.11 | inline_safe | bracket | `EY_i=0.` |
| 3161 | 25974-25977 | 0.39 | normalized_width_not_low | bracket | `D(Y_i)=D(X_i-\overline X) =DX_i+D\overline X-2\operatorname{Cov}(X_i,\overline X).` |
| 3162 | 25979-25981 | 0.42 | inline_safe | bracket | `DX_i=\sigma^2,\qquad D\overline X=\frac{\sigma^2}{n},` |
| 3163 | 25982-25986 | 0.43 | normalized_width_not_low | bracket | `\operatorname{Cov}(X_i,\overline X) =\operatorname{Cov}\left(X_i,\frac1n\sum_{j=1}^n X_j\right) =\frac{\sigma^2}{n}.` |
| 3164 | 25988-25991 | 0.35 | normalized_width_not_low | bracket | `D(Y_i)=\sigma^2+\frac{\sigma^2}{n}-2\frac{\sigma^2}{n} =\frac{n-1}{n}\sigma^2.` |
| 3165 | 25993-25995 | 0.27 | inline_safe | bracket | `Y_i\sim N\left(0,\frac{n-1}{n}\sigma^2\right).` |
| 3166 | 25997-25999 | 0.22 | inline_safe | bracket | `E\|Z\|=\tau\sqrt{\frac2\pi}.` |
| 3167 | 26001-26004 | 0.28 | inline_safe | bracket | `E\|X_i-\overline X\| =\sigma\sqrt{\frac{n-1}{n}}\sqrt{\frac2\pi}.` |
| 3168 | 26006-26009 | 0.34 | normalized_width_not_low | bracket | `E\left[k\sum_{i=1}^{n}\|X_i-\overline X\|\right] =kn\sigma\sqrt{\frac{n-1}{n}}\sqrt{\frac2\pi}.` |
| 3169 | 26011-26014 | 0.30 | normalized_width_not_low | bracket | `k=\frac1{n}\sqrt{\frac{n}{n-1}}\sqrt{\frac{\pi}{2}} =\sqrt{\frac{\pi}{2n(n-1)}}.` |
| 3172 | 26114-26116 | 0.25 | display_environment | env:equation | `P\{\underline{\theta}<\theta<\overline{\theta}\} \ge 1-\alpha` |
| 3173 | 26220-26222 | 0.20 | inline_safe | bracket | `\overline{X}\sim N\!\left(\mu,\frac{\sigma^2}{n}\right).` |
| 3174 | 26224-26226 | 0.26 | inline_safe | bracket | `W=\frac{\overline{X}-\mu}{\sigma/\sqrt{n}}\sim N(0,1).` |
| 3175 | 26230-26232 | 0.45 | inline_safe | bracket | `P\left\{-z_{\alpha/2}<\frac{\overline{X}-\mu}{\sigma/\sqrt{n}}<z_{\alpha/2}\right\}=1-\alpha.` |
| 3177 | 26240-26242 | 0.45 | inline_safe | bracket | `\left(\overline{X}-\frac{\sigma}{\sqrt{n}}z_{\alpha/2},\ \overline{X}+\frac{\sigma}{\sqrt{n}}z_{\alpha/2}\right).` |
| 3178 | 26256-26258 | 0.37 | inline_safe | bracket | `T=\frac{\overline X-\mu}{S/\sqrt n}\sim t(n-1)=t(8).` |
| 3179 | 26260-26262 | 0.34 | inline_safe | bracket | `P\left\{T\ge -t_{0.05}(8)\right\}=0.95,` |
| 3180 | 26264-26266 | 0.44 | inline_safe | bracket | `P\left\{\mu\le \overline X+t_{0.05}(8)\frac{S}{\sqrt n}\right\}=0.95.` |
| 3181 | 26268-26271 | 0.31 | inline_safe | bracket | `U=6+1.8595\cdot\frac{\sqrt{0.33}}{3} \approx 6.356.` |
| 3182 | 26284-26286 | 0.38 | inline_safe | bracket | `b=EX=E(e^Y)=e^{\mu+\frac12}.` |
| 3183 | 26289-26291 | 0.24 | inline_safe | bracket | `\overline Y\sim N\left(\mu,\frac14\right).` |
| 3185 | 26299-26302 | 0.34 | normalized_width_not_low | bracket | `\left(\overline y-\frac{1.96}{2},\ \overline y+\frac{1.96}{2}\right) =(-0.98,\ 0.98).` |
| 3186 | 26305-26309 | 0.32 | normalized_width_not_low | bracket | `-0.98<\mu<0.98 \quad\Longrightarrow\quad -0.48<\mu+\frac12<1.48.` |
| 3187 | 26311-26313 | 0.25 | inline_safe | bracket | `\left(e^{-0.48},\ e^{1.48}\right).` |
| 3188 | 26321-26323 | 0.32 | inline_safe | bracket | `P\{\|\overline X-\mu\|\le20\}\ge0.95.` |
| 3189 | 26325-26327 | 0.23 | inline_safe | bracket | `\frac{\overline X-\mu}{\sigma/\sqrt n}\sim N(0,1),` |
| 3190 | 26329-26332 | 0.23 | inline_safe | bracket | `P\{\|\overline X-\mu\|\le20\} =2\Phi\left(\frac{20\sqrt n}{100}\right)-1.` |
| 3191 | 26334-26336 | 0.32 | inline_safe | bracket | `\frac{20\sqrt n}{100}\ge z_{0.025}=1.96.` |
| 3192 | 26338-26340 | 0.36 | inline_safe | bracket | `n\ge\left(\frac{1.96\times100}{20}\right)^2=96.04.` |
| 3193 | 26349-26352 | 0.23 | inline_safe | bracket | `P\{\|\overline X-\mu\|\le80\} =2\Phi\left(\frac{80\sqrt n}{200}\right)-1.` |
| 3194 | 26354-26356 | 0.19 | inline_safe | bracket | `\frac{80\sqrt n}{200}\ge1.96.` |
| 3195 | 26358-26360 | 0.36 | inline_safe | bracket | `n\ge\left(\frac{1.96\times200}{80}\right)^2=24.01.` |
| 3196 | 26372-26374 | 0.10 | inline_safe | bracket | `\frac{\overline{X}-\mu}{\sigma/\sqrt{n}}.` |
| 3197 | 26378-26380 | 0.28 | inline_safe | bracket | `W=\frac{\overline{X}-\mu}{S/\sqrt{n}}\sim t(n-1).` |
| 3201 | 26411-26413 | 0.36 | inline_safe | bracket | `W=\frac{(n-1)S^2}{\sigma^2}\sim\chi^2(n-1).` |
| 3205 | 26444-26446 | 0.10 | inline_safe | bracket | `\overline{X}-\overline{Y}.` |
| 3210 | 26480-26484 | 0.27 | normalized_width_not_low | bracket | `\frac{S_1^2/\sigma_1^2}{S_2^2/\sigma_2^2} =\frac{S_1^2}{S_2^2}\cdot\frac{\sigma_2^2}{\sigma_1^2} \sim F(n_1-1,n_2-1).` |
| 3214 | 26504-26507 | 0.46 | normalized_width_not_low | bracket | `\left(\frac{S_1^2}{S_2^2}\cdot\frac{1}{F_{\alpha/2}(n_1-1,n_2-1)},\ \frac{S_1^2}{S_2^2}\cdot F_{\alpha/2}(n_2-1,n_1-1)\right).` |
| 3215 | 26522-26524 | 0.42 | display_environment | env:equation* | `\frac{X_i-\mu}{\sigma} \sim N(0,1), \quad i=1,2,\dots,n` |
| 3222 | 26568-26571 | 0.43 | display_environment | env:align* | `E(\overline{X}-\overline{Y}) &= E(\overline{X}) - E(\overline{Y}) = \mu_1 - \mu_2 \\ D(\overline{X}-\overline{Y}) &= D(\overline{X}) + D(\overline{Y}) = \frac{\sigma_1^2}{n_1} +...` |
| 3224 | 26578-26580 | 0.45 | display_environment | env:equation* | `W = \frac{(\overline{X}-\overline{Y}) - (\mu_1-\mu_2)}{\sqrt{\frac{\sigma_1^2}{n_1} + \frac{\sigma_2^2}{n_2}}} \sim N(0,1)` |
| 3236 | 26663-26665 | 0.43 | display_environment | env:equation* | `\left( \overline{X} - \frac{\sigma}{\sqrt{n}} z_{\alpha/2},\ \overline{X} + \frac{\sigma}{\sqrt{n}} z_{\alpha/2} \right)` |
| 3237 | 26667-26669 | 0.20 | inline_safe | bracket | `L = 2\frac{\sigma}{\sqrt{n}} z_{\alpha/2}.` |
| 3238 | 26681-26683 | 0.44 | display_environment | env:equation* | `Z = \frac{\overline{X}-\mu}{\sigma/\sqrt{n}} = \frac{\overline{X}-\mu}{1/\sqrt{100}} \stackrel{\text{近似}}{\sim} N(0,1)` |
| 3239 | 26687-26689 | 0.44 | display_environment | env:equation* | `\left( \overline{X} - \frac{1}{10} \times 1.96,\ \overline{X} + \frac{1}{10} \times 1.96 \right)` |
| 3240 | 26702-26704 | 0.25 | display_environment | env:equation* | `L = 2 \cdot \frac{\sigma}{\sqrt{n}} z_{0.025}` |
| 3243 | 26723-26725 | 0.31 | display_environment | env:equation* | `\frac{1.73}{5} \times 2.0639 \approx 0.7141` |
| 3244 | 26736-26738 | 0.42 | display_environment | env:equation* | `\left( \frac{(n-1)S^2}{\chi^2_{0.025}(9)},\ \frac{(n-1)S^2}{\chi^2_{0.975}(9)} \right)` |
| 3245 | 26740-26742 | 0.49 | display_environment | env:equation* | `\frac{18}{19.023} \approx 0.9462,\quad \frac{18}{2.70} \approx 6.6667` |
| 3246 | 26754-26756 | 0.22 | inline_safe | bracket | `P\{\mu \ge \underline{\mu}\}=0.95.` |
| 3247 | 26758-26760 | 0.33 | display_environment | env:equation* | `P\left( \frac{\overline{X}-\mu}{\sigma/\sqrt{n}} \le z_{0.05} \right) = 0.95` |
| 3248 | 26762-26764 | 0.38 | display_environment | env:equation* | `\underline{\mu} = 6 - 1.645 \frac{\sigma}{3} \approx 6 - 0.5483\sigma` |
| 3249 | 26772-26774 | 0.21 | inline_safe | bracket | `P\{\theta>\underline{\theta}\}\ge 1-\alpha.` |
| 3250 | 26779-26781 | 0.21 | inline_safe | bracket | `P\{\theta>\underline{\theta}\}\ge 1-\alpha.` |
| 3251 | 26783-26785 | 0.20 | inline_safe | bracket | `P\{\theta>\underline{\theta}\}=1-\alpha,` |
| 3253 | 26803-26805 | 0.26 | inline_safe | bracket | `Z=\frac{\overline{X}-\mu}{\sigma/\sqrt{n}}\sim N(0,1).` |
| 3254 | 26807-26811 | 0.45 | normalized_width_not_low | bracket | `\overline{x} =\frac{1820+1834+1831+1816+1824}{5} =\frac{9125}{5}=1825.` |
| 3255 | 26813-26818 | 0.19 | structural | bracket | `\left( \overline{x}-1.96\frac{\sigma}{\sqrt n}, \overline{x}+1.96\frac{\sigma}{\sqrt n} \right).` |
| 3256 | 26820-26822 | 0.22 | inline_safe | bracket | `1.96\frac{10}{\sqrt5}\approx 8.77.` |
| 3258 | 26828-26830 | 0.25 | inline_safe | bracket | `[1816.23,\ 1833.77].` |
| 3259 | 26839-26841 | 0.44 | display_environment | env:equation* | `\overline{X} = \frac{1}{n}\sum_{i=1}^9 X_i = \frac{198}{9} = 22` |
| 3263 | 26869-26871 | 0.26 | inline_safe | bracket | `\hat p=\frac{175}{400}=0.4375.` |
| 3265 | 26877-26879 | 0.38 | inline_safe | bracket | `\sqrt{\frac{0.4375\times0.5625}{400}}\approx0.0248,` |
| 3267 | 26892-26894 | 0.27 | inline_safe | bracket | `\hat p=\frac{275}{600}\approx0.4583.` |
| 3269 | 26900-26902 | 0.33 | inline_safe | bracket | `\sqrt{\frac{\hat p(1-\hat p)}{600}}\approx0.0203,` |
| 3271 | 26915-26917 | 0.30 | inline_safe | bracket | `\frac{\hat p-p}{\sqrt{p(1-p)/n}}\approx N(0,1).` |
| 3272 | 26919-26921 | 0.30 | inline_safe | bracket | `P\{\|\hat p-p\|<0.1\}>0.95.` |
| 3273 | 26923-26925 | 0.31 | inline_safe | bracket | `P\left\{\left\|Z\right\|<\frac{0.1\sqrt n}{1/2}\right\}\ge0.95.` |
| 3274 | 26927-26929 | 0.21 | inline_safe | bracket | `\frac{0.1\sqrt n}{1/2}\ge1.96,` |
| 3275 | 26931-26933 | 0.29 | inline_safe | bracket | `n\ge\left(\frac{1.96}{0.2}\right)^2=96.04.` |
| 3276 | 26964-26966 | 0.16 | inline_safe | bracket | `X\sim N(\mu,\sigma^2)` |
| 3277 | 26968-26970 | 0.36 | inline_safe | bracket | `\overline X=15,\qquad S^2=0.36.` |
| 3278 | 26975-26977 | 0.29 | inline_safe | bracket | `T=\frac{\overline X-\mu}{S/\sqrt n}\sim t(n-1).` |
| 3279 | 26979-26981 | 0.21 | inline_safe | bracket | `P(\mu<\overline\mu)=0.95.` |
| 3280 | 26983-26985 | 0.42 | inline_safe | bracket | `P\left\{\frac{\overline X-\mu}{S/\sqrt n}>-t_{0.05}(15)\right\}=0.95` |
| 3281 | 26987-26989 | 0.32 | inline_safe | bracket | `\mu<\overline X+t_{0.05}(15)\frac{S}{\sqrt n}.` |
| 3282 | 26991-26993 | 0.40 | inline_safe | bracket | `S=\sqrt{0.36}=0.6,\qquad n=16.` |
| 3283 | 26995-27000 | 0.27 | normalized_width_not_low | bracket | `\overline\mu =15+1.7531\cdot\frac{0.6}{4} =15+0.2630 =15.2630.` |
| 3284 | 27002-27004 | 0.19 | inline_safe | bracket | `(-\infty,\,15.2630).` |
| 3286 | 27100-27102 | 0.26 | inline_safe | bracket | `\alpha = P\{\text{拒绝}\, H_0 \mid H_0\text{ 为真}\}.` |
| 3287 | 27104-27106 | 0.28 | inline_safe | bracket | `\beta = P\{\text{未拒绝}\, H_0 \mid H_1\text{ 为真}\}.` |
| 3288 | 27229-27231 | 0.14 | inline_safe | bracket | `H_1\colon \theta>\theta_0` |
| 3289 | 27233-27235 | 0.14 | inline_safe | bracket | `H_1\colon \theta<\theta_0` |
| 3290 | 27237-27239 | 0.13 | inline_safe | bracket | `H_1\colon \theta\ne\theta_0` |
| 3291 | 27254-27256 | 0.25 | inline_safe | bracket | `\alpha=P(\text{拒绝 }H_0\mid H_0\text{ 成立}).` |
| 3292 | 27258-27260 | 0.25 | inline_safe | bracket | `P(\text{接受 }H_1\mid H_0\text{ 成立})=\alpha.` |
| 3293 | 27273-27275 | 0.18 | inline_safe | bracket | `T=\frac{\overline{X}-\mu_0}{S/\sqrt{n}}.` |
| 3294 | 27277-27279 | 0.44 | inline_safe | bracket | `S^2=\frac{Q^2}{n-1},\qquad S=\frac{Q}{\sqrt{n-1}},` |
| 3296 | 27285-27287 | 0.44 | inline_safe | bracket | `\text{故应选取的检验统计量为}\quad T=\frac{\overline{X}\sqrt{n(n-1)}}{Q}.` |
| 3299 | 27395-27397 | 0.35 | inline_safe | bracket | `H_0:\mu=5,\qquad H_1:\mu\ne 5,` |
| 3300 | 27402-27404 | 0.29 | inline_safe | bracket | `Z=\frac{\overline{X}-5}{1/\sqrt{100}}\sim N(0,1).` |
| 3301 | 27407-27409 | 0.28 | inline_safe | bracket | `\|Z\|\ge z_{\alpha/2}=z_{0.005}.` |
| 3302 | 27411-27413 | 0.19 | inline_safe | bracket | `z_{0.005}=2.57.` |
| 3303 | 27416-27420 | 0.16 | inline_safe | bracket | `z=\frac{5.32-5}{1/\sqrt{100}} =\frac{0.32}{0.1} =3.2.` |
| 3304 | 27422-27424 | 0.19 | inline_safe | bracket | `\|z\|=3.2>2.57,` |
| 3305 | 27434-27436 | 0.43 | inline_safe | bracket | `H_0\colon \mu=570,\qquad H_1\colon \mu\neq570.` |
| 3306 | 27438-27440 | 0.29 | inline_safe | bracket | `Z=\frac{\overline{X}-570}{8/\sqrt{10}}\sim N(0,1).` |
| 3307 | 27442-27444 | 0.26 | inline_safe | bracket | `\|z\|\ge z_{0.025}=1.96.` |
| 3308 | 27446-27450 | 0.20 | inline_safe | bracket | `z=\frac{575.2-570}{8/\sqrt{10}} =\frac{5.2\sqrt{10}}{8} \approx 2.055.` |
| 3309 | 27459-27461 | 0.39 | inline_safe | bracket | `H_0\colon \mu \leq 1500,\quad H_1\colon \mu > 1500.` |
| 3310 | 27463-27465 | 0.45 | inline_safe | bracket | `Z = \frac{\overline{X}-\mu_0}{\sigma/\sqrt{n}} = \frac{\overline{X}-1500}{200/\sqrt{25}} \sim N(0,1).` |
| 3311 | 27468-27470 | 0.41 | inline_safe | bracket | `z = \frac{1675-1500}{200/5} = \frac{175}{40} = 4.375.` |
| 3312 | 27497-27499 | 0.40 | inline_safe | bracket | `H_0\colon \mu = 2000,\quad H_1\colon \mu \neq 2000.` |
| 3313 | 27501-27503 | 0.40 | inline_safe | bracket | `t = \frac{\overline{X}-\mu_0}{S/\sqrt{n}} \sim t(n-1) = t(24).` |
| 3315 | 27518-27520 | 0.34 | inline_safe | bracket | `H_0\colon \mu \leq 70,\quad H_1\colon \mu > 70.` |
| 3316 | 27522-27524 | 0.28 | inline_safe | bracket | `t = \frac{\overline{X}-\mu_0}{S/\sqrt{n}} \sim t(24).` |
| 3317 | 27527-27529 | 0.43 | inline_safe | bracket | `t = \frac{69.5-70}{15/\sqrt{25}} = \frac{-0.5}{3} = -0.167.` |
| 3318 | 27544-27546 | 0.29 | inline_safe | bracket | `T=\frac{\overline X-\mu}{S/\sqrt n}\sim t(n-1).` |
| 3319 | 27548-27550 | 0.28 | inline_safe | bracket | `\overline x\pm t_{0.025}(35)\frac{s}{\sqrt n}.` |
| 3320 | 27552-27556 | 0.20 | normalized_width_not_low | bracket | `2.0301\cdot\frac{15}{\sqrt{36}} =2.0301\cdot2.5 =5.07525.` |
| 3321 | 27558-27561 | 0.44 | normalized_width_not_low | bracket | `\mu\in(66.5-5.07525,\ 66.5+5.07525) \approx(61.42,\ 71.58).` |
| 3322 | 27564-27566 | 0.39 | inline_safe | bracket | `H_0\colon\mu=70,\qquad H_1\colon\mu\neq70` |
| 3325 | 27583-27585 | 0.46 | inline_safe | bracket | `\chi^2=\frac{(n-1)s^2}{\sigma_0^2}=\frac{25\times7200}{5000}=36.` |
| 3329 | 27608-27610 | 0.43 | inline_safe | bracket | `\chi^2=\frac{(n-1)s^2}{\sigma_0^2}=\frac{0.82}{0.16}=5.125.` |
| 3332 | 27631-27636 | 0.47 | normalized_width_not_low | bracket | `S^2=\frac1{3}\sum_{i=1}^{4}(x_i-\overline x)^2 =\frac{40}{3}, \qquad S=\sqrt{\frac{40}{3}}\approx3.65.` |
| 3333 | 27639-27641 | 0.43 | inline_safe | bracket | `H_0:\mu=1260,\qquad H_1:\mu\ne1260.` |
| 3334 | 27643-27645 | 0.29 | inline_safe | bracket | `T=\frac{\overline X-1260}{S/\sqrt4}\sim t(3).` |
| 3335 | 27647-27649 | 0.37 | inline_safe | bracket | `\|T_0\|=\frac{1267-1260}{3.65/2}\approx3.836.` |
| 3336 | 27651-27653 | 0.35 | inline_safe | bracket | `3.836>t_{0.025}(3)=3.1824,` |
| 3337 | 27657-27659 | 0.36 | inline_safe | bracket | `H_0:\sigma\le2,\qquad H_1:\sigma>2.` |
| 3338 | 27661-27663 | 0.34 | inline_safe | bracket | `\chi^2=\frac{(n-1)S^2}{\sigma_0^2}\sim\chi^2(3).` |
| 3339 | 27665-27667 | 0.32 | inline_safe | bracket | `\chi_0^2=\frac{3\cdot(40/3)}{4}=10.` |
| 3340 | 27669-27671 | 0.32 | inline_safe | bracket | `\chi^2>\chi^2_{0.05}(3)=7.815.` |
| 3343 | 27696-27698 | 0.39 | inline_safe | bracket | `\chi^2 = \frac{(n-1)S^2}{\sigma_0^2} \sim \chi^2(n-1).` |
| 3345 | 27722-27724 | 0.40 | inline_safe | bracket | `H_0\colon \sigma^2 = 64,\quad H_1\colon \sigma^2 \neq 64.` |
| 3348 | 27735-27737 | 0.45 | inline_safe | bracket | `\chi^2 = \frac{9 \times 68.16}{64} = \frac{613.44}{64} = 9.585.` |
| 3349 | 27743-27745 | 0.39 | inline_safe | bracket | `1.31,\ 1.55,\ 1.34,\ 1.40,\ 1.45.` |
| 3351 | 27755-27759 | 0.35 | normalized_width_not_low | bracket | `\chi^2=\frac{(n-1)S^2}{\sigma_0^2} =\frac{\sum_{i=1}^{n}(X_i-\overline{X})^2}{0.048^2} \sim \chi^2(4).` |
| 3354 | 27771-27773 | 0.33 | inline_safe | bracket | `\chi^2=\frac{0.0362}{0.048^2}\approx15.7118.` |
| 3355 | 27775-27779 | 0.34 | normalized_width_not_low | bracket | `\chi^2\le \chi^2_{0.95}(4)=0.711 \quad\text{或}\quad \chi^2\ge \chi^2_{0.05}(4)=9.488.` |
| 3356 | 27786-27788 | 0.37 | inline_safe | bracket | `H_0\colon \sigma\ge2,\qquad H_1\colon \sigma<2,` |
| 3357 | 27799-27802 | 0.33 | normalized_width_not_low | bracket | `\chi^2=\frac{(n-1)S^2}{\sigma_0^2} =\frac{(n-1)S^2}{4}\sim\chi^2(n-1)` |
| 3358 | 27806-27808 | 0.28 | inline_safe | bracket | `\chi^2\le \chi^2_{1-\alpha}(n-1),` |
| 3362 | 27836-27838 | 0.13 | inline_safe | bracket | `H_0\colon \mu=50` |
| 3363 | 27845-27847 | 0.30 | inline_safe | bracket | `u=\frac{\overline X-\mu_0}{\sigma/\sqrt n}\sim N(0,1).` |
| 3364 | 27849-27851 | 0.30 | inline_safe | bracket | `u=\frac{48.5-50}{2/\sqrt9}=-2.25.` |
| 3365 | 27853-27855 | 0.26 | inline_safe | bracket | `\|u\|\ge u_{0.025}=1.96.` |
| 3366 | 27859-27861 | 0.32 | inline_safe | bracket | `t=\frac{\overline X-\mu_0}{S/\sqrt n}\sim t(n-1).` |
| 3367 | 27863-27865 | 0.28 | inline_safe | bracket | `t=\frac{48.5-50}{2.5/\sqrt9}=-1.8.` |
| 3368 | 27867-27869 | 0.30 | inline_safe | bracket | `\|t\|\ge t_{0.025}(8)=2.31.` |
| 3370 | 27884-27886 | 0.37 | inline_safe | bracket | `\overline x=\frac{6.0+5.7+\cdots+5.0}{9}=6.` |
| 3371 | 27889-27891 | 0.21 | inline_safe | bracket | `\overline X\sim N\!\left(\mu,\frac{\sigma^2}{n}\right),` |
| 3372 | 27893-27895 | 0.23 | inline_safe | bracket | `\overline x\pm u_{0.025}\frac{\sigma}{\sqrt n}.` |
| 3373 | 27897-27900 | 0.18 | inline_safe | bracket | `6\pm1.96\cdot\frac{0.6}{3} =6\pm0.392,` |
| 3374 | 27902-27904 | 0.20 | inline_safe | bracket | `(5.608,\ 6.392).` |
| 3376 | 27912-27914 | 0.21 | inline_safe | bracket | `\frac{\overline X-\mu}{S/\sqrt n}\sim t(8).` |
| 3377 | 27916-27919 | 0.26 | normalized_width_not_low | bracket | `\overline x\pm t_{0.025}(8)\frac{S}{\sqrt n} \approx6\pm2.306\frac{\sqrt{0.33}}{3}.` |
| 3378 | 27921-27923 | 0.23 | inline_safe | bracket | `\mu\in(5.558,\ 6.442).` |
| 3379 | 27932-27934 | 0.40 | inline_safe | bracket | `F = \frac{S_1^2}{S_2^2} \sim F(n_1-1, n_2-1).` |
| 3383 | 27977-27979 | 0.25 | inline_safe | bracket | `F = \frac{0.844}{0.767} \approx 1.100.` |
| 3386 | 27997-27999 | 0.39 | inline_safe | bracket | `1.23,\ 1.22,\ 1.20,\ 1.26,\ 1.23.` |
| 3389 | 28026-28028 | 0.43 | inline_safe | bracket | `H_0\colon \mu=100,\qquad H_1\colon \mu\neq100.` |
| 3390 | 28030-28032 | 0.28 | inline_safe | bracket | `t=\frac{\overline X-100}{S/\sqrt n}\sim t(5).` |
| 3391 | 28034-28036 | 0.33 | inline_safe | bracket | `t=\frac{99.3-100}{6.24/\sqrt6}\approx -0.275.` |
| 3392 | 28040-28042 | 0.37 | inline_safe | bracket | `H_0\colon \sigma\le5,\qquad H_1\colon \sigma>5.` |
| 3394 | 28061-28063 | 0.41 | inline_safe | bracket | `H_0\colon \mu=100,\qquad H_1\colon \mu\ne100.` |
| 3395 | 28065-28067 | 0.40 | inline_safe | bracket | `t=\frac{\overline X-100}{S/\sqrt n}\sim t(n-1)=t(9).` |
| 3396 | 28069-28071 | 0.32 | inline_safe | bracket | `t=\frac{98.2-100}{2.25/\sqrt{10}}\approx -2.53.` |
| 3397 | 28073-28075 | 0.30 | inline_safe | bracket | `\|t\|\ge t_{0.025}(9)=2.26.` |
| 3398 | 28079-28081 | 0.42 | inline_safe | bracket | `H_0\colon \sigma^2\le4,\qquad H_1\colon \sigma^2>4.` |
| 3399 | 28083-28085 | 0.34 | inline_safe | bracket | `\chi^2=\frac{(n-1)S^2}{\sigma_0^2}\sim\chi^2(9).` |
| 3400 | 28087-28089 | 0.34 | inline_safe | bracket | `\chi^2=\frac{9\times2.25^2}{4}\approx11.39.` |
| 3401 | 28091-28093 | 0.24 | inline_safe | bracket | `\chi^2\ge \chi^2_{0.05}(9).` |
| 3404 | 28116-28118 | 0.47 | inline_safe | bracket | `H_0\colon \mu=52.00,\qquad H_1\colon \mu>52.00.` |
| 3405 | 28120-28122 | 0.30 | inline_safe | bracket | `t=\frac{\overline X-52.00}{S/\sqrt n}\sim t(6).` |
| 3406 | 28124-28126 | 0.37 | inline_safe | bracket | `t=\frac{52.1357-52.00}{2.6954/\sqrt7}\approx0.133.` |
| 3407 | 28128-28130 | 0.29 | inline_safe | bracket | `t\ge t_{0.05}(6)\approx1.943.` |
| 3408 | 28134-28137 | 0.31 | normalized_width_not_low | bracket | `\mu\in\left(\overline{x}-t_{0.025}(6)\frac{s}{\sqrt n}, \overline{x}+t_{0.025}(6)\frac{s}{\sqrt n}\right).` |
| 3409 | 28139-28144 | 0.32 | normalized_width_not_low | bracket | `\mu\in \left(52.1357-2.447\frac{2.6954}{\sqrt7}, 52.1357+2.447\frac{2.6954}{\sqrt7}\right) \approx(49.64,\ 54.63).` |
| 3410 | 28154-28156 | 0.46 | inline_safe | bracket | `H_0\colon \mu=235.5,\qquad H_1\colon \mu\ne235.5.` |
| 3411 | 28158-28160 | 0.39 | inline_safe | bracket | `t=\frac{\sqrt n(\overline X-\mu_0)}{S}\sim t(n-1).` |
| 3412 | 28162-28166 | 0.32 | inline_safe | bracket | `\|t\| =\left\|\frac{\sqrt{49}(236.5-235.5)}{3.5}\right\| =2.` |
| 3413 | 28168-28170 | 0.26 | inline_safe | bracket | `\|t\|\ge u_{0.005}=2.58.` |
| 3414 | 28172-28174 | 0.10 | inline_safe | bracket | `2<2.58,` |
| 3415 | 28180-28182 | 0.17 | inline_safe | bracket | `\overline{x}=495.3\ \text{克},` |
| 3416 | 28184-28186 | 0.15 | inline_safe | bracket | `s=13.74\ \text{克}.` |
| 3417 | 28194-28196 | 0.43 | inline_safe | bracket | `H_0\colon \mu=500,\qquad H_1\colon \mu\neq500.` |
| 3418 | 28198-28200 | 0.28 | inline_safe | bracket | `t=\frac{\overline X-500}{S/\sqrt n}\sim t(5).` |
| 3419 | 28202-28206 | 0.20 | inline_safe | bracket | `t=\frac{495.3-500}{13.74/\sqrt6} \approx \frac{-4.7}{5.609} \approx -0.838.` |
| 3420 | 28208-28210 | 0.33 | inline_safe | bracket | `\|t\|\ge t_{0.025}(5)=2.5706.` |
| 3421 | 28214-28216 | 0.39 | inline_safe | bracket | `H_0\colon \sigma\le10,\qquad H_1\colon \sigma>10.` |
| 3422 | 28218-28220 | 0.33 | inline_safe | bracket | `\chi^2=\frac{(n-1)S^2}{100}\sim\chi^2(5)` |
| 3423 | 28222-28226 | 0.24 | normalized_width_not_low | bracket | `\chi^2=\frac{5\times 13.74^2}{100} =\frac{5\times188.7876}{100} \approx9.439.` |
| 3424 | 28228-28230 | 0.35 | inline_safe | bracket | `\chi^2\ge\chi^2_{0.05}(5)=11.071.` |
| 3425 | 28238-28240 | 0.36 | inline_safe | bracket | `\overline X=499,\qquad S=16.03.` |
| 3426 | 28248-28250 | 0.28 | inline_safe | bracket | `T=\frac{\overline X-500}{S/\sqrt n}\sim t(8).` |
| 3427 | 28252-28254 | 0.30 | inline_safe | bracket | `\|T\|>t_{0.025}(8)=2.306.` |
| 3428 | 28256-28260 | 0.21 | normalized_width_not_low | bracket | `T_0=\frac{499-500}{16.03/3} =-\frac3{16.03} \approx -0.187.` |
| 3429 | 28264-28267 | 0.22 | inline_safe | bracket | `\chi^2=\frac{(n-1)S^2}{100} =\frac{8S^2}{100},` |
| 3430 | 28269-28271 | 0.37 | inline_safe | bracket | `\frac{8S^2}{100}>\chi^2_{0.05}(8)=15.507.` |
| 3431 | 28273-28276 | 0.17 | inline_safe | bracket | `\frac{8\times16.03^2}{100} \approx20.56.` |
| 3434 | 28308-28310 | 0.37 | inline_safe | bracket | `F=\frac{S_1^2}{S_2^2}=\frac{3.762}{4.019}\approx0.936.` |
| 3437 | 28328-28333 | 0.38 | normalized_width_not_low | bracket | `\left( \overline X-t_{1-\alpha/2}(n-1)\frac{S}{\sqrt{n-1}}, \overline X+t_{1-\alpha/2}(n-1)\frac{S}{\sqrt{n-1}} \right).` |
| 3439 | 28339-28341 | 0.28 | inline_safe | bracket | `1.943\cdot\frac{2.71}{\sqrt6}\approx2.15.` |
| 3441 | 28347-28349 | 0.20 | inline_safe | bracket | `(122.9,\ 127.1).` |
| 3442 | 28352-28354 | 0.47 | inline_safe | bracket | `H_0\colon\mu_1=\mu_2,\qquad H_1\colon\mu_1\ne\mu_2.` |
| 3443 | 28356-28361 | 0.26 | structural | bracket | `u= \frac{(\overline X-\overline Y)-0} {\sqrt{\sigma_1^2/n+\sigma_2^2/m}} \sim N(0,1).` |
| 3444 | 28363-28368 | 0.26 | structural | bracket | `u= \frac{1295-1230} {\sqrt{84^2/60+96^2/60}} \approx3.95.` |
| 3445 | 28370-28372 | 0.26 | inline_safe | bracket | `\|u\|\ge u_{0.975}=1.96.` |
| 3446 | 28384-28386 | 0.31 | inline_safe | bracket | `T=\frac{\overline X-\mu}{S^*/\sqrt n}\sim t(n-1).` |
| 3447 | 28388-28390 | 0.25 | inline_safe | bracket | `\overline x\pm t_{0.95}(6)\frac{S^*}{\sqrt7}.` |
| 3448 | 28392-28394 | 0.28 | inline_safe | bracket | `1.943\cdot\frac{2.71}{\sqrt7}\approx1.99.` |
| 3450 | 28400-28402 | 0.15 | inline_safe | bracket | `(123,\ 127).` |
| 3451 | 28405-28407 | 0.41 | inline_safe | bracket | `H_0\colon \mu=124,\qquad H_1\colon \mu\ne124.` |
| 3452 | 28409-28413 | 0.18 | inline_safe | bracket | `T=\frac{\overline X-\mu_0}{S^*/\sqrt n} =\frac{125-124}{2.71/\sqrt7} \approx0.976.` |
| 3453 | 28415-28417 | 0.30 | inline_safe | bracket | `\|T\|\ge t_{0.95}(6)=1.943.` |
| 3454 | 28419-28421 | 0.17 | inline_safe | bracket | `0.976<1.943,` |
| 3455 | 28430-28432 | 0.37 | inline_safe | bracket | `H_0\colon \theta=\theta_0,\quad H_1\colon \theta\neq\theta_0,` |
| 3459 | 28460-28462 | 0.42 | inline_safe | bracket | `t = \frac{10-9.7}{0.4/4} = \frac{0.3}{0.1} = 3.0 > 2.132.` |
| 3461 | 28477-28483 | 0.30 | normalized_width_not_low | bracket | `\mu\in \left( \overline x-t_{0.025}(15)\frac{s}{\sqrt n}, \overline x+t_{0.025}(15)\frac{s}{\sqrt n} \right).` |
| 3462 | 28485-28488 | 0.32 | normalized_width_not_low | bracket | `t_{0.025}(15)\frac{s}{\sqrt n} =2.132\cdot\frac{0.4}{4}=0.2132.` |
| 3463 | 28490-28492 | 0.27 | inline_safe | bracket | `\mu\in(9.7868,\ 10.2132).` |
| 3464 | 28495-28498 | 0.35 | normalized_width_not_low | bracket | `H_0\colon \sigma^2=0.048^2,\qquad H_1\colon \sigma^2\ne0.048^2.` |
| 3467 | 28512-28514 | 0.33 | inline_safe | bracket | `\chi^2=\frac{0.031525}{0.048^2}\approx13.683.` |
| 3468 | 28516-28520 | 0.34 | normalized_width_not_low | bracket | `\chi^2>\chi^2_{0.025}(5)=12.833 \quad\text{或}\quad \chi^2<\chi^2_{0.975}(5)=0.831.` |
| 3470 | 28539-28541 | 0.27 | inline_safe | bracket | `\overline{x}=\frac{799.8}{8}=99.975,` |
| 3471 | 28543-28545 | 0.41 | inline_safe | bracket | `\sum_{i=1}^8(x_i-\overline{x})^2=8.815.` |
| 3473 | 28552-28554 | 0.41 | inline_safe | bracket | `H_0\colon \mu=100,\qquad H_1\colon \mu\ne100.` |
| 3474 | 28556-28558 | 0.26 | inline_safe | bracket | `t=\frac{\overline{X}-100}{S/\sqrt n}\sim t(7).` |
| 3475 | 28560-28562 | 0.36 | inline_safe | bracket | `t=\frac{99.975-100}{1.1222/\sqrt8}\approx -0.063.` |
| 3476 | 28564-28566 | 0.32 | inline_safe | bracket | `\|t\|\ge t_{0.025}(7)\approx2.365.` |
| 3477 | 28568-28570 | 0.22 | inline_safe | bracket | `\|-0.063\|<2.365,` |
| 3478 | 28574-28576 | 0.42 | inline_safe | bracket | `\frac{(n-1)S^2}{\sigma^2}\sim\chi^2(n-1)=\chi^2(7).` |
| 3479 | 28578-28583 | 0.18 | structural | bracket | `\left( \frac{(n-1)S^2}{\chi^2_{0.05}(7)}, \frac{(n-1)S^2}{\chi^2_{0.95}(7)} \right).` |
| 3480 | 28585-28591 | 0.25 | structural | bracket | `\left( \frac{8.815}{14.067}, \frac{8.815}{2.167} \right) \approx(0.6268,\ 4.068).` |
| 3481 | 28593-28595 | 0.20 | inline_safe | bracket | `(0.627,\ 4.068).` |
| 3482 | 28600-28602 | 0.46 | inline_safe | bracket | `0.530,\ 0.542,\ 0.510,\ 0.495,\ 0.515.` |
| 3487 | 28624-28626 | 0.48 | inline_safe | bracket | `t=\frac{0.5184-0.5}{0.0182/\sqrt{5}}=\frac{0.0184}{0.00813}\approx 2.264.` |
| 3488 | 28643-28645 | 0.35 | inline_safe | bracket | `H_0\colon\theta=0.1,\quad H_1\colon\theta>0.1,` |
| 3491 | 28664-28666 | 0.12 | inline_safe | bracket | `\alpha=0.009.` |
| 3492 | 28672-28674 | 0.38 | inline_safe | bracket | `H_0\colon\mu=2\quad\text{vs}\quad H_1\colon\mu=3,` |
| 3495 | 28694-28698 | 0.19 | inline_unsafe_marker | bracket | `H_0\colon f(x)=\begin{cases}1/2, & 0\leq x\leq2,\\0, & \text{其他},\end{cases} \quad H_1\colon f(x)=\begin{cases}x/2, & 0\leq x\leq2,\\0, & \text{其他}.\end{cases}` |
| 3498 | 28742-28744 | 0.26 | inline_safe | bracket | `\alpha = P\{\text{拒绝}\,H_0 \mid H_0\text{ 为真}\}.` |
| 3499 | 28814-28816 | 0.49 | inline_safe | bracket | `A_k=\{\text{第 }k\text{ 个人抽中红球}\},\qquad k=1,2,\dots,n.` |
| 3500 | 28821-28823 | 0.42 | inline_safe | bracket | `P(A_k)=\frac{M}{N},\qquad k=1,2,\dots,n.` |
| 3501 | 28828-28830 | 0.16 | inline_safe | bracket | `P(A_1)=\frac{M}{N}.` |
| 3504 | 28841-28846 | 0.40 | display_environment | env:align* | `P(A_2) &=\frac{M-1}{N-1}\cdot\frac{M}{N}+\frac{M}{N-1}\cdot\frac{N-M}{N} \\ &=\frac{M(M-1)+M(N-M)}{N(N-1)} \\ &=\frac{M(N-1)}{N(N-1)}=\frac{M}{N}.` |
| 3505 | 28866-28868 | 0.42 | inline_safe | bracket | `A=\{\text{甲取到红球}\},\qquad B=\{\text{乙取到红球}\}.` |
| 3506 | 28871-28873 | 0.14 | inline_safe | bracket | `P(B)=\frac{5}{12}.` |
| 3507 | 28876-28878 | 0.20 | inline_safe | bracket | `P(B\|\overline A)=\frac{5}{11}.` |
| 3508 | 28881-28883 | 0.37 | inline_safe | bracket | `A\overline B\qquad\text{和}\qquad \overline A B.` |
| 3509 | 28885-28887 | 0.41 | inline_safe | bracket | `P(\text{恰有一人取到红球})=P(A\overline B)+P(\overline A B).` |
| 3510 | 28889-28892 | 0.38 | normalized_width_not_low | bracket | `P(A\overline B)=\frac{5}{12}\cdot\frac{7}{11},\qquad P(\overline A B)=\frac{7}{12}\cdot\frac{5}{11}.` |
| 3511 | 28894-28898 | 0.33 | normalized_width_not_low | bracket | `P(A\overline B)+P(\overline A B) =\frac{5}{12}\cdot\frac{7}{11}+\frac{7}{12}\cdot\frac{5}{11} =\frac{35}{66}.` |
| 3512 | 28901-28903 | 0.41 | inline_safe | bracket | `\frac{5}{12},\qquad \frac{5}{11},\qquad \frac{35}{66}.` |
| 3513 | 28912-28914 | 0.25 | inline_safe | bracket | `C_n=\{\text{至少有两个人生日相同}\}.` |
| 3514 | 28919-28921 | 0.44 | inline_safe | bracket | `P(\overline{C_n})=\frac{365\cdot364\cdots(365-n+1)}{365^n},` |
| 3515 | 28923-28925 | 0.47 | inline_safe | bracket | `P(C_n)=1-\frac{365\cdot364\cdots(365-n+1)}{365^n}.` |
| 3516 | 28935-28939 | 0.41 | normalized_width_not_low | bracket | `P(\overline{C_n}) =1\cdot\frac{364}{365}\cdot\frac{363}{365}\cdots\frac{365-n+1}{365} =\frac{365\cdot364\cdots(365-n+1)}{365^n}.` |
| 3517 | 28941-28944 | 0.39 | normalized_width_not_low | bracket | `P(C_n)=1-P(\overline{C_n}) =1-\frac{365\cdot364\cdots(365-n+1)}{365^n}.` |
| 3518 | 28951-28954 | 0.32 | normalized_width_not_low | bracket | `\prod_{k=0}^{n-1}\left(1-\frac{k}{365}\right) \approx \exp\!\left(-\frac{n(n-1)}{2\cdot365}\right)` |
| 3519 | 28956-28958 | 0.36 | inline_safe | bracket | `P(C_n)\approx 1-\exp\!\left(-\frac{n(n-1)}{730}\right).` |
| 3520 | 28970-28972 | 0.30 | inline_safe | bracket | `C=\{\text{30 名同学中至少有两人同生日}\}.` |
| 3521 | 28974-28976 | 0.30 | inline_safe | bracket | `\overline C=\{\text{30 名同学的生日两两不同}\}.` |
| 3522 | 28979-28983 | 0.37 | normalized_width_not_low | bracket | `P(\overline C) =\frac{365}{365}\cdot\frac{364}{365}\cdot\frac{363}{365}\cdots\frac{336}{365} =\frac{365\cdot364\cdots336}{365^{30}}.` |
| 3523 | 28986-28989 | 0.28 | inline_safe | bracket | `P(C)=1-P(\overline C) =1-\frac{365\cdot364\cdots336}{365^{30}}.` |
| 3524 | 28992-28994 | 0.25 | inline_safe | bracket | `1-\frac{365\cdot364\cdots336}{365^{30}}.` |
| 3525 | 29010-29014 | 0.25 | normalized_width_not_low | bracket | `p_1+p_2+0.25=1, \qquad\text{即}\qquad p_1+p_2=0.75.` |
| 3526 | 29017-29019 | 0.46 | inline_safe | bracket | `m=p_2(1+m)+p_1(2+m)+0.25\cdot3.` |
| 3527 | 29021-29023 | 0.36 | inline_safe | bracket | `7=p_2(8)+p_1(9)+\frac34.` |
| 3528 | 29025-29028 | 0.47 | normalized_width_not_low | bracket | `m=(p_1+p_2)m+p_2+2p_1+\frac34 =0.75m+p_2+2p_1+\frac34.` |
| 3529 | 29030-29032 | 0.43 | inline_safe | bracket | `7=0.75\cdot7+p_2+2p_1+\frac34,` |
| 3530 | 29034-29036 | 0.18 | inline_safe | bracket | `p_2+2p_1=1.` |
| 3531 | 29038-29043 | 0.21 | inline_unsafe_marker | bracket | `\begin{cases} p_1+p_2=0.75,\\ 2p_1+p_2=1, \end{cases}` |
| 3532 | 29045-29047 | 0.37 | inline_safe | bracket | `p_1=0.5,\qquad p_2=0.25.` |
| 3533 | 29055-29057 | 0.08 | inline_safe | bracket | `m=EX.` |
| 3535 | 29063-29065 | 0.20 | inline_safe | bracket | `m=2+\frac23m,` |
| 3536 | 29067-29069 | 0.34 | inline_safe | bracket | `\frac13m=2,\qquad m=6.` |
| 3537 | 29079-29081 | 0.43 | inline_safe | bracket | `P_i=\{\text{从本金 }i\text{ 出发，最终先达到 }N\text{ 而不是先破产的概率}\}.` |
| 3538 | 29086-29088 | 0.38 | inline_safe | bracket | `P_i=\frac{i}{N},\qquad i=0,1,\dots,N.` |
| 3542 | 29120-29122 | 0.31 | inline_safe | bracket | `P_0=0,\qquad P_N=1.` |
| 3543 | 29125-29127 | 0.43 | inline_safe | bracket | `p(P_{i+1}-P_i)=q(P_i-P_{i-1}),` |
| 3544 | 29129-29131 | 0.41 | inline_safe | bracket | `P_{i+1}-P_i=\frac{q}{p}(P_i-P_{i-1}).` |
| 3545 | 29133-29135 | 0.32 | inline_safe | bracket | `P_i=\frac{1-(q/p)^i}{1-q/p}\cdot P_1.` |
| 3547 | 29141-29143 | 0.24 | inline_safe | bracket | `P_i=\frac{1-(q/p)^i}{1-(q/p)^N}.` |
| 3548 | 29148-29150 | 0.31 | inline_safe | bracket | `P_0=0,\qquad P_N=1.` |
| 3550 | 29179-29181 | 0.25 | inline_safe | bracket | `\frac{q}{p}=\frac{3/5}{2/5}=\frac32.` |
| 3551 | 29184-29186 | 0.24 | inline_safe | bracket | `P_i=\frac{1-(q/p)^i}{1-(q/p)^N},` |
| 3552 | 29188-29190 | 0.24 | inline_safe | bracket | `P_2=\frac{1-(3/2)^2}{1-(3/2)^5}.` |
| 3553 | 29193-29195 | 0.49 | inline_safe | bracket | `1-\left(\frac32\right)^2=1-\frac94=-\frac54,` |
| 3554 | 29196-29198 | 0.45 | inline_safe | bracket | `1-\left(\frac32\right)^5=1-\frac{243}{32}=-\frac{211}{32}.` |
| 3555 | 29200-29204 | 0.21 | inline_safe | bracket | `P_2=\frac{-5/4}{-211/32} =\frac{5}{4}\cdot\frac{32}{211} =\frac{40}{211}.` |
| 3556 | 29207-29209 | 0.19 | inline_safe | bracket | `\frac{40}{211}\approx0.1896.` |
| 3558 | 29232-29234 | 0.16 | inline_safe | bracket | `M=\{\text{两人能够见面}\}` |
| 3559 | 29240-29242 | 0.26 | inline_safe | bracket | `P(M)=1-\left(1-\frac{\tau}{T}\right)^2.` |
| 3560 | 29247-29249 | 0.39 | inline_safe | bracket | `2\cdot\frac12(T-\tau)^2=(T-\tau)^2.` |
| 3561 | 29252-29255 | 0.25 | inline_safe | bracket | `P(M)=1-\frac{(T-\tau)^2}{T^2} =1-\left(1-\frac{\tau}{T}\right)^2.` |
| 3562 | 29262-29264 | 0.23 | inline_safe | bracket | `P(\text{针与平行线相交})=\frac{2l}{\pi d}.` |
| 3563 | 29276-29278 | 0.39 | inline_safe | bracket | `X=\text{甲的到达时刻},\qquad Y=\text{乙的到达时刻}.` |
| 3565 | 29285-29290 | 0.28 | normalized_width_not_low | bracket | `P(\text{见面})=1-\left(1-\frac{5}{30}\right)^2 =1-\left(\frac56\right)^2 =1-\frac{25}{36} =\frac{11}{36}.` |
| 3566 | 29295-29297 | 0.06 | inline_safe | bracket | `\frac{11}{36}.` |
| 3568 | 29325-29327 | 0.47 | inline_safe | bracket | `T_k=\text{从已经收集到 }k-1\text{ 种，到第一次收集到第 }k\text{ 种所需的次数},` |
| 3569 | 29338-29340 | 0.33 | inline_safe | bracket | `E(T_k)=\frac{1}{p_k}=\frac{n}{n-k+1}.` |
| 3570 | 29342-29347 | 0.48 | display_environment | env:align* | `E(T) &=E(T_1)+E(T_2)+\cdots+E(T_n) \\ &=\frac{n}{n}+\frac{n}{n-1}+\cdots+\frac{n}{1} \\ &=n\left(1+\frac12+\frac13+\cdots+\frac1n\right).` |
| 3571 | 29364-29366 | 0.40 | inline_safe | bracket | `T=\text{从已有 2 种开始，到集齐 5 种还需的购买次数}.` |
| 3572 | 29368-29372 | 0.34 | normalized_width_not_low | bracket | `T_3=\text{从 2 种到 3 种所需次数},\quad T_4=\text{从 3 种到 4 种所需次数},\quad T_5=\text{从 4 种到 5 种所需次数}.` |
| 3573 | 29379-29381 | 0.30 | inline_safe | bracket | `E(T_3)=\frac{1}{p_3}=\frac53.` |
| 3577 | 29398-29400 | 0.38 | inline_safe | bracket | `E(T)=\frac{10}{6}+\frac{15}{6}+\frac{30}{6}=\frac{55}{6}.` |
| 3578 | 29403-29405 | 0.14 | inline_safe | bracket | `\frac{55}{6}\approx 9.17` |
