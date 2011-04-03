#!/usr/bin/env python

from pycardrpg.scene.scene import Scene

#
# Uses the strategy pattern to encapsulate different 
# scenes in the game.
#

class SceneSystem(object):
    
    def __init__(self):
        self.scenes = {}
        self.current = Scene()

    def add_scene(self, name, scene):
        self.scenes[name] = scene
        scene.manager = self
        
    def switch_scene(self, name):
        if self.current is not None:
            self.current.on_exit()

        self.current = self.scenes[name]
        self.current.on_start()
        
    def on_event(self, event):
        self.current.process(event)
        
    def on_update(self, surface):
        self.current.on_update(surface)

