from random import random, randint, choice
from BaseEntities import *
import globals as global_vars



class Vegetation(Entity):
    def __init__(self, lvl, tile):
        super().__init__(tile)

        self._tokens = ("ʷʬY", "ʷʬϒ")
        self._lvl = lvl
        self._steps_to_reproduce = randint(10, 15)
        self._chance_to_evolve = 1


    def __str__(self):
        return self._tokens[global_vars.anim_toggler][self._lvl]


    @property
    def lvl(self):
        return self._lvl


    def wants_to_grow(self):
        """
        reports whether this plant is ready to grow
        :return: true if plant wants to grow, false otherwise
        """
        self._steps_to_reproduce -= 1
        if self._steps_to_reproduce == 0:
            self._steps_to_reproduce = randint(10, 15)
            return True
        return False


    def try_growth(self, env):
        """
        lets this plant try to grow. growing could be either producing
        a new offspring or rising in level. in the former case, the
        new offspring will be returned by this method.
        :param env: the surrounding tiles of this plant
        :return: a new level 0 Vegetation instance or None
        """
        free_tiles = [tile for row in env for tile in row if tile.empty()]
        if free_tiles:       #reproduce if plant has space
            return Vegetation(0, choice(free_tiles))
        self._evolve(env)    #try to rise in lvl when not reproducing


    def _evolve(self, env):
        """
        lets this plant try to evolve. must not succeed.
        :param env: the surrounding tiles of this plant
        """
        if self._lvl == 2:
            return
        if self._chance_to_evolve < randint(0, 100):
            self._chance_to_evolve += 1
            return
        if all(
            tile.holds_entity(Vegetation) and tile.entity().lvl >= self._lvl or
            tile.holds_entity(Limit) for row in env for tile in row):

            self._lvl = min(self._lvl + 1, 2)



class Animal(Entity):
    def __init__(self, tile):
        super().__init__(tile)
        self._time_to_live = 50
        self._food = 10
        self._energy = 10
        self._lvl = 0
        self._rdy_to_copulate = False
        self._blocks_step = True


    @property
    def lvl(self):
        return self._lvl


    def life_over(self):
        self._time_to_live -= 1
        return not self._time_to_live


    def is_hungry(self):
        return not self._food


    def is_horny(self):
        return self._rdy_to_copulate


    def have_sex(self):
        self._rdy_to_copulate = False


    def move(self, env):
        """
        lets this animal move in a random direction, if there are free tiles.
        moving consumes 1 food, or 1 energy if this animal has run out of
        food. running out of food also triggers non-readyness for reproduction
        :param env: the surrounding tiles of this animal
        """
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
        self._food = 10



class SmallHerbivore(Herbivore):
    def __init__(self, tile):
        super().__init__(tile)
        self._lvl = 0
        self._time_to_live = 50
        self._energy = 10
        self._evolved = BigHerbivore


    def hunger_game(self, env):
        """
        lets this animal try to eat a plant of the same level. this must not
        succeed. if it succeeds, food, energy and libido levels will be filled
        up and the eaten plant will be returned for destruction. this animal
        may also die at this point if it has run out of energy and couldn't
        find any food. in this case, the animal itself will be returned for
        destruction.
        :param env: the surrounding tiles of this animal
        :return: a deceased instance of Animal/Vegetation or None
        """
        eatable_plants = [
            tile.entity(Vegetation, self._lvl) for row in env for tile in row
            if tile.holds_entity(Vegetation, self._lvl)
        ]
        if eatable_plants:
            self._food = 10
            self._energy = 10
            self._rdy_to_copulate = True
            return choice(eatable_plants).die()
        elif not self._energy:
            return self.die()


    def try_reproduction(self, env):
        """
        lets this animal try to reproduce with a partner. if a partner can be
        found on the surrounding tiles, a new level 0 animal will be created
        and 1 food consumed. this new animal will be placed on any walkable
        surrounding tile, or on the parent's tile, if there is none. the new
        animal will be returned.
        :param env: the surrounding tiles of this animal
        :return: new instance of a level 0 herbivore
        """
        mating_partners = [
            tile.entity(Herbivore, self._lvl) for row in env for tile in row
            if tile.holds_entity(Herbivore, self._lvl) and tile != self._tile
        ]
        mating_partners = [
            mate for mate in mating_partners if mate.is_horny()
        ]

        if mating_partners:
            birthplaces = [
                tile for row in env for tile in row if tile.walkable()
            ]
            if not birthplaces: return
            partner = choice(mating_partners)
            partner.have_sex()
            self._rdy_to_copulate = False
            self._food -= 1
            child_class = self._evolved if random() < 0.5 else self.__class__
            return child_class(choice(birthplaces))



