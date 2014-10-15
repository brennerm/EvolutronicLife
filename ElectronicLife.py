#!/usr/bin/env python3.4

from WindowManager import WindowManager
from MapManager import MapManager
import curses
from Option_Pane import OptionPane
from time import sleep, time
import maps


class ElectronicLife(object):

    def __init__(self):
        self._win_manager = WindowManager()
        self._map_manager = MapManager(maps.map_1)

    def run(self):

        self._win_manager.init_curses()

        self._win_manager["info_win"] = curses.newwin(1, 140, 0, 0)
        self._win_manager["game_win"] = curses.newwin(35, 140, 1, 0)
        self._win_manager.add_static_sub_win("option_pane",
                                             OptionPane(["Pause", "Faster", "Slower", "Exit"], 140, 36, 0).return_option_pane_window())

        step = 0.5
        keep_running = True
        while keep_running:

            start = time()

            self._win_manager.clear()
            #self._win_manager["game_win"].addstr(0, 0, 4759*"-")
            #self._win_manager["game_win"].insstr(33, 0, "-")

            self._win_manager["info_win"].addstr(0, 0, "time: " + str(time())
                                                 + " steps per s: " + str(round(1/step, 1)))
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
                step = round(step - 0.1, 1)
                if step <= 0:
                    step = 0.1
            if c == 267:
                step = round(step + 0.1, 1)
                if step > 2:
                    step = 2
            if c == 268:
                keep_running = False

            if time() - start < step:
                sleep(step - (time() - start))

        self._win_manager.deinit_curses()

        return 0

if __name__ == "__main__":
    ElectronicLife().run()
