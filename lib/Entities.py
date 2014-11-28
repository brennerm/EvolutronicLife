from random import random, randint, choice
from math import sqrt, floor
import globals as global_vars


class Entity(object):
    def __init__(self, tile):
        if tile: self._associate_tile(tile)


    def __str__(self):
        return self._token


    @property
    def pos_y(self):
        """
        return this Entity's y position by returning the y position of
        the associated tile.
        :return: the associated tile's y position
        """
        return self._tile.pos_y


    @property
    def pos_x(self):
        """
        return this Entity's x position by returning the x position of
        the associated tile.
        :return: the associated tile's x position
        """
        return self._tile.pos_x


    @property
    def blocks_step(self):
        """
        returns whether this Entity blocks land animals from stepping onto
        the associated tile.
        :return: True if the associated tile can be stepped upon by
        LandAnimals, False otherwise
        """
        return self._blocks_step


    def _associate_tile(self, new_tile):
        """
        pushes this Entity on the given tile and sets reference to the tile
        :param new_tile: the tile to associate the Entity with
        """
        self._tile = new_tile
        new_tile.push_entity(self)

    @property
    def tile(self):
        return self._tile


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
    def __init__(self,tile):
        super().__init__(tile)
        self._token = "|"



class Water(Limit): #inherits from limit so land animals won't step onto water
    def __init__(self, tile):
        super().__init__(tile)
        self._tokens = "~∽"


    def try_spawning(self):
        """
        tries to spawn a new Protozoan. has a certain percentage of a chance
        to succeed. also, its tile shall not already hold a Protozoan.
        :param env: the surrounding tiles of this Water entity
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
        kills this Creature by popping it from the corresponding tile's
        entity stack and returning it for destruction
        :return: this Creature
        """
        self._tile.pop_entity(self)
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
        reports whether this RainForest is ready to grow
        :return: True if RainForest wants to grow, False otherwise
        """
        self._steps_to_reproduce -= 1
        if self._steps_to_reproduce == 0:
            self._steps_to_reproduce = randint(15, 20)
            return True
        return False


    def try_growth(self):
        """
        lets this Vegetation try to grow. if it grows, the
        new offspring will be returned by this method.
        :param env: the surrounding tiles of this Vegetation
        :return: a new level 0 Vegetation instance or None
        """
        env = self.tile.env_rings[0]
        free_tiles = [tile for tile in env if tile.empty()]
        if free_tiles:       #reproduce if plant has space
            return Vegetation(0, choice(free_tiles))


    def __str__(self):
        return self._tokens[global_vars.anim_toggler]



class Vegetation(RainForest):
    def __init__(self, lvl, tile):
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


    def try_growth(self):
        """
        lets this Vegetation try to grow. growing could be either producing
        a new offspring or rising in level. in the former case, the
        new offspring will be returned by this method.
        :param env: the surrounding tiles of this Vegetation
        :return: a new level 0 Vegetation instance or None
        """
        env = self.tile.env_rings[0]
        offspring = super().try_growth()
        if offspring:
            return offspring
        self._evolve()    #try to rise in lvl when not reproducing


    def _evolve(self):
        """
        lets this Vegetation try to evolve. must not succeed.
        :param env: the surrounding tiles of this Vegetation
        """
        env = self.tile.env_rings[0]
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
            self._health = min(self._health * 2, 20)


    def __str__(self):
        return self._tokens[global_vars.anim_toggler][self._lvl]



class Animal(Creature):
    def __init__(self, tile):
        super().__init__(tile)
        self._blocks_step = -1



class Protozoan(Animal):
    def __init__(self, tile):
        super().__init__(tile)
        self._time_to_live = 20
        self._token = '§'


    def beach_reachable(self):
        """
        returns whether an adjacent Beach entity can be seen.
        :param env: the surrounding tiles of this Protozoan
        :return: True if an adjacent tile holds a free Beach entity,
        False otherwise
        """
        env = self.tile.env_rings[0]
        self._beach_tiles = [tile for tile in env if tile.walkable()]
        return True if self._beach_tiles else False


    def jump_on_beach(self):
        """
        lets this Protozoan move onto the beach and transform itself into
        a SmallHerbivore or SmallCarnivore.
        :return: tuple containing old Protozoan entity and new LandAnimal
        entity
        """
        if random() <= 0.8:
            new_animal = SmallHerbivore(choice(self._beach_tiles))
        else:
            new_animal = SmallCarnivore(choice(self._beach_tiles))
        return self.die(), new_animal


    def move(self):
        """
        lets this Protozoan move on a random tile holding only Water. death
        is possible if this protozoan runs out of lifetime.
        :param env: the surrounding tiles of this Protozoan
        :return: this Protozoan if it has died, None otherwise
        """
        env = self.tile.env_rings[0]
        self._tile.pop_entity(self)

        self._time_to_live -= 1
        if not self._time_to_live:
            return self

        swimmable_tiles = [
            tile for tile in env if isinstance(tile.entity(), Water)
        ]
        if swimmable_tiles:
            self._associate_tile(choice(swimmable_tiles))



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


    def life_over(self):
        self._time_to_live -= 1
        return not self._time_to_live


    def is_hungry(self):
        return not self._food


    def is_horny(self):
        return self._rdy_to_copulate


    def have_sex(self):
        self._rdy_to_copulate = False


    def search_for_target(self, target_entity):
        """
        Lets this LandAnimal search for other entities. This can be
        used for the search for food or a mating partner. Returns a tile
        if a entity is in looking range and the best way isn't blocked.
        :param env: field of view of the animal
        :param target_entity: class of searched entity
        :return: best tile for proceeding if no blocked
        """
        possible_targets = None
        for env in self.tile.env_rings[1:self.view_range]:
            possible_targets = [
                tile.entity(target_entity, self._lvl) for tile in env
                if tile.holds_entity(target_entity, self._lvl) and
                tile.entity(target_entity, self._lvl) != self
            ]
            if possible_targets:
                break

        if possible_targets:
            wanted_target = choice(possible_targets)

            x_dir = (wanted_target.pos_x > self.pos_x) - (wanted_target.pos_x < self.pos_x) # signum
            y_dir = (wanted_target.pos_y > self.pos_y) - (wanted_target.pos_y < self.pos_y)
            if y_dir == -1:
                if x_dir == -1:
                    pos=0
                if x_dir == 0:
                    pos=1
                if x_dir == 1:
                    pos=2
            elif y_dir == 0:
                if x_dir == -1:
                    pos=3
                if x_dir == 1:
                    pos=4
            elif y_dir == 1:
                if x_dir == -1:
                    pos=5
                if x_dir == 0:
                    pos=6
                if x_dir == 1:
                    pos=7

            env = self.tile.env_rings[0]
            move_target = env[pos]
            if move_target.walkable(self.lvl):
                return move_target


    def move(self):
        """
        if this LandAnimal can see a suitable target (food or mating partner)
        in its looking environment, it tries to move in its direction. if no
        target can be found, it tries to move on a walkable tile of the
        immediate environment. moving consumes 1 food, or 1 energy if this
        LandAnimal has run out of food. running out of food also triggers
        non-readyness for reproduction.
        :param immediate_env: the surrounding tiles of this LandAnimal of
        distance 1
        :param looking_env: the surrounding tiles of this LandAnimal of a
        distance >= 1
        :return: True if this LandAnimal was able to move, False otherwise
        """
        target_tile = None
        immediate_env = self.tile.env_rings[0]

        if self.is_hungry():
            target_tile = self.search_for_target(
                target_entity=self._prey_class
            )
        elif self.is_horny():
            target_tile = self.search_for_target(
                target_entity=self.__class__
            )

        if not target_tile:     #no target entity found:
            walkable_tiles = [  #choose any free surrounding tile
                tile for tile in immediate_env if tile.walkable(self.lvl)
            ]
            if walkable_tiles:
                target_tile = choice(walkable_tiles)
            else:               #no free surrounding tile: abort
                return False

        self._tile.pop_entity(self)
        self._associate_tile(target_tile)
        if self._food:
            self._food -= 1
        else:
            self._energy -= 1
            self._rdy_to_copulate = False

        return True

    def hunger_game(self):
        """
        lets this LandAnimal try to eat a prey Creature of the same
        level. this must not succeed. if it succeeds, food, energy
        and libido levels will be filled up and the eaten Creature will be
        returned for destruction. The searching LandAnimal may also die
        at this point if it has run out of energy and couldn't find any prey.
        In this case, the LandAnimal itself will be returned for destruction.
        :param env: the surrounding tiles of this LandAnimal
        :return: a deceased instance of LandAnimal or None
        """
        env =  self._tile.env_rings[0]
        eatable_prey = [
            tile.entity(self._prey_class) for tile in env
            if tile.holds_entity(self._prey_class)
        ]

        # eatable_prey = [
        #     entity for entity in eatable_prey
        #     if entity.lvl <= self.lvl
        # ]

        if eatable_prey:
            prey = choice(eatable_prey)
            self._food += prey.nutrition
            self._energy = 10
            self._rdy_to_copulate = True
            prey._health -= self._attack
            if prey._health <= 0:
                return prey.die()
            else:
                return True
        elif not self._energy:
            return self.die()


    def try_reproduction(self):
        """
        lets this LandAnimal try to reproduce with a partner. if a partner can
        be found on the surrounding tiles, a new level LandAnimal will be
        created and 1 food consumed. this new LandAnimal will be placed on any
        walkable surrounding tile. reproduction fails if no walkable tile can
        be found. on success, the new LandAnimal will be returned.
        :param env: the surrounding tiles of this LandAnimal
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



class SmallHerbivore(Herbivore):
    def __init__(self, tile):
        super().__init__(tile)
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
        self._attack = 20

class Carnivore(LandAnimal):
    def __init__(self, tile):
        super().__init__(tile)
        self._tokens = 'ԅԇʡ'
        self._prey_class = Herbivore



class SmallCarnivore(Carnivore):
    def __init__(self, tile):
        super().__init__(tile)
        self._lvl = 0
        self._time_to_live = 50
        self._food = 10
        self._energy = 10
        self._evolved_class = BigCarnivore
        self._view_range = 4
        self._attack = 5


class BigCarnivore(SmallCarnivore):
    def __init__(self, tile):
        super().__init__(tile)
        self._lvl = 1
        self._time_to_live = 100
        self._food = 10
        self._energy = 20
        self._evolved_class = SmartCarnivore
        self._view_range = 6
        self._attack = 10


class SmartCarnivore(BigCarnivore):
    def __init__(self, tile):
        super().__init__(tile)
        self._lvl = 2
        self._time_to_live = 150
        self._food = 10
        self._energy = 30
        self._evolved_class = SmartCarnivore
        self._view_range = 8
        self._attack = 15