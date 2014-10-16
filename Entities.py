from random import randint, choice


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
    def __init__(self, pos_y, pos_x):
        super(Vegetation, self).__init__(pos_y, pos_x)

        self._lvl = 0
        self._steps_to_reproduce = randint(3, 7)

    def update(self, env):
        self._steps_to_reproduce -= 1
        if self._steps_to_reproduce == 0:
            self._steps_to_reproduce = randint(3, 7)
            return self.reproduce(env)

    @staticmethod
    def reproduce(env):
        pass


class Jungle(Vegetation):
    def __init__(self, pos_y, pos_x):
        super(Jungle, self).__init__(pos_y, pos_x)
        self._token = "ϒ"

        self._movable = False
        self._lvl = 2

        self._anim_token = "Υ"
        self._toggler = True

    def __str__(self):
        if self._toggler:
            self._toggler = not self._toggler
            return self._token
        else:
            self._toggler = not self._toggler
            return self._anim_token

    @staticmethod
    def reproduce(env):
        possible_fields = []
        for row in env:
            for cell in row:
                if isinstance(cell, Empty):
                    possible_fields.append(cell)

        if len(possible_fields) == 0:
            return None

        new_field = choice(possible_fields)

        return Grass(new_field.pos_y, new_field.pos_x)


class Grass(Vegetation):
    def __init__(self, pos_y, pos_x):
        super(Grass, self).__init__(pos_y, pos_x)
        self._token = "ʷ"
        self._movable = False

    @staticmethod
    def reproduce(env):
        possible_fields = []
        for row in env:
            for cell in row:
                if isinstance(cell, Empty):
                    possible_fields.append(cell)

        if len(possible_fields) == 0:
            return None

        new_field = choice(possible_fields)

        return Grass(new_field.pos_y, new_field.pos_x)


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


class HorizLimitUp(Entity):
    def __init__(self, pos_y, pos_x):
        super(HorizLimitUp, self).__init__(pos_y, pos_x)
        self._token = "_"
        self._movable = False


class HorizLimitDown(Entity):
    def __init__(self, pos_y, pos_x):
        super(HorizLimitDown, self).__init__(pos_y, pos_x)
        self._token = "‾"
        self._movable = False


class VertLimit(Entity):
    def __init__(self, pos_y, pos_x):
        super(VertLimit, self).__init__(pos_y, pos_x)
        self._token = "|"
        self._movable = False



available_entities = {
    " ": Empty,
    "ʷ": Grass,
    "ϒ": Jungle,
    "#": Animal,
    "_": HorizLimitUp,
    "‾": HorizLimitDown,
    "|": VertLimit
}