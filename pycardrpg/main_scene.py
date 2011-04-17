#!/usr/bin/evn python

import pygame
from pygame.locals import *

from pyengine.scene_system import Scene
from pyengine.event_system import event_system, inject_user_event
from pyengine.render_system import render_system

from pycardrpg.controller import ActionCardController, MoveController
from pycardrpg.model.map_generator import MapGenerator
from pycardrpg.view.map_sprite import MapSprite
from pycardrpg.view.ui import UI

#
# The main scene of the game.
#

class MainScene(Scene):
    
    def __init__(self):
        Scene.__init__(self)
        
        self.events = []
        self.player_turn = True

        self.views = {}
        self.current_view = None
        
        self.controllers = []
        
        # setup the map
        self._setup_model()
        self._setup_controllers()
        self._setup_view()
        
        # listen for the events we care about
        event_system.on(self.on_end_turn, USEREVENT, 'end_turn')
        event_system.on(self.on_switch_view, USEREVENT, 'switch_view')
        event_system.on(self.on_remove_view, USEREVENT, 'remove_view')
        event_system.on(self.on_map_changed, USEREVENT, 'map_changed')

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
        
    def on_map_changed(self, data):
        self.map_sprite.changed = True
        
    def on_switch_view(self, data):
        if self.current_view is not None:
            self.on_remove_view(data)
        
        self.current_view = self.views[data['view']]
        self.current_view.load(data)
        render_system.add(self.current_view.get_sprites(), layer=2)

    def on_remove_view(self, data):
        self.current_view.unload()
        self.current_view = None
        render_system.remove_sprites_of_layer(2)

    def _setup_model(self):
        self.map = MapGenerator().generate()      

    def _setup_controllers(self):
        self.controllers.append(MoveController(self.map))
        self.controllers.append(ActionCardController(self.map))

    def _setup_view(self):
        self.map_sprite = MapSprite(800, 600, self.map)
        render_system.add(self.map_sprite, layer=0)
        
        self.ui_view = UI(800, 600)
        render_system.add(self.ui_view.get_sprites())

