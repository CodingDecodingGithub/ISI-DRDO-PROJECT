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


# print("========== DECRYPTION DEMO ==========\n")

# ciphertext = input("ENTER CIPHERTEXT: ")
# key = input("ENTER KEY: ")

# plaintext = vigenere_decrypt(ciphertext, key)

# print("PLAINTEXT :", plaintext)