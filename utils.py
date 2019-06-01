import time
import datetime



def log(message):
    # print(msg)
    timestamp = datetime.datetime.fromtimestamp(time.time()).strftime("%H:%M:%S")
    print("[{}] ".format(timestamp) + message)



