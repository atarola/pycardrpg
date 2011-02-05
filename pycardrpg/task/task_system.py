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


