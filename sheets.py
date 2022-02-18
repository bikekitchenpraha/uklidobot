import gspread
import datetime
from typing import Tuple, List

from gspread import Worksheet

# SUN
NOTIFY_ON_DOW = 0


def determine_groups(worksheet: Worksheet) -> List[Tuple[int, str]]:
    def find_current_week_row(dates, current_year, current_week):
        for ix, date in enumerate(dates):
            year, week, _ = date.isocalendar()
            if year == current_year and week == current_week:
                return ix + 2

    def to_group_tuple(row) -> Tuple[int, str]:
        return int(row[1]), str(row[2])

    a_col = worksheet.col_values(1)
    raw_dates = a_col[1:]
    dates = [datetime.datetime.strptime(date_str, '%d.%m.%Y') for date_str in raw_dates]

    year, week, _ = datetime.datetime.today().isocalendar()
    row = find_current_week_row(dates, year, week)
    current_wk_group = to_group_tuple(worksheet.row_values(row))
    next_wk_group = to_group_tuple(worksheet.row_values(row + 1))
    return [current_wk_group, next_wk_group]


def find_group_members(worksheet: Worksheet, group_no: int, group_name: str) -> List[str]:
    people_col = worksheet.col_values(1)
    people = people_col[1:]

    group_ix = group_no + 1
    group_col = worksheet.col_values(group_ix)
    actual_group_name = group_col[0]
    if actual_group_name != group_name:
        raise Exception(f"Fetched column for group '{actual_group_name}', but '{group_name}' was needed")
    membership_flags = [bool_value == "TRUE" for bool_value in group_col[1:]]

    group_members = [person for person, is_member in zip(people, membership_flags) if is_member]
    return group_members


def find_member_addresses(people_ws: Worksheet, members: List[str]) -> List[Tuple[str, str]]:
    people_col = people_ws.col_values(1)
    people = people_col[1:]
    email_col = people_ws.col_values(2)
    emails = email_col[1:]

    return [(person, email) for person, email in zip(people, emails) if person in members]


def determine_current_group_and_next(client) -> Tuple[Tuple[int, str]]:
    cal_sheet = client.open_by_key('1tbtHGLT0jvMGMOUF7laOwIOX65szHTkAuFSfGQlwM0I')
    roster_ws = cal_sheet.worksheet('Úklid chodby')

    curr_group, next_group = determine_groups(roster_ws)
    return curr_group, next_group


def determine_group_members(client, group: Tuple[int, str]) -> List[Tuple[str, str]]:
    group_no, group_name = group

    groups_sheet = client.open_by_key('1E9TVhHrWORau9sISgL-9yoCsRdnklr3LYwTPz-FMJqQ')
    groups_ws = groups_sheet.worksheet('Skupiny na klíče')

    members = find_group_members(groups_ws, group_no, group_name)

    people_sheet = client.open_by_key('1qXsG1OpWh2hqBq3SH91MjHp7iLeUVpKVsieJCZvZQU4')
    people_ws = people_sheet.worksheet('Lidi s klíčema')

    return find_member_addresses(people_ws, members)


if __name__ == "__main__":
    client = gspread.service_account()

    curr_group, next_group = determine_current_group_and_next(client)

    members = determine_group_members(client, next_group)

    print('prev. group:', curr_group)
    print('curr. group:', next_group)

    print('curr. group members:', members)
