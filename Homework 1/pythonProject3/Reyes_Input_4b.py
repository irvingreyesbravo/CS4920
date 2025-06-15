# Function that encrypts/decrypts a given text using the Caesar Cipher
def caesar_cipher(text, key, mode="encrypt"):
    """
    Parameters:
    - text (str): The input text to encrypt or decrypt.
    - key (int): The shift key for the Caesar cipher.
    - mode (str): Either "encrypt" or "decrypt". Defaults to "encrypt".

    Returns:
    - str: The encrypted or decrypted text.
    """
    result = []

    # Normalize key for decryption
    if mode == "decrypt":
        key = -key

    # For every character in the given text
    for char in text:
        # Ignore non-letter symbols, if present
        if char.isalpha():  # Ignore non-letter symbols
            base = ord('A') if char.isupper() else ord('a')
            shifted = (ord(char) - base + key) % 26 + base
            result.append(chr(shifted))
        # Ignore non-alphabetic characters, if present
        else:
            result.append(char)

    return ''.join(result)


# Read input file for part B
with open("class_input_b.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()
    key_text = lines[0].strip()  # First line is the key
    plaintext = lines[1].strip()  # Second line is the plaintext

# Convert key to shift value (sum of letter positions modulo 26)
key_value = sum(ord(c) - ord('a') for c in key_text.lower()) % 26

# Encrypt plaintext
ciphertext = caesar_cipher(plaintext, key_value, mode="encrypt")
print(f"Encrypted: {ciphertext}")

# Write ciphertext to file
with open("Reyes_Output_4b.txt", "w", encoding="utf-8") as f:
    f.write(ciphertext)

print("Ciphertext saved to 'Reyes_Output_4b.txt'.")
