import pygame
import pymunk

from pygame import transform
from math import degrees

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .level import Level


class Entity:
    """
    A generic entity object. this will probably only be used for explosions
    """
    level: Level

    def __init__(self, level: Level) -> None:
        self.level = level
        level.add_entity(self)

    def update(self, dt: float) -> None: ...
    def display(self, screen: pygame.Surface) -> None: ...

    def remove(self) -> None:
        self.level.remove_entity(self)


class CorporealEntity(Entity):
    """
    A physical, tangible object that is affected by physics and is able to collide
    or interact with other entities.
    """
    body: pymunk.Body
    image: pygame.Surface

    def __init__(self, level: Level) -> None:
        super().__init__(level)

        new_body = self.create_body()
        self.body = new_body
        self.level.add_body(new_body)

    def update_physics(self, dt: float) -> None: ...
    def create_body(self) -> pymunk.Body: ...

    def remove(self) -> None:
        super().remove()
        self.level.remove_body(self.body)

    def display(self, screen: pygame.Surface):
        rotated_image = transform.rotate(self.image, -degrees(self.body.angle))
        screen.blit(rotated_image, self.body.position)


class FragileEntity(CorporealEntity):
    """A physical object that is susceptible to damage."""
    damage_resistance: float
    health: float

    def on_damage(self) -> None: ...
    def on_break(self) -> None: ...

    def inflict_damage(self, damage: float) -> None:
        self.health -= damage * (1.1 ** -self.damage_resistance)

        self.on_damage()

        if self.health <= 0:
            self.on_break()
            self.remove()
