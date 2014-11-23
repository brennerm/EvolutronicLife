import globals as global_vars


class Entity(object):
    def __init__(self, tile):
        self._movable = False
        self._blocks_step = False
        if tile:
            self._associate_tile(tile)


    def __str__(self):
        return self._token

    @property
    def pos_y(self):
        return self._tile.pos_y

    @property
    def pos_x(self):
        return self._tile.pos_x

    def is_limit(self):
        return self._is_limit

    def blocks_step(self):
        return self._blocks_step

    def _associate_tile(self, new_tile):
        self._tile = new_tile
        new_tile.push_entity(self)

    def _die(self):
        self._tile.pop_entity(self)
        return self



class Beach(Entity):
    def __init__(self, tile):
        super().__init__(tile)
        self._token = ":"
        self._blocks_step = True


class Water(Entity):
    def __init__(self, tile):
        super().__init__(tile)
        self._tokens = "~∽"
        self._blocks_step = True

    def __str__(self):
        return self._tokens[global_vars.anim_toggler]


class Limit(Entity): #shall only be directly initialised as placeholder!
    def __init__(self, tile=None):
        super().__init__(tile)
        self._blocks_step = True


class HorizLimitTop(Limit):
    def __init__(self, tile):
        super().__init__(tile)
        self._token = "_"


class HorizLimitBottom(Limit):
    def __init__(self, tile):
        super().__init__(tile)
        self._token = "‾"


class VertLimit(Limit):
    def __init__(self,tile):
        super().__init__(tile)
        self._token = "|"
