import numpy as np

def gcd(a, b):
    """Compute the greatest common divisor of a and b."""
    while b != 0:
        a, b = b, a % b
    return a

def egcd(a, b):
    """Extended Euclidean Algorithm.
    Returns (g, x, y) such that g = gcd(a, b) and ax + by = g.
    """
    if a == 0:
        return (b, 0, 1)
    else:
        g, x1, y1 = egcd(b % a, a)
        return (g, y1 - (b // a) * x1, x1)

def mod_inverse(a, m):
    """Compute modular inverse of a modulo m.
    Raises ValueError if inverse does not exist.
    """
    g, x, _ = egcd(a, m)
    if g != 1:
        raise ValueError(f"No modular inverse for {a} mod {m}")
    return x % m

def det_mod(matrix, m):
    """Compute determinant modulo m."""
    det = int(round(np.linalg.det(matrix)))
    return det % m

def adjugate(matrix):
    """Compute adjugate (classical adjoint) of a matrix."""
    return np.round(np.linalg.inv(matrix).T * np.linalg.det(matrix)).astype(int)

def matrix_inverse_mod(matrix, m):
    """Compute modular inverse of a matrix modulo m."""
    det = det_mod(matrix, m)
    if gcd(det, m) != 1:
        raise ValueError("Matrix is not invertible modulo m")
    det_inv = mod_inverse(det, m)
    adj = adjugate(matrix)
    return (det_inv * adj) % m

def mod_mul(matrix, vector, m):
    """Matrix-vector multiplication modulo m."""
    return np.dot(matrix, vector) % m

def mod_add(vec1, vec2, m):
    """Element-wise addition modulo m."""
    return (vec1 + vec2) % m
