import curses
import card

MAX_HAND_SIZE = 8

deck = card.generate_deck()

hand = []
card_selected = 0

def newHand():
    hand.clear()
    i = 0
    while i < MAX_HAND_SIZE:
        hand.append(deck.pop())
        i += 1

def renderHand(stdscr, sh, sw):
    left = (sw // 2) - (MAX_HAND_SIZE // 2 * 6) - 4 # hardcoded card size
    h = sh - 9

    for i in range(len(hand)):
        if i == card_selected:
            hand[i].draw(stdscr, h - 2, left)
            stdscr.addstr(h - 3, left + 3, "▼") # more hardcoded card size shenanigans but its ok
            card_stats = hand[i].generateStats()
            stdscr.addstr(h - 4, (left + 3) - (len(card_stats) // 2), card_stats)


        else: 
            hand[i].draw(stdscr, h, left)
        left += 7
    stdscr.refresh()

def update(stdscr):

    sh, sw = stdscr.getmaxyx()  # screen height, width

    stdscr.clear()
    renderHand(stdscr, sh, sw)



def main(stdscr):
    global card_selected
    # Hide the blinking cursor
    curses.curs_set(0)
    # Don't wait for Enter — read keys immediately
    # stdscr.nodelay(True)
    # Let getch() understand arrow keys
    stdscr.keypad(True)


    newHand()
    update(stdscr)

    while True:
        key = stdscr.getkey()

        if key == "KEY_LEFT":
            card_selected = max(0, card_selected - 1)
        elif key == "KEY_RIGHT":
            card_selected = min(len(hand) - 1, card_selected + 1)
        elif key == "q":
            break
        update(stdscr)


curses.wrapper(main)
