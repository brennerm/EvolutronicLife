#!/usr/bin/env python3.4

from lib.WindowManager import WindowManager
from lib.KeyListener import KeyListener
from lib.MapManager import MapManager
from time import sleep, time


class EvolutronicLife(object):

    def __init__(self, map_filename):
        self._map_manager = MapManager(map_filename)
        self._win_manager = WindowManager()


    def run(self):
        """
        the main game loop
        """
        start_time = time()
        sec_per_step = 0.5
        step = 0
        keep_running = True

        key_listener = KeyListener(self._win_manager)
        key_listener.start()

        while not key_listener.quit:
            step += 1
            start = time()

            self._map_manager.update()
            self._win_manager.update(
                self._map_manager.map, start_time, sec_per_step, step
            )


            if (time() - start) < key_listener.step_speed:
                sleep(key_listener.step_speed - (time() - start))

            while key_listener.pause and not key_listener.quit:
                sleep(0.01)


        self._win_manager.deinit_curses()
        key_listener.join()
        return 0
