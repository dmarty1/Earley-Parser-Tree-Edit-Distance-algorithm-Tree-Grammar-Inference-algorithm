"""demonstrate pycairo and pygame"""

from __future__ import print_function
#import module_manager
#module_manager.review()
from itertools import permutations 

import sys
sys.path.append("/Users/diva-oriane/Documents/GitHub/asanas/Parse/")

import math
import random

import contexttest as context
sys.path.append("/Users/diva-oriane/Documents/GitHub/asanas/Parse/Earley Parser/")
from earleyparser6 import main
#from tranform import main as maintranform 

import cairocffi as cairo
import pygame
from testReader import examples
C = context.context

ex = examples()
x = 28
curExample = ex[x]
A = C()#curExample.grammar
S = curExample.S
words = curExample.words
L = curExample.lexicon
antiset = curExample.antiset
setC = []
for a in range(97,123):
    setC.append(chr(a))

GL = context.context()

import time
start = time.time()
t, stack,l = main(A,words,GL,antiset)
end = time.time()
print(end-start)

t = [{'node': '^', 'subtrees': [{'node': 'A', 'subtrees': [{'node': 'A', 'subtrees': ['(', {'node': 'A', 'subtrees': ['[hole0]']}, ')']}, '[hole1]']}]} ,{'node': '^', 'subtrees': [{'node': 'A', 'subtrees': [{'node': 'A', 'subtrees': ['(']}, {'node': 'A', 'subtrees': [{'node': 'A', 'subtrees': ['[', {'node': 'A', 'subtrees': ['a']}, ']']}, {'node': 'A', 'subtrees': [')?']}]}]}]}]
t = [{'node': '^', 'subtrees':[{'node': 'A','subtrees':[{'node':'L','subtrees':['def']},' ', 'fg','(',{'node':'@','subtrees':['A1']},',',{'node':'@','subtrees':['A2']},')']},{'node':'B','subtrees':[{'node':'L','subtrees':['return']},' ', 'z']}]}
,{'node': '^', 'subtrees':[{'node': 'A','subtrees':[{'node':'L','subtrees':['def']}, ' ', 'f']},'(',{'node':'@','subtrees':['A1']},')',{'node': 'A','subtrees':[{'node':'L','subtrees':['def']}, ' ', 'g']},'(',{'node':'@','subtrees':['A2']},')',{'node':'B','subtrees':[{'node':'L','subtrees':['return']},' ', 'z']},{'node':'B','subtrees':[{'node':'L','subtrees':['return']},' ', 'g']}]}]
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
            
