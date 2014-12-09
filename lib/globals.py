# -*- coding: utf-8 -*-
step_duration = 0.5
step = 0
pause = False
quit = False
anim_toggler = False
watched_entity = None
single_step = False
hidden_run = True
swap_step_duration = None
h_starved = 0
h_trampled = 0
h_eaten = 0
h_age = 0
c_starved = 0
c_trampled = 0
c_age = 0

WHITE_ON_BLACK = 0
WHITE_ON_BLUE = 1
BLUE_ON_BLACK = 2
RED_ON_BLACK = 3
GREEN_ON_BLACK = 4
YELLOW_ON_BLACK = 5
CYAN_ON_BLACK = 6
MAGENTA_ON_BLACK = 7
WHITE_ON_CYAN = 8
MAGENTA_ON_CYAN = 9

color = {
    '~': WHITE_ON_CYAN,
    '∽': WHITE_ON_CYAN,
    '§': MAGENTA_ON_CYAN,
    'ʷ': GREEN_ON_BLACK,
    'ʬ': GREEN_ON_BLACK,
    'ϒ': GREEN_ON_BLACK,
    'Y': GREEN_ON_BLACK,
    'ԅ': RED_ON_BLACK,
    'ԇ': RED_ON_BLACK,
    'ʡ': RED_ON_BLACK,
    'җ': YELLOW_ON_BLACK,
    'Җ': YELLOW_ON_BLACK,
    'Ӝ': YELLOW_ON_BLACK,
    ':': YELLOW_ON_BLACK,
    'Ϋ': GREEN_ON_BLACK,
    'ϔ': GREEN_ON_BLACK
}
