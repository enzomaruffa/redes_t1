import sys
import utils
import pickle

# Classe que representa uma mensagem
class Message():

    # Uma mensagem recebe um id, um tipo e um payload para ser gerada
    def __init__(self, message_id, message_type, payload):
        self.id = message_id
        self.payload = payload
        self.message_type = message_type # Os tipos de mensagem utilizados são 'sync' para sincronizar, 'data' para enviar dados e 'exit' para fechar uma conexão

    # Pack retorna uma mensagem serializada
    def pack(self):
        return pickle.dumps(self)
    
    # Unpack é um método estático que recebe uma mensagem serializada e retorna uma mensagem apropriadamente
    @staticmethod
    def unpack(message_string):
        return pickle.loads(message_string)

    # O overload do método __str__ serve para imprimir a mensagem formatada
    def __str__(self):
        rep = "[Mensagem] "
        rep += "id: " + str(self.id) + " | type: "+ str(self.message_type) +" | payload: " + str(self.payload)
        return rep