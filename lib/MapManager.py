from Tile import Tile
from Entities import *
import globals as global_vars


_entity_dict = {
    "ʷ": Vegetation,
    "ʬ": Vegetation,
    "Y": Vegetation,
    'Ϋ': RainForest,
    'ϔ': RainForest,
    "җ": SmallHerbivore,
    "Җ": BigHerbivore,
    "Ӝ": SmartHerbivore,
    "ԅ": SmallCarnivore,
    "ԇ": BigCarnivore,
    "ʡ": SmartCarnivore,
    "§": Protozoan,
    "~": Water,
    "∽": Water,
    ":": Beach,
    "_": HorizLimitTop,
    "‾": HorizLimitBottom,
    "|": VertLimit
}
_plants = []
_herbivores = []
_carnivores = []
_spawners = []
_protozoans = []


def init_map(map_filename):
    """
    sets up the tile_map and map dimension info as global module vars
    :param map_filename: relative path to the map file
    """
    global _tile_map, _map_width, _map_height
    _tile_map = _parse_map('maps/' + map_filename + '.map')
    _map_width = len(_tile_map[0])
    _map_height = len(_tile_map)


def _parse_map(map_path):
    """
    initialises internal map (2D-list) with tiles and puts initialised entity
    on each tile if there is one on that position.
    :param map_path: relative path to the map file
    :return: tile_map
    """
    tile_map = []

    for y, row in enumerate(open(map_path)):
        tile_map.append([])
        for x, token in enumerate(row.rstrip('\n')):
            tile = Tile(y, x)
            if token != " ":    #empty space is not an entity
                _init_entity(token, tile)
            tile_map[-1].append(tile)

    _init_env_rings(tile_map)

    return tile_map


def _init_entity(token, tile):
    """
    initialises actual entity from the token and adds it to one of the entity
    lists, if it belongs there. the entity will associate itself with the
    given tile
    :param token: textual token representing the entity
    :param tile: the tile to be associated with the entity
    """
    try:
        entity_class = _entity_dict[token]
    except KeyError:
        raise KeyError("your map contains this unexpected token: " + token)

    if Carnivore.__subclasscheck__(entity_class):
        _carnivores.append(entity_class(tile))
    elif Herbivore.__subclasscheck__(entity_class):
        _herbivores.append(entity_class(tile))
    elif entity_class == RainForest:
        _plants.append(entity_class(tile))
    elif entity_class == Vegetation:
        _plants.append(entity_class("ʷʬY".index(token), tile))
    elif entity_class == Protozoan:
        _protozoans.append(entity_class(tile))
    elif entity_class == Water:
        _spawners.append(entity_class(tile))
    else:   #basic entities don't need to be held in an extra list
        entity_class(tile)


def token_map():
    """
    builds a token map from the tile map
    :return: textual representation of the current map
    """
    return [map(str, row) for row in _tile_map]


def watch_info():
    if global_vars.watched_entity is None:
        return None
    return _tile_map[global_vars.watched_entity.pos_y][global_vars.watched_entity.pos_x].tile_info


def set_watched_entity(pos_y, pos_x):
    try:
        global_vars.watched_entity = _tile_map[pos_y][pos_x].entity()
    except IndexError:
        global_vars.watched_entity = None


def update():
    """
    updates all entities. this is done in multiple steps, updating each
    entity type separately, one after another.
    """
    global_vars.anim_toggler = not global_vars.anim_toggler
    _handle_animal_type(hunter_class=Carnivore, prey_class=Herbivore)
    _handle_animal_type(hunter_class=Herbivore, prey_class=Vegetation)
    _veggie_action()
    _protozoan_action()
    _spawner_action()


