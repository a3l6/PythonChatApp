import socket
import tkinter
from tkinter import simpledialog

HEADER = 64
PORT = 5050
SERVER = "169.254.170.125"
ADDR = (SERVER, PORT)
FORMAT = "utf-8"


class Client:
    def __init__ (self, host, port):
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect(ADDR)


        self.root = tkinter.Tk()
        

        self.name = simpledialog.askstring("Nickname", "")
        self.send(self.name)
        self.send("!DISCONNECT")
        

        label = tkinter.Label(self.root, text=self.name)
        label.pack()

        self.root.mainloop()
        

    def send(self, msg):
        message = msg.encode(FORMAT)    
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b" " * (HEADER - len(send_length))
        self.conn.send(send_length)
        #print(client.recv(1))
        self.conn.send(message)



client = Client(SERVER, PORT)
