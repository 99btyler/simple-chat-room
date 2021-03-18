import socket
import threading
import tkinter as tk


class Server():

    def __init__(self):

        self.PRINT_TAG = "[SERVER]"

        self.toplevel = None
        self.socket = None

        self.client_sockets = []
    
    def launch(self):

        # toplevel
        self.toplevel = tk.Toplevel()
        self.toplevel.title("server")
        self.toplevel.resizable(False, False)
        self.toplevel.protocol("WM_DELETE_WINDOW", self.handle_close)
        print(f"{self.PRINT_TAG}: Server's toplevel launched!")

        # socket
        self.HEADER = 64
        self.FORMAT = "utf-8"
        self.ALERT_ERROR = "!ERROR"

        self.HOST = socket.gethostbyname(socket.gethostname())
        self.PORT = 5050
        self.ADDRESS = (self.HOST, self.PORT)

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.bind(self.ADDRESS)
            print(f"{self.PRINT_TAG}: Server's socket binded to {self.ADDRESS}!")
            threading.Thread(target=self.listen_for_clients).start()
        except Exception as e:
            print(e)
        
        # toplevel widgets
        label_address = tk.Label(self.toplevel, text=f"{self.HOST} • {self.PORT}")
        label_address.grid()
    
    def listen_for_clients(self):
        self.socket.listen()
        print(f"{self.PRINT_TAG}: Server's socket is now listening...")
        while not self.socket == None:
            try:
                client_socket, client_address = self.socket.accept() # waits here until a client connects
                threading.Thread(target=self.handle_client, args=(client_socket, client_address)).start()
            except Exception as e:
                print(f"{self.PRINT_TAG}: {e}")
                print(f"{self.PRINT_TAG}: Server is alerting all client_sockets of error...")
                self.alert_client_sockets(self.ALERT_ERROR)
    
    def handle_client(self, client_socket, client_address):
        print(f"{self.PRINT_TAG}: Server accepted {client_address}!")
        self.client_sockets.append(client_socket)
        while True:
            header_data = client_socket.recv(self.HEADER).decode(self.FORMAT) # waits here until the client sends a message
            if header_data:
                header_data_length = int(header_data)
                message = client_socket.recv(header_data_length).decode(self.FORMAT)
                print(f"{self.PRINT_TAG}: Server received message from {client_address}")
                print(f"{self.PRINT_TAG}: Server is alerting all client_sockets of message...")
                self.alert_client_sockets(f"{client_address}: {message}\n")
            else:
                print(f"{self.PRINT_TAG}: OMG! NO DATA FROM {client_address}")
                client_socket.close()
                print(f"{self.PRINT_TAG}: Server closed client_socket of {client_address}")
                break
    
    def alert_client_sockets(self, message):
        for client_socket in self.client_sockets:
            data = message.encode(self.FORMAT)
            header_data = str(len(data)).encode(self.FORMAT)
            header_data += (b" " * (self.HEADER - len(header_data)))
            client_socket.send(header_data)
            client_socket.send(data)
    
    def handle_close(self):
        self.socket.close()
        self.socket = None
        print(f"{self.PRINT_TAG}: Server's socket closed and set to None")
        self.toplevel.destroy()
        self.toplevel = None
        print(f"{self.PRINT_TAG}: Server's toplevel destroyed and set to None")