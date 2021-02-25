#string edit distance

import sys
sys.path.append("/Users/diva-oriane/Documents/GitHub/asanas/Parse/")

import contexttest as context
from parse3 import parse3 as parse
import random

costs = context.context(i = 1, d = 1, s = 1)

def argmin(choices,f):
    k0 = None
    v0 = None
    v1 = None
    for k,v in choices:
        #print(k,v,f(v))
        if v1 == None:
            k0 = k
            v0 = v
            v1 = f(v)
        elif f(v)<v1:
            k0 = k
            v0 = v
            v1 = f(v)

    return k0,v0

def argmins(choices,f):
    k0 = None
    v0 = None
    v1 = None
    tester = []
    for k,v in choices:
        #print(k,v,f(v))
        if v1 == None:
            k0 = k
            v0 = v
            v1 = f(v)
            tester = [(k,v)]
        elif f(v)<v1:
            k0 = k
            v0 = v
            v1 = f(v)
            tester = [(k,v)]
        elif f(v)==v1:
            tester.append((k,v))
                
    return v1,tester
        
    
#abstrat choices
def editDistance(w1,w2):

    
    def diff(i, j):
        if i<len(w1) and j<len(w2):
            if w1[i]==w2[j]:
                return 0
            else:
                return 1
        else:
            return 1
            
    E = context.context()    

    m = len(w1)
    n = len(w2)
    
    for i in range(m+1):
        if i>0:
            E[i][0] = (i,[[(i-1,0)]])
        else:
            E[i][0] = (i,[[]])
    for j in range(1,n+1):
        if j>0:
            E[0][j] = (j,[[(0,j-1)]])
        else:
            E[0][j] = (j,[[]])
    for i in range(1,m+1):
        for j in range(1,n+1):
            
            ii = i-1
            jj = j-1
            choices = context.context()
            choices[(ii,j)] = E[ii][j][0] + costs.i,E[ii][j][1]
            choices[(i,jj)] = E[i][jj][0] + costs.d,E[i][jj][1]
            choices[(ii,jj)] = E[ii][jj][0] + diff(i-1, j-1)*costs.s,E[ii][jj][1]
            
            #print("choices",choices)
            #k0,v0 = argmin(choices,lambda x: x[0])
            v1, kvs = argmins(choices,lambda x: x[0])
            #print("kvs",v0,kvs)
            paths = []
            for k,v in kvs:
                for p in v[1]:
                    path = p + [k]
                    paths.append(path)
            #print(i,j,paths)

            
            E[i][j] = v1,paths
    
    cost = E[m][n][0]
    paths = E[m][n][1]
    #if (0,0) not in path:
    #    path = [(0,0)]+path
    paths0 = []
    for path in paths:
        paths0.append(path + [(m,n)])
    E[m][n] = cost, paths0
        
    paths = E[m][n][1]
    return E,cost,paths

uv = "abcd","ab"
uv = "exponential","polynomial"
uv = "snowy","sunny"
uv = "abcd","dcba"
uv = "abc","cbde"
uv = "snowy","sun"
#uv = "def f(A1): def g(A2): return z return g","def fg(A1,A2): return z"

ed, cost, path = editDistance(*uv)

#print(cost)
#print([" "]+[c for c in uv[1]])
for i,l in ed:
    print([uv[0][i-1] if i>0 else " "]+[v[0] for k,v in l])

#print(path)

def moves(E,cost,path,*uv):
    w1,w2 = uv[0],uv[1]
    output = []
    for index in range(len(path)-1):
        i1,j1 = path[index]
        i2,j2 = path[index+1]
        move = context.context()
        #diagonal case
        if i2 == i1+1 and j2 == j1+1:
            #match
            if E[i1][j1][0]==E[i2][j2][0]:
                pass
                #move.op = "match"
            #sub
            else:
                move.op ="sub"
                move.arg[0] = j1
                move.arg[1] = w2[j2-1]
        #right
        elif i2 == i1+1:
            move.op ="del"
            move.arg[0] = j1
            #move.arg[1] = w1[i2-1]
            #deletion
            pass
        #down
        elif j2 == j1+1:
            move.op  = "ins"
            move.arg[0] = j1
            move.arg[1] = w2[j2-1]
            #insertion
            pass
        if move:
            output.append(move)
    return output 




