import tkinter as tk
from tkinter import ttk


class ScreenHost():

    def __init__(self):
        self.toplevel = tk.Toplevel()
        self.toplevel.title("host")
        self.toplevel.resizable(False, False)

