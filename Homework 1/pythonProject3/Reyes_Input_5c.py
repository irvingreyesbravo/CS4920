import numpy as np
from sympy import Matrix


# Function that converts text to numbers while ignoring non-alphabet characters
def text_to_numbers(text):
    text = text.upper()
    return [ord(char) - ord('A') for char in text]


# Function that converts numbers back to text
def numbers_to_text(numbers):
    return ''.join(chr(num + ord('A')) for num in numbers)


# Function that finds the modular inverse of a matrix under modulo m
def mod_inv(matrix, m):
    det = int(np.round(np.linalg.det(matrix)))  # Determinant of the matrix
    det = det % m  # Ensure determinant is within mod 26 range
    if np.gcd(det, m) != 1:
        raise ValueError(f"Key matrix determinant ({det}) is not invertible modulo {m}. Choose a different key matrix.")

    matrix_mod_inv = Matrix(matrix).inv_mod(m)  # Use sympy for modular inverse
    return np.array(matrix_mod_inv).astype(int)  # Convert to numpy array


# Function that converts a key string into a square matrix for Hill Cipher
def key_string_to_matrix(key_string):
    key_numbers = [ord(char.upper()) - ord('A') for char in key_string]
    size = int(len(key_numbers) ** 0.5)  # Determine matrix size
    if size * size != len(key_numbers):
        raise ValueError("Invalid key length. It must be a perfect square!")

    return np.array(key_numbers).reshape(size, size)  # Reshape into a square matrix


# Function that decrypt the message using Hill Cipher
def decrypt(encrypted_message, key_matrix):
    encrypted_numbers = text_to_numbers(encrypted_message)
    block_size = key_matrix.shape[0]

    # Calculate the modular inverse of the key matrix
    inv_key_matrix = mod_inv(key_matrix, 26)

    # Decrypt the message in blocks
    decrypted_numbers = []
    for i in range(0, len(encrypted_numbers), block_size):
        block = np.array(encrypted_numbers[i:i + block_size])
        decrypted_block = np.dot(inv_key_matrix, block) % 26
        decrypted_numbers.extend(decrypted_block)

    return numbers_to_text(decrypted_numbers)


# Function that reads in input, decrypts the message, and writes plaintext to a file
def process_class_input(filename, output_filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        key_string = lines[0].strip()  # First line is the key
        message = lines[1].strip()  # Second line is the message

    print("Ciphertext:", message)

    # Convert key string to matrix
    key_matrix = key_string_to_matrix(key_string)

    # Decrypt the message
    decrypted_message = decrypt(message, key_matrix)
    with open(output_filename, 'w') as output_file:
        output_file.write(decrypted_message)


# Run the decryption process for the given file
input_filename = "class_input_c.txt"
output_files = "Reyes_Output_5c.txt"
process_class_input(input_filename, output_files)

print(f"Plaintext saved to {output_files}.")
