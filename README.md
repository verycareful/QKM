# Quantum K-Means Clustering
<!-- Language -->
[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
<!-- Quantum stack -->
[![Qiskit](https://img.shields.io/badge/Qiskit-1.0+-6929C4?style=flat-square&logo=qiskit&logoColor=white)](https://qiskit.org/)
[![Qiskit Aer](https://img.shields.io/badge/Qiskit%20Aer-simulator-6929C4?style=flat-square&logo=qiskit&logoColor=white)](https://qiskit.github.io/qiskit-aer/)
<!-- Scientific stack -->
[![NumPy](https://img.shields.io/badge/NumPy-013243?style=flat-square&logo=numpy&logoColor=white)](https://numpy.org/)
[![pandas](https://img.shields.io/badge/pandas-150458?style=flat-square&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=flat-square&logo=scikitlearn&logoColor=white)](https://scikit-learn.org/)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-11557C?style=flat-square)](https://matplotlib.org/)
<!-- Publication -->
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.18802705.svg)](https://doi.org/10.5281/zenodo.18802705)
<!-- Project -->
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://www.apache.org/licenses/LICENSE-2.0)
[![Status: Archived](https://img.shields.io/badge/Status-Archived-lightgrey?style=flat-square)](.)

> **A genuine quantum computing implementation of K-Means clustering using SWAP test and quantum fidelity-based distance metrics.**

## Paper

The accompanying research paper is archived on Zenodo under the CC BY-NC 4.0 license:

> Sricharan, "Comparative Analysis of Classical and Quantum K-Means Clustering: SWAP Test and Fidelity-Based Approaches on Benchmark Datasets," Feb 2026. DOI: [10.5281/zenodo.18802705](https://doi.org/10.5281/zenodo.18802705)

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
| Original (ENB2012) | 768 | 10 | Energy efficiency benchmark (X1-X8 + Y1-Y2) |
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

Copyright © 2026 Sricharan Suresh (github.com/verycareful)

This project is licensed under the **[Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0)**.
You may use, modify, and distribute this software in accordance with Apache 2.0 terms.

See the [LICENSE](LICENSE) file for full text and [NOTICE](NOTICE) for attribution information.
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
