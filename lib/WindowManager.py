import curses
from Window import InfoWindow, MapWindow, OptionPane


#start and configure curses as needed
_main_win = curses.initscr()
curses.start_color()
curses.noecho()
curses.cbreak()
curses.curs_set(0)
_main_win.nodelay(1)
_main_win.keypad(1)
_main_win.refresh()
curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)

def init():
    """
    init subwindows
    """
    global _info_win, _map_win, _option_pane
    _info_win = InfoWindow(1, 140, 0, 0)
    _map_win = MapWindow(35, 140, 1, 0)
    _option_pane = OptionPane(1, 140, 36, 0, "Pause", "Faster", "Slower", "Exit")


def update(the_map=None):
    """
    updates content of info window and also the map window, if a map is given
    :param the_map: the game map in the current state
    """
    _info_win.update()
    if(the_map):
        _map_win.update(the_map)


def replace_option(option_to_replace, new_option):
    """
    replaces option_to_replace with new_option in the_option pane
    :param option_to_replace: the option to replace
    :param new_option: the new option to take its place
    """
    _option_pane.replace_option(option_to_replace, new_option)


def key_pressed():
    """
    returns the current pressed key
    """
    return _main_win.getch()


def terminate():
    """
    unloads curses
    """
    curses.nocbreak()
    _main_win.keypad(0)
    curses.echo()
    curses.endwin()
