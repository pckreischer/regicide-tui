from dataclasses import dataclass
import random

RANKS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
SUITS = ['Spades', 'Hearts', 'Diamonds', 'Clubs']
RANK_VALUES = {
    'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7,
    '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 15, 'K': 20
}

@dataclass(frozen=True, order=True)
class Card:
    rank: str
    suit: str

    def __post_init__(self):
        pass  # frozen dataclass auto-generates __eq__, __repr__

    @property
    def value(self):
        return RANK_VALUES[self.rank]

    def __str__(self):
        return f"{self.rank} of {self.suit}"

    @property
    def short(self):
        # e.g. "10♥", "KS", etc — whatever fits your display
        suit_symbols = {'Spades': '♠', 'Hearts': '❤', 'Diamonds': '♦', 'Clubs': '♣'}
        return f"{self.rank}{suit_symbols[self.suit]}"

def build_deck():
    return [Card(rank, suit) for suit in SUITS for rank in RANKS]

deck = build_deck()
random.shuffle(deck)

print(deck[0])
print(deck[0].value)  
print(deck[0].short)