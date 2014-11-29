import curses
from time import time
import globals as global_vars


class Window(object):
    def __init__(self, height, width, pos_y, pos_x):
        self._curses_window = curses.newwin(height, width, pos_y, pos_x)



class InfoWindow(Window):
    def __init__(self, height, width, pos_y, pos_x):
        super().__init__(height, width, pos_y, pos_x)
        self.simulation_start = time()


    def update(self):
        """
        puts updated information into info window
        """
        self._curses_window.clear()

        self._curses_window.addstr(0, 0,
            "{:5s} {:5.1f}".format(
                'time:', round(time() - self.simulation_start, 1)
            )
            + "\t{:13s} {:4.1f}".format(
                ' steps per s:', round(1 / global_vars.step_duration, 1)
            )
            + "\t{:4s} {:4d}".format(' step:', global_vars.step)
			+ "\t{:4s} {:4d}".format(' eaten:', global_vars.eaten)
			+ "\t{:4s} {:4d}".format(' starved:', global_vars.starved)
			+ "\t{:4s} {:4d}".format(' trampled:', global_vars.trampled)
            + "\t{:4s} {:4d}".format(' natural death:', global_vars.age)
        )

        self._curses_window.noutrefresh()



class MapWindow(Window):

    def update(self, the_map, highlight_pos):
        """
        draws map onto map window
        :param the_map: the current game map
        """
        self._curses_window.clear()

        for i, row in enumerate(the_map):
            for j, cell in enumerate(row):
                try:
                    self._curses_window.addstr(i, j, cell, curses.color_pair(global_vars.color.get(cell, 0)))
                except curses.error:
                    pass    #curses throws error @ adding last element of last row

        if not highlight_pos is None:
            self._curses_window.chgat(highlight_pos[0], highlight_pos[1], 1, curses.A_STANDOUT)

        self._curses_window.noutrefresh()



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

        self._curses_window.noutrefresh()


    def replace_option(self, option_to_replace, new_option):
        """
        replaces option_to_replace with new_option
        :param option_to_replace: the option to replace
        :param new_option: the new option to take its place
        """
        self._options[self._options.index(option_to_replace)] = new_option
        self.update()



class TileWindow(Window):
    def __init__(self, height, width,  pos_y, pos_x):
        super(TileWindow, self).__init__(height, width, pos_y, pos_x)
        self.update()

    def update(self, tile_info=None):
        self._curses_window.clear()

        if not tile_info is None:
            for x, entity_info in enumerate(tile_info):
                for y, line in enumerate(entity_info):
                    self._curses_window.addstr(y, x * 30, line + "\n")

        self._curses_window.noutrefresh()
