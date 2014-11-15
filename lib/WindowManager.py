import curses
from lib.Window import *


class WindowManager(object):

    def __init__(self):
        self.init_curses()
        self.info_win = InfoWindow(1, 140, 0, 0)
        self.game_win = Window(35, 140, 1, 0)
        self.option_pane = OptionPane(["Pause", "Faster", "Slower", "Exit"], 140, 36, 0)


    @property
    def main_win(self):
        return self._main_win

    def init_curses(self):
        """
        starts and configures curses as needed
        """
        self._main_win = curses.initscr()
        curses.start_color()
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        self._main_win.nodelay(1)
        self._main_win.keypad(1)
        self._main_win.refresh()

        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)

    def deinit_curses(self):
        """
        unloads curses
        """
        curses.nocbreak()
        self._main_win.keypad(0)
        curses.echo()
        curses.endwin()

    def clear(self):
        """
        clears content of all windows
        """
        self.info_win.clear()
        self.game_win.clear()
        self.option_pane.clear()

    def update(self, start_time, sec_per_step, step):
        """
        updates content of all windows
        """
        self.info_win.update(start_time, sec_per_step, step)
        self.game_win.update()
        self.option_pane.update()