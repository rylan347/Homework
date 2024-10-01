import random
import sys

def is_prime(num):
    """Check if a number is prime using a simple method."""
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

print(is_prime(51))
