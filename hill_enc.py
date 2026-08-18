def letters_to_matrix(letter_rows):
    return [[ord(letter.upper()) - ord('A') for letter in row] for row in letter_rows]


def matrix_vector_mult_mod(matrix, vector, mod=26):
    n = len(matrix)
    result = [0] * n

    for i in range(n):
        total = 0
        for j in range(n):
            total += matrix[i][j] * vector[j]
        result[i] = total % mod

    return result


def hill_encrypt(plaintext, key_matrix):
    """Encrypts the whole message as a single block. key_matrix must be
    n x n, where n is the number of letters in plaintext."""

    letters = "".join(ch for ch in plaintext.upper() if ch.isalpha())
    n = len(key_matrix)

    if len(letters) != n:
        raise ValueError(f"Key matrix must be {len(letters)}x{len(letters)} to match the plaintext length.")

    vector = [ord(ch) - ord('A') for ch in letters]
    enc_vector = matrix_vector_mult_mod(key_matrix, vector)

    return "".join(chr(v + ord('A')) for v in enc_vector)


if __name__ == "__main__":
    print("========== ENCRYPTION DEMO ==========\n")

    plaintext = input("ENTER PLAINTEXT : ")
    letters = "".join(ch for ch in plaintext.upper() if ch.isalpha())
    n = len(letters)

    print(f"Enter the {n}x{n} key matrix, row by row (letters A-Z):")
    letter_rows = []
    for i in range(n):
        row = input(f"ROW {i+1}: ").strip().upper().split()
        letter_rows.append(row)

    key_matrix = letters_to_matrix(letter_rows)
    ciphertext = hill_encrypt(plaintext, key_matrix)

    print("CIPHERTEXT:", ciphertext)