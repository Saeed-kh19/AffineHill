import numpy as np
import pytest
from src import math_mod

def test_mod_inverse():
    assert math_mod.mod_inverse(3, 256) == 171  # since 3*171 ≡ 1 mod 256

def test_matrix_inverse_mod():
    K = np.array([[1,2],[3,5]])
    invK = math_mod.matrix_inverse_mod(K, 256)
    I = (np.dot(K, invK) % 256)
    assert np.array_equal(I % 256, np.identity(2, dtype=int))
