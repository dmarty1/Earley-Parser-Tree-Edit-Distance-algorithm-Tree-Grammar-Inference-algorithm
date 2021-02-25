#string edit distance

import sys
sys.path.append("/Users/diva-oriane/Documents/GitHub/asanas/Parse/")

import contexttest as context
from parse3 import parse3 as parse
import random

costs = context.context(i = 1, d = 1, s = 1)
C = context.context

def matchContext(x,y):
    def aux(x,y):
        
        tx = str(type(x))
        ty = str(type(y))
        if tx==ty:
            if tx==str(type(C())):
                kx = list(x.keys())
                ky = list(y.keys())
                if kx == ky:
                    c = C()
                    for k in kx:
                        fl,cc = aux(x[k],y[k])
                        if fl:
                            c+=cc
                        else:
                            return False, C()
                    return True, c
                     
                else:
                    return False, C()
            elif type(x)==list:
                if len(x)==len(y):
                    c = C()
                    z = zip(x,y)
                    for u,v in z:
                        fl,cc = aux(u,v)
                        if fl:
                            c+=cc
                        else:
                            return False, C()
                    return True, c
        
                else:
                    return False, C()
            elif type(x)==str:
                c = parse(x,y,"{","}")
                return True, c
            else:
                return x==y, C()
            
        else:
            return False, C()
    fl, c = aux(x,y)
    return c
    
    
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

'''
def allPaths(m,n,E,paths = []):
    nodes = []
    for i in range(0,m+1):
        for j in range(0,n+1):
            nodes.append((i,j))
    print(nodes)
    
    edges = []
    for (i,j) in nodes:
        weight = -1
        if i<(m):
            if type(E[i+1][j][0])==int and type(E[i][j][0])==int:
                cn = [(i,j),(i+1,j)]
                if weight==0:
                    e = context.context(node = cn,weight = weight,op = "no move")
                    edges.append(e)
                elif weight==1:
                    e = context.context(node = cn,weight = weight, op = "del")
                    edges.append(e)
                    
        if j<(n):
            if type(E[i][j+1][0])==int and type(E[i][j][0])==int:
                weight = E[i][j+1][0]-E[i][j][0]
                cn = [(i,j),(i,j+1)]
                if weight==0:
                    e = context.context(node = cn,weight = weight,op = "no move")
                    edges.append(e)
                elif weight==1:
                    e = context.context(node = cn,weight = weight,op = "ins")
                    edges.append(e)
        
        if i<(m) and j<(n):
            if type(E[i+1][j+1][0])==int and type(E[i][j][0])==int:
                weight = E[i+1][j+1][0]-E[i][j][0]
                cn = [(i,j),(i+1,j+1)]
                if weight==0:
                    e = context.context(node = cn,weight = weight, op = "match")
                    edges.append(e)
                elif weight==1:
                    e = context.context(node = cn,weight = weight, op = "sub")
                    edges.append(e)
                    
    print("edges")
    print(edges)
'''
'''
def paths(source,target):
    print(source, target)
    targetC = context.context()
    sourceC = context.context()
    
    for ki,i in enumerate(target):
        if i in targetC:
            targetC[i].count +=1
            #targetC[i].loc.add()
        else:
            targetC[i].count = 1
            #targetC[i].loc ={ki}
    for kj,j in enumerate(source):
        if j in sourceC:
            sourceC[j].count +=1
            #sourceC[j].loc.add(kj)
        else:
            sourceC[j].count = 1
            #sourceC[j].loc ={kj}
        
    output = []
    for i in targetC.keys():
        if i not in sourceC.keys() :#or (i in sourceC.keys() and sourceC[i].count<targetC[i].count):
            for loc in range(0,len(source)+1):
                sourcenew = source[:loc]+i+source[loc:]
                output+=["insert",loc,i]
                if sourcenew==target:
                    return output
                else:
                    output+= paths(sourcenew,target)
                    
    for j in sourceC.keys():
        if j not in targetC.keys() :#or(j in targetC.keys() and sourceC[j].count>targetC[j].count):
            for loc in range(0,len(source)):
                if source[loc]==j:
                    sourcenew = source[0:loc]+source[loc+1:]
                    output+=["delete",loc]
                    if sourcenew == target:
                        return output
                    else:
                        output+=paths(sourcenew,target)

    for i in targetC.keys():
        for loc in range(0,len(source)+1):
            sourcenew = source[:loc]+i[0]+source[loc:]
            output+=["insert",loc,i]
            if sourcenew==target:
                return output
            else:
                output+= paths(sourcenew,target)
               

    
    #how to take care of the matching....
    return output
'''


