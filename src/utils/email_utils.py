import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

load_dotenv()

smtp_server = os.getenv("MAIL_SERVER")
port = os.getenv("MAIL_PORT")

def send_email(to_email: str, subject: str, body: str):
    sender_email = os.getenv("MAIL_ID")
    password = os.getenv("MAIL_PASSWORD")
    
    if not sender_email or not password or not smtp_server:
        print("Email configuration is missing. Please check the .env file.")
        return

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = to_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))
    
    try:
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls()  
            server.login(sender_email, password) 
            server.sendmail(sender_email, to_email, message.as_string()) 
        print(f"Email sent successfully to {to_email}")
    except Exception as e:
        print(f"Failed to send email to {to_email}. Error: {e}")
        

def send_password_reset_email(to_email: str, subject: str, body: str):
    send_email(to_email, subject, body)