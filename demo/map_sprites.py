#!/usr/bin/env python

import os

from pycardrpg.application import Application
from pycardrpg.scene.render.sprite_sheet import SpriteSheet
from pycardrpg.scene.scene import Scene

#
# Render the sprites nicely
#

class DummyScene(Scene):
    
    def __init__(self):
        self.sprites = MySpriteSheet("map.png", rows=16, columns=16, starty=40)
        self.spacing = 20
    
    def on_update(self, surface):
        surface.fill((184, 134, 11))
        
        x = 0
        y = 0
        
        for item in self.sprites:
            pos = (x * 18 + 1, y * 18 + 1)
            surface.blit(item, pos)
            
            x += 1
            if x % 16 == 0:
                x = 0
                y += 1
                
#
# Fix the sprite path problems
#

class MySpriteSheet(SpriteSheet):
    
    def _get_filename(self, file):
        return os.path.join('..', 'pycardrpg', 'data', file)

#
# View the map sprites
#

class MapSprites(Application):
    
    def __init__(self):
        Application.__init__(self, "MapSprites", 288, 288, 1)
        
        self.add_scene("DummyScene", DummyScene())
        self.switch_scene("DummyScene")
        
    @classmethod
    def start(cls):
        cls().run()

#
# Run the app if this file is called from the commandline
#

if __name__ == "__main__":
    MapSprites.start()