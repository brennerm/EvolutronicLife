import curses


#creating window of full size
main_win = curses.initscr()

#enabling the use of colored output
curses.start_color()
#check if colors are supported
if curses.has_colors():
    main_win.addstr(1, 0, "colors are supported")
else:
    main_win.addstr(1, 0, "colors are not supported")
#disable echoing of keys
curses.noecho()
#enabling input keys without pressing enter
curses.cbreak()
#enabling curses to provide key presses directly
main_win.keypad(1)

curses.init_pair(1, curses.COLOR_RED, curses.COLOR_YELLOW)
curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLUE)

main_win.addstr(0, 0, "main window")
main_win.refresh()

#creating window of specific size
begin_x = 20
begin_y = 7
height = 9
width = 40

sub_win = curses.newwin(height, width, begin_y, begin_x)
sub_win.addstr(0, 0, "sub window\n")
sub_win.addstr(1, 0, "normal text")
sub_win.addstr(2, 0, "bold text", curses.A_BOLD)
sub_win.addstr(3, 0, "underline text", curses.A_UNDERLINE)
sub_win.addstr(4, 0, "dim text", curses.A_DIM)
sub_win.addstr(5, 0, "reverse text", curses.A_REVERSE)
sub_win.addstr(6, 0, "standout text", curses.A_STANDOUT)
sub_win.addstr(7, 0, "colored text", curses.color_pair(1))
sub_win.addstr(8, 0, "hit SPACE to exit")

sub_win.refresh()

while 1:
    c = main_win.getch()
    main_win.addstr(2, 0, "key " + str(c) + " pressed")

    #stop loop when SPACE is pressed
    if c == 32:
        break

#end curses application
curses.nocbreak()
main_win.keypad(0)

curses.echo()
curses.endwin()