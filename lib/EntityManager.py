from lib.Entities import *


class EntityManager(object):
    def __init__(self, map_manager):
        self._map_manager = map_manager
        self._entities = []
        self._entity_dict = {
            " ": Empty,
            "ʷ": Vegetation,
            "ʬ": Vegetation,
            "Y": Vegetation,
            "#": Animal,
            "~": Water,
            "∽": AlterWater,
            ":": Beach,
            "_": HorizLimitTop,
            "‾": HorizLimitBottom,
            "|": VertLimit
        }


    @property
    def entities(self):
        return self._entities

    def add_entity(self, token, pos_y, pos_x):
        """
        add entity
        :param token: used to determine which kind of entity needs to be added
        :param pos_y: y-coordinate of Entity
        :param pos_x: x-coordinate of Entity
        """
        try:
            entity_class = self._entity_dict[token]
            arg_list = [pos_y, pos_x]
            if token in "ʷʬY":
                arg_list.insert(0, "ʷʬY".index(token))
            self._entities.append(entity_class(*arg_list))
        except KeyError:
            raise KeyError("your map contains this unexpected token: " + token)

    def replace_entity(self, new_entity):
        """
        puts new entity on its given coordinates. deletes old entity on those
        coordinates while doing so
        :param new_entity: the new entity to take the spot
        """
        for entity in self._entities:
            if (entity.pos_y == new_entity.pos_y) and (entity.pos_x == new_entity.pos_x):
                self._entities.remove(entity)
                break
        self._entities.append(new_entity)

    def update(self):
        """
        updates all entities
        """
        new_entities = []
        for entity in self._entities:
            if isinstance(entity, Animal):
                entity.move()
            elif isinstance(entity, Vegetation):
                new_object = entity.update(self._map_manager)
                if not new_object is None:
                    new_entities.append(new_object)

        for new_entity in new_entities:
            self.replace_entity(new_entity)

    def placeholder(self, pos_y, pos_x):
        """
        returns placeholder object for the given map position
        :param pos_y: y coordinate
        :param pos_x: x coordinate
        """
        return Empty(pos_y, pos_x)

    def is_placeholder(self, entity):
        """
        returns whether the given entity is a placeholder
        (instance of Empty)
        :param entity: instance of Entity to check
        """
        return isinstance(entity, Empty)