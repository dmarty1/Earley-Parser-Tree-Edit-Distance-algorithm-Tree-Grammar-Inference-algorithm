import sys
sys.path.append("/Users/diva-oriane/Documents/GitHub/asanas/Parse/")

import contexttest as context
import random
from itertools import permutations 
import scipy.optimize as O
import numpy as N
import matplotlib.pyplot as plt

#DEFINE HERE


    
#MAIN LOOP
debug = False

def Debug(cast=None,active = True):
    
    def h(f):
        
        def g(*args,**kwargs):
            depth = 0 
            if "depth" in kwargs:
                depth = kwargs["depth"]
            if active:
                print1("\t"*depth,f,args,kwargs)
            y = f(*args,**kwargs)
            z = y 
            if cast:
                z = cast(z)
                y = z
            if active:
                print1("\t"*depth,f,args,kwargs,z)
            return y 
        return g
    return h
        
    
def print1(*args,**kwargs):
    if debug:
        print(*args,**kwargs)
        
def main(A,S,words,L,setC):
    
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
    
    '''
    def convertAwithAtomic(A):
        Anew = context.context()
        Anew.__iadd__(A)
        Atomic = atomic(words)
        for (a,b) in Atomic.values():
            for k,v in Anew:
                v0new = v[0].replace(a,b)
                v1new = v[1].replace(a,b)
                Anew[k] = (v0new,v1new)
        return Anew
    '''
    
    
    #Aold = A
    #A = convertAwithAtomic(A)
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
    
        
    def target(Si):
        if Si.it < len(A[Si.ir][1]):
            return A[Si.ir][1][Si.it]
        else:
            return False
    
    def compare(ns0,ns1):
        return (ns0.ir,ns0.j,ns0.it,ns0.m) == (ns1.ir, ns1.j,ns1.it,ns1.m)
    
    def in2(ns,nslist):
        for n in nslist:
            if compare(n,ns):
                return True
        return False
        
    def convertAndSI(i,elem):
        w = []
        c = 0
        for j in range(len(A[elem.ir][1])+1):
            if j==elem.it:
                w.append("$")
            if j<len(A[elem.ir][1]):
                w.append(A[elem.ir][1][j])
        line = str(i)+" "+A[elem.ir][0]+"=>"+A[elem.ir][1]+" "+ "".join(w)+", "+str(elem.j)+" "+str(elem.m)
        
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
        for i,Sis in S:
            for k1, Si in enumerate(Sis):
                B = target(Si)
                if B!=False:
                    if nullable(B):
                        ns = context.context(
                            ir = Si.ir,
                            it = Si.it+1,
                            j = Si.j,
                            m = ["predictorepsilon"],
                           
                        )
                        add.append((i,ns,Si))
                    if B == "@":
                        ns = context.context(
                            ir = Si.ir,
                            it = Si.it,
                            j = i,
                            m = ["predictor@"],
                           
                        )
                        add.append((i,ns,Si))
                    else:
    
                        for k,v in A:
                            if v[0] == B:
                                ns = context.context(
                                    ir = k,
                                    it = 0,
                                    j = i,
                                    m = ["predictor"],
                                
                                )
                                add.append((i,ns,Si))
    
                            
        
        for i,ns,Si in add:
            if not in2(ns,S[i]):
                S[i].append(ns)
                modify = True
        return modify
    
    def init():
        S[0] = []
        ns = context.context(
                ir = 0,
                it = 0,
                j = 0,
                m = ["start"],
              
            )
        S[0].append(ns)
    
   
    
    
    def scanner():
        modify = False
        add = []
        for i,Sis in S:
            for k,Si in enumerate(Sis):
                B = target(Si)  
                if B!=False:
                    
                    if (i<len(words) and (B=="@") and words[Si.j] in setC):
                        new =0
                        inew = i
                        while Si.j+new <(len(words)) and words[Si.j+new] in setC:
                            new +=1
                                            
                        ns = context.context(
                            ir = Si.ir,
                            it = Si.it+1,
                            j = Si.j,
                            m = ["scanner@"]
                        )
                        add.append((i+new,ns))
                        
                        if False:
                            ns = context.context(
                                ir = Si.ir,
                                it = Si.it+1,
                                j = Si.j,
                                m = ["scanner-completer@"]
                            )
                            add.append((i,ns))
                    
                    elif (i<len(words) and ( B=="&") and words[Si.j] in setC):
                        ns = context.context(
                            ir = Si.ir,
                            it = Si.it+1,
                            j = Si.j,
                            m = ["scannerC"]
                        )
                        add.append((i+1,ns))
                    elif  (i<len(words) and (B == words[i] )):
                        ns = context.context(
                            ir = Si.ir,
                            it = Si.it+1,
                            j = Si.j,
                            m = ["scanner"]
                        )
                        add.append((i+1,ns))
                        
                        
                        
                        
                        
        for i,ns in add:
            if i not in S:
                S[i]=[]
            if not in2(ns,S[i]):
                S[i].append(ns)
                modify = True
        return modify
        
    def completer():
        modify = False
        add = []
        print1(S)
        for i,Sis in S: 
            for Si in Sis:
                print1(Si,i)
                B = target(Si)
                if B==False or B == "@":
                    if Si.it==4:
                        print1("completer",Si)
                        print1(Si.j,S[Si.j])
                    for k,elem in enumerate(S[Si.j]):
                        #if Si.it==4:
                        #    print1("target elem",Si,elem,target(elem))
                        if target(elem)== False:
                            pass
                        
                        #elif target(elem)==A[Si.ir][0] or (target(elem) in words) or (nullable(A[elem.ir][0]) and i==elem.j) :
                        else:
                            addition = 1
                            for k,v in L:
                                if A[elem.ir][1]==v:
                                    addition = len(v)
                            ns = context.context(
                                ir = elem.ir,
                                it = elem.it+addition,
                                j = elem.j,
                                m = ["completer"]
                            )
                            if ns.it <= len(A[ns.ir][1]):
                                add.append((i,ns,Si))
        
                
                            
                            
        for i,ns,Si in add:
            if not in2(ns,S[i]):
                S[i].append(ns)
                modify = True
        return modify
    
    def indexes(S):
        index = context.context()
        for i in S.keys():
            for Si in S[i]:
                if (Si.m == ["completer"] or Si.m == ["scanner"]or Si.m==["scannerC"] or Si.m ==["scanner@"]):
                    st = (Si.j,i)
                    if Si.m==["scanner"] or Si.m==["scannerC"]:
                        st = (i-1,i)

                    if st not in index:
                        index[st] = []
                    index[st].append(Si)
        return index
    

    
    def indexes2(S):
        index = context.context()
        for i in S.keys():
            for Si in S[i]:
                st = (Si.j,i)
                if Si.m==["scanner"] or Si.m==["scannerC"]:
                    st = (i-1,i)

                if st not in index:
                    index[st] = []
                index[st].append(Si)
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
        for i in S.keys():
            for elem in S[i]:
                convertAndSI(i,elem)
    
   
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
    
    '''
    def deepfor(*xs):
        if len(xs)>0:
            hs = xs[0]
            ts = xs[1:]
            for h in hs:
                for t in deepfor(*ts):
                    yield [h]+t
        else:
            yield []
    
    def intpart(n,s):
        ns = list(range(1,s+1))

        xs = [ns for _ in range(n)]
        
        for x in deepfor(*xs):
            if sum(x)==s:
                yield x
    

    
    def sumdiffs(xs):
        d = 0
        for i in range(1, len(xs)):
            di = xs[i]-xs[i-1]
            d += di
        return d
    
    def increase(xs):
        ok = True
        for i in range(1, len(xs)):
            ok = ok and xs[i]>=xs[i-1]
        return ok
    
    @Debug(list)
    def partitions(*args,**kwargs):
        return list(partitions0(*args,**kwargs))
    
    def partitions0(n,start,end,mustBe,depth):        
                
        ns = list(range(start,end+1))

        xs = [ns for _ in range(n+1)]

        seen = []
        for p in deepfor(*xs):
            
            
            c0 = sumdiffs(p) == end-start
            c1 = increase(p)
            if c0 and c1 :
            
                    
                pp = []
                for i in range(len(p)-1):
                    
                    pp.append((p[i],p[i+1]))
                    
                ok = True
                #print(pp)
                for i,v,op in mustBe:
                    if op=="==":
                        if not pp[i][1]-pp[i][0]==v:
                            ok = False
                        
                    elif op==">=":
                        if not pp[i][1]-pp[i][0]>= v:
                            ok = False
                    elif op=="in":
                        if not (pp[i][1]-pp[i][0])in v:
                            ok = False
                        
    
                if ok and (pp not in seen):
                    seen.append(pp)
                    yield pp
    
    def flatten(xs):
        x = []
        for y in xs:
            x.extend(y)
        return x 
    
    @Debug(list,active = True)
    
    def partitions(n,start,end,mustBe,depth = 0):
        pp = context.context()
        holes = context.context()
        notdone = []
        #mustBe ad the ops
        for i,v,op in mustBe:
            pp[i] = (i,i+v)
        
        vspp = list(pp.values())
        last1 = 0
        for a,b in vspp:
            if a-last1!=0:
                notdone.append((last1,a))
            last1 = b
            
        if end-last1!=0:
            notdone.append((last1,end))
    
        
        output0 = [None]*n
        for i in pp.keys():
            output0[i] = pp[i]
        i0 = 0
        for w,x in enumerate(output0):
            if x==None:
                holes[i0] = w
                i0+=1
        Nremain = n-len(pp)
        if Nremain==0:
            yield output0
        else:
            for x in intpart(len(notdone),Nremain):
                output1 = context.context()
                for i,j in enumerate(output0):
                    
                    if j:
    
                        output1[i] = [[j]]
                for i,xx in enumerate(x):
                    start,end = notdone[i]
                    ps = partitions0(xx,start,end,[],depth+1)
                    output1[holes[i]] = list(ps)
                ks = list(output1.keys())
                ks = list(sorted(ks))
                vs = [output1[k] for k in ks]
                for y in deepfor(*vs):
                    yield flatten(y) 
    
    #PS = list(partitions(1,0,8,[]))
            
    #PROBLEM (1, 5, 6, [(0, 1, '==')]) {}
    
    def intparts(n,s):
        ns = list(range(0,s+1))

        xs = [ns for _ in range(n)]
        
        for x in deepfor(*xs):
            #too many test genereated by deep for 
            if sum(x)==s:
                yield x
    
    #intparts new recursive 
                
    def intpart2(s,e,n,c):
        xs = intparts(n,e-s)
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
    
    def intpart3(s,e,n,c):
        ns = list(range(0,e-s+1))
        xs = [ns for _ in range(n)]
        
        cur = 0
        print(c)
        for i in intparts(n, s-e):
            cur+=1
            print(i)
            if cur == 5:
                break


        
        for k,v in c:
            cur +=v
            xs[k] = k 
            x[k+1] = k+v
        
        
            
        
    
    
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
            
            
            
    #PS = list(intpart2(5,6,1,c))
            
    
    mustBe = [(0, 1, '=='),(1, 1, '=='),(2, 1, '=='),(3, 1, '=='),(4, 1, '=='),(5, 1, '=='),(6, 1, '==')]
    mustBe = [(0, 1, '=='),(1, 1, '=='),(3, 1, '=='),(4, 1, '=='),(6, 1, '=='),(8,2,"=="),(12,1,"==")]
    c = convertMustBe(mustBe)
    intpart3(8,0,8,c)
    
    
    
    def partitions(n,start,end,mustBe,depth = 0):
        c = convertMustBe(mustBe) #this is good 
        PS = intpart2(start,end,n,c) #need to fix this.......
        for p in PS:
            yield p  
    
    #put the ones that can be put together together
    
    print("here")
    PS = list(partitions(8, 0, 8, [(0, 1, '=='),(1, 1, '=='),(2, 1, '=='),(3, 1, '=='),(4, 1, '=='),(5, 1, '=='),(6, 1, '==')]))
    print(PS)

    return False,False
    '''
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
        cs = convertMustBe(mustBe,start,end) #this is good 
        for c in cs:
            PS = intpart2(start,end,n,c) #fix?
            for p in PS:
                yield p  
            
    def recursive(item):
        return A[item.ir][0] in A[item.ir][1]
        
    def findItems(start,end,symbol): #limit to only completer only marginally faster
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
            if False:
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
                #print0("k1")
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
                #print0("k2")

                Flag = True
                tree = words[start:end] 
                trees = tree
            
            elif end-start==0 and nullable(symbol) and symbol == A[item.ir][0]:
                #print0("k3")

                Flag = True
                tree="#"
                trees=tree
                
            else:
                #print0("k4")

                Flag = False
                n = len(A[item.ir][1]) 
                
                #L M: #(1,2)(8,9) #make sure all the values that are in the word are 
                mustBe = []
                
                R =A[item.ir][1] 
                
                for i,x in enumerate(R):
                    if not nonterminal(x):
                        mustBe.append((i,1,"=="))
                    if x=="@":
                        mustBe.append((i,1,">="))
                        #cannot be just one 1 >= not == 
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
                        #probably a big lose in time here .... too many recursive calls 
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
        for i in S.keys():
            for Si in S[i]:
                if Si.m == ["completer"] and len(A[Si.ir][1])==Si.it and A[Si.ir][0]=="*":
                    startitem = Si
                    break
        #print(repr(startitem))
        if startitem==None:
            return None,None
        return builtree(0,len(words),"*",startitem)
                    
    return bigbuilder()






