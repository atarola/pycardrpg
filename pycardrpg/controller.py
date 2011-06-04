#!/usr/bin/env python

import pygame
from pygame.locals import *

from pycardrpg.engine.entity_system import entity_system
from pycardrpg.engine.event_system import event_system, inject_user_event
from pycardrpg.model.component import TargetComponent

from pycardrpg.command import mapping

#
# SimulationController
# handle the world simulation
#

class SimulationController(object):
    
    def __init__(self, map):
        self.map = map
        
        event_system.on(self.on_end_turn, USEREVENT, 'end_turn')
    
    def on_end_turn(self, data):
        # check for killed npcs
        for npc in entity_system.find("NpcComponent"):
            if npc.get("UnitComponent", 'cur_hp') > 0:
                continue
            
            print "Killed: %s" % npc
            entity_system.remove(npc)
        
        # recharge any npc hitpoints
        for npc in entity_system.find("NpcComponent"):
            npc.get_component("UnitComponent").do_hp_recharge()
        
        # TODO: Run the AI
        
        # send an event on player death
        player = entity_system.find_one("PlayerComponent")
        if player.get("UnitComponent", 'cur_hp') < 0:
            inject_user_event('player_killed')
        
        # recharge the player's heath
        player = entity_system.find_one("PlayerComponent")
        player.get_component("UnitComponent").do_hp_recharge()

#
# MoveController
# handle player movement
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
# TargetController
# handle the selecting of entities
# 

class TargetController(object):
    
    def __init__(self, map):
        self.map = map
        
        event_system.on(self.on_select_target, USEREVENT, 'select_target')
        event_system.on(self.on_remove_target, USEREVENT, 'remove_target')
        
    def on_remove_target(self, data):
        self._remove_old_target()
        
    def on_select_target(self, data):
        target = data.get('target', None)
        if target is None:
            return

        self._remove_old_target()

        # add the target component to the target entity
        target.add_component(TargetComponent())
        inject_user_event('map_changed')
        
    def _remove_old_target(self):
        entity = entity_system.find_one('TargetComponent')
        
        if entity is not None:
            entity.remove_component('TargetComponent')

#
# ActionCardController
# handle using action cards
#

class ActionCardController(object):

    def __init__(self, map):
        self.map = map
        event_system.on(self.on_action_card, USEREVENT, 'action_card')

    def on_action_card(self, data):
        pass

        
