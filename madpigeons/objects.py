import pygame
import pymunk

from typing import Sequence
from pygame import draw
from math import degrees
from pymunk import Vec2d

import assets


class Entity:
    body: pymunk.Body
    image: pygame.Surface

    def __init__(self, scope: list["Entity"], space: pymunk.Space) -> None:
        self.body = pymunk.Body()

        space.add(self.body)
        scope.append(self)

    def draw(self, screen: pygame.Surface):
        rotated = pygame.transform.rotate(self.image, -degrees(self.body.angle))
        screen.blit(rotated, self.body.position - Vec2d(*rotated.size) / 2)


## Bird presets
class RedBird(Entity):
    image = assets.RED_BIRD

    def __init__(self, scope: list[Entity], space: pymunk.Space) -> None:
        super().__init__(scope, space)

        shape = pymunk.Circle(self.body, 18)
        shape.density = 0.3
        shape.friction = 0.4

        space.add(shape)


## Wood presets
class WoodBox(Entity):
    def __init__(self, scope: list[Entity], space: pymunk.Space, size: int) -> None:

        super().__init__(
            scope,
            space,
        )

        shape = pymunk.Poly(
            self.body,
            (
                (-size // 2, -size // 2),
                (size // 2, -size // 2),
                (-size // 2, size // 2),
                (size // 2, size // 2),
            ),
        )
        shape.density = 0.6
        shape.friction = 0.8

        space.add(shape)

        self.image = pygame.transform.scale(assets.WOOD_BOX, (size, size))


class WoodWedge(Entity):
    def __init__(self, scope: list[Entity], space: pymunk.Space, size: int) -> None:
        super().__init__(
            scope,
            space,
        )

        shape = pymunk.Poly(
            self.body,
            (
                (-size // 2, -size // 2),
                (-size // 2, size // 2),
                (size // 2, size // 2),
            ),
        )
        shape.density = 0.6
        shape.friction = 0.8

        space.add(shape)

        self.image = pygame.transform.scale(assets.WOOD_WEDGE, (size, size))


class WoodTriangle(Entity):
    def __init__(self, scope: list[Entity], space: pymunk.Space, size: int) -> None:
        super().__init__(
            scope,
            space,
        )

        shape = pymunk.Poly(
            self.body,
            ((-size // 2, size // 2), (size // 2, size // 2), (0, -size // 2)),
        )
        shape.density = 0.6
        shape.friction = 0.8

        space.add(shape)

        self.image = pygame.transform.scale(assets.WOOD_TRIANGLE, (size, size))


class WoodBall(Entity):
    def __init__(self, scope: list[Entity], space: pymunk.Space, radius: int) -> None:
        super().__init__(scope, space)

        shape = pymunk.Circle(self.body, radius / 2)
        shape.density = 0.6
        shape.friction = 0.8

        space.add(shape)

        self.image = pygame.transform.scale(assets.WOOD_BALL, (radius, radius))
