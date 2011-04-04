#!/usr/bin/env python

import pygame
from pygame.locals import *

#
# Base View
#

class View(object):
    
    def __init__(self, event_system, entity_system, level_map):
        self.event_system = event_system
        self.entity_system = entity_system
        self.level_map = level_map
    
    def load(self, data):
        remove_signal = self.event_system.get(USEREVENT, 'remove_view')
        switch_signal = self.event_system.get(USEREVENT, 'switch_view')
        
        self.event_system.push()
        
        self.event_system.set(remove_signal, USEREVENT, 'remove_view')
        self.event_system.set(switch_signal, USEREVENT, 'switch_view')
        
    def unload(self):
        self.event_system.pop()

    def get_sprites(self):
        return []
