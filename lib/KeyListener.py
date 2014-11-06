#!/usr/bin/env python3.4

from threading import Thread
from time import sleep, time


class KeyListener(Thread):

    def __init__(self, window):
        Thread.__init__(self)
        self._window = window
        self.step_speed = 0.5
        self.keep_running = True

    #@property
    def run(self):
        while self.keep_running:

            c = self._window.getch()

            if c == 265:
                while True:
                    c = self._window.getch()
                    if c == 265:
                        break
                    if c == 268:
                        self.keep_running = False
            if c == 266:
                self.step_speed = round(self.step_speed - 0.1, 1)
                if self.step_speed <= 0:
                    self.step_speed = 0.1
            if c == 267:
                self.step_speed = round(self.step_speed + 0.1, 1)
                if self.step_speed > 2:
                    self.step_speed = 2
            if c == 268:
                #global keep_running
                self.keep_running = False
                with open("log", "a") as f:
                    f.write(str(self.keep_running))

            sleep(0.01)

        return 0
