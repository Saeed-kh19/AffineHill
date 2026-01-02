import numpy as np
from src.keys import generate_random_key
from src.cipher import encrypt_file
from src.discover import recover_key
from src.io_utils import read_file

def test_recover_key(tmp_path):
    # Create sample plaintext file
    plaintext_path = tmp_path / "plain.bin"
    with open(plaintext_path, "wb") as f:
        f.write(b"AffineHillKeyDiscoveryTest")

    # Generate key and save
    key = generate_random_key(2, 256)
    keyfile_path = tmp_path / "key.json"
    key.to_json(keyfile_path)

    # Encrypt
    ciphertext_path = tmp_path / "cipher.bin"
    encrypt_file(plaintext_path, ciphertext_path, keyfile_path)

    # Attempt recovery
    recovered_key, confidence = recover_key(plaintext_path, ciphertext_path, 2, 256)

    assert confidence > 0.9  # should match most blocks
    assert np.array_equal(recovered_key.matrix % 256, key.matrix % 256)
    assert np.array_equal(recovered_key.vector % 256, key.vector % 256)
