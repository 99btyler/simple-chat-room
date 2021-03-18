import socket
import threading
import tkinter as tk


class Client():

    def __init__(self):
        
        self.PRINT_TAG = "[CLIENT]"

        self.toplevel = None
        self.socket = None
    
    def launch(self):

        # toplevel
        self.toplevel = tk.Toplevel()
        self.toplevel.title("client")
        self.toplevel.resizable(False, False)
        self.toplevel.protocol("WM_DELETE_WINDOW", self.handle_close)
        print(f"{self.PRINT_TAG}: Client's toplevel launched!")

        # toplevel widgets
        self.label_host = tk.Label(self.toplevel, text="Host:")
        self.label_host.grid(row=0, column=0)

        self.stringvar_host = tk.StringVar()
        self.entry_host = tk.Entry(self.toplevel, textvariable=self.stringvar_host)
        self.entry_host.grid(row=0, column=1)

        self.label_port = tk.Label(self.toplevel, text="Port:")
        self.label_port.grid(row=1, column=0)

        self.stringvar_port = tk.StringVar()
        self.entry_port = tk.Entry(self.toplevel, textvariable=self.stringvar_port)
        self.entry_port.grid(row=1, column=1)

        self.button_connect = tk.Button(self.toplevel, text="Connect", command=self.connect)
        self.button_connect.grid()

        # socket
        self.FORMAT = "utf-8"
        self.HEADER = 64
        self.ALERT_ERROR = "!ERROR"

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
            print(f"{self.PRINT_TAG}: Client's socket connected to {self.ADDRESS}!")
            threading.Thread(target=self.handle_connection).start()
        except Exception as e:
            print(f"{self.PRINT_TAG}: {e}")
            print(f"{self.PRINT_TAG}: Client's socket couldn't connect to {self.ADDRESS}")
            self.socket = None
            print(f"{self.PRINT_TAG}: Client's socket set to None")
            return
        
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
    
    def handle_connection(self):
        while True:
            try:
                header_data = self.socket.recv(self.HEADER).decode(self.FORMAT) # waits here until the client receives a message
                header_data_length = int(header_data)
                message = self.socket.recv(header_data_length).decode(self.FORMAT)
                if message == self.ALERT_ERROR:
                    print(f"{self.PRINT_TAG}: OMG! AN ERROR FROM SERVER! SHUT IT DOWN!")
                    self.handle_close()
                print(f"{self.PRINT_TAG}: Client received message from server")
                self.text_messages.insert(tk.END, message)
            except Exception as e:
                print(f"{self.PRINT_TAG}: {e}")
                break
    
    def send_message(self, message):
        data = message.encode(self.FORMAT)
        header_data = str(len(data)).encode(self.FORMAT)
        header_data += (b" " * (self.HEADER - len(header_data)))
        self.socket.send(header_data)
        self.socket.send(data)
    
    def handle_close(self):
        if not self.socket == None:
            self.socket.close()
            self.socket = None
            print(f"{self.PRINT_TAG}: Client's socket closed and set to None")
        self.toplevel.destroy()
        self.toplevel = None
        print(f"{self.PRINT_TAG}: Client's toplevel destroyed and set to None")