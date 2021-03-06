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

    # Um cliente recebe uma porta para operar, um ip do servidor, uma porta do servidor e argumentos opcionais
    def __init__(self, port, server_ip, server_port, **kwargs):
        # ===
        output_file = kwargs.get('output_file', 'stdout')
        self.log_output_file = open(output_file, 'w')
        self.log_output_file.flush()

        # === Inicialização do servidor
        utils.log('[Cliente] Iniciando cliente...', optional_output_file=self.log_output_file)
        self.client_address = ('', port)
        # socket.gethostname()  
        self.server_address = (server_ip, server_port)

        self.last_message_id = -1
        self.received_packets = 0
        self.lost_packets = []
        self.delayed_packets = []

        self.received_values = []

        self.running = True

        self.graph = GraphInstance(self.client_address) # Instancialização da figura do gráfico

        # === Criação do socket do cliente

        self.sock = socket.socket(socket.AF_INET, # Internet
                            socket.SOCK_DGRAM) # UDP
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.sock.setblocking(3)
        self.sock.bind((self.client_address))

        # ==== Criação da Thread que ouve
 
        self.handler_thread = threading.Thread(target=self.receive_messages, args=())
        self.handler_thread.start()
        utils.log('[Cliente] Enviando mensagem para o servidor...', optional_output_file=self.log_output_file)
        sent = self.sock.sendto(Message(0, "sync", "").pack(), self.server_address) # Envia uma mensagem para o servidor, pedindo para entrar na lista

        print("Menu do Cliente! Feche o gráfico para calcular as estatísticas")

    def receive_messages(self):
        while self.running:
            utils.log('[Cliente] Aguardando mensagem...', optional_output_file=self.log_output_file)
            data, address = self.sock.recvfrom(utils.MESSAGE_SIZE)
            
            if not running: # Após cancelar, pode acabar pegando alguma mensagem ainda. Assim, garantimos que será ignorada
                break

            message = Message.unpack(data)
            self.received_packets += 1

            if message.message_type == "data":
                # Tratamento da perda de padcotes
                if message.id < self.last_message_id: # Nesse caso, a mensagem atrasou
                    self.delayed_packets.append(message.id)
                elif message.id > self.last_message_id + 1: # Nesse caso, algumas mensagens foram perdidas no meio do caminho
                    if self.last_message_id != -1: #
                        self.lost_packets += list(range(self.last_message_id + 1, message.id)) # Cria uma lista do formato [last + 1, message_id[

                self.received_values.append(message.payload)
    
            self.last_message_id = message.id if message.id > self.last_message_id else self.last_message_id  # Atualiza o ID da última mensagem recebida

            utils.log('[Cliente] Recebido: ' + str(message), optional_output_file=self.log_output_file)

            #### Apenas para testes
            # if len(self.lost_packets) > 5:
            #     utils.log('[Cliente] Transmissão finalizada pois muitas mensagens foram perdidas! Mensagens perdidas: ' + str(self.lost_packets), optional_output_file=self.log_output_file)
            #     break

    def create_statistics(self):
        utils.log('[Cliente] Estatísticas - Total de mensagens recebidas: ' +  str((self.received_packets)), optional_output_file=self.log_output_file)
        utils.log('[Cliente] Estatísticas - Total de mensagens recebidas no momento certo: ' +  str(self.received_packets - len(self.delayed_packets)), optional_output_file=self.log_output_file)
        utils.log('[Cliente] Estatísticas - Mensagens perdidas: ' +  str(len(self.lost_packets)), optional_output_file=self.log_output_file)
        utils.log('[Cliente] Estatísticas - Mensagens atrasadas: ' +  str(len(self.delayed_packets)), optional_output_file=self.log_output_file)

        print("\n\n")

    def handle_close(self, evt):
        global running

        self.sock.sendto(Message(1, "end", "").pack(), self.server_address) # Envia uma mensagem avisando para o servidor que está saindo
        
        utils.log("[Cliente] Finalizando stream......", optional_output_file=self.log_output_file)
        client.running = False
        running = False

        utils.log("[Cliente] Finalizando streaming", optional_output_file=self.log_output_file)
        utils.log("[Cliente] Calculando regressão linear...", optional_output_file=self.log_output_file)

        regression_coefficient = np.polyfit(list(range(0, len(client.received_values))), client.received_values, 1)[0] # Calcula a regressão linear dos dados

        if regression_coefficient < 1:
            utils.log("\nCuidado! As ações vão cair no futuro.... Não recomendo a compra! O coeficiente de crescimento foi de ", regression_coefficient, "\n", optional_output_file=self.log_output_file)
        elif regression_coefficient > 0:
            utils.log("\nCOMPRE COMPRE COMPRE! As ações vão crescer muitooooo!! O coeficiente de crescimento foi de ", regression_coefficient, "\n", optional_output_file=self.log_output_file)
        else:
            utils.log("\nHmmm, você que sabe. As ações ficarão estáveis! O coeficiente de crescimento foi de ", regression_coefficient, "\n", optional_output_file=self.log_output_file)



if (len(sys.argv) != 4) and (len(sys.argv) != 5):
    print("Inicialização errada! Por favor, inicie o cliente com 'python3 client.py <porta_cliente> <ip_servidor> <porta_servidor>' ")
    exit(1)
if (len(sys.argv) == 5):
    client = Client(int(sys.argv[1]), sys.argv[2], int(sys.argv[3]), output_file=sys.argv[4])
else:
    client = Client(int(sys.argv[1]), sys.argv[2], int(sys.argv[3]))
running = True

ani = animation.FuncAnimation(client.graph.fig, client.graph.graph_animation, fargs=(1, client.received_values), interval=100) # Cria a animação do gráfico
client.graph.fig.canvas.mpl_connect('close_event', client.handle_close) # Conecta o evento de fechar o gráfico com a função do cliente 'handle_close()'

plt.show()

while running:
    continue

client.create_statistics()

client.sock.close()

utils.log("========= FIM DA EXECUÇÃO =========\n\n", )