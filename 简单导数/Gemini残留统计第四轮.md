# Gemini 残留统计第四轮

时间：2026-05-15  
范围：`chapters/chap1.tex` 至 `chapters/chap11.tex`，以及 `chapters/special.tex`

## 复扫前分布

上一轮高风险词复扫结果如下：

- `chapters/chap11.tex`：25
- `chapters/special.tex`：9
- `chapters/chap4.tex`：6
- `chapters/chap10.tex`：4
- `chapters/chap8.tex`：2
- `chapters/chap6.tex`：2
- `chapters/chap3.tex`：1
- `chapters/chap1.tex`：1

其中 `chapters/chap11.tex` 注释区单独统计为 26 处，主要集中在：

- 方法总述腔
- 口语评注腔
- “下面举一例/答案是否定的/众所周知”这类作者跳出式说明
- “回代即可/后略”这类收尾占位句

## 本轮处理

本轮继续手工清理，重点做了三件事：

- 把 `chap11.tex` 注释区中明显的 Gemini 腔压成直接叙述
- 把 `chap1.tex`、`chap8.tex`、`chap10.tex` 里偏“讲义旁白”的开场句改平
- 把 `chap3.tex`、`chap4.tex`、`chap6.tex`、`special.tex` 里零星的“怪腔总结句”改成普通数学表述

本轮实际改动文件：

- `chapters/chap1.tex`
- `chapters/chap3.tex`
- `chapters/chap4.tex`
- `chapters/chap6.tex`
- `chapters/chap8.tex`
- `chapters/chap10.tex`
- `chapters/chap11.tex`
- `chapters/special.tex`

## 复扫后结果

按以下高风险模式复扫：

`不难|思路|技巧|推广|频繁|往往|其实|下面举|常见|这个方法|这种方法|方法|答案是否定|留作|回代即可|后略|众所周知|萌新|适合当前这类题|主要原因|富有技巧性`

结果：

- 全部章节合计：0
- `chap11.tex` 注释区：0

## 说明

这一轮的目标不是机械删词，而是把明显的 AI 叙述习惯改掉。  
目前高风险残留已经清零，保留下来的叙述均为正常数学说明，不再带明显 Gemini 腔。
