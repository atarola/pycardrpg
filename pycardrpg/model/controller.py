#!/usr/bin/env python

import pygame
from pygame.locals import *

from pycardrpg.engine.entity_system import entity_system
from pycardrpg.engine.event_system import event_system, inject_user_event

from pycardrpg.model.command import command_mapping
from pycardrpg.model.component import TargetComponent

#
# Controller
# contains the application game state, used to control the commands
#

class Controller(object):
    
    def __init__(self, map):
        self.map = map
        self.target = None
        self.actions = 1
        
        event_system.on(self.on_action_card, USEREVENT, 'action_card')
        event_system.on(self.on_select_target, USEREVENT, 'select_target')
        event_system.on(self.on_end_turn, USEREVENT, 'end_turn')
        event_system.on(self.on_move_player, USEREVENT, 'move_player')

    def on_action_card(self, data):
        index = data.get('card_num', None)
        if index is None:
            return
        
        # get the card from the player's hand
        player = entity_system.find_one('PlayerComponent')
        deck = player.get('UnitComponent', 'deck')
        card = deck.hand[index]
                
        # general data passed into all commands
        data = {
            'controller': self,
            'map': self.map,
            'source': player,
            'target': self.target,
        }
                
        # generate the card commands
        commands = []
        for name, kwargs in card.commands.items():
            # add any properties from the card definition to the general data
            card_data = data.copy()
            if kwargs is not None:
                card_data.update(kwargs)
            
            command = command_mapping[name](**card_data)
            commands.append(command)
        
        # make sure all the card commands are valid
        valid = True
        for command in commands:
            # if the command is not valid, notify the user of it and stop processing the card
            if not command.is_valid():
                valid = False
                inject_user_event('show_notification', text=command.msg)
                return
        
        # execute the card 
        for command in commands:
            print "Command: %s" % command
            command.execute()
    
        # discard the card
        deck.discard(card)
        
        # note that we finished an action
        self.actions -= 1
        
        # if we have no more actions, or no more cards in our hand, end the turn
        if self.actions <= 0 or len(deck.hand) == 0:
            inject_user_event('end_turn')
        
    def on_select_target(self, data):
        if self.target is not None:
            self.target.remove_component('TargetComponent')
        
        self.target = data.get('target', None)
        
        if self.target is not None:
            self.target.add_component(TargetComponent())
        
        inject_user_event('map_changed')
        
    def on_move_player(self, data):
        delta = data.get('delta', None)
        
        if delta is None:
            return
        
        player = entity_system.find_one("PlayerComponent")
        x, y = player.get("RenderComponent", "pos")
        dx, dy = delta
        pos = (x + dx, y + dy)
    
        # if the new spot isn't passible, ignore the command
        if not self.map[pos].passible:
            return

        # if the new spot is occupied, ignore the command
        blocker = entity_system.find_one("NpcComponent", {"RenderComponent#pos": pos})
        if blocker is not None:
            return

        player.set("RenderComponent", "pos", pos)
        fov_radius = player.get('UnitComponent', 'fov_radius')
        self.map.get_fov_tiles(pos, fov_radius).seen = True
        
        inject_user_event('end_turn')
        
    def on_end_turn(self, data):
        # reset the action count
        self.actions = 1
        
        # clear the target component, if necessary
        if self.target is not None:
            self.target.remove_component('TargetComponent')
            self.target = None
        
        # check for killed npcs
        for npc in entity_system.find("NpcComponent"):
            if npc.get("UnitComponent", 'cur_hp') > 0:
                continue
            
            inject_user_event('npc_killed', npc=npc)
            entity_system.remove(npc)
        
        # recharge any npc hitpoints
        for npc in entity_system.find("NpcComponent"):
            npc.get_component("UnitComponent").do_hp_recharge()
        
        # TODO: Run AI
        
        # send an event on player death
        player = entity_system.find_one("PlayerComponent")
        if player.get("UnitComponent", 'cur_hp') < 0:
            inject_user_event('player_killed')
        
        # recharge the player's heath
        player = entity_system.find_one("PlayerComponent")
        player.get_component("UnitComponent").do_hp_recharge()
        
        # refill the player's hand
        player.get('UnitComponent', 'deck').fill_hand()
        
        inject_user_event('map_changed')

