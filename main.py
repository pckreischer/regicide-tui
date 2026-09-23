import curses
import card

MAX_HAND_SIZE = 8
CARD_WIDTH = 7

# game state dict that holds all the changing gameplay elements
gs = {
    'deck': [],
    'discard': [],
    'monarchy_deck': [],
    'current_face': None,
    'hand': [],
    'card_selected': 0,
    'attack_turn': None,
    # blocked effect can be derived from current face
    'piles': {
        'discard': card.Pile('Discard'),
        'draw': card.Pile('Draw')
    }
}

# function to setup all the state variables at game start
def initialize():
    gs['deck'] = card.generate_deck()
    gs['hand'] = new_hand()
    gs['monarchy_deck'] = card.generate_monarchy()
    gs['current_face'] = gs['monarchy_deck'].pop()
    gs['attack_turn'] = True

# calculates where certain UI elements anchors should be placed,
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
        },
        'deck': {
            'top': sh // 2 - 3,
            'left': 5
        },
        'discard': {
            'top': sh // 2 - 3,
            'left': sw - CARD_WIDTH - 5
        }
    }

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
    h_offset = 0
    card_stats = card.generate_card_info(gs['hand'][gs['card_selected']], gs['current_face'], gs['attack_turn'])
    for i in range(len(gs['hand'])):
        if i == gs['card_selected']: # draw selected card up and with info
            gs['hand'][i].draw(stdscr, region['top'] - 2, region['left'] + h_offset)
            stdscr.addstr(region['top'] - 3, region['left'] + 3 + h_offset, '▼') # more hardcoded card size shenanigans but its ok
            # todo: implement new card stat rendering

            v_offset = (len(card_stats))
            for stat in card_stats:
                stdscr.addstr(region['top'] - 3 - v_offset, (region['left'] + 3) - (len(stat) // 2) + h_offset, stat)
                v_offset -= 1

            #card_stats = game_state['hand'][i].generate_stats()
            #stdscr.addstr(region['top'] - 4, (region['left'] + 3) - (len(card_stats) // 2) + offset, card_stats)
        else: 
            gs['hand'][i].draw(stdscr, region['top'], region['left'] + h_offset)
        h_offset += CARD_WIDTH

# function that draws the current monarchy card
def render_monarchy(stdscr, region):
    # face card name
    gs['current_face'].draw(stdscr, region['top'], region['left'])
    card_name = str(gs['current_face'])
    stdscr.addstr(region['top'] - 2, (region['left'] + (CARD_WIDTH // 2)) - (len(card_name) // 2), card_name)

def render_draw_pile(stdscr, region):
    gs['piles']['draw'].draw(stdscr, region['top'], region['left'], len(gs['deck']))

def render_discard_pile(stdscr, region):
    gs['piles']['discard'].draw(stdscr, region['top'], region['left'], len(gs['discard']))

# main rendering update function
def update(stdscr):

    sh, sw = stdscr.getmaxyx()  # screen height, width
    regions = compute_regions(sh, sw)

    stdscr.erase()
    render_draw_pile(stdscr, regions['deck'])
    render_discard_pile(stdscr, regions['discard'])
    render_monarchy(stdscr, regions['monarchy'])
    render_hand(stdscr, regions['hand'])

    stdscr.refresh()

def main(stdscr):
    # Hide the blinking cursor
    curses.curs_set(0)
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
