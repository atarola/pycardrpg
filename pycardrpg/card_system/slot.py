#!/usr/bin/env python

#
# A slot with tags.  For a card to fit into a slot it must have
# at least all the tags of the slot.
# 

class Slot(object):
    
    def __init__(self, tags=[]):
        self.tags = set(tags)
        self.card = None
    
    def card_fit(self, card):
        return self.tags.issubset(card.tags)
    
    def add_card(self, card):
        if not self.card_fit(card):
            raise DoesNotFitException("Card does not fit into the slot")
        
        self.card = card

#
# Slot Holder
#

class SlotHolder(object):
    
    def __init__(self, base_tags=[]):
        self.base_tags = base_tags
        self.slots = []
        
    def add_slot(self, tags=[]):
        tags = tags.extend(self.base_tags)
        self.slots.append(Slot(tags))
        
    def get_cards(self):
        return [slot.card for slot in self.slots if slot.car is not None]
    
    def add_card(self, card):
        for slot in self.slots:
            if slot.card_fit(card):
                slot.add_card(card)
                return
        
        raise DoesNotFitException("There are no valid spaces for the card.")
    
    def remove_card(self, card):
        for slot in self.slots:
            if slot.card == card:
                slot.card = None
                return

#
# Exception stating that a card doesn't fit in the slot
#

class DoesNotFitException(Exception):
    pass
