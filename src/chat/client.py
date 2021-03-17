import socket
import threading
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

        self.button_connect = tk.Button(self.toplevel, text="Connect", command=self.connect)
        self.button_connect.grid()

        # socket
        self.FORMAT = "utf-8"
        self.HEADER = 64
        self.COMMAND_DISCONNECT = "!disconnect"

        self.HOST = None
        self.PORT = None
        self.ADDRESS = None
    
    def connect(self):
        
        # socket continued
        if not self.socket == None:
            return

        self.HOST = self.stringvar_host.get() # 000.000.000.000
        if len(self.HOST.split(".")) < 4:
            return

        self.PORT = int(self.stringvar_port.get()) # range is 1024 to 65535
        if self.PORT < 1024 or self.PORT > 65535:
            return

        self.ADDRESS = (self.HOST, self.PORT)

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.connect(self.ADDRESS)
        except Exception as e:
            print(e)
            self.socket = None
            return
        
        threading.Thread(target=self.handle_messages).start()
        
        # more toplevel widgets
        self.widgets_to_destroy = [self.label_host, self.entry_host, self.label_port, self.entry_port, self.button_connect]
        for widget_to_destroy in self.widgets_to_destroy:
            widget_to_destroy.destroy()
        
        self.text_messages = tk.Text(self.toplevel)
        self.text_messages.grid()

        self.stringvar_input = tk.StringVar()
        self.entry_input = tk.Entry(self.toplevel, textvariable=self.stringvar_input)
        self.entry_input.grid()

        self.button_send = tk.Button(self.toplevel, text="Send", command=lambda:self.send_message(self.stringvar_input.get()))
        self.button_send.grid()
    
    def handle_messages(self):
        while not self.socket == None:
            data = self.socket.recv(self.HEADER).decode(self.FORMAT)
            message_length = int(data)
            message = self.socket.recv(message_length).decode(self.FORMAT)
            self.text_messages.insert(tk.END, f"{message}\n")
    
    def send_message(self, message):
        data = message.encode(self.FORMAT)
        pre_data = str(len(data)).encode(self.FORMAT)
        pre_data += (b" " * (self.HEADER - len(pre_data)))
        self.socket.send(pre_data)
        self.socket.send(data)
    
    def handle_close(self):

        if not self.socket == None:
            self.send_message(self.COMMAND_DISCONNECT)
            self.socket.close()
            self.socket = None
        
        self.toplevel.destroy()
        self.toplevel = None

