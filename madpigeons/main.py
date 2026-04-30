import pygame
from game import Game
from game import PhysGame
from birds import RedBird


from box import Box

GROUND_Y = 349
BOX_POSITIONS = [
    (200, GROUND_Y),        
    (350, GROUND_Y),        
    (500, GROUND_Y - 80),  
    (650, GROUND_Y),        
    (800, GROUND_Y - 120)
    ]
class TheGame(Game):
    window_width = 1000
    window_height = 282 * 2

    def __init__(self) -> None:
        super().__init__()

        self.background_image = pygame.transform.scale(pygame.image.load("madpigeons/assets/background.jpg"), (self.window_width, self.window_height))

        red = RedBird(self.space)

        self.bird = red


    def on_draw(self, out: pygame.Surface):
        out.blit(self.background_image)
        self.bird.draw(out)
        for i in range(len(BOX_POSITIONS)):
            out.blit(self.box.IMAGE, dest = BOX_POSITIONS[i]) #50x49
        
        

game = TheGame()
game.start()