def _handle_animal_type(hunter_class, prey_class):
    """
    lets all animals of the hunter class act. eaten prey will be removed from
    the corresponding prey list. newborn/starved hunters will be added/removed
    from the corresponding hunter lists.
    :param hunter_class: the hunter class
    :param prey_class: the prey class
    """

    if hunter_class == Carnivore:
        hunter_list, prey_list = _carnivores, _herbivores
    else:
        hunter_list, prey_list = _herbivores, _plants

    born_hunters = []

    for hunter in hunter_list:
        if hunter.life_over():
            hunter_list.remove(hunter.die())
            if hunter_class == Carnivore:
                global_vars.c_age += 1
            else:
                global_vars.h_age += 1

        elif hunter.is_hungry():
            dead_animal = hunter.hunger_game()
            if isinstance(dead_animal, prey_class):      #ate whole food
                prey_list.remove(dead_animal)
                if hunter_class == Carnivore:
                    global_vars.h_eaten += 1
            elif isinstance(dead_animal, hunter_class):  #starved
                hunter_list.remove(dead_animal)
                if hunter_class == Carnivore:
                    global_vars.c_starved += 1
                else:
                    global_vars.h_starved += 1
            elif dead_animal is True:                  #ate part of food
                continue
            else:   #hunter moves if it couldn't find food / didn't starve
                if not hunter.move():
                    hunter_list.remove(hunter.die())
                    if hunter_class == Carnivore:
                        global_vars.c_trampled += 1
                    else:
                        global_vars.h_trampled += 1
        else:   #hunter tries to reproduce only if it is not hungry
            newborn_hunter = hunter.try_reproduction()
            if newborn_hunter:
                born_hunters.append(newborn_hunter)
            else:   #hunter tries to move if it couldn't find partner
                if not hunter.move():   #hunter dies if it can't move
                    hunter_list.remove(hunter.die())
                    if hunter_class == Carnivore:
                        global_vars.c_trampled += 1
                    else:
                        global_vars.h_trampled += 1

    hunter_list.extend(born_hunters)


def _veggie_action():
    """
    lets all plants act. new plants (reproduction) will be added to
    the plants list.
    """
    new_plants = []

    for plant in _plants:
        if plant.wants_to_grow():
            grown_plant = plant.try_growth()
            if grown_plant:
                new_plants.append(grown_plant)

    _plants.extend(new_plants)


def _protozoan_action():
    """
    lets all proto animals act. if it makes the jump onto the beach, the old
    protozoan entity will be removed from and the new animal added to the
    corresponding list. protozoans can also die of age when trying to move.
    """
    for proto in _protozoans:
        if proto.beach_reachable():
            old_proto, new_animal = proto.jump_on_beach()
            _protozoans.remove(old_proto)
            if isinstance(new_animal, Herbivore):
                _herbivores.append(new_animal)
            else:
                _carnivores.append(new_animal)
        else:
            dead_proto = proto.move()
            if dead_proto:  #protos can die of age
                _protozoans.remove(dead_proto)


def _spawner_action():
    """
    each spawning entity tries to spawn a new protozoan. the protozoan will
    be added to the corresponding list.
    """
    for spawner in _spawners:
        new_proto = spawner.try_spawning()
        if new_proto:
            _protozoans.append(new_proto)


def _init_env_rings(tile_map, num_rings=8):
    """
    initialises the environment rings for each tile of the map.
    :param tile_map: 2D list containing all tiles of the map
    :param num_rings: the number of environment rings to set up for each tile
    """
    for y, row in enumerate(tile_map):
        for x, tile in enumerate(row):
            env_rings = []
            for scope in range(1, num_rings+1):
                env_rings.append(_calculate_env_ring(tile_map, y, x, scope))
            tile.env_rings = env_rings


def _calculate_env_ring(tile_map, center_y, center_x, scope):
    """
    calculates the tile ring of the given scope around the tile at position
    center_y/center_x. tile coordinates that are outside of the map will be
    ignored.
    :param tile_map: 2D list containing all tiles of the map
    :param pos_y: y-coordinate of the tile
    :param pos_x: x-coordinate of the tile
    :param scope: expanse of the tile ring list to be calculated
    scope = 1 [0][1][2] scope = 2 [x][x][x][x][x]
              [3][o][4]           [x]         [x]
              [5][6][7]           [x]   [o]   [x]
                                  [x]         [x]
                                  [x][x][x][x][x]
    :return: tile ring list
    """
    env_ring = []

    try:
        y_on_map = center_y - scope     #top ring row
        for relative_x in range(-scope, scope+1):
            x_on_map = center_x + relative_x
            env_ring.append(tile_map[y_on_map][x_on_map])

        x_on_map = center_x - scope     #left ring column
        for relative_y in range(-scope+1, scope):
            y_on_map = center_y + relative_y
            env_ring.append(tile_map[y_on_map][x_on_map])

        x_on_map = center_x + scope     #right ring column
        for relative_y in range(-scope+1, scope):
            y_on_map = center_y + relative_y
            env_ring.append(tile_map[y_on_map][x_on_map])

        y_on_map = center_y + scope     #bottom ring row
        for relative_x in range(-scope, scope+1):
            x_on_map = center_x + relative_x
            env_ring.append(tile_map[y_on_map][x_on_map])

    except IndexError:
        pass

    return env_ring
