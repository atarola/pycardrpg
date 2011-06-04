#!/usr/bin/env python

import pygame
from pygame.locals import *

from pycardrpg.engine.script_system import ScriptEvent

#
# TargetCommand
# Choose a target and add it to the memory
#

class VerifyTargetCommand(object):
    pass

#
# DamageCommand
# Do damage from the subject to the target
#

class DamageCommand(object):
    pass

#
# MoveCommand
# Move the player to a chosen spot
#

class MoveCommand(object):
    pass

#
# Command Mapping
# Used to reference the Commands by name
#

mapping = {
    'VerifyTargetCommand': VerifyTargetCommand,
    'DamageCommand': DamageCommand
}

