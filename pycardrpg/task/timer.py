#!/usr/bin/env python

from pycardrpg.task.task import Task

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