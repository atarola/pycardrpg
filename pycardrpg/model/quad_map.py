#!/usr/bin/env python

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
# Level Map
# 

class LevelMap(object):
    
    def __init__(self, width, height, default=TileTypes.CEILING):
        self.fov = FovUtil(self)
        self.default = default
        self.quad_tree = QuadTree(pygame.Rect(0, 0, width, height))
        
    def get(self, pos):
        return self.quad_tree.get(pos)

    def set_default(self, pos):
        tile = self.quad_tree.get(pos)
        
        if tile is not None:
            return tile
        
        tile = TileInstance(self.default, pos)
        self.quad_tree.insert(tile)
        return tile
        
    def get_rect(self, rect):
        return TileList(self.quad_tree.query(rect))
    
    def get_area(self, x, y, width, height):
        rect = pygame.Rect(x, y, width, height)
        return self.get_rect(rect)
    
    def get_fov_tiles(self, pos, radius):
        tiles = self.fov.do_fov(pos, radius)
        return TileList([self.set_default(pos) for pos in tiles])
        
    def in_view_distance(self, source, target, range):
        positions = self.fov.do_fov(source, range + 1)
        return target in positions
    
    def __iter__(self):
        for item in self.quad_tree:
            yield item

#
# Tile List.  
#

class TileList(list):
    
    # Modify a property on each item in the list at once
    def __setattr__(self, name, value):
        if hasattr(self, name):
            self.__dict__[name] = value 
            return
            
        for item in self:
            setattr(item, name, value)

    def filter(self, name, value):
        return TileList([item for item in self if getattr(item, name) == value])        
        
    def count(self, name, value):
        return len([item for item in self if getattr(item, name) == value])

#
# QuadTree Map
# Note: this is a sparce representation of the map. Any point that doesn't
# exist is a ceiling.
#

class QuadTree(object):
    
    CAPACITY = 4
    
    def __init__(self, boundary):
        self.boundary = boundary
        
        # points in this node
        self.tiles = []
        
        # children
        self.north_west = None
        self.north_east = None
        self.south_west = None
        self.south_east = None
    
    def get(self, pos):
        # if the query isn't in scope, return
        if not self.boundary.collidepoint(pos):
            return None
                
        for tile in self.tiles:
            if tile.pos == pos:
                return tile
        
        if self.north_west is None:
            return None
        
        tile = self.north_west.get(pos)
        if tile is not None:
            return tile
        
        tile = self.north_east.get(pos)
        if tile is not None:
            return tile       

        tile = self.south_west.get(pos)
        if tile is not None:
            return tile
            
        tile = self.south_east.get(pos)
        if tile is not None:
            return tile
            
        return None
    
    def query(self, rect):
        output = []
        
        # if the query isn't in scope, return
        if not self.boundary.colliderect(rect):
            return output
        
        # check for objects at this quad level
        output = [tile for tile in self.tiles if rect.collidepoint(tile.pos)]
        
        # if we have no children, return
        if self.north_west is None:
            return output
        
        output.extend(self.north_west.query(rect))
        output.extend(self.north_east.query(rect))
        output.extend(self.south_west.query(rect))
        output.extend(self.south_east.query(rect))
    
        return output
    
    def insert(self, tile):
        if not self.boundary.collidepoint(tile.pos):
            return False
        
        if len(self.tiles) < QuadTree.CAPACITY:
            self.tiles.append(tile)
            return True
        
        if self.north_west is None:
            self.subdivide()
        
        if self.north_west.insert(tile):
            return True
        
        if self.north_east.insert(tile):
            return True
            
        if self.south_west.insert(tile):
            return True
            
        if self.south_east.insert(tile):
            return True
            
        return False
    
    # split this quad into four equally sized children
    def subdivide(self):
        self.north_west = QuadTree(pygame.Rect(self.boundary.topleft, self.boundary.center))
        self.north_east = QuadTree(pygame.Rect(self.boundary.midtop, self.boundary.midright))
        self.south_west = QuadTree(pygame.Rect(self.boundary.midleft, self.boundary.midbottom))
        self.south_east = QuadTree(pygame.Rect(self.boundary.center, self.boundary.bottomright))
        
    def __iter__(self):
        for item in self.tiles:
            yield item
        
        if self.north_west is not None:
            for item in self.north_west:
                yield item
            
            for item in self.north_east:
                yield item
                
            for item in self.south_west:
                yield item
            
            for item in self.south_east:
                yield item

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
    def x(self):
        return self.pos[0]
        
    @property
    def y(self):
        return self.pos[1]

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
        return self.map.set_default(pos).opaque

    def _set_lit(self, pos):
        self.lit_positions.append(pos)
