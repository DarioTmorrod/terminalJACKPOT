import random
import time
import curses
import json
from datetime import date

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
    h,w =stdscr.getmaxyx()
    f = open("CREDITS.json",)
    json_data = json.load(f)
    key = 0
    title = json_data["title"]
    body = json_data["body"]
    while key!=curses.KEY_ENTER and key not in [10,13]:
        stdscr.clear()
        x = w//2 -len(title)//2
        stdscr.attron(curses.A_BOLD)
        stdscr.addstr(1,x,title)
        stdscr.attroff(curses.A_BOLD)
        x = w//2 -len(body)//2
        stdscr.addstr(3,x,body)
        stdscr.addstr(0, 0, "PRESS RETURN TO GO BACK")
        stdscr.refresh()
        key = stdscr.getch()

    main(stdscr)

def initScoreBoard(stdscr):
    stdscr.clear()
    h,w = stdscr.getmaxyx()
    f = open("SCOREBOARD.json",)
    try:
        json_data = json.load(f)
    except:
        txt="THE SCOREBOARD IS EMPTY"
        stdscr.addstr(h//2,w//2 - len(txt)//2,txt)
        stdscr.refresh()
        time.sleep(1.5)
        main(stdscr)

    key = 0
    while key!=curses.KEY_ENTER and key not in [10,13]:
        stdscr.clear()
        row = 2
        for idx,x in enumerate(json_data):
            stdscr.addstr(row , 0 ,x)
            row+=1
            for idx2,y in enumerate(json_data[x]):
                text = "    Result: "+str(json_data[x][idx2]["result"]) +"\n    Date: "+ str(json_data[x][idx2]["date"])
                stdscr.addstr(row, 0 ,text)
                row+=3
        stdscr.addstr(0, 0, "PRESS RETURN TO GO BACK")
        stdscr.refresh()
        key = stdscr.getch()

    main(stdscr)

def roll():
    max = 7
    result = ["","",""]
    for x in range(3):
        tmp = random.randint(1,max)
        if tmp == 1:
            result[x]="!"
        elif tmp == 2:
            result[x]="?"
        elif tmp == 3:
            result[x]="#"
        elif tmp == 4:
            result[x]="@"
        elif tmp == 5:
            result[x]="%"
        elif tmp == 6:
            result[x]="&"
        elif tmp == 7:
            result[x]="$"

    return result

def rollFX(stdscr,result):
    h , w = stdscr.getmaxyx()
    loadEfect = ["-","\\","|","/"]*3
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

    stdscr.addstr(0,0,"PRESS Q TO EXIT")
    if result[0]==result[1] and result[1]==result[2]:
        text = " $  $  $  *YOU WIN*  $  $  $"
        x = w//2 - len(text)/2
        stdscr.addstr(y+3,x,text)
    else:
        text = "SORRY... PRESS ENTER TO TRY AGAIN"
        x = w//2 - len(text)/2
        stdscr.addstr(y+3,x,text)

    stdscr.addstr(h -1,0,"PRESS S TO SAVE SCORE")
    stdscr.refresh()
    
def saveScore(stdscr,result):
    stdscr.clear()
    h , w = stdscr.getmaxyx()
    title= "WRITE YOUR NAME"
    xt = w//2 - len(title)//2
    stdscr.addstr(2,xt,title)
    stdscr.refresh()
    name = ""
    key= stdscr.getch()
    while key != curses.KEY_ENTER and key not in [10,13]:
        stdscr.clear()
        stdscr.addstr(2,xt,title)
        if key in range(32,126,1):
            name += chr(key)
        elif key ==263:
            name = name[0:len(name)-1]
        x = w//2 - len(name)//2
        stdscr.addstr(4,x,name)
        stdscr.refresh()
        key= stdscr.getch()
    strresult=""
    for x in result:
        strresult+=x
    today = date.today()
    strtoday = today.strftime("%d/%m/%Y")

    f = open("SCOREBOARD.json",)
    try:
        json_data = json.load(f)
        data = {name : [ {"result" : strresult , "date" : strtoday}]}
        json_data.update(data)
        with open('SCOREBOARD.json', 'w') as f:
            json.dump(json_data, f)
    except:
        data = {name : [ {"result" : strresult , "date" : strtoday}]}
        with open('SCOREBOARD.json', 'w') as f:
            json.dump(data, f)

    stdscr.clear()
    text = "SAVING SCORE"
    y= h//2
    x= w//2 - len(text)//2
    stdscr.addstr(y,x,text)
    stdscr.refresh()
    time.sleep(1)

    main(stdscr)


def initPlay(stdscr):
    stdscr.clear()
    result = roll()
    rollFX(stdscr,result)
    key = stdscr.getch()
    while key != curses.KEY_ENTER and key not in [10,13] and chr(key)!='s' and chr(key)!='q':
        key = stdscr.getch()
    
    if key == curses.KEY_ENTER or key in [10,13]:
        initPlay(stdscr)
    elif chr(key) == 'q':
        main(stdscr)
    elif chr(key)=='s':
        saveScore(stdscr,result)

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