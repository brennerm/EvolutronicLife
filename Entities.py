from random import randint


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


class Grass(Entity):
    def __init__(self, pos_y, pos_x):
        super(Grass, self).__init__(pos_y, pos_x)
        self._token = "*"
        self._movable = False


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
            return " "


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
            return " "


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



available_entities = {
    " ": Empty,
    "*": Grass,
    "#": Animal,
    ":": Beach,
    "~": Water,
    "∽": AlterWater,
    "_": HorizLimitTop,
    "‾": HorizLimitBottom,
    "|": VertLimit
}