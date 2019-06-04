import socket
import struct
import sys
import utils
from message import Message

class Client():

    def __init__(self, port, server_ip, server_port):
        self.client_address = ('', port)
        self.server_address = (server_ip, server_port)

        self.last_message_id = -1

    def start(self):
        self.sock = socket.socket(socket.AF_INET, # Internet
                            socket.SOCK_DGRAM) # UDP
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.sock.bind(self.client_address)

        sent = self.sock.sendto('SYN'.encode(), self.server_address)

    def received_messages(self):
        while True:
            utils.log('[Client] Waiting to receive message')
            data, address = self.sock.recvfrom(utils.MESSAGE_SIZE)
            
            message = Message.unpack(data)

            #TODO: handle packet loss

            utils.log('[Client] Received: ' + str(message))


if len(sys.argv) != 4:
    print("Invalid start arguments. Please, start the client as 'python3 client.py <client_port> <server_ip> <server_port>' ")
    exit(1)

client = Client(int(sys.argv[1]), sys.argv[2], int(sys.argv[3]))
client.start()
client.received_messages()