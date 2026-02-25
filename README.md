# Quantum K-Means Clustering

[![License](https://img.shields.io/badge/License-Proprietary-red.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![Qiskit](https://img.shields.io/badge/Qiskit-1.0+-purple.svg)](https://qiskit.org)

> **A genuine quantum computing implementation of K-Means clustering using SWAP test and quantum fidelity-based distance metrics.**

## Overview

This project implements **authentic quantum K-Means clustering algorithms** that leverage fundamental quantum computing principles:

- **SWAP Test** - Uses quantum interference to compute inner products between quantum states
- **Quantum Fidelity** - Measures similarity in Hilbert space via statevector simulation
- **Amplitude Encoding** - Maps classical data to quantum state amplitudes

Unlike pseudo-quantum implementations, this project uses **real quantum circuits** executed on Qiskit's quantum simulators.

## Key Features

| Feature | Description |
|---------|-------------|
| **Genuine Quantum Circuits** | Real SWAP test implementation with controlled-SWAP operations |
| **Multiple Distance Metrics** | Quantum fidelity and SWAP-based inner product estimation |
| **Amplitude Encoding** | Efficient classical-to-quantum data mapping |
| **Comparative Analysis** | Side-by-side classical vs quantum performance evaluation |
| **Scalable Design** | Works with datasets from hundreds to thousands of samples |

## Quantum Algorithms Implemented

### SWAP Test
The SWAP test computes the quantum inner product |⟨ψ₁|ψ₂⟩|² using quantum interference:

```
P(ancilla=0) = (1 + |⟨ψ₁|ψ₂⟩|²) / 2
```

**Circuit Structure:**
```
|0⟩ ──H──●──H──M
         │
|ψ₁⟩ ────×────
         │
|ψ₂⟩ ────×────
```

### Quantum Fidelity
Direct computation of state fidelity F = |⟨ψ₁|ψ₂⟩|² with distance:
```
d = √(2(1-F))
```

## Datasets

| Dataset | Samples | Features | Description |
|---------|---------|----------|-------------|
| Original (ENB2012) | 768 | 8 | Energy efficiency benchmark |
| Quantum-Optimized | 4,998 | 16 | High-dimensional expanded dataset |

## Quick Start

### Prerequisites
```bash
pip install numpy pandas scikit-learn matplotlib qiskit qiskit-aer
```

### Run Analysis
```bash
cd code
python comprehensive_quantum_classical_analysis.py
```

### Generate Quantum Dataset
```bash
python create_quantum_optimized_dataset.py
```

## Project Structure

```
quantum-kmeans/
├── code/
│   ├── comprehensive_quantum_classical_analysis.py  # Main analysis script
│   └── create_quantum_optimized_dataset.py          # Dataset generator
├── data/
│   ├── ENB2012_data.csv                             # Original dataset
│   └── quantum_optimized_ENB_data.csv               # Expanded dataset
├── output/
│   ├── quantum_classical_analysis_report_*.txt      # Analysis reports
│   └── quantum_classical_comparison_*.png           # Visualization plots
├── README.md
├── LICENSE
└── Report.md                                        # Detailed research report
```

## Sample Results

### Classical vs Quantum Performance

| Dataset | Method | Best k | Silhouette Score |
|---------|--------|--------|------------------|
| Original (768×8) | Classical K-Means | 2 | 0.391 |
| Original (768×8) | Quantum SWAP Test | 2 | varies |
| Original (768×8) | Quantum Fidelity | 2 | varies |
| Expanded (4998×16) | Classical K-Means | 2 | 0.149 |
| Expanded (4998×16) | Quantum SWAP Test | 2 | varies |
| Expanded (4998×16) | Quantum Fidelity | 4 | varies |

## Technical Details

### Quantum Encoding
Classical data points are encoded into quantum states using **amplitude encoding**:

```python
|ψ⟩ = Σᵢ αᵢ|i⟩  where αᵢ = normalized_feature_i
```

This allows encoding N features using only log₂(N) qubits.

### Distance Computation
Quantum distance between encoded states:

```python
quantum_distance = √(2(1 - |⟨ψ₁|ψ₂⟩|))
```

### K-Means++ Initialization
Uses intelligent centroid initialization for better convergence.

## Limitations

- **Simulation Overhead**: Quantum circuits run on simulators, not actual quantum hardware
- **Scalability**: SWAP test requires O(n×k) circuit executions per iteration
- **Noise**: Statistical estimation introduces measurement uncertainty

## Future Work

- [ ] Implementation on IBM Quantum hardware
- [ ] Variational quantum eigensolver (VQE) integration
- [ ] Quantum error correction
- [ ] Hybrid classical-quantum optimization

## License

This project is **proprietary software**. See [LICENSE](LICENSE) for details.

**© 2026 All Rights Reserved**

Unauthorized copying, modification, distribution, or use of this software is strictly prohibited without explicit written permission from the author.

## References

1. Quantum K-means algorithm - Lloyd, S., Mohseni, M., & Rebentrost, P. (2013)
2. SWAP test for quantum states - Buhrman, H., et al. (2001)
3. Qiskit Documentation - IBM Quantum

## Author

**Sricharan**

---

<p align="center">
  <i>Exploring the intersection of quantum computing and machine learning</i>
</p>
