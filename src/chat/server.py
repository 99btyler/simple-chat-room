import tkinter as tk
from tkinter import ttk


class ScreenHost():

    def __init__(self, title):
        self.toplevel = tk.Toplevel()
        self.toplevel.title(title)
        self.toplevel.resizable(False, False)

