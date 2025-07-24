import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.settings import settings

def send_otp_email(to_email: str, otp_code: str):
    subject = "JamAndFlow OTP Verification"
    html = f"""
    <html>
      <body style='font-family: Arial, sans-serif; background: #f9f9f9; padding: 24px;'>
        <div style='max-width: 480px; margin: auto; background: #fff; border-radius: 8px; box-shadow: 0 2px 8px #0001; padding: 32px;'>
          <h2 style='color: #2d89ef; margin-bottom: 8px;'>JamAndFlow Verification Code</h2>
          <p style='font-size: 1.1em; color: #333;'>
            Use the following One-Time Password (OTP) to complete your registration. This code is valid for <b>5 minutes</b>:
          </p>
          <div style='font-size: 2.5em; font-weight: bold; letter-spacing: 6px; color: #2d89ef; margin: 24px 0 16px 0; text-align: center;'>
            {otp_code}
          </div>
          <p style='color: #555; font-size: 1em;'>
            If you did not request this, please ignore this email. For your security, do not share this code with anyone.
          </p>
          <hr style='margin: 32px 0;'>
          <footer style='font-size: 0.95em; color: #888; text-align: center;'>
            &copy; 2025 JamAndFlow. All rights reserved.
          </footer>
        </div>
      </body>
    </html>
    """
    msg = MIMEMultipart()
    msg['From'] = settings.FROM_EMAIL
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(html, 'html'))

    try:
        with smtplib.SMTP(settings.SMTP_SERVER, 587) as server:
            server.starttls()
            server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
            server.sendmail(settings.FROM_EMAIL, to_email, msg.as_string())
            print(f"OTP email sent to {to_email}")
    except Exception as e:
        print(f"Failed to send OTP email: {e}")