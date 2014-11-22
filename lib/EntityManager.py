from lib.Entities import *


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


def placeholder_limit():
    """
    returns limit entity placeholder
    :return: instance of Limit
    """
    return Limit()


def add_entity(token, tile):
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


def update():
    """
    updates all entities and adds potential new entities to entities list
    """
    from lib.MapManager import get_env  #local to avoid circular import
    new_entities = []

    for entity in _entities:
        if isinstance(entity, Animal):
            entity.act()
            entity.move(get_env(entity.pos_y, entity.pos_x, 1))
        elif isinstance(entity, Vegetation):
            if entity.wants_to_grow():
                new_plant = entity.grow(
                    get_env(entity.pos_y, entity.pos_x, 1)
                )
                if new_plant:   #might not have grown into new plant
                    new_entities.append(new_plant)

    _entities.extend(new_entities)
