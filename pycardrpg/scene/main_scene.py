#!/usr/bin/evn python

import pygame
from pygame import USEREVENT

from pycardrpg.scene.scene import Scene
from pycardrpg.scene.controller.move_controller import MoveController
from pycardrpg.scene.render.render_system import RenderSystem
from pycardrpg.model.map.map_generator import MapGenerator
from pycardrpg.model.entity.entity_system import EntitySystem

#
# The main scene of the game.
#

class MainScene(Scene):
    
    def __init__(self):
        Scene.__init__(self)
        
        self.events = []
        self.player_turn = True
        
        # setup our map
        self.entity_system = EntitySystem() 
        self.map = MapGenerator(self.entity_system).generate()
            
        # wire up our support systems
        self.render_system = RenderSystem(800, 600, self.entity_system, self.map)
        self.move_controller = MoveController(self, self.entity_system, self.map)
        
        # wire up our end_turn event
        self.on(USEREVENT, self.on_end_turn, subtype='end_turn')

    def on_update(self, surface):
        # process any pending events
        if self.player_turn:
            if self.events:
                event = self.events.pop()
                Scene.process(self, event)
        else:
            print 'Computer Turn'
            self.player_turn = True
            
        # render the results
        self.render_system.render(surface)

    def process(self, event):
        self.events.insert(0, event)
        
    def on_end_turn(self, data):
        self.player_turn = False
