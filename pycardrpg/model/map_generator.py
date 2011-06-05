#!/usr/bin/env python

import os
import yaml



from pycardrpg.model.level_map import LevelMap, TileTypes
from pycardrpg.model.unit_repository import unit_repository
from pycardrpg.model.card import card_repository

#
# Map Generator
#

# TODO: properly
class MapGenerator():

    def generate(self):
        level_map = LevelMap(16, 16)
        
        # fill map with ceiling
        level_map.get_area(0, 0, 16, 16).type = TileTypes.CEILING
        
        # add floor
        level_map.get_area(2, 2, 6, 1).type = TileTypes.FLOOR
        level_map.get_area(3, 3, 4, 1).type = TileTypes.FLOOR
        level_map.get((5, 4)).type = TileTypes.FLOOR
        level_map.get((5, 5)).type = TileTypes.FLOOR
        level_map.get_area(5, 6, 9, 1).type = TileTypes.FLOOR
        level_map.get((13, 7)).type = TileTypes.FLOOR
        level_map.get_area(4, 8, 10, 6).type = TileTypes.FLOOR
        level_map.get_area(7, 8, 3, 1).type = TileTypes.CEILING
        level_map.get((7, 11)).type = TileTypes.CEILING
        level_map.get((11, 11)).type = TileTypes.CEILING
        
        # add walls
        level_map.get_area(2, 1, 6, 1).type = TileTypes.WALL
        level_map.get_area(6, 5, 8, 1).type = TileTypes.WALL
        level_map.get_area(4, 8, 3, 1).type = TileTypes.WALL
        level_map.get_area(7, 9, 3, 1).type = TileTypes.WALL
        level_map.get_area(10, 8, 3, 1).type = TileTypes.WALL
        level_map.get((7, 12)).type = TileTypes.WALL
        level_map.get((11, 12)).type = TileTypes.WALL
        
        self._select_tiles(level_map)
        self._create_enemies(level_map)
        self._create_player(level_map)
        return level_map

    def _create_enemies(self, level_map):
        pos = (4, 2)
        enemy = unit_repository.create_from_template("Skeleton")
        enemy.set("RenderComponent", "pos", pos)

    def _select_tiles(self, level_map):
        tile_picker = TilePicker(level_map)
        
        for tile in level_map:
            tile.index = tile_picker.pick(tile)
    
    def _create_player(self, level_map):
        pos = (2, 2)
        player = unit_repository.create_from_template("Player")
        player.set("RenderComponent", "pos", pos)
        fov_radius = player.get("UnitComponent", 'fov_radius')   
        level_map.get_fov_tiles(pos, fov_radius).seen = True
        
        deck = player.get("UnitComponent", 'deck')
        deck.add_card(card_repository.get_action_card('DoubleTap'))
        deck.add_card(card_repository.get_action_card('Attack'))
        deck.add_card(card_repository.get_action_card('Attack'))
        deck.fill_hand()

#
# Given a position, return the proper tile to put there.
#

class TilePicker(object):

    def __init__(self, tile_map):
        self.map = tile_map
        self.rules = []

        # create our rules from the data file
        filename = os.path.join('pycardrpg', 'data', 'rules_tiles.yaml')
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
        return [self.map.get((x + dx, y + dy)) for dx, dy in deltas]

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
# AnyMatcher, just say yes
#

class Any(object):

    def matches(self, tile):
        return True

#
# Is, matches if the item and arg are equal
#

class Is(object):

    def __init__(self, item):
        self.item = item

    def matches(self, tile):
        return self.item == tile

#
# Not, matches all args except item
#

class Not(object):

    def __init__(self, item):
        self.item = item

    def matches(self, tile):
        return self.item != tile

