
import sys
sys.path.append("/Users/diva-oriane/Documents/GitHub/asanas/Parse/")

import contexttest as context
from parse3 import parse3 as parse
import random
import hashlib

'''
tree example:
[[[{'node': 'S', 'subtrees': [[[{'node': 'A', 'subtrees': [[['a']]]}, {'node': 'B', 'subtrees': [[['b']]]}]]]}]]]
'''
def example():
    AA = context.context(node = "AA", subtrees = [[["a"]]])
    A= context.context(node = "A", subtrees = [[[AA]]])
    B=context.context(node = "B", subtrees = [[["b","c","d"]]])
    S= context.context(node = "S", subtrees = [[[A,B]]])
    treeexample=[[[S]]]
    return treeexample

'''
def namesubtrees(Tree,depth = "()"):
    
    while type(Tree[0])==list:
        Tree = Tree[0]
        
    #preNode0 = preNode
    
    for k,elem in enumerate(Tree):
        yield(elem)
        #preNode = preNode0 
        if type(elem)==str:
            pass
            #print(preNode + [elem])
        else:
            #preNode = preNode+[elem.node]
            #allOptions.append(preNode+elem.subtrees)
            for kk,sub in enumerate(namesubtrees(elem.subtrees)):
                print(k,kk,sub)
                yield sub
'''

def convertList(Tree):
    while type(Tree)==list and len(Tree)==1:
        Tree = Tree[0]
    if type(Tree)!=list:
        Tree = [Tree]
    return Tree
    

def lensubtrees(subtrees,index=True):
    def helper(i):
        if type(i)==str:
            return 1
        else:
            next = convertList(i.subtrees)
            value = len(next)
            for ii in next:
                value += helper(ii)
            return value
        return(lengths)
        
    lengths = context.context()
    if index:
        for ind,i in subtrees:
            lengths[(ind,i)] = helper(i)
    else:
        for i in subtrees:
            lengths[i] = helper(i)
        
        
    return lengths

'''
def subtrees(Tree,mode = True,sort = True,index = True,localized = True,startIndex = ()):
    
    T = context.context(nodes = [], edges = context.context(), names = context.context())
    
    input = [(startIndex,Tree)]
    output = []
    associate = context.context()
    while len(input)>0:
        i,x = input.pop(0)

        xs = convertList(x)
        for j,x in enumerate(xs):
            if index:
                
                X = (i+(j,),x)                
            else:
                X = x
            X = [X]
            if mode:
                output = output+X
            else:
                output = X+output

            if type(x) in [str,int]:
                pass
            else:
                ys = x.subtrees
                for k,y in enumerate(ys):
                    input.append((i+(j+k,),y))
                
    
    
    if sort:
        lensub = lensubtrees(output)
        output = list(sorted(output,key=lensub))
    
    for i,k in output:
        if type(k)==str:
            T.names[i] = k
        else:
            T.names[i] = k.node
            
        T.edges[i] = k
        T.nodes.append(i)
        
        
    if localized:
        localizededges = context.context()
        for i,k in output:
            localizededges[i] = lookForSub(i,T.nodes)
        
        T.edges = localizededges
    
    return T  
'''
    
def subtrees(Tree,mode = True,sort = True,index = True,localized = True,startIndex = ()):
    
    T = context.context(nodes = [], edges = context.context(), names = context.context())
    while type(Tree)==list:
        Tree = Tree[0]
        
    input = [(startIndex,Tree.subtrees)]
    output = [(startIndex,Tree)]
    
    while len(input)>0:
        i,x = input.pop(0)

        xs = convertList(x)
        for j,x in enumerate(xs):
            if index:
                
                X = (i+(j,),x)                
            else:
                X = x
            X = [X]
            if mode:
                output = output+X
            else:
                output = X+output

            if type(x) in [str,int]:
                pass
            else:
                ys = x.subtrees
                for k,y in enumerate(ys):
                    input.append((i+(j+k,),y))
                
    
    
    if sort:
        lensub = lensubtrees(output)
        output = list(sorted(output,key=lensub))[::-1]
    
    for i,k in output:
        if type(k)==str:
            T.names[i] = k
        else:
            T.names[i] = k.node
            
        T.edges[i] = k
        T.nodes.append(i)
        
        
    if localized:
        localizededges = context.context()
        for i,k in output:
            localizededges[i] = lookForSub(i,T.nodes)
        
        T.edges = localizededges
    
    return T 
        
