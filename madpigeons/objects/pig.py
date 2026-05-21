import pymunk

from .entity import FragileEntity
from .constants import STANDARD_PIG_RADIUS
import assets


class Pig(FragileEntity):
    max_health = 10
    damage_resistance = 1
    damage_textures = (
        assets.SMALL_PIG_HURT_4,
        assets.SMALL_PIG_HURT_3,
        assets.SMALL_PIG_HURT_2,
        assets.SMALL_PIG_HURT_1,
        assets.SMALL_PIG,
    )
    texture_dimensions = (STANDARD_PIG_RADIUS * 2, STANDARD_PIG_RADIUS * 2)

    def create_body(self) -> pymunk.Body:
        body = pymunk.Body()
        shape = pymunk.Circle(body, STANDARD_PIG_RADIUS)
        shape.density = 0.3
        shape.friction = 0.4
        shape.elasticity = 0.5

        return body
