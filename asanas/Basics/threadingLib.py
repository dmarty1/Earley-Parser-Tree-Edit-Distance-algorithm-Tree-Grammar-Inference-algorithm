import multiprocessing.pool
import threading
from threading import Thread
import time
import random
import sys
from queue import Queue
    
class Worker(Thread):
    def __init__(self, tasks, output):
        Thread.__init__(self)
        self.tasks = tasks
        self.daemon= True
        self.start()
        self.output = output
    def run(self):
        while True:
            func, args, kargs = self.tasks.get()
            try:
                self.output.append(func(*args, **kargs))
            except Exception as e:
                print(e)
            finally:
                self.tasks.task_done()
    def result(self):
        return self.output
    
        
class ThreadPool:
    def __init__(self,num_threads):
        self.tasks = Queue(num_threads)
        self.results = []
        for i in range(num_threads):
            w = Worker(self.tasks,self.results)
            self.results = w.result()
    def add_task(self, func, *args, **kargs):
        self.tasks.put((func, args, kargs))
    def map(self,func, args_list):
        for args in args_list:
            self.add_task(func, args)
        return self.results
    def wait_completion(self):
        self.tasks.join()
