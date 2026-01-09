#  Ceasar Cipher app
FIRST_CHAR_RANGE = ord("A")
LAST_CHAR_CODE = ord("Z")
CHAR_RANGE = LAST_CHAR_CODE - FIRST_CHAR_RANGE + 1

def ceasar_shift(message, shift):
  result = ""

  # Looping through message
  for char in message.upper():
    if char.isalpha():  
      # convert message to ASCII
      char_code = ord(char)
      new_char_code = char_code + shift

      if new_char_code > LAST_CHAR_CODE:
        new_char_code -= CHAR_RANGE

      if new_char_code < FIRST_CHAR_RANGE:
        new_char_code += CHAR_RANGE
      
      new_char = chr(new_char_code)
      result += new_char
    else:
      result += char

  print(result)

user_message = input("Message to encrypt: ")
shift_key = int(input("Shift key (int): "))

ceasar_shift(user_message, shift_key)