def convertST(source, target):
    ref = C()
    for i,s in enumerate(source):
        ref[(0,i)] = s
    for j,t in enumerate(target):
        ref[(1,j)] = t
    
    source = tuple((0, x) for x in range(len(source)))
    target = tuple((1, x) for x in range(len(target)))
    
    return source, target, ref


seen = []

def wrapper(source,target, oldValue):
    #source = tuple([(0, x) for x in range(len(source))])
    #target = tuple([(1, x) for x in range(len(target))])
    output = []
    for mm in ["del","ins","sub"]:
        for m in p(source, target, mm, oldValue):
            newsource = move(source,target,m)
         
            
            s = (source, m, newsource)
            s = str(s)
            if s in seen:
                continue
               
            seen.append(s)
            
            if newsource and newsource!=source:
                output += [(m,newsource,convertword(oldValue,newsource))]
   
    return output 

def convertword(oldValue,w):
    asword = ""
    for i in w:
        asword+=oldValue[i]
    return asword
    
    
            
def p(source,target,mm, oldValue):
    for i,loc in enumerate(source):
       
        if mm == "ins":
            done = []
            for loc2 in target:
                m = C()
                m.op = mm
                m.arg[0] = loc
                m.arg[1] = loc2
                m.arg[2] = "before"
                
                doneE = (loc,oldValue[loc2],"before")
                if doneE not in done:
                    yield m 
                done.append(doneE)
                if i==len(source)-1:
                    m = C()
                    m.op = mm
                    m.arg[0] = loc
                    m.arg[1] = loc2
                    m.arg[2] = "after"
                    doneE = (loc,oldValue[loc2],"after")
                    if doneE not in done:
                        yield m 
                    done.append(doneE)
                    
        elif mm == "del":
            m = C()
            m.op = mm
            m.arg[0] = loc
            yield m
        elif mm == "sub":
            if i <len(target):
                loc2 = target[i]
                m = C()
                m.op = mm
                m.arg[0] = loc
                m.arg[1] = loc2
                #avoid useless step
                if oldValue[loc]!=oldValue[loc2]:
                    yield m
            
            
    

def move(source,target,m):
        
        #print("\t",loc)
        #0 for source, 1 for target in source new
    sourcenew = None

    if m.op == "del":
        sourcenew = []
        for v in source:
            if v != m.arg[0]:
                sourcenew.append(v)
        sourcenew = tuple(sourcenew)

        #print("\t"*2,sourcenew)

    elif m.op == "ins":
        sourcenew = []
        for v in source:
            if v==m.arg[0] and "before"==m.arg[2]:
                sourcenew.append(m.arg[1])
            sourcenew.append(v)
            if v==m.arg[0] and "after" == m.arg[2]:
                sourcenew.append(m.arg[1])
        sourcenew = tuple(sourcenew)
        
        #this case reduces the time significantly 
        if len(sourcenew)>len(target):
            sourcenew = None
            

        
    elif m.op == "sub":
        sourcenew = []
        for v in source:
            if v !=m.arg[0]:
                sourcenew.append(v)
            else:
                sourcenew.append(m.arg[1])

        sourcenew = tuple(sourcenew)
        
    return sourcenew

def findinlist(input,value):
    if value not in input:
        return -1
    else:
        for ind,i in enumerate(input):
            if i == value:
                return ind 

