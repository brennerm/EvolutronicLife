class Tile(object):
    def __init__(self, entity, pos_y, pos_x):
        self._entity_stack = []
        if entity:      #can be None for empty space
            self._entity_stack.append(entity)
        self._pos_y = pos_y
        self._pos_x = pos_x


    @property
    def entity(self):
        return self._entity_stack[-1]


    def empty(self):
        """
        returns true if tile holds empty space, false otherwise
        """
        return bool(self.entity_stack)

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
        return " " if self.empty() else str(self._entity_stack[-1])