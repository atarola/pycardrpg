#!/usr/bin/env python

import math 
import pygame

#
# Camera object
#

class Camera(object):
    CHAR_SIZE = (9, 13)
    
    def __init__(self, width, height):
        width = math.floor(width / Camera.CHAR_SIZE[0]) + 1
        height = math.floor(height / Camera.CHAR_SIZE[1]) + 1
        self.rect = pygame.Rect(0, 0, width, height)

    def move(self, pos):
        self.rect.center = pos
        
    def in_view(self, pos):
        return self.rect.collidepoint(pos)
    
    def translate(self, pos):
        x, y = pos
        a, b = Camera.CHAR_SIZE
        
        tx = x - self.rect.left
        ty = y - self.rect.top
        
        return (tx * a, ty * b) 
        