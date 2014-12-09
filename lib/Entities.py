# -*- coding: utf-8 -*-
from random import random, randint, choice
from math import sqrt, floor
import globals as global_vars


class Entity(object):
    def __init__(self, tile=None):
        if tile: self._associate_tile(tile)


    @property
    def tile(self):
        return self._tile

    @property
    def pos_y(self):
        """
        Return this Entity's y position by returning the y position of
        the associated tile.
        :return: the associated tile's y position
        """
        return self._tile.pos_y

    @property
    def pos_x(self):
        """
        Return this Entity's x position by returning the x position of
        the associated tile.
        :return: the associated tile's x position
        """
        return self._tile.pos_x

    @property
    def blocks_step(self):
        """
        Returns whether this Entity blocks land animals from stepping onto
        the associated tile.
        :return: True if the associated tile can be stepped upon by
        LandAnimals, False otherwise
        """
        return self._blocks_step

    @property
    def pos(self):
        return self.pos_y, self.pos_x

    @property
    def info(self):
        info = [
            "name: " + self.__class__.__name__,
            "token: " + str(self)
        ]
        return info


    def _associate_tile(self, new_tile):
        """
        Pushes this Entity on the given tile and sets reference to the tile.
        :param new_tile: the tile to associate the Entity with
        """
        self._tile = new_tile
        new_tile.push_entity(self)


    def __str__(self):
        return self._token



class Limit(Entity):
    def __init__(self, tile=None):
        super().__init__(tile)
        self._blocks_step = -1



class HorizLimitTop(Limit):
    def __init__(self, tile):
        super().__init__(tile)
        self._token = "_"



class HorizLimitBottom(Limit):
    def __init__(self, tile):
        super().__init__(tile)
        self._token = "‾"



class VertLimit(Limit):
    def __init__(self, tile):
        super().__init__(tile)
        self._token = "|"



class Water(Limit): #inherits from limit so land animals won't step onto water
    def __init__(self, tile):
        super().__init__(tile)
        self._tokens = "~∽"


    def try_spawning(self):
        """
        Tries to spawn a new Protozoan. has a certain percentage of a chance
        to succeed. Also, its tile shall not already hold a Protozoan.
        :return: a new instance of Protozoan or None
        """
        if random() < 0.01 and not self._tile.holds_entity(Protozoan):
            return Protozoan(self._tile)

    def __str__(self):
        return self._tokens[global_vars.anim_toggler]



class Beach(Entity):
    def __init__(self, tile):
        super().__init__(tile)
        self._token = ":"
        self._blocks_step = 3



class Creature(Entity):
    def __init__(self, tile):
        super().__init__(tile)


    def die(self):
        """
        Kills this Creature by popping it from the corresponding tile's
        entity stack and returning it for destruction.
        :return: this Creature
        """
        self._tile.pop_entity(self)
        if global_vars.watched_entity == self:
            global_vars.watched_entity = None
        return self



class RainForest(Creature):
    def __init__(self, tile):
        super().__init__(tile)
        self._tokens = 'Ϋϔ'
        self._blocks_step = -1
        self._steps_to_reproduce = randint(15, 20)


    @property
    def lvl(self):
        return 2


    def wants_to_grow(self):
        """
        Reports whether this RainForest is ready to grow.
        :return: True if RainForest wants to grow, False otherwise
        """
        self._steps_to_reproduce -= 1
        if self._steps_to_reproduce == 0:
            self._steps_to_reproduce = randint(15, 20)
            return True
        return False


    def try_growth(self):
        """
        Lets this Vegetation try to grow. If it grows, the new offspring will
        be returned by this method.
        :return: a new level 0 Vegetation instance or None
        """
        env = self._tile.env_rings[0]
        free_tiles = [tile for tile in env if tile.empty()]
        if free_tiles:       #reproduce if plant has space
            return Vegetation(0, choice(free_tiles))


    def __str__(self):
        return self._tokens[global_vars.anim_toggler]



