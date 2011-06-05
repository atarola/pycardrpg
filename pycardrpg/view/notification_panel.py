#!/usr/bin/env python

import pygame
from pygame.locals import *

from pycardrpg.engine.ui import Panel, Label
from pycardrpg.engine.event_system import event_system


#
# NotificationPanel
# Used to notify the player of any events
#

class NotificationPanel(Panel):
    
    def __init__(self, width, height):
        Panel.__init__(self, (0, 0), (800, 30))
        self.rect.midtop = (width / 2 , 0)
        self.background_color = pygame.Color("#00000000")
        self.border_color = pygame.Color("#00000000")
        self.text = ""
        
        event_system.on(self.on_show_notification, USEREVENT, 'show_notification')
        event_system.on(self.on_hide_notification, USEREVENT, 'hide_notification')

    def do_update(self):
        if len(self.text) == 0:
            return
        
        do_label = Label()
        do_label(self, (8, 8), self.text)
        
    def on_show_notification(self, data):
        self.text = data.get('text', '')
        
    def on_hide_notification(self, data):
        self.text = ''

