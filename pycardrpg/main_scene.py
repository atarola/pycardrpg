#!/usr/bin/evn python

import pygame
from pygame.locals import *

from pycardrpg.engine.scene_system import Scene
from pycardrpg.engine.event_system import event_system, inject_user_event
from pycardrpg.engine.render_system import render_system, LayerTypes
from pycardrpg.engine.script_system import script_system

from pycardrpg.controller import ActionCardController
from pycardrpg.controller import MoveController
from pycardrpg.controller import SimulationController
from pycardrpg.controller import TargetController
from pycardrpg.model.map_generator import MapGenerator
from pycardrpg.view.map_sprite import MapSprite
from pycardrpg.view.sidebar_panel import SidebarPanel

#
# The main scene of the game.
#

class MainScene(Scene):
    
    def __init__(self):
        Scene.__init__(self)
        
    def on_start(self):
        self._setup_model()
        self._setup_controllers()
        self._setup_view()
        
        event_system.on(self.on_user_event, USEREVENT)

    def on_user_event(self, data):
        print "User Event: %s" % data

    def _setup_model(self):
        self.map = MapGenerator().generate()      

    def _setup_controllers(self):
        self.move_controller = MoveController(self.map)
        self.action_card_controller = ActionCardController(self.map)
        self.simulation_controller = SimulationController(self.map)
        self.target_controller = TargetController(self.map)

    def _setup_view(self):
        self.map_sprite = MapSprite(800, 600, self.map)
        render_system.add(self.map_sprite, layer=LayerTypes.MAP_LAYER)
        
        self.sidebar_panel = SidebarPanel(800, 600)
        render_system.add(self.sidebar_panel, layer=LayerTypes.HUD_LAYER)

