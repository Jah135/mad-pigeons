import pymunk

from .entity import FragileEntity
import assets

PIG_RADIUS = 20


class Pig(FragileEntity):
    def create_body(self) -> pymunk.Body:
        body = pymunk.Body()
        shape = pymunk.Circle(body, PIG_RADIUS)
        shape.density = 0.3
        shape.friction = 0.4
        shape.elasticity = 0.5

        return body


class MinionPig(Pig):
    max_health = 5
    damage_resistance = 1
    damage_textures = (
        assets.MEDIUM_PIG_HURT_4,
        assets.MEDIUM_PIG_HURT_3,
        assets.MEDIUM_PIG_HURT_2,
        assets.MEDIUM_PIG_HURT_1,
        assets.MEDIUM_PIG,
    )
    texture_dimensions = (PIG_RADIUS * 2, PIG_RADIUS * 2)


class ForemanPig(Pig):
    max_health = 20
    damage_resistance = 1
    damage_textures = (
        assets.FOREMAN_PIG_HURT_5,
        assets.FOREMAN_PIG_HURT_4,
        assets.FOREMAN_PIG_HURT_3,
        assets.FOREMAN_PIG_HURT_2,
        assets.FOREMAN_PIG_HURT_1,
        assets.FOREMAN_PIG,
    )
    texture_dimensions = (int(PIG_RADIUS * 2 * 1.2), PIG_RADIUS * 2)

    def create_body(self) -> pymunk.Body:
        body = pymunk.Body()
        shape = pymunk.Circle(body, PIG_RADIUS)
        shape.density = 0.3
        shape.friction = 0.4
        shape.elasticity = 0.5

        return body


class CorporalPig(Pig):
    max_health = 10
    damage_resistance = 6
    damage_textures = (
        assets.CORPORAL_PIG_HURT_6,
        assets.CORPORAL_PIG_HURT_5,
        assets.CORPORAL_PIG_HURT_4,
        assets.CORPORAL_PIG_HURT_3,
        assets.CORPORAL_PIG_HURT_2,
        assets.CORPORAL_PIG_HURT_1,
        assets.CORPORAL_PIG,
    )
    texture_dimensions = (int(PIG_RADIUS * 2 * 1.15), PIG_RADIUS * 2)


class KingPig(Pig):
    max_health = 20
    damage_resistance = 3
    damage_textures = (
        assets.KING_PIG_HURT_4,
        assets.KING_PIG_HURT_3,
        assets.KING_PIG_HURT_2,
        assets.KING_PIG_HURT_1,
        assets.KING_PIG,
    )
    texture_dimensions = (PIG_RADIUS * 3, int(PIG_RADIUS * 3 * 1.15))
    texture_offset = (0, -5)

    def create_body(self) -> pymunk.Body:
        body = pymunk.Body()
        shape = pymunk.Circle(body, PIG_RADIUS * 1.5)
        shape.density = 0.3
        shape.friction = 0.4
        shape.elasticity = 0.5

        return body
