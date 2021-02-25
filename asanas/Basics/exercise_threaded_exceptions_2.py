import random
import sys
import threading
import time
import collections

#import Y

CLASS = False
PRINT = False

M = 100
N = 100
T = 3

cancel = False
trace = []
lock = threading.Lock()

class Sync:
    def __init__(self):
        self.cancel  = False
        self.lock    = threading.Lock()
        self.trace   = []
    def __getitem__(self, k):
        v = getattr(self, k)
        return v
    def __setitem__(self, k, v):
        setattr(self, k, v)

class Sync:
    def __init__(self):
        globals()['cancel']  = False
        globals()['lock']    = threading.Lock()
        globals()['trace']   = []
    def __getitem__(self, k):
        v = globals()[k]
        return v
    def __setitem__(self, k, v):
        globals()[k] = v

def sync0():
    if CLASS: r = Sync()
    else:
        t = collections.namedtuple('Sync', ('cancel', 'lock', 'thread'))
        #t = Y.C
        r = dict(
            cancel  = False,
            lock    = threading.Lock(),
            trace   = [],
            )
    return r

def long_risky_computation(t):
    time.sleep(1)
    if t == 't0':
        xs = [True, False]
        x = random.choice(xs)
        if x:
            raise Exception(t, 'mistake')
    else:
        pass

def thread(x, sync, *args, **kwargs):
    for i in range(M):
        #lock.acquire()
        if PRINT: print(i, x)
        if sync['cancel']:
            sys.exit(0)
        else:
            #lock.release()
            try:
                long_risky_computation(x)
                sync['trace'].append(x)
            except Exception as e:
                #print(e)
                #lock.acquire()
                if PRINT: print(i, x, 'error')
                sync['cancel'] = True
                sync['trace'].append('error')
                #lock.release()
                sys.exit(0)

def thread2(x, cancel, trace, *args, **kwargs):
    #global cancel, trace
    for i in range(M):
        #lock.acquire()
        if PRINT: print(i, x)
        if cancel:
            sys.exit(0)
        else:
            #lock.release()
            try:
                long_risky_computation(x)
                trace.append(x)
            except Exception as e:
                #print(e)
                #lock.acquire()
                if PRINT: print(i, x, 'error')
                cancel = True
                trace.append('error')
                #lock.release()
                sys.exit(0)

def process():
    i = 0
    while True:
        i += 1       
        xs = ['t'+str(t) for t in range(T)]
        if not CLASS:
            #global cancel, trace
            cancel  = False
            trace   = []
        sync = sync0()
        def make_thread(x):
            if CLASS:
                t = threading.Thread(
                    args    = (x, sync),
                    name    = x,
                    target  = thread,
                    )
            else:
                t = threading.Thread(
                    args    = (x, cancel, trace),
                    name    = x,
                    target  = thread2,
                    )
            return t
        ys = [make_thread(x) for x in xs] 
        for t in ys:
            t.start()    
        for t in ys:
            t.join()
        #print(sync.trace)
        if CLASS:
            if sync['trace'][-1] == 'error':
                sync['trace'] = []
            if len(sync['trace'])>0:
                print(i, sync['trace'])
        else:
            if trace[-1] == 'error':
                trace = []
            if len(trace)>0:
                print(i, trace)
        if i>=N:
            break

def main():
    process()

main() 