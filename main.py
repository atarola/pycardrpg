#!/usr/bin/env python

from pyengine.application import Application
from pyengine.scene_system import scene_system

from pycardrpg.main_scene import MainScene

#
# PyCardRPG specific Application Class
#

class PyCardRPG(Application):
    
    def __init__(self):        
        Application.__init__(self, "PyGameRPG v0.1", 800, 600, 60)
        
        scene_system.add_scene("MainScene", MainScene())
        scene_system.switch_scene("MainScene")
    
    @classmethod
    def start(cls):
        cls().run()
        
#
# Run the app if this file is called from the commandline
#

if __name__ == "__main__":
    PyCardRPG.start() 