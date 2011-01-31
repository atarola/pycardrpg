#!/usr/bin/env python

#
# Base class for all cards
#

class Card(object):
    
    def __init__(self, name, tags=[], actions=[]):
        self.name = name
        self.tags = set(tags)
        self.actions = []
    