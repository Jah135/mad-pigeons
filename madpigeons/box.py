import pygame
from vec2 import Vec2
from game import Game

class Box:
    IMAGE = pygame.transform.scale_by(pygame.image.load("madpigeons/assets/box.png"), 0.1)

    def __init__(self):
        self.position = Vec2(0, 0)
        self.velocity = Vec2(0, 0)

    def draw(self, screen: pygame.Surface):
        screen.blit(self.IMAGE, self.position.t)