def lookForSub(index,output0):
    children = []
    for x in output0:
        if x[:len(index)]==index and x!=index:
            children.append(x)
    return children

def implicitRep(output,output0):
    implicitoutput = context.context()
    
    for k,v in output:
        if type(v)==str:
            implicitoutput[k] = context.context(node = v)
        else:
            implicitoutput[k] = context.context( node = v.node, subtrees = [])
            for kk in output0:
                if kk[:len(k)]==k and kk!=k and len(kk)==len(k)+1:
                    implicitoutput[k].subtree.append(kk)
    return implicitoutput
        
def trees2nodes(output,output0):
    #extentional representation
    extentionaloutput = context.context()
    for i,k in output:
        extentionaloutput[i] = [i]+lookForSub(i,output0)
    
    return extentionaloutput

treeexample = example()
T = subtrees(treeexample, startIndex = ())

def generateOps(Tree):
    moves = []
    for tree in Tree.nodes:
        move = context.context()
        move.op  = "del"
        move.op = "ins"
        move.op = "sub"
        move.arg[0] = tree
        moves.append(move)
    
    return moves

def generateGraph(treeexample):
    def index(x):
        y = hashlib.sha256(str(x).encode()).hexdigest()[:6]
        return y 
    oldTree = subtrees(treeexample,startIndex = ())
    moves = generateOps(oldTree)
    graph = context.context()
    for m in moves:
        newTree = play(m,oldTree)
        foldTree = index(oldTree)
        fnewTree = index(newTree)
        graph.edges[foldTree][fnewTree] = m
        graph.index[foldTree] = oldTree
        graph.index[fnewTree] = newTree
    return graph

