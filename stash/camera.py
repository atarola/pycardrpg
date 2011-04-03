#!/usr/bin/env python

import math 
import pygame

#
# Camera object
#

class Camera(object):
    CHAR_SIZE = (16, 16)
    
    def __init__(self, width, height):
        width = math.floor(width / Camera.CHAR_SIZE[0]) + 2
        height = math.floor(height / Camera.CHAR_SIZE[1]) + 2
        self.rect = pygame.Rect(-1, -1, width, height)

    def move(self, pos):
        self.rect.center = pos
        
    def in_view(self, pos):
        return self.rect.collidepoint(pos)
    
    def translate(self, pos):
        x, y = pos
        a, b = Camera.CHAR_SIZE
        
        tx = abs(x - self.rect.left) * a
        ty = abs(y - self.rect.top) * b
        
        return (tx, ty) 
        