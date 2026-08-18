import math
import io
import base64
import matplotlib
# Set matplotlib to non-interactive backend to prevent threading issues in Flask[cite: 8]
matplotlib.use('Agg') 
import matplotlib.pyplot as plt

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram

def char_to_int(c):
    return ord(c.upper()) - ord('A')

def int_to_char(i):
    return chr(i + ord('A'))

def fig_to_base64(fig):
    """Converts a matplotlib figure to a base64 string for HTML embedding[cite: 8]."""
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight', facecolor='#212529')
    buf.seek(0)
    b64_str = base64.b64encode(buf.getvalue()).decode('utf-8')
    plt.close(fig)
    return b64_str

def create_oracle(target_binaries, num_qubits):
    """
    Creates an Oracle that marks ALL valid key matrices that encrypt the PT to the CT.
    """
    oracle = QuantumCircuit(num_qubits, name="Oracle")
    
    for target_bin in target_binaries:
        for i, bit in enumerate(reversed(target_bin)):
            if bit == '0':
                oracle.x(i)
                
        oracle.h(num_qubits - 1)
        oracle.mcx(list(range(num_qubits - 1)), num_qubits - 1)
        oracle.h(num_qubits - 1)
        
        for i, bit in enumerate(reversed(target_bin)):
            if bit == '0':
                oracle.x(i)
                
    return oracle

def create_diffuser(num_qubits):
    """Standard Grover Diffuser[cite: 8]."""
    diffuser = QuantumCircuit(num_qubits, name="Diffuser")
    diffuser.h(range(num_qubits))
    diffuser.x(range(num_qubits))
    
    diffuser.h(num_qubits - 1)
    diffuser.mcx(list(range(num_qubits - 1)), num_qubits - 1)
    diffuser.h(num_qubits - 1)
    
    diffuser.x(range(num_qubits))
    diffuser.h(range(num_qubits))
    
    return diffuser

def run_hill_bruteforce(plaintext, ciphertext):
    pt = plaintext.strip().upper()
    ct = ciphertext.strip().upper()
    
    if len(pt) != 2 or len(ct) != 2:
        raise ValueError("For this toy model, plaintext and ciphertext must be exactly 2 characters long.")
        
    valid_chars = set("ABCD")
    if not all(c in valid_chars for c in pt) or not all(c in valid_chars for c in ct):
        raise ValueError("For this toy demonstration, please only use characters A, B, C, and D.")

    # 1. Classical target calculation (Pre-compiling the Oracle)
    p1, p2 = char_to_int(pt[0]), char_to_int(pt[1])
    c1, c2 = char_to_int(ct[0]), char_to_int(ct[1])
    
    target_binaries = []
    
    # Brute-force find all 2x2 keys in Modulo 4 that satisfy: [p1, p2] * K = [c1, c2]
    for k11 in range(4):
        for k12 in range(4):
            for k21 in range(4):
                for k22 in range(4):
                    calc_c1 = (p1 * k11 + p2 * k21) % 4
                    calc_c2 = (p1 * k12 + p2 * k22) % 4
                    if calc_c1 == c1 and calc_c2 == c2:
                        bin_str = f"{k11:02b}{k12:02b}{k21:02b}{k22:02b}"
                        target_binaries.append(bin_str)
                        
    if not target_binaries:
        raise ValueError("No valid Hill key matrix maps this plaintext to this ciphertext in modulo 4.")

    num_qubits = 8
    N = 256
    num_solutions = len(target_binaries)
    
    # 2. Iteration calculation: ~ (pi / 4) * sqrt(N / M)
    iterations = max(1, math.floor((math.pi / 4) * math.sqrt(N / num_solutions)))
    
    # 3. Circuit construction[cite: 8]
    qc = QuantumCircuit(num_qubits, num_qubits)
    qc.h(range(num_qubits))
    qc.barrier()
    
    oracle = create_oracle(target_binaries, num_qubits)
    diffuser = create_diffuser(num_qubits)
    
    for _ in range(iterations):
        qc.append(oracle.to_instruction(), range(num_qubits))
        qc.append(diffuser.to_instruction(), range(num_qubits))
        qc.barrier()
        
    qc.measure(range(num_qubits), range(num_qubits))
    
    # 4. Execution[cite: 8]
    simulator = AerSimulator()
    compiled_circuit = transpile(qc, simulator)
    job = simulator.run(compiled_circuit, shots=1024)
    counts = job.result().get_counts(compiled_circuit)
    
    measured_bin = max(counts, key=counts.get)
    
    # Decode the 8-bit string back into a 2x2 character matrix
    found_matrix = [
        [int_to_char(int(measured_bin[0:2], 2)), int_to_char(int(measured_bin[2:4], 2))],
        [int_to_char(int(measured_bin[4:6], 2)), int_to_char(int(measured_bin[6:8], 2))]
    ]
    
    # 5. Visual Generation[cite: 8]
    circuit_fig = qc.draw(output='mpl', style='clifford')
    circuit_b64 = fig_to_base64(circuit_fig)
    
    plt.style.use('dark_background')
    hist_fig = plot_histogram(counts, title="Measurement Probabilities (1024 Shots)", color='#0d6efd')
    hist_b64 = fig_to_base64(hist_fig)
    
    return {
        "pt": pt,
        "ct": ct,
        "N": N,
        "iterations": iterations,
        "num_solutions": num_solutions,
        "measured_bin": measured_bin,
        "found_matrix": found_matrix,
        "success": measured_bin in target_binaries,
        "circuit_b64": circuit_b64,
        "hist_b64": hist_b64
    }