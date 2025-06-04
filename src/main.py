import pygame
import sys
import bird
import pipe

# Initialize pygame and set up the display first
pygame.init()
WIN_WIDTH, WIN_HEIGHT = 600, 800
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Flappy Bird (No Base)")

# ---- LOAD & RESIZE ASSETS AFTER DISPLAY IS READY ----

# 1) BACKGROUND (bg.png) → scale to exactly (600 × 800)
orig_bg = pygame.image.load("assets/bg.png")
BG_IMG = pygame.transform.scale(orig_bg, (WIN_WIDTH, WIN_HEIGHT))

# 2) BIRD (bird.png) → scale to (50 × 35)
orig_bird = pygame.image.load("assets/bird.png").convert_alpha()
BIRD_WIDTH, BIRD_HEIGHT = 130, 110
scaled_bird = pygame.transform.scale(orig_bird, (BIRD_WIDTH, BIRD_HEIGHT))
bird.BIRD_IMG = scaled_bird  # inject into bird module

# 3) PIPE (pipe.png) → scale to (80 × 500)
orig_pipe = pygame.image.load("assets/pipe.png").convert_alpha()
PIPE_W, PIPE_H = 250, 500
scaled_pipe = pygame.transform.scale(orig_pipe, (PIPE_W, PIPE_H))
pipe.PIPE_IMG = scaled_pipe  # inject into pipe module

# Assign flipped top/bottom to the Pipe class
pipe.Pipe.PIPE_TOP = pygame.transform.flip(scaled_pipe, False, True)
pipe.Pipe.PIPE_BOTTOM = scaled_pipe

# Font for score display
STAT_FONT = pygame.font.SysFont("comicsans", 50)

def draw_window(bird_obj, pipes, score):
    # 1) Draw background
    WIN.blit(BG_IMG, (0, 0))

    # 2) Draw pipes
    for p in pipes:
        p.draw(WIN)

    # 3) Draw bird
    bird_obj.draw(WIN)

    # 4) Draw score in the top-right corner
    score_text = STAT_FONT.render(f"Score: {score}", True, (255, 255, 255))
    WIN.blit(score_text, (WIN_WIDTH - score_text.get_width() - 10, 10))

    pygame.display.update()

def main():
    bird_obj = bird.Bird(230, 350)
    pipes = [pipe.Pipe(700)]
    clock = pygame.time.Clock()
    score = 0
    run = True

    while run:
        clock.tick(30)  # 30 FPS

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
                run = False

            if not p.passed and p.x < bird_obj.x:
                p.passed = True
                add_pipe = True

            if p.x + PIPE_W < 0:
                rem.append(p)

        if add_pipe:
            score += 1
            pipes.append(pipe.Pipe(WIN_WIDTH + 50))

        for r in rem:
            pipes.remove(r)

        # Check if bird flies off the bottom or top of the window
        if bird_obj.y + bird_obj.img.get_height() >= WIN_HEIGHT or bird_obj.y < 0:
            run = False

        draw_window(bird_obj, pipes, score)

    # Restart the game loop once run is False
    main()

if __name__ == "__main__":
    main()
