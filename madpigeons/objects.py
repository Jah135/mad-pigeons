from pygame import draw
from math import degrees

import pygame
import pymunk


class Entity:
    body: pymunk.Body

    def __init__(self, scope: list["Entity"], space: pymunk.Space) -> None:
        self.body = pymunk.Body()

        space.add(self.body)
        scope.append(self)

    def draw(self, screen: pygame.Surface): ...


class RedBird(Entity):
    IMAGE = pygame.transform.scale_by(pygame.image.load("./assets/red.png"), 0.35)

    def __init__(self, scope: list[Entity], space: pymunk.Space) -> None:
        super().__init__(scope, space)

        shape = pymunk.Circle(self.body, 20)
        shape.mass = 0.3
        shape.friction = 0.4

        space.add(shape)

    def draw(self, screen: pygame.Surface):
        rotated = pygame.transform.rotate(self.IMAGE, -degrees(self.body.angle))

        screen.blit(
            rotated,
            (
                self.body.position.x - rotated.width / 2,
                self.body.position.y - rotated.height / 2,
            ),
        )


class Box(Entity):
    def __init__(
        self, scope: list[Entity], space: pymunk.Space, width: int, height: int
    ) -> None:
        super().__init__(scope, space)

        shape = pymunk.Poly(
            self.body,
            (
                (-width / 2, -height / 2),
                (width / 2, -height / 2),
                (-width / 2, height / 2),
                (width / 2, height / 2),
            ),
        )
        shape.mass = 1
        shape.friction = 0.5

        space.add(shape)

        self.shape = shape

        self.width = width
        self.height = height

    def draw(self, screen: pygame.Surface):
        draw.polygon(
            screen,
            "black",
            [
                v.rotated(self.body.angle) + self.body.position
                for v in self.shape.get_vertices()
            ],
        )
