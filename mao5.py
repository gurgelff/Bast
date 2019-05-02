# -*- coding: utf-8 -*-
"""
CollisionHandlerFloor - how to steer an avatar on a uneven terrain keeping it grounded.

by fabius astelix @2010-01-25

Level: INTERMEDIATE

We'll see how to settle up a scene to have a movable avatar following the Z-height of an uneven the terrain. All of this is drived by the panda3D CollisionHandlerFloor collision handler.

NOTE If you won't find here some line of code explained, probably you missed it in the previous steps - if you don't find there as well though, or still isn't clear for you, browse at http://www.panda3d.org/phpbb2/viewtopic.php?t=7918 and post your issue to the thread.

Bast Centipede by Fernando Gurgel @2015

"""

import direct.directbase.DirectStart
import json
from pandac.PandaModules import *
from direct.directtools.DirectGeometry import LineNodePath
from direct.gui.OnscreenText import OnscreenText
from panda3d.core import ColorAttrib
from panda3d.core import *
from panda3d.ode import *
from direct.task import Task
import sys
import time

from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import CollisionHandlerFloor, CollisionNode, CollisionTraverser, BitMask32, CollisionRay

from pandac.PandaModules import loadPrcFileData
loadPrcFileData("", """sync-video 0
"""
)
import direct.directbase.DirectStart
#** snippet support routines - not concerning the tutorial part
import snipstuff

def drawLines():
  # Draws lines between the smiley and frowney.
  lines.reset()
  lines.drawLines([((art.getX(), art.getY(), art.getZ()),
					(avatar.getX(), avatar.getY(), avatar.getZ())),
				   ((avatar.getX(), avatar.getY(), avatar.getZ()),
					(0, 0, 0))])
  lines.create()



def updateTask(task):
	updatePlayer()
	#updateCamera()
	return Task.cont


def checkjson():
	time.sleep(0.1)
	try:
		json_data = open('cmd.json').read()
		data = json.loads(json_data)
		direction1 = data["direction1"]
		direction2 = data["direction2"]
		direction3 = data["direction3"]
		intensity1 = int(data["intensity1"])
		intensity2 = int(data["intensity2"])
		intensity3 = int(data["intensity3"])
		rotz = data["rotation"]
		return direction1, direction2, direction3, intensity1 ,intensity2, intensity3, rotz
	except:
		return "down", "down", "down", 0, 0, 0, 0




def updatePlayer():
	
	(direction1, direction2, direction3, intensity1, intensity2, intensity3, rotz) = checkjson()
	if (direction1=="up"):
		art.setZ(avatar.getZ()+abs(intensity1))
		avatar.setHpr(0,90,rotz)		
	elif (direction1=="down"):
		art.setZ(avatar.getZ()-abs(intensity1))
		avatar.setHpr(0,90,rotz)	
	if (direction2=="up"):
		art2.setZ(avatar.getZ()+abs(intensity2))	
		art2.setHpr(0,0,intensity2*10)		
	elif (direction2=="down"):
		art2.setZ(avatar.getZ()-abs(intensity2))
		art2.setHpr(0,0,intensity2*10)	
	if (direction3=="up"):
		art3.setZ(avatar.getZ()+abs(intensity3))		
		art3.setHpr(0,0,intensity3*10)	
	elif (direction3=="down"):
		art3.setZ(avatar.getZ()-abs(intensity3))
		art3.setHpr(0,0,intensity3*10)	
		
		
		
	



def updateCamera():
	# see issue content for how we calculated these:
	camera.setPos(player2, 25.6225, 3.8807, 10.2779)
	camera.setHpr(player2,94.8996,-16.6549,1.55508)


#=========================================================================
# Scenographic stuff
#=========================================================================
base.cam.setPos(40, -70, 35)

splash=snipstuff.splashCard()
snipstuff.info.append("Collisions With Floor and Walls in action")
snipstuff.info.append("a minimal sample to show how to keep an avatar grounded and blocked by invisible walls")
snipstuff.info.append("WASD=move the avatar around\nSPACE=avatar hiccup")
snipstuff.info_show()

