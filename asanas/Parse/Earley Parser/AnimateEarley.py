"""demonstrate pycairo and pygame"""

from __future__ import print_function
from itertools import permutations 

import math
import random
import sys
sys.path.append("/Users/diva-oriane/Documents/GitHub/asanas/Parse/")
import contexttest as context
from parse3 import parse3 as parse

import cairocffi as cairo
import pygame


variables = {}
functionNames = {}

def convertValue(value):
    if "[" in value and "]" in value:
        thelist = value.replace("[","").replace("]","").split(",")
        return thelist
    elif "{" in value and "}" in value:
        key = {}
        thedict = value.replace("{","").replace("}","")
        thedict = thedict.split(",")
        if ":" in value:
            format = "{key}:{value}"
            for i in thedict:
                term = parse(format,i)
                key[term.key] = term.value
            return key
            #dict
        elif "{}" == value:
            return {}
        else:
            return set(thedict)
            #set
    elif "context.context()"==value.strip():
        print("makecontext")
        return context.context()
    elif value.isnumeric():
        return int(value)
    elif value == "True" or value == "False":
        return bool(value)
    else:
        return value
        

    
def draw(surface,lines,curloc,keptloc,curfunction):
    points = []
    loc = 50
    c = cairo.Context(surface)
    c.set_source_rgb(1,1,1)
    c.set_font_size(30)
    c.move_to(20,loc)
    c.show_text("Variables")
    loc+=30
    points.append(c)
    
    
    for k,v in variables[curfunction]:
        c = cairo.Context(surface)
        c.set_source_rgb(1,1,1)
        c.set_font_size(30)
        c.move_to(20,loc)
        c.show_text(k)
        c.move_to(50,loc)
        c.show_text(str(variables[curfunction][k]))
        loc +=30
        points.append(c)
    loc = 50

    
    
    c = cairo.Context(surface)
    c.set_source_rgb(1,1,1)
    c.set_font_size(30)
    c.move_to(500,loc)
    c.show_text("Functions")
    loc+=30
    points.append(c)
    
    for f in functionNames:
        c = cairo.Context(surface)
        c.set_source_rgb(1,1,1)
        c.set_font_size(30)
        c.move_to(500,loc)
        c.show_text(f+"=>"+str(functionNames[f]))
        loc+=30
        points.append(c)        
        
    loc = 850
    
    for cnt,line in enumerate(lines):
        c = cairo.Context(surface)
        c.set_source_rgb(1,1,1)
        c.set_font_size(30)
        c.move_to(50,loc)
        if curloc==cnt:
            c.show_text("=>Line {}: {}".format(keptloc+cnt, line.strip()))
        else:
            c.show_text("Line {}: {}".format(keptloc+cnt, line.strip()))
        points.append(c) 
        loc +=30
    
                        
    for p in points:
        #p.set_source_rgb(1, 1, 1)
        p.fill_preserve()
        p.stroke()
    
def main():
    
    width, height = 1000, 1200
    # Create PyGame surface from Cairo Surface
    #while True:
    lines = []
    filepath = 'cleaned.py' 
    curfunction = "outsidefunction"
    variables[curfunction] = context.context()
    counter = 0
    l = ""
    
    with open(filepath, encoding='utf-8') as f:
        data = f.read()
    
    lines = data.split("\n")
    
    play = False
    linesdrawn =[]
    
    for cnt,i in enumerate(lines):
        if cnt%10==0:
            linesdrawn = lines[cnt:cnt+10]
        line = i
        
        step = False
        noequalitycheck =False
        for i in ["if","elif","else","while"]:
            if i in line:
                noequalitycheck = True
       
        if "=" in line and noequalitycheck==False:
            theline = line.split("=")
            for i in range(2):
                key = theline[0].strip()
                value = theline[1].strip()
                if "[" in key:
                    format = "{dict}[{loc}]"
                    thekey = parse(format,key)
                    if thekey.dict in variables[curfunction]:
                        if thekey.loc.isnumeric():
                            thekey.loc = int(thekey.loc)
                        try:
                            variables[curfunction][thekey.dict][thekey.loc] = value
                        except:
                            pass
                        
                else:
                    variables[curfunction][key] = convertValue(value)
        elif "def" in line:
            functioname = line.replace("():","").replace("def","").strip()
            functionNames[functioname] = []
            curfunction = functioname
            variables[curfunction] = context.context()
                
        elif "return" in line:
            theline = line.replace("return","").strip().split(",")
            functionNames[curfunction]+= theline 
        print("Line {}: {}".format(cnt, line.strip()))
        
        pygame.init()
        pygame.display.set_mode((width, height))
        screen = pygame.display.get_surface()
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
        draw(surface,linesdrawn,cnt%10,(cnt//10)*10,curfunction)
        buf = surface.get_data()
        image = pygame.image.frombuffer(buf, (width, height), "ARGB")
        screen.blit(image, (0, 0))
        pygame.display.flip()
        
        while step==False and play==False:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit(),sys.exit()
                    return 
                if event.type == pygame.KEYDOWN:
                    key = pygame.key.name(event.key)
                    if key in ["s"]:
                        step = True
                    if key =="p":
                        play = True
    
                        
                            
        
        
        if line == lines[-1]:
            screenon = True
            while screenon:
                for event in pygame.event.get():                        
                    if event.type == pygame.QUIT:
                        pygame.display.quit(),sys.exit()
                        return
                    
        
if __name__ == "__main__":
    main()
