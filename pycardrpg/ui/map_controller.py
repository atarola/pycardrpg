#!/usr/bin/env python

import pygame
from pygame.locals import *

from pycardrpg.event_system import inject_user_event

#
# Map Controller, Handle player movement
#

class MapController(object):
    
    def __init__(self, event_system, entity_system, map):
        self.entity_system = entity_system
        self.map = map
        
        # wire up our listener
        event_system.on(KEYUP, self.on_keyup)
        
    # move the character on keyup
    def on_keyup(self, data):
        key = data.get('key', 0)

        if key in [K_UP, K_w]:
            self.move_player(0, -1)
            return   
            
        if key in [K_DOWN, K_s]:
            self.move_player(0, 1)
            return
            
        if key in [K_LEFT, K_a]:
            self.move_player(-1, 0)
            return
            
        if key in [K_RIGHT, K_d]:
            self.move_player(1, 0)
            return
 
    def move_player(self, dx, dy):
        player = self.entity_system.find_one("PlayerComponent")
        x, y = player.get("RenderComponent", "pos")
        pos = (x + dx, y + dy)
        
        # if the new spot isn't passible, ignore the command
        if not self.map[pos].passible:
            return

        # if the new spot is occupied, ignore the command
        for entity in self.entity_system.find("NpcComponent"):
            if entity.get("RenderComponent", "pos") == pos:
                return

        player.set("RenderComponent", "pos", pos)
        self._update_fov(player)
        
        inject_user_event('map_changed')
        inject_user_event('end_turn')

    def _update_fov(self, player):
        pos = player.get("RenderComponent", "pos")
        fov_radius = player.get("UnitComponent", "fov_radius")
        self.map.get_fov_tiles(pos, fov_radius).seen = True

