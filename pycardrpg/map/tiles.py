#!/usr/bin/env python

#
# A Tile on the map.
# TODO: flyweight pattern?
#

class TileInstance(object):
    def __init__(self, type):
        self.type = type
        self.seen = False
    
    @property
    def symbol(self):
        return self.type.symbol
    
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
        
        def __init__(self, symbol, passible, opaque):
            self.symbol = symbol
            self.passible = passible
            self.opaque = opaque

    WALL = TileType('#', False, True)
    FLOOR = TileType('.', True, False)
    DOOR = TileType('=', True, True)
