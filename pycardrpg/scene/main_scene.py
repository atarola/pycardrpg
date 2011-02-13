#!/usr/bin/evn python

from pycardrpg.scene.scene import Scene
from pycardrpg.scene.controller.player_controller import PlayerController
from pycardrpg.scene.render.render_system import RenderSystem
from pycardrpg.entity.map.map_generator import MapGenerator
from pycardrpg.entity.entity_system import EntitySystem

#
# The main scene of the game.
#

class MainScene(Scene):
    
    def __init__(self):
        self.events = []
        self.player_turn = True
        
        # setup our map
        self.entity_system = EntitySystem() 
        self.map = MapGenerator(self.entity_system).generate()
            
        # wire up our support systems
        self.render_system = RenderSystem(800, 600, self.entity_system, self.map)
        self.player_controller = PlayerController(self, self.entity_system, self.map)

    def on_update(self, surface):
        if self.player_turn:
            self.player_update()
        else:
            self.computer_update()
                
        # render the results
        self.render_system.render(surface)
        
    def on_event(self, event):
        self.events.insert(0, event)

    def player_update(self):
        if self.events:
            event = self.events.pop()
            self.player_controller.on_event(event)
            
        if self.player_controller.update():
            self.player_turn = False
    
    def computer_update(self):
        print "Computer Update"
        self.player_turn = True