class Vegetation(RainForest):
    def __init__(self, lvl, tile=None):
        super().__init__(tile)
        self._tokens = ("ʷʬY", "ʷʬϒ")
        self._lvl = lvl
        self._chance_to_evolve = 1
        self._nutrition = 5
        self._blocks_step = 3
        self._health = 5


    @property
    def lvl(self):
        return self._lvl


    @property
    def nutrition(self):
        return self._nutrition

    @property
    def info(self):
        info = [
            "name: " + self.__class__.__name__,
            "token: " + str(self),
            "health: " + str(self._health)
        ]
        return info

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, new_health):
        self._health = new_health


    def try_growth(self):
        """
        Lets this Vegetation try to grow. growing could be either producing
        a new offspring or rising in level. In the former case, the
        new offspring will be returned by this method.
        :return: a new level 0 Vegetation instance or None
        """
        env = self._tile.env_rings[0]
        offspring = super().try_growth()
        if offspring:
            return offspring
        self._evolve()    #try to rise in lvl when not reproducing


    def _evolve(self):
        """
        Lets this Vegetation try to evolve. Must not succeed.
        """
        env = self._tile.env_rings[0]
        if self._lvl == 2:
            return
        if self._chance_to_evolve < randint(0, 100):
            self._chance_to_evolve += 1
            return
        if all(
            tile.holds_entity(RainForest) and tile.entity().lvl >= self._lvl or
            tile.holds_entity(Limit) for tile in env):

            self._lvl = min(self._lvl + 1, 2)
            self._nutrition = min(self.nutrition + 5, 15)
            self._blocks_step = max(self._blocks_step - 1, 1)
            self._health = min(self._health + 5, 15)


    def devolve(self):
        """
        Lets this Vegetation drop in level if health is in a certain range.
        """
        if 0 < self._health <= 5:
            self.__init__(0)
        elif 5 < self._health <= 10:
            self.__init__(1)


    def __str__(self):
        return self._tokens[global_vars.anim_toggler][self._lvl]



class Animal(Creature):
    def __init__(self, tile):
        super().__init__(tile)
        self._blocks_step = -1


    def _step_on_tile(self, new_tile):
        """
        Lets this Animal move from its old tile to a new tile.
        :param new_tile: The new tile to step onto
        """
        self._tile.pop_entity(self)
        self._associate_tile(new_tile)



class Protozoan(Animal):
    def __init__(self, tile):
        super().__init__(tile)
        self._time_to_live = 20
        self._token = '§'


    @property
    def info(self):
        info = [
            "name: " + self.__class__.__name__,
            "token: " + str(self),
            "ttl: " + str(self._time_to_live)
        ]
        return info


    def beach_reachable(self):
        """
        Returns whether an adjacent Beach entity can be seen.
        :return: True if an adjacent tile can be walked upon, False otherwise
        """
        env = self._tile.env_rings[0]
        self._beach_tiles = [tile for tile in env if tile.walkable()]
        return True if self._beach_tiles else False


    def jump_on_beach(self):
        """
        Lets this Protozoan move onto the beach and transform itself into
        a SmallHerbivore or SmallCarnivore.
        :return: tuple containing old Protozoan entity and new LandAnimal entity
        """
        if random() <= 0.8:
            new_animal = SmallHerbivore(
                choice(self._beach_tiles), rdy_to_copulate=True
            )    #fresh herbies can reproduce right away
        else:
            new_animal = SmallCarnivore(
                choice(self._beach_tiles), energy=3
            )
        return self.die(), new_animal


    def move(self):
        """
        Lets this Protozoan move on a random tile holding only Water. Death
        is possible if this Protozoan runs out of lifetime.
        :return: this Protozoan if it has died, None otherwise
        """
        env = self._tile.env_rings[0]

        self._time_to_live -= 1
        if not self._time_to_live:
            return self.die()

        swimmable_tiles = [
            tile for tile in env if isinstance(tile.entity(), Water)
        ]
        if swimmable_tiles:
            self._step_on_tile(choice(swimmable_tiles))



