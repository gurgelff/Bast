#Autor: totter333
#Tutorial fonte: https://www.youtube.com/watch?v=A-OY1h_iPl4
#import bge
#cont = bge.logic.getCurrentController()
#owner = cont.owner
#if owner['start'] == True:

import _thread as thread
import socket
import time
#import pickle
clients = {}
clientInfo = {}
connections = {}

def startServer(nPort):

    host = socket.gethostbyname(socket.gethostname())
    port = nPort
    
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serverSocket.bind((host,port))
    #serverSocket.setblocking(0)
    serverSocket.listen(5)
    print("Server bound to "+str(host)+" on port "+str(port))
    return serverSocket

def runServer(server):
    recv(server)

def recv(server):
    end = time.time()
    start = time.time()
    ping = 0
    r = ''
    global clients
    
    #server.listen(5)
    (conn, address) = server.accept()
    while(True):
        for i in range(0,len(clients)+1):
            try:               
                
                #(r,address) = server.recvfrom(4096)  
                r = conn.recv(4096)
                #r = pickle.loads(r)
                if type(r) != type(''):
                    r = r.decode()
                    
                if r:
                    print(str(r))
                    
                if address not in clients:
                    addClient(address)

                if r == 'end' or r == 'End' or r=='END':
                    disconnectClient(address)
                    conn.shutdown(socket.SHUT_RD | socket.SHUT_WR)
                    conn.close()      
                    pass              
                    
                clients[address] = r
                ping = round((time.time()-start)*1000,3)
                start = time.time()
                clientInfo[address]['lastPing'] = time.time()
                clientInfo[address]['ping'] = ping
                clientInfo[address]['timeout'] = 0.0
                conn.send("Obrigado ".encode('utf-8'))
                thread.start_new_thread( send, (conn,) )
                print("mensagem enviada")
                #TODO: movimentation methods
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
            #clientSocket.sendto(pickle.dumps(clients),address)
            #clientSocket.sendto("Bem-Vindo!".encode('utf-8'),address)
            clientSocket.sendto(str(clients).encode('utf-8'),address)


      


def addClient(address):

    print(str("adding client"))
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
while go == False:
    port = input("Port: ")
    #port = 8080
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

    thread.start_new_thread( recv, (serverSocket,) )
    #thread.start_new_thread( send, (serverSocket,) )
    print("Server started")
except Exception as e:
    print (str(e))

killServer = input("stop server? (y/n)")
#
#thread.start_new_thread( send), (serverSocket) )
#owner['start'] = False


