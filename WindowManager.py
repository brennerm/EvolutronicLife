import curses
from Window import Window


class WindowManager(object):

    def __init__(self):
        self._main_win = None
        self._sub_wins = {}

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
        for window in self._sub_wins.values():
            window.clear()

    def update(self):
        """
        updates content of all windows
        """
        for window in self._sub_wins.values():
            window.update()

    def __getitem__(self, key):
        """
        overloading function for the getting [] operator
        enables getting sub windows through WindowManager()["main_window"]
        :param key: key of the window
        :return:
        """
        if not key in self._sub_wins:
            raise IndexError("window " + str(key) + " is not available")
        return self._sub_wins[key]

    def __setitem__(self, key, value):
        """
        overloading function for the setting [] operator
        enables setting sub windows through WindowManager()["main_window"] = main_window
        :param key: key of the  window
        :param value: the actual window
        """
        if not isinstance(value, Window):
            raise TypeError("window has to be of type Window")
        self._sub_wins[key] = value