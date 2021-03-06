#!/usr/bin/env python

import sys

import pygame
from pygame.locals import *
from pygame.sprite import Sprite

from pycardrpg.engine.event_system import event_system, EventSystem
from pycardrpg.engine.render_system import render_system, LayerTypes, SpriteSheet

#
# Panel
# Basic UI Container
#

class Panel(Sprite):
    
    def __init__(self, pos, size, es=event_system):
        Sprite.__init__(self)
        
        self.image = pygame.Surface(size).convert_alpha()
        self.rect = pygame.Rect(pos, size)
        
        # panel look and feel options
        self.font = SpriteSheet('nebulas_ray.png', rows=1, columns=40, width=16, height=16)
        self.background_color = pygame.Color("#333333ff")
        self.border_color = pygame.Color("#666666ff")
        self.border_size = 1
        
        # panel state
        self.mousex = 0
        self.mousey = 0
        self.mousedown = False
        self.hotitem = 0
        self.activeitem = 0
        
        # wire up event handlers     
        es.on(self.on_mouse_motion, MOUSEMOTION)
        es.on(self.on_mouse_button_down, MOUSEBUTTONDOWN)
        es.on(self.on_mouse_button_up, MOUSEBUTTONUP)
    
    def update(self):        
        # draw the border
        self.image.fill(self.border_color)
        
        # draw the background
        delta = -(self.border_size * 2)
        rect = pygame.Rect((0, 0), self.rect.size).inflate(delta, delta)
        self.image.fill(self.background_color, rect)
        
        # prep the ui state
        self.hotitem = 0
        
        # let any subclasses do their thing
        self.do_update()
        
        # cleanup the ui state
        if not self.mousedown:
            self.activeitem = 0
        elif self.activeitem == 0:
            self.activeitem = -1

    def on_mouse_motion(self, data):
        x, y = data.get('pos', (0, 0))
        self.mousex = x - self.rect.left
        self.mousey = y - self.rect.top 

    def on_mouse_button_down(self, data):
        button = data.get('button', 0)
        
        if button == 1:
            self.mousedown = True

    def on_mouse_button_up(self, data):
        button = data.get('button', 1)
        
        if button == 1:
            self.mousedown = False

    def translate_pos(self, pos, x, y):
        a, b = pos
        return (a + x, b + y)

    # Subclasses should override this
    def do_update(self):
        pass

#
# ModalWindow
# A panel that runs it's own event pump
#

class ModalWindow(Panel):
    
    FPS = 30
    
    def __init__(self, pos, size):
        self.event_system = EventSystem()
        Panel.__init__(self, pos, size, self.event_system)
        
        self.stop = False
        
    def run(self):
        clock = pygame.time.Clock()
        surface = pygame.display.get_surface()
        render_system.add(self, layer=LayerTypes.UI_LAYER)
        
        while not self.stop:
            self.handle_events()
            self.handle_updates(surface)
            
            pygame.display.flip()
            clock.tick(ModalWindow.FPS)
        
        self.kill()
            
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(0)
            
            self.event_system.process(event)

    def handle_updates(self, surface):
        render_system.update()
        render_system.draw(surface)
       
#
# Widget
# Basic Widget
#

class Widget(object):

    CHARACTERS = """1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ!?"'"""

    def region_hit(self, ui, pos, size):
        rect = pygame.Rect(pos, size)
        return rect.collidepoint(ui.mousex, ui.mousey)
    
    def handle_hot(self, ui, id, pos, size):
        if self.region_hit(ui, pos, size):
            ui.hotitem = id
            if ui.activeitem == 0 and ui.mousedown:
                ui.activeitem = id
    
    def draw_rect(self, ui, pos, size, color):
        rect = pygame.Rect(pos, size)
        ui.image.fill(color, rect)
    
    def draw_string(self, ui, pos, string):
        x, y = pos
        for char in string:
            self.draw_character(ui, (x, y), char)
            x += 16
    
    def draw_character(self, ui, pos, char):
        char = char.upper()
        
        if char not in Widget.CHARACTERS:
            return
        
        index = Widget.CHARACTERS.index(char.upper())
        img = ui.font[index]
        ui.image.blit(img, pos)
        
    def translate_pos(self, pos, x, y):
        a, b = pos
        return (a + x, b + y)

#
# Label
# Label Widget, shows some text
#

class Label(Widget):
    
    def __call__(self, ui, pos, text):
        self.draw_string(ui, pos, text)
        
#
# ProgressBar
# ProgresBar Widget, shows a percentage 
#

class ProgressBar(Widget):
    
    def __init__(self):
        self.background_color = pygame.Color("#000000ff")
        self.border_color = pygame.Color("#666666ff")
        self.progress_color = pygame.Color("#330000ff")
        self.border_size = 1
    
    def __call__(self, ui, pos, size, percent):
        # draw the border
        self.draw_rect(ui, pos, size, self.border_color)
        
        # draw the background
        delta = -(self.border_size * 2)
        rect = pygame.Rect(pos, size).inflate(delta, delta)
        self.draw_rect(ui, rect.topleft, rect.size, self.background_color)
        
        # draw the progress
        rect.width = size[0] * percent + delta 
        self.draw_rect(ui, rect.topleft, rect.size, self.progress_color)

#
# Button
# Button Widget, returns True if the button was clicked 
#

class Button(Widget):
    
    def __init__(self):
        self.button_color = pygame.Color("#666666ff")
        self.hot_color = pygame.Color("#999999ff")
        self.shadow_color = pygame.Color("#111111ff")
        self.shadow_offset = 2
        self.active_offset = 2
        self.text_offset = 4
    
    def __call__(self, ui, id, pos, size, text):
        self.handle_hot(ui, id, pos, size)
        self.draw(ui, id, pos, size, text)
        return self.is_clicked(ui, id)
    
    # render the button
    def draw(self, ui, id, pos, size, text):
        # draw the shadow
        shadow_pos = self.translate_pos(pos, self.shadow_offset, self.shadow_offset)
        self.draw_rect(ui, shadow_pos, size, self.shadow_color)
        
        if ui.hotitem != id:
            # button is not "hot", but may be "active"
            self.draw_rect(ui, pos, size, self.button_color)
            self.draw_text(ui, pos, text)
            return

        if ui.activeitem == id:
            # button is both "hot" and "active"
            active_pos = self.translate_pos(pos, self.active_offset, self.active_offset)
            self.draw_rect(ui, pos, size, self.hot_color)
            self.draw_text(ui, pos, text)
            return
            
        # button is just "hot"
        self.draw_rect(ui, pos, size, self.hot_color)
        self.draw_text(ui, pos, text)

    # draw the text   
    def draw_text(self, ui, pos, text):
        text_pos = self.translate_pos(pos, self.text_offset, self.text_offset)
        self.draw_string(ui, text_pos, text)
      
    # has the button been clicked?
    def is_clicked(self, ui, id):
        is_clicked = ui.mousedown == 0
        is_clicked = is_clicked and ui.hotitem == id
        is_clicked = is_clicked and ui.activeitem == id
        return is_clicked

