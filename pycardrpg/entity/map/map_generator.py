#!/usr/bin/env python

from pycardrpg.entity.map.level_map import LevelMap
from pycardrpg.entity.map.tiles import TileTypes
from pycardrpg.entity.map.tile_picker import TilePicker

#
# Map Generator
#

class MapGenerator():
    
    def generate(self):
        level_map = LevelMap(16, 16)
        
        # fill map with ceiling
        level_map.get_area(0, 0, 16, 16).type = TileTypes.CEILING
        
        # add floor
        level_map.get_area(2, 2, 6, 1).type = TileTypes.FLOOR
        level_map.get_area(3, 3, 4, 1).type = TileTypes.FLOOR
        level_map[5, 4].type = TileTypes.FLOOR
        level_map[5, 5].type = TileTypes.FLOOR
        level_map.get_area(5, 6, 9, 1).type = TileTypes.FLOOR
        level_map[13, 7].type = TileTypes.FLOOR
        level_map.get_area(4, 8, 10, 6).type = TileTypes.FLOOR
        level_map.get_area(7, 8, 3, 1).type = TileTypes.CEILING
        level_map[7, 11].type = TileTypes.CEILING
        level_map[11, 11].type = TileTypes.CEILING
        
        # add walls
        level_map.get_area(2, 1, 6, 1).type = TileTypes.WALL
        level_map.get_area(6, 5, 8, 1).type = TileTypes.WALL
        level_map.get_area(4, 8, 3, 1).type = TileTypes.WALL
        level_map.get_area(7, 9, 3, 1).type = TileTypes.WALL
        level_map.get_area(10, 8, 3, 1).type = TileTypes.WALL
        level_map[7, 12].type = TileTypes.WALL
        level_map[11, 12].type = TileTypes.WALL
        
        self._select_tiles(level_map)
        return level_map

    def _select_tiles(self, level_map):
        tile_picker = TilePicker(level_map)
        
        for tile in level_map:
            tile.index = tile_picker.pick(tile)
        