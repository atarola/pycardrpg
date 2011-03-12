#!/usr/bin/env python

from pycardrpg.scene.controller.action_event import ActionEvent

#
# Move a unit the specified delta.
#

class MoveEvent(ActionEvent):
    
    def __init__(self, name, dx, dy):
        self.name = name
        self.dx = dx
        self.dy = dy
    
    def execute(self, memory):
        entity = memory.get(self.name, None)
        x, y = entity.get("RenderComponent", "pos")
        entity.set("RenderComponent", "pos", (x + self.dx, y + self.dy))
