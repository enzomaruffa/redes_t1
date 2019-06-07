import socket
import time
import struct
import sys
import utils
from message import Message
import threading
import numpy as np
import random

class Server():
    def __init__(self, server_receiver_port, server_sender_port, timeout, time_between_messages):

        utils.log('[Servidor] Iniciando servidor na porta ' + str(server_receiver_port))

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
                message = Message.unpack(data)

                utils.log('[Servidor] Mensagem recebida: ' + str(message))

                if message.message_type == "sync":
                    if address not in self.clients:
                        utils.log('[Servidor] Adicionando o cliente (' + address[0] + ', ' + str(address[1]) + ') na lista')
                        self.clients.append(address) #address example: ('127.0.0.1', 57121)
                elif message.message_type == "end":
                    if address in self.clients:
                        utils.log('[Servidor] Removendo o cliente (' + address[0] + ', ' + str(address[1]) + ') da lista')
                        
                        self.clients.remove(address) #address example: ('127.0.0.1', 57121)

                        message = Message(self.last_message_id, "end", "bye!")
                        self.last_message_id += 1
                        self.listener_sock.sendto(message.pack(), address)

                        utils.log('[Servidor] Enviando para o cliente (' + address[0] + ', ' + str(address[1]) + ') a mensagem: ' + str(message))
                        
                    
        except Exception:
           utils.log('[Servidor] Fechando socket para novos clientes...')

    def send_messages(self):
        try:
            starting_value = random.randint(100,1000)
            while self.running:
                if self.streaming:

                    message_payload = starting_value

                    starting_value += starting_value * np.random.normal(loc = 0, scale = 0.09)
                    if starting_value <= 10:
                        starting_value += random.randint(1,10)
                    
                    self.sent_values.append(message_payload)
                    message = Message(self.last_message_id, "data", message_payload)
                    for client in self.clients:
                        utils.log('[Servidor] Enviando para o cliente (' + client[0] + ', ' + str(client[1]) + ') a mensagem: ' + str(message))
                        sent = self.sender_sock.sendto(message.pack(), client)

                    self.last_message_id += 1
                    time.sleep(self.time_between_messages)
        finally:
            utils.log('[Servidor] Fechando socket de envio...')
            self.sender_sock.close()


if len(sys.argv) != 4:
    print("Inicialização errada! Por favor, inicie o servidor com 'python3 server.py <porta_escuta_servidor> <porta_envio_servidor> <tempo_entre_mensagens>' ")
    exit(1)

server = Server(int(sys.argv[1]), int(sys.argv[2]), 5, float(sys.argv[3]))

running = True

print("Menu do servidor! Use 'p' para despausar o stream, 's' para pausar e 'f' para finalizar!")
try:
    while running:
        input_text = input()
        if input_text == "p":
            print("Rodando stream!")
            server.streaming = True
        elif input_text == "s":
            print("Pausando stream!")
            server.streaming = False
        elif input_text == "f":
            print("Finalizando stream...")
            server.listener_sock.close()
            server.running = False
            running = False
        else: 
            print("Comando desconhecido")
except KeyboardInterrupt:
    server.listener_sock.close()
    server.running = False
    running = False
    print("Finalizando stream...")

print("Streaming finalizado!")
