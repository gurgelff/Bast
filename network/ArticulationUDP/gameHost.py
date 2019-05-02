
import _thread as thread
import socket
import time
import pickle
clients = {}
clientInfo = {}
connections = {}

def startServer(nPort):

    host = socket.gethostbyname(socket.gethostname())
    port = nPort

    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    serverSocket.bind((host, port))
    serverSocket.setblocking(0)
    print(("Server bound to " + str(host) + " on port " + str(port)))
    return serverSocket

def runServer(server):
    recv(server)

def recv(server):
    end = time.time()
    start = time.time()
    ping = 0
    r = ""
    global clients
    server.settimeout(0)
    while(True):
        for i in range(0, len(clients) + 1):
            try:
                (r, address) = server.recvfrom(4096)
                if r:
                    print((str(r)))
                    print((str(address)))
                #r = pickle.loads(r)
                if address not in clients:
                    addClient(address)

                clients[address] = r
                ping = round((time.time()-start)*1000,3)
                start = time.time()
                clientInfo[address]['lastPing'] = time.time()
                clientInfo[address]['ping'] = ping
                clientInfo[address]['timeout'] = 0.0
            except:
                pass
        for c in clients:
            client = clientInfo[c]
            client['timeout'] = round(float(time.time()-client['lastPing'])*1000,3)
            if client['timeout'] > 5000:
                print("client has presumably lost connection")
                disconnectClient(c)
                break
    print("loop has been broken")
def send(clientSocket):
    global clients
    while(True):
        time.sleep(.05)
        for address in clients:
            client = clients[address]
            clientSocket.sendto(pickle.dumps(client),address)



def addClient(address):

    print((str("adding client")))
    clients[address] = {}
    clientInfo[address] = {}
    clientInfo[address]['timeout'] = 0.0
    clientInfo[address]['lastPing'] = time.time()
    print(str("clients:")+str(clients))

def disconnectClient(address):
    print(str("disconnecting ")+str(address))
    del clients[address]
    print("client removed")

go = False
print("What port should the server use? (Enter for default port of 4445)")
if go is False:
    port = input("Port: ")
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


#thread.start_new_thread( print, ("Thread-2","Hello") )
try:
    serverSocket = startServer(port)

    thread.start_new_thread(recv, (serverSocket,))
    thread.start_new_thread(send, (serverSocket,))
    print("Server started")
except Exception as e:
    print ((str(e)))

killServer = eval(input("stop server? (y/n)"))
#
#thread.start_new_thread( send), (serverSocket) )


