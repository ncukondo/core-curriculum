import base64
import datetime
import time

_LAST_TIME=0
_EIDIAN = "big"
_SIZE=100

def time_based_uid(seed:datetime.datetime=None)->str:
    '''
    make uid from unix timestamp(milliseconds)
    '''
    global _LAST_TIME
    epoc_time = seed.timestamp() if seed else time.time()
    time_seed=round(epoc_time*_SIZE)
    if time_seed==_LAST_TIME:
        time.sleep(0.01)
        return time_based_uid()
    _LAST_TIME=time_seed
    b=time_seed.to_bytes(5,_EIDIAN,signed=False)
    id=base64.urlsafe_b64encode(b).decode().replace("=","")
    return id

def decode_time_based_uid(uid:str)->datetime.datetime:
    '''
    decode uid from unix timestamp(milliseconds) to datetime
    '''
    epoc_time = int.from_bytes(base64.urlsafe_b64decode((uid+"=").encode()), byteorder=_EIDIAN, signed=False)/_SIZE
    dt =  datetime.datetime.fromtimestamp(epoc_time)
    return dt

if __name__ == "__main__":
    for i in range(0,1000):
        uid=time_based_uid()
        decoded=decode_time_based_uid(uid)
        print(f"{uid}:  from {decoded}")
    model_time=datetime.datetime(2025,2,6,8,8,11)
    print(time_based_uid(model_time))
