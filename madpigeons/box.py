import pygame
from game import Game

class Box:
    IMAGE = pygame.transform.scale_by(pygame.image.load("madpigeons/assets/box.png"), 0.1)

    def __init__(self):
        self.position = (0, 0)
        self.velocity = (0, 0)

    def draw(self, screen: pygame.Surface):
        screen.blit(self.IMAGE, self.position.t)
