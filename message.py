import sys
import utils
import pickle

class Message():
    def __init__(self, message_id, message_type, payload):
        self.id = message_id
        self.payload = payload
        self.message_type = message_type

    def pack(self):
        return pickle.dumps(self)
    
    @staticmethod
    def unpack(message_string):
        return pickle.loads(message_string)

    def __str__(self):
        rep = "[Mensagem] "
        rep += "id: " + str(self.id) + " | type: "+ str(self.message_type) +" | payload: " + str(self.payload) + "\n"
        return rep