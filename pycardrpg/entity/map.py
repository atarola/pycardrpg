#!/usr/bin/env python

from pycardrpg.entity.fov_util import FovUtil
from pycardrpg.entity.tiles import TileInstance

#
# Map Manager
# Encapsulates all the behaviors surrounding the map
# 

class Map(object):
    
    def __init__(self):
        self.fov = FovUtil(self)
        self.changed = True
        self.tiles = {}
        self.seen_tiles = set()

    def get_seen(self):
        return list(self.seen_tiles)
    
    def set_seen(self, pos, seen=True):
        tile = self.get_tile(pos)
        tile.seen = seen
        
        if seen:
            self.seen_tiles.add(tile)
        else:
            self.seen_tiles.remove(tile)

    def set_all_seen(self, positions, seen=True):
        for pos in positions:
            self.set_seen(pos, seen)
            
    def get_fov(self, pos, radius):
        return self.fov.do_fov(pos, radius)

    def get_fov_seen(self, pos, radius):
        self.set_all_seen(self.get_fov(pos, radius))
            
    def is_seen(self, pos):
        return self.get_tile(pos).seen

    def is_passible(self, pos):
        return self.get_tile(pos).passible
    
    def is_opaque(self, pos):
        return self.get_tile(pos).opaque

    def fill(self, pos, width, height, type):
        startx, starty = pos
        endx = startx + width + 1
        endy = starty + height + 1
        
        for x in range(startx, endx):
            for y in range(starty, endy):
                self.set_tile((x, y), type)

    def set_tile(self, pos, type):
        x, y = pos
        instance = TileInstance(type)
        
        if not x in self.tiles.keys():
            self.tiles[x] = {}
        
        self.tiles[x][y] = instance

    def get_tile(self, pos):
        x, y = pos
        
        if not x in self.tiles.keys():
            return None
        
        if not y in self.tiles[x].keys():
            return None
        
        return self.tiles[x][y]
    
    def get_tiles(self, positions):
        return [self.get_tile(pos) for pos in positions]

