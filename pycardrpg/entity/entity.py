#!/usr/bin/env python

#
# Entity class. A single entity.
#

class Entity(object):
    
    def __init__(self, name, entity_system):
        self.entity_system = entity_system
        self.name = name

    # add a component to this entity
    def add_component(self, component):
        self.entity_system.add_component(self, component)
        
    def get_component(self, component_name):
        return self.entity_system.get_component(self, component_name)