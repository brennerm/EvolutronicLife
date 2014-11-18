#!/usr/bin/env python3.4

from threading import Thread
from time import sleep


class KeyListener(Thread):

    def __init__(self, win_manager):
        Thread.__init__(self)
        self._win_manager = win_manager
        self._step_speed = 0.5
        self._pause = False
        self._quit = False

    @property
    def step_speed(self):
        return self._step_speed

    @property
    def pause(self):
        return self._pause

    @property
    def quit(self):
        return self._quit

    def run(self):
        while not self._quit:

            key = self._win_manager.key_pressed()

            if key == 265:          #F1 / Pause,Resume
                self._pause = True
                self._win_manager.replace_option("Pause", "Resume")
                while not self._quit:
                    key = self._win_manager.key_pressed()
                    if key == 265:
                        self._pause = False
                        self._win_manager.replace_option("Resume", "Pause")
                        break
                    if key == 268:
                        self._quit = True
                    sleep(0.01)
            if key == 266:          #F2 / Faster
                self._step_speed = round(self._step_speed - 0.1, 1)
                if self._step_speed <= 0:
                    self._step_speed = 0.1
            if key == 267:          #F3 / Slower
                self._step_speed = round(self._step_speed + 0.1, 1)
                if self._step_speed > 2:
                    self._step_speed = 2
            if key == 268:          #F4 / Quit
                self._quit = True

            sleep(0.01)

        return 0
