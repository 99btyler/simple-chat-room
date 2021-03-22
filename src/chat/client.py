import socket
import threading
import tkinter as tk


class Client():

    def __init__(self):
        
        self.print_tag = "[CLIENT]"

        self.toplevel = None
        self.socket = None
    
    def launch(self):

        # toplevel
        self.toplevel = tk.Toplevel()
        self.toplevel.title("client")
        self.toplevel.resizable(False, False)
        self.toplevel.protocol("WM_DELETE_WINDOW", self.__handle_close)
        print(f"{self.print_tag}: Client's toplevel launched!")

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

        self.button_connect = tk.Button(self.toplevel, text="Connect", command=self.__connect)
        self.button_connect.grid()

        # socket
        self.format = "utf-8"
        self.header = 64
        self.alert_error = "!ERROR"

        self.host = None
        self.port = None
        self.address = None
    
    def __connect(self):

        # socket continued
        if not self.socket == None:
            return
        
        self.host = self.stringvar_host.get() # 000.000.000.000
        if len(self.host.split(".")) < 4:
            return
        
        self.port = int(self.stringvar_port.get()) # range is 1024 to 65535
        if self.port < 1024 or self.port > 65535:
            return
        
        self.address = (self.host, self.port)

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.connect(self.address)
            print(f"{self.print_tag}: Client's socket connected to {self.address}!")
            threading.Thread(target=self.__handle_connection).start()
        except Exception as e:
            print(f"{self.print_tag}: {e}")
            print(f"{self.print_tag}: Client's socket couldn't connect to {self.address}")
            self.socket = None
            print(f"{self.print_tag}: Client's socket set to None")
            return
        
        # more toplevel widgets
        self.widgets_to_destroy = [self.label_host, self.entry_host, self.label_port, self.entry_port, self.button_connect]
        for widget_to_destroy in self.widgets_to_destroy:
            widget_to_destroy.destroy()
        
        self.text_messages = tk.Text(self.toplevel, state=tk.DISABLED)
        self.text_messages.grid()

        self.stringvar_input = tk.StringVar()
        self.entry_input = tk.Entry(self.toplevel, textvariable=self.stringvar_input)
        self.entry_input.grid()

        self.button_send = tk.Button(self.toplevel, text="Send", command=lambda:self.__send_message(self.stringvar_input.get()))
        self.button_send.grid()
    
    def __handle_connection(self):
        while True:
            try:
                header_data = self.socket.recv(self.header).decode(self.format) # waits here until the client receives a message
                header_data_length = int(header_data)
                message = self.socket.recv(header_data_length).decode(self.format)
                if message == self.alert_error:
                    print(f"{self.print_tag}: OMG! AN ERROR FROM SERVER! SHUT IT DOWN!")
                    self.__handle_close()
                print(f"{self.print_tag}: Client received message from server")
                self.text_messages.configure(state=tk.NORMAL)
                self.text_messages.insert(tk.END, message)
                self.text_messages.configure(state=tk.DISABLED)
            except Exception as e:
                print(f"{self.print_tag}: {e}")
                break
    
    def __send_message(self, message):
        data = message.encode(self.format)
        header_data = str(len(data)).encode(self.format)
        header_data += (b" " * (self.header - len(header_data)))
        self.socket.send(header_data)
        self.socket.send(data)
        self.entry_input.delete(0, tk.END)
    
    def __handle_close(self):
        if not self.socket == None:
            self.socket.close()
            self.socket = None
            print(f"{self.print_tag}: Client's socket closed and set to None")
        self.toplevel.destroy()
        self.toplevel = None
        print(f"{self.print_tag}: Client's toplevel destroyed and set to None")