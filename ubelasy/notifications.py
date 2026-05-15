# ubelasy/notifications.py
import smtplib
from email.message import EmailMessage
import streamlit as st
import requests  # untuk WA jika menggunakan API

def send_email(recipient, subject, body):
    """Kirim email menggunakan SMTP (contoh: Gmail)"""
    smtp_server = st.secrets.get("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = st.secrets.get("SMTP_PORT", 587)
    sender_email = st.secrets.get("EMAIL_SENDER")
    sender_password = st.secrets.get("EMAIL_PASSWORD")
    
    if not sender_email:
        print("Email sender not configured")
        return
    
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = recipient
    msg.set_content(body)
    
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
        print(f"Email sent to {recipient}")
    except Exception as e:
        print(f"Email failed: {e}")

def send_whatsapp(phone_number, message):
    """Contoh menggunakan Twilio atau API lainnya"""
    # Untuk demo, kita hanya print. Implementasi nyata butuh akun Twilio atau WA Business API.
    # Misal menggunakan Twilio:
    # from twilio.rest import Client
    # account_sid = st.secrets["TWILIO_SID"]
    # auth_token = st.secrets["TWILIO_TOKEN"]
    # client = Client(account_sid, auth_token)
    # client.messages.create(body=message, from_='whatsapp:+14155238886', to=f'whatsapp:{phone_number}')
    print(f"WA to {phone_number}: {message}")
