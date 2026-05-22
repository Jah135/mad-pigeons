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

        space.on_collision(begin=self._on_collision_begin, pre_solve=self._on_collision_pre_solve,
                           post_solve=self._on_collision_post_solve, separate=self._on_collision_separate)

        self.space = space
        self.entities = set()
        self._body_to_entity = dict()

    # collision handlers
    def _on_collision_begin(self, arbiter: pymunk.Arbiter, *_):
        entity_a, entity_b = self.get_entities_from_bodies(*arbiter.bodies)

        if entity_a is not None:
            entity_a.on_collide_begin(arbiter)

        if entity_b is not None:
            entity_b.on_collide_begin(arbiter)

    def _on_collision_pre_solve(self, arbiter: pymunk.Arbiter, *_):
        entity_a, entity_b = self.get_entities_from_bodies(*arbiter.bodies)

        if entity_a is not None:
            entity_a.on_collide_pre_solve(arbiter)

        if entity_b is not None:
            entity_b.on_collide_pre_solve(arbiter)

    def _on_collision_post_solve(self, arbiter: pymunk.Arbiter, *_):
        entity_a, entity_b = self.get_entities_from_bodies(*arbiter.bodies)

        if entity_a is not None:
            entity_a.on_collide_post_solve(arbiter)

        if entity_b is not None:
            entity_b.on_collide_post_solve(arbiter)

    def _on_collision_separate(self, arbiter: pymunk.Arbiter, *_):
        entity_a, entity_b = self.get_entities_from_bodies(*arbiter.bodies)

        if entity_a is not None:
            entity_a.on_collide_separate(arbiter)

        if entity_b is not None:
            entity_b.on_collide_separate(arbiter)

    # external updating

    def update_physics(self, dt: float):
        """Performs a physics step update."""
        for entity in self.entities:
            entity.update_physics(dt)

        self.space.step(dt)

    def update(self, dt: float):
        """Performs an update step."""
        for entity in self.entities:
            entity.update(dt)

    def display(self, screen: pygame.Surface):
        """Displays all of the level's entities to the screen."""
        for entity in self.entities:
            entity.display(screen)

    # Body->Entity mapping
    def register_entity_body(self, entity: CorporealEntity):
        """Maps an entity to it's body. This is meant to be used internally."""
        self._body_to_entity[entity.body] = entity

    def deregister_entity_body(self, entity: CorporealEntity):
        """Unmaps an entity from it's body. This is meant to be used internally."""
        del self._body_to_entity[entity.body]

    def get_entities_from_bodies(self, *bodies: pymunk.Body) -> tuple[CorporealEntity | None, ...]:
        """
        Returns a tuple of entities associated with the specified bodies, in the same order that they were given.

        There may be None where a body was not associated with any entities.
        """
        return tuple(self._body_to_entity.get(body, None) for body in bodies)

    # Body
    def add_body(self, body: pymunk.Body):
        """Adds a Body and all of its Shapes to the level's Space."""
        self.space.add(body, *body.shapes)

    def remove_body(self, body: pymunk.Body):
        """Removes a Body and all of its Shapes from the level's Space."""
        self.space.remove(body, *body.shapes)

    # Entity
    def add_entity(self, entity: Entity) -> None:
        """Adds an entity to this level's `entities` set."""
        self.entities.add(entity)

    def remove_entity(self, entity: Entity) -> None:
        """Removes an entity from this level's `entities` set."""
        if entity not in self.entities:
            return
        self.entities.remove(entity)
