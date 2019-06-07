import time
import datetime
from shutil import copyfile
import sys
import ntpath

MESSAGE_SIZE = 8192

def log(message, **kwargs):
    timestamp = datetime.datetime.fromtimestamp(time.time()).strftime("%H:%M:%S")
    optional_output_file = kwargs.get('optional_output_file', None)
    if (optional_output_file) and (optional_output_file.name != 'stdout'):
        optional_output_file.write("[{}] ".format(timestamp) + message + "\n")
    print("[{}] ".format(timestamp) + message + "\n")

def create_log_terminal(filepath, output_file, initTime, lastTime):
    filename = filepath.split('/')[-1].split('.')[0]
    output_file.write("<div class=\"quarter\">\n")
    output_file.write("<header>" + filename + "</header>\n")
    log_file = open(filepath, 'r')
    while (initTime != lastTime):  
        line_list = log_file.readlines()
        hasTimeInLine = False
        for line in line_list:
            if initTime in line:
                hasTimeInLine = True
                output_file.write("<code>" + line.rstrip('\n') + "</code><br/>\n")
        if (hasTimeInLine == False):
            output_file.write("<code> </code><br/>\n")
        splitTime = initTime.split(':')
        initTime = ":".join([splitTime[0], splitTime[1], str(int(splitTime[2]) + 1)])
    output_file.write("</div>\n")