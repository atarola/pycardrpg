#!/usr/bin/env python

import os
import yaml
import random

import pygame

from pycardrpg.model.level_map import LevelMap, TileTypes
from pycardrpg.model.unit_repository import unit_repository
from pycardrpg.model.card import card_repository

#
# Map Generator
#

# TODO: properly
class MapGenerator():

    def generate(self):
        level_map = LevelMap(100, 100)
        
        # x = random.randint(1, 90)
        # y = random.randint(1, 90)
        # w = random.randint(1, 10)
        # h = random.randint(2, 10)
        # 
        # room = Room(x, y, w, h)
        
        room = Room(50, 50, 10, 10)
        room.create(level_map)
        rooms = [room]
        
        num_rooms = random.randint(5, 30)
        
        while num_rooms > 0:
            old_room = random.choice(rooms)
            
            w = random.randint(1, 10)
            h = random.randint(2, 10)
            
            room = Room(w=w, h=h)
            
            direction = random.randint(0, 3)
            
            # north
            if direction == 0:
                door_x = random.randint(old_room.x, old_room.x + old_room.w - 1)
                door_y = old_room.y - 1
                room.rect.midbottom = (door_x, door_y)
                
            # east
            if direction == 1:
                door_x = old_room.x + old_room.w
                door_y = random.randint(old_room.y + 1, old_room.y + old_room.h - 1)
                room.rect.midleft = (door_x + 1, door_y)
                
            # south
            if direction == 2:
                door_x = random.randint(old_room.x, old_room.x + old_room.w - 1)
                door_y = old_room.y + old_room.h
                room.rect.midtop = (door_x, door_y + 1)
                
            # west
            if direction == 3:
                door_x = old_room.x - 1
                door_y = random.randint(old_room.y + 1, old_room.y + old_room.h - 1)
                room.rect.midright = (door_x, door_y)
            
            if room.verify(level_map):
                room.create(level_map)
                level_map.get((door_x, door_y)).type = TileTypes.FLOOR
            
                if direction == 0:
                    level_map.get((door_x, door_y + 1)).type = TileTypes.FLOOR
                
                if direction == 1:
                    level_map.get((door_x, door_y - 1)).type = TileTypes.WALL
                
                if direction == 2:
                    level_map.get((door_x, door_y + 1)).type = TileTypes.FLOOR
            
                if direction == 3:
                    level_map.get((door_x, door_y - 1)).type = TileTypes.WALL
            
                rooms.append(room)
            
                num_rooms -= 1
        
        self._select_tiles(level_map)
        # self._create_enemies(level_map)
        self._create_player(level_map)
        
        return level_map

    # def _create_enemies(self, level_map):
    #     pos = (4, 2)
    #     enemy = unit_repository.create_from_template("Skeleton")
    #     enemy.set("RenderComponent", "pos", pos)

    def _select_tiles(self, level_map):
        tile_picker = TilePicker(level_map)
        
        for tile in level_map:
            tile.index = tile_picker.pick(tile)
    
    def _create_player(self, level_map):
        pos = (52, 52)
        player = unit_repository.create_from_template("Player")
        player.set("RenderComponent", "pos", pos)
        fov_radius = player.get("UnitComponent", 'fov_radius')   
        level_map.get_fov_tiles(pos, fov_radius).seen = True
        
        deck = player.get("UnitComponent", 'deck')
        deck.add_card(card_repository.get_action_card('DoubleTap'))
        deck.add_card(card_repository.get_action_card('Attack'))
        deck.add_card(card_repository.get_action_card('Attack'))
        deck.add_card(card_repository.get_action_card('Attack'))
        deck.add_card(card_repository.get_action_card('Attack'))
        deck.fill_hand()

#
#
#    

class Room(object):
    
    def __init__(self, x=0, y=0, w=1, h=2):
        self.rect = pygame.Rect(x, y, w, h)
        
    def verify(self, level_map):
        tiles = level_map.get_rect(self.rect)
        return len(tiles) == tiles.count('type', TileTypes.CEILING)
        
    def create(self, level_map):
        level_map.get_rect(self.rect).type = TileTypes.FLOOR
        level_map.get_area(self.rect.x, self.rect.y, self.rect.w, 1).type = TileTypes.WALL
    
    @property
    def x(self):
        return self.rect.x
    
    @property
    def y(self):
        return self.rect.y
    
    @property
    def w(self):
        return self.rect.width
    
    @property    
    def h(self):
        return self.rect.height

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

