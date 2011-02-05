#!/usr/bin/env python

from pycardrpg.entity.slot import Slot, DoesNotFitException

#
# Slot Holder
#

class SlotHolder(object):
    
    def __init__(self, base_tags=[]):
        self.base_tags = base_tags
        self.slots = []
        
    def add_slot(self, tags=[]):
        tags.extend(self.base_tags)
        self.slots.append(Slot(tags))
        
    def get_cards(self):
        return [slot.card for slot in self.slots if slot.card is not None]
    
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
