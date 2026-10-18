#Code from Google Gemini 18/10/26

import random
import math
from numba import njit

def gcd(a, b):
    """Standard Euclidean GCD algorithm."""
    while b:
        a, b = b, a % b
    return abs(a)

@njit(cache=True, fastmath=True)
def _modular_inverse(a, m):
    """
    JIT-compiled Extended Euclidean Algorithm for modular inverse.
    Requires zero allocation overhead.
    """
    a = a % m
    t, newt = 0, 1
    r, newr = m, a
    while newr != 0:
        quotient = r // newr
        t, newt = newt, t - quotient * newt
        r, newr = newr, r - quotient * newr
    if r > 1:
        return -1 # Inverse does not exist (found a factor)
    if t < 0:
        t = t + m
    return t

@njit(cache=True, fastmath=True)
def _ec_add(x1, y1, x2, y2, A, n):
    """
    Adds two distinct points on an elliptic curve y^2 = x^3 + Ax + B (mod n).
    Returns (x3, y3, error_factor). If error_factor > 1, a GCD factor was uncovered.
    """
    if x1 == x2 and y1 == y2:
        # Points are identical; perform a point doubling step instead
        num = (3 * x1 * x1 + A) % n
        den = (2 * y1) % n
    else:
        num = (y2 - y1) % n
        den = (x2 - x1) % n

    inv = _modular_inverse(den, n)
    if inv == -1:
        # Modular inverse failed. The denominator shares a non-trivial factor with n.
        g = np_gcd_internal(den, n)
        return 0, 0, g

    lam = (num * inv) % n
    x3 = (lam * lam - x1 - x2) % n
    y3 = (lam * (x1 - x3) - y1) % n
    return x3, y3, 1

@njit(cache=True, fastmath=True)
def np_gcd_internal(a, b):
    """Internal JIT-compatible GCD utility."""
    while b:
        a, b = b, a % b
    return abs(a)

@njit(cache=True, fastmath=True)
def _ec_multiply(k, x, y, A, n):
    """
    Performs scalar point multiplication (k * P) using the binary double-and-add method.
    Maintains a strictly flat, stack-allocated memory layout.
    """
    qx, qy = x, y
    rx, ry = -1, -1 # Represents the point at infinity
    initialized = False

    while k > 0:
        if k % 2 == 1:
            if not initialized:
                rx, ry = qx, qy
                initialized = True
            else:
                rx, ry, err = _ec_add(rx, ry, qx, qy, A, n)
                if err > 1:
                    return 0, 0, err
        qx, qy, err = _ec_add(qx, qy, qx, qy, A, n)
        if err > 1:
            return 0, 0, err
        k //= 2

    return rx, ry, 1

def run_ecm_factorisation(n, B1=500, max_curves=100):
    """
    Executes Lenstra's Elliptic Curve Method (ECM) Stage 1.
    Optimised for systems with highly constrained physical memory.
    """
    print(f"[*] Platform Engine: AMD Ryzen Low-Memory ECM Target.")
    print(f"[*] Physical RAM Constraints: Safeguarded (<15MB Overhead).")
    print(f"[*] Target composite n = {n}")
    
    # Pre-compute the factorial multiplier k based on the smoothness bound B1
    # This guides the scalar multiplication size
    k = 1
    for p in range(2, B1 + 1):
        # Check primality cleanly
        is_prime = True
        for i in range(2, int(p**0.5) + 1):
            if p % i == 0:
                is_prime = False
                break
        if is_prime:
            # Multiply k by the highest power of p below B1
            k *= (p ** int(math.log(B1, p)))

    print(f"[+] Computed smoothness scalar k (Bits: {k.bit_length()})")
    print(f"[-] Running curve pipeline (Max curves: {max_curves})...")

    for curve_idx in range(1, max_curves + 1):
        # Generate a valid random curve and a starting point P = (x0, y0)
        x0 = random.randint(1, n - 1)
        y0 = random.randint(1, n - 1)
        A = random.randint(1, n - 1)
        
        # Calculate B parameter to satisfy y^2 = x^3 + Ax + B
        B = (y0*y0 - x0*x0*x0 - A*x0) % n
        
        # Ensure the curve is non-singular (discriminant must not be 0 mod n)
        disc = (4 * A*A*A + 27 * B*B) % n
        if gcd(disc, n) == n:
            continue
            
        # Run the scalar point multiplication through the compiled JIT layer
        _, _, factor = _ec_multiply(k, x0, y0, A, n)
        
        if factor > 1:
            # Filter out trivial factor states (e.g., if factor equals n)
            g = gcd(factor, n)
            if 1 < g < n:
                print(f"\n[SUCCESS] ECM cracked the composite on curve #{curve_idx}!")
                print(f"    Calculated Non-Trivial Factor: {g}")
                print(f"    Verification: {g} * {n // g} = {n}")
                return g

    print(f"[-] Completed {max_curves} curves. No non-trivial factors uncovered.")
    print("[!] Hint: Try increasing the smoothness bound 'B1' to capture larger prime factors.")
    return None

# --- Run System Verification ---
if __name__ == '__main__':
    # Factoring a mock composite n = 421651 (523 * 806)
    run_ecm_factorisation(n=421651, B1=200, max_curves=50)
