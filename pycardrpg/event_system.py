#!/usr/bin/env python

from weakref import WeakValueDictionary

import pygame
from pygame import USEREVENT
from pygame.event import Event

#
#
#

class EventSystem(object):
    
    def __init__(self):
        self.signals = {}
        self.stack = []
    
    def process(self, event, sprite=None):
        # setup the data dictionary
        data = event.dict
        data.setdefault('subtype', None)
        data.setdefault('sprite', sprite)
        
        # get the signal, and use it to notify the slots
        signal = self._get_signal(event.type, data['subtype'])
        signal(data)

    def on(self, event_type, handler, subtype=None):
        signal = self._get_signal(event_type, subtype)
        signal.connect(handler)

    def remove(self, event_type, handler, subtype=None):
        signal = self._get_signal(event_type, subtype)
        signal.disconnect(handler)

    def clear(self, event_type, subtype=None):
        signal = self._get_signal(event_type, subtype)
        signal.clear()

    def push(self):
        self.stack.append(self.signals)
        self.signals = {}

    def pop(self):
        signals = self.stack.pop()
        self.signals = signals

    def _get_signal(self, event_type, subtype):
        if subtype is not None:
            name = "%s#%s" % (event_type, subtype)
        else:
            name = event_type

        return self.signals.setdefault(name, Signal())

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

#
# method to create and inject user events into the pygame event system.
#

def inject_user_event(subtype, **kwargs):
    kwargs['subtype'] = subtype
    pygame.event.post(Event(USEREVENT, kwargs))

