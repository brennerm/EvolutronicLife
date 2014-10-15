from EntityManager import EntityManager


class MapManager(object):
    def __init__(self, map):
        self._map = map
        self._em = EntityManager()

        self._map_width = len(map[0])
        self._map_height = len(map)

        self.parse_map()

    def parse_map(self):
        y = 0
        for row in self._map:
            x = 0
            for cell in row:
                self._em.add_entity(cell, y, x)
                x += 1
            y += 1

    def create_new_map(self):
        new_map = [[" " for x in range(self._map_width)] for y in range(self._map_height - 1)]
        #curses cant draw last element in last row(window[max_height, max_width])
        new_map.append([" "] * (self._map_width - 1))

        return new_map

    def update(self):
        self._em.update()
        new_map = self.create_new_map()

        for entity in self._em.entities:
            if str(entity) == " ":
                continue
            new_map[entity.pos_y][entity.pos_x] = str(entity)

        self._map = new_map

    def draw_map(self, window):
        i = 0
        for row in self._map:
            window.addstr(i, 0, "".join(row))
            i += 1

