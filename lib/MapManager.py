from lib.EntityManager import EntityManager
import lib.globals as global_vars


class MapManager(object):
    def __init__(self, map_filename):
        map_path = 'maps/' + map_filename + '.map'
        self._map = [list(row.rstrip('\n')) for row in open(map_path)]
        self._em = EntityManager(self)

        self._map_width = len(self._map[1])
        self._map_height = len(self._map)

        self.parse_map()


    @property
    def map(self):
        return self._map

    def parse_map(self):
        """
        parses the initial map and adds new entities to the entity manager accordingly
        """
        for y, row in enumerate(self._map):
            for x, cell in enumerate(row):
                if cell != " ":
                    self._em.add_entity(cell, y, x)

    def create_new_map(self):
        """
        creates a new map with the size of the initial map, filled with Empty objects
        :return: empty map
        """
        new_map = [
            [self._em.placeholder(y, x) for x in range(self._map_width)]
            for y in range(self._map_height - 1)
        ]
        #curses cant draw last element in last row(window[max_height, max_width])
        new_map.append(
            [self._em.placeholder(self._map_height, x) for x in range(self._map_width - 1)]
        )

        return new_map

    def update(self):
        """
        tells the entity manager to update all entities and applies all changes to the map
        """
        self._em.update()
        global_vars.anim_toggler = not global_vars.anim_toggler

        new_map = self.create_new_map()

        for entity in self._em.entities:
            if self._em.is_placeholder(entity):
                continue
            if entity.pos_y > 34 or entity.pos_y < 0 or entity.pos_x > 139 or entity.pos_x < 0:
                continue
            if entity.pos_y == 34 and entity.pos_x == 139:
                continue
            if entity.pos_y == 0 and entity.pos_x == 139:
                continue
            new_map[entity.pos_y][entity.pos_x] = entity

        self._map = new_map


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

    #not perfect yet
    def get_env(self, pos_y, pos_x, scope):
        """
        calculates part of map around a specific object with a given range
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
            for offset_x in range(-scope, scope + 1):
                try:
                    row.append(self._map[pos_y + offset_y][pos_x + offset_x])
                except IndexError:
                    continue
            env.append(row)
        return env
