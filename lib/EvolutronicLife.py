import lib.WindowManager as WinMan
import lib.MapManager as MapMan
import lib.globals as global_vars
from lib.KeyListener import KeyListener
from time import sleep, time


def run(map_filename):
    """
    the main game loop
    """
    key_listener = KeyListener()
    key_listener.start()
    MapMan.init(map_filename)

    while not global_vars.quit:
        global_vars.step += 1
        step_start = time()

        MapMan.update()
        WinMan.update(MapMan.token_map())

        if (time() - step_start) < global_vars.step_duration:
            sleep(global_vars.step_duration - (time() - step_start))

        while global_vars.pause and not global_vars.quit:
            sleep(0.01)

    WinMan.deinit_curses()
    key_listener.join()
