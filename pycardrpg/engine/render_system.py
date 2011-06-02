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
# Layer Types
#

class LayerTypes(object):
    
    class LayerType(object):
        def __init__(self, id):
            self.id = id
    
    MAP_LAYER = LayerType(1)
    HUD_LAYER = LayerType(2)
    UI_LAYER = LayerType(3)

#
# singleton render system
#

render_system = RenderSystem()
