import socket
import time
import struct
import sys
import utils
from message import Message
import threading
import random

class Server():
    def __init__(self, server_receiver_port, server_sender_port, timeout, time_between_messages):

        utils.log('[Server] Starting server on port ' + str(server_receiver_port))

        self.server_receiver_address = ('', server_receiver_port)
        self.server_sender_address = ('', server_sender_port)

        self.time_between_messages = time_between_messages
        self.clients = []

        self.sent_values = []

        self.last_message_id = -1
        self.running = True
        self.streaming = True

        # Creates the receiver socket
        self.listener_sock = socket.socket(socket.AF_INET, # Internet
                            socket.SOCK_DGRAM, # UDP
                            socket.IPPROTO_UDP)
        self.listener_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.listener_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        #self.listener_sock.settimeout(timeout)
        self.listener_sock.bind(self.server_receiver_address)

        # Creates the sender socket
        self.sender_sock = socket.socket(socket.AF_INET, # Internet
                            socket.SOCK_DGRAM, # UDP
                            socket.IPPROTO_UDP)
        self.sender_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sender_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        self.sender_sock.settimeout(timeout)
        self.sender_sock.bind(self.server_sender_address)

        # ====
 
        self.handler_thread = threading.Thread(target=self.receive_messages, args=())
        self.handler_thread.start()

        self.sender_thread = threading.Thread(target=self.send_messages, args=())
        self.sender_thread.start()

        # return super().__init__(*args, **kwargs)

    def receive_messages(self):
        try: 
            while self.running:
                data, address = self.listener_sock.recvfrom(utils.MESSAGE_SIZE)
                utils.log('[Server] Received message: ' + data.decode())
                if address not in self.clients:
                    self.clients.append(address) #address example: ('127.0.0.1', 57121)
        except Exception:
           utils.log('[Server] Closing receiver socket')

    def send_messages(self):
        try:
            i = 0
            while self.running:
                if self.streaming:
                    message_payload = random.randint(1,101)
                    i+=1
                    
                    self.sent_values.append(message_payload)
                    message = Message(self.last_message_id, message_payload)
                    for client in self.clients:
                        utils.log('[Server] Sending to client (' + client[0] + ', ' + str(client[1]) + ') the message: ' + str(message))
                        sent = self.sender_sock.sendto(message.pack(), client)

                    self.last_message_id += 1
                    time.sleep(self.time_between_messages)
        finally:
            utils.log('[Server] Closing sender socket')
            self.sender_sock.close()


if len(sys.argv) != 4:
    print("Invalid start arguments. Please, start the server as 'python3 server.py <server_receiver_port> <server_sender_port> <time_between_messages>' ")
    exit(1)

server = Server(int(sys.argv[1]), int(sys.argv[2]), 5, float(sys.argv[3]))

running = True

print("Server Menu! Use 'p' to play stream, 's' to pause stream and 'f' to end stream!")
while running:
    input_text = input()
    if input_text == "p":
        print("Setting stream status to playing!")
        server.streaming = True
    elif input_text == "s":
        print("Setting stream status to paused!")
        server.streaming = False
    elif input_text == "f":
        print("Finishing stream...")
        server.listener_sock.close()
        server.running = False
        running = False
    else: 
        print("Unknown command")

print("Finished streaming")

