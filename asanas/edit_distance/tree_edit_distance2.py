
import sys
sys.path.append("/Users/diva-oriane/Documents/GitHub/asanas/Parse/")

import contexttest as context
from parse3 import parse3 as parse
import random
import hashlib

C = context.context
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
    
#EXAMPLE:

def exampleSource():
    #input = [{'node': '^', 'subtrees': [{'node': 'A', 'subtrees': [{'node': 'L', 'subtrees': ['def']}, ' ', 'fg', '(', {'node': 'C', 'subtrees': ['A1', {'node': 'C', 'subtrees': ['A2',{'node': 'C', 'subtrees': '#'}]},{'node': 'C', 'subtrees': '#'}]}, ')', ':']}, ' ',{'node': 'B', 'subtrees': [{'node': 'L', 'subtrees': ['return']}, ' ', 'z']}]}]
    input = [{'node': '^', 'subtrees':[{'node': 'A','subtrees':[{'node':'L','subtrees':['def']},' ', 'fg','(',{'node':'@','subtrees':['A1']},',',{'node':'@','subtrees':['A2']},')']},{'node':'B','subtrees':[{'node':'L','subtrees':['return']},' ', 'z']}]}]
    #input = [{'node':'^','subtrees':['[',{'node':'@','subtrees':['f']},'(',{'node':'@','subtrees':['x']},')',']']}]
    return convertToContext(input)
    

def exampleTarget():
    #input = [{'node': '^', 'subtrees': [{'node': 'A', 'subtrees': [{'node': 'L', 'subtrees': ['def']}, ' ', 'f', '(', {'node': 'C', 'subtrees': ['A1',{'node': 'C', 'subtrees': '#'}]}, ')', ':']}, ' ',{'node': 'A', 'subtrees': [{'node': 'L', 'subtrees': ['def']}, ' ', 'g', '(', {'node': 'C', 'subtrees': ['A2',{'node': 'C', 'subtrees': '#'}]}, ')', ':']}, ' ',{'node': 'B', 'subtrees': [{'node': 'L', 'subtrees': ['return']}, ' ', 'z']},' ',{'node': 'B', 'subtrees': [{'node': 'L', 'subtrees': ['return']}, ' ', 'g']}]}]
    input = [{'node': '^', 'subtrees':[{'node': 'A','subtrees':[{'node':'L','subtrees':['def']}, ' ', 'f']},'(',{'node':'@','subtrees':['A1']},')',{'node': 'A','subtrees':[{'node':'L','subtrees':['def']}, ' ', 'g']},'(',{'node':'@','subtrees':['A2']},')',{'node':'B','subtrees':[{'node':'L','subtrees':['return']},' ', 'z']},{'node':'B','subtrees':[{'node':'L','subtrees':['return']},' ', 'g']}]}]

    return convertToContext(input)


    
print(exampleSource())
print(exampleTarget())
#FORMATING EXAMPLE 
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
                #for k,y in enumerate(ys):
                #    input.append((i+(j+k,),y))
                input.append((i+(j,),ys))
    
    
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
    
seen = []
def wrapper(Tsource,Ttarget):
    output = []
    for mm in ["del","ins","sub"]:
        for m in p(Tsource, Ttarget, mm):
            if Tsource.names[m.arg[0]]==Ttarget.names[m.arg[0]]:
                continue
            #print(m)
            #print(Ttarget)
            #print(len(m.arg[1].nodes))
            if (m.op == "ins" or m.op=="sub") and countNumAtLevel(Ttarget,m.arg[0])<len(m.arg[1].nodes):
                continue
            if (m.op=="ins" or m.op=="sub") and Ttarget.names[m.arg[0]]!= m.arg[1].names[shortest(m.arg[1].nodes)]:
                continue
                
            newsource = play(m,Tsource,Ttarget)
            s = (Tsource, m, newsource)
            s = str(s)
            if s in seen:
                continue
               
            seen.append(s)
            
            if newsource and str(newsource.names)!=str(Tsource.names):
                output += [(m,newsource)]
   
    return output 

def countNumAtLevel(T,loc):
    counter = 0
    for i in T.nodes:
        if i[0:len(loc)]==loc:
            #print(i)
            counter+=1
    return counter

