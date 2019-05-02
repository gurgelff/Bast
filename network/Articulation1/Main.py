from bge import logic as l, events
import threading
from queue import Queue
import inspect
import ctypes 


c = l.getCurrentController()
o = c.owner
cena = l.getCurrentScene()
k = l.keyboard.events

lock = threading.Lock()
q = Queue()

def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble, 
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")

def stop_thread(thread):
    _async_raise(thread.ident, SystemExit)
        
def exampleJob(worker):
    with lock:
        import SocketServer
        print(threading.current_thread().name,worker)
        
    
# The threader thread pulls an worker from the queue and processes it        
def threader():
    while True:
        # gets an worker from the queue
        worker = q.get()

        # Run the example job with the avail worker in queue (thread)
        exampleJob(worker)

        # completed with the job
        q.task_done()    
        
# how many threads are we going to allow for
for x in range(1):
     t = threading.Thread(target=threader)

     # classifying as a daemon, so they will die when the main dies
     t.daemon = True

     # begins, must come after daemon definition
     t.start()
     

        
# 20 jobs assigned.
for worker in range(1):
    q.put(worker)

# wait until the thread terminates.
stop_thread(t)
q.join()

            

if k[events.WKEY] in [1, 1]:
    o.applyMovement([ 0.0, 0.0, 0.50])

if k[events.SKEY] in [1,1]:
	o.applyMovement([ 0.0, 0.0, -0.50])