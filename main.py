#!/usr/bin/env python

from pycardrpg.engine.application import Application
from pycardrpg.engine.scene_system import Scene

#
# PyCardRPG specific Application Class
#

class PyCardRPG(Application):
    
    def __init__(self):
        Application.__init__(self, "PyGameRPG v0.1", 800, 600, 30)
        self.add_scene("MainScene", DummyScene())
        self.switch_scene("MainScene")
    
    @classmethod
    def start(cls):
        cls().run()

#
# Dummy Scene
#

class DummyScene(Scene):
    pass
    
#
# Run the app if this file is called from the commandline
#

if __name__ == "__main__":
    PyCardRPG.start()