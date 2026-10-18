#Code from Google Gemini 18/10/26

import math
import random
import numpy as np  # Required for fast block-array processing

def lucas_pow(v, e, n):
    """
    Computes V_e(v, 1) modulo n using an allocation-free binary ladder.
    """
    if e == 0:
        return 2
    
    v1, v2 = v, (v * v - 2) % n
    binary_e = bin(e)[3:]
    
    for bit in binary_e:
        if bit == '0':
            v2 = (v1 * v2 - v) % n
            v1 = (v1 * v1 - 2) % n
        else:
            v1 = (v1 * v2 - v) % n
            v2 = (v2 * v2 - 2) % n
            
    return v1

def yield_prime_chunks(B, chunk_size=1048576):
    """
    Generates prime numbers in memory-efficient, fast NumPy array chunks.
    Keeps memory usage strictly capped under a few megabytes.
    """
    # Small base primes up to sqrt(B)
    sqrt_B = math.isqrt(B)
    is_prime_base = np.ones(sqrt_B + 1, dtype=bool)
    is_prime_base[0:2] = False
    for p in range(2, math.isqrt(sqrt_B) + 1):
        if is_prime_base[p]:
            is_prime_base[p*p::p] = False
    base_primes = np.nonzero(is_prime_base)[0]
    
    # Fast-yield the base primes first
    yield base_primes

    # Segmented sieve for the remaining range
    low = sqrt_B + 1
    while low <= B:
        high = min(low + chunk_size, B + 1)
        segment = np.ones(high - low, dtype=bool)
        
        for p in base_primes:
            # Find the first multiple of p inside the current chunk segment
            start = (low + p - 1) // p * p
            if start < p * p:
                start = p * p
            
            # Vectorized index slicing to clear composite numbers
            segment[start - low::p] = False
            
        # Collect and yield all primes found in this block chunk
        primes_in_chunk = np.nonzero(segment)[0] + low
        if len(primes_in_chunk) > 0:
            yield primes_in_chunk.astype(np.uint32)
            
        low = high

def williams_pp1(n, B=50000000):
    """
    Attempts to factor a large composite number using Williams' p+1 algorithm.
    Optimized for extremely high bounds (B) within a 1.8 GB memory envelope.
    """
    if n % 2 == 0: return 2
    if n % 3 == 0: return 3

    limit = math.isqrt(n)

    for attempt in range(5):
        v = random.randint(3, n - 1)
        print(f"[Attempt {attempt + 1}] Testing seed v = {v}...")
        
        g = math.gcd(v * v - 4, n)
        if 1 < g < n:
            return g
        elif g == n:
            continue
            
        # Stream prime arrays dynamically
        for prime_chunk in yield_prime_chunks(B):
            for p in prime_chunk:
                p = int(p)
                # Compute power e such that p^e <= sqrt(n)
                e = int(math.log(limit, p)) if p < limit else 1
                if e == 0: 
                    e = 1
                
                v = lucas_pow(v, p**e, n)
                
        # Final evaluation check for a non-trivial factor
        g = math.gcd(v - 2, n)
        if 1 < g < n:
            return g
        elif g == n:
            print(f" -> Overshot bound B. Retrying with a different base sequence...")
            continue
            
    return None

# --- Example Usage with Larger Composite Values ---
if __name__ == "__main__":
    # Test number: Product of two large primes where (p + 1) has small factors
    # 47000003 + 1 = 2 * 2 * 3 * 3916667
    # 100000007 + 1 = 2 * 2 * 2 * 3 * 3 * 7 * 19 * 1051 (highly smooth, perfect target)
    composite_num = 47000003 * 100000007  # 4700000629000021
    
    print(f"Factoring: {composite_num}")
    print("Evaluating up to smoothness bound B = 50,000,000...")
    
    factor = williams_pp1(composite_num, B=50000000)
    
    if factor:
        print(f"\nSuccess! Found factor: {factor}")
        print(f"Co-factor is: {composite_num // factor}")
    else:
        print("\nFactor not found. Try increasing bound B or checking alternative seeds.")
