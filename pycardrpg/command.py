#!/usr/bin/env python

import pygame
from pygame.locals import *

from pyengine.script_system import ScriptEvent
from pyengine.entity_system import entity_system
from pyengine.event_system import event_system

from pycardrpg.view.map_sprite import MapSprite

#
# TargetCommand
# Choose a target and add it to the memory
#

# TODO: Handle distance.
class TargetCommand(ScriptEvent):
    
    def __init__(self, **kwargs):
        callback = kwargs.get('callback', None)        
        ScriptEvent.__init__(self, callback=callback)
        
        self.set_handler = False
        self.pos = None
        self.distance = kwargs.get('distance', 1)
    
    def update(self, memory):
        if not self.set_handler:
            event_system.on(self.handle_mouse_up, MOUSEBUTTONUP)
            self.set_handler = True
        
        if self.pos is not None:
            target = entity_system.find_one('RenderComponent', conditions={'RenderComponent#pos': self.pos})
            
            if target is not None:
                memory['target'] = target
                self.callback(self)
            else:
                self.pos = None
    
    # TOOD: think of a better way to do this
    def handle_mouse_up(self, data):
        sprite = data.get('sprite', None)

        if not isinstance(sprite, MapSprite):
            return
        
        self.pos = sprite.to_array(data['pos'])
            
#
# DamageCommand
# Do damage from the subject to the target
#

class DamageCommand(ScriptEvent):
    
    def __init__(self, **kwargs):
        callback = kwargs.get('callback', None)
        ScriptEvent.__init__(self, command=True, callback=callback)
    
    def update(self, memory):
        source = memory.get('source', None)
        target = memory.get('target', None)

        if source is None or target is None:
            return

        attack = source.get('UnitComponent', 'attack')
        defense = target.get('UnitComponent', 'defense')
        damage = attack - defense
        
        if damage > 0:
            hp = target.get('UnitComponent', 'cur_hp')
            target.set('UnitComponent', 'cur_hp', hp - damage)

#
# Command Mapping
# Used to reference the Commands by name
#

mapping = {
    'TargetCommand': TargetCommand,
    'DamageCommand': DamageCommand
}

