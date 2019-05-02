
import _thread as thread
import socket
import time
#import pickle

go = False
print("What port should the server use? (Enter for default port of 4445)")
if go is False:
    port = eval(input("Port: "))
    try:
        port = int(port)
        if port >= 1024:
            go = True
        else:
            print("Port must be greater than 1024")
    except:
        pass
    if port == "":
        port = 4445
        print("Using default port of 4445")
        go = True

host = socket.gethostbyname(socket.gethostname())

server = (host, 8080)

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
serverSocket.bind((host, port))
#serverSocket.setblocking(0)
print(("Server bound to " + str(host) + " on port " + str(port)))

def recv(serverSocket):
    while(True):
        try:
            serverSocket.sendto(b'1', server)
            (r, address) = serverSocket.recvfrom(4096)
            if r == '1' or r == b'1':
                break
            if r:
                print(("Recebido: ", str(r)))
                time.sleep(1)
        except:
            pass
    print("loop has been broken")
    serverSocket.close()

try:
    thread.start_new_thread(recv, (serverSocket,))
    killServer = eval(input("stoping server..."))
    #thread.start_new_thread( send), (serverSocket) )
except Exception as e:
    print ((str(e)))

