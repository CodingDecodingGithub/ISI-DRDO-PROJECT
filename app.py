import os
from flask import Flask, request, render_template
from vigenere_enc import vigenere_encrypt
from vigenere_dec import vigenere_decrypt
from vigenere_crypt import (
        kasiski_examination,
        estimate_key_length,
        split_into_cosets,
        recover_key,
        vigenere_decrypt as kasiski_vigenere_decrypt)
from hill_enc import hill_encrypt, letters_to_matrix as hill_enc_letters_to_matrix
from hill_dec import hill_decrypt, letters_to_matrix as hill_dec_letters_to_matrix
from hill_crypt import recover_key_matrix, hill_decrypt_with_key
from vigenere_bruteforce import run_bruteforce
from swaptest import run_swap_test
from repsubsearch import run_bht_simulation
from periodkeylendetect import calculate_key_length
from hill_bruteforce import run_hill_bruteforce


app = Flask(__name__)
VIGENERE_OUTPUT_FILENAME = "ciphered_output.txt"
HILL_OUTPUT_FILENAME = "hill_ciphered_output.txt"


def read_key_matrix_from_form(form, n):
    """Reads an n x n grid of single-letter cells named key_i_j from a
    submitted form and returns it as a list of letter rows."""
    rows = []
    for i in range(n):
        row = []
        for j in range(n):
            cell = form.get(f"key_{i}_{j}", "").strip().upper()
            if not cell:
                raise ValueError("All key matrix cells must be filled in.")
            row.append(cell)
        rows.append(row)
    return rows


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')


# ==========================================
# 2. Sender Endpoint (Encryption) - Vigenere
# ==========================================
@app.route('/vigenere/sender', methods=['GET', 'POST'])
def handle_encryption():
    if request.method == 'POST':
        message = request.form.get('message')
        key = request.form.get('key')

        if not message or not key:
            return "Error: Both 'message' and 'key' are required fields.", 400

        ciphered_message = vigenere_encrypt(message, key)

        with open(VIGENERE_OUTPUT_FILENAME, "w", encoding="utf-8") as file:
            file.write(ciphered_message)

    return render_template('vigenere-sender.html')


# ==========================================
# 3. Receiver Endpoint (Decryption) - Vigenere
# ==========================================
@app.route('/vigenere/receiver', methods=['GET', 'POST'])
def handle_decryption():

    # For a GET request, read the ciphertext from the text file
    ciphertext = ""
    if os.path.exists(VIGENERE_OUTPUT_FILENAME):
        with open(VIGENERE_OUTPUT_FILENAME, "r", encoding="utf-8") as file:
            ciphertext = file.read()
    else:
        ciphertext = "[No encrypted message found in file]"

    if request.method == 'POST':
        # Retrieve the key and the ciphertext submitted from the receiver form
        key = request.form.get('key')

        if not key or not ciphertext:
            return "Error: Both 'ciphertext' and 'key' are required fields.", 400

        # Process through the imported decryption function
        deciphered_message = vigenere_decrypt(ciphertext, key)

        # Re-render the template, passing the decrypted message to the same display variable
        return render_template(
            'vigenere-receiver.html',
            display_message=deciphered_message,
            status="Decrypted Message:"
        )

    # Render the template, passing the ciphertext to the display variable
    return render_template(
        'vigenere-receiver.html',
        display_message=ciphertext,
        status="Encrypted Message from file:"
    )


@app.route('/vigenere/crypt', methods=['GET', 'POST'])
def handle_kasiski():
    if request.method == 'POST':
        # Retrieve the ciphertext from the submitted form
        ciphertext_input = request.form.get('ciphertext')

        if not ciphertext_input:
            return "Error: 'ciphertext' is a required field.", 400

        # Clean the input as expected by the analysis script
        ciphertext = ciphertext_input.strip().upper()

        # Perform the Kasiski examination and estimate length
        repeats = kasiski_examination(ciphertext)
        key_length = estimate_key_length(repeats)

        if key_length is None:
            return render_template(
                'vigenere-crypt.html',
                error="Could not estimate key length."
            )

        # Recover the key and decrypt the message
        groups = split_into_cosets(ciphertext, key_length)
        recovered_key = recover_key(groups)
        decrypted_message = kasiski_vigenere_decrypt(ciphertext, recovered_key)

        # Render the template with the recovered data
        return render_template(
            'vigenere-crypt.html',
            ciphertext=ciphertext,
            key_length=key_length,
            recovered_key=recovered_key,
            decrypted_message=decrypted_message
        )

    # For a GET request, simply render the form
    return render_template('vigenere-crypt.html')


