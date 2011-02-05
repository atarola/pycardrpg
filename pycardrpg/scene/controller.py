#!/usr/bin/env python

from pygame.locals import *

from pycardrpg.scene.event_system import EventSystem 

#
# Event System
#

class Controller(EventSystem):

    def __init__(self, scene, entity_system, map):
        EventSystem.__init__(self)
        self.scene = scene
        self.entity_system = entity_system
        self.map = map
        
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
        entity = self.entity_system.find_one("PlayerComponent", "RenderComponent", "UnitComponent")
        pos = (entity.pos[0] + dx, entity.pos[1] + dy)
        
        if self.map.is_passible(pos):
            entity.pos = pos
            self.map.get_fov_seen(entity.pos, entity.fov_radius)
            self.scene.player_turn = False
            

