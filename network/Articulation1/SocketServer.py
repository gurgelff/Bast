# Server Program

import socket
import sys
import json
import bge

cont = bge.logic.getCurrentController()
owner = cont.owner

def start():
    
    print ('Starting up')

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        print ("Socket successfully created")
    except socket.error as err:
        print ("socket creation failed with error %s" %(err))



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
       thanks = 'Thank you for connecting'
       c.send(thanks.encode('utf-8'))

        # Receive data
       try:
           data = c.recv(10000)
           # Decode the data into usable lists
           if type(data) != type(''): 
               data = data.decode()

       # Unless there's an error
       except OSError:
           print ("Error in data transmission.")    
       
            
       if data=='1' or data==1:
           owner.applyMovement([0.0,0.0,1])    
            
       if data=='end' or data=='End' or data=='END':
           c.shutdown(socket.SHUT_RD | socket.SHUT_WR)
           c.close()
              
    #   else:
    #           # gives feedback in server command line
     #          data = json.loads(data)
      #         print ('CLIENT: %s' % data)
       #        message = 'ping'
        #       c.send(('SERVER: %s' % message).encode('utf-8'))
         #      print ('SERVER: %s' % message)  