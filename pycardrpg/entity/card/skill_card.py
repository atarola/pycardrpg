#!/usr/bin/env python

from pycardrpg.entity.card.card import Card

#
# Equipment Card
#

class SkillCard(Card):
    
    def __init__(self, name, tags=[]):
        tags.append("Skill")
        Card.__init__(self, name, tags)