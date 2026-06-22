# 批次 002 复核记录

## 批次范围

- 全局序号：`11-40`
- 源码范围：`elegantbook2.tex` 第二节至第六节习题
- 题型：一次式积分、一次根式积分、`x^2\pm a^2`、`ax^2+b`、一般二次式积分

## 整改状态

本批次已完成主端整改：

- 将过长行内公式、连等式和分情况公式拆为 `align*`、`\[...\]` 或 `cases`。
- 一次式题统一使用 `u=ax+b` 口径，并显式写出 `a\neq0`。
- 一次根式题统一使用 `y=\sqrt{ax+b}` 口径，列出 `y^2=ax+b`、`x=(y^2-b)/a`、`dx=2y/a\,dy`。
- 所有依赖 `1/b` 的结论补出 `b\neq0` 使用条件，并补 `b=0` 的直接积分退化式。
- 第 26 题改用 `d(y/(y^2-b))` 的微分恒等式重建推导链，消除原中间推导不闭合问题。
- `ax^2+b` 基本母式补齐 `b>0`、`b<0`、`b=0` 三类。
- 一般二次式积分统一使用 `\Delta=b^2-4ac`，补齐 `\Delta=0` 重根情形。

## 主端数学核验

已用符号求导与关系式检查核验本批重点公式。结果：

- `b=0` 退化式：全局 `15、16、19、25、26、32、35、36、37、38、39` 抽检均回到原 integrand。
- 根式多项式结果：全局 `20-24` 抽检均回到原 integrand。
- 非退化母式关系：全局 `15、16、19、26、35、36、37、38` 的 `b\neq0` 公式或引用关系抽检均闭合。
- `x^2\pm a^2` 与一般二次式重点式：全局 `29、31、39` 抽检通过。

## 主端源码与编译核验

已检查本批当前源码窗口：

- `\begin{solution}` / `\end{solution}`：`30 / 30`
- `\begin{align*}` / `\end{align*}`：`38 / 38`
- `\begin{itemize}` / `\end{itemize}`：`1 / 1`
- `\begin{cases}` / `\end{cases}`：`1 / 1`
- 未发现 `align*` 末行多余换行残留。
- 未发现本批范围内长度超过阈值的数学长行。

已运行：

```powershell
latexmk -xelatex -interaction=nonstopmode -halt-on-error elegantbook2.tex
```

结果：通过，`elegantbook2.pdf` 已生成，共 `670` 页。

日志扫描：

- `LaTeX Error`：无命中
- `Undefined control sequence`：无命中
- `Emergency stop`：无命中
- `Overfull \hbox`：无命中

## PDF 版面核验

使用 `pdftotext` 定位本批 PDF 物理页约为 `83-94`，并使用 `pdftoppm` 渲染：

```powershell
pdftoppm -png -r 120 -f 83 -l 94 elegantbook2.pdf tmp\pdfs\batch002_page
```

人工查看 `tmp/pdfs/batch002_page-083.png` 至 `tmp/pdfs/batch002_page-094.png`：

- 本批新增长公式未见压边、重叠或强行挤压。
- 第 25 题三分支 `cases` 排版正常。
- 第 26 题恒等式推导与 `b=0` 退化公式排版正常。
- 第 32 题三类 `b` 分支排版正常。
- 第 39 题 `\Delta>0`、`\Delta<0`、`\Delta=0` 三分支排版正常。
- 第 94 页下半部已进入第 003 批，仍存在压缩题解问题，留待下一批处理。

## 当前批次结论

- 主端整改：通过
- 主端数学核验：通过
- 主端源码结构核验：通过
- XeLaTeX 编译：通过
- PDF 版面抽查：通过
- 批次放行：已放行

## 后续动作

立即进入第 003 批全局 `41-82`，按已形成的 `batch_003_confirmation.md` 台账直接整改，不再停留在纯审计阶段。
