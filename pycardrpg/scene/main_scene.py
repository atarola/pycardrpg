#!/usr/bin/evn python

from pycardrpg.scene.scene import Scene
from pycardrpg.entity.entity_system import EntitySystem

#
# The main scene of the game.
#

class MainScene(Scene):
    
    def __init__(self):
        self.entity_system = EntitySystem()
