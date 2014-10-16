from Entities import *


class EntityManager(object):
    def __init__(self, map_manager):
        self._entities = []
        self._map_manager = map_manager

    @property
    def entities(self):
        return self._entities

    def add_entity(self, token, pos_y, pos_x):
        """
        add entity
        :param token: used to determine, which kind of entity needs to be added
        :param pos_y: y-coordinate of Entity
        :param pos_x: x-coordinate of Entity
        """
        try:
            self._entities.append((available_entities[token])(pos_y, pos_x))
        except KeyError:
            raise KeyError(token + " is no valid entity! check your map, boon!!!")

    def update(self):
        """
        updates all entities accordingly
        """
        for entity in self._entities:
            if entity.is_movable:
                entity.move()