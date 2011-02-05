#!/usr/bin/env python

import random

#
# A Deck of Cards
#

class Deck(object):
    
    def __init__(self, cards=[], size=40, hand_size=5):
        self.size = size
        self.hand_size = hand_size
        self.cards = list(cards)
        self.pile = []
        self.hand = []
        
        self.validate_deck()

    # TODO: setup the validation of the deck
    def validate_deck(self):
        return True
    
    def discard(self, card):
        self.hand.remove(card)
        self.pile.append(card)

    def shuffle(self):
        random.shuffle(self.cards)
        
    def reset_deck(self):
        self.cards.extend(self.pile)
        self.pile = []
        self.shuffle()
    
    def fill_hand(self):
        while len(self.hand) < self.hand_size:
            # if there are no cards in the good, reset
            if len(self.cards) == 0:
                self.reset_deck() 
            
            # add the next card to the hand
            self.hand.append(self.cards.pop())
