import socket
import threading
import os
import datetime
import pickle
import commons
import requests

import tkinter
import tkinter.scrolledtext
import tkinter.simpledialog
import tkinter.messagebox

import ttkbootstrap as ttk
from ttkbootstrap.constants import *


HEADER = 64
PORT = 5000
SERVER = ""
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
MAINSERVER = commons.get_mainserver()

class Client:
    def __init__ (self, host, port):
        try:
            self.connectionip = host 

            self.theme = "superhero"
            #   Ask if want to connect to main server or to private server
            tempwin = tkinter.Tk()
            tempwin.withdraw() 
            

             # Establish connection
            host = tkinter.messagebox.askquestion("CONNECTION", "Would you like to connect to public server")
            
            if host == "yes":   # I won't be running mainserver
                nomainserver = tkinter.messagebox.showerror("Could not connect to mainserver", "Could not connect to mainserver!\nPlease select a hosted server")
                exit()
               
            else:
                req = requests.get(f"{MAINSERVER}/api/gethosts").content        # Don't want the rest of the object, just the content of the page

                """
                Stackoverflow explanation: 
                https://stackoverflow.com/questions/38763771/how-do-i-remove-double-back-slash-from-a-bytes-object

                My Explation:
                Either flask or requests escapes characters to avoid potential issues. I dont want these escape characters. First decode 
                bytes object req then encode it without escaping characters
                """

                req = req.decode("unicode_escape").encode("raw_unicode_escape")
                req = pickle.loads(req)
                if req == []:       # If no servers have joined network, show error
                    win = tkinter.Tk()
                    win.iconbitmap("icon.ico")
                    win.withdraw()
                    tkinter.messagebox.showerror("No Servers Online", f"No servers appear to be online and registered with the mainserver.\nPlease relaunch the application!", master=win)
                    self.stop()
                else:   # Display window to choose server
                    self.popupList(servers=req) # Blocks execution until server is chosen
            
            
            self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.conn.connect((self.connectionip, port))


          
            self.run = True

            # Draw new tkinter window
            # Hide extra window created
            window = tkinter.Tk()
            window.iconbitmap("icon.ico")
            window.withdraw()
            
            self.name = tkinter.simpledialog.askstring("Nickname", "Please choose a name", parent=window)
            self.send(self.name)
            
            # Start multithreaded processes
            #self.GUIthread = threading.Thread(target=self.gui)
            self.RECEIVEthread = threading.Thread(target=self.receiver)
            
            #self.GUIthread.start()
            self.RECEIVEthread.start()

            self.gui()

        except ConnectionRefusedError as e:
            directory = os.getcwd()
            date = datetime.date.today()
            win = tkinter.Tk()
            win.iconbitmap("icon.ico")
            win.withdraw()
            tkinter.messagebox.showerror("Error Occured", f"Could not connect to server, ensure server is started!\n\nLog File Created at {directory}\log-{date}!", master=win)
            with open(f"log-{date}.txt", "w+") as f:
                f.write(f"{str(e)}\n\nIs the server started?")

    #   Handling Connection + selection of servers that are registered with mainserver
    def connect(self, listboxvar, win):
        for i in listboxvar.curselection():
            self.connectionip = listboxvar.get(i)
        win.quit()

    def popupList(self, servers):
        win = ttk.Toplevel(title="Choose Server", resizable=(False, False))
        win.geometry("200x200")


        servers = tkinter.Variable(value=servers)

        listbox = tkinter.Listbox(win, listvariable=servers, height=6, selectmode=tkinter.EXTENDED)
        listbox.pack(side='top')

        b = ttk.Button(win, text="Okay", command=lambda: self.connect(listbox, win))
        b.pack(side='top')
        win.mainloop()



    # Main GUI using ttkbootstrap
    def gui(self):
        self.win = ttk.Window(themename=self.theme)
        self.win.iconbitmap("icon.ico")

        self.chat_label = ttk.Label(self.win, text="Anonymous Chat Room")
        self.chat_label.config(font=("Arial", 12))
        self.chat_label.pack(padx=20, pady=5)


        self.chat_area = tkinter.scrolledtext.ScrolledText(self.win)
        self.chat_area.config(state="normal")
        self.chat_area.insert("end", f"Welcome to the chat room, {self.name}!\n")
        self.chat_area.yview("end")
        self.chat_area.pack(padx=20, pady=5)
        self.chat_area.config(state="disabled")

        self.message_area = ttk.Text(self.win, height=3)
        self.message_area.pack(padx=20, pady=5)

        self.send_button = ttk.Button(self.win, text="Send", command=self.sendMessage)
        self.send_button.pack(padx=20, pady=5)


        self.win.protocol("WM_DELETE_WINDOW", self.stop)

        self.win.mainloop()



    def stop(self):
        try:
            self.run = False
            self.win.destroy()
            self.disconnect()
        except AttributeError:
            print("Client exited before joining room")
            exit()

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