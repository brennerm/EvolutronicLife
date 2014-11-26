from random import random, randint, choice
import globals as global_vars


class Entity(object):
    def __init__(self, tile):
        if tile: self._associate_tile(tile)


    def __str__(self):
        return self._token


    @property
    def pos_y(self):
        """
        return this entitie's y position by returning the y position of
        the associated tile.
        :return: the associated tile's y position
        """
        return self._tile.pos_y


    @property
    def pos_x(self):
        """
        return this entitie's x position by returning the x position of
        the associated tile.
        :return: the associated tile's x position
        """
        return self._tile.pos_x


    @property
    def blocks_step(self):
        """
        returns whether this entity blocks land animals from stepping onto
        the associated tile.
        :return: True if the associated tile can be stepped upon^by land
        animals, False otherwise
        """
        return self._blocks_step


    def _associate_tile(self, new_tile):
        """
        pushes this entity on the given tile and sets reference to the tile
        :param new_tile: the tile to associate the entity with
        """
        self._tile = new_tile
        new_tile.push_entity(self)



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


    def try_spawning(self, env):
        """
        tries to spawn a new Protozoan. has a certain percentage of a chance
        to succeed. also, its tile should be free.
        :param env: the surrounding tiles of this water entity
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
        self._blocks_step = False



class Creature(Entity):
    def __init__(self, tile):
        super().__init__(tile)


    def die(self):
        """
        kills this creature by popping it from the corresponding tile's
        creature stack and returning it for destruction
        :return: this creature
        """
        self._tile.pop_entity(self)
        return self



class Vegetation(Creature):
    def __init__(self, lvl, tile):
        super().__init__(tile)

        self._tokens = ("ʷʬY", "ʷʬϒ")
        self._blocks_step = False
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



class Animal(Creature):
    def __init__(self, tile):
        super().__init__(tile)
        self._blocks_step = True



class Protozoan(Animal):
    def __init__(self, tile):
        super().__init__(tile)
        self._time_to_live = 20
        self._token = '§'


    def beach_reachable(self, env):
        """
        returns whether an adjacent beach entity can be seen.
        :param env: the surrounding tiles of this protozoan
        :return: True if an adjacent tile holds a free beach entity,
        False otherwise
        """
        self._beach_tiles = [
            tile for row in env for tile in row if tile.walkable()
        ]
        return True if self._beach_tiles else False


    def jump_on_beach(self):
        """
        lets this protozoan move onto the beach and transform itself into
        a land animal, which can be either Herbivore or Carnivore.
        :return: tuple containing old Protozoan entity and new Animal entity
        """
        if random() <= 0.8:
            new_animal = SmallHerbivore(choice(self._beach_tiles))
        else:
            new_animal = Carnivore(choice(self._beach_tiles))
        return self.die(), new_animal


    def move(self, env):
        """
        lets this protozoan move on a random tile holding only Water. death
        is possible if this protozoan ran out of lifetime.
        :param env: the surrounding tiles of this protozoan
        :return: this Protozoan if it has died, None otherwise
        """
        self._tile.pop_entity(self)

        self._time_to_live -= 1
        if not self._time_to_live:
            return self

        swimmable_tiles = [
            tile for row in env for tile in row
            if isinstance(tile.entity(), Water)
        ]
        if swimmable_tiles:
            self._associate_tile(choice(swimmable_tiles))



class LandAnimal(Animal):
    def __init__(self, tile):
        super().__init__(tile)
        self._time_to_live = 50
        self._food = 10
        self._energy = 10
        self._lvl = 0
        self._rdy_to_copulate = False


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



class Herbivore(LandAnimal):
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



class Carnivore(LandAnimal):
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
