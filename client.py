import socket
import struct
import sys

import threading

import numpy as np

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
            utils.log('[Cliente] Aguardando mensagem...')
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

            utils.log('[Cliente] Recebido: ' + str(message))

            self.received_values.append(message.payload)

            #### testing only
            if len(self.lost_packets) > 5:
                utils.log('[Cliente] Transmissão finalizada pois muitas mensagens foram perdidas! Mensagens perdidas: ' + str(self.lost_packets))
                break
            if (self.last_message_id > 200):
                exit(0)


    def create_statistics(self):
        utils.log('[Cliente] Estatísticas - Total de mensagens recebidas: ' +  str((self.received_packets)))
        utils.log('[Cliente] Estatísticas - Total de mensagens recebidas no momento certo: ' +  str(self.received_packets - len(self.delayed_packets)))
        utils.log('[Cliente] Estatísticas - Mensagens perdidas: ' +  str(len(self.lost_packets)))
        utils.log('[Cliente] Estatísticas - Mensagens atrasadas: ' +  str(len(self.delayed_packets)))


if len(sys.argv) != 4:
    print("Inicialização errada! Por favor, inicie o cliente com 'python3 client.py <porta_cliente> <ip_servidor> <porta_servidor>' ")
    exit(1)

client = Client(int(sys.argv[1]), sys.argv[2], int(sys.argv[3]))

running = True

print("Menu do Cliente! Feche o gráfico para calcular as estatísticas")

def handle_close(evt):
    global running

    print("Finalizando stream......")
    client.running = False
    running = False
    client.sock.shutdown(socket.SHUT_RD)
    client.sock.close()

ani = animation.FuncAnimation(client.graph.fig, client.graph.graph_animation, fargs=(1, client.received_values), interval=100)
client.graph.fig.canvas.mpl_connect('close_event', handle_close)

plt.show()

while running:
    continue

print("Finalizando streaming")

print("Calculando regressão linear...")

regression_coefficient = np.polyfit(list(range(0, len(client.received_values))), client.received_values, 1)[1]

if regression_coefficient < 1:
    print("\nCuidado! As ações vão cair no futuro.... Não recomendo a compra! O coeficiente de crescimento foi de ", regression_coefficient, "\n")
elif regression_coefficient > 0:
    print("\nCOMPRE COMPRE COMPRE! As ações vão crescer muitooooo!! O coeficiente de crescimento foi de ", regression_coefficient, "\n")
else:
    print("\nHmmm, você que sabe. As ações ficarão estáveis! O coeficiente de crescimento foi de ", regression_coefficient, "\n")


client.create_statistics()

