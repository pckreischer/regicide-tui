import curses
import card, game

# game state dict that holds all the changing gameplay elements
gs_old = {
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

gs = game.GameState()

# function to setup all the state variables at game start
def initialize():
    gs_old['deck'] = card.generate_deck()
    gs_old['hand'] = new_hand()
    gs_old['monarchy_deck'] = card.generate_monarchy()
    gs_old['current_face'] = gs_old['monarchy_deck'].pop()
    gs_old['attack_turn'] = True

# calculates where certain UI elements anchors should be placed,
# returns dict of the regions
def compute_regions(sh,sw):
    return {
        'hand': {
            'top': sh - 8,
            'left': (sw // 2) - (game.MAX_HAND_SIZE // 2 * card.CARD_WIDTH)
        },
        'monarchy': {
            'top': sh // 2 - 3, 
            'left': sw // 2 - (card.CARD_WIDTH // 2)
        },
        'deck': {
            'top': sh // 2 - 3,
            'left': 5
        },
        'discard': {
            'top': sh // 2 - 3,
            'left': sw - card.CARD_WIDTH - 5
        },
        'jokers': {
            'top': sh - 8,
            'left': sw - card.CARD_WIDTH - 5
        }
    }

# draws a new hand of cards
def new_hand():
    gs_old['hand'].clear()
    hand = []
    i = 0
    while i < game.MAX_HAND_SIZE:
        hand.append(gs_old['deck'].pop())
        i += 1
    return hand

def render_debug(stdscr):
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_MAGENTA)
    stdscr.addstr(3, 10, str(gs.cursor), curses.color_pair(1))

# function that draws cards in your hand, as well as jokers
def render_hand(stdscr, region):
    h_offset = 0
    # rendering individual cards
    for i in range(len(gs.hand)):
        if gs.hand[i] in gs.selected_cards:
            gs.hand[i].draw(stdscr, region['top'] - 2, region['left'] + h_offset)
        else:
            gs.hand[i].draw(stdscr, region['top'], region['left'] + h_offset)
        h_offset += card.CARD_WIDTH
    # rendering jokers
    # actually we'll have another function for that
    #gs.piles['joker'].draw(stdscr, region['top'], region ['left'])
    # render cursor
    select_offset = 0
    if gs.is_selected(gs.hand[gs.cursor]): select_offset = 2
    stdscr.addstr(region['top'] - 1 - select_offset, region['left'] + (card.CARD_WIDTH // 2) + (gs.cursor * card.CARD_WIDTH), '▼') # more hardcoded card size shenanigans but its ok
    # render card info
    card_stats = card.generate_selection_info(gs.selected_cards, gs.current_face, gs.attack_turn)
    v_offset = (len(card_stats))
    for stat in card_stats:
        #stdscr.addstr(region['top'] - 3 - v_offset, (region['left'] + 3) - (len(stat) // 2) + h_offset, stat)
        stdscr.addstr(region['top'] - 3 - v_offset, region['left'] + (card.CARD_WIDTH // 2) + (gs.cursor * card.CARD_WIDTH) - (len(stat) // 2), stat)
        v_offset -= 1

# function that draws the current monarchy card
def render_monarchy(stdscr, region):
    # face card name
    gs_old['current_face'].draw(stdscr, region['top'], region['left'])
    
    card_name = str(gs_old['current_face'])
    stdscr.addstr(region['top'] - 2, (region['left'] + (CARD_WIDTH // 2)) - (len(card_name) // 2), card_name)

def render_draw_pile(stdscr, region):
    gs_old['piles']['draw'].draw(stdscr, region['top'], region['left'], len(gs_old['deck']))

def render_discard_pile(stdscr, region):
    gs_old['piles']['discard'].draw(stdscr, region['top'], region['left'], len(gs_old['discard']))

# main rendering update function
def update(stdscr):

    sh, sw = stdscr.getmaxyx()  # screen height, width
    regions = compute_regions(sh, sw)

    stdscr.erase()
    #render_draw_pile(stdscr, regions['deck'])
    #render_discard_pile(stdscr, regions['discard'])
    #render_monarchy(stdscr, regions['monarchy'])
    render_hand(stdscr, regions['hand'])
    render_debug(stdscr)

    stdscr.refresh()

def main(stdscr):
    # Hide the blinking cursor
    curses.curs_set(0)
    # Let getch() understand arrow keys
    stdscr.keypad(True)

    #initialize()
    update(stdscr)

    while True:
        key = stdscr.getkey()

        if key == 'q':
            break
        else:
            gs.handle_input(key)
        update(stdscr)


curses.wrapper(main)
