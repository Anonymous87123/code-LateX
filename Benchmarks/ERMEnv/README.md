# Risk-Based Energy Resource Management (Risk-ERM)

The **Risk-Based Energy Resource Management (Risk-ERM)** problem originates from the [CEC/GECCO 2025 competition](https://gecco-2025.sigevo.org/Competition?itemId=2388).
It is a large-scale, real-world stochastic optimization problem where an **energy aggregator** must create a **24-hour day-ahead scheduling plan** while facing uncertainties in:

* Renewable generation (PV / wind)
* Load consumption
* Local electricity market prices
* Electric vehicle (EV) mobility / charging behavior

To ensure system robustness, the objective incorporates **Conditional Value-at-Risk (CVaR)** to penalize costly extreme scenarios.

> **In short:** Risk-ERM is a very high-dimensional, risk-aware, multi-scenario economic dispatch problem solved under strict function evaluation limits.

---

# 📦 Installation Requirements

The Risk-ERM problem relies on MATLAB-based simulation modules (including encrypted scenario data, fitness evaluation logic, and internal solvers).
Therefore, the **MATLAB Runtime (MCR)** *must be installed* before running this problem.

---

## 🔧 How to Install MATLAB Runtime (MCR)

1. Visit the official download page:
   [https://www.mathworks.com/products/compiler/matlab-runtime.html](https://www.mathworks.com/products/compiler/matlab-runtime.html)

2. Download the correct version:
   **MATLAB Runtime R2024a**

3. Install the Runtime following the instructions

4. Install the package by:

```shell
cd path/to/ERMEnv/ERMPackage
pip install .
```

Then, you may try testing installation by:

```shell
python -m path/to/ERMEnv/connector
```

---

## 🚀 After Installation

Once MCR is installed:

* The Risk-ERM black-box fitness function will run normally.
* The optimizer can call the evaluation module without any additional setup.
* No MATLAB license is needed.

---

## 🚩 Optimization Objective

For a candidate solution ( x ), the objective value is:

$$

OF = Z_{\text{Ex}} + \beta \cdot CVaR_\alpha

$$

Where:

* ( $ Z_{\text{Ex}} $ ): Expected operational cost over all scenarios
* ( $ CVaR_\alpha $ ): Expected cost of the worst ( $ (1-\alpha) $ ) portion of scenarios
* ( $ \alpha = 95% $ ) and ( $ \beta = 1 $ ) (full risk-aversion in the competition version)

The optimizer must **minimize** ( $ OF $ ) while respecting operational constraints.

---

## 📘 Problem Characteristics

### • **Multiple Scenarios**

The fitness evaluation is stochastic, involving **15 predefined scenarios**, including **3 extreme high-impact events**.
Evaluating one candidate solution requires:

* Running **all scenarios**
* Computing expected cost, VaR, and CVaR
* Applying penalties for constraint violations

### • **Very High Dimensionality**

Each solution represents a complete 24-hour schedule of all devices:

* Diesel and renewable generators
* 500 EVs
* 2 energy storage systems (ESS)
* 25 controllable loads (Demand Response)
* Market participation for energy import/export

Total number of decision variables per solution:

$$

570 \times 24 =  13,680\ \text{variables per individual}

$$

This makes the problem both **large-scale** and **computationally expensive**.

### • **Mixed Variable Types**

* Continuous power outputs
* Charging/discharging levels
* Binary generator on/off states
* Variables repeated for 24 time periods

### • **Black-Box Fitness Function**

The full internal formulation is hidden. The optimizer interacts through:

```text
candidate_solution → fitness_value
```

All simulation logic (constraints, scenario data, CVaR, penalties) is inside the black-box evaluator.

---

## 🔧 Function Evaluation Limit

To simulate real-world operational constraints, the problem enforces a strict evaluation budget:

$$

\text{Maximum of 5000 fitness evaluations}

$$

This forces optimizers to balance:

* exploration efficiency
* convergence speed
* solution robustness

