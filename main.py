import curses
import card

cards = []
selected = 0

def generate_card(rank, suit):
    if len(rank) == 2:
        return [
        "╭─────╮",
        f"│ {rank}{suit} │",
        "│     │",
        "│     │",
        "╰─────╯"
    ]
    else:
        return [
        "╭─────╮",
        f"│ {rank} {suit} │",
        "│     │",
        "│     │",
        "╰─────╯"
    ]

def draw_sprite(stdscr, sprite, top, left):
    for i, row in enumerate(sprite):
        stdscr.addstr(top + i, left, row)

def main(stdscr):
    # Hide the blinking cursor
    curses.curs_set(0)
    # Don't wait for Enter — read keys immediately
    stdscr.nodelay(True)
    # Let getch() understand arrow keys
    stdscr.keypad(True)

    sh, sw = stdscr.getmaxyx()  # screen height, width
    y, x = sh // 2, sw // 2      # player start position

    # 

    while True:
        stdscr.clear()
        draw_sprite(stdscr, generate_card("10", "S"), y, x)
        stdscr.addstr(0, 0, "Arrow keys to move, 'q' to quit")
        stdscr.refresh()


        ## resolve inputs
        key = stdscr.getch()

        if key == curses.KEY_UP and y > 1:
            y -= 1
        elif key == curses.KEY_DOWN and y < sh - 1:
            y += 1
        elif key == curses.KEY_LEFT and x > 0:
            x -= 1
        elif key == curses.KEY_RIGHT and x < sw - 1:
            x += 1
        if key == ord('q'):
            break

        curses.napms(30)  # small delay so it's not maxing out CPU

curses.wrapper(main)