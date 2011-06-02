#!/usr/bin/env python

import os

import pygame

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
    filename = _get_filename(file)

    try:
        image = pygame.image.load(filename).convert_alpha()            
    except pygame.error, message:
        raise Exception('Cannot load image: %s.  Message: %s' % (filename, message))
        
    return image

def _get_filename(file):
    return os.path.join('pycardrpg', 'data', file)

