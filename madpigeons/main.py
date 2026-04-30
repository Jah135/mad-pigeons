import pygame
from game import PhysGame
from birds import RedBird

class TheGame(PhysGame):
    window_width = 1000
    window_height = 282 * 2

    def __init__(self) -> None:
        super().__init__()

        self.background_image = pygame.transform.scale(pygame.image.load("./assets/background.jpg"), (self.window_width, self.window_height))

        red = RedBird(self.space)

        self.bird = red

    def on_mouse_down(self, left: bool, middle: bool, right: bool):
        self.bird.body

    def on_draw(self, out: pygame.Surface):
        out.blit(self.background_image)
        self.bird.draw(out)
    


game = TheGame()
game.start()