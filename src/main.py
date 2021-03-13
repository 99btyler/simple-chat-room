import tkinter as tk
from tkinter import ttk


class Launcher():

    def __init__(self):

        # Tkinter root
        self.root = tk.Tk()
        self.root.title("")
        self.root.resizable(False, False)

        # Tkinter frame
        self.frame = ttk.Frame(self.root)
        self.frame.grid()

        # Tkinter widgets
        self.button_join = ttk.Button(self.frame, text="Join")
        self.button_join["padding"] = 50
        self.button_join.grid(column=0, row=0)

        self.button_host = ttk.Button(self.frame, text="Host")
        self.button_host["padding"] = 50
        self.button_host.grid(column=0, row=1)

        # Tkinter mainloop
        self.root.mainloop()


Launcher()