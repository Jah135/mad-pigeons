import pymunk

from .level import Level

from .entity import CorporealEntity
import assets

BIRD_RADIUS = 15


class Bird(CorporealEntity):
    texture_dimensions = (BIRD_RADIUS * 2, BIRD_RADIUS * 2)

    def create_body(self) -> pymunk.Body:
        body = pymunk.Body()
        shape = pymunk.Circle(body, BIRD_RADIUS)
        shape.density = 3
        shape.friction = 0.4

        return body

    def activate_ability(self): ...


class BirdRed(Bird):
    def __init__(self, level: Level) -> None:
        super().__init__(level)

        self.set_texture(assets.RED_BIRD)
