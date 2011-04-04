#!/usr/bin/env python

#
# EntitySystem class.  Create and manage entities and components
#

class EntitySystem(object):
    
    def __init__(self):
        self.entities = []
        self.components = {}
    
    # create a new entity
    def new(self, name):
        entity = Entity(name, self)
        self.entities.append(entity)
        return entity

    # find an entity based on a set of criteria
    def find(self, *components):   
        result = []
        
        # if a component doesn't have any entities associated with it,
        # then the rest of this method is moot
        for component in components:
            if component not in self.components.keys():
                return []
        
        for entity in self.entities:
            has_components = True
            
            for component in components:
                if entity not in self.components[component].keys():
                    has_components = False
                    break
            
            if has_components:
                result.append(entity)
                
        return result    

    def find_one(self, *args):
        result = self.find(*args)
        
        if len(result) > 0:
            return result[0]
        else:
            return None

    # add a component to an entity
    def add_component(self, entity, component):
        component.entity_system = self
        component_name = component.__class__.__name__
        
        # if the component has no records, create them
        if component_name not in self.components.keys():
            self.components[component_name] = {}
        
        self.components[component_name][entity] = component

    # return all the components on an entity
    def get_components(self, entity):
        components = []
        
        for value in self.components.values():
            if entity in value.keys():
                components.append(value[entity])
        
        return components
    
    def get_component(self, entity, component_name):
        return self.components.get(component_name, {}).get(entity, None)

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

    # get a property from a component
    def get(self, component, name):
        component = self.get_component(component)
        return getattr(component, name)

    # set a property to a component
    def set(self, component, name, value):
        component = self.get_component(component)
        setattr(component, name, value)

    # get a componet for this entity
    def get_component(self, component_name):
        return self.entity_system.get_component(self, component_name)