class BigHerbivore(SmallHerbivore):
    def __init__(self, tile):
        super().__init__(tile)
        self._lvl = 1
        self._time_to_live = 100
        self._energy = 20
        self._evolved = SmartHerbivore


    def move(self, env):
        """
        lets this animal move in a random direction, if there are free tiles.
        moving consumes 1 food, or 1 energy if this animal has run out of
        food. running out of food also triggers non-readyness for reproduction
        :param env: the surrounding tiles of this animal
        """
        walkable_tiles = [
            tile for row in env for tile in row if tile.walkable()
        ]
        plant_tiles = [
            tile for tile in walkable_tiles if tile.holds_entity(Vegetation)
        ]
        food_tiles = [
            tile for tile in plant_tiles if tile.entity().lvl == self._lvl
        ]
        if food_tiles:
            new_tile = choice(food_tiles)
        elif plant_tiles:
            new_tile = choice(plant_tiles)
        elif walkable_tiles:
            new_tile = choice(walkable_tiles)
        else: return

        self._tile.pop_entity(self)
        self._associate_tile(new_tile)
        if self._food:
            self._food -= 1
        else:
            self._energy -= 1
            self._rdy_to_copulate = False



class SmartHerbivore(BigHerbivore):
    def __init__(self, tile):
        super().__init__(tile)
        self._lvl = 2
        self._time_to_live = 150
        self._energy = 30
        self._evolved = SmartHerbivore



class Carnivore(Animal):
    def __init__(self, tile):
        super().__init__(tile)
        self._tokens = 'ԅԇԆ'


    def hunger_game(self, env):
        """
        lets this animal try to eat a herbivore animal of the same or
        lower level. this must not succeed. if it succeeds, food, energy
        and libido levels will be filled up and the eaten animal will be
        returned for destruction. The searching animal may also die
        at this point if it has run out of energy and couldn't find any prey.
        In this case, the animal itself will be returned for
        destruction.
        :param env: the surrounding tiles of this animal
        :return: a deceased instance of Animal or None
        """
        eatable_prey = [
            tile.entity(Herbivore) for row in env for tile in row
            if tile.holds_entity(Herbivore)
        ]
        if eatable_prey:
            self._food = 10
            self._energy = 10
            self._rdy_to_copulate = True
            return choice(eatable_prey).die()
        elif not self._energy:
            return self.die()


    def try_reproduction(self, env):
        """
        lets this animal try to reproduce with a partner. if a partner can be
        found on the surrounding tiles, a new level 0 animal will be created
        and 1 food consumed. this new animal will be placed on any walkable
        surrounding tile, or on the parent's tile, if there is none. the new
        animal will be returned.
        :param env: the surrounding tiles of this animal
        :return: new instance of a level 0 Carnivore
        """
        mating_partners = [
            tile.entity(Carnivore, self._lvl) for row in env for tile in row
            if tile.holds_entity(Carnivore, self._lvl)
        ]
        mating_partners = [
            mate for mate in mating_partners
            if mate.is_horny() and mate != self
        ]

        if mating_partners:
            birthplaces = [
                tile for row in env for tile in row if tile.walkable()
            ]
            if not birthplaces: return
            partner = choice(mating_partners)
            partner.have_sex()
            self._rdy_to_copulate = False
            self._food -= 1
            return Carnivore(choice(birthplaces))
