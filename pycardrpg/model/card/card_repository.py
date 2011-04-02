#!/usr/bin/env python

import os
import yaml

from pycardrpg.model.card.card import Card

#
# Repository for cards, created from the template 
#

class CardRepository(object):

    def __init__(self):
        self.equipment = {}
        self.skills = {}
        
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
            
    def get_equipment_card(self, name):
        return self.equipment.get(name, None)
    
    def get_skill_card(self, name):
        return self.skills.get(name, None)

#
# Singleton Instance
#

card_repository = CardRepository()