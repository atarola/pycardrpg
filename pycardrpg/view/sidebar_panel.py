#!/usr/bin/env python

import pygame
from pygame.locals import *

from pycardrpg.engine.entity_system import entity_system
from pycardrpg.engine.event_system import inject_user_event
from pycardrpg.engine.ui import Panel, Button, Label, ProgressBar

#
# UI Sidebar
#

class SidebarPanel(Panel):
    
    def __init__(self, width, height):
        Panel.__init__(self, (0, 0), (250, 245))
        self.rect.midright = (width - 10, height / 2)
        
    def do_update(self):
        player = entity_system.find_one("PlayerComponent")

        # setup the widgets
        do_button = Button()
        do_progress_bar = ProgressBar()
        do_label = Label()
        
        # Hit Points
        do_label(self, (10, 10), 'HP')
        cur_hp = player.get('UnitComponent', 'cur_hp') * 1.0 
        max_hp = player.get('UnitComponent', 'max_hp')
        do_progress_bar(self, (10, 30), (230, 22), cur_hp / max_hp)
        
        # Action Cards
        do_label(self, (10, 70), 'Action Cards')
        ctr = 0
        deck = player.get('UnitComponent', 'deck')
        for card in deck.hand:
            top = 90 + (30 * ctr)
            id = "card_button_%s" % ctr
            
            if do_button(self, id, (10, top), (230, 22), card.name):
                inject_user_event('action_card', card_num=ctr)
            
            ctr += 1

