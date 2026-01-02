import argparse
import logging
from src import cipher, discover, io_utils, keys

def run():
    parser = argparse.ArgumentParser(
        description="Affine Hill Cryptography CLI"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Encrypt
    enc_parser = subparsers.add_parser("encrypt", help="Encrypt a plaintext file")
    enc_parser.add_argument("plaintext", help="Path to plaintext file")
    enc_parser.add_argument("ciphertext", help="Path to output ciphertext file")
    enc_parser.add_argument("keyfile", help="Path to key JSON file")

    # Decrypt
    dec_parser = subparsers.add_parser("decrypt", help="Decrypt a ciphertext file")
    dec_parser.add_argument("ciphertext", help="Path to ciphertext file")
    dec_parser.add_argument("plaintext", help="Path to output plaintext file")
    dec_parser.add_argument("keyfile", help="Path to key JSON file")

    # Discover
    disc_parser = subparsers.add_parser("discover", help="Attempt key recovery")
    disc_parser.add_argument("plaintext", help="Path to plaintext file")
    disc_parser.add_argument("ciphertext", help="Path to ciphertext file")
    disc_parser.add_argument("--block-size", type=int, required=True, help="Block size used")

    # Verify
    ver_parser = subparsers.add_parser("verify", help="Verify recovered plaintext")
    ver_parser.add_argument("original", help="Path to original plaintext file")
    ver_parser.add_argument("recovered", help="Path to recovered plaintext file")

    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)

    if args.command == "encrypt":
        cipher.encrypt_file(args.plaintext, args.ciphertext, args.keyfile)
    elif args.command == "decrypt":
        cipher.decrypt_file(args.ciphertext, args.plaintext, args.keyfile)
    elif args.command == "discover":
        key, confidence = discover.recover_key(args.plaintext, args.ciphertext, args.block_size)
        print("Recovered key matrix:\n", key.matrix)
        print("Recovered vector:\n", key.vector)
        print(f"Confidence: {confidence:.2f}")
    elif args.command == "verify":
        h1 = io_utils.file_hash(args.original)
        h2 = io_utils.file_hash(args.recovered)
        if h1 == h2:
            print("Verification successful: files match")
        else:
            print("Verification failed: files differ")