def example(N,lenword):
    A = context.context()
    
    L = context.context()
    L[0] = "class"
    L[1] = "def"
    
    S = context.context()
    words = "class a"
    A[0] = "*","S"
    A[1] = "S","L V"
    A[2] = "L","class"
    A[4] = "V","CV"
    A[5] = "V","#"
    wordslength = 0

    ix =97
    while ix-97!=N:
        if chr(ix) not in ["S","V","#","&","*","L"]:
            A[ix] = "C" , chr(ix)
            #if wordslength!=lenword:
            #    words+=chr(ix)
            #    wordslength+=1
        ix+=1
    
    setC = list(words)
                
    return A, L, S, words, setC
 
import time
ns = []
avgs = []

S = context.context()
A = context.context()
L = context.context()

L[0] = "class"
L[1] = "def"

A[0] = "*","S"
A[1] = "S","L V"#"L @: L @"

#A[1] = "S","L @"
A[3] = "V","&V"
A[4] = "V", "#"
A[5] = "L"
#A[6] = "J","def"
#A[7] = "A","a"

setC = []
for a in range(97,123):
    setC.append(chr(a))
#words = "class report: def init"
words = "class ab"
#for i in range(6):
start = time.time()
f, output = main(A,S,words,L,setC)
end = time.time()

