#!/usr/bin/evn python

import pygame
from pygame.locals import *

from pycardrpg.scene_system import Scene
from pycardrpg.event_system import inject_user_event
from pycardrpg.model.map_generator import MapGenerator
from pycardrpg.ui.map_view import MapView
from pycardrpg.ui.test_view import TestView

#
# The main scene of the game.
#

# TODO: extract view handling code into it's own class
class MainScene(Scene):
    
    def __init__(self):
        Scene.__init__(self)
        
        self.events = []
        self.player_turn = True

        self.views = {}
        self.current_view = None
        
        # setup the map
        self._setup_map()
        self._setup_views()
        
        # listen for the events we care about
        self.event_system.on(USEREVENT, self.on_end_turn, 'end_turn')
        self.event_system.on(USEREVENT, self.on_switch_view, 'switch_view')
        self.event_system.on(USEREVENT, self.on_remove_view, 'remove_view')

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
        
    def on_switch_view(self, data):
        if self.current_view is not None:
            self.on_remove_view(data)
        
        self.current_view = self.views[data['view']]
        self.current_view.load(data)
        self.render_system.add(self.current_view.get_sprites(), layer=2)

    def on_remove_view(self, data):
        self.current_view.unload()
        self.current_view = None
        self.render_system.remove_sprites_of_layer(2)

    def _setup_map(self):
        self.map = MapGenerator(self.entity_system).generate()      
        self.map_view = MapView(800, 600, self.event_system, self.entity_system, self.map)
        self.map_view.load({})
        self.render_system.add(self.map_view.get_sprites(), layer=0)

    def _setup_views(self):
        pass

