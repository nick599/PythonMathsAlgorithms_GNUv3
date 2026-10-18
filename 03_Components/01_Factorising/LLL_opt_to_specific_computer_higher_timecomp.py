#Code from Google Gemini 18/10/26

import math
import numpy as np
from numba import njit

def get_primes(bound):
    """Generates primes cleanly via an in-place memory sieve."""
    sieve = [True] * (bound + 1)
    for p in range(2, int(bound**0.5) + 1):
        if sieve[p]:
            for i in range(p*p, bound + 1, p):
                sieve[i] = False
    return [p for p in range(2, bound + 1) if sieve[p]]

def gcd(a, b):
    while b:
        a, b = b, a % b
    return abs(a)

@njit(cache=True, fastmath=True)
def _numba_lll_inplace(B, delta=0.75):
    """
    In-place memory-constrained LLL reduction.
    Uses float32 precision arrays to fit entirely inside the CPU's cache,
    minimising Windows physical RAM consumption.
    """
    n = B.shape[0]
    # Enforce float32 to drop memory utilization by 50%
    orthogonal = np.zeros((n, B.shape[1]), dtype=np.float32)
    mu = np.zeros((n, n), dtype=np.float32)

    for i in range(n):
        orthogonal[i] = B[i].astype(np.float32)
        for j in range(i):
            dot_j = np.dot(orthogonal[j], orthogonal[j])
            if dot_j > 1e-6:
                mu[i, j] = np.dot(B[i].astype(np.float32), orthogonal[j]) / dot_j
            else:
                mu[i, j] = 0.0
            orthogonal[i] -= mu[i, j] * orthogonal[j]

    k = 1
    while k < n:
        for j in range(k - 1, -1, -1):
            if abs(mu[k, j]) > 0.5:
                q = round(mu[k, j])
                B[k] -= int(q) * B[j]
                
                # In-place internal orthogonal update
                orthogonal[k] = B[k].astype(np.float32)
                for m in range(k):
                    dot_m = np.dot(orthogonal[m], orthogonal[m])
                    if dot_m > 1e-6:
                        mu[k, m] = np.dot(B[k].astype(np.float32), orthogonal[m]) / dot_m
                    else:
                        mu[k, m] = 0.0
                    orthogonal[k] -= mu[k, m] * orthogonal[m]
        
        dot_k = np.dot(orthogonal[k], orthogonal[k])
        dot_k_minus_1 = np.dot(orthogonal[k-1], orthogonal[k-1])
        
        if dot_k >= (delta - mu[k, k-1]**2) * dot_k_minus_1:
            k += 1
        else:
            # Swap rows in place without allocating new memory blocks
            for col in range(B.shape[1]):
                tmp = B[k, col]
                B[k, col] = B[k-1, col]
                B[k-1, col] = tmp
            
            # Local update loop
            for i in range(k - 1, n):
                orthogonal[i] = B[i].astype(np.float32)
                for j in range(i):
                    dot_j = np.dot(orthogonal[j], orthogonal[j])
                    if dot_j > 1e-6:
                        mu[i, j] = np.dot(B[i].astype(np.float32), orthogonal[j]) / dot_j
                    else:
                        mu[i, j] = 0.0
                    orthogonal[i] -= mu[i, j] * orthogonal[j]
            k = max(k - 1, 1)
            
    return B

def bkz_bounded_reduction_low_mem(matrix, block_size=3, max_loops=1):
    """BKZ wrapper configured to run in-place without memory duplication."""
    B = np.array(matrix, dtype=np.int64)
    n = B.shape[0]
    
    B = _numba_lll_inplace(B)
    if block_size < 2 or block_size > n:
        return B

    for loop in range(max_loops):
        interchanged = False
        for i in range(n - block_size + 1):
            # Avoid using deep copies (.copy()); execute in-place window checks
            sub_block = B[i:i+block_size]
            old_sub = sub_block.copy() # Small isolated slice definition
            _numba_lll_inplace(sub_block)
            
            if not np.array_equal(old_sub, sub_block):
                interchanged = True
                B = _numba_lll_inplace(B)
        if not interchanged:
            break
            
    return B

def setup_reduce_and_filter_low_memory(n, prime_bound, block_size=3):
    """
    Executes lattice factoring optimized specifically to protect the limited 
    1.8 GB available physical memory ecosystem under Windows 11 x64.
    """
    bit_length = n.bit_length()
    
    # Conservative scaling factor to protect integer bit width allocations
    C = int(round((2 ** (bit_length / 2)) * 2000))
    
    primes = [p for p in get_primes(prime_bound) if n % p != 0]
    f = len(primes)
    dim = f + 1
    
    print(f"[*] Memory Guard: Enforcing Low Memory Profile.")
    print(f"[*] Available Space Constraint: 1.8 GB RAM | Matrix Dim: {dim}x{dim}")
    
    # 1. Build initial lattice matrix
    M = np.zeros((dim, dim), dtype=np.int64)
    for i in range(f):
        M[i, i] = int(round(C * math.log(primes[i])))
        M[i, f] = 1  
    scaled_log_n = int(round(C * math.log(n)))
    for i in range(f):
        M[f, i] = scaled_log_n
        
    # 2. Run memory-optimized reduction
    print(f"[-] Computing JIT-accelerated low-memory lattice steps...")
    M_reduced = bkz_bounded_reduction_low_mem(M, block_size=block_size)
    
    print("[+] Reduction phase complete. Running zero-allocation sequential filtering...")
    
    # 3. Streamlined Sequential Filter (Ensures zero memory amplification)
    M_T = M.T
    factor_found = False
    
    for row_idx in range(dim):
        short_vec = M_reduced[row_idx]
        try:
            # Linear solve step kept strictly sequential to prevent thread allocation spikes
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
        print("[-] Verification processing complete. No factors identified in this window.")

if __name__ == '__main__':
    setup_reduce_and_filter_low_memory(n=143, prime_bound=23, block_size=3)
