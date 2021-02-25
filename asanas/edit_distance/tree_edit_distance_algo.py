
import sys
sys.path.append("/Users/diva-oriane/Documents/GitHub/asanas/Parse/")

import contexttest as context
from parse3 import parse3 as parse
import random
import hashlib
import zss

C = context.context
'''
tried using the last key roots tree instead of the tree edit distance tree

Some bugs remain, but this is appears to be a viable option
'''

def convertToContext(d):
    if type(d)==dict:
        c = context.context()
        for k,v in d.items():
            c[k] = convertToContext(v)
    elif type(d)==list:
        c = []
        for i in d:
            c.append(convertToContext(i))
    else:
        c = d
    return c

def exampleSource():
    input = [{'node': '^', 'subtrees': [{'node': 'A', 'subtrees': [{'node': 'L', 'subtrees': ['def']}, ' ', 'fg', '(', {'node': 'C', 'subtrees': ['A1', {'node': 'C', 'subtrees': ['A2',{'node': 'C', 'subtrees': '#'}]},{'node': 'C', 'subtrees': '#'}]}, ')', ':']}, ' ',{'node': 'B', 'subtrees': [{'node': 'L', 'subtrees': ['return']}, ' ', 'z']}]}]
    #input = [{'node': '^', 'subtrees':[{'node': 'A','subtrees':[{'node':'L','subtrees':['def']},' ', 'fg','(',{'node':'@','subtrees':['A1']},',',{'node':'@','subtrees':['A2']},')']},{'node':'B','subtrees':[{'node':'L','subtrees':['return']},' ', 'z']}]}]
    #input = [{'node':'^','subtrees':['[',{'node':'@','subtrees':['f']},'(',{'node':'@','subtrees':['x']},')',']']}]
    #input = [{'node': '^', 'subtrees': [{'node': 'A', 'subtrees': ['b','c']}]}]
    #input = [{'node': 'f', 'subtrees': [{'node': 'd', 'subtrees': ['a',{'node': 'c', 'subtrees':['b']}]},'e']}]

    return convertToContext(input)
    
def exampleTarget():
    input = [{'node': '^', 'subtrees': [{'node': 'A', 'subtrees': [{'node': 'L', 'subtrees': ['def']}, ' ', 'f', '(', {'node': 'C', 'subtrees': ['A1',{'node': 'C', 'subtrees': '#'}]}, ')', ':']}, ' ',{'node': 'A', 'subtrees': [{'node': 'L', 'subtrees': ['def']}, ' ', 'g', '(', {'node': 'C', 'subtrees': ['A2',{'node': 'C', 'subtrees': '#'}]}, ')', ':']}, ' ',{'node': 'B', 'subtrees': [{'node': 'L', 'subtrees': ['return']}, ' ', 'z']},' ',{'node': 'B', 'subtrees': [{'node': 'L', 'subtrees': ['return']}, ' ', 'g']}]}]
    #input = [{'node': '^', 'subtrees':[{'node': 'A','subtrees':[{'node':'L','subtrees':['def']}, ' ', 'f']},'(',{'node':'@','subtrees':['A1']},')',{'node': 'A','subtrees':[{'node':'L','subtrees':['def']}, ' ', 'g']},'(',{'node':'@','subtrees':['A2']},')',{'node':'B','subtrees':[{'node':'L','subtrees':['return']},' ', 'z']},{'node':'B','subtrees':[{'node':'L','subtrees':['return']},' ', 'g']}]}]
    #input = [{'node': 'f', 'subtrees':[{'node': 'c','subtrees':[{'node':'d','subtrees':['a','b']}]},'e']}]
    #input = [{'node': '^', 'subtrees': [{'node': 'B', 'subtrees': ['a','b']}]}]
    #input = [{'node': '^', 'subtrees': [{'node': 'B', 'subtrees': ['a','b']}]}]
    #input = [{'node': 'f', 'subtrees': [{'node': 'c', 'subtrees': [{'node': 'd', 'subtrees':['a','b']}]},'e']}]

    return convertToContext(input)

source = exampleSource()
target = exampleTarget()
                
               
def tree(T):
    t1 = C(root = 0,nodes = C(),children = C())
    def postorder(T,t1):
        added = []
        for sub in T:
            if type(sub)==str:
                index = len(t1.nodes)+1
                t1.nodes[index]=sub
                t1.children[index] = C()
                added.append(index)
            else:
                preAdd = postorder(sub.subtrees,t1)
                index = len(t1.nodes)+1
                t1.nodes[index]= sub.node
                for i,elem in enumerate(preAdd):
                    t1.children[index][i] = elem
                added.append(index)
            t1.root = index
        return added
    postorder(T,t1)
    return t1
    
