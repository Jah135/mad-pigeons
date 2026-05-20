import pymunk

from .entity import Entity


class Level:
    """
    An object for containing and managing entities.

    It also manages the physics of all CorporealEntity objects stored in it.
    """
    space: pymunk.Space
    entities: set[Entity]

    def __init__(self) -> None:
        self.space = pymunk.Space()
        self.entities = set()

    def add_body(self, body: pymunk.Body):
        self.space.add(body, *body.shapes)

    def remove_body(self, body: pymunk.Body):
        self.space.remove(body, *body.shapes)

    def add_entity(self, entity: Entity) -> None:
        self.entities.add(entity)

    def remove_entity(self, entity: Entity) -> None:
        if entity not in self.entities:
            return
        self.entities.remove(entity)
