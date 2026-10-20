import smtplib
from email.mime.text import MIMEText
from fastapi import BackgroundTasks, FastAPI, status
from pydantic import BaseModel, EmailStr

def send_email_background(recipient: str, subject: str, body: str):
    # Setup your SMTP settings (e.g., Mailtrap, SendGrid, Gmail SMTP)
    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587
    SENDER_EMAIL = "rishukumargupta.offical@gmail.com"
    SENDER_PASSWORD = "gwxzcsftzqbxbloz"

    # Create the message
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = recipient

    # Connect and send
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, [recipient], msg.as_string())
    except Exception as e:
        print(f"Failed to send email to {recipient}: {e}")