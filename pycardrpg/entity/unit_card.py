#!/usr/bin/env python

from pycardrpg.entity.card import Card
from pycardrpg.entity.slot_holder import SlotHolder

#
# UnitCard class, base class for all units in the game.
# TODO: Skills, Action Deck, Action Cards, Equipment Requirements
#

class UnitCard(Card):
    
    def __init__(self, name, tags=[]):
        tags.append("Unit")
        Card.__init__(self, name, tags)
        
        # Unit Attributes
        self.base_strength = 1
        self.base_intelligence = 1
        self.base_dexterity = 1
        self.base_stamina = 1
        self.fov_radius = 6

        # current experience points
        self.exp = 0
        
        # equipment
        self.equipment = SlotHolder(["Equipment"])
        
        # current hit points and action points
        self.cur_hp = self.max_hp
        self.cur_ap = self.max_ap
    
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
        return self.strength + self.stamina * 2
    
    @property
    def ap_recharge(self):
        return self.dexterity + self.stamina
    
    @property
    def max_ap(self):
        return self.ap_recharge * 10

