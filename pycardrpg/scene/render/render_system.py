#!/usr/bin/env python

import sys

import pygame

from pycardrpg.scene.render.camera import Camera
from pycardrpg.scene.render.colors import Colors
from pycardrpg.scene.render.sprite_sheet import SpriteSheet

#
# Render System.
#

class RenderSystem(object):

    def __init__(self, width, height, entity_system, map):
        self.map_sprites = SpriteSheet("map.png", rows=16, columns=16, starty=40)
        self.unit_sprites = SpriteSheet("char.png", rows=41, columns=15, startx=7, 
                                        starty=120, width=26, height=26, skipx=9, 
                                        skipy=8)
        
        self.fow_sprite = pygame.Surface((16, 16)).convert()
        self.fow_sprite.fill(Colors.BLACK)
        self.fow_sprite.set_alpha(128)
        
        self.camera = Camera(width, height)
        self.entity_system = entity_system
        self.map = map

        
    # Render this frame onto the surface, we'll use the painters algorithm
    # and render from back to front    
    def render(self, surface):
        surface.fill(Colors.BLACK)
        
        # move the camera to the player
        player = self.entity_system.find_one("PlayerComponent", "RenderComponent", "UnitCard")
        pos = player.get("RenderComponent", "pos")
        fov_radius = player.get("UnitCard", "fov_radius")
        self.camera.move(pos)
        
        # render the tiles
        tiles = self.map[self.camera.rect].filter("seen", True)
        tiles_fov = self.map.get_fov_tiles(pos, fov_radius)
        for tile in tiles:
            visible = tile in tiles_fov
            self.render_tile(surface, tile, visible)
    
        # render player
        self.render_unit(surface, player)
    
    # render a tile
    def render_tile(self, surface, tile, visible):
        pos = self.camera.translate(tile.pos)
        image = self.map_sprites[tile.index]
        surface.blit(image, pos)
        
        if not visible:
            surface.blit(self.fow_sprite, pos)
    
    def render_unit(self, surface, unit):
        image = self.unit_sprites[unit.get("RenderComponent", "sprite_index")]
        pos = unit.get("RenderComponent", "pos")
        
        # the units are taller and fatter than the tiles, so we'll need to offset
        x, y = self.camera.translate(pos)
        surface.blit(image, (x - 4, y - 12))
    

