import subprocess
import os

def test_cli_encrypt_decrypt(tmp_path):
    plain = tmp_path / "plain.bin"
    with open(plain, "wb") as f:
        f.write(b"AffineHillCLI")

    key = tmp_path / "key.json"
    from src.keys import generate_random_key
    k = generate_random_key(2, 256)
    k.to_json(key)

    cipher = tmp_path / "cipher.bin"
    recovered = tmp_path / "recovered.bin"

    subprocess.run(["python", "-m", "src.cli", "encrypt", str(plain), str(cipher), str(key)], check=True)
    subprocess.run(["python", "-m", "src.cli", "decrypt", str(cipher), str(recovered), str(key)], check=True)

    with open(plain, "rb") as f1, open(recovered, "rb") as f2:
        assert f1.read() == f2.read()
