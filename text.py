from flask import Flask,  request, jsonify,send_file
import os 
from math import gcd
from crypto.cipher import PKCS1_OAEP
from crypto.PublicKey import RSA
from crypto.hash import SHA256
from crypto import Random
import base64
import random
from sympy import randprime 

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB limit

aplhabet_e = {'a': '01', 'b': '02', 'c': '03', 'd': '04', 'e': '05', 'f': '06', 'g': '07', 'h': '08',
              'i': '09', 'j': '10', 'k': '11', 'l': '12', 'm': '13', 'n': '14', 'o': '15', 'p': '16',
              'q': '17', 'r': '18', 's': '19', 't': '20', 'u': '21', 'v': '22', 'w': '23', 'x': '24',
              'y': '25', 'z': '26', 'A': '27', 'B': '28', 'C': '29', 'D': '30', 'E': '31', 'F': '32',
              'G': '33', 'H': '34', 'I': '35', 'J': '36', 'K': '37', 'L': '38', 'M': '39', 'N': '40',
              'O': '41', 'P': '42', 'Q': '43', 'R': '44', 'S': '45', 'T': '46', 'U': '47', 'V': '48',
              'W': '49', 'X': '50', 'Y': '51', 'Z': '52', ' ': '53', '.': '54', ',': '55', '?': '56',
              '!': '57', '@': '58', '#': '59', '$': '60', '%': '61', '^': '62', '&': '63', '*': '64',
              '(': '65', ')': '66', '-': '67', '_': '68', '=': '69', '+': '70', '[': '71', ']': '72',
              '{': '73', '}': '74', '|': '75', '\\': '76', ':': '77', ';': '78', '"': '79', '\'': '80',
              '<': '81', '>': '82', '/': '83', '~': '85', '`': '86', '\n': '87'}
alphabet_d = {v: k for k, v in aplhabet_e.items()}

#RSA key generation
def generate_large_prime(bits=512):
    """generate a large prime number of specified bit length"""
    return RSA.generate(bits, Random.new().read).p

def generate_keys(p, q):
    """Generate RSA keys with proper security"""
    # Validate inputs
    if not isinstance(p, int) or not isinstance(q, int) or p <= 0 or q <= 0:
        raise ValueError("p and q must be positive integers")

    n = p * q 
    phi = (p - 1 ) * (q - 1)

    e = 65537  # common choice for e

    # to ensure e and phi(n) are coprime
    if gcd(e, phi) != 1:
        raise ValueError("e and phi(n) are not coprime. Try different primes.")

    # module inverse of d
    d = pow(e, -1, phi)

    # necessary components for our operations   
    return (n, e, d, p, q)

def rsa_encrypt(plaintext, public_key):
    e, n = public_key 
    key = RSA.construct((n, e))
    cipher = PKCS1_OAEP.new(key, hashAlgo=SHA256)
    encrypted = cipher.encrypt(plaintext.encode('utf-8'))
    return base64.b64encode(encrypted).decode('utf-8')

def rsa_decrypt(ciphertext, private_key):

    d, n, p, q = private_key
    key = RSA.construct((n, 65537, d, p, q))
    cipher = PKCS1_OAEP.new(key, hashAlgo=SHA256)
    encrypted = base64.b64decode(ciphertext)
    return cipher.decrypt(encrypted).decode('utf-8')

#     leaving ceasar cipher unction unchanged
def caesar_encrypt(plaintext, shift):
    encrypted = "" 
    for char in plaintext:
        if char.isaplha():
            base = ord('A') if char.isupper() else ord('a')
            shifted = chr((ord(char) - base + shift ) % 26 + base)
            encrypted += shifted
        else:
            encrypted += char
    return encrypted

def caesar_decrypt(ciphertext, shift):
    return caesar_encrypt(ciphertext, -shift)

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/generate_keys', methods=['POST'])
def generate_key_route():
    p =  int(request.form['p'])
    q =  int(request.form['q'])
    try:
        n, e, d, p, q = generate_keys(p, q)
        return jsonify({
            'success': True,
            'N': N,
            'e': e,
            'd': d,


        })
    
    except ValueError as ve: 
        return jasonify({'success': False, 'error': f"Invalid input: {str(ve)}.Make sure p and q are valid positive integers."})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
    
@app.route('/rsa_encrypt', methods=['POST'])
def rsa_encrypt_route():
    try:
        N = int(request.form['N'])
        e = int(request.form['e'])
        plaintext = request.form['plaintext']
        
        if 'file' in request.files:
            file = request.files['file']
            if file.filename != '':
                plaintext = file.read().decode('utf-8')
        encrypted_text = rsa_encrypt(plaintext, (e, N))

        with open('rsa_encrypted.txt', 'w') as f:
            f.write(encrypted_text)

        return jsonify({
                'success': True,
                'encrypted_text': encrypted_text,
                'download_link': '/download/rsa_encrypted.txt'

            })
    except Exception as ex:
        return jsonify({'success': False, 'error': str(ex)})

@app.route('/rsa_decrypt', methods=['POST'])
def rsa_decrypt_route():
    try:
        N = int(request.form['N'])
        d = int(request.form['d'])
        p = int(request.form['p'])
        q = int(request.form['q'])
        ciphertext = request.form['ciphertext']

        if 'file' in request.files:
            file = request.files['file']
            if file.filename != '':
                ciphertext = file.read().decode('utf-8')
        
        if p == 0 or q == 0:
            return jsonify({'success': False, 'error': "p and q must be non-zero integers for decryption."})
        decrypted_text = rsa_decrypt(ciphertext, (d, N, p, q))
        with open('rsa_decrypted.txt', 'w') as f:
            f.write(decrypted_text)
        return jsonify({
            'success': True,
            'decrypted_text': decrypted_text,
            'download_link': '/download/rsa_decrypted.txt'
        })
    
    except Exception as ex:
        return jsonify({'success': False, 'error': str(ex)})
    
@app.route('/encrypt_caesar', methods=['POST'])
def caesar_encrypt_route():
    try:
        shift = int(request.form['shift'])
        plaintext = request.form['plaintext']
        
        encrypted_text = caesar_encrypt(plaintext, shift)
        with open('caesar_encrypted.txt', 'w') as f:
            f.write(encrypted_text)
        
        return jsonify({
            'success': True,
            'encrypted_text': encrypted_text,
            'download_link': '/download/caesar_encrypted.txt'
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
    
@app.route('/decrypt_caesar', methods=['POST'])   
def caesar_decrypt_route():
    try:
        shift = int(request.form['shift'])
        ciphertext = request.form['ciphertext']
        
        decrypted_text = caesar_decrypt(ciphertext, shift)
        with open('caesar_decrypted.txt', 'w') as f:
            f.write(decrypted_text) 
        return jsonify({
            'success': True,
            'decrypted_text': decrypted_text,
            'download_link': '/download/caesar_decrypted.txt'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
    
    @app.route('/random_primes')
    def random_primes_route():
        prime = randprime(100, 1000)
        return jsonify({'prime': prime})
    
@app.route('/download/<filename>')
def download_file(filename):
    
    #prevent directory traversal attacks
    safe_filename = os.path.basename(filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], safe_filename)
    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=True)
    else:
        return "File not found", 404
    
if __name__ == '__main__':
    app.run(debug=True)
