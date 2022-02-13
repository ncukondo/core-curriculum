#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from lib.dataframe_to_text import dataframe_to_text


r4_full= pd.read_csv("./dist/r4_full.csv")
r4_full=r4_full.fillna("")

r4_to_md=pd.DataFrame(data=[],columns=["第1層","第2層","第3層","第4層"])
r4_to_md["第1層"]="\n"+"# "+r4_full["第1層"]+"\n\n"+r4_full["第1層説明"]+"\n"
r4_to_md["第2層"]="\n"+"## "+r4_full["第2層"]+"\n\n"+r4_full["第2層説明"]+"\n"
r4_to_md["第3層"]="\n"+"### "+r4_full["第3層"]+"\n"
r4_to_md["第4層"]="1. "+r4_full["第4層"]

r4_md_text=dataframe_to_text(r4_to_md)
with open("./dist/r4.md","w") as f:
    f.write(r4_md_text)

print("output... ./dist/r4.md")
r4_md_text


# In[2]:



r4_draft=pd.read_csv("./dist/r4_draft.csv")

r4_to_md_draft=pd.DataFrame(data=[],columns=["第1層","第2層","第3層","第4層"])
r4_to_md_draft["第1層"]="\n"+"# "+r4_draft["第1層"]+"\n\n"+r4_draft["第1層説明"]+"\n"
r4_to_md_draft["第2層"]="\n"+"## "+r4_draft["第2層"]+"\n\n"+r4_draft["第2層説明"]+"\n"
r4_to_md_draft["第3層"]="\n"+"### "+r4_draft["第3層"]+"\n"
r4_to_md_draft["第4層"]="1. "+r4_draft["第4層"]


r4_md_draft=dataframe_to_text(r4_to_md_draft)
r4_md_draft += f"\n\n# 別表\n\n"

ex_tables = {
    "別表:基本的臨床手技": {"path":"./raw/sheets/技能編集用/基本的臨床手技.csv"},
    "別表:基本的診療科": {"path":"./raw/sheets/技能編集用/基本的診療科.csv"},
}

for table_name,info in ex_tables.items():
    table = pd.read_csv(info["path"])
    r4_md_draft += f"\n\n## {table_name}\n\n\n"+table.to_html()

table = pd.read_csv("./raw/sheets/知識編集用/臓器別知識.csv")
table = table.loc[:,["臓器","分類","項目名"]]
columns=list(table.columns.values)
temp_column=table.columns.values[-1]+"-temp"
table[temp_column]=table[table.columns.values[-1]]
table = table.groupby(columns).agg(lambda x:"".join(list(x)))
table=table.drop(temp_column,axis=1)
r4_md_draft += f"\n\n## 臓器別知識\n\n"+table.to_html()


with open("./dist/r4_draft.md","w") as f:
    f.write(r4_md_draft)

print("output... ./dist/r4_draft.md")

table

