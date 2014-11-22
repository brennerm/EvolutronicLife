from lib.Tile import Tile
from lib.Entities import *
import lib.globals as global_vars


_entities = []
_entity_dict = {
    "ʷ": Vegetation,
    "ʬ": Vegetation,
    "Y": Vegetation,
    "#": Animal,
    "~": Water,
    "∽": Water,
    ":": Beach,
    "_": HorizLimitTop,
    "‾": HorizLimitBottom,
    "|": VertLimit
}


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

    return tile_map


def _init_entity(token, tile):
    """
    creates actual entity from the token and adds it to the entities list
    :param token: textual token representing the entity
    :param tile: the tile to be associated with the entity
    """
    try:
        entity_class = _entity_dict[token]
        arg_list = [tile]
        if token in "ʷʬY":     #needs lvl if it is vegetation
            arg_list.insert(0, "ʷʬY".index(token))
        _entities.append(entity_class(*arg_list))
    except KeyError:
        raise KeyError("your map contains this unexpected token: " + token)


def token_map():
    """
    builds a token map from the tile map
    :return: textual representation of the current map
    """
    return [map(str, row) for row in _tile_map]


def update():
    """
    updates all entities. adds potential new entities to entities list and
    removes potential dead/eaten entities from the entities list
    """
    global_vars.anim_toggler = not global_vars.anim_toggler
    new_entities = []

    for entity in _entities:
        if isinstance(entity, Animal):
            entity.act()
            entity.move(_get_env(entity.pos_y, entity.pos_x, 1))
        elif isinstance(entity, Vegetation):
            if entity.wants_to_grow():
                new_plant = entity.grow(
                    _get_env(entity.pos_y, entity.pos_x, 1)
                )
                if new_plant:   #might not have grown into new plant
                    new_entities.append(new_plant)

    _entities.extend(new_entities)


def _get_env(pos_y, pos_x, scope):
    """
    calculates part of map around a specific object with a given range.
    parts that are outside of the map will be filled with tiles holding
    limit placeholder entities.
    :param pos_y: y-coordinate of object in map
    :param pos_x: x-coordinate of object in map
    :param scope: range around object to be returned
    scope = 1 [x][x][x] scope = 2 [x][x][x][x][x]
              [x][o][x]           [x][x][x][x][x]
              [x][x][x]           [x][x][o][x][x]
                                  [x][x][x][x][x]
                                  [x][x][x][x][x]
    :return: part of map as two dimensional list
    """
    env = []

    for offset_y in range(-scope, scope + 1):
        env.append([])
        y_on_map = pos_y + offset_y
        for offset_x in range(-scope, scope + 1):
            x_on_map = pos_x + offset_x
            try:
                env[-1].append(_tile_map[y_on_map][x_on_map])
            except IndexError:
                env[-1].append(Tile(entity=Limit()))

    return env
