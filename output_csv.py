#!/usr/bin/env python
# coding: utf-8

# In[22]:


#!/usr/bin/env python
# coding: utf-8

import csv
import pandas as pd


r4_l1=pd.read_csv("./raw/sheets/R4コアカリ提出用/第1層.csv")
r4_l2=pd.read_csv("./raw/sheets/R4コアカリ提出用/第2層.csv")

columns=["第2層","第3層","第4層","メモ","H28対応項目"]
r4_l234 = pd.DataFrame(data=[],columns=columns)
tabs=r4_l1["タブ名"]
for tab in tabs:
    r4_l34_unit=pd.read_csv(f"./raw/sheets/R4コアカリ提出用/{tab}.csv")
    r4_l234=pd.concat([r4_l234,r4_l34_unit.loc[:,columns]])

r4_l12=pd.merge(r4_l1,r4_l2,how="outer").rename(columns={"メモ":"第2層メモ"})
r4_full=pd.merge(r4_l12,r4_l234,how="outer")
r4_full=r4_full.dropna(subset=["第1層","第2層","第3層","第4層"])

r4_no_disc=r4_full.loc[:,["第1層","第2層","第3層","第4層"]]

r4_full.to_csv("./dist/r4_full.csv",encoding="utf_8_sig",quoting=csv.QUOTE_NONNUMERIC,index=False)
print("output... r4_full.csv")
r4_no_disc.to_csv("./dist/r4_no_disc.csv",encoding="utf_8_sig",quoting=csv.QUOTE_NONNUMERIC,index=False)
print("output... r4_no_dics.csv")

r4_full


# In[29]:


import csv
import pandas as pd

r4_l1_draft=pd.read_csv("./raw/sheets/R4コアカリ提出用/第1層.csv")

r4_l1_draft.to_csv("./dist/output/outcomes_l1.csv",encoding="utf_8_sig",quoting=csv.QUOTE_NONNUMERIC,index=False)
print("output... ./dist/output/outcomes_l1.csv")

columns=["第1層","第2層","第2層説明","第3層","第4層","メモ","UID","H28対応項目"]
r4_l234_draft = pd.DataFrame(data=[],columns=columns)
r4_l2 =  pd.DataFrame(data=[],columns=[])
tabs=r4_l1_draft["タブ名"]
for index, row in r4_l1_draft.iterrows():
    r4_l34_unit=pd.read_csv(f"./raw/sheets/{row.タブ名}編集用/第2から4層.csv")
    r4_l2_unit=pd.read_csv(f"./raw/sheets/{row.タブ名}編集用/第2層.csv")
    r4_l2 = pd.concat([r4_l2,r4_l2_unit])
    r4_l34_unit["第1層"] = row.第1層
    r4_l34_unit = pd.merge(r4_l34_unit,r4_l2_unit,how="left",on="第2層")
    r4_l234_draft=pd.concat([r4_l234_draft,r4_l34_unit.loc[:,columns]])

r4_l2.to_csv("./dist/output/outcomes_l2.csv",encoding="utf_8_sig",quoting=csv.QUOTE_NONNUMERIC,index=False)
print("output... ./dist/output/outcomes_l2.csv")

r4_full_draft=pd.merge(r4_l1_draft,r4_l234_draft,how="outer",on="第1層")
r4_full_draft=r4_full_draft.dropna(subset=["第1層","第2層","第3層","第4層"])
r4_full_draft.to_csv("./dist/r4_draft.csv",encoding="utf_8_sig",quoting=csv.QUOTE_NONNUMERIC,index=False)
print("output... r4_draft.csv")
r4_full_draft.loc[:,["第1層","第2層","第3層","第4層","UID","H28対応項目"]].to_csv("./dist/output/outcomes.csv",encoding="utf_8_sig",quoting=csv.QUOTE_NONNUMERIC,index=False)
print("output... outcomes.csv")

r4_full_draft


# In[24]:


import pandas as pd
import glob
import re
import csv
import os

os.makedirs(os.path.join("dist", "output", "tables"), exist_ok=True)
file_list = glob.glob(f"./raw/sheets/*編集用/別表-*.csv")
for file in file_list:
    name = re.search(r"別表\-(.+)\.csv",file).group(1)
    df = pd.read_csv(file,encoding="utf_8_sig")
    df.to_csv(f"./dist/output/tables/{name}.csv",encoding="utf_8_sig",quoting=csv.QUOTE_NONNUMERIC,index=False)
    print(f"output... ./dist/output/tables/{name}.csv")


# In[25]:


import pandas as pd
import glob
import re
import csv
import os

r4_l1=pd.read_csv("./raw/sheets/R4コアカリ提出用/第1層.csv").loc[:,["タブ名","第1層"]]
os.makedirs(os.path.join("dist", "output", "tables"), exist_ok=True)
file_list = glob.glob(f"./raw/sheets/*編集用/行き先がないID.csv")
df = pd.DataFrame([],columns=[])
for file in file_list:
    name = re.search(r"([^\\\/]+)編集用",file).group(1)
    unit = pd.read_csv(file,encoding="utf_8_sig")
    print(name)
    unit["タブ名"]=name
    df= pd.concat([df,unit])

df=pd.merge(df,r4_l1,how="left",on="タブ名")
df.to_csv(f"./dist/output/deleted_or_moved.csv",encoding="utf_8_sig",quoting=csv.QUOTE_NONNUMERIC,index=False)
print(f"output... ./dist/output/deleted_or_moved.csv")

