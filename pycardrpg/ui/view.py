#!/usr/bin/env python

#
# Base View
#

class View(object):
    
    def __init__(self, event_system, entity_system, level_map):
        self.event_system = event_system
        self.entity_system = entity_system
        self.level_map = level_map
    
    def load(self):
        pass
        
    def unload(self):
        pass

    def get_sprites(self):
        return []
