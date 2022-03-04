#!/usr/bin/env python
# coding: utf-8

# In[1]:


import glob
import os
import re

import pandas as pd

r4_l1= pd.read_csv("./raw/sheets/R4コアカリ提出用/第1層.csv").set_index("タブ名")


r4_full= pd.read_csv("./dist/r4_full.csv")
table_df= pd.DataFrame([])
table_files = glob.glob('./raw/sheets/R4コアカリ提出用-別表/別表-*.csv')
for file in table_files:
    df = pd.read_csv(file)
    table = re.search(r'別表\-(.+)\.csv',file).groups()[0]
    df["項目"]=f"[別表]{table}"
    table_df=pd.concat([table_df,df],axis=0)
table_df.to_csv("./dist/r4_table_all.csv",encoding="utf_8_sig",index=False)


r4_counts=r4_full    .groupby("第1層",sort=False,as_index=False)    .count()    .loc[:,["第1層","第4層"]]    .rename(columns={"第1層":"項目","第4層":"数"})
r4_counts["項目"]=r4_counts["項目"].str.replace(r"(.+)",r"\1-第4層",regex=True)

table_counts=table_df    .groupby(["項目"],sort=False,as_index=False)    .count()    .loc[:,["項目","H28対応項目"]]    .rename(columns={"H28対応項目":"数"})
r4_counts = pd.concat([r4_counts,table_counts],axis=0)

new_line=pd.DataFrame({"項目":[f"合計"],"数":[r4_counts["数"].sum()]})
r4_counts = pd.concat([r4_counts,new_line],axis=0)

r4_counts.to_csv("./dist/r4_counts.csv",encoding="utf_8_sig",index=False)
r4_counts


# In[2]:


h28=pd.read_csv("./dist/H28.csv")
files = glob.glob('./raw/sheets/*編集用/行き先がないID.csv')
removed_ids= pd.DataFrame([])
for file in files:
    if os.path.getsize(file)<8:
        continue
    df = pd.read_csv(file)
    dir = os.path.basename(os.path.dirname(file))
    tab = re.match(r'(.+?)編集用',dir).group(1)
    df["第1層"]=r4_l1.at[tab,"第1層"]
    df=pd.merge(df,h28.loc[:,["id5","text5"]],left_on="H28ID",right_on="id5",how="left")
    removed_ids = pd.concat([removed_ids,df.loc[:,["第1層","H28ID","理由・コメント","text5"]]],axis=0)

removed_ids=removed_ids.rename(columns={"text5":"H28","理由・コメント":"削除コメント","第1層":"削除担当"})


h28_to_r4 = pd.DataFrame([])
for tab in r4_l1.index:
    df = pd.read_csv(f'./raw/sheets/R4コアカリ提出用/{tab}.csv')
    df["第1層"]=r4_l1.at[tab,"第1層"]
    df["行き先"]=df["第1層"]+"/"+df["第2層"]+"/"+df["第3層"]
    h28_to_r4 = pd.concat([h28_to_r4,df.loc[:,["行き先","H28対応項目"]]],axis=0)


table_df = pd.read_csv('./dist/r4_table_all.csv')
table_h28_to_r4 = table_df.rename(columns={"項目":"行き先"})
h28_to_r4 = pd.concat([h28_to_r4,table_h28_to_r4.loc[:,["行き先","H28対応項目"]]],axis=0)

h28_to_r4= h28_to_r4.rename(columns={"H28対応項目":"H28ID"})


h28_to_r4["H28ID"]=h28_to_r4["H28ID"].str.split(",")
h28_to_r4=h28_to_r4.explode("H28ID")

removed_ids["H28ID"]=removed_ids["H28ID"].str.split(",")
removed_ids=removed_ids.explode("H28ID")

def joinText(split:str):
    def joinNonEmpty(l:list[str]):
        l = list(filter(lambda x: x!="",l))
        return split.join(l) if len(l)>0 else None        
    return joinNonEmpty

h28ids=h28.loc[:,["id5"]].rename(columns={"id5":"H28ID"})
h28ids_to_r4=pd.merge(h28ids,h28_to_r4,on="H28ID",how="outer")
h28ids_to_r4=pd.merge(h28ids_to_r4,removed_ids,on="H28ID",how="outer")
h28ids_to_r4=h28ids_to_r4.fillna("")
h28ids_to_r4=h28ids_to_r4.groupby(["H28ID"],as_index=False,sort=False).agg({
    "行き先":joinText(","),
    "削除担当":joinText(","),
    "削除コメント":joinText(","),
    "H28":joinText(",")
})

removed_ids=pd.merge(removed_ids,h28_to_r4,on="H28ID",how="left")
removed_ids.to_csv("./dist/r4_removed_ids.csv",encoding="utf_8_sig",index=False)
removed_ids
h28_to_r4=pd.merge(h28,h28ids_to_r4,left_on="id5",right_on="H28ID")
h28_to_r4.to_csv("./dist/h28_to_r4.csv",encoding="utf_8_sig",index=False)
h28_to_r4


# In[3]:


r4_new = pd.read_csv("./dist/r4_full.csv").loc[:,["第1層","第2層","第3層","第4層","H28対応項目"]]

r4_new= r4_new.rename(columns={"H28対応項目":"H28ID"})
r4_new=r4_new.fillna("")
r4_new=r4_new[r4_new["H28ID"]==""]
r4_new.to_csv("./dist/r4_new.csv",index=False,encoding="utf_8_sig")
r4_new

r4_draft_new = pd.read_csv("./dist/r4_draft.csv").loc[:,["第1層","第2層","第3層","第4層","H28対応項目"]]

r4_draft_new= r4_draft_new.rename(columns={"H28対応項目":"H28ID"})
r4_draft_new=r4_draft_new.fillna("")
r4_draft_new=r4_draft_new[r4_draft_new["H28ID"]==""]
r4_draft_new.to_csv("./dist/r4_draft_new.csv",index=False,encoding="utf_8_sig")
r4_draft_new

