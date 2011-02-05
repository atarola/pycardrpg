#!/usr/bin/env python

import uuid

from pycardrpg.card_system.card_repository import repository

#
# Base class for all cards
#

class Card(object):
    
    def __init__(self, name, tags=[]):
        self.id = uuid.uuid1().get_hex()
        self.name = name
        self.tags = set(tags)
        
        repository.register_card(self)