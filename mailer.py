import smtplib
import ssl
from email.message import Message
from typing import List
from email.mime.text import MIMEText

FROM = "bikekitchenpraha@gmail.com"


def send_email(recipients: List[str], subject: str, msg_body: str, password: str):
    msg = MIMEText(msg_body)

    msg['Subject'] = subject

    _send_email(msg, recipients, password)


def _send_email(message: Message, recipients: List[str], password: str):
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port=465, context=context) as server:
        server.login("bikekitchenpraha@gmail.com", password)
        server.send_message(message, FROM, recipients)
        server.quit()
