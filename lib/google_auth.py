import os.path
import os
import json
from oauth2client.service_account import ServiceAccountCredentials


# load client secret
_keyList=[
    "type",
    "project_id",
    "private_key_id",
    "private_key",
    "client_email",
    "client_id",
    "auth_uri",
    "token_uri",
    "auth_provider_x509_cert_url",
    "client_x509_cert_url"
]
_client_secret_list =[f'"{key}": "{os.environ["GAUTH_"+key.upper()]}"' for key in _keyList]
_comma=',\n    '
_client_secret=f'''
{{
    {_comma.join(_client_secret_list)}
}}
'''

_SCOPES=['https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive']

_creds=None
def get_creds():
    global _creds
    if _creds!=None:
        return _creds
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(
        json.loads(_client_secret),
        scopes=_SCOPES
    )
    return credentials
