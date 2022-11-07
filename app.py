import tkinter
import tkinter.scrolledtext

BG = "lightgrey"


def write():
    pass

def stop():
    pass

win = tkinter.Tk()
win.configure(bg=BG)


chat_label = tkinter.Label(win, text="Anonymous Chat Room", bg=BG)
chat_label.config(font=("Arial", 12))
chat_label.pack(padx=20, pady=5)


chat_area = tkinter.scrolledtext.ScrolledText(win)
chat_area.pack(padx=20, pady=5)
chat_area.config(state="disabled")

message_area = tkinter.Text(win, height=3)
message_area.pack(padx=20, pady=5)

send_button = tkinter.Button(win, text="Send", command=write)
send_button.config(font=("Arial", 12))
send_button.pack(padx=20, pady=5)


win.protocol("WM_DELETE_WINDOW", stop)

win.mainloop()


