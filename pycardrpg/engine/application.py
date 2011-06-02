#!/usr/bin/env python

import pygame
from pygame.locals import *

from pycardrpg.engine.scene_system import scene_system

#
# Main application object
#

class Application(object):
    
    BLACK = (0, 0, 0)

    def __init__(self, caption, width, height, fps):        
        self.stop = False
        self.fps = fps

        pygame.init()
        pygame.font.init()
        pygame.display.set_caption(caption)
        self.surface = pygame.display.set_mode((width, height))
        self.surface.fill(Application.BLACK)

    def run(self):
        clock = pygame.time.Clock()
        
        while not self.stop:
            self._handle_events()
            self._handle_updates()
            
            pygame.display.flip()
            clock.tick(self.fps)

    def _handle_events(self):
        events = pygame.event.get()
        
        for event in events:
            if event.type == QUIT:
                self.stop = True
                return

            scene_system.on_event(event)
            
    def _handle_updates(self):
        scene_system.on_update(self.surface)

