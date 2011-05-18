#!/usr/bin/env python

from pyengine.event_system import event_system
from pyengine.render_system import render_system
from pyengine.script_system import script_system

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
        
    def switch_scene(self, name):
        if self.current is not None:
            self.current.on_exit()

        self.current = self.scenes[name]
        self.current.on_start() 
        
    def on_event(self, event):
        self.current.on_event(event)
        
    def on_update(self, surface):
        self.current.on_update(surface)
        
#
# A single scene.  Represents a single section of the game. 
# contains a list of sprites, and dispatches events.
#

class Scene(object):

    def on_event(self, event):
        sprite = None
        
        if 'pos' in event.dict.keys():
            sprite = render_system.get_sprite(event.pos)
        
        event_system.process(event, sprite)
    
    def on_update(self, surface):
        script_system.update()
        render_system.update()
        render_system.draw(surface)
        
    def on_start(self):
        pass 

    def on_exit(self):
        pass

#
# singleton scene system
#

scene_system = SceneSystem()

