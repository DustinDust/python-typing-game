import curses
from curses import wrapper
import time
from get_text import get_text

def start_screen(stdscr):
    stdscr.erase()
    stdscr.addstr("Welcome to the Speed typing key test")
    stdscr.addstr("\nPress any key to begin")
    stdscr.getkey()


def display_text(stdscr, target_text, current_text, wpm=0):
    stdscr.addstr(target_text, curses.color_pair(3))
    stdscr.addstr(2, 0, f"WPM: {wpm}")

    for index, char in enumerate(current_text):
        correct_char = target_text[index]
        if correct_char != char:
            stdscr.addstr(0, index, correct_char, curses.color_pair(2))
        else:
            stdscr.addstr(0, index, char, curses.color_pair(1))


def display_ending_screen(stdscr, wpm, target_text, current_text) -> int:
    stdscr.erase()
    current_string = "".join(current_text)
    len_diff = 0
    if target_text != current_string:
        for index, char in enumerate(target_text):
            if char != current_string[index]:
                len_diff = len_diff + 1

    score = "%.2f" % (100.0 - (len_diff * 100 / len(target_text)))
    stdscr.addstr(f"Congrats! You've got {score} of the target text correct!")
    stdscr.addstr(f"\nYour WPM is {wpm}\n")
    stdscr.addstr("\n...Press ESC to quit, press Enter to play again")
    stdscr.refresh()
    char = stdscr.getkey()
    return -1 if ord(char) == 27 else 1


def wpm_test(stdscr):
    target_text = get_text()
    current_text = []
    stdscr.erase()
    stdscr.addstr(target_text, curses.color_pair(3))
    stdscr.refresh()
    stdscr.nodelay(True)

    wpm = 0
    start_time = time.time()

    while True:
        time_lapse = max(time.time() - start_time, 1)
        wpm = round((len(current_text) / (time_lapse / 60)) / 5)

        if len(current_text) <= len(target_text):
            stdscr.erase()
            display_text(stdscr, target_text, current_text, wpm=wpm)
            stdscr.refresh()
        else:
            stdscr.nodelay(False)
            option = display_ending_screen(stdscr, wpm, target_text, current_text)
            if option < 0:
                exit()
            else:
                break

        try:
            key = stdscr.getkey()
        except:
            continue

        # key in
        current_text.append(key)

        # if the key user hit is the backspace remove that bull shit
        if key in ("KEY_BACKSPACE", "\b", "\x7f"):
            current_text.pop()
            if len(current_text) > 0:
                current_text.pop()

        if len(key) > 1:
            current_text.pop()
            continue

        if ord(key) == 27:
            break


def main(stdscr):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

    while True:
        start_screen(stdscr=stdscr)
        wpm_test(stdscr)


wrapper(main)
