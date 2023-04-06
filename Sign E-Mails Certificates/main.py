import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from smail import sign_message  # pip install python-smail

# Secure/Multipurpose Internet Mail Extensions

LOGIN_MAIL, LOGIN_PASS = open("LOGIN_INFO", "r").read().split("\n")  # provide your login info in a file
SMTP_SERVER = "your.smtp.server"  # enter SMTP server here
SMTP_PORT = 587

CERT_FILE = "certs/certificate.pem"  # create the file certificate and private key as shown in the video
KEY_FILE = "certs/private_key.pem"

recipient = "enter@recipient.here"  # choose recipient

message = """Hello,

This is my mail for you!

It will be signed!"""

msg = MIMEMultipart("related")
msg.attach(MIMEText(message, "plain", _charset="UTF-8"))
msg['Subject'] = 'Hello Friend'
msg['From'] = LOGIN_MAIL
msg['To'] = recipient

signed_msg = sign_message(msg, KEY_FILE, CERT_FILE)

with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(LOGIN_MAIL, LOGIN_PASS)
    server.send_message(signed_msg)

print('Email sent successfully!')
