#!/usr/bin/env python

import math
import pygame

#
# Types of tiles on the map
#

class TileTypes(object):

    # A single tile type
    class TileType(object):

        def __init__(self, symbol, default_index, passible, opaque):
            self.symbol = symbol
            self.default_index = default_index
            self.passible = passible
            self.opaque = opaque

    CEILING = TileType('#', 24, False, True)
    WALL = TileType('=', 2, False, False)
    FLOOR = TileType('.', 1, True, False)

#
# A Tile on the map.
#

class TileInstance(object):
    def __init__(self, type, pos):
        self.type = type
        self.pos = pos
        self.seen = False
        self.index = self.default_index

    @property
    def symbol(self):
        return self.type.symbol

    @property
    def default_index(self):
        return self.type.default_index

    @property
    def passible(self):
        return self.type.passible

    @property
    def opaque(self):
        return self.type.opaque

    def __repr__(self):
        return self.symbol

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
        return self[y:y + height, x:x + width]
    
    def get_fov(self, pos, radius):
        return self.fov.do_fov(pos, radius)
    
    def get_fov_tiles(self, pos, radius):
        positions = self.fov.do_fov(pos, radius)
        return TileList([self.get(foo) for foo in positions])
    
    def in_view_distance(self, source, target, range):
        positions = self.fov.do_fov(source, range + 1)
        return target in positions
    
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

#
# Get the tiles within a radius that the unit can see.
# From: http://roguebasin.roguelikedevelopment.org/index.php?title=PythonShadowcastingImplementation
#

class FovUtil(object):
    # Multipliers for transforming coordinates to other octants, used for fov.
    mult = [
        [1,  0,  0, -1, -1,  0,  0,  1],
        [0,  1, -1,  0,  0, -1,  1,  0],
        [0,  1,  1,  0,  0, -1, -1,  0],
        [1,  0,  0,  1, -1,  0,  0, -1]
    ]

    def __init__(self, map):
        self.map = map
        self.flag = 0

    def do_fov(self, pos, radius):
        x, y = pos
        self.lit_positions = [pos]

        self.flag += 1
        for oct in range(8):
            self._cast_light(x, y, 1, 1.0, 0.0, radius,
                             FovUtil.mult[0][oct], FovUtil.mult[1][oct],
                             FovUtil.mult[2][oct], FovUtil.mult[3][oct], 0)

        return set(self.lit_positions)

    def _cast_light(self, cx, cy, row, start, end, radius, xx, xy, yx, yy, id):
        if start < end:
            return

        radius_squared = radius * radius

        for j in range(row, radius + 1):
            dx, dy = -j-1, -j
            blocked = False
            while dx <= 0:
                dx += 1
                # Translate the dx, dy coordinates into map coordinates:
                pos = (cx + dx * xx + dy * xy, cy + dx * yx + dy * yy)

                # l_slope and r_slope store the slopes of the left and right
                # extremities of the square we're considering:
                l_slope = (dx - 0.5) / (dy + 0.5)
                r_slope = (dx + 0.5) / (dy - 0.5)

                if start < r_slope:
                    continue
                elif end > l_slope:
                    break
                else:
                    # Our light beam is touching this square; light it:
                    if dx * dx + dy * dy < radius_squared:
                        self._set_lit(pos)

                    if blocked:
                        # we're scanning a row of blocked squares:
                        if self._is_blocked(pos):
                            new_start = r_slope
                            continue
                        else:
                            blocked = False
                            start = new_start
                    else:
                        if self._is_blocked(pos) and j < radius:
                            # This is a blocking square, start a child scan:
                            blocked = True
                            self._cast_light(cx, cy, j + 1, start, l_slope,
                                             radius, xx, xy, yx, yy, id + 1)
                            new_start = r_slope

            # Row is scanned; do next row unless last square was blocked:
            if blocked:
                break

    def _is_blocked(self, pos):
        return self.map[pos].opaque

    def _set_lit(self, pos):
        self.lit_positions.append(pos)

