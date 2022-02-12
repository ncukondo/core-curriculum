#!/usr/bin/env python
# coding: utf-8

# In[7]:


#!/usr/bin/env python
# coding: utf-8

import csv
import pandas as pd


r4_l1=pd.read_csv("./raw/sheets/R4コアカリ提出用/第1層.csv")
r4_l2=pd.read_csv("./raw/sheets/R4コアカリ提出用/第2層.csv")

columns=["第2層","第3層","第4層","メモ"]
r4_l234 = pd.DataFrame(data=[],columns=columns)
tabs=r4_l1["タブ名"]
for tab in tabs:
    r4_l34_unit=pd.read_csv(f"./raw/sheets/R4コアカリ提出用/{tab}.csv")
    r4_l234=pd.concat([r4_l234,r4_l34_unit.loc[:,columns]])

r4_l12=pd.merge(r4_l1,r4_l2,how="outer").rename(columns={"メモ":"第2層メモ"})
r4_full=pd.merge(r4_l12,r4_l234,how="outer")
r4_full.to_csv("./dist/r4_full.csv",encoding="utf_8_sig",quoting=csv.QUOTE_NONNUMERIC)
r4_no_disc=r4_full.loc[:,["第1層","第2層","第3層","第4層"]]
r4_no_disc.to_csv("./dist/r4_no_disc.csv",encoding="utf_8_sig",quoting=csv.QUOTE_NONNUMERIC)


# output ordered table for comments
order=["プロ", "総合", "生涯", "科学", "情報", "コミュ", "連携", "社会", "技能", "知識" ]
order_dict=pd.DataFrame({"order":[i for i,v in enumerate(order)],"タブ名":order})
r4_ordered=pd.merge(r4_full,order_dict,how="left",on="タブ名")
r4_ordered["temp_id"]=r4_ordered.index.astype(str).str.zfill(4)+r4_ordered["タブ名"]
r4_ordered=r4_ordered.sort_values(by="order",kind="mergesort")    .drop("order",axis=1)
r4_ordered    .to_csv("./dist/r4_full_ordered.csv",encoding="utf_8_sig",quoting=csv.QUOTE_NONNUMERIC)
r4_ordered     .loc[:,["temp_id","第1層","第2層","第3層","第4層"]]    .groupby(["第1層","第2層","第3層"], as_index=False,sort=False)    .first()    .drop("第4層",axis=1)    .to_csv("./dist/r4_l123_ordered.csv",encoding="utf_8_sig",quoting=csv.QUOTE_NONNUMERIC)
r4_ordered     .loc[:,["temp_id","第1層","第2層","第2層説明","第3層"]]    .groupby(["第1層","第2層","第2層説明",], as_index=False,sort=False)    .first()    .drop("第3層",axis=1)    .to_csv("./dist/r4_l12_ordered.csv",encoding="utf_8_sig",quoting=csv.QUOTE_NONNUMERIC)

r4_full


# In[8]:



from lib.dataframe_to_text import dataframe_to_text

r4_full=r4_full.fillna("")

r4_to_md=pd.DataFrame(data=[],columns=["第1層","第2層","第3層","第4層"])
r4_to_md["第1層"]="\n"+"# "+r4_full["第1層"]+"\n\n"+r4_full["第1層説明"]+"\n"
r4_to_md["第2層"]="\n"+"## "+r4_full["第2層"]+"\n\n"+r4_full["第2層説明"]+"\n"
r4_to_md["第3層"]="\n"+"### "+r4_full["第3層"]+"\n"
r4_to_md["第4層"]="1. "+r4_full["第4層"]

r4_md_to_edit=pd.DataFrame(data=[],columns=["第1層","第2層","第3層","第4層"])
r4_md_to_edit["第1層"]="\n"+"# "+r4_full["第1層"]+"(第1層)\n\n"+r4_full["第1層説明"]+"\n"
r4_md_to_edit["第2層"]="\n"+"## "+r4_full["第2層"]+"(第2層)\n\n"+r4_full["第2層説明"]+"\n"
r4_md_to_edit["第3層"]="\n"+"### "+r4_full["第3層"]+"(第3層)\n"
r4_md_to_edit["第4層"]="1. "+r4_full["第4層"]

r4_md_text=dataframe_to_text(r4_to_md)
with open("./dist/r4.md","w") as f:
    f.write(r4_md_text)

r4_md_text_to_edit=dataframe_to_text(r4_md_to_edit)
with open("./dist/r4_to_edit.md","w") as f:
    f.write(r4_md_text_to_edit)


# In[23]:


#!/usr/bin/env python
# coding: utf-8

import csv
import pandas as pd

from lib.dataframe_to_text import dataframe_to_text


r4_l1=pd.read_csv("./raw/sheets/R4コアカリ提出用/第1層.csv")
r4_l2=pd.read_csv("./raw/sheets/R4コアカリ提出用/第2層.csv")

columns=["第2層","第3層","第4層","メモ"]
r4_l234 = pd.DataFrame(data=[],columns=columns)
tabs=r4_l1["タブ名"]
for tab in tabs:
    r4_l34_unit=pd.read_csv(f"./raw/sheets/{tab}編集用/第2から4層.csv")
    r4_l234=pd.concat([r4_l234,r4_l34_unit.loc[:,columns]])

r4_l12=pd.merge(r4_l1,r4_l2,how="outer").rename(columns={"メモ":"第2層メモ"})
r4_full=pd.merge(r4_l12,r4_l234,how="outer")
r4_full.to_csv("./dist/r4_draft.csv",encoding="utf_8_sig",quoting=csv.QUOTE_NONNUMERIC)

r4_full

r4_full=r4_full.fillna("")

r4_to_md_draft=pd.DataFrame(data=[],columns=["第1層","第2層","第3層","第4層"])
r4_to_md_draft["第1層"]="\n"+"# "+r4_full["第1層"]+"\n\n"+r4_full["第1層説明"]+"\n"
r4_to_md_draft["第2層"]="\n"+"## "+r4_full["第2層"]+"\n\n"+r4_full["第2層説明"]+"\n"
r4_to_md_draft["第3層"]="\n"+"### "+r4_full["第3層"]+"\n"
r4_to_md_draft["第4層"]="1. "+r4_full["第4層"]


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

table

