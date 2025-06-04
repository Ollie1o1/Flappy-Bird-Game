import pygame
import random

# We'll assign PIPE_IMG (and flipped versions) after display initialization in main.py
PIPE_IMG = None

GAP = 200
VEL = 5

class Pipe:
    def __init__(self, x):
        self.x = x
        self.height = 0
        self.top = 0
        self.bottom = 0

        # We do NOT set these to None here; they will resolve to the class attributes
        # that we inject in main.py (pipe.Pipe.PIPE_TOP / PIPE_BOTTOM).
        # self.PIPE_TOP = None    ← Remove these lines
        # self.PIPE_BOTTOM = None  ← Remove these lines

        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50, 450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + GAP

    def move(self):
        self.x -= VEL

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
