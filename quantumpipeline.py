from repsubsearch import run_bht_simulation
from periodkeylendetect import calculate_key_length
from swaptest import run_swap_test

# Standard English letter frequencies (A-Z)
ENGLISH_FREQ = [
    0.08167, 0.01492, 0.02782, 0.04253, 0.12702, 0.02228, 0.02015, 0.06094, 
    0.06966, 0.00015, 0.00772, 0.04025, 0.02406, 0.06749, 0.07507, 0.01929, 
    0.00095, 0.05987, 0.06327, 0.09056, 0.02758, 0.00978, 0.02360, 0.00150, 
    0.01974, 0.00074
]

def calculate_2bin_frequency(text):
    """Helper to split a string into 2 frequency bins (A-M, N-Z) for the Swap Test."""
    if not text: 
        return 0.5, 0.5
    am_count = sum(1 for c in text if 'A' <= c <= 'M')
    am_ratio = am_count / len(text)
    nz_ratio = 1.0 - am_ratio
    return am_ratio, nz_ratio

def recover_vigenere_key(ciphertext, key_length):
    """
    Recovers the Vigenere key by comparing the frequency distribution 
    of each coset against standard English frequencies.
    """
    recovered_key = ""
    
    for i in range(key_length):
        # Extract the coset for the current key character position
        coset = ciphertext[i::key_length]
        
        best_shift = 0
        max_dot_product = 0
        
        # Test all 26 possible shifts for this coset
        for shift in range(26):
            counts = [0] * 26
            for char in coset:
                # Decrypt the character with the current shift test
                shifted_char_val = (ord(char) - ord('A') - shift) % 26
                counts[shifted_char_val] += 1
                
            # Calculate the dot product of this shift's frequencies vs English frequencies
            coset_len = len(coset)
            dot_product = sum((counts[j] / coset_len) * ENGLISH_FREQ[j] for j in range(26))
            
            # The shift that produces the highest correlation is our key letter
            if dot_product > max_dot_product:
                max_dot_product = dot_product
                best_shift = shift
                
        # Convert the best shift integer back to an uppercase letter
        recovered_key += chr(best_shift + ord('A'))
        
    return recovered_key

def run_complete_quantum_cryptanalysis(ciphertext):
    """
    Strings together BHT Search, GCD Periodicity, Swap Test, and Key Recovery.
    """
    print(f"--- STARTING HYBRID QUANTUM-CLASSICAL PIPELINE ---")
    print(f"Target Ciphertext: {ciphertext}\n")
    
    # ---------------------------------------------------------
    # PHASE 1: BHT Search (Imported from repsubsearch.py)
    # ---------------------------------------------------------
    print("Executing Phase 1: Quantum BHT Collision Search...")
    bht_results = run_bht_simulation(ciphertext)
    
    substring = bht_results['discovered_substring']
    indices = bht_results['measured_indices_quantum']
    print(f"  > Discovered Collision: '{substring}' at indices {indices}\n")
    
    # ---------------------------------------------------------
    # PHASE 2: Key Length Detection (Imported from periodkeylendetect.py)
    # ---------------------------------------------------------
    print("Executing Phase 2: Classical GCD Periodicity...")
    gcd_results = calculate_key_length(indices)
    
    estimated_key_length = gcd_results['gcd']
    print(f"  > Estimated Key Length (GCD): {estimated_key_length}\n")
    
    # ---------------------------------------------------------
    # PHASE 3: Swap Test Verification (Imported from swaptest_2.py)
    # ---------------------------------------------------------
    print("Executing Phase 3: Quantum Swap Test Verification...")
    
    first_coset = ciphertext[0::estimated_key_length]
    print(f"  > Generated Coset 1: {first_coset}")
    
    eng_am, eng_nz = 0.60, 0.40 
    coset_am, coset_nz = calculate_2bin_frequency(first_coset)
    
    print(f"  > Expected Eng Ratio (A-M / N-Z): {eng_am} / {eng_nz}")
    print(f"  > Actual Coset Ratio (A-M / N-Z): {coset_am:.2f} / {coset_nz:.2f}")
    
    swap_results = run_swap_test(eng_am, eng_nz, coset_am, coset_nz)
    similarity = swap_results['similarity']
    
    print(f"  > QUANTUM SIMILARITY SCORE: {similarity}%\n")
    
    # ---------------------------------------------------------
    # PHASE 4: Key Recovery & Decryption
    # ---------------------------------------------------------
    print("Executing Phase 4: Classical Key Recovery...")
    final_key = recover_vigenere_key(ciphertext, estimated_key_length)
    print(f"  > RECOVERED KEY: {final_key}")
    
    print("\n--- PIPELINE COMPLETE ---")
    
    return {
        "substring": substring,
        "indices": indices,
        "key_length": estimated_key_length,
        "coset": first_coset,
        "similarity_score": similarity,
        "recovered_key": final_key,
        "bht_circuit": bht_results['circuit_b64'],
        "swap_histogram": swap_results['hist_b64']
    }

if __name__ == "__main__":
    # Test with a longer Vigenere ciphertext to ensure valid frequency recovery
    # Plaintext: "THEQUICKBROWNFOXJUMPSOVERTHELAZYDOG..." encrypted with key "CAT"
    test_ciphertext = "UQVIEMQKIZEIVJIBZUGXIBZMZFIUWQAKIBQIRABZSBPEGUGBPWZVSUMAAZMKPAXCJVVSZILPUQOZSVLXIBZMZFIUWQATIASVBCCUSZZSBPEGOJIVVUWLPMJVIEMQKSCECLAVQJIBZUGTZWLPMJVIEMQKIVKPCEIVJIBZ"    
    try:
        run_complete_quantum_cryptanalysis(test_ciphertext)
    except ValueError as e:
        print(f"Pipeline Failed: {e}")