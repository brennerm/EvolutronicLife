class Tile(object):
    def __init__(self, pos_y=None, pos_x=None, entity=None):
        self._entity_stack = []
        if entity:      #can be initialised without entity
            self._entity_stack.append(entity)
        self._pos_y = pos_y
        self._pos_x = pos_x


    @property
    def entity(self):
        return self._entity_stack[-1]

    @property
    def pos_y(self):
        return self._pos_y

    @property
    def pos_x(self):
        return self._pos_x

    def empty(self):
        """
        returns true if tile holds no entity, false otherwise
        :return: boolean stating whether the tile holds no entity
        """
        return not self._entity_stack

    def walkable(self):
        """
        returns whether this tile can be walked upon by an entity
        :return: boolean indicating whether an entity can step on this tile
        """
        return self.empty() or not self.entity.blocks_step()

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
        return " " if self.empty() else str(self.entity)
