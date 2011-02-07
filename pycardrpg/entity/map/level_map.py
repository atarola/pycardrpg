#!/usr/bin/env python

import pygame

from pycardrpg.entity.map.fov_util import FovUtil
from pycardrpg.entity.map.tiles import TileInstance, TileTypes

#
# Level Map
# 

class LevelMap(object):
    
    def __init__(self, width, height, default=TileTypes.CEILING):
        self.fov = FovUtil(self)
        self.default = default
        self.rect = pygame.Rect(0, 0, width, height)
        self.tiles = [[TileInstance(default, (x, y)) for x in xrange(width)] for y in xrange(height)] 
        
    def get(self, pos):
        if self.rect.collidepoint(pos):
            x, y = pos 
            return self.tiles[y][x]
        else:
            return TileInstance(self.default, pos)
        
    def get_area(self, x, y, width, height):
        tiles = self[y:y + height, x:x + width]
        return TileList(tiles)
    
    def get_fov(self, pos, radius):
        return self.fov.do_fov(pos, radius)
    
    def get_fov_tiles(self, pos, radius):
        positions = self.fov.do_fov(pos, radius)
        return TileList([self.get(foo) for foo in positions])
    
    def __iter__(self):
        for row in self.tiles:
            for tile in row:
                yield tile
    
    def __contains__(self, tile):
        for row in self.tiles:
            if tile in row:
                return True
        
        return False
    
    def __getitem__(self, pos):
        # handle pygame Rect
        if isinstance(pos, pygame.Rect):
            x_args = [pos.left, pos.right, 1]
            y_args = [pos.top, pos.bottom, 1]
            return self._get_tiles_for_lists(x_args, y_args)
        
        # handle slices
        if isinstance(pos[0], slice) or isinstance(pos[1], slice):
            x_args = self._convert_to_xlist_args(pos[0], self.rect.width)
            y_args = self._convert_to_xlist_args(pos[1], self.rect.height)
            return self._get_tiles_for_lists(x_args, y_args)

        # handle tuples
        if isinstance(pos, tuple):
            return self.get(pos)
        
        raise "array access type unknown"

    def _convert_to_xlist_args(self, item, length):
        if isinstance(item, slice):
            return item.indices(length)
        else:
            return item
        
    def _get_tiles_for_lists(self, x, y):
        output = TileList()
        
        for i in xrange(*y):
            for j in xrange(*x):
                tile = self.get((i, j))
                if tile is not None:
                    output.append(tile)
        
        return output

#
# Tile List.  
#

class TileList(list):
    
    # Modify a property on each item in the list at once
    def __setattr__(self, property, value):
        if hasattr(self, property):
            self.__dict__[property] = value 
            return
            
        for item in self:
            setattr(item, property, value)

    def filter(self, property, value):
        return TileList([item for item in self if getattr(item, property) == value])        
