# Server Program
# Make sure the client is being run on the data generation computer

SERVER_LOOP = True

import socket
import sys
import json
import bge

cont = bge.logic.getCurrentController()
owner = cont.owner


print ('Starting up')

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print ("Socket successfully created")
except socket.error as err:
    print ("socket creation failed with error %s" %(err))

# default port for socket
port = 80

try:
    host_ip = socket.gethostbyname('www.google.com')
except socket.gaierror:
    # this means could not resolve the host
    print ("there was an error resolving the host")
    sys.exit()

# connecting to the server
s.connect((host_ip,port))

print ("the socket has successfully connected to google \
on port == %s" %(host_ip))

port = 12345                

# Next bind to the port
# we have not typed any ip in the ip field
# instead we have inputted an empty string
# this makes the server listen to requests 
# coming from other computers on the network
s.bind(('', port))        
print ("socket binded to %s" %(port))

# put the socket into listening mode
s.listen(5)     
print ("socket is listening")

# a forever loop until we interrupt it or 
# an error occurs
while True:
    
   # Establish connection with client.
   c, addr = s.accept()     
   print ('Got connection from', addr)

   # send a thank you message to the client. 
   c.send('Thank you for connecting')

    # Receive data
    try:
        data = c.recv(10000)

    # Unless there's an error
    except OSError:
        print ("Error in data transmission.")    
   
   
    # Decode the data into usable lists
    if type(data) != type(''): 
        data = data.decode()
        
    if data=='1' or data==1:
        owner.applyMovement([0.0,0.0,1])    
        
    if data=='end' or data=='End' or data=='END':
        c.shutdown(socket.SHUT_RD | socket.SHUT_WR)
        c.close()
    else:
            # gives feedback in server command line
            data = json.loads(data)
            print ('CLIENT: %s' % data)
            message = 'ping'
            c.send(('SERVER: %s' % message).encode('utf-8'))
            print ('SERVER: %s' % message)    