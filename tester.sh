x-terminal-emulator -e "python3 server.py 5001 5002 0.1 > ./logs/server.txt"
x-terminal-emulator -e "python3 client.py 5003 127.0.0.1 5001 > ./logs/client_1.txt"
x-terminal-emulator -e "python3 client.py 5004 127.0.0.1 5001 > ./logs/client_2.txt"
x-terminal-emulator -e "python3 client.py 5005 127.0.0.1 5001 > ./logs/client_3.txt"