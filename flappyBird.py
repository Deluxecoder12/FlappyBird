import pygame

# pygame setup
pygame.init()

screen = pygame.display.set_mode((1000, 720))

# Title bar
pygame.display.set_caption("Flappity")

# Icon for title bar
icon = pygame.image.load("flappyB.png")
pygame.display.set_icon(icon)

# To control fps
clock = pygame.time.Clock()

# For font 
# test_font = pygame.font.Font(type, size)

running = True
x, y = 200, 360
pipe_up_x, pipe_up_y = 600, -900
pipe_down_x, pipe_down_y = 600, 300

#sky_bg = pygame.image.load(".png")   To load regular surface as images
#text_surface = test_font.render(text, anti-alias = True -> smooth edges. for pixel art = False , color)

top_pipe = pygame.Surface((200, 700))
top_pipe.fill("green")

bottom_pipe = pygame.Surface((200, 700))
bottom_pipe.fill("green")

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if y >= 60:
                    y -= 70
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("sky blue")
 
    # RENDER YOUR GAME HERE

    # Bird
    bird = pygame.draw.circle(screen, "yellow", (x, y), 30, 0)

    # Bird tries going across top and bottom border
    if 10 <=  bird.y <= 650:
        y += 3
    else:
        running = False

    screen.blit(top_pipe, (100 ,-600))
    screen.blit(bottom_pipe, (50, 600))

    # top_pipe = pygame.draw.rect(screen, "green", (pipe_up_x, pipe_up_y, 200, 1000))
    # bottom_pipe = pygame.draw.rect(screen, "green", (pipe_down_x, pipe_down_y, 200, 1000))

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()
    