def shortest(nodes):
    shortestLength = None
    shortestVal = None
    for i in nodes:
        if shortestLength==None or len(i)<shortestLength:
            shortestLength=len(i)
            shortestVal = i
    return shortestVal

def createSubTree(Ttarget,loc):
    Toutput = context.context(nodes = [], edges = context.context(), names = context.context())
    for nodein in Ttarget.nodes:
        if (len(loc)<len(nodein) and loc==nodein[:len(loc)]) or loc == nodein:
            Toutput.nodes.append(nodein)
            Toutput.names[nodein] = Ttarget.names[nodein]
            Toutput.edges[nodein] = Ttarget.edges[nodein]
    return Toutput
        

def difTree(T1,T2):
    dif = False
    if len(T2.nodes)!=len(T1.nodes):
        return True
    for n in T2.nodes:
        if T2.names[n]!=T1.names[n]:
            dif = True
    return dif
    
#CREATE NEXT MOVE TO TRY
def p(Tsource,Ttarget,mm):
    for loc in Tsource.nodes:
       
        if mm == "ins":
            done = []
            for loc2 in Ttarget.nodes:
                m = C()
                m.op = mm
                m.arg[0] = loc
                m.arg[1] = createSubTree(Ttarget,loc2)
                m.arg[2] = "before"
                
                doneE = (loc,loc2,"before")
                if doneE not in done:
                    yield m 
                done.append(doneE)
                
                if (len(loc)>0 and loc[:-1]+(loc[-1]+1,) not in Tsource.nodes): #or (len(loc)==0 and (0,) not in Tsource.nodes):
                    m = C()
                    m.op = mm
                    m.arg[0] = loc[:-1]+(loc[-1]+1,)
                    m.arg[1] = createSubTree(Ttarget,loc2)
                    m.arg[2] = "after"
                    doneE = (loc,loc2,"after")
                    if doneE not in done:
                        yield m 
                    done.append(doneE)
                
                    
        elif mm == "del":
            m = C()
            m.op = mm
            m.arg[0] = loc
            yield m
            
        elif mm == "sub":
            if loc in Ttarget.nodes:
                m = C()
                m.op = mm
                m.arg[0] = loc
                m.arg[1] = createSubTree(Ttarget,loc)
                #avoid useless step
                #if Tsource.names[loc]!=Ttarget.names[loc]:
                if difTree(m.arg[1],Tsource):
                    yield m
       
'''
eT22 = C()
eT22[(0,1)] = [(0,1,0), (0,1,1),(0,1,1,0)]
eT22[(0,1,1)] =  [(0,1,1,0)]
eT22[(0,1,0)] =  []
eT22[(0,1,1,0)] =  []
nT22 = C()
nT22[(0,1)] = "A" 
nT22[(0,1,0)]= "AA"
nT22[(0,1,1)]= "AB"
nT22[(0,1,1,0)]= "ABA"
T22 = C(nodes = [(0,1), (0,1,0), (0,1,1),(0,1,1,0)], edges = eT22, names =nT22 )
'''
def shiftStartIndex(startIndex,T):
    newT = C(nodes = [], edges = C(), names = C())
    min = -1
    oldstartIndex = 0
    for i in T.nodes:
        if min == -1 or len(i)<min:
            min = len(i)
            oldstartIndex = i
            
    convertNodes = C()
    for i in T.nodes:
        convertNodes[i] = (startIndex+i[len(oldstartIndex):])
        newT.nodes.append(convertNodes[i])
        newT.names[convertNodes[i]] = T.names[i]
        
    for e,v in T.edges:
        newT.edges[convertNodes[e]] = []
        for i in v:
            newT.edges[convertNodes[e]].append(convertNodes[i])
            
    return newT
        
    #(0,1), (0,1,0), (0,1,1),(0,1,1,0)
    #()
    #(),(0),(1,)(1,0)

    
