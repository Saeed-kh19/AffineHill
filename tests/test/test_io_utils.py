import numpy as np
import os
from src import io_utils

def test_read_write(tmp_path):
    data = np.array([1,2,3,4,255], dtype=np.uint8)
    path = tmp_path / "test.bin"
    io_utils.write_file(path, data)
    read_back = io_utils.read_file(path)
    assert np.array_equal(data, read_back)

def test_split_and_truncate():
    data = np.array([1,2,3,4,5], dtype=np.uint8)
    blocks, length = io_utils.split_blocks(data, 4)
    assert blocks.shape[1] == 4
    recovered = io_utils.truncate_data(blocks.flatten(), length)
    assert np.array_equal(recovered, data)

def test_metadata(tmp_path):
    path = tmp_path / "test.bin"
    with open(path, "wb") as f:
        f.write(b"hello")
    meta = {"hash": io_utils.file_hash(path), "block_size": 4}
    io_utils.save_metadata(str(path), meta)
    loaded = io_utils.load_metadata(str(path))
    assert loaded["hash"] == meta["hash"]
