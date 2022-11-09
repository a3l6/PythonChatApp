import socket
import threading
import os
import datetime

import tkinter
import tkinter.scrolledtext
import tkinter.simpledialog
import tkinter.messagebox

HEADER = 64
PORT = 5000
SERVER = "169.254.170.125" #"140.238.138.95"
ADDR = (SERVER, PORT)
FORMAT = "utf-8"


class Client:
    def __init__ (self, host, port):
        try:
            # Establish connection
            self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.conn.connect((host, port))

            self.run = True

            # Draw new tkinter window
            # Hide extra window created
            window = tkinter.Tk()
            window.withdraw()

            self.name = tkinter.simpledialog.askstring("Nickname", "Please choose a name", parent=window)
            self.send(self.name)
            
            self.BG = "SKyBlue4"

            # Start multithreaded processes
            self.GUIthread = threading.Thread(target=self.gui)
            self.RECEIVEthread = threading.Thread(target=self.receiver)
            
            self.GUIthread.start()
            self.RECEIVEthread.start()
        except ConnectionRefusedError as e:
            directory = os.getcwd()
            date = datetime.date.today()
            win = tkinter.Tk()
            win.withdraw()
            tkinter.messagebox.showerror("Error Occured", f"Could not connect to server, ensure server is started!\n\nLog File Created at {directory}\log-{date}!", master=win)
            with open(f"log-{date}.txt", "w+") as f:
                f.write(f"{str(e)}\n\nIs the server started?")
            

    def gui(self):
        self.win = tkinter.Tk()
        self.win.configure(bg=self.BG)


        self.chat_label = tkinter.Label(self.win, text="Anonymous Chat Room", bg=self.BG)
        self.chat_label.config(font=("Arial", 12))
        self.chat_label.pack(padx=20, pady=5)


        self.chat_area = tkinter.scrolledtext.ScrolledText(self.win)
        self.chat_area.config(state="normal")
        self.chat_area.insert("end", f"Welcome  to the chat room, {self.name}!\n")
        self.chat_area.yview("end")
        self.chat_area.pack(padx=20, pady=5)
        self.chat_area.config(state="disabled")

        self.message_area = tkinter.Text(self.win, height=3)
        self.message_area.pack(padx=20, pady=5)

        self.send_button = tkinter.Button(self.win, text="Send", command=self.sendMessage)
        self.send_button.config(font=("Arial", 12))
        self.send_button.pack(padx=20, pady=5)


        self.win.protocol("WM_DELETE_WINDOW", self.stop)

        self.win.mainloop()


    def stop(self):
        self.run = False
        self.win.destroy()
        self.disconnect()

    def sendMessage(self):
        try:
            if self.message_area.get('1.0', 'end') != "\n":
                msg = f"{self.name}: {self.message_area.get('1.0', 'end')}"
                self.send(msg)
                self.message_area.delete("1.0", "end")
        except ConnectionResetError as e:
            tkinter.messagebox.showerror("Connection Reset", e)

    def receiver(self):
        while self.run:
            try:
                message = self.conn.recv(1024)
                self.chat_area.config(state="normal")
                self.chat_area.insert("end", message)
                self.chat_area.yview("end")
                self.chat_area.config(state="disabled")
            except ConnectionAbortedError as e:
                tkinter.messagebox.showerror("Conection aborted", e)
                break
            except:
                break

    def send(self, msg):
        message = msg.encode(FORMAT)    
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b" " * (HEADER - len(send_length))
        self.conn.send(send_length)
        #print(client.recv(1))
        self.conn.send(message)


    def disconnect(self):
        message = "!DISCONNECT".encode(FORMAT)    
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b" " * (HEADER - len(send_length))
        self.conn.send(send_length)
        self.conn.send(message)
        self.conn.send(self.name.encode(FORMAT))
        self.conn.close()




client = Client(SERVER, PORT)


