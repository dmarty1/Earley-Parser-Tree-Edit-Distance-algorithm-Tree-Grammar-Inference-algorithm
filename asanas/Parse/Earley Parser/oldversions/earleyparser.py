import sys
sys.path.append("/Users/diva-oriane/Documents/GitHub/asanas/Parse/")

import contexttest as context
import random
from itertools import permutations 

'''
A = context.context()


words = "bd"

S  = context.context()
A[0] = "*","S"
A[1] = "B","A"
A[2] = "C", "c"
A[3] = "C", "#"
A[4] = "D","d"
A[5] = "S", "BCD"
A[6] = "A","b"
'''
# # is epsilon
#match B with an empty 
#Si = index of rule(ir),index of target(it), pointer to item set (j)

#CREATE A
def generateDict(size,numofepsilon):
    A = context.context()
    w = ""
    l = size
    possibleEmptyLetters = []
    A[0] = "*","S"

    for i in range(l):
        letter = chr(random.randint(65,90))
        if letter == "S":
            letter = "T"
        while letter in w:
            letter = chr(random.randint(65,90))
        w = w+letter
    A[1] = "S",w
    curNum = 2
    for i in w:
        A[curNum] = i,chr(ord(i)+32)
        curNum+=1
        if numofepsilon>0:
            A[curNum] = i,"#"
            possibleEmptyLetters.append(i)
            numofepsilon-=1
        curNum+=1        
    return [A,possibleEmptyLetters]
    
#CREATE WORD
def generateWord(Dict):
    word = ""
    remL = random.randint(0,len(Dict[1]))
    theWord  = Dict[0][1][1]
    for l in theWord:
        if remL!=0 and l in Dict[1]:
            remL-=1
        else:
            word = word + str(chr(ord(l)+32))
    return word
 
#CHECKER WITH OUTPUT   
  
def powerset(a):
    # returns a list of all subsets of the list a
    if (len(a) == 0):
        return [[]]
    else:
        allSubsets = [ ]
        for subset in powerset(a[1:]):
            allSubsets += [subset]
            allSubsets += [[a[0]] + subset]
        return allSubsets
 
def expectedResult(holes,GD,words,output):
    o = context.context()
    curset = 0
    dif = abs(len(GD[0][1][1])-len(words))
    expectedoutputsize = 2**(holes-dif)
    if len(output)!=expectedoutputsize:
        return False
    switches = []
    for c in GD[1]:
        if chr(ord(c)+32) in words:
            switches.append(c)
            
    for x in powerset(switches):
        o[curset] = context.context()
        o[curset]["*"] = context.context()
        o[curset]["*"]["S"] = context.context()
        for c in words:
            o[curset]["*"]["S"][chr(ord(c)-32)] = c
        for c in GD[1]:
            if chr(ord(c)+32) not in words:
                o[curset]["*"]["S"][c] = "#"

        for y in x:
            o[curset]["*"]["S"][y] = "#"
            
        curset+=1
    return o

def compareResults(expected,actual):
    ok = False
    expectedlist = []
    actuallist = []
    
    for i in expected:
        a = i[1]["*"]["S"]
        sublist = set()
        for k in a:
            sublist.add(k)
        expectedlist.append(sublist)
    for j in actual:
        a = j[1]["*"]["S"]
        sublist = set()
        for k in a:
            sublist.add(k)
        actuallist.append(sublist)
        
    for i in expectedlist:
        if i not in actuallist:
            return False
            
    return True
    

