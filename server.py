import socket
import time
import struct
import sys
import utils

class Server():
    def __init__(self, *args, **kwargs):
        self.server_address = ('', 5006)
        self.send_to = ('', 5005)
        # return super().__init__(*args, **kwargs)

    def start(self):
        self.sock = socket.socket(socket.AF_INET, # Internet
                            socket.SOCK_DGRAM, # UDP
                            socket.IPPROTO_UDP)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        self.sock.settimeout(0.2);
        self.sock.bind(self.server_address)


    def sendMessages(self):
        try:
            i = 0
            while True:
                data, address = self.sock.recvfrom(8192)
                message = str(i)
                i+=1
                utils.log('Sending message: ' + message)
                sent = self.sock.sendto(message.encode(), self.send_to)
                time.sleep(1)
        finally:
            utils.log('Closin socket')
            self.sock.close()

server = Server()
server.start()
server.sendMessages()