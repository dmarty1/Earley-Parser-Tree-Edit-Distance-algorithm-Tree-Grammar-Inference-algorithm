#!/usr/bin/env python

import threading
import time

import contexttest as context
M = 4
N = 20

def f(x):
    time.sleep(1)
    w = threading.get_ident()
    y = (w, 'f', x)
    return y

pool = context.context(
    inputs 	= [],
    outputs	= [],
    threads = [],
    )

def work():
    while True:
        try:
            f, xs = pool.inputs.pop(0)
            ys = f(xs)
            pool.outputs.append(ys)
        except:
            break

for i in range(N):
    pool.inputs.append((f, i))

for i in range(M):
    t = threading.Thread(target=work)
    pool.threads.append(t)
    t.start()
for i in range(M):
    t.join()

print(pool.outputs)