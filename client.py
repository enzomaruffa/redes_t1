import socket
import struct
import sys

import threading
from message import Message
import matplotlib.pyplot as plt
import matplotlib.animation as animation

import utils
from graph import GraphInstance

class Client():

    def __init__(self, port, server_ip, server_port):
        self.client_address = (socket.gethostname(), port)
        
        self.server_address = (server_ip, server_port)

        self.last_message_id = -1
        self.received_packets = 0
        self.lost_packets = []
        self.delayed_packets = []

        self.received_values = []

        self.running = True

        self.graph = GraphInstance(self.client_address)

        # ===

        self.sock = socket.socket(socket.AF_INET, # Internet
                            socket.SOCK_DGRAM) # UDP
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.sock.settimeout(60)
        self.sock.bind(self.client_address)

        # ====
 
        self.handler_thread = threading.Thread(target=self.receive_messages, args=())
        self.handler_thread.start()

        sent = self.sock.sendto('SYN'.encode(), self.server_address)

    def receive_messages(self):
        while self.running:
            utils.log('[Client] Waiting to receive message')
            data, address = self.sock.recvfrom(utils.MESSAGE_SIZE)
            
            if not running: #após cancelar, pode acabar pegando alguma mensagem ainda
                break

            message = Message.unpack(data)
            self.received_packets += 1

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

            self.received_values.append(message.payload)

            #### testing only
            if len(self.lost_packets) > 5:
                utils.log('[Client] Finished transmission because too many packets were lost!' + str(self.lost_packets))
                break
            if (self.last_message_id > 200):
                exit(0)


    def create_statistics(self):
        utils.log('[Client] Statistics - Total received packets: ' +  str((self.received_packets)))
        utils.log('[Client] Statistics - Total received packets on time: ' +  str(self.received_packets - len(self.delayed_packets)))
        utils.log('[Client] Statistics - Lost packets: ' +  str(len(self.lost_packets)))
        utils.log('[Client] Statistics - Delayed packets: ' +  str(len(self.delayed_packets)))


if len(sys.argv) != 4:
    print("Invalid start arguments. Please, start the client as 'python3 client.py <client_port> <server_ip> <server_port>' ")
    exit(1)

client = Client(int(sys.argv[1]), sys.argv[2], int(sys.argv[3]))

running = True

print("Client Menu! Close figure to exit stream and see stats!")

def handle_close(evt):
    global running

    print("Exiting stream...")
    client.running = False
    running = False
    print(client.sock)
    client.sock.shutdown(socket.SHUT_WR)
    client.sock.close()

ani = animation.FuncAnimation(client.graph.fig, client.graph.graph_animation, fargs=(1, client.received_values), interval=100)
client.graph.fig.canvas.mpl_connect('close_event', handle_close)

plt.show()

while running:
    continue

print("Exited streaming")

client.create_statistics()