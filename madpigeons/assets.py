import pygame
import os

os.chdir("C:\\Users\\nbradberry425\\Documents\\GitHub\\mad-pigeons\\madpigeons")

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

# King Pig
KING_PIG = PIG_SPRITESHEET.subsurface(pygame.Rect(679, 2, 129, 144))
KING_PIG_BLINK = PIG_SPRITESHEET.subsurface(pygame.Rect(543, 2, 129, 144))
KING_PIG_LOSE = PIG_SPRITESHEET.subsurface(pygame.Rect(409, 2, 129, 144))
KING_PIG_HURT_1 = PIG_SPRITESHEET.subsurface(pygame.Rect(272, 2, 129, 144))
KING_PIG_HURT_2 = PIG_SPRITESHEET.subsurface(pygame.Rect(137, 2, 129, 144))
KING_PIG_HURT_3 = PIG_SPRITESHEET.subsurface(pygame.Rect(2, 12, 129, 133))
KING_PIG_HURT_4 = PIG_SPRITESHEET.subsurface(pygame.Rect(2, 2, 130, 145))

#Foreman Pig
FOREMAN_PIG = PIG_SPRITESHEET.subsurface(pygame.Rect(507, 152, 118, 101))


PIG_SMILING = PIG_SPRITESHEET.subsurface(pygame.Rect(576, 622, 80, 80))

# objects
WOOD_SPRITESHEET = pygame.image.load("./resources/spritesheets/wood.png")
WOOD_BOX = WOOD_SPRITESHEET.subsurface(pygame.Rect(0, 0, 84, 84))
WOOD_WEDGE = WOOD_SPRITESHEET.subsurface(pygame.Rect(84, 84, 82, 82))
WOOD_TRIANGLE = WOOD_SPRITESHEET.subsurface(pygame.Rect(84, 0, 84, 84))
WOOD_BALL = WOOD_SPRITESHEET.subsurface(pygame.Rect(166, 84, 76, 76))
WOOD_RECTANGLE = WOOD_SPRITESHEET.subsurface(pygame.Rect(167, 162, 84, 40))
WOOD_PLANK = WOOD_SPRITESHEET.subsurface(pygame.Rect(294, 161, 169, 21))
