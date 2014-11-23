from random import randint, choice
from BaseEntities import *
import globals as global_vars



class Vegetation(Entity):
    def __init__(self, lvl, tile):
        super().__init__(tile)

        self._tokens = ("ʷʬY", "ʷʬϒ")
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
        if free_tiles:       #reproduce if plant has space
            return Vegetation(0, choice(free_tiles))
        self._evolve(env)    #try to rise in lvl when not reproducing

    def _evolve(self, env):
        if self._lvl == 2:
            return
        if self._chance_to_evolve < randint(0, 100):
            self._chance_to_evolve += 1
            return
        if all(
            isinstance(tile.entity(), Vegetation) and tile.entity().lvl >= self._lvl or
            isinstance(tile.entity(), Limit) for row in env for tile in row):

            self._lvl = min(self._lvl + 1, 2)



class Animal(Entity):
    def __init__(self, tile):
        super().__init__(tile)
        self._food = 10
        self._energy = 10
        self._lvl = 0
        self._rdy_to_copulate = False
        self._blocks_step = True

    @property
    def lvl(self):
        return self._lvl

    def is_hungry(self):
        return not self._food

    def is_horny(self):
        return self._rdy_to_copulate

    def have_sex(self):
        self._rdy_to_copulate = False

    def move(self, env):
        walkable_tiles = [
            tile for row in env for tile in row if tile.walkable()
        ]
        if walkable_tiles:
            self._tile.pop_entity(self)
            self._associate_tile(choice(walkable_tiles))
        if self._food:
            self._food -= 1
        else:
            self._energy -= 1
            self._rdy_to_copulate = False

    def __str__(self):
        return self._tokens[self._lvl]



class Herbivore(Animal):
    def __init__(self, tile):
        super().__init__(tile)
        self._tokens = 'җҖӜ'

    def hunger_game(self, env):
        eatable_plants = [
            tile.entity(Vegetation, self._lvl) for row in env for tile in row
            if tile.holds_entity(Vegetation, self._lvl)
        ]
        if eatable_plants:
            self._food = 10
            self._energy = 10
            self._rdy_to_copulate = True
            return choice(eatable_plants)._die()
        elif not self._energy:
            return self._die()

    def try_reproduction(self, env):
        mating_partners = [
            tile.entity(Herbivore, self._lvl) for row in env for tile in row
            if tile.holds_entity(Herbivore, self._lvl)
        ]
        mating_partners = [
            mate for mate in mating_partners
            if mate.is_horny() and mate != self
        ]

        if mating_partners:
            partner = choice(mating_partners)
            self._rdy_to_copulate = False
            self._food -= 1
            partner.have_sex()
            birthplaces = [
                tile for row in env for tile in row if tile.walkable()
            ]
            tile = choice(birthplaces) if birthplaces else self._tile
            return Herbivore(tile)