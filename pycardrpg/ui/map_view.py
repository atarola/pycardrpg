#!/usr/bin/env python

import math

import pygame
from pygame.locals import *
from pygame.sprite import Sprite

from pycardrpg.event_system import inject_user_event
from pycardrpg.ui.sprite_sheet import SpriteSheet
from pycardrpg.ui.view import View

#
# Map View, Handle player movement
#

class MapView(View):
    
    def __init__(self, width, height, event_system, entity_system, level_map):
        View.__init__(self, event_system, entity_system, level_map)
        
        self.width = width
        self.height = height
        self.map_sprite = None
        
    def load(self, data):
        self.event_system.on(KEYUP, self.on_keyup)

    def unload(self):
        self.event_system.remove(KEYUP, self.on_keyup)
        
    def get_sprites(self):
        if self.map_sprite is None:
            self.map_sprite = MapSprite(self.width, self.height, self.event_system, self.entity_system, self.level_map)
            
        return [self.map_sprite]

    # move the character on keyup
    def on_keyup(self, data):
        key = data.get('key', 0)

        if key in [K_UP, K_w]:
            self.move_player(0, -1)
            return   
            
        if key in [K_DOWN, K_s]:
            self.move_player(0, 1)
            return
            
        if key in [K_LEFT, K_a]:
            self.move_player(-1, 0)
            return
            
        if key in [K_RIGHT, K_d]:
            self.move_player(1, 0)
            return
 
    def move_player(self, dx, dy):
        player = self.entity_system.find_one("PlayerComponent")
        x, y = player.get("RenderComponent", "pos")
        pos = (x + dx, y + dy)
        
        # if the new spot isn't passible, ignore the command
        if not self.level_map[pos].passible:
            return

        # if the new spot is occupied, ignore the command
        for entity in self.entity_system.find("NpcComponent"):
            if entity.get("RenderComponent", "pos") == pos:
                return

        player.set("RenderComponent", "pos", pos)
        self._update_fov(player)
        
        inject_user_event('map_changed')
        inject_user_event('end_turn')

    def _update_fov(self, player):
        pos = player.get("RenderComponent", "pos")
        fov_radius = player.get("UnitComponent", "fov_radius")
        self.level_map.get_fov_tiles(pos, fov_radius).seen = True

#
# Map Sprite
#

class MapSprite(Sprite):

    BLACK = (0, 0, 0)

    def __init__(self, width, height, event_system, entity_system, level_map):
        Sprite.__init__(self)

        self.map_sprites = SpriteSheet("sprites_map.png", rows=16, columns=16, starty=40)
        self.unit_sprites = SpriteSheet("sprites_char.png", rows=41, columns=15, startx=7, 
                                        starty=120, width=26, height=26, skipx=9, 
                                        skipy=8)

        self.fow_sprite = pygame.Surface((16, 16)).convert()
        self.fow_sprite.fill(MapSprite.BLACK)
        self.fow_sprite.set_alpha(128)

        self.camera = Camera(width, height)
        self.entity_system = entity_system
        self.map = level_map

        self.image = pygame.Surface((width, height)).convert()
        self.rect = pygame.Rect((0, 0), (width, height))
        self.changed = True

        event_system.on(USEREVENT, self.on_changed, subtype="map_changed")

    def update(self):
        if not self.changed:
            return

        self.changed = False
        self.render_map()

    def on_changed(self, data):
        self.changed = True

    # Render this frame onto the surface, we'll use the painters algorithm
    # and render from back to front
    def render_map(self):
        self.image.fill(MapSprite.BLACK)

        # move the camera to the player
        player = self.entity_system.find_one("PlayerComponent")
        pos = player.get("RenderComponent", "pos")
        fov_radius = player.get("UnitComponent", "fov_radius")
        self.camera.move(pos)

        # render the tiles
        tiles = self.map[self.camera.rect].filter("seen", True)
        tiles_fov = self.map.get_fov_tiles(pos, fov_radius)
        for tile in tiles:
            visible = tile in tiles_fov
            self.render_tile(self.image, tile, visible)

        # render the npcs
        npcs = self.entity_system.find("NpcComponent")
        for npc in npcs: 
            tile = self.map[npc.get("RenderComponent", "pos")]         
            if tile in tiles_fov:
                self.render_unit(self.image, npc)

        # render player
        self.render_unit(self.image, player)

    # render a tile
    def render_tile(self, surface, tile, visible):
        pos = self.camera.translate(tile.pos)
        image = self.map_sprites[tile.index]
        surface.blit(image, pos)

        if not visible:
            surface.blit(self.fow_sprite, pos)

    def render_unit(self, surface, unit):
        image = self.unit_sprites[unit.get("RenderComponent", "index")]
        pos = unit.get("RenderComponent", "pos")

        # the units are taller and fatter than the tiles, so we'll need to offset
        x, y = self.camera.translate(pos)
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

    def translate(self, pos):
        x, y = pos
        a, b = Camera.CHAR_SIZE

        tx = abs(x - self.rect.left) * a
        ty = abs(y - self.rect.top) * b

        return (tx, ty) 

