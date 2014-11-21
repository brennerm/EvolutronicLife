from random import randint, choice
import lib.globals as global_vars


class Entity(object):
    def __init__(self, tile):
        self._movable = False
        self._is_limit = False
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

    def _associate_tile(self, new_tile):
        self._tile = new_tile
        new_tile.push_entity(self)



class Vegetation(Entity):
    def __init__(self, lvl, tile):
        super().__init__(tile)

        self._tokens = (("ʷ", "ʬ", "Y"), ("ʷ", "ʬ", "ϒ"))
        self._lvl = lvl
        self._steps_to_reproduce = randint(3, 7)
        self._chance_to_evolve = 1

    def __str__(self):
        return self._tokens[global_vars.anim_toggler][self._lvl]

    @property
    def lvl(self):
        return self._lvl

    def wants_to_grow(self):
        self._steps_to_reproduce -= 1
        if self._steps_to_reproduce == 0:
            self._steps_to_reproduce = randint(3, 7)
            return True
        return False

    def grow(self, env):
        free_tiles = [tile for row in env for tile in row if tile.empty()]
        if len(free_tiles) != 0:     #reproduce if plant has space
            return Vegetation(0, choice(free_tiles))
        self._evolve(env)            #try to rise in lvl when not reproducing

    def _evolve(self, env):
        if self._lvl == 2:
            return
        if self._chance_to_evolve < randint(0, 100):
            self._chance_to_evolve += 1
            return
        if all(
            isinstance(tile.entity, Vegetation) and tile.entity.lvl >= self._lvl or
            tile.entity.is_limit() for row in env for tile in row):

            self._lvl = min(self._lvl + 1, 2)



class Animal(Entity):
    def __init__(self, tile):
        super().__init__(tile)
        self._token = "#"
        self._food = 5
        self._lvl = 0

    def act(self):
        pass

    def move(self, env):
        self._tile.pop_entity(self)
        walkable_tiles = [
            tile for row in env for tile in row if tile.walkable()
        ]
        if walkable_tiles:
            self._associate_tile(choice(walkable_tiles))



class Beach(Entity):
    def __init__(self, tile):
        super().__init__(tile)
        self._token = ":"
        self._is_limit = True


class Water(Entity):
    def __init__(self, tile):
        super().__init__(tile)
        self._tokens = ("~", "∽")
        self._is_limit = True

    def __str__(self):
        return self._tokens[global_vars.anim_toggler]


class Limit(Entity):    #shall only be used as placeholder!
    def __init__(self, tile=None):
        super().__init__(tile)
        self._is_limit = True


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
