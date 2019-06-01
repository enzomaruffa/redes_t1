import sys
import utils

class Message():
    def __init__(self, payload):
        self.payload = payload

    def pack(self, payload):
        return payload.decode()
    
    def unpack(self, message):
        return message.uncode()