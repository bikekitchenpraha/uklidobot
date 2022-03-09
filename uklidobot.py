import ast
from typing import Tuple

from mailer import send_email
from sheets import determine_current_group_and_next, determine_group_members, connect

from decouple import config

SHEET_LINK = "https://docs.google.com/spreadsheets/d/1tbtHGLT0jvMGMOUF7laOwIOX65szHTkAuFSfGQlwM0I/edit#gid=1191004777"

GSHEETS_SERVICE_ACCOUNT = config('GSHEETS_SERVICE_ACCOUNT', cast=ast.literal_eval)
SMTP_PASSWORD = config('SMTP_PASSWORD')
ERROR_EMAIL = config('ERROR_EMAIL')
RECIPIENTS_OVERRIDE = config('RECIPIENTS_OVERRIDE', default=None)


def compose_email(prev_group: Tuple[int, str], next_group: Tuple[int, str]) -> Tuple[str, str]:
    prev_no, prev_name = prev_group
    next_no, next_name = next_group

    subject = "Služba na úklid chodby"
    body = f'<p>Tento týden mají službu: <strong>skupina {next_no} - {next_name}</strong></p>'
    body += f'<p>Minulý týden měli službu: skupina {prev_no} - {prev_name}</p>'
    body += f'<p>Tabulka na služby je <a href="{SHEET_LINK}">zde</a>.</p>'

    return subject, body


def send_error_email(e: Exception, password: str):
    recipients = ERROR_EMAIL
    subject = "Error sending uklidobot email"
    body = str(e)
    send_email(recipients, subject, body, password)


def main():
    try:
        client = connect(GSHEETS_SERVICE_ACCOUNT)

        curr_group, next_group = determine_current_group_and_next(client)

        members = determine_group_members(client, next_group)
    except Exception as ex:
        send_error_email(ex, SMTP_PASSWORD)
        raise ex
    else:
        print('prev. group:', curr_group)
        print('curr. group:', next_group)
        print('curr. group members:', members)

        if RECIPIENTS_OVERRIDE:
            members = [RECIPIENTS_OVERRIDE]

        subject, body = compose_email(curr_group, next_group)
        send_email(members, subject, body, SMTP_PASSWORD)


if __name__ == "__main__":
    main()
