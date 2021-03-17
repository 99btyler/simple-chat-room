import socket
import threading
import tkinter as tk


class Server():

    def __init__(self):

        self.toplevel = None
        self.socket = None

        self.client_sockets = []
    
    def launch(self):

        # toplevel
        if not self.toplevel == None:
            return
        
        self.toplevel = tk.Toplevel()
        self.toplevel.title("server")
        self.toplevel.resizable(False, False)
        self.toplevel.protocol("WM_DELETE_WINDOW", self.handle_close)

        # socket
        if not self.socket == None:
            return
        
        self.HEADER = 64
        self.FORMAT = "utf-8"
        self.COMMAND_DISCONNECT = "!disconnect"
        
        self.HOST = socket.gethostbyname("localhost")
        self.PORT = 5050
        self.ADDRESS = (self.HOST, self.PORT)

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.bind(self.ADDRESS)
            print(f"{self.ADDRESS} was available!")
            threading.Thread(target=self.listen_for_clients).start()
        except Exception as e:
            print(e)

        # toplevel widgets
        label_address = tk.Label(self.toplevel, text=f"{self.HOST} • {self.PORT}")
        label_address.grid()
        
    def listen_for_clients(self):
        self.socket.listen()
        print(f"{self.ADDRESS} is now listening...")
        while True:
            client_socket, client_address = self.socket.accept() # waits until a client connects
            threading.Thread(target=self.handle_client, args=(client_socket, client_address)).start()
    
    def handle_client(self, client_socket, client_address):
        print(f"{self.ADDRESS}: {client_address} connected")
        self.client_sockets.append(client_socket)
        while True:
            data = client_socket.recv(self.HEADER).decode(self.FORMAT) # waits until the client sends message
            message_length = int(data)
            message = client_socket.recv(message_length).decode(self.FORMAT)
            if message == self.COMMAND_DISCONNECT:
                break
            else:
                self.update_client_sockets(f"{client_address}: {message}")
        client_socket.close()
        print(f"{self.ADDRESS}: {client_address} disconnected")
    
    def update_client_sockets(self, message):
        for client_socket in self.client_sockets:
            data = message.encode(self.FORMAT)
            pre_data = str(len(data)).encode(self.FORMAT)
            pre_data += (b" " * (self.HEADER - len(pre_data)))
            client_socket.send(pre_data)
            client_socket.send(data)
    
    def handle_close(self):

        self.socket.close()
        self.socket = None

        self.toplevel.destroy()
        self.toplevel = None

