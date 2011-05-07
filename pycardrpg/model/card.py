#!/usr/bin/env python

import os
import random
import yaml

#
# Base class for all cards
#

class Card(object):
    
    def __init__(self, name, tags=[], modifiers={}, commands=[]):
        self.name = name
        self.tags = set(tags)
        self.modifiers = modifiers
        self.commands = commands
        
    def __repr__(self):
        return "Card[name: %s, tags: %s, mods: %s, commands: %s]" % (self.name, self.tags, self.modifiers, self.commands)

#
# A Deck of Cards
#

class Deck(object):

    def __init__(self, cards=[], hand_size=5):
        self.hand_size = hand_size
        self.cards = list(cards)
        self.pile = []
        self.hand = []

    def add_card(self, card):
        self.cards.append(card)
    
    def discard(self, card):
        self.hand.remove(card)
        self.pile.append(card)
        self.fill_hand()

    def shuffle(self):
        random.shuffle(self.cards)

    def reset_deck(self):
        self.cards.extend(self.pile)
        self.pile = []
        self.shuffle()

    def fill_hand(self):
        while len(self.hand) < self.hand_size:
            # if there are no cards in the good, reset
            if len(self.cards) == 0:
                self.reset_deck() 

            # add the next card to the hand
            if len(self.cards) > 0:
                self.hand.append(self.cards.pop())
            else:
                break

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

#
# Repository for cards, created from the template 
#

class CardRepository(object):

    def __init__(self):
        self.equipment = {}
        self.skills = {}
        self.actions = {}

        # get our cards from the data file
        filename = os.path.join('pycardrpg', 'data', 'templates_cards.yaml')
        data = file(filename).read()
        cards = yaml.load(data)

        # create the equipment cards
        for item in cards['equipment']:
            card = Card(**item)
            self.equipment[card.name] = card

        # create the skill cards
        for item in cards['skills']:
            card = Card(**item)
            self.skills[card.name] = card
            
        # create the action cards
        for item in cards['actions']:
            card = Card(**item)
            self.actions[card.name] = card

    def get_equipment_card(self, name):
        return self.equipment.get(name, None)

    def get_skill_card(self, name):
        return self.skills.get(name, None)
        
    def get_action_card(self, name):
        return self.actions.get(name, None)

#
# Singleton Instance
#

card_repository = CardRepository()

#
# Exception stating that a card doesn't fit in the slot
#

class DoesNotFitException(Exception):
    pass

