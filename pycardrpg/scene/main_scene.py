#!/usr/bin/evn python

from pycardrpg.scene.scene import Scene
from pycardrpg.scene.render.render_system import RenderSystem
from pycardrpg.model.map.map_generator import MapGenerator
from pycardrpg.model.entity.entity_system import EntitySystem

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

    def on_update(self, surface):
        if self.events:
		    self.events.pop()
		    
        # render the results
        self.render_system.render(surface)

    def on_event(self, event):
        self.events.insert(0, event)
