import tkinter as tk
from tkinter import ttk

from chat.client import Client
from chat.server import Server


class Launcher():

    def __init__(self):

        self.client = Client()
        self.server = Server()
        
        # Tkinter root
        self.root = tk.Tk()
        self.root.title("launcher")
        self.root.resizable(False, False)
        self.root.protocol("WM_DELETE_WINDOW", self.handle_close)

        # Tkinter frame
        self.frame = ttk.Frame(self.root)
        self.frame.grid()

        # Tkinter widgets
        self.button_launchclient = ttk.Button(self.frame, text="Client", command=lambda:self.launch(self.client))
        self.button_launchclient["padding"] = 50
        self.button_launchclient.grid()

        self.button_launchserver = ttk.Button(self.frame, text="Server", command=lambda:self.launch(self.server))
        self.button_launchserver["padding"] = 50
        self.button_launchserver.grid()

        # Tkinter mainloop
        self.root.mainloop()
    
    def launch(self, thing):
        thing.launch()
    
    def handle_close(self):

        if not self.server.socket == None:
            self.server.socket.close()
            self.server.socket = None
        if not self.server.toplevel == None:
            self.server.toplevel.destroy()
            self.server.toplevel = None

        self.root.destroy()


Launcher()