#!/usr/bin/env python

from pycardrpg.scene.controller.action_event import ActionEvent

#
# Move a unit the specified delta.
#

class MoveAction(ActionEvent):
    
    def __init__(self, entity, dx, dy):
        ActionEvent.__init__(self)
        self.entity = entity
        self.dx = dx
        self.dy = dy
    
    def execute(self):
        x, y = self.entity.get("RenderComponent", "pos")
        self.entity.set("RenderComponent", "pos", (x + self.dx, y + self.dy))
