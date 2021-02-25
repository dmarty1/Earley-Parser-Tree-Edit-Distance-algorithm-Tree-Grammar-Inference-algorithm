import sys
sys.path.append("/Users/diva-oriane/Documents/GitHub/asanas/Parse/")

import contexttest as context
from parse3 import parse3 as parse
from parse3 import matchContext
from parse3 import parseSpecial
import random
from itertools import permutations 
import scipy.optimize as O
import numpy as N
import matplotlib.pyplot as plt
import time
import re

import hashlib


    
#MAIN LOOP
'''
i = end
j = start
'''
#formating    
C = context.context 
def digest(x):
    y = hashlib.sha256(str(x).encode()).hexdigest()[:6]
    return y 
def setFormat():
    #format must include {start} and {end}
    Format = "{start}.{end}"
    return Format
    
def key(I, Format = setFormat()):
    output = parse(Format,I)
    return (int(output.start),int(output.end))
    
def makeI(start,end,Format = setFormat()):
    I = Format.replace("{start}",str(start)).replace("{end}",str(end))
    return I 

def get(S,I,Format = setFormat()):
    start, end = key(I,Format)
    if end not in S:
        S[end] = context.context()
    if start not in S[end]:
        S[end][start] =[]
    return S[end][start]
    
    
def setVal(S,I,value,Format = setFormat()):
    start, end = key(I,Format)
    if end not in S:
        S[end] = context.context()
    if start not in S[end]:
        S[end][start] = []
    S[end][start].append(value)
    return S

def getAllEnd(S,end,Format = setFormat()):
    for e, Se in S:
        if e == end:
            for s, Ses in Se:
                for elem in Ses:
                    yield s,elem
                #should I yield the start, Ses ?
                
def getAllStart(S,start,Format=setFormat()):
    for e, Se in S:
        for s, Ses in Se:
            if s == start:
                for elem in Ses:
                    yield elem
                #should I yield the end, Ses ?


def getAll(S,Format = setFormat()):
    for e in S.keys():
        for s, elem in getAllEnd(S,e):
            I = makeI(s,e,Format)
            yield I,elem

        
debug = False   
debugSpecial = True 

def Debug(*args0,cast=None,active = True):
    i = C(0)
    def h(f):
        
        def g(*args,**kwargs):
            j = i[0]
            i[0]+=1
            depth = 0     
            if "depth" in kwargs:
                depth = kwargs["depth"]
            args1=[(kwargs[arg] if arg in kwargs else None) if(type(arg)!=int) else args[arg] for arg in args0]
            if active:
                print("\t"*depth,j,f.__name__,*args1)
            y = f(*args,**kwargs)
            z = y 
            if cast:
                z = cast(z)
                y = z
            if active:
                print("\t"*depth,j,f.__name__,*args1,z)
            return y 
        return g
    return h
        
    
def print1(*args,**kwargs):
    if debug:
        print(*args,**kwargs)

def setLexicon():
    L = C()
    L[0] = "False"
    L[1] = "None"
    L[2] = "True"
    L[3] = "and"
    L[4] = "as"
    L[5] = "assert"
    L[6] = "break"
    L[7] = "class"
    L[8] = "continue"
    L[9] = "def"
    L[10] = "del"
    L[11] = "elif"
    L[12] = "else"
    L[13] = "except"
    L[14] = "finally"
    L[15] = "for"
    L[16] = "from"
    L[17] = "global"
    L[18] = "if"
    L[19] = "import"
    L[20] = "in"
    L[21] = "is"
    L[22] = "lambda"
    L[23] = "nonlocal"
    L[24] = "not"
    L[25] = "or"
    L[26] = "pass"
    L[27] = "raise"
    L[28] = "return"
    L[29] = "try"
    L[30] = "while"
    L[31] = "with"
    L[32] = "yield"
    L[33] = "**"
    L[34] = "*"

    return L
    
