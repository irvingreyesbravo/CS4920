import numpy as np
from sympy import Matrix


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
    det = det % m  # Ensure determinant is within mod 26 range
    if np.gcd(det, m) != 1:
        raise ValueError(f"Key matrix determinant ({det}) is not invertible modulo {m}. Choose a different key matrix.")

    matrix_mod_inv = Matrix(matrix).inv_mod(m)  # Use sympy for modular inverse
    return np.array(matrix_mod_inv).astype(int)  # Convert to numpy array


# Function that converts a key string into a square matrix for Hill Cipher
def key_string_to_matrix(key_string):
    key_numbers = [ord(char.upper()) - ord('A') for char in key_string]
    size = int(len(key_numbers) ** 0.5)  # Determine matrix size
    return np.array(key_numbers).reshape(size, size)  # Reshape into a square matrix


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
def process_test_files(filename, output_filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        key_string = lines[0].strip()  # First line is the key
        message = lines[1].strip()  # Second line is the message

    print("Plaintext:", message)

    # Convert key string to matrix
    key_matrix = key_string_to_matrix(key_string)

    # Encrypt the message
    encrypted_text, num_of_spaces = encrypt(message, key_matrix)
    with open(output_filename, 'w') as enc_file:
        enc_file.write(encrypted_text)
    print("Encrypted Message:", encrypted_text)

    # Decrypt the message
    decrypted_text = decrypt(encrypted_text, key_matrix)
    print("Decrypted Message:", decrypted_text)

    # Verify decryption is correct
    if decrypted_text == message:
        print("Decryption successful! The decrypted text matches the original message.")
    else:
        print("Decryption failed! The output doesn't match the original plaintext.")


# Run the decryption process for the given file
input_filename = "Test_Input_5d.txt"
output_files = "Reyes_Output_5d.txt"
process_test_files(input_filename, output_files)

print(f"Ciphertext saved to {output_files}.")
