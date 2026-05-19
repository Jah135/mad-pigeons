import pygame
import os
import pathlib

os.chdir(pathlib.Path(__file__).parent.resolve())

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

# Bad Piggies Sprites
BAD_PIGGIES_SPRITESHEET = pygame.image.load("./resources/spritesheets/bad_piggies.webp")

# King Pig
KING_PIG = PIG_SPRITESHEET.subsurface(pygame.Rect(679, 2, 129, 144))
KING_PIG_BLINK = PIG_SPRITESHEET.subsurface(pygame.Rect(543, 2, 129, 144))
KING_PIG_LOSE = PIG_SPRITESHEET.subsurface(pygame.Rect(409, 2, 129, 144))
KING_PIG_HURT_1 = PIG_SPRITESHEET.subsurface(pygame.Rect(272, 2, 129, 144))
KING_PIG_HURT_2 = PIG_SPRITESHEET.subsurface(pygame.Rect(137, 2, 129, 144))
KING_PIG_HURT_3 = PIG_SPRITESHEET.subsurface(pygame.Rect(2, 12, 129, 133))
KING_PIG_HURT_4 = PIG_SPRITESHEET.subsurface(pygame.Rect(2, 2, 130, 145))

# Foreman Pig
FOREMAN_PIG = PIG_SPRITESHEET.subsurface(pygame.Rect(507, 152, 118, 101))
FOREMAN_PIG_BLINK = PIG_SPRITESHEET.subsurface(pygame.Rect(384, 152, 118, 101))
FOREMAN_PIG_LOSE = PIG_SPRITESHEET.subsurface(pygame.Rect(261, 152, 118, 101))
FOREMAN_PIG_HURT_1 = PIG_SPRITESHEET.subsurface(pygame.Rect(138, 152, 118, 107))
FOREMAN_PIG_HURT_2 = PIG_SPRITESHEET.subsurface(pygame.Rect(138, 264, 118, 107))
FOREMAN_PIG_HURT_3 = PIG_SPRITESHEET.subsurface(pygame.Rect(138, 376, 118, 107))
FOREMAN_PIG_HURT_4 = PIG_SPRITESHEET.subsurface(pygame.Rect(138, 488, 118, 107))
FOREMAN_PIG_HURT_5 = PIG_SPRITESHEET.subsurface(pygame.Rect(138, 600, 118, 107))

# Corporal Pig
CORPORAL_PIG = PIG_SPRITESHEET.subsurface(pygame.Rect(469, 552, 104, 87))
CORPORAL_PIG_BLINK = PIG_SPRITESHEET.subsurface(pygame.Rect(469, 460, 104, 87))
CORPORAL_PIG_LOSE = PIG_SPRITESHEET.subsurface(pygame.Rect(683, 368, 104, 87))
CORPORAL_PIG_HURT_1 = PIG_SPRITESHEET.subsurface(pygame.Rect(576, 368, 104, 87))
CORPORAL_PIG_HURT_2 = PIG_SPRITESHEET.subsurface(pygame.Rect(469, 368, 104, 87))
CORPORAL_PIG_HURT_3 = PIG_SPRITESHEET.subsurface(pygame.Rect(362, 268, 104, 87))
CORPORAL_PIG_HURT_4 = PIG_SPRITESHEET.subsurface(pygame.Rect(362, 460, 104, 87))
CORPORAL_PIG_HURT_5 = PIG_SPRITESHEET.subsurface(pygame.Rect(362, 552, 104, 87))
CORPORAL_PIG_HURT_6 = PIG_SPRITESHEET.subsurface(pygame.Rect(362, 644, 104, 87))

# Big Pig
BIG_PIG = PIG_SPRITESHEET.subsurface(pygame.Rect(671, 264, 100, 98))
BIG_PIG_BLINK = PIG_SPRITESHEET.subsurface(pygame.Rect(568, 264, 100, 98))
BIG_PIG_LOSE = PIG_SPRITESHEET.subsurface(pygame.Rect(465, 264, 100, 98))
BIG_PIG_HURT_1 = PIG_SPRITESHEET.subsurface(pygame.Rect(362, 264, 100, 98))
BIG_PIG_HURT_2 = PIG_SPRITESHEET.subsurface(pygame.Rect(259, 264, 100, 98))
BIG_PIG_HURT_3 = PIG_SPRITESHEET.subsurface(pygame.Rect(259, 368, 100, 98))
BIG_PIG_HURT_4 = PIG_SPRITESHEET.subsurface(pygame.Rect(259, 472, 100, 98))
BIG_PIG_HURT_5 = PIG_SPRITESHEET.subsurface(pygame.Rect(259, 576, 100, 98))

