#!/usr/bin/env python

from pycardrpg.model.card import SlotHolder, Deck

#
#  Base component for all units in the game
#

class UnitComponent(object):
    
    def __init__(self):
        # Unit Attributes
        self.base_strength = 1
        self.base_intelligence = 1
        self.base_dexterity = 1
        self.base_stamina = 1
        self.fov_radius = 6

        # current experience points
        self.exp = 0
        
        # equipment and skills
        self.equipment = SlotHolder(["Equipment"])
        self.skills = SlotHolder(["Skill"])
        
        self.deck = Deck()
        
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

    def add_skill_slot(self, tags=[]):
        self.skills.add_slot(tags)

    def get_skill_cards(self):
        return self.skills.get_cards()

    def add_skill_card(self, card):
        self.skills.add_card(card)
        
    def remove_skill_card(self, card):
        self.skills.remove_card(card)

    def get_modifier(self, name):
        modifier = 0
        
        for card in self.equipment.get_cards():
            modifier += card.modifiers.get(name, 0)

        for card in self.skills.get_cards():
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
    def max_ap(self):
        return self.ap_recharge * 10
    
    @property
    def ap_recharge(self):
        return self.dexterity + self.stamina

    @property
    def attack(self):
        # TODO: make more complicated
        return self.get_modifier('attack')
        
    @property
    def defense(self):
        # TODO: make more complicated
        return self.get_modifier('defense')
    
#
# A renderable thing
#

class RenderComponent(object):

    def __init__(self):
        self.pos = (0, 0)
        self.index = 0
        
    def __repr__(self):
        return 'RenderComponent[pos: %s, index: %s]' % (self.pos, self.index)

#
# Player Component
#

class PlayerComponent(object):
    pass
    

#
# NPC Component
#

class NpcComponent(object):
    pass

#
# Component Mapping
# Used to reference the component classes by name
#

mapping = {
    "UnitComponent": UnitComponent,
    "RenderComponent": RenderComponent,
    "PlayerComponent": PlayerComponent,
    "NpcComponent": NpcComponent
}

