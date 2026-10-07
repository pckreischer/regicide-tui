import card

MAX_HAND_SIZE = 8

# draws a new hand of cards
def new_hand(deck):
    hand = []
    i = 0
    while i < MAX_HAND_SIZE:
        hand.append(deck.pop())
        i += 1
    return hand

class GameState:
    
    def __init__(self):
        self.deck = card.generate_deck()
        self.discard = []
        self.monarchy_deck = card.generate_monarchy()
        self.current_face = self.monarchy_deck.pop()
        self.hand = new_hand(self.deck)
        self.cursor = 0 
        self.selected_cards = set()
        self.attack_turn = True
        self.piles = {
        'discard': card.Pile('Discard'),
        'draw': card.Pile('Draw'),
        'joker': card.Pile('Joker')
        }

    def try_toggle_select(self, card_in):
        # todo: flesh out selection logic
        if self.is_selected(card_in):
            self.selected_cards.remove(card_in)
        else:
            self.selected_cards.add(card_in)
        
    # takes the string key input from stdscr.getkey() and processes it
    def handle_input(self, key):
        if key == 'KEY_LEFT':
            self.cursor = max(0, self.cursor - 1)
        elif key == 'KEY_RIGHT':
            self.cursor = min(len(self.hand), self.cursor + 1)
            #gs_old['card_selected'] = min(len(gs_old['hand']) - 1, gs_old['card_selected'] + 1)
        elif key == 'z':
            if self.cursor < len(self.hand):
                self.try_toggle_select(self.hand[self.cursor])
            else:
                # todo: implement jokers xd
                return 0

    def is_selected(self, card):
        return card in self.selected_cards

