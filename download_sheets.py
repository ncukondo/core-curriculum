import os.path
import os
import json
from dateutil import parser
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import pandas as pd


keyList=[
    "type",
    "project_id",
    "private_key_id",
    "private_key",
    "client_email",
    "client_id",
    "auth_uri",
    "token_uri",
    "auth_provider_x509_cert_url",
    "client_x509_cert_url"
]
client_secret_list =[f'"{key}": "{os.environ["GAUTH_"+key.upper()]}"' for key in keyList]
comma=',\n    '
client_secret=f'''
{{
    {comma.join(client_secret_list)}
}}
'''

def get_creds(scopes:list):
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(
        json.loads(client_secret),
        scopes=scopes
    )
    return credentials

_sheet_app:gspread.Client=None
def get_sheetapp()->gspread.Client:
    global _sheet_app
    if _sheet_app==None:
        _sheet_app=gspread.authorize(get_creds([
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive']))
    return _sheet_app

info=pd.read_csv("./r4_gsheets_info.csv")
try:
    for i,url in enumerate(list(info["url"])):
        spreadsheet = get_sheetapp().open_by_url(url)
        sheet_name=spreadsheet.title
        modified_recorded=None
        if str(info.at[i,"lastUpDate"])!="nan": 
            modified_recorded=parser.parse(str(info.at[i,"lastUpDate"]))
        else:
            modified_recorded=parser.parse("1980-10-06 12:00Z")
        lastUpdate=spreadsheet.lastUpdateTime
        modified=parser.parse(lastUpdate)
        print(f"{sheet_name} - Updated:{modified > modified_recorded}")

        if modified > modified_recorded:
            for sheet in list(spreadsheet.worksheets()):
                dir = f"./raw/gsheets/{sheet_name}"
                os.makedirs(dir, exist_ok=True)
                name=f'{sheet.title}'
                data = pd.DataFrame(sheet.get_all_records())
                print(f'saving {dir}/{sheet.title}.csv')
                data.to_csv(f"{dir}/{sheet.title}.csv",encoding="utf_8_sig",index=False)
        info.at[i,"lastUpDate"]=lastUpdate
except:
    print("APIError")

info.to_csv("./r4_gsheets_info.csv",encoding="utf_8_sig",index=False)



