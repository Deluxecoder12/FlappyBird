"""
    **FIXME: 

    *AI

"""

import pygame
import random

class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("up_bird.png").convert_alpha()
        self.rect = self.image.get_rect(center=(200, 360))
        self.temp_bird_y = 0
        self.gravity = 0
        #self.jump_sound = pygame.mixer.Sound('')
        #self.jump_sound.set_volume(num)
    
    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.gravity = -7
            #self.jump_sound.play(loops = -1 for continuosly)
    
    def apply_gravity(self):
        self.gravity += 1
        self.temp_bird_y = self.rect.y
        # Bird tries going across top and bottom border
        if 0 <=  self.rect.y <= 670:
            self.rect.y += self.gravity
        else:
            global running
            running = False

    def proper_image(self):
        # Tilt bird when it falls
        if self.rect.y - 15 > self.temp_bird_y:
            self.image = pygame.image.load("down_bird.png").convert_alpha()
        else:
            self.image = pygame.image.load("up_bird.png").convert_alpha()

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.proper_image()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, loc, speed, type="bottom-pipe"):
        super().__init__()

        self.speed = speed
        self.pipe_down_x, self.pipe_up_x = 1000, 1000

        if type == "top-pipe":
            self.image = pygame.transform.rotate(pygame.image.load("pipe.png").convert_alpha(), 180)
            self.rect = self.image.get_rect(topleft = (self.pipe_up_x, loc))
        else:
            self.image = pygame.image.load("pipe.png").convert_alpha()
            self.rect = self.image.get_rect(topleft = (self.pipe_down_x, loc))
    
    def destroy(self):
        if self.rect.x <= -195:
            self.kill()
            update_score()

    def update(self):
        #self.obstacle_rect_list = self.obstacle_gen()
        self.rect.x -= self.speed
        self.destroy()

def collision_sprite():
    if pygame.sprite.spritecollide(bird.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    if bird.sprite.rect.y < 0 or bird.sprite.rect.y > 670:
        return False
    return True

def update_score():
    global score
    score += 0.5

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

# fill the screen with a color to hide anything from last frame
sky_bg = pygame.image.load("background.jpg").convert_alpha()  #To load regular surface as images
#text_surface = test_font.render(text, anti-alias = True -> smooth edges. for pixel art = False , color)

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, speed_gen)

bird = pygame.sprite.GroupSingle()
bird.add(Bird())

obstacle_group = pygame.sprite.Group()

bg_music = pygame.mixer.Sound('FlappyBirdBG.mp3')
bg_music.play(loops=-1)

# For font
test_font = pygame.font.Font('Hack-Bold.ttf', 40)

while running:    
    # For Score 
    text_surface = test_font.render('Score: ' + str(int(score)), False, 'Black')

    # poll for events
    for event in pygame.event.get():
        if event.type == obstacle_timer:
            temp -= 100

            generate_y = random.randint(300, 600)
            top_pipe1 = Obstacle(generate_y - 600, speed, "top-pipe")
            bottom_pipe1 = Obstacle(generate_y, speed)

            obstacle_group.add(top_pipe1, bottom_pipe1)

            pygame.time.set_timer(obstacle_timer, speed_gen)

        if event.type == pygame.QUIT:
            running = False


    if temp < 0:
        speed += 0.0000000000000000001
        temp = speed_gen

    screen.blit(sky_bg, (0, 0))
    
    obstacle_group.draw(screen)
    obstacle_group.update()
    
    bird.draw(screen)
    bird.update()
    
    screen.blit(text_surface, (700, 30))

    running = collision_sprite()

    # flip() the display to put your work on screen
    pygame.display.update()

    clock.tick(60)  # limits FPS to 60

print(score, speed_gen, speed)

pygame.quit()
   