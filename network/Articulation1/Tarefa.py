import threading
from queue import Queue


class Tarefa():
    def __init__(self, tipo):
        self.tipo = tipo
        
    def run(self):        
        lock = threading.Lock()
        q = Queue()
        
        def exampleJob(worker):
            with lock:
                print("oi\n")
                #import SocketServer
        
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

        
        # 1 jobs assigned.
        for worker in range(1):
            q.put(worker)

        # wait until the thread terminates.
        #q.join()
         
            