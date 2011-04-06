#!/usr/bin/env python

import pygame

from pycardrpg.ui.image_loader import get_image

#
# Sprite Sheet Handler.  Cuts up and caches sprite sheet elements.
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

