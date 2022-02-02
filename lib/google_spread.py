import gspread
from lib.google_auth import get_creds

_sheet_app:gspread.Client=None
def get_sheetapp()->gspread.Client:
    global _sheet_app
    if _sheet_app==None:
        _sheet_app=gspread.authorize(get_creds())
    return _sheet_app
