# RDG3

The FEs needed by RDG2 is as same as RDG2：

- $n$-dimensional fully separable problem： $3n$
- $n$-dimensional fully non-separable problem： $6n$
- $n$-dimensional partially separable problem with $n/m$ subcomponents :  $3 \times 2m \times log_2(n) \times n/m = 6nlog_2(n)$
- $n$-dimensional partially separable problem with an $m$-dimensional non-separable subcomponent： $3(n-m)+6m \times log_2(n)$
- $n$-dimensional overlapping problem： $6nlog_2(n)$

As the improved version of the RDG2, RDG3 has a following major change over its predecessor：

- Clipping Control: Set an upper bound on the space size for the overlap subspace, and also set an upper bound on the space size for the subspace composed of separable variables. If it exceeds the upper bound, it will be directly cut into smaller and more spaces to ensure that each space is smaller than the upper bound.

## The main improvement skills of RDG3

### Clipping Control

<p align="center">
  <img src="https://github.com/Wukong-SCUT/pyCC/blob/main/picture/RDG3_clip.png" alt="Your Image Description" width="300">
</p>

The main idea for solving the overlapping problem is to break the linkage at shared variables, such that the level of interaction between components is low. 

RDG3 sets the upper bound on the space size for the overlap subspace $\epsilon_n$ to achieve this purpose. In order to prevent the subspace composed of separable variables from being too large, an upper bound on the space size $\epsilon_s$ is also set.

The implementation of the process that was described above:

<div align="center" style="display: flex; justify-content: center;">
  <img src="https://github.com/Wukong-SCUT/pyCC/blob/main/picture/RDG3_decomposition.png" alt="Algorithm 1 RDG" width="300">
  <img src="https://github.com/Wukong-SCUT/pyCC/blob/main/picture/RDG3_interact.png" alt="INTERACT function" width="300">
</div>

