import socket
import threading

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


clients = []
nicknames = []

def broadcast(message: str):
    for client in clients:
        client.send(message.encode(FORMAT))

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            break
"""
def receive():
    connected = True
    while connected:
        client, address = server.accept()
        print(f"Connected with {str(address)}")


        clients.send("NICK".encode(FORMAT))
        nickname = client.recv(1024)
        nicknames.append(nickname)

        clients.append(client)

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


"""












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
                    nicknames.pop(nickname.index(conn.recv(1024).decode(FORMAT)))
                    clients.pop(clients.index(conn))
                    break
            if nickname == None:
                nickname = msg
                nicknames.append(nickname)
                broadcast(f"{nickname} has joined the chat!\n")
                clients.append(conn)
            else:
                broadcast(msg)
            #thread = threading.Thread(target=handle, args=(conn,))
            #thread.start()


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