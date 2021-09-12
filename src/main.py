import tkinter as tk
from tkinter import ttk

from chat.client import Client
from chat.server import Server


class Launcher():

    def __init__(self):

        self.client = Client()
        self.server = Server()

        self.print_tag = "[LAUNCHER]"
        
        # Tkinter root
        self.root = tk.Tk()
        self.root.title("launcher")
        self.root.resizable(False, False)
        self.root.protocol("WM_DELETE_WINDOW", self.__handle_close)

        # Tkinter frame
        self.frame = ttk.Frame(self.root)
        self.frame.grid()

        # Tkinter widgets
        self.button_launchclient = ttk.Button(self.frame, text="Client", padding=50, command=lambda:self.client.launch())
        self.button_launchclient.grid()

        self.button_launchserver = ttk.Button(self.frame, text="Server", padding=50, command=lambda:self.server.launch())
        self.button_launchserver.grid()

        # Tkinter mainloop
        self.root.mainloop()
    
    def __handle_close(self):
        if not self.server.socket == None:
            self.server.socket.close()
            self.server.socket = None
            print(f"{self.print_tag}: Server's socket closed and set to None")
        self.root.destroy()


if __name__ == "__main__":
    Launcher()

