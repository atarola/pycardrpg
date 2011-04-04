#!/usr/bin/env python

import pygame
from pygame.sprite import LayeredUpdates

from pycardrpg.entity_system import EntitySystem
from pycardrpg.event_system import EventSystem

#
# Uses the strategy pattern to encapsulate different 
# scenes in the game.
#

class SceneSystem(object):
    
    def __init__(self):
        self.scenes = {}
        self.current = Scene()

    def add_scene(self, name, scene):
        self.scenes[name] = scene
        scene.manager = self
        
    def switch_scene(self, name):
        if self.current is not None:
            self.current.on_exit()

        self.current = self.scenes[name]
        self.current.on_start() 
        
    def on_event(self, event):
        self.current.on_event(event)
        
    def on_update(self, surface):
        self.current.on_update(surface)
        
#
# A single scene.  Represents a single section of the game. 
# contains a list of sprites, and dispatches events for
# it's subsection
#

class Scene(object):

    def __init__(self):
        self.sprites = LayeredUpdates()
        self.entity_system = EntitySystem() 
        self.event_system = EventSystem()
    
    def on_event(self, event):
        sprite = None
        
        if 'pos' in event.dict.keys():
            sprite = self._get_sprite(event.pos)
        
        self.event_system.process(event, sprite)
    
    def on_update(self, surface):
        self.sprites.update()
        self.sprites.draw(surface)
        
    def on_start(self):
        pass 

    def on_exit(self):
        pass
        
    def _get_sprite(self, pos):
        sprites = self.sprites.get_sprites_at(pos)
        
        if sprites:
            return sprites.pop()
        else:
            return None

