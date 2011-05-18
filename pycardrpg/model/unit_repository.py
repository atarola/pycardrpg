#!/usr/bin/env python

import os
import yaml

from pycardrpg.engine.entity_system import entity_system

from pycardrpg.model.card import card_repository
from pycardrpg.model.component import mapping

#
# Repository for cards, created from the template 
#

class UnitRepository(object):

    def __init__(self):
        self.card_repository = card_repository
        
        # get our cards from the data file
        filename = os.path.join('pycardrpg', 'data', 'templates_units.yaml')
        data = file(filename).read()
        self.templates = yaml.load(data)
        
    def create_from_template(self, name):
        entity = entity_system.new(name)    
        template = self.templates.get(name, {})
     
        components = template.get("components", {})
        self._setup_components(entity, components)
        
        slots = template.get("slots", {})
        self._setup_slots(entity, slots)
        
        return entity

    def _setup_components(self, entity, components):
        for key in components.keys():
            # get this component and add it to the entity
            component = mapping[key]()
            entity.add_component(component)
            
            # add any properties to the components, if needed
            properties = components.get(key, {})  
            if properties:
                for prop, value in properties.items():
                    entity.set(key, prop, value)
    
    def _setup_slots(self, entity, slots):
        unit_component = entity.get_component("UnitComponent")
        
        equipment = slots.get("equipment", [])
        for item in equipment:
            tags = item.get("tags", [])
            
            # TODO: Fix
            unit_component.add_equipment_slot(tags)
            if "content" in item.keys():
                name = item["content"]
                card = self.card_repository.get_equipment_card(name)
                unit_component.add_equipment_card(card)
        
        skills = slots.get("skills", [])
        for item in skills:
            tags = item.get("tags", [])
            
            # TODO: Fix
            unit_component.add_skill_slot(tags)
            if "content" in item.keys():
                name = item["content"]
                card = self.card_repository.get_skill_card(name)
                unit_component.add_skill_card(card)

#
# Singleton Unit Repository
#

unit_repository = UnitRepository()