def walk(source, target,depth = None,flat = False):
    
    source0, target0, oldValue = convertST(source, target)
    print(oldValue)
    g = context.context()
    q = [(source0,target0,[])]
    paths = []
    step = 0
    maxstep = 0
    donestep = 0
    otherpaths = []
    minpathLength = 0 
    edgekeysconvert = set()
    wordsConvert = C()
    wordsConvert[source0] = source
    wordsConvert[target0] = target
    
    while len(q)>0:
        donestep+=1
        if depth is not None:
            if step>maxstep:
                break
            step+=1
        #random.shuffle(q)
        s,t,p = q.pop(0)
        
        
        if wordsConvert[s] in edgekeysconvert:
            continue
        '''
        if s in g.edges.keys():
            #if t in g.edges[s].keys():
            continue
        '''
      
        if wordsConvert[s] == wordsConvert[t]:
        #if s ==t:
            if flat:
                p = p+[t]
            if minpathLength==0 or minpathLength>=len(p):
                minpathLength = len(p)
                paths.append(p)
            continue
        output = wrapper(s,t, oldValue)
        if depth is not None:
            if depth>0:
                maxstep += len(output)
                depth -=1
        for (e,n,nasword) in output:
            #if not g.edges[s][n]:
            
            wordsConvert[n] = nasword
            if flat:
                pp = (s)
            else:
                #if n equivalent not in p (regardless, nequiv)
                pp = (s,n)
            newpath = p+[pp]
                        
            ok = True
            
            addnewpath = []
            for u,v in newpath:
                
                nextelem = wordsConvert[u]
                addnewpath.append(nextelem)
            
            nextelem = wordsConvert[newpath[-1][1]]
            addnewpath.append(nextelem)
            
            if minpathLength!=0 and minpathLength<len(newpath):
                ok = False
            if ok:
                for ppp in otherpaths:
                    particularCase = True
                    lastv = 0
                    numnotfound = 0
                    for e in addnewpath:
                        f = findinlist(ppp,e)
                        if f!=-1:
                            if (f == lastv+1 or f==lastv) and numnotfound>0:
                                ok = False
                                break
                            lastv = f
                            numnotfound = 0
                        else:
                            numnotfound+=1
            
            if ok:
                
                q.append((n,t,newpath))
                g.edges[s][n][len(g.edges[s][n])]= e
                edgekeysconvert.add(wordsConvert[s])
                otherpaths.append(addnewpath)
            
        
    print("donestep",donestep)
    edges =0
    for i,v in g.edges:
        for n in v:
            edges+=len(n)
            
    print("numofedges", edges)
    return g,paths

sys.path.append("/Users/diva-oriane/Documents/GitHub/asanas/Graphics/")
from Task4Graphics import main as visualize

theedges = C()
thenodes = C()
A = C(x=10,y=10,prev = None)

def printTree(source, target, tree, depth = 0, convert = True):
    A.x = depth*50
    if type(tree)==list:
        
        for t in tree:
            printTree(source, target, t,depth+1)
            
    elif type(tree)==str:
        print("\t"*depth,tree)
        thenodes[tree] = (str(tree),A.x,A.y)
        if A.prev!=None:
            theedges[len(theedges)]= ((thenodes[A.prev][1],thenodes[A.prev][2]),(thenodes[tree][1],thenodes[tree][2]))
        A.y +=40
        A.prev = tree
    elif type(tree)==tuple:
        if convert:
            print("\t"*depth, tree, convertToRead(source, target, tree))
            thenodes[tree] = (convertToRead(source, target, tree),A.x,A.y)
                    
            if A.prev!=None:
                theedges[len(theedges)]= ((thenodes[A.prev][1],thenodes[A.prev][2]),(thenodes[tree][1],thenodes[tree][2]))
            A.prev = tree
            
            A.y +=40
        else:
            print("\t"*depth, tree)
            thenodes[tree] = (str(tree),A.x,A.y)
            if A.prev!=None:
                theedges[len(theedges)]= ((thenodes[A.prev][1],thenodes[A.prev][2]),(thenodes[tree][1],thenodes[tree][2]))
            A.prev = tree
            A.y +=40
        
    else:
        print("\t"*depth, tree.op)
        if tree.op == "seq":
            A.y+=40
    
        printTree(source, target, tree.arg,depth)
       



