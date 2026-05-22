import pymunk

from .entity import FragileEntity
from .constants import PIG_RADIUS
import assets


class Pig(FragileEntity):
    texture_dimensions = (PIG_RADIUS * 2, PIG_RADIUS * 2)

    def create_body(self) -> pymunk.Body:
        body = pymunk.Body()
        shape = pymunk.Circle(body, PIG_RADIUS)
        shape.density = 0.3
        shape.friction = 0.4
        shape.elasticity = 0.5

        return body


class RegularPig(Pig):
    max_health = 10
    damage_resistance = 1
    damage_textures = (
        assets.SMALL_PIG_HURT_4,
        assets.SMALL_PIG_HURT_3,
        assets.SMALL_PIG_HURT_2,
        assets.SMALL_PIG_HURT_1,
        assets.SMALL_PIG,
    )


class ForemanPig(Pig):
    max_health = 20
    damage_resistance = 1
    damage_textures = (assets.FOREMAN_PIG_HURT_5, assets.FOREMAN_PIG_HURT_4, assets.FOREMAN_PIG_HURT_3,
                       assets.FOREMAN_PIG_HURT_2, assets.FOREMAN_PIG_HURT_1, assets.FOREMAN_PIG)


class CorporalPig(Pig):
    max_health = 40
    damage_resistance = 6
    damage_textures = (assets.CORPORAL_PIG_HURT_6, assets.CORPORAL_PIG_HURT_5, assets.CORPORAL_PIG_HURT_4,
                       assets.CORPORAL_PIG_HURT_3, assets.CORPORAL_PIG_HURT_2, assets.CORPORAL_PIG_HURT_1, assets.CORPORAL_PIG)


class KingPig(Pig):
    max_health = 40
    damage_resistance = 3
    damage_textures = (assets.KING_PIG_HURT_4, assets.KING_PIG_HURT_3,
                       assets.KING_PIG_HURT_2, assets.KING_PIG_HURT_1, assets.KING_PIG)
    texture_dimensions = (PIG_RADIUS * 4, PIG_RADIUS * 4)

    def create_body(self) -> pymunk.Body:
        body = pymunk.Body()
        shape = pymunk.Circle(body, PIG_RADIUS * 2)
        shape.density = 0.3
        shape.friction = 0.4
        shape.elasticity = 0.5

        return body