t = convertToContext(t)

    
def main(trees,lines):
    treesContext = context.context()
    for t in trees:
        treesContext[len(treesContext)] = context.context(tree = t, elem = context.context(),edges = set(),largestxelem= 0,largestyelem =0, minxelem= 0,minyelem =0  )
    
    
    delta = context.context(x = 0, y= 0)
    def reemovNestings(l,output=[]): 
        if type(l)==list:
            for i in l: 
                if type(i) == list: 
                    reemovNestings(i,output) 
                else: 
                    output.append(i) 
            return output
        return l
        
    def assigningValues(treenum,tree,q0=(0,),q=(0,),output= context.context()):
    
        tree = reemovNestings(tree,[])
        if type(tree)==str:
            #print(tree,q)
            output[q] = tree
            pass
            
        elif type(tree)==list:
            #qk = q+(0,)
            for k,v in enumerate(tree):
                if len(q)>0:
                    qk = q[:-1]+(k,)
                else:
                    qk = (0,)
                assigningValues(treenum,v,q0,qk,output)
                
        
        elif str(type(tree))== "<class 'contexttest.super_context.<locals>.Y.<locals>.X'>":
            qk =q+(0,)
            #print(tree.node,q)
            output[q] = tree.node
            assigningValues(treenum,tree.subtrees,q,qk,output)
        return output
    
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
            
    
    
    def makeelemOld(treenum, tree,q0=(0,),q=(0,),i=0,n=0,depth=0,takenPositions=[],largestxelem=100,largestyelem=100):
        def print0(*args,**kwargs):
            print("\t"*depth,*args,**kwargs)
    
        tree = reemovNestings(tree,[])
        treesContext[treenum].edges.add((q0,q))
        if q0 in treesContext[treenum].elem.keys():
            x = 0 
            for i in q:
                x+=i*50
            y = len(q)*100
    
            while (x,y) in takenPositions:
                x+=50
    
        else:
            x = 100
            y = 100
        
        if x>largestxelem:
            largestxelem = x
        if y>largestyelem:
            largestyelem = y
        
        
        takenPositions.append((x,y))
    
        if type(tree)==str:
            treesContext[treenum].elem[q] = [repr(tree),x,y]
            
            
        elif type(tree)==list:
            #qk = q+(0,)
            for k,v in enumerate(tree):
                if len(q)>0:
                    qk = q[:-1]+(k,)
                else:
                    qk = (0,)
                largestxelem,largestyelem = makeelemOld(treenum,v,q0,qk,k,n,depth+1,takenPositions,largestxelem,largestyelem)
                
        
        elif str(type(tree))== "<class 'contexttest.super_context.<locals>.Y.<locals>.X'>":
            treesContext[treenum].elem[q] = [tree.node,x,y]
            n = len(tree.subtrees[0][0])
            qk =q+(0,)
            largestxelem,largestyelem = makeelemOld(treenum,tree.subtrees,q,qk,i,n,depth+1,takenPositions,largestxelem,largestyelem)
        
        return largestxelem,largestyelem
    
    def makeelem(startx, xyvalues, treenum, tree,q0=(0,),q=(0,),i=0,n=0,depth=0,takenPositions=[],largestxelem=None,largestyelem=None,minxelem = None, minyelem = None):
        def print0(*args,**kwargs):
            print("\t"*depth,*args,**kwargs)
    
        tree = reemovNestings(tree,[])
        treesContext[treenum].edges.add((q0,q))
        (x,y) = xyvalues[q]
        x -= (startx-100)
        if largestxelem ==None or x>largestxelem:
            largestxelem = x
        if largestyelem ==None or y>largestyelem:
            largestyelem = y
        if minxelem == None or x<minxelem:
            minxelem = x
        if minyelem == None or y<minyelem:
            minyelem = y
        
        takenPositions.append((x,y))
    
        if type(tree)==str:
            treesContext[treenum].elem[q] = [repr(tree),x,y]
            
            
        elif type(tree)==list:
            #qk = q+(0,)
            for k,v in enumerate(tree):
                if len(q)>0:
                    qk = q[:-1]+(k,)
                else:
                    qk = (0,)
                largestxelem,largestyelem,minxelem,minyelem = makeelem(startx, xyvalues,treenum,v,q0,qk,k,n,depth+1,takenPositions,largestxelem,largestyelem,minxelem,minyelem)
                
        
        elif str(type(tree))== "<class 'contexttest.super_context.<locals>.Y.<locals>.X'>":
            treesContext[treenum].elem[q] = [tree.node,x,y]
            n = len(tree.subtrees[0][0])
            qk =q+(0,)
            largestxelem,largestyelem,minxelem,minyelem = makeelem(startx, xyvalues,treenum,tree.subtrees,q,qk,i,n,depth+1,takenPositions,largestxelem,largestyelem,minxelem,minyelem)
        
        return largestxelem,largestyelem,minxelem,minyelem
    
    def flat_list(i):
        
        if type(i)== list:
            flat_list = []
    
            for sublist in i:
                if type(sublist)==list:
                    for item in sublist:
                        flat_list.append(item)
                else:
                    flat_list.append(sublist)
            return flat_list
        else:
            return i
    
    for k,v in treesContext:
        levels = assigningValues(k,treesContext[k].tree)
        startx, xyset = countByLevel(list(levels.keys()))
        largestxelem,largestyelem,minxelem,minyelem = makeelem(startx, xyset,k,treesContext[k].tree,takenPositions = [])
        #largestxelem,largestyeelem = makeelemOld(k, treesContext[k].tree,takenPositions = [])
        treesContext[k].largestxelem = largestxelem
        treesContext[k].largestyelem = largestyelem
        treesContext[k].minxelem = minxelem
        treesContext[k].minyelem = minyelem

    
    def draw(surface,items,showtext=True):#elem,edges,tnum,cfactor,shiftx,shifty,showtext=True):
        b = cairo.Context(surface)
        b.move_to(0,0)
        b.rectangle(0,0,1000, 1200)
        b.set_source_rgb(0.5, 0.5, 0.5)
        b.fill()
        points = []
        text = []
        lastX = 0
        for i,(k,v) in enumerate(items):
            for (i,j) in v.edges:
                q = cairo.Context(surface)
                q.move_to(lastX+delta.x+v.cfactor*v.elem[i][1]+v.shiftx,delta.y+v.cfactor*v.elem[i][2]+v.shifty)
                q.line_to(lastX+delta.x+v.cfactor*v.elem[j][1]+v.shiftx,delta.y+v.cfactor*v.elem[j][2]+v.shifty)
                points.append(q)
            for a,aa in v.elem:
                c = cairo.Context(surface)
                c.set_line_width(2)
                xx = lastX+delta.x+v.cfactor*aa[1]+v.shiftx
                yy = delta.y+v.cfactor*aa[2]+v.shifty
                c.arc(xx, yy, 20*v.cfactor, 0, 2.0 * math.pi)
                points.append(c)
                
            
                
        
            if v.d!=False:
                c3 = cairo.Context(surface)
                c3.set_source_rgb(1, 1, 1)
                c3.set_font_size(20)
                c3.select_font_face("Arial")
                c3.move_to(250, 250)
                c3.show_text(v.d)
                points.append(c3)
            lastX += v.largestxelem
    
        
        for p in points:
            p.set_source_rgb(1, 1, 1)
            p.fill_preserve()
            p.stroke()
        
        if showtext:
            c2 = cairo.Context(surface)
            lastX = 0
            for i,(k,v) in enumerate(items):
                for a,aa in v.elem:

                    
                    c2.set_font_size(v.cfactor*20)
                    c2.select_font_face("Courier")
                    halflenword = (len(aa[0])*10*v.cfactor) /2
                    c2.move_to(lastX+delta.x+v.shiftx+v.cfactor*aa[1]-halflenword, delta.y+v.shifty+v.cfactor*aa[2]+5)
                    c2.show_text(aa[0])
                lastX += v.largestxelem
                    
            c2.fill_preserve()
            c2.stroke()
                    
            
        
        for t in text:
            t.fill_preserve()
            t.stroke()
        
        

        c4 = cairo.Context(surface)
        c4.set_font_size(20)
        c4.select_font_face("Courier")
        c4.set_source_rgb(1, 1, 1)
        c4.move_to(50,50)
        c4.show_text(str(tnum+1)+"/"+str(len(treesContext)))
    
        c4.fill_preserve()
        c4.stroke()
        
      
        
    def printContext(surface,C,x,y,elem,edges):
        if type(C)==list:
            newContext = context.context()
            for k,i in enumerate(C):
                newContext[k] = i
            C = newContext
                
    
        if str(type(C))== "<class 'contexttest.super_context.<locals>.Y.<locals>.X'>":
            x+=20
            for k,v in C:
                printable = str(k)
                if type(v)==str or type(v)==int:
                    printable+=str(v)
    
                c = cairo.Context(surface)
                c.set_source_rgb(1,1,1)
                c.set_font_size(20)
                c.select_font_face("Courier")
                c.move_to(delta.x + x,delta.y +y)
                c.show_text(printable)
                c.fill_preserve()
                c.stroke()
                y+=20
                    
                if type(v)!=str and type(v)!=int:
                    x,y = printContext(surface,v,x,y)                
            x-=20
        elif type(C)==str or type(C)==int or type(C)==tuple:
            c = cairo.Context(surface)
            c.set_source_rgb(1,1,1)
            c.set_font_size(20)
            c.select_font_face("Courier")
            c.move_to(x,y)
            c.show_text(str(C))
            c.fill_preserve()
            c.stroke()
            y+=20
        return x,y
        
    
    def printOutput(surface,x,y,elem,edges):
        
        c = cairo.Context(surface)
        c.set_source_rgb(1,1,1)
        c.set_font_size(20)
        c.select_font_face("Courier")
        c.move_to(delta.x + x,delta.y +y)
        c.show_text("OUTPUT")
        c.fill_preserve()
        c.stroke()
        y+=40
        
        c = cairo.Context(surface)
        c.set_source_rgb(1,1,1)
        c.set_font_size(20)
        c.select_font_face("Courier")
        c.move_to(delta.x + x,delta.y +y)
        c.show_text("iteration | j.i | Grammar Rule | Cur Location | Cur Process")
        c.fill_preserve()
        c.stroke()
        y+=40
        
        for k, (A,B,C,D,E) in enumerate(lines):
            c = cairo.Context(surface)
            c.set_source_rgb(1,1,1)
            c.set_font_size(20)
            c.select_font_face("Courier")
            c.move_to(delta.x + x,delta.y +y)
            c.show_text("line"+str(k)+":  "+A+"|\t"+B+"|\t"+C+"|\t"+D+"|\t"+E)
            c.fill_preserve()
            c.stroke()
            y+=20
    
    def printInput(surface,x,y,elem,edges):
        c = cairo.Context(surface)
        c.set_source_rgb(1,1,1)
        c.set_font_size(20)
        c.select_font_face("Courier")
        c.move_to(delta.x + x,delta.y +y)
        c.show_text("INPUT")
        c.fill_preserve()
        c.stroke()
        y+=40
        
        c = cairo.Context(surface)
        c.set_source_rgb(1,1,1)
        c.set_font_size(20)
        c.select_font_face("Courier")
        c.move_to(delta.x + x,delta.y +y)
        c.show_text("GRAMMAR")
        c.fill_preserve()
        c.stroke()
        y+=30
        
        for ind,(l,r) in A:
            c = cairo.Context(surface)
            c.set_source_rgb(1,1,1)
            c.set_font_size(20)
            c.select_font_face("Courier")
            c.move_to(delta.x + x,delta.y +y)
            c.show_text(str(l)+"=>"+str(r))
            c.fill_preserve()
            c.stroke()
            y+=20
        y+=20
        
        c = cairo.Context(surface)
        c.set_source_rgb(1,1,1)
        c.set_font_size(20)
        c.select_font_face("Courier")
        c.move_to(delta.x + x,delta.y +y)
        c.show_text("WORD")
        c.fill_preserve()
        c.stroke()
        y+=30
        
        c = cairo.Context(surface)
        c.set_source_rgb(1,1,1)
        c.set_font_size(20)
        c.select_font_face("Courier")
        c.move_to(delta.x + x,delta.y +y)
        c.show_text(words)
        c.fill_preserve()
        c.stroke()
        y+=40
        
        c = cairo.Context(surface)
        c.set_source_rgb(1,1,1)
        c.set_font_size(20)
        c.select_font_face("Courier")
        c.move_to(delta.x + x,delta.y +y)
        c.show_text("SET C")
        c.fill_preserve()
        c.stroke()
        y+=30
        
        c = cairo.Context(surface)
        c.set_source_rgb(1,1,1)
        c.set_font_size(20)
        c.select_font_face("Courier")
        c.move_to(delta.x + x,delta.y +y)
        c.show_text(str(setC))
        c.fill_preserve()
        c.stroke()
        y+=40
        
        c = cairo.Context(surface)
        c.set_source_rgb(1,1,1)
        c.set_font_size(20)
        c.select_font_face("Courier")
        c.move_to(delta.x + x,delta.y +y)
        c.show_text("LEXICON")
        c.fill_preserve()
        c.stroke()
        y+=30
        
        c = cairo.Context(surface)
        c.set_source_rgb(1,1,1)
        c.set_font_size(20)
        c.select_font_face("Courier")
        c.move_to(delta.x + x,delta.y +y)
        c.show_text(str(L))
        c.fill_preserve()
        c.stroke()
        y+=40
        
        c = cairo.Context(surface)
        c.set_source_rgb(1,1,1)
        c.set_font_size(20)
        c.select_font_face("Courier")
        c.move_to(delta.x + x,delta.y +y)
        c.show_text("GRAMMAR LEXICON")
        c.fill_preserve()
        c.stroke()
        y+=30
        
        c = cairo.Context(surface)
        c.set_source_rgb(1,1,1)
        c.set_font_size(20)
        c.select_font_face("Courier")
        c.move_to(delta.x + x,delta.y +y)
        c.show_text(str(GL))
        c.fill_preserve()
        c.stroke()
        y+=40
        
        return x,y
            
                    
        
    def showname(pos,elem,edges):
        for k,v in elem:
            difx = abs(v[1]-pos[0])
            dify = abs(v[2]-pos[1])
            if difx<20 and dify<20:
                #print(v[0],k)
                return v[0]
        return False
    
    width, height = 1000, 1200
    selection = []
    move = ""
    # Create PyGame surface from Cairo Surface
    movex, movey = 0,0
    cfactor = 1
    fitscreenscale = 1
    setscreen = True
    
    starttn = 0
    showTrees = []
    perGroup = 1

    while True:
        
        pygame.init()
        pygame.display.set_mode((width, height))
        screen = pygame.display.get_surface()
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
        
        items = C()
        #showTrees = [6,7,8,9,10]
        showTrees = []
        for i in range(perGroup):
            if starttn+i not in treesContext:
                break
            showTrees.append(starttn+i)
        #showTrees=[tnum]
        for tnum in showTrees:
            elem = treesContext[tnum].elem
            edges = treesContext[tnum].edges
            
            largestxelem = cfactor*treesContext[tnum].largestxelem 
            largestyelem = cfactor*treesContext[tnum].largestyelem 
            
            if setscreen:
                if treesContext[tnum].minxelem!=None:
                    shiftx = 100-(treesContext[tnum].minxelem)
                if treesContext[tnum].minyelem!=None:
                    shifty = 100-(treesContext[tnum].minyelem)
                
                modWidth = (treesContext[tnum].largestxelem+shiftx+100)
                modHeight = (treesContext[tnum].largestyelem+shifty+100)
                fitscreenscale = min((width/modWidth), (height/modHeight))
                cfactor = fitscreenscale
                shiftx = fitscreenscale*shiftx
                shifty = fitscreenscale*shifty
            else:
                shiftx = 0
                shifty = 0
        
            items[tnum].elem = elem
            items[tnum].edges = edges
            items[tnum].cfactor = cfactor
            items[tnum].shiftx = shiftx
            items[tnum].shifty = shifty
            items[tnum].d = showname(pygame.mouse.get_pos(),elem,edges)
            items[tnum].largestxelem = largestxelem
            items[tnum].largestyelem = largestyelem

        # = [elem,edges,cfactor,shiftx,shifty]
        draw(surface,items)#elem,edges,tnum,cfactor,shiftx,shifty)
        #printContext(surface,curExample,500,50)
        lastx,lasty = printInput(surface,50,largestyelem+100,elem,edges)
        printOutput(surface,lastx,lasty,elem,edges)
        buf = surface.get_data()
        image = pygame.image.frombuffer(buf, (width, height), "ARGB")
        # Tranfer to Screen
        screen.blit(image, (movex, movey))
        pygame.image.save(screen,"imageofvisualtree.png")

        pygame.display.flip()
        
        for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    x = showname(pygame.mouse.get_pos(),elem,edges)
                    if x!=False and x not in selection:
                        selection.append(x)
                    
                if event.type == pygame.QUIT:
                    pygame.display.quit(),sys.exit()
                    return 
                if event.type in [pygame.KEYDOWN]:#, pygame.KEYUP):
                    key = pygame.key.name(event.key)

                    if key=="up":
                        delta.y +=20
                    
                    elif key=="down":
                        delta.y -=20
                    
                    if key=="right":
                        delta.x -=20
                    elif key=="left":
                        delta.x +=20
                    elif key == "space":
                        if starttn<len(treesContext):
                            starttn+=perGroup
                        else:
                            starttn = 0
                    elif key =="=":
                        cfactor*=1.1
                    elif key=="-":
                        cfactor/=1.1
                    elif key=="f":
                        setscreen = not setscreen
                    elif key == "o":
                        cfactor = 1
                        
                        
        
                        

                    
    
if __name__ == "__main__":
    main(t,l)

