#!/usr/bin/env python

#
# A renderable thing
#

class RenderComponent(object):
    
    def __init__(self):
        self.pos = (0, 0)
        self.symbol = "@"
        self.color = (255, 255, 255)
