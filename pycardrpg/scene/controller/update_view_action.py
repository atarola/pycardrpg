#!/usr/bin/env python

from pycardrpg.scene.controller.action_event import ActionEvent

#
# Move a unit the specified delta.
#

class UpdateViewAction(ActionEvent):
    
    def __init__(self, entity, map):
        ActionEvent.__init__(self)
        self.entity = entity
        self.map = map
    
    def execute(self):
        pos = self.entity.get("RenderComponent", "pos")
        fov_radius = self.entity.get("UnitComponent", "fov_radius")
        self.map.get_fov_tiles(pos, fov_radius).seen = True
