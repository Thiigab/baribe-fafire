import pygame
import random

class Particle:

    def __init__(self, x, y):
        # --- Positions ---
        self.x = x
        self.y = y

        # --- vel_x ---
        self.velocity_x = random.uniform(-0.5, 0.5)
        self.velocity_y = random.uniform(-1.5, -0.5)

        self.size = random.randint(2,5)

        self.life = random.randint(40,65)

    # ----------------------
    # UPDATE
    # ----------------------    
    def update(self):

        self.x += self.velocity_x
        self.y += self.velocity_y

        self.size *= 0.98

        self.life -= 1

    # ----------------------
    # DRAW
    # ----------------------
    def draw(self, screen):

        pygame.draw.circle(
            screen,
            (200,220,255),
            (int(self.x), int(self.y)),
            self.size
        )