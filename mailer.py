import smtplib
import ssl
from email.message import Message
from typing import List
from email.mime.text import MIMEText

EMAIL_ACC = "bikekitchenpraha@riseup.net"


def send_email(recipients: List[str], subject: str, msg_body: str, password: str):
    msg = MIMEText(msg_body)

    msg['Subject'] = subject
    msg['From'] = EMAIL_ACC
    msg['To'] = ','.join(recipients)

    _send_email(msg, password)


def _send_email(message: Message, password: str):
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("mail.riseup.net", port=465, context=context) as server:
        server.login(EMAIL_ACC, password)
        server.send_message(message)
        server.quit()
