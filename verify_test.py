# def verification(phone_number):
#   try:
#     # generating and sending code via sms
#     client.verify.v2.services(service_sid)\
#     .verifications\
#     .create(to=phone_number, channel='whatsapp')

#     print(f"Verification code sent to {phone_number} via whatsapp")

#     # user input code for verification
#     input_code = input("Enter 2FA code: ")

#     # code verification
#     check = client.verify.v2.services(service_sid)\
#       .verification_checks\
#       .create(to=phone_number, code=input_code)

#     return check.status == 'approved'
#   except Exception as e:
#     print(f"Twilio Error: {e}")
#     return False