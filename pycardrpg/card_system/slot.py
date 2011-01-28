#!/usr/bin/env python

#
# A slot with tags.  For a card to fit into a slot it must have
# at least all the tags of the slot.
# 

class Slot(object):
    
    def __init__(self, name, tags=[]):
        self.name = name
        self.tags = set(tags)
        self.card = None
        
    def add_card(self, card):
        if not self.tags.issubset(card.tags):
            raise DoesNotFitException("Card does not fit into the slot")
        
        self.card = card

#
# Exception stating that a card doesn't fit in the slot
#

class DoesNotFitException(Exception):
    pass
