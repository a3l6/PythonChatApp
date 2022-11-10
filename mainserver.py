import socket
import threading

HEADER = 64
PORT = 5000
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

clients = []
serverList = []

def handle_conn(conn, addr):
    ipaddr = None
    connected = True
    while connected:
        # Get header
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)

            #   Recieve message with length
            msg = conn.recv(msg_length).decode(FORMAT)

            if msg == DISCONNECT_MESSAGE:
                    connected = False
                    serverList.pop(serverList.index(ipaddr))
                    clients.pop(clients.index(conn))
                    break

            if ipaddr == None:
                serverList.append(msg)
                clients.append(conn)
                ipaddr = msg
            


def start():
    server.listen()
    print(f"[LISTENING] Server is on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_conn, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    start()