# RDG2

The FEs needed by RDG2 is as same as RDG：

- $n$-dimensional fully separable problem： $3n$
- $n$-dimensional fully non-separable problem： $6n$
- $n$-dimensional partially separable problem with $n/m$ subcomponents :  $3 \times 2m \times log_2(n) \times n/m = 6nlog_2(n)$
- $n$-dimensional partially separable problem with an $m$-dimensional non-separable subcomponent： $3(n-m)+6m \times log_2(n)$
- $n$-dimensional overlapping problem： $6nlog_2(n)$

As the improved version of the RDG, RDG2 has the following major changes over its predecessor：

- Accuracy: Higher interaction detection accuracy
- Parameter-free

## The main improvement skills of RDG2

### Adaptive Threshold

The adaptive threshold value estimation mechanism of RDG2 is inspired by the DG2. However, different from DG2's variable pair detection, RDG is a set of pair detection, so there are still some small differences.

First of all, the threshold proposed by RDG is :

- Global ：RDG using only one global threshold value may be insufficient to completely identify variable interactions in a given problem with imbalanced components.
- Manually set ：RDG requires users to specify an appropriate parameter value to estimate the threshold, however this parameter is highly dependent on the structural property of the problem.

Therefore, we need a threshold that automatically adapts to local specific conditions.

According to the theory in DG2, the threshold value  $\epsilon$ obtained after analysis is：

$$
\epsilon:=\gamma_{\sqrt{n}+2}\left(\left|f\left(x_{l, l}\right)\right|+\left|f\left(x_{u, l}\right)\right|+\left|f\left(x_{l, m}\right)\right|+\left|f\left(x_{u, m}\right)\right|\right)
$$

It should be noted that here is the root n plus 2, which is different from DG2. For the specific definition of the gamma function $\gamma$ , see the paper