# Medium Pig
MEDIUM_PIG = PIG_SPRITESHEET.subsurface(pygame.Rect(740, 542, 79, 77))
MEDIUM_PIG_BLINK = PIG_SPRITESHEET.subsurface(pygame.Rect(658, 542, 79, 77))
MEDIUM_PIG_LOSE = PIG_SPRITESHEET.subsurface(pygame.Rect(576, 624, 79, 77))
MEDIUM_PIG_HURT_1 = PIG_SPRITESHEET.subsurface(pygame.Rect(740, 460, 79, 77))
MEDIUM_PIG_HURT_2 = PIG_SPRITESHEET.subsurface(pygame.Rect(658, 460, 79, 77))
MEDIUM_PIG_HURT_3 = PIG_SPRITESHEET.subsurface(pygame.Rect(576, 460, 79, 77))
MEDIUM_PIG_HURT_4 = PIG_SPRITESHEET.subsurface(pygame.Rect(576, 542, 79, 77))
MEDIUM_PIG_HURT_5 = PIG_SPRITESHEET.subsurface(pygame.Rect(469, 644, 79, 77))

# Small Pig
SMALL_PIG = PIG_SPRITESHEET.subsurface(pygame.Rect(760, 624, 48, 46))
SMALL_PIG_BLINK = PIG_SPRITESHEET.subsurface(pygame.Rect(709, 674, 48, 46))
SMALL_PIG_LOSE = PIG_SPRITESHEET.subsurface(pygame.Rect(709, 624, 48, 46))
SMALL_PIG_HURT_1 = PIG_SPRITESHEET.subsurface(pygame.Rect(658, 624, 48, 46))
SMALL_PIG_HURT_2 = PIG_SPRITESHEET.subsurface(pygame.Rect(658, 674, 48, 46))
SMALL_PIG_HURT_3 = PIG_SPRITESHEET.subsurface(pygame.Rect(259, 680, 48, 46))
SMALL_PIG_HURT_4 = PIG_SPRITESHEET.subsurface(pygame.Rect(310, 680, 48, 46))

# Wood
WOOD_SPRITESHEET = pygame.image.load("./resources/spritesheets/wood.png")
WOOD_BOX = WOOD_SPRITESHEET.subsurface(pygame.Rect(0, 0, 84, 84))
WOOD_WEDGE = WOOD_SPRITESHEET.subsurface(pygame.Rect(84, 84, 82, 82))
WOOD_TRIANGLE = WOOD_SPRITESHEET.subsurface(pygame.Rect(84, 0, 84, 84))
WOOD_BALL = WOOD_SPRITESHEET.subsurface(pygame.Rect(166, 84, 76, 76))
WOOD_RECTANGLE = WOOD_SPRITESHEET.subsurface(pygame.Rect(167, 162, 84, 40))
WOOD_PLANK = WOOD_SPRITESHEET.subsurface(pygame.Rect(294, 161, 169, 21))

# Stone
STONE_SPRITESHEET = pygame.image.load("./resources/spritesheets/stone.png")

# Stone Box
STONE_BOX = STONE_SPRITESHEET.subsurface(pygame.Rect(0, 0, 84, 84))
DAMAGED_STONE_BOX_1 = STONE_SPRITESHEET.subsurface(pygame.Rect(0, 84, 84, 84))
DAMAGED_STONE_BOX_2 = STONE_SPRITESHEET.subsurface(pygame.Rect(0, 168, 84, 84))
DAMAGED_STONE_BOX_3 = STONE_SPRITESHEET.subsurface(pygame.Rect(0, 252, 84, 84))

# Stone Triangle
STONE_TRIANGLE = STONE_SPRITESHEET.subsurface(pygame.Rect(84, 0, 84, 84))
DAMAGED_STONE_TRIANGLE_1 = STONE_SPRITESHEET.subsurface(pygame.Rect(84, 84, 84, 84))
DAMAGED_STONE_TRIANGLE_2 = STONE_SPRITESHEET.subsurface(pygame.Rect(84, 168, 84, 84))
DAMAGED_STONE_TRIANGLE_3 = STONE_SPRITESHEET.subsurface(pygame.Rect(84, 252, 84, 84))

# Stone Wedge
STONE_WEDGE = STONE_SPRITESHEET.subsurface(pygame.Rect(168, 0, 82, 82))
DAMAGED_STONE_WEDGE_1 = STONE_SPRITESHEET.subsurface(pygame.Rect(250, 0, 82, 82))
DAMAGED_STONE_WEDGE_2 = STONE_SPRITESHEET.subsurface(pygame.Rect(332, 0, 82, 82))
DAMAGED_STONE_WEDGE_3 = STONE_SPRITESHEET.subsurface(pygame.Rect(414, 0, 82, 82))

# Large Stone Ball
LARGE_STONE_BALL = STONE_SPRITESHEET.subsurface(pygame.Rect(168, 82, 76, 76))
LARGE_DAMAGED_STONE_BALL_1 = STONE_SPRITESHEET.subsurface(pygame.Rect(168, 157, 77, 76))
LARGE_DAMAGED_STONE_BALL_2 = STONE_SPRITESHEET.subsurface(pygame.Rect(168, 232, 77, 76))
LARGE_DAMAGED_STONE_BALL_3 = STONE_SPRITESHEET.subsurface(pygame.Rect(168, 307, 77, 75))

