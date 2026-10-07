import random

CARD_WIDTH = 7
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
        for rank in list(RANK_VALUES)[:10]:
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

# returns list of stats based on current cards, face card, and attack turn
# note: immunity logic should be handled before feeding values here
def generate_selection_info(cards_in, face_in, attack_turn):

    if attack_turn:
        values = [0, 0, 0, 0]  
        info = []

        # find totals in each suit
        for card in cards_in:
            match card.suit_name:
                case 'Hearts': values[0] += RANK_VALUES[card.rank]
                case 'Diamonds': values[1] += RANK_VALUES[card.rank]
                case 'Clubs': values[2] += RANK_VALUES[card.rank]
                case 'Spades': values[3] += RANK_VALUES[card.rank]

        # generate text
        info = []
        if values[0] != 0: 
            if values[0] == 1: info.append(f'Restore 1 card')
            else: info.append(f'Restores {values[0]} cards')
        if values[1] != 0: 
            if values[1] == 1: info.append(f'Draw 1 card')
            else: info.append(f'Draw {values[1]} cards')
        if values[2] != 0: info.append(f'Deals {values[2]} damage')
        if values[3] != 0: info.append(f'Shields {values[3]} attack')

    else:
        for card in cards_in:
            total += RANK_VALUES[card.rank]
        info.append(f'Block {total} damage')

    #info.append(cards_in.__str__())
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

    def draw(self, stdscr, top, left, value = -1):
        self.sprite = []
        self.sprite.append(self.pile_type)
        match self.pile_type:
            case 'Joker':
                self.sprite.extend([
                    "╭─────╮",
                    "│  J  │╮",
                    "│     ││",
                    "│     ││",
                    "╰─────╯│",
                    " ╰─────╯",
                    # todo: qol feature where this icon changes when there's 1 or 0 cards left
                ])
            case _:
                self.sprite.extend([
                    "╭─────╮",
                    "│╲╱╲╱╲│╮",
                    "│╱╲╱╲╱││",
                    "│╲╱╲╱╲││",
                    "╰─────╯│",
                    " ╰─────╯",
                    # todo: qol feature where this icon changes when there's 1 or 0 cards left
                ])
                self.sprite.append(f"({value}/40)") # note: hardcoded deck size (at least graphically)
        for i, row in enumerate(self.sprite):
            stdscr.addstr(top + i, left, row)

