import sys

# Permuted Choice Table 1 (PC-1)

PC_1 = [
    57, 49, 41, 33, 25, 17, 9,
     1, 58, 50, 42, 34, 26, 18,
    10,  2, 59, 51, 43, 35, 27,
    19, 11,  3, 60, 52, 44, 36,
    63, 55, 47, 39, 31, 23, 15,
     7, 62, 54, 46, 38, 30, 22,
    14,  6, 61, 53, 45, 37, 29,
    21, 13,  5, 28, 20, 12,  4
    ]

# Permuted Choice Table 2 (PC-2)
PC_2 = [
    14, 17, 11, 24,  1,  5,
     3, 28, 15,  6, 21, 10,
    23, 19, 12,  4, 26,  8,
    16,  7, 27, 20, 13,  2,
    41, 52, 31, 37, 47, 55,
    30, 40, 51, 45, 33, 48,
    44, 49, 39, 56, 34, 53,
    46, 42, 50, 36, 29, 32
]

# Initial Permutation Table (IP)
IP = [
    58, 50, 42, 34, 26, 18, 10,  2,
    60, 52, 44, 36, 28, 20, 12,  4,
    62, 54, 46, 38, 30, 22, 14,  6,
    64, 56, 48, 40, 32, 24, 16,  8,
    57, 49, 41, 33, 25, 17,  9,  1,
    59, 51, 43, 35, 27, 19, 11,  3,
    61, 53, 45, 37, 29, 21, 13,  5,
    63, 55, 47, 39, 31, 23, 15,  7
]

# Inverse Initial Permutation Table (IP-INV)
IP_INV = [
    40,  8, 48, 16, 56, 24, 64, 32,
    39,  7, 47, 15, 55, 23, 63, 31,
    38,  6, 46, 14, 54, 22, 62, 30,
    37,  5, 45, 13, 53, 21, 61, 29,
    36,  4, 44, 12, 52, 20, 60, 28,
    35,  3, 43, 11, 51, 19, 59, 27,
    34,  2, 42, 10, 50, 18, 58, 26,
    33,  1, 41,  9, 49, 17, 57, 25
]

# Expansion Table (E)
E = [
    32,  1,  2,  3,  4,  5,
     4,  5,  6,  7,  8,  9,
     8,  9, 10, 11, 12, 13,
    12, 13, 14, 15, 16, 17,
    16, 17, 18, 19, 20, 21,
    20, 21, 22, 23, 24, 25,
    24, 25, 26, 27, 28, 29,
    28, 29, 30, 31, 32,  1
]

# Permutation P
P = [
    16,  7, 20, 21,
    29, 12, 28, 17,
     1, 15, 23, 26,
     5, 18, 31, 10,
     2,  8, 24, 14,
    32, 27,  3,  9,
    19, 13, 30,  6,
    22, 11,  4, 25
]

