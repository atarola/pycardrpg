#!/usr/bin/env python

import unittest
from unittest import TestCase

from pycardrpg.card_system.card import Card
from pycardrpg.card_system.slot import Slot, DoesNotFitException

#
# 
#

class SlotTest(TestCase):
    
    def setUp(self):
        self.foo_card = Card('foo', ['foo'])
        self.bar_card = Card('bar', ['bar'])
        self.foobar_card = Card('foobar', ['foo', 'bar'])
    
    def testSlotWithNoRequirements(self):
        slot = Slot('a')
        slot.add_card(self.foo_card)
        slot.add_card(self.bar_card)
    
    def testSlotWithOneReqirement(self):
        slot = Slot('a', ['foo'])
        slot.add_card(self.foo_card)
        slot.add_card(self.foobar_card)
        self.assertRaises(DoesNotFitException, slot.add_card, self.bar_card)
        
    def testSlotWithTwoRequirements(self):
        slot = Slot('a', ['foo', 'bar'])
        slot.add_card(self.foobar_card)
        self.assertRaises(DoesNotFitException, slot.add_card, self.foo_card)
        self.assertRaises(DoesNotFitException, slot.add_card, self.bar_card)

#
# Make sure the unit test runs on its own
#

if __name__ == '__main__':
    unittest.main()
