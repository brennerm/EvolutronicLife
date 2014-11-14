#!/usr/bin/env python3.4

from lib.Window import Window, OptionPane
from lib.WindowManager import WindowManager
from lib.KeyListener import KeyListener
from lib.MapManager import MapManager
from time import sleep, time


class EvolutronicLife(object):

    def __init__(self, map_filename):
        self._win_manager = WindowManager()
        self._win_manager.init_curses()
        self._map_manager = MapManager(map_filename)

    def run(self):
        """
        the main game loop + some initial configurations
        """

        self._win_manager.init_curses()

        self._win_manager["info_win"] = Window(1, 140, 0, 0)
        self._win_manager["game_win"] = Window(35, 140, 1, 0)
        self._win_manager["option_pane"] = OptionPane(["Pause", "Faster", "Slower", "Exit"], 140, 36, 0)

        key_listener = KeyListener(self._win_manager)
        key_listener.start()

        step = 0
        start_time = time()
        while not key_listener.quit:
            step += 1
            start = time()

            self._win_manager.clear()

            self._win_manager["info_win"].curses_window.addstr(0, 0,
                                                               "{:5s} {:5.1f}".format('time:', round(time() - start_time, 1))
                                                               + "{:13s} {:4.1f}".format(' steps per s:', round(1 / key_listener.step_speed, 1))
                                                               + "{:4s} {:4d}".format(' step:', step))

            self._map_manager.update()
            self._map_manager.draw_map(self._win_manager["game_win"].curses_window)

            self._win_manager.update()

            if (time() - start) < key_listener.step_speed:
                sleep(key_listener.step_speed - (time() - start))

            while key_listener.pause and not key_listener.quit:
                sleep(0.01)

        self._win_manager.deinit_curses()
        key_listener.join()
        return 0
