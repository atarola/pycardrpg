#!/usr/bin/env python

import os

import pygame

#
# Sprite Sheet Handler.  Cuts up and caches sprite sheet elements.
#

class SpriteSheet(list):
    
    def __init__(self, file, rows=1, columns=1, width=16, height=16, 
                 startx=0, starty=0, skipx=0, skipy=0):
                 
        list.__init__(self)
        
        rect = pygame.Rect(startx, starty, width, height)
        image = self._get_image(file)
        
        for row in range(rows):
            for column in range(columns):
                rect.left = ((rect.width + skipx) * column) + startx
                rect.top = ((rect.height + skipy) * row) + starty
                self.append(image.subsurface(rect))
                
    def _get_image(self, file):
        filename = self._get_filename(file)
    
        try:
            image = pygame.image.load(filename)
            
            if image.get_alpha() is None:
                image = image.convert()
            else:
                image = image.convert_alpha()
                
        except pygame.error, message:
            raise Exception('Cannot load image: %s.  Message: %s' % (filename, message))
            
        return image
    
    def _get_filename(self, file):
        return os.path.join('pycardrpg', 'data', file)

