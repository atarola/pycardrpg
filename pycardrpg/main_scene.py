#!/usr/bin/evn python

import pygame
from pygame.locals import *

from pycardrpg.engine.scene_system import Scene
from pycardrpg.engine.render_system import render_system, LayerTypes
from pycardrpg.engine.event_system import inject_user_event

from pycardrpg.model.controller import Controller
from pycardrpg.model.map_generator import MapGenerator
from pycardrpg.view.map_sprite import MapSprite
from pycardrpg.view.sidebar_panel import SidebarPanel
from pycardrpg.view.notification_panel import NotificationPanel

#
# The main scene of the game.
#

class MainScene(Scene):
    
    def __init__(self):
        Scene.__init__(self)
        
    def on_start(self):
        self.map = MapGenerator().generate()
        self.game_state = Controller(self.map)
        
        self.map_sprite = MapSprite(800, 600, self.map)
        self.sidebar_panel = SidebarPanel(800, 600)
        self.notification_panel = NotificationPanel(800, 600)
        render_system.add(self.map_sprite, layer=LayerTypes.MAP_LAYER)
        render_system.add(self.sidebar_panel, layer=LayerTypes.HUD_LAYER)
        render_system.add(self.notification_panel, layer=LayerTypes.HUD_LAYER)