# Small Stone Ball
SMALL_STONE_BALL = STONE_SPRITESHEET.subsurface(pygame.Rect(44, 337, 40, 40))
DAMAGED_SMALL_STONE_BALL_1 = STONE_SPRITESHEET.subsurface(pygame.Rect(128, 337, 40, 40))
DAMAGED_SMALL_STONE_BALL_2 = STONE_SPRITESHEET.subsurface(pygame.Rect(418, 126, 40, 40))
DAMAGED_SMALL_STONE_BALL_3 = STONE_SPRITESHEET.subsurface(pygame.Rect(459, 126, 40, 40))

# Stone Rectangle
STONE_RECTANGLE = STONE_SPRITESHEET.subsurface(pygame.Rect(247, 82, 84, 40))
DAMAGED_STONE_RECTANGLE_1 = STONE_SPRITESHEET.subsurface(pygame.Rect(382, 82, 84, 40))
DAMAGED_STONE_RECTANGLE_2 = STONE_SPRITESHEET.subsurface(pygame.Rect(417, 82, 84, 40))
DAMAGED_STONE_RECTANGLE_3 = STONE_SPRITESHEET.subsurface(pygame.Rect(247, 125, 84, 40))

# Large Stone Plank
LARGE_STONE_PLANK = STONE_SPRITESHEET.subsurface(pygame.Rect(247, 168, 203, 21))
LARGE_DAMAGED_STONE_PLANK_1 = STONE_SPRITESHEET.subsurface(
    pygame.Rect(247, 191, 203, 21)
)
LARGE_DAMAGED_STONE_PLANK_2 = STONE_SPRITESHEET.subsurface(
    pygame.Rect(247, 213, 203, 21)
)
LARGE_DAMAGED_STONE_PLANK_3 = STONE_SPRITESHEET.subsurface(
    pygame.Rect(247, 235, 203, 21)
)

# Medium Stone Plank
MEDIUM_STONE_PLANK = STONE_SPRITESHEET.subsurface(pygame.Rect(247, 257, 168, 21))
MEDIUM_DAMAGED_STONE_PLANK_1 = STONE_SPRITESHEET.subsurface(
    pygame.Rect(247, 279, 168, 21)
)
MEDIUM_DAMAGED_STONE_PLANK_2 = STONE_SPRITESHEET.subsurface(
    pygame.Rect(247, 301, 168, 21)
)
MEDIUM_DAMAGED_STONE_PLANK_3 = STONE_SPRITESHEET.subsurface(
    pygame.Rect(247, 323, 168, 21)
)

# Small Stone Plank
SMALL_STONE_PLANK = STONE_SPRITESHEET.subsurface(pygame.Rect(417, 256, 82, 21))
SMALL_DAMAGED_STONE_PLANK_1 = STONE_SPRITESHEET.subsurface(
    pygame.Rect(247, 345, 82, 21)
)
SMALL_DAMAGED_STONE_PLANK_2 = STONE_SPRITESHEET.subsurface(
    pygame.Rect(332, 345, 82, 21)
)
SMALL_DAMAGED_STONE_PLANK_3 = STONE_SPRITESHEET.subsurface(
    pygame.Rect(417, 278, 82, 21)
)

# XSmall Stone Plank
XSMALL_STONE_PLANK = STONE_SPRITESHEET.subsurface(pygame.Rect(417, 256, 82, 21))
XSMALL_DAMAGED_STONE_PLANK_1 = STONE_SPRITESHEET.subsurface(
    pygame.Rect(247, 345, 82, 21)
)
XSMALL_DAMAGED_STONE_PLANK_2 = STONE_SPRITESHEET.subsurface(
    pygame.Rect(332, 345, 82, 21)
)
XSMALL_DAMAGED_STONE_PLANK_3 = STONE_SPRITESHEET.subsurface(
    pygame.Rect(417, 279, 82, 21)
)

# Large Stone Square
LARGE_STONE_SQUARE = STONE_SPRITESHEET.subsurface(pygame.Rect(2, 338, 40, 40))
DAMAGED_LARGE_STONE_SQUARE_1 = STONE_SPRITESHEET.subsurface(
    pygame.Rect(85, 338, 40, 40)
)
DAMAGED_LARGE_STONE_SQUARE_2 = STONE_SPRITESHEET.subsurface(
    pygame.Rect(332, 127, 40, 40)
)
DAMAGED_LARGE_STONE_SQUARE_3 = STONE_SPRITESHEET.subsurface(
    pygame.Rect(375, 127, 40, 40)
)

# Small Stone Square
SMALL_STONE_SQUARE = STONE_SPRITESHEET.subsurface(pygame.Rect(417, 301, 9, 9))
DAMAGED_SMALL_STONE_SQUARE_1 = STONE_SPRITESHEET.subsurface(pygame.Rect(417, 323, 9, 9))
DAMAGED_SMALL_STONE_SQUARE_2 = STONE_SPRITESHEET.subsurface(pygame.Rect(417, 345, 9, 9))
DAMAGED_SMALL_STONE_SQUARE_3 = STONE_SPRITESHEET.subsurface(pygame.Rect(439, 301, 9, 9))


# Misc
TNT = BAD_PIGGIES_SPRITESHEET.subsurface(pygame.Rect(554, 566, 106, 106))
