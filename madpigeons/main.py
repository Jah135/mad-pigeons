import pygame
from vec2 import Vec2
from game import Game

class RedBird:
    IMAGE = pygame.transform.scale_by(pygame.image.load("./assets/red.png"), 0.35)

    def __init__(self) -> None:
        self.position = Vec2(0, 0)
        self.velocity = Vec2(0, 0)
    
    def update(self, dt: float):
        self.position += self.velocity * dt
        self.velocity += Vec2(0, 4)

    def draw(self, screen: pygame.Surface):
        screen.blit(self.IMAGE, self.position.t)

class TheGame(Game):
    window_width = 1000
    window_height = 282 * 2

    def __init__(self) -> None:
        super().__init__()

        self.background_image = pygame.transform.scale(pygame.image.load("./assets/background.jpg"), (self.window_width, self.window_height))
        self.bird = RedBird()

    def on_draw(self, out: pygame.Surface):
        out.blit(self.background_image)
        

game = TheGame()
game.start()