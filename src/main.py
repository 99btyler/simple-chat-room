import tkinter as tk
from tkinter import ttk

from chat.server import Hoster
from chat.client import Joiner

class Launcher():

    def __init__(self):

        self.launched_host = False

        # Tkinter root
        self.root = tk.Tk()
        self.root.title("launcher")
        self.root.resizable(False, False)

        # Tkinter frame
        self.frame = ttk.Frame(self.root)
        self.frame.grid()

        # Tkinter widgets
        self.button_host = ttk.Button(self.frame, text="Host", command=lambda: self.handle_launch("host"))
        self.button_host["padding"] = 50
        self.button_host.grid(column=0, row=0)

        self.button_join = ttk.Button(self.frame, text="Join", command=lambda: self.handle_launch("join"))
        self.button_join["padding"] = 50
        self.button_join.grid(column=0, row=1)

        # Tkinter mainloop
        self.root.mainloop()
    
    def handle_launch(self, type):
        if type == "host" and self.launched_host:
            return
        self.launch(type)
    
    def launch(self, type):

        toplevel = tk.Toplevel()
        toplevel.title(type)
        toplevel.resizable(False, False)

        if type == "host":
            Hoster(toplevel)
            self.launched_host = True
        elif type == "join":
            Joiner(toplevel)


Launcher()