class LandAnimal(Animal):
    def __init__(self, tile):
        super().__init__(tile)
        self._lvl = 0
        self._rdy_to_copulate = False


    @property
    def lvl(self):
        return self._lvl

    @property
    def view_range(self):
        return self._view_range

    @property
    def info(self):
        info = [
            "name: " + self.__class__.__name__,
            "token: " + str(self),
            "ttl: " + str(self._time_to_live),
            "food: " + str(self._food),
            "energy: " + str(self._energy),
            "rdy_to_copulate: " + str(self._rdy_to_copulate)
        ]
        return info


    def life_over(self):
        self._time_to_live -= 1
        return not self._time_to_live


    def is_hungry(self):
        return not self._food


    def is_horny(self):
        return self._rdy_to_copulate


    def have_sex(self):
        self._rdy_to_copulate = False


    def search_for_target(self, target_entity, lvl=None):
        """
        Lets this LandAnimal search for entities of class target_entity. This
        can be used for searching food or a mating partner. In the former case,
        no level argument should be passed so the method detects the nearest
        food entity. In the latter case, a level should be passed because a
        partner should be of the same level. Returns a Tile if an entity was
        found and the best way isn't blocked.
        :param target_entity: class of searched entity
        :param lvl: the level of the searched entity (makes sense for mating
        partners)
        :return: best Tile for proceeding, or None if this Tile is not walkable
        or no target could be found
        """
        for env in self._tile.env_rings[1:self.view_range]:
            possible_targets = [
                tile.entity(target_entity, lvl) for tile in env
                if tile.holds_entity(target_entity, lvl)
            ]
            if possible_targets:
                break
        else: return    #stop when no target could be found

        if lvl is None:
            highest_target_lvl = max(possible_targets, key=lambda t: t.lvl).lvl
            wanted_target = choice(tuple(
                filter(lambda t: t.lvl == highest_target_lvl, possible_targets)
            ))   #pick the highest level entity of the found targets
        else:
            wanted_target = choice(possible_targets)

        immediate_env = self._tile.env_rings[0]
        step_position = self._calculate_step(wanted_target)
        target_tile = immediate_env[step_position]

        if target_tile.walkable(self.lvl):
            return target_tile


    def _calculate_step(self, wanted_target):
        """
        Calculates step position in the immediate environment based on the
        position of the wanted target.
        :param wanted_target: the target entity to move towards
        :return: one of these positions in the immediate environment:
                    [0][1][2]
                    [3][x][4]
                    [5][6][7]
        """
        x_dir = ((wanted_target.pos_x > self.pos_x) -       #signum
                (wanted_target.pos_x < self.pos_x))
        y_dir = ((wanted_target.pos_y > self.pos_y) -
                (wanted_target.pos_y < self.pos_y))
        if y_dir == -1:
            if x_dir == -1: return 0
            if x_dir == 0:  return 1
            if x_dir == 1:  return 2
        elif y_dir == 0:
            if x_dir == -1: return 3
            if x_dir == 1:  return 4
        elif y_dir == 1:
            if x_dir == -1: return 5
            if x_dir == 0:  return 6
            if x_dir == 1:  return 7


    def move(self):
        """
        If this LandAnimal can see a suitable target (food or mating partner)
        in its looking environment, it tries to move in its direction. If no
        target could be found, it tries to move on a walkable tile of the
        immediate environment. Moving consumes 1 food, or 1 energy if this
        LandAnimal has run out of food. Running out of food also triggers
        non-readyness for reproduction.
        :return: True if this LandAnimal was able to move, False otherwise
        """
        target_tile = None
        immediate_env = self._tile.env_rings[0]

        if self.is_hungry():
            target_tile = self.search_for_target(self._prey_class)
        elif self.is_horny():
            target_tile = self.search_for_target(self.__class__, self._lvl)

        if not target_tile:     #no target entity found:
            walkable_tiles = [  #choose any free surrounding tile
                tile for tile in immediate_env if tile.walkable(self.lvl)
            ]
            if walkable_tiles:
                target_tile = choice(walkable_tiles)
            else:               #no free surrounding tile: abort
                return False

        self._step_on_tile(target_tile)
        if self._food:
            self._food -= 1
        else:
            self._energy -= 1
            self._rdy_to_copulate = False

        return True


    def hunger_game(self):
        """
        Lets this LandAnimal try to eat a prey Creature. This must not succeed.
        If it succeeds, food, energy and libido levels will be filled up and
        the eaten Creature will be returned for destruction. This LandAnimal
        may just eat a part of a prey Creature, in which case True is returned.
        The searching LandAnimal may also die if it has run out of energy and
        couldn't find any prey. In this case, the LandAnimal itself will be
        returned for destruction.
        :return: a deceased instance of a Creature if a whole Creature died,
        True if part of a Creature was eaten,
        None if none of the above occured
        """
        env = self._tile.env_rings[0]
        eatable_prey = [
            tile.entity(self._prey_class) for tile in env
            if tile.holds_entity(self._prey_class)
        ]

        if eatable_prey:
            prey = choice(eatable_prey)
            self._food += prey.nutrition
            self._energy = min(10, self._energy + 1)
            self._rdy_to_copulate = True
            prey.health -= self._attack
            if prey.health <= 0:
                return prey.die()
            else:
                if isinstance(prey, Vegetation) and prey.lvl > 0:
                    prey.devolve()  #plants can shrink
                return True
        elif not self._energy:
            return self.die()


    def try_reproduction(self):
        """
        Lets this LandAnimal try to reproduce with a partner. If a partner can
        be found on the surrounding tiles, a new level LandAnimal will be
        created and 1 food consumed. This new LandAnimal will be placed on any
        walkable surrounding tile. Reproduction fails if no walkable tile can
        be found. On success, the new LandAnimal will be returned.
        :return: new instance of a LandAnimal
        """
        env = self._tile.env_rings[0]
        mating_partners = [
            tile.entity(self.__class__, self._lvl) for tile in env
            if tile.holds_entity(self.__class__, self._lvl)
        ]
        mating_partners = [
            mate for mate in mating_partners
            if mate.is_horny() and mate != self
        ]

        if mating_partners:
            birthplaces = [tile for tile in env if tile.walkable(self.lvl)]
            if not birthplaces: return
            partner = choice(mating_partners)
            partner.have_sex()
            self._rdy_to_copulate = False
            self._food -= 1
            if random() < 0.5:
                return self._evolved_class(choice(birthplaces))
            else:
                return self.__class__(choice(birthplaces))


    def __str__(self):
        return self._tokens[self._lvl]



