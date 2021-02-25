from threadingLibwContext import * 

dictionary = {}

def flatten(x):
    y = []
    for xx in x:
        y.extend(xx)
    return y

def generator(ys):
    x = threading.get_ident()

    if x in dictionary:
        threadname = dictionary[x]
    else:
        if len(dictionary)==0:
            dictionary[x]=1
        else:
            values = dictionary.values()
            dictionary[x] = max(values)+1
        threadname = dictionary[x]
    t = threading.current_thread()
    t.setName(threadname)
    for y in ys:
        timer = random.randint(0,10)
        timer = timer/100
        time.sleep(timer)
        z = 'f({:02d})'.format(y)
        print(timer, t.getName(), z)
        yield (timer, t.getName(), z)

def groups(xs, n, f=None):
    nx = len(xs)
    a = list(zip(*[iter(xs)]*n))
    na = len(a)*n
    b = tuple(xs[na:])
    Xs = a
    if na<nx:
        Xs = Xs+[b]
    return Xs

def input():
    x = list(range(51))
    return x

def threads(f, x, n):
    def g(x):
        y = list(f(x))
        return y
    
    initThreadPool(n)
    ynew = map(g,x)
    print(ynew)
    wait_completion()
    return ynew

def threaded_generators(f, x, ng, np):
    if (np<1):
        print("not possible")
        return []
    y = groups(x, ng)
    y = threads(f, y, np)
    y = flatten(y)
    return y

def main():
    f = generator
    x = input()
    y = threaded_generators(f, x, 5, 5)
    for yy in y:
        print(yy)

main()