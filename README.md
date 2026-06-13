# Applied Cryptography Security Assessment

## Overview
This project demonstrates cryptographic implementation failures in a simulated environment.

## Key Issues
- Weak JWT secret usage
- Missing token validation (exp, aud)
- Insecure encoding (ROT13)
- IV reuse concept issues
- Weak cryptographic design patterns

## How to Run
```bash
cd crypto-lab
python crypto_demo.py