import time
import datetime
from shutil import copyfile
import sys
import ntpath

MESSAGE_SIZE = 8192

def log(message):
    # print(msg)
    timestamp = datetime.datetime.fromtimestamp(time.time()).strftime("%H:%M:%S")
    print("[{}] ".format(timestamp) + message)

def create_log_terminal(filepath, output_file):
    filename = filepath.split('/')[-1].split('.')[0]
    output_file.write("<div class=\"quarter\">\n")
    output_file.write("<header>" + filename + "</header>\n")
    with open(filepath, 'r') as fp:  
        line_list = fp.readlines()
        for line in line_list:
            output_file.write("<code>" + line.rstrip('\n') + "</code><br/>\n")
    output_file.write("</div>\n")
