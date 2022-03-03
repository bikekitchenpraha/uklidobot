from typing import Tuple

from mailer import send_email
from sheets import determine_current_group_and_next, determine_group_members, connect


def compose_email(prev_group: Tuple[int, str], next_group: Tuple[int, str]) -> Tuple[str, str]:
    prev_no, prev_name = prev_group
    next_no, next_name = next_group

    subject = "Bike Kitchen Praha: služby na úklid chodby"
    body = f"Tento týden mají službu: skupina {next_no} - {next_name}\n\n"
    body += f"Minulý týden měli službu: skupina {prev_no} - {prev_name}"

    return subject, body


def main():
    password = "FIXME heslo pritece zvenku"

    client = connect()

    curr_group, next_group = determine_current_group_and_next(client)

    members = determine_group_members(client, next_group)

    print('prev. group:', curr_group)
    print('curr. group:', next_group)

    print('curr. group members:', members)

    # FIXME odstranit
    members = ["vladimirkroupa@gmail.com", "vlada.k@volny.cz"]

    subject, body = compose_email(curr_group, next_group)
    send_email(members, subject, body, password)


if __name__ == "__main__":
    main()
