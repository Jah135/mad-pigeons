from __future__ import annotations

import pygame
import pymunk

from pygame import transform
from math import degrees
from typing import TYPE_CHECKING, Sequence, Type, Self, Any

if TYPE_CHECKING:
    from .level import Level

from .constants import get_collision_force


class EntitySnapshot:
    data: dict[str, Any]
    creator: Type[Entity]

    def __init__(self, entity: Entity) -> None:
        self.data = dict()
        self.creator = entity.__class__

        entity.write_snapshot(self.data)

    def recreate(self, level: Level) -> Entity:
        return self.creator.from_snapshot(level, self.data)


class Entity:
    """
    A generic level object.
    """

    level: Level

    def __init__(self, level: Level) -> None:
        self.level = level
        level.add_entity(self)

    def write_snapshot(self, data: dict):
        """
        An abstract method for use in subclasses.

        This method is used for saving attributes of an Entity in a dictionary, for later use in `from_snapshot`.
        """
        ...

    @classmethod
    def from_snapshot(cls, level: Level, data: dict) -> Self:
        """
        An abstract method for use in subclasses.

        This method is used for loading an entity from a previous snapshot taken with `write_snapshot`.
        """
        ...

    def update(self, dt: float) -> None:
        """
        An abstract method for use in subclasses.

        This method is called every frame that this Entity exists.
        """
        ...

    def update_physics(self, dt: float) -> None:
        """
        An abstract method for use in subclasses.

        This method is called every physics step that this Entity exists.
        """
        ...

    def display(self, screen: pygame.Surface) -> None:
        """
        An abstract method for use in subclasses.

        This method is called every frame to render this Entity to the screen.
        """
        ...

    def display_debug(self, screen: pygame.Surface) -> None:
        """
        An abstract method for use in subclasses.

        This method is called every frame while debugging, to render this Entity to the screen.
        """

    def remove(self) -> None:
        """Removes this Entity from the level it was instantiated in."""
        self.level.remove_entity(self)


class CorporealEntity(Entity):
    """
    A physical, tangible object that is affected by physics and is able to collide
    or interact with other entities.
    """

    body: pymunk.Body
    texture: pygame.Surface
    texture_dimensions: tuple[int, int]
    texture_offset: tuple[int, int] = (0, 0)

    def __init__(self, level: Level) -> None:
        super().__init__(level)

        new_body = self.create_body()

        self.body = new_body
        self.level.add_body(new_body)
        self.level.register_entity_body(self)

    def write_snapshot(self, data: dict):
        body = self.body

        data["position"] = (body.position.x, body.position.y)
        data["angle"] = body.angle

    @classmethod
    def from_snapshot(cls, level: Level, data: dict) -> Self:
        self = cls(level)
        self.body.position = data.get("position", (0, 0))
        self.body.angle = data.get("angle", 0)

        return self

    def create_body(self) -> pymunk.Body:
        """An abstract method for use in subclasses.

        This method is used to create a pymunk Body that will be used for physics collisions.
        """
        ...

    def on_collide_begin(
        self, arbiter: pymunk.Arbiter, other: CorporealEntity | None
    ) -> None:
        """
        An abstract method for use in subclasses.

        This method is called during the `begin` phase of a physics collision.
        """
        ...

    def on_collide_pre_solve(
        self, arbiter: pymunk.Arbiter, other: CorporealEntity | None
    ) -> None:
        """
        An abstract method for use in subclasses.

        This method is called during the `pre_solve` phase of a physics collision.
        """
        ...

    def on_collide_post_solve(
        self, arbiter: pymunk.Arbiter, other: CorporealEntity | None
    ) -> None:
        """
        An abstract method for use in subclasses.

        This method is called during the `post_solve` phase of a physics collision.
        """
        ...

    def on_collide_separate(
        self, arbiter: pymunk.Arbiter, other: CorporealEntity | None
    ) -> None:
        """
        An abstract method for use in subclasses.

        This method is called during the `separate` phase of a physics collision.
        """
        ...

    def set_texture(self, new_texture: pygame.Surface):
        self.texture = transform.smoothscale(new_texture, self.texture_dimensions)

    def remove(self) -> None:
        super().remove()
        self.level.remove_body(self.body)
        self.level.deregister_entity_body(self)

    def display(self, screen: pygame.Surface):
        rotated_image = transform.rotate(self.texture, degrees(-self.body.angle))
        screen.blit(
            rotated_image,
            self.body.position
            + pymunk.Vec2d(*self.texture_offset).rotated(self.body.angle)
            - (rotated_image.width / 2, rotated_image.height / 2),
        )


class FragileEntity(CorporealEntity):
    """A physical object that is susceptible to damage."""

    health: float
    max_health: float

    damage_resistance: float
    damage_textures: Sequence[pygame.Surface]

    def __init__(self, level: Level) -> None:
        super().__init__(level)

        self.health = self.max_health
        self._update_image()

    def on_collide_post_solve(
        self, arbiter: pymunk.Arbiter, other: CorporealEntity | None
    ) -> None:
        impulse = get_collision_force(arbiter)

        if impulse > 200:
            self.inflict_damage((impulse - 200) / 200)

    def on_death(self) -> None:
        """
        An abstract method for use in subclasses.

        This method is called when this Entity's health reaches zero.
        """
        ...

    def _update_image(self):
        index = round(self.health / self.max_health * (len(self.damage_textures) - 1))

        self.set_texture(self.damage_textures[index])

    def inflict_damage(self, damage: float) -> None:
        if self.health <= 0:
            return

        weighted_damage = damage * (1.1**-self.damage_resistance)

        self.health -= weighted_damage

        if self.health <= 0:
            self.on_death()
            self.remove()
        else:
            self._update_image()