t1 = tree(source)
t2 = tree(target)
print(t1)
print(t2)
'''
t1 = C(nodes = C(),children = C())
t1.nodes[1]="a"
t1.nodes[2]="b"
t1.nodes[3]="c"
t1.nodes[4] = "d"
t1.nodes[5] ="e"
t1.nodes[6] ="f"

t1.children[1] = C()
t1.children[2] = C()
t1.children[3] = C()
t1.children[3][0] = 2
t1.children[4] = C()
t1.children[4][0] = 1
t1.children[4][1] = 3

t1.children[5] = C()
t1.children[6] = C()
t1.children[6][0] = 4
t1.children[6][1] = 5

t1.root = 6

t2 = C()
t2.nodes[1]="a"
t2.nodes[2]="b"
t2.nodes[3]="d"
t2.nodes[4] = "c"
t2.nodes[5] ="e"
t2.nodes[6] ="f"

t2.children[1] =C()
t2.children[2] =C()
t2.children[3] =C()
t2.children[3][0] = 1
t2.children[3][1] = 2
t2.children[4] =C()
t2.children[4][0] = 3
t2.children[5] =C()
t2.children[6] = C()
t2.children[6][0] = 4
t2.children[6][1] = 5

t2.root = 6
'''
runPrints = False

def antitree(t1):
    subT = C()
    for k,a in t1.children:
        if a:
            tree = C(node = '', subtrees = [])
            tree.node = t1.nodes[k]
            for aa, v in a: 
                tree.subtrees.append(v)
        else:
            tree = t1.nodes[k]
        subT[k] = tree
    def putIn(subT,cur):
        if type(subT[cur])==str:
            return subT[cur]
        else:
            newsubtree = []
            for i in subT[cur].subtrees:
                newsubtree.append(putIn(subT,i))
            subT[cur] = C(node = subT[cur].node, subtrees = newsubtree)
                
        return subT[cur]
    return putIn(subT,t1.root)

def print1(*args):
    if runPrints:
        for i in args:
            print(i)
    
def getKeyroots(T):
    Keyroots = []
    for k,v in T.children:
        if len(v)>0:
            exclude = min(v.values())
        for kv, vv in v:
            if vv !=exclude:
                Keyroots.append(vv)
    Keyroots.append(max(T.nodes.keys()))
    return Keyroots

def getLeftMost(T,node):
    while len(T.children[node])>0:
        node = min(T.children[node].values())
    return node
    
def tdist(t1,t2):
    treedist = C()
    lastone = C()
    keyrootsT1 = getKeyroots(t1)
    keyrootsT2 = getKeyroots(t2)
    for s in range(0,len(keyrootsT1)):
        for t in range(0,len(keyrootsT2)):
            i = keyrootsT1[s]
            j = keyrootsT2[t]
            lastone = Treedist(i,j,t1,t2,treedist)
            
    
    return lastone

costs = context.context(i = 1, d = 1, s = 1)
def Treedist(pos1,pos2,t1,t2,treedist):#(i,j)
    print1(pos1,pos2)
    li = getLeftMost(t1,pos1)
    lj = getLeftMost(t2,pos2)
    bound1 = pos1 - li +2
    bound2 = pos2 - lj +2
    fdist = C()
        
    fdist[0][0] = 0
    for i in range(1,bound1):
        fdist[i][0] = fdist[i-1][0] +1 #+c[][] cost of inserting
    for j in range(1,bound2):
        fdist[0][j] = fdist[0][j-1] +1 #+c[][] cost of deleting 
    leni1 = pos1+1-li
    lenj1 = pos2+1-lj
    for i1 in range(1,leni1+1):
        for j1 in range(1,lenj1+1):
            k = li+i1-1
            l = lj+j1-1
            
            kk = k-1
            ll = l-1
            
            #also equivalence to saying i1 ==li and j1==lj
            if getLeftMost(t1,k)==li and getLeftMost(t2,l) == lj:
                if (i1-1) in fdist.keys() and j1 in fdist[i1-1].keys():
                    insert = fdist[i1-1][j1]+1
                else:
                    insert = costs.i
                
                if (i1) in fdist.keys() and (j1-1) in fdist[i1].keys():

                    delete = fdist[i1][j1-1]+costs.d
                else:
                    delete = 1

                if (i1-1) in fdist.keys() and (j1-1) in fdist[i1-1].keys():
                    swapmatch = fdist[i1-1][j1-1]+0
                else:
                    swapmatch = 0
                if t1.nodes[k]!=t2.nodes[l]:
                    swapmatch +=costs.s
                    
               
                fdist[i1][j1] = min(insert, delete, swapmatch)
               
                    
                treedist[k][l] = fdist[i1][j1]
                #print(i1,j1,t1.nodes[k],t2.nodes[l],":",insert,delete,swapmatch)
            else:
                if (i1-1) in fdist.keys() and j1 in fdist[i1-1].keys():
                    insert = fdist[i1-1][j1]+costs.i
                else:
                    insert = 1
                if (i1) in fdist.keys() and (j1-1) in fdist[i1].keys():
                    delete = fdist[i1][j1-1]+costs.d
                else:
                    delete = 1
                if (i1-1) in fdist.keys() and (j1-1) in fdist[i1-1].keys():
                    swapmatch = fdist[i1-1][j1-1] + treedist[k][l]
                else:
                    swapmatch = treedist[k][l]
               
    
                fdist[i1][j1] = min(insert, delete, swapmatch)
                
               
                #print(i1,j1,t1.nodes[k],t2.nodes[l],":",insert,delete,swapmatch)
            
    for a in fdist.keys():
        line = []
        for b in fdist[a].keys():
            line.append(fdist[a][b])
        print1(line)
    print1("\n treedist")
    print1(treedist)
    for a in sorted(treedist.keys()):
        line =[]
        for b in sorted(treedist[a].keys()):
            line.append(treedist[a][b])
        print1(line)
    print1("\n")
    return fdist
            
