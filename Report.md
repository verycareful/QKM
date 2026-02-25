# Comparative Analysis: Classical vs Quantum K-Means Clustering Algorithms

## Executive Summary

This research presents a comprehensive implementation and evaluation of **genuine quantum K-means clustering algorithms** using authentic quantum circuits executed on Qiskit simulators. We implement two quantum approaches—**SWAP Test** and **Quantum Fidelity**—and compare them against classical K-means on benchmark datasets. Our findings provide valuable insights into the current state of quantum machine learning and the challenges that must be overcome to achieve practical quantum advantage in clustering applications.

**Key Results:**
- Implemented authentic quantum circuits using SWAP test for inner product estimation
- Evaluated on 768-sample original (10 features) and 4,998-sample expanded (16 features) datasets
- Classical K-means achieved superior silhouette scores (0.39 vs 0.03 on original data)
- Quantum methods demonstrated fundamentally different distance metrics based on Hilbert space geometry

## 1. Introduction and Motivation

### 1.1 Research Objectives
This study aims to:
1. Implement **genuine quantum algorithm** simulations 
2. Provide **honest evaluation** of current quantum clustering capabilities
3. Identify **barriers to quantum advantage** in clustering tasks
4. Establish **baseline benchmarks** for future quantum hardware implementations

### 1.2 Classical K-Means Overview
Classical K-means minimizes within-cluster variance using Euclidean distance:
```
J = Σₖ Σᵢ∈Cₖ ||xᵢ - μₖ||²
```

**Strengths:**
- Fast convergence (typically O(nkdi) per iteration)
- Well-understood theoretical properties
- Highly optimized implementations available

**Limitations:**
- Sensitive to initialization
- Assumes spherical clusters
- Struggles with high-dimensional sparse data

### 1.3 Quantum Computing Potential
Quantum algorithms offer theoretical advantages through:
- **Superposition**: Parallel state exploration
- **Entanglement**: Complex correlation capture
- **Quantum Interference**: Enhanced discrimination
- **Amplitude Encoding**: Exponential data compression

## 2. Quantum Algorithm Implementations

### 2.1 SWAP Test Algorithm
The SWAP test is a fundamental quantum algorithm for computing inner products between quantum states.

**Circuit Structure:**
```
|0⟩ ──H──●──H──M     (ancilla qubit)
         │
|ψ₁⟩ ────×────       (first state register)
         │
|ψ₂⟩ ────×────       (second state register)
```

**Mathematical Foundation:**
```
P(ancilla = 0) = (1 + |⟨ψ₁|ψ₂⟩|²) / 2
```

From the measurement probability, we extract the inner product:
```
|⟨ψ₁|ψ₂⟩|² = 2 × P(0) - 1
```

**Quantum Distance Metric:**
```
d_quantum = √(2(1 - |⟨ψ₁|ψ₂⟩|))
```

### 2.2 Quantum Fidelity Algorithm
Direct computation of state fidelity via statevector simulation.

**Fidelity Definition:**
```
F(ψ₁, ψ₂) = |⟨ψ₁|ψ₂⟩|²
```

**Distance Conversion:**
```
d_fidelity = √(2(1 - F))
```

This approach provides exact fidelity computation without measurement noise.

### 2.3 Amplitude Encoding
Classical data is encoded into quantum state amplitudes:
```
|ψ⟩ = Σᵢ αᵢ|i⟩
where αᵢ = xᵢ / ||x||
```

**Properties:**
- Encodes N features using log₂(N) qubits
- Requires normalization (loses magnitude information)
- State preparation via `qc.initialize()`

## 3. Experimental Setup

### 3.1 Datasets

| Dataset | Samples | Features | Description |
|---------|---------|----------|-------------|
| Original (ENB2012) | 768 | 10 | Energy efficiency benchmark (X1-X8, Y1-Y2) |
| Expanded | 4,998 | 16 | High-dimensional synthetic data |

### 3.2 Implementation Details

| Parameter | SWAP Test | Fidelity | Classical |
|-----------|-----------|----------|-----------|
| Simulator | AerSimulator | Statevector | N/A |
| Shots | 512 | N/A | N/A |
| Max Iterations | 10 | 20 | 300 |
| Initialization | K-means++ | K-means++ | K-means++ |
| Qubits Used | 2×⌈log₂(d)⌉+1 | ⌈log₂(d)⌉ | N/A || Original Dataset Used | 10 features | 10 features | 10 features |
### 3.3 Evaluation Metrics
- **Silhouette Score**: Measures cluster cohesion and separation [-1, 1]
- **Inertia**: Sum of squared distances to centroids
- **Execution Time**: Wall-clock time per k value

