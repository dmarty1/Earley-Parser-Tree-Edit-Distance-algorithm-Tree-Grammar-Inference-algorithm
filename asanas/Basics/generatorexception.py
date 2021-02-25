'''
def gen():
    yield 'so far so good'
    closed = False
    try:
        yield 'yay'
    except ValueError:
        closed = True
        yield "no"
    finally:
        if not closed:
            yield 'boo'
        else:
            yield 'boo2'

g = gen()
print(next(g))
print(next(g))
print(g.throw(ValueError))
print(next(g))
print(next(g))
'''

def gen():
    for i in range(100):
        if i == 10:
            #replace raise with yield and it works
            raise Exception('error')
        else:
            yield ('f', i)

def newgen(generator):
    i =0
    while True:
        print(i)
        try:
            for x in generator:
                g_next = next(generator)
                yield g_next
        except Exception as e:
            print(e)
            yield False
        i+=1

        
                                
xs = newgen(gen())
for x in xs: 
    print(x)
