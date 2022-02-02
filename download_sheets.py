import os.path
import os
from dateutil import parser
import pandas as pd
from lib.google_spread import get_sheetapp


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