#MAKE THE MOVE GIVEN (ADD,DEL,or INSERT)
def play(move,T,target):
    
    def shiftIndex(index,shift,x):
        
        if len(x)==0:
            treeoutput = (0,)
        elif len(index)==0 or (len(index)<=len(x) and x[:len(index)-1]==index[:len(index)-1] and index[len(index)-1]<=x[len(index)-1]):
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
            if len(x)>=len(index) and x[:len(index)]!=index:
                oldx = x
                x = shiftIndex(index,-1,oldx)
                newnodes.append(x)
                newedges[x] = T.edges[oldx]
                newnames[x] = T.names[oldx]
            elif len(x)<len(index):
                newnodes.append(x)
                newedges[x] = T.edges[x]
                newnames[x] = T.names[x]
                
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
        '''
        we add the elem at its index
        then want to shift over all indexes that have 
        '''
        
            
        index, added, updatednodes,addedname = addTree(index,addT,nodes)
        #this whole add things is really problematic.... 
        #what to shift the tree that was at that location over the whole subtree over 
        #updated nodes are wrong. 
        for x in updatednodes:
            
            #adding to newnodes too many times....
            if x==index:
                newnodes.append(x)
                newedges[x]=addelem
            

            if  (x[:len(index)]==index or (len(x)>=len(index) and x[len(index)-1]>index[-1]))and added==False:
                oldx = x
                #doing the shift correctly but onto a location that arleady exists.... so what do u do when it is already tehre ....
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
    
    
    if move.op == "del":
        Tnew = (walk_delsubtree(move.arg[0]))
        
    elif move.op == "ins":
        #addelem = context.context(node = "test", subtrees = [[["testsub"]]])
        #addT = subtrees(addelem,startIndex =move.arg[0])
        addT = shiftStartIndex(move.arg[0] ,move.arg[1] )    
        
        for k,v in addT.edges:
            if (Tnew.nodes,Tnew.edges) != (None,None):
                Tnew = walk_inssubtree(k,v,addT,Tnew.nodes,Tnew.edges,Tnew.names)
            else:
                Tnew = walk_inssubtree(k,v,addT)
        #to Increase Speed
        if len(Tnew.nodes)>len(target.nodes):
            return None
    elif move.op == "sub":
        
        #addelem = context.context(node = "test", subtrees = [[["testsub"]]])
        #addT = subtrees(addelem,startIndex = move.arg[0])
        addT = move.arg[1]
        #for sub move.arg[0] the location is irrelavent already taken into account with move.arg[1]
        
        for k,v in addT.edges:
            if (Tnew.nodes,Tnew.edges) != (None,None):
                Tnew = walk_subsubtree(k,v,addT,Tnew.nodes,Tnew.edges,Tnew.names)
            else:
                Tnew = walk_subsubtree(k,v,addT)
    
    return Tnew
    
def findinlist(input,value):
    if value not in input:
        return -1
    else:
        for ind,i in enumerate(input):
            if i == value:
                return ind 


def walk(source, target,depth = None,flat = False):
    g = context.context()
    q = [(source,target,[],[])]
    paths = []
    pathsm = []
    step = 0
    maxstep = 0
    donestep = 0
    otherpaths = []
    minpathLength = 0 

    
    while len(q)>0:
        donestep+=1
        if depth is not None:
            if step>maxstep:
                break
            step+=1
        #random.shuffle(q)
        s,t,p,pm = q.pop(0)
        if s in g.edges.keys():
            #if t in g.edges[s].keys():
            continue
        
        if minpathLength!=0 and len(p)>minpathLength:
            continue
        
        if difTree(s,t)==False:
            print(s)
            print(t)
            print("TRUE")

            if flat:
                p = p+[t]
            if minpathLength==0 or minpathLength>=len(p):
                minpathLength = len(p)
                paths.append(p)
                pathsm.append(pm)
            continue
        output = wrapper(s,t)
        #merge paths that have already been seen in output
        if depth is not None:
            if depth>0:
                maxstep += len(output)
                depth -=1
        for (e,n) in output:  
        
            #if not g.edges[s][n]:
            #print("source",s)
            #print("target",t)
            #print("operation",e)
            if flat:
                pp = (s)
            else:
                #if n equivalent not in p (regardless, nequiv)
                pp = (s,n)
            newpath = p+[pp]
            newpathm = pm +[e]
                        
            ok = True
            
            addnewpath = []
            for u,v in newpath:
                
                nextelem = u
                addnewpath.append(nextelem)
            
            nextelem = newpath[-1][1]
            addnewpath.append(nextelem)
            if minpathLength!=0 and minpathLength<len(newpath):
                ok = False
            if ok:
                for ppp in otherpaths:
                    particularCase = True
                    lastv = 0
                    numnotfound = 0
                    for ee in addnewpath:
                        f = findinlist(ppp,ee)
                        if f!=-1:
                            if (f == lastv+1 or f==lastv) and numnotfound>0:
                                ok = False
                                break
                            lastv = f
                            numnotfound = 0
                        else:
                            numnotfound+=1
            
            if ok:
                
                q.append((n,t,newpath,newpathm))
                g.edges[s][n][len(g.edges[s][n])]= e
                otherpaths.append(addnewpath)
            
        
    print("donestep",donestep)
    edges =0
    for i,v in g.edges:
        for n in v:
            edges+=len(n)
            
    print("numofedges", edges)
    return g,paths,pathsm



