import numpy as np
import numpy as np
import os
from src.keys import generate_random_key
from src.cipher import encrypt_file, decrypt_file
from src.io_utils import read_file

from src.keys import generate_random_key
from src.cipher import encrypt_block, decrypt_block

def test_block_roundtrip():
    key = generate_random_key(3, 256)
    block = np.array([10, 20, 30], dtype=np.uint8)
    encrypted = encrypt_block(block, key)
    decrypted = decrypt_block(encrypted, key)
    assert np.array_equal(block % 256, decrypted % 256)



def test_file_roundtrip(tmp_path):
    # Create sample plaintext file
    plaintext_path = tmp_path / "plain.bin"
    with open(plaintext_path, "wb") as f:
        f.write(b"HelloAffineHill")

    # Generate key and save
    key = generate_random_key(3, 256)
    keyfile_path = tmp_path / "key.json"
    key.to_json(keyfile_path)

    # Encrypt
    ciphertext_path = tmp_path / "cipher.bin"
    encrypt_file(plaintext_path, ciphertext_path, keyfile_path)

    # Decrypt
    recovered_path = tmp_path / "recovered.bin"
    decrypt_file(ciphertext_path, recovered_path, keyfile_path)

    # Verify recovery
    original = read_file(plaintext_path)
    recovered = read_file(recovered_path)
    assert np.array_equal(original, recovered)


def test_encrypt_decrypt_roundtrip(tmp_path):
    # Create sample plaintext file
    plaintext_path = tmp_path / "plain.bin"
    with open(plaintext_path, "wb") as f:
        f.write(b"AffineHillTest")

    # Generate key and save
    key = generate_random_key(3, 256)
    keyfile_path = tmp_path / "key.json"
    key.to_json(keyfile_path)

    # Encrypt
    ciphertext_path = tmp_path / "cipher.bin"
    encrypt_file(plaintext_path, ciphertext_path, keyfile_path)

    # Decrypt
    recovered_path = tmp_path / "recovered.bin"
    decrypt_file(ciphertext_path, recovered_path, keyfile_path)

    # Verify recovery
    original = read_file(plaintext_path)
    recovered = read_file(recovered_path)
    assert np.array_equal(original, recovered)
