import random
import curses

CARD_RANKS = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
CARD_SUITS = {"Spades": "♤", "Hearts": "♡", "Clubs": "♧", "Diamonds": "♢"}
#CARD_SUITS = {"Spades": "♠", "Hearts": "♥", "Clubs": "♣", "Diamonds": "♦"}

def generate_deck():
    deck = []
    for suit in CARD_SUITS:
        for rank in CARD_RANKS:
            deck.append(Card(rank, suit))
    random.shuffle(deck)
    return deck

class Card:

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit_name = suit
        self.suit_icon = CARD_SUITS[suit]

    def __str__(self):
        return f"{self.rank} of {self.suit_name}"

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
        