#!/usr/bin/env python
# coding: utf-8

# In[8]:


import pandas as pd
from lib.dataframe_to_table import make_latex_table
from lib.dataframe_to_table import make_html_table
from textwrap import dedent
import glob

def make_draft_tables():
    table_index = pd.read_csv('./raw/sheets/別表一覧/別表一覧.csv')

    latex_output=""
    html_output=""
    for row in table_index.itertuples():
        file = list[0] if len(list:=glob.glob(f"./raw/sheets/*編集用/{row.データ元}.csv"))>0 else ""
        if file=="":
            continue
        table = pd.read_csv(file)

        table = table.loc[:,row.列.split(",")]
        latex_output+=make_latex_table(table,row.id,group=True)+"\n\n"
        html_output+=make_html_table(table,group=True)+"\n\n"

    with open("./dist/r4_draft_tables.tex","w") as f:
        f.write(latex_output)
    with open("./dist/r4_draft_tables.html","w") as f:
        f.write(html_output)

    print("output... ./dist/r4_tables.tex")

make_draft_tables()

