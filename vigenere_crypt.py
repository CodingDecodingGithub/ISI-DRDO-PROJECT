from collections import defaultdict, Counter
from math import gcd
from functools import reduce
import string


# ==================================================
# INPUT CIPHERTEXT
# ==================================================
# print("========== KASISKI ANALYSIS DEMO ==========\n")

# ciphertext = input("ENTER CIPHERTEXT: ").strip().upper()


# ==================================================
# KASISKI EXAMINATION
# ==================================================

def kasiski_examination(ciphertext, n=3):

    positions = defaultdict(list)

    for i in range(len(ciphertext) - n + 1):
        gram = ciphertext[i:i+n]
        positions[gram].append(i)

    repeated = {}

    for gram, pos_list in positions.items():

        if len(pos_list) > 1:

            distances = []

            for j in range(len(pos_list)-1):
                distances.append(pos_list[j+1] - pos_list[j])

            repeated[gram] = distances

    return repeated


def estimate_key_length(repeated_patterns):

    distances = []

    for dists in repeated_patterns.values():
        distances.extend(dists)

    if not distances:
        return None

    return reduce(gcd, distances)


# ==================================================
# SPLIT INTO COSETS
# ==================================================

def split_into_cosets(ciphertext, key_length):

    groups = []

    for i in range(key_length):

        group = []

        for j in range(i, len(ciphertext), key_length):
            group.append(ciphertext[j])

        groups.append(group)

    return groups


# ==================================================
# ENGLISH LETTER FREQUENCIES
# ==================================================

english_freq = {
    'A': 0.08167, 'B': 0.01492, 'C': 0.02782,
    'D': 0.04253, 'E': 0.12702, 'F': 0.02228,
    'G': 0.02015, 'H': 0.06094, 'I': 0.06966,
    'J': 0.00153, 'K': 0.00772, 'L': 0.04025,
    'M': 0.02406, 'N': 0.06749, 'O': 0.07507,
    'P': 0.01929, 'Q': 0.00095, 'R': 0.05987,
    'S': 0.06327, 'T': 0.09056, 'U': 0.02758,
    'V': 0.00978, 'W': 0.02360, 'X': 0.00150,
    'Y': 0.01974, 'Z': 0.00074
}


# ==================================================
# CAESAR DECRYPTION
# ==================================================

def decrypt_caesar(text, shift):

    result = ""

    for c in text:
        value = (ord(c) - ord('A') - shift) % 26
        result += chr(value + ord('A'))

    return result


# ==================================================
# CHI-SQUARE SCORE
# ==================================================

def chi_square_score(text):

    count = Counter(text)
    N = len(text)

    score = 0

    for letter in string.ascii_uppercase:

        observed = count.get(letter, 0)
        expected = english_freq[letter] * N

        score += ((observed - expected) ** 2) / expected

    return score


# ==================================================
# RECOVER KEY
# ==================================================

def recover_key(groups):

    key = ""

    for group in groups:

        coset = "".join(group)

        best_shift = 0
        best_score = float("inf")

        for shift in range(26):

            decrypted = decrypt_caesar(coset, shift)
            score = chi_square_score(decrypted)

            if score < best_score:
                best_score = score
                best_shift = shift

        key += chr(best_shift + ord('A'))

    return key

def vigenere_decrypt(ciphertext, key):
    plaintext = ""
    key = key.upper()
    key_index = 0

    for char in ciphertext.upper():
        if char.isalpha():
            shift = ord(key[key_index % len(key)]) - ord('A')
            decrypted = chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
            plaintext += decrypted
            key_index += 1
        else:
            plaintext += char

    return plaintext


# ==================================================
# MAIN
# ==================================================

# repeats = kasiski_examination(ciphertext)

# key_length = estimate_key_length(repeats)

# if key_length is None:
#     print("Could not estimate key length.")
# else:
#     groups = split_into_cosets(ciphertext, key_length)
#     key = recover_key(groups)
#     decrypted = vigenere_decrypt(ciphertext, key)
#     print("KEY", key)
#     print("PLAINTEXT :", decrypted)