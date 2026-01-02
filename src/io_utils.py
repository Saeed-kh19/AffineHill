import numpy as np
import hashlib
import json
import os

def read_file(path):
    """Read binary file into numpy array of bytes."""
    with open(path, "rb") as f:
        data = f.read()
    return np.frombuffer(data, dtype=np.uint8)

def write_file(path, data):
    """Write numpy array of bytes back to file."""
    with open(path, "wb") as f:
        f.write(bytearray(data.tolist()))

def split_blocks(data, block_size, pad=True):
    """Split data into blocks of size n, pad with zeros if needed."""
    length = len(data)
    remainder = length % block_size
    if pad and remainder != 0:
        padding = block_size - remainder
        data = np.concatenate([data, np.zeros(padding, dtype=np.uint8)])
    blocks = data.reshape(-1, block_size)
    return blocks, length  # return original length for metadata

def truncate_data(data, original_length):
    """Truncate padded data back to original length."""
    return data[:original_length]

def file_hash(path):
    """Compute SHA-256 hash of file contents."""
    sha = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha.update(chunk)
    return sha.hexdigest()

def save_metadata(path, metadata):
    """Save metadata JSON next to output file."""
    meta_path = path + ".meta.json"
    with open(meta_path, "w") as f:
        json.dump(metadata, f, indent=4)

def load_metadata(path):
    """Load metadata JSON."""
    meta_path = path + ".meta.json"
    if not os.path.exists(meta_path):
        raise FileNotFoundError("Metadata file not found")
    with open(meta_path, "r") as f:
        return json.load(f)
