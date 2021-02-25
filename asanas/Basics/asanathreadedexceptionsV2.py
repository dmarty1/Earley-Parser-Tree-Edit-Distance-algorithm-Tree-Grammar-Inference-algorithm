from threadingLib import *
lock = threading.Lock()

class CancellationToken:
   def __init__(self):
       self.is_cancelled = False
       self.lock = threading.Lock()
       self.a = []

   def cancel(self):
       self.is_cancelled = True

def long_risky_computation(x):
    time.sleep(0.01)
    if x == 'a':
        xs = [True, False]
        x = random.choice(xs)
        if x:
            raise Exception()
    else:
        pass

def thread(x,cancel):
    for i in range(100):
        if cancel.is_cancelled:
            sys.exit(0)
        cancel.a.append(x)
        try:
            long_risky_computation(x)
        except:
            cancel.cancel()            
            cancel.a.append((x,"error"))
            sys.exit(0)
            

def process():
    xs = 'abc'
    cancel = CancellationToken()
    pool = ThreadPool(len(xs))
    for x in xs:
        pool.add_task(thread,x,cancel)
    pool.wait_completion()
    
    print(cancel.a)


def main():
    process()

main()
