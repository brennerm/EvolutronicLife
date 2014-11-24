import atexit
from time import sleep, time
from KeyListener import KeyListener
import WindowManager as WinMan
import MapManager as MapMan
import globals as global_vars


def run(map_filename, starting_step):
    """
    the main game loop. runs until user hits quit button (F4)
    """
    atexit.register(WinMan.terminate)

    key_listener = KeyListener()
    key_listener.start()
    MapMan.init_map(map_filename)

    #print('Generating...')

    visual_run = False
    while not global_vars.quit:
        global_vars.step += 1
        step_start = time()

        MapMan.update()

        if not visual_run:
            if global_vars.step >= starting_step:
                WinMan.init()
                visual_run = True
            else:
                WinMan.progress_info(starting_step)

        if visual_run:
            WinMan.update(MapMan.token_map())

            if (time() - step_start) < global_vars.step_duration:
                sleep(global_vars.step_duration - (time() - step_start))

            while global_vars.pause and not global_vars.quit:
                sleep(0.01)

    key_listener.join()
