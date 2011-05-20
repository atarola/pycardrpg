#!/usr/bin/env python

from pycardrpg.engine.entity_system import entity_system

#
# Simulation
#

class Simulation(object):
    
    def __init__(self, map):
        self.map = map
        
    def update(self):
        self.end_player_turn()
        self.begin_npc_turn()
        self.run_ai()
        self.end_npc_turn()
        self.begin_player_turn()
        
    def end_player_turn(self):
        for npc in entity_system.find("NpcComponent"):
            if npc.get("UnitComponent", 'cur_hp') > 0:
                continue
            
            print "Killed: %s" % npc
            entity_system.remove(npc)
        
    def begin_npc_turn(self):
        for npc in entity_system.find("NpcComponent"):
            npc.get_component("UnitComponent").do_hp_recharge()
        
    def run_ai(self):
        print "Run AI"
        
    def end_npc_turn(self):
        player = entity_system.find_one("PlayerComponent")
        
        if player.get("UnitComponent", 'cur_hp') < 0:
            print "Killed: %s" % player
            entity_system.remove(player)
        
    def begin_player_turn(self):
        player = entity_system.find_one("PlayerComponent")
        player.get_component("UnitComponent").do_hp_recharge()

