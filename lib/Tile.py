class Tile(object):
    def __init__(self, pos_y=None, pos_x=None, entity=None):
        self._entity_stack = []
        if entity:      #can be initialised without entity
            self._entity_stack.append(entity)
        self._pos_y = pos_y
        self._pos_x = pos_x

    @property
    def pos_y(self):
        return self._pos_y

    @property
    def pos_x(self):
        return self._pos_x

    @property
    def env_rings(self):
        return self._env_rings

    def set_env_rings(self, env_rings):
        self._env_rings = env_rings


    def entity(self, entity_class=None, lvl=None):
        """
        if entity_class is given, returns an entity of the given class. also
        checks for the entity level if lvl is given. if no arguments are
        given, the topmost entity of the entity stack is returned.
        :param entity_class: the class of the searched entity
        :param lvl: the level of the searched entity (makes only sense for
            vegetation)
        :return: found entity
        """
        if entity_class:
            for entity in self._entity_stack:
                if isinstance(entity, entity_class):
                    if lvl is None or entity.lvl == lvl:
                        return entity
        else:
            return self._entity_stack[-1]


    def holds_entity(self, entity_class, lvl=None):
        """
        return true if the tile holds an entity of the given class. also
        checks for the entity level if lvl is given.
        :param entity_class: the class of the searched entity
        :param lvl: the level of the searched entity (makes only sense for
            vegetation)
        :return: boolean indicating whether the tile holds such an entity
        """
        return any(
            isinstance(entity, entity_class) and
            (lvl == None or entity.lvl == lvl)
            for entity in self._entity_stack
        )


    def empty(self):
        """
        returns true if tile holds no entity, false otherwise. use this method
        to check whether the tile holds any entities before calling entity()
        to avoid exceptions.
        :return: boolean stating whether the tile holds no entity
        """
        return not self._entity_stack


    def walkable(self, lvl=0):
        """
        returns whether this tile can be walked upon by an entity
        :return: boolean indicating whether an entity can step on this tile
        """
        return self.empty() or lvl < self.entity().blocks_step


    def push_entity(self, entity):
        """
        pushes given entity on entity stack
        """
        self._entity_stack.append(entity)


    def pop_entity(self, entity):
        """
        pops given entity from entity stack
        """
        self._entity_stack.remove(entity)


    def __str__(self):
        """
        returns the string representation of the topmost entity of the
        entity stack, or " " if the entity stack is empty
        """
        return " " if self.empty() else str(self.entity())
