import os
import pygame
import random
import neat

class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("up_bird.png").convert_alpha()
        self.rect = self.image.get_rect(center=(200, 360))
        self.temp_bird_y = 0
        self.gravity = 0
        # self.jump_sound = pygame.mixer.Sound('jump.mp3')
        # self.jump_sound.set_volume(3)
    
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
        self.type = type
        self.speed = speed
        self.pipe_down_x, self.pipe_up_x = 1000, 1000

        if self.type == "top-pipe":
            self.image = pygame.transform.rotate(pygame.image.load("pipe.png").convert_alpha(), 180)
            self.rect = self.image.get_rect(topleft = (self.pipe_up_x, loc))
        else:
            self.image = pygame.image.load("pipe.png").convert_alpha()
            self.rect = self.image.get_rect(topleft = (self.pipe_down_x, loc))
    
    def destroy(self):
        if self.rect.x <= -195:
            self.kill()

    def update(self):
        self.rect.x -= self.speed
        self.destroy()

def collision_sprite(bird, obstacle_group):
    if pygame.sprite.spritecollide(bird.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    if bird.sprite.rect.y < 0 or bird.sprite.rect.y > 670:
        return False
    return True

def calculate_neural_network_inputs(bird, obstacle_group):
    bird_x = bird.sprite.rect.centerx  # Horizontal position of the bird
    bird_y = bird.sprite.rect.centery  # Vertical position of the bird

    # Initialize distances with a large number if no pipes are present
    from_bird_to_pipe = float('inf')
    vertical_distance = float('inf')

    for obstacle in obstacle_group:
        # Since pipes come in pairs, check for bottom pipe to calculate gap center
        if obstacle.rect.left > bird_x and obstacle.type == "bottom-pipe":
            # Horizontal distance to the next pipe
            distance_to_next_pipe = obstacle.rect.left - bird_x

            # If this pipe is closer than the previous closest, update the distances
            if distance_to_next_pipe < from_bird_to_pipe:
                from_bird_to_pipe = distance_to_next_pipe
                
                gap_height = 100  # The vertical space between the top and bottom pipes
                gap_center = obstacle.rect.top + (gap_height / 2)  # Center of the gap

                # Vertical distance to the center of the gap
                vertical_distance = gap_center - bird_y

    return from_bird_to_pipe, vertical_distance

def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        genome.fitness = play_game(net)  # Your function to play the game

def play_game(net):
    # Reset or set up the game environment
    pygame.init()
    screen = pygame.display.set_mode((1000, 720))
    bird = pygame.sprite.GroupSingle()
    bird.add(Bird())
    obstacle_group = pygame.sprite.Group()

    score = 0
    running = True
    clock = pygame.time.Clock()
    speed = 5.0
    speed_gen = 3500
    frames_alive = 0

    obstacle_timer = pygame.USEREVENT + 1
    pygame.time.set_timer(obstacle_timer, 500)
    
    # For font
    test_font = pygame.font.Font('Hack-Bold.ttf', 40)

    last_passed_pipe = None  # Track the last pipe passed

    # Start the main game loop
    while running:
        text_surface = test_font.render('Score: ' + str(int(score)), False, 'Black')

        # Poll events (simulate user input)
        for event in pygame.event.get():
            if event.type == obstacle_timer:
                generate_y = random.randint(300, 600)
                top_pipe1 = Obstacle(generate_y - 600, speed, "top-pipe")
                bottom_pipe1 = Obstacle(generate_y, speed)

                obstacle_group.add(top_pipe1, bottom_pipe1)

                pygame.time.set_timer(obstacle_timer, speed_gen)

            if event.type == pygame.QUIT:
                running = False

        # Neural network input: distance to next pipe, bird's y position, etc.
        from_bird_to_pipe, vertical_distance = calculate_neural_network_inputs(bird, obstacle_group)

        # Use the neural network to decide whether to jump
        output = net.activate((from_bird_to_pipe, bird.sprite.rect.y, vertical_distance))
        if output[0] > 0.5:  # threshold to jump
            bird.sprite.gravity = -7  # jump

        # Game logic
        obstacle_group.update()
        bird.update()

        # Collision check
        if not collision_sprite(bird, obstacle_group):
            running = False  # End the game simulation

        # Increment the frames_alive count
        frames_alive += 1


        for pipe in obstacle_group:
            if pipe.rect.right < bird.sprite.rect.left and (last_passed_pipe is None):
                score += 1  # Increment score for each pipe passed
                pipe.kill()

        # Update the game screen (optional, you could run without rendering for faster training)
        screen.blit(pygame.image.load('background.jpg').convert_alpha(), (0, 0))
        obstacle_group.draw(screen)
        bird.draw(screen)
        screen.blit(text_surface, (700, 30))
        
        pygame.display.flip()

        # Control the frame rate
        clock.tick(30)
        

    # Return the fitness score
    fitness = score + (frames_alive / 100.0)  # Adjust scoring formula as needed
    return fitness

def run(config_path):
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, 
                                neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
    
    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    # Run until a solution is found.
    winner = p.run(eval_genomes, 50)
    print('\nBest genome:\n{!s}'.format(winner))

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    run(config_path)
   
