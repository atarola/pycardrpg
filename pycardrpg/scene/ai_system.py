#!/usr/bin/env python

#
# AI System
#

class AISystem(object):
    
    def __init__(self, entity_system, map):
        self.entity_system = entity_system
        self.map = map
        
    def update(self):
        print "Update AI System"
