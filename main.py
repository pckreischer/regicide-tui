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
            'top': sh - 9,
            'left': sw - card.CARD_WIDTH - 5
        },
        'attack_turn': {
            'top': sh - 5,
            'left': 5
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
    # render cursor
    if gs.cursor < len(gs.hand):
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

def render_jokers(stdscr, region):
    gs.piles['joker'].draw(stdscr, region['top'], region['left'], gs.jokers)
    if gs.cursor >= len(gs.hand):
        stdscr.addstr(region['top'] - 1, region['left'] + (card.CARD_WIDTH // 2), '▼')

# function that draws the current monarchy card
def render_monarchy(stdscr, region):
    gs.current_face.draw(stdscr, region['top'], region['left'])
    
    # face card name
    card_name = str(gs.current_face)
    stdscr.addstr(region['top'] - 2, (region['left'] + (card.CARD_WIDTH // 2)) - (len(card_name) // 2), card_name)

def render_draw_pile(stdscr, region):
    gs.piles['draw'].draw(stdscr, region['top'], region['left'], len(gs.deck))

def render_discard_pile(stdscr, region):
    gs.piles['discard'].draw(stdscr, region['top'], region['left'], len(gs.discard))

def render_attack_turn(stdscr, region):
    if gs.attack_turn:
        stdscr.addstr(region['top'], region['left'], 'Turn: ATTACK')
    else:
        stdscr.addstr(region['top'], region['left'], 'Turn: DEFEND')

# main rendering update function
def update(stdscr):

    sh, sw = stdscr.getmaxyx()  # screen height, width
    regions = compute_regions(sh, sw)

    stdscr.erase()
    render_draw_pile(stdscr, regions['deck'])
    render_discard_pile(stdscr, regions['discard'])
    render_monarchy(stdscr, regions['monarchy'])
    render_attack_turn(stdscr, regions['attack_turn'])
    render_hand(stdscr, regions['hand'])
    render_jokers(stdscr, regions['jokers'])
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
