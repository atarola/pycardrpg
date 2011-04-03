#!/usr/bin/env python

from pycardrpg.scene.event_system import EventSystem

#
# A single scene
#            

class Scene(EventSystem):
    
    def __init__(self):
        EventSystem.__init__(self)
    
    def on_start(self):
        pass
    
    def on_update(self, surface):
        pass
    
    def on_exit(self):
        pass
