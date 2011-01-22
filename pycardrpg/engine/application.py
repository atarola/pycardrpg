#!/usr/bin/env python

import pygame
from pygame.locals import *

from engine.scene_system import SceneSystem

#
# Main application object
#

class Application(SceneSystem):

    def __init__(self, caption, width, height, fps):
        SceneSystem.__init__(self)
        
        self.stop = False
        self.fps = fps

        pygame.init()
        pygame.font.init()
        pygame.display.set_caption(caption)
        self.surface = pygame.display.set_mode((width, height))
        self.surface.fill((0, 0, 0))

    def run(self):
        clock = pygame.time.Clock()
        
        while not self.stop:
            self.handle_events()
            self.on_update(self.surface)
            
            pygame.display.flip()
            clock.tick(self.fps)

    def handle_events(self):
        events = pygame.event.get()
        
        for event in events:
            if event.type == QUIT:
                self.stop = True
                return
            
            self.on_event(event)

