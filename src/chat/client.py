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

        # toplevel widgets
        self.label_host = tk.Label(self.toplevel, text="Host:")
        self.label_host.grid(column=0, row=0)

        self.stringvar_host = tk.StringVar()
        self.entry_host = tk.Entry(self.toplevel, textvariable=self.stringvar_host)
        self.entry_host.grid(column=1, row=0)

        self.label_port = tk.Label(self.toplevel, text="Port:")
        self.label_port.grid(column=0, row=1)

        self.stringvar_port = tk.StringVar()
        self.entry_port = tk.Entry(self.toplevel, textvariable=self.stringvar_port)
        self.entry_port.grid(column=1, row=1)

        self.button_connect = tk.Button(self.toplevel, text="Connect")
        self.button_connect.grid()

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

