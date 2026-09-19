import curses
import card

MAX_HAND_SIZE = 8
CARD_WIDTH = 7

# game state dict that holds all the changing gameplay elements
gs = {
    'deck': [],
    'monarchy_deck': [],
    'current_face': None,
    'hand': [],
    'card_selected': 0,
    'attack_turn': True
}

# function to setup all the state variables at game start
def initialize():
    gs['deck'] = card.generate_deck()
    gs['hand'] = new_hand()
    gs['monarchy_deck'] = card.generate_monarchy()
    gs['current_face'] = gs['monarchy_deck'].pop()
    

# calculates where certain UI elements should be placed,
# returns dict of the regions
def compute_regions(sh,sw):
    return {
        'hand': {
            'top': sh - 8,
            'left': (sw // 2) - (MAX_HAND_SIZE // 2 * CARD_WIDTH)
        },
        'monarchy': {
            'top': sh // 2 - 3, 
            'left': sw // 2 - (CARD_WIDTH // 2)
        }
    }

# returns list of stats based on current card
def generate_card_info(card, face):
        info = []
        info.append(card.__str__())
        
        match card.suit_name:
            case 'Spades':
                info.append(f'')
            case 'Hearts':
                return 0
            case 'Clubs':
                return 0
            case 'Diamonds':
                return 0

        return info

# draws a new hand of cards
def new_hand():
    gs['hand'].clear()
    hand = []
    i = 0
    while i < MAX_HAND_SIZE:
        hand.append(gs['deck'].pop())
        i += 1
    return hand

# function that draws each card in the hand
def render_hand(stdscr, region):
    offset = 0
    #card_stats = generate_card_info(gs['card_selected'], gs['current_face'])
    for i in range(len(gs['hand'])):
        if i == gs['card_selected']:
            gs['hand'][i].draw(stdscr, region['top'] - 2, region['left'] + offset)
            stdscr.addstr(region['top'] - 3, region['left'] + 3 + offset, '▼') # more hardcoded card size shenanigans but its ok
            # todo: implement new card stat rendering
            #card_stats = game_state['hand'][i].generate_stats()
            #stdscr.addstr(region['top'] - 4, (region['left'] + 3) - (len(card_stats) // 2) + offset, card_stats)
        else: 
            gs['hand'][i].draw(stdscr, region['top'], region['left'] + offset)
        offset += CARD_WIDTH

# function that draws the current monarchy card
def render_monarchy(stdscr, region):
    gs['current_face'].draw(stdscr, region['top'], region['left'])
    card_name = str(gs['current_face'])
    stdscr.addstr(region['top'] - 2, (region['left'] + (CARD_WIDTH // 2)) - (len(card_name) // 2), card_name)

# main rendering update function
def update(stdscr):

    sh, sw = stdscr.getmaxyx()  # screen height, width
    regions = compute_regions(sh, sw)

    stdscr.erase()
    render_hand(stdscr, regions['hand'])
    render_monarchy(stdscr, regions['monarchy'])

    stdscr.refresh()

def main(stdscr):
    #global card_selected
    # Hide the blinking cursor
    curses.curs_set(0)
    # Don't wait for Enter — read keys immediately
    # stdscr.nodelay(True)
    # Let getch() understand arrow keys
    stdscr.keypad(True)

    initialize()
    update(stdscr)

    while True:
        key = stdscr.getkey()

        if key == 'KEY_LEFT':
            gs['card_selected'] = max(0, gs['card_selected'] - 1)
        elif key == 'KEY_RIGHT':
            gs['card_selected'] = min(len(gs['hand']) - 1, gs['card_selected'] + 1)
        elif key == 'q':
            break
        update(stdscr)


curses.wrapper(main)
