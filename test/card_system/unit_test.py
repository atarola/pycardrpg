#!/usr/bin/env python

import unittest
from unittest import TestCase

from pycardrpg.card_system.card import Card
from pycardrpg.card_system.unit import Unit

#
# 
#

class MyUnitTest(TestCase):
    
    def setUp(self):
        self.card = Card(name="Shield", 
                         tags=['Equipment', 'Hand'], 
                         modifiers={"Armor": 1337})
        
        self.unit = Unit("bob")
        self.unit.add_equipment_slot(["Hand"])
        self.unit.add_equipment_card(self.card)

    def testGetModifier(self):
        self.assertEquals(self.unit.get_modifier("Armor"), 1337)

    def testRemoveEquipmentCard(self):
        self.unit.remove_equipment_card(self.card)
        self.assertEquals(self.unit.get_modifier("Armor"), 0)

    def testAddEquipmentCard(self):
        self.unit.remove_equipment_card(self.card)
        self.assertEquals(self.unit.get_modifier("Armor"), 0)
        self.unit.add_equipment_card(self.card)
        self.assertEquals(self.unit.get_modifier("Armor"), 1337)

    def testUnitHP(self):
        self.unit.base_strength = 1
        self.unit.base_stamina = 1
        self.assertEquals(self.unit.max_hp, 1)
        
        self.unit.base_strength = 2
        self.assertEquals(self.unit.max_hp, 2)
        
        self.unit.base_stamina = 2
        self.assertEquals(self.unit.max_hp, 3)
    
    def testUnitAP(self):
        self.unit.base_dexterity = 1
        self.unit.base_stamina = 1
        self.assertEquals(self.unit.max_ap, 1)
        
        self.unit.base_dexterity = 2
        self.assertEquals(self.unit.max_ap, 2)
        
        self.unit.base_stamina = 2
        self.assertEquals(self.unit.max_ap, 3)
    
#
# Make sure the unit test runs on its own
#

if __name__ == '__main__':
    unittest.main()
