#!/usr/bin/env python

import multiprocessing.pool
import threading
import time
from queue import Queue
from threading import Thread

dictionary = {}

def flatten(x):
    y = []
    for xx in x:
        y.extend(xx)
    return y

def generator(ys):
    x = threading.get_ident()
    if x in dictionary:
        threadname = dictionary[x]
    else:
        dictionary[x] = chr(65+x%10)
        threadname = dictionary[x]
    t = threading.current_thread()
    t.setName(threadname)
    for y in ys:
        time.sleep(1)
        z = 'f({:02d})'.format(y)
        print(t.getName(), z)
        yield (t.getName(), z)

def groups(xs, n, f=None):
    nx = len(xs)
    a = list(zip(*[iter(xs)]*n))
    na = len(a)*n
    b = tuple(xs[na:])
    Xs = a
    if na<nx:
        Xs = Xs+[b]
    return Xs

def input():
    x = list(range(16))
    return x

def threads(f, x, n):
    def g(x):
        y = list(f(x))
        return y
    P = multiprocessing.pool.ThreadPool
    p = P(n)
    
    q = Queue()
    for i in range(n):
        t = Thread(target=g, args=(i,))
        t.daemon =True
        t.start()
    for i in x:
        q.put(i)
    q.join()
    
    y = p.map(g, x)
    p.close()
    p.join()
    return y

def threaded_generators(f, x, ng, np):
    y = groups(x, ng)
    y = threads(f, y, np)
    y = flatten(y)
    return y

def main():
    f = generator
    x = input()
    y = threaded_generators(f, x, 5, 4)
    for yy in y:
        print(yy)

main()