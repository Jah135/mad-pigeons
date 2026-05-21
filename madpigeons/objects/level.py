import pymunk
import pygame

from .entity import Entity, CorporealEntity


class Level:
    """
    An object for containing and managing entities.

    It also manages the physics of all CorporealEntity objects stored in it.
    """

    space: pymunk.Space
    entities: set[Entity]

    _body_to_entity: dict[pymunk.Body, CorporealEntity]

    def __init__(self) -> None:
        space = pymunk.Space()
        space.gravity = (0, 800)

        self.space = space
        self.entities = set()
        self._body_to_entity = {}

    def update_physics(self, dt: float):
        for entity in self.entities:
            entity.update_physics(dt)

        self.space.step(dt)

    def update(self, dt: float):
        for entity in self.entities:
            entity.update(dt)

    def display(self, screen: pygame.Surface):
        for entity in self.entities:
            entity.display(screen)

    # Body->Entity mapping
    def register_entity_body(self, entity: CorporealEntity):
        self._body_to_entity[entity.body] = entity

    def deregister_entity_body(self, entity: CorporealEntity):
        del self._body_to_entity[entity.body]

    def get_entity_from_body(self, body: pymunk.Body) -> CorporealEntity | None:
        return self._body_to_entity.get(body)

    # Body
    def add_body(self, body: pymunk.Body):
        self.space.add(body, *body.shapes)

    def remove_body(self, body: pymunk.Body):
        self.space.remove(body, *body.shapes)

    # Entity
    def add_entity(self, entity: Entity) -> None:
        self.entities.add(entity)

    def remove_entity(self, entity: Entity) -> None:
        if entity not in self.entities:
            return
        self.entities.remove(entity)
