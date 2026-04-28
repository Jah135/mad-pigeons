import pygame
from vec2 import Vec2

RESOLUTION = (1000, 2*282)

screen = pygame.display.set_mode(RESOLUTION)

running = True

clock = pygame.Clock()

background = pygame.transform.scale(pygame.image.load("./backgroundbetter.jpg"), RESOLUTION)
red = pygame.transform.scale_by(pygame.image.load("./red.png"), 0.35)

red_position = Vec2(100, 400)
red_velocity = Vec2(0, 0)

start_position = Vec2(0, 0)
end_position = Vec2(0, 0)

def update_physics():
    global red_position, red_velocity

    red_position += red_velocity * 1/60
    red_velocity += Vec2(0, 4)

def draw_display():
    screen.fill("black")
    screen.blit(background, (0, 0))

    pygame.draw.circle(screen, "red", start_position.t, 4)
    pygame.draw.circle(screen, "red", end_position.t, 4)
    pygame.draw.line(screen, "red", start_position.t, end_position.t)

    screen.blit(red, red_position.t)

    pygame.display.flip()


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    left_down = pygame.mouse.get_just_pressed()[0]
    left_up = pygame.mouse.get_just_released()[0]

    if left_down:
        start_position = Vec2(*pygame.mouse.get_pos())
    elif left_up:
        end_position = Vec2(*pygame.mouse.get_pos())

        red_position = start_position
        red_velocity = end_position - start_position

    update_physics()
    draw_display()

    clock.tick(60)