#!/usr/bin/evn python

from pycardrpg.scene.scene import Scene
from pycardrpg.scene.render.render_system import RenderSystem
from pycardrpg.scene.controller import Controller
from pycardrpg.scene.ai_system import AISystem
from pycardrpg.entity.map.map_generator import MapGenerator

from pycardrpg.entity.entity_system import EntitySystem
from pycardrpg.entity.card.unit_card import UnitCard
from pycardrpg.entity.player_component import PlayerComponent
from pycardrpg.entity.render_component import RenderComponent

#
# The main scene of the game.
#

class MainScene(Scene):
    
    def __init__(self):
        self.events = []
        self.player_turn = True
        
        # setup our map
        self.map = MapGenerator().generate()
        
        # setup the entities
        self.entity_system = EntitySystem()       
        unit = self.entity_system.new("player")
        unit.add_component(PlayerComponent())
        unit.add_component(UnitCard("player"))
        unit.add_component(RenderComponent())    
        unit.set("RenderComponent", "pos", (2, 2))
        unit.set("RenderComponent", "index", 1)
        
        pos = unit.get("RenderComponent", "pos")
        fov_radius = unit.get("UnitCard", 'fov_radius')   
        self.map.get_fov_tiles(pos, fov_radius).seen = True
        
        # wire up our support systems
        self.render_system = RenderSystem(800, 600, self.entity_system, self.map)
        self.controller = Controller(self, self.entity_system, self.map)
        self.ai = AISystem(self.entity_system, self.map)

    def on_update(self, surface):
        if self.player_turn:
            if self.events:
                event = self.events.pop()
                self.controller.on_event(event)
        else:
            self.ai.update()
            self.player_turn = True
        
        # render the results
        self.render_system.render(surface)
        
    def on_event(self, event):
        self.events.insert(0, event)
    