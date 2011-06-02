#!/usr/bin/env python

import pygame
from pygame.locals import *

from pycardrpg.engine.event_system import inject_user_event
from pycardrpg.engine.ui import ModalWindow, Button

class TestWindow(ModalWindow):
    
    def __init__(self):
        ModalWindow.__init__(self, (350, 250), (100, 100))
        
    def do_update(self):
        do_button = Button()
        
        if do_button(self, 1, (10, 10), (80, 80), 'Foo!'):
            self.stop = True

