from lib.WindowManager import WindowManager
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

        while keep_running:
            step += 1
            start = time()

            self._map_manager.update()
            self._win_manager.update(
                self._map_manager.map, start_time, sec_per_step, step
            )

            c = self.getch()

            if c == 265:        #F1 / Pause
                while True:
                    c = self.getch()
                    if c == 265:
                        break
                    if c == 268:
                        keep_running = False
                        break
            elif c == 266:      #F2 / Faster
                sec_per_step = round(sec_per_step - 0.1, 1)
                if sec_per_step <= 0:
                    sec_per_step = 0.1
            elif c == 267:      #F3 / Slower
                sec_per_step = round(sec_per_step + 0.1, 1)
                if sec_per_step > 2:
                    sec_per_step = 2
            elif c == 268:      #F4 / Exit
                keep_running = False

            if time() - start < sec_per_step:
                sleep(sec_per_step - (time() - start))

        self._win_manager.deinit_curses()

        return 0


    def getch(self):
        return self._win_manager.getch()