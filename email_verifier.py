import smtplib
import time
import random
from email.mime.text import MIMEText
from itsdangerous import URLSafeTimedSerializer

#  Centralized Config (Step 2)
from config import EMAIL_ADDRESS, EMAIL_PASSWORD, SECRET_KEY, BASE_URL

#  Safety check
if not EMAIL_ADDRESS or not EMAIL_PASSWORD or not SECRET_KEY or not BASE_URL:
    raise ValueError("EMAIL_ADDRESS, EMAIL_PASSWORD, SECRET_KEY, or BASE_URL not set properly in config.py")

# Token serializer for email link
serializer = URLSafeTimedSerializer(SECRET_KEY)
otp_storage = {}  # email → (otp, timestamp)

# ----------------------
#  Token-Based Email Verification
# ----------------------
def generate_token(email):
    return serializer.dumps(email, salt="email-confirm")

def confirm_token(token, expiration=3600):
    try:
        return serializer.loads(token, salt="email-confirm", max_age=expiration)
    except Exception:
        return None

def send_verification_email(email):
    token = generate_token(email)
    link = f"{BASE_URL}/?verify={token}"

    subject = "Verify Your Email - Resume Analyzer"
    body = f"""Hello,

Please click the link below to verify your email address:

{link}

If you did not sign up, you can safely ignore this email.

Regards,
Resume Analyzer Team
"""

    _send_email(email, subject, body)

# ----------------------
# OTP-Based Verification
# ----------------------
def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp_email(email):
    otp = generate_otp()
    otp_storage[email] = (otp, time.time())

    subject = "Your Resume Analyzer OTP"
    body = f"""Hello,

Your one-time password (OTP) is: {otp}

This OTP will expire in 10 minutes.

If you did not request this, please ignore this email.

Regards,
Resume Analyzer Team
"""

    print(f"[DEBUG] OTP for {email} is: {otp}")  # 🔧 Remove in production
    _send_email(email, subject, body)

def verify_otp(email, entered_otp, expiry=600):
    if email not in otp_storage:
        return False
    otp, timestamp = otp_storage[email]
    if time.time() - timestamp > expiry:
        del otp_storage[email]
        return False
    if entered_otp == otp:
        del otp_storage[email]
        return True
    return False

# ----------------------
# Resend Handler
# ----------------------
def resend_verification_email(email, method="link"):
    if method == "otp":
        send_otp_email(email)
    else:
        send_verification_email(email)

# ----------------------
# Internal Mail Sender
# ----------------------
def _send_email(to_email, subject, body):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = to_email

    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, [to_email], msg.as_string())
        server.quit()
        print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email to {to_email}.")
        print("Error:", e)
        print("Ensure your Gmail App Password is correct and 2FA is enabled.")
