from Entities import *


class EntityManager(object):
    def __init__(self):
        self._entities = []

    @property
    def entities(self):
        return self._entities

    def add_entity(self, token, pos_y, pos_x):
        try:
            self._entities.append((available_entities[token])(pos_y, pos_x))
        except KeyError:
            raise KeyError(token + " is no valid entity! check your map, boon!!!")

    def update(self):
        for entity in self._entities:
            if entity.is_movable:
                entity.move()