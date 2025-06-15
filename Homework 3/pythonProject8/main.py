# Function that converts 8-bit binary string to integer
def binary_to_int(binary_str):
    return int(binary_str, 2)


# Function that converts integer to 8-bit binary string
def int_to_binary(num):
    return format(num, '08b')


# Function that performs addition in GF(2^8) (XOR operation)
def add_GF(a, b):
    return a ^ b


# Function that performs subtraction in GF(2^8) like addition (XOR operation)
def subtract_GF(a, b):
    return a ^ b


# Function that performs multiplication in GF(2^8) with reduction by m(x) = x^8 + x^4 + x^3 + x + 1
def multiply_GF(a, b):
    # AES irreducible polynomial represented as a number
    AES_POLYNOMIAL = 0x11b  # x^8 + x^4 + x^3 + x + 1

    p = 0
    for i in range(8):
        # If the i-th bit of b is set
        if b & (1 << i):
            # Add (XOR) a shifted i times to the product
            p ^= a << i

    # Modular Reduction:
    for i in range(15, 7, -1):  # From degree 15 to degree 8
        # If the i-th bit is set
        if p & (1 << i):
            # reduce the polynomial, then shift it to align with the i-th bit
            p ^= AES_POLYNOMIAL << (i - 8)

    return p


# Function that finds the multiplicative inverse of a element in GF(2^8)
def inverse_GF(a):
    # Edge case: 0 has no multiplicative inverse
    if a == 0:
        raise ValueError("Zero has no multiplicative inverse in GF(2^8)")

    # Extended Euclidean Algorithm:
    AES_POLYNOMIAL = 0x11b  # x^8 + x^4 + x^3 + x + 1
    r0, r1 = AES_POLYNOMIAL, a
    s0, s1 = 0, 1
    t0, t1 = 1, 0

    while r1 != 0:
        # Degree of r0 and r1
        deg_r0 = r0.bit_length() - 1 if r0 > 0 else -1
        deg_r1 = r1.bit_length() - 1 if r1 > 0 else -1

        if deg_r1 <= 0:
            break

        # Compute quotient and remainder
        shift = deg_r0 - deg_r1
        if shift >= 0:
            r0 ^= r1 << shift
            s0 ^= s1 << shift
            t0 ^= t1 << shift

        # Swap variables
        r0, r1 = r1, r0
        s0, s1 = s1, s0
        t0, t1 = t1, t0

    # Ensures result is in the field (0-255)
    return s1 & 0xFF


# Function that performs division in GF(2^8) (multiplication by the inverse)
def divide_GF(a, b):
    if b == 0:
        raise ValueError("Division by zero in GF(2^8)")

    # Find the multiplicative inverse of b
    b_inverse = inverse_GF(b)

    # Multiply a by the inverse of b
    return multiply_GF(a, b_inverse)


# Function that processes a single calculation from an input file's line
def perform_calculation(line):
    parts = line.strip().split()
    if len(parts) != 3:
        raise ValueError(f"Invalid input format: {line}")

    a_bin, b_bin, op = parts
    a = binary_to_int(a_bin)
    b = binary_to_int(b_bin)

    if op == '+':
        result = add_GF(a, b)
    elif op == '-':
        result = subtract_GF(a, b)
    elif op == '*':
        result = multiply_GF(a, b)
    elif op == '/':
        try:
            result = divide_GF(a, b)
        except ValueError as e:
            return f"Error: {e}"
    else:
        return f"Error: Unknown operation {op}"

    return int_to_binary(result)


# Function that processes all calculations from input file; writes to output file
def process_files(input_file_path, output_file_path):
    with open(input_file_path, 'r') as infile, open(output_file_path, 'w') as outfile:
        for line in infile:
            if line.strip():  # Skip empty lines
                result = perform_calculation(line)
                outfile.write(f"{result}\n")


# Main function that tests the program with both input files
def main():
    # Test with the provided input file
    process_files("class_input_5C.txt", "class_output_5C.txt")

    # Test with my own calculations , Wh
    process_files("reyes_input_5C.txt", "reyes_output_5C.txt")


if __name__ == "__main__":
    main()
