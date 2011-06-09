#!/usr/bin/env python

#
# EntitySystem class.  Create and manage entities and components
# For more information, see: http://cowboyprogramming.com/2007/01/05/evolve-your-heirachy
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
    
    # remove all traces of an entity
    def remove(self, entity):
        for value in self.components.values():
            if entity in value:
                del value[entity]
                
        if entity in self.entities:
            self.entities.remove(entity)

    # find an entity based on a set of criteria
    def find(self, component, conditions={}):
        if component not in self.components.keys():
            return []
        
        result = self.components[component].keys()
        result = self._filter_by_conditions(result, conditions)
        return result
        
    def find_one(self, component, conditions={}):
        result = self.find(component, conditions)
        
        if result == []:
            return None
        else:
            return result[0]

    # add a component to an entity
    def add_component(self, entity, component):
        component.entity_system = self
        component_name = component.__class__.__name__
        
        # if the component has no records, create them
        if component_name not in self.components.keys():
            self.components[component_name] = {}
        
        self.components[component_name][entity] = component
        
    # remove a component from an entity
    def remove_component(self, entity, component_name):
        if component_name not in self.components.keys():
            return
            
        if entity in self.components[component_name]:
            del self.components[component_name][entity]
            
    # does the entity have a component
    def has_component(self, entity, component_name):
        if component_name not in self.components.keys():
            return False
            
        return entity in self.components[component_name]

    # return all the components on an entity
    def get_components(self, entity):
        components = []
        
        for value in self.components.values():
            if entity in value.keys():
                components.append(value[entity])
        
        return components
    
    def get_component(self, entity, component_name):
        return self.components.get(component_name, {}).get(entity, None)
    
    def _filter_by_conditions(self, entities, conditions):
        if conditions == {}:
            return entities

        results = []

        for entity in entities:
            ok = True
            
            for key, value in conditions.items():
                component, prop = key.split('#')
                ok = ok and entity.get(component, prop) == value

            if ok:
                results.append(entity)
        
        return results

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

    # remove a component from this entity
    def remove_component(self, component):
        self.entity_system.remove_component(self, component)
        
    # get a componet for this entity
    def get_component(self, component_name):
        return self.entity_system.get_component(self, component_name)
        
    # does this entity have a component
    def has_component(self, component):
        return self.get_component(component) is not None

    # get a property from a component
    def get(self, component, name):
        component = self.get_component(component)
        return getattr(component, name)

    # set a property to a component
    def set(self, component, name, value):
        component = self.get_component(component)
        setattr(component, name, value)
        
    def __repr__(self):
        strings = ", ".join([str(item) for item in self.entity_system.get_components(self)])
        return "Entity[name: %s, components: %s]" % (self.name, strings)

#
# Singleton EntitySystem
# 

entity_system = EntitySystem()

