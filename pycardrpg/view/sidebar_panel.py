#!/usr/bin/env python

import pygame
from pygame.locals import *

from pycardrpg.engine.event_system import inject_user_event
from pycardrpg.engine.ui import Panel, Button

#
# UI Sidebar
#

class SidebarPanel(Panel):
    
    def __init__(self, width, height):
        Panel.__init__(self, (0, 0), (250, 400))
        self.rect.midright = (width - 10, height / 2)
        
    def do_update(self):
        pos = (self.rect.left, self.rect.top)
        size = (230, 45)
        
        do_button = Button()
        do_button.text_offset = 16
        
        if do_button(self, 1, (10, 125), size, 'one'):
            inject_user_event('action_card', card_num=0)

        if do_button(self, 2, (10, 175), size, 'two'):
            inject_user_event('action_card', card_num=1)

        if do_button(self, 3, (10, 225), size, 'three'):
            inject_user_event('action_card', card_num=2)

        if do_button(self, 4, (10, 275), size, 'four'):
            inject_user_event('action_card', card_num=3)

        if do_button(self, 5, (10, 325), size, 'five'):
            inject_user_event('action_card', card_num=4)