def convertToRead(source,target,e):
    eword = ""
    for (st, ind) in e:
        if st==0:
            eword+=source[ind]
        else:
            eword+=target[ind]
    return eword
            
def compresspaths(paths,source,target,option = True):
    source0, target0, oldValue = convertST(source, target)
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
            #ii = convertToRead(source,target, i)
            #jj = convertToRead(source,target,j)
            #print(i,ii,j,jj)
            ni = name(i)
            nj = name(j)
            if ni==nj:
                pass
                #print("CASE",ni,nj,ii,jj,i,j)
            else:
                g[ni][nj][len(g[ni][nj])] = True
    
    ns = name(source0)
    nt = name(target0)
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
                        refs = [convertToRead(source,target,arg.arg[-1])==convertToRead(source, target, ref) for arg in args]
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
    visualize(thenodes,theedges)
    #tree = clean(tree)
    #printTree(tree)
        
        
            
    
    
    return g,names


    
uv = "abcd","ab"
uv = "exponential","polynomial"
uv = "snowy","sunny"
uv = "abcd","dcba"
uv = "abc","cbde"


#ed, cost, path = editDistance(*uv)

source = "snowy"
target = "sun"
#random.seed(1)
g, p=  walk(source,target)

'''
theedges = C()
thenodes = C()
x = 20
y = 20
for k,v in g.edges:
    x=20
    if k not in thenodes:
        thenodes[k] = [convertToRead(source,target,k),x,y]
    y+=20
    for kk,vv in v:
        
        if kk not in thenodes:
            thenodes[kk] = [convertToRead(source,target,kk),x,y]
            theedges[len(theedges)]= ((thenodes[k][1],thenodes[k][2]),(thenodes[kk][1],thenodes[kk][2]))
            x+=100
    y+=50
    
sys.path.append("/Users/diva-oriane/Documents/GitHub/asanas/Graphics/")
from Task4Graphics import main as visualize

#visualize(thenodes,theedges)
'''

'''
for k,v in g.edges:
    for kk, vv in v:
        #print(k,vv)
        print("k",convertToRead(source,target,k),"kk",convertToRead(source,target,kk), vv)
'''

q = p

print("walk done")
'''
for pp in q:
    output = []
    for u,v in pp:
        nextelem = convertToRead(source, target, u)
        if nextelem in output:
            print("double",nextelem)
        output += [ nextelem]
        
    output+= [convertToRead(source, target, pp[-1][1])]
    output = " ".join(output)
    print(output)
'''
def findinlist(input,value):
    if value not in input:
        return -1
    else:
        for ind,i in enumerate(input):
            if i == value:
                return ind 

for pp in q:
    output = []
    for u,v in pp:
        nextelem = convertToRead(source, target, u)
        output += [nextelem]
        nextelem = convertToRead(source, target, v)
    output+= [nextelem]
    #output = " ".join(output)
    print(output, len(output))
    for ppp in q:
        if ppp !=pp:
            outputother = []
            found = []
            for u,v in ppp:
                nextelem = convertToRead(source, target, u)
                found.append(findinlist(output,nextelem))
                outputother += [nextelem]
                nextelem = convertToRead(source, target, v)
            found.append(findinlist(output,nextelem))
            outputother+= [nextelem]
            #outputother = " ".join(outputother)
            #print("\t",found)
            particularCase = True
            for i in range(len(output)):
                if i not in found:
                    particularCase = False
            if particularCase:
                if -1 not in found[:-1]:
                    particularCase = False
                
            if particularCase:
                print("\t",found)
                print("\t",outputother)
        
    

print("\n")

g,names= compresspaths(q,source,target)

#print(names)
#print("graph",g)

#for k,v in g:
#    for kk, vv in v:
#        print(k,names[0][k],kk,names[0][kk])