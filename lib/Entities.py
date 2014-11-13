from random import randint, choice
import globals


class Entity(object):
    def __init__(self, pos_y, pos_x):
        self._pos_y = pos_y
        self._pos_x = pos_x
        self._movable = False

        self._token = ""

    def __str__(self):
        return self._token

    @property
    def is_movable(self):
        return self._movable

    @property
    def pos_y(self):
        return self._pos_y

    @property
    def pos_x(self):
        return self._pos_x


class Empty(Entity):
    def __init__(self, pos_y, pos_x):
        super(Empty, self).__init__(pos_y, pos_x)
        self._token = " "
        self._movable = False


class Vegetation(Entity):
    def __init__(self, lvl, pos_y, pos_x):
        super(Vegetation, self).__init__(pos_y, pos_x)

        self._tokens = ["ʷ", "ʬ", "Y"]
        self._anim_tokens = ["ʷ", "ʬ", "ϒ"]

        self._lvl = min(lvl, 2)
        self._steps_to_reproduce = randint(3, 7)
        self.chance_to_evolve = 1

    def __str__(self):
        if globals.anim_toggler:
            return self._tokens[self._lvl]
        else:
            return self._anim_tokens[self._lvl]

    @property
    def lvl(self):
        return self._lvl

    def update(self, map_manager):
        self._steps_to_reproduce -= 1
        if self._steps_to_reproduce == 0:
            self._steps_to_reproduce = randint(3, 7)
            return self.reproduce(map_manager)

    def reproduce(self, map_manager):
        env = map_manager.get_env(self.pos_y, self.pos_x, 1)

        possible_fields = []
        for row in env:
            for cell in row:
                if isinstance(cell, Empty):
                    possible_fields.append(cell)

        if len(possible_fields) == 0:
            return self.evolve(env)

        new_field = choice(possible_fields)

        return Vegetation(0, new_field.pos_y, new_field.pos_x)

    def evolve(self, env):
        if self._lvl == 2:
            return None
        rand_int = randint(0, 100)
        if self.chance_to_evolve < rand_int:
            self.chance_to_evolve += 1
            return None

        if all(isinstance(cell, Vegetation) and cell.lvl >= max(self._lvl, 0) for row in env for cell in row):
            return Vegetation(self._lvl + 1, self.pos_y, self.pos_x)


class Animal(Entity):
    def __init__(self, pos_y, pos_x):
        super(Animal, self).__init__(pos_y, pos_x)
        self._token = "#"
        self._movable = True

        self._food = 5
        self._lvl = 0

    def move(self):
        dir_x = randint(-1, 1)
        dir_y = randint(-1, 1)

        self._pos_y += dir_y
        self._pos_x += dir_x


class Beach(Entity):
    def __init__(self, pos_y, pos_x):
        super(Beach, self).__init__(pos_y, pos_x)
        self._token = ":"
        self._movable = False


class Water(Entity):
    def __init__(self, pos_y, pos_x):
        super(Water, self).__init__(pos_y, pos_x)
        self._token = "~"
        self._movable = False

        self._toggler = False

    def __str__(self):
        self._toggler = not self._toggler

        if self._toggler:
            return self._token
        else:
            return "∽"


class AlterWater(Entity):
    def __init__(self, pos_y, pos_x):
        super(AlterWater, self).__init__(pos_y, pos_x)
        self._token = "~"
        self._movable = False

        self._toggler = True

    def __str__(self):

        self._toggler = not self._toggler

        if self._toggler:
            return self._token
        else:
            return "∽"


class HorizLimitTop(Entity):
    def __init__(self, pos_y, pos_x):
        super(HorizLimitTop, self).__init__(pos_y, pos_x)
        self._token = "_"
        self._movable = False


class HorizLimitBottom(Entity):
    def __init__(self, pos_y, pos_x):
        super(HorizLimitBottom, self).__init__(pos_y, pos_x)
        self._token = "‾"
        self._movable = False


class VertLimit(Entity):
    def __init__(self, pos_y, pos_x):
        super(VertLimit, self).__init__(pos_y, pos_x)
        self._token = "|"
        self._movable = False
