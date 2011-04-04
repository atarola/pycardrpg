#!/usr/bin/env python

import pygame
from pygame.sprite import LayeredUpdates

#
# Rendering System
#

class RenderSystem(LayeredUpdates):
    
    # rendering layers. pygame will render added sprites sorted by this order, 
    # then by which sprite was added first
    MAP_LAYER = 0
    UI_LAYER = 1
    PANEL_LAYER = 2
    
    def __init__(self):
        LayeredUpdates.__init__(self)
    
    # return the top sprite at the position
    def get_sprite(self, pos):
        sprites = self.get_sprites_at(pos)
        
        if sprites:
            return sprites.pop()
        else:
            return None

