#!/usr/bin/evn python

import pygame
from pygame import USEREVENT

from pycardrpg.scene_system import Scene
from pycardrpg.model.map_generator import MapGenerator
from pycardrpg.ui.map_controller import MapController
from pycardrpg.ui.map_sprite import MapSprite

#
# The main scene of the game.
#

class MainScene(Scene):
    
    def __init__(self):
        Scene.__init__(self)
        self.events = []
        self.player_turn = True
        
    def on_start(self):
        self._setup_map()
        self.event_system.on(USEREVENT, self.on_end_turn, subtype='end_turn')

    def on_update(self, surface):
        # process any pending events
        if self.player_turn:
            if self.events:
                event = self.events.pop()
                Scene.on_event(self, event)
        else:
            print 'Computer Turn'
            self.player_turn = True
        
        Scene.on_update(self, surface)

    def on_event(self, event):
        self.events.append(event)

    def on_end_turn(self, data):
        self.player_turn = False

    def _setup_map(self):
        self.map = MapGenerator(self.entity_system).generate()
        self.map_controller = MapController(self.event_system, self.entity_system, self.map)
        map_sprite = MapSprite(800, 600, self.event_system, self.entity_system, self.map)
        self.render_system.add(map_sprite, layer=0)

