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

def char_to_int(c):
    return ord(c.upper()) - ord('A')

def int_to_char(i):
    return chr(i + ord('A'))

def create_oracle(target_key_bin, num_qubits):
    oracle = QuantumCircuit(num_qubits, name="Oracle")
    for i, bit in enumerate(reversed(target_key_bin)):
        if bit == '0':
            oracle.x(i)
            
    oracle.h(num_qubits - 1)
    oracle.mcx(list(range(num_qubits - 1)), num_qubits - 1)
    oracle.h(num_qubits - 1)
    
    for i, bit in enumerate(reversed(target_key_bin)):
        if bit == '0':
            oracle.x(i)
            
    return oracle

def create_diffuser(num_qubits):
    diffuser = QuantumCircuit(num_qubits, name="Diffuser")
    diffuser.h(range(num_qubits))
    diffuser.x(range(num_qubits))
    
    diffuser.h(num_qubits - 1)
    diffuser.mcx(list(range(num_qubits - 1)), num_qubits - 1)
    diffuser.h(num_qubits - 1)
    
    diffuser.x(range(num_qubits))
    diffuser.h(range(num_qubits))
    
    return diffuser

def fig_to_base64(fig):
    """Converts a matplotlib figure to a base64 string for HTML embedding."""
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight', facecolor='#212529') # Matches dark theme
    buf.seek(0)
    b64_str = base64.b64encode(buf.getvalue()).decode('utf-8')
    plt.close(fig)
    return b64_str

def run_bruteforce(plaintext, ciphertext):
    pt = plaintext.strip().upper()
    ct = ciphertext.strip().upper()
    
    if not pt or not ct:
        raise ValueError("Plaintext and ciphertext cannot be empty.")
    if len(pt) != len(ct):
        raise ValueError("Plaintext and ciphertext must be of equal length.")
        
    valid_chars = set("ABCD")
    if not all(c in valid_chars for c in pt) or not all(c in valid_chars for c in ct):
        raise ValueError("For this toy demonstration, please only use characters A, B, C, and D.")

    # 1. Classical target calculation
    target_key_ints = [(char_to_int(c) - char_to_int(p)) % 4 for p, c in zip(pt, ct)]
    target_key_chars = "".join([int_to_char(i) for i in target_key_ints])
    target_key_bin = "".join([format(i, '02b') for i in target_key_ints])
    num_qubits = len(target_key_bin)
    
    # 2. Iteration calculation
    N = 2 ** num_qubits
    iterations = math.floor((math.pi / 4) * math.sqrt(N))
    
    # 3. Circuit construction
    qc = QuantumCircuit(num_qubits, num_qubits)
    qc.h(range(num_qubits))
    qc.barrier()
    
    oracle = create_oracle(target_key_bin, num_qubits)
    diffuser = create_diffuser(num_qubits)
    
    for _ in range(iterations):
        qc.append(oracle.to_instruction(), range(num_qubits))
        qc.append(diffuser.to_instruction(), range(num_qubits))
        qc.barrier()
        
    qc.measure(range(num_qubits), range(num_qubits))
    
    # 4. Execution
    simulator = AerSimulator()
    compiled_circuit = transpile(qc, simulator)
    job = simulator.run(compiled_circuit, shots=1024)
    result = job.result()
    counts = result.get_counts(compiled_circuit)
    
    measured_bin = max(counts, key=counts.get)
    
    # Decode dynamically for any key length
    found_key = ""
    for i in range(0, len(measured_bin), 2):
        chunk = measured_bin[i:i+2]
        found_key += int_to_char(int(chunk, 2))
        
    # 5. Visual Generation
    circuit_fig = qc.draw(output='mpl', style='clifford')
    circuit_b64 = fig_to_base64(circuit_fig)
    
    # Customize histogram for dark mode
    plt.style.use('dark_background')
    hist_fig = plot_histogram(counts, title="Measurement Probabilities (1024 Shots)", color='#0d6efd')
    hist_b64 = fig_to_base64(hist_fig)
    
    return {
        "pt": pt,
        "ct": ct,
        "target_key": target_key_chars,
        "target_bin": target_key_bin,
        "N": N,
        "iterations": iterations,
        "measured_bin": measured_bin,
        "found_key": found_key,
        "success": found_key == target_key_chars,
        "circuit_b64": circuit_b64,
        "hist_b64": hist_b64
    }