print(output)

def run(x,m,N,lenword):
    ns.append(N)
    A,L,S,words,setC = example(N,lenword)
    sum = 0
    for i in range(m):
        start = time.time()
        f, output = (main(A,S,words,L,setC)) 
        print1(output) 
        end = time.time()
        sum += (end-start)
    print1(output) 
    avg = sum/m
    avgs.append(avg)
    x.write(str(N)+","+str(avg)+"\n")
    print(N,avg)
x = open("output.txt", "w")    
x.write("N,avg"+"\n")

n = 25
#N the number of definitions for a symbol in the grammar
for i in range(3,n):
    run(x,4,i,3)

print1("\n")
x.flush()

ns = N.array(ns)
avgs = N.array(avgs)

def model2(x, a, b, c):
    y = a + b*x + c*x**2
    #y = a+b*N.exp(c*x)
    #y = a/(b+N.exp(-c*x))
    return y

def model(x,a,b,c):
    y = a+b*N.exp(c*x)
    return y 


def function(model, magic):
    def aux(x):
        y = model(x, *magic)
        return y
    return aux
try:
    magic, _ = O.curve_fit(model2, ns, avgs)
    print(magic)
    fx = function(model2, magic)
except:
    fx = lambda x: x
try:
    magic2,_ = O.curve_fit(model, ns,avgs)
    print(magic2)
    fx2 = function(model, magic2)
except:
    fx2 = lambda x: x
    


# x axis values 
a = ns
# corresponding y axis values 
b = avgs
  
# plotting the points 
print(a)
print(b) 
plt.plot(a, b,label = "data",marker = "o") 
#plt.plot(a,fx(a),label = "model2")
#plt.plot(a,fx2(a),label = "model1")
plt.ylim(min(b),max(b))
# naming the x axis 
plt.legend()
plt.xlabel('N') 
# naming the y axis 
plt.ylabel('Avgs') 
  
# giving a title to my graph 
plt.title('N vs. Avg!') 
  
# function to show the plot 
plt.show()
