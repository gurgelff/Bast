#Autor: totter333
#Tutorial fonte: https://www.youtube.com/watch?v=A-OY1h_iPl4
import time
import pickle
class network:
    def __init__(self):
        import bge
        import socket
        import random
        self.mainSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.mainSocket.setblocking(0)
        self.controller = bge.logic.getCurrentController()
        self.spawner = self.controller.actuators['spawner']
        bge.network = self
        self.host = self.controller.owner['host']
        self.port = self.controller.owner['port']
        self.connection = "connected"
        self.fragment = b""
        
        #network objects
        self.gameState = {}
        self.netObjects = {}
        self.localNetObjects = {}
        self.ghostObjects = {}
        self.localGhostObjects = {}
        self.extra = {}
        self.connectedClients = {}
        
        #client identification
        self.nextID = 0
        self.clientID = str(socket.gethostbyname(socket.gethostname()))+str(random.randrange(0,100,1))
        
        #ping and time properties
        t = time.time()
        self.ping = 0
        self.maxTimeout = t+10
        self.timeout = t
        
        #message sending properties
        self.inBuffer = {}
        self.outBuffer = {}
        self.handledList = []
        self.packet = b""
        
        print("Created client:")
        print("-ID = "+str(self.clientID))
        print("-Host = "+str((self.host,self.port)))
        print("-Extra = "+str(self.extra))

    def getNextID(self):
        ID = self.nextID
        self.nextID+=1
        return ID

    def addLocalNetObject(self,netObject):
        self.localNetObjects[str(netObject.ID)] = netObject

    def addPublicNetObject(self,netObject):
        self.netObjects[str(netObject.gameObject['publicID'])] = netObject
    
    def createNetObject(self,name,publicID):
        import netObject
        print("adding "+str(name))
        self.spawner.object = name
        self.spawner.instantAddObject()
        last = self.spawner.objectLastCreated
        self.controller.owner["local"] = False
        last["local"] = False
        last['publicID'] = publicID

    def removeClient(self,clientKey):
        #for each physical object, remove
        #clean public ghost objects
        #remove client from game state
        client = self.connectedClients[clientKey]
        for ghostKey in client['ghostObjects']:
            ID = ghostKey
            if ID in self.netObjects:
                
                netObject = self.netObjects[ID]
                netObject.gameObject.endObject()
                print("Removed object "+str(ID))
            else:
                pass
                print("Missing object "+str(ID)+"!")
        self.netObjects = {}
        self.ghostObjects = {}

    def handleDisconnects(self):
        for clientKey in self.connectedClients:
            if clientKey not in self.gameState:
                print("client needs to be removed")
                self.removeClient(clientKey)
        self.extra = self.outBuffer

    def setConnectedClients(self):
        self.connectedClients = self.gameState

    def handleConnections(self):
        self.handleDisconnects()
        self.setConnectedClients()
    
    def updateNetObjects(self):
        #this function checks to make sure the dictionary
        #of actual objects is in sync with the server objects.
        #any time an object is not found in the real objects
        #dictionary, it is spawned and synced.         
        for ghostKey in self.ghostObjects:
            ghost = self.ghostObjects[ghostKey]
            if ghostKey in self.netObjects:
                self.netObjects[ghostKey].hardSync(ghost)
            else:
                print("netObjects are inconsistant "+str(ghost['n'])+str(ghostKey))
                newNetObject = self.createNetObject(ghost['n'],ghostKey)

    def syncGhostObjects(self,clientID,ghostObjects):
        #syncs new ghost objects with their respective netObjects
        for ghostKey in ghostObjects:
            ghost = ghostObjects[ghostKey]
            ghost['ID'] = str(ghost['ID'])
            self.ghostObjects[ghost['ID']] = ghost
            
    def updateScene(self):
        self.ghostObjects = {}
        for clientKey in self.gameState:
            client = self.gameState[clientKey]
            try:
                if client['clientID'] != self.clientID:

                    clientID = client['clientID']
                    ghostObjects = client['ghostObjects']
                    try:
                        extra = client['extra'] #corrigido de "client['exta']"
                    except:
                        pass
                    
                    self.syncGhostObjects(clientID,ghostObjects)
            except:
                print(client)
                
        self.updateNetObjects()


    def syncLocalGhosts(self):
        garbageGhosts = []
        for objectKey in self.localNetObjects:
            netObject = self.localNetObjects[objectKey]
            try:
                netObject.syncNetObject()
                self.localGhostObjects[netObject.ID] = netObject.getGhost()

            except:
                #This will catch when the blender object has been deleted
                print(str("Local network object ")+str(objectKey)+str(" has been deleted"))
                garbageGhosts.append(objectKey)
        for objectKey in garbageGhosts:
            del self.localNetObjects[objectKey]
            del self.localGhostObjects[objectKey]
        
    def sendGameState(self):
        sendData = {}
        sendData['ghostObjects'] = self.localGhostObjects
        sendData['extra'] = self.extra #TODO: padronizar dados de movimentos
        sendData['clientID'] = self.clientID
        try:
            self.mainSocket.sendto(pickle.dumps(sendData),(self.host,self.port))
        except:
            pass
    
        
    def handleMessages(self):
        import time
        remove = []
        for m in self.outBuffer:
            if time.time()-m > .2:
                remove.append(m)
        for m in remove:
            del self.outBuffer[m]
        #add messages to in buffer which have not already been processed
        for s in self.gameState:
            for e in self.gameState[s]['extra']:
                message = self.gameState[s]['extra'][e]
                self.inBuffer[e] = message
        for m in self.inBuffer:
            if m not in self.handledList:
                self.handledList.append(m)
                self.handleMessage(m)
        self.inBuffer = {}

    
    def handleMessage(self,m):
        message = self.inBuffer[m]
        import bge
        cont = bge.logic.getCurrentController()
        owner = cont.owner
        for obj in bge.logic.getCurrentScene().objects:
            if obj != owner:
                owner.sendMessage(message['subject'], message['body'], obj.name)
        print(str("handled message ")+str(m)+str(" ")+str(self.inBuffer[m]['body']))

    def handleDeletedGhosts(self):
        deletedObjects = []
        for netObjectKey in self.netObjects:
            if netObjectKey in self.ghostObjects:
                pass
            else:
                deletedObjects.append(netObjectKey)
        for objectKey in deletedObjects:
            print("ghost object no longer exists.. deleting")
            self.netObjects[objectKey].gameObject.endObject()
            del self.netObjects[objectKey]

    def handleDeletedObjects(self):
        deletedObjects = []
        for netObjectKey in self.localNetObjects:
            try:
                self.localNetObjects[netObjectKey].gameObject
            except:
                print("blarg!")
                del self.localNetObjects[netObjectKey]
                del self.localGhostObjects[netObjectKey]
        for objectKey in deletedObjects:
            print("ghost object no longer exists.. deleting")
            self.netObjects[objectKey].gameObject.endObject()
            del self.netObjects[objectKey]

    def recvGameState(self):
        r = b""
        result = False
        try:
            r,addr = self.mainSocket.recvfrom(65535)
            self.packet += r
            try:
                result = pickle.loads(self.packet)
                self.packet = b""
            except:
                
                print("message was too large" ) 
        except:
            pass     
        return result,len(r)

    def sendMessage(self,sender,subject,body):
        import time
        sendTime = time.time()
        try:
            self.outBuffer[sendTime]
            sendTime += .000001
        except:
            pass
        self.outBuffer[sendTime] = {"sender":sender,"subject":subject,"body":body}
        print(str("sending message ")+str(sendTime))
        
    def run(self):
        size = 0
        if self.connection == "connected":
            #print(self.localNetObjects[str(self.clientID)+str(":")+str(0)].gameObject['ID'])
            #self.handleDeletedObjects()
            self.syncLocalGhosts()
            self.sendGameState()
            self.setConnectedClients()
            result,size = self.recvGameState()
            if result != False:
                self.gameState = result
                self.handleDeletedGhosts()
                self.handleConnections()
                self.setPing()
                self.updateScene()
                #print(str("true")+str(size))
            else:
                #print("false")
                self.timeout = time.time()
        
            if self.timeout >= self.maxTimeout:
                print("socket timed out")
                self.disconnect()
        
        return (self.connection,self.ping,len(self.gameState),size)

    def setPing(self):
        import time
        t = time.time()
        self.ping = round(float(t-self.timeout)*1000,2)
        self.timeout = t
        self.maxTimeout = t+100

    def disconnect(self):
        self.connection = "disconnected"
        self.mainSocket.close()
        print("you have been disconnected")
        
        
