# NeuroEvolution (NE) Problem Set

## Overview

The NeuroEvolution problem set provides optimization challenges for training neural network-based reinforcement learning agents on robotic control tasks. This problem set uses the [EvoX](https://github.com/EMI-Group/evox) framework's Brax physics engine integration to evaluate neural network parameters.

## Problem Description

NeuroEvolution problems involve optimizing the weights of Multi-Layer Perceptron (MLP) networks to control various robotic agents in physics-based environments. The goal is to maximize cumulative rewards over episodes by finding optimal network parameters.

### Key Features

- **11 Control Environments**: Including Ant, HalfCheetah, Hopper, Humanoid, InvertedPendulum, Reacher, Walker2D, and more
- **6 Network Architectures**: MLP structures with 0-5 hidden layers (depths)
- **66 Total Problem Instances**: Combinations of environments and network depths
- **High-Dimensional**: Problem dimensions range from ~1000D to several thousand dimensions
- **GPU-Accelerated**: Evaluation uses CUDA for efficient parallel fitness computation

## Problem Class: `NE_Problem`

### Attributes

- `env_name` (str): Name of the Brax environment
- `model_depth` (int): Number of hidden layers in the MLP
- `seed` (int): Random seed for reproducibility
- `dim` (int): Total number of network parameters
- `ub` (float): Upper bound for parameter values
- `lb` (float): Lower bound for parameter values

### Methods

- `func(x)`: Evaluates a batch of neural network parameter vectors
  - **Input**: `x` - numpy array of shape `(batch_size, dim)`
  - **Output**: Cost values (lower is better, computed as `1e5 - reward`)
  - Runs 10 episodes of length 200 for each parameter vector
  - Handles NaN/Inf values by assigning penalty cost

## Implementation Details

### Neural Network Architecture

The MLP architecture is defined in `evox_ne.py` with:
- Input layer matching environment observation space
- Hidden layers with 64 neurons each (number determined by `model_depth`)
- Output layer matching environment action space
- Tanh activation functions

### Evaluation Process

1. Convert numpy parameter array to PyTorch tensors
2. Map flat parameter vector to network weights using `ParamsAndVector` adapter
3. Evaluate policy in Brax environment for 10 episodes of 200 steps each
4. Average rewards across episodes
5. Convert rewards to costs (minimization objective)

### GPU Requirements

This problem set requires CUDA-capable GPU for evaluation. The code automatically sets the default device to CUDA during evaluation.

## References

- **Paper**: [EvoX: A Distributed GPU-accelerated Framework for Scalable Evolutionary Computation](https://ieeexplore.ieee.org/abstract/document/10499977)
- **Code**: [EvoX Brax Integration](https://github.com/EMI-Group/evox)
- **Brax Environments**: [Brax Documentation](https://evox.readthedocs.io/en/latest/examples/brax.html)

## Notes

- Problem instances are named as `{env_name}-{depth}` (e.g., "ant-3" for Ant environment with 3 hidden layers)
- Evaluation is computationally expensive due to RL episode rollouts
- The problem set is designed for large-scale optimization algorithms capable of handling high-dimensional search spaces


