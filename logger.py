import utils
import sys
from shutil import copyfile


if len(sys.argv) != 5:
    print("Invalid start arguments. Please, start the client as 'python3 utils.py <input_log_1> <input_log_2> <input_log_3> <input_log_4>' ")
    exit(1)

output_filepath =  './logs/log.html'
copyfile('./logs/template.html', output_filepath)

output_file = open(output_filepath, 'a+')
output_file.seek(47)

output_file.write("<div class=\"row\">\n")
utils.create_log_terminal(sys.argv[1], output_file, '18:37:12', '18:37:48')
utils.create_log_terminal(sys.argv[2], output_file, '18:37:12', '18:37:48')
output_file.write("</div>\n")
output_file.write("<div class=\"row\">\n")
utils.create_log_terminal(sys.argv[3], output_file, '18:37:12', '18:37:48')
utils.create_log_terminal(sys.argv[4], output_file, '18:37:12', '18:37:48')
output_file.write("</div>\n")
output_file.write("<script src=\"./log.js\"></script>\n")

