import socket
import threading
import sys
import commons
import requests
import pickle

HEADER = 64
PORT = 5000
MAINSERVER = commons.get_mainserver()

FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"


def register():
    myip = commons.getIP()
    #req = requests.get(f"{MAINSERVER}/api/addserver/{myip}").content        # Add server and get content of returned html page
    req = requests.get(f"{MAINSERVER}/api/addserver/10.110.41.121").content 
    req = req.decode("unicode_escape").encode("raw_unicode_escape")
    req = pickle.loads(req)
    if str(req) == "Added":
        print(f"Added server with addr: {myip}")
    else:
        print(req)
        exit()

def disconnect():
    myip = commons.getIP()
    req = requests.get(f"{MAINSERVER}/api/deleteserver/{myip}")
    print(req.content)      # Wont even bother to remove backslashes again
    exit()


ipaddr = sys.argv[1]
if ipaddr == "-l":
    SERVER = socket.gethostbyname(socket.gethostname())
elif ipaddr == "-h":
    SERVER = ""
elif ipaddr == "-d":
    disconnect()
else:
    print("Not valid arguement")
    exit()

register()

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
        try: 

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
        except ConnectionResetError:
            print(f"{addr} did not exit cleanly")
            conn.close()
            break

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
