import numpy as np
import json
import hashlib
from dataclasses import dataclass
from src import math_mod

@dataclass
class AffineHillKey:
    matrix: np.ndarray
    vector: np.ndarray
    modulus: int = 256
    block_size: int = None

    def __post_init__(self):
        if self.block_size is None:
            self.block_size = self.matrix.shape[0]
        if self.matrix.shape[0] != self.matrix.shape[1]:
            raise ValueError("Key matrix must be square")
        if self.matrix.shape[0] != len(self.vector):
            raise ValueError("Vector length must match matrix dimension")
        # Check invertibility
        det = math_mod.det_mod(self.matrix, self.modulus)
        if math_mod.gcd(det, self.modulus) != 1:
            raise ValueError("Matrix is not invertible modulo modulus")

    def inverse_matrix(self):
        """Return inverse of matrix modulo m."""
        return math_mod.matrix_inverse_mod(self.matrix, self.modulus)

    def fingerprint(self):
        """SHA-256 fingerprint of matrix+vector for integrity."""
        data = self.matrix.tobytes() + self.vector.tobytes()
        return hashlib.sha256(data).hexdigest()

    def to_json(self, path):
        """Save key to JSON file."""
        key_dict = {
            "matrix": self.matrix.tolist(),
            "vector": self.vector.tolist(),
            "modulus": self.modulus,
            "block_size": self.block_size,
            "fingerprint": self.fingerprint()
        }
        with open(path, "w") as f:
            json.dump(key_dict, f, indent=4)

    @staticmethod
    def from_json(path):
        """Load key from JSON file."""
        with open(path, "r") as f:
            key_dict = json.load(f)
        matrix = np.array(key_dict["matrix"], dtype=int)
        vector = np.array(key_dict["vector"], dtype=int)
        return AffineHillKey(matrix, vector, key_dict["modulus"], key_dict["block_size"])

def generate_random_key(n=4, m=256):
    """Generate a random valid key."""
    while True:
        matrix = np.random.randint(0, m, size=(n, n))
        vector = np.random.randint(0, m, size=n)
        try:
            return AffineHillKey(matrix, vector, m, n)
        except ValueError:
            continue  # retry until invertible
