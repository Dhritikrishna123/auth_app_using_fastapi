import smtplib
import asyncio
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.config import settings

async def send_email(to_email: str, subject: str, body: str, is_html: bool = False):
    message = MIMEMultipart()
    message["From"] = settings.SMTP_USERNAME
    message["To"] = to_email
    message["Subject"] = subject
    
    if is_html:
        message.attach(MIMEText(body, "html"))
    else:
        message.attach(MIMEText(body, "plain"))
    
    try:
        # Run SMTP operations in a thread pool to avoid blocking the event loop
        return await asyncio.to_thread(_send_email_sync, message)
    except Exception as e:
        print(f"Error sending email: {e}")
        # Consider logging this error properly
        return False

def _send_email_sync(message):
    try:
        # Use context manager for proper cleanup
        with smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT, timeout=10) as server:
            server.starttls()
            server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
            server.send_message(message)
        return True
    except Exception as e:
        # Re-raise to be caught in the calling async function
        raise e

async def send_otp_email(to_email: str, otp: str):
    subject = "Your OTP for Authentication"
    body = f"""
    <html>
    <body>
        <h2>Authentication OTP</h2>
        <p>Your One-Time Password (OTP) for account verification is:</p>
        <h1 style="color: #4CAF50;">{otp}</h1>
        <p>This OTP will expire in {settings.OTP_EXPIRY_MINUTES} minutes.</p>
        <p>If you did not request this OTP, please ignore this email.</p>
    </body>
    </html>
    """
    return await send_email(to_email, subject, body, is_html=True)