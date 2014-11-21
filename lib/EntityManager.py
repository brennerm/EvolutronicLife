from lib.Entities import *


class EntityManager(object):
    def __init__(self, map_manager):
        self._map_manager = map_manager
        self._entities = []
        self._entity_dict = {
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


    def placeholder_limit(self):
        """
        returns limit entity placeholder
        :return: instance of Limit
        """
        return Limit()


    def add_entity(self, token, tile):
        """
        translates given token to an actual entity and adds it to the entities
        list, if it is not empty space. also returns the entity.
        :param token: textual token representing the entity
        :param pos_y: y coord of the entity
        :param pos_x: x coord of the entity
        """
        if token == " ":
            return
        try:
            entity_class = self._entity_dict[token]
            arg_list = [tile]
            if token in "ʷʬY":     #needs lvl if it is vegetation
                arg_list.insert(0, "ʷʬY".index(token))
            self._entities.append(entity_class(*arg_list))
        except KeyError:
            raise KeyError("your map contains this unexpected token: " + token)        


    def update(self):
        """
        updates all entities
        """
        new_entities = []

        for entity in self._entities:
            if isinstance(entity, Animal):
                entity.act()
                entity.move(
                    self._map_manager.get_env(entity.pos_y, entity.pos_x, 1)
                )
            elif isinstance(entity, Vegetation):
                if entity.wants_to_grow():
                    new_plant = entity.grow(
                        self._map_manager.get_env(entity.pos_y, entity.pos_x, 1)
                    )
                    if new_plant:   #might not have grown yet
                        new_entities.append(new_plant)

        self._entities.extend(new_entities)
