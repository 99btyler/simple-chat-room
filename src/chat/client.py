import socket
import tkinter as tk


class Client():

    def __init__(self):
        self.toplevel = None
        self.socket = None
    
    def launch(self):

        # toplevel
        if not self.toplevel == None:
            return
        
        self.toplevel = tk.Toplevel()
        self.toplevel.title("client")
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

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def handle_close(self):
        self.socket.close()
        self.socket = None
        self.toplevel.destroy()
        self.toplevel = None

