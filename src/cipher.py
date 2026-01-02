import numpy as np
import logging
from src import io_utils, keys
from src import io_utils, keys
from src import math_mod, io_utils, keys

def encrypt_block(block, key: keys.AffineHillKey):
    """Encrypt a single block using Affine Hill cipher."""
    if len(block) != key.block_size:
        raise ValueError("Block size does not match key dimension")
    return (np.dot(key.matrix, block) + key.vector) % key.modulus

def decrypt_block(block, key: keys.AffineHillKey):
    """Decrypt a single block using Affine Hill cipher."""
    if len(block) != key.block_size:
        raise ValueError("Block size does not match key dimension")
    inv_matrix = key.inverse_matrix()
    return np.dot(inv_matrix, (block - key.vector)) % key.modulus

def encrypt_file(input_path, output_path, key: keys.AffineHillKey):
    """Encrypt entire file."""
    data = io_utils.read_file(input_path)
    blocks, original_length = io_utils.split_blocks(data, key.block_size)
    encrypted_blocks = [encrypt_block(block, key) for block in blocks]
    encrypted_data = np.array(encrypted_blocks, dtype=np.uint8).flatten()
    io_utils.write_file(output_path, encrypted_data)
    # Save metadata
    metadata = {
        "original_length": original_length,
        "block_size": key.block_size,
        "modulus": key.modulus,
        "key_fingerprint": key.fingerprint(),
        "input_hash": io_utils.file_hash(input_path)
    }
    io_utils.save_metadata(output_path, metadata)

def decrypt_file(input_path, output_path, key: keys.AffineHillKey):
    """Decrypt entire file."""
    data = io_utils.read_file(input_path)
    blocks, _ = io_utils.split_blocks(data, key.block_size, pad=False)
    decrypted_blocks = [decrypt_block(block, key) for block in blocks]
    decrypted_data = np.array(decrypted_blocks, dtype=np.uint8).flatten()
    # Load metadata to truncate correctly
    metadata = io_utils.load_metadata(input_path)
    truncated = io_utils.truncate_data(decrypted_data, metadata["original_length"])
    io_utils.write_file(output_path, truncated)
    
    


logger = logging.getLogger(__name__)

def encrypt_file(input_path, output_path, keyfile_path):
    """Encrypt a plaintext file into ciphertext using Affine Hill cipher."""
    # Load key
    key = keys.AffineHillKey.from_json(keyfile_path)
    logger.info(f"Loaded key with fingerprint {key.fingerprint()}")

    # Read plaintext
    data = io_utils.read_file(input_path)
    logger.info(f"Read {len(data)} bytes from {input_path}")

    # Split into blocks
    blocks, original_length = io_utils.split_blocks(data, key.block_size)
    logger.info(f"Split into {len(blocks)} blocks of size {key.block_size}")

    # Encrypt each block
    encrypted_blocks = [encrypt_block(block, key) for block in blocks]
    encrypted_data = np.array(encrypted_blocks, dtype=np.uint8).flatten()

    # Write ciphertext
    io_utils.write_file(output_path, encrypted_data)
    logger.info(f"Ciphertext written to {output_path}")

    # Save metadata
    metadata = {
        "original_length": original_length,
        "block_size": key.block_size,
        "modulus": key.modulus,
        "key_fingerprint": key.fingerprint(),
        "input_hash": io_utils.file_hash(input_path)
    }
    io_utils.save_metadata(output_path, metadata)
    logger.info(f"Metadata saved to {output_path}.meta.json")

    return output_path





logger = logging.getLogger(__name__)

def decrypt_file(input_path, output_path, keyfile_path):
    """Decrypt a ciphertext file back into plaintext using Affine Hill cipher."""
    # Load key
    key = keys.AffineHillKey.from_json(keyfile_path)
    logger.info(f"Loaded key with fingerprint {key.fingerprint()}")

    # Read ciphertext
    data = io_utils.read_file(input_path)
    logger.info(f"Read {len(data)} bytes from {input_path}")

    # Split into blocks (no padding added here)
    blocks, _ = io_utils.split_blocks(data, key.block_size, pad=False)
    logger.info(f"Split into {len(blocks)} blocks of size {key.block_size}")

    # Decrypt each block
    decrypted_blocks = [decrypt_block(block, key) for block in blocks]
    decrypted_data = np.array(decrypted_blocks, dtype=np.uint8).flatten()

    # Load metadata to truncate correctly
    metadata = io_utils.load_metadata(input_path)
    truncated = io_utils.truncate_data(decrypted_data, metadata["original_length"])

    # Write recovered plaintext
    io_utils.write_file(output_path, truncated)
    logger.info(f"Recovered plaintext written to {output_path}")

    return output_path
