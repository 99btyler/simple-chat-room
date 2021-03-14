import socket


class Joiner():

    def __init__(self):

        self.HOST = socket.gethostbyname("localhost")
        self.PORT = 5050
        self.ADDRESS = (self.HOST, self.PORT)

        self.HEADER = 64
        self.FORMAT = "utf-8"

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(self.ADDRESS)
    
    def send_message(self, message):

        data = message.encode(self.FORMAT)

        pre_data = str(len(data)).encode(self.FORMAT)
        pre_data += (b" " * (self.HEADER - len(pre_data)))
        self.client.send(pre_data)

        self.client.send(data)