# ==========================================
# 4. Sender Endpoint (Encryption) - Hill
# ==========================================
@app.route('/hill/sender', methods=['GET', 'POST'])
def handle_hill_encryption():
    if request.method == 'POST':
        message = request.form.get('message')

        try:
            n = int(request.form.get('matrix_size', 0))
        except ValueError:
            n = 0

        letters = "".join(ch for ch in (message or "").upper() if ch.isalpha())

        if not message or n == 0 or len(letters) != n:
            return "Error: 'message' and a matching key matrix are required fields.", 400

        try:
            letter_rows = read_key_matrix_from_form(request.form, n)
            key_matrix = hill_enc_letters_to_matrix(letter_rows)
            ciphered_message = hill_encrypt(message, key_matrix)
        except ValueError as exc:
            return f"Error: {exc}", 400

        with open(HILL_OUTPUT_FILENAME, "w", encoding="utf-8") as file:
            file.write(ciphered_message)

    return render_template('hill-sender.html')


# ==========================================
# 5. Receiver Endpoint (Decryption) - Hill
# ==========================================
@app.route('/hill/receiver', methods=['GET', 'POST'])
def handle_hill_decryption():

    # For a GET request, read the ciphertext from the text file
    ciphertext = ""
    if os.path.exists(HILL_OUTPUT_FILENAME):
        with open(HILL_OUTPUT_FILENAME, "r", encoding="utf-8") as file:
            ciphertext = file.read()
    else:
        ciphertext = "[No encrypted message found in file]"

    if request.method == 'POST':
        try:
            n = int(request.form.get('matrix_size', 0))
        except ValueError:
            n = 0

        letters = "".join(ch for ch in ciphertext.upper() if ch.isalpha())

        if n == 0 or len(letters) != n:
            return "Error: A key matrix matching the ciphertext length is required.", 400

        try:
            letter_rows = read_key_matrix_from_form(request.form, n)
            key_matrix = hill_dec_letters_to_matrix(letter_rows)
            deciphered_message = hill_decrypt(ciphertext, key_matrix)
        except ValueError as exc:
            return f"Error: {exc}", 400

        if deciphered_message is None:
            return render_template(
                'hill-receiver.html',
                display_message="Key matrix is not invertible mod 26.",
                status="Error:"
            )

        return render_template(
            'hill-receiver.html',
            display_message=deciphered_message,
            status="Decrypted Message:"
        )

    return render_template(
        'hill-receiver.html',
        display_message=ciphertext,
        status="Encrypted Message from file:"
    )


# ==========================================
# 6. Known-Plaintext Cryptanalysis - Hill
# ==========================================
@app.route('/hill/crypt', methods=['GET', 'POST'])
def handle_hill_kasiski():
    if request.method == 'POST':
        try:
            n = int(request.form.get('matrix_size', 0))
        except ValueError:
            n = 0

        full_ciphertext = request.form.get('full_ciphertext', '').strip().upper()

        if n == 0:
            return render_template('hill-crypt.html', error="Enter a known plaintext to begin.")

        known_plaintexts = []
        known_ciphertexts = []

        for i in range(1, n + 1):
            pt = request.form.get(f'known_pt_{i}', '').strip().upper()
            ct = request.form.get(f'known_ct_{i}', '').strip().upper()

            pt_letters = "".join(ch for ch in pt if ch.isalpha())
            ct_letters = "".join(ch for ch in ct if ch.isalpha())

            if len(pt_letters) != n or len(ct_letters) != n:
                return render_template(
                    'hill-crypt.html',
                    error=f"Pair #{i} must contain exactly {n} letters in both fields."
                )

            known_plaintexts.append(pt_letters)
            known_ciphertexts.append(ct_letters)

        key_matrix = recover_key_matrix(known_plaintexts, known_ciphertexts)

        if key_matrix is None:
            return render_template(
                'hill-crypt.html',
                error="Known plaintext pairs are not invertible mod 26. Try a different sample."
            )

        decrypted_message = hill_decrypt_with_key(full_ciphertext, key_matrix)

        if decrypted_message is None:
            return render_template(
                'hill-crypt.html',
                error=f"Full ciphertext must contain exactly {n} letters."
            )

        # Render the template with the recovered data
        return render_template(
            'hill-crypt.html',
            matrix_size=n,
            recovered_key=key_matrix,
            full_ciphertext=full_ciphertext,
            decrypted_message=decrypted_message
        )

    # For a GET request, simply render the form
    return render_template('hill-crypt.html')


