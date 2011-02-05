#!/usr/bin/env python

from pycardrpg.card_system.slot import SlotHolder

#
# Unit Class
#

class Unit(object):
    
    def __init__(self, name):
        self.name = name

        # Unit Attributes
        self.base_strength = 1
        self.base_intelligence = 1
        self.base_dexterity = 1
        self.base_stamina = 1

        # current hitpoints and actionpoints
        self.cur_hp = 1
        self.cur_ap = 1
        
        # current experience points
        self.exp = 0
        
        # equipment
        self.equipment = SlotHolder(["Equipment"])
    
    def add_equipment_slot(self, tags=[]):
        self.equipment.add_slot(tags)

    def get_equipment_cards(self):
        return self.equipment.get_cards()

    def add_equipment_card(self, card):
        self.equipment.add_card(card)
    
    def remove_equipment_card(self, card):
        self.equipment.remove_card(card)

    def get_modifier(self, name):
        modifier = 0
        
        for card in self.equipment.get_cards():
            modifier += card.modifiers.get(name, 0)

        return modifier

    @property
    def strength(self):
        return self.base_strength + self.get_modifier("strength")

    @property
    def intelligence(self):
        return self.base_intelligence + self.get_modifier("intelligence")
    
    @property
    def dexterity(self):
        return self.base_dexterity + self.get_modifier("dexterity")
    
    @property
    def stamina(self):
        return self.base_stamina + self.get_modifier("stamina")

    @property
    def max_hp(self):
        return int(round(self.strength  / 2) + self.stamina)
    
    @property
    def max_ap(self):
        return int(round(self.dexterity / 2) + self.stamina)