## 4. Results

### 4.1 Original Dataset (768 samples × 10 features)

| Method | Best k | Silhouette | Inertia | Time |
|--------|--------|------------|---------|------|
| **Classical** | 2 | **0.3906** | 3,497.23 | 1.63s |
| Quantum Fidelity | 4 | 0.0308 | 5,493.10 | 27.23s |
| Quantum SWAP | 6 | 0.0141 | 5,476.68 | 104.83s |

**Detailed Classical Results:**
| k | Silhouette | Inertia |
|---|------------|---------|
| 2 | 0.3906 | 3,497.23 |
| 3 | 0.2947 | 3,083.50 |
| 4 | 0.2200 | 2,697.53 |
| 5 | 0.2185 | 2,454.19 |
| 6 | 0.2052 | 2,259.14 |
| 7 | 0.2097 | 2,075.38 |

**Detailed Quantum Fidelity Results:**
| k | Silhouette | Inertia |
|---|------------|---------|
| 2 | 0.0249 | 6,115.46 |
| 3 | -0.0224 | 6,109.21 |
| 4 | 0.0308 | 5,493.10 |
| 5 | 0.0301 | 5,421.26 |
| 6 | 0.0201 | 5,646.92 |
| 7 | -0.0011 | 5,464.29 |

### 4.2 Expanded Dataset (4,998 samples × 16 features)

| Method | Best k | Silhouette | Inertia | Time |
|--------|--------|------------|---------|------|
| **Classical** | 2 | **0.1494** | 66,834.80 | 0.01s |
| Quantum Fidelity | 6 | 0.0173 | 73,362.41 | 274.79s |
| Quantum SWAP | 4 | 0.0117 | 76,549.07 | 543.70s |

**Detailed Classical Results:**
| k | Silhouette | Inertia |
|---|------------|---------|
| 2 | 0.1494 | 66,834.80 |
| 3 | 0.1143 | 64,187.68 |
| 4 | 0.0662 | 61,934.84 |
| 5 | 0.0636 | 60,327.75 |
| 6 | 0.0656 | 58,576.60 |

**Detailed Quantum Fidelity Results:**
| k | Silhouette | Inertia |
|---|------------|---------|
| 2 | 0.0011 | 79,806.97 |
| 3 | 0.0111 | 78,100.39 |
| 4 | 0.0165 | 76,368.84 |
| 5 | 0.0158 | 74,908.42 |
| 6 | 0.0173 | 73,362.41 |

### 4.3 Performance Comparison Summary

| Dataset | Metric | Classical | Q-Fidelity | Q-SWAP |
|---------|--------|-----------|------------|--------|
| Original | Silhouette | **0.3906** | 0.0308 | 0.0141 |
| Original | Best k | 2 | 4 | 6 |
| Expanded | Silhouette | **0.1494** | 0.0173 | 0.0117 |
| Expanded | Best k | 2 | 6 | 4 |

## 5. Analysis and Discussion

### 5.1 Why Classical Outperformed Quantum

**1. Distance Metric Mismatch**
- Classical K-means uses **Euclidean distance** in original feature space
- Quantum methods use **fidelity-based distance** in Hilbert space
- Silhouette score is computed using Euclidean distance, favoring classical

**2. Information Loss in Amplitude Encoding**
- Normalization requirement: `|ψ⟩ = x/||x||`
- Magnitude information is lost
- Two vectors with same direction but different magnitudes become identical

**3. Simulation Overhead**
- SWAP test requires O(n×k) circuit executions per iteration
- Each circuit needs multiple shots for statistical estimation
- No quantum parallelism benefit in simulation

### 5.2 Fundamental Differences in Clustering Behavior

**Classical K-means:**
- Finds spherical clusters in Euclidean space
- Centroids are arithmetic means
- Distance based on coordinate differences

**Quantum K-means:**
- Finds clusters based on quantum state similarity
- Operates in Hilbert space geometry
- Distance based on state overlap (inner product)

### 5.3 Computational Complexity

| Operation | Classical | Quantum (Theory) | Quantum (Simulation) |
|-----------|-----------|------------------|---------------------|
| Distance Calc | O(d) | O(log d) | O(2^d) |
| Per Iteration | O(nkd) | O(nk log d) | O(nk × 2^d × shots) |
| Total | O(nkdi) | O(nki log d) | Hours for full data |

**Key Insight:** Quantum advantage requires actual quantum hardware. Simulation negates the theoretical speedup.

## 6. Technical Implementation Details

