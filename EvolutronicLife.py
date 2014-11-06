#!/usr/bin/env python3.4

from Window import Window, OptionPane
from WindowManager import WindowManager
import KeyListener
from MapManager import MapManager
import curses
from time import sleep, time
import maps


class EvolutronicLife(object):

    def __init__(self):
        self._win_manager = WindowManager()
        self._win_manager.init_curses()
        #self._key_listener = KeyListener.KeyListener(self._win_manager.main_win)
        self._map_manager = MapManager(maps.map_1)

    @property
    def run(self):
        """
        the main game loop + some initial configurations
        """
        self._win_manager["info_win"] = Window(1, 140, 0, 0)
        self._win_manager["game_win"] = Window(35, 140, 1, 0)
        self._win_manager["option_pane"] = OptionPane(["Pause", "Faster", "Slower", "Exit"], 140, 36, 0)

        win =self._win_manager.main_win
        key_listener = KeyListener.KeyListener(win)
        key_listener.start()

        step = 0
        start_time = time()
        while KeyListener.keep_running:

            step += 1
            start = time()
            self._win_manager.clear()
            self._win_manager["info_win"].curses_window.addstr(0, 0,
            "{:5s} {:5.1f}".format('time:', round(time() - start_time, 1))
            + "{:13s} {:4.1f}".format(' steps per s:', round(1 / KeyListener.step_speed, 1))
            + "{:4s} {:4d}".format(' step:', step))
            self._map_manager.update()
            self._map_manager.draw_map(self._win_manager["game_win"].curses_window)
            self._win_manager.update()

            if time() - start < KeyListener.step_speed:
                sleep(KeyListener.step_speed - (time() - start))

        self._win_manager.deinit_curses()
        key_listener.join()
        return 0

if __name__ == "__main__":
    EvolutronicLife().run


