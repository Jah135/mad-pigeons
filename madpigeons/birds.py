import pygame
import pymunk
from math import degrees

class RedBird:
    IMAGE = pygame.transform.scale_by(pygame.image.load("./assets/red.png"), 0.35)

    def __init__(self, space: pymunk.Space) -> None:
        body = pymunk.Body()
        body.position = (0, 0)

        shape = pymunk.Circle(body, 20)
        shape.density = 0.001
        shape.friction = 40

        space.add(body, shape)
        self.body = body
        self.shape = shape

    def draw(self, screen: pygame.Surface):
        rotated = pygame.transform.rotate(self.IMAGE, -degrees(self.body.angle))

        screen.blit(rotated, (self.body.position.x - rotated.width / 2, self.body.position.y - rotated.height / 2))