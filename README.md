# LSGO-platform
This library is a platform of Large Scale Global Optimization (LSGO)

# Review

A review of the recent use of Differential Evolution for Large-Scale Global Optimization: An analysis of selected algorithms on the CEC 2013 LSGO benchmark suite (2019)

Large‑scale evolutionary optimization: a survey and experimental comparative study (2020)

A review of population-based metaheuristics for large-scale black-box global optimization (2022)

# Benchmark

|Benchmark|Paper Link|Version|
|:-:|:-:|:-:|
|cec2013lsgo|Li X, Tang K, Omidvar M N, et al. "[**Benchmark functions for the CEC 2013 special session and competition on large-scale global optimization**](https://al-roomi.org/multimedia/CEC_Database/CEC2015/LargeScaleGlobalOptimization/CEC2015_LargeScaleGO_TechnicalReport.pdf)". (2013). |[Original code](https://github.com/dmolina/cec2013lsgo),[Python Efficient Parallel Version](https://github.com/Wukong-SCUT/cec2013lsgo_TEP)|

# Cooperative Co-evolution (CC)

## Static Decomposition
Static decomposition involves a one-time random decomposition, with each subgroup independently optimized and then combined to form the final optimization result.

| Strategy     | Paper Link | Year | Description |
| ----------- | ----------- |---------|----------|
| CCGA      | A Cooperative Coevolutionary Approach to Function Optimization|  1994 | The first decomposition strategy|
| CPSO  |A Cooperative Approach to Particle Swarm Optimization         | 2004 | $𝑘-𝑠$ dimensional decomposition|
| CCDE  |Cooperative Co-evolutionary Differential Evolution for Function Optimization             | 2005 | Bipartite decomposition|


## Statistic-based Decomposition
Statistic-based Decomposition aiming mitigate the issues inherent in static decomposition by capturing problem structure and variable interactions, with multiple rounds of decomposition before forming the final optimization result.

## Random Decomposition (RD)
| Strategy     | Paper Link | Year | Description |
| ----------- | ----------- |---------|----------|
| FEPCC | Scaling up fast evolutionary programming with cooperative coevolution | 2001 | |
| DECC-G | Large scale evolutionary optimization using cooperative coevolution |   2008         |Introduce the random decomposition scheme |
| MLCC |Cooperative Co-evolution for Large Scale Optimization Through More frequent Random Grouping        |   2010   |Self-adaptation of the subcomponent sizes|


## Strategie Based On Variable Interactions

### Variable Interaction Learning (VIL)
**Theory:** linkage identification by non-monotonicity detection (LIMD)

**Paper:** Linkage Identification by Non-monotonicity Detection for Overlapping Functions (1999)

**Author** Masaharu Munetomo，David E. Goldberg


| Strategy     | Paper Link | Year | Description |
| ----------- | ----------- |---------|----------|
| CCVIL | Large-Scale Global Optimization Using Cooperative Coevolution with Variable Interaction Learning | 2010 | Propose the VIL based on LIMD |
| SVIL | A cooperative particle swarm optimizer with statistical variable interdependence learning |   2012         | |
| FVIL |Cooperative differential evolution with fast variable interdependence learning and cross-cluster mutation |   2015   |Propose a generalized version of the monotonicity check|

### Finite Differences (FD)
**Theory:** linkage identification by nonlinearity check (LINC)

**Paper:** Identifying Linkage by Nonlinearity Check （1998）

**Author** Masaharu Munetomo，David E. Goldberg

| Strategy     | Paper Link | Year | Description |
| ----------- | ----------- |---------|----------|
| DG | Cooperative Co-Evolution With Differential Grouping for Large Scale Optimization | 2014 |  |
| XDG |Extended Differential Grouping for Large Scale Global Optimization with Direct and Indirect Variable Interactions | 2015 |  |
| GDG |A Competitive Divide-and-Conquer Algorithm for Unconstrained Large-Scale Black-Box Optimization |   2016         | |
| gDG |Cooperative Co-evolution with Graph-based Differential Grouping for Large Scale Global Optimization|   2016   ||
| [DG2](https://github.com/Wukong-SCUT/pyCC/tree/main/FD/DG2) |DG2: A Faster and More Accurate Differential Grouping for Large-Scale Black-Box Optimization|   2017   | The parameter-free and efficiency-improving method of DG|
| DIAT |A Global Information Based Adaptive Threshold for Grouping Large Scale Optimization Problems|   2018   ||
| [RDG](https://github.com/Wukong-SCUT/pyCC/tree/main/FD/RDG) |A Recursive Decomposition Method for Large Scale Continuous Optimization|   2018   |Propose the recursive decomposition method of DG |
| [RDG2](https://github.com/Wukong-SCUT/pyCC/tree/main/FD/RDG2) |Adaptive Threshold Parameter Estimation with Recursive Differential Grouping for Problem Decomposition|   2018   |The parameter-free method of RDG|
| [RDG3](https://github.com/Wukong-SCUT/pyCC/tree/main/FD/RDG3) |Decomposition for Large-scale Optimization Problems with Overlapping Components|   2019   |The clipping control for the overlapping components of RDG2|
| DGSC |Differential Grouping with Spectral Clustering for Large Scale Global Optimization|   2019   ||
| ERDG |An Efficient Recursive Differential Grouping for Large-Scale Continuous Problems| 2021 ||

## Non-Decomposition Algorithms (NDAs)
