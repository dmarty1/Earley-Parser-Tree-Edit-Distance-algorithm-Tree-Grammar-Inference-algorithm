import random
import sys
import threading
from threading import Semaphore
import time
import threadingLib
from threadingLib import *

sem = Semaphore()
#e = threading.Event()
lock = threading.Lock()

def help():
    print("doc")

class CancellationToken:
   def __init__(self):
       self.is_cancelled = False
       self.lock = threading.Lock()
       self.sem = threading.BoundedSemaphore(1)
       self.a = []

   def cancel(self):
       self.is_cancelled = True

def long_risky_computation(x):
    # long
    time.sleep(0.01)
    # risky
    # thread a makes no mistake
    #if x == 'a':
    #    pass
    # thread b makes a mistake with a 50% chance
    if x == 'a':
        xs = [True, False]
        x = random.choice(xs)
        if x:
            raise Exception()
    else:
        pass

def thread(x,cancel):
    # name x
    for i in range(100):
        
        #print(x, cancel.is_cancelled)
        if cancel.is_cancelled:
            sys.exit(0)
        print(x, i)
        cancel.a.append(x)
        try:
            long_risky_computation(x)
            #cancel.lock.release()
        except:
                    # exit on error
            cancel.cancel()

            #print(x, i, 'error')
            cancel.a.append((x,"error"))
            #cancel.lock.acquire()
            sys.exit(0)
            

def process():
    xs = 'abc'
    cancel = CancellationToken()
    ys = [threading.Thread(name = x, target=thread, args=(x,cancel,)) for x in xs]

    for t in ys:
        t.start()    
    for t in ys:
        t.join()
    
    if (cancel.a[-1]==("a", "error")):
        pass

        #process()
    print(cancel.a)


def main():
    help()
    process()

main()
