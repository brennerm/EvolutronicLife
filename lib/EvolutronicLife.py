#!/usr/bin/env python3.4

from lib.WindowManager import WindowManager
from lib.KeyListener import KeyListener
from lib.MapManager import MapManager
from time import sleep, time
import lib.globals as global_vars


class EvolutronicLife(object):

    def __init__(self, map_filename):
        self._win_manager = WindowManager()
        self._map_manager = MapManager(map_filename)
        self._key_listener = KeyListener(self._win_manager)


    def run(self):
        """
        the main game loop
        """
        self._key_listener.start()

        while not global_vars.quit:
            global_vars.step += 1
            step_start = time()

            self._map_manager.update()
            self._win_manager.update(self._map_manager.map)

            if (time() - step_start) < global_vars.step_duration:
                sleep(global_vars.step_duration - (time() - step_start))

            while global_vars.pause and not global_vars.quit:
                sleep(0.01)

        self._win_manager.deinit_curses()
        self._key_listener.join()
