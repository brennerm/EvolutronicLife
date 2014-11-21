from lib.EntityManager import EntityManager
from lib.Tile import Tile
import lib.globals as global_vars


class MapManager(object):
    def __init__(self, map_filename):
        self._em = EntityManager(self)
        self._map = self._init_map('maps/' + map_filename + '.map')
        self._map_width = len(self._map[1])
        self._map_height = len(self._map)


    def _init_map(self, map_path):
        """
        initialises internal map (2D-list) with tiles. also puts entities
        on those tiles if there is one on that position.
        :param map_path: relative path to the map file
        :return: tile_map
        """
        tile_map = []

        for y, row in enumerate(open(map_path)):
            tile_map.append([])
            for x, token in enumerate(row.rstrip('\n')):
                tile = Tile(y, x)
                self._em.add_entity(token, tile)
                tile_map[-1].append(tile)

        return tile_map


    @property
    def map(self):
        """
        builds a token map from the tile map
        :return: token_map
        """
        return [map(str, row) for row in self._map]


    def update(self):
        """
        tells the entity manager to update all entities
        """
        global_vars.anim_toggler = not global_vars.anim_toggler
        self._em.update()


    def get_env(self, pos_y, pos_x, scope):
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
                    env[-1].append(self._map[y_on_map][x_on_map])
                except IndexError:
                    env[-1].append(Tile(self._em.placeholder_limit()))

        return env
