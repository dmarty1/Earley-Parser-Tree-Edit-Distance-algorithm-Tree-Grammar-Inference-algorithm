
import inspect
#import Y

grammar = None

def parse(grammar, function):
    source = inspect.getsource(function)
    return None

def before(xs):
    ys = []
    for x in xs:
        for y in x:
            ys.append(y)
    return ys

def after(xs0):
    def xs1():
        for x0 in xs0:
            yield x0
    for x1 in xs1():
        for y in x1:
            yield y

'''
    
for x0 in xs0:
    for y in x0:
        yield y
'''
def transform(x):
    return None

x = "write grammar, parse, and transform such that parse(grammar, after)=F(parse(grammar, before))"
print(x)
print(before("xs"))
print(next(after("xs")))
print(next(after("xs")))