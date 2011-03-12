#!/usr/bin/env python

import random

#
# Handle dice rolls
#

class Dice(object):
    
    @classmethod
    def roll(cls, dice):
        count, size = dice.split("d")
        result = 0
        
        for i in range(0, count):
            result += random.randint(1, size)
        
        return result