Texamplesource = exampleSource()
T1 = subtrees(Texamplesource, startIndex = ())
Texampletarget = exampleTarget()
T2 = subtrees(Texampletarget, startIndex = ())
g, p, pm=  walk(T1,T2)

sys.path.append("/Users/diva-oriane/Documents/GitHub/asanas/Graphics/")
from Task4Graphics import main as visualize

def visualizeTreePaths(p):
    def countByLevel(levelValues):
        
        output3 = context.context()
        startx =None 
        
        for i in levelValues:
            output3[i] = 0
            for j in levelValues:
                if len(i)+1 ==len(j) and (i == j[:len(i)] or (len(i)>1 and j[:(len(i)-1)]==i[:-1] and j[len(i)-1]>=i[-1]) ):
                    output3[i]+=1
                    
        output = context.context()
        for i in levelValues:
            if len(i) not in output.keys():
                output[len(i)] = [i]
            else:
                output[len(i)].append(i)
        output2 = context.context()
        
        outputnew = context.context()
        for k,v in output:
            
            weight = context.context()
            for x in v:
                w = 0
                for ii,i in enumerate(x):
                    w+=(10**(len(x)-ii))*(i+1)
                weight[w] = x
            newv = []
            while weight:
                nextOne = min(weight.keys())
                newv.append(weight[nextOne])
                weight.__delitem__(nextOne)
            outputnew[k] = newv

        output = outputnew
        for k,v in output:
            lastX = 0
            for i,x in enumerate(v):
                if x[:-1] in output2:
                    xOld,yOld = output2[x[:-1]]
                    if xOld>lastX:
                        xpos = xOld
                    else:
                        xpos = lastX + 50
                else:
                    xpos = lastX + 50
                output2[x] = (xpos,k*100)
                lastX = xpos
        
        startx = 0
        
        return startx,output2

    def drawATree(T,thenodes,theedges,shift,loc):
        startx, xyset = countByLevel(T.nodes)
        

        biggest = 0
        for n in T.nodes:
            
            x,y = xyset[n]
            x+=shift
            y+=100
            if n == loc:                
                thenodes[(n,shift)] = [T.names[n],x,y,"red"]
            else:
                thenodes[(n,shift)] = [T.names[n],x,y]
                
            if x+100>biggest:
                biggest = x+100
        for k,v in T.edges:
            for kk in v:
                if k == kk[:len(k)] and len(k) == len(kk)-1: #only draw edges between parents and children
                    theedges[len(theedges)] = [(thenodes[(k,shift)][1],thenodes[(k,shift)][2]),(thenodes[(kk,shift)][1],thenodes[(kk,shift)][2])]
        
        return thenodes,theedges,biggest
        
    theedges = C()
    thenodes = C()
    thetext = []
    shift = 100
    for i,pp in enumerate(p):
        thetext.append((str("path"+str(i)),shift,50))
        for ii,(u,v) in enumerate(pp):

            nextelem = u
            print(nextelem)
            thenodes,theedges,shift = drawATree(nextelem,thenodes,theedges,shift,pm[i][ii].arg[0])
            print(pm[i][ii])
            thetext.append((str(pm[i][ii].op),shift,50))
            nextelem = v
        print(nextelem)
        thenodes,theedges,shift = drawATree(nextelem,thenodes,theedges,shift,pm[i][ii].arg[0])
        tester = nextelem
    
    visualize(thenodes,theedges, thetext,True)

