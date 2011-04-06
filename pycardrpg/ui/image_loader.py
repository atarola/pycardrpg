#!/user/bin/env python

import os

import pygame

#
# Get an image from the data directory and return it as a 
# surface.
#

def get_image(file):
    filename = _get_filename(file)

    try:
        image = pygame.image.load(filename)
        
        if image.get_alpha() is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
            
    except pygame.error, message:
        raise Exception('Cannot load image: %s.  Message: %s' % (filename, message))
        
    return image

def _get_filename(file):
    return os.path.join('pycardrpg', 'data', file)