def letters_to_matrix(letter_rows):
    return [[ord(letter.upper()) - ord('A') for letter in row] for row in letter_rows]


def mod_inverse(a, m):
    a = a % m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None


def matrix_minor(matrix, i, j):
    return [row[:j] + row[j+1:] for row in (matrix[:i] + matrix[i+1:])]


def determinant(matrix):
    n = len(matrix)

    if n == 1:
        return matrix[0][0]

    if n == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]

    det = 0
    for j in range(n):
        det += ((-1) ** j) * matrix[0][j] * determinant(matrix_minor(matrix, 0, j))

    return det


def cofactor_matrix(matrix):
    n = len(matrix)
    cofactors = []

    for i in range(n):
        row = []
        for j in range(n):
            minor = matrix_minor(matrix, i, j)
            row.append(((-1) ** (i + j)) * determinant(minor))
        cofactors.append(row)

    return cofactors


def transpose(matrix):
    return [list(row) for row in zip(*matrix)]


def mod_matrix_inverse(matrix, mod=26):
    n = len(matrix)

    det = determinant(matrix) % mod
    det_inv = mod_inverse(det, mod)

    if det_inv is None:
        return None

    cofactors = cofactor_matrix(matrix)
    adjugate = transpose(cofactors)

    return [[(det_inv * adjugate[i][j]) % mod for j in range(n)] for i in range(n)]


def matrix_vector_mult_mod(matrix, vector, mod=26):
    n = len(matrix)
    result = [0] * n

    for i in range(n):
        total = 0
        for j in range(n):
            total += matrix[i][j] * vector[j]
        result[i] = total % mod

    return result


def hill_decrypt(ciphertext, key_matrix):
    """Decrypts the whole message as a single block. key_matrix must be
    n x n, where n is the number of letters in ciphertext."""

    letters = "".join(ch for ch in ciphertext.upper() if ch.isalpha())
    n = len(key_matrix)

    if len(letters) != n:
        raise ValueError(f"Key matrix must be {len(letters)}x{len(letters)} to match the ciphertext length.")

    inverse_matrix = mod_matrix_inverse(key_matrix)

    if inverse_matrix is None:
        return None

    vector = [ord(ch) - ord('A') for ch in letters]
    dec_vector = matrix_vector_mult_mod(inverse_matrix, vector)

    return "".join(chr(v + ord('A')) for v in dec_vector)


if __name__ == "__main__":
    print("========== DECRYPTION DEMO ==========\n")

    ciphertext = input("ENTER CIPHERTEXT : ")
    letters = "".join(ch for ch in ciphertext.upper() if ch.isalpha())
    n = len(letters)

    print(f"Enter the {n}x{n} key matrix, row by row (letters A-Z):")
    letter_rows = []
    for i in range(n):
        row = input(f"ROW {i+1}: ").strip().upper().split()
        letter_rows.append(row)

    key_matrix = letters_to_matrix(letter_rows)
    plaintext = hill_decrypt(ciphertext, key_matrix)

    if plaintext is None:
        print("Key matrix is not invertible mod 26.")
    else:
        print("PLAINTEXT :", plaintext)