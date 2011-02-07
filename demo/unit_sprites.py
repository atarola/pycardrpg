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
        self.sprites = MySpriteSheet("char.png", rows=41, columns=15, 
                                     startx=7, starty=120, 
                                     width=26, height=26, 
                                     skipx=9, skipy=8)
    
    def on_update(self, surface):
        surface.fill((184, 134, 11))
        
        x = 0
        y = 0
        
        for item in self.sprites:
            pos = (x * 28 + 1, y * 28 + 1)
            surface.blit(item, pos)
            
            x += 1
            if x % 30 == 0:
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
        Application.__init__(self, "UnitSprites", 840, 602, 1)
        
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