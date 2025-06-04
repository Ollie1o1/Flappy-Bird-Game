import pygame
import random

# We'll inject PIPE_IMG and flipped variants from main/train later
PIPE_IMG = None

# Start with a base speed of 5; we’ll scale this dynamically
PIPE_SPEED = 5

GAP = 200

class Pipe:
    def __init__(self, x):
        self.x = x
        self.height = 0
        self.top = 0
        self.bottom = 0
        # These get assigned in main.py / train.py:
        #   Pipe.PIPE_TOP = ...
        #   Pipe.PIPE_BOTTOM = ...
        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50, 450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + GAP

    def move(self):
        # Use the global PIPE_SPEED instead of a fixed VEL
        self.x -= PIPE_SPEED

    def draw(self, win):
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        return (
            bird_mask.overlap(top_mask, top_offset)
            or bird_mask.overlap(bottom_mask, bottom_offset)
        )
