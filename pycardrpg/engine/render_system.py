#!/usr/bin/env python

import os

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
# Sprite Sheet Handler.  
# Cuts up and caches sprite sheet elements.
#

class SpriteSheet(list):

    def __init__(self, file, rows=1, columns=1, width=16, height=16, 
                 startx=0, starty=0, skipx=0, skipy=0):

        list.__init__(self)

        rect = pygame.Rect(startx, starty, width, height)
        image = get_image(file)

        for row in range(rows):
            for column in range(columns):
                rect.left = ((rect.width + skipx) * column) + startx
                rect.top = ((rect.height + skipy) * row) + starty
                self.append(image.subsurface(rect))

#
# Get an image from a file and return it as a sprite
#

def get_sprite(file):
    sprite = pygame.sprite.Sprite()
    sprite.image = get_image(file)
    sprite.rect = sprite.image.get_rect()
    return sprite

#
# Get an image from the data directory and return it as a 
# surface.
#

def get_image(file):
    filename = os.path.join('pycardrpg', 'data', file)

    try:
        image = pygame.image.load(filename).convert_alpha()            
    except pygame.error, message:
        raise Exception('Cannot load image: %s.  Message: %s' % (filename, message))

    return image

#
# singleton render system
#

render_system = RenderSystem()
