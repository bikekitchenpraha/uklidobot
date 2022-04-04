import ast
from typing import Tuple

from mailer import send_email
from model import Group
from sheets import determine_prev_curr_next_groups, determine_group_members, connect

from decouple import config

SHEET_LINK = "https://docs.google.com/spreadsheets/d/1tbtHGLT0jvMGMOUF7laOwIOX65szHTkAuFSfGQlwM0I/edit#gid=1191004777"

GSHEETS_SERVICE_ACCOUNT = config('GSHEETS_SERVICE_ACCOUNT', cast=ast.literal_eval)
SMTP_PASSWORD = config('SMTP_PASSWORD')
ERROR_EMAIL = config('ERROR_EMAIL')
RECIPIENTS_OVERRIDE = config('RECIPIENTS_OVERRIDE', default=None)


def compose_email(prev_group: Group, current_group: Group, next_group: Group) -> Tuple[str, str]:
    prev_no, prev_name = prev_group
    curr_no, curr_name = current_group
    next_no, next_name = next_group

    subject = "Služba na úklid chodby"
    body = f'<p>Tento týden mají službu: <strong>skupina {curr_no} - {curr_name}</strong></p>'
    body += f'<p>Minulý týden měli službu: skupina {prev_no} - {prev_name}</p>'
    body += f'<p>Příští týden budou mít službu: skupina {next_no} - {next_name}</p>'
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

        prev_group, curr_group, next_group = determine_prev_curr_next_groups(client)
        members = determine_group_members(client, curr_group)
    except Exception as ex:
        send_error_email(ex, SMTP_PASSWORD)
        raise ex
    else:
        print('prev. group:', prev_group)
        print('curr. group:', curr_group)
        print('next group:', next_group)
        print('curr. group members:', members)

        recipients = [email for _, email in members]

        if RECIPIENTS_OVERRIDE:
            recipients = [RECIPIENTS_OVERRIDE]

        subject, body = compose_email(prev_group, curr_group, next_group)
        send_email(recipients, subject, body, SMTP_PASSWORD)


if __name__ == "__main__":
    main()
