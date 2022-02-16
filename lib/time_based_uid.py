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
    uid=base64.urlsafe_b64encode(b).decode().replace("=","")
    return uid

def decode_time_based_uid(uid:str)->datetime.datetime:
    '''
    decode uid from unix timestamp(milliseconds) to datetime
    '''
    decoded_bytes=base64.urlsafe_b64decode((uid+"=").encode())
    epoc_time = int.from_bytes(decoded_bytes, byteorder=_EIDIAN, signed=False)/_SIZE
    decoded =  datetime.datetime.fromtimestamp(epoc_time)
    return decoded

def main():
    """ for test """
    ids = []
    for _ in range(0,1000):
        uid=time_based_uid()
        ids.append(uid)
        decoded=decode_time_based_uid(uid)
        print(f"{uid}\tfrom {decoded}")
    print(ids)
    with open("./uid_list.txt","w",encoding="utf_8") as f:
        f.write("\n".join(ids))
    model_time=datetime.datetime(2025,2,6,8,8,11)
    print(time_based_uid(model_time))

if __name__ == "__main__":
    main()
