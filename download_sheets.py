#!/usr/bin/env python
# coding: utf-8

# In[6]:


import os
import tempfile
import pandas as pd
import csv

from lib.export_google_sheets import export_google_sheets


folder_ids=[
        '1IDl3cSc8u5y4Gf13_PBCEZdFFnDv6Ilz', #入力
        '1HhIkzwUMBTfStSCyhSRf1SkbQq21hLnM', #データフォーマット
        '1NrjWTGweLNoUU1n-EH9yhIU5ZBUHOLs1', # R4 version0131に対する査読
        '1FlCwwi71s1BI4uhOf2CefX85byj1Alo_', #各チーム編集用シート
]
DIST_DIR="./raw/sheets/"

try:
    with tempfile.TemporaryDirectory() as temp_dir:
        file_list=export_google_sheets(folder_ids,temp_dir,info_stor_file="./raw/sheets/sheets_info.json")
        for file in file_list:
            book = pd.ExcelFile(file["export_path"])
            dir_name = os.path.join(DIST_DIR,file['name'])
            os.makedirs(dir_name,exist_ok=True)
            for name in book.sheet_names:
                sheet:pd.DataFrame = book.parse(name)
                sheet.to_csv(os.path.join(dir_name,f"{name}.csv"),encoding="utf_8_sig",index=False,)
except:
    import traceback
    traceback.print_exc()

