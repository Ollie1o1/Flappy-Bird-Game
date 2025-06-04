import pygame
import sys
import src.pipe as pipe_module
import src.bird as bird_module

# Initialize pygame and display
pygame.init()
WIN_WIDTH, WIN_HEIGHT = 600, 800
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Flappy Bird (Speed-Up Every 5 Points)")

# ---- LOAD & RESIZE ASSETS (same as before) ----

# Background (600×800)
orig_bg = pygame.image.load("assets/bg.png")
BG_IMG = pygame.transform.scale(orig_bg, (WIN_WIDTH, WIN_HEIGHT))

# Bird (50×35)
orig_bird = pygame.image.load("assets/bird.png").convert_alpha()
scaled_bird = pygame.transform.scale(orig_bird, (110, 95))
bird_module.BIRD_IMG = scaled_bird

# Pipe (80×500)
orig_pipe = pygame.image.load("assets/pipe.png").convert_alpha()
scaled_pipe = pygame.transform.scale(orig_pipe, (250, 500))
pipe_module.PIPE_IMG = scaled_pipe
pipe_module.Pipe.PIPE_TOP = pygame.transform.flip(scaled_pipe, False, True)
pipe_module.Pipe.PIPE_BOTTOM = scaled_pipe

STAT_FONT = pygame.font.SysFont("comicsans", 50)

def draw_window(bird_obj, pipes, score):
    WIN.blit(BG_IMG, (0, 0))
    for p in pipes:
        p.draw(WIN)
    bird_obj.draw(WIN)
    # Draw score in top-right
    score_text = STAT_FONT.render(f"Score: {score}", True, (255, 255, 255))
    WIN.blit(score_text, (WIN_WIDTH - score_text.get_width() - 10, 10))
    pygame.display.update()

def main():
    bird_obj = bird_module.Bird(230, 350)
    pipes = [pipe_module.Pipe(700)]
    clock = pygame.time.Clock()
    score = 0
    run = True

    # If you want to reset PIPE_SPEED whenever the game restarts:
    pipe_module.PIPE_SPEED = 5

    while run:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird_obj.flap()

        bird_obj.move()

        rem = []
        add_pipe = False

        for p in pipes:
            p.move()
            if p.collide(bird_obj):
                run = False  # end this game

            if not p.passed and p.x < bird_obj.x:
                p.passed = True
                add_pipe = True

            if p.x + p.PIPE_TOP.get_width() < 0:
                rem.append(p)

        if add_pipe:
            score += 1

            # EVERY time score hits a multiple of 5, multiply speed by 1.2
            if score % 5 == 0:
                pipe_module.PIPE_SPEED *= 1.2

            pipes.append(pipe_module.Pipe(WIN_WIDTH + 50))

        for r in rem:
            pipes.remove(r)

        # If bird goes off-screen top or bottom, end game
        if bird_obj.y + bird_obj.img.get_height() >= WIN_HEIGHT or bird_obj.y < 0:
            run = False

        draw_window(bird_obj, pipes, score)

    # Restart the game after a crash
    main()

if __name__ == "__main__":
    main()
