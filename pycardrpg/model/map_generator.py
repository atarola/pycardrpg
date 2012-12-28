#!/usr/bin/env python

import os
import yaml
import random

import pygame

from pycardrpg.model.quad_map import LevelMap, TileTypes, TileInstance
from pycardrpg.model.unit_repository import unit_repository
from pycardrpg.model.card import card_repository

#
# Map Generator
#

class MapGenerator():
    
    MAP_WIDTH = 100
    MAP_HEIGHT = 100
    
    ROOM_MAX_SIZE = 10
    ROOM_MIN_SIZE = 6
    MAX_ROOMS = 25
    
    def generate(self):
        level_map = LevelMap(self.MAP_WIDTH, self.MAP_HEIGHT)
        
        rooms = self.create_rooms(level_map)
        self.create_ceilings(level_map)
        self.select_tiles(level_map)
        self.create_enemies(level_map, rooms)
        self.create_player(level_map, rooms[0].center)
        
        return level_map
        
    def create_rooms(self, level_map):
        rooms = []
        
        # create our rooms
        for r in range(self.MAX_ROOMS):
            w = random.randrange(self.ROOM_MIN_SIZE, self.ROOM_MAX_SIZE)
            h = random.randrange(self.ROOM_MIN_SIZE, self.ROOM_MAX_SIZE)
            x = random.randrange(1, self.MAP_WIDTH - w - 1)
            y = random.randrange(1, self.MAP_HEIGHT - h - 1)
            
            new_room = pygame.Rect(x, y, w, h)
            failed = False

            for room in rooms:
                if room.colliderect(new_room):
                    failed = True
                    break
            
            if not failed:
                self.create_room(level_map, new_room)

                if len(rooms) == 0:
                    # set the player's position
                    player_pos = new_room.center
                else:
                    # connect this room to the previous one
                    new_x, new_y = new_room.center
                    old_x, old_y = rooms[-1].center
                
                    if random.randrange(2) == 1:
                        self.create_h_tunnel(level_map, old_x, new_x, old_y)
                        self.create_v_tunnel(level_map, old_y, new_y, new_x)
                    else:
                        self.create_v_tunnel(level_map, old_y, new_y, old_x)
                        self.create_h_tunnel(level_map, old_x, new_x, new_y)
                
                rooms.append(new_room)
        
        return rooms
        
    def create_ceilings(self, level_map):      
        tiles = [tile for tile in level_map]                
        deltas = [(-1, -1), (0, -1), (1, -1), (-1, 0), (0, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
        
        for tile in tiles:
            x, y = tile.pos
            
            for dx, dy in deltas:
                level_map.set_default((x + dx, y + dy))   
    
    # TODO: walls
    def create_room(self, level_map, rect):
        x1, y1 = rect.topleft
        x2, y2 = rect.bottomright
        
        for x in range(x1, x2):
            for y in range(y1, y2):
                level_map.set_default((x, y)).type = TileTypes.FLOOR
            
    def create_h_tunnel(self, level_map, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            level_map.set_default((x, y)).type = TileTypes.FLOOR
            
    def create_v_tunnel(self, level_map, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            level_map.set_default((x, y)).type = TileTypes.FLOOR

    def select_tiles(self, level_map):
        tile_picker = TilePicker(level_map)
        
        for tile in level_map:
            tile.index = tile_picker.pick(tile)
    
    def create_enemies(self, level_map, rooms):
        pass
    
    def create_player(self, level_map, pos):        
        # Create a new player and set their position
        player = unit_repository.create_from_template("Player")
        player.set("RenderComponent", "pos", pos)
        
        # make sure any seen tiles are seen
        fov_radius = player.get("UnitComponent", "fov_radius")
        level_map.get_fov_tiles(pos, fov_radius).seen = True
        
        # create the player's deck
        deck = player.get("UnitComponent", 'deck')
        deck.add_card(card_repository.get_action_card("DoubleTap"))
        deck.add_card(card_repository.get_action_card("Attack"))
        deck.add_card(card_repository.get_action_card("Attack"))
        deck.add_card(card_repository.get_action_card("Attack"))
        deck.add_card(card_repository.get_action_card("Attack"))
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
        tiles = []
        
        for dx, dy in deltas:
            new_pos = (x + dx, y + dy)
            tile = self.map.get(new_pos)
            
            if tile is None:
                tile = TileInstance(TileTypes.CEILING, new_pos)
            
            tiles.append(tile)
        
        return tiles

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

