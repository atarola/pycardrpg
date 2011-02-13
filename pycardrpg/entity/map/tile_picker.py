#!/usr/bin/env python

import os

import yaml 

#
# Given a position, return the proper tile for that.
#

class TilePicker(object):
    
    def __init__(self, tile_map):
        self.map = tile_map
        self.rules = []
        
        # create our rules from the data file
        filename = os.path.join('pycardrpg', 'data', 'tile_rules.yaml')
        data = file(filename).read()
        rules = yaml.load(data)       
        
        for rule in rules:
            self.rules.append(TileRule(**rule))
        
    def pick(self, tile):
        # get the 3x3 grid of tiles surrounding the position
        tiles = self._get_tiles(tile.pos)
        
        # try to find a rule that matches this situation, 
        for rule in self.rules:
            if rule.matches(tiles):
                return rule.result

        # no rules found, return the default
        return tile.default_index
    
    def _get_tiles(self, pos):
        x, y = pos
        deltas = [(-1, -1), (0, -1), (1, -1), (-1, 0), (0, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
        return [self.map[x + dx, y + dy] for dx, dy in deltas]

#
# Contains a tile rule and the proper result
#

class TileRule(object):

    def __init__(self, rules, result):
        self.result = result
        self.rules = []
        
        for rule in rules:
            if rule == "!":
                # Not ceiling
                self.rules.append(Not("#"))
            elif rule == "*":
                # any rule
                self.rules.append(Any())
                continue
            else:
                # is rule
                self.rules.append(Is(rule))
    
    def matches(self, tiles):
        for rule, tile in zip(self.rules, tiles):
            if not rule.matches(tile.symbol):
                return False
        
        return True
        
#
# A matching rule 
#

class Matcher(object):
    
    def matches(self, tile):
        raise Exception("Subclass me!")

#
# AnyMatcher, just say yes
#

class Any(Matcher):
    
    def matches(self, tile):
        return True

#
# Is, matches if the item and arg are equal
#

class Is(Matcher):
    
    def __init__(self, item):
        self.item = item
        
    def matches(self, tile):

        return self.item == tile
    
#
# Not, matches all args except item
#

class Not(Matcher):
    
    def __init__(self, item):
        self.item = item
        
    def matches(self, tile):
        return self.item != tile

