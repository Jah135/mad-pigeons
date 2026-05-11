import pygame
import os

os.chdir("C:\\Users\\ehopper848\\Documents\\GitHub\\mad-pigeons\\madpigeons")

# backgrounds
BACKGROUND_1 = pygame.image.load("./resources/backgrounds/background1.jpg")
BACKGROUND_2 = pygame.image.load("./resources/backgrounds/background2.png")
BACKGROUND_3 = pygame.image.load("./resources/backgrounds/background3.png")

# birds
BIRD_SPRITESHEET = pygame.image.load("./resources/spritesheets/birds.png")
RED_BIRD = pygame.transform.scale_by(
    BIRD_SPRITESHEET.subsurface(pygame.Rect(0, 0, 64, 64)), 0.5
)

# pigs
PIG_SPRITESHEET = pygame.image.load("./resources/spritesheets/pigs.png")
PIG_SMILING = PIG_SPRITESHEET.subsurface(pygame.Rect(576, 622, 80, 80))

# objects
WOOD_SPRITESHEET = pygame.image.load("./resources/spritesheets/wood.png")
WOOD_BOX = WOOD_SPRITESHEET.subsurface(pygame.Rect(0, 0, 84, 84))
WOOD_WEDGE = WOOD_SPRITESHEET.subsurface(pygame.Rect(84, 84, 82, 82))
WOOD_TRIANGLE = WOOD_SPRITESHEET.subsurface(pygame.Rect(84, 0, 84, 84))
WOOD_BALL = WOOD_SPRITESHEET.subsurface(pygame.Rect(166, 84, 76, 76))
WOOD_RECTANGLE = WOOD_SPRITESHEET.subsurface(pygame.Rect(167, 162, 84, 40))
WOOD_PLANK = WOOD_SPRITESHEET.subsurface(pygame.Rect(294, 161, 169, 21))
