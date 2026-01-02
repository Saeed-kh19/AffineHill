import numpy as np
from src import io_utils, math_mod, keys

def recover_key(plaintext_path, ciphertext_path, block_size, modulus=256):
    """Attempt to recover key matrix K and vector b from plaintext/ciphertext pairs."""
    P = io_utils.read_file(plaintext_path)
    C = io_utils.read_file(ciphertext_path)

    # Split into aligned blocks
    P_blocks, _ = io_utils.split_blocks(P, block_size, pad=False)
    C_blocks, _ = io_utils.split_blocks(C, block_size, pad=False)

    if len(P_blocks) != len(C_blocks):
        raise ValueError("Plaintext and ciphertext block counts do not match")

    # Build linear system: C = K*P + b (mod m)
    equations = []
    results = []
    for p, c in zip(P_blocks, C_blocks):
        # Each block gives n equations
        for i in range(block_size):
            row = list(p) + [1 if j == i else 0 for j in range(block_size)]
            equations.append(row)
            results.append(c[i])

    A = np.array(equations, dtype=int)
    b = np.array(results, dtype=int)

    # Solve system modulo m
    try:
        # Use least squares over integers, then reduce mod m
        x, _, _, _ = np.linalg.lstsq(A, b, rcond=None)
        x = np.round(x).astype(int) % modulus
    except Exception as e:
        raise ValueError(f"Key recovery failed: {e}")

    # Extract matrix and vector
    K = x[:block_size*block_size].reshape(block_size, block_size)
    v = x[block_size*block_size:]
    candidate_key = keys.AffineHillKey(K, v, modulus, block_size)

    # Validate by re-encrypting blocks
    matches = 0
    for p, c in zip(P_blocks, C_blocks):
        test_c = (np.dot(candidate_key.matrix, p) + candidate_key.vector) % modulus
        if np.array_equal(test_c, c):
            matches += 1

    confidence = matches / len(P_blocks)
    return candidate_key, confidence
