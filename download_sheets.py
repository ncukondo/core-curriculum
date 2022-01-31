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

GAUTH_TYPE=os.environ.get('GAUTH_TYPE')
GAUTH_PROJECT_ID=os.environ.get('GAUTH_PROJECT_ID')
GAUTH_PRIVATE_KEY_ID=os.environ.get('GAUTH_PRIVATE_KEY_ID')
GAUTH_PRIVATE_KEY=os.environ.get('GAUTH_PRIVATE_KEY')
GAUTH_CLIENT_EMAIL=os.environ.get('GAUTH_CLIENT_EMAIL')
GAUTH_CLIENT_ID=os.environ.get('GAUTH_CLIENT_ID')
GAUTH_AUTH_URI=os.environ.get('GAUTH_AUTH_URI')
GAUTH_TOKEN_URI=os.environ.get('GAUTH_TOKEN_URI')
GAUTH_AUTH_PROVIDER_X509_CERT_URL=os.environ.get('GAUTH_AUTH_PROVIDER_X509_CERT_URL')
GAUTH_CLIENT_X509_CERT_URL=os.environ.get('GAUTH_CLIENT_X509_CERT_URL')

client_secret=f'''
{"{"}
    "type":"{GAUTH_TYPE}",
    "project_id":"{GAUTH_PROJECT_ID}",
    "private_key_id":"{GAUTH_PRIVATE_KEY_ID}",
    "private_key":"{GAUTH_PRIVATE_KEY}",
    "client_email":"{GAUTH_CLIENT_EMAIL}",
    "client_id":"{GAUTH_CLIENT_ID}",
    "auth_uri":"{GAUTH_AUTH_URI}",
    "token_uri":"{GAUTH_TOKEN_URI}",
    "auth_provider_x509_cert_url":"{GAUTH_AUTH_PROVIDER_X509_CERT_URL}",
    "client_x509_cert_url":"{GAUTH_CLIENT_X509_CERT_URL}"
{"}"}
'''

'''
with open("./client_secret.json","w") as f:
    f.write(client_secret)
'''
def get_creds(scopes:list,client_secret_file:str):
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        "./client_secret.json",
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
    print(f"{sheet_name} - Updated:{modified > modified_recorded}")

    try:
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



