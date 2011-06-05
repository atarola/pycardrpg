#!/usr/bin/env python

#
# Command
# A command is a thing a card can do.
#

class Command(object):
    
    def __init__(self):
        self.msg = ""
    
    # can this command be executed?
    def is_valid(self):
        return True
    
    # execute the command
    def execute(self):
        pass

#
# DamageCommand
#

class DamageCommand(Command):
    
    def __init__(self, **data):
        Command.__init__(self)
        
        # default properties needed
        self.map = data.get('map', None)
        self.source = data.get('source', None)
        self.target = data.get('target', None)
        
        # property on card
        self.range = data.get('range', None)
    
    def is_valid(self):
        valid = True
        
        # make sure we got all our needed properties
        valid = valid and self.map is not None
        valid = valid and self.source is not None
        valid = valid and self.target is not None
        valid = valid and self.range is not None
    
        # make sure the target is in range
        if valid:
            source_pos = self.source.get('RenderComponent', 'pos')
            dest_pos = self.target.get('RenderComponent', 'pos')
            valid = valid and self.map.in_view_distance(source_pos, dest_pos, self.range)
    
        return valid
    
    def execute(self):
        attack = self.source.get('UnitComponent', 'attack')
        defense = self.target.get('UnitComponent', 'defense')
        damage = attack - defense
        
        if damage > 0:
            hp = self.target.get('UnitComponent', 'cur_hp')
            self.target.set('UnitComponent', 'cur_hp', hp - damage)

        hp = self.target.get('UnitComponent', 'cur_hp')
        print "DamageCommand[damage: %s, hp left: %s]" % (damage, hp)

#
# used to reference the commands by a string name
#

command_mapping = {
    'DamageCommand': DamageCommand
}