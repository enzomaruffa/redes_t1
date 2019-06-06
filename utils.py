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

def create_log_terminal(filepath):
    filename = filepath.split('/')[-1].split('.')[0]
    output_file.write("<div class=\"quarter\">\n")
    output_file.write("<header>" + filename + "</header>\n")
    with open(filepath, 'r') as fp:  
        line_list = fp.readlines()
        for line in line_list:
            output_file.write("<code>" + line.rstrip('\n') + "</code><br/>\n")
    output_file.write("</div>\n")

if len(sys.argv) != 5:
    print("Invalid start arguments. Please, start the client as 'python3 utils.py <input_log_1> <input_log_2> <input_log_3> <input_log_4>' ")
    exit(1)

output_filepath =  './logs/log.html'
copyfile('./logs/template.html', output_filepath)

output_file = open(output_filepath, 'a+')
output_file.seek(8)


output_file.write("<div class=\"row\">\n")
create_log_terminal(sys.argv[1])
create_log_terminal(sys.argv[2])
output_file.write("</div>\n")
output_file.write("<div class=\"row\">\n")
create_log_terminal(sys.argv[3])
create_log_terminal(sys.argv[4])
output_file.write("</div>\n")

