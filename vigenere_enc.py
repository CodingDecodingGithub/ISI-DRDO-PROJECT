def vigenere_encrypt(plaintext, key):
    ciphertext = ""
    key = key.upper()
    key_index = 0

    for char in plaintext.upper():
        if char.isalpha():
            shift = ord(key[key_index % len(key)]) - ord('A')
            encrypted = chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
            ciphertext += encrypted
            key_index += 1
        else:
            ciphertext += char

    return ciphertext


# print("========== ENCRYPTION DEMO ==========\n")

# plaintext = input("ENTER PLAINTEXT: ")
# key = input("ENTER KEY: ")

# ciphertext = vigenere_encrypt(plaintext, key)

# print("CIPHERTEXT:", ciphertext)