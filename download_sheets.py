import os.path
import os
import json
from dateutil import parser
from datetime import date, time, datetime

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import pandas as pd

client_secret=f'''
{"{"}
    "type": "{os.environ['GAUTH_TYPE']}",
    "project_id": "{os.environ['GAUTH_PROJECT_ID']}",
    "private_key_id": "{os.environ['GAUTH_PRIVATE_KEY_ID']}",
    "private_key": "{os.environ['GAUTH_PRIVATE_KEY']}",
    "client_email": "{os.environ['GAUTH_CLIENT_EMAIL']}",
    "client_id": "{os.environ['GAUTH_CLIENT_ID']}",
    "auth_uri": "{os.environ['GAUTH_AUTH_URI']}",
    "token_uri": "{os.environ['GAUTH_TOKEN_URI']}",
    "auth_provider_x509_cert_url": "{os.environ['GAUTH_AUTH_PROVIDER_X509_CERT_URL']}",
    "client_x509_cert_url": "{os.environ['GAUTH_CLIENT_X509_CERT_URL']}"
{"}"}
'''

def get_creds(scopes:list,client_secret_file:str):
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
            'https://www.googleapis.com/auth/drive'],"client_secret.json"))
    return _sheet_app

info=pd.read_csv("./r4_gsheets_info.csv")
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
    info.at[i,"lastUpDate"]=lastUpdate
    print(f"{sheet_name} - Updated:{modified > modified_recorded}")

    if modified > modified_recorded:
        for sheet in list(spreadsheet.worksheets()):
            dir = f"./raw/gsheets/{sheet_name}"
            os.makedirs(dir, exist_ok=True)
            name=f'{sheet.title}'
            data = pd.DataFrame(sheet.get_all_records())
            print(f'saving {dir}/{sheet.title}.csv')
            data.to_csv(f"{dir}/{sheet.title}.csv",encoding="utf_8_sig",index=False)

info.to_csv("./r4_gsheets_info.csv",encoding="utf_8_sig",index=False)



