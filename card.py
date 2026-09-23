import random
import curses

RANK_VALUES = {
    "A": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10,
    "J": 10, "Q": 15, "K": 20,
}
RANK_NAMES = {"A": "Ace", "J": "Jack", "Q": "Queen", "K": "King"}
CARD_SUITS = {"Spades": "♤", "Hearts": "♡", "Clubs": "♧", "Diamonds": "♢"}
#CARD_SUITS = {"Spades": "♠", "Hearts": "♥", "Clubs": "♣", "Diamonds": "♦"}

# returns deck without face cards
def generate_deck():
    deck = []
    for suit in CARD_SUITS:
        # 0 - 9: number cards
        for rank in list(RANK_VALUES)[:9]:
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

# returns list of stats based on current card
def generate_card_info(card_in, face_in, attack_turn):
        info = []
        info.append(card_in.__str__())
        
        # suit effects
        if attack_turn:
            match card_in.suit_name:
                case 'Spades':
                    info.append(f'Blocks {RANK_VALUES[card_in.rank]} damage')
                case 'Hearts':
                    info.append(f'Restores {RANK_VALUES[card_in.rank]} cards')
                case 'Clubs':
                    info.append(f'Deals {RANK_VALUES[card_in.rank] * 2} damage')
                case 'Diamonds':
                    info.append(f'Draws {RANK_VALUES[card_in.rank]} cards')

        return info

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

class Pile:

    def __init__(self, pile_type):
        self.pile_type = pile_type

    def draw(self, stdscr, top, left, value):
        self.sprite = []
        self.sprite.extend([
            "╭─────╮",
            "│╲╱╲╱╲│╮",
            "│╱╲╱╲╱││",
            "│╲╱╲╱╲││",
            "╰─────╯│",
            " ╰─────╯",
            # todo: qol feature where this icon changes when there's 1 or 0 cards left
        ])
        self.sprite.append(self.pile_type)
        self.sprite.append(f"({value}/40)") # note: hardcoded deck size (at least graphically)
        for i, row in enumerate(self.sprite):
            stdscr.addstr(top + i, left, row)

