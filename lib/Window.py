import curses
from time import time


class Window(object):
    def __init__(self, height, width, pos_y, pos_x):
        self._curses_window = curses.newwin(height, width, pos_y, pos_x)



class InfoWindow(Window):

    def update(self, start_time, sec_per_step, step):
        """
        puts updated information into info window
        :param start_time: time of simulation start in secs
        :param sec_per_step: length of one step in secs
        :param step: the count of the current step
        """
        self._curses_window.addstr(0, 0,
            "{:5s} {:5.1f}".format('time:', round(time() - start_time, 1))
            + "{:13s} {:4.1f}".format(' steps per s:', round(1 / sec_per_step, 1))
            + "{:4s} {:4d}".format(' step:', step)
        )

        self._curses_window.refresh()



class MapWindow(Window):

    def update(self, the_map):
        """
        draws map onto map window
        :param the_map: the current game map
        """
        for i, row in enumerate(the_map):
            line = "".join(str(cell) for cell in row)
            self._curses_window.addstr(i, 0, line)

        self._curses_window.refresh()



class OptionPane(Window):
    def __init__(self, height, width,  pos_y, pos_x, *options):
        super(OptionPane, self).__init__(height, width, pos_y, pos_x)

        self._options = list(options)
        self._width = width
        self.update()


    def update(self):
        """
        updates the option pane with the current options
        """
        self._curses_window.clear()

        offset = 0
        for i, option in enumerate(self._options, start=1):
            try:
                self._curses_window.addstr(0, offset, "F" + str(i), curses.A_BOLD)
                offset += 1 + len(str(i))

                self._curses_window.addstr(0, offset, option, curses.color_pair(1))
                offset += 1 + len(option) + 1
            except:
                raise Exception("given width is not sufficient for displaying all options")

        self._curses_window.refresh()

    def replace_option(self, option_to_replace, new_option):
        """
        replaces option_to_replace with new_option
        :param option_to_replace: the option to replace
        :param new_option: the new option to take its place
        """
        self._options[self._options.index(option_to_replace)] = new_option
        self.update()
