import contexttest as context
import random
from itertools import permutations 
import scipy.optimize as O
import numpy as N
import matplotlib.pyplot as plt

def deepfor(*xs):
    if len(xs)>0:
        hs = xs[0]
        ts = xs[1:]
        if type(hs)==int:
            hs = [hs]
        for h in hs:
            for t in deepfor(*ts):
                yield [h]+t
    else:
        yield []

def intparts(n,s,c):
    ns = list(range(0,s+1))

    xs = [ns for _ in range(n)]
    
    for k,v in c:
        xs[k] = v
        
    for x in deepfor(*xs):
        if sum(x)==s:
            yield x

            
def intpart2(s,e,n,c):
    xs = intparts(n,e-s,c)
    for x in xs:
        ok = True
        for k,v in c:
            if not x[k]==v:
                ok = False
        if ok:
            y = []
            n0 = s
            for nn in x:
                y.append((n0,n0+nn))
                n0 = n0+nn
            yield y
c = context.context()
c[0]=1


def convertMustBe(mustBe):
    c = context.context()
    curkey = ""
    curvalue = ""
    added = set()
    keys = []
    values = []
    for i,v,op in mustBe:
        keys.append(i)
        values.append(v)
        if curkey == "":
            curkey = i
            curvalue = v
        if curkey+curvalue == i:
            added.add(i)
            curvalue = curvalue +v
            c[curkey] = curvalue 
        else:
            c[curkey] = curvalue
            curkey = i
            curvalue = v
    
    lastkey = keys[-1]
    if lastkey not in added:
        c[lastkey] =values[-1]
    return c


def partitions(n,start,end,mustBe,depth = 0):
    c = convertMustBe(mustBe) #this is good 
    PS = intpart2(start,end,n,c) #fix?
    for p in PS:
        yield p  

#put the ones that can be put together together

#PS = list(partitions(8, 0, 8, [(0, 1, '=='),(1, 1, '=='),(2, 1, '=='),(3, 1, '=='),(4, 1, '=='),(5, 1, '=='),(6, 1, '==')]))
PS = list(partitions(1,5,6,[(0,1,"==")]))
print(PS)