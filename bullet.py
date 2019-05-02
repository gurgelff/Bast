import direct.directbase.DirectStart
import random
from panda3d.core import Vec3
from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletPlaneShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletBoxShape
from panda3d.bullet import BulletConvexHullShape
from panda3d.bullet import BulletCylinderShape
from panda3d.bullet import BulletDebugNode
from direct.showbase.DirectObject import DirectObject
 

 
debugNode = BulletDebugNode('Debug')
debugNode.showWireframe(True)
debugNode.showConstraints(True)
debugNode.showBoundingBoxes(False)
debugNode.showNormals(False)
debugNP = render.attachNewNode(debugNode)
debugNP.show()


 
base.cam.setPos(0, -10, 0)
base.cam.lookAt(0, 0, 0)
 
# World
world = BulletWorld()
world.setGravity(Vec3(0, 0, -9.81))
world.setDebugNode(debugNP.node())
 
# Plane
shape = BulletPlaneShape(Vec3(0, 0, 1), 1)
node = BulletRigidBodyNode('Ground')
node.addShape(shape)
np = render.attachNewNode(node)
np.setPos(0, 0, -2)
world.attachRigidBody(node)
 
# Box
shape = BulletBoxShape(Vec3(0.5, 0.5, 0.5))
node = BulletRigidBodyNode('Box')
node.setMass(1.0)
node.addShape(shape)
np = render.attachNewNode(node)
np.setPos(0, 0, 2)
world.attachRigidBody(node)
model = loader.loadModel('models/box.egg')
model.flattenLight()
model.reparentTo(np)

# Box2
shape = BulletBoxShape(Vec3(0.5, 0.5, 0.5))
node = BulletRigidBodyNode('Box')
node.setMass(20.0)
node.addShape(shape)
np = render.attachNewNode(node)
np.setPos(0, 0, 4)
world.attachRigidBody(node)
model = loader.loadModel('models/box.egg')
model.flattenLight()
model.reparentTo(np)

 
# Update
def update(task):
  dt = globalClock.getDt()
  world.doPhysics(dt, 25, 1.0/180.0)
  return task.cont
 
def toggleDebug():
  if debugNP.isHidden():
    debugNP.show()
  else:
    debugNP.hide()

def addBox():
	# Box
	#shape = BulletCylinderShape(0.5, 3, 2) 
	
	geomNodes = loader.loadModel('cilindroB').findAllMatches('**/+GeomNode')
	geomNode = geomNodes.getPath(0).node()
	geom = geomNode.getGeom(0)
	
	shape = BulletConvexHullShape()
	shape.addGeom(geom)
	node = BulletRigidBodyNode('Cylinder')
	node.setMass(random.randint(1,10))
	node.addShape(shape)
	np = render.attachNewNode(node)
	np.setPos(0, 0, 10)
	world.attachRigidBody(node)
	#model = loader.loadModel('cilindroR')
	model.flattenLight()
	model.reparentTo(np)

o = DirectObject()
o.accept('f1', toggleDebug)
o.accept('a', addBox)
 
taskMgr.add(update, 'update')
base.run()
