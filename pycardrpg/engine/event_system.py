#!/usr/bin/env python

import pygame
from pygame.locals import *

APPMOUSEFOCUS = 1
APPINPUTFOCUS = 2
APPACTIVE = 4
LEFT_BUTTON = 1
MIDDLE_BUTTON = 2
RIGHT_BUTTON = 3

#
# Event System.  Handle user events
#

class EventSystem(object):
    
    # delegate the event to the proper method
    def on_event(self, event):
        
        # we don't care about these here (or at all)
        if event.type in [QUIT, JOYAXISMOTION, JOYBALLMOTION, JOYHATMOTION]:
            return
        
        if self.filter_event(event):
            return
        
        if event.type == ACTIVEEVENT:
            # Mouse Focus
            if event.state == APPMOUSEFOCUS:
                if event.gain:
                    self.on_mouse_focus()
                    return
                else:
                    self.on_mouse_blur()
                    return
                    
            # Keyboard Focus
            if event.state == APPINPUTFOCUS:
                if event.gain:
                    self.on_input_focus()
                    return
                else:
                    self.on_input_blur()
                    return
                    
            # Window State
            if event.state == APPACTIVE:
                if event.gain:
                    self.on_restore()
                    return
                else:
                    self.on_minimize()
                    return
        
        if event.type == KEYDOWN:
            self.on_key_down(event.scancode, event.key, event.mod, event.unicode)
            return
          
        if event.type == KEYUP:
            self.on_key_up(event.scancode, event.key, event.mod)
            return
            
        if event.type == MOUSEMOTION:
            self.on_mouse_move(event.pos[0], 
                               event.pos[1], 
                               event.rel[0], 
                               event.rel[1], 
                               event.buttons[0],
                               event.buttons[1],
                               event.buttons[2])
            return
        
        if event.type == MOUSEBUTTONDOWN:
            if event.button == LEFT_BUTTON:
                self.on_left_button_down(event.pos[0], event.pos[1])
                return
                
            if event.button == MIDDLE_BUTTON:
                self.on_middle_button_down(event.pos[0], event.pos[1])
                return
            
            if event.button == RIGHT_BUTTON:
                self.on_right_button_down(event.pos[0], event.pos[1])
                return
        
        if event.type == MOUSEBUTTONUP:            
            if event.button == LEFT_BUTTON:
                self.on_left_button_up(event.pos[0], event.pos[1])
                return
                
            if event.button == MIDDLE_BUTTON:
                self.on_middle_button_up(event.pos[0], event.pos[1])
                return
            
            if event.button == RIGHT_BUTTON:
                self.on_right_button_up(event.pos[0], event.pos[1])
                return

        if event.type == VIDEORESIZE:
            self.on_resize(event.w, event.h)
            return
            
        if event.type == VIDEOEXPOSE:
            self.on_expose()
            return
        
        if event.type == USEREVENT:
            self.on_user(event.message, event.data)
        
    # return true if the event should not be processed  
    def filter_event(self, event):
        return False
    
    # 
    # Active Events
    #
    
    def on_input_focus(self):
        pass
    
    def on_input_blur(self):
        pass
    
    def on_mouse_focus(self):
        pass
    
    def on_mouse_blur(self):
        pass
    
    def on_minimize(self):
        pass
    
    def on_restore(self):
        pass
    
    #
    # Keyboard Events
    #
    
    def on_key_down(self, scancode, key, mod, unicode):
        pass
    
    def on_key_up(self, scancode, key, mod):
        pass
    
    #
    # Mouse Events
    #
    
    def on_mouse_move(self, x, y, relx, rely, left, middle, right):
        pass
    
    def on_left_button_down(self, x, y):
        pass
    
    def on_left_button_up(self, x, y):
        pass
    
    def on_right_button_down(self, x, y):
        pass
    
    def on_right_button_up(self, x, y):
        pass
    
    def on_middle_button_down(self, x, y):
        pass
    
    def on_middle_button_up(self, x, y):
        pass

    #
    # Window events
    #
    
    def on_resize(self, width, height):
        pass
    
    def on_expose(self):
        pass
    
    #
    # User Events
    #
    
    def on_user(self, message, data):
        pass
