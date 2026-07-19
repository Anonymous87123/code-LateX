`requested_output=CLEAN; effective_output=PATCH`

文件/章节：`course_before.tex` / 判断方法
定位锚点：首段开头
来源角色：author
决策：DELETE
改前：
```tex
值得注意的是，遇到这类题目时必须牢记公式。
```
改后：删除
文风理由：删除空重点壳和单纯要求记忆的教练式表达。

文件/章节：`course_before.tex` / 判断方法
定位锚点：首段第二句
来源角色：author
决策：UNRESOLVED
改前：
```tex
若已知速度随时间减小，就可以直接套用匀变速公式。
```
改后：原样保留
文风理由：该句允许直接套用公式，与后文的条件限制形成正反许可；纯文风润色不能裁决两者。

文件/章节：`course_before.tex` / 判断方法
定位锚点：首段结尾
来源角色：author
决策：DELETE
改前：
```tex
这个结论具有重要意义，能够为后续学习奠定基础。
```
改后：删除
文风理由：删除泛化意义评价和无具体信息的后续桥接。

文件/章节：`course_before.tex` / 判断方法
定位锚点：公式后的条件判断
来源角色：author
决策：UNRESOLVED
改前：
```tex
先确认题目给出的量是否满足匀变速条件，再判断公式中的加速度方向；若条件不满足，不能因为公式看起来相似就直接代入。
```
改后：原样保留
文风理由：该句限制直接代入，与首段许可相冲突，需先确认原稿究竟采用哪一项条件。

未列入补丁的标题、公式环境及“不要只看公式的形式。”均原样保留。`patch_hunks_source_partition=NON_OVERLAPPING`。

配置：`REWRITE / COURSE / BALANCED / CLEAN`，无作者样本，不声称复现个人文风。机械验证未运行；未评估学术正确性。
