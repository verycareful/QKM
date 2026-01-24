"""
Comprehensive Quantum vs Classical K-means Analysis
====================================================
This script compares:
1. Classical K-means clustering
2. Quantum K-means using SWAP Test (genuine quantum circuit)
3. Quantum K-means using Quantum Fidelity (statevector simulation)

On two datasets:
- Original ENB2012 dataset (768 samples, 10 features)
- Quantum-optimized expanded dataset (4998 samples, 16 features)
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator
from qiskit.quantum_info import Statevector
import warnings
import time
import os

warnings.filterwarnings('ignore')

# ============================================================================
# QUANTUM K-MEANS IMPLEMENTATIONS
# ============================================================================

class QuantumKMeansSwapTest:
    """
    Quantum K-means using the SWAP test for distance calculation.
    
    The SWAP test is a genuine quantum algorithm that computes the inner product
    between two quantum states using quantum interference.
    
    P(ancilla=0) = (1 + |⟨ψ₁|ψ₂⟩|²) / 2
    """
    
    def __init__(self, n_clusters=3, max_iter=10, random_state=None, shots=512):
        self.n_clusters = n_clusters
        self.max_iter = max_iter
        self.random_state = random_state
        self.shots = shots
        self.centroids = None
        self.labels_ = None
        self.inertia_ = None
        self.simulator = AerSimulator()
        
        if random_state is not None:
            np.random.seed(random_state)
    
    def _normalize_vector(self, vec):
        """Normalize vector for quantum amplitude encoding"""
        norm = np.linalg.norm(vec)
        if norm == 0:
            return np.zeros_like(vec)
        return vec / norm
    
    def _pad_vector(self, vec, target_size):
        """Pad vector to match required qubit size (must be power of 2)"""
        if len(vec) < target_size:
            padded = np.zeros(target_size)
            padded[:len(vec)] = vec
            return padded
        return vec[:target_size]
    
    def _create_swap_test_circuit(self, state1_vec, state2_vec, n_qubits):
        """
        Create a SWAP test circuit to measure similarity between two quantum states.
        """
        ancilla = QuantumRegister(1, 'ancilla')
        reg1 = QuantumRegister(n_qubits, 'reg1')
        reg2 = QuantumRegister(n_qubits, 'reg2')
        classical = ClassicalRegister(1, 'measure')
        
        qc = QuantumCircuit(ancilla, reg1, reg2, classical)
        
        state_size = 2 ** n_qubits
        padded_state1 = self._pad_vector(self._normalize_vector(state1_vec), state_size)
        padded_state2 = self._pad_vector(self._normalize_vector(state2_vec), state_size)
        
        # Ensure valid quantum states
        norm1 = np.linalg.norm(padded_state1)
        norm2 = np.linalg.norm(padded_state2)
        if norm1 > 0:
            padded_state1 = padded_state1 / norm1
        if norm2 > 0:
            padded_state2 = padded_state2 / norm2
        
        qc.initialize(padded_state1, reg1)
        qc.initialize(padded_state2, reg2)
        
        # SWAP test protocol
        qc.h(ancilla[0])
        for i in range(n_qubits):
            qc.cswap(ancilla[0], reg1[i], reg2[i])
        qc.h(ancilla[0])
        qc.measure(ancilla[0], classical[0])
        
        return qc
    
    def _quantum_inner_product(self, vec1, vec2, n_qubits):
        """Calculate quantum inner product using SWAP test."""
        swap_circuit = self._create_swap_test_circuit(vec1, vec2, n_qubits)
        job = self.simulator.run(swap_circuit, shots=self.shots)
        result = job.result()
        counts = result.get_counts()
        
        prob_0 = counts.get('0', 0) / self.shots
        inner_product_squared = max(0, 2 * prob_0 - 1)
        
        return inner_product_squared
    
    def _quantum_distance(self, vec1, vec2, n_qubits):
        """Calculate quantum-based distance between two vectors."""
        inner_prod_sq = self._quantum_inner_product(vec1, vec2, n_qubits)
        inner_prod = np.sqrt(inner_prod_sq)
        distance_squared = 2 * (1 - inner_prod)
        return np.sqrt(max(0, distance_squared))
    
    def _determine_n_qubits(self, n_features):
        """Determine number of qubits needed to encode features"""
        n_qubits = int(np.ceil(np.log2(max(n_features, 2))))
        return min(n_qubits, 6)  # Limit for simulation speed
    
    def _initialize_centroids_kmeans_plusplus(self, X):
        """Initialize centroids using k-means++ algorithm"""
        n_samples, n_features = X.shape
        centroids = np.zeros((self.n_clusters, n_features))
        centroids[0] = X[np.random.randint(n_samples)]
        
        for k in range(1, self.n_clusters):
            distances = np.array([
                min([np.linalg.norm(x - c) for c in centroids[:k]]) 
                for x in X
            ])
            distances_sq = distances ** 2
            probabilities = distances_sq / distances_sq.sum()
            next_idx = np.random.choice(n_samples, p=probabilities)
            centroids[k] = X[next_idx]
        
        return centroids
    
    def fit_predict(self, X, verbose=False):
        """Fit quantum K-means and return cluster labels."""
        n_samples, n_features = X.shape
        n_qubits = self._determine_n_qubits(n_features)
        
        self.centroids = self._initialize_centroids_kmeans_plusplus(X)
        
        for iteration in range(self.max_iter):
            # Assign clusters using quantum distance
            labels = np.zeros(n_samples, dtype=int)
            for i, point in enumerate(X):
                distances = [self._quantum_distance(point, c, n_qubits) for c in self.centroids]
                labels[i] = np.argmin(distances)
            
            # Update centroids
            new_centroids = np.zeros_like(self.centroids)
            for k in range(self.n_clusters):
                cluster_points = X[labels == k]
                if len(cluster_points) > 0:
                    new_centroids[k] = cluster_points.mean(axis=0)
                else:
                    new_centroids[k] = X[np.random.randint(len(X))]
            
            # Check convergence
            shift = np.linalg.norm(new_centroids - self.centroids)
            if shift < 1e-4:
                break
            self.centroids = new_centroids
        
        self.labels_ = labels
        self.inertia_ = sum(
            np.sum(np.linalg.norm(X[labels == k] - self.centroids[k], axis=1) ** 2)
            for k in range(self.n_clusters) if np.sum(labels == k) > 0
        )
        
        return self.labels_


class QuantumKMeansFidelity:
    """
    Quantum K-means using quantum state fidelity for distance calculation.
    Uses statevector simulation for exact fidelity computation.
    """
    
    def __init__(self, n_clusters=3, max_iter=20, random_state=None):
        self.n_clusters = n_clusters
        self.max_iter = max_iter
        self.random_state = random_state
        self.centroids = None
        self.labels_ = None
        self.inertia_ = None
        
        if random_state is not None:
            np.random.seed(random_state)
    
    def _create_state_preparation_circuit(self, data_point, n_qubits):
        """Create circuit to prepare quantum state from data"""
        state_size = 2 ** n_qubits
        
        norm = np.linalg.norm(data_point)
        if norm > 0:
            normalized = data_point / norm
        else:
            normalized = data_point
        
        padded = np.zeros(state_size)
        padded[:len(normalized)] = normalized
        padded = padded / np.linalg.norm(padded) if np.linalg.norm(padded) > 0 else padded
        
        qc = QuantumCircuit(n_qubits)
        qc.initialize(padded, range(n_qubits))
        
        return qc
    
    def _quantum_fidelity(self, vec1, vec2, n_qubits):
        """Calculate quantum state fidelity |⟨ψ₁|ψ₂⟩|²"""
        qc1 = self._create_state_preparation_circuit(vec1, n_qubits)
        qc2 = self._create_state_preparation_circuit(vec2, n_qubits)
        
        sv1 = Statevector(qc1)
        sv2 = Statevector(qc2)
        
        overlap = np.abs(np.dot(np.conj(sv1.data), sv2.data))
        fidelity = overlap ** 2
        
        return fidelity
    
    def _quantum_distance(self, vec1, vec2, n_qubits):
        """Distance based on quantum fidelity: d = sqrt(2(1-F))"""
        fidelity = self._quantum_fidelity(vec1, vec2, n_qubits)
        distance = np.sqrt(2 * (1 - fidelity))
        return distance
    
    def _determine_n_qubits(self, n_features):
        n_qubits = int(np.ceil(np.log2(max(n_features, 2))))
        return min(n_qubits, 8)
    
    def fit_predict(self, X, verbose=False):
        """Fit using quantum fidelity-based distances"""
        n_samples, n_features = X.shape
        n_qubits = self._determine_n_qubits(n_features)
        
        # Initialize centroids
        self.centroids = X[np.random.choice(n_samples, self.n_clusters, replace=False)]
        
        for iteration in range(self.max_iter):
            # Assign clusters
            labels = np.zeros(n_samples, dtype=int)
            for i, point in enumerate(X):
                distances = [self._quantum_distance(point, c, n_qubits) for c in self.centroids]
                labels[i] = np.argmin(distances)
            
            # Update centroids
            new_centroids = np.zeros_like(self.centroids)
            for k in range(self.n_clusters):
                cluster_points = X[labels == k]
                if len(cluster_points) > 0:
                    new_centroids[k] = cluster_points.mean(axis=0)
                else:
                    new_centroids[k] = self.centroids[k]
            
            shift = np.linalg.norm(new_centroids - self.centroids)
            if shift < 1e-4:
                break
            self.centroids = new_centroids
        
        self.labels_ = labels
        self.inertia_ = sum(
            np.sum(np.linalg.norm(X[labels == k] - self.centroids[k], axis=1) ** 2)
            for k in range(self.n_clusters) if np.sum(labels == k) > 0
        )
        
        return self.labels_


# ============================================================================
# ANALYSIS FUNCTIONS
# ============================================================================

def run_classical_kmeans(X, k_range, dataset_name):
    """Run classical K-means for various k values"""
    print(f"\n  Running Classical K-means on {dataset_name}...")
    results = []
    
    for k in k_range:
        start_time = time.time()
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        labels = kmeans.fit_predict(X)
        elapsed = time.time() - start_time
        
        sil_score = silhouette_score(X, labels) if len(np.unique(labels)) > 1 else 0
        
        results.append({
            'k': k,
            'silhouette': sil_score,
            'inertia': kmeans.inertia_,
            'time': elapsed
        })
        print(f"    k={k}: silhouette={sil_score:.4f}, inertia={kmeans.inertia_:.2f}, time={elapsed:.2f}s")
    
    return results


def run_quantum_swap_kmeans(X, k_range, dataset_name, sample_size=None):
    """Run Quantum K-means with SWAP test"""
    if sample_size and len(X) > sample_size:
        print(f"\n  Running Quantum SWAP Test K-means on {dataset_name} (sample={sample_size})...")
        indices = np.random.choice(len(X), sample_size, replace=False)
        X_sample = X[indices]
    else:
        print(f"\n  Running Quantum SWAP Test K-means on {dataset_name} (FULL DATA: {len(X)} samples)...")
        X_sample = X
    
    results = []
    
    for k in k_range:
        start_time = time.time()
        qkm = QuantumKMeansSwapTest(n_clusters=k, max_iter=10, random_state=42, shots=512)
        labels = qkm.fit_predict(X_sample)
        elapsed = time.time() - start_time
        
        sil_score = silhouette_score(X_sample, labels) if len(np.unique(labels)) > 1 else 0
        
        results.append({
            'k': k,
            'silhouette': sil_score,
            'inertia': qkm.inertia_,
            'time': elapsed
        })
        print(f"    k={k}: silhouette={sil_score:.4f}, inertia={qkm.inertia_:.2f}, time={elapsed:.2f}s")
    
    return results


def run_quantum_fidelity_kmeans(X, k_range, dataset_name, sample_size=None):
    """Run Quantum K-means with Fidelity"""
    if sample_size and len(X) > sample_size:
        print(f"\n  Running Quantum Fidelity K-means on {dataset_name} (sample={sample_size})...")
        indices = np.random.choice(len(X), sample_size, replace=False)
        X_sample = X[indices]
    else:
        print(f"\n  Running Quantum Fidelity K-means on {dataset_name} (FULL DATA: {len(X)} samples)...")
        X_sample = X
    
    results = []
    
    for k in k_range:
        start_time = time.time()
        qkm = QuantumKMeansFidelity(n_clusters=k, max_iter=20, random_state=42)
        labels = qkm.fit_predict(X_sample)
        elapsed = time.time() - start_time
        
        sil_score = silhouette_score(X_sample, labels) if len(np.unique(labels)) > 1 else 0
        
        results.append({
            'k': k,
            'silhouette': sil_score,
            'inertia': qkm.inertia_,
            'time': elapsed
        })
        print(f"    k={k}: silhouette={sil_score:.4f}, inertia={qkm.inertia_:.2f}, time={elapsed:.2f}s")
    
    return results


def generate_plots(results_dict, timestamp, output_dir):
    """Generate comparison plots"""
    
    # Plot 1: Silhouette Score Comparison
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Original Dataset - Silhouette
    ax1 = axes[0, 0]
    for method, results in results_dict['original'].items():
        k_vals = [r['k'] for r in results]
        sil_vals = [r['silhouette'] for r in results]
        ax1.plot(k_vals, sil_vals, marker='o', label=method)
    ax1.set_xlabel('Number of Clusters (k)')
    ax1.set_ylabel('Silhouette Score')
    ax1.set_title('Original Dataset (768×10) - Silhouette Score')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Expanded Dataset - Silhouette
    ax2 = axes[0, 1]
    for method, results in results_dict['expanded'].items():
        k_vals = [r['k'] for r in results]
        sil_vals = [r['silhouette'] for r in results]
        ax2.plot(k_vals, sil_vals, marker='o', label=method)
    ax2.set_xlabel('Number of Clusters (k)')
    ax2.set_ylabel('Silhouette Score')
    ax2.set_title('Expanded Dataset (4998×16) - Silhouette Score')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # Original Dataset - Inertia
    ax3 = axes[1, 0]
    for method, results in results_dict['original'].items():
        k_vals = [r['k'] for r in results]
        inertia_vals = [r['inertia'] for r in results]
        ax3.plot(k_vals, inertia_vals, marker='s', label=method)
    ax3.set_xlabel('Number of Clusters (k)')
    ax3.set_ylabel('Inertia')
    ax3.set_title('Original Dataset (768×10) - Inertia')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # Expanded Dataset - Inertia
    ax4 = axes[1, 1]
    for method, results in results_dict['expanded'].items():
        k_vals = [r['k'] for r in results]
        inertia_vals = [r['inertia'] for r in results]
        ax4.plot(k_vals, inertia_vals, marker='s', label=method)
    ax4.set_xlabel('Number of Clusters (k)')
    ax4.set_ylabel('Inertia')
    ax4.set_title('Expanded Dataset (4998×16) - Inertia')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plot_path = os.path.join(output_dir, f'quantum_classical_comparison_{timestamp}.png')
    plt.savefig(plot_path, dpi=150)
    plt.close()
    
    return plot_path


def generate_report(results_dict, original_shape, expanded_shape, timestamp, output_dir):
    """Generate comprehensive analysis report"""
    
    report_lines = []
    report_lines.append("=" * 80)
    report_lines.append("⚛️ QUANTUM vs CLASSICAL K-MEANS COMPREHENSIVE ANALYSIS ⚛️")
    report_lines.append("=" * 80)
    report_lines.append(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append("")
    
    report_lines.append("QUANTUM METHODS IMPLEMENTED:")
    report_lines.append("-" * 40)
    report_lines.append("1. SWAP Test (Genuine Quantum Circuit)")
    report_lines.append("   - Uses quantum interference to compute |⟨ψ₁|ψ₂⟩|²")
    report_lines.append("   - P(ancilla=0) = (1 + |⟨ψ₁|ψ₂⟩|²) / 2")
    report_lines.append("   - Amplitude encoding of classical data")
    report_lines.append("   - Controlled-SWAP operations between quantum registers")
    report_lines.append("")
    report_lines.append("2. Quantum Fidelity (Statevector Simulation)")
    report_lines.append("   - Computes quantum state fidelity F = |⟨ψ₁|ψ₂⟩|²")
    report_lines.append("   - Distance: d = √(2(1-F))")
    report_lines.append("   - Exact computation via statevector simulation")
    report_lines.append("")
    
    report_lines.append("DATASET INFORMATION:")
    report_lines.append("-" * 40)
    report_lines.append(f"Original Dataset:  {original_shape[0]} samples × {original_shape[1]} features")
    report_lines.append(f"Expanded Dataset:  {expanded_shape[0]} samples × {expanded_shape[1]} features")
    report_lines.append("")
    
    # Results for each dataset
    for dataset_name, dataset_label in [('original', 'ORIGINAL DATASET'), ('expanded', 'EXPANDED DATASET')]:
        report_lines.append("")
        report_lines.append("=" * 80)
        report_lines.append(f"{dataset_label} RESULTS")
        report_lines.append("=" * 80)
        
        for method, results in results_dict[dataset_name].items():
            report_lines.append("")
            report_lines.append(f"{method.upper()}:")
            report_lines.append("-" * 40)
            
            best_result = max(results, key=lambda x: x['silhouette'])
            
            report_lines.append(f"Best k: {best_result['k']}")
            report_lines.append(f"Best Silhouette: {best_result['silhouette']:.4f}")
            report_lines.append(f"Inertia at best k: {best_result['inertia']:.2f}")
            report_lines.append(f"Time at best k: {best_result['time']:.2f}s")
            report_lines.append("")
            report_lines.append("All k values:")
            for r in results:
                report_lines.append(f"  k={r['k']}: silhouette={r['silhouette']:.4f}, inertia={r['inertia']:.2f}, time={r['time']:.2f}s")
    
    # Comparison summary
    report_lines.append("")
    report_lines.append("=" * 80)
    report_lines.append("COMPARISON SUMMARY")
    report_lines.append("=" * 80)
    report_lines.append("")
    
    for dataset_name, dataset_label in [('original', 'Original Dataset'), ('expanded', 'Expanded Dataset')]:
        report_lines.append(f"{dataset_label}:")
        report_lines.append("-" * 40)
        
        best_results = {}
        for method, results in results_dict[dataset_name].items():
            best = max(results, key=lambda x: x['silhouette'])
            best_results[method] = best
        
        # Find overall best
        best_method = max(best_results.keys(), key=lambda m: best_results[m]['silhouette'])
        
        for method, best in best_results.items():
            marker = " ⭐ BEST" if method == best_method else ""
            report_lines.append(f"  {method}: k={best['k']}, silhouette={best['silhouette']:.4f}{marker}")
        
        report_lines.append("")
        
        # Calculate improvements
        classical_best = best_results['Classical']
        for qmethod in ['Quantum_SWAP', 'Quantum_Fidelity']:
            if qmethod in best_results:
                q_best = best_results[qmethod]
                sil_improvement = ((q_best['silhouette'] - classical_best['silhouette']) / classical_best['silhouette']) * 100
                inertia_improvement = ((classical_best['inertia'] - q_best['inertia']) / classical_best['inertia']) * 100
                
                report_lines.append(f"  {qmethod} vs Classical:")
                report_lines.append(f"    Silhouette change: {sil_improvement:+.2f}%")
                report_lines.append(f"    Inertia change: {inertia_improvement:+.2f}%")
        report_lines.append("")
    
    report_lines.append("")
    report_lines.append("=" * 80)
    report_lines.append("CONCLUSIONS")
    report_lines.append("=" * 80)
    report_lines.append("")
    report_lines.append("The quantum K-means implementations use genuine quantum computing concepts:")
    report_lines.append("- Amplitude encoding maps classical data to quantum state amplitudes")
    report_lines.append("- SWAP test uses quantum interference for inner product estimation")
    report_lines.append("- Quantum fidelity measures similarity in Hilbert space")
    report_lines.append("")
    report_lines.append("Key observations:")
    report_lines.append("- Quantum methods offer alternative distance metrics based on quantum state overlap")
    report_lines.append("- SWAP test introduces measurement noise (statistical estimation)")
    report_lines.append("- Fidelity-based method provides exact quantum overlap computation")
    report_lines.append("- Performance varies based on data structure and cluster separability")
    report_lines.append("")
    
    # Save report
    report_text = '\n'.join(report_lines)
    report_path = os.path.join(output_dir, f'quantum_classical_analysis_report_{timestamp}.txt')
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report_text)
    
    return report_path, report_text


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    print("=" * 80)
    print("⚛️ QUANTUM vs CLASSICAL K-MEANS COMPREHENSIVE ANALYSIS ⚛️")
    print("=" * 80)
    
    # Generate timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Setup paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, '..', 'data')
    output_dir = os.path.join(script_dir, '..', 'output')
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"\nTimestamp: {timestamp}")
    print(f"Output directory: {os.path.abspath(output_dir)}")
    
    # Load datasets
    print("\n" + "=" * 60)
    print("LOADING DATASETS")
    print("=" * 60)
    
    original_df = pd.read_csv(os.path.join(data_dir, 'ENB2012_data.csv'))
    expanded_df = pd.read_csv(os.path.join(data_dir, 'quantum_optimized_ENB_data.csv'))
    
    # Prepare features (exclude target columns for original dataset)
    if 'Y1' in original_df.columns:
        X_original = original_df.drop(columns=['Y1', 'Y2']).values
    else:
        X_original = original_df.values
    
    X_expanded = expanded_df.values
    
    print(f"Original dataset shape: {X_original.shape}")
    print(f"Expanded dataset shape: {X_expanded.shape}")
    
    # Standardize
    scaler_orig = StandardScaler()
    scaler_exp = StandardScaler()
    X_original_scaled = scaler_orig.fit_transform(X_original)
    X_expanded_scaled = scaler_exp.fit_transform(X_expanded)
    
    # Define k range
    k_range = range(2, 8)  # Reduced range for quantum speed
    k_range_classical = range(2, 11)  # Full range for classical
    
    # Store all results
    results_dict = {
        'original': {},
        'expanded': {}
    }
    
    # Run Classical K-means
    print("\n" + "=" * 60)
    print("RUNNING CLASSICAL K-MEANS")
    print("=" * 60)
    
    results_dict['original']['Classical'] = run_classical_kmeans(
        X_original_scaled, k_range_classical, "Original (768×10)")
    
    results_dict['expanded']['Classical'] = run_classical_kmeans(
        X_expanded_scaled, k_range_classical, "Expanded (4998×16)")
    
    # Run Quantum Fidelity K-means (faster)
    print("\n" + "=" * 60)
    print("RUNNING QUANTUM FIDELITY K-MEANS")
    print("=" * 60)
    
    results_dict['original']['Quantum_Fidelity'] = run_quantum_fidelity_kmeans(
        X_original_scaled, k_range, "Original (768×8)")  # Full data
    
    results_dict['expanded']['Quantum_Fidelity'] = run_quantum_fidelity_kmeans(
        X_expanded_scaled, k_range, "Expanded (4998×16)")  # Full data
    
    # Run Quantum SWAP Test K-means (slower, more authentic)
    print("\n" + "=" * 60)
    print("RUNNING QUANTUM SWAP TEST K-MEANS")
    print("=" * 60)
    
    results_dict['original']['Quantum_SWAP'] = run_quantum_swap_kmeans(
        X_original_scaled, k_range, "Original (768×8)")  # Full data
    
    results_dict['expanded']['Quantum_SWAP'] = run_quantum_swap_kmeans(
        X_expanded_scaled, k_range, "Expanded (4998×16)")  # Full data
    
    # Generate plots
    print("\n" + "=" * 60)
    print("GENERATING VISUALIZATIONS")
    print("=" * 60)
    
    plot_path = generate_plots(results_dict, timestamp, output_dir)
    print(f"  Plot saved: {plot_path}")
    
    # Generate report
    print("\n" + "=" * 60)
    print("GENERATING ANALYSIS REPORT")
    print("=" * 60)
    
    report_path, report_text = generate_report(
        results_dict, 
        X_original.shape, 
        X_expanded.shape, 
        timestamp, 
        output_dir
    )
    print(f"  Report saved: {report_path}")
    
    # Print summary to console
    print("\n" + report_text)
    
    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETE!")
    print("=" * 80)
    print(f"\nOutput files:")
    print(f"  - {plot_path}")
    print(f"  - {report_path}")


if __name__ == "__main__":
    main()
