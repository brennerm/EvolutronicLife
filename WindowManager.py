import curses


class WindowManager(object):

    def __init__(self):
        self._main_win = None
        self._sub_wins = {}
        self._static_sub_wins = {}

    @property
    def main_win(self):
        return self._main_win

    def init_curses(self):
        self._main_win = curses.initscr()
        curses.start_color()
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        self._main_win.nodelay(1)
        self._main_win.keypad(1)
        self._main_win.refresh()

    def deinit_curses(self):
        curses.nocbreak()
        self._main_win.keypad(0)
        curses.echo()
        curses.endwin()

    def add_static_sub_win(self, key, value):
        self._static_sub_wins[key] = value
        value.refresh()

    def clear(self):
        for window in self._sub_wins.values():
            window.clear()

    def update(self):
        for window in self._sub_wins.values():
            window.refresh()

    def __getitem__(self, key):
        if not key in self._sub_wins:
            raise IndexError("window " + str(key) + " is not available")
        return self._sub_wins[key]

    def __setitem__(self, key, value):
        self._sub_wins[key] = value