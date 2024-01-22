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

def decrypt_data(encrypted_value):
    
    ciphertext=base64.b64decode(encrypted_value)
    original_value = box.decrypt(ciphertext).decode('ascii')

    return(original_value)