# S-boxes (S1 to S8)
S_BOX = {
    0: [
        [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
        [ 0,15, 7, 4,14, 2,13, 1,10, 6,12,11, 9, 5, 3, 8],
        [ 4, 1,14, 8,13, 6, 2,11,15,12, 9, 7, 3,10, 5, 0],
        [15,12, 8, 2, 4, 9, 1, 7, 5,11, 3,14,10, 0, 6,13]
    ],
    1: [
        [15, 1, 8,14, 6,11, 3, 4, 9, 7, 2,13,12, 0, 5,10],
        [ 3,13, 4, 7,15, 2, 8,14,12, 0, 1,10, 6, 9,11, 5],
        [ 0,14, 7,11,10, 4,13, 1, 5, 8,12, 6, 9, 3, 2,15],
        [13, 8,10, 1, 3,15, 4, 2,11, 6, 7,12, 0, 5,14, 9]
    ],
    2: [
        [10, 0, 9,14, 6, 3,15, 5, 1,13,12, 7,11, 4, 2, 8],
        [13, 7, 0, 9, 3, 4, 6,10, 2, 8, 5,14,12,11,15, 1],
        [13, 6, 4, 9, 8,15, 3, 0,11, 1, 2,12, 5,10,14, 7],
        [ 1,10,13, 0, 6, 9, 8, 7, 4,15,14, 3,11, 5, 2,12]
    ],
    3: [
        [ 7,13,14, 3, 0, 6, 9,10, 1, 2, 8, 5,11,12, 4,15],
        [13, 8,11, 5, 6,15, 0, 3, 4, 7, 2,12, 1,10,14, 9],
        [10, 6, 9, 0,12,11, 7,13,15, 1, 3,14, 5, 2, 8, 4],
        [ 3,15, 0, 6,10, 1,13, 8, 9, 4, 5,11,12, 7, 2,14]
    ],
    4: [
        [ 2,12, 4, 1, 7,10,11, 6, 8, 5, 3,15,13, 0,14, 9],
        [14,11, 2,12, 4, 7,13, 1, 5, 0,15,10, 3, 9, 8, 6],
        [ 4, 2, 1,11,10,13, 7, 8,15, 9,12, 5, 6, 3, 0,14],
        [11, 8,12, 7, 1,14, 2,13, 6,15, 0, 9,10, 4, 5, 3]
    ],
    5: [
        [12, 1,10,15, 9, 2, 6, 8, 0,13, 3, 4,14, 7, 5,11],
        [10,15, 4, 2, 7,12, 9, 5, 6, 1,13,14, 0,11, 3, 8],
        [ 9,14,15, 5, 2, 8,12, 3, 7, 0, 4,10, 1,13,11, 6],
        [ 4, 3, 2,12, 9, 5,15,10,11,14, 1, 7, 6, 0, 8,13]
    ],
    6: [
        [ 4,11, 2,14,15, 0, 8,13, 3,12, 9, 7, 5,10, 6, 1],
        [13, 0,11, 7, 4, 9, 1,10,14, 3, 5,12, 2,15, 8, 6],
        [ 1, 4,11,13,12, 3, 7,14,10,15, 6, 8, 0, 5, 9, 2],
        [ 6,11,13, 8, 1, 4,10, 7, 9, 5, 0,15,14, 2, 3,12]
    ],
    7: [
        [13, 2, 8, 4, 6,15,11, 1,10, 9, 3,14, 5, 0,12, 7],
        [ 1,15,13, 8,10, 3, 7, 4,12, 5, 6,11, 0,14, 9, 2],
        [ 7,11, 4, 1, 9,12,14, 2, 0, 6,10,13,15, 3, 5, 8],
        [ 2, 1,14, 7, 4,10, 8,13,15,12, 9, 0, 3, 5, 6,11]
    ]
}

# Left bit shifts per Round 1 - 16
SHIFT_SCHEDULE = [
    1, 1, 2, 2, 2, 2, 2, 2,
    1, 2, 2, 2, 2, 2, 2, 1
]

# Helper functions

def hex_to_bin(hex_str):
    """ Converts the hex string to int base 16. zfill ensures that
    the hex digit is 4 bits. Returns a list of 1s and 0s"""
    bin_str = bin(int(hex_str, 16))[2:].zfill(len(hex_str) * 4)
    return [int(b) for b in bin_str]

def bin_to_hex(bin_list):
    """ Join list of bits into string, convert bits to int,
    then convert to hex string and remove 0x prefix."""
    hex_str = hex(int(''.join(map(str, bin_list)), 2))[2:].upper()
    return hex_str.zfill(len(bin_list)//4)

def permute(bits, table):
    """ Reorders bits based on permutation table. """
    return [bits[i - 1] for i in table]

def left_shift(bits, n):
    """ Left shift bit rotation by n. """
    return bits[n:] + bits[:n]

def xor(bits1, bits2):
    """ Acts as xor bitwise operand for parameter pairs. """
    return [b1 ^ b2 for b1, b2 in zip(bits1, bits2)]

def sbox_substitute(bits):
    """ Substitutes the 48-bit input using the s-boxes into a 32 bit output. """
    result = []
    for i in range(8):
        # Divide the blocks into 6 bits
        block = bits[i*6:(i+1)*6]
        # Determine row and columns for s-box lookup
        row = (block[0] << 1) + block[5]
        column = (block[1] << 3) + (block[2] << 2) + (block[3] << 1) + block[4]
        # s-box lookup
        sbox_val = S_BOX[i][row][column]
        # Convert s-box values into 4-bit
        bin_val = [int(b) for b in bin(sbox_val)[2:].zfill(4)]
        result.extend(bin_val)
    return result

def f_function(R, K):
    """ Takes 32-bit right and 48-bit subkey K"""
    # Expansion
    R_expansion = permute(R, E)
    # XOR with subkey
    R_xor_K = xor(R_expansion, K)
    # S-box substitution
    R_sbox = sbox_substitute(R_xor_K)
    # P Permutation
    R_P = permute(R_sbox, P)
    return R_P

def generate_subkeys(key):
    """ Generates 16 subkeys, one for each round"""
    # PC-1
    key_pc1 = permute(key, PC_1)
    # Split into C and D halves
    C = key_pc1[:28]
    D = key_pc1[28:]
    subkeys = []
    for shift in SHIFT_SCHEDULE:
        # Left shifts
        C = left_shift(C, shift)
        D = left_shift(D, shift)
        # PC-2
        subkey = permute(C + D, PC_2)
        subkeys.append(subkey)
    return subkeys

def encrypt_block(plaintext_block, subkeys):
    """ Encrypts a 64-bit block of plaintext """
    # Initial Permutation
    block = permute(plaintext_block, IP)
    L, R = block[:32], block[32:]
    # 16 rounds
    for i in range(16):
        L_new = R
        R_new = xor(L, f_function(R, subkeys[i]))
        L, R = L_new, R_new
    # Combine R16 and L16
    combined = R + L
    # Final Permutation
    ciphertext_block = permute(combined, IP_INV)
    return ciphertext_block

def decrypt_block(ciphertext_block, subkeys):
    """ Same as the encryption block, but in reverse order. """
    # Initial Permutation
    block = permute(ciphertext_block, IP)
    L, R = block[:32], block[32:]
    # 16 rounds (reverse order of subkeys)
    for i in range(15, -1, -1):
        L_new = R
        R_new = xor(L, f_function(R, subkeys[i]))
        L, R = L_new, R_new
    # Combine R16 and L16
    combined = R + L
    # Final Permutation
    plaintext_block = permute(combined, IP_INV)
    return plaintext_block

# Functions to encrypt or decrypt data
def encrypt(plaintext_hex, key_hex):
    key_bits = hex_to_bin(key_hex)
    subkeys = generate_subkeys(key_bits)
    plaintext_bits = hex_to_bin(plaintext_hex)
    ciphertext_bits = encrypt_block(plaintext_bits, subkeys)
    ciphertext_hex = bin_to_hex(ciphertext_bits)
    return ciphertext_hex

def decrypt(ciphertext_hex, key_hex):
    key_bits = hex_to_bin(key_hex)
    subkeys = generate_subkeys(key_bits)
    ciphertext_bits = hex_to_bin(ciphertext_hex)
    plaintext_bits = decrypt_block(ciphertext_bits, subkeys)
    plaintext_hex = bin_to_hex(plaintext_bits)
    return plaintext_hex

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  To encrypt: python des.py encrypt <plaintext_hex> <key_hex>")
        print("  To decrypt: python des.py decrypt <ciphertext_hex> <key_hex>")
        sys.exit(1)

    mode = sys.argv[1].lower()
    input_hex = sys.argv[2]
    key_hex = sys.argv[3]

    # Check to make sure input and key are 16 hex chars (64 bits)
    input_hex = input_hex.upper().ljust(16, '0')[:16]
    key_hex = key_hex.upper().ljust(16, '0')[:16]

    if mode == 'encrypt':
        ciphertext_hex = encrypt(input_hex, key_hex)
        print(f'Ciphertext: {ciphertext_hex}')
    elif mode == 'decrypt':
        plaintext_hex = decrypt(input_hex, key_hex)
        print(f'Plaintext: {plaintext_hex}')
    else:
        print("Invalid mode. Use 'encrypt' or 'decrypt'.")

if __name__ == "__main__":
    main()
