#!/usr/bin/env python

#
# Implements a round-robin scheduler for simple, cooperative
# multitasking with generators
#

class TaskSystem(object):
    
    def __init__(self):
        self.tasks = []
    
    def iterate(self):
        for task in self.tasks:
            
            # it it is not running, kill it
            if not task.is_running: 
                self.tasks.remove(task)
                task.on_stop()
                continue
            
            # if its paused, skip it
            if task.is_paused:
                continue
            
            # if there is no generator on the task, start one
            if task.generator == None:
                task.generator = task.run()
                task.on_start()
            
            try:
                task.generator.next()
            except StopIteration:
                self.tasks.remove(task)
                task.on_stop()
    
    def add(self, task):
        self.tasks.append(task)
        
    def remove(self, task):
        self.tasks.remove(task)

#
# A generator based cooperative task
#

class Task(object):
     
    def __init__(self):
        # used by the scheduler to keep track of this item
        self.generator = None
        self.is_running = True
        self.is_paused = False
    
    def stop(self):
        self.is_running = False
        
    def pause(self):
        self.is_paused = True
        self.on_pause()
        
    def resume(self):
        self.is_paused = False
        self.on_resume()
    
    # should be overridden by a subclass. must be a generator
    def run(self):
        yield
    
    #
    # Event methods
    #
    
    def on_start(self):
        pass
    
    def on_stop(self):
        pass
    
    def on_pause(self):
        pass
    
    def on_resume(self):
        pass

#
# A task that fires off every interval scheduler calls
#

class Timer(Task):
    
    def __init__(self, interval):
        Task.__init__(self)
        self.interval = interval
        self.count = 1
        
    def run(self):
        while True:
            self.manage_count()
            
            if self.count % self.interval == 0:
                self.on_interval()
               
            self.count += 1
             
            yield
    
    def manage_count(self):
        if self.count > self.interval * 10:
            self.count = 0
    
    def on_interval(self):
        pass

