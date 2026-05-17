import pygame
import random
import math


class OxygenBubble:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y

        self.base_x = x
        self.base_y = y

        self.image = image
        self.rect = self.image.get_rect(center=(self.x, self.y))

        self.float_timer = random.uniform(0, 100)
        self.float_speed = random.uniform(0.025, 0.045)
        self.float_range = random.randint(4, 10)

    def update(self):
        self.float_timer += self.float_speed

        self.x = self.base_x + math.sin(self.float_timer) * self.float_range
        self.y = self.base_y + math.cos(self.float_timer * 0.7) * 2

        self.rect.center = (int(self.x), int(self.y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def is_off_screen(self):
        return False