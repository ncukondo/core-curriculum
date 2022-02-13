#!/usr/bin/env python
# coding: utf-8

# In[2]:


import os
import json
import tempfile

from dateutil.parser import parse as parse_date

from lib.google_drive import from_service_account

folder_id="1L4fQFNd42HEN5mPEgicRxZe3rY5_ZliB"

drive = from_service_account()
file_list= [
    "./dist/r4_draft.md",
    "./dist/r4_draft.pdf",
    "./dist/r4_draft.docx",
    "./dist/r4.md",
    "./dist/r4.pdf",
    "./dist/r4.docx",
]
for file_path in file_list:
    id=drive.update_by_name(file_path,folder_id)
    print(f"deploy {os.path.basename(file_path)} as {id}")

