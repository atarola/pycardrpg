#!/usr/bin/env python

from pygame.locals import *

from pycardrpg.scene.event_system import EventSystem
from pycardrpg.scene.controller.move_action import MoveAction
from pycardrpg.scene.controller.update_view_action import UpdateViewAction

#
# Player controller.  Handle what the player does
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
        
        for action in self.actions:
            action.execute()
        
        self.actions = []
        self.ready = False
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
        
        if self.map[x + dx, y + dy].passible:
            self.actions.append(MoveAction(entity, dx, dy))
            self.actions.append(UpdateViewAction(entity, self.map))
            self.ready = True
