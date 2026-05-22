from __future__ import annotations

import pygame
import pymunk

from pygame import transform
from math import degrees

from typing import TYPE_CHECKING, Sequence

if TYPE_CHECKING:
    from .level import Level


class Entity:
    """
    A generic object.

    this will probably only be used for explosions
    """

    level: Level

    def __init__(self, level: Level) -> None:
        self.level = level
        level.add_entity(self)

    def update(self, dt: float) -> None:
        """An abstract method for use in subclasses that is called every frame."""
        ...

    def update_physics(self, dt: float) -> None:
        """An abstract method for use in subclasses that is called every physics step."""
        ...

    def display(self, screen: pygame.Surface) -> None:
        """An abstract method for use in subclasses that is called every frame to render this Entity to the screen."""
        ...

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

    def __init__(self, level: Level) -> None:
        super().__init__(level)

        new_body = self.create_body()

        self.body = new_body
        self.level.add_body(new_body)
        self.level.register_entity_body(self)

    def create_body(self) -> pymunk.Body:
        """An abstract method for use in subclasses to create a pymunk Body instance that will be used in physics calculations."""
        ...

    def set_texture(self, new_texture: pygame.Surface):
        self.texture = transform.scale(new_texture, self.texture_dimensions)

    def remove(self) -> None:
        super().remove()
        self.level.remove_body(self.body)
        self.level.deregister_entity_body(self)

    def display(self, screen: pygame.Surface):
        rotated_image = transform.rotate(self.texture, -degrees(self.body.angle))
        screen.blit(
            rotated_image,
            self.body.position - (rotated_image.width / 2, rotated_image.height / 2),
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

    def on_death(self) -> None:
        """An abstract method for use in subclasses that is called when this Entity's health reaches zero."""
        ...

    def _update_image(self):
        index = int(self.health / self.max_health * (len(self.damage_textures) - 1))

        self.set_texture(self.damage_textures[index])

    def inflict_damage(self, damage: float) -> None:
        self.health -= damage * (1.1**-self.damage_resistance)

        if self.health <= 0:
            self.on_death()
            self.remove()
        else:
            self._update_image()
