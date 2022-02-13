#!/usr/bin/env python
# coding: utf-8

# In[1]:


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
r4_no_disc=r4_full.loc[:,["第1層","第2層","第3層","第4層"]]

r4_full.to_csv("./dist/r4_full.csv",encoding="utf_8_sig",quoting=csv.QUOTE_NONNUMERIC,index=False)
print("output... r4_full.csv")
r4_no_disc.to_csv("./dist/r4_no_disc.csv",encoding="utf_8_sig",quoting=csv.QUOTE_NONNUMERIC,index=False)
print("output... r4_no_dics.csv")

r4_full


# In[4]:


import csv
import pandas as pd

r4_l1_draft=pd.read_csv("./raw/sheets/R4コアカリ提出用/第1層.csv")
r4_l2_draft=pd.read_csv("./raw/sheets/R4コアカリ提出用/第2層.csv")

columns=["第2層","第3層","第4層","メモ"]
r4_l234_draft = pd.DataFrame(data=[],columns=columns)
tabs=r4_l1_draft["タブ名"]
for tab in tabs:
    r4_l34_unit=pd.read_csv(f"./raw/sheets/{tab}編集用/第2から4層.csv")
    r4_l234_draft=pd.concat([r4_l234_draft,r4_l34_unit.loc[:,columns]])

r4_l12_draft=pd.merge(r4_l1_draft,r4_l2_draft,how="outer").rename(columns={"メモ":"第2層メモ"})
r4_full_draft=pd.merge(r4_l12_draft,r4_l234_draft,how="outer")
r4_full_draft=r4_full_draft.fillna("")
r4_full_draft.to_csv("./dist/r4_draft.csv",encoding="utf_8_sig",quoting=csv.QUOTE_NONNUMERIC,index=False)
print("output... r4_draft.csv")

r4_full_draft
