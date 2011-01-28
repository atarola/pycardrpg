#!/usr/bin/env python

#
# Base class for all cards
#

class Card(object):
    
    def __init__(self, name, tags=[]):
        self.name = name
        self.tags = set(tags)