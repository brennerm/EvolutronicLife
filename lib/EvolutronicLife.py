import atexit
from time import sleep, time
from InputListener import InputListener
import WindowManager as WinMan
import MapManager as MapMan
import globals as global_vars


def run(map_filename, starting_step):
    """
    the main game loop. runs until user hits quit button (F4)
    """
    atexit.register(WinMan.terminate)

    input_listener = InputListener()
    input_listener.start()
    MapMan.init_map(map_filename)

    while not global_vars.quit:
        global_vars.step += 1
        step_start = time()

        MapMan.update()

        if global_vars.hidden_run:
            if global_vars.step >= starting_step:
                WinMan.init()
                global_vars.hidden_run = False
            else:
                WinMan.progress_info(starting_step)

        else:
            WinMan.update(MapMan.token_map(), MapMan.watch_info())

            current_time = time()
            if (current_time - step_start) < global_vars.step_duration:
                sleep(global_vars.step_duration - (current_time - step_start))

            while global_vars.pause and not global_vars.quit:
                if global_vars.single_step:
                    global_vars.single_step = False
                    break
                sleep(0.01)

    input_listener.join()
