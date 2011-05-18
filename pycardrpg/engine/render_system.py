#!/usr/bin/env python

import pygame
from pygame.sprite import LayeredUpdates

#
# Rendering System
#

class RenderSystem(LayeredUpdates):
    
    def __init__(self):
        LayeredUpdates.__init__(self)
    
    # return the top sprite at the position
    def get_sprite(self, pos):
        sprites = self.get_sprites_at(pos)
        
        if sprites:
            return sprites.pop()
        else:
            return None

#
# singleton render system
#

render_system = RenderSystem()

