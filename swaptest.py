import io
import base64
import matplotlib
# Set matplotlib to non-interactive backend
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
import numpy as np

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram

def fig_to_base64(fig):
    """Converts a matplotlib figure to a base64 string for HTML embedding."""
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight', facecolor='#212529')
    buf.seek(0)
    b64_str = base64.b64encode(buf.getvalue()).decode('utf-8')
    plt.close(fig)
    return b64_str

def run_swap_test(lang1, ciph1, lang2, ciph2):
    # The inputs act as probability weights. We must convert them to valid amplitudes.
    # A valid quantum state vector requires that |a|^2 + |b|^2 = 1.
    norm1 = np.sqrt(lang1**2 + ciph1**2)
    norm2 = np.sqrt(lang2**2 + ciph2**2)
    
    if norm1 == 0 or norm2 == 0:
        raise ValueError("State probabilities cannot both be zero.")
        
    psi_1 = [lang1 / norm1, ciph1 / norm1]
    psi_2 = [lang2 / norm2, ciph2 / norm2]
    
    # Qubit 0 = ancilla, Qubit 1 = state 1, Qubit 2 = state 2
    qc = QuantumCircuit(3, 1)
    
    # Initialize states[cite: 4]
    qc.initialize(psi_1, 1)
    qc.initialize(psi_2, 2)
    
    # SWAP Test Circuit logic[cite: 4]
    qc.h(0)
    qc.cswap(0, 1, 2)
    qc.h(0)
    
    # Measure the ancilla[cite: 4]
    qc.measure(0, 0)
    
    # Run Simulation[cite: 4]
    sim = AerSimulator()
    compiled_circuit = transpile(qc, sim)
    result = sim.run(compiled_circuit, shots=8192).result()
    counts = result.get_counts(compiled_circuit)
    
    # Compute Similarity[cite: 4]
    p0 = counts.get('0', 0) / 8192
    similarity = 2 * p0 - 1
    
    # Visual Output Generation
    circuit_fig = qc.draw(output='mpl', style='clifford')
    circuit_b64 = fig_to_base64(circuit_fig)
    
    plt.style.use('dark_background')
    hist_fig = plot_histogram(counts, title="Measurement Probabilities (8192 Shots)", color='#0d6efd')
    hist_b64 = fig_to_base64(hist_fig)
    
    return {
        "similarity": round(similarity*100, 4),
        "p0": round(p0, 4),
        "psi_1": [round(val, 4) for val in psi_1],
        "psi_2": [round(val, 4) for val in psi_2],
        "circuit_b64": circuit_b64,
        "hist_b64": hist_b64
    }