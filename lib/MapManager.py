import lib.EntityManager as EntMan
from lib.Tile import Tile
import lib.globals as global_vars


def init(map_filename):
    global _tile_map, _map_width, _map_height
    _tile_map = _init_map('maps/' + map_filename + '.map')
    _map_width = len(_tile_map[0])
    _map_height = len(_tile_map)


def _init_map(map_path):
    """
    initialises internal map (2D-list) with tiles and puts entity
    on each tile if there is one on that position. also adds all found
    entities to the entity manager.
    :param map_path: relative path to the map file
    :return: tile_map
    """
    tile_map = []

    for y, row in enumerate(open(map_path)):
        tile_map.append([])
        for x, token in enumerate(row.rstrip('\n')):
            tile = Tile(y, x)
            if token != " ":    #empty space is not an entity
                EntMan.add_entity(token, tile)
            tile_map[-1].append(tile)

    return tile_map


def token_map():
    """
    builds a token map from the tile map
    :return: textual representation of the current map
    """
    return [map(str, row) for row in _tile_map]


def update():
    """
    tells the entity manager to update all entities
    """
    global_vars.anim_toggler = not global_vars.anim_toggler
    EntMan.update()


def get_env(pos_y, pos_x, scope):
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
                env[-1].append(Tile(EntMan.placeholder_limit()))

    return env
