import socket
import threading
import tkinter as tk


class Server():

    def __init__(self):

        self.toplevel = None
        self.socket = None

        self.print_tag = "[SERVER]"

        self.client_sockets = []
    
    def launch(self):

        if not (self.toplevel == None and self.socket == None):
            print(f"{self.print_tag}: FAIL. Server is already launched")
            return

        # toplevel
        self.toplevel = tk.Toplevel()
        self.toplevel.title("server")
        self.toplevel.resizable(False, False)
        self.toplevel.protocol("WM_DELETE_WINDOW", self.__handle_close)
        print(f"{self.print_tag}: Server's toplevel launched!")

        # socket
        self.header = 64
        self.format = "utf-8"
        self.alert_error = "!ERROR"

        self.host = socket.gethostbyname(socket.gethostname())
        self.port = 5050
        self.address = (self.host, self.port)

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.bind(self.address)
            print(f"{self.print_tag}: Server's socket binded to {self.address}!")
            threading.Thread(target=self.__listen_for_clients).start()
        except Exception as e:
            print(e)
        
        # toplevel widgets
        label_address = tk.Label(self.toplevel, text=f"{self.host} • {self.port}")
        label_address.grid()
    
    def __listen_for_clients(self):
        self.socket.listen()
        print(f"{self.print_tag}: Server's socket is now listening...")
        while not self.socket == None:
            try:
                client_socket, client_address = self.socket.accept() # waits here until a client connects
                threading.Thread(target=self.__handle_client, args=(client_socket, client_address)).start()
            except Exception as e:
                print(f"{self.print_tag}: {e}")
                print(f"{self.print_tag}: Server is alerting all client_sockets of error...")
                self.__alert_client_sockets(self.alert_error)
    
    def __handle_client(self, client_socket, client_address):
        print(f"{self.print_tag}: Server accepted {client_address}!")
        self.client_sockets.append(client_socket)
        while True:
            header_data = client_socket.recv(self.header).decode(self.format) # waits here until the client sends a message
            if header_data:
                header_data_length = int(header_data)
                message = client_socket.recv(header_data_length).decode(self.format)
                print(f"{self.print_tag}: Server received message from {client_address}")
                print(f"{self.print_tag}: Server is alerting all client_sockets of message...")
                self.__alert_client_sockets(f"{client_address}: {message}\n")
            else:
                print(f"{self.print_tag}: OMG! NO DATA FROM {client_address}")
                client_socket.close()
                self.client_sockets.remove(client_socket)
                print(f"{self.print_tag}: Server closed and removed client_socket of {client_address}")
                break
    
    def __alert_client_sockets(self, message):
        for client_socket in self.client_sockets:
            data = message.encode(self.format)
            header_data = str(len(data)).encode(self.format)
            header_data += (b" " * (self.header - len(header_data)))
            client_socket.send(header_data)
            client_socket.send(data)
    
    def __handle_close(self):
        self.socket.close()
        self.socket = None
        print(f"{self.print_tag}: Server's socket closed and set to None")
        self.toplevel.destroy()
        self.toplevel = None
        print(f"{self.print_tag}: Server's toplevel destroyed and set to None")