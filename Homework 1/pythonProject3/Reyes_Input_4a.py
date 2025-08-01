import string


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


# Example usage for part A
plaintext = "Hello, World!"
key_value = 3

# Encrypt plaintext
ciphertext = caesar_cipher(plaintext, key_value, mode="encrypt")
print(f"Encrypted: {ciphertext}")

# Decrypt ciphertext
decrypted_text = caesar_cipher(ciphertext, key_value, mode="decrypt")
print(f"Decrypted: {decrypted_text}")
