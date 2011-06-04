#!/usr/bin/env python

import math

import pygame
from pygame.locals import *
from pygame.sprite import Sprite

from pycardrpg.engine.entity_system import entity_system
from pycardrpg.engine.event_system import event_system, inject_user_event
from pycardrpg.engine.render_system import SpriteSheet

#
# Map Sprite
#

class MapSprite(Sprite):

    BLACK = (0, 0, 0)
    TARGET_COLOR = (255, 0, 0)

    def __init__(self, width, height, level_map):
        Sprite.__init__(self)

        self.map_sprites = SpriteSheet("sprites_map.png", rows=16, columns=16, starty=40)
        self.unit_sprites = SpriteSheet("sprites_char.png", rows=41, columns=15, startx=7, 
                                        starty=120, width=26, height=26, skipx=9, 
                                        skipy=8)

        self.fow_sprite = pygame.Surface((16, 16)).convert()
        self.fow_sprite.fill(MapSprite.BLACK)
        self.fow_sprite.set_alpha(128)

        self.camera = Camera(width, height)
        self.map = level_map

        self.image = pygame.Surface((width, height)).convert()
        self.rect = pygame.Rect((0, 0), (width, height))
        self.on_map_changed(None)
        
        event_system.on(self.on_map_changed, USEREVENT, 'map_changed')
        event_system.on(self.on_mouse_up, MOUSEBUTTONUP)
        
    # If we are the sprite under the cursor, do some work.
    def on_mouse_up(self, data):
        pos = data.get('pos', None)
        array_pos = self.camera.to_array(pos)
        
        # if there is an entity under the cursor, it needs to be targeted
        entity = entity_system.find_one('RenderComponent', conditions={'RenderComponent#pos': array_pos})
        if entity:
            inject_user_event('select_target', target=entity)

    # Render this frame onto the surface, we'll use the painters algorithm
    # and render from back to front
    def on_map_changed(self, data):
        self.image.fill(MapSprite.BLACK)

        # move the camera to the player
        player = entity_system.find_one("PlayerComponent")
        pos = player.get("RenderComponent", "pos")
        fov_radius = player.get("UnitComponent", "fov_radius")
        
        # move the camera to follow the player
        self.camera.move((pos[0] + 5, pos[1]))

        # render the tiles
        tiles = self.map[self.camera.rect].filter("seen", True)
        tiles_fov = self.map.get_fov_tiles(pos, fov_radius)
        for tile in tiles:
            visible = tile in tiles_fov
            self._render_tile(self.image, tile, visible)

        # render the npcs
        npcs = entity_system.find("NpcComponent")
        for npc in npcs: 
            tile = self.map[npc.get("RenderComponent", "pos")]         
            if tile in tiles_fov:
                self._render_unit(self.image, npc)

        # render player
        self._render_unit(self.image, player)

    # render a tile
    def _render_tile(self, surface, tile, visible):
        pos = self.camera.to_pixels(tile.pos)
        image = self.map_sprites[tile.index]
        surface.blit(image, pos)

        if not visible:
            surface.blit(self.fow_sprite, pos)

    # render a unit
    def _render_unit(self, surface, unit):
        self._render_unit_background(surface, unit)
        self._render_unit_sprite(surface, unit)
        
    def _render_unit_background(self, surface, unit):
        pos = unit.get("RenderComponent", "pos")
        pos = self.camera.to_pixels(pos)
        
        # if the unit is the target, draw the targetting square around them
        if unit.has_component('TargetComponent'):
            rect = pygame.Rect(pos, Camera.CHAR_SIZE)
            pygame.draw.rect(surface, MapSprite.TARGET_COLOR, rect, 2)
        
    def _render_unit_sprite(self, surface, unit):
        image = self.unit_sprites[unit.get("RenderComponent", "index")]
        pos = unit.get("RenderComponent", "pos")

        # the units are taller and fatter than the tiles, so we'll need to offset
        x, y = self.camera.to_pixels(pos)
        surface.blit(image, (x - 4, y - 12))

#
# Camera object
#

class Camera(object):
    CHAR_SIZE = (16, 16)

    def __init__(self, width, height):
        width = math.floor(width / Camera.CHAR_SIZE[0]) + 2
        height = math.floor(height / Camera.CHAR_SIZE[1]) + 2
        self.rect = pygame.Rect(-1, -1, width, height)

    def move(self, pos):
        self.rect.center = pos

    def in_view(self, pos):
        return self.rect.collidepoint(pos)
        
    def to_array(self, pos):
        x, y = pos
        a, b = Camera.CHAR_SIZE
  
        tx = (x / a) + self.rect.left
        ty = (y / b) + self.rect.top

        return (tx, ty)

    def to_pixels(self, pos):
        x, y = pos
        a, b = Camera.CHAR_SIZE

        tx = abs(x - self.rect.left) * a
        ty = abs(y - self.rect.top) * b

        return (tx, ty) 

