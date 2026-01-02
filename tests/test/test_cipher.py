import numpy as np
from src.keys import generate_random_key
from src.cipher import encrypt_block, decrypt_block

def test_block_roundtrip():
    key = generate_random_key(3, 256)
    block = np.array([10, 20, 30], dtype=np.uint8)
    encrypted = encrypt_block(block, key)
    decrypted = decrypt_block(encrypted, key)
    assert np.array_equal(block % 256, decrypted % 256)
