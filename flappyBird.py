"""
    **FIXME: 

    *AI

"""

import pygame
import random

# Obstacle list
def obstacle_gen(rect_list):
    global score
    global speed
    if rect_list:
        for i, j in rect_list:
            screen.blit(top_pipe, j)
            screen.blit(bottom_pipe, i)
            j.x -= speed
            i.x -= speed
            if (i.x < -194):
                score += 1
        return [[top, bottom] for top, bottom in rect_list if top.x > -195] # deleting pipes that go off screen
    return []

def collisions(bird, obstacles):
    if obstacles:
        for obstacle1, obstacle2 in obstacles:
            if bird.colliderect(obstacle1) or bird.colliderect(obstacle2): return False
    return True

# pygame setup
pygame.init()

screen = pygame.display.set_mode((1000, 720))

# Name, Icon for title bar
pygame.display.set_caption("Flappity")
icon = pygame.image.load("logo.png").convert_alpha()
pygame.display.set_icon(icon)

# To control fps
clock = pygame.time.Clock()

score = 0
speed = 3.0
speed_gen = temp = 3500

running = True
x, y = 200, 360
bird_gravity = 0
pipe_generation_speed = 0

# fill the screen with a color to hide anything from last frame
sky_bg = pygame.image.load("background.jpg").convert_alpha()  #To load regular surface as images
#text_surface = test_font.render(text, anti-alias = True -> smooth edges. for pixel art = False , color)

top_pipe = pygame.transform.rotate(pygame.image.load("pipe.png").convert_alpha(), 180)
bottom_pipe = pygame.image.load("pipe.png").convert_alpha()

# Bird
bird_surf = pygame.image.load("up_bird.png").convert_alpha()
bird_rect = bird_surf.get_rect(center = (x, y))

# Timer
obstacle_rect_list = []
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, speed_gen)


while running:
    pipe_down_x, pipe_down_y = 1000, random.randint(300, 600)
    pipe_up_x, pipe_up_y = 1000, pipe_down_y - 600

    top_pipe_rect = top_pipe.get_rect(topleft = (pipe_up_x, pipe_up_y))
    bottom_pipe_rect = bottom_pipe.get_rect(topleft = (pipe_down_x, pipe_down_y))
    
    # For Score and font 
    test_font = pygame.font.Font('Hack-Bold.ttf', 50)
    text_surface = test_font.render('Score: ' + str(score), False, 'Black')

    # poll for events
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                bird_gravity = -10

        if event.type == obstacle_timer:
            obstacle_rect_list.append([bottom_pipe.get_rect(topleft = (pipe_down_x, pipe_down_y)), top_pipe.get_rect(topleft = (pipe_up_x, pipe_up_y))])
            if speed_gen >= 10: speed_gen -= 1
            pygame.time.set_timer(obstacle_timer, speed_gen)

        if event.type == pygame.QUIT:
            running = False


    if speed_gen + 15 >= temp:
        temp = speed_gen
        speed += 0.000000000000000001

    # Bird tries going across top and bottom border
    temp_bird_y = bird_rect.y
    bird_gravity += 1
    if 70 <=  bird_rect.bottom <= 650 and collisions(bird_rect, obstacle_rect_list):
        bird_rect.y += bird_gravity
    else:
        # Bird crashes to the borders or the pipes
        running = False
    
    # Tilt bird when it falls
    if bird_rect.y - 10 > temp_bird_y:
        bird_surf = pygame.image.load("down_bird.png").convert_alpha()
    else:
        bird_surf = pygame.image.load("up_bird.png").convert_alpha()

    screen.blit(sky_bg, (0, 0))
    screen.blit(bird_surf, bird_rect)    
    obstacle_rect_list = obstacle_gen(obstacle_rect_list)
    screen.blit(text_surface, (700, 30))


    # flip() the display to put your work on screen
    pygame.display.update()

    clock.tick(60)  # limits FPS to 60

print(score, speed_gen, speed)

pygame.quit()
   