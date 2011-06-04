#!/usr/bin/env python

import pygame
from pygame.locals import *

from pycardrpg.engine.entity_system import entity_system
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
        # setup the widgets
        do_button = Button()
        
        # render the card buttons
        ctr = 0
        deck = self._get_player_deck()
        
        for card in deck.hand:
            top = 125 + (30 * ctr)
            id = "card_button_%s" % ctr
            
            if do_button(self, id, (10, top), (230, 22), card.name):
                inject_user_event('action_card', card_num=ctr)
            
            ctr += 1

    def _get_player_deck(self):
        return entity_system.find_one("PlayerComponent").get('UnitComponent', 'deck')