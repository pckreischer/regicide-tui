import random
import curses

CARD_RANKS = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
RANK_NAMES = {"A": "Ace", "J": "Jack", "Q": "Queen", "K": "King"}
CARD_SUITS = {"Spades": "♤", "Hearts": "♡", "Clubs": "♧", "Diamonds": "♢"}
#CARD_SUITS = {"Spades": "♠", "Hearts": "♥", "Clubs": "♣", "Diamonds": "♦"}

# returns deck without face cards
def generate_deck():
    deck = []
    for suit in CARD_SUITS:
        # 0 - 9: number cards
        for rank in CARD_RANKS[:9]:
            deck.append(Card(rank, suit))
    random.shuffle(deck)
    return deck

# creates shuffled monarchy deck, random suits
# but always jacks then queens then kings
def generate_monarchy():
    monarchy = [
        Card(rank, suit)
        # built in reverse so pop() works as expected
        for rank in ("K", "Q", "J")
        for suit in random.sample(list(CARD_SUITS), k = 4) # samples all of the suits
    ]
    return monarchy

class Card:

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit_name = suit
        self.suit_icon = CARD_SUITS[suit]

    def __str__(self):
        rank_name = RANK_NAMES.get(self.rank, self.rank)
        return f"{rank_name} of {self.suit_name}"

    def draw(self, stdscr, top, left):

        if len(self.rank) == 2:
            self.sprite = [
            "╭─────╮",
            f"│ {self.rank}{self.suit_icon} │",
            "│     │",
            "│     │",
            "╰─────╯"
        ]
        else:
            self.sprite = [
            "╭─────╮",
            f"│ {self.rank} {self.suit_icon} │",
            "│     │",
            "│     │",
            "╰─────╯"
        ]

        for i, row in enumerate(self.sprite):
            stdscr.addstr(top + i, left, row)

    # method to return a list of strings detailing the card value and effect
    def generate_stats(self):
        return str(self)