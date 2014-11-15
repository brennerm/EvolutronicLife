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

            key = self.pressed_key()

            if key == 265:        #F1 / Pause
                while True:
                    key = self.pressed_key()
                    if key == 265:
                        break
                    if key == 268:
                        keep_running = False
                        break
            elif key == 266:      #F2 / Faster
                sec_per_step = round(sec_per_step - 0.1, 1)
                if sec_per_step <= 0:
                    sec_per_step = 0.1
            elif key == 267:      #F3 / Slower
                sec_per_step = round(sec_per_step + 0.1, 1)
                if sec_per_step > 2:
                    sec_per_step = 2
            elif key == 268:      #F4 / Exit
                keep_running = False

            if time() - start < sec_per_step:
                sleep(sec_per_step - (time() - start))

        self._win_manager.deinit_curses()

        return 0


    def pressed_key(self):
        return self._win_manager.getch()