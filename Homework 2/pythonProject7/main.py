# Extended Euclidean Algorithm program
# Irving Reyes Bravo
# 02/25/2025


# Computes the GCD of a and b using the Extended Euclidean Algorithm.
def extended_euclidean(a, b):
    r_prev, r = a, b
    x_prev, x = 1, 0
    y_prev, y = 0, 1

    table = []  # Store table rows

    i = -1
    while r != 0:
        i += 1
        q = r_prev // r
        r_prev, r = r, r_prev - q * r
        x_prev, x = x, x_prev - q * x
        y_prev, y = y, y_prev - q * y
        table.append([i, r_prev, q if i >= 0 else "", x_prev, y_prev])

    # If GCD is not 1, no multiplicative inverse exists
    gcd = r_prev
    if gcd != 1:
        return None, table

    # Return x_prev as the modular inverse (mod b)
    return x_prev % b, table


# Writes the Extended Euclidean Algorithm steps to a file.
def write_table_to_file(a, b, inverse, table, filename="output.txt"):
    with open(filename, "w") as f:
        f.write(f"Extended Euclidean Algorithm for a = {a}, b = {b}\n")
        f.write(f"Multiplicative Inverse: {inverse}\n" if inverse else "No Inverse Exists\n")
        f.write("\nTable:\n")
        f.write("i   |   r_i   |   q_i   |   x_i   |   y_i   \n")
        f.write("-" * 40 + "\n")
        for row in table:
            f.write(f"{row[0]:<3} | {row[1]:<7} | {row[2]:<6} | {row[3]:<7} | {row[4]:<7}\n")


# Test cases
problems = [(550, 1769), (950, 1767), (8144, 39901)]
for a, b in problems:
    inverse, table = extended_euclidean(a, b)
    write_table_to_file(a, b, inverse, table, f"output_{a}_{b}.txt")
    print(f"Processed (a={a}, b={b}). Output saved to output_{a}_{b}.txt")

