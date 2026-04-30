import pygame
import pymunk

class RedBird:
    IMAGE = pygame.transform.scale_by(pygame.image.load("./assets/red.png"), 0.35)

    def __init__(self, space: pymunk.Space) -> None:
        body = pymunk.Body()
        body.position = (0, 0)

        shape = pymunk.Circle(body, 20)
        shape.density = 0.001

        space.add(body, shape)

        print(body.mass)
        
        self.body = body

    def draw(self, screen: pygame.Surface):
        screen.blit(self.IMAGE, self.body.position.int_tuple)