import math
import io
import base64
import matplotlib
# Set matplotlib to non-interactive backend to prevent threading issues in Flask
matplotlib.use('Agg') 
import matplotlib.pyplot as plt

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

def find_longest_repeating_substring(text):
    """
    Classically simulates the BHT collision memory.
    Automatically finds the LONGEST repeating substring in the text.
    """
    n = len(text)
    # Start checking from the largest possible repeating length down to 2
    for length in range(n // 2, 1, -1):
        seen_substrings = {}
        for i in range(n - length + 1):
            sub = text[i:i+length]
            if sub in seen_substrings:
                seen_substrings[sub].append(i)
            else:
                seen_substrings[sub] = [i]
                
        # If we find a collision at this length, return it immediately
        # because we are counting down from the longest possible length
        for sub, indices in seen_substrings.items():
            if len(indices) > 1:
                return sub, indices
                
    return None, []

def create_index_oracle(target_indices, num_qubits):
    """Dynamically creates the Oracle based on the collision indices."""
    oracle = QuantumCircuit(num_qubits, name="Oracle")
    for idx in target_indices:
        bin_idx = format(idx, f'0{num_qubits}b')
        for i, bit in enumerate(reversed(bin_idx)):
            if bit == '0':
                oracle.x(i)
        oracle.h(num_qubits - 1)
        if num_qubits > 1:
            oracle.mcx(list(range(num_qubits - 1)), num_qubits - 1)
        oracle.h(num_qubits - 1)
        for i, bit in enumerate(reversed(bin_idx)):
            if bit == '0':
                oracle.x(i)
    return oracle

def create_diffuser(num_qubits):
    """Creates the Grover Diffuser operator."""
    diffuser = QuantumCircuit(num_qubits, name="Diffuser")
    diffuser.h(range(num_qubits))
    diffuser.x(range(num_qubits))
    diffuser.h(num_qubits - 1)
    if num_qubits > 1:
        diffuser.mcx(list(range(num_qubits - 1)), num_qubits - 1)
    diffuser.h(num_qubits - 1)
    diffuser.x(range(num_qubits))
    diffuser.h(range(num_qubits))
    return diffuser

def run_bht_simulation(ciphertext):
    """Simulates the BHT algorithm for finding unknown repeats of unknown lengths."""
    ciphertext = ciphertext.strip().upper()
    N_chars = len(ciphertext)
    
    if N_chars < 4:
        raise ValueError("Ciphertext is too short to contain a meaningful repeating substring.")
    
    # 1. Classical Phase (Simulating BHT collision lookup)
    # Automatically finds the longest repeat without needing a length parameter
    discovered_sub, target_indices = find_longest_repeating_substring(ciphertext)
            
    if not discovered_sub:
        raise ValueError("No repeating substrings of length 2 or greater found in the ciphertext.")
        
    num_qubits = math.ceil(math.log2(N_chars))
    N_indices = 2 ** num_qubits 
    num_solutions = len(target_indices)
    
    # 2. Calculate iterations
    iterations = math.floor((math.pi / 4) * math.sqrt(N_indices / num_solutions))
    if iterations == 0:
        iterations = 1 
        
    # 3. Build the Quantum Circuit
    qc = QuantumCircuit(num_qubits, num_qubits)
    qc.h(range(num_qubits))
    qc.barrier()
    
    oracle = create_index_oracle(target_indices, num_qubits)
    diffuser = create_diffuser(num_qubits)
    
    for _ in range(iterations):
        qc.append(oracle.to_instruction(), range(num_qubits))
        qc.append(diffuser.to_instruction(), range(num_qubits))
        qc.barrier()
        
    qc.measure(range(num_qubits), range(num_qubits))
    
    # 4. Execute the Circuit
    simulator = AerSimulator()
    compiled_circuit = transpile(qc, simulator)
    job = simulator.run(compiled_circuit, shots=1024)
    result = job.result()
    counts = result.get_counts(compiled_circuit)
    
    # Sort and extract top measurements
    sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    top_measurements = sorted_counts[:num_solutions]
    measured_indices = [int(binary, 2) for binary, count in top_measurements]
    
    # 5. Visual Output
    circuit_fig = qc.draw(output='mpl', style='clifford')
    circuit_b64 = fig_to_base64(circuit_fig)
    
    plt.style.use('dark_background')
    hist_fig = plot_histogram(counts, title=f"Index Measurement Probabilities (1024 Shots)", color='#0d6efd')
    hist_b64 = fig_to_base64(hist_fig)
    
    return {
        "ciphertext": ciphertext,
        "discovered_substring": discovered_sub,
        "total_indices": N_indices,
        "solutions_found": num_solutions,
        "iterations": iterations,
        "measured_indices_quantum": measured_indices,
        "success": set(target_indices) == set(measured_indices),
        "circuit_b64": circuit_b64,
        "hist_b64": hist_b64
    }

# ==========================================
# Example Usage 
# ==========================================
if __name__ == "__main__":
    # We only provide the string. We do NOT specify the substring or the length.
    ct = "XYABZZAB" 
    
    print(f"Executing BHT Collision Search on Ciphertext: '{ct}'...")
    results = run_bht_simulation(ct)
    
    print("\n--- QUANTUM MEASUREMENT RESULTS ---")
    print(f"Collision Discovered: Substring '{results['discovered_substring']}'")
    print(f"Quantum state collapsed to indices: {results['measured_indices_quantum']}")
    print(f"Index Space Size (N): {results['total_indices']}")
    print(f"Algorithm Successful: {results['success']}")