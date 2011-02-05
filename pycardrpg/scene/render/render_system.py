#!/usr/bin/env python

import os
import pygame

from pycardrpg.scene.render.colors import Colors
from pycardrpg.scene.render.camera import Camera

#
# Render System.
#

class RenderSystem(object):

    def __init__(self, width, height, entity_system, map):
        # will be structured as [symbol][color] = image
        self.image_cache = {}
        self.font = pygame.font.Font(os.path.join('pycardrpg', 'data', 'lucon.ttf'), 12)
        
        self.entity_system = entity_system
        self.map = map
        self.camera = Camera(width, height)

    # Render this frame onto the surface    
    def render(self, surface):
        surface.fill(Colors.BLACK)

        # keeps track of rendered positions, each spot should only render once.
        rendered_pos = []
        
        player = self.entity_system.find_one("PlayerComponent", "RenderComponent", "UnitCard")
        pos = player.get("RenderComponent", "pos")
        fov_radius = player.get("UnitCard", "fov_radius")
        visible_pos = self.map.get_fov(pos, fov_radius)
        
        # move the camera to the player, then render the player
        self.camera.move(pos)
        self.render_entity(surface, rendered_pos, visible_pos, player)

        # Render units
        entities = self.entity_system.find("RenderComponent", "NPCComponent")
        for entity in entities:
            self.render_entity(surface, rendered_pos, visible_pos, entity)
            
        # Render items 
        entities = self.entity_system.find("RenderComponent", "ItemComponent")
        for entity in entities:
            self.render_entity(surface, rendered_pos, visible_pos, entity)
        
        # Figure out a better way!
#        # Render visible tiles
#        for tile in self.map.get_tiles(visible_pos):      
#            self.render_tile(surface, rendered_pos, tile, Colors.LIGHTGREY)
#        
#        # Render seen tiles
#        tiles = self.map.get_seen()
#        for tile in tiles:
#            if not self.camera.in_view(tile.pos):
#                continue
#            
#            self.render_tile(surface, rendered_pos, tile, Colors.DARKGREY)
    
    # render an entity
    def render_entity(self, surface, rendered_pos, visible_pos, entity):
        pos = entity.get("RenderComponent", "pos")
        symbol = entity.get("RenderComponent", "symbol")
        color = entity.get("RenderComponent", "color")
        
        if pos in rendered_pos:
            return
        
        if pos not in visible_pos:
            return
        
        if not self.camera.in_view(pos):
            return
        
        rendered_pos.append(pos)
        self.render_item(surface, pos, symbol, color) 
    
    # render a tile
    def render_tile(self, surface, rendered_pos, tile, color):
        if not tile.pos in rendered_pos:
            rendered_pos.append(tile.pos)
            self.render_item(surface, tile.pos, tile.symbol, color)
    
    # Render a single item onto the surface
    def render_item(self, surface, pos, symbol, color):   
        image = self.get_image(symbol, color) 
        image_pos = self.camera.translate(pos)
        surface.blit(image, image_pos)
    
    # Get the image for the symbol / color pair.
    def get_image(self, symbol, color):
        if symbol not in self.image_cache.keys():
            self.image_cache[symbol] = {}
        
        # if we have a cached version of the image, return it.
        if color in self.image_cache[symbol].keys():
            return self.image_cache[symbol][color]
        
        # create a new image, cache it, then return it.
        image = self.font.render(symbol, 0, color).convert_alpha()
        self.image_cache[symbol][color] = image
        return image
