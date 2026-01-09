import time
import pyotp
import secrets
from cryptography.hazmat.primitives.twofactor.totp import TOTP
from cryptography.hazmat.primitives.hashes import SHA1


# key = secrets.token_bytes(32)
# totp = TOTP(key, 8, SHA1(), 30)
# time_value = time.time()
# totp_value = totp.generate(time_value)
# totp.verify(totp_value, time_value)

key = pyotp.random_base32()
totp = pyotp.TOTP(key)
print(totp.now())
input_code = input("Enter 2FA code: ")

totp.verify(input_code)