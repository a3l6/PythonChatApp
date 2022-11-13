import socket
import threading
import sys
import commons

HEADER = 64
PORT = 5050
MAINSERVER = commons.get_mainserver()

FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"


def send(msg, conn):
    message = msg.encode(FORMAT)    
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b" " * (HEADER - len(send_length))
    conn.send(send_length)
    conn.send(message)

def disconnect(conn):
    message = "!DISCONNECT".encode(FORMAT)    
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b" " * (HEADER - len(send_length))
    conn.send(send_length)
    conn.send(message)
    conn.close()

def closeconn(conn):
    message = "closeconn".encode(FORMAT)    
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b" " * (HEADER - len(send_length))
    conn.send(send_length)
    conn.send(message)
    conn.close()



ipaddr = sys.argv[1]
if ipaddr == "-l":
    SERVER = socket.gethostbyname(socket.gethostname())
else:
    SERVER = ipaddr
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((SERVER, PORT))
    send(SERVER, conn=sock)
    closeconn()


ADDR = (SERVER, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


clients = []
nicknames = []

def broadcast(message: str):
    for client in clients:
        client.send(message.encode(FORMAT))

def handle_conn(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected")
    nickname = None
    connected = True
    while connected:
        

        #   Get HEADER
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
                
            msg_length = int(msg_length)

            #   Recieve message with length
            msg = conn.recv(msg_length).decode(FORMAT)

            if msg == DISCONNECT_MESSAGE:
                    connected = False
                    #   Ugly code
                    broadcast(f"{nickname} has left the chat!")
                    nicknames.pop(nicknames.index(conn.recv(1024).decode(FORMAT)))
                    clients.pop(clients.index(conn))
                    break
            if nickname == None:
                nickname = msg
                nicknames.append(nickname)
                broadcast(f"{nickname} has joined the chat!\n")
                clients.append(conn)
            else:
                broadcast(msg)


    conn.close()



def start():
    server.listen()
    print(f"[LISTENING] Server is on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_conn, args=(conn, addr))
        thread.start()

print("[STARTING] server is starting...")
start()
