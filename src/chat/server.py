import socket
import threading
import tkinter as tk
from tkinter import ttk


class Hoster():

    def __init__(self, toplevel):

        self.HOST = socket.gethostbyname("localhost")
        self.PORT = 5050
        self.ADDRESS = (self.HOST, self.PORT)

        self.HEADER = 64
        self.FORMAT = "utf-8"

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.server.bind(self.ADDRESS)
        except:
            print(f"{self.ADDRESS} is already being used")
            return

        # Tkinter widgets
        self.label_ipv4 = tk.Label(toplevel, text=self.HOST)
        self.label_ipv4.grid()

        self.button_start = tk.Button(toplevel, text="Start")
        self.button_start.grid()

        self.button_stop = tk.Button(toplevel, text="Stop")
        self.button_stop.grid()
    
    def start(self):
        self.server.listen()
        print(f"{self.ADDRESS} is now listening")
        while True:
            connection, address = self.server.accept() # waits until a client connects
            threading.Thread(target=self.handle_client, args=(connection, address)).start()
    
    def handle_client(self, connection, address):
        print(f"{self.ADDRESS}: {address} connected")
        connected = True
        while connected:
            data = connection.recv(HEADER).decode(FORMAT) # waits until the client sends message
            if data:
                message_length = int(data)
                message = connection.recv(message_length).decode(FORMAT)
                print(f"{self.ADDRESS}: {address} sent \"{message}\"")
        connection.close()

