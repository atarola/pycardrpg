#!/usr/bin/env python

import pygame
from pygame.locals import *

from pyengine.entity_system import entity_system
from pyengine.event_system import event_system, inject_user_event
from pyengine.script_system import script_system, Script

from pycardrpg.command import mapping

#
# Move Controller, handle player movement
#

class MoveController(object):

    def __init__(self, map):
        self.map = map
        event_system.on(self.on_keyup, KEYUP)
            
    # move the character on keyup
    def on_keyup(self, data):
        key = data.get('key', 0)

        if key in [K_UP, K_w]:
            self.move_player(0, -1)
            return
        
        if key in [K_DOWN, K_s]:
            self.move_player(0, 1)
            return
        
        if key in [K_LEFT, K_a]:
            self.move_player(-1, 0)
            return
        
        if key in [K_RIGHT, K_d]:
            self.move_player(1, 0)
            return

    def move_player(self, dx, dy):
        player = entity_system.find_one("PlayerComponent")
        x, y = player.get("RenderComponent", "pos")
        pos = (x + dx, y + dy)
    
        # if the new spot isn't passible, ignore the command
        if not self.map[pos].passible:
            return

        # if the new spot is occupied, ignore the command
        blocker = entity_system.find_one("NpcComponent", {"RenderComponent#pos": pos})
        if blocker is not None:
            return

        player.set("RenderComponent", "pos", pos)
        self._update_fov(player)
    
        inject_user_event('map_changed')
        inject_user_event('end_turn')

    def _update_fov(self, player):
        pos = player.get("RenderComponent", "pos")
        fov_radius = player.get("UnitComponent", "fov_radius")
        self.map.get_fov_tiles(pos, fov_radius).seen = True

#
# Action Card Controller, handle using action cards
#

class ActionCardController(object):

    def __init__(self, map):
        self.map = map
        event_system.on(self.on_action_card, USEREVENT, 'action_card')

    def on_action_card(self, data):
        # stop the current event handlers from firing, by pushing a new
        # set into the event handler
        event_system.push()
        
        deck = self._get_player_deck()
        card = deck.hand[data['card_num']]
        deck.discard(card)
                
        # setup the script
        memory = self._get_default_memory()
        script = Script(memory=memory, callback=self.on_script_done)
        for name, kwargs in card.commands.items():
            if kwargs is None:
                kwargs = {}
            
            command = mapping[name](**kwargs)
            script.append(command)
        
        # put the script in to be executed
        script_system.add('action_cards', script, self.on_script_done)
        
    def on_script_done(self, script):
        # bring back the original event handlers
        event_system.pop()
        inject_user_event('map_changed')
        inject_user_event('end_turn')

    def _get_player_deck(self):
        return entity_system.find_one("PlayerComponent").get('UnitComponent', 'deck')
        
    def _get_default_memory(self):
        memory = {
            'source': entity_system.find_one("PlayerComponent"),
            'map': self.map
        }
        
        return memory

