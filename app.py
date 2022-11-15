import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter.scrolledtext


class window():
    def __init__ (self):
        self.win = ttk.Window(themename="vapor")
        self.win.iconbitmap("icon.ico")

        self.chat_label = ttk.Label(self.win, text="Anonymous Chat Room")
        self.chat_label.config(font=("Arial", 12))
        self.chat_label.pack(padx=20, pady=5)


        self.chat_area = tkinter.scrolledtext.ScrolledText(self.win)
        self.chat_area.config(state="normal")
        self.chat_area.insert("end", f"Welcome  to the chat room, EMilio!\n")
        self.chat_area.yview("end")
        self.chat_area.pack(padx=20, pady=5)
        self.chat_area.config(state="disabled")

        self.message_area = ttk.Text(self.win, height=3)
        self.message_area.pack(padx=20, pady=5)

        self.send_button = ttk.Button(self.win, text="Send")
        #self.send_button.config(font=("Arial", 12))
        self.send_button.pack(padx=20, pady=5)


        #self.win.protocol("WM_DELETE_WINDOW", self.stop)

        self.win.mainloop()


window()