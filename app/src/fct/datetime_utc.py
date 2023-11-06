import datetime   
import time

def str_to_datetime_obj(timestamp:str):
    timestamp = timestamp.upper()
    timestamp = timestamp.replace("T", " ")
    timestamp = timestamp.replace("Z", "")
    if "." in timestamp:
        timestamp = timestamp.split(".")[0]
    timestamp = datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
    return timestamp

def str_to_local_time(timestamp:str):
    timestamp = timestamp.upper()
    is_utc = False
    if "Z" in timestamp:
        is_utc = True
    timestamp = str_to_datetime_obj(timestamp)
    if not is_utc:
        return timestamp.strftime("%Y-%m-%d %H:%M:%S")
    now_timestamp = time.time()
    offset = datetime.datetime.fromtimestamp(now_timestamp) - datetime.datetime.utcfromtimestamp(now_timestamp)
    if datetime.datetime.fromtimestamp(now_timestamp) > timestamp:
        timestamp = timestamp + offset
    return timestamp.strftime("%Y-%m-%d %H:%M:%S")