def play(move,T):
    
    def shiftIndex(index,shift,x):
        if len(index)<=len(x) and x[:len(index)-1]==index[:len(index)-1] and index[len(index)-1]<=x[len(index)-1]:
            x = list(x)
            x = tuple(x[:len(index)-1]+[x[len(index)-1]+shift]+x[len(index):])
            treeoutput = x
        else:
            treeoutput = x
        return treeoutput 
        
    
    def addTree(index,addT,nodes = T.nodes):
        newnodes = nodes
        added = False
        addedname = None
        if index not in nodes: 
            addindexname = addT.names[index]
            added = True

            parent = index[:-1]
            while parent not in nodes:
                parent = parent[:-1]
            preLastC = None
            LastC = tuple(list(parent)+[0])
        
            while LastC in nodes:
                preLastC = LastC
                LastC = tuple(list(LastC[:-1])+[LastC[-1]+1])
                
            index = LastC
                
            location = 0

            newnodes = [None]*(len(nodes)+1)
            for k,t in enumerate(nodes):
                newnodes[location] = t

                if (t == parent and preLastC==None) or (t==preLastC):
                    location+=1
                    newnodes[location] = index
                location+=1
            
            addedname = (index,addindexname)
        
        return index, added, newnodes,addedname
        
    def editSubtreesImplicit(newedges):
        for k,v in newedges:
            newedges[k] = lookForSub(k,list(newedges.keys()))
        return newedges
                
    def walk_delsubtree(index):
        Tupdate = context.context()
        newnodes = []
        newedges = context.context()
        newnames = context.context()
        for x in T.nodes:
            if x[:len(index)]!=index:
                oldx = x
                x = shiftIndex(index,-1,oldx)
                newnodes.append(x)
                newedges[x] = T.edges[oldx]
                newnames[x] = T.names[oldx]
        newedges = editSubtreesImplicit(newedges)
        Tupdate.nodes=newnodes
        Tupdate.edges = newedges
        Tupdate.names = newnames
        return Tupdate
    
    def walk_inssubtree(index,addelem,addT,nodes=T.nodes,edges=T.edges,names = T.names):
        Tupdate = context.context()
        newnodes = []
        newedges = context.context()
        newnames = context.context()
        index, added, updatednodes,addedname = addTree(index,addT,nodes)
        for x in updatednodes:
            if x==index:
                newnodes.append(x)
                newedges[x]=addelem
            if x[:len(index)]==index and added==False:
                oldx = x
                x = shiftIndex(index,1,oldx)
                newnodes.append(x)
                newedges[x] = edges[oldx]
                newnames[x] = names[oldx]
            elif x!=index:
                newnodes.append(x)
                newedges[x] = edges[x]
                newnames[x] = names[x]
        if added:
            newnames[addedname[0]] = addedname[1]
        else:
            newnames[index] = addT.names[index]
            
        newedges = editSubtreesImplicit(newedges)
        Tupdate.nodes=newnodes
        Tupdate.edges = newedges
        Tupdate.names = newnames
        return Tupdate
    
    def walk_subsubtree(index,addelem,addT, nodes = T.nodes,edges = T.edges,names = T.names):
        Tupdate = context.context()
        newnodes = []
        newedges = context.context()
        newnames = context.context()
        index, added, updatednodes,addedname = addTree(index,addT,nodes)
        for x in updatednodes:
            if x[:len(index)]!=index:
                newnodes.append(x)
                newedges[x] = edges[x]
                newnames[x] = names[x]
            elif x == index:
                newnodes.append(x)
                newedges[x] = addelem
                
        if added:
            newnames[addedname[0]] = addedname[1]
        else:
            newnames[index] = addT.names[index]
            
        newedges = editSubtreesImplicit(newedges)
        Tupdate.nodes=newnodes
        Tupdate.edges = newedges
        Tupdate.names = newnames
        return Tupdate  
        
    
    Tnew = context.context(nodes = None, edges = None, names = None)
    
    #print("old nodes")
    #print(T.nodes)
    #print("old edges")
    #print(T.edges)
    #print("old names")
    #print(T.names)
    #print("\n")
    
    #print("index:", move.arg[0])
    
    if move.op == "del":
        Tnew = (walk_delsubtree(move.arg[0]))
        
    elif move.op == "ins":
        addelem = context.context(node = "test", subtrees = [[["testsub"]]])
        addT = subtrees(addelem,startIndex =(2,))
        for k,v in addT.edges:
            if (Tnew.nodes,Tnew.edges) != (None,None):
                Tnew = walk_inssubtree(k,v,addT,Tnew.nodes,Tnew.edges,Tnew.names)
            else:
                Tnew = walk_inssubtree(k,v,addT)
    
    elif move.op == "sub":
        
        addelem = context.context(node = "test", subtrees = [[["testsub"]]])
        addT = subtrees(addelem,startIndex =(2,))
        for k,v in addT.edges:
            if (Tnew.nodes,Tnew.edges) != (None,None):
                Tnew = walk_subsubtree(k,v,addT,Tnew.nodes,Tnew.edges,Tnew.names)
            else:
                Tnew = walk_subsubtree(k,v,addT)
      
    #print("newnodes")
    #print(Tnew.nodes)
    #print("\n")
    #print("newedges")
    #print(Tnew.edges)
    #print("newnames")
    #print(Tnew.names)
    #print("\n")
    
    return Tnew

            

treeexample = example()    
G = generateGraph(treeexample)

for k,v in G.edges:
    for k1,v1 in v:
        if v1.arg[0] == (0,0):
            print(k,k1,v1)
            print(G.index[k1])
            
            
#update names part of the tree too 

