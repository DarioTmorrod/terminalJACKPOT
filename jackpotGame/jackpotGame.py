import random
import time
import curses
import json

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
        else:
            print_menu(stdscr,current_row_idx)

def initCredits(stdscr):
    stdscr.clear()
    f = open("CREDITS.json",)
    json_data = json.load(f)
    key = 0
    while key!=curses.KEY_ENTER and key not in [10,13]:
        stdscr.clear()
        stdscr.addstr(0,0,json_data["title"])
        stdscr.addstr(1,0,json_data["body"])
        stdscr.addstr(10, 0, "PRESS RETURN TO GO BACK")
        stdscr.refresh()
        key = stdscr.getch()

    main(stdscr)

def initScoreBoard(stdscr):
    stdscr.clear()
    f = open("SCOREBOARD.json",)
    json_data = json.load(f)
    key = 0
    while key!=curses.KEY_ENTER and key not in [10,13]:
        stdscr.clear()
        #i=0
        #for row in json_data["AAA"]:
        #    stdscr.addstr(i, 0, row[i +1])
        #    i+=1
        
        stdscr.addstr(0, 0, "(DEVELOPING) PRESS RETURN TO GO BACK")
        stdscr.refresh()
        key = stdscr.getch()

    main(stdscr)

def roll(max):
    result = [random.randint(1,max),random.randint(1,max),random.randint(1,max)]

    return result

def rollFX(stdscr,result):
    h , w = stdscr.getmaxyx()
    loadEfect = ["/","-","\\","|"]*3
    rollStates = ["[ - : - : - ]","[ "+str(result[0])+" : - : - ]","[ "+str(result[0])+" : "+str(result[1])+" : - ]","[ "+str(result[0])+" : "+str(result[1])+" : "+str(result[2])+" ]"] 

    for state in rollStates:
        x = w//2 - len(state)//2
        y = h//2 
        if state.find("-")!= -1:
            for bar in loadEfect:
                temp = state.replace("-",bar,1)
                stdscr.clear()
                stdscr.addstr(y, x, temp)
                stdscr.refresh()
                time.sleep(0.2)
        else:
            temp = state
            stdscr.clear()
            stdscr.addstr(y, x, temp)
            stdscr.refresh()
            time.sleep(0.2)

    stdscr.addstr(0,0,"PRESS ESC TO EXIT")
    if result[0]==result[1] and result[1]==result[2]:
        text = " $  $  $  *YOU WIN*  $  $  $"
        x = w//2 - len(text)/2
        stdscr.addstr(y+3,x,text)
    else:
        text = "SORRY... PRESS ENTER TO TRY AGAIN"
        x = w//2 - len(text)/2
        stdscr.addstr(y+3,x,text)
    


def initPlay(stdscr):
    stdscr.clear()
    result = roll(5)
    rollFX(stdscr,result)
    key = stdscr.getch()
    while key != curses.KEY_ENTER and key not in [10,13,27]:
        key = stdscr.getch()
    
    if key == curses.KEY_ENTER or key in [10,13]:
        initPlay(stdscr)
    elif key == 27:
        main(stdscr)

    main(stdscr)

        

def main(stdscr):
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK,curses.COLOR_WHITE)
    selected = init_menu(stdscr)

    if selected == menu_str[0]:#PLAY
        initPlay(stdscr)
    elif selected == menu_str[1]:#CREDIT
        initCredits(stdscr)
    elif selected == menu_str[2]:#SCORE BOARD
        initScoreBoard(stdscr)
    elif selected == menu_str[3]:#quit
        exit()

    Wait()
        

    
curses.wrapper(main)