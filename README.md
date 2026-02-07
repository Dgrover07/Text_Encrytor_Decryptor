# Text_Encrytor_Decryptor



This is a practice project to get some hands on experience,



A Flask-based web application for encrypting and decrypting text using RSA and Caesar cipher algorithms.

Overview
This application provides a REST API for performing cryptographic operations:

RSA Encryption/Decryption: Asymmetric encryption using PKCS#1 OAEP with SHA-256
Caesar Cipher: Simple substitution cipher with configurable shift values
Features
RSA key generation with custom prime numbers
File upload support for plaintext and ciphertext
Download encrypted/decrypted results
Input validation and error handling
16 MB file size limit
Installation
Prerequisites
Python 3.6+
pip
Dependencies
Required packages:

flask - Web framework
pycryptodome - Cryptographic operations
sympy - Prime number generation
Usage
Starting the Application
The application runs on http://localhost:5000 by default.

API Endpoints
1. Generate RSA Keys
POST /generate_keys

Parameters:

p (int): First prime number
q (int): Second prime number
Response:

2. RSA Encrypt
POST /rsa_encrypt

Parameters:

N (int): Public modulus
e (int): Public exponent
plaintext (string): Text to encrypt
file (optional): Upload file instead of plaintext
Response:

3. RSA Decrypt
POST /rsa_decrypt

Parameters:

N (int): Public modulus
d (int): Private exponent
p (int): First prime
q (int): Second prime
ciphertext (string): Text to decrypt
file (optional): Upload file instead of ciphertext
Response:

4. Caesar Cipher Encrypt
POST /encrypt_caesar

Parameters:

plaintext (string): Text to encrypt
shift (int): Shift value (1-25)
Response:

5. Caesar Cipher Decrypt
POST /decrypt_caesar

Parameters:

ciphertext (string): Text to decrypt
shift (int): Shift value used for encryption
Response:

6. Get Random Prime
GET /random_primes

Response:

7. Download File
GET /download/<filename>

Downloads encrypted/decrypted files.

Known Issues & Fixes Needed
Line 77: Typo in function call

jasonify should be jsonify
Line 54: Method name typo

char.isaplha() should be char.isalpha()
Line 95: Undefined variable

N should be n (lowercase) to match the return value
Missing import

render_template is used but not imported from Flask
Missing configuration

UPLOAD_FOLDER is referenced but not configured
Security Considerations
⚠️ This application is for educational purposes only.

RSA key size should be ≥ 2048 bits for production use (currently 512 bits in examples)
Caesar cipher is cryptographically weak; use only for learning
Avoid debug mode in production
Implement proper file path validation
Add authentication/authorization for production deployment
Store sensitive keys securely (not in code)
Example Workflow
