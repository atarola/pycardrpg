#!/usr/bin/env python

import unittest
from unittest import TestCase

from card_system.card import Card
from card_system.deck import Deck

#
#
#

class SlotTest(TestCase):
    
    def setUp(self):
        self.cards = [Card('A'), Card('B'), Card('C'), Card('D'), Card('E')]
        
    def testShouldHaveHand(self):
        deck = Deck(self.cards, 1)
        self.assertEquals(len(deck.hand), 1)
        
        deck = Deck(self.cards, 2)
        self.assertEquals(len(deck.hand), 2)
    
    def testShouldHandleDiscards(self):
        deck = Deck(self.cards, 2)
        card = deck.hand[0]
        deck.discard(card)    
        self.assertTrue(card not in deck.hand)
        self.assertEquals(len(deck.hand), 2)
        self.assertEquals(len(deck.pile), 1)
        
    def testShouldResetDeck(self):
        deck = Deck(self.cards, 4)        
        card = deck.hand[0]
        deck.discard(card)  
        self.assertEquals(len(deck.pile), 1)
        card = deck.hand[0]
        deck.discard(card)
        self.assertEquals(len(deck.pile), 0)

#
# Make sure the unit test runs on its own
#

if __name__ == '__main__':
    unittest.main()
