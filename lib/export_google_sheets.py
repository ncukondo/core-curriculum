import os
import json
import datetime
import tempfile

from dateutil.parser import parse as parse_date

from lib.google_drive import from_service_account


def export_google_sheets(folder_ids:list[str],dist_dir:str=None,info_stor_file:str="gsheets_info.json"):
    """ export excel from google sheet"""
    epoc_time='1970-01-01T00:00:00.000+00:00'

    if dist_dir is None:
        dist_dir=os.path.join(tempfile.gettempdir(),"exported_excel")
    os.makedirs(dist_dir, exist_ok=True)

    drive = from_service_account()
    gsheets_info={}
    with open(info_stor_file,"r",encoding="utf_8") as f:
        gsheets_info=json.load(f)

    check_datetime=datetime.datetime.now(datetime.timezone.utc).isoformat()

    global_updated=gsheets_info.get("global",{}).get("updated",epoc_time)
    query="\n and \n".join([ 
        "mimeType='application/vnd.google-apps.spreadsheet'",
        f"modifiedTime > '{global_updated}'",
        "trashed=false",
        f"""({" or ".join([f"'{x}' in parents" for x in folder_ids])})"""
    ])
    try:
        file_list =drive.get_list(query,["name","id","modifiedTime"])
        for file in file_list:
            timestamp=file["modifiedTime"].isoformat()
            file["timestamp"]=timestamp
            old_time_stamp=gsheets_info\
                .get("files",{}).get(file["id"],{})\
                .get("timestamp",epoc_time)
            if parse_date(timestamp) <= parse_date(old_time_stamp):
                print(f"skip: {file['name']}")
                continue
            file["export_path"]=drive.export(file["id"],"xlsx",dist_dir)
            yield file
            print(f'{file["name"]} in {timestamp}')
            gsheets_info["files"]=gsheets_info.get("files",{})
            gsheets_info["files"][file["id"]]={"timestamp":timestamp,"name":file["name"],"id":file["id"]}

        gsheets_info["global"]=gsheets_info.get("global",{})
        gsheets_info["global"]["updated"]=check_datetime
    except:
        raise
    finally:
        with open(info_stor_file,"w",encoding="utf_8") as f:
            json.dump(gsheets_info,f,indent=4, ensure_ascii=False)
