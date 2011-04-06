#!/usr/bin/env python

import pygame
from pygame.locals import *

from pycardrpg.ui.view import View

#
# UI View
#

class UIView(View):
    
    def __init__(self, width, height, event_system, entity_system, level_map):
        View.__init__(self, event_system, entity_system, level_map)
        
        self.width = width
        self.height = height
        self.sprite_cache = []
        
    def load(self, data):
        self.event_system.on(MOUSEBUTTONUP, self.on_mouse_up)
        
    def unload(self):
        pass
        
    def get_sprites(self):
        if self.sprite_cache == []:
            pass
            
        return self.sprite_cache
        
    def on_mouse_up(self, data):
        if not data['sprite'] in self.sprite_cache:
            return

        