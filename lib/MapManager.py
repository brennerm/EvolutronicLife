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
        initialises internal map (2D-list) with tiles holding entities
        :param map_path: relative path to the map file
        :return: tile_map
        """
        tile_map = []
        for y, row in enumerate(open(map_path)):
            tile_map.append([])
            for x, token in enumerate(row.rstrip('\n')):
                entity = self._em.add_entity(token, y, x)
                tile = Tile(entity, y ,x)
                if entity:  #entity can be None if token is empty space (" ")
                    entity.set_tile(tile)
                tile_map[-1].append(tile)
        return tile_map


    @property
    def map(self):
        """
        builds a token map from the tile map
        :return: token_map
        """
        token_map = []
        for row in self._map:
            token_map.append([str(tile) for tile in row])
        return token_map


    def update(self):
        """
        tells the entity manager to update all entities and applies all changes to the map
        """
        global_vars.anim_toggler = not global_vars.anim_toggler

        self._em.update()   #entities will be removed from their current tiles
        for entity in self._em.entities:    #and put on new tiles
            self._map[entity.pos_y][entity.pos_x].push_entity(entity)


    def get_field(self, pos_y, pos_x):
        """
        gets object of map with a given y and x coordinate
        :param pos_y: y-coordinate of object in map
        :param pos_x: x-coordinate of object in map
        :return: object of given position
        """
        try:
            return self._map[pos_y][pos_x]
        except IndexError:
            raise ValueError("field " + str(pos_y) + "," + str(pos_x) + " is not available")


    def get_env(self, pos_y, pos_x, scope):
        """
        calculates part of map around a specific object with a given range.
        parts that are outside of the map will be filled with limit entities.
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
            row = []
            y_on_map = pos_y + offset_y

            if 0 <= y_on_map < self._map_height:

                for offset_x in range(-scope, scope + 1):
                    x_on_map = pos_x + offset_x

                    if 0 <= x_on_map < self._map_width:
                        row.append(self._map[y_on_map][x_on_map])
                    else:
                        row.append(self._em.limit_placeholder())

                env.append(row)
            else:
                env.append([self._em.limit_placeholder()] * (2*scope + 1))

        return env
