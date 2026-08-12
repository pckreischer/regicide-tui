import curses
import card

deck = card.generate_deck()
selected = 0 

hand = []

def newHand():
    hand.clear()
    i = 0
    while i < 8: # hardcoded hand size
        hand.append(deck.pop())
        i += 1

def renderHand(stdscr, sh, sw):
    left = (sw // 2) - (4 * 6) - 3 # more hardcoded hand size
    for card_obj in hand:
        card_obj.draw(stdscr, sh // 2, left)
        left += 8
    stdscr.refresh()

def main(stdscr):
    # Hide the blinking cursor
    curses.curs_set(0)
    # Don't wait for Enter — read keys immediately
    # stdscr.nodelay(True)
    # Let getch() understand arrow keys
    stdscr.keypad(True)

    sh, sw = stdscr.getmaxyx()  # screen height, width

    newHand()
    renderHand(stdscr, sh, sw)

    stdscr.getkey()


curses.wrapper(main)
