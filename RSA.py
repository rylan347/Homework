import random
import sys

def is_prime(num):
    """Check if number is prime."""
    if num <= 1:
        return False
    if num <= 3:
        return True
    # Check for divisibility by 2 and 3
    if num % 2 == 0 or num % 3 == 0:
        return False
    # Check the rest
    i = 5
    while i * i <= num:
        if num % i == 0 or num % (i + 2) == 0:
            return False
        i += 6
    return True

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def choose_e(phi_n):
    """ Choose int e such that 1 < e < phi_n and gcd(e phi_n) = 1. """
    e = 3
    while e < phi_n:
        if gcd(e, phi_n) == 1:
            return e
        e += 2 
    raise Exception("Failed to increment e.")

def choose_d(e, phi_n):
    """ Calculate d by finding inverse of e % phi_n. """
    def egcd(a, b):
        if a == 0:
            return b, 0, 1
        gcd_val, x1, y1 = egcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd_val, x, y
    gcd_val, x, y = egcd(e, phi_n)
    if gcd_val != 1:
        raise Exception("Error calculating d.")
    else:
        return x % phi_n

def generate_keys(P, Q):
    """ Generate RSA public and private keys. """
    if not (is_prime(P) and is_prime(Q)):
        raise ValueError("Both numbers must be prime.")
    elif P == Q:
        raise ValueError("P and Q need to be different values.")
    # Computer n and ph(n)
    phi_n = (P-1)(Q-1)
    # Choose e
    e = choose_e(phi_n)
    # Choose d
    d = choose_d(2, phi_n)
    # Return public and private keys
    return ((n, e), (n, d))

def main():
    # Accept user input for P and Q
    try:
        P = int(input("Enter a prime number P: "))
        Q = int(input("Enter a prime number Q: "))
    except ValueError:
        print("Please enter an integer for P and Q")
        sys.exit(1)
    try:
        public_key, private_key = generate_keys(P, Q)



print(is_prime(51))