def play(moves,*uv):
    word = uv[0]
    print(word)
    for mov in moves:
        if mov.op == "sub":
            word = word[:mov.arg[0]]+mov.arg[1]+word[mov.arg[0]+1:]
        elif mov.op == "del":
            word = word[:mov.arg[0]]+word[mov.arg[0]+1:]
        elif mov.op == "ins":
            word = word[:mov.arg[0]]+mov.arg[1]+word[mov.arg[0]:]
        #print(word)
 
for i,p in enumerate(path):
    mov = moves(ed,cost,p,*uv)
    print(i,"mov",mov)
    play(mov,*uv)
    


'''
def combineAlltest(alltest,i,j,paths = []):
    if len(alltest([i,j]))>1:
        return wrapper(alltest,i,j)
    if (i,j)==(0,0):
        return [(0,0)] 
    paths = [None]*len(alltest[(i,j)])
    for k,(ii,jj) in enumerate(alltest[(i,j)]):
        paths[k] =  [(i,j)]+combineAlltest(alltest,ii,jj)
    
    return paths[k]

def combineAlltest(alltest,i,j,paths = []):
    if (i,j)==(0,0):
        return [(0,0)] 
    for k,(ii,jj) in enumerate(alltest[(i,j)]):
        return  [(i,j)]+combineAlltest(alltest,ii,jj)
    

def wrapper(alltest,i,j):
    paths  = []
    for k,(ii,jj) in enumerate(alltest[(i,j)]):
        paths+=[combineAlltest(alltest,ii,jj)]
    return paths
    

#m,n
print((wrapper(alltest,4,4)))
'''
        
        
    


    #look one ahead and compare
    #diagonal (i,j)->(i+1,j+1) math or sub
    #down (i,j)->(i,j+1) deletion
    #right (i,j)->(i+1,j) insertion
        
        

        
            
'''
for i in range(1,m+1):
    for j in range(1,n+1):
        ii = i-1
        jj = j-1
        if ii>-1 and jj>-1 and E[ii][jj] == E[i][j]:
            pass

#Edges so create a connection down, right, downright
edges = []
for i in range(m+1):
    for j in range(n+1):
        if i+1<m+1:
            edges.append([(i,j),(i+1,j)])
        if j+1<n+1:
            edges.append([(i,j),(i,j+1)])
        if i+1<m+1 and j+1<n+1:
            edges.append([(i,j),(i+1,j+1)])

weights = context.context()
weights[0] = []
weights[1] = []
for e in edges:
    [(i1,j1),(i2,j2)]  = e
    flipe = [(i2,j2),(i1,j1)]
    if E[i1][j1]==E[i2][j2] and flipe not in weights[0]:
            weights[0].append(e)
    elif flipe not in weights[1]:
        weights[1].append(e)
    
edges = context.context()
weights = context.context()
weights[0]=[]
weights[1] = []

for i in range(m+1):
    for j in range(n+1):
        e1 = str((i,j))+","+str((i+1,j))
        #flipe1 = str((i+1,j))+","+str((i,j))
        e2 = str((i,j))+","+str((i,j+1))
        #flipe2 = str((i,j+1))+","+str((i,j))
        e3 = str((i,j))+","+str((i+1,j+1))
        #flipe3 = str((i+1,j+1))+","+str((i,j))
        if i+1<m+1:
            edges[e1] = 1
            weights[1].append(e1)
        if j+1<n+1:
            edges[e2] = 1
            weights[1].append(e2)
        if i+1<m+1 and j+1<n+1:
            if E[i][j] == E[i+1][j+1]:
                edges[e3] = 0
                weights[0].append(e3)
                
        
#distance between 0,0 to m,n

        # ij -> i+1,j 
        #ij ->i,j+1
        #ij ->i+1,j+1
        
        
'''
