import random

# Constants for card ranks and suits
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
suits = ['hearts', 'diamonds', 'clubs', 'spades']

# Hand rankings used for poker evaluation
HAND_RANKINGS = {
            "high_card": 0,
            "one_pair": 1,
            "two_pairs": 2,
            "three_of_a_kind": 3,
            "straight": 4,
            "flush": 5,
            "full_house": 6,
            "four_of_a_kind": 7,
            "straight_flush": 8,
        }

# Define a Card class to represent playing cards
class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        
        # Mapping of card ranks to integer values for poker hand evaluation
        rankToVal = {
            '2':2,
            '3':3,
            '4':4,
            '5':5,
            '6':6,
            '7':7,
            '8':8,
            '9':9,
            '10':10,
            'J':11,
            'Q':12,
            'K':13,
            'A':1
        }
        self.value = rankToVal[self.rank]
    
    def __str__(self):
        return f"{self.rank} of {self.suit}"
          
# Define a Deck class to represent a deck of playing cards
class Deck:
    def __init__(self):
        # Create a list of Card objects for a standard deck of 52 cards and shuffle it
        self.cards = [Card(rank,suit) for suit in suits for rank in ranks]
        self.size = 52
        # Shuffle the deck
        random.shuffle(self.cards)
        
    def drawCard(self) -> Card:
        # Draw (pop) a card from the deck and return it
        if self.size == 0:
            return None
        
        self.size -= 1
        return self.cards.pop()
    
     