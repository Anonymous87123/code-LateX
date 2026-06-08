# 2026-05-16 清理补记

## 范围

- 手工润改了 `chapters/chap5.tex`、`chapters/chap6.tex`、`chapters/chap7.tex`、`chapters/chap8.tex` 的一批生硬句子。
- 顺手修好了 `chapters/chap4.tex` 里会卡住编译的 LaTeX 环境写法。

## 本轮主要处理

- 去掉了 `终极表达式`、`精确锁定`、`全局自由度`、`手性统一` 一类夸张说法。
- 把 `万能算子弦长公式`、`纯算子`、`算子拉格朗日恒等式` 这类术语壳压回普通几何或代数叙述。
- 把 `全局坐标系 / 全局方程 / 全局恒等式 / 局部原点 / 构型` 一类说法改成更自然的教材表述。
- `chap8.tex` 里个别过重的术语也顺了一遍，包括 `拓扑对象`。

## 复核

- 重新扫了 `chapters/chap1.tex` 到 `chapters/chap9.tex`，重点看两组词：
  - `终极|锁定|量纲分析|万能算子弦长公式|纯算子|全局自由度|手性统一|拓扑对象|全局恒等式|完全对称性|绝对代数控制|严格的多项式除法降次|转移算子链|特征不变量|代数等价性|迹不变量|斜率调整法公式`
  - `局部原点|全局坐标系|全局方程|全局不变量|全局坐标|构型`
- 这两组词在正文里复扫后都没有命中。
- 编译命令：

```powershell
latexmk -xelatex -interaction=nonstopmode -file-line-error main.tex
```

- 修完以后，`main.pdf` 可以正常生成。
- 剩下的是警告级信息，主要还是原来的 overfull boxes 和数学字体里的全角逗号缺字。

## 备注

- `chap4.tex` 原来有 `tcolorbox` 定理环境的写法问题：
  - `\begin{definition}[...]` 和 `\begin{conclusion}[...]`
  - 现已改成 `\begin{definition}{...}{}` 和 `\begin{conclusion}{...}{}`。
- `chap4.tex` 里的 `\begin{note}` / `\end{note}` 已改成 `remark`。
