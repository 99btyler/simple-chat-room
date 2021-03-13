import tkinter as tk
from tkinter import ttk

from chat.server import ScreenHost
from chat.client import ScreenJoin

class Launcher():

    def __init__(self):

        # Tkinter root
        self.root = tk.Tk()
        self.root.title("launcher")
        self.root.resizable(False, False)

        # Tkinter frame
        self.frame = ttk.Frame(self.root)
        self.frame.grid()

        # Tkinter widgets
        self.button_host = ttk.Button(self.frame, text="Host", command=lambda: self.launch("host"))
        self.button_host["padding"] = 50
        self.button_host.grid(column=0, row=0)

        self.button_join = ttk.Button(self.frame, text="Join", command=lambda: self.launch("join"))
        self.button_join["padding"] = 50
        self.button_join.grid(column=0, row=1)

        # Tkinter mainloop
        self.root.mainloop()
    
    def launch(self, type):
        if type == "host":
            ScreenHost(type)
        elif type == "join":
            ScreenJoin(type)


Launcher()