# ==========================================
# 7. Grover Brute-Force Demo - Vigenere
# ==========================================
@app.route('/vigenere/bruteforce', methods=['GET', 'POST'])
def handle_vigenere_bruteforce():
    if request.method == 'POST':
        plaintext = request.form.get('plaintext', '')
        ciphertext = request.form.get('ciphertext', '')

        try:
            results = run_bruteforce(plaintext, ciphertext)
        except ValueError as exc:
            return render_template(
                'vigenere-bruteforce.html',
                error=str(exc),
                plaintext=plaintext,
                ciphertext=ciphertext
            )

        return render_template('vigenere-bruteforce.html', results=results)

    return render_template('vigenere-bruteforce.html')

# ==========================================
# 8. Swap Test Demonstration
# ==========================================
@app.route('/swaptest', methods=['GET', 'POST'])
def handle_swaptest():
    if request.method == 'POST':
        try:
            # Extract values from form, default to 0 if missing/invalid
            lang1 = float(request.form.get('lang1', 0.8))
            ciph1 = float(request.form.get('ciph1', 0.2))
            lang2 = float(request.form.get('lang2', 0.8))
            ciph2 = float(request.form.get('ciph2', 0.2))

            results = run_swap_test(lang1, ciph1, lang2, ciph2)

            return render_template(
                'swaptest.html',
                results=results,
                lang1=lang1, ciph1=ciph1,
                lang2=lang2, ciph2=ciph2
            )
        except Exception as exc:
            return render_template('swaptest.html', error=str(exc))

    return render_template('swaptest.html')

# ==========================================
# 9. BHT Repeated Substring Search
# ==========================================
@app.route('/repsubsearch', methods=['GET', 'POST'])
def handle_repsubsearch():
    if request.method == 'POST':
        ciphertext = request.form.get('ciphertext', '')

        try:
            results = run_bht_simulation(ciphertext)
            return render_template(
                'repsubsearch.html', 
                results=results,
                ciphertext=ciphertext
            )
        except ValueError as exc:
            return render_template(
                'repsubsearch.html',
                error=str(exc),
                ciphertext=ciphertext
            )

    return render_template('repsubsearch.html')

# ==========================================
# 10. Period Key Length Detection (GCD)
# ==========================================
@app.route('/periodkeylendetect', methods=['GET', 'POST'])
def handle_periodkeylendetect():
    if request.method == 'POST':
        positions = []
        try:
            # Safely extract and convert all 6 position inputs
            for i in range(1, 7):
                val = request.form.get(f'pos_{i}')
                if val is None or val.strip() == '':
                    raise ValueError(f"Position {i} cannot be empty.")
                positions.append(int(val))

            results = calculate_key_length(positions)
            
            return render_template(
                'periodkeylendetect.html', 
                results=results,
                inputs=positions
            )
            
        except ValueError as exc:
            return render_template(
                'periodkeylendetect.html',
                error=str(exc),
                inputs=positions  # Passes back whatever was successfully parsed before failure
            )

    return render_template('periodkeylendetect.html')

# ==========================================
# 11. Grover Brute-Force Demo - Hill Cipher
# ==========================================
@app.route('/hill/bruteforce', methods=['GET', 'POST'])
def handle_hill_bruteforce():
    if request.method == 'POST':
        plaintext = request.form.get('plaintext', '')
        ciphertext = request.form.get('ciphertext', '')

        try:
            results = run_hill_bruteforce(plaintext, ciphertext)
            return render_template(
                'hill-bruteforce.html', 
                results=results, 
                plaintext=plaintext, 
                ciphertext=ciphertext
            )
        except ValueError as exc:
            return render_template(
                'hill-bruteforce.html',
                error=str(exc),
                plaintext=plaintext,
                ciphertext=ciphertext
            )

    return render_template('hill-bruteforce.html')


if __name__ == '__main__':
    app.run(debug=True)