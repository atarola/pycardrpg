#!/usr/bin/env python

from pygame.locals import *

from pycardrpg.scene.event_system import EventSystem
from pycardrpg.scene.controller.move_event import MoveEvent

#
# Player controller.  
#

class PlayerController(EventSystem):
    
    def __init__(self, scene, entity_system, map):
        EventSystem.__init__(self)
        
        self.actions = []
        self.ready = False
        
        self.scene = scene
        self.entity_system = entity_system
        self.map = map
    
    def update(self):
        if not self.ready:
            return False
        
        player = self.entity_system.find_one("PlayerComponent")
        memory = {"player": player, "map": self.map}

        while len(self.actions) > 0:
            action = self.actions.pop(0)
            action.execute(memory)
        
        self.ready = False 
        self._update_fov(player)
        
        return True
    
    def on_key_down(self, scancode, key, mod, unicode):
        
        if key == K_UP or key == K_w:
            self.move_player(0, -1)
            return
        
        if key == K_DOWN or key == K_s:
            self.move_player(0, 1)
            return
        
        if key == K_LEFT or key == K_a:
            self.move_player(-1, 0)
            return
        
        if key == K_RIGHT or key == K_d:
            self.move_player(1, 0)
            return
        
    def move_player(self, dx, dy):
        entity = self.entity_system.find_one("PlayerComponent")
        x, y = entity.get("RenderComponent", "pos")
        pos = (x + dx, y + dy)
        
        # if the new spot isn't passible, ignore the command
        if not self.map[pos].passible:
            return
        
        # if the new spot is occupied, ignore the command
        for entity in self.entity_system.find("NpcComponent"):
            if entity.get("RenderComponent", "pos") == pos:
                return
        
        # add the move event and allow the events to run
        self.actions.append(MoveEvent("player", dx, dy))
        self.ready = True

    def _update_fov(self, player):
        pos = player.get("RenderComponent", "pos")
        fov_radius = player.get("UnitComponent", "fov_radius")
        self.map.get_fov_tiles(pos, fov_radius).seen = True
