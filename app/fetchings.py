import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()



import gspread
from oauth2client.service_account import ServiceAccountCredentials
from app.models import *
from django.utils.timezone import localtime


SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
CREDENTIALS = ServiceAccountCredentials.from_json_keyfile_name(r'/home/projects/application/credentials.json', SCOPE)


def clone_datas():
    client = gspread.authorize(CREDENTIALS)
    spreadsheet = client.open('MY.GOV.UZ')
    worksheet = spreadsheet.worksheet('ALL')

    existing_rows = worksheet.get_all_values()
    existing_ids = set()

    for row in existing_rows[1:]:
        if len(row) >= 1:
            existing_ids.add(row[0])

    logs = RequestLog.objects.all().order_by('created_at')
    new_rows = []

    for log in logs:
        if str(log.id) not in existing_ids:
            created_str = localtime(log.created_at).strftime("%d.%m.%Y %H:%M")
            new_rows.append([
                str(log.id),
                created_str,
                log.operator.fio if log.operator else "",
                log.phone_num,
                log.num_app,
                log.theme.title if log.theme else "",
                log.service_id,
                log.comment
            ])
            existing_ids.add(str(log.id))

    if new_rows:
        worksheet.append_rows(new_rows, value_input_option="USER_ENTERED")
    
        print("Данные загружены")






def get_operator():
    client = gspread.authorize(CREDENTIALS)
    spreadsheet = client.open('MY.GOV.UZ')
    worksheet = spreadsheet.worksheet('SETTING')

    data = worksheet.get('A2:B')

    for row in data:
        if len(row) >= 2:
            fio = row[0].strip()
            operator_id = row[1].strip()

            Operator.objects.update_or_create(
                operator_id=operator_id,
                defaults={"fio": fio}
            )

def get_theme():
    client = gspread.authorize(CREDENTIALS)
    spreadsheet = client.open('MY.GOV.UZ')
    worksheet = spreadsheet.worksheet('SETTING')

    data = worksheet.get('C2:C')

    for row in data:
        if row and row[0].strip():
            title = row[0].strip()

            Theme.objects.update_or_create(title=title)




if __name__ == "__main__":
    # get_operator()
    # print("Операторы загружены.")
    # get_theme()
    clone_datas()
    print("Данные загружены")




