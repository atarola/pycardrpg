#!/usr/bin/env python

#
# ScriptSystem
#

class ScriptSystem(object):
    
    def __init__(self):
        self.scripts = {}

    def get(self, name):
        return self.scripts[name][0]

    def add(self, name, script, callback):
        script.callback = self.on_script_done
        self.scripts[name] = (script, callback)
        
    def update(self):
        for script, callback in self.scripts.values():
            script.update()
        
    def on_script_done(self, item):
        for name, data in self.scripts.items():
            script, callback = data
                        
            if script != item:
                continue
            
            del self.scripts[name]
            callback(script)

#
# Script
#

class Script(list):
    
    def __init__(self, callback=None, memory={}):
        self.memory = memory
        self.callback = callback
    
    def update(self):        
        while True:
            if len(self) == 0:
                self.callback(self)
                return
            
            event = self[0]
               
            if event.command == False:
                break
            
            event.update(self.memory)
            self.remove(event)
        
        event.callback = self.on_event_done
        event.update(self.memory)
        
        if len(self) == 0:
            self.callback(self)
            return
            
    def on_event_done(self, event):
        self.remove(event)
        
        if len(self) == 0:
            self.callback(self)

#
# ScriptEvent
# A single item in a script.  If the command flag is set to True,
# the update will be run once.  Otherwise, the update will block
# the script until the callback is called.
#

class ScriptEvent(object):

    def __init__(self, command=False, callback=None):
        self.command = command
        self.callback = callback

    def update(self, memory):
        pass

#
# Script System singleton
#

script_system = ScriptSystem()

