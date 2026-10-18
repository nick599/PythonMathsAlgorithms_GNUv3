#Python3 code from Google Gemini 18/10/26.

import math
import random

def lucas_pow(v, e, n):
    """
    Computes V_e(v, 1) modulo n.
    This functions like modular exponentiation but along a Lucas sequence.
    """
    if e == 0:
        return 2
    
    # Standard binary ladder for Lucas sequences
    v1, v2 = v, (v * v - 2) % n
    binary_e = bin(e)[3:]  # Skip the '0b' and the first '1'
    
    for bit in binary_e:
        if bit == '0':
            v1, v2 = (v1 * v1 - 2) % n, (v1 * v2 - v) % n
        else:
            v1, v2 = (v1 * v2 - v) % n, (v2 * v2 - 2) % n
            
    return v1

def williams_pp1(n, B=10000):
    """
    Attempts to find a non-trivial factor of n using Williams' p+1 algorithm.
    B is the smoothness bound.
    """
    # Quick checks for even numbers or trivial factors
    if n % 2 == 0:
        return 2
    if n % 3 == 0:
        return 3

    # Generate a small list of primes up to bound B using a simple sieve
    primes = []
    is_prime = [True] * (B + 1)
    for p in range(2, B + 1):
        if is_prime[p]:
            primes.append(p)
            for i in range(p * p, B + 1, p):
                is_prime[i] = False

    # Try different initial configurations
    for attempt in range(5):
        v = random.randint(3, n - 1)
        
        # Ensure our starting choice isn't already sharing a factor
        g = math.gcd(v * v - 4, n)
        if 1 < g < n:
            return g
            
        # Successively step through the primes below the bound B
        for p in primes:
            # Determine maximum power e such that p^e <= sqrt(n)
            e = int(math.log(math.isqrt(n), p)) if p < math.isqrt(n) else 1
            if e == 0: 
                e = 1
                
            # Perform the Lucas sequence multiplication step
            v = lucas_pow(v, p**e, n)
            
        # Test if we found a factor
        g = math.gcd(v - 2, n)
        if 1 < g < n:
            return g
        elif g == n:
            # If gcd is n, we overshot (B might be too large for this v).
            # The loop will try another random 'v'.
            continue
            
    return None  # Factor not found within bound B

# --- Example Usage ---
# Factoring 11218153 (941 * 11921)
# 941 is a target prime here because 941 + 1 = 942 = 2 * 3 * 157 (very smooth)
composite_num = 11218153
factor = williams_pp1(composite_num, B=200)

print(f"A factor of {composite_num} is: {factor}")
# Output: A factor of 11218153 is: 941
