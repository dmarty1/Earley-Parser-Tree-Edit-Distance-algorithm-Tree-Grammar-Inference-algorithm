from threadingLib import *
from parse3 import *
lock = threading.Lock()

cancel = context.context(is_cancelled = False, lock = threading.Lock(), a = [])
def long_risky_computation(e,x):
    time.sleep(0.01)
    if x == e:
        xs = [True, False]
        x = random.choice(xs)
        if x:
            raise Exception()
    else:
        pass

def thread(e,x):
    for i in range(100):
        if cancel.is_cancelled == True:
            sys.exit(0)        
        cancel.a.append(x)
        try:
            long_risky_computation(e,x)
        except:
            cancel.is_cancelled = True
            cancel.a.append((x,"error"))   
            sys.exit(0)
            
def input():
    while True:
        l = random.randint(1,10)
        x = ""
        for i in range(l):
            letter = str(chr(random.randint(97,123)))
            while (letter in x):
                letter = str(chr(random.randint(97,123)))
            x = x+letter
        yield x
                    
def process(xs):
    cancel.is_cancelled = False
    cancel.a = []
    #xs = 'abc'
    pool = ThreadPool(len(xs))
    for x in xs:
        pool.add_task(thread,xs[0],x)
    pool.wait_completion()
    return cancel.a
    
def test(x,y):
    return y[-1]==(x[0],"error")
    
def checker(numofchecks,func,test,input):
    xs = input()
    for i in range(numofchecks):
        x = next(xs)
        y = func(x)
        if not test(x,y):
            yield (x,y)
g = checker(100,process,test,input)
for x in g:
    print(x)
    print("\n")


            
            

