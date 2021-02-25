import sys
sys.path.append("/Users/diva-oriane/Documents/GitHub/asanas/Parse/")

import contexttest as context
import random
import re
from parse3 import parse3 as parse
from parse3 import parseSpecial

A = context.context()

words = ""
E = context.context()
S  = context.context()


def example1():
    A[0] = "*","S"
    A[1] = "B","I"
    A[2] = "C", "c"
    A[4] = "D","d"
    A[5] = "S", "BCD"
    A[6] = "I","b"
    E.x = "bcd"
def example2():
    A[0] = "*","SQ"
    A[5] = "S", "AB"
    A[7] = "Q", "CD"
    A[1] = "A","a"
    A[6] = "B","b"
    A[8] = "C","c"
    A[9] = "D","d"
    E.x = "abcd"
def example3():
    A[0] = "*","SQ"
    A[5] = "S", "ABC"
    A[7] = "Q", "D"
    A[1] = "A","a"
    A[6] = "B","b"
    A[8] = "C","c"
    A[9] = "D","d"
    E.x = "abcd"

def example4():
    A[0] = "*","S"
    A[1] = "S", "ABCDE"
    A[2] = "A", "c"
    A[3] = "B","l"
    A[4] = "C","a"
    A[5] = "D","s"
    A[6] = "E","s"

    E.x = "class"
    
example4()
    
    
import difflib

def holes(form):
    forms = [form]
    for i in range(len(form)):
        if form[i] == "…":
            forms.append(form[:i]+form[i+1:])
    forms.append(form.replace("…",""))
    for i in range(len(forms)):
        forms[i] = forms[i].replace("…","{}")
    return forms
    
def convert(form):
    for i in form:
        if i.isalpha():
            form = form.replace(i,"{"+i+"}")
    return holes(form)

def necessaryChanges(A,B):
    cases = [(A,B)]
    output = []
    for a,b in cases:     
        for i,s in enumerate(difflib.ndiff(a, b)):
            if s[0]==' ': continue
            elif s[0]=='-':
                output.append(("Delete",s[-1],i))
            elif s[0]=='+':
                output.append(("Add",s[-1],i))    
    return output  


def findall(c,s):
    output = []
    for i in range(len(s)):
        if c == s[i]:
            output.append(i)
    return output 

def apply(Si,checkforform,αparse,changes):

    def Rcalc(Si,checkforform):
        R3 = context.context()
        for k in checkforform:
            if k not in αparse.keys():
                w = k
            else:
                w = αparse[k]
                
            i0 = findall(k,checkforform)
            n0 = len(k) 
            i1 = findall(w,Si) 
            n1 = len(w)
            for j,(u,v) in enumerate(zip(i0,i1)):
                R3[k][j][u][n0] = (v,v+n1)
                    
        return(R3)

    output = str(Si) 
    curLocation = -1
    for (action,c,loc) in changes:
        R3 = Rcalc(output,checkforform)
        cnew = αparse[c]
        y = checkforform[loc]
        for j,w in R3[y]:
            z= w[loc][len(y)]
            if z:
                newloc,end = z
                if action == "Add":
                    output = output[:newloc]+cnew+output[newloc:]
                    checkforform = checkforform[:loc]+c+checkforform[loc:]
                elif action == "Delete":
                    output = output[:newloc]+output[end:]
                    checkforform = checkforform[:loc]+checkforform[loc+1:]

                    
    return output
                    
        
def init():
    S[0] = []
    S[0].append("A→…•"+A[0][0]+"…,0")

#rules = grammar
#items = S

r = context.context()
r.start = "add [* → • α,0 ] to S(0) for all rules [*→α]."
r.scanner = "If [A → … • a…,j ] is in S(i) and a = x(i), then add [A → …a • …,j ] to S(i)."
r.predictor = "If [A → … • B…,j ] is in S(i), then add [B →•α, i] to S(i) for all rules [B → α]."
r.completer = "If [A → … •, j ] is in S(i), then add [B → …A •…,k] to S(i) for all items [B → … • A…,k] in S(j)."
#r.predictorEpsilon = "If [A → … • B…,j ] is in S(i), then add [B →•α, i] to S(i) for all rules [B → α]. If [B] is nullable, then also add [A → …B • …,j] to S(i)."

def splitRule(r):
    r = r.split(", add")
    condition = r[0]
    outcome = "add"+r[1]
    return (condition,outcome)


def convertintoParser(r):
    return r.replace("[","|").replace("]","|").replace("(","|").replace(")","|")

def replace(r, input):
    output = ""
    on = True
    for i in r:
        if i =="|":
            on = not on
            if len(input)>0 and on:
                output+=str(input[0])
                input = input[1:]  
        elif on:
            output +=i
    return output

