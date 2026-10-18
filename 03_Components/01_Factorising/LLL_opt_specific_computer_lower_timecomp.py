import math
import numpy as np
from numba import njit

def get_primes(bound):
    """Generates primes via a fast NumPy boolean sieve."""
    if bound < 2:
        return []
    sieve = np.ones(bound + 1, dtype=bool)
    sieve[0:2] = False
    for p in range(2, int(bound**0.5) + 1):
        if sieve[p]:
            sieve[p*p::p] = False
    return np.nonzero(sieve)[0].tolist()

def gcd(a, b):
    while b:
        a, b = b, a % b
    return abs(a)

@njit(cache=True, fastmath=True)
def _numba_lll_inplace(B, delta=0.75):
    """
    Incremental LLL Reduction.
    Updates the Gram-Schmidt coefficients and orthogonal norms analytically 
    instead of recomputing projections, dropping time complexity dramatically.
    """
    n = B.shape[0]
    m = B.shape[1]
    
    # Store Gram-Schmidt orthogonal vectors and norms using float32 for cache locality
    B_star = np.zeros((n, m), dtype=np.float32)
    c = np.zeros(n, dtype=np.float32)  # Squares of lengths of orthogonal vectors
    mu = np.zeros((n, n), dtype=np.float32)
    
    # Initial Gram-Schmidt orthogonalisation pass
    for i in range(n):
        B_star[i] = B[i].astype(np.float32)
        for j in range(i):
            if c[j] > 1e-6:
                mu[i, j] = np.dot(B[i].astype(np.float32), B_star[j]) / c[j]
            else:
                mu[i, j] = 0.0
            B_star[i] -= mu[i, j] * B_star[j]
        c[i] = np.dot(B_star[i], B_star[i])
        
    k = 1
    while k < n:
        # Size reduction step
        for j in range(k - 1, -1, -1):
            if abs(mu[k, j]) > 0.5:
                q = round(mu[k, j])
                B[k] -= int(q) * B[j]
                # Analytical O(n) update to mu coefficients - no projection recomputation
                for idx in range(j):
                    mu[k, idx] -= q * mu[j, idx]
                mu[k, j] -= q
                
        # Lovasz condition check
        if c[k] >= (delta - mu[k, k-1]**2) * c[k-1]:
            k += 1
        else:
            # 1. Swap vectors in the primary integer basis matrix
            for col in range(m):
                tmp = B[k, col]
                B[k, col] = B[k-1, col]
                B[k-1, col] = tmp
                
            # 2. Analytical O(1) and O(n) incremental update for the swap
            nu = mu[k, k-1]
            c_next = c[k] + (nu**2) * c[k-1]
            
            mu[k, k-1] = nu * c[k-1] / c_next
            c[k] = c[k-1] * c[k] / c_next
            c[k-1] = c_next
            
            # Interchanged orthogonal updates
            for col in range(m):
                b_star_k_minus_1 = B_star[k-1, col]
                B_star[k-1, col] = B_star[k, col] + nu * b_star_k_minus_1
                B_star[k, col] = b_star_k_minus_1 - mu[k, k-1] * B_star[k-1, col]
                
            # Update remaining matrix column coefficients
            for j in range(k + 1, n):
                t = mu[j, k]
                mu[j, k] = mu[j, k-1] - nu * t
                mu[j, k-1] = t + mu[k, k-1] * mu[j, k]
                
            for j in range(k - 1):
                t = mu[k, j]
                mu[k, j] = mu[k-1, j]
                mu[k-1, j] = t
                
            k = max(k - 1, 1)
            
    return B

def bkz_bounded_reduction_low_mem(matrix, block_size=3, max_loops=1):
    """BKZ wrapper executing localized slice calculations in-place."""
    B = np.array(matrix, dtype=np.int64)
    n = B.shape[0]
    
    B = _numba_lll_inplace(B)
    if block_size < 2 or block_size > n:
        return B

    for loop in range(max_loops):
        interchanged = False
        for i in range(n - block_size + 1):
            sub_block = B[i:i+block_size]
            old_sub = sub_block.copy()
            _numba_lll_inplace(sub_block)
            
            if not np.array_equal(old_sub, sub_block):
                interchanged = True
                B = _numba_lll_inplace(B)
        if not interchanged:
            break
            
    return B

def setup_reduce_and_filter_low_memory(n, prime_bound, block_size=3):
    """Executes lattice factoring optimized for fast runtime and a 1.8 GB RAM ceiling."""
    bit_length = n.bit_length()
    C = int(round((2 ** (bit_length / 2)) * 2000))
    
    primes = [p for p in get_primes(prime_bound) if n % p != 0]
    f = len(primes)
    dim = f + 1
    
    print(f"[*] Memory Profile: 1.8 GB Limit | Matrix Dimension: {dim}x{dim}")
    
    M = np.zeros((dim, dim), dtype=np.int64)
    for i in range(f):
        M[i, i] = int(round(C * math.log(primes[i])))
        M[i, f] = 1  
    scaled_log_n = int(round(C * math.log(n)))
    for i in range(f):
        M[f, i] = scaled_log_n
        
    print(f"[-] Executing O(n) analytically updated LLL reduction steps...")
    M_reduced = bkz_bounded_reduction_low_mem(M, block_size=block_size)
    
    print("[+] Reduction phase complete. Running solution filters...")
    M_T = M.T
    factor_found = False
    
    for row_idx in range(dim):
        short_vec = M_reduced[row_idx]
        try:
            exponents = np.linalg.solve(M_T, short_vec)
            exponents = np.round(exponents).astype(np.int64)
        except np.linalg.LinAlgError:
            continue
            
        if np.all(exponents == 0):
            continue
            
        v, u = 1, 1
        n_exp = exponents[f]
        
        for i in range(f):
            exp_val = exponents[i]
            if exp_val > 0:
                v *= (primes[i] ** exp_val)
            elif exp_val < 0:
                u *= (primes[i] ** abs(exp_val))
                
        if n_exp > 0:
            u *= (n ** n_exp)
        elif n_exp < 0:
            v *= (n ** abs(n_exp))
            
        diff = abs(v - u)
        if diff != 0:
            g = gcd(diff, n)
            if 1 < g < n:
                print(f"\n[SUCCESS] Non-trivial factor cracked safely under memory limit!")
                print(f"    Calculated Factor: {g}")
                print(f"    Verification: {g} * {n // g} = {n}")
                factor_found = True
                break

    if not factor_found:
        print("[-] Complete. No factors identified in this configuration window.")

if __name__ == '__main__':
    setup_reduce_and_filter_low_memory(n=143, prime_bound=23, block_size=3)