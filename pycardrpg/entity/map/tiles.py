#!/usr/bin/env python

#
# A Tile on the map.
# TODO: flyweight pattern?
#

class TileInstance(object):
    def __init__(self, type, pos):
        self.type = type
        self.pos = pos
        self.seen = False
    
    @property
    def symbol(self):
        return self.type.symbol
    
    @property
    def sprite_index(self):
        return self.type.sprite_index
    
    @property
    def passible(self):
        return self.type.passible

    @property
    def opaque(self):
        return self.type.opaque
    
    def __repr__(self):
        return self.symbol

#
# Types of tiles on the map
#

class TileTypes(object):

    # A single tile type
    class TileType(object):
        
        def __init__(self, symbol, sprite_index, passible, opaque):
            self.symbol = symbol
            self.sprite_index = sprite_index
            self.passible = passible
            self.opaque = opaque

    CEILING = TileType('#', 24, False, True)
    WALL = TileType('=', 2, False, False)
    FLOOR = TileType('.', 1, True, False)
