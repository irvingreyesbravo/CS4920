import numpy as np


# Function that converts text to numbers while ignoring non-alphabet characters
def text_to_numbers(text):
    text = text.upper()
    positions = {i: char for i, char in enumerate(text) if char == ' '}  # Store space positions
    text = ''.join(filter(str.isalpha, text))  # Remove spaces and non-alphabet characters
    return [ord(char) - ord('A') for char in text], positions


# Function that converts numbers back to text
def numbers_to_text(numbers, positions):
    text = ''.join(chr(num + ord('A')) for num in numbers)
    for pos, char in positions.items():
        text = text[:pos] + char + text[pos:]  # Reinsert spaces
    return text


# Function that finds the modular inverse of a matrix under modulo m
def mod_inv(matrix, m):
    det = int(np.round(np.linalg.det(matrix)))  # Determinant of the matrix
    det_inv = pow(det, -1, m)  # Modular inverse of the determinant
    matrix_adj = np.round(det_inv * np.linalg.inv(matrix) * det) % m  # Adjugate matrix
    return matrix_adj.astype(int)


# Function that encrypts the message using Hill Cipher
def encrypt(message, key_matrix):
    message_numbers, positions = text_to_numbers(message)
    block_size = key_matrix.shape[0]

    # Pad message (with 'X') if necessary
    while len(message_numbers) % block_size != 0:
        message_numbers.append(ord('X') - ord('A'))

    # Encrypt the message in blocks
    encrypted_numbers = []
    for i in range(0, len(message_numbers), block_size):
        block = np.array(message_numbers[i:i + block_size])
        encrypted_block = np.dot(key_matrix, block) % 26
        encrypted_numbers.extend(encrypted_block)

    return numbers_to_text(encrypted_numbers, {}), positions


# Function that decrypt the message using Hill Cipher
def decrypt(encrypted_message, key_matrix, positions):
    encrypted_numbers, _ = text_to_numbers(encrypted_message)
    block_size = key_matrix.shape[0]

    # Calculate the modular inverse of the key matrix
    inv_key_matrix = mod_inv(key_matrix, 26)

    # Decrypt the message in blocks
    decrypted_numbers = []
    for i in range(0, len(encrypted_numbers), block_size):
        block = np.array(encrypted_numbers[i:i + block_size])
        decrypted_block = np.dot(inv_key_matrix, block) % 26
        decrypted_numbers.extend(decrypted_block)

    return numbers_to_text(decrypted_numbers, positions)


# Example usage for part A
if __name__ == "__main__":
    given_matrix = np.array([[3, 3], [2, 5]])

    plaintext = "HELLO WORLD"

    # Encrypt the message
    encrypted_text, num_of_spaces = encrypt(plaintext, given_matrix)
    print("Encrypted Message:", encrypted_text)

    # Decrypt the message
    decrypted_text = decrypt(encrypted_text, given_matrix, num_of_spaces)
    print("Decrypted Message:", decrypted_text)


