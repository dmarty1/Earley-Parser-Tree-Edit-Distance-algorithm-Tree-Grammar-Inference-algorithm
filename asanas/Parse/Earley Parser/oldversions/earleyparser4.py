

import contexttest as context
import random
from itertools import permutations 
import scipy.optimize as O
import numpy as N
import matplotlib.pyplot as plt
import time

    
#MAIN LOOP
'''
i = end
j = start
'''
debug = False

def Debug(cast=None,active = True):
    
    def h(f):
        
        def g(*args,**kwargs):
            depth = 0 
            if "depth" in kwargs:
                depth = kwargs["depth"]
            if active:
                print("\t"*depth,f,args,kwargs)
            y = f(*args,**kwargs)
            z = y 
            if cast:
                z = cast(z)
                y = z
            if active:
                print("\t"*depth,f,args,kwargs,z)
            return y 
        return g
    return h
        
    
def print1(*args,**kwargs):
    if debug:
        print(*args,**kwargs)
        
def main(A,S,words,L,setC,S2):
    
    def atomic(words):
        Atomic = context.context()
        alphabet = ["α","β","Γ","γ","Δ","δ","ε","ζ","η","θ","λ","μ","ν","Ξ","ξ","π","ρ","Σ","σ","ς","τ","υ","Φ","χ","Ψ","Ω","ω"]        
            
        alphabetedited = []
        for a in alphabet:
            if a not in words:
                alphabetedited.append(a)
        
        lmapped = {}
        for i in L.values():
            lmapped[i] = alphabetedited[0]
            alphabetedited = alphabetedited[1:]
            
    
        for i in range(len(words)):
            for v in L.values():
                if i+len(v)<=len(words) and words[i:i+len(v)] ==v:
                    Atomic[(i,i+len(v)-1)] = (v,lmapped[v])
        return Atomic
    
    Atomic = atomic(words)
    
    def convertWordWithAtomic(words):
        Atomic = atomic(words)
        word = str(words)
        for (a,b) in Atomic.values():
            word = word.replace(a,b)
            A[len(A)]= "L",b
        return word 
    

    words = convertWordWithAtomic(words)
  
    def nullablenew():
        newlableset = ["#"]
        flag = True
        while flag:
            flag = False
            for k,i in A:
                ok = True
                for x in i[1]:
                    if x not in newlableset:
                        ok = False
                if ok:
                    if i[0] not in newlableset:
                        newlableset.append(i[0])
                        flag = True
                
        return newlableset
        

    def nullable(symbol):
        return symbol in nullablenew()
    
        
    def target(es):
        if es.it < len(A[es.ir][1]):
            return A[es.ir][1][es.it]
        else:
            return False
    
    def compare(ns0,ns1):
        return (ns0.ir,ns0.it,ns0.m) == (ns1.ir,ns1.it,ns1.m)
    
    def in2(ns,nslist):
        for n in nslist:
            if compare(n,ns):
                return True
        return False
        
    def convertAndSI(end,start,elem):
        w = []
        c = 0
        for g in range(len(A[elem.ir][1])+1):
            if g==elem.it:
                w.append("$")
            if g<len(A[elem.ir][1]):
                w.append(A[elem.ir][1][g])
        line = str(start)+","+str(end)+" "+A[elem.ir][0]+"=>"+A[elem.ir][1]+" "+ "".join(w)+", "+str(elem.m)
        
        for (k1,k2),(v1,v2) in Atomic:
            line = line.replace(v2,v1)
        print1(line)
            
    
    
    def getNullK(B):
        for k,i in A:
            if i[0] == B:
                if i[1] == "#":
                    return k
    def predictorepsilon():
                
        modify = False
        add = []
        for end,Se in S:
            for start,Ses in Se:
                for es in Ses:
                    B = target(es)
                    if B!=False:
                        if nullable(B):
                            ns = context.context(
                                ir = es.ir,
                                it = es.it+1,
                                m = ["predictorepsilon"],
                            
                            )
                            add.append((end,start,ns,es))
                        if B == "@":
                            ns = context.context(
                                ir = es.ir,
                                it = es.it,
                                m = ["predictor@"],
                            
                            )
                            add.append((end,end,ns,es))
                        else:
        
                            for k,v in A:
                                if v[0] == B:
                                    ns = context.context(
                                        ir = k,
                                        it = 0,
                                        m = ["predictor"],
                                    
                                    )
                                    add.append((end,end,ns,es))
    
                            
        
        for end,start,ns,es in add:
            if start not in S[end]:
                S[end][start] = []
            if not in2(ns,S[end][start]):
                S[end][start].append(ns)
                modify = True
        return modify
    
    def init():
        start = 0
        end = 0
        S[end] = context.context()
        S[end][start] = []
        ns = context.context(
                ir = 0,
                it = 0,
                m = ["start"],
            )
        S[end][start].append(ns)

   
    
    
    def scanner():
        modify = False
        add = []
        for end,Se in S:
            for start,Ses in Se:
                for es in Ses:
                    B = target(es)  
                    if B!=False:
                        if (end<len(words) and (B=="@") and words[start] in setC):
                            new =0
                            while start+new <(len(words)) and words[start+new] in setC:
                                new +=1
                                                
                            ns = context.context(
                                ir = es.ir,
                                it = es.it+1,
                                m = ["scanner@"]
                            )
                            add.append((end+new,start,ns))
                        
                        elif (end<len(words) and ( B=="&") and words[start] in setC):
                            
                            ns = context.context(
                                ir = es.ir,
                                it = es.it+1,
                                m = ["scannerC"]
                            )
                            add.append((end+1,start,ns))
                        elif  (end<len(words) and (B == words[end] )):
                            ns = context.context(
                                ir = es.ir,
                                it = es.it+1,
                                m = ["scanner"]
                            )
                            add.append((end+1,start,ns))
                        
                        
                        
                        
                        
        for end,start,ns in add:
            if end not in S:
                S[end]=context.context()
            if start not in S[end]:
                S[end][start] = []
            if not in2(ns,S[end][start]):
                S[end][start].append(ns)
                modify = True
        return modify
        
        #need to big really fixed ....
    def completer():
        modify = False
        add = []
        print1(S)
        print(S)
        for end,Se in S: 
            for start,Ses in Se:
                for es in Ses:
                    B= target(es)
                    if B==False or B=="@":
                        for jj, Sjj in S[start]:
                            for elem in Sjj:
                                if target(elem)==False:
                                    pass
                                else:
                                    addition = 1
                                    for k,v in L:
                                        if A[elem.ir][1]==v:
                                            addition = len(v)
                                    ns = context.context(
                                        ir = elem.ir,
                                        it = elem.it+addition,
                                        m = ["completer"]
                                    )
                                    if ns.it <= len(A[ns.ir][1]):
                                        add.append((end,jj,ns,es))
                                            
                                        
                    
                
        for end,jj,ns,es in add:
            if jj not in S[end]:
                S[end][jj]=[]
            if not in2(ns,S[end][jj]):
                S[end][jj].append(ns)
                modify = True
        return modify
        
    
    def indexes(S):
        index = context.context()
        for end in S.keys():
            for start,Ses in S[end]:
                for es in Ses:
                    if (es.m == ["completer"] or es.m == ["scanner"]or es.m==["scannerC"] or es.m ==["scanner@"]):
                        st = (start,end)
                        if es.m==["scanner"] or es.m==["scannerC"]:
                            st = (end-1,end)
    
                        if st not in index:
                            index[st] = []
                        index[st].append(es)
        return index
    
    

    
    def indexes2(S):
        index = context.context()
        for end in S.keys():
            for start,Ses in S[end]:
                for es in Ses:
                    st = (start,end)
                    if es.m==["scanner"] or es.m==["scannerC"]:
                        st = (end-1,end)
    
                    if st not in index:
                        index[st] = []
                    index[st].append(es)
        return index 
        
    init()
    rules = [predictorepsilon,scanner,completer]
    ok = True
    while ok:
        ok = False
        for r in rules:
            try:
                modify1 = r()
                if modify1:
                    I = indexes2(S)
                    print1(I,r)
                    ok = True
                    
            except Exception as e:
                print1(e)
                break
    
    
        
    def converter():
        print1(A)
        for end,Se in S:
            for start,Ses in Se:
                for elem in Ses:
                    convertAndSI(end,start,elem)
    
   
    converter()
 
    
    def outputtoTree(output,tree):
        if len(output)==0:
            return
        if len(output)>0:
            if (output[0] not in tree):
                tree[output[0]] = context.context()
            outputtoTree(output[1:],tree[output[0]])
     
    
    
    ind = indexes(S)
    for i in ind:
        print1(i)
    
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

    
    def convertMustBe(mustBe,start,end):
        c = context.context()
        
        for i,v,op in mustBe:
            if op=="==":
                c[i]=[v]
            elif op==">=":
                c[i]=list(range(v,end-start+1))
        
        holes = context.context()
        
        i0 = 0
        for k,v in c:
            holes[i0] = k
            i0+=1
                
        ks = list(c.keys())
        ks = list(sorted(ks))
        vs = [c[k] for k in ks]
        for y in deepfor(*vs):
            z = context.context()
            for i,yy in enumerate(y):
                z[holes[i]]=yy
            
            yield z 
        
    
    
    def partitions(n,start,end,mustBe,depth = 0):
        cs = convertMustBe(mustBe,start,end) 
        for c in cs:
            PS = intpart2(start,end,n,c) 
            for p in PS:
                yield p  
            
    def recursive(item):
        return A[item.ir][0] in A[item.ir][1]
        
    def findItems(start,end,symbol):
        for i in ind[(start,end)]:
            if A[i.ir][0] == symbol and i.m==["completer"]:
                yield i 
    
                        
    def findItemsScanner(start,end,symbol):
        found = False
        for i in ind[(start,end)]:
            if i.m == ["scanner@"]:
                found = True
                yield i
        if found == False:
            if end-start==1:
                for i in ind[(start,end)]:
                    if i.m == ["scanner"] and words[start]==symbol:
                        yield i
                    elif i.m ==["scannerC"]:
                        yield i
            elif end-start==0 and nullable(symbol):
                for i in ind[(start,end)]:
                    yield i
    
    
            
    
    def allConnected(symbol,allconnected = [],depth = 0):
        for k,v in A:
            if v[0]==symbol and v[1] not in allconnected:
                allconnected.append(v[1])
                for i in v[1]:
                    allConnected(i,allconnected,depth+1)
        output = []
        for i in allconnected:
            output+=list(i)
            
        return output
        
    def okToaddNullable(symbol):
        if nullable(symbol):
            for k,vs in ind:
                for v in vs:
                    if A[v.ir][0] in symbol and (v.m ==["scanner"] or v.m==["scannerC"]):
                        return False
    
    
        return True
    
                   
    J = context.context()
    CycleCheck = True
    
    def nonterminal(x):
        if x == "@": return True
        for i,(l,r) in A:
            if l==x:
                return True
        return False
    
    @Debug (active=False)
    def builtree(start,end,symbol,item,depth=0,check=[],frm = "",partitionorig = None):
        def print0(*args,**kwargs):
            print1("\t"*depth, *args,**kwargs)
            
        print0(start,end,symbol,repr(item),frm,partitionorig)
        trees = context.context()
        output = None
        if CycleCheck:
            next = [start,end,symbol,item]
            check0 = list(check)
            if next in check0:
                output = False, []
            else:
                check0.append(next)
        subtrees = context.context()
        node = symbol
       
        if output==None:
            if end-start == 1 and symbol == A[item.ir][0] and (item.m == ["scanner"] or item.m==["scannerC"]):
                
                sub = None
                for (k1,k2),(v1,v2) in Atomic:
                    if words[start] == v2:
                        sub=v1
                        break
                Flag = True
                if sub==None:
                    sub = words[start]
                tree=sub
                trees=tree
            elif (symbol == A[item.ir][0] and item.m ==["scanner@"]):
               

                Flag = True
                tree = words[start:end] 
                trees = tree
            
            elif end-start==0 and nullable(symbol) and symbol == A[item.ir][0]:
              
                Flag = True
                tree="#"
                trees=tree
                
            else:
              

                Flag = False
                n = len(A[item.ir][1]) 
                
                
                mustBe = []
                
                R =A[item.ir][1] 
                
                for i,x in enumerate(R):
                    if not nonterminal(x):
                        mustBe.append((i,1,"=="))
                    if x=="@":
                        mustBe.append((i,1,">="))
                        
                    if x=="L":
                        mustBe.append((i,1,"=="))
                        
            
                p = partitions(n,start,end,mustBe)
                p = list(p)
                
                for k,q in enumerate(p):
                    print0("q",q)
                    ok = True
                    for k0,(i,j) in enumerate(q):
                        subtrees[k0]=[]
                        
                        flag = False
                        
                        if k0<len(A[item.ir][1]):
                            items = list(findItems(i,j,A[item.ir][1][k0]))
                            if len(items)>0:
                                for item0 in items:
                                    flag, subtree = builtree(i,j,A[item0.ir][0],item0,depth+1,check0,frm = "item1",partitionorig= (q,mustBe,A[item.ir][1]))
                                    compar1 = str(subtree).replace("[","").replace("]","")
                                    compar2 = str(subtrees[k0]).replace("[","").replace("]","")
                                    subtree = context.context(node=A[item.ir][1][k0], subtrees = subtree)
                                    if not flag and compar1 not in compar2:
                                        subtrees[k0].append(subtree)
    
                            if len(subtrees[k0])==0:
                                items2 = list(findItemsScanner(i,j,A[item.ir][1][k0]))

                                if len(items2)>0:
                                    for item0 in items2:  
                                        flag, subtree = builtree(i,j,A[item0.ir][0],item0,depth+1,check0, frm = "item 2",partitionorig = (q,mustBe,A[item.ir][1]))
                                        compar1 = str(subtree).replace("[","").replace("]","")
                                        compar2 = str(subtrees[k0]).replace("[","").replace("]","")
                                        if subtree=="#" or item0.m == ["scanner@"]:
                                            subtree = context.context(node=A[item.ir][1][k0],subtrees=subtree)
                                        if compar1 not in compar2:
                                            subtrees[k0].append(subtree)
                        
    
                    
                    stv = list(subtrees.values())
                  
                    
                    if len(stv)>0:
                        for st in deepfor(*stv):
                         
                            tree = st
                          
                            if k not in trees.keys():   
                                trees[k]= []
                           
                                
                            trees[k].append(tree)
            
            if str(type(trees))== "<class 'contexttest.super_context.<locals>.Y.<locals>.X'>":
                trees = list(trees.values())
                trees = list(filter(len, trees))
            
            
            output = Flag,trees
        
        print0(start,end,symbol,repr(item),frm,partitionorig,output)

        return output
    
            
                                    
    def bigbuilder():
        startitem = None
        for end in S.keys():
            for start,Ses in S[end]:
                for es in Ses:
                    if es.m == ["completer"] and len(A[es.ir][1])==es.it and A[es.ir][0]=="*":
                        startitem = es
                        break
        if startitem==None:
            return None,None
        return builtree(0,len(words),"*",startitem)
                    
    return bigbuilder()
    

ns = []
avgs = []

S = context.context()
S2 = context.context()
A = context.context()
L = context.context()

L[0] = "class"
L[1] = "def"

A[0] = "*","S"
A[1] = "S","L @: L @"


#A[1] = "S","L @"
#A[3] = "V","&V"
#A[4] = "V", "#"
#A[6] = "J","def"
#A[7] = "A","a"

setC = []
for a in range(97,123):
    setC.append(chr(a))
words = "class report: def init"
start = time.time()
f, output = main(A,S,words,L,setC,S2)
end = time.time()

print(output)