### 6.1 SWAP Test Circuit Implementation
```python
# Create SWAP test circuit
qc = QuantumCircuit(ancilla, reg1, reg2, classical)
qc.initialize(state1, reg1)  # Encode first data point
qc.initialize(state2, reg2)  # Encode second data point
qc.h(ancilla[0])             # Superposition
for i in range(n_qubits):
    qc.cswap(ancilla[0], reg1[i], reg2[i])  # Controlled-SWAP
qc.h(ancilla[0])             # Interference
qc.measure(ancilla[0], classical[0])
```

### 6.2 Quantum Fidelity Implementation
```python
# Direct fidelity computation
sv1 = Statevector(circuit1)
sv2 = Statevector(circuit2)
fidelity = |np.dot(np.conj(sv1.data), sv2.data)|²
distance = √(2(1 - fidelity))
```

### 6.3 Software Stack
- **Qiskit 1.0+**: Quantum circuit construction and simulation
- **Qiskit-Aer**: High-performance quantum simulator
- **scikit-learn**: Classical K-means and evaluation metrics
- **NumPy/Pandas**: Data processing
- **Matplotlib**: Visualization

## 7. Limitations and Challenges

### 7.1 Current Limitations
1. **Simulation bottleneck**: No speedup without real quantum hardware
2. **Encoding overhead**: State preparation dominates runtime
3. **Metric incompatibility**: Quantum distance ≠ Euclidean distance
4. **Noise sensitivity**: SWAP test statistical error accumulates

### 7.2 Barriers to Quantum Advantage
1. **NISQ hardware limitations**: Current devices have high error rates
2. **Qubit connectivity**: Limited entanglement between non-adjacent qubits
3. **Decoherence**: Quantum states decay before computation completes
4. **Classical competition**: K-means is highly optimized

## 8. Future Directions

### 8.1 Near-Term Improvements
1. **Variational quantum clustering**: Trainable quantum circuits
2. **Hybrid classical-quantum**: Use quantum for specific subroutines
3. **Custom distance metrics**: Design problems suited to quantum geometry
4. **Error mitigation**: Zero-noise extrapolation, probabilistic error cancellation

### 8.2 Hardware Requirements for Quantum Advantage
- **Logical qubits**: 50-100 error-corrected qubits
- **Gate fidelity**: >99.9% two-qubit gate fidelity
- **Coherence time**: Milliseconds for complex circuits
- **Connectivity**: All-to-all or efficient routing

### 8.3 Alternative Quantum Approaches
1. **Quantum annealing**: D-Wave systems for optimization
2. **Quantum kernel methods**: Quantum-enhanced SVM/kernel K-means
3. **Quantum neural networks**: Variational classifiers
4. **Grover-enhanced search**: Speedup for nearest neighbor queries

## 9. Conclusions

### 9.1 Key Findings
1. **Genuine quantum implementation achieved**: Successfully implemented SWAP test and fidelity-based quantum K-means using authentic quantum circuits
2. **Classical superiority confirmed**: For standard clustering metrics, classical K-means significantly outperforms current quantum approaches
3. **Different problem geometry**: Quantum methods optimize in Hilbert space, not Euclidean space
4. **Simulation limits quantum benefit**: True advantage requires fault-tolerant quantum hardware

### 9.2 Contributions
- Open-source implementation of quantum K-means with SWAP test
- Honest benchmarking against classical methods
- Analysis of why quantum advantage is not yet achievable
- Roadmap for future quantum clustering research

### 9.3 Final Remarks
This research demonstrates that while quantum K-means can be implemented using genuine quantum circuits, achieving practical quantum advantage in clustering remains an open challenge. The fundamental difference between Euclidean and Hilbert space geometries, combined with simulation overhead, currently favors classical approaches. However, this work establishes important baselines and identifies specific areas where future quantum hardware and algorithm improvements may eventually provide benefits.

---

## References

1. Lloyd, S., Mohseni, M., & Rebentrost, P. (2013). Quantum algorithms for supervised and unsupervised machine learning. arXiv:1307.0411
2. Buhrman, H., et al. (2001). Quantum Fingerprinting. Physical Review Letters, 87(16).
3. Kerenidis, I., & Prakash, A. (2017). Quantum Recommendation Systems. arXiv:1603.08675
4. Schuld, M., & Petruccione, F. (2018). Supervised Learning with Quantum Computers. Springer.
5. Qiskit Development Team. (2024). Qiskit: An Open-source Framework for Quantum Computing.

---

**Generated:** January 25, 2026  
**Analysis Runtime:** ~1.5 hours (full dataset evaluation)  
**Author:** Sricharan (github.com/verycareful)

*This report presents an honest evaluation of quantum K-means clustering, acknowledging both the theoretical promise and current practical limitations of quantum machine learning.*