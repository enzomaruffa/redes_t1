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
        self.lost_packets = []
        self.delayed_packets = []

    def start(self):
        self.sock = socket.socket(socket.AF_INET, # Internet
                            socket.SOCK_DGRAM) # UDP
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.sock.settimeout(60)
        self.sock.bind(self.client_address)

        sent = self.sock.sendto('SYN'.encode(), self.server_address)

    def received_messages(self):
        while True:
            utils.log('[Client] Waiting to receive message')
            data, address = self.sock.recvfrom(utils.MESSAGE_SIZE)
            
            message = Message.unpack(data)

            #handles packet loss
            if message.id < self.last_message_id:
                # delayed
                self.delayed_packets.append(message.id)
            elif message.id > self.last_message_id + 1:
                # lost a few between
                if self.last_message_id != -1: #
                    self.lost_packets += list(range(self.last_message_id + 1, message.id)) #creates a range [last + 1, message_id[
    
            self.last_message_id = message.id

            utils.log('[Client] Received: ' + str(message))

            #### testing only
            if len(self.lost_packets) > 5:
                break

        utils.log('[Client] Finished transmission because too many packets were lost!' + str(self.lost_packets))

    def create_statistics(self):
        utils.log('[Client] Statistics - Lost packets: ' +  str(len(self.lost_packets)))
        utils.log('[Client] Statistics - Delayed packets: ' +  str(len(self.delayed_packets)))


if len(sys.argv) != 4:
    print("Invalid start arguments. Please, start the client as 'python3 client.py <client_port> <server_ip> <server_port>' ")
    exit(1)

client = Client(int(sys.argv[1]), sys.argv[2], int(sys.argv[3]))
client.start()
client.received_messages()
client.create_statistics()