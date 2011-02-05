#!/usr/bin/env python

#
# Card Repository, used to track and search for cards in the game.
#

class CardRepository(object):
    
    def __init__(self):
        self.ids = {}
        self.tags = {}
        self.names = {}
    
    def register_card(self, card):
        # register by id
        self.ids[card.id] = card
        
        # register by name
        name = card.name
        if name not in self.names.keys():
            self.names[name] = set()
        self.names[name].add(card)
        
        # register by tags
        tags = card.tags
        for tag in tags:
            if tag not in self.tags.keys():
                self.tags[tag] = set()    
            self.tags[tag].add(card)
    
    def find_by_name(self, name):
        return list(self.names.get(name, []))
    
    def find_by_id(self, id):
        return self.ids.get(id, None)
    
    def find_by_tags(self, *args):
        cards = None
        
        for tag in args:
            # if there are no cards in the repository
            # with that tag, don't bother to continue
            if tag not in self.tags.keys():
                return []
            
            if cards is None:
                cards = set(self.tags[tag])
            else:
                cards.intersection_update(self.tags[tag])
        
        return list(cards)

#
# Singleton instance of CardRepository
#

repository = CardRepository()