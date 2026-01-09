import secrets
import pyotp
import time
import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()
account_sid = os.getenv("ACCOUNT_SID")
account_token = os.getenv("ACCOUNT_TOKEN")
service_sid = os.getenv("SERVICE_SID")

client = Client(account_sid, account_token)


def format_phone_number(raw_input, country_code="+254"):
    # Remove any spaces, dashes, or brackets
    clean = "".join(filter(str.isdigit, raw_input))
    
    # If it starts with '0', remove it (common in Kenya: 0712 -> 712)
    if clean.startswith('0'):
      clean = clean[1:]
        
    # If it's already full length with country code but missing the '+'
    if not clean.startswith(country_code.replace("+", "")):
      clean = f"{country_code.replace('+', '')}{clean}"
      return f"+{clean}"

    clean = f"{country_code}{clean}"
    print(f"Clean number: {clean}")
    # Otherwise, add the country code and '+'
    return f"{clean}"


def send_otp(phone_number):
  channel_success = False
  otp = str(secrets.randbelow(1000000)).zfill(6)
  sms_target = format_phone_number(phone_number)
  whatsapp_target = f"whatsapp:{phone_number}"

  # SMS Trial
  try:
    message = client.messages.create(
      from_ = os.getenv("twilio_number"),
      body = otp,
      to = sms_target
    )
    print(f"Code sent! (SID: {message.sid})")
    channel_success = True

    if message.sid and message.error_code is None:
      print(f"[SMS] Message queued successfully. SID: {message.sid}")
      channel_success = True
    else:
      # Manually trigger the fallback if there's an immediate error code
      raise Exception(f"SMS Error Code: {message.error_code}")
  
  except Exception as e:
    print(f"\n[!] SMS Blocked: {e.msg if hasattr(e, 'msg') else e}")
    print(f"\nTrying Whatsapp!!")

    # Whatsapp Trial
    try:
      print(f"Switched to Whatsapp")
      print(f"Whatsapp number: {whatsapp_target}")
      message = client.messages.create(
        from_ = os.getenv("twilio_whatsapp"),
        body = f"Your secure code is: {otp}",
        to = whatsapp_target
      )
      print(f"Code sent! (SID: {message.sid})")
      channel_success = True
    except Exception as wa_e:
      print(f"Whatsapp failed: {wa_e}")

  if channel_success:
    user_input = input("Enter 2FA code received: ")
    if user_input == otp:
      return True
    else:
      print(f"Invalid code entered")
      return False
  else:
    print("[!] Could not deliver code via any channel.")
    return False 



# Symmetric encryption
def aes_ed(msg, raw_phone):

  # phone_number = "+254731033723"
  phone_number = format_phone_number(raw_phone)

  # generate key and nonce using secrets, more secure that pyotp.randombase32
  key = secrets.token_bytes(32)
  nonce = secrets.token_bytes(12)
  aes = AESGCM(key)
  # encrypt given data and print ciphertext
  ciphertext = nonce + aes.encrypt(nonce, msg.encode(), None)
  print(f"Encrypted ciphertext: {ciphertext.hex()}")

  # cross check phone number and otp sent to decrypt data otherwise fail
  if send_otp(phone_number):
    print("2FA Verified, Decrypting...")
    plaintext = aes.decrypt(ciphertext[:12], ciphertext[12:], None)
    return {
      "key": key.hex(),
      "ciphertext": ciphertext.hex(),
      "plaintext": plaintext.decode()
    }
  else:
    print("2FA failed, Access Denied")
    return None


if __name__ == '__main__':
  msg = input("Input message to encrypt: ")
  number = input("Enter phone number: ")

  result = aes_ed(msg, number)

  # print out results
  if result:
    print("-" * 30)
    print(f"KEY: {result['key']}")
    print(f"CIPHER: {result['ciphertext']}")
    print(f"PLAINTEXT: {result['plaintext']}")
    print("-" * 30)