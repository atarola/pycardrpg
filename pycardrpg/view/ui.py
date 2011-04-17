#!/usr/bin/env python

import pygame
from pygame.locals import *

from pyengine.event_system import event_system, inject_user_event

from pycardrpg.view import get_image

#
# UI View
#

class UI(object):
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.sprite_cache = None
        
        event_system.on(self.on_mouse_up, MOUSEBUTTONUP)
    
    def get_sprites(self):
        # create and position the ui background
        self.sidebar_bg = self._create_sprite('sidebar_bg.png')
        self.sidebar_bg.rect.midright = (self.width, self.height / 2)
        
        sidebar_top = self.sidebar_bg.rect.top
        sidebar_left = self.sidebar_bg.rect.left
        
        self.action_card_one = self._create_sprite('action_card_bg.png', topleft=(sidebar_left + 10, sidebar_top + 125))
        self.action_card_two = self._create_sprite('action_card_bg.png', topleft=(sidebar_left + 10, sidebar_top + 175))
        self.action_card_three = self._create_sprite('action_card_bg.png', topleft=(sidebar_left + 10, sidebar_top + 225))
        self.action_card_four = self._create_sprite('action_card_bg.png', topleft=(sidebar_left + 10, sidebar_top + 275))
        self.action_card_five = self._create_sprite('action_card_bg.png', topleft=(sidebar_left + 10, sidebar_top + 325))

        sprites = [
            self.sidebar_bg,
            self.action_card_one,
            self.action_card_two,
            self.action_card_three,
            self.action_card_four,
            self.action_card_five
        ]
        
        return sprites
        
    def _create_sprite(self, filename, **kwargs):
        sprite = pygame.sprite.Sprite()
        sprite.image = get_image(filename);
        sprite.rect = sprite.image.get_rect(**kwargs)
        return sprite

    def on_mouse_up(self, data):
        sprite = data.get('sprite', None)
        event_type = 'action_card'
        
        mapping = {
            self.action_card_one: 0,
            self.action_card_two: 1,
            self.action_card_three: 2,
            self.action_card_four: 3,
            self.action_card_five: 4
        }
    
        card_num = mapping.get(sprite, None)

        if card_num is not None:
            inject_user_event('action_card', card_num=card_num)