def printTree(source, target, tree, depth = 0):
    if type(tree)==list:
        
        for t in tree:
            printTree(source, target, t,depth+1)
            
    elif type(tree)==str:
        print("\t"*depth,tree)
     
    elif type(tree)==tuple:
        print("\t"*depth, tree)
            
        
    else:
        if "op" in tree:
    
            print("\t"*depth, tree.op)
            printTree(source, target, tree.arg,depth)
        elif "names" in tree:
            print("\t"*depth,str(tree.names))
            
       
            
def compresspaths(paths,source,target,option = True):
    names = C()
    def name(i):
        if i not in names[1].keys():
            v = len(names[0])
            names[0][v] = i
            names[1][i] = v
        else:
            v = names[1][i]
        return v
    def antiname(x):
        return names[0][x]
        
        
    g = C()
    for p in paths:
        for (i, j) in p:
            
            ni = name(i)
            nj = name(j)
            if ni==nj:
                pass
            else:
                g[ni][nj][len(g[ni][nj])] = True
    
    ns = name(source)
    nt = name(target)
    out = C()
    def at(cur,lookfor = "seq",depth=0):
        #print("\t"*depth, cur, lookfor)
        if len(g[cur])==0:
            x = antiname(cur)
            output = C(op = "seq",arg = [x])
        else:
            output = C()
            arg = []
            if lookfor=="seq":
                cur0 = cur
                arg = [antiname(cur0)]
                while len(g[cur0])==1:
                    xs = []
                    for k,v in g[cur0]:
                        xs.append(k)
                    x = xs[0]
                    y = antiname(x)
                    arg.append(y)
                    cur0 = x
                    
            # print(arg)
            # print("cur0,gcurc0",cur0,g[cur0])
                output.op = "seq"
                output.arg = arg
                        
                if len(g[cur0])>1:
                    #never reaches this .... 
                    newoutput= at(cur0,"choice",depth+1)
                    args = newoutput.arg
                    ops = [i.op == "seq" for i in args]
                    if all(ops):
                        ref  = args[0].arg[-1]
                        refs = [difTree(arg.arg[-1],ref)==False for arg in args]
                        refs0 = [arg.arg[-1] for arg in args]
                        #print("REFS",refs0, ref, all(refs))
                        if all(refs):
                            #print("newoutput1",newoutput)
                            #print("arg", args)
                            #args0 = [C(op = arg.op, arg = arg.arg[:-1] )for arg in args.arg]
                            newargs =[]
                            for arg in args:
                                x = arg.arg[:-1]
                                if len(x)==0:
                                    x = ["#"]
                                newargs.append(C(op = "seq", arg = x))
                                
                            args0 = C(op = newoutput.op, arg = newargs)
                            newoutput = [args0,ref]
                    
                    output.arg+=newoutput                
                    #output = newoutput
            else:
                op = "choice"
                argnew = [at(k,"seq",depth+1) for k,v in g[cur]]
                #if len(argnew)==1:
                #    output = argnew[0]
                #else:                    
                #print("argnew",argnew)
                #output = C( op = "seq", arg = [antiname(cur), C(op = op, arg = argnew)])
                output = C(op = op, arg = argnew)
            
        #print("\t"*depth, cur, lookfor, output)
        return output
        
    patternoption = C(
        op = "choice", 
        arg = [
            C(op = "seq", arg = ["#"]),
            C(op = "seq", arg = ["{option}"])
            ]
        )
        
    def clean(tree):
        
        if option:
            res = matchContext(patternoption,tree)
            if res:
                newtree = C(op = "option", arg = [res.option])
                tree = newtree
                            
        if type(tree)==str:
            return tree
        elif type(tree)==list:
            l = []
            for x in tree:
                l.append(clean(x))
            return l
        else:
            if tree.op == "seq" and len(tree.arg)==1:
                return tree.arg[0]
            else:
                newtree = C(op = tree.op , arg = [])
                for v in tree.arg:
                    newtree.arg.append(clean(v))
                return newtree
            
            
            
            
    tree = at(ns)
    print("tree",tree)
    print("\n")
    printTree(source, target,tree)
    #visualize(thenodes,theedges)
    #tree = clean(tree)
    #printTree(tree)    
    
    return g,names
    

            
#add To Visualizer 
#use space bar to slowly show each step ....

#compress paths TED

#SED visuallize compress path format ...

print("compresspaths")
g,names= compresspaths(p,T1,T2)
visualizeTreePaths(p)


