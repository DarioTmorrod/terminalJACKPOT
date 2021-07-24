#import random
import time
import curses

def Wait():
    time.sleep(1.0)

menu_str=["PLAY","CREDIT","SCORE BOARD","QUIT"]
def print_menu(stdscr, selected_row_idx):
    stdscr.clear()
    h , w = stdscr.getmaxyx()

    for idx, row in enumerate(menu_str):
        if(idx==selected_row_idx):
            x = w//2 - len(row)//2
            y = h//2 - len(menu_str)//2 + idx
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, x, row)
            stdscr.attroff(curses.color_pair(1))
        else:
            x = w//2 - len(row)//2
            y = h//2 - len(menu_str)//2 + idx
            stdscr.addstr(y, x, row)
    
    stdscr.refresh()

def init_menu(stdscr):
    current_row_idx = 0
    print_menu(stdscr, current_row_idx)
    while 1:
        key = stdscr.getch()
        stdscr.clear()
        if key == curses.KEY_UP and current_row_idx > 0:
            current_row_idx -= 1
            print_menu(stdscr,current_row_idx)
        elif key == curses.KEY_DOWN and current_row_idx < len(menu_str) -1:
            current_row_idx += 1
            print_menu(stdscr,current_row_idx)
        elif key == curses.KEY_ENTER or key in [10,13]:
            selected = menu_str[current_row_idx]
            return selected
        

def main(stdscr):
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK,curses.COLOR_WHITE)
    selected = init_menu(stdscr)
    stdscr.addstr(0, 0,selected)
    stdscr.refresh()

    Wait()
        

    
curses.wrapper(main)