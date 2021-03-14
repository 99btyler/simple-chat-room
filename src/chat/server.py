import socket
import threading
import tkinter as tk
from tkinter import ttk


class ScreenHost():

    def __init__(self, title):

        self.HOST = socket.gethostbyname("localhost")
        self.PORT = 5050
        self.ADDRESS = (self.HOST, self.PORT)

        self.HEADER = 64
        self.FORMAT = "utf-8"

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.server.bind(self.ADDRESS)
        except:
            print(f"{self.ADDRESS}: this is already being used")
            return

        # Tkinter widgets
        self.toplevel = tk.Toplevel()
        self.toplevel.title(title)
        self.toplevel.resizable(False, False)

        self.label_ipv4 = tk.Label(self.toplevel, text=self.HOST)
        self.label_ipv4.grid()

        self.button_start = tk.Button(self.toplevel, text="Start")
        self.button_start.grid()

        self.button_stop = tk.Button(self.toplevel, text="Stop")
        self.button_stop.grid()
    
    def start(self):
        self.server.listen()
        print(f"{self.ADDRESS}: server is now listening")
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

