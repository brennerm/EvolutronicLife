import curses
from lib.Window import InfoWindow, MapWindow, OptionPane


class WindowManager(object):

    def __init__(self):
        self.init_curses()
        self._info_win = InfoWindow(1, 140, 0, 0)
        self._map_win = MapWindow(35, 140, 1, 0)
        self._option_pane = OptionPane(
            1, 140, 36, 0, "Pause", "Faster", "Slower", "Exit"
        )


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

    def update(self, the_map, start_time, sec_per_step, step):
        """
        updates content of all windows
        :param the_map: the game map in the current state
        :param start_time: the time of the game start
        :param sec_per_step: duration of a step in seconds
        :param step: the number of the current step
        """
        self._info_win.update(start_time, sec_per_step, step)
        self._map_win.update(the_map)
        self._option_pane.update()

    def replace_option(self, option_to_replace, new_option):
        """
        replaces option_to_replace with new_option in the_option pane
        :param option_to_replace: the option to replace
        :param new_option: the new option to take its place
        """
        self._option_pane.replace_option(option_to_replace, new_option)

    def key_pressed(self):
        """
        returns the current pressed key
        """
        return self._main_win.getch()