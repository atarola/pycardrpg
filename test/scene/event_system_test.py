#!/usr/bin/env python

import unittest
from unittest import TestCase

import pygame
from pygame import USEREVENT
from pygame.event import Event

from pycardrpg.scene.event_system import EventSystem

#
#
#

class EventSystemTest(TestCase):

    def setUp(self):
        self.event_system = EventSystem()

    def testHandle(self):
        event = Event(USEREVENT, {'a' : 1})
        handler = Fake()
        
        self.event_system.on(USEREVENT, handler.handle)
        self.event_system.process(event)
        
        self.assertEquals(handler.data['a'], 1)

#
# Fake object, to test the handling of stuff
#

class Fake(object):
    
    def __init__(self):
        self.data = {}
    
    def handle(self, **kwargs):
        self.data = kwargs

#
# Execute the test
#

if __name__ == "__main__":
    unittest.main()