from twilio.rest import Client
from dotenv import load_dotenv
import os

load_dotenv()

account_sid = os.getenv("ACCOUNT_SID")
account_token = os.getenv("ACCOUNT_TOKEN")

client = Client(account_sid, account_token)
message = client.messages.create(
  from_= os.getenv("twilio_number"),
  body="Testing Twilio",
  to = os.getenv("target_number")
)
print(f"Message Sent! SID: {message.sid}")
print("testing")