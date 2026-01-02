import numpy as np
import os
from src.keys import AffineHillKey, generate_random_key

def test_key_generation_and_inverse():
    key = generate_random_key(3, 256)
    inv = key.inverse_matrix()
    I = (np.dot(key.matrix, inv) % key.modulus)
    assert np.array_equal(I % key.modulus, np.identity(key.block_size, dtype=int))

def test_key_save_and_load(tmp_path):
    key = generate_random_key(2, 256)
    path = tmp_path / "key.json"
    key.to_json(path)
    loaded = AffineHillKey.from_json(path)
    assert key.fingerprint() == loaded.fingerprint()
