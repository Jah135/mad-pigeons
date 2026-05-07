import pygame

# backgrounds
BACKGROUND_1 = pygame.image.load("./resources/backgrounds/background2.png")

# birds
BIRD_SPRITESHEET = pygame.image.load("./resources/spritesheets/birds.png")
RED_BIRD = pygame.transform.scale_by(
    BIRD_SPRITESHEET.subsurface(pygame.Rect(0, 0, 64, 64)), 0.5
)

# pigs

# objects
WOOD_SPRITESHEET = pygame.image.load("./resources/spritesheets/wood.png")
WOOD_BOX = WOOD_SPRITESHEET.subsurface(pygame.Rect(0, 0, 84, 84))
WOOD_WEDGE = WOOD_SPRITESHEET.subsurface(pygame.Rect(84, 84, 82, 82))
WOOD_TRIANGLE = WOOD_SPRITESHEET.subsurface(pygame.Rect(84, 0, 84, 84))
WOOD_BALL = WOOD_SPRITESHEET.subsurface(pygame.Rect(166, 84, 76, 76))
