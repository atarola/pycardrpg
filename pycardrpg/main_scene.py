#!/usr/bin/evn python

import pygame
from pygame.locals import *

from pycardrpg.engine.scene_system import Scene
from pycardrpg.engine.event_system import event_system, inject_user_event
from pycardrpg.engine.render_system import render_system, LayerTypes
from pycardrpg.engine.script_system import script_system

from pycardrpg.controller import ActionCardController, MoveController
from pycardrpg.simulation import Simulation
from pycardrpg.model.map_generator import MapGenerator
from pycardrpg.view.map_sprite import MapSprite
from pycardrpg.view.sidebar import Sidebar
from pycardrpg.view.test_window import TestWindow

#
# The main scene of the game.
#

class MainScene(Scene):
    
    def __init__(self):
        Scene.__init__(self)
        
        self.events = []
        self.player_turn = True
        
        self._setup_model()
        self._setup_controllers()
        self._setup_view()
        
        # listen for the events we care about
        event_system.on(self.on_end_turn, USEREVENT, 'end_turn')
        event_system.on(self.on_map_changed, USEREVENT, 'map_changed')
        event_system.on(self.on_show_gui, USEREVENT, 'show_gui')

    def on_update(self, surface):
        if self.player_turn:
            # process any pending events
            if self.events:
                event = self.events.pop()
                Scene.on_event(self, event)            
        else:
            self.simulation.update()
            self.player_turn = True

        Scene.on_update(self, surface)

    def on_event(self, event):
        self.events.append(event)

    def on_end_turn(self, data):
        self.player_turn = False
        
    def on_map_changed(self, data):
        self.map_sprite.changed = True
        
    def on_show_gui(self, data):
        name = data.get('name', None)
        
        guis = {
            'test_window': TestWindow
        }
        
        guis[name]().run()

    def _setup_model(self):
        self.map = MapGenerator().generate()      

    def _setup_controllers(self):
        self.move_controller = MoveController(self.map)
        self.action_card_controller = ActionCardController(self.map)
        self.simulation = Simulation(self.map)

    def _setup_view(self):
        self.map_sprite = MapSprite(800, 600, self.map)
        render_system.add(self.map_sprite, layer=LayerTypes.MAP_LAYER)
        
        self.sidebar_view = Sidebar(800, 600)
        render_system.add(self.sidebar_view, layer=LayerTypes.HUD_LAYER)

