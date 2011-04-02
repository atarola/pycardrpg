#!/usr/bin/env python

import unittest
from unittest import TestCase

from pycardrpg.model.entity.unit_component import UnitComponent
from pycardrpg.model.card.card import Card

class UnitComponentTest(TestCase):

    def setUp(self):
        self.unit_card = UnitComponent()
    
    def testAddEquipmentCard(self):
        equipment_card = Card("foo", ["Equipment"])
        
        self.unit_card.add_equipment_slot()
        self.unit_card.add_equipment_card(equipment_card)
                      
        self.assertTrue(equipment_card in self.unit_card.get_equipment_cards())

    def testRemoveEquipmentCard(self):
        equipment_card = Card("foo", ["Equipment"])
        
        self.unit_card.add_equipment_slot()
        self.unit_card.add_equipment_card(equipment_card)
        self.unit_card.remove_equipment_card(equipment_card)
        
        self.assertFalse(equipment_card in self.unit_card.get_equipment_cards())

#
# Execute the test
#

if __name__ == "__main__":
    unittest.main()
