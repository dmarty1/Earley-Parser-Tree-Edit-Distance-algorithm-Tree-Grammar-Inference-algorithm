#test Reader

import math
import random
import sys
sys.path.append("/Users/diva-oriane/Documents/GitHub/asanas/Parse/")
import contexttest as context
from parse3 import parse3 as parse


def examples():
    examples = context.context()
    curValue = 0 
    curExample = 0
    level = "example"

    filepath = '/Users/diva-oriane/Documents/GitHub/asanas/Parse/Earley Parser/ExampleTest.txt' 
    with open(filepath) as fp:
        line = fp.readline()
        while line:
            line = line.strip()            
            if line == "":
                pass
            else:
                if "Example" in line:
                    format = "Example{num}"
                    example = parse(format,line)
                    level = "example"
                    curExample = int(example.num.strip())
                    examples[curExample] = context.context()
                    examples[curExample].S = context.context()
    
                elif "grammar" in line:
                    level = "grammar"
                    examples[curExample].grammar = context.context()
                elif "words" in line:
                    level = "words"
                    examples[curExample].words = ""
                    line = fp.readline().strip()
                    examples[curExample].words = line
                elif "lexicon" in line:
                    level = "lexicon"
                    examples[curExample].lexicon = context.context()
                elif "antiset" in line:
                    level = "antiset"
                    examples[curExample].antiset = ""
                    line = fp.readline().strip()
                    examples[curExample].antiset = list(line)
                elif level == "grammar":
                    if line.isnumeric():
                        curValue = int(line)
                        level = "grammarValue"
                elif level == "grammarValue":
                    v1 = line
                    line = fp.readline()
                    v2 = line.strip()
                    if len(v2)==0:
                        v2 = " "
                    examples[curExample].grammar[curValue] = v1, v2
                    level = "grammar"
                elif level == "lexicon":
                    format = "{i} {x}"
                    y = parse(format, line)
                    examples[curExample].lexicon[y.i] = y.x
                    
                    
    
            line = fp.readline()
            
    return examples
            
            