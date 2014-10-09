import curses


class OptionPane():
    def __init__(self, options, width,  pos_y, pos_x):
        if not isinstance(options, list):
            raise ValueError("options is not of type \"list\"")

        self._options = options
        self._width = width
        self._pos_y = pos_y
        self._pos_x = pos_x

    def return_option_pane_window(self):
        opt_win = curses.newwin(1, self._width, self._pos_y, self._pos_x)
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
        index = 1
        offset = 0
        for option in self._options:
            try:
                opt_win.addstr(0, offset, "F" + str(index), curses.A_BOLD)
                offset += 1 + len(str(index))

                opt_win.addstr(0, offset, option, curses.color_pair(1))
                offset += 1 + len(option) + 1
                index += 1
            except:
                raise Exception("given width is not sufficient for displaying all options")
        return opt_win


