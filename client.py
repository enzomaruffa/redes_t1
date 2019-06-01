import socket
import struct
import sys
import utils

class Client():
    def __init__(self, port):
        self.client_address = ('', port)
        self.server_address = ('', 5006)

    def start(self):
        self.sock = socket.socket(socket.AF_INET, # Internet
                            socket.SOCK_DGRAM) # UDP
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.sock.bind(self.client_address)

    def receiveMessages(self):
        while True:
            sent = self.sock.sendto('SYN', self.server_address)
            utils.log('Waiting to receive message')
            data, address = self.sock.recvfrom(1024)
            utils.log('Received: ' + data.decode())


client = Client(5005)
client.start()
client.receiveMessages()