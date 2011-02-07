#!/usr/bin/env python

import unittest
from unittest import TestCase

import pygame

from pycardrpg.entity.map.level_map import LevelMap
from pycardrpg.entity.map.tiles import TileTypes

#
#
#

class LevelMapTest(TestCase):

    def setUp(self):
        self.map = LevelMap(10, 10)
  
    def testGet(self):
        pos = (1, 1)
        self.map.get(pos).seen = True
        
        self.assertTrue(self.map.get(pos).seen)
  
    def testArraySyntaxSinglePosition(self):
        self.map[1, 1].seen = True
        
        self.assertTrue(self.map[1, 1].seen)

    def testArraySyntaxWithSlice(self):
        tiles = self.map[2:4, 2:4]
        
        self.assertEquals(len(tiles), 4)
        
    def testArraySyntaxWithRect(self):
        rect = pygame.Rect(2, 2, 2, 2)
        self.map[rect].seen = True
        
        self.assertTrue(self.map[2, 2].seen)
        self.assertTrue(self.map[3, 3].seen)
        self.assertFalse(self.map[1, 1].seen)
        self.assertFalse(self.map[4, 4].seen)

    def testSettingPropertiesWithSlice(self):
        self.map[2:4, 2:4].seen = True
        
        self.assertTrue(self.map[2, 2].seen)
        self.assertTrue(self.map[3, 3].seen)
        self.assertFalse(self.map[1, 1].seen)
        self.assertFalse(self.map[4, 4].seen)
 
    def testSettingPropertiesWithSliceExclusive(self):
        self.map[2:4, 2:4].seen = True
        
        self.assertFalse(self.map[2, 4].seen)

    def testGetArea(self):
        tiles = self.map.get_area((2, 2), 2, 2)
        
        self.assertEquals(len(tiles), 4)

    def testFOVEmptyArea(self):
        pos = (1, 1)
        self.map.get_area(pos, 8, 8).type = TileTypes.FLOOR
        tiles = self.map.get_fov(pos, 5)      
        
        self.assertTrue(self.map[1, 5] in tiles)
        self.assertFalse(self.map[1, 6] in tiles)
        self.assertTrue(self.map[5, 1] in tiles)
        self.assertFalse(self.map[6, 1] in tiles)

    def testFOVBlocked(self):
        pos = (1, 1)
        self.map.get_area(pos, 8, 8).type = TileTypes.FLOOR
        self.map[1, 3].type = TileTypes.WALL
        tiles = self.map.get_fov(pos, 5)
        
        self.assertTrue(self.map[1, 3] in tiles)
        self.assertFalse(self.map[1, 4] in tiles)
        
    def testFilter(self):
        self.map[2, 2].seen = True
        tiles = self.map[2:4, 2:4]
        
        self.assertEquals(len(tiles.filter("seen", True)), 1)

#
# Execute the test
#

if __name__ == "__main__":
    unittest.main()