tree_dist = tdist(t1,t2)

def drawGrid(tree_dist,t1,t2):
    fixedGrid = []
    for a in sorted(tree_dist.keys()):
        line =[]
        for b in sorted(tree_dist[a].keys()):
            line.append(tree_dist[a][b])
        print(line)
        fixedGrid.append(line)
    return fixedGrid
    
def findPath(tree_dist,t1,t2):
    path = []
    maxi = max(t1.nodes.keys())
    maxj = max(t2.nodes.keys())
    i,j = 1,1
    #path.append(("start",(0,0)))
    while i!=maxi and j!=maxj:
        possibleMoves = C()
        if i+1<=maxi :#and tree_dist[i][j]+1==tree_dist[i+1][j]:
            move = C()
            move.op = "del"
            move.arg[0] = i+1
            possibleMoves.delete = tree_dist[i+1][j],(i+1,j),move
        else:
            possibleMoves.delete = None,None,None
            
        if j+1<=maxj:# and tree_dist[i][j]+1==tree_dist[i][j+1]:
            move = C()
            move.op = "ins"
            move.arg[0] = i
            move.arg[1] = t2.nodes[j+1]
            possibleMoves.insert = tree_dist[i][j+1],(i,j+1),move
        else:
            possibleMoves.insert = None,None,None
        if i+1<=maxi and j+1<=maxj:
            if t1.nodes[i+1]!=t2.nodes[j+1]:
                move = C()
                move.op = "sub"
                move.arg[0] = i+1
                move.arg[1] = t2.nodes[j+1]
                possibleMoves.sub = tree_dist[i+1][j+1],(i+1,j+1),move
                possibleMoves.match = None,None,None
            else:
                move = C()
                move.op = "match"
                move.arg[0] = i+1
                move.arg[1] = t2.nodes[j+1]
                possibleMoves.match = tree_dist[i+1][j+1],(i+1,j+1),move
                possibleMoves.sub = None,None,None
        
        lowestValue = None
        lowestValueMove = None
        for k,v in possibleMoves:
            if (k == "match" or k=="sub") and v[0]!=None:
                lowestValue = v[0]
                lowestValueMove = k,v[1],v[2]
                
            if v[0]!=None and (lowestValue==None or v[0]<lowestValue):
                lowestValue = v[0]
                lowestValueMove = k,v[1],v[2]
           
            
        if lowestValueMove!=None:
            i,j = lowestValueMove[1]   
            if lowestValueMove[0]!="match":
                path.append(lowestValueMove[2])
                
    return path  

drawGrid(tree_dist,t1,t2)
print("\n")
path = findPath(tree_dist,t1,t2)
print(path)
def implement(path,t1,t2):
    def findParent(t1,child):
        for parent,v in t1.children:
            if child in v.values():
                return parent
    for move in path:
        if move.op == "del":
            t1.nodes[move.arg[0]] =  ''
            parent = findParent(t1,move.arg[0])
            if parent!=None:
                removing = None
                newChildren = C()
                curLoc = 0
                for k,v in t1.children[parent]:
                    if v != move.arg[0]:
                        newChildren[curLoc] = v
                        curLoc+=1
                    else:
                        for kk,vv in t1.children[move.arg[0]]:
                            newChildren[curLoc] = vv
                            curLoc+=1
                t1.children[parent] = newChildren
                t1.children[move.arg[0]] = C()
            else:
                t1.root = t1.children[move.arg[0]][0]
        elif move.op=="ins":
            index =len(t1.nodes)+1
            t1.nodes[index] = move.arg[1]
            t1.children[index] = C()
            t1.children[index][0] = move.arg[0]
            parent = findParent(t1,move.arg[0])
            if parent!=None:
                newChildren = C()
    
                for k,v in t1.children[parent]:
                    if v != move.arg[0]:
                        newChildren[k] = v
                    else:
                        newChildren[k] = index
                t1.children[parent] = newChildren
            else:
                t1.root = t1.children[move.arg[0]][0]
        elif move.op =="sub":
            t1.nodes[move.arg[0]] = move.arg[1]
            
    return t1

t1 = implement(path,t1,t2)
print(t1)
fixedTree = antitree(t1)
print("fix treee",fixedTree)
print(antitree(t2))
                
'''
from zss import simple_distance, Node

A = (
    Node("c")
        .addkid(Node("b"))
    )
B = (
    Node("f")
        .addkid(Node("c")
            .addkid(Node("d"))
                .addkid(Node("a")
                .addkid(Node("b"))))
        .addkid(Node("e"))
    )
    
print(simple_distance(A, B))
'''              