from hill_dec import mod_matrix_inverse


def matrix_mult_mod(A, B, mod=26):
    rows_a = len(A)
    cols_a = len(A[0])
    cols_b = len(B[0])

    result = [[0] * cols_b for _ in range(rows_a)]

    for i in range(rows_a):
        for j in range(cols_b):
            total = 0
            for k in range(cols_a):
                total += A[i][k] * B[k][j]
            result[i][j] = total % mod

    return result


def messages_to_matrix(messages):
    """Each message (a string of n letters) becomes one COLUMN of the matrix."""
    n = len(messages[0])
    return [[ord(msg[i]) - ord('A') for msg in messages] for i in range(n)]


def recover_key_matrix(known_plaintexts, known_ciphertexts):
    """known_plaintexts / known_ciphertexts: lists of n same-length (n letter)
    strings. Recovers the n x n key matrix K such that C = K * P mod 26."""

    P = messages_to_matrix(known_plaintexts)
    C = messages_to_matrix(known_ciphertexts)

    P_inv = mod_matrix_inverse(P)

    if P_inv is None:
        return None

    return matrix_mult_mod(C, P_inv)


def matrix_vector_mult_mod(matrix, vector, mod=26):
    n = len(matrix)
    result = [0] * n

    for i in range(n):
        total = 0
        for j in range(n):
            total += matrix[i][j] * vector[j]
        result[i] = total % mod

    return result


def hill_decrypt_with_key(ciphertext, key_matrix):
    letters = "".join(ch for ch in ciphertext.upper() if ch.isalpha())
    n = len(key_matrix)

    if len(letters) != n:
        return None

    inverse_matrix = mod_matrix_inverse(key_matrix)

    if inverse_matrix is None:
        return None

    vector = [ord(ch) - ord('A') for ch in letters]
    dec_vector = matrix_vector_mult_mod(inverse_matrix, vector)

    return "".join(chr(v + ord('A')) for v in dec_vector)


if __name__ == "__main__":
    print("========== KNOWN-PLAINTEXT CRYPTANALYSIS DEMO ==========\n")

    n = int(input("ENTER MATRIX SIZE (n) : "))

    known_plaintexts = []
    known_ciphertexts = []

    for i in range(n):
        pt = input(f"KNOWN PLAINTEXT  #{i+1} ({n} letters) : ").strip().upper()
        ct = input(f"KNOWN CIPHERTEXT #{i+1} ({n} letters) : ").strip().upper()
        known_plaintexts.append(pt)
        known_ciphertexts.append(ct)

    key_matrix = recover_key_matrix(known_plaintexts, known_ciphertexts)

    if key_matrix is None:
        print("Known plaintext messages are not invertible mod 26. Choose different samples.")
    else:
        print("RECOVERED KEY MATRIX:")
        for row in key_matrix:
            print(row)

        full_ciphertext = input("\nENTER FULL CIPHERTEXT TO DECRYPT : ")
        plaintext = hill_decrypt_with_key(full_ciphertext, key_matrix)

        print("PLAINTEXT :", plaintext)