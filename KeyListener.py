#!/usr/bin/env python3.4

from threading import Thread
from time import sleep, time

step_speed = 0.5
keep_running = True


class KeyListener(Thread):

    def __init__(self, window):
        Thread.__init__(self)
        self._window = window

    #@property
    def run(self):

        global step_speed
        global keep_running

        while keep_running:

            c = self._window.getch()

            if c == 265:
                while True:
                    c = self._window.getch()
                    if c == 265:
                        break
                    if c == 268:
                        keep_running = False
            if c == 266:
                step_speed = round(step_speed - 0.1, 1)
                if step_speed <= 0:
                    step_speed = 0.1
            if c == 267:
                step_speed = round(step_speed + 0.1, 1)
                if step_speed > 2:
                    step_speed = 2
            if c == 268:
                #global keep_running
                keep_running = False
                with open("log", "a") as f:
                    f.write(str(keep_running))

            sleep(0.01)

        return 0
