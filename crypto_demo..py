"""
Applied Cryptography Security Assessment - Demo Lab

This script demonstrates common cryptographic implementation failures:
- Weak JWT secret usage
- Missing token validation checks
- Insecure encoding (ROT13)
- Demonstration of IV reuse concept (simulated, not real encryption attack)

NOTE: This is for educational and portfolio demonstration only.
"""

import base64
import hashlib
import hmac
import json
import time


# -----------------------------
# 1. WEAK JWT IMPLEMENTATION
# -----------------------------

SECRET = "12345"  # weak secret (intentionally insecure)


def create_jwt(payload):
    header = {"alg": "HS256", "typ": "JWT"}

    def encode(data):
        return base64.urlsafe_b64encode(
            json.dumps(data).encode()
        ).decode().rstrip("=")

    header_enc = encode(header)
    payload_enc = encode(payload)

    signature_data = f"{header_enc}.{payload_enc}".encode()
    signature = hmac.new(
        SECRET.encode(),
        signature_data,
        hashlib.sha256
    ).hexdigest()

    return f"{header_enc}.{payload_enc}.{signature}"


def verify_jwt(token):
    try:
        header_b64, payload_b64, signature = token.split(".")

        expected_sig = hmac.new(
            SECRET.encode(),
            f"{header_b64}.{payload_b64}".encode(),
            hashlib.sha256
        ).hexdigest()

        # Missing proper validation checks (intentional weakness demo)
        if signature != expected_sig:
            return False

        payload = json.loads(
            base64.urlsafe_b64decode(payload_b64 + "==")
        )

        # NO exp validation (intentionally missing)
        return payload

    except Exception:
        return False


# -----------------------------
# 2. INSECURE ENCODING (ROT13)
# -----------------------------

def rot13(text):
    result = []
    for char in text:
        if 'a' <= char <= 'z':
            result.append(chr((ord(char) - 97 + 13) % 26 + 97))
        elif 'A' <= char <= 'Z':
            result.append(chr((ord(char) - 65 + 13) % 26 + 65))
        else:
            result.append(char)
    return "".join(result)


# -----------------------------
# 3. IV REUSE SIMULATION
# -----------------------------

def simulate_iv_reuse():
    """
    This does NOT perform real encryption.
    It demonstrates the concept of IV reuse risk.
    """

    iv = "STATIC_IV_1234"  # reused IV (bad practice)

    messages = ["user=admin", "user=guest"]

    encrypted = []

    for msg in messages:
        # fake "encryption"
        ciphertext = hashlib.sha256((iv + msg).encode()).hexdigest()
        encrypted.append(ciphertext)

    return encrypted


# -----------------------------
# DEMO EXECUTION
# -----------------------------

if __name__ == "__main__":
    print("\n=== WEAK JWT DEMO ===")

    token = create_jwt({
        "user": "victim",
        "role": "admin",
        "iat": int(time.time())
        # missing exp intentionally
    })

    print("Generated Token:", token)

    print("\nVerifying Token...")
    print("Result:", verify_jwt(token))

    print("\n=== ROT13 INSECURE ENCODING ===")
    print("Original: security")
    print("Encoded :", rot13("security"))

    print("\n=== IV REUSE SIMULATION ===")
    print(simulate_iv_reuse())

    print("\nNOTE: These are intentional insecure implementations for learning.")