#=========================================================================
# Main
"""
Starting from step1, we just put an additional collision handler to take care to keep the avatar grounded. This will PUSH the avatar back as soon as hit geometry we settled to be a wall: in blender we modelled polygons to wrap around the little house and all around the terrain area so that this time the avatar, differently from step1, won't pass through the house and won't be able to leave the terrain perimeter anymore. I suggest you to open the blender source to find out what I'm talking about here.
"""
#=========================================================================

#** Collision system ignition
base.cTrav=CollisionTraverser()
# did you saw this stuff in step1?
floorHandler = CollisionHandlerFloor()
floorHandler.setMaxVelocity(14)
# here it is the new fella - this will take care to push the avatar off the walls
wallHandler = CollisionHandlerPusher()

#** As you know this mask is used to mark the geometries for the floor collisions...
FLOOR_MASK=BitMask32.bit(1)
#... and this time we need another one to mark the walls as well.
WALL_MASK=BitMask32.bit(2)

#** This is our steering avatar - this time we use a little different setup, more close to real applications: we wrap either the avatar and its collision ray into another nodepath. This way we add lotta flexibility allowing us to make fancy things like you'll see below, to make the avatar rolling while steering, a thing not possible before and also to get rid of the global floorHandler.setOffset(1.0) shift, to set our avatar precisly placed above the surface.
avatarNP=NodePath('smileyNP')
avatarNP.reparentTo(base.render)

avatar = loader.loadModel('cilindroB')
avatar.reparentTo(avatarNP)
# since our avatar origin is centered in a model sized 2,2,2, we need to shift it 1 unit above the ground and this time we make this happen shifting it off its own root node (avatarNP)
avatar.setPos(0,0,1)
avatar.setHpr(0,90,0)
avatar.setColor(0, 0, 1, 1)
avatar.setCollideMask(BitMask32.allOff())

art = loader.loadModel('cilindroR')
art.reparentTo(avatar)
# since our avatar origin is centered in a model sized 2,2,2, we need to shift it 1 unit above the ground and this time we make this happen shifting it off its own root node (avatarNP)
art.setPos(avatar.getX(),avatar.getY(), avatar.getZ())
art.setColor(1, 0, 0, 1)
art.setCollideMask(BitMask32.allOff())

avatar2 = loader.loadModel('cilindroB')
avatar2.reparentTo(art)
# since our avatar origin is centered in a model sized 2,2,2, we need to shift it 1 unit above the ground and this time we make this happen shifting it off its own root node (avatarNP)
avatar2.setPos(art.getX(),art.getY(), art.getZ()+3.325)
avatar2.setColor(1, 1, 0, 1)
avatar2.setCollideMask(BitMask32.allOff())

art2 = loader.loadModel('cilindroR')
art2.reparentTo(avatar2)
# since our avatar origin is centered in a model sized 2,2,2, we need to shift it 1 unit above the ground and this time we make this happen shifting it off its own root node (avatarNP)
art2.setPos(avatar2.getX(),avatar2.getY(), avatar2.getZ())
art2.setColor(1, 0, 0,1)
art2.setCollideMask(BitMask32.allOff())

avatar3 = loader.loadModel('cilindroB')
avatar3.reparentTo(art2)
# since our avatar origin is centered in a model sized 2,2,2, we need to shift it 1 unit above the ground and this time we make this happen shifting it off its own root node (avatarNP)
avatar3.setPos(art2.getX(),art2.getY(), art2.getZ())
avatar3.setColor(1, 0.5, 0, 1)
avatar3.setCollideMask(BitMask32.allOff())

art3 = loader.loadModel('cilindroR')
art3.reparentTo(avatar3)
# since our avatar origin is centered in a model sized 2,2,2, we need to shift it 1 unit above the ground and this time we make this happen shifting it off its own root node (avatarNP)
art3.setPos(avatar3.getX(),avatar3.getY(), avatar3.getZ())
art3.setColor(1, 0, 0,1)
art3.setCollideMask(BitMask32.allOff())




avatarNP.setPos(0,0,15)
# we reintroduced in this snippet the renowned smiley collision sphere - we need it as low-poly collision geometry for the wall collision handler to know when the smiley hit a wall.
avatarCollider = avatar.attachNewNode(CollisionNode('smileycnode'))
avatarCollider.node().addSolid(CollisionSphere(0, 0, 0, 1))
# of course we mark it with the wall mask
avatarCollider.node().setFromCollideMask(WALL_MASK)
avatarCollider.node().setIntoCollideMask(BitMask32.allOff())