def setSetC():
    #lowercase (a,z), uppercase (A,Z), digits(0,9) or an underscore _
    #cannot start with a digit
    #keywords cannot be used as identifiers
    #we cannot use special symbols like !, @, #, $, % etc. in our identifier.
    setC = [chr(i) for i in range(97,123)]
    setC +=[chr(y) for y in range(65,91)]
    setC +=[chr(z) for z in range(48,58)]
    setC +=["_"]
    return setC
    

        
def main(A,words,GL,antisetC=[]):
    S = C()
    setC = setSetC()
    L = setLexicon()
    
    lines = []
    def addToLexicon(A):
        w = []
        theGrammarInString = ""
        for k,v in A:
            for e in v:
                e1list = e.split("'")
                for i in range(1,len(e1list),2):
                    w.append(e1list[i])
                theGrammarInString+=e
        
        for ww in w:
            if ww not in L.values():
                L[len(L)] = ww
        
        
        return L 
    
    L = addToLexicon(A)
                    
    
    def atomicGrammar(A):
        w = []
        theGrammarInString = ""
        for k,v in A:
            for e in v:
                e1list = e.split("_")
                for i in range(1,len(e1list),2):
                    w.append(e1list[i])
                theGrammarInString+=e
                
        #alphabet will need to be improved
        alphabet = [chr(ns) for ns in range(48,58)]
        
        alphabetedited = []
        for a in alphabet:
            if a not in theGrammarInString:
                alphabetedited.append(a)
        
        for i in w:
            if i not in GL.values():
                GL[len(GL)] = i
        
        glmapped = context.context()
        for i in GL.values():
            glmapped[i] = alphabetedited[0]
            alphabetedited = alphabetedited[1:]
        
        
                
        Atomic = context.context()
        
        
        
        for k,v in A:
            for kk, vv in enumerate(v):
                e = vv.split("_")
                for ee in e:
                    if ee in GL.values():
                        Atomic[k,kk,ee] = ee,glmapped[ee]
                    

        return Atomic
        
        
    atomGrammar  = atomicGrammar(A)

    def atomicGrammarConverted(A):
        def recognizeParseFormat(r,thechar):
            output = ""
            start = None
            end = 0
            i = 0
            n = 0
            while i<len(r):
                if r[i]=="(":
                    start = i
                if start!=None and r[i:i+2]==")"+str(thechar):
                    if start!=end:
                        output+="{}"
                    output+="({value"+str(n)+"})"+str(thechar)
                    end = i+2
                    start = None
                    n+=1
                i+=1
            if end!=len(r):
                output+="{}"
            return output 

        Atomic = atomicGrammar(A)
        
        Anew = context.context()
        for k,v in A:
            v0,v1 = A[k][0].split("_"),A[k][1].split("_")
            for i,o in Atomic.values():
                for ii in range(len(v0)):
                    if v0[ii] == i:
                        v0[ii] = o
                
                for jj in range(len(v1)):
                    if v1[jj] == i:
                        v1[jj] = o
            Anew[k] = "".join(v0),"".join(v1)
        return Anew
                
                
                
        
    def convertWithLexicon(A):
        
        Anew = context.context()
        for k,v in A:
            v0,v1 = A[k][0].split("'"),A[k][1].split("'")
            for i in L.values():
                for ii in range(len(v0)):
                    if v0[ii] == i:
                        v0[ii] = "L"
                
                for jj in range(len(v1)):
                    if v1[jj] == i:
                        v1[jj] = "L"
            Anew[k] = "".join(v0),"".join(v1)
        
        return Anew

    A = convertWithLexicon(A)
    A = atomicGrammarConverted(A)

    def atomic(words):
        Atomic = context.context()
        #alphabet = ["α","β","Γ","γ","Δ","δ","ε","ζ","η","θ","ι","Λ","λ","μ","ν","Ξ","ξ","π","ρ","Σ","σ","ς","τ","υ","Φ","χ","Ψ","Ω","ω",""]        
        alphabet = [chr(x) for x in range(945,1000)]
        alphabetedited = []
        for a in alphabet:
            if a not in words:
                alphabetedited.append(a)
        
        lmapped = {}
        for i in L.values():
            lmapped[i] = alphabetedited[0]
            alphabetedited = alphabetedited[1:]
            
        wordlist = re.split(r'(\s+)', words)
    
        for i in range(len(words)):
            for v in L.values():
                if i+len(v)<=len(words) and words[i:i+len(v)] ==v and v in wordlist:
                    Atomic[(i,i+len(v)-1)] = (v,lmapped[v])
        return Atomic
    
    Atomic = atomic(words)
    
    
    def convertWordWithAtomic(words):
        Atomic = atomic(words)
        word = str(words)
        wordlist = re.split(r'(\s+)', word)
        for (a,b) in Atomic.values():
            for i,x in enumerate(wordlist):
                if x ==a:
                    wordlist[i]=b
                    A[len(A)] = "L",b
                
        word = ""
        for i in wordlist:
            word+=i
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
        
    def convertAndSI(I,elem):
        w = []
        c = 0
        for g in range(len(A[elem.ir][1])+1):
            if g==elem.it:
                w.append("•")
            if g<len(A[elem.ir][1]):
                w.append(A[elem.ir][1][g])
        
        
        temp = [str(A[elem.ir][0]),str(A[elem.ir][1])]
        for (k,kk,ee),(x, xx) in atomGrammar:
            temp = [str(temp[0].replace(xx,x)),str(temp[1].replace(xx,x))]
        
        lineA, lineB, lineC, lineD,lineE = str(elem.iteration),I, temp[0]+"=>"+temp[1], "".join(w), elem.m[0]
        line = I+" "+temp[0]+"=>"+temp[1]+" "+ "".join(w)+", "+str(elem.m) +str(elem.iteration)
        
        for (k1,k2),(v1,v2) in Atomic:
            line = line.replace(v2,v1)
    
        lines.append([lineA,lineB,lineC,lineD,lineE])
        if debugSpecial:
            print(line)            
    
    
    def getNullK(B):
        for k,i in A:
            if i[0] == B:
                if i[1] == "#":
                    return k
    def predictorepsilon(iteration=0):
                
        modify = False
        add = []
        for I, es in getAll(S):
            start,end = key(I)
            
            B = target(es)
            if B!=False:
                if nullable(B):
                    ns = context.context(
                        ir = es.ir,
                        it = es.it+1,
                        m = ["predictorepsilon"],
                        iteration = iteration
                    
                    )
                    I = makeI(start,end)
                    add.append((I,ns,es))
                if B == "@":
                    ns = context.context(
                        ir = es.ir,
                        it = es.it,
                        m = ["predictor@"],
                        iteration = iteration
                    )

                    I = makeI(end,end)
                    add.append((I,ns,es))
                elif B == "$":
                    ns = context.context(
                        ir = es.ir,
                        it = es.it,
                        m = ["predictor$"],
                        iteration = iteration
                    )

                    I = makeI(end,end)
                    add.append((I,ns,es))
               
                else:

                    for k,v in A:
                        if v[0] == B:
                            ns = context.context(
                                ir = k,
                                it = 0,
                                m = ["predictor"],
                                iteration = iteration
                            
                            )
                            I = makeI(end,end)
                            add.append((I,ns,es))
                
                
            

                            
        for I,ns,es in add:
            if not in2(ns,get(S,I)):
                S.__iadd__(setVal(S,I,ns))
                modify = True
        return modify
    
    def init():
        
        I = makeI(0,0)
        
        ns = context.context(
                ir = 0,
                it = 0,
                m = ["start"],
                iteration = 0,
            )
            
        S.__iadd__(setVal(S,I,ns))

   
    
    
    def scanner(iteration=0):
        modify = False
        add = []
        
        for I, es in getAll(S):
            start, end = key(I)
            B = target(es) 
            if B!=False:
                if es.m == ["predictor@"] and (end<len(words) and (B=="@") and words[start] in setC):
                    new =0
                    while end+new <(len(words)) and words[end+new] in setC:
                        new +=1
         
                    ns = context.context(
                        ir = es.ir,
                        it = es.it+1,
                        m = ["scanner@"],
                        iteration = iteration
                    )
                    
                    I = makeI(start,end+new)
                    add.append((I,ns))
                    
                    ns2 = context.context(
                        ir = es.ir,
                        it = es.it+1,
                        m = ["completer"],
                        iteration = iteration
                    )
                    for I2,es2 in getAll(S):
                        if A[es2.ir]==A[es.ir] and es2.it==0 and es2.m == ["predictor"]:
                            start2, end2 = key(I2)
                        
                    I = makeI(start2,end+new)
                    add.append((I,ns2))
                    
                    
                elif es.m == ["predictor$"] and (end<len(words) and (B=="$") and (words[start] not in antisetC)):
                    new =0
                   
                    while end+new <(len(words)) and (words[end+new] not in antisetC):
                        new +=1
                    ns = context.context(
                        ir = es.ir,
                        it = es.it+1,
                        m = ["scanner$"],
                        iteration = iteration
                    )
                    
                    I = makeI(start,end+new)
                    add.append((I,ns))
                    ns2 = context.context(
                        ir = es.ir,
                        it = es.it+1,
                        m = ["completer"],
                        iteration = iteration
                    )
                    for I2,es2 in getAll(S):
                        if A[es2.ir]==A[es.ir] and es2.it==0 and es2.m == ["predictor"]:
                            start2, end2 = key(I2)
                            #print(es2,start2,end2,A[es.ir])
                    if start2<=(end+new):
                        I = makeI(start2,end+new)
                        add.append((I,ns2))
                        #print("being added", I ,ns2)
                    
               
                elif (end<len(words) and ( B=="&") and words[start] in setC):
                    
                    ns = context.context(
                        ir = es.ir,
                        it = es.it+1,
                        m = ["scannerC"],
                        iteration = iteration,
                    )
                    I = makeI(start,end+1)
                    add.append((I,ns))
                
                
                    
                elif  (end<len(words) and (B == words[end])):
                    ns = context.context(
                        ir = es.ir,
                        it = es.it+1,
                        m = ["scanner"],
                        iteration = iteration
                    )
                    I = makeI(start,end+1)
                    add.append((I,ns))
                
                
                
                
                
                    
                        
                        
        for I,ns in add:
            if not in2(ns,get(S,I)):
                S.__iadd__(setVal(S,I,ns))
                modify = True
        return modify
        
    def completer(iteration=0):
        modify = False
        add = []
        print1(S)
        for I, es in getAll(S):
            start,end = key(I)
            #if es.m == ["predictorepsilon"]:
            #    print(target(es))
            #test = start == 0 and end == 0 and es.ir==2
            #if test:
            #    print("completer",es,target(es))
            
            B= target(es)
            if B==False:
                for jj, elem in getAllEnd(S,start):
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
                            m = ["completer"],
                            iteration = iteration
                        )
                        if ns.it <= len(A[ns.ir][1]):
                            Inew = makeI(jj,end)
                            add.append((Inew,ns,es))
                                        
                                        
        for I,ns,es in add:
            if not in2(ns,get(S,I)):
                S.__iadd__(setVal(S,I,ns))
                modify = True
        return modify
        
    
    def indexes(S):
        index = context.context()
        for I, es in getAll(S):
            start,end = key(I)
            if (es.m == ["completer"] or es.m == ["scanner"]or es.m==["scannerC"] or es.m ==["scanner@"] or es.m==["scanner$"]):
             
            
                st = (start,end)
                if es.m==["scanner"] or es.m==["scannerC"]:
                    st = (end-1,end)

                if st not in index:
                    index[st] = []
                index[st].append(es)
        return index
    
    

    
    def indexes2(S):
        index = context.context()
        for I, es in getAll(S):
            start,end = key(I)
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
    iteration=0
    while ok:
        ok = False
        for r in rules:
            try:
                modify1 = r(iteration)
                if modify1:
                    I = indexes2(S)
                    print1(I,r)
                    ok = True
                    
            except Exception as e:
                print1(e)
                break
        
        iteration+=1

        
    
    
        
    def converter():
        print1(A)
        for I, elem in getAll(S):
            convertAndSI(I,elem)
    
   
    converter()
 
    
    def outputtoTree(output,tree):
        if len(output)==0:
            return
        if len(output)>0:
            if (output[0] not in tree):
                tree[output[0]] = context.context()
            outputtoTree(output[1:],tree[output[0]])
    
    ind = indexes(S)
    
    if debugSpecial:
        for k,v in ind:
            print(k)
            for vv in v:
                print("\t",vv,A[vv.ir])
            print("\n")
    
    
    
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
    
    def deepfor2(*xs):
        if len(xs)>0:
            hs = xs[0]
            ts = xs[1:]
            for h in hs:
                for t in deepfor2(*ts):
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
        
    def findItems(start,end,symbol,item0):
        for i in ind[(start,end)]:
            if A[i.ir][0] == symbol and i.m==["completer"] and str(i)!=str(item0):
                yield i 
    
                        
    def findItemsScanner(start,end,symbol,item0):
        
        found = False
        for i in ind[(start,end)]:
            if (i.m == ["scanner@"] or i.m==["scanner$"]) and (item0.m==["completer"] and item0.ir==i.ir) and str(i)!=str(item0):
                found = True
                yield i
        if found == False:
            if end-start==1:
                for i in ind[(start,end)]:
                    if i.m == ["scanner"] and words[start]==symbol and str(i)!=str(item0):
                        yield i
                    elif i.m ==["scannerC"] and str(i)!=str(item0):
                        yield i
            elif end-start==0 and nullable(symbol):
                for i in ind[(start,end)]:
                    if A[i.ir][0] == symbol and str(i)!=str(item0):
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
        if x == "@" or x == "$": return True
        for i,(l,r) in A:
            if l==x:
                return True
            
        return False
    
    def reemovNestings(l,output = [],control= False): 
        if type(l)==list:
            if control == False or len(l)==1:
                for i in l: 
                    if type(i) == list: 
                        reemovNestings(i,output) 
                    else: 
                        output.append(i) 
                return output
        return l
    def compareEquivTree(tree1, tree2):
        if convertToString(tree1)==convertToString(tree2):
            return True
        else:
            return False
        
    
    def convertToString(tree1):
        finalword = ""
        tree1 = reemovNestings(tree1,[])
        if str(type(tree1))== "<class 'contexttest.super_context.<locals>.Y.<locals>.X'>":
            finalword+=convertToString(tree1.subtrees)
        for sub in tree1:
            if type(sub)==str:
                if sub == "#":
                    pass
                else:
                    finalword+=sub
            elif str(type(sub))== "<class 'contexttest.super_context.<locals>.Y.<locals>.X'>":
                finalword+=convertToString(sub.subtrees)
        return finalword
                
                
    def inside(x,xs):
        xx = str(x)
        for y in xs:
            yy = str(y)
            if yy == xx:
                return True
                
        return False
    
    #might want to clean up code for memo
    def memo(*args0, **kwargs0):
        memory = C()
        def F(f):
            def g(*args,**kwargs):
                c = C()
                
                newargs3 = C()
                for k, v in args[3]:
                    if k!="iteration":
                        newargs3[k] = v
                c.args = [args[arg] for arg in args0[:-1]]
                for i,(k,v) in enumerate(newargs3):
                    c.args.append(v)
                    
                h = digest(c)
                if h not in memory.keys():
                    result = f(*args,**kwargs)
                    memory[h] = result 
                else:
                    result = memory[h]
                return result 
            return g
        return F 
    
    
    stack = context.context(s=[],stackappend = True)
    @memo(0,1,2,3)
    @Debug (0,1,2,3,"partitionorig",active=True)
    def builtree(start,end,symbol,item,depth=0,check=[],frm = "",partitionorig = None):
        
        def print0(*args,**kwargs):
            print1("\t"*depth, *args,**kwargs)
            
        def addsymbol(subtrees):
            return C(node = symbol, subtrees = subtrees)
            
        print0("(",start,end,")","[",A[item.ir][0],"=>",A[item.ir][1],item.it,"]",item.m)
        if stack.stackappend:
            stack.s.append((start,end,symbol,repr(item)))
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
                tree = sub
                trees[0][0]= tree
                trees = [tree]
            elif (symbol == A[item.ir][0] and (item.m ==["scanner@"] or item.m==["scanner$"])):
                Flag = True
                tree=words[start:end]

                trees[0][0] = tree
                trees = [tree]
            
            elif end-start==0 and nullable(symbol) :#and A[item.ir][1] == "#":#and symbol == A[item.ir][0]:
                Flag = False
                tree= "#"
                trees[0] = list(map(addsymbol,[tree]))
                
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
                    if x=="$":
                        mustBe.append((i,1,">="))
                    if x=="L":
                        mustBe.append((i,1,"=="))
                    if not nullable(x):
                        mustBe.append((i,1,">="))
                                        
                                
                p = partitions(n,start,end,mustBe)
                p = list(p)
                for k,q in enumerate(p):
                    
                    print0("partition:",q)
                    tree0 = C()
                    for k0,(i,j) in enumerate(q):
                        
                        newnode = str(A[item.ir][1][k0])
                        
                        for (k,kk,ee),(x, xx) in atomGrammar:
                            newnode = str(newnode.replace(xx,x))
                    
                       
                        flag = False
                        
                        symbol0 = A[item.ir][1][k0]
                        if k0<len(A[item.ir][1]):
                            
                            items0 = list(findItems(i,j,symbol0,item))
                            items1 = list(findItemsScanner(i,j,symbol0,item))
                            items = items0+items1
                            items = list(set(items))
                            
                            for item0 in items:
                                flag, subtree = builtree(i,j,A[item0.ir][0],item0,depth = depth+1,check = check0,frm = "item1",partitionorig= (q,mustBe,A[item.ir]))
                                
                                if len(subtree)==0:
                                    continue
                                
                                if flag:
                                    for sub in subtree:
                                        if not inside(sub,tree0[k][k0].values()) and len(sub)>0:
                                            nt = len(tree0[k][k0])
                                            tree0[k][k0][nt]=sub
                                else:
                                    #if A[item.ir][1] in precedence.keys() and A[item0.ir][1] not in precedence[A[item.ir][1]]:
                                    #    pass
                                    #else:
                                    for sub in subtree:
                                        for subsub in sub:
                                            if not inside(subsub,tree0[k][k0].values()) and len(subsub)>0:
                                                nt = len(tree0[k][k0])
                                                tree0[k][k0][nt]=subsub
    
                            
                            
                    
                    if len(tree0[k]) == len(q):                    
                        t = [list(vo.values()) for ko,vo in tree0[k]]
                        trees1 = list(deepfor2(*t))
                        trees2 = list(map(addsymbol,trees1))
                    
                        trees[k] = trees2
                        
            
            if str(type(trees))== "<class 'contexttest.super_context.<locals>.Y.<locals>.X'>":
               
                trees = [v for k,v in trees]
                trees = list(filter(len, trees))
                
               
            output = Flag,trees
        
        print0("(",start,end,")","[",A[item.ir][0],"=>",A[item.ir][1],item.it,"]",item.m)
        print0(output)
        return output
    
            
    
            
                                    
    def bigbuilder():
        startitem = None
        for I, es in getAll(S):
            if es.m == ["completer"] and len(A[es.ir][1])==es.it and A[es.ir][0]=="^":
                startitem = es
                break
        if startitem==None:
            return None,None
        f, output = builtree(0,len(words),"^",startitem)
        thefinalTree = context.context(node = "^", subtrees = output)
        return output[0]
                    
    return bigbuilder(),stack,lines
    


A = context.context()
GL = context.context()


A[0] = "^","A"
A[1] = "A","L @(@):"


#A[5] = "_ARGS_","*@"
#A[6] = "_KWARGS_","**@"
'''
words = "def f(a):"

output, stack,lines = main(A,words,GL,[])

print("\n")
for i,k in enumerate(output):
    print(i,k)
    print("\n")

'''
