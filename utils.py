import time
import datetime

MESSAGE_SIZE = 8192

def log(message):
    # print(msg)
    timestamp = datetime.datetime.fromtimestamp(time.time()).strftime("%H:%M:%S")
    print("[{}] ".format(timestamp) + message)



