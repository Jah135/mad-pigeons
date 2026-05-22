import pymunk

from .entity import CorporealEntity
from .constants import STANDARD_BIRD_RADIUS
import assets


class BirdRed(CorporealEntity):
    texture = assets.RED_BIRD
    texture_dimensions = (STANDARD_BIRD_RADIUS * 2, STANDARD_BIRD_RADIUS * 2)

    def create_body(self) -> pymunk.Body:
        body = pymunk.Body()

        shape = pymunk.Circle(body, STANDARD_BIRD_RADIUS)
        shape.density = 0.3
        shape.friction = 0.4

        return body
