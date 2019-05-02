class netObject:
    #defanitions
    #ghost object = an object that is not attached to a kx_gameObject
    #sendable = a copy of all the 
    def __init__(self):
        import bge
        try:
            self.network = bge.network
            self.ID = str(bge.network.clientID)+str(":")+str(bge.network.getNextID())
        except:
            self.ID = 0
            print("bge.logic.network has not been defined! This netObject cannot be synced.")
            import network
            self.network = network.network
        self.res = 3
        self.controller = bge.logic.getCurrentController()
        self.gameObject = self.controller.owner
        if "publicID" in self.gameObject:
            self.ID = str(self.gameObject['publicID'])
        self.name = self.gameObject.name
        self.position = self.getListThree(self.gameObject.position)
        self.orientation = self.getListNine(self.gameObject.orientation)
        try:
            self.linearVelocity = self.getListThree(self.gameObject.getLinearVelocity())
            self.angularVelocity = self.getListThree(self.gameObject.getAngularVelocity())
        except:
            self.linearVelocity = [0,0,0]
            self.angularVelocity = [0,0,0]
        self.gameObject['ID'] = self.ID
        self.properties = {}
        for prop in self.gameObject.getPropertyNames():
            if prop != "ID" and prop != "publicID" and prop != "local":
                if type(self.gameObject[prop]) == bool or type(self.gameObject[prop]) == str or type(self.gameObject[prop]) == int or type(self.gameObject[prop]) == float:
                    self.properties[prop] = self.gameObject[prop]
            
        self.sendable = {"ID":self.ID,"n":self.name,"p":self.position,"o":self.orientation,"lv":self.linearVelocity,"av":self.angularVelocity,"pr":self.properties}

            
        if self.gameObject['local'] == False:
            self.network.addPublicNetObject(self)
            print("created public netObject "+str(self.ID)+".")
        else:
            self.network.addLocalNetObject(self)
            print("created local netObject "+str(self.ID)+".")

    def setObject(self,xk_object):
        self.gameObject = xk_object

    def setID(self,ID):
        self.ID = ID

    def getGhost(self):
        self.syncNetObject()
        return self.sendable
        
    def hardSync(self,ghost):
        self.position = ghost['p']
        self.orientation = ghost['o']
        self.linearVelocity = ghost['lv']
        self.angularVelocity = ghost['av']
        for prop in ghost['pr']:
            if prop != 'local' and prop != 'publicID':
                self.properties[prop] = ghost['pr'][prop]
        self.syncGameObject()

    def syncGameObject(self):
        self.gameObject.position = self.position
        self.gameObject.orientation = self.orientation
        try:
            self.gameObject.setLinearVelocity(self.linearVelocity)
            self.gameObject.setAngularVelocity(self.angularVelocity)
            self.gameObject.resumeDynamics()
        except:
            self.gameObject.suspendDynamics()
        for prop in self.properties:
            if prop != 'local' and prop != 'publicID':
                self.gameObject[prop] = self.properties[prop]

    def syncNetObject(self):
        self.position = self.getListThree(self.gameObject.position)
        self.orientation = self.getListNine(self.gameObject.orientation)
        try:
            self.linearVelocity = self.getListThree(self.gameObject.linearVelocity)
            self.angularVelocity = self.getListThree(self.gameObject.angularVelocity)
        except:
            self.linearVelocity = [0,0,0]
            self.angularVelocity = [0,0,0]
        for prop in self.gameObject.getPropertyNames():
            if prop != "ID" and prop != "publicID" and prop != "local":
                if type(self.gameObject[prop]) == bool or type(self.gameObject[prop]) == str or type(self.gameObject[prop]) == int or type(self.gameObject[prop]) == float:
                    self.properties[prop] = self.gameObject[prop]
        self.sendable = {"ID":self.ID,"n":self.name,"p":self.position,"o":self.orientation,"lv":self.linearVelocity,"av":self.angularVelocity,"pr":self.properties}
        
    def getListThree(self,pos):
        newPos = [0,0,0]
        for i in range(0,3):
            newPos[i] = round(pos[i],self.res)
        return newPos

    def getListNine(self,ori):
        newOri = [[1,0,0],[0,1,0],[0,0,1]]
        for i in range(0,3):
            for w in range(0,3):
                newOri[i][w] = round(ori[i][w],self.res)
        return newOri