#MAIN LOOP
def main(A,S,words,L):
    
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
            word = words.replace(a,b)
        return word 
    
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
    Aold = A
    A = convertAwithAtomic(A)
    words = convertWordWithAtomic(words)
    
    '''
    def nullable(symbol):
        for k,i in A:
            if i[0] == symbol:
                if i[1] == "#":
                    return True
        return False
    '''
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
        #print(line)
            
    def predictor():
        modify = False
        add = []
        for i,Sis in S:
            for k1, Si in enumerate(Sis):
                B = target(Si)
                if B!=False:
                    for k,v in A:
                        if v[0] == B:
                            ns = context.context(
                                ir = k,
                                it = 0,
                                j = i,
                                #m = ["predictor"]
                                m = Si.m+ [("predictor",i,k1)],
                                #p = Si.p ,
                                #s = Si.s 
                            )
                            add.append((i,ns,Si))
        
        for i,ns,Si in add:
            if not in2(ns,S[i]):
                S[i].append(ns)
                modify = True
        return modify
    
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
                            #m = Si.m+ [("predictorepsilon",i,k1)],
                            #p = Si.p,
                            #s = Si.s +[getNullK(B),"this"]
                        )
                        add.append((i,ns,Si))
    
                    for k,v in A:
                        if v[0] == B:
                            ns = context.context(
                                ir = k,
                                it = 0,
                                j = i,
                                m = ["predictor"],
                                #m = Si.m+ [("predictor",i,k1)],
                                #p = Si.p,
                                #s = Si.s 
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
                #p = [],
                #s = []
            )
        S[0].append(ns)
    
    def scannerold():
        modify = False
        add = []
        for i,Sis in S:
            for k,Si in enumerate(Sis):
                B = target(Si)
        
                if B!=False:
                    if (i<len(words) and (B == words[i])):
                        ns = context.context(
                            ir = Si.ir,
                            it = Si.it+1,
                            j = Si.j,
                            m = ["scanner"]
                        )
                        add.append((i+1,ns))
        if len(S[i+1])==0:
            S[i+1]=[]
        for i,ns in add:
            if not in2(ns,S[i]):
                S[i].append(ns)
                modify = True
        return modify
    
    
    def scanner():
        modify = False
        add = []
        for i,Sis in S:
            for k,Si in enumerate(Sis):
                B = target(Si)
                if B!=False:
                    #could remove the addition now 
                    addition = 1
                    if  (i<len(words) and (B == words[i])):
                        for k,v in L:
                            if i+len(v)<len(words) and words[i:i+len(v)]==v:
                                #print()
                                addition = len(v)
                        ns = context.context(
                            ir = Si.ir,
                            it = Si.it+addition,
                            j = Si.j,
                            m = ["scanner"]
                        )
                        add.append((i+addition,ns))
        #if len(S[i+1])==0:
        #    S[i+1]=[]
        for i,ns in add:
            if i not in S:
                S[i]=[]
            if not in2(ns,S[i]):
                S[i].append(ns)
                modify = True
        return modify
        
        
    def completerold():
        modify = False
        add = []
        for i,Sis in S: 
            for Si in Sis:
                B = target(Si)
                if B==False:
                    for k,elem in enumerate(S[Si.j]):
                        #print(A[elem.ir][0],nullable(A[elem.ir][0]))
                        #verification = False
                        #if target(elem)!=False and target(elem) in words:
                        #    s1 = context.context(ir=elem.ir,it=elem.it+1, j= elem.j, m = ["scanner"])
                        #    s2 = context.context(ir = elem.ir, it=elem.it+1, j = elem.j-1, m = ["completer"])
                        #    if (s2 in S[Si.j-1]) or (s1 in S[Si.j]):
                        #        verification = True                                 
                            
                        if target(elem)== False:
                            pass
                        elif target(elem)==A[Si.ir][0] or (target(elem) in words) or nullable(A[elem.ir][0]):#or target(elem)=="#":
                            
                            ns = context.context(
                                ir = elem.ir,
                                it = elem.it+1,
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
        
    def completer():
        modify = False
        add = []
        for i,Sis in S: 
            for Si in Sis:
                B = target(Si)
                if B==False:
                    for k,elem in enumerate(S[Si.j]):
                        #print(A[elem.ir][0],nullable(A[elem.ir][0]))
                        #verification = False
                        #if target(elem)!=False and target(elem) in words:
                        #    s1 = context.context(ir=elem.ir,it=elem.it+1, j= elem.j, m = ["scanner"])
                        #    s2 = context.context(ir = elem.ir, it=elem.it+1, j = elem.j-1, m = ["completer"])
                        #    if (s2 in S[Si.j-1]) or (s1 in S[Si.j]):
                        #        verification = True                                 
                        
                        if target(elem)== False:
                            pass
                        elif target(elem)==A[Si.ir][0] or (target(elem) in words) or (nullable(A[elem.ir][0]) and i==elem.j):#or target(elem)=="#":
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
                        
        
    init()
    iteration = 1
    while True:
        try:
            #print("iteration", iteration)
            modify1 = predictorepsilon()
            #print(S,modify1)
            while predictorepsilon():
                pass
            modify2 = scanner()
            while scanner():
                pass
            modify3 = completer()
            while completer():    
                pass
            iteration+=1
            if modify1==False and modify2==False and modify3 == False:
                break
        except Exception as e:
            print(e)
            break
    
    
        
    def converter():
        #print(A)
        for i in S.keys():
            for elem in S[i]:
                convertAndSI(i,elem)
    
    #print("\n")
    #print("converter")
    converter()
    #print("\n")
    
    #building a tree
    
            
    def outputtoTree(output,tree):
        if len(output)==0:
            return
        if len(output)>0:
            if (output[0] not in tree):
                tree[output[0]] = context.context()
            outputtoTree(output[1:],tree[output[0]])
        '''
        else: <=2E
            if (output[0] not in tree):
                tree[output[0]] = output[1]
        '''
        
    
    #ir is which A
    #it is where in A[ir]
    #j is where in words
    
    def indexes():
        index = context.context()
        for i in S.keys():
            for Si in S[i]:
                if (Si.m == ["completer"] or Si.m == ["scanner"]):
                    st = (Si.j,i)
                    if Si.m==["scanner"]:
                        st = (i-1,i)
                    if st not in index:
                        index[st] = []
                    index[st].append(Si)
        return index
    
    ind = indexes()
    for k,vs in ind:
       for v in vs:
            #print(k,v,A[v.ir])
            pass
    

    def deepfor(*xs):
        if len(xs)>0:
            hs = xs[0]
            ts = xs[1:]
            for h in hs:
                for t in deepfor(*ts):
                    yield [h]+t
        else:
            yield []
    
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

                
            
    
    #print(convertWordWithAtomic("class ab class"))
    #return False, False

    def partitions(n,start,end,mask):
    
        
                
        ns = list(range(start,end+1))

        xs = [ns for _ in range(n+1)]

        seen = []
        for p in deepfor(*xs):
            
            
            #continue
            c0 = sumdiffs(p) == end-start#n
            c1 = increase(p)
            if c0 and c1 :
            
                    
                pp = []
                '''
                print("p",p)
                for i in range(len(p)-1):
                    for (u,v),(h,g) in Atomic:
                        if wordNew[p[i]:p[i+1]] == g:
                            for j in range(i+1,len(p)):
                                p[j]+=len(h)
                print("pnew",p)
                '''
                pp0 = []
                for i in range(len(p)-1):
                    
                    pp.append((p[i],p[i+1]))
                
                if pp not in seen:
                    seen.append(pp)
                    yield pp
                
                nexti = p[0]
                for i in range(len(p)-1):
                    if i in mask:
                        pp0.append((p[i],p[i]))
                    pp0.append((p[i],p[i+1]))
                
                if pp0 not in seen:
                    seen.append(pp0)
                    yield pp0
            
                
                '''
                for m in mask:
                    
                    qq = list(pp)
                    print("pp",pp)
                    qqm = qq[m][0],qq[m][0]
                    if m <len(qq)-1:
                        qqm1=qq[m][1],qq[m+1][1]
                        qq[m+1] = qqm1
                    qq[m]=qqm
                    if qq not in seen:
                        seen.append(qq)
                        print("qq",qq)
                        yield qq
                '''
                
    
    
            
    def recursive(item):
        return A[item.ir][0] in A[item.ir][1]
        
    def findItems(start,end,symbol):
        #print(start,end,symbol)
        for i in ind[(start,end)]:
            if A[i.ir][0] == symbol:
                yield i 
    
                        
    def findItemsScanner(start,end,symbol):
        #print(start,end,symbol)
        if end-start==1:
            for i in ind[(start,end)]:
                if i.m == ["scanner"] and words[start]==symbol:
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
                    if A[v.ir][0] in symbol and v.m ==["scanner"]:
                        #if A[v.ir][0] is connected to symbol in some way 
                        return False
    
        return True
    
                
    J = context.context()
    CycleCheck = True
    def builtree(start,end,symbol,item,depth=0,check=[]):
        def print0(*args,**kwargs):
            print("\t"*depth,*args,**kwargs)
        #print0(start,end,symbol,item)
        trees = context.context()
        output = None
        if CycleCheck:
            next = [start,end,symbol,item]
            check0 = list(check)
            if next in check0:
                output = False, []
                #print0("check")
            else:
                check0.append(next)
        subtrees = context.context()
        node = symbol
        #print(symbol,end,start)
        #if end-start == len(A[item.ir][1])  and symbol == A[item.ir][0] and item.m == ["scanner"]:
        #    return True,A[item.ir][1]#words[start]
        if output==None:
            if end-start == 1 and symbol == A[item.ir][0] and item.m == ["scanner"]:
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
                #print("here")
                #return True,A[item.ir][1]#words[start]
            #if end-start==A[item.ir][1] and symbol == A[item.ir][0] and item.m ==["scanner"]:
            #    print(symbol)
            #    return True,A[item.ir][1]
            
            #there are only certain cases where this should be in invoked, it is invoked too often only if there was no scanner for this iteam 
            
            elif end-start==0 and nullable(symbol) and symbol == A[item.ir][0]:
                #print(symbol,end,start)
                Flag = True
                tree="#"
                trees=tree
                
            else:
                Flag = False
                n = len(A[item.ir][1]) 
                mask = [i for i,x in enumerate(A[item.ir][1])if nullable(x)]
                mask = []
                p = partitions(n,start,end,mask)
                
                
                #words = convertWordWithAtomic(words)
                #the converting before the partitions take place 
                #maybe duing the atomic conversion before the builtree in the builder tree change all the symbols in 
                
                #p = list(p)
                for k,q in enumerate(p):
                    #print0("part",k,q, A[item.ir])
                    ok = True
                    for k0,(i,j) in enumerate(q):
                        subtrees[k0]=[]
                        #A[item.ir][1][k0] must be nullabel if len(i,j)==0 otherwise skip this p all together 
                        #if i-j==0 and not nullable(A[item.ir][1][k0]):
                        #    break   
                        flag = False
                        if k0<len(A[item.ir][1]):
                            items = list(findItems(i,j,A[item.ir][1][k0]))
                            if len(items)>0:
                                for item0 in items:
                                    flag, subtree = builtree(i,j,A[item0.ir][0],item0,depth+1,check0)
                                    compar1 = str(subtree).replace("[","").replace("]","")
                                    compar2 = str(subtrees[k0]).replace("[","").replace("]","")
                                    subtree = context.context(node=A[item.ir][1][k0], subtrees = subtree)
                                    if not flag and compar1 not in compar2:
                                        subtrees[k0].append(subtree)
    
                            if len(subtrees[k0])==0:
                                items2 = list(findItemsScanner(i,j,A[item.ir][1][k0]))
                                if len(items2)>0:
                                    for item0 in items2:
                                        flag, subtree = builtree(i,j,A[item0.ir][0],item0,depth+1,check0)
                                        #print0(flag,subtree)
                                        #if flag:
                                        #    subtree = context.context(node=node, subtrees=subtree)
                                        compar1 = str(subtree).replace("[","").replace("]","")
                                        compar2 = str(subtrees[k0]).replace("[","").replace("]","")
                                        if subtree=="#":
                                            subtree = context.context(node=A[item.ir][1][k0],subtrees=subtree)
                                        if compar1 not in compar2:
                                            subtrees[k0].append(subtree)
                        #if flag:
                        #    subtrees[k0] = context.context(node=node,subtrees= subtrees[k0])
                    
    
                    
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
            
            
            if False:
                treetest = str(trees)
                if (start,end) not in J.keys():
                    #print(start,end)
                    J[(start,end)] = []
                    
                if treetest in J[(start,end)]:
                    output = False,[]
                else:
                    J[(start,end)].append(treetest)
                    output = False,trees
            output = Flag,trees
            
        #print0(start,end,symbol,item,output)

        return output
    
            
                                    
    def bigbuilder():
        startitem = ""
        for i in S.keys():
            for Si in S[i]:
                if Si.m == ["completer"] and len(A[Si.ir][1])==Si.it and A[Si.ir][0]=="*":
                    startitem = Si
                    break
        return builtree(0,len(words),"*",startitem)
                    
    return bigbuilder()


#DEFINE HERE
'''
l = random.randint(1,10)
h = random.randint(0,l)
GD = generateDict(l,h)
A = GD[0]
words = generateWord(GD)
S = context.context()
    
output = (main(A,S,words))  
print(output)
print("\n")
expected =expectedResult(h,GD,words,output)
print(expected)
print(compareResults(expected,output))
'''
'''
ok = True
c = 0
while ok and c<1:
    l = random.randint(1,10)
    h = random.randint(0,l)
    GD = generateDict(l,h)
    A = GD[0]
    words = generateWord(GD)
    S = context.context()
    output = (main(A,S,words))  
    expected =expectedResult(h,GD,words,output)
    ok = compareResults(expected,output)
    c+=1
print(ok)
'''
A = context.context()
'''
line = "class rep"
allwords =line.split(" ")
terms = ["class","def"]

VariableGrammar = context.context()
VariableGrammar[0] = "*","V"
VariableGrammar[1] = "V","CV"
VariableGrammar[2] = "V","#"
for i in range(3,29):
    VariableGrammar[i] = "C",chr(97+i-3)
    

A[0] = "*","S"
A[1] = "S", "V"
A[2] = "V","class"

outputs = []
for words in allwords:
    S = context.context()
    if words in terms:
        print(words)
        b, output = (main(A,S,words)) 
        outputs.append(output)
    else:
        print(words)
        b,output = (main(VariableGrammar,S,words))
        outputs.append(output)

for i in outputs:
    print(i)
        
        
    

#for i in range(2,28):
#    A[i] = "C",chr(65+i-2)
'''

L = context.context()
'''
L[0] = "class"
L[1] = "def"

S = context.context()
words = "class a"
A[0] = "*","S"
A[1] = "S","L V"
A[2] = "L","class"
A[56] = "V","CV"
A[59] = "V","#"
A[60] = "C","a"
A[61] = "C","b"
words = "class ab"
'''
#A[4] = "C","c"
#A[4] = "Q","AB"
#A[2] = "A","a"
#A[3] ="B","b"

#for i in range(2,28):
#    A[i] = "C",chr(65+i-2)
#for i in range(28,54):
#    A[i] = "C",chr(97+i-28)
#A[2] = "C","A"
#A[3] = "C","B"

#A[55] = "V","CV"
#A[56] = "V","CV"
#A[57] = "C","ab"
#A[58] = "V","#"
#A[58] = "B","#"

A = context.context()

A[0] = "*","S"
A[1] = "S", "A B"
A[2]  = "A", "class"
A[3]= "B", "report"


words = "class report"
S = context.context()
f, output = (main(A,S,words,L)) 
print("\n")
print(output) 

'''
# x axis values 
a = ns
# corresponding y axis values 
b = avgs
  
# plotting the points 
print(a)
print(b) 
plt.plot(a, b,label = "data",marker = "o") 
plt.plot(a,fx(a),label = "model2")
plt.plot(a,fx2(a),label = "model1")
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
'''