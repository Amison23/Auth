
from Crypto.Cipher import AES
from secrets import token_bytes

key = token_bytes(16)

def encrypt(msg):
  cipher = AES.new(key, AES.MODE_GCM)
  nonce = cipher.nonce  
  ciphertext, tag = cipher.encrypt_and_digest(msg.encode("ASCII"))
 
  return nonce, ciphertext, tag

def decrypt(ciphertext, nonce, tag):
  cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
  plaintext = cipher.decrypt(ciphertext)

  try:
    cipher.verify(tag)
    return plaintext.decode("ASCII")
  except ValueError:
    return False

nonce, ciphertext, tag = encrypt(input("Enter message: "))
plaintext = decrypt(ciphertext, nonce, tag)
print(f"Cipher text: {ciphertext}")

if not plaintext:
  print("Message is corrupted")
else:
  print(f"Decrypted Plain text: {plaintext}") 


def otp_generate(key):
  otp_key_string = base64.b64encode(key)