#!/usr/bin/env python

from pycardrpg.entity.card.card import Card

#
# Equipment Card
#

class EquipmentCard(Card):
    
    def __init__(self, name, tags=[], modifiers={}):
        tags.append("Equipment")
        Card.__init__(self, name, tags)
        self.modifiers = modifiers