F = context.context("{}, then{}.", "{}.")   
def match(r):
    while True:
        change = False
        for name,ther in r:
            for k,v in F:
                output = parse(v,ther)
                if output:
                    break
            if len(output)==2:
                for x in iF(output[0],A,E.x):
                    if addTo(A,E.x,output[1],x)!=False:
                        change = True
            elif len(output)==1:
                
                if addTo(A,E.x,output[0])!=False:
                    change = True
        if change == False:
            print(E)
            return E
        
def iF(ther,grammar,words, x = context.context()):
    formatcondition = context.context("If {form} is in {location} and {addition}","If {form} is in {location}")
    for i,formatcond in formatcondition:
        theif = parse(formatcond,ther)
        if len(theif)>0:
            break 
    formaddition = "{a}=x({index})"
    if "addition" in theif:
        theif.addition= theif.addition.replace(" ","")
        theif.addition = parse(formaddition,theif.addition)
    formatlocation = "{S}({i})"
    l = parse(formatlocation,theif.location)
    for i,Sis in E[l.S]:
        for Si in Sis:
            patterns = convert(theif.form)
            Si = Si.replace(" ","")
            for pattern in patterns:
                pattern = pattern.replace(" ","")
                contextDone = parseSpecial(pattern,Si)

                if len(contextDone)>0:
                    break
            if len(contextDone)!=0:
                contextDone.i = i
                if "addition" in theif.keys():
                    if type(theif.addition.index)==str:
                        index = int(theif.addition.index.replace("i",i))
                    
                    if index<len(E.x) and contextDone[theif.addition.a] == E.x[index]:
                        yield contextDone
                else:
                    yield contextDone
        
    for i,Sis in E[l.S]:
        for Si in Sis:
            c = "{}({})".format(l.S,i)
            
    return False
    
def addTo(grammar,words,ther,x=context.context()):
    add = False
    ther = ther.split("for all")
    ther[0] = ther[0].strip().replace(" ","")
    formatadd = "add{add}to{location}"
    formatadd2 ="{}add{add}to{location}"
    theadd = parse(formatadd,ther[0])
    
    if len(theadd)==0:
        theadd = parse(formatadd2,ther[0])
    for j in x:
        for k,v in theadd:
            theadd[k] = v.replace(str(j[0]),str(j[1]))
    formatlocation = "{S}({i})"
    l = parse(formatlocation,theadd.location)
    if l.i not in E[l.S]:
        E[l.S][l.i] = []
    if len(ther)==2:
        ther[1] = ther[1].strip()
        ther[1] = ther[1].replace(" ","")
        formats = context.context("{}[{value}→{α}]in{location}","{}[{value}→{α}]")
        for i,f in formats:
            content = parse(f,ther[1])
            if len(content)!=0:
                break
        if "location" in content:
            content += parse(formatlocation,content.location)
            content.__delitem__("location")
        for j in x:
            for k,v in content:
                if k!=0:
                    content[k] = v.replace(str(j[0]),str(j[1]))
        if "rules"in content[0]:
            for k,i in grammar:
                if i[0] == content.value:
                    x = theadd.add.replace(content.α,i[1])
                    if x not in E[l.S][l.i]: 
                        E[l.S][l.i].append(x)
                        add =True
        elif "items" in content[0]:
            checkforform = "["+content.value+"→"+content.α+"]"
            checkforforms = convert(checkforform)
            changes = necessaryChanges(checkforform,theadd.add)
            for i,Sis in E[l.S]:
                for Si in Sis:
                    for f in range(len(checkforforms)):
                        αparse = parseSpecial(checkforforms[f],Si)
                        if len(αparse)!=0:
                            applied = apply(Si, checkforform, αparse,changes)
                            if len(applied)!=0 and applied not in E[l.S][l.i]:
                                E[l.S][l.i].append(applied)
                                add = True
                            break
        
                        
                            
    else:
        
        x = theadd.add.replace("…","")
        if x not in E[l.S][l.i]:
            E[l.S][l.i].append(x)
            add = True
        
    if add == False:
        return False
    


def outputtoTree(output,tree):
    if len(output)==0:
        return
    if len(output)>2:
        if (output[0] not in tree):
            tree[output[0]] = context.context()
        outputtoTree(output[1:],tree[output[0]])
    else:
        if (output[0] not in tree):
            tree[output[0]] = output[1]


def order(output,word):
    ordered = []
    for i in word:
        w = []
        preCur = ""
        cur = i 
        while preCur!=cur:
            preCur = cur
            for j in output:
                if cur in j[1]:
                    w.append(j)
                    cur = j[0]
        w = w[::-1]
        append = []
        for i,j in w:
            append.append(i)
        append.append(w[-1][-1])
        ordered.append(append)
    return ordered
    
    
def convertToTree(E):
    tree = context.context()
    output = []
    for k,i in E.S:
        for j in i:
            format = "[{start}→{end}•,{}]"
            content = parse(format,j)
            if len(content)!=0:
                output.append([content.start,content.end])
    ordered = order(output,E.x)
    for i in ordered:
        outputtoTree(i,tree)
    return(tree)
 
match(r)    
print(convertToTree(E))