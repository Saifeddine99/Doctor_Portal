# This function will be used to encrypt data before saving it to database.
#We'll be using AES encryption algorithm with a 265-bit encryption key
import os
import base64
import binascii
from dotenv import load_dotenv
from nacl.secret import SecretBox

# Load environment variables from .env file
load_dotenv()
# Retrieve the encryption key from the environment variable
hex_key = os.environ.get('KEY')
# Convert hexadecimal string to bytes
key = binascii.unhexlify(hex_key)
box = SecretBox(key)
hex_nonce = os.environ.get('NONCE')
nonce= binascii.unhexlify(hex_nonce)

def encrypt_data(value):

    ciphertext = box.encrypt(value.encode('ascii'), nonce)
    encrypted_value_str=base64.b64encode(ciphertext).decode('utf-8')
    
    return(encrypted_value_str)