# we reintroduced in this snippet the renowned smiley collision sphere - we need it as low-poly collision geometry for the wall collision handler to know when the smiley hit a wall.
artCollider = art.attachNewNode(CollisionNode('smileycnode'))
artCollider.node().addSolid(CollisionSphere(avatar.getX(),avatar.getY(), avatar.getZ(), 1))
# of course we mark it with the wall mask
artCollider.node().setFromCollideMask(BitMask32.allOff())


# we reintroduced in this snippet the renowned smiley collision sphere - we need it as low-poly collision geometry for the wall collision handler to know when the smiley hit a wall.
avatar2Collider = avatar2.attachNewNode(CollisionNode('smileycnode'))
avatar2Collider.node().addSolid(CollisionSphere(art.getX(),art.getY(), art.getZ()+3.325, 1))
# of course we mark it with the wall mask
avatar2Collider.node().setFromCollideMask(BitMask32.allOff())


# we reintroduced in this snippet the renowned smiley collision sphere - we need it as low-poly collision geometry for the wall collision handler to know when the smiley hit a wall.
art2Collider = art2.attachNewNode(CollisionNode('smileycnode'))
art2Collider.node().addSolid(CollisionSphere(avatar2.getX(),avatar2.getY(), avatar2.getZ(), 1))
# of course we mark it with the wall mask
art2Collider.node().setFromCollideMask(BitMask32.allOff())




#** Here we stick and set the ray collider to the avatar - note that we set it well above the avatar position because like this we are sure to always find a floor surface higher than the avatar top - try to change the third value i.e. to 0 and see what happen steering the avatar to get what I mean
raygeometry = CollisionRay(0, 0, 2, 0, 0, -1)
avatarRay = avatarNP.attachNewNode(CollisionNode('avatarRay'))
avatarRay.node().addSolid(raygeometry)
# this is how we tell the collision system that this ray would collide just with the floor acting as a FROM collider.
avatarRay.node().setFromCollideMask(FLOOR_MASK)
# we then exclude the ray from acting as an INTO collider
avatarRay.node().setIntoCollideMask(BitMask32.allOff())




#** This is the terrain map - the egg model loaded contains also the collider geometry for the terrain and for the walls as childs
terrain = loader.loadModel("scene1")
terrain.reparentTo(render)
terrain.setCollideMask(BitMask32.allOff())
terrain.setScale(16)
# here how we tell the collision system that the terrain collider geometry is allowed to collide with the avatar ray as INTO collider...
floorcollider=terrain.find("**/floor_collide")
floorcollider.node().setIntoCollideMask(FLOOR_MASK)
#...and the same goes for the walls
wallcollider=terrain.find("**/wall_collide")
wallcollider.node().setIntoCollideMask(WALL_MASK)

#** as said in step1 we tells to our collision handlers who take part to the respective tasks: for the floor the avatar ray and the avatar nodepath...
floorHandler.addCollider(avatarRay, avatarNP)
# ...and for the walls the avatar sphere collider together with - again - the avatar nodepath
wallHandler.addCollider(avatarCollider, avatarNP)

wallHandler.addCollider(artCollider, avatarNP)
wallHandler.addCollider(avatar2Collider, avatarNP)
wallHandler.addCollider(art2Collider, avatarNP)

#** Now we're ready to start the collisions using the avatar ray to use to fire collisions for the floorHandler...
base.cTrav.addCollider(avatarRay, floorHandler)
# ... and the sphere for the wallHandler
base.cTrav.addCollider(avatarCollider, wallHandler)

base.cTrav.addCollider(artCollider, wallHandler)
base.cTrav.addCollider(avatar2Collider, wallHandler)
base.cTrav.addCollider(art2Collider, wallHandler)

# A task to run every frame, some keyboard setup and our speed
taskMgr.add(updateTask, "update")
#** Activating avatar steering function - now we're ready to go
steering=snipstuff.avatar_steer(avatarNP,  fwspeed=12.)
steering.start()
splash.destroy()
base.run()
