from email.message import EmailMessage
import smtplib
from pydantic import EmailStr
from app.core.config import settings

def sendMail(email: EmailStr,token: str):

    # if we get credential
    # cache its credential
    '''
    credential(uuid,email,password)
    '''
    sender_email = settings.sender_email
    receiver_email = email
    password = settings.email_password
    msg = EmailMessage()

    msg["Subject"] = "01. Bilali.Space Verification Email"
    msg["From"] = sender_email
    msg["To"] = receiver_email

    msg.set_content("Email Verification")
    msg.add_alternative(
        f"""
        <html>
        <head>
        </head>
        <body>
            <h5>Welcome to Bilali.Space</h2>
            <p>Hey {email}</p>
            <pre>
                Thanks for registering to our learning platform 
                Before we get started We will need you to verify your email
            </pre>
            <a href="http://127.0.0.1:8000/api/v1/auth/verify_email/{token}" target="_blank">Verify Email</a>
        </body>
        </html>
        """,subtype="html"
    )

    try:
        with smtplib.SMTP("smtp.gmail.com",587) as server:
            server.starttls()
            server.login(sender_email,password)
            server.send_message(msg)
    except:
        return False

    return True
