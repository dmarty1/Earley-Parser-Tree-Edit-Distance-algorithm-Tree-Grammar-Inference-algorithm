
from __future__ import print_function
#import module_manager
#module_manager.review()
from itertools import permutations 

import sys
sys.path.append("/Users/diva-oriane/Documents/GitHub/asanas/Parse/")
from parse3 import matchContext

import math
import random

import contexttest as context
sys.path.append("/Users/diva-oriane/Documents/GitHub/asanas/Parse/Earley Parser/")
from earleyparser6 import main as mainEP

from testReader import examples
C = context.context

ex = examples()
curExample22 = ex[22]
A22 = curExample22.grammar
curExample24 = ex[24]
A24 = curExample24.grammar

curExample27 = ex[27]
A27 = curExample27.grammar

GL = context.context()

patterns = C()
patterns["?"].pattern = C(node = 'A', subtrees = [ C( node = 'A' , subtrees = ['(', '[hole0]', ')']), '?'])
patterns["?"].callback = lambda x : C(node = 'A', subtrees = [x])
patterns["?"].sideeffects = lambda symbol,output: [(symbol[0],"#"),(symbol[0],output.hole[0])]
patterns["?"].name = "?"
patterns["?"].arity = 1
patterns["*"].pattern = C(node = 'A', subtrees = [ C( node = 'A' , subtrees = ['(', '[hole0]', ')']), '*'])
patterns["*"].callback = lambda x : C(node = 'A', subtrees = [x])
patterns["*"].sideeffects = lambda symbol,output: [(symbol[0],"#"),(symbol[1],output.hole[0]),(symbol[0],symbol[1]+symbol[0])]
patterns["*"].name = "*"
patterns["*"].arity = 2

patterns["[]"].pattern =  C( node = 'A' , subtrees = ["[", '[hole0]', "]"])
patterns["[]"].callback = lambda x : C(node = 'A', subtrees = [x])
patterns["[]"].sideeffects = lambda symbol,output: [(symbol[0],output.hole[0])]
patterns["[]"].name = "[]"
patterns["[]"].arity = 1


    
def flatten(tree):
    if context.isContext(tree):
        return "".join(map(flatten,tree.subtrees)) 
    elif type(tree)==list:
        return "".join(tree)
    else:
        return tree

