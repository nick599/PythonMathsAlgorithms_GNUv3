#Code from Google Gemini 18/10/26

import math
import numpy as np

def get_primes(bound):
    """Returns a list of primes up to the bound."""
    primes = []
    for possiblePrime in range(2, bound + 1):
        isPrime = True
        for num in range(2, int(possiblePrime ** 0.5) + 1):
            if possiblePrime % num == 0:
                isPrime = False
                break
        if isPrime:
            primes.append(possiblePrime)
    return primes

def lll_reduction(matrix, delta=0.75):
    """
    A native Python implementation of the LLL lattice reduction algorithm.
    Operates on row vectors.
    """
    B = np.array(matrix, dtype=np.float64)
    n = B.shape[0]
    orthogonal = np.zeros_like(B)
    mu = np.zeros((n, n))

    def gram_schmidt():
        for i in range(n):
            orthogonal[i] = B[i]
            for j in range(i):
                mu[i, j] = np.dot(B[i], orthogonal[j]) / np.dot(orthogonal[j], orthogonal[j])
                orthogonal[i] -= mu[i, j] * orthogonal[j]

    gram_schmidt()
    k = 1
    while k < n:
        # Size reduction step
        for j in reversed(range(k)):
            if abs(mu[k, j]) > 0.5:
                q = round(mu[k, j])
                B[k] -= q * B[j]
                gram_schmidt()
        
        # Lovász condition check
        if np.dot(orthogonal[k], orthogonal[k]) >= (delta - mu[k, k-1]**2) * np.dot(orthogonal[k-1], orthogonal[k-1]):
            k += 1
        else:
            # Swap vectors
            B[k], B[k-1] = B[k-1].copy(), B[k].copy()
            gram_schmidt()
            k = max(k - 1, 1)
            
    return np.round(B).astype(np.int64)

def setup_and_reduce_lattice_py(n, prime_bound, C=1000):
    """
    Sets up a Schnorr-style factoring lattice in pure Python and reduces it.
    """
    primes = [p for p in get_primes(prime_bound) if n % p != 0]
    f = len(primes)
    dim = f + 1
    
    print(f"[*] Target composite n = {n}")
    print(f"[*] Prime base ({f} primes): {primes}")
    print(f"[*] Lattice dimension: {dim}x{dim}\n")
    
    # Initialize a zero matrix of size (dim, dim)
    # Rows will represent our basis vectors for the LLL implementation
    M = np.zeros((dim, dim), dtype=np.int64)
    
    # Populate the basis vectors (Rows 0 to f-1 represent primes)
    for i in range(f):
        scaled_log = int(round(C * math.log(primes[i])))
        M[i, i] = scaled_log
        M[i, f] = 1  # Index weight constraint
        
    # Row f (the last row) represents the target number n
    scaled_log_n = int(round(C * math.log(n)))
    for i in range(f):
        M[f, i] = scaled_log_n
    M[f, f] = 0
    
    print("[-] Original Matrix Basis:")
    print(M)
    print("\n" + "="*50 + "\n")
    
    # Perform LLL Reduction on rows
    M_reduced = lll_reduction(M)
    
    print("[+] LLL Reduced Matrix Basis (Shortest vectors on top rows):")
    print(M_reduced)
    print("\n" + "="*50 + "\n")
    
    # Grab the shortest vector (Row 0)
    shortest_vector = M_reduced[0]
    print(f"[+] Target Shortest Vector: {list(shortest_vector)}")
    
    # Reconstruct the structural equation:
    # A vector close to 0 means: e_1*log(p_1) + ... - e_{f+1}*log(n) ≈ 0
    # We look for terms that reveal multiplicative approximations.
    print("[*] Algorithmic next step: Parse geometric vector back into prime exponents.")

# --- Run Example ---
# Factoring n = 35 with a small prime base using pure Python 3
setup_and_reduce_lattice_py(n=35, prime_bound=7, C=1000)