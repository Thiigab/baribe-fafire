import pygame
import random

class Particle:

    def __init__(self, x, y, from_player=False):
        self.x = x
        self.y = y

        if from_player:
            self.velocity_x = random.uniform(-0.3, 0.3)
            self.velocity_y = random.uniform(-2.2, -1.2)
            self.size = random.randint(3, 7)
            self.life = random.randint(45, 80)
        else:
            self.velocity_x = random.uniform(-0.5, 0.5)
            self.velocity_y = random.uniform(-1.5, -0.5)
            self.size = random.randint(2, 5)
            self.life = random.randint(40, 65)

    # ----------------------
    # UPDATE
    # ----------------------    
    def update(self):

        self.x += self.velocity_x + random.uniform(-0.15, 0.15)
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