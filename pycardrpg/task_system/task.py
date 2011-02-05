#!/usr/bin/env python

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