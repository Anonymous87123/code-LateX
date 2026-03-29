# RDG

The FEs needed by RDG：

- $n$-dimensional fully separable problem： $3n$
- $n$-dimensional fully non-separable problem： $6n$
- $n$-dimensional partially separable problem with $n/m$ subcomponents :  $3 \times 2m \times log_2(n) \times n/m = 6nlog_2(n)$
- $n$-dimensional partially separable problem with an $m$-dimensional non-separable subcomponent： $3(n-m)+6m \times log_2(n)$
- $n$-dimensional overlapping problem： $6nlog_2(n)$

The major ideas of RDG：

- Use checking for variable interactions between disjoint sets instead of checking for pairs of variables
- Use a **recursive method** to check the interaction of variable pairs based on the method of checking disjoint sets.

## The main skills of RDG

###  Checking for variable interactions between disjoint sets

The previous paper's definition of additive separability is：

*Definition 1：* A function is partially additively separable if it has the following general form:

$$
f(\mathbf{x})=\sum_{i=1}^{m} f_{i}\left(\mathbf{x}_{i}\right), m>1
$$

where $f_i(\cdot )$ is a non-separable subfunction, and $m$ is the number of non-separable components of $f$.

This paper gives an equivalent definition to facilitate analysis combined with mathematical theory.

*Definition 2：* Let $f: \mathbb{R}^{n} \rightarrow \mathbb{R}$ be a differentiable function. Decision variables $x_{1}$ and $x_{2}$ don’t have the indirect interaction if $f(\mathbf{x})$ holds the following condition：

$$
\frac{\partial^{2} f\left(\mathbf{x}\right)}{\partial x_{1} \partial x_{2}} = 0
$$

Then the $f$ is additively separable with respect to $x_1$ and $x_2$ , with has the general form：


$$
f(\mathbf{x})=f_{1}\left(X_{1}\right) + f_{2}\left(X_{2}\right)
$$


where $X_{1}$ is the set containing variable  $x_1$ and $X_{2}$ is the set containing variable $x_2$. 

This paper extends the interaction check between two variables to the interaction check between two sets.

$X_{1} = \left\[ x_{1,1}, \ldots, x_{1,p} \right\]$ and $X_{2}=\left\[x_{2,1}, \ldots, x_{2, p}\right\]$ are two mutually exclusive subsets of decision variables. $u^1$ and $u^2$ are the $n$-dimensional unit vectors of the two subsets respectively. If $x_{j,i} \notin \mathbf{X}_{j}$ , $u^j_i = 0$. 

*Definition 3 :* If $f(\mathbf{x})$ holds the following condition：

$$
\sum_{i=1}^{p} \sum_{j=1}^{q} \frac{\partial^{2} f\left(\mathbf{x}^{*}\right)}{\partial x_{1, i} \partial x_{2, j}} u_{1, i}^{1} u_{2, j}^{2} \neq 0
$$

there is some interaction between decision variables in $X_{1}$ and $X_{2}$

According to the equivalence of line integral and inverse proposition, we can get the following results :

$$
f\left(\mathbf{x}+l_{1} \mathbf{u}^{1}+l_{2} \mathbf{u}^{2}\right)-f\left(\mathbf{x}+l_{2} \mathbf{u}^{2}\right) \neq f\left(\mathbf{x}+l_{1} \mathbf{u}^{1}\right)-f\left(\mathbf{x}\right) \Leftrightarrow \sum_{i=1}^{p} \sum_{j=1}^{q} \frac{\partial^{2} f\left(\mathbf{x}^{*}\right)}{\partial x_{1, i} \partial x_{2, j}} u_{1, i}^{1} u_{2, j}^{2} \neq 0
$$

where $l_1$ and $l_2$ are two real numbers. 

In fact, this is an obvious conclusion. Even in the DG series, the essence of the formula to check the interaction of variables is the control variable method. In other words, when variable one changes, will variable two affect the change in fitness caused by variable one? Think about it, the essence of partial derivatives is this: whether the change in variable one is affected by the change in variable two. 

Therefore we can use the following equation to directly check whether there is an interaction between two disjoint sets：

$$
f\left(\mathbf{x}+l_{1} \mathbf{u}^{1}+l_{2} \mathbf{u}^{2}\right)-f\left(\mathbf{x}+l_{2} \mathbf{u}^{2}\right) \neq f\left(\mathbf{x}+l_{1} \mathbf{u}^{1}\right)-f\left(\mathbf{x}\right)
$$

### A recursive method to check the interaction of variable pairs

<p align="center">
  <img src="https://github.com/Wukong-SCUT/pyCC/blob/main/picture/RDG_roadmap.png" alt="Your Image Description" width="600">
</p>

The above figure gives a roadmap for a recursive check. First we have a set $X_1$ and the complement of $X_1$ in n-dimensional decision space $X_2$. If it is detected that there is an interaction between the two collections, $X_2$ is split in half into two subsets. 

If there is no interaction between some subsets and $X_1$, then all variables in these subsets will no longer be checked. The subset with interaction continues to be split until the subset has only one element. If there is still interaction, it is merged into $X_1$ and removed from $X_2$. 

At this time,  and $X_2$ have been updated. Repeat the above process until there is no interaction between $X_1$ and $X_2$. In general, the above process can check out all the variables that interact directly and indirectly with $X_1$ (we set up only one variable in it at the beginning). 

After the above process is completed, clear $X_1$, extract the first variable in $X_2$ and add it to $X_1$, and eliminate the variables in $X_2$ at the same time.

The implementation of the process that was described above：

<div align="center" style="display: flex; justify-content: center;">
  <img src="https://github.com/Wukong-SCUT/pyCC/blob/main/picture/RDG.png" alt="Algorithm 1 RDG" width="300">
  <img src="https://github.com/Wukong-SCUT/pyCC/blob/main/picture/RDG_interact.png" alt="INTERACT function" width="300">
</div>

## Noteworthy points

1. RDG cannot interact directly and indirectly respectively. Therefore, the overlap problem cannot be dealt with.
2. RDG is quite sensitive to thresholds, and there is room for improvement in the way the threshold is determined in the paper. **If you find something unrecognizable, you can adjust the alpha value.**