def main(A,words,GL):
    usedSymbols = [l for k,(l,r) in A]
    usedSymbols.append("L")
    #rightToLeft = C()
    
    def findNewSymbol():
        alphabet = [chr(ns) for ns in range(66,91)]
        for x in alphabet:
            ok = True
            if x not in usedSymbols:
                return x
    
    def subTreeContext(tree):
        if context.isContext(tree):
            output = ""
            for item in tree.subtrees:
                output+=subTreeContext(item)
            return output
        else:
            return tree
    def counter():
        i =  0 
        while True:
            yield i
            i+=1
    def BtoHole(tree,counter):
        if context.isContext(tree):
            if tree.node == "B":
                newTree = "[hole"+str(next(counter))+"]"
            else:
                newSubtrees = []
                for t in tree.subtrees:
                    
                    nt = BtoHole(t,counter)
                    newSubtrees.append(nt)
                if len(newSubtrees)==1 and "[hole" in newSubtrees[0]:
                    newTree = C(node = tree.node, subtrees = newSubtrees[0])
                else:
                    newTree = C(node = tree.node, subtrees = newSubtrees)
        else:
            newTree = tree
        return newTree
    
    def argMin(listofTree):
        
        def heightOfTree(tree):
            if context.isContext(tree):
                return 1+heightOfTree(tree.subtrees)
            elif type(tree)==list:
                listHeight = []
                for i in tree:
                    listHeight.append(heightOfTree(i))
                return max(listHeight)
            else:
                return 0
        
        def nodeOfTree(tree):
            if context.isContext(tree):
                return 1+nodeOfTree(tree.subtrees)
            elif type(tree)==list:
                listHeight = []
                for i in tree:
                    listHeight.append(nodeOfTree(i))
                return sum(listHeight)
            else:
                return 0
        
        minTrees = []
        minTreeHeight = None
        
        for tree in listofTree:
            treeheight = heightOfTree(tree)
            if minTreeHeight==None or treeheight<minTreeHeight:
                minTreeHeight = treeheight
                minTrees = [tree]
            elif treeheight==minTreeHeight:
                minTrees.append(tree)
        minnumNode = None
        minTrees2 = []
        for tree in minTrees:
            numofnodes = nodeOfTree(tree)
            if minnumNode == None or numofnodes<minnumNode:
                minnumNode = numofnodes
                minTrees2 = [tree]
            elif numofnodes==minnumNode:
                minTrees2.append(tree)
        return minTrees2
            
        
    def walkTree(tree,Anew = C()):
        if context.isContext(tree):
            foundPattern = False
            for kk,pattern in patterns:
                output = matchContext(pattern.pattern,tree)
                if output and type(output.hole[0])==str:
                    newSymbol = C()
                    for i in range(pattern.arity):
                        newSymbol[i] = findNewSymbol()
                    newTree = pattern.callback(newSymbol[0])

                    for l,r in pattern.sideeffects(newSymbol,output):
                        #if r not in rightToLeft.keys():
                        #    rightToLeft[r] = l
                        Anew[len(Anew)] = l,r
                        usedSymbols.append(l)
                        #else:
                        #    print(l,r)
                    return Anew,newTree
                    
                elif output:
                    
                    Anew, newsub = walkTree(output.hole[0],Anew)
                    output.hole[0] = subTreeContext(newsub)
                    newSymbol = C()
                    for i in range(pattern.arity):
                        newSymbol[i] = findNewSymbol()
                    for l,r in pattern.sideeffects(newSymbol,output):
                        #if r not in rightToLeft.keys():
                        #    rightToLeft[r] = l
                        Anew[len(Anew)] = l,r
                        usedSymbols.append(l)

                        
                    #newTree = C(node = tree.node, subtrees = newsub)
                    newTree = pattern.callback(newSymbol[0])
                    
                    
                    return Anew,newTree
                
               
            newsubtrees = []
            #print("SUBTREE",tree.subtrees)
            for subtree in tree.subtrees:
                Anew, newsubtree = walkTree(subtree,Anew)

                #if some of newsubtrees produce a output that is different and others that do not seperate anyways ...?
                newsubtrees.append(newsubtree)
            newTree = C(node = tree.node, subtrees = newsubtrees)
            #print("newTREE",newTree)
            return Anew,newTree
        else:
            return Anew, tree

    AnewTotal = C()
    for k,(l,r) in A:
        print(l,r)
        found3 = []
        try:
            #must take in AnewTotal?????
            found,stack,lines = mainEP(A22,r,C(),["[","]"])
        except: 
            found = C()
        try:
            found2,stack2,lines2 = mainEP(A24,r,C(),[" ","(",")"])
            #print(found2)
        except:
            found2 = C()
    
        if len(found2)>0:
            for ff in argMin(found2):
                form = BtoHole(ff,counter())

                for i,f in enumerate(found):
                    res = matchContext(form,f)
                    print(res)
                    if res:
                        found3.append((form,f))
        else:
            found3 = found
        
        print(found3)
        for (a,b) in found3:
            print(a)
            print(b)
        if len(found3)>0:
            tree = found3[0][1] #within found3 there are some that work and some that do not match patterns
            print("the used one",found3[0])
            Anew, newtree = walkTree(tree,C())
            for kkk,(v1,v2) in Anew:
                AnewTotal[len(AnewTotal)] = v1,v2
            AnewTotal[len(AnewTotal)] = l,flatten(newtree)
        else:
            AnewTotal[len(AnewTotal)] = l,r

        
    for k,(l,r) in A:
        print(l,r)
    for k,(l,r) in AnewTotal:
        print(l,r)
    return mainEP(AnewTotal,words,GL)
    
curEx = ex[27]
A = curEx.grammar
GL = C()
words = curEx.words
precedence = curEx.precedence
       
main(A,words,GL)
