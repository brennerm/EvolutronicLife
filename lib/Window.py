import curses
from time import time


class Window(object):
    def __init__(self, height, width, pos_y, pos_x):
        self._curses_window = curses.newwin(height, width, pos_y, pos_x)

    @property
    def curses_window(self):
        return self._curses_window

    def clear(self):
        self._curses_window.clear()

    def update(self):
        self._curses_window.refresh()


class InfoWindow(Window):

    def update(self, start_time, sec_per_step, step):
        self._curses_window.addstr(0, 0,
            "{:5s} {:5.1f}".format('time:', round(time() - start_time, 1))
            + "{:13s} {:4.1f}".format(' steps per s:', round(1 / sec_per_step, 1))
            + "{:4s} {:4d}".format(' step:', step)
        )
        self._curses_window.refresh()


class OptionPane(Window):
    def __init__(self, options, width,  pos_y, pos_x):
        if not isinstance(options, list):
            raise ValueError('options is not of type "list"')

        super(OptionPane, self).__init__(1, width, pos_y, pos_x)

        self._options = options
        self._width = width

    def update(self):
        index = 1
        offset = 0

        for option in self._options:
            try:
                self._curses_window.addstr(0, offset, "F" + str(index), curses.A_BOLD)
                offset += 1 + len(str(index))

                self._curses_window.addstr(0, offset, option, curses.color_pair(1))
                offset += 1 + len(option) + 1
                index += 1
            except:
                raise Exception("given width is not sufficient for displaying all options")

        self._curses_window.refresh()

    def replace_option(self, old_option, new_option):

        i = 0
        for option in list(self._options):

            if option == old_option:
                self._options[i] = new_option
                return
            i += 1

        raise ValueError("option " + old_option + " is not in option pane")