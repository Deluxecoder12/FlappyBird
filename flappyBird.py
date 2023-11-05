"""
    #FIXME: 
    1. Rotate the bird as it moves and falls down
    2. Random generation of pipes
    3. Keep track of scores
    4. AI
"""

import pygame
import random

# pygame setup
pygame.init()

screen = pygame.display.set_mode((1000, 720))

# Title bar
pygame.display.set_caption("Flappity")

# Icon for title bar
icon = pygame.image.load("logo.png").convert_alpha()
pygame.display.set_icon(icon)

# To control fps
clock = pygame.time.Clock()

score = 0

running = True
x, y = 200, 360
pipe_down_x, pipe_down_y = 900, random.randint(300, 600)
pipe_up_x, pipe_up_y = 900, pipe_down_y - 600

# fill the screen with a color to hide anything from last frame
sky_bg = pygame.image.load("background.jpg").convert_alpha()  #To load regular surface as images
#text_surface = test_font.render(text, anti-alias = True -> smooth edges. for pixel art = False , color)

top_pipe = pygame.transform.rotate(pygame.image.load("pipe.png").convert_alpha(), 180)
top_pipe_rect = top_pipe.get_rect(topleft = (pipe_up_x, pipe_up_y))

bottom_pipe = pygame.image.load("pipe.png").convert_alpha()
bottom_pipe_rect = bottom_pipe.get_rect(topleft = (pipe_down_x, pipe_down_y))

while running:
    # Bird
    bird_surf = pygame.image.load("bird.png").convert_alpha()
    bird_rect = bird_surf.get_rect(center = (x, y))

    # For Score and font 
    test_font = pygame.font.Font('Hack-Bold.ttf', 50)
    text_surface = test_font.render('Score: ' + str(score), False, 'Black')

    # poll for events
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                y -= 55
        if event.type == pygame.QUIT:
            running = False
 
    # RENDER YOUR GAME HERE

    # pace = clock.get_time()
    # print(pace)

    #if pipe goes too left, render it back to the right as the obstacle
    if top_pipe_rect.x < 0:
        score += 1 
        top_pipe_rect.x, bottom_pipe_rect.x = 900, 900
        bottom_pipe_rect.y = random.randint(300, 600)
        top_pipe_rect.y = bottom_pipe_rect.y - 600
    
    
    # Bird tries going across top and bottom border
    if 10 <=  bird_rect.y <= 650:
        y += 3
    else:
        running = False

    screen.blit(sky_bg, (0, 0))
    screen.blit(bird_surf, bird_rect)
    screen.blit(top_pipe, top_pipe_rect)
    screen.blit(bottom_pipe, bottom_pipe_rect)
    screen.blit(text_surface, (700, 30))

    if bird_rect.colliderect(top_pipe_rect) or bird_rect.colliderect(bottom_pipe_rect):
        running = False
    
    top_pipe_rect.x -= 3
    bottom_pipe_rect.x -= 3

    # flip() the display to put your work on screen
    pygame.display.update()

    clock.tick(60)  # limits FPS to 60

pygame.quit()
    