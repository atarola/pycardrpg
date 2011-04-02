#!/usr/bin/env python

from weakref import WeakValueDictionary

import pygame
from pygame.locals import * 

#
# Event System.  Uses a signal/slot system to process information.
#

class EventSystem(object):
	
	def __init__(self):
		self.signals = {}
	
	def process(self, event):
		signal = self._get_signal(event.type)
		signal(**event.dict)
	
	def on(self, event_type, handler):
		signal = self._get_signal(event_type)
		signal.connect(handler)
		
	def remove(self, event_type, handler):
		signal = self._get_signal(event_type)
		signal.disconnect(handler)

	def clear(self, event_type):
		signal = self._get_signal(event_type)
		signal.clear()
		
	def _get_signal(self, event_type):
		return self.signals.setdefault(event_type, Signal())

#
# Signal Class, used to represent a single signal type.  
# From: http://code.activestate.com/recipes/576477-yet-another-signalslot-implementation-in-python
#

class Signal(object):
    def __init__(self):
        self.__slots = WeakValueDictionary()

    def __call__(self, *args, **kargs):
        for key in self.__slots:
            func, _ = key
            func(self.__slots[key], *args, **kargs)

    def connect(self, slot):
        key = (slot.im_func, id(slot.im_self))
        self.__slots[key] = slot.im_self

    def disconnect(self, slot):
        key = (slot.im_func, id(slot.im_self))
        if key in self.__slots:
            self.__slots.pop(key)

    def clear(self):
        self.__slots.clear()
