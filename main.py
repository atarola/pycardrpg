#!/usr/bin/env python

from pycardrpg.application import Application
from pycardrpg.scene.main_scene import MainScene

#
# PyCardRPG specific Application Class
#

class PyCardRPG(Application):
    
    def __init__(self):        
        Application.__init__(self, "PyGameRPG v0.1", 800, 600, 30)
        
        self.add_scene("MainScene", MainScene())
        self.switch_scene("MainScene")
    
    @classmethod
    def start(cls):
        cls().run()
    
#
# Run the app if this file is called from the commandline
#

if __name__ == "__main__":
    PyCardRPG.start()