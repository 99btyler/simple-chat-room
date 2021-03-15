import socket
import threading
import tkinter as tk


class Server():

    def __init__(self):
        self.toplevel = None
        self.socket = None
    
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
        
        self.HOST = socket.gethostbyname("localhost")
        self.PORT = 5050
        self.ADDRESS = (self.HOST, self.PORT)

        self.HEADER = 64
        self.FORMAT = "utf-8"
        self.COMMAND_DISCONNECT = "!disconnect"

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.bind(self.ADDRESS)
            print(f"{self.ADDRESS} was available!")
            print(f"{self.ADDRESS} is ready to listen")
        except Exception as e:
            print(e)
        
        threading.Thread(target=self.listen_for_clients).start()

        # toplevel widgets
        label_address = tk.Label(self.toplevel, text=f"{self.HOST} • {self.PORT}")
        label_address.grid()
        
    def listen_for_clients(self):
        self.socket.listen()
        print(f"{self.ADDRESS} is now listening...")
        while True:
            connection, address = self.socket.accept() # waits until a client connects
            threading.Thread(target=self.handle_client, args=(connection, address)).start()
    
    def handle_client(self, connection, address):
        print(f"{self.ADDRESS}: {address} connected")
        while True:
            data = connection.recv(self.HEADER).decode(self.FORMAT) # waits until the client sends message
            if data:
                message_length = int(data)
                message = connection.recv(message_length).decode(self.FORMAT)
                if message == self.COMMAND_DISCONNECT:
                    print(f"{self.ADDRESS}: {address} disconnected")
                    break
                print(f"{self.ADDRESS}: \"{message}\" sent by {address}")
        connection.close()
    
    def handle_close(self):

        self.socket.close()
        self.socket = None

        self.toplevel.destroy()
        self.toplevel = None

