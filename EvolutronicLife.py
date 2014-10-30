#!/usr/bin/env python3.4

from WindowManager import WindowManager
from MapManager import MapManager
import curses
from Option_Pane import OptionPane
from time import sleep, time
import maps


class EvolutronicLife(object):

    def __init__(self):
        self._win_manager = WindowManager()
        self._map_manager = MapManager(maps.map_1)

    def run(self):
        """
        the main game loop + some initial configurations
        """

        self._win_manager.init_curses()

        self._win_manager["info_win"] = curses.newwin(1, 140, 0, 0)
        self._win_manager["game_win"] = curses.newwin(35, 140, 1, 0)
        self._win_manager.add_static_sub_win("option_pane",
                                             OptionPane(["Pause", "Faster", "Slower", "Exit"], 140, 36, 0).return_option_pane_window())

        start_time = time()
        step_per_s = 0.5
        step = 0
        keep_running = True
        while keep_running:
            step += 1
            start = time()

            self._win_manager.clear()

            self._win_manager["info_win"].addstr(0, 0,
                                                 "{:5s} {:5.1f}".format('time:', round(time() - start_time, 1))
                                                 + "{:13s} {:4.1f}".format(' steps per s:', round(1 / step_per_s, 1))
                                                 + "{:4s} {:4d}".format(' step:', step))

            self._map_manager.update()
            self._map_manager.draw_map(self._win_manager["game_win"])

            self._win_manager.update()

            c = self._win_manager.main_win.getch()

            if c == 265:
                while True:
                    c = self._win_manager.main_win.getch()
                    if c == 265:
                        break
                    if c == 268:
                        keep_running = False
            if c == 266:
                step_per_s = round(step_per_s - 0.1, 1)
                if step_per_s <= 0:
                    step_per_s = 0.1
            if c == 267:
                step_per_s = round(step_per_s + 0.1, 1)
                if step_per_s > 2:
                    step_per_s = 2
            if c == 268:
                keep_running = False

            if time() - start < step_per_s:
                sleep(step_per_s - (time() - start))

        self._win_manager.deinit_curses()

        return 0

if __name__ == "__main__":
    EvolutronicLife().run()
