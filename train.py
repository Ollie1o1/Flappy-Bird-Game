import pygame
import neat
import os
import random

from src.bird import Bird
from src.pipe import Pipe, PIPE_SPEED  # PIPE_SPEED is a module‐level variable

# Window dimensions
WIN_WIDTH, WIN_HEIGHT = 600, 800

# Initialize pygame & window
pygame.init()
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Flappy NEAT (Speed-Up Every 5 Points)")

# 1) Background
orig_bg = pygame.image.load("assets/bg.png")
BG_IMG = pygame.transform.scale(orig_bg, (WIN_WIDTH, WIN_HEIGHT))

# 2) Bird (50×35)
orig_bird = pygame.image.load("assets/bird.png").convert_alpha()
scaled_bird = pygame.transform.scale(orig_bird, (110, 95))
import src.bird as bird_module
bird_module.BIRD_IMG = scaled_bird

# 3) Pipe (80×500)
orig_pipe = pygame.image.load("assets/pipe.png").convert_alpha()
scaled_pipe = pygame.transform.scale(orig_pipe, (250, 500))
import src.pipe as pipe_module
pipe_module.PIPE_IMG = scaled_pipe
pipe_module.Pipe.PIPE_TOP = pygame.transform.flip(scaled_pipe, False, True)
pipe_module.Pipe.PIPE_BOTTOM = scaled_pipe

STAT_FONT = pygame.font.SysFont("comicsans", 30)

def draw_window(birds, pipes, score, generation):
    WIN.blit(BG_IMG, (0, 0))
    for p in pipes:
        p.draw(WIN)
    for b in birds:
        b.draw(WIN)
    # Score (top-right)
    score_text = STAT_FONT.render(f"Score: {score}", True, (255, 255, 255))
    WIN.blit(score_text, (WIN_WIDTH - score_text.get_width() - 10, 10))
    # Generation number (top-left)
    gen_text = STAT_FONT.render(f"Gen: {generation}", True, (255, 255, 255))
    WIN.blit(gen_text, (10, 10))
    pygame.display.update()

def eval_genomes(genomes, config):
    # Reset pipe speed at start of each generation
    pipe_module.PIPE_SPEED = 5

    nets = []
    ge = []
    birds = []

    for genome_id, genome in genomes:
        genome.fitness = 0.0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        birds.append(Bird(230, 350))
        ge.append(genome)

    pipes = [Pipe(700)]
    score = 0
    generation = eval_genomes.generation
    clock = pygame.time.Clock()

    # Run until all birds die
    while len(birds) > 0:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # Choose which pipe to feed into the network
        pipe_ind = 0
        if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
            pipe_ind = 1

        # Move each bird & decide “flap” based on its network output
        for idx, bird_obj in enumerate(birds):
            bird_obj.move()
            ge[idx].fitness += 0.1  # small stay‐alive bonus

            top_dist = abs(bird_obj.y - pipes[pipe_ind].height)
            bottom_dist = abs(bird_obj.y - pipes[pipe_ind].bottom)
            horiz_dist = abs(pipes[pipe_ind].x - bird_obj.x)

            output = nets[idx].activate((bird_obj.y, top_dist, bottom_dist, horiz_dist))
            if output[0] > 0.5:
                bird_obj.flap()

        # Move pipes & check for new ones
        add_pipe = False
        removed = []
        for p in pipes:
            p.move()
            if not p.passed and birds and p.x < birds[0].x:
                p.passed = True
                add_pipe = True
            if p.x + p.PIPE_TOP.get_width() < 0:
                removed.append(p)

        if add_pipe:
            score += 1
            # Every time score % 5 == 0, speed up pipes by 1.2×
            if score % 5 == 0:
                pipe_module.PIPE_SPEED *= 1.2

            for genome in ge:
                genome.fitness += 5.0  # reward for passing a pipe
            pipes.append(Pipe(WIN_WIDTH + 50))

        for r in removed:
            pipes.remove(r)

        # Collision & off-screen checks
        birds_to_remove = set()
        for idx, bird_obj in enumerate(birds):
            if bird_obj.y + bird_obj.img.get_height() >= WIN_HEIGHT or bird_obj.y < 0:
                ge[idx].fitness -= 1.0
                birds_to_remove.add(idx)
                continue
            for p in pipes:
                if p.collide(bird_obj):
                    ge[idx].fitness -= 1.0
                    birds_to_remove.add(idx)
                    break

        # Remove all dead birds in descending index order
        if birds_to_remove:
            for idx in sorted(birds_to_remove, reverse=True):
                birds.pop(idx)
                nets.pop(idx)
                ge.pop(idx)

        draw_window(birds, pipes, score, generation)

    eval_genomes.generation += 1

def run_neat(config_path):
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path,
    )
    pop = neat.Population(config)
    pop.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)

    eval_genomes.generation = 1
    winner = pop.run(eval_genomes, 50)

    # Save the best genome
    with open("best_flappy_genome.pkl", "wb") as f:
        import pickle
        pickle.dump(winner, f)

    print("\nBest genome saved as best_flappy_genome.pkl")

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    run_neat(config_path)
# This script sets up a NEAT-based Flappy Bird game where the pipe speed increases every 5 points.
# It initializes the game window, loads assets, and defines the main game loop for evaluating genomes.
