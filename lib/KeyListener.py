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

            c = self._win_manager.main_win.getch()

            if c == 265:
                self._pause = True
                self._win_manager["option_pane"].replace_option("Pause", "Resume")
                self._win_manager["option_pane"].clear()
                self._win_manager["option_pane"].update()
                while not self._quit:
                    c = self._win_manager.main_win.getch()
                    if c == 265:
                        self._pause = False
                        self._win_manager["option_pane"].replace_option("Resume", "Pause")
                        break
                    if c == 268:
                        self._quit = True
                    sleep(0.01)
            if c == 266:
                self._step_speed = round(self._step_speed - 0.1, 1)
                if self._step_speed <= 0:
                    self._step_speed = 0.1
            if c == 267:
                self._step_speed = round(self._step_speed + 0.1, 1)
                if self._step_speed > 2:
                    self._step_speed = 2
            if c == 268:
                self._quit = True

            sleep(0.01)

        return 0
