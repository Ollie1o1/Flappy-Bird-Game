import pygame

# We'll assign BIRD_IMG after display initialization in main.py
BIRD_IMG = None

class Bird:
    MAX_ROTATION  = 25
    ROT_VEL       = 20
    GRAVITY       = 3
    FLAP_STRENGTH = -10.5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = y
        self.img = BIRD_IMG

    def flap(self):
        self.vel = self.FLAP_STRENGTH
        self.tick_count = 0
        self.height = self.y

    def move(self):
        self.tick_count += 1
        disp = self.vel * self.tick_count + 0.5 * self.GRAVITY * (self.tick_count ** 2)
        if disp >= 16:
            disp = 16
        if disp < 0:
            disp -= 2
        self.y += disp

        if disp < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL

    def draw(self, win):
        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(
            center=self.img.get_rect(topleft=(self.x, self.y)).center
        )
        win.blit(rotated_image, new_rect.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)
