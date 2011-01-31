#!/usr/bin/env python

from pycardrpg.card_system.deck import Deck

#
# Unit Class
#

class Unit(object):
    
    def __init__(self, name):
        self.name = name

        self.max_hp = 0
        self.max_ap = 0
        self.cur_hp = 0
        self.cur_ap = 0
        
        self.sp = 0
        
        self.deck = Deck()
        self.deck_size = 0
        
        self.equipment = []
        self.skills = []

    def available_actions(self):
        pass
    
    