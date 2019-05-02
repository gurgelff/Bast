#Autor: totter333
#Tutorial fonte: https://www.youtube.com/watch?v=A-OY1h_iPl4
import bge
cont = bge.logic.getCurrentController()
owner = cont.owner
if cont.sensors['run'].positive:
    connection, ping, players, size = bge.network.run()
    owner['ping'] = ping
    owner['players'] = players
    owner['connection'] = connection
    owner['size'] = size
    

        
        
