#!/usr/bin/env python3.4

from lib.WindowManager import WindowManager
from lib.KeyListener import KeyListener
from lib.MapManager import MapManager
from time import sleep, time


class EvolutronicLife(object):

    def __init__(self, map_filename):
        self._win_manager = WindowManager()
        self._map_manager = MapManager(map_filename)
        self._key_listener = KeyListener(self._win_manager)


    def run(self):
        """
        the main game loop
        """
        start_time = time()
        step = 0

        self._key_listener.start()

        while not self._key_listener.quit:
            step += 1
            start = time()

            self._map_manager.update()
            self._win_manager.update(
                self._map_manager.map, start_time,
                self._key_listener.step_duration, step
            )

            if (time() - start) < self._key_listener.step_duration:
                sleep(self._key_listener.step_duration - (time() - start))

            while self._key_listener.pause and not self._key_listener.quit:
                sleep(0.01)

        self._win_manager.deinit_curses()
        self._key_listener.join()
