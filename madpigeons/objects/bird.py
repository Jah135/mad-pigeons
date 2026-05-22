import pymunk

from .entity import CorporealEntity
from .constants import BIRD_RADIUS
import assets


class Bird(CorporealEntity):
    texture_dimensions = (BIRD_RADIUS * 2, BIRD_RADIUS * 2)

    def create_body(self) -> pymunk.Body:
        body = pymunk.Body()
        shape = pymunk.Circle(body, BIRD_RADIUS)
        shape.density = 0.3
        shape.friction = 0.4

        return body


class BirdRed(Bird):
    texture = assets.RED_BIRD
