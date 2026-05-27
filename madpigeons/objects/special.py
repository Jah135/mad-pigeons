import pygame
import pymunk

from pygame import transform

from . import polygon
from .level import Level
from .entity import FragileEntity, Entity
from .constants import BOX_WIDTH
from .wood import (
    WOOD_DENSITY,
    WOOD_ELASTICITY,
    WOOD_FRICTION,
)
import assets

EXPLOSION_FRAMES = (
    assets.SMOKE_0,
    assets.SMOKE_1,
    assets.SMOKE_2,
    assets.SMOKE_3,
    assets.SMOKE_4,
    assets.SMOKE_5,
)


class Explosion(Entity):
    position: tuple[int, int]

    current_frame: int
    animate_timer: float

    def __init__(
        self, level: Level, position: tuple[int, int], radius: float, pressure: float
    ) -> None:
        super().__init__(level)

        bodies_in_radius = [
            info.shape.body
            for info in level.space.point_query(position, radius, pymunk.ShapeFilter())
            if info.shape.body is not None
        ]
        entities_in_radius = self.level.get_entities_from_bodies(*bodies_in_radius)

        for body, entity in zip(bodies_in_radius, entities_in_radius):
            delta = body.position - position

            body.apply_impulse_at_local_point(delta.normalized() * pressure)

            if entity is not None and isinstance(entity, FragileEntity):
                entity.inflict_damage((1 - delta.length / radius) * 10)

        self.position = position
        self.radius = radius

        self.current_frame = 0
        self.animate_timer = 0

    def update(self, dt: float) -> None:
        self.animate_timer += dt

        if self.animate_timer >= 0.04:
            self.animate_timer = 0
            self.current_frame += 1

        if self.current_frame >= len(EXPLOSION_FRAMES):
            self.remove()

    def display(self, screen: pygame.Surface) -> None:
        image = transform.smoothscale_by(
            EXPLOSION_FRAMES[self.current_frame], self.radius / 100
        )

        screen.blit(
            image,
            (self.position[0] - image.width / 2, self.position[1] - image.height / 2),
        )


class TNT(FragileEntity):
    max_health = 3
    damage_resistance = 0.7
    damage_textures = (assets.TNT,)
    texture_dimensions = (BOX_WIDTH, BOX_WIDTH)

    def create_body(self) -> pymunk.Body:
        body = pymunk.Body()
        shape = pymunk.Poly(body, polygon.generate_rectangle(BOX_WIDTH))
        shape.density = WOOD_DENSITY
        shape.friction = WOOD_FRICTION
        shape.elasticity = WOOD_ELASTICITY

        return body

    def on_death(self) -> None:
        Explosion(self.level, self.body.position.int_tuple, 100, 500000)
