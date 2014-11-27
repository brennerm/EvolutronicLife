from threading import Thread
from time import sleep
import WindowManager as WinMan
import globals as global_vars
import curses

class KeyListener(Thread):

    def __init__(self):
        Thread.__init__(self)


    def run(self):
        """
        periodically querys the keyboard keypress and acts accordingly in its
        own thread. responds to the following keypresses: F1, F2, F3, F4
        """
        while not global_vars.quit:

            key = WinMan.key_pressed()

            if key == 265:          #F1 / Pause
                global_vars.pause = True
                WinMan.replace_option("Pause", "Resume")
                while True:
                    key = WinMan.key_pressed()
                    if key == 265:      #F1 / Resume (changed at this point)
                        global_vars.pause = False
                        WinMan.replace_option("Resume", "Pause")
                        break
                    elif key == 268:    #F4 / Quit
                        global_vars.quit = True
                        break
                    sleep(0.01)

            elif key == 266:        #F2 / Faster
                global_vars.step_duration = round(
                    global_vars.step_duration - 0.1, 1
                )
                if global_vars.step_duration <= 0:
                    global_vars.step_duration = 0.1
                WinMan.update()

            elif key == 267:        #F3 / Slower
                global_vars.step_duration = round(
                    global_vars.step_duration + 0.1, 1
                )
                if global_vars.step_duration > 2:
                    global_vars.step_duration = 2
                WinMan.update()

            elif key == 268:        #F4 / Quit
                global_vars.quit = True

            elif key == curses.KEY_MOUSE:
                id, x, y, z, bstate = curses.getmouse()

                with open("log", "a") as f:
                    f.write("x: " + str(x) + " y: " + str(y) + "bstate" + str(bstate))

            sleep(0.01)
