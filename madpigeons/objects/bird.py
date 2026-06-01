from __future__ import annotations

import pymunk
from typing import TYPE_CHECKING

from .constants import get_collision_force
from .entity import CorporealEntity, FragileEntity
import assets

if TYPE_CHECKING:
    from .level import Level

BIRD_RADIUS = 15


class Bird(CorporealEntity):
    texture_dimensions = (BIRD_RADIUS * 2, BIRD_RADIUS * 2)

    def create_body(self) -> pymunk.Body:
        body = pymunk.Body()
        shape = pymunk.Circle(body, BIRD_RADIUS)
        shape.collision_type = 1
        shape.density = 1
        shape.friction = 0.4
        shape.elasticity = 0.4

        return body

    def on_collide_post_solve(
        self, arbiter: pymunk.Arbiter, other: CorporealEntity | None
    ) -> None:
        if isinstance(other, FragileEntity):
            force = get_collision_force(arbiter)

            if force > 100:
                print("bird doing things")
                other.inflict_damage(2 + force / 100)

    def activate_ability(self): ...


class BirdRed(Bird):
    def __init__(self, level: Level) -> None:
        super().__init__(level)

        self.set_texture(assets.RED_BIRD)