class Herbivore(LandAnimal):
    def __init__(self, tile):
        super().__init__(tile)
        self._tokens = 'җҖӜ'
        self._prey_class = Vegetation
        self._nutrition = None

    @property
    def nutrition(self):
        return self._nutrition

    @property
    def info(self):
        info = [
            "name: " + self.__class__.__name__,
            "token: " + str(self),
            "ttl: " + str(self._time_to_live),
            "food: " + str(self._food),
            "energy: " + str(self._energy),
            "health: " + str(self._health),
            "rdy_to_copulate: " + str(self._rdy_to_copulate)
        ]
        return info

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, new_health):
        self._health = new_health



class SmallHerbivore(Herbivore):
    def __init__(self, tile, rdy_to_copulate = False):
        super().__init__(tile)
        self._rdy_to_copulate = rdy_to_copulate
        self._lvl = 0
        self._time_to_live = 50
        self._food = 10
        self._energy = 10
        self._evolved_class = BigHerbivore
        self._view_range = 4
        self._nutrition = 5
        self._health = 5
        self._attack = 5


class BigHerbivore(SmallHerbivore):
    def __init__(self, tile):
        super().__init__(tile)
        self._lvl = 1
        self._time_to_live = 100
        self._food = 10
        self._energy = 20
        self._evolved_class = SmartHerbivore
        self._view_range = 6
        self._nutrition = 6
        self._health = 10
        self._attack = 10


class SmartHerbivore(BigHerbivore):
    def __init__(self, tile):
        super().__init__(tile)
        self._lvl = 2
        self._time_to_live = 150
        self._food = 10
        self._energy = 30
        self._evolved_class = SmartHerbivore
        self._view_range = 8
        self._nutrition = 8
        self._health = 15
        self._attack = 15


class Carnivore(LandAnimal):
    def __init__(self, tile):
        super().__init__(tile)
        self._tokens = 'ԅԇʡ'
        self._prey_class = Herbivore


class SmallCarnivore(Carnivore):
    def __init__(self, tile, energy=5):
        super().__init__(tile)
        self._lvl = 0
        self._time_to_live = 50
        self._food = 10
        self._energy = energy
        self._evolved_class = BigCarnivore
        self._view_range = 4
        self._attack = 5

class BigCarnivore(SmallCarnivore):
    def __init__(self, tile):
        super().__init__(tile)
        self._lvl = 1
        self._time_to_live = 100
        self._food = 10
        self._energy = 7
        self._evolved_class = SmartCarnivore
        self._view_range = 6
        self._attack = 10

class SmartCarnivore(BigCarnivore):
    def __init__(self, tile):
        super().__init__(tile)
        self._lvl = 2
        self._time_to_live = 150
        self._food = 10
        self._energy = 10
        self._evolved_class = SmartCarnivore
        self._view_range = 8
        self._attack = 15
