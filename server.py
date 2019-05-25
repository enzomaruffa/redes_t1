import socket
import time

UDP_IP = "127.0.0.1"
UDP_PORT = 5005


print("UDP target IP:", UDP_IP)
print("UDP target port:", UDP_PORT)

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP

for i in range(0, 100):
    message = "Message number: " + str(i) 
    print(message)
    sock.sendto(message.encode(), (UDP_IP, UDP_PORT))
    time.sleep(1)