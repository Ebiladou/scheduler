from twilio.rest import Client
import os

def send_whatsapp_message(phone: str, message: str):
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    client = Client(account_sid, auth_token)
    
    client.messages.create(
        body=message,
        from_="whatsapp:+16315156379",  
        to=f"whatsapp:{phone}"
    )