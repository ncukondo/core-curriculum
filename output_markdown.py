#!/usr/bin/env python
# coding: utf-8

# In[18]:


import pandas as pd
from lib.dataframe_to_text import dataframe_to_text


r4_full= pd.read_csv("./dist/r4_full.csv")
r4_full=r4_full.dropna(subset=["第1層","第2層","第3層","第4層"])

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


# In[5]:


import pandas as pd

from lib.dataframe_to_text import dataframe_to_text


r4_draft=pd.read_csv("./dist/r4_draft.csv")

r4_to_md_draft=pd.DataFrame(data=[],columns=["第1層","第2層","第3層","第4層"])
r4_to_md_draft["第1層"]="\n"+"# "+r4_draft["第1層"]+"\n\n"+r4_draft["第1層説明"]+"\n"
r4_to_md_draft["第2層"]="\n"+"## "+r4_draft["第2層"]+"\n\n"+r4_draft["第2層説明"]+"\n"
r4_to_md_draft["第3層"]="\n"+"### "+r4_draft["第3層"]+"\n"
r4_to_md_draft["第4層"]="1. "+r4_draft["第4層"]
r4_to_md_draft=r4_to_md_draft.dropna(subset=["第1層","第2層","第3層","第4層"])
r4_to_md_draft=r4_to_md_draft[~(r4_to_md_draft["第4層"].str.startswith("削除"))]

r4_to_md_draft

r4_md_draft=r"""---
title: "医学教育モデル・コア・カリキュラム"
header-includes: 
- \usepackage{multirow}
- \usepackage{xltabular}
- \usepackage{longtable}
- \usepackage{ltablex}
- \usepackage {booktabs}
figureTitle: "図 "
tableTitle: "表 "
listingTitle: "コード "
figPrefix: "図."
eqnPrefix: "式."
tblPrefix: "表."
lstPrefix: "コード."
---
"""
r4_md_draft += dataframe_to_text(r4_to_md_draft)
r4_md_draft += f"\n\n# 別表\n\n"

tables = ""

with open("./dist/r4_draft_tables.tex","r") as f:
    latex_tables = f.read()

r4_md_draft += latex_tables


with open("./dist/r4_draft.md","w") as f:
    f.write(r4_md_draft)

print("output... ./dist/r4_draft.md")

