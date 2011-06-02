#!/usr/bin/env python

import pygame
from pygame.locals import *

from pycardrpg.engine.script_system import ScriptEvent
from pycardrpg.engine.entity_system import entity_system
from pycardrpg.engine.event_system import event_system

from pycardrpg.view.map_sprite import MapSprite

#
# TargetCommand
# Choose a target and add it to the memory
#

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
            # get our target
            target = entity_system.find_one('RenderComponent', conditions={'RenderComponent#pos': self.pos})
            if target is None:
                self.pos = None
                self.callback(self)
                return
            
            # verify the target is equal or closer than the max distance
            source_pos = memory['source'].get('RenderComponent', 'pos')
            if memory['map'].in_distance(source_pos, self.pos, self.distance):
                self.pos = None
                self.callback(self)
                return
            
            memory['target'] = target
            self.callback(self)
    
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
            print "old hp: %s" % hp
            print "damage: %s" % damage

#
# Command Mapping
# Used to reference the Commands by name
#

mapping = {
    'TargetCommand': TargetCommand,
    'DamageCommand': DamageCommand
}

